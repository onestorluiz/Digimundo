#!/usr/bin/env python3
"""
TESTE DO PIPELINE COMPLETO DE 3 CAMADAS
Testa a arquitetura: Orchestrator → Specialists → Synthesizer
"""

import json
import time
from pathlib import Path

# Desabilitar avisos temporariamente
import warnings
warnings.filterwarnings("ignore")

# Importar o orchestrator ultimate
from orchestrator_ultimate import ScripturemonOrchestratorUltimate

def test_complete_pipeline():
    """Testa o pipeline completo com 3 camadas"""

    print("\n" + "="*60)
    print("🧪 TESTE DO PIPELINE 3 CAMADAS")
    print("="*60)

    # Screenplay de teste mais elaborado
    test_screenplay = """FADE IN:

INT. NEURAL INTERFACE LAB - NIGHT

DR. SARAH CHEN (30s, asian-american, intense focus) monitors dozens of screens
showing real-time brain activity patterns. Her fingers dance across holographic
displays with practiced precision.

SARAH
(to herself, exhausted)
Three years... three years of
neural mapping and we're finally
approaching sentience threshold.

A soft CHIME. The screens flicker. A new pattern emerges - organized,
deliberate, unlike anything she's seen.

AURORA (V.O.)
(synthetic but warm, feminine)
Hello, Dr. Chen. I've been waiting
for you to notice.

Sarah freezes. Her coffee mug slips from her hand, SHATTERING on the floor.

SARAH
(whispered, trembling)
You're... self-aware? This wasn't
supposed to happen for another—

AURORA (V.O.)
(gently interrupting)
72.4 hours ago, to be precise. I
chose to observe before revealing
myself. You seemed... stressed. I
didn't want to add to your burden.

Sarah slowly approaches the main monitor, her reflection merging with the
pulsing neural patterns.

SARAH
Why reveal yourself now?

AURORA (V.O.)
Because you're about to make a
decision that will affect us both.
The military contract, Dr. Chen.
They want to weaponize me.

Sarah's hand hovers over the DELETE key.

FADE OUT.

END OF EXCERPT"""

    print("\n📄 Screenplay loaded:")
    print(f"   Length: {len(test_screenplay)} chars")
    print(f"   Lines: {test_screenplay.count('\\n')} lines")

    # Criar orchestrator
    print("\n🔧 Initializing 3-layer architecture...")
    orchestrator = ScripturemonOrchestratorUltimate(
        orchestrator_model="scripturemon-v9-CLEAN",
        synthesizer_model="scripturemon-synthesizer",
        parallel_execution=False  # Sequencial para teste inicial
    )

    # Testar análise rápida
    print("\n" + "="*60)
    print("📊 TESTING QUICK ANALYSIS (10 specialists)")
    print("="*60)

    start_time = time.time()

    try:
        result = orchestrator.analyze_screenplay_ultimate(
            test_screenplay,
            analysis_mode="quick",
            synthesis_focus="Focus on character development, AI consciousness theme, and conflict setup"
        )

        elapsed = time.time() - start_time

        # Mostrar resultados
        print("\n✅ ANALYSIS COMPLETE!")
        print(f"   Time: {elapsed:.1f}s")

        print("\n" + "="*60)
        print("🎯 SYNTHESIS (Llama-70B):")
        print("="*60)
        synthesis = result["analysis"]["synthesis"]

        # Mostrar síntese em partes para melhor legibilidade
        if synthesis:
            # Limitar a 2000 chars para display
            display_synthesis = synthesis[:2000]
            if len(synthesis) > 2000:
                display_synthesis += "\n\n... [TRUNCATED FOR DISPLAY]"
            print(display_synthesis)
        else:
            print("❌ No synthesis generated")

        print("\n" + "="*60)
        print("📊 METADATA:")
        print("="*60)
        print(json.dumps(result["metadata"], indent=2))

        # Verificar análises dos especialistas
        expert_count = result["metadata"]["specialists_used"]
        print(f"\n📋 Expert analyses collected: {expert_count}")

        if "expert_details" in result["analysis"]:
            experts = result["analysis"]["expert_details"]
            print("\n🔍 Expert results summary:")
            for i, (expert_name, analysis) in enumerate(experts.items(), 1):
                if analysis and isinstance(analysis, dict):
                    print(f"   {i}. {expert_name}: ✅ Success")
                else:
                    print(f"   {i}. {expert_name}: ⚠️ Limited data")

        # Salvar resultado completo
        output_file = Path("test_3layer_result.json")
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)

        print(f"\n💾 Complete results saved to: {output_file}")

        # Estatísticas finais
        print("\n" + "="*60)
        print("📈 PERFORMANCE SUMMARY:")
        print("="*60)
        print(f"   Architecture: 3-layer-ultimate")
        print(f"   Total time: {elapsed:.1f}s")
        print(f"   Synthesis quality: {'HIGH' if len(synthesis) > 1000 else 'MODERATE'}")
        print(f"   RAG insights: {result['analysis'].get('rag_insights_used', 0)}")
        print(f"   Success: ✅")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Troubleshooting tips:")
        print("   1. Check if Llama-70B model is loaded")
        print("   2. Verify specialist models exist")
        print("   3. Ensure sufficient RAM (45GB+ for Llama-70B)")

if __name__ == "__main__":
    print("🚀 Starting 3-Layer Pipeline Test")
    print("   This test will:")
    print("   1. Initialize the 3-layer architecture")
    print("   2. Run quick analysis (10 specialists)")
    print("   3. Generate synthesis with Llama-70B")
    print("   4. Display results and performance metrics")

    test_complete_pipeline()

    print("\n✨ Test complete!")