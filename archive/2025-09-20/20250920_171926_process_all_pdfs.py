#!/usr/bin/env python3
"""
Processa todos os PDFs de cinema com o Scripturemon RAG
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any

# Adiciona o diretório correto ao path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, "/Users/clubproducoes/Digimundo/pesquisa_rag/digimundo_rag")

def find_pdfs(base_path: str = "/Users/clubproducoes/Digimundo/digimons/scripturemon/cinema") -> List[Path]:
    """Encontra todos os PDFs no diretório cinema"""
    pdfs = []
    
    if not os.path.exists(base_path):
        print(f"❌ Diretório não encontrado: {base_path}")
        return pdfs
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdfs.append(Path(root) / file)
    
    return sorted(pdfs)

def process_single_pdf(pdf_path: Path) -> Dict[str, Any]:
    """Processa um único PDF"""
    try:
        from app.processing.pipeline import process_pdf
        
        # Determina tipo baseado no diretório
        path_str = str(pdf_path)
        if "roteiros_mestres" in path_str:
            doc_type = "roteiro_mestre"
        elif "roteiros_criador" in path_str:
            doc_type = "roteiro_criador"
        else:
            doc_type = "teoria_roteiro"
        
        print(f"  📄 Processando como '{doc_type}'...")
        start = time.time()
        result = process_pdf(str(pdf_path), doc_type=doc_type)
        elapsed = time.time() - start
        
        print(f"  ✅ Processado em {elapsed:.1f}s")
        print(f"     - {result.get('metadados', {}).get('paginas', 0)} páginas")
        print(f"     - {result.get('stats', {}).get('chunks', 0)} chunks")
        print(f"     - Nota: {result.get('avaliacao', {}).get('score', 0)}/100")
        
        return {"success": True, "result": result, "time": elapsed}
        
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return {"success": False, "error": str(e)}

def main():
    """Processa todos os PDFs encontrados"""
    print("="*60)
    print("🎬 SCRIPTUREMON - PROCESSADOR DE ROTEIROS")
    print("="*60)
    
    # Encontra PDFs
    print("\n🔍 Procurando PDFs...")
    pdfs = find_pdfs()
    
    if not pdfs:
        print("❌ Nenhum PDF encontrado!")
        return
    
    print(f"✅ Encontrados {len(pdfs)} PDFs")
    
    # Mostra primeiros PDFs
    print("\n📚 Primeiros arquivos:")
    for pdf in pdfs[:5]:
        print(f"  - {pdf.name}")
    if len(pdfs) > 5:
        print(f"  ... e mais {len(pdfs)-5} arquivos")
    
    # Processa em batch
    print(f"\n🚀 Iniciando processamento de {len(pdfs)} PDFs...")
    print("⚠️ Isso pode demorar vários minutos...\n")
    
    success = 0
    failed = 0
    total_time = 0
    
    for i, pdf in enumerate(pdfs, 1):
        print(f"\n[{i}/{len(pdfs)}] {pdf.name}")
        
        result = process_single_pdf(pdf)
        
        if result["success"]:
            success += 1
            total_time += result.get("time", 0)
        else:
            failed += 1
        
        # Limite para teste (processa apenas 5 por enquanto)
        if i >= 5:
            print("\n⚠️ Processamento limitado a 5 PDFs para teste")
            remaining = len(pdfs) - i
            if remaining > 0:
                print(f"   Restam {remaining} PDFs para processar")
            break
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DO PROCESSAMENTO")
    print("="*60)
    print(f"✅ Sucesso: {success} PDFs")
    print(f"❌ Falhas: {failed} PDFs")
    print(f"⏱️ Tempo total: {total_time:.1f}s")
    if success > 0:
        print(f"📈 Tempo médio: {total_time/success:.1f}s por PDF")
    
    # Testa busca RAG com o conhecimento processado
    if success > 0:
        print("\n🔍 Testando busca RAG com novo conhecimento...")
        try:
            from app.retrieval.hybrid import HybridRetriever
            
            retriever = HybridRetriever()
            
            queries = [
                "protagonista herói jornada",
                "conflito dramático tensão",
                "três atos estrutura"
            ]
            
            for query in queries:
                results = retriever.search(query, top_k=2)
                if results:
                    print(f"\n  Query: '{query}'")
                    print(f"  ✅ {len(results)} resultados encontrados")
                    if results[0].get('text'):
                        preview = results[0]['text'][:100]
                        print(f"  Preview: {preview}...")
        except Exception as e:
            print(f"❌ Erro ao testar RAG: {e}")
    
    print("\n🏁 Processamento concluído!")
    return success > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)