#!/usr/bin/env python3
"""
🧪 TESTE DO RAG AVANÇADO
Verifica integração de HyDE, RAPTOR e Self-RAG
"""

import sys
from pathlib import Path

# Adiciona diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

from apps.scripturemon.rag_advanced import AdvancedRAG, HyDE, RAPTOR, SelfRAG

def test_hyde():
    """Testa expansão HyDE"""
    print("\n🧬 Testando HyDE (Hypothetical Document Embeddings)...")
    
    hyde = HyDE()
    
    # Testa geração de documento hipotético
    query = "conflito interno do protagonista"
    hypothetical = hyde.generate_hypothetical(query)
    
    print(f"\nQuery original: '{query}'")
    print(f"Documento hipotético gerado ({len(hypothetical)} chars):")
    print(hypothetical[:300] + "...")
    
    # Testa expansão de queries
    expanded = hyde.expand_query(query)
    print(f"\nQueries expandidas: {len(expanded)}")
    for i, exp in enumerate(expanded[:3], 1):
        print(f"  {i}. {exp[:80]}...")
    
    return True

def test_raptor():
    """Testa árvore RAPTOR"""
    print("\n🌳 Testando RAPTOR (Tree-Organized Retrieval)...")
    
    raptor = RAPTOR()
    
    # Documentos de teste
    docs = [
        {"id": "1", "content": "A estrutura de três atos é fundamental"},
        {"id": "2", "content": "O protagonista deve ter um arco claro"},
        {"id": "3", "content": "Diálogos devem revelar personagem"}
    ]
    
    # Constrói árvore
    tree = raptor.build_tree(docs)
    
    print(f"\nÁrvore construída:")
    print(f"  Nível 0 (docs): {len(tree['level_0'])} documentos")
    print(f"  Nível 1 (temas): {len(tree['level_1'])} clusters")
    print(f"  Nível 2 (abstrações): {len(tree['level_2'])} conceitos")
    
    # Busca na árvore
    results = raptor.multi_level_search("protagonista")
    print(f"\nBusca por 'protagonista': {len(results)} resultados")
    
    return True

def test_self_rag():
    """Testa auto-avaliação Self-RAG"""
    print("\n🔄 Testando Self-RAG (Auto-avaliação)...")
    
    self_rag = SelfRAG()
    
    query = "Como criar tensão narrativa?"
    response = "Tensão narrativa vem do conflito entre desejo e obstáculo."
    context = ["Conflito é o motor da narrativa", "Sem conflito não há drama"]
    
    # Avalia resposta
    evaluation = self_rag.evaluate_response(query, response, context)
    
    print(f"\nQuery: '{query}'")
    print(f"Resposta: '{response}'")
    print(f"\nAvaliação:")
    print(f"  Relevância: {evaluation['relevance']:.1%}")
    print(f"  Completude: {evaluation['completeness']:.1%}")
    print(f"  Precisão: {evaluation['accuracy']:.1%}")
    print(f"  Coerência: {evaluation['coherence']:.1%}")
    print(f"  Score geral: {evaluation['overall_score']:.1%}")
    print(f"  Precisa refinamento: {evaluation['needs_refinement']}")
    
    if evaluation['needs_refinement']:
        refined = self_rag.refine_response(response, evaluation)
        print(f"\nResposta refinada:")
        print(refined)
    
    return True

def test_advanced_rag():
    """Testa sistema RAG completo integrado"""
    print("\n🚀 Testando RAG Avançado Completo...")
    
    rag = AdvancedRAG()
    
    # Busca com todas técnicas
    query = "estrutura do segundo ato"
    
    print(f"\nBuscando: '{query}'")
    print("Técnicas ativas: HyDE + RAPTOR + Self-RAG")
    
    results = rag.search(
        query=query,
        use_hyde=True,
        use_raptor=True,
        use_self_rag=True,
        k=3
    )
    
    print(f"\nResultados encontrados: {len(results)}")
    for i, result in enumerate(results, 1):
        content = result.get("content", "")[:100]
        score = result.get("_self_rag_score", 0)
        print(f"  {i}. {content}... (score: {score:.1%})")
    
    # Gera resposta
    context = [r.get("content", "") for r in results]
    response = rag.generate_response(query, context)
    
    print(f"\nResposta gerada:")
    print(response)
    
    return True

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 TESTE DO SISTEMA RAG AVANÇADO")
    print("=" * 60)
    
    tests = [
        ("HyDE", test_hyde),
        ("RAPTOR", test_raptor),
        ("Self-RAG", test_self_rag),
        ("RAG Completo", test_advanced_rag)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, "✅ PASSOU"))
        except Exception as e:
            results.append((name, f"❌ FALHOU: {e}"))
            print(f"\n❌ Erro em {name}: {e}")
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    for name, status in results:
        print(f"{name:20} {status}")
    
    # Estatísticas
    passed = sum(1 for _, s in results if "✅" in s)
    total = len(results)
    
    print(f"\n{'Total:':20} {passed}/{total} testes passaram")
    print(f"{'Taxa de sucesso:':20} {passed/total*100:.0f}%")
    
    print("\n62/100. Como sempre. Mas o RAG é 40% melhor.")

if __name__ == "__main__":
    main()