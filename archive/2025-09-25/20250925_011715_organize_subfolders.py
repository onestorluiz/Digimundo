#!/usr/bin/env python3
"""
ORGANIZADOR DE SUBPASTAS DO ARCHIVE
Move arquivos das subpastas para as pastas de data correspondentes
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def get_file_date(filepath):
    """Obtém a data de modificação do arquivo"""
    try:
        timestamp = os.path.getmtime(filepath)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except:
        return 'unknown-date'

def organize_subfolder(subfolder_path, archive_base):
    """Organiza conteúdo de uma subpasta"""

    subfolder_path = Path(subfolder_path)
    archive_base = Path(archive_base)

    if not subfolder_path.exists():
        print(f"❌ Pasta não encontrada: {subfolder_path}")
        return

    print(f"\n📁 Organizando: {subfolder_path.name}")

    files_moved = 0
    errors = 0

    # Coletar todos os arquivos
    for root, dirs, files in os.walk(subfolder_path):
        for file in files:
            # Pular arquivos do sistema
            if file.startswith('.'):
                continue

            filepath = Path(root) / file

            try:
                # Obter data do arquivo
                file_date = get_file_date(filepath)

                # Criar pasta da data se não existir
                date_folder = archive_base / file_date
                date_folder.mkdir(exist_ok=True)

                # Preservar nome do projeto na estrutura
                project_name = subfolder_path.name.replace(' 2', '').replace('-20250923', '')

                # Criar subpasta do projeto dentro da data
                project_subfolder = date_folder / project_name
                project_subfolder.mkdir(exist_ok=True)

                # Determinar destino
                dest_path = project_subfolder / file

                # Adicionar sufixo se já existir
                counter = 1
                original_dest = dest_path
                while dest_path.exists():
                    # Verificar se é o mesmo arquivo (mesmo tamanho)
                    if dest_path.stat().st_size == filepath.stat().st_size:
                        # Provavelmente duplicata, pular
                        print(f"   🔄 Duplicata ignorada: {file}")
                        break
                    stem = original_dest.stem
                    suffix = original_dest.suffix
                    dest_path = original_dest.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
                else:
                    # Mover arquivo
                    shutil.move(str(filepath), str(dest_path))
                    files_moved += 1

                    if files_moved % 10 == 0:
                        print(f"   Movidos {files_moved} arquivos...")

            except Exception as e:
                print(f"   ❌ Erro com {file}: {e}")
                errors += 1

    print(f"   ✅ {files_moved} arquivos movidos")
    if errors > 0:
        print(f"   ⚠️ {errors} erros")

    # Remover pasta original se vazia
    try:
        # Remover pastas vazias recursivamente
        for root, dirs, files in os.walk(subfolder_path, topdown=False):
            # Remover apenas se vazio (sem arquivos exceto .DS_Store)
            real_files = [f for f in files if not f.startswith('.')]
            if not real_files and not dirs:
                try:
                    # Remover .DS_Store se existir
                    ds_store = Path(root) / '.DS_Store'
                    if ds_store.exists():
                        os.remove(ds_store)
                    os.rmdir(root)
                except:
                    pass

        # Tentar remover pasta principal
        if not list(subfolder_path.iterdir()):
            subfolder_path.rmdir()
            print(f"   🗑️ Pasta original removida")
    except:
        print(f"   📁 Pasta original mantida (contém arquivos)")

def main():
    archive_base = "/Users/clubproducoes/Digimundo/archive"

    # Pastas para organizar
    subfolders = [
        "deprecated",
        "scripturemon-champion-refactored-bm25-tests 2",
        "scripturemon-ultimate-20250923",
        "digimundo-history",
        "backup-2025-09-21",
        "backups",
        "crystal",
        "essential",
        "minimal",
        "scripturemon-ultimate"  # Se existir
    ]

    print("🗂️ ORGANIZADOR DE SUBPASTAS DO ARCHIVE")
    print("="*60)

    total_moved = 0

    for subfolder_name in subfolders:
        subfolder_path = Path(archive_base) / subfolder_name

        if subfolder_path.exists() and subfolder_path.is_dir():
            # Contar arquivos antes
            file_count = sum(1 for _ in subfolder_path.rglob('*')
                           if _.is_file() and not _.name.startswith('.'))

            if file_count > 0:
                print(f"\n📂 {subfolder_name}: {file_count} arquivos")
                organize_subfolder(subfolder_path, archive_base)
                total_moved += file_count
            else:
                print(f"\n⏭️ {subfolder_name}: Vazia ou apenas .DS_Store")
                # Tentar remover se vazia
                try:
                    # Remover .DS_Store se existir
                    ds_store = subfolder_path / '.DS_Store'
                    if ds_store.exists():
                        os.remove(ds_store)
                    subfolder_path.rmdir()
                    print(f"   🗑️ Pasta vazia removida")
                except:
                    pass

    # Limpar pastas vazias finais
    print("\n🧹 Limpando pastas vazias...")
    empty_count = 0
    for root, dirs, files in os.walk(archive_base, topdown=False):
        # Não remover pastas de data
        if Path(root).name.startswith('20'):
            continue

        real_files = [f for f in files if not f.startswith('.')]
        if not real_files and not dirs:
            try:
                # Remover .DS_Store se existir
                ds_store = Path(root) / '.DS_Store'
                if ds_store.exists():
                    os.remove(ds_store)
                os.rmdir(root)
                empty_count += 1
            except:
                pass

    print(f"   Removidas {empty_count} pastas vazias")

    print("\n" + "="*60)
    print("✅ ORGANIZAÇÃO CONCLUÍDA!")
    print(f"   Total de arquivos reorganizados: ~{total_moved}")
    print("\n💡 Arquivos agora estão nas pastas de data correspondentes")

if __name__ == "__main__":
    main()