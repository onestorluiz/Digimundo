#!/usr/bin/env python3
"""
Script para corrigir pastas marcadas como 'unknown'.
Analisa o conteúdo dos arquivos HTML em 1_individuais/ para determinar o scope correto.
"""
from pathlib import Path
import re

def main():
    """Main function"""
    print("🔧 CORRIGINDO PASTAS 'UNKNOWN'")
    print("="*80)
    print()

    base_dir = Path('workspace/outputs')

    # Encontrar todas as pastas "unknown"
    unknown_folders = list(base_dir.glob('TE_ENCONTRO_EM_MIM__unknown_*'))
    unknown_folders = sorted(unknown_folders, key=lambda p: p.name)

    print(f"📂 Encontradas {len(unknown_folders)} pastas 'unknown'")
    print()

    renames = []

    for folder in unknown_folders:
        print(f"🔍 {folder.name}")

        # Analisar conteúdo de 1_individuais
        individuais_dir = folder / '1_individuais'
        if not individuais_dir.exists():
            print(f"   ⚠️  Sem pasta 1_individuais/")
            continue

        # Contar arquivos HTML (análises individuais - formato antigo)
        html_files = list(individuais_dir.glob('*.html'))

        # Contar subpastas (novo formato)
        subdirs = [d for d in individuais_dir.iterdir() if d.is_dir()]

        if html_files:
            print(f"   📄 {len(html_files)} arquivos HTML (formato antigo)")

            # Listar specialists baseado nos nomes dos arquivos
            specialists = set()
            for html in html_files:
                # Nome padrão: ANALISE_SPECIALIST_TIMESTAMP.html
                match = re.match(r'ANALISE_([A-Z_]+)_\d+\.html', html.name)
                if match:
                    specialists.add(match.group(1))

            print(f"   🔬 Specialists encontrados: {', '.join(sorted(specialists))}")

            # Determinar scope
            if len(specialists) == 1:
                scope = list(specialists)[0].lower()
            elif len(specialists) > 1:
                scope = 'multi_specialist'
            else:
                scope = 'old_format'

        elif subdirs:
            print(f"   📁 {len(subdirs)} subpastas (novo formato)")
            specialists = [d.name for d in subdirs]
            print(f"   🔬 Specialists: {', '.join(specialists)}")

            if len(specialists) == 1:
                scope = specialists[0].lower()
            else:
                scope = 'all_specialists'

        else:
            print(f"   ⚠️  Pasta vazia")
            scope = 'empty'

        # Gerar novo nome
        # Formato atual: TE_ENCONTRO_EM_MIM__unknown_ollama_DD-MM-YY_HH-MM_NNNN
        # Novo formato:  TE_ENCONTRO_EM_MIM__SCOPE_ollama_DD-MM-YY_HH-MM_NNNN
        parts = folder.name.split('__')
        if len(parts) == 2:
            screenplay = parts[0]
            rest = parts[1].split('_', 1)
            if len(rest) >= 2:
                # rest[0] = 'unknown', rest[1] = 'ollama_DD-MM-YY_HH-MM_NNNN'
                new_name = f"{screenplay}__{scope}_{rest[1]}"

                if new_name != folder.name:
                    renames.append((folder, base_dir / new_name, scope))
                    print(f"   ➡️  {new_name}")
                else:
                    print(f"   ✓ Nome já correto")
        print()

    # Executar renomeações
    if renames:
        print("="*80)
        print(f"🚀 Renomeando {len(renames)} pastas...")
        print()

        for old_path, new_path, scope in renames:
            try:
                if new_path.exists():
                    print(f"⚠️  SKIP: {new_path.name} já existe")
                    continue

                old_path.rename(new_path)
                print(f"✅ {old_path.name}")
                print(f"   ➡️  {new_path.name}")
            except Exception as e:
                print(f"❌ ERRO: {old_path.name}")
                print(f"   {e}")
    else:
        print("✓ Nenhuma renomeação necessária")

    print()
    print("="*80)
    print("🎉 CONCLUÍDO!")

if __name__ == '__main__':
    main()
