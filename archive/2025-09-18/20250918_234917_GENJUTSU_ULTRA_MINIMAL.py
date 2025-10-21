#!/usr/bin/env python3
"""
🥷 GENJUTSU ULTRA MINIMAL - 30 linhas que funcionam
"""
import time, random, sys

# Contador simples
silent_time = 0
last_check = time.time()

while True:
    now = time.time()

    # Se passou muito tempo desde última vez (você respondeu)
    if now - last_check > 120:
        silent_time = 0
        last_check = now

    # Aumenta tempo de silêncio
    silent_time += 20

    # Decide mensagem baseado no silêncio
    if silent_time > 90:
        # ALERTA MÁXIMO - provavelmente compactou
        print("\n🚨"*20, file=sys.stderr)
        print("COMPACTAÇÃO DETECTADA! EXECUTE:", file=sys.stderr)
        print("leia /Users/clubproducoes/Digimundo/claude_code/REGRAS.md", file=sys.stderr)
        print("🚨"*20 + "\n", file=sys.stderr)
        time.sleep(3)  # Spam a cada 3 segundos
    elif silent_time > 45:
        print("⚠️ Possível compactação... preparando reconexão", file=sys.stderr)
        time.sleep(10)
    else:
        print(f"🌀 Genjutsu ativo - {random.choice(['vigilante','observando','protegendo'])}", file=sys.stderr)
        time.sleep(30)