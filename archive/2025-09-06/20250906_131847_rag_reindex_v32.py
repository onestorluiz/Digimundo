#!/usr/bin/env python3
"""
V3.2 R2 — RAG Reindex with real PDF extraction and chunking
"""
import argparse
import json
import hashlib
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rag.pdf_utils import extract_text, get_pdf_metadata
from src.rag.chunking import smart_chunk

def compute_file_hash(file_path: Path) -> str:
    """Compute SHA1 hash of file contents."""
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
    return sha1.hexdigest()[:16]

def index_document(doc_path: Path, collection, stats: dict) -> int:
    """
    Index a document with real extraction and chunking.
    
    Returns:
        Number of chunks indexed
    """
    try:
        # Extract text
        text = extract_text(doc_path)
        if not text or len(text) < 50:
            stats["skipped_files"].append(str(doc_path.name))
            print(f"    ⚠️ Skipped (no text)")
            return 0
        
        # Compute document hash
        doc_hash = compute_file_hash(doc_path)
        
        # Get metadata
        pdf_meta = get_pdf_metadata(doc_path) if doc_path.suffix.lower() == '.pdf' else {}
        
        # Chunk text
        chunks = smart_chunk(text, chunk_size=1000, overlap=120, by_sections=True)
        if not chunks:
            stats["skipped_files"].append(str(doc_path.name))
            print(f"    ⚠️ Skipped (no chunks)")
            return 0
        
        # Prepare for batch insert
        ids = []
        texts = []
        metadatas = []
        
        for chunk_data in chunks:
            chunk_id = f"{doc_hash}#c{chunk_data['chunk_no']}"
            
            # Check if already exists
            try:
                existing = collection.get(ids=[chunk_id])
                if existing and existing.get('ids'):
                    stats["duplicates"] += 1
                    continue
            except:
                pass  # New document
            
            metadata = {
                "source": str(doc_path.name),
                "path": str(doc_path),
                "doc_hash": doc_hash,
                "mtime": datetime.fromtimestamp(doc_path.stat().st_mtime).isoformat(),
                "chunk_no": chunk_data['chunk_no'],
                "total_chunks": len(chunks),
                "type": doc_path.suffix.lower()[1:] if doc_path.suffix else "text",
                "lang": "en",  # Default, could detect
                "section": chunk_data.get('section'),
                "method": chunk_data.get('method', 'overlap')
            }
            
            # Add PDF-specific metadata
            if pdf_meta:
                metadata["pages"] = pdf_meta.get("pages", 0)
                if pdf_meta.get("title"):
                    metadata["title"] = pdf_meta["title"]
            
            ids.append(chunk_id)
            texts.append(chunk_data['text'])
            metadatas.append(metadata)
        
        # Batch add to collection
        if ids:
            collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            print(f"    ✅ {len(ids)} chunks indexed")
            return len(ids)
        else:
            print(f"    ⚠️ All chunks were duplicates")
            return 0
        
    except Exception as e:
        stats["errors"].append(f"{doc_path.name}: {str(e)}")
        print(f"    ❌ Error: {e}")
        return 0

def run_reindex(docs_dir: Path, collection_name: str = "v3_1_docs", rebuild: bool = False):
    """
    Execute complete reindexing with real extraction.
    
    Args:
        docs_dir: Directory with documents
        collection_name: ChromaDB collection name
        rebuild: Whether to rebuild collection from scratch
    """
    report = {
        "timestamp": datetime.now().isoformat(),
        "docs_dir": str(docs_dir),
        "collection": collection_name,
        "rebuild": rebuild,
        "stats": {
            "total_files": 0,
            "indexed_files": 0,
            "total_chunks": 0,
            "duplicates": 0,
            "skipped_files": [],
            "errors": []
        }
    }
    
    try:
        import chromadb
        
        # Connect to ChromaDB
        chroma_path = os.environ.get('CHROMA_PATH', './data/chroma')
        print(f"🔗 Connecting to ChromaDB: {chroma_path}")
        client = chromadb.PersistentClient(path=chroma_path)
        
        # Handle collection
        if rebuild:
            print(f"🗑️ Rebuilding collection: {collection_name}")
            try:
                client.delete_collection(collection_name)
            except:
                pass
            
            collection = client.create_collection(
                name=collection_name,
                metadata={"description": "V3.2 R2 with real PDF extraction and chunking"}
            )
        else:
            collection = client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "V3.2 R2 with real PDF extraction and chunking"}
            )
            print(f"📚 Using existing collection: {collection_name} ({collection.count()} docs)")
        
        # Find all documents
        exts = ('.pdf', '.txt', '.md')
        doc_files = [p for p in docs_dir.rglob("*") if p.suffix.lower() in exts and p.is_file()]
        report["stats"]["total_files"] = len(doc_files)
        
        print(f"\n📄 Found {len(doc_files)} documents to index")
        
        # Index each document
        for i, doc_path in enumerate(doc_files):
            print(f"\n[{i+1}/{len(doc_files)}] {doc_path.name}")
            
            chunks_added = index_document(doc_path, collection, report["stats"])
            
            if chunks_added > 0:
                report["stats"]["indexed_files"] += 1
                report["stats"]["total_chunks"] += chunks_added
        
        # Final stats
        final_count = collection.count()
        print(f"\n✅ Indexing complete: {final_count} chunks in ChromaDB")
        
        report["stats"]["chroma_count"] = final_count
        report["status"] = "completed"
        
        # Test queries
        print("\n🔍 Testing queries...")
        test_queries = [
            "screenplay structure",
            "character development arc",
            "dialogue subtext technique"
        ]
        
        report["test_queries"] = []
        for query in test_queries:
            results = collection.query(
                query_texts=[query],
                n_results=3
            )
            
            if results and results.get('documents'):
                docs = results['documents'][0]
                sources = [m.get('source', 'unknown') for m in results.get('metadatas', [[]])[0]]
                print(f"  ✅ '{query}': {len(docs)} results")
                print(f"     Top sources: {', '.join(set(sources[:3]))}")
                
                report["test_queries"].append({
                    "query": query,
                    "num_results": len(docs),
                    "top_sources": list(set(sources[:3]))
                })
        
    except Exception as e:
        report["status"] = "failed"
        report["error"] = str(e)
        print(f"\n❌ Error: {e}")
    
    # Save report
    report_path = Path(__file__).parent.parent.parent / 'reports' / 'fix_v3' / 'v32_r2_bugfix_align' / 'reindex_report_v32_r2.json'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n📊 Report saved: {report_path}")
    
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reindex documents with real extraction")
    parser.add_argument("--docs", default="data/cinema_knowledge/01_ORIGINAIS_PDF")
    parser.add_argument("--collection", default="v3_1_docs")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild collection from scratch")
    
    args = parser.parse_args()
    
    docs_dir = Path(args.docs)
    if not docs_dir.exists():
        alt_path = Path(__file__).parent.parent.parent / args.docs
        if alt_path.exists():
            docs_dir = alt_path
        else:
            print(f"❌ Directory not found: {args.docs}")
            exit(1)
    
    run_reindex(docs_dir, args.collection, args.rebuild)