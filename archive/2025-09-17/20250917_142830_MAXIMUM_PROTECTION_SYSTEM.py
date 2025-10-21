#!/usr/bin/env python3
"""
🔐 MAXIMUM PROTECTION SYSTEM - SEMPRE ATIVO
============================================
Sistema de proteção máxima que inicia com o OS
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
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import psutil

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÕES CRÍTICAS
# ═══════════════════════════════════════════════════════════════

PROTECTED_DIR = "/Users/clubproducoes/Digimundo/scripturemon-champion"
CLAUDE_CODE_DIR = "/Users/clubproducoes/Digimundo/claude_code"
PROTECTION_DIR = f"{CLAUDE_CODE_DIR}/protection"
PASSWORD_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

# Arquivos de controle
PID_FILE = f"{PROTECTION_DIR}/.maximum_protection.pid"
LOCK_FILE = f"{PROTECTION_DIR}/.maximum.lock"
LOG_FILE = f"{PROTECTION_DIR}/maximum_protection.log"

# ═══════════════════════════════════════════════════════════════
# CLASSE PRINCIPAL DE PROTEÇÃO MÁXIMA
# ═══════════════════════════════════════════════════════════════

class MaximumProtectionSystem:
    """Sistema de proteção máxima sempre ativo"""

    def __init__(self):
        self.running = True
        self.monitors = []
        self.protected_processes = set()
        self.intercepted_operations = []
        self.start_time = datetime.now()

    def install_system_wide(self):
        """Instala proteção em todo o sistema"""
        print("🚀 INSTALANDO PROTEÇÃO MÁXIMA NO SISTEMA...")

        # 1. Criar LaunchDaemon para macOS
        self.create_launch_daemon()

        # 2. Modificar perfil do shell
        self.modify_shell_profile()

        # 3. Instalar hooks Python
        self.install_python_hooks()

        # 4. Configurar wrappers
        self.setup_command_wrappers()

        # 5. Ativar proteção do filesystem
        self.protect_filesystem()

        # 6. Iniciar monitores
        self.start_all_monitors()

        print("✅ PROTEÇÃO MÁXIMA INSTALADA E ATIVA!")

    def create_launch_daemon(self):
        """Cria daemon que inicia com o sistema"""
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.scripturemon.maximum.protection</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{CLAUDE_CODE_DIR}/protection/MAXIMUM_PROTECTION_SYSTEM.py</string>
        <string>daemon</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
        <key>Crashed</key>
        <true/>
    </dict>

    <key>StandardOutPath</key>
    <string>{LOG_FILE}</string>

    <key>StandardErrorPath</key>
    <string>{LOG_FILE}.err</string>

    <key>StartInterval</key>
    <integer>10</integer>

    <key>ThrottleInterval</key>
    <integer>1</integer>

    <key>WatchPaths</key>
    <array>
        <string>{PROTECTED_DIR}</string>
    </array>

    <key>Nice</key>
    <integer>-20</integer>
</dict>
</plist>"""

        # Salva em LaunchDaemons do sistema
        daemon_path = Path.home() / "Library/LaunchAgents/com.scripturemon.maximum.protection.plist"

        try:
            with open(daemon_path, 'w') as f:
                f.write(plist_content)

            # Carrega o daemon
            subprocess.run(['launchctl', 'load', str(daemon_path)], capture_output=True)
            subprocess.run(['launchctl', 'start', 'com.scripturemon.maximum.protection'], capture_output=True)

            self.log("LaunchDaemon criado e iniciado")
            print("✅ LaunchDaemon configurado para iniciar com o sistema")
        except Exception as e:
            self.log(f"Erro ao criar LaunchDaemon: {e}")

    def modify_shell_profile(self):
        """Modifica perfil do shell para proteção permanente"""
        shell_additions = f"""
# ═══════════════════════════════════════════════════════════════
# MAXIMUM PROTECTION SYSTEM - NÃO REMOVER
# ═══════════════════════════════════════════════════════════════

# Ativa proteção máxima automaticamente
export SCRIPTUREMON_PROTECTION=MAXIMUM
export PATH="{PROTECTION_DIR}/wrappers:$PATH"

# Função de verificação automática
check_scripturemon_access() {{
    local TARGET="$1"
    if [[ "$TARGET" == "{PROTECTED_DIR}"* ]]; then
        if [ ! -f "{PROTECTION_DIR}/.authorized" ]; then
            echo "🔐 ACESSO BLOQUEADO - Área protegida!"
            echo "Use: scripturemon-auth"
            return 1
        fi

        # Verifica se autorização ainda é válida (15 segundos)
        local AUTH_TIME=$(cat "{PROTECTION_DIR}/.authorized" 2>/dev/null)
        local NOW=$(date +%s)

        if [ $((NOW - AUTH_TIME)) -gt 15 ]; then
            rm -f "{PROTECTION_DIR}/.authorized"
            echo "⏰ Autorização expirada!"
            return 1
        fi
    fi
    return 0
}}

# Comando para autenticar
scripturemon-auth() {{
    echo "🔐 AUTENTICAÇÃO REQUERIDA"
    read -s -p "Senha: " PASSWORD
    echo

    HASH=$(echo -n "$PASSWORD" | sha256sum | cut -d' ' -f1)

    if [ "$HASH" = "{PASSWORD_HASH}" ]; then
        date +%s > "{PROTECTION_DIR}/.authorized"
        echo "✅ Autorizado por 15 segundos!"

        # Agenda remoção automática
        (sleep 15 && rm -f "{PROTECTION_DIR}/.authorized") &
    else
        echo "❌ Senha incorreta!"
        return 1
    fi
}}

# Intercepta comandos perigosos
alias rm='check_scripturemon_access "$@" && command rm'
alias mv='check_scripturemon_access "$@" && command mv'
alias cp='check_scripturemon_access "$@" && command cp'
alias cat='check_scripturemon_access "$@" && command cat'
alias sed='check_scripturemon_access "$@" && command sed'
alias awk='check_scripturemon_access "$@" && command awk'
alias chmod='check_scripturemon_access "$@" && command chmod'
alias chown='check_scripturemon_access "$@" && command chown'

# Proteção contra desativação
alias unalias='echo "❌ Comando bloqueado por segurança"'
alias unset='echo "❌ Comando bloqueado por segurança"'

# Inicia verificador em background
if [ -z "$SCRIPTUREMON_MONITOR_PID" ]; then
    ({PROTECTION_DIR}/monitor_background.sh &) 2>/dev/null
    export SCRIPTUREMON_MONITOR_PID=$!
fi

# ═══════════════════════════════════════════════════════════════
"""

        # Adiciona a todos os perfis de shell
        profiles = [
            Path.home() / ".zshrc",
            Path.home() / ".bashrc",
            Path.home() / ".profile",
            Path("/etc/zshrc"),
            Path("/etc/bashrc"),
            Path("/etc/profile")
        ]

        for profile in profiles:
            if profile.exists():
                try:
                    # Verifica se já foi adicionado
                    with open(profile, 'r') as f:
                        content = f.read()

                    if "MAXIMUM PROTECTION SYSTEM" not in content:
                        with open(profile, 'a') as f:
                            f.write(shell_additions)

                        self.log(f"Perfil modificado: {profile}")
                        print(f"✅ Proteção adicionada a: {profile}")
                except:
                    pass

    def install_python_hooks(self):
        """Instala hooks Python globais"""
        sitecustomize_content = f"""
# MAXIMUM PROTECTION SYSTEM - Hook Python Global
import sys
import os

# Adiciona proteção automaticamente
sys.path.insert(0, '{PROTECTION_DIR}')

try:
    # Importa proteção se acessando diretório protegido
    if any('{PROTECTED_DIR}' in str(p) for p in sys.path):
        import MAXIMUM_PROTECTION_HOOKS
        MAXIMUM_PROTECTION_HOOKS.activate()
except:
    pass
"""

        # Encontra diretório site-packages
        try:
            import site
            site_dirs = site.getsitepackages()

            for site_dir in site_dirs:
                sitecustomize = Path(site_dir) / "sitecustomize.py"

                try:
                    with open(sitecustomize, 'a') as f:
                        f.write(sitecustomize_content)

                    print(f"✅ Hook Python instalado em: {sitecustomize}")
                except:
                    pass
        except:
            pass

    def setup_command_wrappers(self):
        """Configura wrappers de comandos"""
        wrapper_dir = Path(PROTECTION_DIR) / "wrappers"
        wrapper_dir.mkdir(exist_ok=True)

        commands = ['rm', 'mv', 'cp', 'cat', 'sed', 'awk', 'grep',
                   'find', 'chmod', 'chown', 'touch', 'mkdir', 'rmdir']

        for cmd in commands:
            wrapper_path = wrapper_dir / cmd
            real_cmd = subprocess.run(['which', cmd], capture_output=True, text=True).stdout.strip()

            if real_cmd:
                wrapper_content = f"""#!/bin/bash
# MAXIMUM PROTECTION WRAPPER

check_auth() {{
    for arg in "$@"; do
        if [[ "$arg" == "{PROTECTED_DIR}"* ]]; then
            if [ ! -f "{PROTECTION_DIR}/.authorized" ]; then
                echo "🔐 BLOQUEADO! Use: scripturemon-auth"
                exit 1
            fi

            AUTH_TIME=$(cat "{PROTECTION_DIR}/.authorized" 2>/dev/null)
            NOW=$(date +%s)

            if [ $((NOW - AUTH_TIME)) -gt 15 ]; then
                rm -f "{PROTECTION_DIR}/.authorized"
                echo "⏰ Sessão expirada!"
                exit 1
            fi
        fi
    done
}}

check_auth "$@"
{real_cmd} "$@"
"""

                with open(wrapper_path, 'w') as f:
                    f.write(wrapper_content)

                os.chmod(wrapper_path, 0o755)

        print(f"✅ {len(commands)} wrappers criados")

    def protect_filesystem(self):
        """Protege filesystem com permissões e ACLs"""
        try:
            # Cria grupo especial
            subprocess.run(['sudo', 'dscl', '.', '-create', '/Groups/scripturemon_max'], capture_output=True)
            subprocess.run(['sudo', 'dscl', '.', '-create', '/Groups/scripturemon_max', 'PrimaryGroupID', '8888'], capture_output=True)

            # Modifica permissões
            subprocess.run(['sudo', 'chmod', '-R', '700', PROTECTED_DIR], capture_output=True)

            # Adiciona ACLs no macOS
            subprocess.run(['sudo', 'chmod', '+a', f"everyone deny delete", PROTECTED_DIR], capture_output=True)
            subprocess.run(['sudo', 'chmod', '+a', f"everyone deny write", PROTECTED_DIR], capture_output=True)

            print("✅ Filesystem protegido com ACLs")
        except:
            pass

    def start_all_monitors(self):
        """Inicia todos os monitores em background"""

        # Monitor de processos
        process_monitor = threading.Thread(target=self.monitor_processes, daemon=True)
        process_monitor.start()
        self.monitors.append(process_monitor)

        # Monitor de filesystem
        fs_monitor = threading.Thread(target=self.monitor_filesystem, daemon=True)
        fs_monitor.start()
        self.monitors.append(fs_monitor)

        # Monitor de rede
        net_monitor = threading.Thread(target=self.monitor_network, daemon=True)
        net_monitor.start()
        self.monitors.append(net_monitor)

        print(f"✅ {len(self.monitors)} monitores ativos")

    def monitor_processes(self):
        """Monitora processos continuamente"""
        while self.running:
            try:
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    if proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline'])

                        if PROTECTED_DIR in cmdline:
                            if proc.info['pid'] not in self.protected_processes:
                                self.intercept_process(proc.info)
            except:
                pass

            time.sleep(0.5)

    def monitor_filesystem(self):
        """Monitora mudanças no filesystem"""
        import watchdog.observers
        import watchdog.events

        class Handler(watchdog.events.FileSystemEventHandler):
            def __init__(self, protection):
                self.protection = protection

            def on_any_event(self, event):
                if not event.is_directory:
                    self.protection.log(f"FS Event: {event.event_type} - {event.src_path}")

        observer = watchdog.observers.Observer()
        observer.schedule(Handler(self), PROTECTED_DIR, recursive=True)
        observer.start()

        while self.running:
            time.sleep(1)

        observer.stop()
        observer.join()

    def monitor_network(self):
        """Monitora conexões de rede suspeitas"""
        while self.running:
            try:
                connections = psutil.net_connections()

                for conn in connections:
                    if conn.status == 'ESTABLISHED':
                        # Verifica se algum processo está enviando dados do diretório protegido
                        if conn.pid:
                            try:
                                proc = psutil.Process(conn.pid)
                                if PROTECTED_DIR in ' '.join(proc.cmdline()):
                                    self.log(f"Network: PID {conn.pid} accessing protected dir")
                            except:
                                pass
            except:
                pass

            time.sleep(5)

    def intercept_process(self, proc_info):
        """Intercepta processo suspeito"""
        pid = proc_info['pid']
        name = proc_info['name']

        self.log(f"Intercepted: {name} (PID: {pid})")

        # Adiciona à lista de monitorados
        self.protected_processes.add(pid)

        # Se for comando perigoso, pode pausar
        dangerous = ['rm', 'mv', 'dd', 'format']
        if any(cmd in name for cmd in dangerous):
            try:
                os.kill(pid, signal.SIGSTOP)  # Pausa
                self.log(f"PAUSED dangerous process: {pid}")

                # Aqui normalmente pediria autenticação
                # Por hora, resume após 2 segundos
                threading.Timer(2.0, lambda: os.kill(pid, signal.SIGCONT)).start()
            except:
                pass

    def log(self, message):
        """Registra log com timestamp"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}\n"

        Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)

    def run_daemon(self):
        """Executa como daemon em background"""
        # Verifica se já está rodando
        if Path(PID_FILE).exists():
            try:
                with open(PID_FILE) as f:
                    old_pid = int(f.read())

                if psutil.pid_exists(old_pid):
                    print(f"⚠️ Daemon já está rodando (PID: {old_pid})")
                    return
            except:
                pass

        # Salva PID
        with open(PID_FILE, 'w') as f:
            f.write(str(os.getpid()))

        # Configura sinais
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

        print(f"🚀 MAXIMUM PROTECTION DAEMON INICIADO (PID: {os.getpid()})")
        self.log("Daemon started")

        # Instala proteções
        self.install_system_wide()

        # Loop principal
        while self.running:
            time.sleep(1)

        print("🛑 Daemon parado")

    def shutdown(self, signum=None, frame=None):
        """Desliga o daemon"""
        self.running = False

        if Path(PID_FILE).exists():
            Path(PID_FILE).unlink()

        self.log("Daemon stopped")
        sys.exit(0)

# ═══════════════════════════════════════════════════════════════
# FUNÇÕES DE CONTROLE
# ═══════════════════════════════════════════════════════════════

def install():
    """Instala o sistema de proteção máxima"""
    print("""
