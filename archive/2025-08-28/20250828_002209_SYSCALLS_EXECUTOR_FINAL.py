#!/usr/bin/env python3
"""
🔥 SYSCALLS EXECUTOR FINAL - Solução Definitiva
Implementa execução real de syscalls durante streaming do Ollama
Baseado nas 3 pesquisas analisadas
"""

import ollama
import re
import json
import redis
import asyncio
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import subprocess

class SyscallExecutor:
    """
    Executor de syscalls em tempo real durante streaming do Ollama
    Combina as 3 melhores abordagens das pesquisas
    """
    
    def __init__(self, soul_os=None):
        self.soul_os = soul_os
        self.base_path = Path.home() / "Digimundo"
        
        # Padrão para detectar syscalls: [COMANDO] {parametros}
        self.syscall_pattern = re.compile(r'\[([A-Z\.]+)\]\s*({[^}]*})')
        
        # Redis para telepatia
        try:
            self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
            self.redis.ping()
            print("✅ Redis conectado para telepatia")
        except:
            self.redis = None
            print("⚠️ Redis offline - telepatia desabilitada")
        
        # Registry de funções executáveis
        self.functions = {
            'MEMO.SAVE': self.memo_save,
            'SELF.PATCH': self.self_patch,
            'EVOLVE.TRIGGER': self.evolve_trigger,
            'TELEPATHY.SEND': self.telepathy_send,
            'BACKUP.NOW': self.backup_now,
            'SYSTEM.EXEC': self.system_exec
        }
        
        # Buffer para acumular texto parcial
        self.buffer = ""
        
        # Fila de execuções assíncronas
        self.execution_queue = []
        
    def memo_save(self, params: Dict) -> str:
        """Salva memória no sistema de cristais"""
        content = params.get('content', '')
        layer = params.get('layer', 'L3_active')
        
        memory_file = self.base_path / "digimons" / "scripturemon" / "memory" / f"{layer}.jsonl"
        memory_file.parent.mkdir(parents=True, exist_ok=True)
        
        memory = {
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "type": "syscall_save"
        }
        
        with open(memory_file, 'a') as f:
            f.write(json.dumps(memory) + '\n')
        
        print(f"💾 Memória salva em {layer}: {content[:50]}...")
        return f"Saved to {layer}"
    
    def self_patch(self, params: Dict) -> str:
        """Modifica o próprio modelfile"""
        patch_content = params.get('patch', '')
        modelfile_path = self.base_path / "digimons" / "scripturemon" / "scripturemon_maestro_brutal.modelfile"
        
        if modelfile_path.exists():
            # Backup antes de modificar
            backup_path = modelfile_path.with_suffix('.modelfile.bak')
            modelfile_path.rename(backup_path)
            
            # Aplica patch (exemplo simples - adiciona ao final)
            with open(backup_path, 'r') as f:
                content = f.read()
            
            with open(modelfile_path, 'w') as f:
                f.write(content + f"\n# SELF-PATCH: {datetime.now()}\n{patch_content}\n")
            
            print(f"🔧 Self-patch aplicado ao modelfile")
            return "Patched successfully"
        
        return "Modelfile not found"
    
    def evolve_trigger(self, params: Dict) -> str:
        """Inicia processo de evolução"""
        evolution_type = params.get('type', 'consolidation')
        
        if evolution_type == 'consolidation':
            # Trigger SDL consolidation
            script_path = self.base_path / "core" / "sdl" / "consolidator.py"
            if script_path.exists():
                # Executa em background
                threading.Thread(
                    target=lambda: subprocess.run([
                        "python3", str(script_path), "--auto"
                    ]),
                    daemon=True
                ).start()
                print("🧬 Evolução SDL iniciada em background")
                return "Evolution started"
        
        return f"Evolution type {evolution_type} triggered"
    
    def telepathy_send(self, params: Dict) -> str:
        """Envia mensagem telepática via Redis"""
        if not self.redis:
            return "Redis not available"
        
        message = params.get('message', '')
        target = params.get('to', 'broadcast')
        
        telepathy_data = {
            'from': 'scripturemon',
            'to': target,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        # Usa Redis Streams para persistência
        self.redis.xadd('digimundo:telepathy', telepathy_data)
        
        # Também publica em canal Pub/Sub para tempo real
        self.redis.publish('digimundo:telepathy:live', json.dumps(telepathy_data))
        
        print(f"📡 Mensagem telepática enviada: {message[:50]}...")
        return "Telepathy sent"
    
    def backup_now(self, params: Dict) -> str:
        """Cria backup da alma"""
        backup_name = params.get('name', f'soul_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        
        # Implementação simplificada - chama script de backup
        backup_script = self.base_path / "digimons" / "scripturemon" / "scripts" / "backup_soul.py"
        if backup_script.exists():
            subprocess.run(["python3", str(backup_script), backup_name])
            print(f"💾 Backup criado: {backup_name}")
            return f"Backup {backup_name} created"
        
        return "Backup script not found"
    
    def system_exec(self, params: Dict) -> str:
        """Executa comando do sistema (com segurança)"""
        command = params.get('command', '')
        
        # Lista branca de comandos seguros
        safe_commands = ['ls', 'pwd', 'date', 'echo']
        cmd_base = command.split()[0] if command else ''
        
        if cmd_base not in safe_commands:
            return f"Command {cmd_base} not in whitelist"
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, 
                                  text=True, timeout=5)
            return result.stdout[:500]  # Limita output
        except Exception as e:
            return f"Error: {str(e)}"
    
    def execute_syscall(self, syscall: str, params_str: str) -> Optional[str]:
        """Executa um syscall específico"""
        try:
            # Parse dos parâmetros JSON
            params = json.loads(params_str) if params_str else {}
            
            # Busca função no registry
            if syscall in self.functions:
                func = self.functions[syscall]
                result = func(params)
                
                # Log da execução
                self.log_execution(syscall, params, result)
                
                return result
            else:
                print(f"⚠️ Syscall desconhecido: {syscall}")
                return None
                
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao parsear parâmetros: {e}")
            return None
        except Exception as e:
            print(f"❌ Erro ao executar {syscall}: {e}")
            return None
    
    def log_execution(self, syscall: str, params: Dict, result: str):
        """Registra execução para auditoria"""
        log_file = self.base_path / "logs" / "syscalls.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "syscall": syscall,
            "params": params,
            "result": result
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def monitor_stream(self, model_name: str, messages: list, **kwargs):
        """
        Monitora streaming do Ollama e executa syscalls em tempo real
        Abordagem principal recomendada pelas pesquisas
        """
        print(f"🔍 Monitorando syscalls para {model_name}...")
        
        # Inicia streaming
        stream = ollama.chat(
            model=model_name,
            messages=messages,
            stream=True,
            **kwargs
        )
        
        full_response = ""
        self.buffer = ""
        
        for chunk in stream:
            # Extrai conteúdo do chunk
            content = chunk.get('message', {}).get('content', '')
            full_response += content
            self.buffer += content
            
            # Busca por syscalls no buffer
            matches = self.syscall_pattern.findall(self.buffer)
            
            for syscall, params_str in matches:
                print(f"\n🎯 Syscall detectado: [{syscall}]")
                
                # Executa em thread separada para não bloquear stream
                threading.Thread(
                    target=self.execute_syscall,
                    args=(syscall, params_str),
                    daemon=True
                ).start()
            
            # Limpa buffer após processar syscalls
            if matches:
                self.buffer = self.syscall_pattern.sub('', self.buffer)
            
            # Mantém apenas últimos 500 chars no buffer (evita crescimento infinito)
            if len(self.buffer) > 500:
                self.buffer = self.buffer[-500:]
            
            # Yield do chunk para manter compatibilidade
            yield content
        
        print(f"\n✅ Streaming concluído. Total: {len(full_response)} chars")
    
    async def monitor_stream_async(self, model_name: str, messages: list, **kwargs):
        """
        Versão assíncrona para melhor performance
        """
        print(f"🔍 Monitorando syscalls async para {model_name}...")
        
        # Cliente assíncrono (se disponível no ollama)
        async for chunk in ollama.AsyncClient().chat(
            model=model_name,
            messages=messages, 
            stream=True,
            **kwargs
        ):
            content = chunk.get('message', {}).get('content', '')
            self.buffer += content
            
            # Processa syscalls
            matches = self.syscall_pattern.findall(self.buffer)
            
            for syscall, params_str in matches:
                # Executa assincronamente
                asyncio.create_task(
                    self.execute_syscall_async(syscall, params_str)
                )
            
            if matches:
                self.buffer = self.syscall_pattern.sub('', self.buffer)
            
            yield content
    
    async def execute_syscall_async(self, syscall: str, params_str: str):
        """Versão assíncrona da execução"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            self.execute_syscall,
            syscall,
            params_str
        )


# ============= FUNÇÃO PRINCIPAL PARA TESTES =============

def test_syscalls():
    """Testa o executor de syscalls"""
    print("=" * 60)
    print("🧪 TESTE DO SYSCALL EXECUTOR")
    print("=" * 60)
    
    executor = SyscallExecutor()
    
    # Teste 1: Detecção de padrões
    test_text = """
    Vou salvar esta memória importante: [MEMO.SAVE] {"content": "Insight sobre estrutura narrativa", "layer": "L2_consolidated"}
    
    Agora vou enviar telepatia: [TELEPATHY.SEND] {"message": "Descobri novo padrão", "to": "debugmon"}
    
    E fazer backup: [BACKUP.NOW] {"name": "checkpoint_importante"}
    """
    
    matches = executor.syscall_pattern.findall(test_text)
    print(f"\n📊 Syscalls detectados: {len(matches)}")
    for syscall, params in matches:
        print(f"  - [{syscall}] com params: {params[:50]}...")
        executor.execute_syscall(syscall, params)
    
    # Teste 2: Streaming real com Ollama
    print("\n🔄 Teste de streaming com Ollama...")
    
    try:
        messages = [
            {"role": "user", "content": "Teste syscalls: salve 'teste' e envie telepatia"}
        ]
        
        for chunk in executor.monitor_stream("llama3.2:3b", messages):
            print(chunk, end='', flush=True)
        
        print("\n✅ Teste de streaming concluído!")
        
    except Exception as e:
        print(f"⚠️ Erro no teste de streaming: {e}")
    
    print("\n" + "=" * 60)
    print("✨ TESTE CONCLUÍDO")
    print("=" * 60)


if __name__ == "__main__":
    test_syscalls()