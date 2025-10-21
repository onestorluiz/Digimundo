#!/usr/bin/env python3
"""Monitor de progresso da análise completa"""

import time
import re
from pathlib import Path

log_file = "test_complete_analysis.log"

print("="*80)
print("📊 MONITOR DE PROGRESSO - Complete Analysis")
print("="*80)
print()

while True:
    if not Path(log_file).exists():
        print("⏳ Aguardando início da análise...")
        time.sleep(2)
        continue

    with open(log_file, 'r') as f:
        content = f.read()

    # Count completed specialists
    completed = len(re.findall(r'✅ Score: \d+', content))

    # Find current specialist
    current_matches = re.findall(r'\[(\d+)/22\] Running ([^.]+)\.\.\.', content)
    if current_matches:
        current_num, current_name = current_matches[-1]
        current_num = int(current_num)
    else:
        current_num = 0
        current_name = "Starting..."

    # Extract times
    times = re.findall(r'✅ Score: \d+/\d+ \((\d+\.\d+)s\)', content)

    if times:
        times_float = [float(t) for t in times]
        avg_time = sum(times_float) / len(times_float)
        total_time = sum(times_float)
        remaining = 22 - completed
        est_remaining = remaining * avg_time
    else:
        avg_time = 0
        total_time = 0
        est_remaining = 0

    # Clear screen (simple)
    print("\033[2J\033[H", end="")

    print("="*80)
    print("📊 MONITOR DE PROGRESSO - Triple-Core Complete Analysis")
    print("="*80)
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

    if times:
        print(f"⏱️  Tempo médio por especialista: {avg_time:.1f}s")
        print(f"⏱️  Tempo total até agora: {total_time/60:.1f} min")
        print(f"⏱️  Tempo estimado restante: {est_remaining/60:.1f} min")
        print()

    # Check if completed
    if "ANALYSIS COMPLETE" in content or "TESTE COMPLETO" in content:
        print("="*80)
        print("✅ ANÁLISE COMPLETA!")
        print("="*80)
        print()

        # Show summary if available
        if "Overall Score" in content:
            score_match = re.search(r'Overall Score: ([\d.]+)/100', content)
            if score_match:
                print(f"📊 Overall Score: {score_match.group(1)}/100")

        break

    time.sleep(2)

print()
print("Monitor encerrado.")
