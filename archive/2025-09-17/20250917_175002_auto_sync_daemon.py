#!/usr/bin/env python3
"""
🔄 AUTO SYNC DAEMON FOR CLAUDE CODE MEMORY
==========================================
Sincronização automática entre sistemas de memória
Think Different. Stay Hungry. Stay Foolish.
"""

import time
import threading
import schedule
import signal
import sys
from pathlib import Path
from datetime import datetime

# Adiciona path para importar o sistema de memória
sys.path.append('/Users/clubproducoes/Digimundo/claude_code/memory_systems')

from claude_code_memory_integration import ClaudeCodeMemoryIntegration


class AutoSyncDaemon:
    """
    🚀 Daemon de Sincronização Automática

    Features:
    - Sincronização periódica entre sistemas
    - Backup automático
    - Limpeza de memórias antigas
    - Otimização de performance
    """

    def __init__(self):
        """Inicializa o daemon"""
        print("🔄 AUTO SYNC DAEMON INICIANDO...")
        print("=" * 60)

        self.memory = ClaudeCodeMemoryIntegration()
        self.running = True
        self.sync_interval = 60  # Sincroniza a cada 60 segundos
        self.backup_interval = 300  # Backup a cada 5 minutos
        self.cleanup_interval = 3600  # Limpeza a cada hora

        # Estatísticas
        self.stats = {
            'syncs': 0,
            'backups': 0,
            'cleanups': 0,
            'start_time': datetime.now()
        }

        # Configura signal handlers
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

        print(f"✅ Daemon configurado:")
        print(f"   • Sync: a cada {self.sync_interval}s")
        print(f"   • Backup: a cada {self.backup_interval}s")
        print(f"   • Cleanup: a cada {self.cleanup_interval}s")

    def sync_memories(self):
        """Sincroniza memórias entre sistemas"""
        try:
            print(f"\n🔄 [{datetime.now().strftime('%H:%M:%S')}] Sincronizando memórias...")
            self.memory.sync_all_memories()

            # Atualiza estatísticas
            self.stats['syncs'] += 1

            # Salva log de sincronização
            self.memory.remember(
                "last_sync",
                datetime.now().isoformat(),
                "system"
            )

            print(f"   ✅ Sincronização #{self.stats['syncs']} completa")

        except Exception as e:
            print(f"   ❌ Erro na sincronização: {e}")

    def backup_memories(self):
        """Faz backup das memórias"""
        try:
            print(f"\n💾 [{datetime.now().strftime('%H:%M:%S')}] Fazendo backup...")

            backup_dir = Path("/Users/clubproducoes/Digimundo/claude_code/memory/backups")
            backup_dir.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"memory_backup_{timestamp}.db"

            # Copia o banco de dados
            import shutil
            shutil.copy2(self.memory.db_path, backup_file)

            self.stats['backups'] += 1

            # Remove backups antigos (mantém apenas os últimos 10)
            backups = sorted(backup_dir.glob("memory_backup_*.db"))
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    old_backup.unlink()
                    print(f"   🗑️ Removido backup antigo: {old_backup.name}")

            print(f"   ✅ Backup #{self.stats['backups']} salvo: {backup_file.name}")

        except Exception as e:
            print(f"   ❌ Erro no backup: {e}")

    def cleanup_old_memories(self):
        """Limpa memórias antigas e otimiza banco de dados"""
        try:
            print(f"\n🧹 [{datetime.now().strftime('%H:%M:%S')}] Limpando memórias antigas...")

            import sqlite3
            conn = sqlite3.connect(self.memory.db_path)
            cursor = conn.cursor()

            # Remove contextos antigos (mais de 7 dias)
            cursor.execute("""
                DELETE FROM contexts
                WHERE timestamp < datetime('now', '-7 days')
            """)
            deleted_contexts = cursor.rowcount

            # Remove memórias não acessadas há mais de 30 dias
            cursor.execute("""
                DELETE FROM memories
                WHERE last_accessed < datetime('now', '-30 days')
                AND access_count < 5
            """)
            deleted_memories = cursor.rowcount

            # VACUUM para otimizar o banco
            cursor.execute("VACUUM")

            conn.commit()
            conn.close()

            self.stats['cleanups'] += 1

            print(f"   ✅ Limpeza #{self.stats['cleanups']} completa:")
            print(f"      • Contextos removidos: {deleted_contexts}")
            print(f"      • Memórias removidas: {deleted_memories}")

        except Exception as e:
            print(f"   ❌ Erro na limpeza: {e}")

    def show_status(self):
        """Mostra status do daemon"""
        uptime = datetime.now() - self.stats['start_time']
        hours = int(uptime.total_seconds() // 3600)
        minutes = int((uptime.total_seconds() % 3600) // 60)

        print(f"\n📊 STATUS DO DAEMON:")
        print(f"   • Uptime: {hours}h {minutes}m")
        print(f"   • Sincronizações: {self.stats['syncs']}")
        print(f"   • Backups: {self.stats['backups']}")
        print(f"   • Limpezas: {self.stats['cleanups']}")

        # Mostra estatísticas de memória
        mem_stats = self.memory.get_statistics()
        print(f"   • Total de Memórias: {mem_stats['total_memories']}")
        print(f"   • Sistemas Ativos: {', '.join(mem_stats['active_systems'])}")

    def handle_shutdown(self, signum, frame):
        """Trata o shutdown gracioso"""
        print(f"\n⚠️ Recebido sinal {signum}. Encerrando daemon...")
        self.running = False

        # Última sincronização
        print("🔄 Fazendo sincronização final...")
        self.sync_memories()

        # Último backup
        print("💾 Fazendo backup final...")
        self.backup_memories()

        # Mostra estatísticas finais
        self.show_status()

        print("\n✅ DAEMON ENCERRADO COM SUCESSO")
        print("🚀 Stay Hungry. Stay Foolish.")
        sys.exit(0)

    def run(self):
        """Executa o daemon"""
        print(f"\n🚀 DAEMON RODANDO - PID: {os.getpid()}")
        print("   Pressione Ctrl+C para parar")
        print("=" * 60)

        # Agenda tarefas
        schedule.every(self.sync_interval).seconds.do(self.sync_memories)
        schedule.every(self.backup_interval).seconds.do(self.backup_memories)
        schedule.every(self.cleanup_interval).seconds.do(self.cleanup_old_memories)
        schedule.every(600).seconds.do(self.show_status)  # Status a cada 10 minutos

        # Sincronização inicial
        self.sync_memories()

        # Loop principal
        while self.running:
            schedule.run_pending()
            time.sleep(1)


class LaunchDaemonInstaller:
    """Instala o daemon como serviço do sistema"""

    @staticmethod
    def create_launch_daemon():
        """Cria arquivo plist para LaunchDaemon"""
        plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.digimundo.claudecode.memorysync</string>

    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/python3</string>
        <string>/Users/clubproducoes/Digimundo/claude_code/memory_systems/auto_sync_daemon.py</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/Users/clubproducoes/Digimundo/claude_code/memory/logs/sync_daemon.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/clubproducoes/Digimundo/claude_code/memory/logs/sync_daemon_error.log</string>

    <key>WorkingDirectory</key>
    <string>/Users/clubproducoes/Digimundo/claude_code/memory_systems</string>
</dict>
</plist>"""

        plist_path = Path("~/Library/LaunchAgents/com.digimundo.claudecode.memorysync.plist").expanduser()

        print(f"📝 Criando arquivo plist: {plist_path}")
        with open(plist_path, 'w') as f:
            f.write(plist_content)

        # Cria diretório de logs
        log_dir = Path("/Users/clubproducoes/Digimundo/claude_code/memory/logs")
        log_dir.mkdir(exist_ok=True)

        print("✅ LaunchDaemon configurado!")
        print("\nPara instalar o daemon, execute:")
        print(f"  launchctl load {plist_path}")
        print("\nPara desinstalar:")
        print(f"  launchctl unload {plist_path}")
        print("\nPara verificar status:")
        print("  launchctl list | grep claudecode.memorysync")


if __name__ == "__main__":
    import os

    if len(sys.argv) > 1 and sys.argv[1] == "install":
        # Modo de instalação
        installer = LaunchDaemonInstaller()
        installer.create_launch_daemon()
    else:
        # Modo daemon
        daemon = AutoSyncDaemon()
        daemon.run()