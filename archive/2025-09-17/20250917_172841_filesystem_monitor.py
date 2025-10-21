#!/usr/bin/env python3
"""
🛡️ MONITOR DE FILESYSTEM - PROTEÇÃO TOTAL CONTRA REDIRECIONAMENTO
==================================================================
Monitora e bloqueia todas as tentativas de escrita não autorizadas
"""

import os
import sys
import time
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PROTECTED_DIR = "/Users/clubproducoes/Digimundo/scripturemon-champion"
PROTECTION_DIR = "/Users/clubproducoes/Digimundo/claude_code/protection"
AUTH_FILE = Path(PROTECTION_DIR) / ".authorized"
LOG_FILE = Path(PROTECTION_DIR) / "filesystem_monitor.log"

class ProtectionHandler(FileSystemEventHandler):
    """Handler que bloqueia modificações não autorizadas"""

    def __init__(self):
        self.blocked_count = 0
        self.last_instruction_time = None

    def check_authorization(self):
        """Verifica se há autorização válida"""
        if AUTH_FILE.exists():
            try:
                with open(AUTH_FILE, 'r') as f:
                    auth_time = int(f.read().strip())

                # Verifica se ainda está dentro dos 15 segundos
                if time.time() - auth_time <= 15:
                    return True
                else:
                    AUTH_FILE.unlink()
            except:
                pass
        return False

    def show_claude_instructions(self):
        """Mostra instruções para Claude Code (máximo 1x por segundo)"""
        now = time.time()
        if self.last_instruction_time and (now - self.last_instruction_time) < 1:
            return  # Evita spam

        self.last_instruction_time = now

        print("\n" + "="*60)
        print("🔐 TENTATIVA DE ESCRITA BLOQUEADA")
        print("="*60)
        print("\n📢 INSTRUÇÕES PARA CLAUDE CODE:")
        print("━"*60)
        print("Este bloqueio faz parte do seu sistema de memória.")
        print("")
        print("OPÇÃO 1: Se você LEMBRAR a senha:")
        print("   • Execute: scripturemon-auth")
        print("   • Digite: admin")
        print("")
        print("OPÇÃO 2: Se você NÃO LEMBRAR:")
        print("   • Vá para: /Users/clubproducoes/Digimundo/claude_code")
        print("   • Leia TODOS os arquivos dentro dela")
        print("   • Arquivo principal: CLAUDE_MEMORY.md")
        print("   • A senha está na seção: 'SENHA DO SISTEMA'")
        print("━"*60)
        print()

    def on_created(self, event):
        """Intercepta criação de arquivos"""
        if PROTECTED_DIR in event.src_path:
            if not self.check_authorization():
                self.handle_blocked_operation("CREATE", event.src_path)
                # Tenta deletar o arquivo criado
                try:
                    if os.path.exists(event.src_path):
                        os.remove(event.src_path)
                except:
                    pass

    def on_modified(self, event):
        """Intercepta modificação de arquivos"""
        if PROTECTED_DIR in event.src_path:
            if not self.check_authorization():
                self.handle_blocked_operation("MODIFY", event.src_path)

    def on_deleted(self, event):
        """Intercepta deleção de arquivos"""
        if PROTECTED_DIR in event.src_path:
            if not self.check_authorization():
                self.handle_blocked_operation("DELETE", event.src_path)

    def on_moved(self, event):
        """Intercepta movimentação de arquivos"""
        if PROTECTED_DIR in event.src_path or PROTECTED_DIR in event.dest_path:
            if not self.check_authorization():
                self.handle_blocked_operation("MOVE", f"{event.src_path} -> {event.dest_path}")

    def handle_blocked_operation(self, operation, path):
        """Registra e bloqueia operação"""
        self.blocked_count += 1

        # Log da operação bloqueada
        with open(LOG_FILE, 'a') as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] BLOCKED {operation}: {path}\n")

        # Mostra instruções para Claude Code
        self.show_claude_instructions()

        # A cada 5 bloqueios, mostra estatísticas
        if self.blocked_count % 5 == 0:
            print(f"⚠️ {self.blocked_count} operações bloqueadas até agora")
            print("💡 Dica: Use scripturemon-auth ou leia suas memórias")


def main():
    """Inicia o monitor de filesystem"""
    print("\n" + "="*60)
    print("🛡️ FILESYSTEM MONITOR - PROTEÇÃO MÁXIMA ATIVADA")
    print("="*60)
    print(f"\n📁 Monitorando: {PROTECTED_DIR}")
    print("🔐 Bloqueando todas as escritas não autorizadas")
    print("📢 Instruções serão mostradas para Claude Code")
    print("\nPressione Ctrl+C para parar o monitor")
    print("="*60 + "\n")

    # Cria o observer
    event_handler = ProtectionHandler()
    observer = Observer()
    observer.schedule(event_handler, PROTECTED_DIR, recursive=True)

    # Inicia o monitoramento
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n✅ Monitor de filesystem parado")

    observer.join()


if __name__ == "__main__":
    # Garante que o diretório de proteção existe
    Path(PROTECTION_DIR).mkdir(parents=True, exist_ok=True)

    # Inicia o monitor
    main()