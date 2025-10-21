#!/usr/bin/env python3
"""
Test PDF extraction and chunking with detailed statistics
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

def compute_file_hash(file_path: Path) -> str:
    """Compute hash of file content."""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]

def test_extraction_with_stats(pdf_dir: Path, max_docs: int = 5):
    """Test extraction and chunking with detailed statistics."""
    
    pdf_files = sorted(pdf_dir.glob("*.pdf"))[:max_docs]
    
    if not pdf_files:
        print(f"No PDFs found in {pdf_dir}")
        return None
    
    print(f"\n{'='*60}")
    print(f"Testing PDF extraction with {len(pdf_files)} documents")
    print(f"{'='*60}")
    
    stats = {
        "timestamp": datetime.now().isoformat(),
        "pdf_dir": str(pdf_dir),
        "docs_tested": len(pdf_files),
        "total_chars": 0,
        "total_chunks": 0,
        "avg_chars_per_doc": 0,
        "avg_chunks_per_doc": 0,
        "documents": []
    }
    
    for pdf_path in pdf_files:
        print(f"\n📄 Processing: {pdf_path.name}")
        print(f"   Size: {pdf_path.stat().st_size / 1024:.1f} KB")
        
        # Extract metadata
        metadata = get_pdf_metadata(pdf_path)
        print(f"   Pages: {metadata['pages']}")
        
        # Extract text
        text = extract_text(pdf_path)
        char_count = len(text)
        print(f"   Extracted: {char_count:,} characters")
        
        # Check if stub
        is_stub = text.startswith("[PDF Content:")
        if is_stub:
            print(f"   ⚠️  WARNING: Stub content detected!")
        
        # Chunk text
        chunks = smart_chunk(text, chunk_size=1000, overlap=120)
        chunk_count = len(chunks)
        print(f"   Chunks: {chunk_count}")
        
        # Analyze chunking method
        methods = set(c["method"] for c in chunks)
        print(f"   Method: {', '.join(methods)}")
        
        # Sample chunks info
        if chunks:
            avg_chunk_size = sum(len(c["text"]) for c in chunks) / len(chunks)
            print(f"   Avg chunk size: {avg_chunk_size:.0f} chars")
            
            # Show sections if section-based
            if "section" in methods:
                sections = [c["section"] for c in chunks if c["section"]]
                unique_sections = list(dict.fromkeys(sections))[:5]  # First 5 unique
                print(f"   Sections: {', '.join(unique_sections[:3])}")
                if len(unique_sections) > 3:
                    print(f"            ... and {len(set(sections)) - 3} more")
        
        # Compute hash
        doc_hash = compute_file_hash(pdf_path)
        
        # Add to stats
        doc_stats = {
            "name": pdf_path.name,
            "path": str(pdf_path),
            "hash": doc_hash,
            "size_kb": pdf_path.stat().st_size / 1024,
            "pages": metadata["pages"],
            "chars_extracted": char_count,
            "is_stub": is_stub,
            "chunks": chunk_count,
            "chunking_method": list(methods),
            "avg_chunk_size": sum(len(c["text"]) for c in chunks) / len(chunks) if chunks else 0
        }
        
        # Add sample chunk IDs
        if chunks:
            doc_stats["sample_chunk_ids"] = [
                f"{doc_hash}#c{i}" for i in range(min(3, len(chunks)))
            ]
        
        stats["documents"].append(doc_stats)
        stats["total_chars"] += char_count
        stats["total_chunks"] += chunk_count
    
    # Calculate averages
    if stats["docs_tested"] > 0:
        stats["avg_chars_per_doc"] = stats["total_chars"] / stats["docs_tested"]
        stats["avg_chunks_per_doc"] = stats["total_chunks"] / stats["docs_tested"]
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Documents tested: {stats['docs_tested']}")
    print(f"Total characters: {stats['total_chars']:,}")
    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Avg chars/doc: {stats['avg_chars_per_doc']:,.0f}")
    print(f"Avg chunks/doc: {stats['avg_chunks_per_doc']:.1f}")
    
    # Check for issues
    issues = []
    for doc in stats["documents"]:
        if doc["is_stub"]:
            issues.append(f"- {doc['name']}: Stub content detected")
        if doc["chunks"] < 10 and doc["chars_extracted"] > 10000:
            issues.append(f"- {doc['name']}: Too few chunks for text size")
        if doc["chunks"] == 0:
            issues.append(f"- {doc['name']}: No chunks generated")
    
    if issues:
        print(f"\n⚠️  ISSUES FOUND:")
        for issue in issues:
            print(issue)
    else:
        print(f"\n✅ All documents processed successfully")
    
    return stats

def main():
    # Test with PDFs
    pdf_dir = Path("data/cinema_knowledge/01_ORIGINAIS_PDF")
    
    if not pdf_dir.exists():
        print(f"Error: {pdf_dir} not found")
        return 1
    
    # Run test
    stats = test_extraction_with_stats(pdf_dir, max_docs=5)
    
    if stats:
        # Save report
        report_dir = Path("reports/fix_v3/v32_r3_corrections")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_path = report_dir / "phase_01_extraction_stats.json"
        with open(report_path, 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"\n📊 Report saved to: {report_path}")
        
        # Check if extraction is working properly
        if stats["avg_chunks_per_doc"] < 50:
            print("\n⚠️  WARNING: Average chunks per doc is low. Check extraction!")
            return 1
        
        print("\n✅ Extraction and chunking working properly!")
        return 0
    
    return 1

if __name__ == "__main__":
    sys.exit(main())