#!/usr/bin/env python3
"""
V3.2 R4.2 - Generate cite() smoke samples
Collects 6 snippets via adapter.retrieve() and generates citation strings.
"""
import sys
import json
from pathlib import Path
from datetime import datetime
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def generate_cite_samples():
    """Generate 6 cite samples from RAG results."""
    
    print(f"\n{'='*60}")
    print(f"CITE SMOKE TEST - 6 SAMPLES")
    print(f"{'='*60}")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "num_samples": 0,
        "samples": [],
        "source_unknown_count": 0,
        "missing_meta_fields": []
    }
    
    # Import and initialize adapter
    try:
        from src.rag.adapter import RAGAdapter
        adapter = RAGAdapter({'rag': {'enabled': True, 'provider': 'chroma'}})
        
        if not adapter.chroma_collection:
            print("❌ ChromaDB not available")
            results["error"] = "ChromaDB not available"
            return results
            
        print(f"Collection: {adapter.chroma_collection.name}")
        print(f"Documents: {adapter.chroma_collection.count()}")
        
    except Exception as e:
        print(f"❌ Adapter init failed: {e}")
        results["error"] = str(e)
        return results
    
    # Test queries for variety
    test_queries = [
        "three act structure screenplay",
        "character development arc",
        "dialogue subtext technique",
        "visual storytelling cinema",
        "plot twist revelation",
        "emotional journey protagonist"
    ]
    
    print(f"\nGenerating citations...")
    
    for i, query in enumerate(test_queries):
        print(f"\n{i+1}. Query: '{query}'")
        
        try:
            # Retrieve top result
            docs = adapter.retrieve(query, k=1)
            
            if not docs:
                print("   No results")
                continue
                
            doc = docs[0]
            
            # Extract metadata
            meta = doc.get('metadata') or doc.get('meta', {})
            text_snippet = doc.get('text', '')[:100] + "..."
            
            # Build citation
            source = meta.get('source', 'unknown')
            path = meta.get('path', '')
            chunk_no = meta.get('chunk_no', 0)
            total_chunks = meta.get('total_chunks', 1)
            
            # Extract basename from path or source
            if path and path != 'unknown':
                basename = os.path.basename(path)
                if basename.endswith('.pdf'):
                    basename = basename[:-4]  # Remove .pdf
            elif source != 'unknown':
                basename = source
                if basename.endswith('.pdf'):
                    basename = basename[:-4]
            else:
                basename = "source:unknown"
                results["source_unknown_count"] += 1
            
            # Check for missing metadata
            missing = []
            if 'source' not in meta:
                missing.append('source')
            if 'path' not in meta:
                missing.append('path')
            if 'chunk_no' not in meta:
                missing.append('chunk_no')
            if 'total_chunks' not in meta:
                missing.append('total_chunks')
            
            if missing:
                for field in missing:
                    if field not in results["missing_meta_fields"]:
                        results["missing_meta_fields"].append(field)
            
            # Generate citation string
            # Note: page number not available in metadata, would need PDF processing
            citation = f"{basename}.pdf · c{chunk_no}/{total_chunks}"
            
            sample = {
                "query": query,
                "citation": citation,
                "text_preview": text_snippet,
                "metadata_present": list(meta.keys()),
                "missing_fields": missing
            }
            
            results["samples"].append(sample)
            results["num_samples"] += 1
            
            print(f"   Citation: {citation}")
            if missing:
                print(f"   Missing: {missing}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
    
    # Calculate statistics
    total = results["num_samples"]
    unknown = results["source_unknown_count"]
    
    if total > 0:
        results["source_unknown_percent"] = round((unknown / total) * 100, 1)
    else:
        results["source_unknown_percent"] = 0
    
    return results

def main():
    results = generate_cite_samples()
    
    # Save report
    report_dir = Path("reports/fix_v3/v32_r4_2_microfinal")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / "cite_samples.json"
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Report saved to: {report_path}")
    
    # Summary
    print(f"\n{'='*40}")
    print("CITE SUMMARY")
    print(f"{'='*40}")
    print(f"Samples generated: {results['num_samples']}/6")
    print(f"Source unknown: {results['source_unknown_count']} ({results['source_unknown_percent']}%)")
    
    if results.get("missing_meta_fields"):
        print(f"Missing fields seen: {results['missing_meta_fields']}")
    
    # Acceptance check
    acceptable = (
        results["num_samples"] == 6 and
        results["source_unknown_count"] <= 2
    )
    
    if acceptable:
        print("✅ ACCEPTABLE")
    else:
        print("⚠️ PARTIAL SUCCESS")
    
    return 0 if acceptable else 1

if __name__ == "__main__":
    sys.exit(main())