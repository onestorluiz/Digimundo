#!/usr/bin/env python3
"""
Teste Isolado - Core 2 Keywords para DrTheme
Valida que recomendações de theme mapeiam para keywords corretos
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE ISOLADO - Core 2 Keywords para Theme")
print("="*80)
print()

# Simular análise do Core 1 (DrTheme) com recomendações típicas
fake_core1_result = {
    'score': 68.0,
    'recommendations': [
        'Establish a clear central theme to unify the story',
        'Strengthen thematic consistency throughout all acts',
        'Express themes more subtly through action and subtext',
        'Add supporting themes to create thematic depth',
        'Provide clearer thematic resolution in the final act',
        'Include opposing viewpoints to create thematic complexity',
        'Show theme through character actions, not just dialogue',
        'Make thematic choices matter to characters'
    ],
    'rule_violations': [
        {
            'rule_id': 'THE.R001',
            'title': 'Clear Central Theme',
            'severity': 'critical',
            'message': 'No clear central theme identified',
            'fix': 'Establish a clear central theme that drives the story'
        }
    ]
}

print("📋 RECOMENDAÇÕES SIMULADAS DO CORE 1:")
for i, rec in enumerate(fake_core1_result['recommendations'], 1):
    print(f"{i}. {rec}")
print()

# Executar Core 2
print("📚 Executando Core 2 (ExampleFinder)...")
finder = ExampleFinderCore()
core2_result = finder.analyze(
    base_analysis=fake_core1_result,
    screenplay_text="",  # Não importa para este teste
    max_examples_per_problem=7
)

print(f"   Problemas detectados: {len(core2_result['problems_analyzed'])}")
print(f"   Exemplos encontrados: {core2_result['total_examples']}")
print()

# Validar mapeamento
print("="*80)
print("🔍 MAPEAMENTO DE KEYWORDS:")
print("="*80)
print()

problems_found = core2_result['problems_analyzed']

# Expected mappings
expected_keywords = {
    'Central theme': 'CENTRAL_THEME',
    'Consistency': 'THEME_CONSISTENCY',
    'Subtly': 'HEAVY_HANDED',
    'Thematic depth': 'THEMATIC_DEPTH',
    'Resolution': 'THEME_RESOLUTION',
    'Opposing viewpoints': 'OPPOSING_VIEWS',
    'Theme through action': 'SHOW_NOT_TELL',
    'Theme stakes': 'THEME_STAKES'
}

print(f"✅ PROBLEMAS MAPEADOS ({len(problems_found)}):")
for i, prob in enumerate(problems_found, 1):
    print(f"{i}. {prob}")
print()

# Validações
print("="*80)
print("✅ VALIDAÇÕES:")
print("="*80)

errors = []

# Deve ter detectado pelo menos 6 problemas (cada recomendação mapeou)
if len(problems_found) < 6:
    errors.append(f"❌ Poucos problemas detectados: {len(problems_found)} (esperado ≥6)")
else:
    print(f"✅ Problemas detectados: {len(problems_found)}")

# Deve ter encontrado exemplos (7 por problema)
expected_examples = len(problems_found) * 7
if core2_result['total_examples'] < expected_examples * 0.5:  # 50% tolerance
    errors.append(f"❌ Poucos exemplos: {core2_result['total_examples']} (esperado ~{expected_examples})")
else:
    print(f"✅ Exemplos encontrados: {core2_result['total_examples']} (~{len(problems_found)}×7)")

# Verificar que não mapeia para DIALOGUE (cross-contamination)
dialogue_contamination = [p for p in problems_found if 'voice' in p.lower() or 'subtext' in p.lower() and 'theme' not in p.lower()]
if dialogue_contamination:
    errors.append(f"❌ Cross-contamination com dialogue: {dialogue_contamination}")
else:
    print("✅ Sem cross-contamination com dialogue")

# Verificar que a maioria dos problemas são de theme (não structure ou outros)
theme_related = [p for p in problems_found if 'theme' in p.lower() or 'opposing' in p.lower()]
non_theme = [p for p in problems_found if 'theme' not in p.lower() and 'opposing' not in p.lower()]
theme_ratio = len(theme_related) / max(len(problems_found), 1)

if theme_ratio >= 0.6:  # Pelo menos 60% devem ser theme-related
    print(f"✅ Theme-related problems: {len(theme_related)}/{len(problems_found)} ({theme_ratio:.0%})")
else:
    errors.append(f"❌ Poucos problemas theme-related: {len(theme_related)}/{len(problems_found)} ({theme_ratio:.0%})")

# Verificar keywords específicos de theme presentes
theme_keywords = ['Central theme', 'Thematic consistency', 'Multiple theme layers', 'Opposing']
found_theme = [kw for kw in theme_keywords if any(kw.lower() in p.lower() for p in problems_found)]
if len(found_theme) < 3:
    errors.append(f"❌ Poucos keywords de theme mapeados: {found_theme}")
else:
    print(f"✅ Keywords de theme mapeados: {len(found_theme)}")

print()

if errors:
    print("="*80)
    print("❌ ERROS ENCONTRADOS:")
    print("="*80)
    for err in errors:
        print(f"   {err}")
    print()
    exit(1)
else:
    print("="*80)
    print("🎉 TODOS OS TESTES PASSARAM!")
    print("="*80)
    print()
    print(f"📊 RESUMO:")
    print(f"   Problemas detectados: {len(problems_found)}")
    print(f"   Exemplos encontrados: {core2_result['total_examples']}")
    print(f"   Ratio: ~{core2_result['total_examples'] // max(len(problems_found), 1)} exemplos/problema")
    print(f"   Screenplays pesquisados: {core2_result['screenplays_searched']}")
    print()
    print("✅ DrTheme Core 2 keywords validados!")
    exit(0)
