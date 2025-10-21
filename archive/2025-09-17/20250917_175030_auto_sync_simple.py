#!/usr/bin/env python3
"""
🔄 SIMPLE AUTO SYNC FOR CLAUDE CODE MEMORY
==========================================
Versão simplificada sem dependências externas
"""

import time
import threading
import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.append('/Users/clubproducoes/Digimundo/claude_code/memory_systems')

from claude_code_memory_integration import ClaudeCodeMemoryIntegration


class SimpleAutoSync:
    """Sincronização simples sem bibliotecas externas"""

    def __init__(self):
        print("🔄 SIMPLE AUTO SYNC INICIANDO...")
        self.memory = ClaudeCodeMemoryIntegration()
        self.running = True

        # Intervalos em segundos
        self.sync_interval = 60
        self.backup_interval = 300

    def run_sync(self):
        """Thread de sincronização"""
        while self.running:
            try:
                print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] Sincronizando...")
                self.memory.sync_all_memories()
                stats = self.memory.get_statistics()
                print(f"   ✅ {stats['total_memories']} memórias sincronizadas")
            except Exception as e:
                print(f"   ❌ Erro: {e}")

            time.sleep(self.sync_interval)

    def run_backup(self):
        """Thread de backup"""
        while self.running:
            try:
                backup_dir = Path("/Users/clubproducoes/Digimundo/claude_code/memory/backups")
                backup_dir.mkdir(exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = backup_dir / f"memory_backup_{timestamp}.db"

                import shutil
                shutil.copy2(self.memory.db_path, backup_file)
                print(f"💾 [{datetime.now().strftime('%H:%M:%S')}] Backup salvo: {backup_file.name}")

                # Remove backups antigos
                backups = sorted(backup_dir.glob("memory_backup_*.db"))
                if len(backups) > 10:
                    for old_backup in backups[:-10]:
                        old_backup.unlink()

            except Exception as e:
                print(f"   ❌ Erro no backup: {e}")

            time.sleep(self.backup_interval)

    def start(self):
        """Inicia as threads"""
        print(f"🚀 AUTO SYNC RODANDO - PID: {os.getpid()}")
        print(f"   • Sync: a cada {self.sync_interval}s")
        print(f"   • Backup: a cada {self.backup_interval}s")
        print("   • Ctrl+C para parar")
        print("=" * 60)

        # Inicia threads
        sync_thread = threading.Thread(target=self.run_sync, daemon=True)
        backup_thread = threading.Thread(target=self.run_backup, daemon=True)

        sync_thread.start()
        backup_thread.start()

        # Mantém o programa rodando
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⚠️ Encerrando...")
            self.running = False
            print("✅ AUTO SYNC ENCERRADO")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        # Cria LaunchAgent
        plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.digimundo.claudecode.memorysync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/python3</string>
        <string>/Users/clubproducoes/Digimundo/claude_code/memory_systems/auto_sync_simple.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/clubproducoes/Digimundo/claude_code/memory/logs/sync.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/clubproducoes/Digimundo/claude_code/memory/logs/sync_error.log</string>
</dict>
</plist>"""

        plist_path = Path("~/Library/LaunchAgents/com.digimundo.claudecode.memorysync.plist").expanduser()
        plist_path.parent.mkdir(exist_ok=True)

        # Cria diretório de logs
        Path("/Users/clubproducoes/Digimundo/claude_code/memory/logs").mkdir(exist_ok=True, parents=True)

        with open(plist_path, 'w') as f:
            f.write(plist_content)

        print(f"✅ LaunchAgent criado: {plist_path}")
        print("\nPara ativar:")
        print(f"  launchctl load {plist_path}")
        print("\nPara desativar:")
        print(f"  launchctl unload {plist_path}")
    else:
        # Modo normal
        sync = SimpleAutoSync()
        sync.start()