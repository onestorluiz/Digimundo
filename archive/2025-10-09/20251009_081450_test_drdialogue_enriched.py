#!/usr/bin/env python3
"""
Teste do DrDialogue com mapeamento ENRIQUECIDO
Compara análise com 1 livro vs 7 livros
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path.cwd()))

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

# Roteiro de teste (curto para demonstração)
SCREENPLAY_TEST = """
INT. CAFÉ - DIA

MARIA, 30s, nervosa, mexe sua xícara sem parar.

JOÃO entra, vê Maria e se aproxima.

JOÃO
Oi.

MARIA
Oi.

Silêncio desconfortável.

JOÃO
Então... sobre ontem...

MARIA
(cortando)
Não quero falar sobre isso.

JOÃO
Maria, a gente precisa conversar.

MARIA
Precisa? Ou você quer se justificar?

JOÃO
Não é sobre justificar. É sobre...
(pausa)
É sobre nós.

MARIA
Não existe mais "nós", João.

Maria se levanta para sair.

JOÃO
(segurando seu braço)
Por favor.

MARIA
(olhando para a mão dele)
Me solta.

João solta. Maria vai embora sem olhar para trás.

FADE OUT.
"""

print('='*80)
print('🎭 TESTE: DrDialogue com Mapeamento ENRIQUECIDO')
print('='*80)
print()

print('📄 Roteiro de teste: Cena de café (conflito entre Maria e João)')
print(f'📏 Tamanho: {len(SCREENPLAY_TEST.split())} palavras')
print()

# ============================================================================
# TESTE 1: MODO ANTIGO (1 livro - apenas McKee Dialogue)
# ============================================================================

print('='*80)
print('📖 TESTE 1: Modo ANTIGO (1 livro)')
print('='*80)
print()

specialist_old = DrDialogue()

# Simular mapeamento antigo manualmente (só McKee Dialogue)
from core.theory_indexer import get_theory_indexer
indexer_old = get_theory_indexer(specialist_type='mckee_dialogue', force_reload=True)
stats_old = indexer_old.get_stats()

print(f'📚 Livros indexados: {stats_old["books_indexed"]}')
print(f'📊 Total de chunks: {stats_old["total_chunks"]:,}')
print()

print('⏳ Executando análise Python (Core 1)...')
python_result = specialist_old.analyze(SCREENPLAY_TEST)

print(f'   ✅ Score diálogo: {python_result["overall_score"]}/100')
print(f'   📊 Problemas detectados: {len(python_result["problems"])}')
print()

# Buscar teoria (shallow mode - BM25 search)
print('🔍 Buscando teoria relevante (BM25)...')
theory_results = indexer_old.search_for_problems(python_result['problems'], limit=5)

total_chunks_old = sum(len(chunks) for chunks in theory_results.values())
print(f'   📚 Chunks recuperados: {total_chunks_old}')

# Mostrar exemplo de chunk
if theory_results:
    first_problem = list(theory_results.keys())[0]
    first_chunk = theory_results[first_problem][0] if theory_results[first_problem] else None
    if first_chunk:
        print(f'   📖 Exemplo de fonte: {first_chunk["book"][:50]}...')
        print(f'   💡 Texto: {first_chunk["text"][:100]}...')

print()

# ============================================================================
# TESTE 2: MODO NOVO (7 livros enriquecidos)
# ============================================================================

print('='*80)
print('📚 TESTE 2: Modo NOVO ENRIQUECIDO (7 livros)')
print('='*80)
print()

specialist_new = DrDialogue()

# Usar mapeamento enriquecido (7 livros)
indexer_new = get_theory_indexer(specialist_type='dialogue', force_reload=True)
stats_new = indexer_new.get_stats()

print(f'📚 Livros indexados: {stats_new["books_indexed"]}')
print(f'📊 Total de chunks: {stats_new["total_chunks"]:,}')
print()

print('Livros indexados:')
for book_name in indexer_new.books.keys():
    author = indexer_new._get_author(book_name)
    chunks_count = len(indexer_new.books[book_name])
    print(f'   ✅ {author:20} → {chunks_count:3} chunks')

print()

print('⏳ Executando análise Python (Core 1)...')
python_result_new = specialist_new.analyze(SCREENPLAY_TEST)

print(f'   ✅ Score diálogo: {python_result_new["overall_score"]}/100')
print(f'   📊 Problemas detectados: {len(python_result_new["problems"])}')
print()

# Buscar teoria (shallow mode - BM25 search nos 7 livros)
print('🔍 Buscando teoria relevante (BM25 nos 7 livros)...')
theory_results_new = indexer_new.search_for_problems(python_result_new['problems'], limit=5)

total_chunks_new = sum(len(chunks) for chunks in theory_results_new.values())
print(f'   📚 Chunks recuperados: {total_chunks_new}')

# Contar autores únicos
unique_authors = set()
for chunks in theory_results_new.values():
    for chunk in chunks:
        author = indexer_new._get_author(chunk['book'])
        unique_authors.add(author)

print(f'   👥 Autores citados: {len(unique_authors)} ({", ".join(sorted(unique_authors))})')
print()

# Mostrar exemplos de chunks de diferentes autores
print('💡 Exemplos de teoria de múltiplos autores:')
shown_authors = set()
for problem, chunks in theory_results_new.items():
    for chunk in chunks[:3]:
        author = indexer_new._get_author(chunk['book'])
        if author not in shown_authors and len(shown_authors) < 3:
            shown_authors.add(author)
            print(f'\n   📚 {author}:')
            print(f'      "{chunk["text"][:120]}..."')

print()

# ============================================================================
# COMPARAÇÃO
# ============================================================================

print('='*80)
print('📊 COMPARAÇÃO: Antigo vs Novo')
print('='*80)
print()

print(f'{"Métrica":<30} | {"Antigo (1 livro)":<20} | {"Novo (7 livros)":<20} | {"Melhoria":<15}')
print('-'*90)

books_diff = stats_new['books_indexed'] - stats_old['books_indexed']
print(f'{"Livros indexados":<30} | {stats_old["books_indexed"]:<20} | {stats_new["books_indexed"]:<20} | {f"+{books_diff} livros":<15}')

chunks_diff = stats_new['total_chunks'] - stats_old['total_chunks']
chunks_pct = (chunks_diff / stats_old['total_chunks'] * 100) if stats_old['total_chunks'] > 0 else 0
print(f'{"Chunks disponíveis":<30} | {stats_old["total_chunks"]:<20,} | {stats_new["total_chunks"]:<20,} | {f"+{chunks_pct:.0f}%":<15}')

retrieved_diff = total_chunks_new - total_chunks_old
retrieved_pct = (retrieved_diff / total_chunks_old * 100) if total_chunks_old > 0 else 0
print(f'{"Chunks recuperados":<30} | {total_chunks_old:<20} | {total_chunks_new:<20} | {f"+{retrieved_pct:.0f}%":<15}')

authors_old = 1
print(f'{"Autores citados":<30} | {authors_old:<20} | {len(unique_authors):<20} | {f"{len(unique_authors)}x mais":<15}')

print()

# ============================================================================
# TESTE 3: Análise COMPLETA com LLM (opcional)
# ============================================================================

print('='*80)
print('🤖 TESTE 3: Análise COMPLETA (Python + LLM)')
print('='*80)
print()

response = input('Executar análise completa com LLM? (Pode demorar ~30-60s) [s/N]: ')

if response.lower() == 's':
    print()
    print('⏳ Executando análise dual-core (Python + LLM)...')
    print('   📚 Usando 7 livros de teoria')
    print('   🎯 Modo: shallow (BM25 search)')
    print()

    wrapper = DualCoreWrapper(
        python_specialist=specialist_new,
        llm_model='scripturemon-optimized',
        llm_timeout=120,
        use_theory=True,
        deep_context=False,  # Shallow = usa todos os 7 livros via BM25
        specialist_type='dialogue'
    )

    start_time = datetime.now()
    result = wrapper.analyze(SCREENPLAY_TEST)
    elapsed = (datetime.now() - start_time).total_seconds()

    print(f'✅ Análise completa em {elapsed:.1f}s')
    print()

    llm_text = result.get('llm_insights', '')
    if llm_text:
        print(f'📏 Output LLM: {len(llm_text):,} caracteres')
        print()

        # Verificar citações de múltiplos autores
        cited_authors = []
        for author in ['McKee', 'Truby', 'Field', 'Seger', 'Egri', 'Cowgill']:
            if author.lower() in llm_text.lower():
                cited_authors.append(author)

        if cited_authors:
            print(f'👥 Autores citados no output LLM: {", ".join(cited_authors)}')
        else:
            print('⚠️  Nenhum autor específico citado no output')

        print()
        print('💡 Preview do output LLM:')
        print('-'*80)
        print(llm_text[:500] + '...')
        print('-'*80)

    # Exportar HTML
    html_path = wrapper.export_formatted(
        result,
        screenplay_title='TEST_DRDIALOGUE_ENRICHED',
        format='html'
    )

    print()
    print(f'💾 HTML exportado: {html_path}')
else:
    print('   ⏭️  Pulando análise LLM')

print()
print('='*80)
print('✅ TESTE COMPLETO!')
print('='*80)
print()

print('📊 Resumo:')
print(f'   • Modo antigo: 1 livro, {total_chunks_old} chunks recuperados')
print(f'   • Modo novo: 7 livros, {total_chunks_new} chunks recuperados')
print(f'   • Melhoria: {len(unique_authors)}x mais autores, +{chunks_pct:.0f}% chunks')
print()
print('🎉 Sistema enriquecido funcionando!')
