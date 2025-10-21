#!/usr/bin/env python3
"""
Teste rápido com um único autor para validar correção
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path.cwd()))

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

print('='*80)
print('🧪 TESTE RÁPIDO: Um Autor (TRUBY)')
print('='*80)
print()

# Carregar roteiro
screenplay_path = Path('content/screenplays/personal/sonhos_sem_lembrancas_t3.txt')
screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')
screenplay_excerpt = ' '.join(screenplay.split()[:1000])

print(f'📄 Roteiro: {len(screenplay_excerpt.split())} palavras')
print()

# Criar wrapper para Truby
print('📖 Analisando com TRUBY...')
specialist = DrDialogue()
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model='scripturemon-optimized',
    llm_timeout=900,
    use_theory=True,
    deep_context=True,
    specialist_type='truby'
)

print('⏳ Executando análise Deep...')
start = time.time()

result = wrapper.analyze(screenplay_excerpt)

elapsed = time.time() - start
llm_text = result.get('llm_insights', '')

print(f'✅ Completo em {elapsed:.1f}s')
print(f'📏 Output: {len(llm_text):,} chars')
print()

# Verificar se menciona Truby
if 'truby' in llm_text.lower():
    print('✅ SUCESSO: Menciona "Truby"')
else:
    print('⚠️  NÃO menciona "Truby"')

if 'mckee' in llm_text.lower():
    print('⚠️  AINDA menciona "McKee"')
else:
    print('✅ SUCESSO: NÃO menciona "McKee"')

# Export HTML
html_path = wrapper.export_formatted(
    result,
    screenplay_title="TEST_TRUBY_SINGLE",
    format="html",
    auto_open=True
)

print()
print(f'💾 HTML salvo: {html_path}')
print('🌐 Abrindo no browser...')
