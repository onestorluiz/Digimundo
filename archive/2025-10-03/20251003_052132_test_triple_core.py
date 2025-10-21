#!/usr/bin/env python3
"""
Test Script - Triple-Core com configuração otimizada
Executa análise de diálogo com 15×7 exemplos
"""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from triple_core import TripleCoreWrapper
from triple_core.core_1_specialists.dialogue import DrDialogue
from triple_core.exporters import FormattedExporter

print("="*80)
print("🎬 TESTE TRIPLE-CORE - CONFIGURAÇÃO OTIMIZADA (15×7)")
print("="*80)
print()

# 1. Carregar screenplay
screenplay_path = Path("workspace/inputs/test_screenplay.txt")
print(f"📄 Carregando screenplay: {screenplay_path}")

with open(screenplay_path, 'r', encoding='utf-8') as f:
    screenplay_text = f.read()

print(f"   Tamanho: {len(screenplay_text)} caracteres")
print()

# 2. Criar especialista
print("🔧 Criando DrDialogue (Especialista de Diálogo)")
specialist = DrDialogue()
print()

# 3. Criar Triple-Core wrapper
print("🎯 Criando TripleCoreWrapper")
print("   Configuração:")
print("   - Deep Context: True (McKee full book)")
print("   - Problemas: até 15")
print("   - Exemplos/problema: 7")
print("   - Total exemplos esperado: ~105")
print()

wrapper = TripleCoreWrapper(
    python_specialist=specialist,
    llm_model="scripturemon-optimized",
    deep_context=True
)

# 4. Executar análise
print("⚡ Iniciando análise Triple-Core...")
print("   Isso levará ~5-7 minutos (LLM Deep Dive)")
print()

try:
    result = wrapper.analyze(screenplay_text)

    print("="*80)
    print("✅ ANÁLISE COMPLETA!")
    print("="*80)
    print()

    # Estatísticas
    print("📊 ESTATÍSTICAS:")
    print(f"   Core 1 (Python): {len(str(result.get('python_core1', {})))} chars")
    print(f"   Core 2 (Examples): {result.get('python_core2', {}).get('total_examples', 0)} exemplos")
    print(f"   Core 3 (LLM): {len(str(result.get('llm_insights', '')))} chars")
    print(f"   Quality Score: {result.get('synthesis', {}).get('quality_score', 'N/A')}")
    print()

    # Exportar
    print("📄 Exportando resultados...")
    exporter = FormattedExporter()

    txt_file = exporter.export_txt(result, "Test_Triple_Optimized")
    html_file = exporter.export_html(result, "Test_Triple_Optimized")

    print(f"   TXT:  {txt_file}")
    print(f"   HTML: {html_file}")
    print()

    print("="*80)
    print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
    print("="*80)

except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
