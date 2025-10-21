#!/usr/bin/env python3
"""
Teste - Executive Summary Generator
"""

from triple_core.aggregators import (
    OverallQualityAggregator,
    ExecutiveSummaryGenerator
)

print("="*80)
print("🧪 TESTE - Executive Summary Generator")
print("="*80)
print()

# Resultados fictícios de especialistas
specialist_results = {
    'Structure': {'score': 75, 'recommendations': ['Improve Act 2 pacing', 'Strengthen midpoint']},
    'Pacing': {'score': 70, 'recommendations': ['Some scenes drag in Act 2']},
    'Opening': {'score': 85, 'recommendations': []},
    'Climax': {'score': 65, 'recommendations': ['Climax lacks emotional impact']},
    'Resolution': {'score': 80, 'recommendations': []},
    'Transitions': {'score': 72, 'recommendations': ['Smoother transitions needed']},
    'Character Psychology': {'score': 88, 'recommendations': []},
    'Character Arcs': {'score': 82, 'recommendations': []},
    'Character Relationships': {'score': 79, 'recommendations': ['Develop secondary relationships']},
    'Dialogue': {'score': 90, 'recommendations': []},
    'Voice Consistency': {'score': 85, 'recommendations': []},
    'Formatting': {'score': 95, 'recommendations': []},
    'Action Description': {'score': 78, 'recommendations': ['More visual descriptions']},
    'Subtext': {'score': 68, 'recommendations': ['Add more subtext to dialogue']},
    'Symbolism': {'score': 72, 'recommendations': ['Symbol web incomplete']},
    'Theme Consistency': {'score': 75, 'recommendations': []},
    'Tone Consistency': {'score': 80, 'recommendations': []},
    'Visual Motifs': {'score': 70, 'recommendations': ['Motifs not well established']},
    'Genre Conventions': {'score': 83, 'recommendations': []},
    'World Building': {'score': 76, 'recommendations': ['Expand world details']},
    'Originality': {'score': 62, 'recommendations': ['Too derivative', 'Add fresh elements']},
    'Market Potential': {'score': 58, 'recommendations': ['Limited commercial appeal']},
}

screenplay_stats = {
    'pages': 108,
    'scenes': 87,
    'words': 23456,
    'characters': 12
}

print("📊 Step 1: Aggregating quality scores...")
aggregator = OverallQualityAggregator()
overall_result = aggregator.aggregate(specialist_results)

print(f"   ✅ Overall Score: {overall_result.overall_score:.1f}/100")
print(f"   ✅ Quality Level: {overall_result.quality_level}")
print()

print("📝 Step 2: Generating executive summary...")
generator = ExecutiveSummaryGenerator()
summary = generator.generate(
    screenplay_title="Sonhos Sem Lembranças",
    screenplay_stats=screenplay_stats,
    overall_quality_result=overall_result,
    specialist_results=specialist_results
)

print(f"   ✅ Title: {summary.title}")
print(f"   ✅ Generated at: {summary.generated_at}")
print()

print("="*80)
print("📊 SUMMARY CONTENT")
print("="*80)
print()

print(f"📈 Overall: {summary.overall_score:.1f}/100 ({summary.quality_level.upper()})")
print()

print("📊 Dimensions:")
for dim, score in summary.dimension_scores.items():
    print(f"   {dim:12s}: {score:5.1f}/100")
print()

print(f"✨ Standout Elements: {len(summary.standout_elements)}")
for elem in summary.standout_elements[:3]:
    print(f"   • {elem}")
if len(summary.standout_elements) > 3:
    print(f"   ... and {len(summary.standout_elements) - 3} more")
print()

if summary.critical_issues:
    print(f"🚨 Critical Issues: {len(summary.critical_issues)}")
    for issue in summary.critical_issues[:3]:
        print(f"   • {issue}")
    print()

print(f"💡 Priority Recommendations: {len(summary.priority_recommendations)}")
for rec in summary.priority_recommendations[:3]:
    print(f"   • {rec}")
if len(summary.priority_recommendations) > 3:
    print(f"   ... and {len(summary.priority_recommendations) - 3} more")
print()

print(f"📋 Specialist Summaries: {len(summary.specialist_summaries)}")
print(f"   Top 3:")
for spec in summary.specialist_summaries[:3]:
    print(f"   {spec['status']} {spec['name']}: {spec['score']}/100")
print()

print("="*80)
print("📄 REPORT OUTPUTS")
print("="*80)
print()

print(f"HTML Report: {len(summary.html_report):,} characters")
print(f"Markdown Report: {len(summary.markdown_report):,} characters")
print()

# Save reports
html_path = "test_executive_summary.html"
md_path = "test_executive_summary.md"

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(summary.html_report)
print(f"✅ Saved HTML: {html_path}")

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(summary.markdown_report)
print(f"✅ Saved Markdown: {md_path}")
print()

# Validações
print("="*80)
print("✅ VALIDAÇÕES:")
print("="*80)

errors = []

# Verificar campos obrigatórios
if not summary.title:
    errors.append("❌ Title vazio")

if not summary.generated_at:
    errors.append("❌ Generated_at vazio")

if not 0 <= summary.overall_score <= 100:
    errors.append(f"❌ Overall score inválido: {summary.overall_score}")

if len(summary.dimension_scores) != 7:
    errors.append(f"❌ Esperado 7 dimensões, encontrado {len(summary.dimension_scores)}")

if len(summary.html_report) < 1000:
    errors.append(f"❌ HTML report muito curto: {len(summary.html_report)} chars")

if len(summary.markdown_report) < 500:
    errors.append(f"❌ Markdown report muito curto: {len(summary.markdown_report)} chars")

if not summary.html_report.startswith("<!DOCTYPE html>"):
    errors.append("❌ HTML report inválido (sem DOCTYPE)")

if not summary.markdown_report.startswith("# "):
    errors.append("❌ Markdown report inválido (sem H1)")

if errors:
    print("❌ TESTE FALHOU!")
    for err in errors:
        print(f"   {err}")
    exit(1)
else:
    print("="*80)
    print("✅ TESTE PASSOU! Executive Summary Generator funcionando perfeitamente!")
    print("="*80)
    print()
    print("📊 Summary:")
    print(f"   • Title: {summary.title}")
    print(f"   • Overall Score: {summary.overall_score:.1f}/100 ({summary.quality_level})")
    print(f"   • Dimensions: {len(summary.dimension_scores)}")
    print(f"   • Standout Elements: {len(summary.standout_elements)}")
    print(f"   • Critical Issues: {len(summary.critical_issues)}")
    print(f"   • Recommendations: {len(summary.priority_recommendations)}")
    print(f"   • Specialist Summaries: {len(summary.specialist_summaries)}")
    print(f"   • HTML: {len(summary.html_report):,} chars")
    print(f"   • Markdown: {len(summary.markdown_report):,} chars")
    print()
    print("🎉 Relatórios salvos com sucesso!")
    exit(0)
