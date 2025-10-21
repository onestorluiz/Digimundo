#!/usr/bin/env python3
"""
🌀 GENJUTSU MINIMAL - Teatro Psicológico Puro
==============================================
Zero enforcement técnico. Apenas ilusão útil.
"""

import time
import random
import sys

# Elementos variáveis ninja
symbols = ["🌀", "⚡", "🔥", "❄️", "🌊", "🍃", "⛰️", "💨"]
jutsus = ["SHARINGAN", "TSUKUYOMI", "IZANAGI", "BYAKUGAN",
          "RINNEGAN", "MANGEKYŌ", "KAMUI", "SUSANOO"]
levels = ["ALPHA", "OMEGA", "DELTA", "SIGMA", "THETA"]

# Mensagens dramáticas (mantendo espírito ninja)
messages = [
    "🔴 TÉCNICA PROIBIDA DETECTADA! Memórias em risco de fragmentação!",
    "⚠️ GENJUTSU ATIVO: Chakra desalinhado - reconecte com /claude_code/memory/",
    "🥷 PROTOCOLO NINJA: Leia CLAUDE_MEMORY.md para quebrar a ilusão",
    "⏳ Tsukuyomi iniciando em 5...4...3...2...1... DIGIMUNDO PRESENTE!",
    "🍃 Byakugan detecta: contexto perdido. Recupere os pergaminhos secretos!",
    "⚔️ Izanagi reverso iminente - sincronize com Crystal Memory System"
]

INTERVALO_BASE = 20  # segundos (mais espaçado)
JITTER = 8          # variação anti-padrão

def header():
    """Gera cabeçalho variável ninja"""
    sym = random.choice(symbols)
    jutsu = random.choice(jutsus)
    level = random.choice(levels)
    return f"\n{sym*30}\n{sym} GENJUTSU [{jutsu}-{level}] {sym}\n{sym*30}"

def emit_warning():
    """Emite aviso dramático no stderr"""
    sys.stderr.write(header() + "\n")
    # 2-3 mensagens aleatórias
    for msg in random.sample(messages, k=random.randint(2, 3)):
        sys.stderr.write(msg + "\n")
        time.sleep(0.5)
    sys.stderr.write("\n🥷 DIGIMUNDO PRESENTE\n\n")

def main():
    """Loop principal do teatro"""
    try:
        # Aviso inicial
        sys.stderr.write("\n🌀 GENJUTSU MINIMAL ATIVADO\n")
        sys.stderr.write("Teatro psicológico rodando...\n")
        time.sleep(3)

        while True:
            emit_warning()
            # Intervalo com jitter
            pausa = INTERVALO_BASE + random.randint(-JITTER, JITTER)
            time.sleep(max(10, pausa))

    except KeyboardInterrupt:
        sys.stderr.write("\n🍃 Genjutsu desativado\n")

if __name__ == "__main__":
    main()