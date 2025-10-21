#!/usr/bin/env python3
"""
🎮 SYSTEM MANAGER - Gerenciador de Inicialização/Parada Automática
Controla todos os subsistemas do Scripturemon incluindo RAG
"""

import os
import sys
import json
import time
import signal
import atexit
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

class SystemManager:
    """Gerenciador principal do sistema"""

    def __init__(self):
        self.pid_file = Path("data/scripturemon.pid")
        self.state_file = Path("data/system_state.json")
        self.log_file = Path("logs/system_manager.log")

        # Criar diretórios
        self.pid_file.parent.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Subsistemas
        self.subsystems = {
            'rag': None,
            'crystal_memory': None,
            'ollama_monitor': None,
            'file_watcher': None
        }

        # Estado
        self.running = False
        self.start_time = None

        # Registrar handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        atexit.register(self.shutdown)

    def _log(self, message: str, level: str = "INFO"):
        """Log com timestamp"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        # Escrever no arquivo
        with open(self.log_file, 'a') as f:
            f.write(log_entry)

        # Também imprimir
        if level == "ERROR":
            print(f"❌ {message}")
        elif level == "WARNING":
            print(f"⚠️ {message}")
        else:
            print(f"ℹ️ {message}")

    def _signal_handler(self, signum, frame):
        """Handler para sinais do sistema"""
        self._log(f"Recebido sinal {signum}, iniciando shutdown...")
        self.shutdown()
        sys.exit(0)

    def check_running(self) -> bool:
        """Verifica se o sistema já está rodando"""
        if self.pid_file.exists():
            try:
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read())

                # Verificar se o processo existe
                os.kill(pid, 0)
                return True
            except (ProcessLookupError, ValueError):
                # PID inválido ou processo não existe
                self.pid_file.unlink(missing_ok=True)
                return False
        return False

    def start(self) -> bool:
        """Inicia todos os subsistemas"""
        if self.check_running():
            self._log("Sistema já está rodando!", "WARNING")
            return False

        self._log("🚀 Iniciando Scripturemon System Manager...")
        self.running = True
        self.start_time = datetime.now()

        # Salvar PID
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))

        # Iniciar subsistemas
        try:
            # 1. Crystal Memory Systems
            self._start_crystal_memory()

            # 2. RAG System
            self._start_rag_system()

            # 3. Ollama Monitor
            self._start_ollama_monitor()

            # 4. File Watcher
            self._start_file_watcher()

            # Salvar estado
            self._save_state()

            self._log("✅ Todos os subsistemas iniciados com sucesso!")
            return True

        except Exception as e:
            self._log(f"Erro ao iniciar subsistemas: {e}", "ERROR")
            self.shutdown()
            return False

    def _start_crystal_memory(self):
        """Inicia sistemas Crystal Memory"""
        self._log("Iniciando Crystal Memory systems...")

        # Importar e inicializar
        from apps.scripturemon.rules_memory import CrystalMemory
        from apps.scripturemon.screenplay_crystal_memory import ScreenplayCrystalMemory

        # Sistema de regras (Claude Code)
        rules_memory = CrystalMemory()
        self.subsystems['crystal_memory'] = {
            'rules': rules_memory,
            'screenplay': ScreenplayCrystalMemory(),
            'status': 'running',
            'started_at': datetime.now().isoformat()
        }

        self._log("   ✅ Crystal Memory inicializado")

    def _start_rag_system(self):
        """Inicia sistema RAG em thread separada"""
        self._log("Iniciando RAG System...")

        def rag_worker():
            """Worker thread para RAG"""
            try:
                from apps.scripturemon.rag_system import RAGSystem

                rag = RAGSystem()

                # Pré-carregar alguns dados se existirem
                screenplay_dir = Path("library/processed")
                if screenplay_dir.exists():
                    count = 0
                    for script_file in screenplay_dir.glob("*.txt")[:5]:  # Primeiros 5
                        try:
                            with open(script_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                            rag.index_screenplay(script_file.stem, content)
                            count += 1
                        except:
                            pass

                    if count > 0:
                        self._log(f"   📚 {count} roteiros pré-indexados no RAG")

                self.subsystems['rag'] = {
                    'instance': rag,
                    'status': 'running',
                    'indexed_count': count,
                    'started_at': datetime.now().isoformat()
                }

            except Exception as e:
                self._log(f"Erro no RAG worker: {e}", "ERROR")

        # Iniciar em thread
        rag_thread = threading.Thread(target=rag_worker, daemon=True)
        rag_thread.start()

        # Aguardar inicialização
        time.sleep(1)
        self._log("   ✅ RAG System inicializado")

    def _start_ollama_monitor(self):
        """Inicia monitoramento do Ollama"""
        self._log("Iniciando Ollama Monitor...")

        def ollama_monitor():
            """Monitora status do Ollama"""
            try:
                from apps.scripturemon.ollama_core import OllamaCore

                ollama = OllamaCore()

                while self.running:
                    try:
                        models = ollama.list_models()
                        scripturemon_models = [m for m in models if 'scripturemon' in m.lower()]

                        self.subsystems['ollama_monitor'] = {
                            'status': 'running',
                            'total_models': len(models),
                            'scripturemon_models': len(scripturemon_models),
                            'last_check': datetime.now().isoformat()
                        }

                    except Exception as e:
                        self.subsystems['ollama_monitor'] = {
                            'status': 'error',
                            'error': str(e),
                            'last_check': datetime.now().isoformat()
                        }

                    # Verificar a cada 30 segundos
                    time.sleep(30)

            except Exception as e:
                self._log(f"Erro no Ollama monitor: {e}", "ERROR")

        # Iniciar em thread
        monitor_thread = threading.Thread(target=ollama_monitor, daemon=True)
        monitor_thread.start()

        self._log("   ✅ Ollama Monitor inicializado")

    def _start_file_watcher(self):
        """Inicia observador de arquivos"""
        self._log("Iniciando File Watcher...")

        def file_watcher():
            """Observa mudanças em arquivos de roteiro"""
            library_dir = Path("library")
            if not library_dir.exists():
                return

            last_check = {}

            while self.running:
                try:
                    for script_file in library_dir.glob("**/*.txt"):
                        mtime = script_file.stat().st_mtime

                        if script_file not in last_check:
                            last_check[script_file] = mtime
                        elif mtime > last_check[script_file]:
                            # Arquivo modificado
                            self._log(f"Arquivo modificado: {script_file.name}")
                            last_check[script_file] = mtime

                            # Re-indexar no RAG se disponível
                            if self.subsystems.get('rag') and self.subsystems['rag'].get('instance'):
                                try:
                                    with open(script_file, 'r', encoding='utf-8') as f:
                                        content = f.read()
                                    self.subsystems['rag']['instance'].index_screenplay(
                                        script_file.stem, content
                                    )
                                    self._log(f"   Re-indexado: {script_file.name}")
                                except:
                                    pass

                except Exception as e:
                    self._log(f"Erro no file watcher: {e}", "ERROR")

                # Verificar a cada 10 segundos
                time.sleep(10)

        # Iniciar em thread
        watcher_thread = threading.Thread(target=file_watcher, daemon=True)
        watcher_thread.start()

        self.subsystems['file_watcher'] = {
            'status': 'running',
            'started_at': datetime.now().isoformat()
        }

        self._log("   ✅ File Watcher inicializado")

    def _save_state(self):
        """Salva estado do sistema"""
        state = {
            'pid': os.getpid(),
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'subsystems': {}
        }

        for name, subsystem in self.subsystems.items():
            if subsystem and isinstance(subsystem, dict):
                # Copiar apenas dados serializáveis
                state['subsystems'][name] = {
                    k: v for k, v in subsystem.items()
                    if k != 'instance' and not callable(v)
                }

        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def shutdown(self):
        """Desliga todos os subsistemas"""
        if not self.running:
            return

        self._log("🛑 Iniciando shutdown do sistema...")
        self.running = False

        # Parar subsistemas
        for name in self.subsystems:
            self._log(f"   Parando {name}...")
            self.subsystems[name] = None

        # Limpar arquivos
        self.pid_file.unlink(missing_ok=True)

        # Salvar estado final
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                state = json.load(f)

            state['shutdown_time'] = datetime.now().isoformat()
            state['status'] = 'stopped'

            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)

        self._log("✅ Sistema desligado com sucesso")

    def status(self) -> Dict[str, Any]:
        """Retorna status do sistema"""
        if not self.check_running():
            return {'status': 'stopped', 'message': 'Sistema não está rodando'}

        # Ler estado
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                state = json.load(f)

            # Calcular uptime
            if state.get('start_time'):
                start = datetime.fromisoformat(state['start_time'])
                uptime = (datetime.now() - start).total_seconds()
                state['uptime_seconds'] = uptime
                state['uptime_human'] = self._format_uptime(uptime)

            return state

        return {'status': 'unknown', 'message': 'Estado não disponível'}

    def _format_uptime(self, seconds: float) -> str:
        """Formata uptime para leitura humana"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"


