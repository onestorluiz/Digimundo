#!/usr/bin/env python3
"""
Análise Crítica Real de Roteiros
Avalia com critérios rigorosos e honestos
"""

import sys
sys.path.insert(0, 'src')

from pathlib import Path
from scripturemon_champion.analysis.script_doctor import ScriptDoctor

def critical_analysis(screenplay_path: str):
    """Análise crítica honesta do roteiro"""

    print("=" * 80)
    print("🔍 ANÁLISE CRÍTICA REAL - SEM FILTROS")
    print("=" * 80)

    # Carregar roteiro
    text = Path(screenplay_path).read_text(encoding='utf-8', errors='ignore')

    # Análise básica
    doctor = ScriptDoctor()
    analysis = doctor.analyze_script(text, Path(screenplay_path).stem)
    stc = doctor.analyze_save_the_cat(text)

    print(f"\n📚 Roteiro: {Path(screenplay_path).name}")
    print(f"📊 Tamanho: {len(text):,} caracteres (~{len(text.split()):,} palavras)")

    # ESTRUTURA
    print("\n📐 ESTRUTURA:")
    print(f"  • Cenas: {analysis.scenes}")
    print(f"  • Beats detectados: {len(stc.beats)}/15")
    print(f"  • Beats faltando: {', '.join(stc.missing_beats) if stc.missing_beats else 'Nenhum'}")

    # Análise crítica de estrutura
    structural_issues = []

    if len(stc.beats) < 10:
        structural_issues.append("❌ Estrutura incompleta - faltam beats essenciais")

    if analysis.scenes < 40:
        structural_issues.append("⚠️ Muito curto para longa-metragem (menos de 40 cenas)")
    elif analysis.scenes > 70:
        structural_issues.append("⚠️ Potencialmente longo demais (mais de 70 cenas)")

    # PERSONAGENS
    print(f"\n👥 PERSONAGENS:")
    print(f"  • Principais: {', '.join(analysis.top_characters[:5]) if analysis.top_characters else 'Não identificados'}")
    print(f"  • Total: {len(analysis.top_characters)}")

    character_issues = []

    if len(analysis.top_characters) < 3:
        character_issues.append("❌ Poucos personagens principais (menos de 3)")
    elif len(analysis.top_characters) > 10:
        character_issues.append("⚠️ Muitos personagens (pode diluir foco)")

    # DIÁLOGO
    print(f"\n💬 DIÁLOGO:")
    print(f"  • Proporção: {analysis.dialogue_ratio:.1%}")

    dialogue_issues = []

    if analysis.dialogue_ratio < 0.2:
        dialogue_issues.append("❌ Muito pouco diálogo (menos de 20%)")
    elif analysis.dialogue_ratio > 0.5:
        dialogue_issues.append("⚠️ Diálogo excessivo (mais de 50%)")

    # RITMO
    print(f"\n🎬 RITMO E PACING:")
    print(f"  • Score: {analysis.pacing_score:.2f}")
    print(f"  • Média de cena: {analysis.avg_scene_len:.0f} palavras")

    pacing_issues = []

    if analysis.pacing_score < 0.5:
        pacing_issues.append("❌ Ritmo problemático (score < 0.5)")

    if analysis.avg_scene_len > 400:
        pacing_issues.append("⚠️ Cenas muito longas (média > 400 palavras)")
    elif analysis.avg_scene_len < 150:
        pacing_issues.append("⚠️ Cenas muito curtas (média < 150 palavras)")

    # PROBLEMAS DETECTADOS
    print("\n🚨 PROBLEMAS DETECTADOS:")

    all_issues = structural_issues + character_issues + dialogue_issues + pacing_issues

    if all_issues:
        for issue in all_issues:
            print(f"  {issue}")
    else:
        print("  ✅ Nenhum problema crítico detectado")

    # COMPARAÇÃO COM TEORIAS CLÁSSICAS
    print("\n📖 ADERÊNCIA ÀS TEORIAS CLÁSSICAS:")

    # Save the Cat
    stc_adherence = (len(stc.beats) / 15) * 100
    print(f"  • Save the Cat: {stc_adherence:.0f}%")
    if stc_adherence < 60:
        print(f"    ❌ Baixa aderência - faltam {15 - len(stc.beats)} beats essenciais")

    # Three Act Structure
    act1_expected = analysis.scenes * 0.25
    act2_expected = analysis.scenes * 0.50
    act3_expected = analysis.scenes * 0.25

    print(f"  • Estrutura 3 Atos: Esperado 25%-50%-25%")

    # Character Arc
    has_clear_protagonist = len(analysis.top_characters) > 0 and analysis.top_characters[0] != "Unknown"
    if has_clear_protagonist:
        print(f"  • Protagonista claro: ✅ {analysis.top_characters[0]}")
    else:
        print(f"  • Protagonista claro: ❌ Não identificado")

    # VEREDITO FINAL
    print("\n⚖️ VEREDITO FINAL:")

    total_score = 0
    max_score = 100

    # Estrutura (30 pontos)
    structure_score = min(30, (len(stc.beats) / 15) * 30)
    total_score += structure_score

    # Personagens (20 pontos)
    character_score = 20 if 3 <= len(analysis.top_characters) <= 8 else 10
    total_score += character_score

    # Diálogo (20 pontos)
    dialogue_score = 20 if 0.2 <= analysis.dialogue_ratio <= 0.4 else 10
    total_score += dialogue_score

    # Ritmo (20 pontos)
    pacing_score = analysis.pacing_score * 20
    total_score += pacing_score

    # Tamanho adequado (10 pontos)
    size_score = 10 if 40 <= analysis.scenes <= 60 else 5
    total_score += size_score

    print(f"  📊 Score Total: {total_score:.0f}/100")

    if total_score >= 80:
        print("  🏆 EXCELENTE - Roteiro bem estruturado")
        category = "universal"
    elif total_score >= 60:
        print("  ✅ BOM - Precisa de alguns ajustes")
        category = "good_with_notes"
    elif total_score >= 40:
        print("  ⚠️ REGULAR - Necessita revisão significativa")
        category = "needs_work"
    else:
        print("  ❌ PROBLEMÁTICO - Requer reescrita substancial")
        category = "experimental"

    # RECOMENDAÇÕES ESPECÍFICAS
    print("\n💡 RECOMENDAÇÕES ESPECÍFICAS:")

    if len(stc.missing_beats) > 5:
        print(f"  1. Adicionar beats faltantes: {', '.join(stc.missing_beats[:3])}...")

    if analysis.dialogue_ratio < 0.2:
        print("  2. Aumentar diálogos para desenvolver personagens")
    elif analysis.dialogue_ratio > 0.4:
        print("  2. Reduzir diálogos, mostrar mais através de ações")

    if analysis.pacing_score < 0.6:
        print("  3. Revisar ritmo - alternar cenas longas e curtas")

    if len(analysis.top_characters) < 3:
        print("  4. Desenvolver mais personagens secundários")

    if analysis.scenes < 40:
        print("  5. Expandir história - adicionar subplots ou desenvolvimento")

    print("\n" + "=" * 80)

    return {
        'score': total_score,
        'category': category,
        'issues': all_issues,
        'stc_adherence': stc_adherence
    }

if __name__ == "__main__":
    # Analisar Sonhos Sem Lembranças
    result = critical_analysis("/Users/clubproducoes/Digimundo/scripturemon-ultimate/my_screenplays/sonhos_sem_lembrancas_t3.txt")

    print(f"\n📝 RESUMO:")
    print(f"  • Categoria: {result['category']}")
    print(f"  • Score: {result['score']:.0f}/100")
    print(f"  • Aderência Save the Cat: {result['stc_adherence']:.0f}%")
    print(f"  • Problemas encontrados: {len(result['issues'])}")