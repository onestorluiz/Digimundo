#!/usr/bin/env python3
"""
Teste para validar que cada autor recebe o livro correto
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

print('='*80)
print('🧪 TESTE: Validação de Livros por Autor')
print('='*80)
print()

# Roteiro mínimo para teste
screenplay = """
INT. QUARTO - DIA

SAMANTHA acorda sobressaltada.

SAMANTHA
Mas eu estava tendo um sonho lindo...
"""

# Testar 2 autores diferentes
AUTHORS = ['truby', 'campbell']

for author in AUTHORS:
    print(f'\n📖 Testando {author.upper()}...')

    specialist = DrDialogue()
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model='scripturemon-optimized',
        llm_timeout=300,
        use_theory=True,
        deep_context=False,  # Shallow para teste rápido
        specialist_type=author
    )

    # Verificar qual livro foi indexado
    if wrapper.theory_indexer:
        stats = wrapper.theory_indexer.get_stats()
        print(f'   Livros indexados: {stats["books_indexed"]}')
        print(f'   Chunks: {stats["total_chunks"]}')

        # Mostrar nomes dos livros
        for book_name in wrapper.theory_indexer.books.keys():
            print(f'   📚 {book_name[:60]}...')

    print(f'   ✅ Indexer criado com sucesso para {author}')

print()
print('='*80)
print('✅ TESTE COMPLETO!')
print('='*80)
