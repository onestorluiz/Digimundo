#!/usr/bin/env python3
"""
Teste para validar que deep_context carrega o livro correto por autor
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from core.theory_indexer import get_theory_indexer

print('='*80)
print('🧪 TESTE: Deep Context por Autor')
print('='*80)
print()

# Testar 2 autores
AUTHORS = ['truby', 'campbell']

for author in AUTHORS:
    print(f'\n📖 Testando deep_context com {author.upper()}...')

    indexer = get_theory_indexer(specialist_type=author, force_reload=True)

    # Simular get_full_book_context
    result = indexer.get_full_book_context(
        query="analyze screenplay dialogue",
        specialist_type=author
    )

    if result['primary_book']:
        book = result['primary_book']
        print(f'   ✅ Livro carregado: {book["name"][:60]}...')
        print(f'   📏 Palavras: {book["word_count"]:,}')
        print(f'   📄 Chars: {book["char_count"]:,}')
        print(f'   🎯 Método: {result.get("method", "fallback")}')
    else:
        print(f'   ❌ Nenhum livro carregado!')

print()
print('='*80)
print('✅ TESTE COMPLETO!')
print('='*80)
