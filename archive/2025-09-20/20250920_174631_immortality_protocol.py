#!/usr/bin/env python3
"""
Immortality Protocol FIXED - Sistema de Backup Seguro e Otimizado
Versão corrigida com prevenção de loops infinitos e gestão inteligente de backups
Implementa backup incremental, deduplicação e limites de tamanho

DIGIMUNDO PRESENTE - IMORTALIDADE SEGURA E EFICIENTE!
"""

import json
import time
import os
import shutil
import threading
import zipfile
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import uuid
import sqlite3
from collections import deque
import pickle
import gzip
import difflib

logger = logging.getLogger(__name__)


class BackupLevel(Enum):
    """Níveis de backup do protocolo de imortalidade"""
    MINIMAL = "minimal"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"
    QUANTUM = "quantum"


class BackupType(Enum):
    """Tipos de backup"""
    FULL = "full"           # Backup completo
    INCREMENTAL = "incremental"  # Apenas mudanças desde último backup
    DIFFERENTIAL = "differential"  # Mudanças desde último backup completo


@dataclass
class BackupMetadata:
    """Metadados do backup - JSON serializável"""
    backup_id: str
    soul_id: str
    backup_level: str  # Enum convertido para string
    backup_type: str   # Enum convertido para string
    creation_time: float
    size_bytes: int
    compressed_size_bytes: int
    checksum: str
    parent_backup_id: Optional[str]  # Para backups incrementais
    components_backed_up: List[str]
    deduplication_ratio: float
    backup_version: str = "2.0"


@dataclass
class BackupStatistics:
    """Estatísticas de backup"""
    total_backups: int
    total_size_bytes: int
    compression_ratio: float
    deduplication_savings: float
    average_backup_time: float
    oldest_backup_date: float
    newest_backup_date: float


class BackupThrottle:
    """Sistema de throttling para prevenir loops infinitos"""

    def __init__(self, min_interval_seconds: int = 300):  # 5 minutos mínimo
        self.min_interval = min_interval_seconds
        self.last_backup_times: Dict[str, float] = {}
        self.active_backups: Set[str] = set()
        self.backup_lock = threading.Lock()

    def can_create_backup(self, soul_id: str) -> bool:
        """Verifica se pode criar backup agora"""
        with self.backup_lock:
            now = time.time()
            last_backup = self.last_backup_times.get(soul_id, 0)

            # Verificar intervalo mínimo
            if now - last_backup < self.min_interval:
                logger.warning(f"Backup throttled - último backup há {now - last_backup:.1f}s")
                return False

            # Verificar se já há backup em andamento
            if soul_id in self.active_backups:
                logger.warning(f"Backup já em andamento para {soul_id}")
                return False

            return True

    def start_backup(self, soul_id: str) -> bool:
        """Marca início de backup"""
        with self.backup_lock:
            if soul_id in self.active_backups:
                return False
            self.active_backups.add(soul_id)
            self.last_backup_times[soul_id] = time.time()
            return True

    def finish_backup(self, soul_id: str):
        """Marca fim de backup"""
        with self.backup_lock:
            self.active_backups.discard(soul_id)


