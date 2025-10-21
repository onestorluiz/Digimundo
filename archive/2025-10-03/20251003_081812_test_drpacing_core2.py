#!/usr/bin/env python3
"""
Teste Isolado - Core 2 Keywords para DrPacing
Valida que recomendações de pacing mapeiam para keywords corretos
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE ISOLADO - Core 2 Keywords para Pacing")
print("="*80)
print()

# Simular análise do Core 1 (DrPacing) com recomendações típicas
fake_core1_result = {
    'score': 65.0,
    'recommendations': [
        'Vary scene lengths: quick 1-page beats between 2-3 page dramatic scenes',
        'Break up paragraphs - max 4 lines per action block for white space',
        'Shorten scenes and increase cuts as approaching climax for momentum',
        'Insert character moments after action sequences for breathing room',
        'Tighten first 10 pages - cut exposition, start later in opening',
        'Add subplot complications, raise stakes at midpoint to fix Act 2 sag',
        'Use match cuts, momentum cuts for better transitions',
        'Aim for 40-60% dialogue-to-action ratio balance'
    ],
    'rule_violations': [
        {
            'rule_id': 'PACE.R001',
            'title': 'Scene Length Balance',
            'severity': 'high',
            'message': 'Scenes too uniform in length',
            'fix': 'Vary scene lengths for better rhythm'
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
    'Scene length balance': 'SCENE_LENGTH',
    'White space': 'WHITE_SPACE',
    'Momentum': 'MOMENTUM',
    'Breathing room': 'BREATHING_ROOM',
    'Opening': 'OPENING_PACE',
    'Act 2': 'ACT2_SAG',
    'Transition': 'TRANSITIONS',
    'Dialogue ratio': 'DIALOGUE_RATIO'
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
dialogue_contamination = [p for p in problems_found if 'voice' in p.lower() or 'subtext' in p.lower()]
if dialogue_contamination:
    errors.append(f"❌ Cross-contamination com dialogue: {dialogue_contamination}")
else:
    print("✅ Sem cross-contamination com dialogue")

# Verificar keywords de pacing foram capturados (não apenas genéricos)
pacing_specific = ['Scene length balance', 'White space', 'Momentum', 'Breathing room', 'Transition']
found_pacing_specific = [kw for kw in pacing_specific if any(kw.lower() in p.lower() for p in problems_found)]
if len(found_pacing_specific) >= 3:
    print(f"✅ Keywords específicos de pacing presentes: {len(found_pacing_specific)}")
else:
    errors.append(f"❌ Poucos keywords específicos: {found_pacing_specific}")

# Verificar keywords específicos de pacing presentes
pacing_keywords = ['Scene length balance', 'White space', 'Momentum', 'Breathing room']
found_pacing = [kw for kw in pacing_keywords if any(kw.lower() in p.lower() for p in problems_found)]
if len(found_pacing) < 3:
    errors.append(f"❌ Poucos keywords de pacing mapeados: {found_pacing}")
else:
    print(f"✅ Keywords de pacing mapeados: {len(found_pacing)}")

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
    print("✅ DrPacing Core 2 keywords validados!")
    exit(0)
