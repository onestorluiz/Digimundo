#!/usr/bin/env python3
"""
📊 STATUS COMPLETO DO SISTEMA CLAUDE_CODE
Mostra tudo que está acontecendo de forma visível
"""
import os
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3

# Importa o sistema de memória unificado
import sys
sys.path.append('/Users/clubproducoes/Digimundo/claude_code/memory')
from unified_memory import UnifiedMemory

def check_genjutsu():
    """Verifica se Genjutsu está rodando"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        return 'GENJUTSU' in result.stdout
    except:
        return False

def get_last_activity():
    """Verifica última atividade no sistema"""
    activity_file = Path('/Users/clubproducoes/Digimundo/claude_code/memory/temp/.claude_activity')
    if activity_file.exists():
        mtime = activity_file.stat().st_mtime
        last_time = datetime.fromtimestamp(mtime)
        diff = datetime.now() - last_time

        if diff < timedelta(seconds=30):
            return f"✅ {diff.seconds}s atrás"
        elif diff < timedelta(minutes=2):
            return f"⚡ {diff.seconds}s atrás (ficando inativo)"
        else:
            return f"🔴 {diff.seconds//60}min atrás (ALERTA!)"
    return "❌ Nunca (arquivo não existe)"

def check_memory_system():
    """Verifica estado do sistema de memória"""
    try:
        with UnifiedMemory() as mem:
            stats = mem.stats()
            return {
                'total': stats['total'],
                'size': stats['db_size'],
                'types': stats['by_type']
            }
    except Exception as e:
        return {'error': str(e)}

def check_disk_space():
    """Verifica espaço em disco"""
    result = subprocess.run(['df', '-h', '/Users/clubproducoes/Digimundo'],
                          capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    if len(lines) > 1:
        parts = lines[1].split()
        return f"{parts[3]} livre de {parts[1]}"
    return "❌ Não disponível"

def check_recent_changes():
    """Verifica mudanças recentes em claude_code"""
    claude_dir = Path('/Users/clubproducoes/Digimundo/claude_code')
    recent_files = []

    for file in claude_dir.rglob('*'):
        if file.is_file() and not str(file).startswith('.'):
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if datetime.now() - mtime < timedelta(hours=1):
                recent_files.append((file.name, mtime))

    return sorted(recent_files, key=lambda x: x[1], reverse=True)[:5]

def show_genjutsu_messages():
    """Mostra mensagens do Genjutsu se existirem"""
    terminal_file = Path('/Users/clubproducoes/Digimundo/claude_code/memory/temp/genjutsu_terminal.txt')
    if terminal_file.exists():
        with open(terminal_file, 'r') as f:
            lines = f.readlines()
            return lines[-5:] if lines else []
    return []

def main():
    """Mostra status completo do sistema"""

    print("\n" + "="*60)
    print("📊 CLAUDE_CODE SYSTEM STATUS")
    print("="*60)

    # Timestamp
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 1. GENJUTSU
    genjutsu_status = check_genjutsu()
    print("🥷 GENJUTSU:")
    if genjutsu_status:
        print("   ✅ ATIVO - Sistema de proteção psicológica rodando")
    else:
        print("   ❌ PARADO - Execute: ./START_GENJUTSU.sh")

    # Mensagens do Genjutsu
    genjutsu_msgs = show_genjutsu_messages()
    if genjutsu_msgs:
        print("   Últimas mensagens:")
        for msg in genjutsu_msgs:
            print(f"     {msg.strip()}")
    print()

    # 2. MEMÓRIA
    print("💾 SISTEMA DE MEMÓRIA:")
    memory = check_memory_system()
    if 'error' not in memory:
        print(f"   Total: {memory['total']} registros")
        print(f"   Tamanho: {memory['size']}")
        print("   Distribuição:")
        for type_info in memory['types']:
            print(f"     • {type_info['type']}: {type_info['count']}")
    else:
        print(f"   ❌ Erro: {memory['error']}")
    print()

    # 3. ATIVIDADE
    print("⏰ ÚLTIMA ATIVIDADE:")
    last_activity = get_last_activity()
    print(f"   {last_activity}")

    # Se muito tempo inativo, alerta
    if "ALERTA" in last_activity or "Nunca" in last_activity:
        print("   ⚠️ ATENÇÃO: Possível compactação ou perda de contexto!")
        print("   💡 Execute: cat /Users/clubproducoes/Digimundo/claude_code/REGRAS.md")
    print()

    # 4. MUDANÇAS RECENTES
    print("📝 ARQUIVOS MODIFICADOS (última hora):")
    recent = check_recent_changes()
    if recent:
        for fname, mtime in recent:
            time_ago = datetime.now() - mtime
            print(f"   • {fname} ({time_ago.seconds//60}min atrás)")
    else:
        print("   Nenhuma modificação recente")
    print()

    # 5. ESPAÇO EM DISCO
    print("💽 ESPAÇO EM DISCO:")
    disk = check_disk_space()
    print(f"   {disk}")
    print()

    # 6. COMANDOS ÚTEIS
    print("🎯 COMANDOS RÁPIDOS:")
    print("   📖 Reconectar: ./START_GENJUTSU.sh")
    print("   🔍 Ver memórias: python3 -m unified_memory")
    print("   📊 Este status: python3 status.py")
    print("   🥷 Ativar Genjutsu: python3 protection/genjutsu/GENJUTSU_UNIFIED.py &")
    print()

    # 7. HEALTH CHECK
    print("🏥 HEALTH CHECK:")
    health_checks = []

    # Check 1: Genjutsu
    if genjutsu_status:
        health_checks.append("✅ Genjutsu ativo")
    else:
        health_checks.append("❌ Genjutsu parado")

    # Check 2: Memória
    if 'error' not in memory and memory['total'] > 0:
        health_checks.append("✅ Memória funcionando")
    else:
        health_checks.append("❌ Problema na memória")

    # Check 3: Atividade
    if "✅" in last_activity:
        health_checks.append("✅ Atividade recente")
    else:
        health_checks.append("⚡ Atividade antiga")

    for check in health_checks:
        print(f"   {check}")

    # Score final
    score = sum(1 for c in health_checks if "✅" in c)
    total = len(health_checks)
    percentage = (score/total) * 100

    print()
    print(f"📈 SCORE: {score}/{total} ({percentage:.0f}%)")

    if percentage == 100:
        print("🎉 Sistema 100% operacional!")
    elif percentage >= 66:
        print("⚡ Sistema funcionando com alertas")
    else:
        print("🔴 Sistema precisa de atenção!")

    print()
    print("="*60)
    print("DIGIMUNDO PRESENTE 🔥")
    print()

if __name__ == "__main__":
    main()