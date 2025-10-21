#!/usr/bin/env python3
"""
Teste rápido para verificar se o TheoryIndexer está carregando os livros corretamente.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from engine.indexer.theory_indexer import get_theory_indexer

print("=" * 80)
print("🧪 TESTE DO THEORY INDEXER - VERIFICAÇÃO DE CAMINHO")
print("=" * 80)
print()

# Inicializar indexer via get_theory_indexer() (como o sistema realmente usa)
print("📚 Inicializando TheoryIndexer para 'aristotle'...")
indexer = get_theory_indexer(specialist_type='aristotle', force_reload=True)

print()
print("=" * 80)
print("📖 LIVROS CARREGADOS:")
print("=" * 80)
print()

# Verificar livros carregados
if hasattr(indexer, 'books') and indexer.books:
    print(f"✅ Total de livros carregados: {len(indexer.books)}")
    print()
    for book_name, book_info in indexer.books.items():
        if isinstance(book_info, dict):
            total_words = book_info.get('total_words', 0)
            total_chunks = book_info.get('total_chunks', 0)
            print(f"  📕 {book_name}")
            print(f"      Palavras: {total_words:,}")
            print(f"      Chunks: {total_chunks:,}")
        else:
            print(f"  📕 {book_name}: {book_info}")
        print()
else:
    print("❌ ERRO: Nenhum livro foi carregado!")
    print()

# Verificar theory_dir
print("=" * 80)
print("📂 DIRETÓRIO DE TEORIA:")
print("=" * 80)
print()
print(f"  Path: {indexer.theory_dir}")
print(f"  Existe? {indexer.theory_dir.exists()}")
if indexer.theory_dir.exists():
    txt_files = list(indexer.theory_dir.glob("*.txt"))
    print(f"  Arquivos .txt: {len(txt_files)}")
    if txt_files and len(txt_files) <= 5:
        for f in txt_files:
            print(f"    - {f.name}")
print()

print("=" * 80)
print("✅ TESTE CONCLUÍDO")
print("=" * 80)
