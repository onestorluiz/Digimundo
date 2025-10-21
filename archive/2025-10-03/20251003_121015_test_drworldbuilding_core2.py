#!/usr/bin/env python3
"""
Teste Isolado Core 2 - DrWorldBuilding Keywords
Valida mapeamento de keywords sem rodar Core 1 ou Core 3
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE CORE 2 - DrWorldBuilding Keywords")
print("="*80)
print()

# Simular recomendações do DrWorldBuilding Core 1
print("📝 Simulando 8 tipos de recomendações DrWorldBuilding...")
fake_core1_recommendations = [
    "World establishment is unclear - readers don't understand the setting",
    "World consistency breaks in Act 2 - magic rules contradict earlier scenes",
    "Environmental detail is lacking - scenes feel generic",
    "Cultural depth is shallow - society feels one-dimensional",
    "Geography is confusing - spatial relationships unclear",
    "Time period is ambiguous - anachronisms present",
    "Technology level is inconsistent across scenes",
    "World integration is weak - world feels like backdrop to story"
]

print(f"   Total: {len(fake_core1_recommendations)} recomendações")
print()

# Criar análise fake do Core 1
fake_core1_analysis = {
    'specialist': 'DrWorldBuilding',
    'score': 55,
    'recommendations': fake_core1_recommendations,
    'rule_violations': []
}

# Criar ExampleFinderCore
print("🔧 Criando ExampleFinderCore...")
finder = ExampleFinderCore()
print()

# Mapear problemas via _extract_problems
print("🗺️  Extraindo problemas da análise Core 1...")
problems = finder._extract_problems(fake_core1_analysis)
print(f"   Problemas detectados: {len(problems)}")
print()

# Validar mapeamentos
print("="*80)
print("✅ VALIDAÇÃO DOS MAPEAMENTOS:")
print("="*80)

expected_rules = {
    'WORLD_ESTABLISHMENT',
    'WORLD_CONSISTENCY',
    'ENVIRONMENTAL_DETAIL',
    'CULTURAL_DEPTH',
    'GEOGRAPHIC_CLARITY',
    'TEMPORAL_CONSISTENCY',
    'TECHNOLOGY_CONSISTENCY',
    'WORLD_INTEGRATION'
}

found_rules = {p['rule_id'] for p in problems}

print(f"Expected: {len(expected_rules)} categorias")
print(f"Found: {len(found_rules)} categorias")
print()

# Checar cobertura
missing = expected_rules - found_rules
extra = found_rules - expected_rules

errors = []

if missing:
    errors.append(f"❌ Keywords faltando: {missing}")
else:
    print("✅ Todas as 8 categorias mapeadas!")

if extra:
    # Filtrar categorias de outros especialistas que são OK
    worldbuilding_specific = extra - {
        'STRUCTURE',  # Pode vir do DrStructure
        'THEME',  # Pode vir do DrTheme
        'SETTING'  # Genérico, OK
    }
    if worldbuilding_specific:
        errors.append(f"❌ Categorias inesperadas: {worldbuilding_specific}")
    else:
        print("✅ Nenhuma categoria extra inesperada")
else:
    print("✅ Nenhuma categoria extra")

print()

# Mostrar mapeamentos
print("🗺️  MAPEAMENTOS DETECTADOS:")
for p in problems:
    print(f"   {p['rule_id']}: {p['title']}")
print()

# Verificar cross-contamination
print("="*80)
print("🔍 VERIFICAÇÃO DE CROSS-CONTAMINATION:")
print("="*80)

# Testar com recomendações de OUTROS especialistas
other_recommendations = [
    "Add more dialogue",  # DrDialogue - não deve mapear
    "Scene is too long",  # DrPacing - não deve mapear
    "Character arc incomplete",  # DrArcs - não deve mapear
    "Theme is unclear",  # DrTheme - não deve mapear
]

other_analysis = {
    'specialist': 'Other',
    'score': 70,
    'recommendations': other_recommendations,
    'rule_violations': []
}

other_problems = finder._extract_problems(other_analysis)
other_worldbuilding_problems = [p for p in other_problems if p['rule_id'] in expected_rules]

if other_worldbuilding_problems:
    errors.append(f"❌ CROSS-CONTAMINATION! Recomendações de outros especialistas mapearam para worldbuilding: {[p['rule_id'] for p in other_worldbuilding_problems]}")
else:
    print("✅ Sem cross-contamination - keywords não capturam outros especialistas")

print()

# Resultado final
if errors:
    print("="*80)
    print("❌ TESTE FALHOU!")
    print("="*80)
    for err in errors:
        print(f"   {err}")
    print()
    exit(1)
else:
    print("="*80)
    print("🎉 TESTE PASSOU!")
    print("="*80)
    print()
    print(f"✅ {len(found_rules)} categorias worldbuilding mapeadas corretamente")
    print(f"✅ Sem cross-contamination")
    print()
    print("➡️  Pronto para teste Triple-Core completo!")
    print()
    exit(0)
