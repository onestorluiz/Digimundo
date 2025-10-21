#!/usr/bin/env python3
"""
Debug: Verificar o prompt que está sendo enviado ao LLM
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

print('='*80)
print('🔍 DEBUG: Verificando prompt construído')
print('='*80)
print()

# Carregar roteiro
screenplay_path = Path('content/screenplays/personal/sonhos_sem_lembrancas_t3.txt')
screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')
screenplay_excerpt = ' '.join(screenplay.split()[:1000])

# Criar wrapper
specialist = DrDialogue()
wrapper = DualCoreWrapper(
    python_specialist=specialist,
    llm_model='scripturemon-optimized',
    use_theory=True,
    deep_context=False,
    specialist_type='all'
)

print(f'✅ Wrapper criado com specialist_type="{wrapper.specialist_type}"')
print()

# Executar análise Python
print('⏳ Executando análise Python...')
python_result = specialist.analyze(screenplay_excerpt)
print(f'✅ Python análise completa')
print()

# Construir prompt (SEM executar LLM)
print('🔨 Construindo prompt LLM...')
prompt = wrapper._build_llm_prompt(screenplay_excerpt, python_result)

print(f'✅ Prompt construído: {len(prompt):,} chars')
print()

# Salvar prompt
prompt_file = Path('workspace/outputs/debug_prompt_all_books.txt')
prompt_file.parent.mkdir(parents=True, exist_ok=True)
prompt_file.write_text(prompt, encoding='utf-8')

print(f'💾 Prompt salvo em: {prompt_file}')
print()

# Preview
print('📄 Preview do prompt (primeiros 3000 chars):')
print('='*80)
print(prompt[:3000])
print('...')
print('='*80)
print()

# Verificar palavras-chave
keywords = ['MULTI-AUTHOR', 'specialist_type', '12-14 SUBSTANTIAL', '8000-12000 characters', 'CADA autor']
print('🔍 Verificando palavras-chave no prompt:')
for kw in keywords:
    if kw in prompt:
        print(f'   ✅ "{kw}" encontrado')
    else:
        print(f'   ❌ "{kw}" NÃO encontrado')
print()

print('📊 Stats do prompt:')
print(f'   Tamanho total: {len(prompt):,} chars')
print(f'   Linhas: {len(prompt.splitlines())}')
print(f'   Palavras: {len(prompt.split())}')
print()
