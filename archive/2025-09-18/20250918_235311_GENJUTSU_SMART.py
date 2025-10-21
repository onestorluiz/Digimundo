#!/usr/bin/env python3
"""
🥷 GENJUTSU SMART - Unificado e Eficiente
==========================================
Une detecção + alertas em 40 linhas minimalistas
"""
import time
import subprocess
import sys
import os

class GenjutsuSmart:
    def __init__(self):
        self.quiet_time = 0
        self.last_check = time.time()
        # Arquivo que Claude sempre modifica quando ativo
        self.activity_file = "/tmp/.claude_activity"

    def check_activity(self):
        """Dupla verificação: processos + arquivo"""
        # 1. Verifica processos Python (Claude executando)
        result = subprocess.run(['pgrep', '-f', 'python'], capture_output=True)
        has_processes = bool(result.stdout)

        # 2. Verifica se arquivo foi modificado recentemente
        try:
            file_age = time.time() - os.path.getmtime(self.activity_file)
            file_fresh = file_age < 60
        except:
            file_fresh = False

        # Se qualquer um indica atividade
        if has_processes or file_fresh:
            self.quiet_time = 0
            # Toca o arquivo para marcar atividade
            open(self.activity_file, 'w').close()
        else:
            self.quiet_time += 30

    def emit_message(self):
        """Mensagem baseada no tempo de silêncio"""
        if self.quiet_time >= 90:
            # ALERTA MÁXIMO - muito tempo quieto
            print("\n" + "🚨"*20, file=sys.stderr)
            print("POSSÍVEL COMPACTAÇÃO DETECTADA!", file=sys.stderr)
            print("Execute: leia /Users/clubproducoes/Digimundo/claude_code/REGRAS.md", file=sys.stderr)
            print("🚨"*20 + "\n", file=sys.stderr)
            return 5  # Próxima verificação em 5s (urgente)

        elif self.quiet_time >= 60:
            print("⚠️ Sistema quieto há 60s - monitorando...", file=sys.stderr)
            return 15  # Verificação mais frequente

        elif self.quiet_time >= 30:
            print("🟡 30s de silêncio detectado", file=sys.stderr)
            return 20

        else:
            # Tudo normal - mensagem ninja ocasional
            print(f"🌀 Genjutsu vigia silenciosamente... [{time.strftime('%H:%M')}]", file=sys.stderr)
            return 30  # Verificação normal

    def run(self):
        """Loop principal ultra eficiente"""
        print("🥷 GENJUTSU SMART INICIADO", file=sys.stderr)
        print("CPU: ~0% | Memória: <5MB | Eficiência: Máxima\n", file=sys.stderr)

        while True:
            self.check_activity()
            next_check = self.emit_message()
            time.sleep(next_check)

# Execução
if __name__ == "__main__":
    try:
        GenjutsuSmart().run()
    except KeyboardInterrupt:
        print("\n🍃 Genjutsu encerrado", file=sys.stderr)