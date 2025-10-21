#!/usr/bin/env python3
"""
RE-TESTE DOS 3 ESPECIALISTAS COM NOVO PROMPT V4
Compara resultados antigos vs novos
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from specialists.implementations.character_dialogue_specialist import DrDialogue
from specialists.implementations.character_psychology_specialist import DrCharacterPsychology
from specialists.implementations.subtext_specialist import DrSubtext
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


def test_specialist(specialist_name, specialist_class, screenplay):
    """Testa um especialista com Deep Dive"""
    print(f"\n{'='*80}")
    print(f"🎬 TESTANDO: {specialist_name}")
    print(f"{'='*80}")

    specialist = specialist_class()
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model="scripturemon-ultimate:latest",
        llm_timeout=300,
        use_theory=True,
        deep_context=True  # DEEP DIVE
    )

    start = time.time()
    result = wrapper.analyze(screenplay)
    elapsed = time.time() - start

    insights = result.get('llm_insights', '')

    print(f"\n✅ Análise completa em {elapsed:.1f}s")
    print(f"📊 Output: {len(insights)} chars")
    print(f"\n📖 Preview (primeiros 500 chars):")
    print('-'*80)
    print(insights[:500] + "...")
    print('-'*80)

    return {
        'specialist': specialist_name,
        'elapsed': elapsed,
        'insights': insights,
        'insights_length': len(insights),
        'python_success': result.get('python_success', False),
        'llm_success': result.get('llm_success', False),
        'quality_score': result.get('synthesis', {}).get('quality_score', 0)
    }


def main():
    print("\n" + "="*80)
    print("🔄 RE-TESTE DOS 3 ESPECIALISTAS - PROMPT V4")
    print("="*80)
    print("\nObjetivo: Comparar resultados antigos (prompt v1-v3) com novo (v4)")
    print("="*80)

    # Carregar roteiro
    screenplay = load_screenplay()
    print(f"\n✅ Roteiro carregado: {len(screenplay.split())} palavras")

    # Testar os 3 especialistas
    results = []

    # 1. DrDialogue
    results.append(test_specialist(
        "DrDialogue (Character Dialogue Specialist)",
        DrDialogue,
        screenplay
    ))

    time.sleep(5)

    # 2. DrPsychemon
    results.append(test_specialist(
        "DrPsychemon (Character Psychology Specialist)",
        DrCharacterPsychology,
        screenplay
    ))

    time.sleep(5)

    # 3. DrSubmon
    results.append(test_specialist(
        "DrSubmon (Subtext Specialist)",
        DrSubtext,
        screenplay
    ))

    # Comparação
    print(f"\n{'='*80}")
    print("📊 RESUMO COMPARATIVO")
    print(f"{'='*80}")

    print(f"\n{'Especialista':<45} {'Tempo':>10} {'Output':>10} {'Quality':>10}")
    print('-'*80)

    for r in results:
        name = r['specialist'].split('(')[0].strip()
        print(f"{name:<45} {r['elapsed']:>9.1f}s {r['insights_length']:>9}c {r['quality_score']:>9.2f}")

    print('-'*80)
    avg_time = sum(r['elapsed'] for r in results) / len(results)
    avg_length = sum(r['insights_length'] for r in results) / len(results)
    avg_quality = sum(r['quality_score'] for r in results) / len(results)

    print(f"{'MÉDIA':<45} {avg_time:>9.1f}s {avg_length:>9.0f}c {avg_quality:>9.2f}")

    # Comparação com resultados anteriores
    print(f"\n{'='*80}")
    print("📈 COMPARAÇÃO COM RESULTADOS ANTERIORES")
    print(f"{'='*80}")

    previous_results = {
        'DrDialogue': {'length': 3117, 'citations': 19, 'quality': 1.0},
        'DrPsychemon': {'length': 2811, 'citations': 10, 'quality': 1.0},
        'DrSubmon (v1)': {'length': 2787, 'citations': 10, 'quality': 1.0}
    }

    for r in results:
        name = r['specialist'].split('(')[0].strip()

        if name in previous_results:
            prev = previous_results[name]
            current_length = r['insights_length']
            prev_length = prev['length']
            diff = ((current_length / prev_length) - 1) * 100

            print(f"\n{name}:")
            print(f"   Anterior: {prev_length} chars, {prev['citations']} citações")
            print(f"   Novo (v4): {current_length} chars ({diff:+.1f}%)")
            print(f"   Quality: {r['quality_score']:.2f}")

    # Salvar resultados
    output = {
        'timestamp': time.time(),
        'prompt_version': 'v4_script_doctor_philosophy',
        'specialists_tested': results
    }

    output_file = Path(__file__).parent / "test_all_specialists_v4_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Resultados salvos em: {output_file}")

    print("\n" + "="*80)
    print("✅ TESTE COMPLETO!")
    print("="*80)


if __name__ == "__main__":
    main()
