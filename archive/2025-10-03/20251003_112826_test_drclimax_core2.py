#!/usr/bin/env python3
"""
Teste Core 2 - DrClimax Keywords (isolado)
"""

from triple_core.core_2_examples.example_finder import ExampleFinderCore

print("="*80)
print("🔍 TESTE CORE 2 - DrClimax Keywords (Isolado)")
print("="*80)
print()

# Simular análise do Core 1 (DrClimax) com recomendações típicas
fake_core1_result = {
    'score': 55.0,
    'recommendations': [
        'Final confrontation lacks tension and stakes',
        'Climactic battle feels rushed and underwhelming',
        'Ultimate showdown needs more emotional weight',
        'Climax stakes are too low - raise everything at stake',
        'Maximum tension at climax is missing',
        'Climax payoff doesn\'t deliver on earlier setup',
        'Setup payoff in climax is weak',
        'Climax timing is off - arrives too early',
        'Climax placement feels premature',
        'Emotional peak at climax is missing',
        'Weak climax fails to deliver catharsis',
        'Anticlimax - climax falls flat',
        'Climax clarity is poor - action is confusing',
        'Climax resolution connection is weak',
        'Satisfying climax is missing'
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

# Verificar que não mapeia para PACING
pacing_hits = [p for p in problem_titles_lower if 'pacing and rhythm' in p and 'climax' not in p]
if pacing_hits:
    errors.append(f"❌ Cross-contamination com pacing: {pacing_hits}")

# Verificar que não mapeia para DIALOGUE
dialogue_hits = [p for p in problem_titles_lower if 'dialogue' in p]
if dialogue_hits:
    errors.append(f"❌ Cross-contamination com dialogue: {dialogue_hits}")

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
