#!/usr/bin/env python3
"""
🎬 TESTE DO SISTEMA RAG COM PDFS DE CINEMA
"""

import sys
sys.path.insert(0, '.')

from apps.scripturemon.cinema_knowledge import get_cinema_knowledge

def test_cinema_rag():
    print("\n" + "="*70)
    print("🎬 TESTE DO SISTEMA CINEMA KNOWLEDGE RAG")
    print("="*70)
    
    cinema = get_cinema_knowledge()
    
    # 1. Estatísticas
    print("\n📊 ESTATÍSTICAS DO SISTEMA:")
    stats = cinema.get_stats()
    print(f"  • Total de PDFs: {stats['total_pdfs']}")
    print(f"  • Total de páginas: {stats['total_pages']}")
    print(f"  • Tamanho total: {stats['total_size_mb']} MB")
    print(f"  • Categorias:")
    for cat, count in stats['categories'].items():
        print(f"    - {cat}: {count} PDFs")
    
    # 2. Teste de busca
    print("\n🔍 TESTE DE BUSCA:")
    test_queries = [
        "screenplay structure",
        "character development",
        "dialogue",
        "three act",
        "plot"
    ]
    
    for query in test_queries:
        results = cinema.search(query, limit=3)
        print(f"\n  Query: '{query}'")
        if results:
            for r in results[:2]:
                print(f"    ✅ {r['name'][:40]} (score: {r['score']:.2f})")
        else:
            print(f"    ❌ Nenhum resultado")
    
    # 3. Teste de contexto RAG
    print("\n\n🤖 TESTE DE CONTEXTO RAG:")
    questions = [
        "How to write good dialogue?",
        "What is the three act structure?",
        "How to develop characters?"
    ]
    
    for question in questions:
        print(f"\n  Pergunta: {question}")
        context = cinema.get_relevant_context(question, max_context_length=500)
        if context:
            print(f"  Contexto recuperado ({len(context)} chars):")
            print(f"  {context[:200]}...")
        else:
            print("  ❌ Nenhum contexto encontrado")
    
    # 4. Exemplos de roteiro
    print("\n\n📝 EXEMPLOS DE ELEMENTOS DE ROTEIRO:")
    examples = cinema.get_screenplay_examples("dialogue")
    if examples:
        print(f"  Encontrados {len(examples)} exemplos de diálogo:")
        for ex in examples[:2]:
            print(f"    • {ex['source']}: {ex['count']} ocorrências")
    
    # 5. Dicas de escrita
    print("\n\n💡 DICAS DE ESCRITA:")
    tips = cinema.get_writing_tips("character")
    if tips:
        for i, tip in enumerate(tips[:3], 1):
            print(f"  {i}. {tip[:100]}...")
    
    # Score final
    print("\n" + "="*70)
    print("📊 RESULTADO DO TESTE RAG")
    print("="*70)
    
    total_score = 0
    if stats['total_pdfs'] >= 40:
        total_score += 30
        print("  ✅ PDFs carregados: 30/30 pontos")
    else:
        partial = (stats['total_pdfs'] / 40) * 30
        total_score += partial
        print(f"  ⚠️ PDFs carregados: {partial:.1f}/30 pontos")
    
    if results:
        total_score += 30
        print("  ✅ Busca funcionando: 30/30 pontos")
    else:
        print("  ❌ Busca falhando: 0/30 pontos")
    
    if context:
        total_score += 40
        print("  ✅ RAG funcionando: 40/40 pontos")
    else:
        print("  ❌ RAG falhando: 0/40 pontos")
    
    print(f"\n🎯 SCORE FINAL: {total_score}/100")
    
    if total_score >= 95:
        print("✅ SISTEMA RAG PERFEITO!")
    elif total_score >= 80:
        print("⚠️ SISTEMA RAG BOM")
    else:
        print("❌ SISTEMA RAG PRECISA MELHORIAS")
    
    return total_score

if __name__ == "__main__":
    score = test_cinema_rag()
    
    # Salvar score
    import json
    from pathlib import Path
    
    report = {
        "cinema_rag_score": score,
        "timestamp": str(Path(__file__).stat().st_mtime)
    }
    
    with open("cinema_rag_test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Relatório salvo em cinema_rag_test_report.json")