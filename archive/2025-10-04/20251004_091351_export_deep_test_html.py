#!/usr/bin/env python3
"""
Exportar resultado do teste deep_context para HTML
"""

import sys
from pathlib import Path
import time
import re

sys.path.insert(0, str(Path.cwd()))

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper
from triple_core.exporters.formatted_exporter import FormattedExporter

print('='*80)
print('📄 EXPORTANDO TESTE DEEP CONTEXT PARA HTML')
print('='*80)

# Carregar roteiro (primeiras 1000 palavras)
screenplay_path = Path('content/screenplays/personal/sonhos_sem_lembrancas_t3.txt')
screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')
screenplay_excerpt = ' '.join(screenplay.split()[:1000])

print(f'\n📚 Roteiro carregado: {len(screenplay_excerpt.split())} palavras')

# Criar wrapper com DEEP CONTEXT
specialist = DrDialogue()
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model='scripturemon-optimized',
    llm_timeout=600,
    use_theory=True,
    deep_context=True  # ⚡ DEEP DIVE
)

print(f'\n⏳ Executando análise Deep Dive...')
start = time.time()

result = wrapper.analyze(screenplay_excerpt)
elapsed = time.time() - start

print(f'✅ Análise completa em {elapsed:.1f}s ({elapsed/60:.1f} minutos)')

# Exportar para HTML
print(f'\n📤 Exportando para HTML...')
exporter = FormattedExporter()

html_path = exporter.export_html(
    result,
    screenplay_title="SONHOS_DEEP_CONTEXT_TEST"
)

print(f'\n✅ HTML GERADO!')
print(f'📄 Arquivo: {html_path}')
print(f'💾 Tamanho: {html_path.stat().st_size:,} bytes')

# Verificar qualidade
llm_text = result.get('llm_insights', '')
scenes = len(re.findall(r'\bcena\s+\d+', llm_text, re.IGNORECASE))
quotes = len(re.findall(r'["""]([^"""]{15,})["""]', llm_text))

print(f'\n📊 Resumo:')
print(f'   Output LLM: {len(llm_text):,} chars')
print(f'   Cenas citadas: {scenes}')
print(f'   Diálogos citados: {quotes}')
print(f'   Status: {"✅ EXCELLENT" if scenes >= 3 and quotes >= 4 else "⚠️ REGULAR"}')

print(f'\n🌐 Para visualizar:')
print(f'   open {html_path}')
