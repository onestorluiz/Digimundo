#!/usr/bin/env python3
"""
Teste REAL do DrDialogue Dual-Core
Usa roteiro: sonhos_sem_lembrancas_t3.txt
"""

import sys
import time
from pathlib import Path

# Setup paths
sys.path.insert(0, str(Path(__file__).parent))

from specialists.implementations.character_dialogue_specialist import DrDialogue
from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper

# Configuração
SCREENPLAY_PATH = Path("content/screenplays/personal/sonhos_sem_lembrancas_t3.txt")
LLM_MODEL = "mixtral:8x7b-instruct-v0.1-q5_K_M"
LLM_TIMEOUT = 120  # 2 minutos

def load_screenplay():
    """Carrega roteiro"""
    print(f"📖 Carregando roteiro: {SCREENPLAY_PATH.name}")

    if not SCREENPLAY_PATH.exists():
        print(f"❌ Roteiro não encontrado: {SCREENPLAY_PATH}")
        sys.exit(1)

    content = SCREENPLAY_PATH.read_text(encoding='utf-8', errors='ignore')

    # Limitar a primeiras 2000 palavras para teste (análise mais rápida)
    words = content.split()
    if len(words) > 2000:
        content = ' '.join(words[:2000])
        print(f"   Usando primeiras 2000 palavras ({len(content)} chars)")
    else:
        print(f"   Roteiro completo ({len(content)} chars)")

    return content


def test_python_only(screenplay):
    """TESTE 1: Análise Python-only (baseline)"""
    print("\n" + "="*70)
    print("🔬 TESTE 1: PYTHON-ONLY ANALYSIS (Baseline)")
    print("="*70)

    start = time.time()

    # Criar especialista Python
    dr_dialogue = DrDialogue()

    print("\n⏳ Executando análise Python...")
    result = dr_dialogue.analyze(screenplay)

    duration = time.time() - start

    print(f"\n✅ Análise Python completa em {duration:.2f}s")
    print("\n📊 RESULTADOS PYTHON:")
    print("-" * 70)

    # Mostrar métricas principais
    if isinstance(result, dict):
        print(f"Character Count: {result.get('character_count', 0)}")
        print(f"Dialogue Count: {result.get('dialogue_count', 0)}")
        print(f"Total Words: {result.get('total_words', 0)}")
        print(f"Avg Words per Line: {result.get('avg_words_per_line', 0):.1f}")

        if 'score' in result:
            print(f"\n🎯 Overall Score: {result['score']}/100")

        if 'diagnosis' in result:
            print(f"\n💬 Diagnosis: {result['diagnosis']}")

        if 'recommendations' in result:
            recs = result['recommendations']
            if recs:
                print(f"\n📋 Top Recommendations:")
                for i, rec in enumerate(recs[:3], 1):
                    print(f"   {i}. {rec}")

    print("-" * 70)

    return result, duration


def test_dual_core(screenplay):
    """TESTE 2: Análise Dual-Core (Python + LLM)"""
    print("\n" + "="*70)
    print("🔥 TESTE 2: DUAL-CORE ANALYSIS (Python + LLM)")
    print("="*70)

    start = time.time()

    # Criar especialista Python
    dr_dialogue = DrDialogue()

    # Envolver em DualCoreWrapper
    print(f"\n🔧 Configurando Dual-Core:")
    print(f"   Python Specialist: {dr_dialogue.name}")
    print(f"   LLM Model: {LLM_MODEL}")
    print(f"   Timeout: {LLM_TIMEOUT}s")

    dual_core = DualCoreWrapper(
        python_specialist=dr_dialogue,
        llm_model=LLM_MODEL,
        llm_timeout=LLM_TIMEOUT,
        fallback_to_python=True
    )

    print("\n⏳ Executando análise Dual-Core...")
    print("   📊 Fase 1: Python structural analysis...")
    print("   🧠 Fase 2: LLM qualitative insights...")
    print("   🔬 Fase 3: Synthesis...")

    try:
        result = dual_core.analyze(screenplay)
        duration = time.time() - start

        print(f"\n✅ Análise Dual-Core completa em {duration:.2f}s")

        # Mostrar resultados
        print("\n📊 RESULTADOS DUAL-CORE:")
        print("-" * 70)

        print(f"Python Success: {result.get('python_success', False)}")
        print(f"LLM Success: {result.get('llm_success', False)}")

        # Synthesis
        if 'synthesis' in result:
            synthesis = result['synthesis']
            print(f"\n🔬 Synthesis Quality Score: {synthesis.get('quality_score', 'N/A')}")

        # LLM Insights (preview)
        if result.get('llm_success') and 'llm_insights' in result:
            llm_text = result['llm_insights']
            print(f"\n🧠 LLM INSIGHTS (preview):")
            print("-" * 70)
            # Mostrar primeiros 800 chars
            preview = llm_text[:800] if len(llm_text) > 800 else llm_text
            print(preview)
            if len(llm_text) > 800:
                print(f"\n... ({len(llm_text) - 800} chars mais)")
            print("-" * 70)
        elif not result.get('llm_success'):
            print("\n⚠️ LLM falhou - usando fallback Python-only")
            if 'llm_insights' in result:
                print(f"   Erro: {result['llm_insights']}")

        return result, duration

    except Exception as e:
        print(f"\n❌ ERRO no Dual-Core: {e}")
        import traceback
        traceback.print_exc()
        return None, time.time() - start


