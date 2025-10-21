#!/usr/bin/env python3
"""
Debug: Verificar se citações por autor estão sendo enviadas ao LLM
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from core.theory_indexer import get_theory_indexer

print('='*80)
print('🔍 DEBUG: Verificando format_theory_context com specialist_type="all"')
print('='*80)
print()

# Criar indexer com 'all'
indexer = get_theory_indexer(specialist_type='all')
stats = indexer.get_stats()

print(f'📚 Indexer stats:')
print(f'   Livros: {stats["books_indexed"]}')
print(f'   Chunks: {stats["total_chunks"]}')
print()

# Criar problemas de exemplo
problems = [
    "on-the-nose dialogue",
    "lack of subtext",
    "artificial character voice"
]

print(f'🔍 Buscando teoria para problemas:')
for p in problems:
    print(f'   • {p}')
print()

# Buscar citações
theory_results = indexer.search_for_problems(problems, limit_per_problem=2)

print(f'📊 Resultados da busca:')
for problem, chunks in theory_results.items():
    print(f'   {problem}: {len(chunks)} chunks')
print()

# Formatar contexto (organizado por autor)
formatted = indexer.format_theory_context(theory_results)

print('='*80)
print('📄 CONTEXTO FORMATADO (primeiros 5000 chars):')
print('='*80)
print(formatted[:5000])
print('...')
print('='*80)
print()

print(f'📏 Tamanho total: {len(formatted):,} chars')
print()

# Verificar autores presentes
authors_found = []
for author in ['MCKEE', 'TRUBY', 'CAMPBELL', 'SNYDER', 'FIELD', 'EGRI', 'VOGLER', 'SEGER', 'WEILAND']:
    if author in formatted.upper():
        count = formatted.upper().count(author)
        authors_found.append(f'   ✅ {author}: {count} menções')

if authors_found:
    print('📚 Autores encontrados no contexto formatado:')
    print('\n'.join(authors_found))
else:
    print('⚠️  PROBLEMA: Nenhum autor encontrado no formato "DE ACORDO COM"')

print()
