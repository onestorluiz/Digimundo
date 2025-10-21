#!/usr/bin/env python3
"""
TESTE COMPLETO END-TO-END DO SISTEMA
Testa análise real com Ollama + Memória + Parser
"""

import time
import json
from ollama_with_memory import OllamaWithMemory

def test_analise_completa():
    """Teste de análise completa com roteiro"""

    print("\n🧪 TESTE 7: Análise Completa End-to-End")
    print("="*60)

    # Roteiro de teste
    test_screenplay = """
    FADE IN:

    INT. LABORATÓRIO - NOITE

    DR. SARAH (40s) trabalha sozinha, cercada por monitores.

    DR. SARAH
    A inteligência artificial está
    evoluindo rápido demais...

    Um ALARME dispara. Ela corre para o terminal.

    DR. SARAH (CONT'D)
    Não... ela acordou.

    FADE OUT.
    """

    print("📝 Roteiro de teste preparado")
    print("-"*40)

    try:
        # Criar analisador
        print("\n1. Inicializando sistema...")
        analyzer = OllamaWithMemory(debug=False)
        print("   ✅ Sistema inicializado")

        # Stats antes
        stats_before = analyzer.get_memory_stats()
        print(f"   📊 Memórias antes: {stats_before.get('total_memories', 0)}")

        # Fazer análise
        print("\n2. Executando análise...")
        start = time.time()

        result = analyzer.analyze_with_context(
            test_screenplay,
            save_result=True
        )

        elapsed = time.time() - start
        print(f"   ⏱️ Tempo: {elapsed:.1f}s")

        # Verificar resultado
        if 'error' in result:
            print(f"   ❌ Erro: {result['error']}")
            return False
        else:
            print("   ✅ Análise concluída")

            # Verificar estrutura
            has_metadata = '_metadata' in result
            has_content = any(k in result for k in ['metadata', 'insight', 'analysis'])

            print(f"   {'✅' if has_metadata else '❌'} Metadados presentes")
            print(f"   {'✅' if has_content else '❌'} Conteúdo analisado")

            # Stats depois
            stats_after = analyzer.get_memory_stats()
            print(f"\n3. Verificando persistência...")
            print(f"   📊 Memórias depois: {stats_after.get('total_memories', 0)}")

            diff = stats_after.get('total_memories', 0) - stats_before.get('total_memories', 0)
            if diff > 0:
                print(f"   ✅ Persistência confirmada (+{diff} registro)")
            else:
                print(f"   ⚠️ Nenhum novo registro salvo")

            # Salvar resultado para análise
            with open('test_result_complete.json', 'w') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print("\n💾 Resultado salvo em test_result_complete.json")

            return True

    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_analise_completa()

    if success:
        print("\n✅ TESTE COMPLETO PASSOU!")
    else:
        print("\n❌ TESTE COMPLETO FALHOU!")

    print("\n🥷 DIGIMUNDO PRESENTE")