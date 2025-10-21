#!/usr/bin/env python3
"""
Teste Isolado - Core 2 Keywords para DrTransitions
Valida que recomendações de transitions mapeiam para keywords corretos
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE ISOLADO - Core 2 Keywords para Transitions")
print("="*80)
print()

# Simular análise do Core 1 (DrTransitions) com recomendações típicas
fake_core1_result = {
    'score': 58.0,
    'recommendations': [
        'Avoid jarring transitions - create smoother connections between scenes',
        'Improve smooth flow and seamless transitions between sequences',
        'Scene loses momentum - transitions stall the narrative drive',
        'Use match cuts to create visual connections between scenes',
        'Establish clearer cause-and-effect relationships between scenes',
        'Add temporal clarity - unclear when scenes take place',
        'Strengthen connective tissue between scenes for better flow',
        'Improve flow rhythm - transition pacing feels uneven'
    ],
    'rule_violations': [
        {
            'rule_id': 'TRN.R001',
            'title': 'Jarring Transitions',
            'severity': 'high',
            'message': 'Abrupt scene changes',
            'fix': 'Create smoother connections'
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

# Verificar que não mapeia para PACING ou STRUCTURE (cross-contamination)
pacing_contamination = [p for p in problems_found if 'scene length' in p.lower() or 'white space' in p.lower()]
structure_contamination = [p for p in problems_found if 'three-act' in p.lower() or 'plot point' in p.lower()]
if pacing_contamination or structure_contamination:
    if pacing_contamination:
        errors.append(f"❌ Cross-contamination com pacing: {pacing_contamination}")
    if structure_contamination:
        errors.append(f"❌ Cross-contamination com structure: {structure_contamination}")
else:
    print("✅ Sem cross-contamination com pacing/structure")

# Verificar que a maioria dos problemas são de transitions/flow
transitions_related = [p for p in problems_found if
                       'transition' in p.lower() or 'flow' in p.lower() or
                       'jarring' in p.lower() or 'smooth' in p.lower() or
                       'momentum' in p.lower() or 'connection' in p.lower() or
                       'scene' in p.lower()]
transitions_ratio = len(transitions_related) / max(len(problems_found), 1)

if transitions_ratio >= 0.65:  # Pelo menos 65% devem ser transitions-related
    print(f"✅ Transitions-related problems: {len(transitions_related)}/{len(problems_found)} ({transitions_ratio:.0%})")
else:
    errors.append(f"❌ Poucos problemas transitions-related: {len(transitions_related)}/{len(problems_found)} ({transitions_ratio:.0%})")

# Verificar keywords específicos de transitions presentes
transitions_keywords = ['transition', 'flow', 'jarring', 'smooth', 'momentum', 'connection']
found_transitions = [kw for kw in transitions_keywords if any(kw.lower() in p.lower() for p in problems_found)]
if len(found_transitions) < 4:
    errors.append(f"❌ Poucos keywords de transitions mapeados: {found_transitions}")
else:
    print(f"✅ Keywords de transitions mapeados: {len(found_transitions)}")

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
    print("✅ DrTransitions Core 2 keywords validados!")
    exit(0)
