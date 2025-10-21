#!/usr/bin/env python3
"""
Teste Isolado Core 2 - DrOriginality Keywords
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE CORE 2 - DrOriginality Keywords")
print("="*80)
print()

fake_core1_recommendations = [
    "Concept originality is low - derivative of existing works",
    "Plot innovation is lacking - too predictable and generic",
    "Character originality is weak - stereotypical stock characters",
    "Dialogue freshness is poor - too many clichés and overused phrases",
    "Too many derivative elements - heavily derivative overall",
    "Trope usage is problematic - tropes played straight without innovation",
    "Lack of innovation - no innovation points detected",
    "Unique elements are lacking - uniqueness low across all aspects"
]

fake_core1_analysis = {
    'specialist': 'DrOriginality',
    'score': 35,
    'recommendations': fake_core1_recommendations,
    'rule_violations': []
}

finder = ExampleFinderCore()
problems = finder._extract_problems(fake_core1_analysis)

expected_rules = {
    'ORIGINALITY_CONCEPT',
    'ORIGINALITY_PLOT',
    'ORIGINALITY_CHARACTERS',
    'ORIGINALITY_DIALOGUE',
    'ORIGINALITY_DERIVATIVE',
    'ORIGINALITY_TROPES',
    'ORIGINALITY_INNOVATION',
    'ORIGINALITY_UNIQUE'
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
