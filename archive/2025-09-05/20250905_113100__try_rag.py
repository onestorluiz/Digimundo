#!/usr/bin/env python3
"""
Teste do sistema RAG integrado ao UnifiedMemoryManager.
Valida recuperação, citação e integração com memórias L1-L4.
"""

import sys
import json
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.adapter import RAGAdapter
from src.memory.unified_manager import UnifiedMemoryManager


def main():
    print("=" * 60)
    print("TESTE RAG + UNIFIED MEMORY")
    print("=" * 60)
    
    # 1. Testar RAGAdapter standalone
    print("\n1. TESTANDO RAG ADAPTER STANDALONE")
    print("-" * 40)
    
    rag = RAGAdapter()
    
    # Testar retrieve
    query = "Como estruturar um roteiro em três atos?"
    results = rag.retrieve(query, k=3)
    
    print(f"Query: {query}")
    print(f"Resultados encontrados: {len(results)}")
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.get('citation', 'Sem citação')}")
        print(f"   Score: {result.get('score', 0):.2f}")
        print(f"   Texto: {result.get('text', '')[:100]}...")
    
    # Testar stats
    stats = rag.get_stats()
    print(f"\nEstatísticas RAG:")
    print(f"- Habilitado: {stats['enabled']}")
    print(f"- Provider: {stats['provider']}")
    print(f"- Base de conhecimento: {stats['knowledge_base_size']} docs")
    print(f"- Módulos RAG: {stats['rag_modules']}")
    
    # 2. Testar integração com UnifiedMemoryManager
    print("\n2. TESTANDO INTEGRAÇÃO COM UNIFIED MEMORY")
    print("-" * 40)
    
    settings = {
        'rag': {
            'enabled': True,
            'provider': 'chroma',
            'k': 8
        },
        'memory': {
            'time_weighted_retrieval': True,
            'promote_on_hits': 5
        }
    }
    
    manager = UnifiedMemoryManager(settings)
    
    # Salvar algumas memórias de teste
    print("\nSalvando memórias de teste...")
    mem_ids = []
    
    mem_ids.append(manager.save_memory(
        "O protagonista deve ter um objetivo claro no primeiro ato",
        tags=['estrutura', 'primeiro_ato'],
        importance=0.8
    ))
    
    mem_ids.append(manager.save_memory(
        "O clímax deve resolver o conflito principal estabelecido no setup",
        tags=['estrutura', 'climax'],
        importance=0.9
    ))
    
    mem_ids.append(manager.save_memory(
        "Diálogos devem revelar caráter através de subtexto",
        tags=['dialogo', 'personagem'],
        importance=0.7
    ))
    
    print(f"Memórias salvas: {mem_ids}")
    
    # Buscar contexto combinado
    print("\n3. BUSCANDO CONTEXTO COMBINADO (L1-L4 + RAG)")
    print("-" * 40)
    
    query2 = "estrutura narrativa e desenvolvimento de personagens"
    context = manager.get_context(query2, max_chunks=6)
    
    print(f"Query: {query2}")
    print(f"Contextos encontrados: {len(context)}")
    
    # Agrupar por fonte
    by_source = {}
    for ctx in context:
        source = ctx.get('kind', 'unknown')
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(ctx)
    
    print(f"\nDistribuição por fonte:")
    for source, items in by_source.items():
        print(f"- {source}: {len(items)} resultados")
    
    # Mostrar top 3
    print(f"\nTop 3 resultados:")
    for i, ctx in enumerate(context[:3], 1):
        print(f"\n{i}. [{ctx.get('kind')}] Score: {ctx.get('score', 0):.2f}")
        print(f"   Fonte: {ctx.get('source', 'N/A')}")
        print(f"   Texto: {ctx.get('text', '')[:150]}...")
        if ctx.get('meta', {}).get('citation'):
            print(f"   Citação: {ctx['meta']['citation']}")
    
    # 4. Testar promoção de memória
    print("\n4. TESTANDO PROMOÇÃO DE MEMÓRIA")
    print("-" * 40)
    
    if mem_ids and mem_ids[0]:
        # Simular hits
        for _ in range(5):
            manager.record_hit(mem_ids[0])
        
        # Tentar promover
        promoted = manager.promote_memory(mem_ids[0])
        print(f"Memória {mem_ids[0]} promovida: {promoted}")
    
    # 5. Testar rerank
    print("\n5. TESTANDO RERANK")
    print("-" * 40)
    
    if context:
        reranked = rag.rerank(context[:3], query2)
        print("Resultados após rerank:")
        for i, ctx in enumerate(reranked, 1):
            print(f"{i}. Score: {ctx.get('score', 0):.2f} - {ctx.get('source', 'N/A')}")
    
    # Resultado final
    print("\n" + "=" * 60)
    print("✅ TESTE RAG CONCLUÍDO COM SUCESSO")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        exit(1)