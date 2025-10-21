#!/usr/bin/env python3
"""
TESTE: DIALOGUE SPECIALIST - MODELO 70B COM 32K TOKENS
Comparar modelo atual (scripturemon-ultimate) vs qwen2.5:70b com 32k context
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from specialists.implementations.character_dialogue_specialist import DrDialogue
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
    print("🎬 TESTE: DrDialogue - MODELO 70B COM 32K TOKENS")
    print("="*80)
    print("\nObjetivo: Testar qwen2.5:70b com 32k context window")
    print("Comparar com: scripturemon-ultimate:latest (resultado anterior)")
    print("="*80)

    # Carregar roteiro
    screenplay = load_screenplay()
    print(f"\n✅ Roteiro carregado: {len(screenplay.split())} palavras")

    # Criar especialista
    print(f"\n🎯 Inicializando DrDialogue (Dialogue Specialist)...")
    specialist = DrDialogue()

    # Wrapper com modelo 70b e 32k tokens
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model="llama3.1-70b-32k",  # Modelo 70b com 32k context
        llm_timeout=600,  # 10 minutos (modelo maior pode ser mais lento)
        use_theory=True,
        deep_context=True  # DEEP DIVE - Livro completo
    )

    # Executar análise
    print(f"\n🔥 Executando análise com llama3.1:70b (32k context)...")
    print(f"   Livro: Dialogue by Robert McKee (77,627 palavras)")
    print(f"   Modelo: llama3.1-70b-32k")
    print(f"   Context: 32768 tokens")
    print(f"   Prompt: V4.1 - Estrutura Obrigatória (12-14 parágrafos)")

    start = time.time()
    result = wrapper.analyze(screenplay)
    elapsed = time.time() - start

    # Resultados
    insights = result.get('llm_insights', '')

    print(f"\n{'='*80}")
    print("📊 RESULTADOS - MODELO 70B")
    print(f"{'='*80}")

    print(f"\n⏱️  Tempo: {elapsed:.1f}s")
    print(f"📏 Output: {len(insights)} chars")
    print(f"✅ Quality Score: {result.get('synthesis', {}).get('quality_score', 0):.2f}")

    # Contar parágrafos
    paragraphs = len([p for p in insights.split('\n\n') if p.strip()])
    print(f"📝 Parágrafos: {paragraphs}")

    print(f"\n📖 PREVIEW DA ANÁLISE (primeiros 1500 chars):")
    print('-'*80)
    print(insights[:1500] + "...")
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

    # Verificar especificidade
    import re
    scene_refs = len(re.findall(r'\bscene\s+\d+|\bcena\s+\d+', insights, re.IGNORECASE))
    dialogue_quotes = len(re.findall(r'["""]([^"""]{15,})["""]', insights))

    print(f"\n   📍 Especificidade:")
    print(f"      Scene references: {scene_refs}")
    print(f"      Dialogue quotes: {dialogue_quotes}")

    # Comparação com resultado anterior
    print(f"\n📈 COMPARAÇÃO COM MODELO ANTERIOR:")

    # Carregar resultado anterior
    prev_result_path = Path(__file__).parent.parent.parent / "results/v4.1_graduation/test_dialogue_v4.1_results.json"
    if prev_result_path.exists():
        with open(prev_result_path, 'r', encoding='utf-8') as f:
            prev_data = json.load(f)

        prev_chars = prev_data.get('insights_length', 4498)
        prev_time = prev_data.get('elapsed', 195.1)

        print(f"   Modelo Anterior:  {prev_chars:,} chars em {prev_time:.1f}s")
        print(f"   Modelo 70b:       {len(insights):,} chars em {elapsed:.1f}s")

        char_diff = ((len(insights) / prev_chars) - 1) * 100
        time_diff = ((elapsed / prev_time) - 1) * 100

        print(f"\n   Diferença Output: {char_diff:+.1f}%")
        print(f"   Diferença Tempo:  {time_diff:+.1f}%")
    else:
        print(f"   (Resultado anterior não encontrado)")

    # Salvar resultados
    output_data = {
        'timestamp': time.time(),
        'specialist': 'DrDialogue (Dialogue Specialist)',
        'model': 'llama3.1-70b-32k',
        'context_window': '32768',
        'prompt_version': 'v4.1_structured',
        'elapsed': elapsed,
        'insights': insights,
        'insights_length': len(insights),
        'quality_score': result.get('synthesis', {}).get('quality_score', 0),
        'python_success': result.get('python_success', False),
        'llm_success': result.get('llm_success', False),
        'structure_score': structure_score,
        'paragraphs': paragraphs,
        'specificity': {
            'scene_references': scene_refs,
            'dialogue_quotes': dialogue_quotes
        }
    }

    output_file = Path(__file__).parent.parent.parent / "results/v4.1_graduation/test_dialogue_70b_32k_results.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Resultados salvos em: {output_file}")

    # Avaliação
    print(f"\n{'='*80}")
    print("🎓 AVALIAÇÃO MODELO 70B")
    print(f"{'='*80}")

    print(f"\n✅ TESTE COMPLETO!")
    print("="*80)


if __name__ == "__main__":
    main()
