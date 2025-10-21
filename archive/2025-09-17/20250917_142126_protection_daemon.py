#!/usr/bin/env python3
"""
🛡️ PROTECTION DAEMON - Proteção Total Contra Bash
==================================================
Daemon que monitora e bloqueia acessos não autorizados
"""

import os
import sys
import json
import time
import signal
import hashlib
import threading
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psutil

PROTECTED_DIR = "/Users/clubproducoes/Digimundo/scripturemon-champion"
CLAUDE_CODE_DIR = "/Users/clubproducoes/Digimundo/claude_code"
DAEMON_PID_FILE = Path(CLAUDE_CODE_DIR) / "protection/.daemon.pid"
DAEMON_LOG = Path(CLAUDE_CODE_DIR) / "protection/daemon.log"
SESSION_FILE = Path(CLAUDE_CODE_DIR) / ".daemon_session"
PASSWORD_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

class FileProtectionHandler(FileSystemEventHandler):
    """Handler para eventos do filesystem"""

    def __init__(self, daemon):
        self.daemon = daemon
        self.protected_operations = set()

    def on_modified(self, event):
        if not event.is_directory:
            self.check_protection(event.src_path, "modified")

    def on_created(self, event):
        if not event.is_directory:
            self.check_protection(event.src_path, "created")

    def on_deleted(self, event):
        if not event.is_directory:
            self.check_protection(event.src_path, "deleted")

    def on_moved(self, event):
        self.check_protection(event.src_path, "moved")
        self.check_protection(event.dest_path, "moved_to")

    def check_protection(self, filepath, operation):
        """Verifica se operação é autorizada"""
        filepath = Path(filepath).resolve()

        # Ignora operações do próprio daemon
        if str(filepath).startswith(str(CLAUDE_CODE_DIR)):
            return

        # Verifica se está no diretório protegido
        if str(filepath).startswith(PROTECTED_DIR):
            # Identifica processo que fez a mudança
            accessor_pid = self.find_accessor_process(filepath)

            if accessor_pid and not self.daemon.is_authorized(accessor_pid):
                self.daemon.block_operation(filepath, operation, accessor_pid)

    def find_accessor_process(self, filepath):
        """Encontra processo que está acessando o arquivo"""
        try:
            # Lista processos com arquivo aberto
            result = subprocess.run(
                ['lsof', str(filepath)],
                capture_output=True,
                text=True
            )

            if result.stdout:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    parts = line.split()
                    if len(parts) > 1:
                        return int(parts[1])  # PID
        except:
            pass

        return None

