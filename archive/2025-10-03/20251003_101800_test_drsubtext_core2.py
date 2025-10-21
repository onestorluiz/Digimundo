#!/usr/bin/env python3
"""
Teste Isolado - Core 2 Keywords para DrSubtext
Valida que recomendações de subtext mapeiam para keywords corretos
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE ISOLADO - Core 2 Keywords para Subtext")
print("="*80)
print()

# Simular análise do Core 1 (DrSubtext) com recomendações típicas
fake_core1_result = {
    'score': 55.0,
    'recommendations': [
        'Reduce on-the-nose dialogue where characters state emotions directly',
        'Add layers of subtext to create implicit meaning',
        'Use contradictions - characters saying one thing, meaning another',
        'Develop power dynamics in relationships for richer subtext',
        'Give characters hidden agendas and ulterior motives',
        'Use pauses and beats to create meaningful silences',
        'Add avoidance patterns where characters deflect',
        'Incorporate irony and double meanings for depth'
    ],
    'rule_violations': [
        {
            'rule_id': 'SUB.R001',
            'title': 'On-the-Nose Dialogue',
            'severity': 'high',
            'message': 'Too much direct statement of emotions',
            'fix': 'Communicate emotions indirectly'
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

# Verificar que não mapeia para THEME ou TONE (cross-contamination)
theme_contamination = [p for p in problems_found if 'central theme' in p.lower() or 'thematic anchor' in p.lower()]
tone_contamination = [p for p in problems_found if 'tonal consistency' in p.lower() or 'establish tone' in p.lower()]
if theme_contamination or tone_contamination:
    if theme_contamination:
        errors.append(f"❌ Cross-contamination com theme: {theme_contamination}")
    if tone_contamination:
        errors.append(f"❌ Cross-contamination com tone: {tone_contamination}")
else:
    print("✅ Sem cross-contamination com theme/tone")

# Verificar que a maioria dos problemas são de subtext (não dialogue genérico)
subtext_related = [p for p in problems_found if 'subtext' in p.lower() or 'on-the-nose' in p.lower() or 'contradiction' in p.lower() or 'power dynamic' in p.lower() or 'hidden agenda' in p.lower() or 'silence' in p.lower()]
subtext_ratio = len(subtext_related) / max(len(problems_found), 1)

if subtext_ratio >= 0.65:  # Pelo menos 65% devem ser subtext-related
    print(f"✅ Subtext-related problems: {len(subtext_related)}/{len(problems_found)} ({subtext_ratio:.0%})")
else:
    errors.append(f"❌ Poucos problemas subtext-related: {len(subtext_related)}/{len(problems_found)} ({subtext_ratio:.0%})")

# Verificar keywords específicos de subtext presentes
subtext_keywords = ['on-the-nose', 'subtext', 'contradiction', 'power dynamic']
found_subtext = [kw for kw in subtext_keywords if any(kw.lower() in p.lower() for p in problems_found)]
if len(found_subtext) < 3:
    errors.append(f"❌ Poucos keywords de subtext mapeados: {found_subtext}")
else:
    print(f"✅ Keywords de subtext mapeados: {len(found_subtext)}")

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
    print("✅ DrSubtext Core 2 keywords validados!")
    exit(0)