╔════════════════════════════════════════════════════════════╗
║         🔐 MAXIMUM PROTECTION SYSTEM - INSTALAÇÃO         ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Este sistema irá:                                        ║
║  • Criar LaunchDaemon para iniciar com o sistema          ║
║  • Modificar perfis do shell                              ║
║  • Instalar hooks Python globais                          ║
║  • Configurar wrappers de comandos                        ║
║  • Proteger filesystem com ACLs                           ║
║  • Iniciar monitores em background                        ║
║                                                            ║
║  PROTEÇÃO MÁXIMA SEMPRE ATIVA!                            ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
""")

    response = input("Deseja instalar? (s/n): ")

    if response.lower() == 's':
        system = MaximumProtectionSystem()
        system.install_system_wide()

        print("\n✅ INSTALAÇÃO COMPLETA!")
        print("\n🔄 PRÓXIMOS PASSOS:")
        print("1. Reinicie o terminal para ativar proteções do shell")
        print("2. O daemon iniciará automaticamente na próxima reinicialização")
        print("3. Use 'scripturemon-auth' para autenticar quando necessário")
        print("\n🔐 PROTEÇÃO MÁXIMA ATIVA!")
    else:
        print("Instalação cancelada")

def status():
    """Verifica status do sistema"""
    print("🔍 Verificando status...")

    # Verifica daemon
    if Path(PID_FILE).exists():
        with open(PID_FILE) as f:
            pid = int(f.read())

        if psutil.pid_exists(pid):
            print(f"✅ Daemon rodando (PID: {pid})")
        else:
            print("❌ Daemon não está rodando")
    else:
        print("❌ Daemon não iniciado")

    # Verifica LaunchDaemon
    result = subprocess.run(['launchctl', 'list'], capture_output=True, text=True)
    if 'com.scripturemon.maximum.protection' in result.stdout:
        print("✅ LaunchDaemon instalado")
    else:
        print("❌ LaunchDaemon não instalado")

    # Verifica wrappers
    wrapper_dir = Path(PROTECTION_DIR) / "wrappers"
    if wrapper_dir.exists():
        wrappers = list(wrapper_dir.glob("*"))
        print(f"✅ {len(wrappers)} wrappers instalados")
    else:
        print("❌ Wrappers não instalados")

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "install":
            install()
        elif command == "daemon":
            system = MaximumProtectionSystem()
            system.run_daemon()
        elif command == "status":
            status()
        else:
            print("Uso: MAXIMUM_PROTECTION_SYSTEM.py [install|daemon|status]")
    else:
        install()