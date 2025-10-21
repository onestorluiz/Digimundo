#!/usr/bin/env python3
"""
RE-TESTE: DIALOGUE SPECIALIST - PROMPT V4.1
Comparar V4 vs V4.1 (estruturado)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from specialists.implementations.character_dialogue_specialist import DrDialogue
from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper
import json
import time


def load_screenplay():
    """Carrega roteiro do usuário"""
    screenplay_path = Path(__file__).parent / "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"

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
    print("🎬 RE-TESTE: DrDialogue - PROMPT V4.1 (Estruturado)")
    print("="*80)
    print("\nObjetivo: Comparar V4 (3,865 chars) vs V4.1 (estruturado)")
    print("Expectativa: +100% profundidade (~7,000-8,000 chars)")
    print("="*80)

    # Carregar roteiro
    screenplay = load_screenplay()
    print(f"\n✅ Roteiro carregado: {len(screenplay.split())} palavras")

    # Criar especialista
    print(f"\n🎯 Inicializando DrDialogue (Dialogue Specialist)...")
    specialist = DrDialogue()

    # Wrapper com Deep Dive 128k + Prompt V4.1 (já está no código)
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model="scripturemon-ultimate:latest",
        llm_timeout=300,
        use_theory=True,
        deep_context=True  # DEEP DIVE - Livro completo 128k
    )

    # Executar análise
    print(f"\n🔥 Executando análise com V4.1 (Estruturado)...")
    print(f"   Livro: Dialogue by Robert McKee (77,627 palavras)")
    print(f"   Contexto: ~100k tokens")
    print(f"   Prompt: V4.1 - Estrutura Obrigatória (12-14 parágrafos)")

    start = time.time()
    result = wrapper.analyze(screenplay)
    elapsed = time.time() - start

    # Resultados
    insights = result.get('llm_insights', '')

    print(f"\n{'='*80}")
    print("📊 RESULTADOS V4.1")
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

    # Comparação com V4
    print(f"\n📈 COMPARAÇÃO COM V4 (ORIGINAL):")
    v4_chars = 3865
    v4_time = 169.4

    print(f"   V4 Original:  {v4_chars:,} chars em {v4_time:.1f}s")
    print(f"   V4.1 Atual:   {len(insights):,} chars em {elapsed:.1f}s")

    char_diff = ((len(insights) / v4_chars) - 1) * 100
    time_diff = ((elapsed / v4_time) - 1) * 100

    print(f"\n   Profundidade: {char_diff:+.1f}%")
    print(f"   Tempo:        {time_diff:+.1f}%")

    if char_diff > 80:
        print(f"\n   🎉 SUCESSO! Quase DOBROU a profundidade!")
    elif char_diff > 50:
        print(f"\n   ✅ Muito bom! +50% de profundidade")
    elif char_diff > 20:
        print(f"\n   ✅ Bom! +20% de profundidade")
    else:
        print(f"\n   ⚠️ Ganho menor que esperado")

    # Salvar resultados
    output_data = {
        'timestamp': time.time(),
        'specialist': 'DrDialogue (Dialogue Specialist)',
        'prompt_version': 'v4.1_structured',
        'elapsed': elapsed,
        'insights': insights,
        'insights_length': len(insights),
        'quality_score': result.get('synthesis', {}).get('quality_score', 0),
        'python_success': result.get('python_success', False),
        'llm_success': result.get('llm_success', False),
        'structure_score': structure_score,
        'paragraphs': paragraphs,
        'comparison_v4': {
            'v4_chars': v4_chars,
            'v4_time': v4_time,
            'v4_1_chars': len(insights),
            'v4_1_time': elapsed,
            'improvement_chars': char_diff,
            'improvement_time': time_diff
        }
    }

    output_file = Path(__file__).parent / "test_dialogue_v4.1_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Resultados salvos em: {output_file}")

    # Avaliação
    print(f"\n{'='*80}")
    print("🎓 AVALIAÇÃO V4.1")
    print(f"{'='*80}")

    criteria_met = 0
    total_criteria = 6

    print(f"\nCritérios:")

    c1 = result.get('llm_success', False)
    print(f"  {'✅' if c1 else '❌'} 1. LLM executado com sucesso")
    criteria_met += 1 if c1 else 0

    c2 = len(insights) > 5000
    print(f"  {'✅' if c2 else '❌'} 2. Análise profunda (>5000 chars)")
    criteria_met += 1 if c2 else 0

    c3 = structure_score >= 4
    print(f"  {'✅' if c3 else '❌'} 3. Estrutura V4.1 adequada (4/5 seções)")
    criteria_met += 1 if c3 else 0

    c4 = result.get('synthesis', {}).get('quality_score', 0) >= 0.9
    print(f"  {'✅' if c4 else '❌'} 4. Quality score ≥ 0.9")
    criteria_met += 1 if c4 else 0

    c5 = elapsed < 300
    print(f"  {'✅' if c5 else '❌'} 5. Tempo aceitável (<5min)")
    criteria_met += 1 if c5 else 0

    c6 = char_diff > 50
    print(f"  {'✅' if c6 else '❌'} 6. Ganho significativo (>50% vs V4)")
    criteria_met += 1 if c6 else 0

    success = criteria_met >= 5

    print(f"\n{'='*80}")
    if success:
        print("🎉 RESULTADO: V4.1 APROVADO ✅")
        print(f"   Critérios atendidos: {criteria_met}/{total_criteria}")
        print(f"   DrDialogue migrado com sucesso para V4.1!")
    else:
        print("⚠️ RESULTADO: NECESSITA REVISÃO")
        print(f"   Critérios atendidos: {criteria_met}/{total_criteria}")
        print(f"   Requer ajustes antes de aprovar migração")
    print(f"{'='*80}")

    print("\n✅ RE-TESTE COMPLETO!")
    print("="*80)


if __name__ == "__main__":
    main()
