#!/usr/bin/env python3
"""
Análise de Diálogo - SONHOS SEM LEMBRANÇAS T.3
Sistema enriquecido com 7 livros de teoria
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path.cwd()))

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

print('='*80)
print('🎬 ANÁLISE DE DIÁLOGO - SONHOS SEM LEMBRANÇAS T.3')
print('='*80)
print()

# Caminho do roteiro
screenplay_path = 'content/screenplays/personal/SONHOS SEM LEMBRANÇAS T.3.pdf'

print(f'📄 Roteiro: {screenplay_path}')
print()

# Verificar indexação dos 7 livros
from core.theory_indexer import get_theory_indexer

print('📚 Preparando sistema de teoria enriquecido...')
indexer = get_theory_indexer(specialist_type='dialogue', force_reload=True)
stats = indexer.get_stats()

print(f'   ✅ {stats["books_indexed"]} livros indexados')
print(f'   📊 {stats["total_chunks"]:,} chunks disponíveis')
print()

print('📖 Livros carregados:')
for book_name in indexer.books.keys():
    author = indexer._get_author(book_name)
    chunks = len(indexer.books[book_name])
    print(f'   • {author:20} → {chunks:3} chunks')
print()

# Criar wrapper dual-core
print('🎯 Configurando análise Dual-Core...')
specialist = DrDialogue()

wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model='scripturemon-optimized',
    llm_timeout=120,
    use_theory=True,
    deep_context=False,  # Shallow = BM25 search nos 7 livros
    specialist_type='dialogue'
)
print('   ✅ Core 1 (Python): Métricas objetivas de diálogo')
print('   ✅ Core 2 (LLM): Insights qualitativos com teoria')
print('   ✅ Teoria: 7 livros via BM25 search')
print()

# Ler o roteiro
print('📖 Lendo roteiro PDF...')
try:
    # Tentar ler como PDF
    import PyPDF2
    with open(screenplay_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        screenplay_text = ""
        for page in pdf_reader.pages:
            screenplay_text += page.extract_text() + "\n"

    word_count = len(screenplay_text.split())
    print(f'   ✅ PDF lido: {len(pdf_reader.pages)} páginas, {word_count:,} palavras')
except Exception as e:
    print(f'   ⚠️  Erro ao ler PDF: {e}')
    print('   🔄 Tentando arquivo .txt...')

    txt_path = screenplay_path.replace('.pdf', '.txt')
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            screenplay_text = f.read()
        word_count = len(screenplay_text.split())
        print(f'   ✅ TXT lido: {word_count:,} palavras')
    except Exception as e2:
        print(f'   ❌ ERRO: {e2}')
        sys.exit(1)

print()

# Executar análise
print('='*80)
print('⏳ EXECUTANDO ANÁLISE DUAL-CORE')
print('='*80)
print()

start_time = datetime.now()
result = wrapper.analyze(screenplay_text)
elapsed = (datetime.now() - start_time).total_seconds()

print()
print(f'✅ Análise concluída em {elapsed:.1f}s ({elapsed/60:.1f} min)')
print()

# Resultados Python (Core 1)
python_data = result.get('python_analysis', {})
print('='*80)
print('📊 RESULTADOS PYTHON (Core 1)')
print('='*80)
print()
print(f'   ✅ Score Geral: {python_data.get("score", 0):.1f}/100')
print(f'   📝 Linhas de Diálogo: {python_data.get("total_dialogue_lines", 0)}')
print(f'   👥 Personagens: {python_data.get("character_count", 0)}')
print(f'   🎭 Autenticidade: {python_data.get("authenticity_score", 0):.1f}/100')
print(f'   💬 Naturalidade: {python_data.get("natural_speech_score", 0):.1f}/100')
print(f'   🎯 On-the-nose: {python_data.get("on_the_nose_count", 0)} detectados')
print(f'   ⚠️  Clichês: {python_data.get("cliches_found", 0)} encontrados')

# Problemas detectados
problems = python_data.get('problems', [])
if problems:
    print()
    print(f'   📋 Problemas Detectados: {len(problems)}')
    for i, problem in enumerate(problems[:5], 1):
        severity = problem.get('severity', 'unknown')
        issue_type = problem.get('type', 'unknown')
        print(f'      {i}. [{severity.upper()}] {issue_type}')
    if len(problems) > 5:
        print(f'      ... e mais {len(problems) - 5} problemas')

print()

# Resultados LLM (Core 2)
llm_text = result.get('llm_insights', '')
if llm_text:
    print('='*80)
    print('🤖 RESULTADOS LLM (Core 2)')
    print('='*80)
    print()
    print(f'   📏 Output: {len(llm_text):,} caracteres')

    # Verificar citações de autores
    cited_authors = []
    author_keywords = {
        'McKee': ['mckee', 'robert mckee'],
        'Truby': ['truby', 'john truby'],
        'Field': ['field', 'syd field'],
        'Seger': ['seger', 'linda seger'],
        'Egri': ['egri', 'lajos egri'],
        'Cowgill': ['cowgill', 'linda j cowgill', 'linda cowgill'],
    }

    llm_lower = llm_text.lower()
    for author, keywords in author_keywords.items():
        if any(kw in llm_lower for kw in keywords):
            cited_authors.append(author)

    if cited_authors:
        print(f'   👥 Autores Citados: {", ".join(cited_authors)}')
        print(f'   🎯 Diversidade: {len(cited_authors)}/7 livros')
    else:
        print('   ⚠️  Nenhum autor específico detectado')

    print()
    print('   💡 Preview (primeiros 500 chars):')
    print('   ' + '-'*76)
    preview = llm_text[:500].replace('\n', '\n   ')
    if len(llm_text) > 500:
        preview += '...'
    print('   ' + preview)
    print('   ' + '-'*76)

print()

# Exportar HTML
print('='*80)
print('💾 EXPORTANDO RELATÓRIO')
print('='*80)
print()

html_path = wrapper.export_formatted(
    result,
    screenplay_title='SONHOS_SEM_LEMBRANCAS_T3_DIALOGUE',
    format='html'
)

print(f'✅ HTML exportado: {html_path}')
print()

# Síntese final
synthesis = result.get('synthesis', {})
quality_score = synthesis.get('quality_score', result.get('quality_score', 0))

print('='*80)
print('✨ SÍNTESE FINAL')
print('='*80)
print()
print(f'   📊 Quality Score: {quality_score:.1f}/1.0')
print(f'   ⏱️  Tempo total: {elapsed:.1f}s')
print(f'   📚 Livros utilizados: 7')
print(f'   📄 Chunks acessados: ~{len(problems) * 5} (BM25 search)')
if cited_authors:
    print(f'   👥 Autores citados: {len(cited_authors)}')
print()

print('='*80)
print('🎉 ANÁLISE COMPLETA!')
print('='*80)
print()
print(f'Para visualizar o relatório:')
print(f'   open {html_path}')
print()
