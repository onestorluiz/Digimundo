#!/usr/bin/env python3
"""
Teste Isolado Core 2 - DrArcs Keywords
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE CORE 2 - DrArcs Keywords")
print("="*80)
print()

fake_core1_recommendations = [
    "Character arc is not established - unclear trajectory",
    "No transformation shown - character remains unchanged",
    "Missing catalyst for change - no inciting incident",
    "Transformation feels unearned - sudden change",
    "No resistance to change shown - character accepts too easily",
    "Cost of change not shown - no sacrifice or price paid",
    "Arc is incomplete and unresolved at the end",
    "Static character with flat arc - consider if appropriate"
]

fake_core1_analysis = {
    'specialist': 'DrArcs',
    'score': 45,
    'recommendations': fake_core1_recommendations,
    'rule_violations': []
}

finder = ExampleFinderCore()
problems = finder._extract_problems(fake_core1_analysis)

expected_rules = {
    'ARC_ESTABLISHMENT',
    'ARC_TRANSFORMATION',
    'ARC_CATALYST',
    'ARC_EARNED',
    'ARC_RESISTANCE',
    'ARC_COST',
    'ARC_COMPLETION',
    'FLAT_ARC'
}

found_rules = {p['rule_id'] for p in problems}

print(f"Expected: {len(expected_rules)} categorias")
print(f"Found: {len(found_rules)} categorias")
print()

errors = []

if expected_rules != found_rules:
    missing = expected_rules - found_rules
    extra = found_rules - expected_rules
    if missing:
        errors.append(f"❌ Keywords faltando: {missing}")
    if extra:
        errors.append(f"❌ Categorias inesperadas: {extra}")
else:
    print("✅ Todas as 8 categorias mapeadas!")
    print()
    for rule in sorted(found_rules):
        print(f"   ✅ {rule}")

if errors:
    print("❌ TESTE FALHOU!")
    for err in errors:
        print(f"   {err}")
    exit(1)
else:
    print()
    print("🎉 TESTE PASSOU!")
    exit(0)
