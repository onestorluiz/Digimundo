#!/usr/bin/env python3
"""
✨ DETECTOR MINIMALISTA - 15 linhas que resolvem
"""
import time, subprocess

last_active = time.time()

while True:
    # Checa se tem processos Python (Claude trabalhando)
    ps = subprocess.run(['pgrep', '-f', 'python'], capture_output=True)

    if ps.stdout:
        last_active = time.time()

    # Se ficou 90+ segundos parado = compactou
    if time.time() - last_active > 90:
        print("\n🚨 COMPACTAÇÃO PROVÁVEL - 90s de silêncio!")
        print("Execute: leia /Users/clubproducoes/Digimundo/claude_code/REGRAS.md\n")
        last_active = time.time()  # Reset para não spammar

    time.sleep(30)  # Checa a cada 30s (quase zero CPU)