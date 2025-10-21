#!/usr/bin/env python3
"""
Test Deep Dive vs Shallow mode
Compara qualidade de análise Dual-Core com chunks vs livro completo
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from specialists.implementations.character_dialogue_specialist import DrDialogue
from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper
import json
import time


def load_screenplay():
    """Carrega roteiro do usuário"""
    screenplay_path = Path(__file__).parent / "content/screenplays/personal/sonhos_sem_lembrancas_t3.txt"

    if not screenplay_path.exists():
        print(f"❌ Roteiro não encontrado: {screenplay_path}")
        sys.exit(1)

    screenplay = screenplay_path.read_text(encoding='utf-8', errors='ignore')

    # Limitar a 5000 palavras para testes (análise completa seria muito longa)
    words = screenplay.split()
    if len(words) > 5000:
        screenplay = ' '.join(words[:5000])
        print(f"⚠️ Roteiro limitado a 5000 palavras para teste")

    return screenplay


def test_shallow_mode(screenplay: str):
    """Testa modo SHALLOW (chunks apenas)"""
    print("\n" + "="*80)
    print("🔍 TESTE 1: SHALLOW MODE (Chunks)")
    print("="*80)

    specialist = DrDialogue()
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model="scripturemon-ultimate:latest",  # 128K context!
        llm_timeout=300,
        use_theory=True,
        deep_context=False  # SHALLOW
    )

    print(f"\n📊 Configuração:")
    print(f"   - Theory: ✅ Enabled (chunks)")
    print(f"   - Deep Context: ❌ Disabled")
    print(f"   - Expected context: ~4.5k words (6k tokens)")

    start = time.time()
    result = wrapper.analyze(screenplay)
    elapsed = time.time() - start

    print(f"\n⏱️ Tempo total: {elapsed:.1f}s")
    print(f"\n📈 Resultados Python:")
    print(f"   - Success: {result['python_success']}")
    print(f"   - Data size: {len(str(result['python_analysis']))} bytes")

    print(f"\n🤖 Resultados LLM:")
    print(f"   - Success: {result['llm_success']}")

    if result['llm_success']:
        llm_text = result['llm_insights']
        print(f"   - Response length: {len(llm_text)} chars")
        print(f"   - Words: {len(llm_text.split())} words")
        print(f"\n💬 LLM Insights (preview):")
        print("-" * 80)
        print(llm_text[:800] + "..." if len(llm_text) > 800 else llm_text)
        print("-" * 80)

    return result


def test_deep_mode(screenplay: str):
    """Testa modo DEEP DIVE (livro completo)"""
    print("\n" + "="*80)
    print("📚 TESTE 2: DEEP DIVE MODE (Full Book)")
    print("="*80)

    specialist = DrDialogue()
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model="scripturemon-ultimate:latest",  # 128K context!
        llm_timeout=600,  # Timeout maior para deep dive
        use_theory=True,
        deep_context=True  # DEEP DIVE
    )

    print(f"\n📊 Configuração:")
    print(f"   - Theory: ✅ Enabled (full book)")
    print(f"   - Deep Context: ✅ ENABLED")
    print(f"   - Expected context: ~77k words (100k tokens)")

    start = time.time()
    result = wrapper.analyze(screenplay)
    elapsed = time.time() - start

    print(f"\n⏱️ Tempo total: {elapsed:.1f}s")
    print(f"\n📈 Resultados Python:")
    print(f"   - Success: {result['python_success']}")
    print(f"   - Data size: {len(str(result['python_analysis']))} bytes")

    print(f"\n🤖 Resultados LLM:")
    print(f"   - Success: {result['llm_success']}")

    if result['llm_success']:
        llm_text = result['llm_insights']
        print(f"   - Response length: {len(llm_text)} chars")
        print(f"   - Words: {len(llm_text.split())} words")
        print(f"\n💬 LLM Insights (preview):")
        print("-" * 80)
        print(llm_text[:800] + "..." if len(llm_text) > 800 else llm_text)
        print("-" * 80)

    return result


def compare_results(shallow_result: dict, deep_result: dict):
    """Compara resultados dos dois modos"""
    print("\n" + "="*80)
    print("⚖️ COMPARAÇÃO: Shallow vs Deep")
    print("="*80)

    # Comparar tamanho de resposta
    shallow_text = shallow_result.get('llm_insights', '')
    deep_text = deep_result.get('llm_insights', '')

    print(f"\n📏 Tamanho das respostas:")
    print(f"   Shallow: {len(shallow_text)} chars ({len(shallow_text.split())} palavras)")
    print(f"   Deep:    {len(deep_text)} chars ({len(deep_text.split())} palavras)")
    print(f"   Diferença: {((len(deep_text) - len(shallow_text)) / len(shallow_text) * 100):.1f}%")

    # Comparar citações (heurística: menciona página/capítulo/exemplo)
    shallow_citations = sum([
        shallow_text.lower().count('page'),
        shallow_text.lower().count('chapter'),
        shallow_text.lower().count('example'),
        shallow_text.lower().count('mckee')
    ])

    deep_citations = sum([
        deep_text.lower().count('page'),
        deep_text.lower().count('chapter'),
        deep_text.lower().count('example'),
        deep_text.lower().count('mckee')
    ])

    print(f"\n📖 Citações detectadas (heurística):")
    print(f"   Shallow: {shallow_citations} menções")
    print(f"   Deep:    {deep_citations} menções")

    # Análise qualitativa simples
    print(f"\n🎯 Análise Qualitativa:")

    # Deep deve ser mais específico
    deep_is_longer = len(deep_text) > len(shallow_text)
    deep_has_more_citations = deep_citations > shallow_citations

    if deep_is_longer and deep_has_more_citations:
        print("   ✅ Deep mode parece superior: mais detalhado e com mais citações")
    elif deep_is_longer:
        print("   ⚠️ Deep mode é mais detalhado, mas não necessariamente mais rico em citações")
    elif deep_has_more_citations:
        print("   ⚠️ Deep mode tem mais citações, mas resposta mais curta")
    else:
        print("   ❌ Deep mode não mostrou vantagem clara nos testes automáticos")

    print(f"\n💡 Recomendação:")
    if deep_has_more_citations or deep_is_longer:
        print("   → Deep Dive parece agregar valor. Leia as respostas completas para confirmar.")
    else:
        print("   → Resultados inconclusivos. Análise manual necessária.")

    # Salvar resultados completos
    output_file = Path(__file__).parent / "test_deep_dive_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'shallow': shallow_result,
            'deep': deep_result,
            'comparison': {
                'shallow_length': len(shallow_text),
                'deep_length': len(deep_text),
                'shallow_citations': shallow_citations,
                'deep_citations': deep_citations
            }
        }, f, indent=2, default=str)

    print(f"\n💾 Resultados completos salvos em: {output_file}")


def main():
    print("\n" + "🧪" * 40)
    print("TESTE COMPARATIVO: Deep Dive vs Shallow Mode")
    print("🧪" * 40)

    # Carregar roteiro
    print("\n📖 Carregando roteiro...")
    screenplay = load_screenplay()
    print(f"✅ Roteiro carregado: {len(screenplay.split())} palavras")

    # Teste 1: Shallow
    shallow_result = test_shallow_mode(screenplay)

    # Teste 2: Deep
    deep_result = test_deep_mode(screenplay)

    # Comparação
    compare_results(shallow_result, deep_result)

    print("\n✅ Testes concluídos!")


if __name__ == "__main__":
    main()
