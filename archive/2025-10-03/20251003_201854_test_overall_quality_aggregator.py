#!/usr/bin/env python3
"""
Teste - Overall Quality Aggregator
"""

from triple_core.aggregators.overall_quality_aggregator import OverallQualityAggregator

print("="*80)
print("🧪 TESTE - Overall Quality Aggregator")
print("="*80)
print()

# Resultados fictícios de especialistas (simulando Triple-Core)
specialist_results = {
    # NARRATIVE (25% weight)
    'Structure': {'score': 75, 'recommendations': ['Improve Act 2 pacing']},
    'Pacing': {'score': 70, 'recommendations': ['Some scenes drag']},
    'Opening': {'score': 85, 'recommendations': []},
    'Climax': {'score': 65, 'recommendations': ['Climax lacks impact']},
    'Resolution': {'score': 80, 'recommendations': []},
    'Transitions': {'score': 72, 'recommendations': ['Smoother transitions needed']},

    # CHARACTER (20% weight)
    'Character Psychology': {'score': 88, 'recommendations': []},
    'Character Arcs': {'score': 82, 'recommendations': []},
    'Character Relationships': {'score': 79, 'recommendations': ['Develop secondary relationships']},

    # DIALOGUE (15% weight)
    'Dialogue': {'score': 90, 'recommendations': []},
    'Voice Consistency': {'score': 85, 'recommendations': []},

    # TECHNICAL (10% weight)
    'Formatting': {'score': 95, 'recommendations': []},
    'Action Description': {'score': 78, 'recommendations': ['More visual descriptions']},

    # DEPTH (15% weight)
    'Subtext': {'score': 68, 'recommendations': ['Add more subtext to dialogue']},
    'Symbolism': {'score': 72, 'recommendations': ['Symbol web incomplete']},
    'Theme Consistency': {'score': 75, 'recommendations': []},
    'Tone Consistency': {'score': 80, 'recommendations': []},
    'Visual Motifs': {'score': 70, 'recommendations': ['Motifs not well established']},

    # CRAFT (10% weight)
    'Genre Conventions': {'score': 83, 'recommendations': []},
    'World Building': {'score': 76, 'recommendations': ['Expand world details']},

    # MARKET (5% weight)
    'Originality': {'score': 62, 'recommendations': ['Too derivative', 'Add fresh elements']},
    'Market Potential': {'score': 58, 'recommendations': ['Limited commercial appeal']},
}

print(f"📊 Agregando resultados de {len(specialist_results)} especialistas...")
print()

# Criar aggregator
aggregator = OverallQualityAggregator()

# Agregar
result = aggregator.aggregate(specialist_results)

# Resultados
print("="*80)
print("✅ RESULTADOS AGREGADOS")
print("="*80)
print()

print(f"🎯 OVERALL QUALITY: {result.overall_score:.1f}/100")
print(f"📈 Quality Level: {result.quality_level.upper()}")
print()

print("📊 SCORES POR DIMENSÃO:")
print(f"   Narrative:  {result.narrative_score:.1f}/100 (6 specialists)")
print(f"   Character:  {result.character_score:.1f}/100 (3 specialists)")
print(f"   Dialogue:   {result.dialogue_score:.1f}/100 (2 specialists)")
print(f"   Technical:  {result.technical_score:.1f}/100 (2 specialists)")
print(f"   Depth:      {result.depth_score:.1f}/100 (5 specialists)")
print(f"   Craft:      {result.craft_score:.1f}/100 (2 specialists)")
print(f"   Market:     {result.market_score:.1f}/100 (2 specialists)")
print()

print("🔍 DETALHES POR DIMENSÃO:")
for dim in result.dimension_scores:
    print(f"\n   {dim.dimension.upper()}:")
    print(f"      Score: {dim.score:.1f}/100")
    print(f"      Specialists: {dim.specialist_count}")
    if dim.strengths:
        print(f"      ✅ Strengths: {len(dim.strengths)}")
    if dim.weaknesses:
        print(f"      ⚠️ Weaknesses: {len(dim.weaknesses)}")
print()

if result.standout_elements:
    print("✨ ELEMENTOS DE DESTAQUE (score >= 80):")
    for elem in result.standout_elements[:5]:
        print(f"   ✅ {elem}")
    print()

if result.critical_issues:
    print("❌ PROBLEMAS CRÍTICOS (score < 50):")
    for issue in result.critical_issues:
        print(f"   ❌ {issue}")
    print()

print("💡 RECOMENDAÇÕES PRIORITÁRIAS:")
for i, rec in enumerate(result.recommendations[:7], 1):
    print(f"   {i}. {rec}")
print()

# Validações
print("="*80)
print("✅ VALIDAÇÕES:")
print("="*80)

errors = []

# Verificar que overall_score está no range
if not 0 <= result.overall_score <= 100:
    errors.append(f"❌ Overall score fora do range: {result.overall_score}")

# Verificar que quality_level é válido
valid_levels = ['amateur', 'developing', 'competent', 'professional', 'excellent', 'masterful']
if result.quality_level not in valid_levels:
    errors.append(f"❌ Quality level inválido: {result.quality_level}")

# Verificar que tem scores para todas as 7 dimensões
if len(result.dimension_scores) != 7:
    errors.append(f"❌ Esperado 7 dimensões, encontrado {len(result.dimension_scores)}")

# Verificar que overall_score é média ponderada razoável
expected_range = (65, 80)  # Baseado nos scores de entrada
if not expected_range[0] <= result.overall_score <= expected_range[1]:
    errors.append(
        f"⚠️ Overall score {result.overall_score:.1f} "
        f"fora do range esperado {expected_range}"
    )

if errors:
    print("❌ TESTE FALHOU!")
    for err in errors:
        print(f"   {err}")
    exit(1)
else:
    print("="*80)
    print("✅ TESTE PASSOU! Overall Quality Aggregator funcionando perfeitamente!")
    print("="*80)
    print()
    print(f"📊 Summary:")
    print(f"   • Overall Score: {result.overall_score:.1f}/100")
    print(f"   • Quality Level: {result.quality_level}")
    print(f"   • Dimensions: {len(result.dimension_scores)}")
    print(f"   • Standout Elements: {len(result.standout_elements)}")
    print(f"   • Critical Issues: {len(result.critical_issues)}")
    print(f"   • Recommendations: {len(result.recommendations)}")
    exit(0)
