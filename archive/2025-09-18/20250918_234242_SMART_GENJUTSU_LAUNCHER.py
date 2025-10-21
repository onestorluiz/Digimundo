#!/usr/bin/env python3
"""
🧠 SMART GENJUTSU LAUNCHER - Sistema Inteligente de Proteção
=============================================================
Detecta estado do Claude e ajusta Genjutsu dinamicamente
"""

import subprocess
import time
import os
import sys
from datetime import datetime

class SmartGenjutsuLauncher:
    def __init__(self):
        self.genjutsu_minimal = "/Users/clubproducoes/Digimundo/claude_code/protection/genjutsu/GENJUTSU_MINIMAL.py"
        self.genjutsu_detector = "/Users/clubproducoes/Digimundo/claude_code/protection/genjutsu/GENJUTSU_COMPACT_DETECTOR.py"
        self.current_mode = None
        self.current_process = None

    def check_claude_activity(self):
        """
        Verifica sinais de atividade do Claude
        Pode ser expandido para monitorar:
        - Modificações em arquivos
        - Processos Python ativos
        - Uso de CPU
        """
        # Por ora, monitora se há processos python3 rodando (Claude executando código)
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            python_processes = [line for line in result.stdout.split('\n')
                              if 'python' in line and 'claude' not in line.lower()]
            return len(python_processes) > 5  # Ativo se muitos processos Python
        except:
            return False

    def is_compacting_likely(self):
        """
        Detecta sinais de que pode estar compactando:
        - Pouca atividade
        - Tempo desde última interação
        - Padrões de uso de memória
        """
        # Verifica uso de memória/CPU do Claude (simplificado)
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)

            # Se tem processo com "compact" ou similar no nome
            if 'compact' in result.stdout.lower():
                return True

            # Se não há muita atividade Python
            if not self.check_claude_activity():
                return True

            return False
        except:
            return False

    def kill_current_genjutsu(self):
        """Mata processo Genjutsu atual"""
        if self.current_process:
            try:
                self.current_process.terminate()
                time.sleep(0.5)
                self.current_process.kill()
            except:
                pass
            self.current_process = None

        # Mata qualquer Genjutsu órfão
        subprocess.run(['pkill', '-f', 'GENJUTSU'], stderr=subprocess.DEVNULL)

    def start_genjutsu(self, mode="normal"):
        """Inicia Genjutsu no modo apropriado"""
        self.kill_current_genjutsu()

        if mode == "detector":
            script = self.genjutsu_detector
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔴 Modo DETECTOR - Possível compactação!")
        else:
            script = self.genjutsu_minimal
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🟢 Modo NORMAL - Sistema estável")

        try:
            self.current_process = subprocess.Popen(
                ['python3', script],
                stdout=subprocess.DEVNULL,
                stderr=None  # Deixa stderr visível para ver mensagens
            )
            self.current_mode = mode
            return True
        except Exception as e:
            print(f"❌ Erro ao iniciar Genjutsu: {e}")
            return False

    def run(self):
        """Loop principal do launcher inteligente"""
        print("🧠 SMART GENJUTSU LAUNCHER INICIADO")
        print("="*50)
        print("Monitorando estado do sistema...\n")

        check_interval = 30  # Verifica a cada 30 segundos
        compacting_counter = 0

        while True:
            try:
                # Verifica se está compactando
                if self.is_compacting_likely():
                    compacting_counter += 1

                    if compacting_counter >= 2:  # 2 checks = 1 minuto suspeito
                        if self.current_mode != "detector":
                            print("\n⚠️ Sinais de compactação detectados!")
                            print("Mudando para modo DETECTOR...")
                            self.start_genjutsu("detector")
                        compacting_counter = 0
                else:
                    compacting_counter = 0

                    if self.current_mode != "normal":
                        print("\n✅ Sistema normal detectado")
                        print("Voltando para modo NORMAL...")
                        self.start_genjutsu("normal")

                # Verifica se Genjutsu ainda está rodando
                if self.current_process and self.current_process.poll() is not None:
                    print("\n⚠️ Genjutsu morreu! Reiniciando...")
                    self.start_genjutsu(self.current_mode or "normal")

                time.sleep(check_interval)

            except KeyboardInterrupt:
                print("\n👋 Smart Genjutsu Launcher encerrado")
                self.kill_current_genjutsu()
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
                time.sleep(5)

if __name__ == "__main__":
    launcher = SmartGenjutsuLauncher()
    launcher.run()