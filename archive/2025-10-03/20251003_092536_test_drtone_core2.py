#!/usr/bin/env python3
"""
Teste Isolado - Core 2 Keywords para DrTone
Valida que recomendações de tone mapeiam para keywords corretos
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🧪 TESTE ISOLADO - Core 2 Keywords para Tone")
print("="*80)
print()

# Simular análise do Core 1 (DrTone) com recomendações típicas
fake_core1_result = {
    'score': 65.0,
    'recommendations': [
        'Establish consistent tone in opening scenes',
        'Maintain tonal consistency or justify shifts',
        'Align tone with genre conventions',
        'Create smooth bridges between tonal changes',
        'Align dialogue tone with scene atmosphere',
        'Write action lines that reinforce tone',
        'Vary emotional intensity within tonal framework',
        'Balance humor with overall tone',
        'Adjust tone to reflect narrative stakes',
        'Intensify tone approaching climax'
    ],
    'rule_violations': [
        {
            'rule_id': 'TON.R001',
            'title': 'Established Tone',
            'severity': 'critical',
            'message': 'No clear tone established',
            'fix': 'Establish consistent tone in opening scenes'
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

# Verificar que não mapeia para DIALOGUE ou THEME (cross-contamination)
dialogue_contamination = [p for p in problems_found if 'voice' in p.lower() or ('subtext' in p.lower() and 'theme' not in p.lower())]
theme_contamination = [p for p in problems_found if 'central theme' in p.lower() or 'thematic anchor' in p.lower()]
if dialogue_contamination or theme_contamination:
    if dialogue_contamination:
        errors.append(f"❌ Cross-contamination com dialogue: {dialogue_contamination}")
    if theme_contamination:
        errors.append(f"❌ Cross-contamination com theme: {theme_contamination}")
else:
    print("✅ Sem cross-contamination com dialogue/theme")

# Verificar que a maioria dos problemas são de tone (não structure ou outros)
tone_related = [p for p in problems_found if 'tone' in p.lower() or 'tonal' in p.lower() or 'emotional' in p.lower() or 'atmospheric' in p.lower() or 'comic relief' in p.lower()]
tone_ratio = len(tone_related) / max(len(problems_found), 1)

if tone_ratio >= 0.6:  # Pelo menos 60% devem ser tone-related
    print(f"✅ Tone-related problems: {len(tone_related)}/{len(problems_found)} ({tone_ratio:.0%})")
else:
    errors.append(f"❌ Poucos problemas tone-related: {len(tone_related)}/{len(problems_found)} ({tone_ratio:.0%})")

# Verificar keywords específicos de tone presentes
tone_keywords = ['Tonal consistency', 'Establish', 'Genre-appropriate', 'Emotional']
found_tone = [kw for kw in tone_keywords if any(kw.lower() in p.lower() for p in problems_found)]
if len(found_tone) < 3:
    errors.append(f"❌ Poucos keywords de tone mapeados: {found_tone}")
else:
    print(f"✅ Keywords de tone mapeados: {len(found_tone)}")

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
    print("✅ DrTone Core 2 keywords validados!")
    exit(0)
