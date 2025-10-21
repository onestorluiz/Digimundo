#!/usr/bin/env python3
"""
ORGANIZADOR DO ARCHIVE POR DATA
Organiza todos os arquivos em pastas por data de criação
Remove duplicatas mantendo apenas uma cópia
"""

import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import json

def get_file_date(filepath):
    """Obtém a data de modificação do arquivo"""
    try:
        timestamp = os.path.getmtime(filepath)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except:
        return 'unknown-date'

def get_file_hash(filepath):
    """Calcula hash MD5 do arquivo para detectar duplicatas"""
    try:
        with open(filepath, 'rb') as f:
            file_hash = hashlib.md5()
            chunk = f.read(8192)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(8192)
            return file_hash.hexdigest()
    except:
        return None

def organize_archive(base_path):
    """Organiza o archive por data"""

    base_path = Path(base_path)

    # Estatísticas
    stats = {
        'total_files': 0,
        'files_moved': 0,
        'duplicates_removed': 0,
        'errors': 0,
        'dates_created': set(),
        'file_hashes': {}  # Para detectar duplicatas
    }

    print(f"📊 Iniciando organização do archive: {base_path}")
    print(f"   Isso pode levar alguns minutos...")

    # Coletar todos os arquivos primeiro
    all_files = []
    for root, dirs, files in os.walk(base_path):
        # Pular pastas já organizadas por data
        if Path(root).name.startswith('2025-') or Path(root).name.startswith('2024-'):
            continue

        for file in files:
            # Pular arquivos do sistema
            if file.startswith('.'):
                continue

            filepath = Path(root) / file

            # Pular arquivos Python do organizador
            if file == 'organize_archive.py':
                continue

            all_files.append(filepath)

    print(f"📁 Encontrados {len(all_files)} arquivos para organizar")

    # Processar cada arquivo
    for i, filepath in enumerate(all_files, 1):
        if i % 100 == 0:
            print(f"   Processando arquivo {i}/{len(all_files)}...")

        stats['total_files'] += 1

        try:
            # Obter data do arquivo
            file_date = get_file_date(filepath)
            stats['dates_created'].add(file_date)

            # Obter hash para detectar duplicatas
            file_hash = get_file_hash(filepath)

            if file_hash:
                if file_hash in stats['file_hashes']:
                    # Duplicata encontrada
                    print(f"   🔄 Duplicata: {filepath.name}")

                    # Manter o arquivo mais antigo
                    existing_file = stats['file_hashes'][file_hash]
                    existing_date = get_file_date(existing_file)
                    current_date = file_date

                    if current_date < existing_date:
                        # Arquivo atual é mais antigo, remover o existente
                        os.remove(existing_file)
                        stats['file_hashes'][file_hash] = filepath
                    else:
                        # Remover arquivo atual
                        os.remove(filepath)
                        stats['duplicates_removed'] += 1
                        continue
                else:
                    # Arquivo único, adicionar ao registro
                    stats['file_hashes'][file_hash] = filepath

            # Criar pasta da data se não existir
            date_folder = base_path / file_date
            date_folder.mkdir(exist_ok=True)

            # Determinar destino
            relative_path = filepath.relative_to(base_path)

            # Preservar estrutura de subpastas importantes
            if 'scripturemon' in str(relative_path):
                dest_subfolder = date_folder / 'scripturemon'
                dest_subfolder.mkdir(exist_ok=True)
                dest_path = dest_subfolder / filepath.name
            elif 'claude_code' in str(relative_path):
                dest_subfolder = date_folder / 'claude_code'
                dest_subfolder.mkdir(exist_ok=True)
                dest_path = dest_subfolder / filepath.name
            else:
                # Arquivo genérico, colocar direto na pasta da data
                dest_path = date_folder / filepath.name

            # Mover arquivo se não estiver no local correto
            if filepath.parent != dest_path.parent:
                # Adicionar sufixo se arquivo já existir
                counter = 1
                original_dest = dest_path
                while dest_path.exists():
                    stem = original_dest.stem
                    suffix = original_dest.suffix
                    dest_path = original_dest.parent / f"{stem}_{counter}{suffix}"
                    counter += 1

                shutil.move(str(filepath), str(dest_path))
                stats['files_moved'] += 1

        except Exception as e:
            print(f"   ❌ Erro ao processar {filepath}: {e}")
            stats['errors'] += 1

    # Limpar pastas vazias
    print("\n🧹 Removendo pastas vazias...")
    for root, dirs, files in os.walk(base_path, topdown=False):
        # Não remover pastas de datas
        if Path(root).name.startswith('2025-') or Path(root).name.startswith('2024-'):
            continue

        if not dirs and not files and root != str(base_path):
            try:
                os.rmdir(root)
                print(f"   Removida pasta vazia: {Path(root).name}")
            except:
                pass

    # Relatório final
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE ORGANIZAÇÃO")
    print("="*60)
    print(f"Total de arquivos processados: {stats['total_files']}")
    print(f"Arquivos movidos: {stats['files_moved']}")
    print(f"Duplicatas removidas: {stats['duplicates_removed']}")
    print(f"Erros: {stats['errors']}")
    print(f"Pastas de datas criadas: {len(stats['dates_created'])}")
    print(f"\nDatas organizadas:")
    for date in sorted(stats['dates_created']):
        date_path = base_path / date
        if date_path.exists():
            file_count = sum(1 for _ in date_path.rglob('*') if _.is_file())
            print(f"   {date}: {file_count} arquivos")

    # Salvar log
    log_file = base_path / f"organization_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'stats': {
                'total_files': stats['total_files'],
                'files_moved': stats['files_moved'],
                'duplicates_removed': stats['duplicates_removed'],
                'errors': stats['errors'],
                'dates': list(stats['dates_created'])
            }
        }, f, indent=2)

    print(f"\n💾 Log salvo em: {log_file}")
    print("✅ Organização concluída!")

if __name__ == "__main__":
    archive_path = "/Users/clubproducoes/Digimundo/archive"

    print("🗂️ ORGANIZADOR DO ARCHIVE")
    print("="*60)
    print(f"Pasta: {archive_path}")
    print("⚠️  Este processo pode levar vários minutos...")
    print("="*60)

    response = input("\nDeseja continuar? (s/n): ")

    if response.lower() == 's':
        organize_archive(archive_path)
    else:
        print("Operação cancelada.")