#!/usr/bin/env python3
"""
Script para limpar workspace/outputs e deixar apenas análises válidas.
Move análises antigas para backup.
"""
from pathlib import Path
from datetime import datetime
import shutil
import json

def is_analysis_complete(folder: Path) -> bool:
    """Verifica se análise está completa"""
    checkpoint = folder / '2_logs' / 'checkpoint.json'
    if not checkpoint.exists():
        return False

    try:
        with open(checkpoint) as f:
            data = json.load(f)
        completed = len(data.get('completed', []))
        total = data.get('total_analyses', 312)
        return completed >= total
    except:
        return False

def get_analysis_info(folder: Path) -> dict:
    """Pega informações da análise"""
    checkpoint = folder / '2_logs' / 'checkpoint.json'
    info = {
        'complete': False,
        'progress': '0/0',
        'percentage': 0.0
    }

    if checkpoint.exists():
        try:
            with open(checkpoint) as f:
                data = json.load(f)
            completed = len(data.get('completed', []))
            total = data.get('total_analyses', 312)
            info['complete'] = completed >= total
            info['progress'] = f"{completed}/{total}"
            info['percentage'] = (completed / total * 100) if total > 0 else 0
        except:
            pass

    return info

def main():
    """Main cleanup function"""
    print("🧹 LIMPEZA DO WORKSPACE")
    print("="*80)
    print()

    base_dir = Path('workspace/outputs')
    backup_dir = Path('workspace/backup_old_analyses')

    # Criar backup dir
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Encontrar todas as pastas
    all_folders = sorted([
        d for d in base_dir.iterdir()
        if d.is_dir() and d.name.startswith('TE_ENCONTRO')
    ], key=lambda p: p.stat().st_mtime)

    print(f"📂 Encontradas {len(all_folders)} pastas\n")

    # Separar por tipo
    old_format = []
    all_specialists = []

    for folder in all_folders:
        if 'old_format' in folder.name:
            old_format.append(folder)
        elif 'all_specialists' in folder.name:
            all_specialists.append(folder)

    print(f"📊 ANÁLISE:")
    print(f"   • old_format: {len(old_format)}")
    print(f"   • all_specialists: {len(all_specialists)}")
    print()

    # Mostrar all_specialists
    print("="*80)
    print("🎯 ANÁLISES all_specialists (MANTER):")
    print("="*80)
    for folder in all_specialists:
        info = get_analysis_info(folder)
        status = "✅ COMPLETA" if info['complete'] else f"⏳ {info['progress']} ({info['percentage']:.1f}%)"
        print(f"   {folder.name}")
        print(f"      {status}")
    print()

    # Confirmar
    print("="*80)
    print("🗑️  AÇÃO PROPOSTA:")
    print("="*80)
    print(f"   1. MANTER: {len(all_specialists)} pastas all_specialists")
    print(f"   2. MOVER PARA BACKUP: {len(old_format)} pastas old_format")
    print(f"   3. Destino: {backup_dir}")
    print()

    response = input("Continuar? [s/N]: ").strip().upper()
    if response not in ['S', 'SIM', 'Y', 'YES']:
        print("❌ Cancelado")
        return

    print()
    print("="*80)
    print("🚀 MOVENDO PARA BACKUP...")
    print("="*80)
    print()

    moved = 0
    errors = 0

    for folder in old_format:
        try:
            dest = backup_dir / folder.name
            if dest.exists():
                print(f"⚠️  SKIP: {folder.name} (já existe no backup)")
                continue

            shutil.move(str(folder), str(dest))
            print(f"✅ {folder.name}")
            moved += 1
        except Exception as e:
            print(f"❌ ERRO: {folder.name} - {e}")
            errors += 1

    print()
    print("="*80)
    print("🎉 LIMPEZA CONCLUÍDA!")
    print("="*80)
    print(f"   ✅ Movidas: {moved}")
    print(f"   ❌ Erros: {errors}")
    print(f"   📂 Backup: {backup_dir}")
    print()

    # Mostrar estado final
    remaining = list(base_dir.glob('TE_ENCONTRO*'))
    print(f"📁 Pastas restantes em workspace/outputs: {len(remaining)}")
    for folder in sorted(remaining):
        print(f"   • {folder.name}")

if __name__ == '__main__':
    main()
