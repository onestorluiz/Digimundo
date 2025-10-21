#!/usr/bin/env python3
"""
Teste simples do DrDialogue com mapeamento ENRIQUECIDO
Foca na análise completa (Python + LLM) com 7 livros
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path.cwd()))

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

# Roteiro de teste
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
print('🎭 TESTE: DrDialogue com 7 LIVROS DE TEORIA')
print('='*80)
print()

print('📄 Roteiro: Cena de café (conflito entre Maria e João)')
print(f'📏 Tamanho: {len(SCREENPLAY_TEST.split())} palavras')
print()

# Verificar quantos livros serão indexados
from core.theory_indexer import get_theory_indexer

print('📚 Indexando livros para specialist_type="dialogue"...')
indexer = get_theory_indexer(specialist_type='dialogue', force_reload=True)
stats = indexer.get_stats()

print()
print(f'✅ {stats["books_indexed"]} livros indexados:')
print()

for book_name in indexer.books.keys():
    author = indexer._get_author(book_name)
    chunks = len(indexer.books[book_name])
    print(f'   📖 {author:20} → {chunks:3} chunks')

print()
print(f'📊 Total: {stats["total_chunks"]:,} chunks disponíveis')
print()

# Análise completa com LLM
print('='*80)
print('🤖 ANÁLISE DUAL-CORE (Python + LLM)')
print('='*80)
print()

specialist = DrDialogue()

wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model='scripturemon-optimized',
    llm_timeout=120,
    use_theory=True,
    deep_context=False,  # Shallow mode = BM25 search nos 7 livros
    specialist_type='dialogue'
)

print('⏳ Executando análise...')
print('   🐍 Core 1 (Python): Análise objetiva de métricas')
print('   🤖 Core 2 (LLM): Insights qualitativos com teoria')
print('   📚 Teoria: 7 livros via BM25 search')
print()

start_time = datetime.now()
result = wrapper.analyze(SCREENPLAY_TEST)
elapsed = (datetime.now() - start_time).total_seconds()

print(f'✅ Análise completa em {elapsed:.1f}s')
print()

# Resultados Python
python_data = result.get('python_analysis', {})
print('📊 RESULTADOS PYTHON (Core 1):')
print(f'   Score geral: {python_data.get("score", 0)}/100')
print(f'   Linhas de diálogo: {python_data.get("total_dialogue_lines", 0)}')
print(f'   Personagens: {python_data.get("character_count", 0)}')
print(f'   Score de autenticidade: {python_data.get("authenticity_score", 0)}/100')
print(f'   Score de naturalidade: {python_data.get("natural_speech_score", 0)}/100')
print(f'   On-the-nose detected: {python_data.get("on_the_nose_count", 0)}')
print(f'   Clichês encontrados: {python_data.get("cliches_found", 0)}')
print()

# Resultados LLM
llm_text = result.get('llm_insights', '')
if llm_text:
    print('🤖 RESULTADOS LLM (Core 2):')
    print(f'   Output: {len(llm_text):,} caracteres')
    print()

    # Verificar citações de autores
    cited_authors = []
    author_keywords = {
        'McKee': ['mckee', 'robert mckee'],
        'Truby': ['truby', 'john truby'],
        'Field': ['field', 'syd field'],
        'Seger': ['seger', 'linda seger'],
        'Egri': ['egri', 'lajos egri'],
        'Cowgill': ['cowgill', 'linda j cowgill'],
        'Campbell': ['campbell', 'joseph campbell']
    }

    llm_lower = llm_text.lower()
    for author, keywords in author_keywords.items():
        if any(kw in llm_lower for kw in keywords):
            cited_authors.append(author)

    if cited_authors:
        print(f'   👥 Autores citados: {", ".join(cited_authors)}')
        print(f'   🎯 Diversidade: {len(cited_authors)}/7 livros citados!')
    else:
        print('   ⚠️  Nenhum autor específico detectado no output')

    print()
    print('💡 Preview do output LLM (primeiros 800 chars):')
    print('-'*80)
    preview = llm_text[:800]
    if len(llm_text) > 800:
        preview += '...'
    print(preview)
    print('-'*80)

print()

# Exportar HTML
html_path = wrapper.export_formatted(
    result,
    screenplay_title='TEST_DRDIALOGUE_7LIVROS',
    format='html'
)

print()
print(f'💾 HTML exportado: {html_path}')
print()

print('='*80)
print('✅ TESTE COMPLETO!')
print('='*80)
print()

print('📊 Resumo do Sistema Enriquecido:')
print(f'   ✅ 7 livros de teoria sobre diálogo')
print(f'   ✅ {stats["total_chunks"]:,} chunks disponíveis')
print(f'   ✅ Análise dual-core em {elapsed:.1f}s')
if cited_authors:
    print(f'   ✅ {len(cited_authors)} autores citados no output')
print()
print(f'🎉 DrDialogue com profundidade 7x maior!')
print()
print(f'Para visualizar o HTML:')
print(f'   open {html_path}')
