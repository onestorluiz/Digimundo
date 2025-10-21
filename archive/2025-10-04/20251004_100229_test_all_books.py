#!/usr/bin/env python3
"""
Teste: DrDialogue com specialist_type='all' (TODOS os 13 livros)
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path.cwd()))

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

print('='*80)
print('📚 TESTE: DrDialogue com TODOS OS 13 LIVROS')
print('='*80)
print()

# Carregar roteiro (primeiras 1000 palavras)
screenplay_path = Path('content/screenplays/personal/sonhos_sem_lembrancas_t3.txt')
screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')
screenplay_excerpt = ' '.join(screenplay.split()[:1000])

print(f'📄 Roteiro: {len(screenplay_excerpt.split())} palavras')
print()

# Criar wrapper com specialist_type='all'
print('🔧 Configurando DualCoreWrapper...')
specialist = DrDialogue()
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model='scripturemon-optimized',
    llm_timeout=600,
    use_theory=True,
    deep_context=True,
    specialist_type='all'  # ⚡ TODOS OS LIVROS!
)

print(f'   ✅ Specialist: {wrapper.specialist_name}')
print(f'   ✅ Theory Mode: specialist_type="all"')
print(f'   ✅ Deep Context: {wrapper.deep_context}')
print()

# Executar análise
print('⏳ Executando análise Deep Dive com TODOS os livros...')
print('   (Estimativa: ~7-10 minutos)')
print()

start = time.time()
result = wrapper.analyze(screenplay_excerpt)
elapsed = time.time() - start

print()
print('='*80)
print('✅ ANÁLISE COMPLETA!')
print('='*80)
print()
print(f'⏱️  Tempo: {elapsed:.1f}s ({elapsed/60:.1f} minutos)')

# Verificar output
llm_text = result.get('llm_insights', '')
print(f'📏 Output LLM: {len(llm_text):,} chars ({len(llm_text.split())} palavras)')
print()

# Verificar citações por autor
print('📚 Verificando citações por autor:')
authors_found = []
for author in ['MCKEE', 'TRUBY', 'CAMPBELL', 'SNYDER', 'FIELD', 'EGRI', 'VOGLER', 'SEGER', 'WEILAND']:
    if author in llm_text.upper():
        count = llm_text.upper().count(author)
        authors_found.append(f"   ✅ {author}: {count} menções")

if authors_found:
    print('\n'.join(authors_found))
else:
    print('   ⚠️  Nenhuma citação de autor detectada no output')
print()

# Exportar para HTML
print('📤 Exportando para HTML...')
html_path = wrapper.export_formatted(
    result,
    screenplay_title="SONHOS_ALL_BOOKS_TEST",
    format="html",
    auto_open=False
)

print(f'✅ HTML gerado: {html_path}')
print(f'💾 Tamanho: {html_path.stat().st_size:,} bytes')
print()

# Preview do output
print('📄 Preview (primeiros 2000 chars):')
print('-' * 80)
print(llm_text[:2000])
print('-' * 80)
print()

print('🌐 Para visualizar no browser:')
print(f'   open {html_path}')
print()
