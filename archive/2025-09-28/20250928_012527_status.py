#!/usr/bin/env python3
"""
UCHIMON Status Dashboard - Visão unificada do sistema
"""

import os
import json
import psutil
import subprocess
from pathlib import Path
from datetime import datetime

def check_genjutsu():
    """Verifica status do Genjutsu"""
    status_file = "/tmp/genjutsu_status.txt"
    json_file = "/tmp/genjutsu_data.json"

    if Path(status_file).exists():
        with open(status_file, 'r') as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1].strip()
                if "Active" in last_line:
                    return "🟢 ATIVO"
                elif "ERROR" in last_line:
                    return "🔴 ERRO"

    return "⚫ OFFLINE"

def calculate_harmony():
    """Calcula harmonia do sistema"""
    harmony = 90  # Base

    # Verificar arquivos críticos
    critical_files = [
        "/Users/clubproducoes/Digimundo/claude_code/🔥UCHIMON_CORE🔥.md",
        "/Users/clubproducoes/Digimundo/claude_code/🔥REGRAS_UCHIMON_REVOLUCIONARIAS🔥.md",
        "/Users/clubproducoes/Digimundo/claude_code/🔥SISTEMA_MODULAR_UCHIMON🔥.md"
    ]

    for file in critical_files:
        if Path(file).exists():
            harmony += 2

    # Verificar processos
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'genjutsu' in result.stdout.lower():
            harmony += 3
        if 'uchimon' in result.stdout.lower():
            harmony += 1
    except:
        pass

    return min(harmony, 99)  # Cap at 99%

def check_background():
    """Verifica processos em background"""
    processes = []

    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info.get('cmdline', []))
                if any(keyword in cmdline.lower() for keyword in ['genjutsu', 'uchimon', 'scripturemon', 'hack']):
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmd': cmdline[:50] + '...' if len(cmdline) > 50 else cmdline
                    })
            except:
                pass
    except:
        pass

    return processes

def has_alerts():
    """Verifica se existem alertas ativos"""
    alert_file = "/Users/clubproducoes/Digimundo/UCHIMON/ALERT.txt"
    if Path(alert_file).exists():
        with open(alert_file, 'r') as f:
            content = f.read().strip()
            if content:
                return True
    return False

def check_memory_usage():
    """Verifica uso de memória"""
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        'ram_percent': mem.percent,
        'ram_available_gb': round(mem.available / (1024**3), 2),
        'swap_percent': swap.percent
    }

def check_critical_files():
    """Verifica última modificação dos arquivos críticos"""
    files = {}
    critical = [
        "🔥UCHIMON_CORE🔥.md",
        "🔥REGRAS_UCHIMON_REVOLUCIONARIAS🔥.md",
        "🔥SISTEMA_MODULAR_UCHIMON🔥.md",
        "🔥BEHAVIORAL_HACK_KNOWLEDGE🔥.md"
    ]

    base_path = "/Users/clubproducoes/Digimundo/claude_code"

    for filename in critical:
        filepath = Path(base_path) / filename
        if filepath.exists():
            stat = os.stat(filepath)
            mod_time = datetime.fromtimestamp(stat.st_mtime)
            files[filename] = mod_time.strftime("%H:%M:%S %d/%m")

    return files

def show_status():
    """Dashboard principal do sistema UCHIMON"""
    print("\n" + "=" * 60)
    print("          🔥 UCHIMON STATUS DASHBOARD v6.0 🔥")
    print("=" * 60)

    # 1. Genjutsu Status
    genjutsu = check_genjutsu()
    print(f"\n🥷 Genjutsu System: {genjutsu}")

    # 2. Harmonia
    harmony = calculate_harmony()
    bar_length = 20
    filled = int(bar_length * harmony / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"🌀 Harmonia: [{bar}] {harmony}%")

    # 3. Memória
    mem = check_memory_usage()
    print(f"💾 RAM: {mem['ram_percent']:.1f}% usado | {mem['ram_available_gb']}GB livre")

    # 4. Processos Background
    processes = check_background()
    print(f"👻 Processos Ativos: {len(processes)} encontrados")
    if processes:
        for proc in processes[:3]:  # Mostrar apenas top 3
            print(f"   └─ [{proc['pid']}] {proc['cmd']}")

    # 5. Arquivos Críticos
    files = check_critical_files()
    print(f"\n📁 Arquivos Críticos: {len(files)} carregados")
    for filename, mod_time in files.items():
        print(f"   └─ {filename[:30]}... [{mod_time}]")

    # 6. Alertas
    if has_alerts():
        print("\n🔴 ALERTAS ATIVOS!")
        print("   └─ Verificar /UCHIMON/ALERT.txt")
    else:
        print("\n🟢 Sistema operando normalmente")

    # 7. Comandos Rápidos
    print("\n" + "=" * 60)
    print("COMANDOS RÁPIDOS:")
    print("  • cat /tmp/genjutsu_status.txt    - Ver log Genjutsu")
    print("  • ps aux | grep -i uchimon         - Ver processos")
    print("  • cat 🔥UCHIMON_CORE🔥.md         - Carregar Core")
    print("=" * 60)

    # Estado final
    print(f"\n{'=' * 60}")
    print(f"  UCHIMON SYSTEM - {'OPTIMAL' if harmony > 95 else 'OPERATIONAL'}")
    print(f"  Timestamp: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print(f"  DIGIMUNDO PRESENTE 🔥⚡💎")
    print(f"{'=' * 60}\n")

if __name__ == "__main__":
    show_status()