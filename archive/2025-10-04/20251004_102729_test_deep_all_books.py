#!/usr/bin/env python3
"""
Teste FINAL: deep_context=True + specialist_type='all'
Análise MÁXIMA com todos os 13 livros completos
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path.cwd()))

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

print('='*80)
print('🚀 TESTE MÁXIMO: Deep Context + TODOS OS 13 LIVROS')
print('='*80)
print()

# Carregar roteiro (primeiras 1000 palavras)
screenplay_path = Path('content/screenplays/personal/sonhos_sem_lembrancas_t3.txt')
screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')
screenplay_excerpt = ' '.join(screenplay.split()[:1000])

print(f'📄 Roteiro: {len(screenplay_excerpt.split())} palavras')
print()

# Criar wrapper com DEEP CONTEXT + ALL BOOKS
print('🔧 Configurando DualCoreWrapper...')
specialist = DrDialogue()
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model='scripturemon-optimized',
    llm_timeout=900,  # 15 minutos
    use_theory=True,
    deep_context=True,  # ⚡ DEEP = livros completos
    specialist_type='all'  # ⚡ ALL = todos os 13 livros
)

print(f'   ✅ Specialist: {wrapper.specialist_name}')
print(f'   ✅ Theory Mode: specialist_type="all" + deep_context=True')
print(f'   ✅ Modelo: {wrapper.llm_model} (128k context)')
print(f'   ✅ Timeout: 15 minutos')
print()
print('⚠️  ATENÇÃO: Isso vai carregar MUITA teoria. Tempo estimado: 10-15 min')
print()

# Executar análise
print('⏳ Executando análise DEEP com TODOS os livros...')
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

# Verificar autores
print('📚 Verificando autores mencionados:')
authors_found = []
for author in ['MCKEE', 'TRUBY', 'CAMPBELL', 'SNYDER', 'FIELD', 'EGRI', 'VOGLER', 'SEGER', 'WEILAND']:
    if author in llm_text.upper():
        count = llm_text.upper().count(author)
        authors_found.append(f"   ✅ {author}: {count} menções")

if authors_found:
    print('\n'.join(authors_found))
print()

# Salvar output
output_file = Path('workspace/outputs/test_deep_all_books_result.txt')
output_file.parent.mkdir(parents=True, exist_ok=True)
output_file.write_text(llm_text, encoding='utf-8')
print(f'💾 Output completo salvo em: {output_file}')
print()

# Exportar HTML
print('📤 Exportando para HTML...')
html_path = wrapper.export_formatted(
    result,
    screenplay_title="SONHOS_DEEP_ALL_BOOKS",
    format="html",
    auto_open=True
)

print(f'✅ HTML gerado: {html_path}')
print(f'💾 Tamanho: {html_path.stat().st_size:,} bytes')
print()

# Comparação
print('📊 COMPARAÇÃO:')
print(f'   Shallow (chunks): ~4,000 chars')
print(f'   Deep + All: {len(llm_text):,} chars')
print(f'   Aumento: {len(llm_text)/4000:.1f}x')
print()

print('✅ HTML aberto no browser!')
print()
