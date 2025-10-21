#!/usr/bin/env python3
"""
Teste de análise com PDF
Demonstra como analisar roteiros em formato PDF
"""

from triple_core.orchestrators.screenplay_analyzer import ScreenplayAnalyzer
from triple_core.orchestrators.fast_analyzer import FastAnalyzer

def test_pdf_support():
    """Testa suporte a PDF"""

    print("="*80)
    print("📄 TESTE: Análise de Roteiro em PDF")
    print("="*80)
    print()

    # Verificar se há PDFs disponíveis
    import os
    from pathlib import Path

    pdf_paths = list(Path("content/screenplays").rglob("*.pdf"))

    if not pdf_paths:
        print("⚠️  Nenhum PDF encontrado em content/screenplays/")
        print()
        print("📝 Para testar:")
        print("1. Converter roteiro TXT para PDF:")
        print("   - Usar Highland, Final Draft, WriterDuet")
        print("   - Ou converter online: https://www.scriptpdf.com/")
        print()
        print("2. Salvar em: content/screenplays/personal/meu_roteiro.pdf")
        print()
        print("3. Executar: python3 test_pdf_analysis.py")
        return

    print(f"✅ Encontrados {len(pdf_paths)} PDF(s):")
    for pdf in pdf_paths:
        print(f"   • {pdf}")
    print()

    # Usar o primeiro PDF
    pdf_path = str(pdf_paths[0])

    print(f"📖 Testando leitura de: {pdf_path}")
    print()

    # Testar leitura básica
    print("1️⃣  Teste de leitura básica...")
    try:
        with open(pdf_path, 'rb') as f:
            import PyPDF2
            reader = PyPDF2.PdfReader(f)
            num_pages = len(reader.pages)
            first_page_text = reader.pages[0].extract_text()[:200]

            print(f"   ✅ PDF lido com sucesso!")
            print(f"   📄 Páginas: {num_pages}")
            print(f"   📝 Primeiras linhas:")
            print(f"      {first_page_text[:100]}...")
    except Exception as e:
        print(f"   ❌ Erro ao ler PDF: {e}")
        return

    print()
    print("2️⃣  Teste de análise RÁPIDA (Core 1 apenas)...")
    try:
        fast = FastAnalyzer()
        result = fast.analyze_screenplay(
            screenplay_path=pdf_path,
            output_dir="workspace/outputs/pdf_test"
        )
        print(f"   ✅ Análise rápida completa!")
        print(f"   📊 Score: {result['overall_score']}/100")
        print(f"   📄 Páginas detectadas: {result['screenplay_stats']['pages']}")
        print(f"   📝 HTML: {result['html_path']}")
    except Exception as e:
        print(f"   ❌ Erro na análise rápida: {e}")

    print()
    print("3️⃣  Teste de análise COMPLETA (Triple-Core)...")
    print("   ⚠️  Isto levará ~25 minutos (22 especialistas × LLM)")
    print()

    response = input("   Executar análise completa? (s/n): ")
    if response.lower() != 's':
        print("   ⏭️  Análise completa pulada.")
        print()
        print("="*80)
        print("✅ TESTE CONCLUÍDO - PDF SUPORTADO")
        print("="*80)
        return

    try:
        analyzer = ScreenplayAnalyzer(
            llm_model="scripturemon-optimized",
            deep_context=False
        )

        result = analyzer.analyze_screenplay(
            screenplay_path=pdf_path,
            output_dir="workspace/outputs/pdf_test"
        )

        print(f"   ✅ Análise completa!")
        print(f"   📊 Score: {result['overall_score']}/100")
        print(f"   📄 Páginas: {result['screenplay_stats']['pages']} (EXATAS do PDF)")
        print(f"   📝 HTML: {result['html_report_path']}")
        print(f"   📝 MD: {result['markdown_report_path']}")
    except Exception as e:
        print(f"   ❌ Erro na análise completa: {e}")

    print()
    print("="*80)
    print("✅ TESTE CONCLUÍDO")
    print("="*80)

if __name__ == "__main__":
    test_pdf_support()
