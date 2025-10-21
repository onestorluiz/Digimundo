#!/usr/bin/env python3
"""
Script para migrar pastas antigas para o novo formato de nomenclatura.
Analisa cada pasta, determina o tipo real de análise e modelo usado.
"""
import json
import shutil
from pathlib import Path
from datetime import datetime

def analyze_folder(folder_path: Path) -> dict:
    """
    Analisa uma pasta para determinar seu conteúdo real.
    Returns: {
        'scope': 'all_specialists' or 'dialogue' or other,
        'model': 'ollama' or 'gpt',
        'timestamp': datetime object,
        'is_complete': bool
    }
    """
    info = {
        'scope': 'unknown',
        'model': 'ollama',  # default
        'timestamp': None,
        'is_complete': False,
        'total_analyses': 0,
        'completed_analyses': 0
    }

    # Verificar checkpoint para determinar o tipo real
    checkpoint_path = folder_path / '2_logs' / 'checkpoint.json'
    if checkpoint_path.exists():
        try:
            with open(checkpoint_path, 'r') as f:
                checkpoint = json.load(f)

            # Parse timestamp do checkpoint
            if 'started_at' in checkpoint:
                info['timestamp'] = datetime.fromisoformat(checkpoint['started_at'])

            # Determinar scope pelo total de análises
            total = checkpoint.get('total_analyses', 0)
            info['total_analyses'] = total
            info['completed_analyses'] = len(checkpoint.get('completed', []))

            if total == 312:  # 24 specialists × 13 authors
                info['scope'] = 'all_specialists'
            elif total == 13:  # 1 specialist × 13 authors
                # Verificar qual specialist
                completed = checkpoint.get('completed', [])
                if completed:
                    specialist = completed[0][0] if completed else 'dialogue'
                    info['scope'] = specialist
            else:
                info['scope'] = 'custom'

            # Verificar se está completo
            if info['completed_analyses'] >= info['total_analyses']:
                info['is_complete'] = True

        except Exception as e:
            print(f"   ⚠️  Erro ao ler checkpoint: {e}")

    # Se não tem checkpoint, usar timestamp da pasta
    if not info['timestamp']:
        info['timestamp'] = datetime.fromtimestamp(folder_path.stat().st_mtime)

    # Verificar logs para determinar modelo
    logs_dir = folder_path / '2_logs'
    if logs_dir.exists():
        for log_file in logs_dir.glob('*.log'):
            content = log_file.read_text()
            if 'gpt-' in content.lower() or 'openai' in content.lower():
                info['model'] = 'gpt'
                break

    # Verificar individuais para confirmar scope
    individuais_dir = folder_path / '1_individuais'
    if individuais_dir.exists():
        specialists = [d.name for d in individuais_dir.iterdir() if d.is_dir()]
        if len(specialists) > 1:
            info['scope'] = 'all_specialists'
        elif len(specialists) == 1:
            info['scope'] = specialists[0].lower()

    return info

def generate_new_name(old_name: str, info: dict) -> str:
    """
    Gera o novo nome no formato:
    {SCREENPLAY}__{SCOPE}_{MODEL}_{DD-MM-YY}_{HH-MM}_{SEQ}
    """
    # Extrair screenplay name (sempre TE_ENCONTRO_EM_MIM)
    screenplay = "TE_ENCONTRO_EM_MIM"

    # Scope
    scope = info['scope']

    # Model
    model = info['model']

    # Timestamp
    ts = info['timestamp']
    date_str = ts.strftime("%d-%m-%y")
    time_str = ts.strftime("%H-%M")

    # Sequence number (do nome antigo)
    old_parts = old_name.split('_')
    seq_num = old_parts[-1] if old_parts[-1].isdigit() else "0000"

    return f"{screenplay}__{scope}_{model}_{date_str}_{time_str}_{seq_num}"

def main():
    """Main migration function"""
    print("🔄 MIGRAÇÃO DE PASTAS ANTIGAS PARA NOVO FORMATO")
    print("="*80)
    print()

    base_dir = Path('workspace/outputs')

    # Encontrar todas as pastas no formato antigo
    old_folders = []

    # Padrão 1: dialogue_XXXX
    old_folders.extend(base_dir.glob('TE_ENCONTRO_EM_MIM__dialogue_[0-9][0-9][0-9][0-9]'))

    # Padrão 2: all_specialists_XXXX
    old_folders.extend(base_dir.glob('TE_ENCONTRO_EM_MIM__all_specialists_[0-9][0-9][0-9][0-9]'))

    # Ordenar por data de modificação
    old_folders = sorted(old_folders, key=lambda p: p.stat().st_mtime)

    print(f"📂 Encontradas {len(old_folders)} pastas para migrar:")
    print()

    migrations = []

    # Analisar cada pasta
    for folder in old_folders:
        print(f"🔍 Analisando: {folder.name}")
        info = analyze_folder(folder)

        print(f"   📊 Scope: {info['scope']}")
        print(f"   🤖 Model: {info['model']}")
        print(f"   📅 Data: {info['timestamp'].strftime('%d/%m/%Y %H:%M')}")
        print(f"   ✅ Completo: {info['is_complete']} ({info['completed_analyses']}/{info['total_analyses']})")

        new_name = generate_new_name(folder.name, info)
        print(f"   ➡️  Novo nome: {new_name}")

        migrations.append({
            'old_path': folder,
            'new_name': new_name,
            'info': info
        })
        print()

    # Confirmar migração
    print("="*80)
    print(f"📋 RESUMO: {len(migrations)} pastas serão renomeadas")
    print()

    # IMPORTANTE: Verificar análises em andamento
    in_progress = [m for m in migrations if not m['info']['is_complete']]
    if in_progress:
        print(f"⚠️  ATENÇÃO: {len(in_progress)} análises em andamento:")
        for m in in_progress:
            print(f"   - {m['old_path'].name} ({m['info']['completed_analyses']}/{m['info']['total_analyses']})")
        print()

    # Executar migração
    print("🚀 Iniciando migração...")
    print()

    for i, migration in enumerate(migrations, 1):
        old_path = migration['old_path']
        new_name = migration['new_name']
        new_path = base_dir / new_name

        try:
            # Verificar se novo nome já existe
            if new_path.exists():
                print(f"⚠️  [{i}/{len(migrations)}] SKIP: {new_name} já existe")
                continue

            # Renomear
            old_path.rename(new_path)
            print(f"✅ [{i}/{len(migrations)}] {old_path.name}")
            print(f"   ➡️  {new_name}")

        except Exception as e:
            print(f"❌ [{i}/{len(migrations)}] ERRO: {old_path.name}")
            print(f"   {e}")

    print()
    print("="*80)
    print("🎉 MIGRAÇÃO CONCLUÍDA!")
    print()

    # Listar resultado final
    print("📁 Pastas após migração:")
    all_folders = sorted(base_dir.glob('TE_ENCONTRO_EM_MIM__*'),
                         key=lambda p: p.stat().st_mtime,
                         reverse=True)
    for folder in all_folders[:10]:  # Mostrar últimas 10
        print(f"   - {folder.name}")

    if len(all_folders) > 10:
        print(f"   ... e mais {len(all_folders) - 10} pastas")

if __name__ == '__main__':
    main()
