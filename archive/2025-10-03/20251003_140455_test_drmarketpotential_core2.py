#!/usr/bin/env python3
"""
Teste Isolado Core 2 - DrMarketPotential Keywords
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE CORE 2 - DrMarketPotential Keywords")
print("="*80)
print()

fake_core1_recommendations = [
    "Market potential is weak - limited commercial viability",
    "Audience appeal is narrow - limited audience size and engagement",
    "Hook lacks market strength - not a strong marketable concept",
    "Genre marketability is weak - genre has limited commercial potential",
    "Commercial elements are weak - lacks strong commercial appeal",
    "Market risks are high - significant commercial risk factors",
    "Revenue potential is low - weak return on investment",
    "International appeal is limited - not suitable for global markets"
]

fake_core1_analysis = {
    'specialist': 'DrMarketPotential',
    'score': 40,
    'recommendations': fake_core1_recommendations,
    'rule_violations': []
}

finder = ExampleFinderCore()
problems = finder._extract_problems(fake_core1_analysis)

expected_rules = {
    'MARKET_VIABILITY',
    'MARKET_AUDIENCE',
    'MARKET_HOOK',
    'MARKET_GENRE',
    'MARKET_ELEMENTS',
    'MARKET_RISKS',
    'MARKET_REVENUE',
    'MARKET_GLOBAL'
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
