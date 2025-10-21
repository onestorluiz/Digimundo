#!/usr/bin/env python3
"""
Test script for FASE 2: Personalized Prompts Integration

This script tests the personalized prompts system with EGRI author
to validate that the integration with dual_core_wrapper works correctly.

Expected behavior:
- Two-Pass LLM should be enabled
- Personalized prompts should be used (opt-in)
- Quality validation should check for nivel 10 criteria:
  * 15K+ chars
  * 3+ scene citations
  * 3+ verbatim quotes
  * 2+ ANTES/DEPOIS rewrites
  * 3+ theory citations

Target: Score >= 7.0/10 for professional quality
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from engine.analyzers.dr_dialogue import DrDialogue
from engine.orchestration.dual_core_wrapper import DualCoreWrapper

def main():
    print("="*80)
    print("🧪 TESTE: FASE 2 - PROMPTS PERSONALIZADOS")
    print("="*80)
    print()

    # Test screenplay (small excerpt for quick testing)
    test_screenplay = """
    INT. CAFETERIA - DIA

    SOFIA (30s) está sentada sozinha, mexendo no café. ALBERTO (35) se aproxima.

    ALBERTO
    Você está evitando todo mundo.

    SOFIA
    Não estou evitando ninguém.

    ALBERTO
    Sofia, eu conheço você. Desde que aquilo aconteceu—

    SOFIA
    (interrompendo)
    Eu não quero falar sobre isso.

    ALBERTO
    Mas você precisa. Guardar tudo dentro vai te destruir.

    SOFIA
    Eu estou bem.

    ALBERTO
    Não, você não está.

    Sofia desvia o olhar, os olhos marejados.

    SOFIA
    Eu... eu tenho medo de me abrir. De me machucar de novo.

    CUT TO:

    INT. ESCRITÓRIO DE TERAPIA - DIA

    Sofia está deitada no divã. A TERAPEUTA (50s) anota.

    TERAPEUTA
    O que você sente quando pensa nele?

    SOFIA
    Dor. Muita dor. E raiva. E culpa.

    TERAPEUTA
    Culpa?

    SOFIA
    Eu deveria ter percebido antes. Os sinais estavam todos lá.
    """

    print("📄 Roteiro de teste:")
    print(f"   - {len(test_screenplay)} caracteres")
    print(f"   - 2 cenas")
    print(f"   - Diálogos com problemas típicos (on-the-nose, exposição)")
    print()

    print("🎯 Configuração:")
    print("   - Autor: EGRI (Premise theory)")
    print("   - Two-Pass LLM: ✅ ATIVADO")
    print("   - Personalized Prompts: ✅ ATIVADO")
    print("   - Deep Context: ❌ Desativado (teste rápido)")
    print()

    # Initialize specialist
    specialist = DrDialogue()

    # Initialize wrapper WITH personalized prompts (FASE 2)
    print("⚙️  Inicializando DualCoreWrapper com prompts personalizados...")
    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model='scripturemon-optimized',
        use_theory=True,
        deep_context=False,  # Disable for quick test
        specialist_type='egri',  # EGRI author
        two_pass_llm=True,  # Two-Pass architecture
        use_personalized_prompts=True  # ⚠️ FASE 2: ATIVAR PROMPTS PERSONALIZADOS
    )
    print("✅ Wrapper inicializado")
    print()

    # Run analysis
    print("▶️  Executando análise...")
    print()
    try:
        result = wrapper.analyze(test_screenplay)

        print()
        print("="*80)
        print("📊 RESULTADOS")
        print("="*80)
        print()

        # Python analysis
        print("1️⃣  Python Analysis:")
        if result.get('python_success'):
            print("   ✅ Sucesso")
            python_analysis = result.get('python_analysis', {})
            if isinstance(python_analysis, dict):
                issues = python_analysis.get('total_issues', 0)
                print(f"   📈 Total de issues: {issues}")
        else:
            print("   ❌ Falhou")
        print()

        # LLM analysis
        print("2️⃣  LLM Analysis:")
        if result.get('llm_success'):
            print("   ✅ Sucesso")
            llm_insights = result.get('llm_insights', '')
            char_count = len(llm_insights) if isinstance(llm_insights, str) else 0
            print(f"   📏 Output: {char_count} caracteres")
            print(f"   ⭐ Quality Score (basic): {result.get('quality_score', 0):.1f}/10")
        else:
            print("   ❌ Falhou")
        print()

        # Nivel 10 validation
        print("3️⃣  Nivel 10 Validation:")
        nivel_validation = result.get('nivel_10_validation')
        if nivel_validation:
            passed = nivel_validation['passed']
            score = nivel_validation['score']
            issues = nivel_validation['issues']

            status = "✅ PASSOU" if passed else "❌ FALHOU"
            print(f"   {status}")
            print(f"   📊 Score: {score:.1f}/10")
            print(f"   📋 Critérios:")
            for issue in issues:
                print(f"      {issue}")
        else:
            print("   ⚠️  Validação não executada (personalized_prompts desativado?)")
        print()

        # Summary
        print("="*80)
        print("📝 RESUMO")
        print("="*80)
        if nivel_validation:
            if nivel_validation['passed']:
                print("✅ TESTE PASSOU: Análise atingiu critérios nivel 10 (score >= 7.0)")
            else:
                print(f"❌ TESTE FALHOU: Score {nivel_validation['score']:.1f}/10 < 7.0")
                print()
                print("💡 Possíveis causas:")
                print("   - Roteiro de teste muito curto (considerar usar roteiro completo)")
                print("   - Deep context desativado (teoria limitada)")
                print("   - Prompts personalizados precisam de ajuste fino")
        else:
            print("⚠️  ATENÇÃO: Validação nivel 10 não foi executada")

    except Exception as e:
        print()
        print("="*80)
        print("❌ ERRO")
        print("="*80)
        print(f"Erro durante análise: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
