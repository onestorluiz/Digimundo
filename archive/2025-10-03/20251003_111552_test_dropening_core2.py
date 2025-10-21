#!/usr/bin/env python3
"""
Teste Core 2 - DrOpening Keywords (isolado)
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🔍 TESTE CORE 2 - DrOpening Keywords (Isolado)")
print("="*80)
print()

# Simular análise do Core 1 (DrOpening) com recomendações típicas
fake_core1_result = {
    'score': 65.0,
    'recommendations': [
        'Opening lacks strong hook to grab attention',
        'First 10 pages need more conflict',
        'Inciting incident arrives too late',
        'World establishment is unclear in opening',
        'Protagonist introduction is weak in opening scenes',
        'Opening doesn\'t establish tone effectively',
        'Stakes are not established early enough',
        'Opening has slow start that drags',
        'Opening hook needs to be more compelling',
        'First ten pages lack urgency',
        'Call to action is missing from opening',
        'World building in opening scenes is confusing',
        'Introduce character earlier in opening',
        'Set tone more clearly in opening',
        'What\'s at stake is unclear from the start',
        'Weak opening fails to engage reader'
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

# Verificar que não mapeia para STRUCTURE
structure_hits = [p for p in problem_titles_lower if 'act' in p and 'structure' in p]
if structure_hits:
    errors.append(f"❌ Cross-contamination com structure: {structure_hits}")

# Verificar que não mapeia para PACING
pacing_hits = [p for p in problem_titles_lower if 'pacing' in p and 'hook' not in p]
if pacing_hits:
    errors.append(f"❌ Cross-contamination com pacing: {pacing_hits}")

# Verificar que não mapeia para DIALOGUE
dialogue_hits = [p for p in problem_titles_lower if 'dialogue' in p or 'conversation' in p]
if dialogue_hits:
    errors.append(f"❌ Cross-contamination com dialogue: {dialogue_hits}")

# Verificar que não mapeia para ACTION
action_hits = [p for p in problem_titles_lower if 'show don\'t tell' in p or 'unfilmable' in p]
if action_hits:
    errors.append(f"❌ Cross-contamination com action: {action_hits}")

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
