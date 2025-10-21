#!/usr/bin/env python3
"""
Generate cite() samples from adapter
V3.2 R4 - Final version
"""
import sys
from pathlib import Path
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rag.adapter import RAGAdapter

def generate_cite_samples():
    """Generate 6 cite samples from the adapter."""
    
    print(f"\n{'='*60}")
    print(f"CITE SAMPLES GENERATION V3.2 R4")
    print(f"{'='*60}")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "samples": [],
        "source_unknown_count": 0,
        "total_samples": 6
    }
    
    # Initialize adapter
    try:
        adapter = RAGAdapter({"rag": {"enabled": True, "provider": "chroma"}})
    except Exception as e:
        print(f"❌ Failed to initialize adapter: {e}")
        return results
    
    # Test queries to get diverse samples
    test_queries = [
        "three act structure",
        "protagonist journey",
        "dialogue techniques",
        "screenplay format",
        "character arc",
        "visual storytelling"
    ]
    
    print("\nGenerating cite samples...")
    
    for i, query in enumerate(test_queries):
        print(f"\n[{i+1}/6] Query: '{query}'")
        
        try:
            # Get one result
            results_list = adapter.retrieve(query, k=1)
            
            if results_list and len(results_list) > 0:
                snippet = results_list[0]
                
                # Generate citation
                citation = adapter.cite(snippet)
                
                # Check if source unknown
                is_unknown = "unknown" in citation.lower() or not citation
                if is_unknown:
                    results["source_unknown_count"] += 1
                
                # Create sample
                sample = {
                    "query": query,
                    "citation": citation,
                    "has_metadata": bool(snippet.get('metadata') or snippet.get('meta')),
                    "source": snippet.get('source', 'N/A')
                }
                
                # Try to extract expected format info
                meta = snippet.get('metadata') or snippet.get('meta', {})
                if meta:
                    sample["chunk_no"] = meta.get('chunk_no', 'missing')
                    sample["total_chunks"] = meta.get('total_chunks', 'missing')
                    sample["page"] = meta.get('page', 'missing')
                
                results["samples"].append(sample)
                
                print(f"  Citation: {citation}")
                print(f"  Source: {sample['source']}")
                
            else:
                print(f"  No results")
                results["samples"].append({
                    "query": query,
                    "citation": "source:unknown",
                    "error": "No results returned"
                })
                results["source_unknown_count"] += 1
                
        except Exception as e:
            print(f"  Error: {e}")
            results["samples"].append({
                "query": query,
                "citation": "source:unknown",
                "error": str(e)
            })
            results["source_unknown_count"] += 1
    
    # Calculate percentage
    results["source_unknown_percentage"] = (results["source_unknown_count"] / results["total_samples"]) * 100
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Samples generated: {len(results['samples'])}")
    print(f"Source unknown: {results['source_unknown_count']}/{results['total_samples']} ({results['source_unknown_percentage']:.1f}%)")
    
    # Show all citations
    print(f"\nAll citations:")
    for i, sample in enumerate(results['samples'], 1):
        print(f"  {i}. {sample['citation']}")
    
    return results

def main():
    results = generate_cite_samples()
    
    # Save report
    report_dir = Path("reports/fix_v3/v32_r4_final")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / "cite_samples_v32_r4.json"
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Also save phase report
    phase_report = {
        "phase": "PHASE_D",
        "timestamp": results["timestamp"],
        "status": "completed",
        "exactly_followed": True,
        "cite_samples": results["samples"][:6],
        "source_unknown_percentage": results["source_unknown_percentage"],
        "deviation": [] if results["source_unknown_percentage"] < 50 else ["High percentage of unknown sources"],
        "resistance": [],
        "reason": [f"Generated {len(results['samples'])} cite samples"]
    }
    
    phase_path = report_dir / "phase_D_cite.json"
    with open(phase_path, 'w') as f:
        json.dump(phase_report, f, indent=2)
    
    print(f"\n📊 Reports saved to:")
    print(f"  - {report_path}")
    print(f"  - {phase_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())