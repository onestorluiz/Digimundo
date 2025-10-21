#!/usr/bin/env python3
"""
Teste da busca de teoria - ver o que Python está encontrando
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.theory_indexer import get_theory_indexer

# Problemas típicos de diálogo
problems = [
    "[CRITICAL] Use contractions, interruptions, incomplete thoughts",
    "[HIGH] Have characters talk around issues, hide true feelings",
    "[MEDIUM] Characters should want different things from conversation"
]

print("🔍 TESTANDO BUSCA DE TEORIA\n")
print("="*70)

indexer = get_theory_indexer()

print(f"\n📚 Indexador stats:")
print(f"   {indexer.get_stats()}\n")

# Buscar teoria para cada problema
for i, problem in enumerate(problems, 1):
    print(f"\n{'='*70}")
    print(f"PROBLEMA {i}: {problem}")
    print("="*70)

    # Buscar
    results = indexer.search_for_problems([problem], limit_per_problem=2)

    if problem in results and results[problem]:
        print(f"\n✅ Encontrou {len(results[problem])} resultados:\n")

        for j, chunk in enumerate(results[problem], 1):
            print(f"--- Resultado {j} ---")
            print(f"Book: {chunk['book']}")
            print(f"Score: {chunk['score']}")
            print(f"Text preview:")
            print(chunk['text'][:400] + "..." if len(chunk['text']) > 400 else chunk['text'])
            print()
    else:
        print("\n❌ Nenhum resultado encontrado")

# Testar formatação completa
print("\n" + "="*70)
print("FORMATAÇÃO COMPLETA PARA LLM:")
print("="*70)

results = indexer.search_for_problems(problems, limit_per_problem=2)
formatted = indexer.format_theory_context(results)

print(formatted)

print(f"\n📏 Tamanho total do contexto: {len(formatted)} chars")
