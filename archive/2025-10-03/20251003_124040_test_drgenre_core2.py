#!/usr/bin/env python3
"""
Teste Isolado Core 2 - DrGenre Keywords
Valida mapeamento de keywords sem rodar Core 1 ou Core 3
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE CORE 2 - DrGenre Keywords")
print("="*80)
print()

# Simular recomendações do DrGenre Core 1
print("📝 Simulando 8 tipos de recomendações DrGenre...")
fake_core1_recommendations = [
    "Genre identity is unclear and confusing to audience",
    "Missing essential conventions for the drama genre",
    "Tropes are missing - need to use genre tropes appropriately",
    "Audience expectations are not met for this genre",
    "Hybrid genres are unbalanced - drama and comedy don't blend well",
    "Genre pacing doesn't match typical thriller pacing",
    "Genre tone is misaligned with horror conventions",
    "Tropes are predictable and cliché - need trope subversion"
]

print(f"   Total: {len(fake_core1_recommendations)} recomendações")
print()

# Criar análise fake do Core 1
fake_core1_analysis = {
    'specialist': 'DrGenre',
    'score': 45,
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
    'GENRE_CLARITY',
    'GENRE_CONVENTIONS',
    'GENRE_TROPES',
    'GENRE_EXPECTATIONS',
    'GENRE_HYBRID',
    'GENRE_PACING',
    'GENRE_TONE',
    'TROPE_SUBVERSION'
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
    genre_specific = extra - {
        'THEME',  # Pode vir do DrTheme
        'PACING',  # Pode vir do DrPacing (genérico)
        'TONE'  # Pode vir do DrTone (genérico)
    }
    if genre_specific:
        errors.append(f"❌ Categorias inesperadas: {genre_specific}")
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
    "Scene pacing is slow",  # DrPacing - não deve mapear
    "Theme is unclear",  # DrTheme - não deve mapear
    "Character arcs weak",  # DrArcs - não deve mapear
]

other_analysis = {
    'specialist': 'Other',
    'score': 70,
    'recommendations': other_recommendations,
    'rule_violations': []
}

other_problems = finder._extract_problems(other_analysis)
other_genre_problems = [p for p in other_problems if p['rule_id'] in expected_rules]

if other_genre_problems:
    errors.append(f"❌ CROSS-CONTAMINATION! Recomendações de outros especialistas mapearam para genre: {[p['rule_id'] for p in other_genre_problems]}")
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
    print(f"✅ {len(found_rules)} categorias genre mapeadas corretamente")
    print(f"✅ Sem cross-contamination")
    print()
    print("➡️  Pronto para teste Triple-Core completo!")
    print()
    exit(0)
