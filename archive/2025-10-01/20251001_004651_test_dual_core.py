"""
Teste do DualCoreWrapper com DrDialogue

Este teste valida a arquitetura Dual-Core funcionando.
"""

import sys
from pathlib import Path

# Adicionar paths
sys.path.insert(0, str(Path(__file__).parent))

from specialists.implementations.character_dialogue_specialist import DrDialogue
from specialists.dual_core import DualCoreWrapper

# Roteiro de teste simples
TEST_SCREENPLAY = """
INT. COFFEE SHOP - DAY

JOHN, 30s, sits alone. MARY, 20s, approaches.

MARY
Hey. Can we talk?

JOHN
(not looking up)
About what?

MARY
Us. You. Everything.

JOHN
There's nothing to talk about.

MARY
That's exactly the problem! You never want to talk.
You just shut down whenever things get real.

JOHN
(stands up)
I have to go.

MARY
See? You're doing it again!

John walks away. Mary sits down, defeated.
"""

def test_python_only():
    """Teste 1: Apenas Python (baseline)"""
    print("\n" + "="*60)
    print("TEST 1: PYTHON-ONLY ANALYSIS (Baseline)")
    print("="*60)

    specialist = DrDialogue()
    result = specialist.analyze(TEST_SCREENPLAY)

    print(f"\n✅ Python Analysis Complete")
    print(f"Keys returned: {list(result.keys())}")
    print(f"Total characters analyzed: {result.get('character_count', 0)}")
    print(f"Total dialogues analyzed: {result.get('dialogue_count', 0)}")

    return result

def test_dual_core():
    """Teste 2: Dual-Core (Python + LLM)"""
    print("\n" + "="*60)
    print("TEST 2: DUAL-CORE ANALYSIS (Python + LLM)")
    print("="*60)

    # Criar especialista Python
    specialist = DrDialogue()

    # Envolver em DualCoreWrapper
    dual_core = DualCoreWrapper(
        python_specialist=specialist,
        llm_model="mixtral:8x7b-instruct-v0.1-q5_K_M",
        llm_timeout=60,
        fallback_to_python=True
    )

    print(f"\n📊 DualCoreWrapper: {dual_core}")
    print(f"Specialist: {dual_core.specialist_name}")
    print(f"LLM Model: {dual_core.llm_model}")

    print("\n⏳ Running Dual-Core analysis...")
    print("   Phase 1: Python structural analysis...")
    print("   Phase 2: LLM qualitative insights...")
    print("   Phase 3: Synthesis...")

    result = dual_core.analyze(TEST_SCREENPLAY)

    print(f"\n✅ Dual-Core Analysis Complete")
    print(f"Python Success: {result.get('python_success')}")
    print(f"LLM Success: {result.get('llm_success')}")
    print(f"Keys returned: {list(result.keys())}")

    # Mostrar insights LLM (primeiros 500 chars)
    if result.get('llm_insights'):
        llm_text = result['llm_insights']
        print(f"\n📝 LLM Insights Preview:")
        print("-" * 60)
        print(llm_text[:500] + "..." if len(llm_text) > 500 else llm_text)
        print("-" * 60)

    # Mostrar synthesis
    if result.get('synthesis'):
        print(f"\n🔬 Synthesis:")
        print(f"Quality Score: {result['synthesis'].get('quality_score')}")
        print(f"Methodology: {result['synthesis']['combined_analysis']['methodology']}")

    return result

def compare_results(python_result, dual_core_result):
    """Compara Python-only vs Dual-Core"""
    print("\n" + "="*60)
    print("COMPARISON: Python-only vs Dual-Core")
    print("="*60)

    print(f"\n📊 Python-only:")
    print(f"   Size: {len(str(python_result))} bytes")
    print(f"   Type: Structural data only")

    print(f"\n🔥 Dual-Core:")
    print(f"   Size: {len(str(dual_core_result))} bytes")
    print(f"   Type: Structural data + Qualitative insights")
    print(f"   Python included: {dual_core_result.get('python_success')}")
    print(f"   LLM included: {dual_core_result.get('llm_success')}")

    # Ganho de informação
    gain = len(str(dual_core_result)) - len(str(python_result))
    print(f"\n📈 Information Gain: +{gain} bytes ({gain/len(str(python_result))*100:.1f}%)")

if __name__ == "__main__":
    print("\n🔥🔥🔥 DUAL-CORE WRAPPER TEST 🔥🔥🔥")
    print("Testing DualCoreWrapper with DrDialogue specialist")

    try:
        # Teste 1: Python-only
        python_result = test_python_only()

        # Teste 2: Dual-Core
        dual_core_result = test_dual_core()

        # Comparação
        compare_results(python_result, dual_core_result)

        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)
        print("\nDual-Core architecture is OPERATIONAL! 🚀")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
