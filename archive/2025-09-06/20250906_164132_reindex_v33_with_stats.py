#!/usr/bin/env python3
"""
Reindex PDFs with complete statistics and all fields filled
V3.2 R3 - Final corrections
"""
import sys
from pathlib import Path
import json
import hashlib
from datetime import datetime
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rag.pdf_utils import extract_text, get_pdf_metadata
from src.rag.chunking import smart_chunk
from src.rag.adapter import RAGAdapter, SCHEMA_KEYS, COLLECTION_NAME

def compute_file_hash(file_path: Path) -> str:
    """Compute hash of file content."""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]

def detect_language(text: str) -> str:
    """Simple language detection based on common words."""
    pt_words = ["de", "que", "para", "com", "não", "uma", "por", "mais", "mas", "foi"]
    en_words = ["the", "and", "for", "with", "not", "that", "but", "was", "are", "have"]
    
    text_lower = text.lower()
    pt_score = sum(1 for word in pt_words if word in text_lower)
    en_score = sum(1 for word in en_words if word in text_lower)
    
    if pt_score > en_score * 1.5:
        return "pt"
    else:
        return "en"

def ensure_schema(metadata: dict) -> dict:
    """Ensure all SCHEMA_KEYS are present with defaults."""
    from src.rag.adapter import SCHEMA_KEYS
    
    defaults = {
        'source': 'unknown',
        'path': 'unknown',
        'doc_hash': 'unknown',
        'mtime': 0,
        'chunk_no': 0,
        'total_chunks': 1,
        'type': 'pdf',
        'lang': 'en'
    }
    
    for key in SCHEMA_KEYS:
        if key not in metadata:
            metadata[key] = defaults.get(key, 'unknown')
    
    return metadata

def determine_doc_type(path: Path, text: str) -> str:
    """Determine document type from path and content."""
    name_lower = path.name.lower()
    
    if "screenplay" in name_lower or "script" in name_lower:
        return "screenplay"
    elif "draft" in name_lower:
        return "draft"
    elif "release" in name_lower:
        return "release"
    elif "story" in name_lower or "book" in name_lower:
        return "book"
    elif "guide" in name_lower or "manual" in name_lower:
        return "guide"
    elif "plano" in name_lower or "plan" in name_lower:
        return "plan"
    
    # Check content
    if "INT." in text[:1000] or "EXT." in text[:1000] or "FADE IN:" in text[:1000]:
        return "screenplay"
    elif "Chapter" in text[:1000] or "CHAPTER" in text[:1000]:
        return "book"
    
    return "document"

