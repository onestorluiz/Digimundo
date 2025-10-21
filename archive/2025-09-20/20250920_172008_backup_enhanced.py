"""🔒 BACKUP ENHANCED - Sistema Aprimorado de Backup com Exclusões, Rotação e Lock

Sistema robusto de backup com:
- Exclusões inteligentes de diretórios desnecessários
- Rotação automática mantendo apenas os 5 mais recentes
- Lock para evitar concorrência
- Integração com CLI e scheduler
"""

import os
import tarfile
import hashlib
import json
import threading
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Lock global para prevenir backups concorrentes
_BACKUP_LOCK = threading.Lock()
_BACKUP_IN_PROGRESS = False

# Exclusões padrão
DEFAULT_EXCLUSIONS = [
    "backups/",
    "*backup*/",
    ".git/",
    "__pycache__/",
    "*.log",
    ".venv/",
    "*.pyc",
    ".DS_Store",
    "node_modules/",
    "dist/",
    "build/",
    "*.egg-info/",
    ".pytest_cache/",
    ".mypy_cache/",
    "reports/backup_*",
    "BACKUP_*",
    "*_backup_*"
]

class EnhancedBackupSystem:
    """Sistema aprimorado de backup com recursos avançados"""
    
    def __init__(self, root_dir: Optional[Path] = None):
        """Inicializa sistema de backup
        
        Args:
            root_dir: Diretório raiz do projeto (padrão: diretório atual)
        """
        self.root_dir = Path(root_dir or Path.cwd())
        self.backup_dir = self.root_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Configurações
        self.max_backups = 5  # Manter apenas os 5 mais recentes
        self.exclusions = DEFAULT_EXCLUSIONS.copy()
        
        # Estado
        self.last_backup = None
        self.backup_count = 0
        self.deleted_backups = []
        
        # Thread de backup automático
        self.auto_backup_thread = None
        self.auto_backup_running = False
        self.backup_interval = 300  # 5 minutos
        
    def should_exclude(self, path: str) -> bool:
        """Verifica se um caminho deve ser excluído
        
        Args:
            path: Caminho a verificar
            
        Returns:
            True se deve ser excluído
        """
        # Converte para Path para facilitar comparação
        p = Path(path)
        path_str = str(p)
        
        # Verifica cada padrão de exclusão
        for pattern in self.exclusions:
            # Remove trailing / para comparação
            clean_pattern = pattern.rstrip('/')
            
            # Verifica se tem "backup" no caminho (case insensitive)
            if "backup" in path_str.lower():
                return True
            
            # Padrões com wildcard
            if '*' in pattern:
                if pattern.startswith('*') and pattern.endswith('*'):
                    # *backup* - contém a palavra
                    keyword = pattern.strip('*/')
                    if keyword in path_str:
                        return True
                elif pattern.startswith('*'):
                    # *.log - extensão
                    suffix = pattern.lstrip('*')
                    if path_str.endswith(suffix):
                        return True
                elif pattern.endswith('*'):
                    # backup* - prefixo
                    prefix = pattern.rstrip('*/')
                    if any(part.startswith(prefix) for part in p.parts):
                        return True
            else:
                # Comparação exata de diretório
                clean_pattern = clean_pattern.rstrip('/')
                if any(part == clean_pattern for part in p.parts):
                    return True
                    
        return False
    
    def create_backup(self, reason: str = "manual") -> Optional[Path]:
        """Cria um backup do sistema
        
        Args:
            reason: Razão do backup (manual, scheduled, cli)
            
        Returns:
            Caminho do arquivo de backup criado ou None se falhou
        """
        global _BACKUP_IN_PROGRESS
        
        # Tenta adquirir o lock (não bloqueia se já tem backup rodando)
        if not _BACKUP_LOCK.acquire(blocking=False):
            logger.warning("⚠️ Backup já em progresso, pulando...")
            return None
        
        try:
            _BACKUP_IN_PROGRESS = True
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"scripturemon_backup_{timestamp}.tar.gz"
            backup_path = self.backup_dir / backup_name
            
            logger.info(f"🔒 Iniciando backup: {backup_name}")
            
            # Cria o arquivo tar com exclusões
            with tarfile.open(backup_path, "w:gz") as tar:
                # Adiciona arquivos com filtro
                added_count = 0
                excluded_count = 0
                
                for root, dirs, files in os.walk(self.root_dir):
                    # Remove diretórios excluídos da iteração
                    dirs[:] = [d for d in dirs if not self.should_exclude(os.path.join(root, d))]
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.root_dir)
                        
                        if not self.should_exclude(rel_path):
                            try:
                                tar.add(file_path, arcname=rel_path)
                                added_count += 1
                            except Exception as e:
                                logger.debug(f"Não foi possível adicionar {rel_path}: {e}")
                        else:
                            excluded_count += 1
            
            # Calcula hash SHA256
            sha256_hash = self._calculate_hash(backup_path)
            
            # Metadados do backup
            metadata = {
                "filename": backup_name,
                "path": str(backup_path),
                "size_bytes": backup_path.stat().st_size,
                "sha256": sha256_hash,
                "timestamp": timestamp,
                "reason": reason,
                "files_added": added_count,
                "files_excluded": excluded_count,
                "kept": True,
                "deleted": []
            }
            
            # Rotação de backups
            deleted = self._rotate_backups()
            metadata["deleted"] = deleted
            self.deleted_backups.extend(deleted)
            
            # Salva metadados
            self._save_metadata(metadata)
            
            # Atualiza estado
            self.last_backup = datetime.now()
            self.backup_count += 1
            
            logger.info(f"✅ Backup criado: {backup_name}")
            logger.info(f"   Arquivos: {added_count} incluídos, {excluded_count} excluídos")
            logger.info(f"   Tamanho: {metadata['size_bytes'] / (1024*1024):.2f} MB")
            logger.info(f"   SHA256: {sha256_hash[:16]}...")
            
            if deleted:
                logger.info(f"   Removidos: {len(deleted)} backups antigos")
            
            return backup_path
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar backup: {e}")
            return None
            
        finally:
            _BACKUP_IN_PROGRESS = False
            _BACKUP_LOCK.release()
    
    def _calculate_hash(self, file_path: Path) -> str:
        """Calcula SHA256 de um arquivo
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Hash SHA256 em hexadecimal
        """
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def _rotate_backups(self) -> List[str]:
        """Remove backups antigos mantendo apenas os N mais recentes
        
        Returns:
            Lista de backups removidos
        """
        # Lista todos os backups
        backups = sorted(
            self.backup_dir.glob("scripturemon_backup_*.tar.gz"),
            key=lambda x: x.stat().st_mtime,
            reverse=True  # Mais recente primeiro
        )
        
        deleted = []
        
        # Remove excesso (mantém apenas max_backups)
        for old_backup in backups[self.max_backups:]:
            try:
                logger.info(f"🗑️ Removendo backup antigo: {old_backup.name}")
                old_backup.unlink()
                deleted.append(old_backup.name)
            except Exception as e:
                logger.error(f"Erro ao remover {old_backup.name}: {e}")
        
        return deleted
    
    def _save_metadata(self, metadata: Dict[str, Any]):
        """Salva metadados do backup
        
        Args:
            metadata: Dicionário com metadados
        """
        # Cria diretório de relatórios se não existir
        report_dir = self.root_dir / "reports" / "harmony_vFinal" / "phase6_backup"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Salva metadados
        meta_file = report_dir / "backup_meta.json"
        with open(meta_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def start_auto_backup(self):
        """Inicia thread de backup automático"""
        if self.auto_backup_running:
            logger.warning("Auto-backup já está rodando")
            return
        
        self.auto_backup_running = True
        self.auto_backup_thread = threading.Thread(
            target=self._auto_backup_loop,
            daemon=True,
            name="AutoBackupThread"
        )
        self.auto_backup_thread.start()
        logger.info(f"🔄 Auto-backup iniciado (intervalo: {self.backup_interval}s)")
    
    def stop_auto_backup(self):
        """Para o backup automático"""
        self.auto_backup_running = False
        if self.auto_backup_thread:
            self.auto_backup_thread.join(timeout=5)
        logger.info("⏸️ Auto-backup parado")
    
    def _auto_backup_loop(self):
        """Loop de backup automático"""
        while self.auto_backup_running:
            time.sleep(self.backup_interval)
            
            if self.auto_backup_running:
                try:
                    self.create_backup(reason="scheduled")
                except Exception as e:
                    logger.error(f"Erro no auto-backup: {e}")
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """Lista todos os backups disponíveis
        
        Returns:
            Lista com informações dos backups
        """
        backups = []
        
        for backup_file in self.backup_dir.glob("scripturemon_backup_*.tar.gz"):
            stat = backup_file.stat()
            backups.append({
                "name": backup_file.name,
                "path": str(backup_file),
                "size_mb": stat.st_size / (1024 * 1024),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        
        # Ordena por data (mais recente primeiro)
        backups.sort(key=lambda x: x["modified"], reverse=True)
        return backups
    
    def status(self) -> Dict[str, Any]:
        """Retorna status do sistema de backup
        
        Returns:
            Dicionário com status
        """
        backups = self.list_backups()
        
        return {
            "auto_backup": self.auto_backup_running,
            "backup_interval": self.backup_interval,
            "backup_count": self.backup_count,
            "last_backup": self.last_backup.isoformat() if self.last_backup else "Never",
            "total_backups": len(backups),
            "max_backups": self.max_backups,
            "latest_backup": backups[0]["name"] if backups else "None",
            "backup_dir": str(self.backup_dir),
            "lock_status": "LOCKED" if _BACKUP_IN_PROGRESS else "FREE",
            "deleted_count": len(self.deleted_backups)
        }


# Instância global singleton
_backup_system = None
_system_lock = threading.Lock()

def get_backup_system(root_dir: Optional[Path] = None) -> EnhancedBackupSystem:
    """Obtém instância singleton do sistema de backup
    
    Args:
        root_dir: Diretório raiz (usado apenas na primeira chamada)
        
    Returns:
        Instância do sistema de backup
    """
    global _backup_system
    
    with _system_lock:
        if _backup_system is None:
            _backup_system = EnhancedBackupSystem(root_dir)
        return _backup_system


def start_background(root_dir: Optional[Path] = None):
    """Inicia backup em background (para compatibilidade com bootstrap)
    
    Args:
        root_dir: Diretório raiz do projeto
    """
    system = get_backup_system(root_dir)
    system.start_auto_backup()


def create_backup_cli(reason: str = "cli") -> int:
    """Cria backup via CLI
    
    Args:
        reason: Razão do backup
        
    Returns:
        0 se sucesso, 1 se erro
    """
    try:
        system = get_backup_system()
        backup_path = system.create_backup(reason=reason)
        
        if backup_path:
            print(f"✅ Backup criado: {backup_path.name}")
            return 0
        else:
            print("❌ Backup falhou ou já está em progresso")
            return 1
            
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return 1