def compare_results(python_result, python_time, dual_core_result, dual_core_time):
    """Compara resultados Python-only vs Dual-Core"""
    print("\n" + "="*70)
    print("📊 COMPARAÇÃO: Python-only vs Dual-Core")
    print("="*70)

    # Tempo
    print(f"\n⏱️ TEMPO:")
    print(f"   Python-only:  {python_time:.2f}s")
    print(f"   Dual-Core:    {dual_core_time:.2f}s")
    print(f"   Diferença:    +{dual_core_time - python_time:.2f}s ({dual_core_time/python_time:.1f}x)")

    # Tamanho da informação
    python_size = len(str(python_result))

    if dual_core_result:
        dual_core_size = len(str(dual_core_result))

        print(f"\n📏 TAMANHO DA INFORMAÇÃO:")
        print(f"   Python-only:  {python_size:,} bytes")
        print(f"   Dual-Core:    {dual_core_size:,} bytes")

        gain = dual_core_size - python_size
        gain_pct = (gain / python_size) * 100
        print(f"   Ganho:        +{gain:,} bytes (+{gain_pct:.1f}%)")

        # Componentes
        print(f"\n🔍 COMPONENTES DUAL-CORE:")
        print(f"   Python Analysis: {dual_core_result.get('python_success', False)}")
        print(f"   LLM Insights:    {dual_core_result.get('llm_success', False)}")
        print(f"   Synthesis:       {'synthesis' in dual_core_result}")

        # Qualidade
        if dual_core_result.get('llm_success'):
            print(f"\n✅ GANHO QUALITATIVO:")
            print(f"   Python fornece:  Dados objetivos (métricas, contagens, padrões)")
            print(f"   LLM adiciona:    Insights qualitativos, interpretação, soluções")
            print(f"   Resultado:       Análise completa e profunda")
        else:
            print(f"\n⚠️ LLM falhou - Dual-Core em modo fallback (Python-only)")


def save_results(python_result, dual_core_result):
    """Salva resultados completos em arquivo"""
    output_dir = Path("workspace/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    # Salvar Python result
    python_file = output_dir / f"dialogue_python_{timestamp}.json"
    import json
    with open(python_file, 'w', encoding='utf-8') as f:
        json.dump(python_result, f, indent=2, default=str)
    print(f"\n💾 Python result salvo: {python_file}")

    # Salvar Dual-Core result
    if dual_core_result:
        dual_core_file = output_dir / f"dialogue_dual_core_{timestamp}.json"
        with open(dual_core_file, 'w', encoding='utf-8') as f:
            json.dump(dual_core_result, f, indent=2, default=str)
        print(f"💾 Dual-Core result salvo: {dual_core_file}")


def main():
    print("\n" + "🔥"*35)
    print("🔥 TESTE REAL: DrDialogue Dual-Core")
    print("🔥"*35)

    # Carregar roteiro
    screenplay = load_screenplay()

    # TESTE 1: Python-only
    python_result, python_time = test_python_only(screenplay)

    # Pausa
    print("\n⏸️  Pausa de 3 segundos...")
    time.sleep(3)

    # TESTE 2: Dual-Core
    dual_core_result, dual_core_time = test_dual_core(screenplay)

    # Comparação
    compare_results(python_result, python_time, dual_core_result, dual_core_time)

    # Salvar resultados
    save_results(python_result, dual_core_result)

    # Resumo final
    print("\n" + "="*70)
    if dual_core_result and dual_core_result.get('llm_success'):
        print("✅ TESTE COMPLETO - DUAL-CORE FUNCIONANDO!")
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("   1. Revisar insights LLM nos arquivos salvos")
        print("   2. Avaliar qualidade da synthesis")
        print("   3. Decidir se converter mais especialistas")
    else:
        print("⚠️ TESTE PARCIAL - LLM não respondeu")
        print("\n🔧 VERIFICAR:")
        print("   1. Ollama está rodando? (ollama ps)")
        print("   2. Modelo existe? (ollama list)")
        print("   3. Timeout suficiente?")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
