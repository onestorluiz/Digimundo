#!/usr/bin/env python3
"""
TESTE: GENRE CONVENTIONS SPECIALIST - PROMPT V4.1
15º Especialista a ser graduado
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from specialists.implementations.genre_conventions_specialist import DrGenreConventions
from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper
import json
import time


def load_screenplay():
    """Carrega roteiro do usuário"""
    screenplay_path = Path(__file__).parent.parent.parent / "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"

    if not screenplay_path.exists():
        print(f"❌ Roteiro não encontrado")
        sys.exit(1)

    screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')

    # Limitar a 5000 palavras
    words = screenplay.split()
    if len(words) > 5000:
        screenplay = ' '.join(words[:5000])

    return screenplay


def main():
    print("\n" + "="*80)
    print("🎬 TESTE: DrGenreConventions - PROMPT V4.1 (15º Especialista)")
    print("="*80)
    print("\nMetodologia: Script Doctor Philosophy V4.1")
    print("Prompt: Estrutura Obrigatória (12-14 parágrafos)")
    print("Expectativa: ~5,500-6,000 chars (baseado em média V4.1)")
    print("="*80)

    # Carregar roteiro
    screenplay = load_screenplay()
    print(f"\n✅ Roteiro carregado: {len(screenplay.split())} palavras")

    # Criar especialista
    print(f"\n🎯 Inicializando DrGenreConventions (Genre Conventions Specialist)...")
    specialist = DrGenreConventions()

    # Wrapper com Deep Dive 128k + Prompt V4.1
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model="scripturemon-ultimate:latest",
        llm_timeout=300,
        use_theory=True,
        deep_context=True  # DEEP DIVE - Livro completo 128k
    )

    # Executar análise
    print(f"\n🔥 Executando análise Deep Dive (128k) com V4.1...")
    print(f"   Livro: Dialogue by Robert McKee (77,627 palavras)")
    print(f"   Contexto: ~100k tokens")
    print(f"   Prompt: V4.1 - Estrutura Obrigatória")

    start = time.time()
    result = wrapper.analyze(screenplay)
    elapsed = time.time() - start

    # Resultados
    insights = result.get('llm_insights', '')

    print(f"\n{'='*80}")
    print("📊 RESULTADOS")
    print(f"{'='*80}")

    print(f"\n⏱️  Tempo: {elapsed:.1f}s")
    print(f"📏 Output: {len(insights)} chars")
    print(f"✅ Quality Score: {result.get('synthesis', {}).get('quality_score', 0):.2f}")

    # Contar parágrafos
    paragraphs = len([p for p in insights.split('\n\n') if p.strip()])
    print(f"📝 Parágrafos: {paragraphs}")

    print(f"\n📖 PREVIEW DA ANÁLISE (primeiros 1000 chars):")
    print('-'*80)
    print(insights[:1000] + "...")
    print('-'*80)

    # Análise de qualidade
    print(f"\n🔍 ANÁLISE DE QUALIDADE:")

    # Verificar estrutura V4.1
    has_interpretation = 'INTERPRETATION' in insights or '1.' in insights
    has_patterns = 'PATTERN' in insights or '2.' in insights
    has_problems = 'PROBLEM' in insights or '3.' in insights
    has_solutions = 'SOLUTION' in insights or '4.' in insights
    has_depth = 'DEPTH' in insights or 'SYNTHESIS' in insights or '5.' in insights

    structure_score = sum([has_interpretation, has_patterns, has_problems, has_solutions, has_depth])
    print(f"   Estrutura V4.1: {structure_score}/5 seções")

    # Verificar profundidade
    is_substantial = len(insights) > 5000
    print(f"   Análise profunda: {'✅' if is_substantial else '⚠️'} ({len(insights)} chars)")

    # Comparação com média V4.1
    print(f"\n📈 COMPARAÇÃO COM MÉDIA V4.1:")
    v41_avg_chars = 5954
    v41_avg_time = 204.7

    print(f"   Média V4.1:  {v41_avg_chars:,} chars em {v41_avg_time:.1f}s")
    print(f"   DrGenreConventions: {len(insights):,} chars em {elapsed:.1f}s")

    char_diff = ((len(insights) / v41_avg_chars) - 1) * 100
    time_diff = ((elapsed / v41_avg_time) - 1) * 100

    print(f"\n   Profundidade: {char_diff:+.1f}% vs média")
    print(f"   Tempo:        {time_diff:+.1f}% vs média")

    if char_diff > 10:
        print(f"\n   ✅ Acima da média!")
    elif char_diff > -10:
        print(f"\n   ✅ Dentro da média esperada")
    else:
        print(f"\n   ⚠️ Abaixo da média")

    # Salvar resultados
    output_data = {
        'timestamp': time.time(),
        'specialist': 'DrGenreConventions (Genre Conventions Specialist)',
        'specialist_number': 15,
        'prompt_version': 'v4.1_structured',
        'elapsed': elapsed,
        'insights': insights,
        'insights_length': len(insights),
        'quality_score': result.get('synthesis', {}).get('quality_score', 0),
        'python_success': result.get('python_success', False),
        'llm_success': result.get('llm_success', False),
        'structure_score': structure_score,
        'paragraphs': paragraphs,
        'comparison_v4_1_avg': {
            'avg_chars': v41_avg_chars,
            'avg_time': v41_avg_time,
            'this_chars': len(insights),
            'this_time': elapsed,
            'diff_chars_pct': char_diff,
            'diff_time_pct': time_diff
        }
    }

    output_file = Path(__file__).parent.parent.parent / "results/v4.1_graduation/test_genre_v4.1_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Resultados salvos em: {output_file}")

    # Avaliação de graduação
    print(f"\n{'='*80}")
    print("🎓 AVALIAÇÃO DE GRADUAÇÃO")
    print(f"{'='*80}")

    criteria_met = 0
    total_criteria = 5

    print(f"\nCritérios:")

    c1 = result.get('llm_success', False)
    print(f"  {'✅' if c1 else '❌'} 1. LLM executado com sucesso")
    criteria_met += 1 if c1 else 0

    c2 = len(insights) > 2000
    print(f"  {'✅' if c2 else '❌'} 2. Análise substancial (>2000 chars)")
    criteria_met += 1 if c2 else 0

    c3 = structure_score >= 3
    print(f"  {'✅' if c3 else '❌'} 3. Estrutura adequada (≥3/5 seções)")
    criteria_met += 1 if c3 else 0

    c4 = result.get('synthesis', {}).get('quality_score', 0) >= 0.9
    print(f"  {'✅' if c4 else '❌'} 4. Quality score ≥ 0.9")
    criteria_met += 1 if c4 else 0

    c5 = elapsed < 300
    print(f"  {'✅' if c5 else '❌'} 5. Tempo aceitável (<5min)")
    criteria_met += 1 if c5 else 0

    graduation = criteria_met >= 4

    print(f"\n{'='*80}")
    if graduation:
        print("🎉 RESULTADO: GRADUADO ✅")
        print(f"   Critérios atendidos: {criteria_met}/{total_criteria}")
        print(f"   DrGenreConventions é o 15º especialista 128k V4.1!")
    else:
        print("⚠️ RESULTADO: NECESSITA REVISÃO")
        print(f"   Critérios atendidos: {criteria_met}/{total_criteria}")
        print(f"   Requer ajustes antes de graduação")
    print(f"{'='*80}")

    print("\n✅ TESTE COMPLETO!")
    print("="*80)


if __name__ == "__main__":
    main()