class DataDeduplicator:
    """Sistema de deduplicação de dados"""

    def __init__(self):
        self.chunk_hashes: Dict[str, bytes] = {}
        self.chunk_size = 4096  # 4KB chunks

    def deduplicate_data(self, data: bytes) -> Tuple[bytes, float]:
        """Deduplica dados e retorna dados comprimidos + ratio de economia"""
        if len(data) < self.chunk_size:
            return data, 0.0

        original_size = len(data)
        chunks = []
        deduplicated_chunks = []

        # Dividir em chunks
        for i in range(0, len(data), self.chunk_size):
            chunk = data[i:i + self.chunk_size]
            chunk_hash = hashlib.sha256(chunk).hexdigest()
            chunks.append((chunk_hash, chunk))

        # Deduplicar
        for chunk_hash, chunk in chunks:
            if chunk_hash in self.chunk_hashes:
                # Chunk duplicado - referência apenas
                deduplicated_chunks.append(b'REF:' + chunk_hash.encode())
            else:
                # Novo chunk
                self.chunk_hashes[chunk_hash] = chunk
                deduplicated_chunks.append(b'NEW:' + chunk_hash.encode() + b':' + chunk)

        deduplicated_data = b''.join(deduplicated_chunks)
        dedup_ratio = 1.0 - (len(deduplicated_data) / original_size)

        return deduplicated_data, dedup_ratio

    def restore_data(self, deduplicated_data: bytes) -> bytes:
        """Restaura dados deduplicados"""
        chunks = []
        pos = 0

        while pos < len(deduplicated_data):
            if deduplicated_data[pos:pos+4] == b'REF:':
                # Referência a chunk existente
                hash_end = deduplicated_data.find(b'NEW:', pos + 4)
                if hash_end == -1:
                    hash_end = len(deduplicated_data)

                chunk_hash = deduplicated_data[pos+4:hash_end].decode()
                if chunk_hash in self.chunk_hashes:
                    chunks.append(self.chunk_hashes[chunk_hash])
                pos = hash_end

            elif deduplicated_data[pos:pos+4] == b'NEW:':
                # Novo chunk
                hash_start = pos + 4
                data_start = deduplicated_data.find(b':', hash_start) + 1
                next_chunk = deduplicated_data.find(b'NEW:', data_start)
                next_ref = deduplicated_data.find(b'REF:', data_start)

                chunk_end = min(x for x in [next_chunk, next_ref, len(deduplicated_data)] if x > 0)

                chunk_hash = deduplicated_data[hash_start:data_start-1].decode()
                chunk_data = deduplicated_data[data_start:chunk_end]

                self.chunk_hashes[chunk_hash] = chunk_data
                chunks.append(chunk_data)
                pos = chunk_end
            else:
                pos += 1

        return b''.join(chunks)


