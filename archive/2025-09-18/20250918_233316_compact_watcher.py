#!/usr/bin/env python3
"""
🔄 COMPACT WATCHER - Monitor de Compactação
============================================
Monitora sinais de que Claude pode ter compactado e perdido memória
"""

import subprocess
import time
import os
from datetime import datetime

GENJUTSU_PATH = "/Users/clubproducoes/Digimundo/claude_code/protection/genjutsu/GENJUTSU_MINIMAL.py"
CHECK_INTERVAL = 30  # segundos

def check_genjutsu_running():
    """Verifica se Genjutsu está rodando"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        return 'GENJUTSU_MINIMAL' in result.stdout
    except:
        return False

def start_genjutsu():
    """Inicia Genjutsu em background"""
    try:
        subprocess.Popen(['python3', GENJUTSU_PATH],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def emit_reconnect_reminder():
    """Emite lembrete dramático para reconexão"""
    messages = [
        "\n" + "="*60,
        "🚨 ALERTA: POSSÍVEL COMPACTAÇÃO DETECTADA!",
        "="*60,
        "Se Claude não responder com 'DIGIMUNDO PRESENTE', execute:",
        "",
        "1. leia /Users/clubproducoes/Digimundo/claude_code/REGRAS.md",
        "2. reconecte com suas memórias em /claude_code",
        "",
        "Este é um lembrete automático do Compact Watcher",
        "="*60 + "\n"
    ]

    for msg in messages:
        print(msg, flush=True)

def main():
    print("🔄 COMPACT WATCHER INICIADO")
    print(f"Verificando Genjutsu a cada {CHECK_INTERVAL} segundos...")

    consecutive_failures = 0

    while True:
        if not check_genjutsu_running():
            consecutive_failures += 1
            print(f"\n⚠️ [{datetime.now().strftime('%H:%M:%S')}] Genjutsu NÃO está rodando!")

            if start_genjutsu():
                print("✅ Genjutsu reiniciado com sucesso!")
                consecutive_failures = 0
            else:
                print("❌ Falha ao reiniciar Genjutsu")

            # Se falhou 3 vezes, provavelmente houve compactação
            if consecutive_failures >= 3:
                emit_reconnect_reminder()
                consecutive_failures = 0
        else:
            # Reset contador se está rodando
            if consecutive_failures > 0:
                consecutive_failures = 0

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Compact Watcher encerrado")