#!/usr/bin/env python3
"""
Teste completo do sistema DUAL-CORE DrDialogue
Reproduz o output de 02/10/2025 07:35:34
"""

from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper
from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue
from datetime import datetime

print("="*80)
print("🧪 TESTE COMPLETO DUAL-CORE DRDIALOGUE")
print("="*80)
print()
print("📋 Objetivo: Reproduzir output de 02/10/2025 07:35:34")
print()

# Load screenplay
screenplay_path = 'content/screenplays/personal/sonhos_sem_lembrancas_t3.txt'
with open(screenplay_path, 'r', encoding='utf-8') as f:
    screenplay_text = f.read()

print(f"📄 Roteiro carregado: {len(screenplay_text)} chars")
print()

# Create Python Core 1
print("⚙️  [1/3] Criando Python Core 1 (DrDialogue)...")
dialogue_specialist = DrDialogue()
print(f"   ✅ Specialist: {dialogue_specialist.name}")
print()

# Wrap in Dual-Core
print("🔧 [2/3] Criando Dual-Core Wrapper...")
wrapper = DualCoreWrapper(
    python_specialist=dialogue_specialist,
    llm_model="scripturemon-optimized",
    llm_timeout=600,
    fallback_to_python=True,
    use_theory=True,
    deep_context=False  # SHALLOW mode (como exemplo 02/10)
)
print(f"   ✅ Model: scripturemon-optimized")
print(f"   ✅ Mode: SHALLOW (teoria via chunks)")
print()

# Analyze
print("🚀 [3/3] Executando análise DUAL-CORE...")
print("-" * 80)
start_time = datetime.now()

try:
    result = wrapper.analyze(screenplay_text)

    elapsed = (datetime.now() - start_time).total_seconds()

    print("-" * 80)
    print()
    print("="*80)
    print("✅ ANÁLISE DUAL-CORE COMPLETA")
    print("="*80)
    print()

    # Show results
    print(f"⏱️  Tempo total: {elapsed:.1f}s")
    print()

    if result.get('python_success'):
        python_result = result.get('python_analysis', {})
        print("📊 PARTE 1: ANÁLISE PYTHON")
        print(f"   Score: {python_result.get('score', 'N/A')}/100")
        print(f"   Violations: {len(python_result.get('rule_violations', []))}")
        print(f"   Recommendations: {len(python_result.get('recommendations', []))}")
        print()

    if result.get('llm_success'):
        llm_insights = result.get('llm_insights', '')
        print("🤖 PARTE 2: INSIGHTS LLM")
        print(f"   Tamanho: {len(llm_insights)} chars")
        print(f"   Preview: {llm_insights[:200]}...")
        print()

    synthesis = result.get('synthesis', {})
    if synthesis:
        print("🎯 PARTE 3: SÍNTESE")
        print(f"   Quality Score: {synthesis.get('quality_score', 'N/A'):.2f}/1.0")
        print()

    # Export formatted
    print("📝 Exportando relatório formatado...")
    output_path = wrapper.export_formatted(
        result=result,
        screenplay_title="Sonhos_Sem_Lembrancas_TEST",
        format="txt",
        auto_open=False
    )
    print(f"   ✅ Salvo em: {output_path}")
    print()

    print("="*80)
    print("🎉 SUCESSO - Sistema DUAL-CORE funcionando!")
    print("="*80)

except Exception as e:
    print()
    print("="*80)
    print("❌ ERRO NA ANÁLISE")
    print("="*80)
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()
