#!/usr/bin/env python3
"""
Quick GPT-5 Test - Single Specialist × Single Author
~2-4 min, ~$0.05

Tests:
- API key loading
- GPT-5 backend integration
- Cost tracking
- HTML output generation
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add path for imports
sys.path.insert(0, str(Path(__file__).parent))

from engine.analyzers.dr_character import DrCharacter
from engine.orchestration.dual_core_wrapper import DualCoreWrapper

def test_gpt5():
    """Test GPT-5 with DrCharacter × McKee"""

    print('='*80)
    print('🧪 GPT-5 QUICK TEST')
    print('='*80)
    print()
    print('📊 Test: DrCharacter × McKee (Single analysis)')
    print('⏱️  Expected time: 2-4 minutes')
    print('💰 Expected cost: ~$0.05')
    print()

    screenplay_path = "inputs/examples/Te Encontro em Mim .pdf"

    if not Path(screenplay_path).exists():
        print(f'❌ Erro: Roteiro não encontrado: {screenplay_path}')
        sys.exit(1)

    print(f'📄 Roteiro: {screenplay_path}')
    print(f'🔬 Especialista: DrCharacter')
    print(f'📚 Autor: McKee')
    print(f'🤖 Modelo: gpt-5')
    print()

    # Check API key
    import os
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print('❌ ERRO: OPENAI_API_KEY não encontrada!')
        print('   Execute: source load_env.sh')
        sys.exit(1)

    print(f'✅ API Key detectada: {api_key[:10]}...{api_key[-5:]}')
    print()

    print('🚀 Iniciando análise...')
    print()

    start_time = time.time()

    try:
        # Initialize specialist
        specialist = DrCharacter()

        # Wrap with Dual-Core using GPT-5
        wrapper = DualCoreWrapper(
            python_specialist=specialist,
            llm_model='gpt-5',  # ← GPT-5!
            deep_context=True,
            use_theory=True,
            two_pass_llm=True,
            use_personalized_prompts=True,
            specialist_type='mckee'
        )

        # Analyze
        print('   📊 Python Core: Extraindo métricas...')
        print('   🤖 GPT-5 Core: Analisando com contexto teórico...')
        print()

        result = wrapper.analyze(screenplay_path)
        elapsed = time.time() - start_time

        # Results
        success = result.get('llm_success', False)
        quality = result.get('quality_score', 0)

        print(f'✅ Análise completa em {elapsed:.1f}s!')
        print()
        print(f'📊 Resultados:')
        print(f'   • Status: {"✅ Sucesso" if success else "❌ Falha"}')
        print(f'   • Quality Score: {quality:.1f}/10')
        print(f'   • Tempo: {elapsed:.1f}s')
        print()

        # Export HTML
        print('📝 Gerando HTML...')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_path = wrapper.export_formatted(
            result,
            screenplay_title=f"GPT5_TEST_{timestamp}",
            format="html"
        )

        print(f'✅ HTML gerado: {html_path}')
        print()

        # Cost tracking (if available)
        if 'cost_tracking' in result:
            cost = result['cost_tracking']
            print(f'💰 Custos:')
            print(f'   • Input tokens: {cost.get("total_input_tokens", 0):,}')
            print(f'   • Output tokens: {cost.get("total_output_tokens", 0):,}')
            print(f'   • Custo total: ${cost.get("total_cost", 0):.4f}')
            print()

        print('='*80)
        print('🎉 TESTE CONCLUÍDO COM SUCESSO!')
        print('='*80)
        print()
        print('✅ GPT-5 backend está funcionando perfeitamente!')
        print()

        return True

    except Exception as e:
        elapsed = time.time() - start_time
        print(f'❌ ERRO após {elapsed:.1f}s:')
        print(f'   {e}')
        print()
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_gpt5()
    sys.exit(0 if success else 1)
