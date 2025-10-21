#!/usr/bin/env python3
"""
REMOVEDOR COMPLETO DE DUPLICATAS DO ARCHIVE
Remove TODAS as duplicatas, mantendo apenas uma cópia de cada arquivo
"""

import os
import hashlib
from pathlib import Path
from datetime import datetime
import json

def get_file_hash(filepath, chunk_size=8192):
    """Calcula hash MD5 do arquivo"""
    try:
        md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5.update(chunk)
        return md5.hexdigest()
    except Exception as e:
        print(f"   ⚠️ Erro ao calcular hash de {filepath}: {e}")
        return None

def find_and_remove_duplicates(base_path):
    """Encontra e remove todas as duplicatas"""

    base_path = Path(base_path)

    # Estatísticas
    stats = {
        'total_files': 0,
        'unique_files': 0,
        'duplicates_removed': 0,
        'space_saved': 0,
        'errors': 0,
        'file_hashes': {}  # hash -> (filepath, size)
    }

    print("🔍 REMOVEDOR DE DUPLICATAS DO ARCHIVE")
    print("="*60)
    print(f"📁 Analisando: {base_path}")
    print("   Isso pode levar alguns minutos...")
    print()

    # Coletar todos os arquivos
    all_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            # Pular arquivos do sistema e scripts
            if file.startswith('.') or file.endswith('.py'):
                continue

            filepath = Path(root) / file
            all_files.append(filepath)

    print(f"📊 Total de arquivos para analisar: {len(all_files)}")
    print()

    # Processar cada arquivo
    for i, filepath in enumerate(all_files, 1):
        if i % 100 == 0:
            print(f"   Processando arquivo {i}/{len(all_files)}...")

        stats['total_files'] += 1

        try:
            file_size = filepath.stat().st_size

            # Calcular hash
            file_hash = get_file_hash(filepath)

            if file_hash:
                if file_hash in stats['file_hashes']:
                    # Duplicata encontrada!
                    existing_path, existing_size = stats['file_hashes'][file_hash]

                    # Manter o arquivo com caminho mais curto (menos aninhado)
                    # ou o mais antigo se mesmo nível
                    existing_depth = len(existing_path.parts)
                    current_depth = len(filepath.parts)

                    if current_depth < existing_depth:
                        # Arquivo atual está menos aninhado, remover o existente
                        print(f"   🗑️ Removendo duplicata: {existing_path.name}")
                        print(f"      Mantendo: {filepath.name}")
                        os.remove(existing_path)
                        stats['file_hashes'][file_hash] = (filepath, file_size)
                        stats['duplicates_removed'] += 1
                        stats['space_saved'] += existing_size
                    else:
                        # Remover arquivo atual
                        print(f"   🗑️ Removendo duplicata: {filepath.name}")
                        print(f"      Original em: {existing_path.parent.name}/")
                        os.remove(filepath)
                        stats['duplicates_removed'] += 1
                        stats['space_saved'] += file_size
                else:
                    # Arquivo único
                    stats['file_hashes'][file_hash] = (filepath, file_size)
                    stats['unique_files'] += 1

        except Exception as e:
            print(f"   ❌ Erro ao processar {filepath.name}: {e}")
            stats['errors'] += 1

    # Limpar pastas vazias
    print("\n🧹 Removendo pastas vazias...")
    empty_count = 0

    for root, dirs, files in os.walk(base_path, topdown=False):
        # Não remover a pasta base ou pastas de datas principais
        if root == str(base_path):
            continue

        # Verificar se está vazia (ignorando .DS_Store)
        real_files = [f for f in files if not f.startswith('.')]

        if not real_files and not dirs:
            try:
                # Remover .DS_Store se existir
                ds_store = Path(root) / '.DS_Store'
                if ds_store.exists():
                    os.remove(ds_store)

                # Remover pasta
                os.rmdir(root)
                empty_count += 1

            except Exception as e:
                pass

    # Relatório final
    print("\n" + "="*60)
    print("📊 RELATÓRIO FINAL")
    print("="*60)
    print(f"Total de arquivos analisados:  {stats['total_files']:,}")
    print(f"Arquivos únicos mantidos:      {stats['unique_files']:,}")
    print(f"Duplicatas removidas:          {stats['duplicates_removed']:,}")
    print(f"Pastas vazias removidas:       {empty_count}")
    print(f"Erros:                         {stats['errors']}")
    print()

    # Calcular economia
    mb_saved = stats['space_saved'] / (1024 * 1024)
    gb_saved = mb_saved / 1024

    if gb_saved > 1:
        print(f"💾 Espaço economizado: {gb_saved:.2f} GB")
    else:
        print(f"💾 Espaço economizado: {mb_saved:.1f} MB")

    # Taxa de duplicação
    if stats['total_files'] > 0:
        dup_rate = (stats['duplicates_removed'] / stats['total_files']) * 100
        print(f"📈 Taxa de duplicação: {dup_rate:.1f}%")

    # Salvar log detalhado
    log_file = base_path / f"duplicate_removal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    log_data = {
        'timestamp': datetime.now().isoformat(),
        'stats': {
            'total_files': stats['total_files'],
            'unique_files': stats['unique_files'],
            'duplicates_removed': stats['duplicates_removed'],
            'space_saved_bytes': stats['space_saved'],
            'space_saved_mb': mb_saved,
            'errors': stats['errors'],
            'empty_folders_removed': empty_count
        }
    }

    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)

    print(f"\n📝 Log salvo em: {log_file.name}")

    print("\n✅ LIMPEZA CONCLUÍDA!")

    return stats

if __name__ == "__main__":
    archive_path = "/Users/clubproducoes/Digimundo/archive"

    print("🚨 REMOVEDOR COMPLETO DE DUPLICATAS")
    print("="*60)
    print("⚠️  ATENÇÃO: Este script irá DELETAR permanentemente")
    print("   todas as duplicatas encontradas!")
    print("="*60)

    response = input("\n❓ Tem certeza que deseja continuar? (sim/não): ")

    if response.lower() in ['sim', 's', 'yes', 'y']:
        print()
        find_and_remove_duplicates(archive_path)
    else:
        print("\n❌ Operação cancelada.")