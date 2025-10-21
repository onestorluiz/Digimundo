#!/usr/bin/env python3
"""Verificar Core 2 para DrDialogue"""

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from triple_core.core_2_examples.example_finder import ExampleFinderCore

screenplay_text = open('content/screenplays/personal/sonhos_sem_lembrancas_t3.txt').read()

# Core 1
specialist = DrDialogue()
core1_result = specialist.analyze(screenplay_text)

print("="*80)
print("CORE 1 - DrDialogue")
print("="*80)
print(f"Score: {core1_result['score']}/100")
print(f"Recommendations: {len(core1_result.get('recommendations', []))}")
for i, rec in enumerate(core1_result.get('recommendations', []), 1):
    print(f"  {i}. {rec}")
print()

# Core 2
finder = ExampleFinderCore()
core2_result = finder.analyze(
    base_analysis=core1_result,
    screenplay_text=screenplay_text,
    max_examples_per_problem=7
)

print("="*80)
print("CORE 2 - Example Finder")
print("="*80)
print(f"Problemas detectados: {len(core2_result['problems_analyzed'])}")
print(f"Exemplos encontrados: {core2_result['total_examples']}")
print()
print("PROBLEMAS MAPEADOS:")
for i, prob in enumerate(core2_result['problems_analyzed'], 1):
    print(f"  {i}. {prob}")
