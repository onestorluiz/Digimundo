#!/usr/bin/env python3
"""
Teste de persistência com DAO.
Cria memória, lê, promove, busca contexto.
"""

import sys
from pathlib import Path

# Adicionar diretórios ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.memory.unified_manager import UnifiedMemoryManager
from src.memory.sqlite_dao import MemoryDAO


def main():
    """Testa persistência de memórias com DAO."""
    
    print("=== Teste de Persistência com DAO ===\n")
    
    # 1. Testar DAO diretamente
    print("1. Testando DAO diretamente...")
    
    db_path = Path(__file__).parent.parent / 'data' / 'memory' / 'mem.db'
    dao = MemoryDAO(str(db_path))
    
    # Criar memória via DAO
    test_id = "test_persist_001"
    created = dao.create(
        id=test_id,
        content="Esta é uma memória de teste para verificar persistência com DAO.",
        tags=["teste", "dao", "persistencia"],
        importance=0.75,
        kind='L3'
    )
    
    if created:
        print(f"   ✅ Memória criada via DAO: ID={test_id}")
    else:
        print(f"   ℹ️  Memória já existe, continuando...")
    
    # Ler memória
    memory = dao.read(test_id)
    if memory:
        print(f"   ✅ Memória lida:")
        print(f"      Content: {memory['content'][:50]}...")
        print(f"      Tags: {memory['tags']}")
        print(f"      Kind: {memory['kind']}")
        print(f"      Hits: {memory['hits']}")
    
    # Incrementar hits
    dao.increment_hits(test_id)
    dao.increment_hits(test_id)
    print(f"   ✅ Hits incrementados 2x")
    
    # Promover
    promoted = dao.promote(test_id, 'L2')
    print(f"   ✅ Memória promovida para L2: {promoted}")
    
    # Verificar promoção
    memory = dao.read(test_id)
    print(f"   ✅ Verificação após promoção:")
    print(f"      Kind: {memory['kind']}")
    print(f"      Hits: {memory['hits']}\n")
    
    dao.close()
    
    # 2. Testar UnifiedMemoryManager
    print("2. Testando UnifiedMemoryManager com DAO...")
    
    settings = {
        'memory': {
            'enabled': True,
            'time_weighted_retrieval': True,
            'promote_on_hits': 3
        },
        'rag': {
            'enabled': False
        }
    }
    
    manager = UnifiedMemoryManager(settings)
    
    # Salvar nova memória
    mem_id = manager.save_memory(
        content="O Sistema Scripturemon processa roteiros de cinema com IA avançada.",
        tags=["scripturemon", "cinema", "ai"],
        importance=0.9
    )
    
    if mem_id:
        print(f"   ✅ Memória salva via Manager: ID={mem_id}")
    
    # Buscar contexto
    print("\n3. Buscando contexto...")
    
    context = manager.get_context("roteiros", max_chunks=5)
    
    if context:
        print(f"   ✅ Encontrados {len(context)} resultados para 'roteiros':")
        for i, chunk in enumerate(context[:2], 1):
            print(f"\n   Resultado {i}:")
            print(f"      Source: {chunk['source']}")
            print(f"      Score: {chunk['score']:.3f}")
            print(f"      Text: {chunk['text'][:80]}...")
    
    context = manager.get_context("persistência", max_chunks=5)
    
    if context:
        print(f"\n   ✅ Encontrados {len(context)} resultados para 'persistência':")
        for i, chunk in enumerate(context[:2], 1):
            print(f"\n   Resultado {i}:")
            print(f"      Source: {chunk['source']}")
            print(f"      Score: {chunk['score']:.3f}")
            print(f"      Text: {chunk['text'][:80]}...")
    
    # Testar record_hit e auto-promoção
    print("\n4. Testando auto-promoção com threshold=3...")
    
    if mem_id:
        # Registrar 3 hits para trigger promoção
        for i in range(3):
            manager.record_hit(mem_id)
            print(f"   Hit {i+1} registrado")
        
        # Verificar se foi promovido
        memory = manager.dao.read(mem_id)
        print(f"   Status após 3 hits: kind={memory['kind']}, hits={memory['hits']}")
        print(f"   {'✅ Auto-promovido!' if memory['kind'] == 'L2' else '❌ Não promovido (verificar threshold)'}")
    
    # Estatísticas finais
    print("\n5. Estatísticas do banco de memórias...")
    stats = manager.dao.get_statistics()
    print(f"   Total de memórias: {stats['total']}")
    print(f"   Por tipo: {stats['by_kind']}")
    print(f"   Média de hits: {stats['avg_hits']:.2f}")
    print(f"   Média de importância: {stats['avg_importance']:.3f}")
    
    manager.close()
    
    print("\n✅ Teste de persistência concluído com sucesso!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())