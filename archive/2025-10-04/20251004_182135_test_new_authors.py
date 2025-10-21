#!/usr/bin/env python3
"""
Teste para validar os novos autores: Aristotle e Cowgill
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from core.theory_indexer import get_theory_indexer

print('='*80)
print('🧪 TESTE: Novos Autores (Aristotle & Cowgill)')
print('='*80)
print()

# Testar 4 novos mapeamentos
NEW_AUTHORS = ['aristotle', 'cowgill', 'mckee_character', 'mckee_dialogue']

for author in NEW_AUTHORS:
    print(f'📖 Testando {author.upper()}...')

    try:
        indexer = get_theory_indexer(specialist_type=author, force_reload=True)

        # Verificar se indexou corretamente
        stats = indexer.get_stats()
        print(f'   ✅ Livros indexados: {stats["books_indexed"]}')
        print(f'   📊 Chunks totais: {stats["total_chunks"]:,}')

        # Simular get_full_book_context
        result = indexer.get_full_book_context(
            query="analyze story structure",
            specialist_type=author
        )

        if result['primary_book']:
            book = result['primary_book']
            print(f'   📚 Livro carregado: {book["name"][:60]}...')
            print(f'   📏 Palavras: {book["word_count"]:,}')
            print(f'   🎯 Método: {result.get("method", "fallback")}')
        else:
            print(f'   ❌ Nenhum livro carregado!')

    except Exception as e:
        print(f'   ❌ ERRO: {e}')

    print()

print('='*80)
print('✅ TESTE COMPLETO!')
print('='*80)
