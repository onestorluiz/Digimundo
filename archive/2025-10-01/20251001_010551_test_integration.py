"""
Teste de integração end-to-end do sistema Scripturemon com Dual-Core

Valida que o sistema completo funciona com Dual-Core integrado.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.scripturemon import ScripturemonSystem

# Roteiro de teste
TEST_SCREENPLAY = """
INT. OFFICE - DAY

SARAH, 35, stressed executive, types furiously.

MARK, 40, her boss, enters.

MARK
We need to talk.

SARAH
(not looking up)
I'm busy.

MARK
This can't wait. The client pulled out.

SARAH
(stops typing, looks up slowly)
What?

MARK
They're going with our competitor.
All because of that presentation you gave.

SARAH
That presentation was perfect!

MARK
Sarah, you have to understand--

SARAH
(standing up)
No, YOU have to understand. I worked 80 hours
on that presentation. Every slide, every word.

MARK
And it was too technical. They needed emotion,
not data.

Sarah sits back down, defeated.

SARAH
(quietly)
I thought data was what mattered.

MARK
(softening)
In this business? It's all about the story.

He puts a hand on her shoulder. She doesn't pull away.

FADE OUT.
"""

def main():
    print("\n🔥🔥🔥 SCRIPTUREMON DUAL-CORE INTEGRATION TEST 🔥🔥🔥\n")

    try:
        # Inicializar sistema com Dual-Core
        print("Inicializando ScripturemonSystem com Dual-Core...")
        system = ScripturemonSystem(use_memory=False, use_dual_core=True)

        print(f"\n✅ Sistema inicializado:")
        print(f"   Dual-Core: {system.use_dual_core}")
        print(f"   Python Specialists: {list(system.python_specialists.keys())}")
        print(f"   Memory: {system.use_memory}")

        # Executar análise QUICK (apenas dialogue)
        print(f"\n🎬 Analisando roteiro em modo QUICK (character_dialogue)...")
        print(f"   Tamanho do roteiro: {len(TEST_SCREENPLAY)} caracteres")

        report_path = system.analyze(
            screenplay_content=TEST_SCREENPLAY,
            title='Test_Dual_Core_Integration',
            mode='QUICK'  # Apenas character_dialogue
        )

        print(f"\n✅ Análise completa!")
        print(f"   Report Path: {report_path}")

        # Verificar se usou Dual-Core
        stats = system.session_stats
        print(f"\n📊 Estatísticas da sessão:")
        print(f"   Análises totais: {stats['analyses_performed']}")
        print(f"   Dual-Core analyses: {stats['dual_core_analyses']}")
        print(f"   Specialists executados: {stats['specialists_executed']}")

        if stats['dual_core_analyses'] > 0:
            print(f"\n🔥 SUCESSO! Sistema usou Dual-Core! 🔥")
        else:
            print(f"\n⚠️ AVISO: Dual-Core não foi usado (fallback para LLM-only)")

        # Verificar output
        report_file = Path(report_path)

        if report_file.exists():
            print(f"\n📄 Relatório gerado:")
            print(f"   Path: {report_file}")
            print(f"   Size: {report_file.stat().st_size} bytes")

            # Ler primeiras linhas do relatório
            with open(report_file, 'r') as f:
                lines = f.readlines()[:50]
                print(f"\n📝 Preview do relatório (primeiras 50 linhas):")
                print("".join(lines))
        else:
            print(f"\n⚠️ Relatório não encontrado em {report_file}")

        print("\n" + "="*60)
        print("✅ TESTE DE INTEGRAÇÃO COMPLETO")
        print("="*60)

    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
