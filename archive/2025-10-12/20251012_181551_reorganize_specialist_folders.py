#!/usr/bin/env python3
"""
Script para reorganizar pastas de especialistas antigas para novo formato.
Adiciona timestamps nas pastas de especialistas em 1_individuais/ e 3_consolidados/.
"""
from pathlib import Path
from datetime import datetime
import shutil
import re

def extract_timestamp_from_filename(filename: str) -> str:
    """
    Extrai timestamp de um arquivo no formato YYYYMMDD_HHMMSS.
    Retorna formato DD-MM-YY_HH-MM.
    """
    # Padrão: ANALISE_XXX_YYY_20251012_142002.html
    match = re.search(r'(\d{8})_(\d{6})', filename)
    if match:
        date_str = match.group(1)  # 20251012
        time_str = match.group(2)  # 142002

        # Converter para datetime
        dt = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")

        # Retornar no formato DD-MM-YY_HH-MM
        return dt.strftime("%d-%m-%y_%H-%M")

    return None

def get_specialist_timestamp(specialist_folder: Path) -> str:
    """
    Pega o timestamp mais recente dos arquivos HTML do especialista.
    Retorna formato DD-MM-YY_HH-MM.
    """
    html_files = list(specialist_folder.glob('*.html'))
    if not html_files:
        # Sem arquivos, usar timestamp da pasta
        dt = datetime.fromtimestamp(specialist_folder.stat().st_mtime)
        return dt.strftime("%d-%m-%y_%H-%M")

    # Pegar último arquivo (mais recente)
    last_file = max(html_files, key=lambda f: f.stat().st_mtime)

    # Extrair timestamp do nome
    timestamp = extract_timestamp_from_filename(last_file.name)
    if timestamp:
        return timestamp

    # Fallback: usar timestamp do arquivo
    dt = datetime.fromtimestamp(last_file.stat().st_mtime)
    return dt.strftime("%d-%m-%y_%H-%M")

def reorganize_analysis_folder(analysis_folder: Path, dry_run: bool = True, skip_incomplete: bool = True):
    """
    Reorganiza uma pasta de análise específica.
    """
    print(f"\n📂 {analysis_folder.name}")
    print("="*80)

    # Verificar se análise está completa (se skip_incomplete=True)
    if skip_incomplete:
        checkpoint_file = analysis_folder / '2_logs' / 'checkpoint.json'
        if checkpoint_file.exists():
            import json
            try:
                with open(checkpoint_file, 'r') as f:
                    checkpoint = json.load(f)

                completed = len(checkpoint.get('completed', []))
                total = checkpoint.get('total_analyses', 312)

                if completed < total:
                    print(f"   ⚠️  ANÁLISE INCOMPLETA ({completed}/{total}) - PULANDO para não quebrar processo em andamento")
                    return
            except:
                pass

    individuais_dir = analysis_folder / '1_individuais'
    consolidados_dir = analysis_folder / '3_consolidados'

    if not individuais_dir.exists():
        print("   ⚠️  Sem pasta 1_individuais/")
        return

    # Encontrar pastas de especialistas sem timestamp (formato antigo)
    specialist_folders = [
        d for d in individuais_dir.iterdir()
        if d.is_dir() and not re.search(r'\d{2}-\d{2}-\d{2}_\d{2}-\d{2}', d.name)
    ]

    if not specialist_folders:
        print("   ✅ Todas as pastas já têm timestamp (formato novo)")
        return

    print(f"   📋 Encontradas {len(specialist_folders)} pastas para reorganizar")
    print()

    for specialist_folder in specialist_folders:
        specialist_name = specialist_folder.name
        print(f"   🔧 {specialist_name}")

        # Pegar timestamp
        timestamp = get_specialist_timestamp(specialist_folder)
        new_folder_name = f"{specialist_name}_{timestamp}"

        # Novo caminho em 1_individuais/
        new_individual_path = individuais_dir / new_folder_name

        print(f"      ➡️  {new_folder_name}")

        if dry_run:
            print(f"      [DRY RUN] Renomearia: {specialist_folder} → {new_individual_path}")
        else:
            try:
                if new_individual_path.exists():
                    print(f"      ⚠️  SKIP: {new_folder_name} já existe")
                    continue

                # Renomear pasta em 1_individuais/
                specialist_folder.rename(new_individual_path)
                print(f"      ✅ Renomeado em 1_individuais/")

                # Criar pasta em 3_consolidados/ e mover arquivo consolidado
                new_consolidado_path = consolidados_dir / new_folder_name
                new_consolidado_path.mkdir(exist_ok=True)

                # Procurar arquivo consolidado correspondente
                consolidado_pattern = f"CONSOLIDADO_{specialist_name}_*.html"
                consolidado_files = list(consolidados_dir.glob(consolidado_pattern))

                if consolidado_files:
                    for consolidado_file in consolidado_files:
                        dest_file = new_consolidado_path / consolidado_file.name
                        shutil.move(str(consolidado_file), str(dest_file))
                        print(f"      ✅ Consolidado movido para 3_consolidados/{new_folder_name}/")

            except Exception as e:
                print(f"      ❌ ERRO: {e}")

def main():
    """Main function"""
    import sys

    print("🔄 REORGANIZAÇÃO DE PASTAS DE ESPECIALISTAS")
    print("="*80)
    print()
    print("Este script vai:")
    print("  1. Adicionar timestamps nas pastas de especialistas em 1_individuais/")
    print("  2. Criar pastas correspondentes em 3_consolidados/")
    print("  3. Mover arquivos consolidados para as novas pastas")
    print()

    # Check for dry-run flag
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv

    if dry_run:
        print("🧪 MODO DRY RUN (apenas simulação, sem mudanças reais)")
    else:
        print("⚠️  MODO REAL (vai fazer mudanças!)")
        response = input("\nContinuar? [s/N]: ").strip().upper()
        if response not in ['S', 'SIM', 'Y', 'YES']:
            print("❌ Cancelado")
            return

    print()
    print("="*80)

    base_dir = Path('workspace/outputs')

    # Encontrar todas as pastas de análise
    analysis_folders = [
        d for d in base_dir.iterdir()
        if d.is_dir() and d.name.startswith('TE_ENCONTRO_EM_MIM__')
    ]

    # Ordenar por data de modificação (mais antigas primeiro)
    analysis_folders = sorted(analysis_folders, key=lambda p: p.stat().st_mtime)

    print(f"\n📁 Encontradas {len(analysis_folders)} pastas de análise")
    print()

    for folder in analysis_folders:
        reorganize_analysis_folder(folder, dry_run=dry_run, skip_incomplete=True)

    print()
    print("="*80)
    if dry_run:
        print("🎉 SIMULAÇÃO CONCLUÍDA!")
        print("\nExecute sem --dry-run para aplicar as mudanças:")
        print("  python3 reorganize_specialist_folders.py")
    else:
        print("🎉 REORGANIZAÇÃO CONCLUÍDA!")

if __name__ == '__main__':
    main()