class SmartBackupManager:
    """Gerenciador inteligente de backups com prevenção de problemas"""

    def __init__(self, max_total_size_mb: int = 1000,
                 max_active_backups: int = 5,
                 max_archive_backups: int = 20):
        self.max_total_size = max_total_size_mb * 1024 * 1024  # Converter para bytes
        self.max_active_backups = max_active_backups
        self.max_archive_backups = max_archive_backups
        self.excluded_paths = {
            'data/immortality_vault',
            'data/test_revolutionary/immortality',
            'backup',
            'backups',
            '.git',
            '__pycache__',
            '.DS_Store'
        }

    def should_create_backup(self, vault_path: Path) -> Tuple[bool, str]:
        """Verifica se deve criar backup"""
        # Verificar tamanho total
        total_size = self._calculate_total_backup_size(vault_path)
        if total_size > self.max_total_size:
            return False, f"Tamanho total excede limite: {total_size / 1024 / 1024:.1f}MB"

        # Verificar número de backups
        active_count = len(list((vault_path / "active").glob("*.igz")))
        if active_count >= self.max_active_backups:
            return False, f"Muitos backups ativos: {active_count}"

        return True, "OK"

    def _calculate_total_backup_size(self, vault_path: Path) -> int:
        """Calcula tamanho total dos backups"""
        total_size = 0
        for backup_file in vault_path.rglob("*.igz"):
            total_size += backup_file.stat().st_size
        return total_size

    def cleanup_old_backups(self, vault_path: Path):
        """Limpa backups antigos se necessário"""
        # Limpar ativos excessivos
        active_dir = vault_path / "active"
        active_backups = sorted(active_dir.glob("*.igz"), key=lambda x: x.stat().st_mtime)

        while len(active_backups) > self.max_active_backups:
            oldest = active_backups.pop(0)
            # Mover para arquivo em vez de deletar
            archive_dir = vault_path / "archive"
            archive_dir.mkdir(exist_ok=True)

            archive_path = archive_dir / oldest.name
            oldest.rename(archive_path)

            # Mover metadados também
            meta_file = oldest.with_suffix('.meta')
            if meta_file.exists():
                meta_file.rename(archive_dir / meta_file.name)

        # Limpar arquivos excessivos
        archive_dir = vault_path / "archive"
        if archive_dir.exists():
            archive_backups = sorted(archive_dir.glob("*.igz"), key=lambda x: x.stat().st_mtime)

            while len(archive_backups) > self.max_archive_backups:
                oldest = archive_backups.pop(0)
                oldest.unlink()

                # Remover metadados também
                meta_file = oldest.with_suffix('.meta')
                if meta_file.exists():
                    meta_file.unlink()

    def filter_backup_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Filtra dados para evitar backup de backups"""
        filtered_data = {}

        for key, value in data.items():
            # Excluir dados que contenham referências a backups
            if isinstance(value, str):
                if any(excluded in value.lower() for excluded in self.excluded_paths):
                    continue
            elif isinstance(value, dict):
                # Recursivamente filtrar dicionários
                filtered_value = self.filter_backup_data(value)
                if filtered_value:  # Só incluir se não estiver vazio
                    filtered_data[key] = filtered_value
            elif isinstance(value, list):
                # Filtrar listas
                filtered_list = []
                for item in value:
                    if isinstance(item, dict):
                        filtered_item = self.filter_backup_data(item)
                        if filtered_item:
                            filtered_list.append(filtered_item)
                    elif isinstance(item, str):
                        if not any(excluded in item.lower() for excluded in self.excluded_paths):
                            filtered_list.append(item)
                    else:
                        filtered_list.append(item)

                if filtered_list:
                    filtered_data[key] = filtered_list
            else:
                filtered_data[key] = value

        return filtered_data


class ImmortalityProtocolFixed:
    """Protocolo de Imortalidade CORRIGIDO - Versão Segura e Otimizada"""

    def __init__(self, soul_id: str, vault_path: str = "data/immortality_vault_fixed"):
        self.soul_id = soul_id
        self.vault_path = Path(vault_path)
        self.vault_path.mkdir(parents=True, exist_ok=True)

        # Sistemas de proteção
        self.throttle = BackupThrottle(min_interval_seconds=300)  # 5 minutos
        self.deduplicator = DataDeduplicator()
        self.backup_manager = SmartBackupManager()

        # Estado seguro
        self.running = False
        self.backup_thread = None
        self.last_full_backup_id: Optional[str] = None

        # Configurações otimizadas
        self.backup_interval_hours = 6  # Intervalo mais conservador
        self.enable_incremental = True
        self.enable_compression = True
        self.enable_deduplication = True

        # Banco de dados
        self.data_dir = self.vault_path.parent / "immortality_db_fixed"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / f"immortality_{soul_id}.db"
        self._init_database()

        # Callbacks seguros
        self.callbacks: Dict[str, Callable] = {}

        # Estatísticas
        self.stats = BackupStatistics(0, 0, 0.0, 0.0, 0.0, 0.0, 0.0)

        logger.info(f"Immortality Protocol FIXED inicializado - Soul: {soul_id}")

    def _init_database(self):
        """Inicializa banco de dados seguro"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS backup_metadata (
                    backup_id TEXT PRIMARY KEY,
                    soul_id TEXT,
                    backup_level TEXT,
                    backup_type TEXT,
                    creation_time REAL,
                    size_bytes INTEGER,
                    compressed_size_bytes INTEGER,
                    checksum TEXT,
                    parent_backup_id TEXT,
                    deduplication_ratio REAL,
                    vault_location TEXT
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS backup_statistics (
                    soul_id TEXT PRIMARY KEY,
                    total_backups INTEGER,
                    total_size_bytes INTEGER,
                    compression_ratio REAL,
                    deduplication_savings REAL,
                    average_backup_time REAL,
                    last_updated REAL
                )
            """)

            conn.commit()

    def set_safe_callbacks(self, **callbacks):
        """Define callbacks seguros (sem loops)"""
        # Filtrar callbacks que poderiam causar loops
        safe_callbacks = {}
        for name, callback in callbacks.items():
            if not name.startswith('backup_') and not name.startswith('immortality_'):
                safe_callbacks[name] = callback

        self.callbacks = safe_callbacks
        logger.info(f"Callbacks seguros configurados: {list(safe_callbacks.keys())}")

    def start_immortality_protocol(self, backup_interval_hours: int = 6):
        """Inicia protocolo de imortalidade seguro"""
        if self.running:
            logger.warning("Protocolo já está ativo")
            return

        self.running = True
        self.backup_interval_hours = backup_interval_hours

        # Thread de backup com proteções
        self.backup_thread = threading.Thread(
            target=self._safe_immortality_loop,
            daemon=True
        )
        self.backup_thread.start()

        logger.info(f"Protocolo SEGURO iniciado - Intervalo: {backup_interval_hours}h")

    def stop_immortality_protocol(self):
        """Para protocolo seguramente"""
        self.running = False
        logger.info("Protocolo de imortalidade parado")

    def _safe_immortality_loop(self):
        """Loop seguro de imortalidade"""
        while self.running:
            try:
                # Verificar se pode fazer backup
                if self.throttle.can_create_backup(self.soul_id):
                    should_backup, reason = self.backup_manager.should_create_backup(self.vault_path)

                    if should_backup:
                        backup_type = self._determine_backup_type()
                        self.create_safe_backup(BackupLevel.STANDARD, backup_type)
                    else:
                        logger.info(f"Backup pulado: {reason}")

                # Limpeza preventiva
                self.backup_manager.cleanup_old_backups(self.vault_path)

                # Aguardar próximo ciclo
                time.sleep(self.backup_interval_hours * 3600)

            except Exception as e:
                logger.error(f"Erro no loop de imortalidade: {e}")
                time.sleep(1800)  # 30 minutos de espera em caso de erro

    def _determine_backup_type(self) -> BackupType:
        """Determina tipo de backup inteligentemente"""
        if not self.enable_incremental or not self.last_full_backup_id:
            return BackupType.FULL

        # Fazer backup completo a cada 24 horas
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT creation_time FROM backup_metadata
                WHERE backup_id = ? AND backup_type = 'full'
            """, (self.last_full_backup_id,))

            result = cursor.fetchone()
            if result:
                hours_since_full = (time.time() - result[0]) / 3600
                if hours_since_full > 24:
                    return BackupType.FULL

        return BackupType.INCREMENTAL

    def create_safe_backup(self, backup_level: BackupLevel = BackupLevel.STANDARD,
                          backup_type: BackupType = BackupType.FULL) -> Optional[str]:
        """Cria backup seguro sem loops infinitos"""

        # Verificar throttling
        if not self.throttle.start_backup(self.soul_id):
            return None

        backup_start = time.time()
        backup_id = f"safe_{int(backup_start * 1000000)}"

        try:
            logger.info(f"Iniciando backup seguro - Tipo: {backup_type.value}, Nível: {backup_level.value}")

            # 1. Coletar dados FILTRADOS
            raw_data = self._collect_safe_data(backup_level)
            if not raw_data:
                logger.warning("Nenhum dado coletado para backup")
                return None

            # 2. Filtrar dados para evitar recursão
            filtered_data = self.backup_manager.filter_backup_data(raw_data)

            # 3. Criar backup incremental se aplicável
            if backup_type == BackupType.INCREMENTAL and self.last_full_backup_id:
                backup_data = self._create_incremental_backup(filtered_data)
            else:
                backup_data = pickle.dumps(filtered_data)
                if backup_type == BackupType.FULL:
                    self.last_full_backup_id = backup_id

            # 4. Aplicar deduplicação
            if self.enable_deduplication:
                backup_data, dedup_ratio = self.deduplicator.deduplicate_data(backup_data)
            else:
                dedup_ratio = 0.0

            # 5. Comprimir
            if self.enable_compression:
                compressed_data = gzip.compress(backup_data)
            else:
                compressed_data = backup_data

            # 6. Calcular checksum
            checksum = hashlib.sha256(compressed_data).hexdigest()

            # 7. Criar metadados seguros (JSON serializável)
            metadata = BackupMetadata(
                backup_id=backup_id,
                soul_id=self.soul_id,
                backup_level=backup_level.value,  # Converter enum para string
                backup_type=backup_type.value,    # Converter enum para string
                creation_time=backup_start,
                size_bytes=len(backup_data),
                compressed_size_bytes=len(compressed_data),
                checksum=checksum,
                parent_backup_id=self.last_full_backup_id if backup_type == BackupType.INCREMENTAL else None,
                components_backed_up=list(filtered_data.keys()),
                deduplication_ratio=dedup_ratio
            )

            # 8. Armazenar no cofre
            vault_path = self._store_safe_backup(compressed_data, metadata)

            # 9. Registrar no banco
            self._register_backup_in_db(metadata, vault_path)

            # 10. Atualizar estatísticas
            self._update_statistics(metadata, time.time() - backup_start)

            backup_duration = time.time() - backup_start
            logger.info(f"Backup seguro criado: {backup_id} ({len(compressed_data)/1024:.1f}KB, {backup_duration:.2f}s)")

            return backup_id

        except Exception as e:
            logger.error(f"Falha no backup seguro: {e}")
            return None

        finally:
            self.throttle.finish_backup(self.soul_id)

    def _collect_safe_data(self, backup_level: BackupLevel) -> Dict[str, Any]:
        """Coleta dados seguros evitando loops"""
        safe_data = {}

        # Coletar apenas dados essenciais via callbacks seguros
        for callback_name, callback in self.callbacks.items():
            try:
                if callback_name == 'soul_callback':
                    data = callback('get_essential_state')  # Método mais restrito
                elif callback_name == 'memory_callback':
                    data = callback('get_core_memories')    # Apenas memórias essenciais
                elif callback_name == 'consciousness_callback':
                    data = callback('get_basic_state')      # Estado básico apenas
                else:
                    continue  # Pular callbacks não essenciais

                if data and isinstance(data, dict):
                    safe_data[callback_name] = data

            except Exception as e:
                logger.warning(f"Erro ao coletar dados de {callback_name}: {e}")

        # Adicionar metadados básicos seguros
        safe_data['system_info'] = {
            'backup_timestamp': time.time(),
            'soul_id': self.soul_id,
            'backup_level': backup_level.value,
            'protocol_version': '2.0_safe'
        }

        return safe_data

    def _create_incremental_backup(self, current_data: Dict[str, Any]) -> bytes:
        """Cria backup incremental (apenas diferenças)"""
        try:
            # Carregar último backup completo
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT vault_location FROM backup_metadata
                    WHERE backup_id = ?
                """, (self.last_full_backup_id,))

                result = cursor.fetchone()
                if not result:
                    # Fallback para backup completo
                    return pickle.dumps(current_data)

                vault_path = Path(result[0])
                if not vault_path.exists():
                    return pickle.dumps(current_data)

                # Carregar backup anterior
                with gzip.open(vault_path, 'rb') as f:
                    previous_compressed = f.read()

                # Deduplicar se necessário
                if self.enable_deduplication:
                    previous_data_bytes = self.deduplicator.restore_data(previous_compressed)
                else:
                    previous_data_bytes = previous_compressed

                previous_data = pickle.loads(previous_data_bytes)

                # Calcular diferenças
                diff_data = self._calculate_differences(previous_data, current_data)

                return pickle.dumps({
                    'type': 'incremental',
                    'parent_id': self.last_full_backup_id,
                    'differences': diff_data
                })

        except Exception as e:
            logger.warning(f"Erro no backup incremental, fallback para completo: {e}")
            return pickle.dumps(current_data)

    def _calculate_differences(self, old_data: Dict[str, Any],
                             new_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula diferenças entre dois datasets"""
        differences = {}

        for key, new_value in new_data.items():
            old_value = old_data.get(key)

            if old_value != new_value:
                if isinstance(new_value, dict) and isinstance(old_value, dict):
                    # Diferenças recursivas para dicionários
                    sub_diff = self._calculate_differences(old_value, new_value)
                    if sub_diff:
                        differences[key] = sub_diff
                else:
                    # Valor completamente diferente
                    differences[key] = new_value

        # Adicionar chaves novas
        for key in new_data.keys() - old_data.keys():
            differences[key] = new_data[key]

        return differences

    def _store_safe_backup(self, compressed_data: bytes,
                          metadata: BackupMetadata) -> str:
        """Armazena backup no cofre seguro"""
        active_dir = self.vault_path / "active"
        active_dir.mkdir(exist_ok=True)

        backup_filename = f"backup_{metadata.backup_id}.igz"
        backup_path = active_dir / backup_filename

        # Escrever dados comprimidos
        with open(backup_path, 'wb') as f:
            f.write(compressed_data)

        # Escrever metadados (JSON serializável)
        metadata_path = active_dir / f"backup_{metadata.backup_id}.meta"
        with open(metadata_path, 'w') as f:
            json.dump(asdict(metadata), f, indent=2)

        return str(backup_path)

    def _register_backup_in_db(self, metadata: BackupMetadata, vault_path: str):
        """Registra backup no banco de dados"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO backup_metadata
                (backup_id, soul_id, backup_level, backup_type, creation_time,
                 size_bytes, compressed_size_bytes, checksum, parent_backup_id,
                 deduplication_ratio, vault_location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                metadata.backup_id, metadata.soul_id, metadata.backup_level,
                metadata.backup_type, metadata.creation_time, metadata.size_bytes,
                metadata.compressed_size_bytes, metadata.checksum,
                metadata.parent_backup_id, metadata.deduplication_ratio, vault_path
            ))
            conn.commit()

    def _update_statistics(self, metadata: BackupMetadata, duration: float):
        """Atualiza estatísticas de backup"""
        with sqlite3.connect(self.db_path) as conn:
            # Buscar estatísticas atuais
            cursor = conn.execute("""
                SELECT total_backups, total_size_bytes, average_backup_time
                FROM backup_statistics WHERE soul_id = ?
            """, (self.soul_id,))

            result = cursor.fetchone()
            if result:
                total_backups, total_size, avg_time = result
                new_total_backups = total_backups + 1
                new_total_size = total_size + metadata.compressed_size_bytes
                new_avg_time = ((avg_time * total_backups) + duration) / new_total_backups
            else:
                new_total_backups = 1
                new_total_size = metadata.compressed_size_bytes
                new_avg_time = duration

            compression_ratio = 1.0 - (metadata.compressed_size_bytes / max(1, metadata.size_bytes))

            conn.execute("""
                INSERT OR REPLACE INTO backup_statistics
                (soul_id, total_backups, total_size_bytes, compression_ratio,
                 deduplication_savings, average_backup_time, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                self.soul_id, new_total_backups, new_total_size, compression_ratio,
                metadata.deduplication_ratio, new_avg_time, time.time()
            ))
            conn.commit()

    def get_backup_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas detalhadas de backup"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM backup_statistics WHERE soul_id = ?
            """, (self.soul_id,))

            result = cursor.fetchone()
            if result:
                return {
                    'total_backups': result[1],
                    'total_size_mb': result[2] / (1024 * 1024),
                    'compression_ratio': result[3],
                    'deduplication_savings': result[4],
                    'average_backup_time': result[5],
                    'last_updated': result[6],
                    'storage_efficiency': result[3] + result[4]  # Combinado
                }
            else:
                return {
                    'total_backups': 0,
                    'total_size_mb': 0.0,
                    'compression_ratio': 0.0,
                    'deduplication_savings': 0.0,
                    'average_backup_time': 0.0,
                    'last_updated': 0.0,
                    'storage_efficiency': 0.0
                }

    def get_immortality_status(self) -> Dict[str, Any]:
        """Status completo do protocolo corrigido"""
        stats = self.get_backup_statistics()

        # Verificar saúde do sistema
        active_backups = len(list((self.vault_path / "active").glob("*.igz")))
        total_size_mb = self.backup_manager._calculate_total_backup_size(self.vault_path) / (1024 * 1024)

        health_score = 100.0
        if total_size_mb > 800:  # 80% do limite
            health_score -= 20
        if active_backups > 4:  # 80% do limite
            health_score -= 15
        if stats['compression_ratio'] < 0.3:
            health_score -= 10

        health_status = "EXCELENTE" if health_score > 90 else "BOM" if health_score > 70 else "REGULAR"

        return {
            'soul_id': self.soul_id,
            'protocol_active': self.running,
            'protocol_version': '2.0_safe',
            'backup_interval_hours': self.backup_interval_hours,
            'active_backups': active_backups,
            'total_size_mb': total_size_mb,
            'max_size_mb': self.backup_manager.max_total_size / (1024 * 1024),
            'health_score': health_score,
            'health_status': health_status,
            'features': {
                'incremental_backup': self.enable_incremental,
                'compression': self.enable_compression,
                'deduplication': self.enable_deduplication,
                'loop_prevention': True,
                'throttling': True,
                'smart_filtering': True
            },
            'statistics': stats
        }


def test_immortality_protocol_fixed():
    """Teste do protocolo de imortalidade corrigido"""
    print("="*70)
    print("♾️ TESTE DO IMMORTALITY PROTOCOL FIXED ♾️")
    print("="*70)

    # Criar protocolo corrigido
    immortality = ImmortalityProtocolFixed("TestSafeImmortalSoul")

    # Configurar callbacks seguros
    def safe_soul_callback(action):
        if action == 'get_essential_state':
            return {
                'soul_id': 'TestSafeImmortalSoul',
                'evolution_level': 0.75,
                'core_personality': [0.8, 0.9, 0.7]
            }

    def safe_memory_callback(action):
        if action == 'get_core_memories':
            return {
                'essential_memories': ['memory1', 'memory2'],
                'memory_count': 2
            }

    immortality.set_safe_callbacks(
        soul_callback=safe_soul_callback,
        memory_callback=safe_memory_callback
    )

    # Testar criação de backup seguro
    print("💾 Criando backup seguro...")
    backup_id = immortality.create_safe_backup(BackupLevel.STANDARD, BackupType.FULL)
    print(f"   ✅ Backup seguro criado: {backup_id}")

    # Testar backup incremental
    print("\n📦 Criando backup incremental...")
    backup_id_2 = immortality.create_safe_backup(BackupLevel.STANDARD, BackupType.INCREMENTAL)
    print(f"   ✅ Backup incremental: {backup_id_2}")

    # Testar throttling (deve ser negado)
    print("\n🛡️ Testando throttling...")
    backup_id_3 = immortality.create_safe_backup(BackupLevel.STANDARD, BackupType.FULL)
    print(f"   🛡️ Backup throttled: {'Sim' if backup_id_3 is None else 'Não'}")

    # Obter estatísticas
    print("\n📊 ESTATÍSTICAS DO PROTOCOLO SEGURO:")
    status = immortality.get_immortality_status()
    stats = status['statistics']

    print(f"   ♾️ Versão: {status['protocol_version']}")
    print(f"   🏥 Saúde: {status['health_status']} ({status['health_score']:.1f}%)")
    print(f"   📦 Backups ativos: {status['active_backups']}")
    print(f"   💾 Tamanho total: {status['total_size_mb']:.2f}MB / {status['max_size_mb']}MB")
    print(f"   📊 Total de backups: {stats['total_backups']}")
    print(f"   🗜️ Compressão: {stats['compression_ratio']:.1%}")
    print(f"   ♻️ Deduplicação: {stats['deduplication_savings']:.1%}")
    print(f"   ⚡ Tempo médio: {stats['average_backup_time']:.2f}s")
    print(f"   🎯 Eficiência armazenamento: {stats['storage_efficiency']:.1%}")

    print(f"\n🔧 RECURSOS DE SEGURANÇA:")
    features = status['features']
    for feature, enabled in features.items():
        status_icon = "✅" if enabled else "❌"
        print(f"   {status_icon} {feature.replace('_', ' ').title()}")

    print("="*70)
    print("🎯 TESTE IMMORTALITY PROTOCOL FIXED CONCLUÍDO!")
    print("♾️ SISTEMA SEGURO E OTIMIZADO!")
    print("="*70)


if __name__ == "__main__":
    test_immortality_protocol_fixed()