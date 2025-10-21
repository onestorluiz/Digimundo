#!/usr/bin/env python3
"""
Teste Isolado - Core 2 Keywords para DrFormatting
Valida que recomendações de formatting mapeiam para keywords corretos
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE ISOLADO - Core 2 Keywords para Formatting")
print("="*80)
print()

# Simular análise do Core 1 (DrFormatting) com recomendações típicas
fake_core1_result = {
    'score': 65.0,
    'recommendations': [
        'Fix scene heading format - use INT./EXT. LOCATION - TIME OF DAY',
        'Screenplay too long at 145 pages - trim to 90-120 pages',
        'Add more white space - paragraphs too dense for readability',
        'Ensure character names in dialogue are properly formatted and ALL CAPS',
        'Fix dialogue formatting - parentheticals should be on own line',
        'Remove camera directions like CLOSE ON and ANGLE ON from spec script',
        'Avoid "we see" and "we hear" constructions in action lines',
        'Minimize transition usage - excessive CUT TO and FADE TO'
    ],
    'rule_violations': [
        {
            'rule_id': 'FMT.R001',
            'title': 'Scene Heading Format',
            'severity': 'critical',
            'message': 'Malformed scene headings',
            'fix': 'Use standard format'
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

# Verificar que não mapeia para ACTION ou DIALOGUE (cross-contamination)
action_contamination = [p for p in problems_found if 'show' in p.lower() or 'visual clarity' in p.lower()]
dialogue_contamination = [p for p in problems_found if 'character voice' in p.lower() or 'subtext' in p.lower()]
if action_contamination or dialogue_contamination:
    if action_contamination:
        errors.append(f"❌ Cross-contamination com action: {action_contamination}")
    if dialogue_contamination:
        errors.append(f"❌ Cross-contamination com dialogue: {dialogue_contamination}")
else:
    print("✅ Sem cross-contamination com action/dialogue")

# Verificar que a maioria dos problemas são de formatting
formatting_related = [p for p in problems_found if
                      'format' in p.lower() or 'heading' in p.lower() or
                      'white space' in p.lower() or 'page' in p.lower() or
                      'camera' in p.lower() or 'we see' in p.lower() or
                      'transition' in p.lower()]
formatting_ratio = len(formatting_related) / max(len(problems_found), 1)

if formatting_ratio >= 0.65:  # Pelo menos 65% devem ser formatting-related
    print(f"✅ Formatting-related problems: {len(formatting_related)}/{len(problems_found)} ({formatting_ratio:.0%})")
else:
    errors.append(f"❌ Poucos problemas formatting-related: {len(formatting_related)}/{len(problems_found)} ({formatting_ratio:.0%})")

# Verificar keywords específicos de formatting presentes
formatting_keywords = ['heading', 'page', 'white space', 'format', 'camera', 'transition']
found_formatting = [kw for kw in formatting_keywords if any(kw.lower() in p.lower() for p in problems_found)]
if len(found_formatting) < 4:
    errors.append(f"❌ Poucos keywords de formatting mapeados: {found_formatting}")
else:
    print(f"✅ Keywords de formatting mapeados: {len(found_formatting)}")

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
    print("✅ DrFormatting Core 2 keywords validados!")
    exit(0)
