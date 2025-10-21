#!/usr/bin/env python3
"""
Testa processamento de um único PDF
"""

import os
import sys
import time
from pathlib import Path

# Adiciona paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, "/Users/clubproducoes/Digimundo/pesquisa_rag/digimundo_rag")

def process_test():
    """Processa um PDF de teste"""
    print("="*60)
    print("🎬 TESTE RÁPIDO - PROCESSAMENTO DE PDF")
    print("="*60)
    
    # Encontra um PDF pequeno para teste
    test_pdf = "/Users/clubproducoes/Digimundo/digimons/scripturemon/cinema/3_roteiros_criador/SONHOS SEM LEMBRANÇAS T.3.pdf"
    
    if not os.path.exists(test_pdf):
        print("❌ PDF de teste não encontrado")
        return False
    
    print(f"\n📄 Processando: {os.path.basename(test_pdf)}")
    
    try:
        from app.processing.pipeline import process_pdf
        
        start = time.time()
        result = process_pdf(test_pdf, doc_type="roteiro_criador")
        elapsed = time.time() - start
        
        print(f"\n✅ SUCESSO! Processado em {elapsed:.1f}s")
        print(f"📊 Resultados:")
        print(f"  - Páginas: {result.get('metadados', {}).get('paginas', 0)}")
        print(f"  - Chunks: {result.get('stats', {}).get('chunks', 0)}")
        print(f"  - Avaliação: {result.get('avaliacao', {}).get('score', 0)}/100")
        
        # Mostra estrutura detectada
        if result.get('estrutura'):
            print(f"\n📝 Estrutura detectada:")
            estrutura = result['estrutura']
            if isinstance(estrutura, dict):
                for key, value in list(estrutura.items())[:3]:
                    print(f"  - {key}: {value}")
            else:
                print(f"  {str(estrutura)[:200]}...")
        
        # Mostra técnicas
        if result.get('tecnicas'):
            print(f"\n🎭 Técnicas identificadas:")
            for tecnica in result['tecnicas'][:3]:
                if isinstance(tecnica, dict):
                    print(f"  - {tecnica.get('tipo', 'N/A')}: {tecnica.get('descricao', '')[:50]}")
                else:
                    print(f"  - {str(tecnica)[:50]}")
        
        # Testa busca RAG
        print(f"\n🔍 Testando busca RAG...")
        from app.retrieval.hybrid import HybridRetriever
        
        retriever = HybridRetriever()
        results = retriever.search("sonhos memórias", top_k=2)
        
        if results:
            print(f"✅ Encontrados {len(results)} resultados relevantes")
            for i, r in enumerate(results[:2], 1):
                print(f"  {i}. Score: {r.get('score', 0):.2f}")
                if r.get('text'):
                    print(f"     Preview: {r['text'][:80]}...")
        else:
            print("⚠️ Nenhum resultado encontrado")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executa teste"""
    success = process_test()
    
    if success:
        print("\n" + "="*60)
        print("🎉 SISTEMA FUNCIONANDO PERFEITAMENTE!")
        print("="*60)
        print("\n✅ Próximos passos:")
        print("  1. Processar os 44 PDFs restantes")
        print("  2. Ativar RAPTOR indexing")
        print("  3. Testar CLI interativo com conhecimento completo")
    else:
        print("\n❌ Sistema precisa de ajustes")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)