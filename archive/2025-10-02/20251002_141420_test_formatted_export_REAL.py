#!/usr/bin/env python3
"""
Teste do Formatted Exporter - Com ROTEIRO COMPLETO para resultado de qualidade
"""

import sys
from pathlib import Path

# Add project root to path (necessário até scripturemon ser instalado globalmente)
sys.path.insert(0, str(Path(__file__).parent.parent))

from specialists.implementations.character_dialogue_specialist import DrDialogue
from specialists.dual_core.base.dual_core_wrapper import DualCoreWrapper
from specialists.dual_core.exporters.formatted_exporter import FormattedExporter

def main():
    print("=" * 80)
    print("TESTE: FORMATTED EXPORT - COM ROTEIRO COMPLETO")
    print("=" * 80)
    print()

    # Carregar roteiro COMPLETO (não um snippet!)
    SCREENPLAY_PATH = Path("content/screenplays/personal/sonhos_sem_lembrancas_t3.txt")

    # Verificar se roteiro existe
    if not SCREENPLAY_PATH.exists():
        print(f"❌ Roteiro não encontrado: {SCREENPLAY_PATH}")
        print("Usando roteiro de exemplo alternativo...")
        SCREENPLAY_PATH = Path("content/screenplays/examples/sonhos_sem_lembrancas_t3.txt")
        if not SCREENPLAY_PATH.exists():
            print("❌ Nenhum roteiro disponível!")
            return

    # Carregar roteiro completo
    print(f"📄 Carregando roteiro: {SCREENPLAY_PATH}")
    with open(SCREENPLAY_PATH, 'r', encoding='utf-8') as f:
        screenplay_text = f.read()

    print(f"   Tamanho: {len(screenplay_text):,} caracteres")
    print(f"   Linhas: {len(screenplay_text.splitlines()):,}")
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
    print("   ⏱️  Isso pode demorar ~10 minutos com deep_context...")
    print()
    try:
        result = wrapper.analyze(screenplay_text)

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
    txt_path = exporter.export_txt(result, screenplay_title="Sonhos_Sem_Lembrancas_REAL")
    print(f"✅ TXT salvo em: {txt_path}")
    print(f"   Tamanho: {txt_path.stat().st_size:,} bytes")
    print()

    # 5. Exportar HTML
    print("🌐 Exportando HTML formatado...")
    html_path = exporter.export_html(result, screenplay_title="Sonhos_Sem_Lembrancas_REAL")
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

    print("=" * 80)
    print("✅ TESTE CONCLUÍDO COM ROTEIRO COMPLETO!")
    print("=" * 80)
    print()
    print("💡 DIFERENÇA: Este teste usa roteiro COMPLETO (~10-50 páginas)")
    print("   ao invés de snippet de 7 linhas, resultando em análise")
    print("   muito mais específica e precisa do LLM.")
    print()

if __name__ == "__main__":
    main()
