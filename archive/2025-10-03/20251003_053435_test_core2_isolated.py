#!/usr/bin/env python3
"""
Teste Isolado - Core 2 (Example Finder)
Testa apenas o mapeamento de keywords sem rodar LLM
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE ISOLADO - CORE 2 (EXAMPLE FINDER)")
print("="*80)
print()

# Simular resultado do Core 1 (DrDialogue)
fake_core1_result = {
    'specialist': {
        'name': 'DrDialogue'
    },
    'score': 100.0,
    'recommendations': [
        "Have characters talk around issues instead of stating them directly",
        "Give each character unique vocabulary, rhythm, and speech patterns",
        "Add more subtext to dialogue",
        "Avoid on-the-nose dialogue that states emotions",
        "Reduce exposition dumps",
        "Improve natural speech rhythm",
        "Add more conflict in dialogue",
    ]
}

print("📋 CORE 1 (Simulado) - Recomendações:")
for i, rec in enumerate(fake_core1_result['recommendations'], 1):
    print(f"   {i}. {rec}")
print()

# Criar Core 2
print("🔧 Criando ExampleFinderCore...")
core2 = ExampleFinderCore()
print()

# Analisar
print("⚡ Executando Core 2...")
result = core2.analyze(
    base_analysis=fake_core1_result,
    screenplay_text="dummy screenplay text"
)
print()

# Resultados
print("="*80)
print("✅ RESULTADOS DO CORE 2")
print("="*80)
print()

print(f"📊 ESTATÍSTICAS:")
print(f"   Problemas analisados: {len(result['problems_analyzed'])}")
print(f"   Exemplos encontrados: {result['total_examples']}")
print(f"   Roteiros pesquisados: {result['screenplays_searched']}")
print()

print(f"🔍 PROBLEMAS MAPEADOS:")
for i, problem in enumerate(result['problems_analyzed'], 1):
    print(f"   {i}. {problem}")
print()

print(f"📚 EXEMPLOS POR PROBLEMA:")
# Agrupar por problema
examples_by_problem = {}
for ex in result['examples_found']:
    problem = ex['problem_addressed']
    if problem not in examples_by_problem:
        examples_by_problem[problem] = []
    examples_by_problem[problem].append(ex)

for problem, examples in examples_by_problem.items():
    print(f"\n   🎯 {problem}:")
    print(f"      {len(examples)} exemplos encontrados")
    for ex in examples[:3]:  # Mostrar só 3
        print(f"      • {ex['screenplay']}: {ex['character']}")

print()
print("="*80)
print("🎉 TESTE CONCLUÍDO")
print("="*80)
print()

# Validação
print("✅ VALIDAÇÕES:")
errors = []

# Validar que "talk around" mapeia para SUBTEXT
if "Lacking subtext in dialogue" not in result['problems_analyzed']:
    errors.append("❌ 'talk around' não mapeou para SUBTEXT")
else:
    print("   ✅ 'talk around' → SUBTEXT (correto)")

# Validar que temos vários problemas diferentes
if len(set(result['problems_analyzed'])) < 3:
    errors.append(f"❌ Poucos problemas únicos: {len(set(result['problems_analyzed']))}")
else:
    print(f"   ✅ {len(set(result['problems_analyzed']))} problemas únicos detectados")

# Validar que não mapeou para STRUCTURE
if "Three-act structure problems" in result['problems_analyzed']:
    errors.append("❌ Mapeou incorretamente para STRUCTURE")
else:
    print("   ✅ Não mapeou para STRUCTURE (correto)")

# Validar que temos exemplos suficientes
if result['total_examples'] < 20:
    errors.append(f"❌ Poucos exemplos: {result['total_examples']}")
else:
    print(f"   ✅ {result['total_examples']} exemplos encontrados (bom)")

print()
if errors:
    print("❌ ERROS ENCONTRADOS:")
    for err in errors:
        print(f"   {err}")
    sys.exit(1)
else:
    print("🎉 TODOS OS TESTES PASSARAM!")
    sys.exit(0)
