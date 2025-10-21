#!/usr/bin/env python3
"""
Teste Isolado - Core 2 Keywords para DrAction
Valida que recomendações de action mapeiam para keywords corretos
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE ISOLADO - Core 2 Keywords para Action")
print("="*80)
print()

# Simular análise do Core 1 (DrAction) com recomendações típicas
fake_core1_result = {
    'score': 58.0,
    'recommendations': [
        'Convert internal states to observable actions (show don\'t tell)',
        'Review all action and convert to present tense',
        'Use active voice instead of passive constructions',
        'Add visual clarity with concrete, specific descriptions',
        'Remove unfilmable elements like "realizes" and "remembers"',
        'Replace weak verbs with vivid, specific verbs',
        'Keep action paragraphs concise - break up overlong blocks',
        'Improve character introductions with age and visual description'
    ],
    'rule_violations': [
        {
            'rule_id': 'ACT.R001',
            'title': 'Show Don\'t Tell',
            'severity': 'critical',
            'message': 'Too much telling, not enough showing',
            'fix': 'Visualize internal states as external actions'
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

# Verificar que não mapeia para DIALOGUE ou SUBTEXT (cross-contamination)
dialogue_contamination = [p for p in problems_found if 'natural dialogue' in p.lower() or 'character voice' in p.lower()]
subtext_contamination = [p for p in problems_found if 'on-the-nose' in p.lower() or 'contradiction' in p.lower()]
if dialogue_contamination or subtext_contamination:
    if dialogue_contamination:
        errors.append(f"❌ Cross-contamination com dialogue: {dialogue_contamination}")
    if subtext_contamination:
        errors.append(f"❌ Cross-contamination com subtext: {subtext_contamination}")
else:
    print("✅ Sem cross-contamination com dialogue/subtext")

# Verificar que a maioria dos problemas são de action (não dialogue genérico)
action_related = [p for p in problems_found if
                  'show' in p.lower() or 'tense' in p.lower() or
                  'active voice' in p.lower() or 'visual' in p.lower() or
                  'unfilmable' in p.lower() or 'verbs' in p.lower() or
                  'action' in p.lower() or 'character intro' in p.lower()]
action_ratio = len(action_related) / max(len(problems_found), 1)

if action_ratio >= 0.65:  # Pelo menos 65% devem ser action-related
    print(f"✅ Action-related problems: {len(action_related)}/{len(problems_found)} ({action_ratio:.0%})")
else:
    errors.append(f"❌ Poucos problemas action-related: {len(action_related)}/{len(problems_found)} ({action_ratio:.0%})")

# Verificar keywords específicos de action presentes
action_keywords = ['show', 'tense', 'active voice', 'visual', 'unfilmable', 'verbs']
found_action = [kw for kw in action_keywords if any(kw.lower() in p.lower() for p in problems_found)]
if len(found_action) < 4:
    errors.append(f"❌ Poucos keywords de action mapeados: {found_action}")
else:
    print(f"✅ Keywords de action mapeados: {len(found_action)}")

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
    print("✅ DrAction Core 2 keywords validados!")
    exit(0)
