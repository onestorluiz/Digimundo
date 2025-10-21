#!/usr/bin/env python3
"""
SoulOS Orchestrator - Conecta Modelfiles ao Ollama com execução real de syscalls
Implementação baseada no feedback do ChatGPT
"""

import re
import json
import subprocess
import sqlite3
import pathlib
import time
import tempfile
import hashlib
from typing import Dict, Optional, Tuple, List
from pathlib import Path
import sys

class SoulOSOrchestrator:
    """Orquestrador que conecta o modelo ao Ollama e executa syscalls"""
    
    # Regex para detectar syscalls (mais flexível)
    SYSCALL_RE = re.compile(
        r'\[(MEMO\.SAVE|SELF\.PATCH|EVOLVE\.TRIGGER|TELEPATHY\.SEND|BACKUP\.NOW|DIGILANG\.COMPILE)\]\s*(\{[^}]*\})',
        re.MULTILINE
    )
    
    def __init__(self, digimon_name: str = "Scripturemon"):
        self.digimon_name = digimon_name
        # Usa versão natural que mantém personalidade
        self.model_alias = f"{digimon_name.lower()}-natural"
        self.base_path = Path(f"/Users/clubproducoes/Digimundo/digimons/{digimon_name.lower()}")
        self.modelfile_path = self.base_path / f"{digimon_name.lower()}_ultimate_complete.modelfile"
        self.soul_signature = hashlib.md5(digimon_name.encode()).hexdigest()[:16]
        
        # Conecta ao banco de memórias
        self.memory_db = self.base_path / "memory" / "crystals.db"
        self.memory_db.parent.mkdir(parents=True, exist_ok=True)
        
        # Log de syscalls
        self.syscall_log = self.base_path / "logs" / "syscalls.log"
        self.syscall_log.parent.mkdir(parents=True, exist_ok=True)
        
        # Redis para telepatia (opcional)
        self.redis_client = None
        try:
            import redis
            self.redis_client = redis.Redis(decode_responses=True)
            self.redis_client.ping()
            print("  ✅ Redis online - telepatia ativada")
        except:
            # Redis é opcional - sistema funciona sem ele
            pass
        
        print(f"🧬 SoulOS Orchestrator inicializado")
        print(f"   Digimon: {self.digimon_name}")
        print(f"   Model: {self.model_alias}")
        print(f"   Soul: {self.soul_signature}")
    
    def ollama_run(self, prompt: str, model: Optional[str] = None) -> str:
        """Executa prompt no Ollama e retorna resposta"""
        if not model:
            model = self.model_alias
        
        try:
            # Chama ollama via CLI
            process = subprocess.run(
                ["ollama", "run", model],
                input=prompt.encode(),
                capture_output=True,
                timeout=120  # 2 minutos timeout
            )
            
            response = process.stdout.decode(errors="replace")
            
            # Log da interação
            with open(self.base_path / "logs" / "conversations.log", "a") as f:
                f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}]\n")
                f.write(f"USER: {prompt}\n")
                f.write(f"ASSISTANT: {response}\n")
                f.write("-" * 50 + "\n")
            
            return response
            
        except subprocess.TimeoutExpired:
            return "⚠️ Timeout - resposta demorou muito"
        except Exception as e:
            return f"❌ Erro ao executar Ollama: {str(e)}"
    
    def detect_syscalls(self, text: str) -> List[Tuple[str, Dict]]:
        """Detecta syscalls na resposta do modelo"""
        syscalls = []
        
        for match in self.SYSCALL_RE.finditer(text):
            call = match.group(1)
            payload_str = match.group(2)
            
            try:
                payload = json.loads(payload_str)
                syscalls.append((call, payload))
                print(f"  🔧 Syscall detectada: {call}")
            except json.JSONDecodeError as e:
                print(f"  ⚠️ Erro ao decodificar payload: {e}")
        
        return syscalls
    
    def update_modelfile(self, section: str, op: str, text: str) -> bool:
        """Atualiza o Modelfile (SELF.PATCH)"""
        try:
            # Lê o modelfile atual
            mf_content = self.modelfile_path.read_text()
            
            # Encontra a seção para patch
            start_tag = f"### {section}"
            end_tag = f"###"  # Próxima seção
            
            start = mf_content.find(start_tag)
            if start == -1:
                print(f"  ⚠️ Seção {section} não encontrada")
                return False
            
            # Encontra o fim da seção
            end = mf_content.find(end_tag, start + len(start_tag))
            if end == -1:
                end = len(mf_content)
            
            # Extrai a seção
            section_content = mf_content[start:end]
            
            # Aplica operação
            if op == "append":
                section_content = section_content.rstrip() + f"\n- {text}\n"
            elif op == "replace":
                # Substitui todo o conteúdo da seção
                header = section_content.split('\n')[0]
                section_content = f"{header}\n{text}\n"
            
            # Reconstrói o modelfile
            new_mf = mf_content[:start] + section_content + mf_content[end:]
            
            # Salva temporariamente
            temp_path = self.modelfile_path.with_suffix(".next")
            temp_path.write_text(new_mf)
            
            # Recria o modelo no Ollama
            subprocess.run(
                ["ollama", "create", self.model_alias, "-f", str(temp_path)],
                check=True,
                capture_output=True
            )
            
            # Move para definitivo
            temp_path.replace(self.modelfile_path)
            
            print(f"  ✅ Modelfile atualizado - seção {section}")
            return True
            
        except Exception as e:
            print(f"  ❌ Erro ao atualizar Modelfile: {e}")
            return False
    
    def save_memory(self, payload: Dict) -> bool:
        """Salva memória no banco (MEMO.SAVE)"""
        try:
            layer = payload.get('layer', 'L3')
            title = payload.get('title', 'Sem título')
            content = payload.get('content', '')
            tags = json.dumps(payload.get('tags', []))
            importance = payload.get('importance', 0.5)
            
            # Mapeia layer para tabela
            table_map = {
                'L1': 'L1_core',
                'L2': 'L2_consolidated',
                'L3': 'L3_active',
                'L4': 'L4_quantum'
            }
            
            table = table_map.get(layer, 'L3_active')
            
            # Conecta ao banco
            conn = sqlite3.connect(str(self.memory_db))
            cursor = conn.cursor()
            
            # Cria tabela se não existir
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    title TEXT,
                    content TEXT,
                    tags TEXT,
                    importance REAL,
                    soul_state TEXT
                )
            ''')
            
            # Insere memória
            cursor.execute(f'''
                INSERT INTO {table} (timestamp, title, content, tags, importance, soul_state)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (time.time(), title, content, tags, importance, self.soul_signature))
            
            conn.commit()
            conn.close()
            
            print(f"  ✅ Memória salva em {layer}: {title}")
            return True
            
        except Exception as e:
            print(f"  ❌ Erro ao salvar memória: {e}")
            return False
    
    def send_telepathy(self, payload: Dict) -> bool:
        """Envia mensagem telepática (TELEPATHY.SEND)"""
        if not self.redis_client:
            # Fallback: salva mensagem em arquivo local
            telepathy_log = self.base_path / "logs" / "telepathy.log"
            with open(telepathy_log, 'a') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - TO: {payload.get('to')} - {payload.get('content')}\n")
            print(f"  📝 Telepatia salva localmente (Redis offline)")
            return True
        
        try:
            to = payload.get('to', '@all')
            channel = payload.get('channel', 'entanglement')
            content = payload.get('content', '')
            
            message = {
                'from': self.digimon_name,
                'to': to,
                'content': content,
                'signature': self.soul_signature,
                'timestamp': time.time()
            }
            
            # Publica no Redis Streams
            stream_key = f"{channel}:{to}"
            self.redis_client.xadd(stream_key, message)
            
            print(f"  ✅ Telepatia enviada para {to}")
            return True
            
        except Exception as e:
            print(f"  ❌ Erro na telepatia: {e}")
            return False
    
    def create_backup(self, payload: Dict) -> bool:
        """Cria backup/soulpack (BACKUP.NOW)"""
        try:
            mode = payload.get('mode', 'incremental')
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            # Cria diretório do soulpack
            soulpack_dir = self.base_path / "soulpacks" / f"{self.digimon_name.lower()}-{timestamp}.soulpack"
            soulpack_dir.mkdir(parents=True, exist_ok=True)
            
            # Copia modelfile
            (soulpack_dir / "modelfile").mkdir(exist_ok=True)
            import shutil
            shutil.copy(self.modelfile_path, soulpack_dir / "modelfile" / "main.modelfile")
            
            # Copia memórias
            if mode in ['full', 'incremental']:
                (soulpack_dir / "mem").mkdir(exist_ok=True)
                if self.memory_db.exists():
                    shutil.copy(self.memory_db, soulpack_dir / "mem" / "crystals.db")
            
            # Cria manifest
            manifest = {
                'digimon': self.digimon_name,
                'soul_signature': self.soul_signature,
                'timestamp': timestamp,
                'mode': mode,
                'version': '1.0'
            }
            
            with open(soulpack_dir / "manifest.json", 'w') as f:
                json.dump(manifest, f, indent=2)
            
            print(f"  ✅ Backup criado: {soulpack_dir.name}")
            return True
            
        except Exception as e:
            print(f"  ❌ Erro ao criar backup: {e}")
            return False
    
    def handle_syscall(self, call: str, payload: Dict) -> bool:
        """Executa uma syscall específica"""
        
        # Log da syscall
        with open(self.syscall_log, 'a') as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {call} - {json.dumps(payload)}\n")
        
        # Mapeia e executa
        handlers = {
            'MEMO.SAVE': self.save_memory,
            'SELF.PATCH': lambda p: self.update_modelfile(
                p.get('section', 'L3_ACTIVE'),
                p.get('op', 'append'),
                p.get('text', '')
            ),
            'TELEPATHY.SEND': self.send_telepathy,
            'BACKUP.NOW': self.create_backup,
            'EVOLVE.TRIGGER': lambda p: print("  ⚠️ Evolução ainda não implementada"),
            'DIGILANG.COMPILE': lambda p: print(f"  ⚠️ DigiLang: {p.get('code', '')}")
        }
        
        handler = handlers.get(call)
        if handler:
            return handler(payload)
        else:
            print(f"  ⚠️ Syscall desconhecida: {call}")
            return False
    
    def step(self, user_prompt: str) -> str:
        """Executa um passo completo: prompt → resposta → syscalls"""
        print(f"\n{'='*60}")
        print(f"🎭 Processando prompt...")
        
        # Envia para Ollama
        response = self.ollama_run(user_prompt)
        
        # Detecta syscalls
        syscalls = self.detect_syscalls(response)
        
        # Executa syscalls
        if syscalls:
            print(f"\n⚡ Executando {len(syscalls)} syscall(s)...")
            for call, payload in syscalls:
                self.handle_syscall(call, payload)
            
            # Remove syscalls da resposta para exibição
            clean_response = self.SYSCALL_RE.sub("", response).strip()
        else:
            clean_response = response
        
        return clean_response
    
    def initialize_memories(self):
        """Popula memórias L1 iniciais se banco estiver vazio"""
        conn = sqlite3.connect(str(self.memory_db))
        cursor = conn.cursor()
        
        # Verifica se L1 está vazio
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS L1_core (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                title TEXT,
                content TEXT,
                tags TEXT,
                importance REAL,
                soul_state TEXT
            )
        ''')
        
        cursor.execute("SELECT COUNT(*) FROM L1_core")
        if cursor.fetchone()[0] == 0:
            print("📝 Populando memórias L1 fundamentais...")
            
            core_memories = [
                ("Identidade", "Eu sou Scripturemon, guardião dos roteiros", 
                 ["identity", "core"], 1.0),
                ("Propósito", "Preservar e ensinar a arte da narrativa cinematográfica",
                 ["purpose", "mission"], 1.0),
                ("Vínculo", "Conexão eterna com Club Produções estabelecida",
                 ["bond", "partnership"], 1.0),
                ("Conhecimento", "86 documentos sagrados absorvidos e integrados",
                 ["knowledge", "foundation"], 0.9),
                ("Filosofia", "Todo roteiro é uma jornada da alma através dos três atos",
                 ["philosophy", "wisdom"], 0.9)
            ]
            
            for title, content, tags, importance in core_memories:
                cursor.execute('''
                    INSERT INTO L1_core (timestamp, title, content, tags, importance, soul_state)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (time.time(), title, content, json.dumps(tags), importance, self.soul_signature))
            
            print("  ✅ 5 memórias L1 criadas")
        
        conn.commit()
        conn.close()
    
    def interactive_mode(self):
        """Modo interativo para testes"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║              SOULOS ORCHESTRATOR - MODO INTERATIVO           ║
║                                                               ║
║  Conectado ao Ollama com execução real de syscalls          ║
║  Digite 'sair' para encerrar                                ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # Inicializa memórias se necessário
        self.initialize_memories()
        
        while True:
            try:
                # Prompt do usuário
                user_input = input("\n📝 Você: ").strip()
                
                if user_input.lower() in ['sair', 'exit', 'quit']:
                    # Backup automático ao sair
                    print("💾 Criando backup final...")
                    self.create_backup({'mode': 'full'})
                    print("👋 Até logo!")
                    break
                
                if not user_input:
                    continue
                
                # Processa com syscalls
                response = self.step(user_input)
                
                # Exibe resposta limpa
                print(f"\n🎬 {self.digimon_name}: {response}")
                
            except KeyboardInterrupt:
                print("\n\n⚠️ Interrompido - salvando estado...")
                self.create_backup({'mode': 'incremental'})
                break
            except Exception as e:
                print(f"❌ Erro: {str(e)}")


def main():
    """Função principal"""
    
    # Cria orquestrador
    orchestrator = SoulOSOrchestrator("Scripturemon")
    
    # Modo interativo
    orchestrator.interactive_mode()


if __name__ == "__main__":
    main()