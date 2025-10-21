#!/usr/bin/env python3
"""Monitor de progresso da geração do HTML detalhado"""

import time
import re
from pathlib import Path

log_file = "detailed_html.log"

print("=" * 80)
print("📊 MONITOR - Geração HTML Detalhado")
print("=" * 80)
print()

last_size = 0
while True:
    if not Path(log_file).exists():
        print("⏳ Aguardando início...")
        time.sleep(2)
        continue

    with open(log_file, 'r') as f:
        content = f.read()

    # Check if file grew
    current_size = len(content)
    if current_size == last_size and current_size > 100:
        # No growth, might be done or stuck
        if "CONCLUÍDO" in content or "HTML detalhado gerado" in content:
            print()
            print("=" * 80)
            print("✅ GERAÇÃO COMPLETA!")
            print("=" * 80)
            print()

            # Extract file path
            file_match = re.search(r'HTML detalhado gerado: (.+)', content)
            if file_match:
                print(f"📄 Arquivo: {file_match.group(1)}")

            break

    last_size = current_size

    # Count completed specialists
    completed = len(re.findall(r'\[(\d+)/22\].*?✅', content))

    # Find current specialist
    current_matches = re.findall(r'\[(\d+)/22\] Running ([^.]+)', content)
    if current_matches:
        current_num, current_name = current_matches[-1]
        current_num = int(current_num)
    else:
        current_num = 0
        current_name = "Iniciando..."

    # Clear screen
    print("\033[2J\033[H", end="")

    print("=" * 80)
    print("📊 MONITOR - Geração HTML Detalhado com 22 Especialistas")
    print("=" * 80)
    print()

    # Progress bar
    progress = (completed / 22) * 100
    bar_length = 50
    filled = int(bar_length * completed / 22)
    bar = "█" * filled + "░" * (bar_length - filled)

    print(f"Progresso: [{bar}] {completed}/22 ({progress:.1f}%)")
    print()
    print(f"✅ Completados: {completed}/22")
    print(f"⚡ Atual: [{current_num}/22] {current_name}")
    print(f"⏳ Restantes: {22 - completed}")
    print()

    time.sleep(2)

print()
print("Monitor encerrado.")
