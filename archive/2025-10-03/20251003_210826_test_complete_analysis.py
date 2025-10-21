#!/usr/bin/env python3
"""
Teste Completo - Análise de Screenplay com Todos os 22 Especialistas
"""

from triple_core.orchestrators.screenplay_analyzer import ScreenplayAnalyzer

print("="*80)
print("🎬 TESTE COMPLETO - Screenplay Analyzer")
print("="*80)
print()

# Create analyzer
print("🔧 Criando ScreenplayAnalyzer...")
analyzer = ScreenplayAnalyzer(
    llm_model="scripturemon-optimized",
    deep_context=False  # False = rápido, True = melhor qualidade
)
print()

# Run complete analysis
result = analyzer.analyze_screenplay(
    screenplay_path="content/screenplays/personal/sonhos_sem_lembrancas_t3.txt",
    output_dir="workspace/outputs/analysis"
)

# Summary
print("="*80)
print("📊 RESULTADO FINAL")
print("="*80)
print()

overall = result['overall_quality']
stats = result['screenplay_stats']

print(f"📄 Screenplay: {result['screenplay_path']}")
print(f"   Pages: {stats['pages']}")
print(f"   Scenes: {stats['scenes']}")
print(f"   Words: {stats['words']:,}")
print()

print(f"🎯 Overall Quality:")
print(f"   Score: {overall.overall_score:.1f}/100")
print(f"   Level: {overall.quality_level.upper()}")
print()

print(f"📊 Dimension Scores:")
print(f"   Narrative:  {overall.narrative_score:.1f}/100")
print(f"   Character:  {overall.character_score:.1f}/100")
print(f"   Dialogue:   {overall.dialogue_score:.1f}/100")
print(f"   Technical:  {overall.technical_score:.1f}/100")
print(f"   Depth:      {overall.depth_score:.1f}/100")
print(f"   Craft:      {overall.craft_score:.1f}/100")
print(f"   Market:     {overall.market_score:.1f}/100")
print()

if overall.standout_elements:
    print(f"✨ Standout Elements ({len(overall.standout_elements)}):")
    for elem in overall.standout_elements[:5]:
        print(f"   • {elem}")
    if len(overall.standout_elements) > 5:
        print(f"   ... and {len(overall.standout_elements) - 5} more")
    print()

if overall.critical_issues:
    print(f"🚨 Critical Issues ({len(overall.critical_issues)}):")
    for issue in overall.critical_issues[:5]:
        print(f"   • {issue}")
    print()

print(f"💡 Priority Recommendations ({len(overall.recommendations)}):")
for i, rec in enumerate(overall.recommendations[:5], 1):
    print(f"   {i}. {rec}")
if len(overall.recommendations) > 5:
    print(f"   ... and {len(overall.recommendations) - 5} more")
print()

print(f"⏱️  Analysis Time: {result['total_time']:.1f}s")
print()

print("📄 Reports saved:")
print(f"   HTML: {result['html_report_path']}")
print(f"   MD:   {result['markdown_report_path']}")
print()

print("="*80)
print("✅ TESTE COMPLETO!")
print("="*80)