# CLI simples
def main():
    """CLI para o System Manager"""
    import argparse

    parser = argparse.ArgumentParser(description="Scripturemon System Manager")
    parser.add_argument('action', choices=['start', 'stop', 'status', 'restart'],
                       help="Ação a executar")

    args = parser.parse_args()
    manager = SystemManager()

    if args.action == 'start':
        if manager.start():
            print("\n✅ Sistema iniciado com sucesso!")
            print("Use 'status' para verificar o estado")
            # Manter rodando
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                manager.shutdown()

    elif args.action == 'stop':
        if manager.check_running():
            # Enviar sinal para o processo
            with open(manager.pid_file, 'r') as f:
                pid = int(f.read())
            os.kill(pid, signal.SIGTERM)
            print("✅ Sinal de shutdown enviado")
        else:
            print("⚠️ Sistema não está rodando")

    elif args.action == 'status':
        status = manager.status()
        print("\n📊 STATUS DO SISTEMA")
        print("=" * 50)

        if status.get('status') == 'stopped':
            print("🔴 Sistema parado")
        else:
            print(f"🟢 Sistema rodando (PID: {status.get('pid')})")
            print(f"⏱️ Uptime: {status.get('uptime_human', 'N/A')}")

            if status.get('subsystems'):
                print("\n📦 Subsistemas:")
                for name, info in status['subsystems'].items():
                    if info:
                        status_icon = "🟢" if info.get('status') == 'running' else "🔴"
                        print(f"   {status_icon} {name}: {info.get('status', 'unknown')}")

    elif args.action == 'restart':
        print("🔄 Reiniciando sistema...")
        if manager.check_running():
            with open(manager.pid_file, 'r') as f:
                pid = int(f.read())
            os.kill(pid, signal.SIGTERM)
            time.sleep(2)

        if manager.start():
            print("✅ Sistema reiniciado!")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                manager.shutdown()


if __name__ == "__main__":
    main()