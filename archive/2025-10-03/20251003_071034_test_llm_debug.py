#!/usr/bin/env python3
"""
Debug: Verificar prompt enviado ao LLM
"""

import subprocess
from triple_core.core_1_specialists.structure.dr_structure import DrStructure
from triple_core.orchestrators.triple_core_wrapper import TripleCoreWrapper

# Carregar screenplay
screenplay_text = open('workspace/inputs/test_screenplay.txt').read()

# Criar especialista
specialist = DrStructure()

# Criar wrapper
wrapper = TripleCoreWrapper(
    python_specialist=specialist,
    llm_model="scripturemon-optimized",
    deep_context=True
)

# Core 1
core1_result = specialist.analyze(screenplay_text)
print("="*80)
print("CORE 1 RESULT:")
print(f"Score: {core1_result.get('score')}")
print(f"Recommendations: {len(core1_result.get('recommendations', []))}")
print()

# Construir prompt (método herdado do DualCoreWrapper)
llm_prompt = wrapper._build_llm_prompt(
    screenplay_text=screenplay_text,
    python_result=core1_result
)

print("="*80)
print("LLM PROMPT (primeiros 1000 chars):")
print(llm_prompt[:1000])
print(f"\n... (total: {len(llm_prompt)} chars)")
print()

# Testar chamada LLM
print("="*80)
print("TESTANDO LLM...")
result = subprocess.run(
    ['ollama', 'run', 'scripturemon-optimized'],
    input=llm_prompt,
    capture_output=True,
    text=True,
    timeout=60
)

print(f"Return code: {result.returncode}")
print(f"Stdout length: {len(result.stdout)}")
print(f"Stderr length: {len(result.stderr)}")
print()

if result.stdout:
    print("STDOUT (primeiros 500 chars):")
    print(result.stdout[:500])
else:
    print("❌ STDOUT VAZIO!")

if result.stderr:
    print("\nSTDERR:")
    print(result.stderr)
