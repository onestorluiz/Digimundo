#!/usr/bin/env python3
"""
Teste Isolado Core 2 - DrRelationships Keywords
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE CORE 2 - DrRelationships Keywords")
print("="*80)
print()

fake_core1_recommendations = [
    "No central relationship defined - unclear story focus",
    "Chemistry between characters is lacking - feels flat",
    "Relationship conflict is missing - too harmonious",
    "Relationship doesn't evolve - remains static throughout",
    "Relationship stakes are too low - no consequences",
    "Relationship variety is lacking - only one type shown",
    "No vulnerability shown in relationships - characters too guarded",
    "Relationship subtext is missing - everything stated directly"
]

fake_core1_analysis = {
    'specialist': 'DrRelationships',
    'score': 40,
    'recommendations': fake_core1_recommendations,
    'rule_violations': []
}

finder = ExampleFinderCore()
problems = finder._extract_problems(fake_core1_analysis)

expected_rules = {
    'RELATIONSHIP_CENTRAL',
    'RELATIONSHIP_CHEMISTRY',
    'RELATIONSHIP_CONFLICT',
    'RELATIONSHIP_EVOLUTION',
    'RELATIONSHIP_STAKES',
    'RELATIONSHIP_VARIETY',
    'RELATIONSHIP_VULNERABILITY',
    'RELATIONSHIP_SUBTEXT'
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