def reindex_with_stats(pdf_dir: Path, max_docs: int = None, rebuild: bool = True):
    """
    Reindex PDFs with complete statistics.
    
    Args:
        pdf_dir: Directory with PDFs
        max_docs: Maximum documents to index (None for all)
        rebuild: Whether to clear collection first
    """
    
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    if max_docs:
        pdf_files = pdf_files[:max_docs]
    
    if not pdf_files:
        print(f"No PDFs found in {pdf_dir}")
        return None
    
    print(f"\n{'='*60}")
    print(f"REINDEXING WITH COMPLETE STATISTICS")
    print(f"{'='*60}")
    print(f"PDFs to index: {len(pdf_files)}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Rebuild: {rebuild}")
    
    # Initialize adapter
    adapter = RAGAdapter({"rag": {"enabled": True, "provider": "chroma"}})
    
    if not adapter.chroma_collection:
        print("❌ ChromaDB not available!")
        return None
    
    # Clear collection if rebuild
    if rebuild:
        print("\n🗑️  Clearing existing collection...")
        try:
            # Delete all documents
            all_ids = adapter.chroma_collection.get()['ids']
            if all_ids:
                adapter.chroma_collection.delete(ids=all_ids)
                print(f"   Deleted {len(all_ids)} existing documents")
        except Exception as e:
            print(f"   Warning: Could not clear collection: {e}")
    
    # Statistics
    stats = {
        "timestamp": datetime.now().isoformat(),
        "pdf_dir": str(pdf_dir),
        "collection": COLLECTION_NAME,
        "rebuild": rebuild,
        "docs_processed": 0,
        "docs_indexed": 0,
        "total_chunks": 0,
        "total_chars": 0,
        "errors": [],
        "documents": [],
        "statistics": {
            "extraction_methods": {},
            "chunking_methods": {},
            "languages": {},
            "doc_types": {},
            "avg_chunks_per_doc": 0,
            "avg_chars_per_chunk": 0,
            "total_time_seconds": 0
        }
    }
    
    start_time = time.time()
    
    # Process each PDF
    for pdf_idx, pdf_path in enumerate(pdf_files):
        print(f"\n📄 [{pdf_idx+1}/{len(pdf_files)}] {pdf_path.name}")
        
        doc_stats = {
            "name": pdf_path.name,
            "path": str(pdf_path),
            "status": "processing"
        }
        
        try:
            # Get file metadata
            file_stat = pdf_path.stat()
            mtime = int(file_stat.st_mtime)
            size_kb = file_stat.st_size / 1024
            
            # Extract PDF metadata
            pdf_meta = get_pdf_metadata(pdf_path)
            
            # Extract text
            text = extract_text(pdf_path)
            char_count = len(text)
            
            # Check if stub with NEW heuristic
            # OLD: is_stub = text.startswith("[PDF Content:")
            # NEW: NOT stub if chars >= 2000 OR chunks >= 4
            #      IS stub only if chars < 2000 AND chunks <= 1
            
            # First, chunk to get count
            chunks = smart_chunk(text, chunk_size=1000, overlap=120)
            chunk_count = len(chunks)
            
            # Apply new heuristic
            is_stub = (char_count < 2000 and chunk_count <= 1)
            
            if is_stub:
                print(f"   ⚠️  Stub detected (chars={char_count}, chunks={chunk_count}), skipping")
                doc_stats["status"] = "skipped_stub"
                doc_stats["reason"] = f"Stub by new heuristic: chars={char_count}<2000 AND chunks={chunk_count}<=1"
                doc_stats["chars_extracted"] = char_count
                doc_stats["chunks_created"] = chunk_count
                stats["documents"].append(doc_stats)
                continue
            
            print(f"   Extracted: {char_count:,} chars")
            
            # Detect language
            lang = detect_language(text)
            
            # Determine document type
            doc_type = determine_doc_type(pdf_path, text)
            
            # Compute document hash
            doc_hash = compute_file_hash(pdf_path)
            
            # Already chunked above for stub check
            print(f"   Chunks: {chunk_count}")
            
            # Track chunking method
            if chunks:
                method = chunks[0].get("method", "unknown")
                stats["statistics"]["chunking_methods"][method] = \
                    stats["statistics"]["chunking_methods"].get(method, 0) + 1
            
            # Add each chunk to ChromaDB
            chunks_added = 0
            for chunk_data in chunks:
                # Prepare metadata with ALL required fields
                metadata = {
                    "source": pdf_path.name,
                    "path": str(pdf_path),
                    "doc_hash": doc_hash,
                    "mtime": mtime,
                    "chunk_no": chunk_data["chunk_no"],
                    "total_chunks": chunk_count,
                    "type": doc_type,
                    "lang": lang
                }
                
                # Add optional fields
                if chunk_data.get("section"):
                    metadata["section"] = chunk_data["section"]
                if pdf_meta.get("pages"):
                    metadata["pages"] = pdf_meta["pages"]
                if pdf_meta.get("author"):
                    metadata["author"] = pdf_meta["author"]
                
                # Ensure schema completeness
                metadata = ensure_schema(metadata)
                
                # Add to collection
                success = adapter.add_document(
                    text=chunk_data["text"],
                    metadata=metadata
                )
                
                if success:
                    chunks_added += 1
            
            print(f"   ✅ Added {chunks_added}/{chunk_count} chunks")
            
            # Update statistics
            stats["docs_indexed"] += 1
            stats["total_chunks"] += chunks_added
            stats["total_chars"] += char_count
            
            # Track language and type
            stats["statistics"]["languages"][lang] = \
                stats["statistics"]["languages"].get(lang, 0) + 1
            stats["statistics"]["doc_types"][doc_type] = \
                stats["statistics"]["doc_types"].get(doc_type, 0) + 1
            
            # Document stats
            doc_stats.update({
                "status": "indexed",
                "hash": doc_hash,
                "size_kb": size_kb,
                "mtime": mtime,
                "pages": pdf_meta.get("pages", 0),
                "chars_extracted": char_count,
                "chunks_created": chunk_count,
                "chunks_indexed": chunks_added,
                "language": lang,
                "type": doc_type,
                "chunking_method": chunks[0].get("method") if chunks else "none"
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            doc_stats["status"] = "error"
            doc_stats["error"] = str(e)
            stats["errors"].append({
                "file": pdf_path.name,
                "error": str(e)
            })
        
        stats["documents"].append(doc_stats)
        stats["docs_processed"] += 1
    
    # Calculate final statistics
    elapsed = time.time() - start_time
    stats["statistics"]["total_time_seconds"] = elapsed
    
    if stats["docs_indexed"] > 0:
        stats["statistics"]["avg_chunks_per_doc"] = stats["total_chunks"] / stats["docs_indexed"]
    
    if stats["total_chunks"] > 0:
        stats["statistics"]["avg_chars_per_chunk"] = stats["total_chars"] / stats["total_chunks"]
    
    # Verify collection
    print(f"\n{'='*60}")
    print(f"VERIFICATION")
    print(f"{'='*60}")
    
    collection_count = adapter.chroma_collection.count()
    print(f"Collection documents: {collection_count}")
    
    # Test query
    test_results = adapter.retrieve("screenplay structure", k=3)
    print(f"Test query returned: {len(test_results)} results")
    
    if test_results:
        first = test_results[0]
        print(f"\nFirst result metadata check:")
        meta = first.get('metadata', {})
        for key in SCHEMA_KEYS:
            status = "✓" if key in meta else "✗"
            value = meta.get(key, "MISSING")
            print(f"  {status} {key}: {value}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Documents processed: {stats['docs_processed']}")
    print(f"Documents indexed: {stats['docs_indexed']}")
    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Total characters: {stats['total_chars']:,}")
    print(f"Time elapsed: {elapsed:.2f}s")
    
    if stats["docs_indexed"] > 0:
        print(f"\nAverages:")
        print(f"  Chunks per doc: {stats['statistics']['avg_chunks_per_doc']:.1f}")
        print(f"  Chars per chunk: {stats['statistics']['avg_chars_per_chunk']:.0f}")
    
    print(f"\nLanguages: {stats['statistics']['languages']}")
    print(f"Doc types: {stats['statistics']['doc_types']}")
    print(f"Chunking methods: {stats['statistics']['chunking_methods']}")
    
    if stats["errors"]:
        print(f"\n⚠️  Errors encountered: {len(stats['errors'])}")
        for err in stats["errors"][:3]:
            print(f"  - {err['file']}: {err['error'][:50]}...")
    
    return stats

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Reindex PDFs with complete statistics")
    parser.add_argument("--pdf-dir", default="data/cinema_knowledge/01_ORIGINAIS_PDF",
                       help="Directory containing PDFs")
    parser.add_argument("--max-docs", type=int, default=10,
                       help="Maximum documents to index (default: 10)")
    parser.add_argument("--rebuild", action="store_true",
                       help="Clear collection before indexing")
    
    args = parser.parse_args()
    
    pdf_dir = Path(args.pdf_dir)
    if not pdf_dir.exists():
        print(f"Error: {pdf_dir} not found")
        
        # Try fallback
        fallback = Path("data/cinema_knowledge/01_ORIGINAIS_PDF")
        if fallback.exists():
            print(f"Using fallback: {fallback}")
            pdf_dir = fallback
        else:
            return 1
    
    # Run reindex
    stats = reindex_with_stats(pdf_dir, max_docs=args.max_docs, rebuild=args.rebuild)
    
    if stats:
        # Save report
        report_dir = Path("reports/fix_v3/v32_r3_corrections")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_path = report_dir / "phase_03_reindex_stats.json"
        with open(report_path, 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"\n📊 Report saved to: {report_path}")
        
        # Check success
        if stats["docs_indexed"] > 0 and stats["total_chunks"] > 100:
            print("\n✅ Reindex successful with statistics!")
            return 0
        else:
            print("\n⚠️  Reindex completed but with low numbers")
            return 1
    
    return 1

if __name__ == "__main__":
    sys.exit(main())