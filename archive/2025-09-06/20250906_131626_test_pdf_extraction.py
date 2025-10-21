#!/usr/bin/env python3
"""Test PDF extraction and chunking"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.pdf_utils import extract_text, get_pdf_metadata
from src.rag.chunking import smart_chunk

def test_extraction():
    pdf_dir = Path("data/cinema_knowledge/01_ORIGINAIS_PDF")
    
    # Test 3 representative PDFs
    test_pdfs = [
        "Chinatown - Screenplay.pdf",
        "The Godfather - Screenplay.pdf",
        "Inception - Screenplay.pdf"
    ]
    
    results = []
    for pdf_name in test_pdfs:
        pdf_path = pdf_dir / pdf_name
        if not pdf_path.exists():
            print(f"❌ {pdf_name} not found")
            continue
        
        print(f"\n📄 Testing: {pdf_name}")
        
        # Extract text
        text = extract_text(pdf_path)
        print(f"  Extracted: {len(text)} chars")
        
        # Get metadata
        meta = get_pdf_metadata(pdf_path)
        print(f"  Pages: {meta['pages']}")
        
        # Chunk text
        chunks = smart_chunk(text, chunk_size=1000, overlap=120)
        print(f"  Chunks: {len(chunks)} (method: {chunks[0]['method'] if chunks else 'none'})")
        
        # Show sample
        if text and len(text) > 100:
            sample = text[:200].replace('\n', ' ')
            print(f"  Sample: {sample}...")
        
        results.append({
            "pdf": pdf_name,
            "chars": len(text),
            "pages": meta['pages'],
            "chunks": len(chunks),
            "avg_chunk_size": sum(len(c['text']) for c in chunks) / len(chunks) if chunks else 0
        })
    
    print("\n📊 Summary:")
    total_chunks = sum(r['chunks'] for r in results)
    avg_chunks = total_chunks / len(results) if results else 0
    print(f"  Average chunks per PDF: {avg_chunks:.1f}")
    print(f"  Total chunks from {len(results)} PDFs: {total_chunks}")
    
    return results

if __name__ == "__main__":
    test_extraction()