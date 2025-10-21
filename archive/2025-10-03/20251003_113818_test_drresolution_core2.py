#!/usr/bin/env python3
"""
Teste Core 2 - DrResolution Keywords (isolado)
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🔍 TESTE CORE 2 - DrResolution Keywords (Isolado)")
print("="*80)
print()

# Simular análise do Core 1 (DrResolution) com recomendações típicas
fake_core1_result = {
    'score': 45.0,
    'recommendations': [
        'Rushed resolution leaves audience unsatisfied',
        'Too quick ending doesn\'t allow emotional processing',
        'Loose ends remain - multiple plot threads unresolved',
        'Incomplete resolution for secondary characters',
        'Emotional resolution is missing - no closure provided',
        'Emotional closure needed for protagonist arc',
        'Thematic resolution unclear - theme not fully resolved',
        'Theme payoff in resolution is weak',
        'Character arc resolution incomplete',
        'Character transformation not completed in ending',
        'Denouement pacing feels rushed',
        'Falling action needs better pacing',
        'Unsatisfying ending - resolution payoff missing',
        'Satisfying conclusion needed',
        'Ending too long - dragging after climax',
        'Overlong resolution loses momentum'
    ]
}

print("📝 Recomendações mock do Core 1:")
for i, rec in enumerate(fake_core1_result['recommendations'], 1):
    print(f"   {i}. {rec}")
print()

# Criar ExampleFinderCore
finder = ExampleFinderCore()

# Testar mapeamento
print("🔄 Testando mapeamento de keywords...")
result = finder.analyze(
    base_analysis=fake_core1_result,
    screenplay_text="",  # Não importa para este teste
    max_examples_per_problem=7
)

# Validar
print()
print("="*80)
print("✅ RESULTADOS:")
print("="*80)

problems = result.get('problems_analyzed', [])
total_examples = result.get('total_examples', 0)
screenplays = result.get('screenplays_searched', 0)

print(f"Problemas detectados: {len(problems)}")
print(f"Exemplos encontrados: {total_examples}")
print(f"Screenplays buscados: {screenplays}")
print()

print("✅ PROBLEMAS MAPEADOS:")
for i, prob in enumerate(problems, 1):
    print(f"{i}. {prob}")
print()

# Validações
errors = []

if len(problems) < 6:
    errors.append(f"❌ Poucos problemas detectados: {len(problems)} (esperado: 6-8)")

if total_examples < 40:
    errors.append(f"❌ Poucos exemplos: {total_examples} (esperado: ~42-56 = 6-8 × 7)")

# Anti-cross-contamination checks
problem_titles_lower = [p.lower() for p in problems]

# Verificar que não mapeia para STRUCTURE BEATS
structure_hits = [p for p in problem_titles_lower if 'structural beats' in p]
if structure_hits:
    errors.append(f"❌ Cross-contamination com structure beats: {structure_hits}")

# Verificar que não mapeia para CLIMAX
climax_hits = [p for p in problem_titles_lower if 'climax' in p and 'resolution' not in p]
if climax_hits:
    errors.append(f"❌ Cross-contamination com climax: {climax_hits}")

# Verificar que não mapeia para THEME (except thematic resolution)
theme_hits = [p for p in problem_titles_lower if 'central theme' in p or 'thematic consistency' in p]
if theme_hits:
    errors.append(f"❌ Cross-contamination com theme: {theme_hits}")

print()
if errors:
    print("❌ ERROS ENCONTRADOS:")
    for err in errors:
        print(f"   {err}")
    print()
    exit(1)
else:
    print("="*80)
    print("🎉 CORE 2 KEYWORDS VALIDADOS!")
    print("="*80)
    print()
    print("✅ Keywords mapeiam corretamente")
    print("✅ Nenhuma cross-contamination detectada")
    print("✅ Quantidade adequada de exemplos")
    print()
    exit(0)
