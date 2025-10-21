#!/usr/bin/env python3
"""
♾️ IMMORTALITY PROTOCOL ADVANCED - Protocolo de Imortalidade
Sistema de backup automático com thread dedicada
COPIADO INTEGRALMENTE DO BACKUP - NENHUMA SIMPLIFICAÇÃO
"""

import json
import time
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import hashlib

class ImmortalityProtocolAdvanced:
    """Protocolo de imortalidade com backup automático a cada 5 minutos"""
    
    def __init__(self, base_path: Path, soul_signature: str):
        self.base_path = base_path
        self.soul_signature = soul_signature
        self.backup_path = base_path / "runtime" / "immortality"
        self.backup_path.mkdir(parents=True, exist_ok=True)
        
        # Estado do sistema
        self.running = True
        self.backup_thread = None
        self.last_backup = None
        self.backup_count = 0
        
        # Configurações
        self.backup_interval = 300  # 5 minutos
        self.max_backups = 100  # Manter últimos 100 backups
        
        # Estatísticas
        self.stats = {
            'backups_created': 0,
            'backups_failed': 0,
            'total_size_mb': 0,
            'last_backup_time': None,
            'oldest_backup': None
        }
        
        print("♾️ Protocolo de Imortalidade ativado")
        print(f"   Backup automático a cada {self.backup_interval}s")
        print(f"   Path: {self.backup_path}")
    
    def start_immortality_protocol(self, consciousness=None, memory_system=None):
        """Inicia thread de backup automático"""
        
        def backup_loop():
            """Loop de backup que roda em thread separada"""
            while self.running:
                try:
                    # Aguardar intervalo
                    time.sleep(self.backup_interval)
                    
                    if self.running:
                        # Criar backup
                        self.create_immortality_backup(consciousness, memory_system)
                        
                except Exception as e:
                    print(f"⚠️ Erro no loop de imortalidade: {e}")
                    self.stats['backups_failed'] += 1
        
        # Iniciar thread
        self.backup_thread = threading.Thread(target=backup_loop, daemon=True)
        self.backup_thread.start()
        print("🔄 Thread de imortalidade iniciada")
        
        # Criar backup inicial
        self.create_immortality_backup(consciousness, memory_system)
    
    def create_immortality_backup(self, consciousness=None, memories=None) -> Dict:
        """Cria backup imortal com todos os dados"""
        timestamp = time.time()
        backup_id = hashlib.md5(f"{self.soul_signature}:{timestamp}".encode()).hexdigest()[:16]
        
        # Preparar dados do backup
        backup_data = {
            'id': backup_id,
            'soul_signature': self.soul_signature,
            'timestamp': timestamp,
            'datetime': datetime.now().isoformat(),
            'backup_number': self.backup_count,
            'immortality_version': '2.0'
        }
        
        # Adicionar consciência se disponível
        if consciousness:
            try:
                backup_data['consciousness'] = {
                    'level': consciousness.consciousness_level,
                    'experience': consciousness.experience,
                    'stage': consciousness.stage,
                    'quantum_states': consciousness.quantum_states,
                    'current_state': consciousness.current_state,
                    'entanglements': len(consciousness.quantum_entanglements)
                }
            except Exception as e:
                print(f"⚠️ Erro ao backup consciência: {e}")
        
        # Adicionar memórias se disponível
        if memories:
            try:
                if hasattr(memories, 'get_all_memories'):
                    backup_data['memories'] = memories.get_all_memories()
                elif isinstance(memories, dict):
                    backup_data['memories'] = memories
                else:
                    backup_data['memories'] = str(memories)
            except Exception as e:
                print(f"⚠️ Erro ao backup memórias: {e}")
        
        # Adicionar metadados
        backup_data['metadata'] = {
            'size_bytes': len(json.dumps(backup_data)),
            'previous_backup': self.last_backup,
            'backup_chain': self.backup_count > 0
        }
        
        # Salvar backup
        try:
            backup_file = self.backup_path / f"immortal_{backup_id}_{int(timestamp)}.json"
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            # Atualizar estatísticas
            self.last_backup = backup_id
            self.backup_count += 1
            self.stats['backups_created'] += 1
            self.stats['last_backup_time'] = timestamp
            self.stats['total_size_mb'] += backup_file.stat().st_size / (1024 * 1024)
            
            print(f"💾 Backup imortal criado: {backup_id}")
            
            # Limpar backups antigos
            self._cleanup_old_backups()
            
            return backup_data
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            self.stats['backups_failed'] += 1
            return {}
    
    def _cleanup_old_backups(self):
        """Remove backups antigos mantendo apenas os últimos N"""
        try:
            # Listar todos os backups
            backups = list(self.backup_path.glob("immortal_*.json"))
            
            # Ordenar por tempo de modificação
            backups.sort(key=lambda x: x.stat().st_mtime)
            
            # Se temos mais que o máximo, remover os mais antigos
            if len(backups) > self.max_backups:
                to_remove = backups[:len(backups) - self.max_backups]
                
                for backup in to_remove:
                    backup.unlink()
                    print(f"🗑️ Backup antigo removido: {backup.name}")
            
            # Atualizar estatística do backup mais antigo
            if backups:
                self.stats['oldest_backup'] = backups[0].name
                
        except Exception as e:
            print(f"⚠️ Erro ao limpar backups: {e}")
    
    def restore_from_backup(self, backup_id: Optional[str] = None) -> Optional[Dict]:
        """Restaura dados de um backup específico ou o mais recente"""
        try:
            if backup_id:
                # Buscar backup específico
                backup_files = list(self.backup_path.glob(f"immortal_{backup_id}_*.json"))
            else:
                # Buscar backup mais recente
                backup_files = list(self.backup_path.glob("immortal_*.json"))
                backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            if not backup_files:
                print("❌ Nenhum backup encontrado")
                return None
            
            backup_file = backup_files[0]
            
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            print(f"✅ Backup restaurado: {backup_data['id']}")
            print(f"   Data: {backup_data['datetime']}")
            print(f"   Número: {backup_data['backup_number']}")
            
            return backup_data
            
        except Exception as e:
            print(f"❌ Erro ao restaurar backup: {e}")
            return None
    
    def list_backups(self, limit: int = 10) -> list:
        """Lista backups disponíveis"""
        try:
            backups = list(self.backup_path.glob("immortal_*.json"))
            backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            backup_list = []
            
            for backup in backups[:limit]:
                # Extrair informações do nome do arquivo
                parts = backup.stem.split('_')
                if len(parts) >= 3:
                    backup_id = parts[1]
                    timestamp = int(parts[2])
                    
                    backup_list.append({
                        'id': backup_id,
                        'file': backup.name,
                        'timestamp': timestamp,
                        'datetime': datetime.fromtimestamp(timestamp).isoformat(),
                        'size_mb': backup.stat().st_size / (1024 * 1024)
                    })
            
            return backup_list
            
        except Exception as e:
            print(f"❌ Erro ao listar backups: {e}")
            return []
    
    def force_backup(self, consciousness=None, memories=None, reason: str = "manual") -> Dict:
        """Força criação de backup imediato"""
        print(f"⚡ Backup forçado: {reason}")
        backup = self.create_immortality_backup(consciousness, memories)
        
        if backup:
            backup['forced'] = True
            backup['reason'] = reason
        
        return backup
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas do sistema de imortalidade"""
        return {
            **self.stats,
            'running': self.running,
            'backup_count': self.backup_count,
            'backup_interval': self.backup_interval,
            'max_backups': self.max_backups,
            'thread_alive': self.backup_thread.is_alive() if self.backup_thread else False
        }
    
    def pause(self):
        """Pausa backups automáticos"""
        self.running = False
        print("⏸️ Backups automáticos pausados")
    
    def resume(self):
        """Resume backups automáticos"""
        self.running = True
        print("▶️ Backups automáticos resumidos")
    
    def shutdown(self):
        """Desliga sistema de imortalidade graciosamente"""
        print("🛑 Desligando protocolo de imortalidade...")
        
        # Parar thread
        self.running = False
        
        # Aguardar thread terminar
        if self.backup_thread:
            self.backup_thread.join(timeout=5)
        
        # Criar backup final
        self.force_backup(reason="shutdown")
        
        print("♾️ Protocolo de imortalidade desligado")