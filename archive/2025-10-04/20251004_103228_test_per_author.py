#!/usr/bin/env python3
"""
Análise POR AUTOR: Gera 1 HTML profundo para cada autor
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path.cwd()))

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

# Lista de autores para analisar
AUTHORS = ['mckee', 'truby', 'campbell', 'vogler', 'seger', 'field']

print('='*80)
print('🎯 ANÁLISE POR AUTOR - Profundidade Máxima')
print('='*80)
print()

# Carregar roteiro
screenplay_path = Path('content/screenplays/personal/sonhos_sem_lembrancas_t3.txt')
screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')
screenplay_excerpt = ' '.join(screenplay.split()[:1000])

print(f'📄 Roteiro: {len(screenplay_excerpt.split())} palavras')
print(f'📚 Autores para analisar: {len(AUTHORS)}')
print()

total_chars = 0
total_time = 0

for i, author in enumerate(AUTHORS, 1):
    print(f'\n{"="*80}')
    print(f'📖 [{i}/{len(AUTHORS)}] Analisando com {author.upper()}...')
    print(f'{"="*80}\n')

    # Criar wrapper específico para este autor
    specialist = DrDialogue()
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model='scripturemon-optimized',
        llm_timeout=900,
        use_theory=True,
        deep_context=True,  # Livro completo
        specialist_type=author  # UM autor por vez
    )

    print(f'⏳ Executando análise Deep com {author.upper()}...')
    start = time.time()

    result = wrapper.analyze(screenplay_excerpt)

    elapsed = time.time() - start
    total_time += elapsed

    llm_text = result.get('llm_insights', '')
    total_chars += len(llm_text)

    print(f'✅ Completo em {elapsed:.1f}s')
    print(f'📏 Output: {len(llm_text):,} chars')

    # Export HTML
    html_path = wrapper.export_formatted(
        result,
        screenplay_title=f"SONHOS_ANALISE_{author.upper()}",
        format="html",
        auto_open=False
    )

    print(f'💾 HTML salvo: {html_path.name}')

print(f'\n{"="*80}')
print('✅ TODAS AS ANÁLISES COMPLETAS!')
print(f'{"="*80}\n')

print(f'📊 Estatísticas:')
print(f'   Total de autores: {len(AUTHORS)}')
print(f'   Tempo total: {total_time:.1f}s ({total_time/60:.1f} min)')
print(f'   Output total: {total_chars:,} chars')
print(f'   Média por autor: {total_chars/len(AUTHORS):,.0f} chars')
print()

print(f'📁 Arquivos HTML gerados em:')
print(f'   workspace/outputs/formatted/SONHOS_ANALISE_*.html')
print()

print('💡 Para visualizar:')
print('   open workspace/outputs/formatted/SONHOS_ANALISE_*.html')
print()
