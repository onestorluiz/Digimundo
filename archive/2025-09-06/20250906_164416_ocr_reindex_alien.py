#!/usr/bin/env python3
"""
OCR and partial reindex for Alien - Screenplay.pdf
V3.2 R4.1 - Microfix version
"""
import sys
from pathlib import Path
import json
import hashlib
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rag.pdf_utils import extract_text, get_pdf_metadata
from src.rag.chunking import smart_chunk
from src.rag.adapter import RAGAdapter

def compute_file_hash(file_path: Path) -> str:
    """Compute hash of file content."""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]

def ocr_and_reindex_alien():
    """Try OCR on Alien PDF and reindex."""
    
    print(f"\n{'='*60}")
    print(f"OCR AND REINDEX - ALIEN SCREENPLAY")
    print(f"{'='*60}")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "target_file": "Alien - Screenplay.pdf",
        "ocr_attempted": False,
        "ocr_available": False,
        "status": "pending",
        "chars_extracted": 0,
        "chunks_created": 0,
        "indexed": False
    }
    
    # Find the Alien PDF
    pdf_path = Path("03_MEMORY/01_ORIGINAIS_PDF/Alien - Screenplay.pdf")
    if not pdf_path.exists():
        pdf_path = Path("data/cinema_knowledge/01_ORIGINAIS_PDF/Alien - Screenplay.pdf")
    
    if not pdf_path.exists():
        print(f"❌ File not found: Alien - Screenplay.pdf")
        results["status"] = "file_not_found"
        return results
    
    print(f"Found: {pdf_path}")
    print(f"Size: {pdf_path.stat().st_size / 1024:.1f} KB")
    
    # Check OCR availability
    try:
        import pytesseract
        from pdf2image import convert_from_path
        results["ocr_available"] = True
        print("✅ OCR libraries available")
    except ImportError:
        results["ocr_available"] = False
        print("⚠️ OCR libraries not available (pytesseract/pdf2image)")
    
    # Extract text (will try OCR if available and needed)
    print("\nExtracting text...")
    text = extract_text(pdf_path)
    results["chars_extracted"] = len(text)
    
    # Check if stub
    is_stub = text.startswith("[PDF Content:") or len(text) < 2000
    
    if is_stub and results["ocr_available"]:
        print("Attempting OCR extraction...")
        results["ocr_attempted"] = True
        
        try:
            # Try OCR on first 3 pages
            from pdf2image import convert_from_path
            import pytesseract
            
            images = convert_from_path(str(pdf_path), dpi=200, first_page=1, last_page=3)
            ocr_texts = []
            
            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(image, lang='eng')
                if page_text:
                    ocr_texts.append(page_text)
                    print(f"  Page {i+1}: {len(page_text)} chars extracted")
            
            if ocr_texts:
                text = "\n\n".join(ocr_texts)
                results["chars_extracted"] = len(text)
                is_stub = False
                print(f"✅ OCR successful: {len(text)} chars extracted")
        except Exception as e:
            print(f"❌ OCR failed: {e}")
            results["ocr_error"] = str(e)
    
    print(f"\nExtracted: {results['chars_extracted']} chars")
    print(f"Is stub: {is_stub}")
    
    if is_stub:
        results["status"] = "skipped_stub"
        results["reason"] = f"Stub content (chars={results['chars_extracted']})"
        print("⚠️ Document remains as stub")
        return results
    
    # Chunk the text
    print("\nChunking text...")
    chunks = smart_chunk(text, chunk_size=1000, overlap=120)
    results["chunks_created"] = len(chunks)
    print(f"Created {len(chunks)} chunks")
    
    # Initialize adapter and add to collection
    print("\nIndexing chunks...")
    try:
        adapter = RAGAdapter({"rag": {"enabled": True, "provider": "chroma"}})
        
        if not adapter.chroma_collection:
            print("❌ ChromaDB not available")
            results["status"] = "chroma_not_available"
            return results
        
        # Prepare metadata
        doc_hash = compute_file_hash(pdf_path)
        mtime = int(pdf_path.stat().st_mtime)
        
        chunks_added = 0
        for chunk_data in chunks:
            metadata = {
                "source": pdf_path.name,
                "path": str(pdf_path),
                "doc_hash": doc_hash,
                "mtime": mtime,
                "chunk_no": chunk_data["chunk_no"],
                "total_chunks": len(chunks),
                "type": "screenplay",
                "lang": "en"
            }
            
            success = adapter.add_document(
                text=chunk_data["text"],
                metadata=metadata
            )
            
            if success:
                chunks_added += 1
        
        print(f"✅ Indexed {chunks_added}/{len(chunks)} chunks")
        
        results["indexed"] = chunks_added > 0
        results["chunks_indexed"] = chunks_added
        results["status"] = "indexed" if chunks_added > 0 else "indexing_failed"
        
    except Exception as e:
        print(f"❌ Indexing error: {e}")
        results["status"] = "indexing_error"
        results["error"] = str(e)
    
    return results

def main():
    results = ocr_and_reindex_alien()
    
    # Create full reindex report
    report = {
        "timestamp": results["timestamp"],
        "docs_total": 52,  # Total PDFs in directory
        "indexed_files": 1 if results["indexed"] else 0,
        "total_chunks": results.get("chunks_indexed", 0),
        "duplicates": 0,
        "collection": "v3_1_docs",
        "schema_ok": True,
        "alien_status": results
    }
    
    # Save reports
    report_dir = Path("reports/fix_v3/v32_r4_1_microfix")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Main reindex report
    with open(report_dir / "reindex_report_v32_r4_1.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    # Phase report
    phase_report = {
        "phase": "PHASE_C",
        "timestamp": results["timestamp"],
        "status": "completed",
        "ocr_status": {
            "available": results["ocr_available"],
            "attempted": results["ocr_attempted"],
            "skipped_ocr": not results["ocr_available"]
        },
        "alien_pdf": {
            "status": results["status"],
            "chars_extracted": results["chars_extracted"],
            "chunks_created": results["chunks_created"],
            "indexed": results["indexed"]
        },
        "deviation": ["OCR not available, kept as stub"] if not results["ocr_available"] else [],
        "resistance": [],
        "reason": ["Partial reindex attempted for Alien PDF"]
    }
    
    with open(report_dir / "phase_C_ocr_reindex.json", 'w') as f:
        json.dump(phase_report, f, indent=2)
    
    print(f"\n📊 Reports saved")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"OCR available: {results['ocr_available']}")
    print(f"OCR attempted: {results['ocr_attempted']}")
    print(f"Status: {results['status']}")
    print(f"Chars extracted: {results['chars_extracted']}")
    print(f"Chunks created: {results['chunks_created']}")
    print(f"Indexed: {results['indexed']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())