class ProtectionDaemon:
    """Daemon de proteção principal"""

    def __init__(self):
        self.running = False
        self.observer = None
        self.authorized_pids = set()
        self.blocked_files = {}
        self.session_valid_until = None
        self.monitoring_thread = None

        # Cria diretório de proteção
        Path(CLAUDE_CODE_DIR, "protection").mkdir(parents=True, exist_ok=True)

    def start(self):
        """Inicia o daemon"""
        # Verifica se já está rodando
        if self.is_already_running():
            print("⚠️ Daemon já está em execução")
            return

        print("🚀 Iniciando Protection Daemon...")

        # Salva PID
        with open(DAEMON_PID_FILE, 'w') as f:
            f.write(str(os.getpid()))

        self.running = True

        # Configura handler de sinais
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)

        # Inicia observer do filesystem
        self.start_filesystem_monitor()

        # Inicia monitor de processos
        self.start_process_monitor()

        # Cria arquivos shadow protegidos
        self.create_shadow_protection()

        print("✅ Protection Daemon iniciado")
        self.log("Daemon started")

        # Loop principal
        try:
            while self.running:
                self.check_sessions()
                self.check_blocked_files()
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self, signum=None, frame=None):
        """Para o daemon"""
        print("\n🛑 Parando Protection Daemon...")
        self.running = False

        if self.observer:
            self.observer.stop()
            self.observer.join()

        # Remove PID file
        if DAEMON_PID_FILE.exists():
            DAEMON_PID_FILE.unlink()

        self.log("Daemon stopped")
        print("✅ Daemon parado")
        sys.exit(0)

    def is_already_running(self):
        """Verifica se daemon já está rodando"""
        if DAEMON_PID_FILE.exists():
            try:
                with open(DAEMON_PID_FILE) as f:
                    pid = int(f.read())

                # Verifica se processo existe
                if psutil.pid_exists(pid):
                    return True
            except:
                pass

        return False

    def start_filesystem_monitor(self):
        """Inicia monitoramento do filesystem"""
        event_handler = FileProtectionHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, PROTECTED_DIR, recursive=True)
        self.observer.start()

        self.log(f"Monitoring {PROTECTED_DIR}")

    def start_process_monitor(self):
        """Inicia monitor de processos"""
        def monitor():
            while self.running:
                try:
                    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                        if proc.info['cmdline']:
                            cmdline = ' '.join(proc.info['cmdline'])

                            # Detecta comandos perigosos
                            dangerous = ['rm', 'mv', 'sed', 'awk', 'cat', '>', '>>']

                            for cmd in dangerous:
                                if cmd in cmdline and PROTECTED_DIR in cmdline:
                                    if proc.info['pid'] not in self.authorized_pids:
                                        self.intercept_command(proc.info)
                except:
                    pass

                time.sleep(0.5)

        self.monitoring_thread = threading.Thread(target=monitor, daemon=True)
        self.monitoring_thread.start()

    def intercept_command(self, proc_info):
        """Intercepta comando perigoso"""
        pid = proc_info['pid']
        name = proc_info['name']
        cmdline = ' '.join(proc_info['cmdline'])

        self.log(f"Intercepted dangerous command: PID={pid} CMD={cmdline}")

        # Tenta pausar o processo
        try:
            os.kill(pid, signal.SIGSTOP)  # Pausa processo

            print(f"""
╔════════════════════════════════════════════════════════════╗
║                   🛑 COMANDO BLOQUEADO! 🛑                ║
╠════════════════════════════════════════════════════════════╣
║ Processo: {name:49} ║
║ PID: {pid:54} ║
║ Comando detectado tentando acessar área protegida         ║
╚════════════════════════════════════════════════════════════╝
""")

            # Pede autenticação
            if self.authenticate_interactive():
                self.authorized_pids.add(pid)
                os.kill(pid, signal.SIGCONT)  # Resume processo
                print("✅ Comando autorizado e resumido")
            else:
                os.kill(pid, signal.SIGKILL)  # Mata processo
                print("❌ Comando bloqueado e terminado")

        except:
            pass

    def create_shadow_protection(self):
        """Cria proteção shadow com links simbólicos"""
        shadow_dir = Path(CLAUDE_CODE_DIR) / "protection/shadow"
        shadow_dir.mkdir(exist_ok=True)

        # Cria shadow copies dos arquivos importantes
        for filepath in Path(PROTECTED_DIR).glob("*.py"):
            if filepath.is_file():
                shadow_path = shadow_dir / filepath.name

                # Cria hardlink (mesmo inode)
                if not shadow_path.exists():
                    try:
                        os.link(filepath, shadow_path)
                        self.log(f"Shadow link created: {filepath.name}")
                    except:
                        pass

    def block_operation(self, filepath, operation, pid):
        """Bloqueia operação não autorizada"""
        # Registra tentativa
        self.blocked_files[str(filepath)] = {
            'operation': operation,
            'pid': pid,
            'time': datetime.now().isoformat(),
            'blocked': True
        }

        self.log(f"BLOCKED: {operation} on {filepath} by PID {pid}")

        # Tenta reverter operação
        if operation == "deleted":
            self.restore_from_shadow(filepath)
        elif operation in ["modified", "created"]:
            self.quarantine_file(filepath)

        print(f"""
🚫 OPERAÇÃO BLOQUEADA!
Arquivo: {filepath}
Operação: {operation}
PID: {pid}
""")

    def restore_from_shadow(self, filepath):
        """Restaura arquivo da shadow copy"""
        shadow_dir = Path(CLAUDE_CODE_DIR) / "protection/shadow"
        shadow_file = shadow_dir / Path(filepath).name

        if shadow_file.exists():
            try:
                shutil.copy2(shadow_file, filepath)
                self.log(f"Restored {filepath} from shadow")
                print(f"✅ Arquivo restaurado: {filepath}")
            except:
                pass

    def quarantine_file(self, filepath):
        """Move arquivo suspeito para quarentena"""
        quarantine_dir = Path(CLAUDE_CODE_DIR) / "protection/quarantine"
        quarantine_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        quarantine_path = quarantine_dir / f"{timestamp}_{Path(filepath).name}"

        try:
            shutil.move(str(filepath), str(quarantine_path))
            self.log(f"Quarantined {filepath}")
            print(f"🔒 Arquivo em quarentena: {quarantine_path}")
        except:
            pass

    def is_authorized(self, pid):
        """Verifica se PID está autorizado"""
        # Verifica sessão
        if not self.check_session_valid():
            return False

        return pid in self.authorized_pids

    def check_session_valid(self):
        """Verifica se sessão ainda é válida"""
        if SESSION_FILE.exists():
            try:
                with open(SESSION_FILE) as f:
                    data = json.load(f)
                expiry = datetime.fromisoformat(data['valid_until'])

                if datetime.now() < expiry:
                    return True
            except:
                pass

        return False

    def authenticate_interactive(self):
        """Autenticação interativa"""
        print("\n🔐 AUTENTICAÇÃO REQUERIDA")

        import getpass
        password = getpass.getpass("Senha: ")

        if hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH:
            # Cria sessão de 15 segundos
            session_data = {
                'valid_until': (datetime.now() + timedelta(seconds=15)).isoformat(),
                'pids': list(self.authorized_pids)
            }

            with open(SESSION_FILE, 'w') as f:
                json.dump(session_data, f)

            print("✅ Autenticado! Sessão de 15 segundos.")
            return True

        print("❌ Senha incorreta")
        return False

    def check_sessions(self):
        """Verifica e limpa sessões expiradas"""
        if self.session_valid_until:
            if datetime.now() > self.session_valid_until:
                self.authorized_pids.clear()
                self.session_valid_until = None
                self.log("Session expired, cleared authorized PIDs")

    def check_blocked_files(self):
        """Verifica arquivos bloqueados"""
        # Limpa entradas antigas (mais de 1 hora)
        current_time = datetime.now()
        to_remove = []

        for filepath, info in self.blocked_files.items():
            block_time = datetime.fromisoformat(info['time'])
            if (current_time - block_time).seconds > 3600:
                to_remove.append(filepath)

        for filepath in to_remove:
            del self.blocked_files[filepath]

    def log(self, message):
        """Registra log"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}\n"

        with open(DAEMON_LOG, 'a') as f:
            f.write(log_entry)

# ═══════════════════════════════════════════════════════════════
# COMANDOS DE CONTROLE
# ═══════════════════════════════════════════════════════════════

def daemon_status():
    """Verifica status do daemon"""
    if DAEMON_PID_FILE.exists():
        with open(DAEMON_PID_FILE) as f:
            pid = int(f.read())

        if psutil.pid_exists(pid):
            print(f"✅ Daemon rodando (PID: {pid})")
            return True

    print("❌ Daemon não está rodando")
    return False

def start_daemon():
    """Inicia o daemon em background"""
    if daemon_status():
        return

    print("Iniciando daemon em background...")

    # Fork para criar processo daemon
    pid = os.fork()

    if pid > 0:
        # Processo pai
        print(f"✅ Daemon iniciado (PID: {pid})")
        return

    # Processo filho (daemon)
    os.setsid()  # Cria nova sessão
    daemon = ProtectionDaemon()
    daemon.start()

def stop_daemon():
    """Para o daemon"""
    if DAEMON_PID_FILE.exists():
        with open(DAEMON_PID_FILE) as f:
            pid = int(f.read())

        try:
            os.kill(pid, signal.SIGTERM)
            print("✅ Daemon parado")
        except:
            print("❌ Erro ao parar daemon")
    else:
        print("Daemon não está rodando")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "start":
            daemon = ProtectionDaemon()
            daemon.start()
        elif command == "stop":
            stop_daemon()
        elif command == "status":
            daemon_status()
        elif command == "background":
            start_daemon()
        else:
            print("Uso: protection_daemon.py [start|stop|status|background]")
    else:
        print("""
╔════════════════════════════════════════════════════════════╗
║              🛡️ PROTECTION DAEMON                          ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Daemon que monitora e protege o diretório                ║
║  scripturemon-champion contra acessos não autorizados     ║
║                                                            ║
║  Comandos:                                                ║
║    start      - Inicia daemon em foreground               ║
║    background - Inicia daemon em background               ║
║    stop       - Para o daemon                             ║
║    status     - Verifica status                           ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
""")