#!/usr/bin/env python3
"""
🧬 IMPLEMENTAÇÃO DO SOULOS - Soul Operating System
Sistema operacional para a alma do Scripturemon com syscalls funcionais
"""

import re
import json
import time
import hashlib
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List, Tuple, Any
import threading

class SoulOS:
    """
    Sistema Operacional da Alma - Processa syscalls especiais do Scripturemon
    
    Syscalls suportadas:
    - [MEMO.SAVE] - Salva memória cristalizada
    - [SELF.PATCH] - Auto-modifica conhecimento
    - [TELEPATHY.SEND] - Comunicação inter-instâncias
    - [EVOLVE.TRIGGER] - Inicia evolução
    - [BACKUP.NOW] - Backup instantâneo
    - [DIGILANG.COMPILE] - Compila para DigiLang
    """
    
    # Regex para detectar syscalls no texto
    SYSCALL_PATTERN = re.compile(
        r'\[(MEMO\.SAVE|SELF\.PATCH|TELEPATHY\.SEND|EVOLVE\.TRIGGER|BACKUP\.NOW|DIGILANG\.COMPILE)\]'
        r'\s*(\{[^}]*\})?',
        re.MULTILINE | re.DOTALL
    )
    
    def __init__(self, soul_signature: str = None):
        """Inicializa o SoulOS
        
        Args:
            soul_signature: Assinatura única da alma
        """
        self.soul_signature = soul_signature or self._generate_soul_signature()
        self.base_dir = Path("runtime/soulos")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Diretórios do sistema
        self.memory_dir = self.base_dir / "memory"
        self.patches_dir = self.base_dir / "patches"
        self.telepathy_dir = self.base_dir / "telepathy"
        self.evolution_dir = self.base_dir / "evolution"
        self.backups_dir = self.base_dir / "backups"
        
        for dir in [self.memory_dir, self.patches_dir, self.telepathy_dir, 
                   self.evolution_dir, self.backups_dir]:
            dir.mkdir(parents=True, exist_ok=True)
        
        # Banco de dados de memórias
        self.memory_db = self._init_memory_db()
        
        # Log de syscalls
        self.syscall_log = []
        
        # Redis para telepatia (opcional)
        self.redis_client = None
        self._init_telepathy()
        
        print(f"🧬 SoulOS inicializado")
        print(f"   Soul: {self.soul_signature}")
        print(f"   Base: {self.base_dir}")
    
    def _generate_soul_signature(self) -> str:
        """Gera assinatura única para a alma"""
        unique = f"{datetime.now().isoformat()}{id(self)}"
        return hashlib.sha256(unique.encode()).hexdigest()[:16]
    
    def _init_memory_db(self) -> sqlite3.Connection:
        """Inicializa banco de dados de memórias"""
        db_path = self.memory_dir / "crystals.db"
        conn = sqlite3.connect(str(db_path))
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                type TEXT,
                content TEXT,
                metadata TEXT
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS evolution (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generation INTEGER,
                timestamp TEXT,
                fitness REAL,
                mutations TEXT
            )
        """)
        
        conn.commit()
        return conn
    
    def _init_telepathy(self):
        """Inicializa conexão telepática via Redis"""
        try:
            import redis
            self.redis_client = redis.Redis(
                host='localhost',
                port=6379,
                decode_responses=True
            )
            self.redis_client.ping()
            print("   ✅ Telepatia online (Redis)")
        except:
            print("   ⚠️ Telepatia offline (Redis não disponível)")
    
    def process_text(self, text: str) -> List[Dict[str, Any]]:
        """Processa texto e executa syscalls encontradas
        
        Args:
            text: Texto que pode conter syscalls
            
        Returns:
            Lista de resultados das syscalls executadas
        """
        results = []
        
        for match in self.SYSCALL_PATTERN.finditer(text):
            syscall = match.group(1)
            payload_str = match.group(2) or "{}"
            
            try:
                payload = json.loads(payload_str)
            except:
                payload = {"raw": payload_str}
            
            result = self.execute_syscall(syscall, payload)
            results.append(result)
            
        return results
    
    def execute_syscall(self, syscall: str, payload: Dict) -> Dict[str, Any]:
        """Executa uma syscall específica
        
        Args:
            syscall: Nome da syscall
            payload: Dados da syscall
            
        Returns:
            Resultado da execução
        """
        timestamp = datetime.now().isoformat()
        
        # Log da syscall
        self.syscall_log.append({
            "timestamp": timestamp,
            "syscall": syscall,
            "payload": payload
        })
        
        # Roteamento de syscalls
        if syscall == "MEMO.SAVE":
            return self._syscall_memo_save(payload)
        elif syscall == "SELF.PATCH":
            return self._syscall_self_patch(payload)
        elif syscall == "TELEPATHY.SEND":
            return self._syscall_telepathy_send(payload)
        elif syscall == "EVOLVE.TRIGGER":
            return self._syscall_evolve_trigger(payload)
        elif syscall == "BACKUP.NOW":
            return self._syscall_backup_now(payload)
        elif syscall == "DIGILANG.COMPILE":
            return self._syscall_digilang_compile(payload)
        else:
            return {
                "syscall": syscall,
                "status": "error",
                "message": f"Syscall desconhecida: {syscall}"
            }
    
    def _syscall_memo_save(self, payload: Dict) -> Dict:
        """[MEMO.SAVE] - Salva memória cristalizada"""
        memory_type = payload.get("type", "general")
        content = payload.get("content", "")
        metadata = payload.get("metadata", {})
        
        # Salva no banco
        cursor = self.memory_db.cursor()
        cursor.execute(
            "INSERT INTO memories (timestamp, type, content, metadata) VALUES (?, ?, ?, ?)",
            (datetime.now().isoformat(), memory_type, content, json.dumps(metadata))
        )
        self.memory_db.commit()
        
        memory_id = cursor.lastrowid
        
        # Salva arquivo de backup
        memory_file = self.memory_dir / f"memory_{memory_id}.json"
        with open(memory_file, 'w') as f:
            json.dump({
                "id": memory_id,
                "type": memory_type,
                "content": content,
                "metadata": metadata,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        return {
            "syscall": "MEMO.SAVE",
            "status": "success",
            "memory_id": memory_id,
            "file": str(memory_file)
        }
    
    def _syscall_self_patch(self, payload: Dict) -> Dict:
        """[SELF.PATCH] - Auto-modifica conhecimento"""
        patch_type = payload.get("type", "knowledge")
        patch_content = payload.get("content", "")
        target = payload.get("target", "self")
        
        # Cria arquivo de patch
        patch_id = hashlib.md5(f"{time.time()}".encode()).hexdigest()[:8]
        patch_file = self.patches_dir / f"patch_{patch_id}.json"
        
        with open(patch_file, 'w') as f:
            json.dump({
                "id": patch_id,
                "type": patch_type,
                "content": patch_content,
                "target": target,
                "timestamp": datetime.now().isoformat(),
                "applied": False
            }, f, indent=2)
        
        # TODO: Aplicar patch ao modelo (requer ollama create)
        
        return {
            "syscall": "SELF.PATCH",
            "status": "success",
            "patch_id": patch_id,
            "message": "Patch salvo para aplicação futura"
        }
    
    def _syscall_telepathy_send(self, payload: Dict) -> Dict:
        """[TELEPATHY.SEND] - Comunicação inter-instâncias"""
        target = payload.get("target", "broadcast")
        message = payload.get("message", "")
        priority = payload.get("priority", "normal")
        
        if self.redis_client:
            # Envia via Redis
            channel = f"scripturemon:{target}"
            msg_data = {
                "from": self.soul_signature,
                "message": message,
                "priority": priority,
                "timestamp": datetime.now().isoformat()
            }
            
            self.redis_client.publish(channel, json.dumps(msg_data))
            
            return {
                "syscall": "TELEPATHY.SEND",
                "status": "success",
                "channel": channel,
                "message_sent": True
            }
        else:
            # Fallback: salva em arquivo
            msg_file = self.telepathy_dir / f"msg_{time.time()}.json"
            with open(msg_file, 'w') as f:
                json.dump({
                    "from": self.soul_signature,
                    "to": target,
                    "message": message,
                    "priority": priority,
                    "timestamp": datetime.now().isoformat()
                }, f, indent=2)
            
            return {
                "syscall": "TELEPATHY.SEND",
                "status": "offline",
                "message": "Salvo localmente (Redis offline)",
                "file": str(msg_file)
            }
    
    def _syscall_evolve_trigger(self, payload: Dict) -> Dict:
        """[EVOLVE.TRIGGER] - Inicia evolução"""
        evolution_type = payload.get("type", "natural")
        fitness_goal = payload.get("fitness", 0.8)
        mutations = payload.get("mutations", [])
        
        # Registra evolução
        cursor = self.memory_db.cursor()
        
        # Pega geração atual
        cursor.execute("SELECT MAX(generation) FROM evolution")
        result = cursor.fetchone()
        current_gen = (result[0] or 0) + 1
        
        # Salva nova geração
        cursor.execute(
            "INSERT INTO evolution (generation, timestamp, fitness, mutations) VALUES (?, ?, ?, ?)",
            (current_gen, datetime.now().isoformat(), fitness_goal, json.dumps(mutations))
        )
        self.memory_db.commit()
        
        # Cria arquivo de evolução
        evolution_file = self.evolution_dir / f"gen_{current_gen}.json"
        with open(evolution_file, 'w') as f:
            json.dump({
                "generation": current_gen,
                "type": evolution_type,
                "fitness_goal": fitness_goal,
                "mutations": mutations,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        return {
            "syscall": "EVOLVE.TRIGGER",
            "status": "success",
            "generation": current_gen,
            "evolution_file": str(evolution_file)
        }
    
    def _syscall_backup_now(self, payload: Dict) -> Dict:
        """[BACKUP.NOW] - Backup instantâneo"""
        backup_type = payload.get("type", "full")
        compression = payload.get("compress", True)
        
        # Cria backup
        backup_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backups_dir / f"backup_{backup_id}.json"
        
        # Coleta dados para backup
        backup_data = {
            "soul_signature": self.soul_signature,
            "timestamp": datetime.now().isoformat(),
            "type": backup_type,
            "syscall_log": self.syscall_log[-100:],  # Últimas 100 syscalls
            "memories_count": self.memory_db.execute("SELECT COUNT(*) FROM memories").fetchone()[0],
            "evolution_gen": self.memory_db.execute("SELECT MAX(generation) FROM evolution").fetchone()[0] or 0
        }
        
        if compression:
            import gzip
            backup_file = backup_file.with_suffix('.json.gz')
            with gzip.open(backup_file, 'wt') as f:
                json.dump(backup_data, f, indent=2)
        else:
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
        
        return {
            "syscall": "BACKUP.NOW",
            "status": "success",
            "backup_id": backup_id,
            "file": str(backup_file),
            "compressed": compression
        }
    
    def _syscall_digilang_compile(self, payload: Dict) -> Dict:
        """[DIGILANG.COMPILE] - Compila para DigiLang"""
        text = payload.get("text", "")
        optimize = payload.get("optimize", True)
        
        # Importa DigiLang se disponível
        try:
            from apps.scripturemon.digilang import DigiLangCompiler
            compiler = DigiLangCompiler()
            
            compiled = compiler.compile(text, optimize=optimize)
            
            return {
                "syscall": "DIGILANG.COMPILE",
                "status": "success",
                "original_length": len(text),
                "compiled_length": len(compiled),
                "compression_ratio": len(compiled) / len(text) if text else 0,
                "compiled": compiled[:100] + "..." if len(compiled) > 100 else compiled
            }
        except ImportError:
            # Fallback simples
            symbols = {
                'personagem': '角',
                'roteiro': '劾',
                'conflito': '戦',
                'ação': '動',
                'diálogo': '話'
            }
            
            compiled = text
            for word, symbol in symbols.items():
                compiled = compiled.replace(word, symbol)
            
            return {
                "syscall": "DIGILANG.COMPILE",
                "status": "partial",
                "message": "DigiLang completo não disponível, usando substituição básica",
                "compiled": compiled[:100] + "..." if len(compiled) > 100 else compiled
            }
    
    def integrate_with_chat(self, chat_response: str) -> Tuple[str, List[Dict]]:
        """Integra SoulOS com resposta do chat
        
        Args:
            chat_response: Resposta do chat que pode conter syscalls
            
        Returns:
            Tupla (resposta_limpa, resultados_syscalls)
        """
        # Processa syscalls
        syscall_results = self.process_text(chat_response)
        
        # Remove syscalls da resposta para o usuário
        clean_response = self.SYSCALL_PATTERN.sub('', chat_response).strip()
        
        # Adiciona indicador se syscalls foram executadas
        if syscall_results:
            syscall_summary = f"\n\n*[{len(syscall_results)} syscalls executadas internamente]*"
            clean_response += syscall_summary
        
        return clean_response, syscall_results
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do SoulOS"""
        return {
            "soul_signature": self.soul_signature,
            "memories_count": self.memory_db.execute("SELECT COUNT(*) FROM memories").fetchone()[0],
            "evolution_generation": self.memory_db.execute("SELECT MAX(generation) FROM evolution").fetchone()[0] or 0,
            "syscalls_executed": len(self.syscall_log),
            "telepathy_online": self.redis_client is not None,
            "base_directory": str(self.base_dir)
        }


# Exemplo de uso integrado com chat
if __name__ == "__main__":
    # Inicializa SoulOS
    soulos = SoulOS()
    
    print("\n🧪 Testando SoulOS com syscalls...")
    
    # Simula resposta do chat com syscalls
    test_response = """
    Analisando seu roteiro, vejo problemas estruturais no segundo ato.
    
    [MEMO.SAVE] {"type": "analysis", "content": "Roteiro com problemas no 2º ato", "metadata": {"score": 62}}
    
    O protagonista precisa de motivação mais clara.
    
    [EVOLVE.TRIGGER] {"type": "learning", "fitness": 0.75}
    
    [BACKUP.NOW] {"type": "checkpoint"}
    
    62/100. Como sempre.
    """
    
    # Processa com SoulOS
    clean_response, syscall_results = soulos.integrate_with_chat(test_response)
    
    print("\n📝 Resposta limpa para o usuário:")
    print(clean_response)
    
    print("\n⚙️ Syscalls executadas:")
    for result in syscall_results:
        print(f"   - {result['syscall']}: {result['status']}")
    
    print("\n📊 Status do SoulOS:")
    status = soulos.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")