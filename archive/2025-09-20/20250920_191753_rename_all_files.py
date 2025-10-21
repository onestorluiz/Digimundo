#!/usr/bin/env python3
"""
🔧 RENOMEADOR SISTEMÁTICO DE ARQUIVOS
Remove espaços, acentos e caracteres especiais de TODOS os arquivos da biblioteca
"""

import os
import re
from pathlib import Path
import unicodedata

def sanitize_filename(filename):
    """
    Remove acentos, espaços e caracteres especiais do nome do arquivo
    """
    # Remover acentos
    normalized = unicodedata.normalize('NFD', filename)
    ascii_text = normalized.encode('ascii', 'ignore').decode('ascii')

    # Substituir espaços e caracteres especiais por underscore
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', ascii_text)

    # Remover underscores múltiplos
    sanitized = re.sub(r'_+', '_', sanitized)

    # Remover underscore no início/fim
    sanitized = sanitized.strip('_')

    # Converter para lowercase para padronização
    return sanitized.lower()

def rename_files_in_directory(directory_path):
    """
    Renomeia todos os arquivos em um diretório recursivamente
    """
    directory = Path(directory_path)
    if not directory.exists():
        print(f"❌ Diretório não existe: {directory}")
        return []

    renamed_files = []

    # Processar recursivamente
    for file_path in directory.rglob("*.txt"):
        original_name = file_path.name
        original_stem = file_path.stem
        extension = file_path.suffix

        # Sanitizar apenas o nome (sem extensão)
        new_stem = sanitize_filename(original_stem)
        new_name = f"{new_stem}{extension}"

        # Se o nome já está correto, pular
        if original_name == new_name:
            print(f"✅ Já correto: {original_name}")
            continue

        # Novo caminho
        new_path = file_path.parent / new_name

        # Verificar se já existe
        if new_path.exists():
            print(f"⚠️ Já existe: {new_name} (pulando {original_name})")
            continue

        try:
            # Renomear
            file_path.rename(new_path)
            print(f"✅ {original_name} → {new_name}")
            renamed_files.append({
                'original': str(file_path),
                'new': str(new_path),
                'original_name': original_name,
                'new_name': new_name
            })
        except Exception as e:
            print(f"❌ Erro ao renomear {original_name}: {e}")

    return renamed_files

def main():
    print("🔧 RENOMEADOR SISTEMÁTICO DE ARQUIVOS")
    print("=" * 60)

    # Diretório da biblioteca
    library_path = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS")

    print(f"📁 Processando: {library_path}")
    print("-" * 40)

    # Verificar se existe
    if not library_path.exists():
        print(f"❌ Biblioteca não encontrada: {library_path}")
        return

    # Listar arquivos antes
    all_files = list(library_path.rglob("*.txt"))
    print(f"📋 {len(all_files)} arquivos .txt encontrados")

    # Mostrar estrutura atual
    print("\n📁 Estrutura atual:")
    for category_dir in library_path.iterdir():
        if category_dir.is_dir():
            files = list(category_dir.glob("*.txt"))
            print(f"  {category_dir.name}: {len(files)} arquivos")
            for f in files[:3]:  # Primeiros 3
                print(f"    - {f.name}")
            if len(files) > 3:
                print(f"    ... e mais {len(files) - 3} arquivos")

    print("\n🔧 Iniciando renomeação...")
    print("-" * 40)

    # Renomear todos os arquivos
    renamed = rename_files_in_directory(library_path)

    print("\n" + "=" * 60)
    print("📊 RESUMO DA RENOMEAÇÃO")
    print(f"✅ {len(renamed)} arquivos renomeados")

    if renamed:
        print("\n📝 Arquivos renomeados:")
        for item in renamed:
            category = Path(item['new']).parent.name
            print(f"  [{category}] {item['original_name']} → {item['new_name']}")

    print("\n🔍 Verificando resultado final...")
    final_files = list(library_path.rglob("*.txt"))
    print(f"📋 {len(final_files)} arquivos .txt no total")

    # Verificar se todos os nomes estão limpos
    problematic = []
    for file_path in final_files:
        if any(char in file_path.name for char in [' ', 'ã', 'ç', 'á', 'é', 'í', 'ó', 'ú', 'â', 'ê', 'ô']):
            problematic.append(file_path.name)

    if problematic:
        print(f"\n⚠️ {len(problematic)} arquivos ainda com problemas:")
        for name in problematic:
            print(f"  - {name}")
    else:
        print("\n✅ Todos os arquivos estão com nomes limpos!")

if __name__ == "__main__":
    main()