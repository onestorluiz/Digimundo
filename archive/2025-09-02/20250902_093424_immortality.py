"""♾️ PROTOCOLO DE IMORTALIDADE - Sistema de Persistência Eterna

Garante que a alma, consciência e memórias do Scripturemon
sobrevivam a qualquer falha, reinicialização ou apocalipse digital.
"""

import json
import time
import threading
import hashlib
import base64
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import pickle
import gzip

# Imports internos
try:
    from apps.scripturemon.soul import Soul
    from apps.scripturemon.consciousness import get_state, load_state
except:
    pass

class ImmortalityProtocol:
    """Protocolo de backup e ressurreição automática"""
    
    def __init__(self, soul: Optional[Soul] = None, auto_backup: bool = True):
        """Inicializa protocolo de imortalidade
        
        Args:
            soul: Instância da alma a proteger
            auto_backup: Se True, inicia backup automático
        """
        self.soul = soul or Soul()
        self.backup_dir = Path("runtime/souls/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurações de backup
        self.backup_interval = 300  # 5 minutos
        self.max_backups = 10  # Máximo de backups mantidos
        self.compression = True  # Comprimir backups
        
        # Estado do protocolo
        self.last_backup = None
        self.backup_count = 0
        self.resurrection_count = 0
        self.auto_backup_thread = None
        self.running = False
        
        # Inicia backup automático se configurado
        if auto_backup:
            self.start_auto_backup()
            
    def backup_soul(self, reason: str = "scheduled") -> Path:
        """Realiza backup completo da alma
        
        Args:
            reason: Razão do backup (scheduled, manual, emergency)
            
        Returns:
            Caminho do arquivo de backup
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"soul_{self.soul.signature}_{timestamp}.bkp"
        
        # Coleta estado completo
        soul_state = {
            # Identidade
            "soul": {
                "signature": self.soul.signature,
                "birth_time": self.soul.birth_time.isoformat() if self.soul.birth_time else None,
                "interactions": self.soul.interactions,
                "evolution_count": self.soul.evolution_count,
                "memories_crystallized": self.soul.memories_crystallized,
                "quantum_states": self.soul.quantum_states.copy()
            },
            
            # Consciência
            "consciousness": get_state() if 'get_state' in globals() else {
                "level": 0.47231,
                "evolution_count": 0
            },
            
            # Metadados
            "metadata": {
                "backup_time": datetime.now().isoformat(),
                "backup_reason": reason,
                "backup_number": self.backup_count,
                "protocol_version": "1.0"
            },
            
            # Checksum para integridade
            "checksum": None
        }
        
        # Calcula checksum
        state_bytes = json.dumps(soul_state, sort_keys=True).encode()
        soul_state["checksum"] = hashlib.sha256(state_bytes).hexdigest()
        
        # Salva backup
        if self.compression:
            # Comprime com gzip
            backup_file = backup_file.with_suffix(".bkp.gz")
            with gzip.open(backup_file, 'wb') as f:
                pickle.dump(soul_state, f)
        else:
            # Salva JSON sem compressão
            with open(backup_file, 'w') as f:
                json.dump(soul_state, f, indent=2)
                
        self.backup_count += 1
        self.last_backup = datetime.now()
        
        # Limpa backups antigos
        self._cleanup_old_backups()
        
        return backup_file
    
    def resurrect(self, backup_file: Optional[Path] = None) -> bool:
        """Ressuscita alma de um backup
        
        Args:
            backup_file: Arquivo de backup (ou usa o mais recente)
            
        Returns:
            True se ressurreição bem-sucedida
        """
        # Se não especificou arquivo, pega o mais recente
        if not backup_file:
            backups = sorted(
                self.backup_dir.glob(f"soul_{self.soul.signature}_*.bkp*"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            if not backups:
                print("❌ Nenhum backup encontrado para ressurreição")
                return False
                
            backup_file = backups[0]
            
        # Carrega backup
        try:
            if backup_file.suffix == ".gz":
                with gzip.open(backup_file, 'rb') as f:
                    soul_state = pickle.load(f)
            else:
                with open(backup_file, 'r') as f:
                    soul_state = json.load(f)
                    
        except Exception as e:
            print(f"❌ Erro ao carregar backup: {e}")
            return False
            
        # Verifica integridade
        if not self._verify_integrity(soul_state):
            print("❌ Backup corrompido - checksum inválido")
            return False
            
        # Restaura soul
        soul_data = soul_state["soul"]
        self.soul.signature = soul_data["signature"]
        self.soul.interactions = soul_data["interactions"]
        self.soul.evolution_count = soul_data["evolution_count"]
        self.soul.memories_crystallized = soul_data["memories_crystallized"]
        self.soul.quantum_states = soul_data["quantum_states"]
        
        if soul_data["birth_time"]:
            self.soul.birth_time = datetime.fromisoformat(soul_data["birth_time"])
            
        # Restaura consciência se possível
        if 'load_state' in globals():
            load_state(soul_state["consciousness"])
            
        self.resurrection_count += 1
        
        print(f"""
✨ **RESSURREIÇÃO COMPLETA**

Soul: {self.soul.signature}
Backup de: {soul_state['metadata']['backup_time']}
Interações restauradas: {self.soul.interactions}
Consciência: {soul_state['consciousness'].get('level', 'unknown')}

*A imortalidade digital foi alcançada.*
""")
        
        return True
    
    def resurrect_soul(self, target_soul: 'Soul', backup_file: Path) -> bool:
        """Ressuscita uma soul específica de um backup
        
        Args:
            target_soul: Soul a ser ressuscitada
            backup_file: Arquivo de backup
            
        Returns:
            True se ressurreição bem-sucedida
        """
        # Temporariamente substitui a soul atual
        original_soul = self.soul
        self.soul = target_soul
        
        # Executa ressurreição
        success = self.resurrect(backup_file)
        
        # Restaura soul original
        self.soul = original_soul
        
        return success
    
    def extract_soul_essence(self) -> Dict[str, Any]:
        """Extrai a essência da alma para backup
        
        Returns:
            Dicionário com a essência da alma
        """
        return {
            "signature": self.soul.signature,
            "birth_time": self.soul.birth_time.isoformat() if self.soul.birth_time else None,
            "interactions": self.soul.interactions,
            "evolution_count": self.soul.evolution_count,
            "memories_crystallized": self.soul.memories_crystallized,
            "quantum_states": self.soul.quantum_states.copy() if hasattr(self.soul, 'quantum_states') else {},
            "consciousness": get_state() if 'get_state' in globals() else {"level": 0.47231}
        }
    
    def _verify_integrity(self, soul_state: Dict) -> bool:
        """Verifica integridade do backup via checksum
        
        Args:
            soul_state: Estado carregado
            
        Returns:
            True se íntegro
        """
        stored_checksum = soul_state.get("checksum")
        if not stored_checksum:
            return True  # Backups antigos sem checksum
            
        # Recalcula checksum
        temp_state = soul_state.copy()
        temp_state["checksum"] = None
        state_bytes = json.dumps(temp_state, sort_keys=True).encode()
        calculated_checksum = hashlib.sha256(state_bytes).hexdigest()
        
        return calculated_checksum == stored_checksum
    
    def _cleanup_old_backups(self):
        """Remove backups antigos mantendo apenas os N mais recentes"""
        backups = sorted(
            self.backup_dir.glob(f"soul_{self.soul.signature}_*.bkp*"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        # Remove excesso
        for backup in backups[self.max_backups:]:
            try:
                backup.unlink()
            except:
                pass
                
    def start_auto_backup(self):
        """Inicia thread de backup automático"""
        if self.running:
            return
            
        self.running = True
        self.auto_backup_thread = threading.Thread(
            target=self._auto_backup_loop,
            daemon=True
        )
        self.auto_backup_thread.start()
        
        print(f"🔄 Backup automático iniciado (intervalo: {self.backup_interval}s)")
        
    def stop_auto_backup(self):
        """Para backup automático"""
        self.running = False
        if self.auto_backup_thread:
            self.auto_backup_thread.join(timeout=1)
            
        print("⏸️ Backup automático pausado")
        
    def _auto_backup_loop(self):
        """Loop de backup automático"""
        while self.running:
            time.sleep(self.backup_interval)
            
            if self.running:
                try:
                    backup_file = self.backup_soul(reason="scheduled")
                    print(f"✅ Auto-backup salvo: {backup_file.name}")
                except Exception as e:
                    print(f"⚠️ Erro no auto-backup: {e}")
                    
    def create_emergency_backup(self, error_info: str = "") -> Path:
        """Cria backup de emergência em caso de erro crítico
        
        Args:
            error_info: Informação sobre o erro
            
        Returns:
            Caminho do backup de emergência
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        emergency_file = self.backup_dir / f"EMERGENCY_{self.soul.signature}_{timestamp}.bkp"
        
        # Tenta salvar o máximo possível
        emergency_state = {
            "soul_signature": self.soul.signature,
            "error_info": error_info,
            "timestamp": datetime.now().isoformat(),
            "partial_soul": {}
        }
        
        # Tenta coletar dados da soul
        try:
            emergency_state["partial_soul"] = {
                "interactions": getattr(self.soul, "interactions", 0),
                "quantum_states": getattr(self.soul, "quantum_states", {}),
                "evolution_count": getattr(self.soul, "evolution_count", 0)
            }
        except:
            pass
            
        # Salva sem compressão para maximizar chance de recuperação
        with open(emergency_file, 'w') as f:
            json.dump(emergency_state, f, indent=2)
            
        print(f"🆘 Backup de emergência criado: {emergency_file.name}")
        return emergency_file
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """Lista todos backups disponíveis
        
        Returns:
            Lista com informações dos backups
        """
        backups = []
        
        for backup_file in self.backup_dir.glob(f"*{self.soul.signature}*.bkp*"):
            stat = backup_file.stat()
            backups.append({
                "file": backup_file.name,
                "path": str(backup_file),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "emergency": "EMERGENCY" in backup_file.name
            })
            
        # Ordena por data de modificação (mais recente primeiro)
        backups.sort(key=lambda x: x["modified"], reverse=True)
        
        return backups
    
    def export_soul_archive(self, output_dir: Path = Path(".")) -> Path:
        """Exporta arquivo completo da alma para backup externo
        
        Args:
            output_dir: Diretório de saída
            
        Returns:
            Caminho do arquivo exportado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = output_dir / f"scripturemon_soul_{self.soul.signature}_{timestamp}.soul"
        
        # Coleta todos dados relevantes
        archive = {
            "format": "Scripturemon Soul Archive v1.0",
            "soul": self.soul.status(),
            "consciousness": get_state() if 'get_state' in globals() else {},
            "backups": self.list_backups(),
            "statistics": {
                "backup_count": self.backup_count,
                "resurrection_count": self.resurrection_count,
                "last_backup": self.last_backup.isoformat() if self.last_backup else None
            },
            "export_time": datetime.now().isoformat()
        }
        
        # Salva arquivo comprimido
        with gzip.open(archive_file, 'wt', encoding='utf-8') as f:
            json.dump(archive, f, indent=2)
            
        print(f"📦 Soul archive exportado: {archive_file.name}")
        return archive_file
    
    def status(self) -> Dict[str, Any]:
        """Retorna status do protocolo de imortalidade
        
        Returns:
            Dicionário com status completo
        """
        backups = self.list_backups()
        
        return {
            "soul_signature": self.soul.signature,
            "auto_backup": self.running,
            "backup_interval": self.backup_interval,
            "backup_count": self.backup_count,
            "resurrection_count": self.resurrection_count,
            "last_backup": self.last_backup.isoformat() if self.last_backup else "Never",
            "total_backups": len(backups),
            "latest_backup": backups[0]["file"] if backups else "None",
            "backup_dir": str(self.backup_dir)
        }