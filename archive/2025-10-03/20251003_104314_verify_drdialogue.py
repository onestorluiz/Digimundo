#!/usr/bin/env python3
"""Verificar score real do DrDialogue"""

from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue

screenplay_text = open('content/screenplays/personal/sonhos_sem_lembrancas_t3.txt').read()

specialist = DrDialogue()
result = specialist.analyze(screenplay_text)

print("="*80)
print("VERIFICAÇÃO DrDialogue")
print("="*80)
print(f"Score: {result['score']}/100")
print(f"Recommendations: {len(result.get('recommendations', []))}")
print()
print("RECOMENDAÇÕES:")
for i, rec in enumerate(result.get('recommendations', [])[:10], 1):
    print(f"{i}. {rec}")
