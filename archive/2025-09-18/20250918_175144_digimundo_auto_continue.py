#!/usr/bin/env python3
"""
🥷 DIGIMUNDO AUTO-CONTINUE
==========================
Monitora output do terminal para "DIGIMUNDO PRESENTE"
e automaticamente envia "continue a refatoração"
"""

import subprocess
import time
import sys
import os
from datetime import datetime

# Tentar importar pyautogui (para automação de teclado)
try:
    import pyautogui
except ImportError:
    print("❌ pyautogui não instalado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
    import pyautogui

# Configurar pyautogui para ser mais rápido
pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = True  # Mover mouse para canto superior esquerdo para parar

class DigimundoAutoContinue:
    def __init__(self):
        self.trigger_phrase = "DIGIMUNDO PRESENTE 🥷"
        self.continue_message = "continue a refatoração"
        self.last_trigger = 0
        self.cooldown = 5  # Segundos entre triggers
        self.active = True
        self.trigger_count = 0
        self.max_triggers = 50  # Limite de segurança

    def watch_terminal_output(self, log_file="/tmp/claude_output.log"):
        """Monitora arquivo de log para o trigger"""
        print("🥷 DIGIMUNDO AUTO-CONTINUE ATIVADO")
        print("="*50)
        print(f"📍 Monitorando: {log_file}")
        print(f"🎯 Trigger: '{self.trigger_phrase}'")
        print(f"📝 Mensagem: '{self.continue_message}'")
        print(f"⏱️  Cooldown: {self.cooldown}s")
        print(f"🔒 Limite: {self.max_triggers} triggers")
        print("\n💡 DICA: Para capturar output do Claude:")
        print("   Terminal 1: python3 digimundo_auto_continue.py")
        print("   Terminal 2: claude_session | tee /tmp/claude_output.log")
        print("\n🛑 Para parar: Ctrl+C ou mova mouse para canto superior esquerdo")
        print("="*50)

        # Criar arquivo se não existe
        if not os.path.exists(log_file):
            open(log_file, 'w').close()

        # Monitorar arquivo
        with open(log_file, 'r') as f:
            # Ir para o final do arquivo
            f.seek(0, 2)

            while self.active and self.trigger_count < self.max_triggers:
                line = f.readline()

                if not line:
                    time.sleep(0.1)
                    continue

                # Verificar trigger
                if self.trigger_phrase in line:
                    current_time = time.time()

                    # Verificar cooldown
                    if current_time - self.last_trigger < self.cooldown:
                        print(f"⏸️  Cooldown ativo, aguardando...")
                        continue

                    self.trigger_count += 1
                    self.last_trigger = current_time

                    print(f"\n🎯 [{datetime.now().strftime('%H:%M:%S')}] "
                          f"TRIGGER #{self.trigger_count} DETECTADO!")

                    # Aguardar um pouco para garantir que o terminal está pronto
                    time.sleep(1)

                    # Enviar comando
                    self.send_continue_command()

                    print(f"✅ Comando enviado! "
                          f"({self.max_triggers - self.trigger_count} restantes)")

        print(f"\n🛑 Limite de {self.max_triggers} triggers atingido. Finalizando.")

    def send_continue_command(self):
        """Envia o comando de continuação via pyautogui"""
        try:
            # Método 1: Digitar diretamente
            pyautogui.typewrite(self.continue_message)
            pyautogui.press('enter')

        except Exception as e:
            print(f"❌ Erro ao enviar comando: {e}")

            # Método 2: Usar AppleScript no Mac
            if sys.platform == "darwin":
                self.send_via_applescript()

    def send_via_applescript(self):
        """Método alternativo para Mac usando AppleScript"""
        script = f'''
        tell application "System Events"
            keystroke "{self.continue_message}"
            key code 36
        end tell
        '''
        subprocess.run(['osascript', '-e', script])

    def run_with_file_monitor(self):
        """Método alternativo: monitora arquivo diretamente"""
        try:
            self.watch_terminal_output()
        except KeyboardInterrupt:
            print("\n\n🛑 Auto-continue desativado pelo usuário")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

def main():
    """Entry point principal"""
    auto = DigimundoAutoContinue()

    # Verificar argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            print("🧪 MODO TESTE - Enviando comando em 3 segundos...")
            time.sleep(3)
            auto.send_continue_command()
            print("✅ Teste concluído!")
            return
        elif sys.argv[1] == "--help":
            print("""
DIGIMUNDO AUTO-CONTINUE
=======================

Uso:
  python3 digimundo_auto_continue.py           # Modo normal
  python3 digimundo_auto_continue.py --test    # Testar envio
  python3 digimundo_auto_continue.py --help    # Esta ajuda

Como usar com Claude:
  1. Abra 2 terminais
  2. Terminal 1: python3 digimundo_auto_continue.py
  3. Terminal 2: sua_sessao_claude | tee /tmp/claude_output.log

Ou use com script wrapper:
  ./auto_refactor.sh
            """)
            return

    # Executar monitor
    auto.run_with_file_monitor()

if __name__ == "__main__":
    main()