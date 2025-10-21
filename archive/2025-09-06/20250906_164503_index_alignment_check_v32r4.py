#!/usr/bin/env python3
"""
Index alignment check with complete field verification
V3.2 R4 - Final version
"""
import sys
from pathlib import Path
import json
from datetime import datetime
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rag.adapter import RAGAdapter, SCHEMA_KEYS, COLLECTION_NAME

def check_index_alignment():
    """Check complete index alignment with all required fields."""
    
    print(f"\n{'='*60}")
    print(f"INDEX ALIGNMENT CHECK V3.2 R4")
    print(f"{'='*60}")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "adapter_backend": None,
        "collection_adapter": None,
        "collection_tooling": None,
        "schema_ok": False,
        "smoke_queries": [],
        "status": "checking",
        "notes": []
    }
    
    # Initialize adapter
    try:
        adapter = RAGAdapter({"rag": {"enabled": True, "provider": "chroma"}})
        
        # Get backend and collection info
        results["adapter_backend"] = adapter.provider if hasattr(adapter, 'provider') else "unknown"
        
        if adapter.chroma_collection:
            results["collection_adapter"] = adapter.chroma_collection.name
            doc_count = adapter.chroma_collection.count()
            print(f"Adapter backend: {results['adapter_backend']}")
            print(f"Collection: {results['collection_adapter']} ({doc_count} docs)")
        else:
            results["notes"].append("ChromaDB collection not initialized")
            
    except Exception as e:
        results["notes"].append(f"Adapter initialization failed: {str(e)}")
        results["status"] = "misaligned"
        return results
    
    # Check collection from environment/tooling
    results["collection_tooling"] = os.environ.get("RAG_COLLECTION", COLLECTION_NAME)
    print(f"Tooling collection: {results['collection_tooling']}")
    
    # Run smoke queries
    test_queries = [
        "screenplay structure",
        "character development arc", 
        "dialogue subtext technique"
    ]
    
    print(f"\n{'='*40}")
    print("SMOKE QUERIES")
    print(f"{'='*40}")
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        try:
            results_list = adapter.retrieve(query, k=3)
            
            query_result = {
                "query": query,
                "results_count": len(results_list),
                "has_metadata": False,
                "schema_fields_present": []
            }
            
            if results_list and len(results_list) > 0:
                # Check first result for schema
                first = results_list[0]
                # Check both 'metadata' and 'meta' keys
                meta = first.get('metadata') or first.get('meta', {})
                
                # Check which schema fields are present
                for key in SCHEMA_KEYS:
                    if key in meta:
                        query_result["schema_fields_present"].append(key)
                
                query_result["has_metadata"] = len(query_result["schema_fields_present"]) > 0
                
                print(f"  Results: {len(results_list)}")
                print(f"  Metadata fields: {len(query_result['schema_fields_present'])}/{len(SCHEMA_KEYS)}")
                
                # Show sample if good
                if len(query_result["schema_fields_present"]) == len(SCHEMA_KEYS):
                    print(f"  ✅ All schema fields present")
                else:
                    missing = set(SCHEMA_KEYS) - set(query_result["schema_fields_present"])
                    print(f"  ⚠️  Missing fields: {missing}")
            else:
                print(f"  No results returned")
                
            results["smoke_queries"].append(query_result)
            
        except Exception as e:
            print(f"  ❌ Query failed: {e}")
            results["smoke_queries"].append({
                "query": query,
                "error": str(e)
            })
    
    # Check schema completeness
    schema_complete_count = 0
    for sq in results["smoke_queries"]:
        if "schema_fields_present" in sq:
            if len(sq["schema_fields_present"]) == len(SCHEMA_KEYS):
                schema_complete_count += 1
    
    results["schema_ok"] = (schema_complete_count > 0)
    
    # Determine final status
    print(f"\n{'='*40}")
    print("ALIGNMENT STATUS")
    print(f"{'='*40}")
    
    backend_ok = results["adapter_backend"] == "chroma"
    collections_match = results["collection_adapter"] == results["collection_tooling"]
    
    print(f"Backend is chroma: {backend_ok}")
    print(f"Collections match: {collections_match}")
    print(f"Schema OK: {results['schema_ok']}")
    
    if backend_ok and collections_match and results["schema_ok"]:
        results["status"] = "aligned"
        print(f"\n✅ ALIGNED")
    else:
        results["status"] = "misaligned"
        if not backend_ok:
            results["notes"].append(f"Backend is {results['adapter_backend']}, expected chroma")
        if not collections_match:
            results["notes"].append(f"Collection mismatch: adapter={results['collection_adapter']}, tooling={results['collection_tooling']}")
        if not results["schema_ok"]:
            results["notes"].append("Schema incomplete in query results")
        print(f"\n❌ MISALIGNED")
        for note in results["notes"]:
            print(f"  - {note}")
    
    return results

def main():
    results = check_index_alignment()
    
    # Save reports
    report_dir = Path("reports/fix_v3/v32_r4_final")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to both locations as specified
    report_path1 = report_dir / "index_alignment.json"
    with open(report_path1, 'w') as f:
        json.dump(results, f, indent=2)
    
    report_path2 = report_dir / "phase_B_alignment.json"
    with open(report_path2, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Reports saved to:")
    print(f"  - {report_path1}")
    print(f"  - {report_path2}")
    
    return 0 if results["status"] == "aligned" else 1

if __name__ == "__main__":
    sys.exit(main())