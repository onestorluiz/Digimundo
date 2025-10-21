#!/usr/bin/env python3
"""
🥷 VERSÃO SIMPLES - AUTO CONTINUE
==================================
Versão minimalista que funciona com watchdog
"""

import time
import subprocess
import sys
from pathlib import Path

# Instalar dependências se necessário
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Instalando watchdog...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "watchdog"])
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

class TriggerHandler(FileSystemEventHandler):
    def __init__(self):
        self.trigger_file = Path("/tmp/digimundo_trigger.txt")
        self.last_trigger = 0

    def on_modified(self, event):
        if event.src_path == str(self.trigger_file):
            current_time = time.time()
            if current_time - self.last_trigger > 5:  # Cooldown de 5s
                self.last_trigger = current_time
                print(f"🎯 TRIGGER DETECTADO!")

                # Simular tecla usando osascript (Mac)
                if sys.platform == "darwin":
                    script = '''
                    tell application "Terminal"
                        activate
                        tell application "System Events"
                            keystroke "continue a refatoração"
                            key code 36
                        end tell
                    end tell
                    '''
                    subprocess.run(['osascript', '-e', script])
                    print("✅ Comando enviado!")

def main():
    print("🥷 AUTO-CONTINUE SIMPLES ATIVADO")
    print("="*40)
    print("Para ativar, escreva em: /tmp/digimundo_trigger.txt")
    print("Exemplo: echo 'TRIGGER' > /tmp/digimundo_trigger.txt")
    print("="*40)

    # Criar arquivo trigger se não existe
    trigger_file = Path("/tmp/digimundo_trigger.txt")
    trigger_file.touch()

    # Configurar observer
    event_handler = TriggerHandler()
    observer = Observer()
    observer.schedule(event_handler, '/tmp', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Auto-continue desativado")
    observer.join()

if __name__ == "__main__":
    main()