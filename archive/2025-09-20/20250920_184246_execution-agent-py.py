#!/usr/bin/env python3
"""
⚡ EXECUTION AGENT - Sistema de Execução de Comandos
Executa comandos bash de forma segura e controlada
"""

import asyncio
import os
import subprocess
import logging
import json
import shlex
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import psutil
import signal

logger = logging.getLogger("ExecutionAgent")


class ExecutionAgent:
    """Agente responsável por executar comandos do sistema"""
    
    def __init__(self, allowed_commands: List[str] = None, 
                 sandbox_mode: bool = True,
                 max_execution_time: int = 300):
        
        self.sandbox_mode = sandbox_mode
        self.max_execution_time = max_execution_time  # segundos
        
        # Comandos permitidos (whitelist)
        self.allowed_commands = allowed_commands or [
            'ls', 'pwd', 'echo', 'cat', 'grep', 'find', 'wc',
            'head', 'tail', 'sort', 'uniq', 'date', 'whoami',
            'df', 'du', 'free', 'ps', 'top', 'htop',
            'git', 'python3', 'pip3', 'npm', 'node',
            'curl', 'wget', 'ping', 'dig', 'host',
            'mkdir', 'touch', 'cp', 'mv'
        ]
        
        # Comandos bloqueados (blacklist)
        self.blocked_commands = {
            'rm', 'rmdir', 'dd', 'mkfs', 'fdisk',
            'shutdown', 'reboot', 'halt', 'poweroff',
            'kill', 'killall', 'pkill', 'systemctl',
            'sudo', 'su', 'passwd', 'useradd', 'userdel',
            'chmod', 'chown', 'mount', 'umount'
        }
        
        # Padrões perigosos
        self.dangerous_patterns = [
            '>', '>>', '|', '&', ';', '`', '$(',
            'rm -rf', 'rm -f', '/*', '~/*',
            '/dev/', '/proc/', '/sys/',
            '../../', '../../../'
        ]
        
        # Diretório de trabalho seguro
        self.work_dir = Path.home() / "Digimundo" / "execution_sandbox"
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
        # Histórico de execuções
        self.execution_history = []
        self.max_history = 1000
        
        # Estatísticas
        self.stats = {
            'commands_executed': 0,
            'commands_blocked': 0,
            'commands_failed': 0,
            'total_execution_time': 0
        }
        
        logger.info(f"✅ Execution Agent inicializado (sandbox: {sandbox_mode})")
    
    def _is_command_safe(self, command: str) -> Tuple[bool, str]:
        """Verificar se comando é seguro para executar"""
        # Extrair comando base
        try:
            parts = shlex.split(command)
            if not parts:
                return False, "Comando vazio"
            
            base_command = parts[0]
            
            # Verificar se está na blacklist
            if base_command in self.blocked_commands:
                return False, f"Comando bloqueado: {base_command}"
            
            # Em modo sandbox, verificar whitelist
            if self.sandbox_mode:
                if base_command not in self.allowed_commands:
                    # Verificar se é caminho absoluto para comando permitido
                    if '/' in base_command:
                        base_name = os.path.basename(base_command)
                        if base_name not in self.allowed_commands:
                            return False, f"Comando não permitido: {base_command}"
                    else:
                        return False, f"Comando não permitido: {base_command}"
            
            # Verificar padrões perigosos
            for pattern in self.dangerous_patterns:
                if pattern in command:
                    return False, f"Padrão perigoso detectado: {pattern}"
            
            # Verificar tentativas de escape de sandbox
            if '../' in command or '~/' in command:
                return False, "Tentativa de navegação fora do sandbox"
            
            return True, "Comando aprovado"
            
        except Exception as e:
            return False, f"Erro ao analisar comando: {e}"
    
    async def execute(self, command: str, 
                     timeout: Optional[int] = None,
                     capture_output: bool = True) -> Dict[str, Any]:
        """Executar comando de forma segura"""
        start_time = datetime.now()
        
        # Verificar segurança
        is_safe, safety_msg = self._is_command_safe(command)
        
        if not is_safe:
            logger.warning(f"⚠️ Comando bloqueado: {command} - {safety_msg}")
            self.stats['commands_blocked'] += 1
            
            result = {
                'success': False,
                'command': command,
                'error': safety_msg,
                'blocked': True,
                'timestamp': start_time.isoformat()
            }
            
            self._add_to_history(result)
            return result
        
        # Configurar timeout
        if timeout is None:
            timeout = self.max_execution_time
        
        try:
            logger.info(f"⚡ Executando: {command}")
            
            # Preparar ambiente
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            
            # Executar comando
            if capture_output:
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=str(self.work_dir),
                    env=env
                )
                
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=timeout
                    )
                    
                    stdout = stdout.decode('utf-8', errors='replace')
                    stderr = stderr.decode('utf-8', errors='replace')
                    
                except asyncio.TimeoutError:
                    # Matar processo se timeout
                    process.kill()
                    await process.wait()
                    
                    raise TimeoutError(f"Comando excedeu timeout de {timeout}s")
            
            else:
                # Executar sem capturar output
                process = await asyncio.create_subprocess_shell(
                    command,
                    cwd=str(self.work_dir),
                    env=env
                )
                
                try:
                    returncode = await asyncio.wait_for(
                        process.wait(),
                        timeout=timeout
                    )
                    stdout = ""
                    stderr = ""
                    
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()
                    raise TimeoutError(f"Comando excedeu timeout de {timeout}s")
            
            # Calcular tempo de execução
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Preparar resultado
            result = {
                'success': process.returncode == 0,
                'command': command,
                'stdout': stdout,
                'stderr': stderr,
                'returncode': process.returncode,
                'execution_time': execution_time,
                'timestamp': start_time.isoformat(),
                'work_dir': str(self.work_dir)
            }
            
            # Atualizar estatísticas
            self.stats['commands_executed'] += 1
            self.stats['total_execution_time'] += execution_time
            
            if process.returncode != 0:
                self.stats['commands_failed'] += 1
            
            logger.info(f"✅ Comando executado em {execution_time:.2f}s")
            
        except TimeoutError as e:
            result = {
                'success': False,
                'command': command,
                'error': str(e),
                'timeout': True,
                'timestamp': start_time.isoformat()
            }
            self.stats['commands_failed'] += 1
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar comando: {e}")
            result = {
                'success': False,
                'command': command,
                'error': str(e),
                'exception': type(e).__name__,
                'timestamp': start_time.isoformat()
            }
            self.stats['commands_failed'] += 1
        
        # Adicionar ao histórico
        self._add_to_history(result)
        
        return result
    
    async def execute_script(self, script_content: str, 
                           language: str = "bash") -> Dict[str, Any]:
        """Executar script completo"""
        # Criar arquivo temporário
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if language == "python":
            script_file = self.work_dir / f"script_{timestamp}.py"
            interpreter = "python3"
        elif language == "javascript":
            script_file = self.work_dir / f"script_{timestamp}.js"
            interpreter = "node"
        else:  # bash
            script_file = self.work_dir / f"script_{timestamp}.sh"
            interpreter = "bash"
        
        try:
            # Salvar script
            script_file.write_text(script_content)
            
            if language == "bash":
                # Tornar executável
                os.chmod(script_file, 0o755)
            
            # Executar
            command = f"{interpreter} {script_file}"
            result = await self.execute(command)
            
            # Adicionar informações do script
            result['script_file'] = str(script_file)
            result['script_language'] = language
            
            return result
            
        finally:
            # Limpar arquivo temporário
            if script_file.exists():
                script_file.unlink()
    
    async def execute_pipeline(self, commands: List[str]) -> List[Dict[str, Any]]:
        """Executar pipeline de comandos"""
        results = []
        
        for i, command in enumerate(commands):
            logger.info(f"📊 Pipeline [{i+1}/{len(commands)}]: {command}")
            
            result = await self.execute(command)
            results.append(result)
            
            # Parar se comando falhar
            if not result['success']:
                logger.warning(f"⚠️ Pipeline interrompido no comando {i+1}")
                break
        
        return results
    
    async def check_process(self, process_name: str) -> Dict[str, Any]:
        """Verificar se processo está rodando"""
        try:
            # Buscar processos
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    if process_name.lower() in proc.info['name'].lower():
                        processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cpu_percent': proc.info['cpu_percent'],
                            'memory_percent': proc.info['memory_percent']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            return {
                'found': len(processes) > 0,
                'count': len(processes),
                'processes': processes
            }
            
        except Exception as e:
            return {
                'found': False,
                'error': str(e)
            }
    
    async def manage_service(self, service_name: str, 
                           action: str = "status") -> Dict[str, Any]:
        """Gerenciar serviço do sistema (limitado)"""
        # Apenas permitir ações seguras
        allowed_actions = ["status", "is-active", "is-enabled"]
        
        if action not in allowed_actions:
            return {
                'success': False,
                'error': f"Ação não permitida: {action}"
            }
        
        # Verificar se é um serviço seguro
        safe_services = [
            "ollama", "docker", "nginx", "postgresql",
            "mysql", "redis", "elasticsearch"
        ]
        
        if service_name not in safe_services:
            return {
                'success': False,
                'error': f"Serviço não permitido: {service_name}"
            }
        
        # Executar comando
        command = f"systemctl {action} {service_name}"
        return await self.execute(command)
    
    def _add_to_history(self, result: Dict[str, Any]):
        """Adicionar execução ao histórico"""
        self.execution_history.append(result)
        
        # Limitar tamanho do histórico
        if len(self.execution_history) > self.max_history:
            self.execution_history.pop(0)
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obter histórico de execuções"""
        return self.execution_history[-limit:]
    
    def clear_history(self):
        """Limpar histórico"""
        self.execution_history.clear()
        logger.info("🗑️ Histórico limpo")
    
    def get_stats(self) -> Dict[str, Any]:
        """Obter estatísticas do agente"""
        avg_time = (self.stats['total_execution_time'] / 
                   self.stats['commands_executed'] 
                   if self.stats['commands_executed'] > 0 else 0)
        
        return {
            'commands_executed': self.stats['commands_executed'],
            'commands_blocked': self.stats['commands_blocked'],
            'commands_failed': self.stats['commands_failed'],
            'success_rate': ((self.stats['commands_executed'] - self.stats['commands_failed']) / 
                           self.stats['commands_executed'] 
                           if self.stats['commands_executed'] > 0 else 0),
            'average_execution_time': avg_time,
            'total_execution_time': self.stats['total_execution_time'],
            'sandbox_mode': self.sandbox_mode,
            'work_directory': str(self.work_dir)
        }
    
    async def health_check(self) -> bool:
        """Verificar saúde do agente"""
        try:
            # Testar execução simples
            result = await self.execute("echo 'health check'", timeout=5)
            return result['success']
        except:
            return False
    
    def add_allowed_command(self, command: str):
        """Adicionar comando à whitelist"""
        if command not in self.allowed_commands:
            self.allowed_commands.append(command)
            logger.info(f"✅ Comando '{command}' adicionado à whitelist")
    
    def remove_allowed_command(self, command: str):
        """Remover comando da whitelist"""
        if command in self.allowed_commands:
            self.allowed_commands.remove(command)
            logger.info(f"🗑️ Comando '{command}' removido da whitelist")
    
    async def create_sandbox_file(self, filename: str, content: str) -> Path:
        """Criar arquivo no sandbox"""
        file_path = self.work_dir / filename
        file_path.write_text(content)
        return file_path
    
    async def read_sandbox_file(self, filename: str) -> Optional[str]:
        """Ler arquivo do sandbox"""
        file_path = self.work_dir / filename
        
        if file_path.exists():
            return file_path.read_text()
        return None
    
    def list_sandbox_files(self) -> List[str]:
        """Listar arquivos no sandbox"""
        return [f.name for f in self.work_dir.iterdir() if f.is_file()]


# Teste do agente
async def test_execution_agent():
    """Testar o Execution Agent"""
    print("🧪 Testando Execution Agent...")
    
    agent = ExecutionAgent(sandbox_mode=True)
    
    # Teste 1: Comando permitido
    print("\n1️⃣ Testando comando permitido...")
    result = await agent.execute("echo 'Hello DigiMundo!'")
    print(f"   Sucesso: {result['success']}")
    print(f"   Output: {result.get('stdout', '').strip()}")
    
    # Teste 2: Comando bloqueado
    print("\n2️⃣ Testando comando bloqueado...")
    result = await agent.execute("rm -rf /")
    print(f"   Bloqueado: {result.get('blocked', False)}")
    print(f"   Erro: {result.get('error', '')}")
    
    # Teste 3: Script Python
    print("\n3️⃣ Testando script Python...")
    script = """
print("DigiMundo Script Test")
for i in range(3):
    print(f"Iteration {i+1}")
"""
    result = await agent.execute_script(script, language="python")
    print(f"   Sucesso: {result['success']}")
    
    # Teste 4: Pipeline
    print("\n4️⃣ Testando pipeline...")
    pipeline = [
        "echo 'Step 1'",
        "echo 'Step 2'",
        "echo 'Step 3'"
    ]
    results = await agent.execute_pipeline(pipeline)
    print(f"   Comandos executados: {len(results)}")
    
    # Teste 5: Estatísticas
    print("\n5️⃣ Estatísticas:")
    stats = agent.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Testes concluídos!")


if __name__ == "__main__":
    asyncio.run(test_execution_agent())
