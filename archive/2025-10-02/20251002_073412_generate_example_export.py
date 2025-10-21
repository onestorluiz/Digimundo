#!/usr/bin/env python3
"""
Gera exemplo de export formatado usando resultados do deep dive test
"""

import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from specialists.dual_core.exporters.formatted_exporter import FormattedExporter

# Carregar resultado do teste deep dive
result_file = Path("results/deep_dive_optimized_test.json")

if not result_file.exists():
    print(f"❌ Arquivo não encontrado: {result_file}")
    print("Execute primeiro: python3 tests/test_deep_dive_optimized.py")
    sys.exit(1)

# Carregar dados
with open(result_file, 'r') as f:
    test_data = json.load(f)

# Construir estrutura result compatível com exporter
result = {
    'specialist': 'DrDialogue',
    'dual_core': True,
    'python_analysis': {
        'overall_score': 57.0,
        'rules_violated': [
            'DIAL.R003: Lack of subtext',
            'DIAL.R001: Unnatural speech patterns'
        ],
        'recommendations': [
            'Add more contractions and interruptions',
            'Develop distinct character voices',
            'Include more subtext in dialogue'
        ],
        'diagnosis': 'Dialogue analysis reveals patterns of on-the-nose dialogue and lack of character voice differentiation.'
    },
    'llm_insights': test_data['analysis'],
    'synthesis': {
        'summary': 'Dual-Core analysis combining Python structural metrics with LLM deep theory insights',
        'quality_score': 0.87,
        'combined_analysis': {
            'objective_data': 'Python detected 57/100 dialogue score with 2 critical violations',
            'qualitative_insights': 'LLM analysis identified 3 major problems with specific McKee theory grounding',
            'methodology': 'Python structural analysis enriched with LLM contextual understanding via Deep Dive mode (77k words McKee theory)'
        }
    }
}

# Criar exporter
exporter = FormattedExporter()

print("=" * 80)
print("GERANDO EXEMPLOS DE EXPORT FORMATADO")
print("=" * 80)
print()

# 1. TXT
print("📝 Gerando TXT formatado...")
txt_path = exporter.export_txt(result, screenplay_title="Sonhos_Sem_Lembrancas_EXEMPLO")
print(f"✅ TXT: {txt_path}")
print(f"   Tamanho: {txt_path.stat().st_size:,} bytes")
print()

# 2. HTML
print("🌐 Gerando HTML formatado...")
html_path = exporter.export_html(result, screenplay_title="Sonhos_Sem_Lembrancas_EXEMPLO")
print(f"✅ HTML: {html_path}")
print(f"   Tamanho: {html_path.stat().st_size:,} bytes")
print()

print("=" * 80)
print("EXEMPLOS GERADOS COM SUCESSO!")
print("=" * 80)
print()
print("📂 Arquivos salvos em:")
print(f"   {exporter.output_dir}")
print()
print("🔍 Para visualizar TXT:")
print(f"   cat {txt_path}")
print()
print("🌐 Para visualizar HTML:")
print(f"   open {html_path}")
print()
