#!/usr/bin/env python3
"""
🧪 TESTE DIRETO DA BIBLIOTECA DE ROTEIROS
"""

from pathlib import Path

# Caminho absoluto
library_path = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_ROTEIROS")

print("🔍 TESTANDO ACESSO DIRETO À BIBLIOTECA")
print("=" * 60)

# Listar todas as pastas
print("\n📁 Estrutura encontrada:")
for folder in library_path.iterdir():
    if folder.is_dir():
        files = list(folder.glob("*.txt"))
        print(f"  {folder.name}: {len(files)} arquivos")
        for f in files[:3]:  # Primeiros 3
            print(f"    - {f.name}")

# Tentar ler SONHOS SEM LEMBRANÇAS T.3
target_file = library_path / "meus_filmes" / "SONHOS SEM LEMBRANÇAS T.3.txt"
print(f"\n📖 Tentando ler: {target_file}")
print(f"   Existe? {target_file.exists()}")

if target_file.exists():
    content = target_file.read_text(encoding='utf-8', errors='ignore')
    print(f"   ✅ Lido com sucesso! Tamanho: {len(content)} caracteres")
    print(f"   Preview: {content[:200]}...")

    # Testar com a biblioteca
    print("\n🧪 Agora testando com ScreenplayLibrary...")
    from src.core.screenplay_library import ScreenplayLibrary
    library = ScreenplayLibrary()

    # Testar diferentes formas de buscar
    tests = [
        "SONHOS SEM LEMBRANÇAS T.3",
        "SONHOS SEM LEMBRANÇAS T.3.txt",
        "sonhos sem lembranças",
        str(target_file)
    ]

    for test in tests:
        print(f"\n   Buscando por: '{test}'")
        result = library.get_screenplay(test)
        if result:
            print(f"   ✅ Encontrado! Tamanho: {len(result)}")
        else:
            print(f"   ❌ Não encontrado")

    # Verificar o mapeamento interno
    print("\n📋 Mapeamento interno da biblioteca:")
    library.list_screenplays(force_refresh=True)
    if "SONHOS SEM LEMBRANÇAS T.3" in library._file_paths:
        mapped_path = library._file_paths["SONHOS SEM LEMBRANÇAS T.3"]
        print(f"   'SONHOS SEM LEMBRANÇAS T.3' → {mapped_path}")
        print(f"   Arquivo existe? {mapped_path.exists()}")