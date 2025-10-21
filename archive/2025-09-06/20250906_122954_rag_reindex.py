#!/usr/bin/env python3
"""
V3.2 — RAG Reindex Tool
Indexa TODOS os documentos na collection ChromaDB alinhada.
"""
import argparse
import json
import hashlib
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

def compute_doc_hash(content: str) -> str:
    """Computa hash determinístico do documento."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Divide texto em chunks com overlap."""
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end]
        
        # Se não é o último chunk, tenta cortar em espaço
        if end < text_len and ' ' in chunk[-50:]:
            last_space = chunk.rfind(' ')
            if last_space > chunk_size - 200:
                chunk = chunk[:last_space]
                end = start + last_space
        
        chunks.append(chunk)
        start = end - overlap if end < text_len else end
    
    return chunks

def extract_pdf_text(pdf_path: Path) -> str:
    """Extrai texto de PDF (stub por agora)."""
    # Stub: apenas retorna nome do arquivo
    # Em produção, usar PyPDF2 ou pdfplumber
    return f"[PDF Content: {pdf_path.name}]"

def index_document(doc_path: Path, collection, batch_docs: List, batch_ids: List, batch_metas: List) -> int:
    """
    Indexa um documento no batch.
    
    Returns:
        Número de chunks adicionados ao batch
    """
    try:
        # Ler conteúdo
        if doc_path.suffix.lower() == '.pdf':
            content = extract_pdf_text(doc_path)
        else:
            content = doc_path.read_text(encoding='utf-8', errors='ignore')
        
        # Computar hash do documento
        doc_hash = compute_doc_hash(content)
        
        # Criar chunks
        chunks = chunk_text(content, chunk_size=1000, overlap=200)
        
        # Adicionar cada chunk ao batch
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc_hash}#c{i}"
            
            metadata = {
                "source": str(doc_path.name),
                "path": str(doc_path),
                "doc_hash": doc_hash,
                "chunk_no": i,
                "total_chunks": len(chunks),
                "mtime": datetime.fromtimestamp(doc_path.stat().st_mtime).isoformat()
            }
            
            # Adicionar tipo específico
            if doc_path.suffix.lower() == '.pdf':
                metadata["type"] = "pdf"
            elif doc_path.suffix.lower() == '.md':
                metadata["type"] = "markdown"
            else:
                metadata["type"] = "text"
            
            batch_ids.append(chunk_id)
            batch_docs.append(chunk)
            batch_metas.append(metadata)
        
        return len(chunks)
        
    except Exception as e:
        print(f"⚠️ Erro ao indexar {doc_path}: {e}")
        return 0

def run_reindex(docs_dir: Path, collection_name: str = "v3_1_docs", batch_size: int = 100):
    """
    Executa reindexação completa.
    
    Args:
        docs_dir: Diretório com documentos
        collection_name: Nome da collection ChromaDB
        batch_size: Tamanho do batch para indexação
    """
    report = {
        "timestamp": datetime.now().isoformat(),
        "docs_dir": str(docs_dir),
        "collection": collection_name,
        "status": "started",
        "stats": {
            "total_files": 0,
            "indexed_files": 0,
            "total_chunks": 0,
            "errors": []
        }
    }
    
    try:
        import chromadb
        
        # Conectar ao ChromaDB
        chroma_path = os.environ.get('CHROMA_PATH', str(Path(__file__).parent.parent.parent / 'data' / 'chroma'))
        print(f"🔗 Conectando ao ChromaDB: {chroma_path}")
        client = chromadb.PersistentClient(path=chroma_path)
        
        # Resetar collection para reindexação limpa
        print(f"🗑️ Resetando collection: {collection_name}")
        try:
            client.delete_collection(collection_name)
        except:
            pass
        
        collection = client.create_collection(
            name=collection_name,
            metadata={"description": "V3.2 aligned collection - full reindex"}
        )
        
        # Encontrar todos os documentos
        exts = ('.pdf', '.txt', '.md')
        doc_files = [p for p in docs_dir.rglob("*") if p.suffix.lower() in exts and p.is_file()]
        report["stats"]["total_files"] = len(doc_files)
        
        print(f"📚 Encontrados {len(doc_files)} documentos para indexar")
        
        # Indexar em batches
        batch_ids = []
        batch_docs = []
        batch_metas = []
        
        for i, doc_path in enumerate(doc_files):
            print(f"  [{i+1}/{len(doc_files)}] {doc_path.name}...", end="")
            
            chunks_added = index_document(doc_path, collection, batch_docs, batch_ids, batch_metas)
            
            if chunks_added > 0:
                report["stats"]["indexed_files"] += 1
                report["stats"]["total_chunks"] += chunks_added
                print(f" ✅ {chunks_added} chunks")
            else:
                print(f" ⚠️ skipped")
            
            # Fazer commit do batch quando atingir o tamanho
            if len(batch_ids) >= batch_size:
                print(f"  💾 Salvando batch de {len(batch_ids)} chunks...")
                collection.add(
                    ids=batch_ids,
                    documents=batch_docs,
                    metadatas=batch_metas
                )
                batch_ids = []
                batch_docs = []
                batch_metas = []
        
        # Fazer commit do batch final
        if batch_ids:
            print(f"  💾 Salvando batch final de {len(batch_ids)} chunks...")
            collection.add(
                ids=batch_ids,
                documents=batch_docs,
                metadatas=batch_metas
            )
        
        # Verificar resultado
        final_count = collection.count()
        print(f"\n✅ Indexação completa: {final_count} chunks em ChromaDB")
        
        report["status"] = "completed"
        report["stats"]["chroma_count"] = final_count
        
        # Testar busca
        print("\n🔍 Testando busca...")
        test_results = collection.query(
            query_texts=["screenplay structure"],
            n_results=3
        )
        
        if test_results and test_results.get('documents'):
            print(f"  ✅ Busca funcionando - {len(test_results['documents'][0])} resultados")
            report["test_query"] = {
                "query": "screenplay structure",
                "results": len(test_results['documents'][0])
            }
        
    except Exception as e:
        report["status"] = "failed"
        report["error"] = str(e)
        print(f"\n❌ Erro: {e}")
    
    # Salvar relatório
    report_path = Path(__file__).parent.parent.parent / 'reports' / 'fix_v3' / 'v32_bugfix_indexalign' / 'reindex_report.json'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n📊 Relatório salvo: {report_path}")
    
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reindexar documentos no ChromaDB")
    parser.add_argument("--docs", default="data/cinema_knowledge/01_ORIGINAIS_PDF", help="Diretório com documentos")
    parser.add_argument("--collection", default="v3_1_docs", help="Nome da collection ChromaDB")
    parser.add_argument("--batch-size", type=int, default=100, help="Tamanho do batch")
    
    args = parser.parse_args()
    
    docs_dir = Path(args.docs)
    if not docs_dir.exists():
        # Tentar caminho alternativo
        alt_path = Path(__file__).parent.parent.parent / args.docs
        if alt_path.exists():
            docs_dir = alt_path
        else:
            print(f"❌ Diretório não encontrado: {args.docs}")
            exit(1)
    
    run_reindex(docs_dir, args.collection, args.batch_size)