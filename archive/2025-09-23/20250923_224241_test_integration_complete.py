#!/usr/bin/env python3
"""
TESTE COMPLETO DA INTEGRAÇÃO
Verifica se ollama_with_memory.py está funcionando corretamente
"""

import json
from pathlib import Path
from ollama_with_memory import OllamaWithMemory
from rag_integration import SimpleRAG

def test_complete_integration():
    """Testa o ciclo completo de integração"""

    print("\n🔬 TESTE DE INTEGRAÇÃO COMPLETA\n")
    print("="*60)

    # 1. Verificar RAG
    print("\n1️⃣ Testando RAG...")
    rag = SimpleRAG()
    stats = rag.get_stats()
    print(f"   ✅ RAG conectado: {stats['total_memories']} memórias")

    # 2. Buscar memória teste
    print("\n2️⃣ Buscando memórias...")
    memories = rag.search_similar("screenplay", limit=2)
    if memories:
        print(f"   ✅ Encontradas {len(memories)} memórias")
        for m in memories[:1]:
            preview = str(m.get('content', ''))[:100]
            print(f"      - {preview}...")
    else:
        print("   ⚠️ Nenhuma memória encontrada")

    # 3. Testar Ollama com Memória
    print("\n3️⃣ Testando Ollama com Memória...")
    analyzer = OllamaWithMemory(debug=False)

    # Roteiro teste mínimo
    test_screenplay = """
    FADE IN:

    INT. LABORATÓRIO - NOITE

    Um CIENTISTA (40s) trabalha sozinho.

    CIENTISTA
    A integração está completa!

    FADE OUT.
    """

    print("   Analisando roteiro teste...")
    result = analyzer.analyze_with_context(test_screenplay, save_result=False)

    if 'error' not in result:
        print("   ✅ Análise completada!")

        # Verificar componentes
        components = ['_metadata', 'metadata', 'evidence_log',
                     'analise_estrutural', 'analise_personagem', 'validation']

        found = [c for c in components if c in result]
        print(f"   📊 Componentes encontrados: {len(found)}/{len(components)}")
        for c in found:
            print(f"      ✅ {c}")

        missing = [c for c in components if c not in result]
        for c in missing:
            print(f"      ❌ {c}")

        # Verificar se usou contexto
        if '_metadata' in result:
            context_count = result['_metadata'].get('context_used', 0)
            print(f"\n   📚 Contexto usado: {context_count} memórias")

    else:
        print(f"   ❌ Erro: {result['error']}")

    # 4. Verificar feedback loop
    print("\n4️⃣ Verificando feedback loop...")

    # Contar memórias antes
    stats_before = rag.get_stats()

    # Fazer análise que salva
    print("   Salvando nova análise...")
    result2 = analyzer.analyze_simple("FADE IN: Teste de feedback")

    # Contar memórias depois
    stats_after = rag.get_stats()

    if stats_after['total_memories'] > stats_before['total_memories']:
        print(f"   ✅ Feedback loop funcionando!")
        print(f"      Antes: {stats_before['total_memories']} memórias")
        print(f"      Depois: {stats_after['total_memories']} memórias")
    else:
        print("   ⚠️ Feedback loop não detectado")

    # 5. Resumo final
    print("\n" + "="*60)
    print("📊 RESUMO DA INTEGRAÇÃO:")
    print("="*60)

    integration_score = 0

    # RAG funcionando
    if stats['total_memories'] > 0:
        print("✅ RAG: Funcional")
        integration_score += 25
    else:
        print("❌ RAG: Sem memórias")

    # Busca funcionando
    if memories:
        print("✅ Busca: Funcional")
        integration_score += 25
    else:
        print("❌ Busca: Não funciona")

    # Ollama respondendo
    if 'error' not in result:
        print("✅ Ollama: Respondendo")
        integration_score += 25
    else:
        print("❌ Ollama: Com erro")

    # Contexto sendo usado
    if '_metadata' in result and result['_metadata'].get('context_used', 0) > 0:
        print("✅ Contexto: Sendo usado")
        integration_score += 25
    else:
        print("⚠️ Contexto: Não usado")

    print(f"\n🎯 Score de Integração: {integration_score}/100")

    if integration_score >= 75:
        print("✅ SISTEMA INTEGRADO COM SUCESSO!")
    elif integration_score >= 50:
        print("⚠️ Sistema parcialmente integrado")
    else:
        print("❌ Integração incompleta")

    # Fechar conexões
    rag.close()

    print("\n🥷 DIGIMUNDO PRESENTE")

    return integration_score

if __name__ == "__main__":
    score = test_complete_integration()
    exit(0 if score >= 75 else 1)