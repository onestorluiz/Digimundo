#!/usr/bin/env python3
"""
Test Deep Dive vs Shallow mode - CHARACTER PSYCHOLOGY SPECIALIST
Compara qualidade de análise Dual-Core com chunks vs livro completo
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from specialists.implementations.character_psychology_specialist import DrCharacterPsychology
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

    specialist = DrCharacterPsychology()
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model="scripturemon-ultimate:latest",  # 128K context!
        llm_timeout=300,
        use_theory=True,
        deep_context=False  # SHALLOW
    )

    start = time.time()
    result = wrapper.analyze(screenplay)
    elapsed = time.time() - start

    print(f"\n✅ Análise SHALLOW completa em {elapsed:.1f}s")
    print(f"📊 LLM insights: {len(result['llm_insights'])} chars")

    # Contar citações (aproximado)
    citations = result['llm_insights'].count('p. ')
    print(f"📚 Citações aproximadas: {citations}")

    return result


def test_deep_mode(screenplay: str):
    """Testa modo DEEP (livro completo)"""
    print("\n" + "="*80)
    print("🔥 TESTE 2: DEEP DIVE MODE (Livro Completo)")
    print("="*80)

    specialist = DrCharacterPsychology()
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model="scripturemon-ultimate:latest",  # 128K context!
        llm_timeout=300,
        use_theory=True,
        deep_context=True  # DEEP DIVE
    )

    start = time.time()
    result = wrapper.analyze(screenplay)
    elapsed = time.time() - start

    print(f"\n✅ Análise DEEP DIVE completa em {elapsed:.1f}s")
    print(f"📊 LLM insights: {len(result['llm_insights'])} chars")

    # Contar citações (aproximado)
    citations = result['llm_insights'].count('p. ')
    print(f"📚 Citações aproximadas: {citations}")

    return result


def compare_results(shallow, deep):
    """Compara resultados de ambos os modos"""
    print("\n" + "="*80)
    print("📊 COMPARAÇÃO DE RESULTADOS")
    print("="*80)

    shallow_length = len(shallow['llm_insights'])
    deep_length = len(deep['llm_insights'])

    shallow_citations = shallow['llm_insights'].count('p. ')
    deep_citations = deep['llm_insights'].count('p. ')

    print(f"\n📏 Tamanho do Output LLM:")
    print(f"   Shallow: {shallow_length} chars")
    print(f"   Deep:    {deep_length} chars")
    print(f"   Ganho:   +{((deep_length/shallow_length - 1) * 100):.1f}%")

    print(f"\n📚 Citações Específicas:")
    print(f"   Shallow: {shallow_citations}")
    print(f"   Deep:    {deep_citations}")
    print(f"   Ganho:   +{((deep_citations/shallow_citations - 1) * 100):.1f}%" if shallow_citations > 0 else "   Ganho:   N/A")

    print(f"\n✅ Quality Score:")
    print(f"   Shallow: {shallow['synthesis']['quality_score']:.2f}")
    print(f"   Deep:    {deep['synthesis']['quality_score']:.2f}")

    # Procurar páginas específicas para validar livro completo
    print(f"\n🔍 Validação de Livro Completo:")
    print(f"   Buscando citações de páginas tardias (>300)...")

    import re
    deep_pages = re.findall(r'p\.\s*(\d+)', deep['llm_insights'])
    if deep_pages:
        deep_pages = [int(p) for p in deep_pages]
        max_page = max(deep_pages)
        print(f"   Página máxima citada: p. {max_page}")

        if max_page > 300:
            print(f"   ✅ CONFIRMADO: Livro completo sendo usado!")
        else:
            print(f"   ⚠️ ATENÇÃO: Máximo p.{max_page} - verificar se livro completo")
    else:
        print(f"   ⚠️ Nenhuma citação de página encontrada")

    return {
        "shallow_length": shallow_length,
        "deep_length": deep_length,
        "shallow_citations": shallow_citations,
        "deep_citations": deep_citations
    }


def main():
    """Executa teste comparativo completo"""
    print("\n" + "="*80)
    print("🎬 TESTE DEEP DIVE - CHARACTER PSYCHOLOGY SPECIALIST")
    print("="*80)

    # Carregar roteiro
    screenplay = load_screenplay()
    print(f"✅ Roteiro carregado: {len(screenplay.split())} palavras")

    # Teste 1: Shallow
    shallow_result = test_shallow_mode(screenplay)

    # Teste 2: Deep
    deep_result = test_deep_mode(screenplay)

    # Comparação
    comparison = compare_results(shallow_result, deep_result)

    # Salvar resultados
    results = {
        "shallow": shallow_result,
        "deep": deep_result,
        "comparison": comparison
    }

    output_file = Path(__file__).parent / "test_deep_dive_psychology_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Resultados salvos em: {output_file}")

    print("\n" + "="*80)
    print("✅ TESTE COMPLETO!")
    print("="*80)


if __name__ == "__main__":
    main()
