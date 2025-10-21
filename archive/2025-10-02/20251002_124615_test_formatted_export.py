#!/usr/bin/env python3
"""
Teste do Formatted Exporter - Demonstração dos formatos TXT e HTML
"""

import sys
from pathlib import Path

# Add project root to path (necessário até scripturemon ser instalado globalmente)
sys.path.insert(0, str(Path(__file__).parent.parent))

from specialists.implementations.character_dialogue_specialist import DrDialogue
from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper
from specialists.dual_core.exporters.formatted_exporter import FormattedExporter

# Roteiro de teste (curto)
TEST_SCREENPLAY = """
INT. OFFICE - DAY

SARAH, 35, stressed executive, types furiously.

MARK, 40, her boss, enters. He looks serious.

MARK
We need to talk.

SARAH
(without looking up)
Can it wait? I'm finishing the report.

MARK
This can't wait. The client pulled out.

SARAH
(stops, shocked)
What? But I worked 80 hours on that presentation!

MARK
I know. But they said it lacked emotion.

SARAH
(defensive)
It had all the data they needed!

MARK
(sits down, calm)
Sarah... sometimes people need to feel, not just think.
"""

def main():
    print("=" * 80)
    print("TESTE: FORMATTED EXPORT - TXT vs HTML")
    print("=" * 80)
    print()

    # 1. Criar especialista e wrapper
    print("📚 Criando DrDialogue com Deep Context...")
    specialist = DrDialogue()

    wrapper = DualCoreWrapper(
        python_specialist=specialist,
        llm_model="scripturemon-optimized",
        llm_timeout=600,  # 10 min (tempo adequado para análise completa)
        deep_context=True  # Deep context habilitado para análise de qualidade
    )

    # 2. Executar análise
    print("⚙️  Executando análise Dual-Core...")
    try:
        result = wrapper.analyze(TEST_SCREENPLAY)

        print(f"✅ Análise concluída!")
        print(f"   Python: {'✓' if result.get('python_success') else '✗'}")
        print(f"   LLM: {'✓' if result.get('llm_success') else '✗'}")
        print()
    except Exception as e:
        print(f"❌ ERRO na análise: {e}")
        print(f"   Tipo: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return

    # 3. Criar exporter
    exporter = FormattedExporter()

    # 4. Exportar TXT
    print("📝 Exportando TXT formatado...")
    txt_path = exporter.export_txt(result, screenplay_title="Test_Office_Scene")
    print(f"✅ TXT salvo em: {txt_path}")
    print(f"   Tamanho: {txt_path.stat().st_size:,} bytes")
    print()

    # 5. Exportar HTML
    print("🌐 Exportando HTML formatado...")
    html_path = exporter.export_html(result, screenplay_title="Test_Office_Scene")
    print(f"✅ HTML salvo em: {html_path}")
    print(f"   Tamanho: {html_path.stat().st_size:,} bytes")
    print()

    # 6. Mostrar preview do TXT
    print("=" * 80)
    print("PREVIEW TXT (primeiras 50 linhas):")
    print("=" * 80)
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:50], 1):
            print(line.rstrip())

    if len(lines) > 50:
        print(f"\n... (mais {len(lines) - 50} linhas)")
    print()

    # 7. Instruções para abrir
    print("=" * 80)
    print("COMO VISUALIZAR:")
    print("=" * 80)
    print()
    print("📝 TXT:")
    print(f"   cat {txt_path}")
    print(f"   open {txt_path}  # macOS")
    print()
    print("🌐 HTML:")
    print(f"   open {html_path}  # Abre no browser padrão")
    print()

    # 8. Comparação dos formatos
    print("=" * 80)
    print("COMPARAÇÃO DOS FORMATOS:")
    print("=" * 80)
    print()
    print("📝 TXT FORMATADO:")
    print("   ✅ Abre em qualquer editor (VS Code, Sublime, Notepad++)")
    print("   ✅ Legível sem formatação especial")
    print("   ✅ Fácil de compartilhar (email, Slack)")
    print("   ✅ Bordas e seções delimitadas com caracteres")
    print("   ✅ Copia-cola preserva estrutura")
    print()
    print("🌐 HTML:")
    print("   ✅ Formatação visual rica (cores, cards, badges)")
    print("   ✅ Abre no browser (Chrome, Safari, Firefox)")
    print("   ✅ Pode gerar PDF (Print > Save as PDF)")
    print("   ✅ Seções com cores diferentes")
    print("   ✅ Responsivo (adapta ao tamanho da tela)")
    print()
    print("📄 MD (já existe):")
    print("   ✅ Bom para documentação")
    print("   ⚠️  Precisa de viewer MD ou GitHub para ver formatado")
    print()

    print("=" * 80)
    print("✅ TESTE CONCLUÍDO!")
    print("=" * 80)

if __name__ == "__main__":
    main()
