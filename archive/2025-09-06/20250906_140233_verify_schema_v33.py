#!/usr/bin/env python3
"""
Verify and validate schema alignment across components
"""
import sys
from pathlib import Path
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rag.adapter import RAGAdapter, SCHEMA_KEYS, COLLECTION_NAME

def verify_schema_alignment():
    """Verify schema is properly aligned across all components."""
    
    print(f"\n{'='*60}")
    print(f"SCHEMA ALIGNMENT VERIFICATION")
    print(f"{'='*60}")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "schema_keys": SCHEMA_KEYS,
        "collection_name": COLLECTION_NAME,
        "checks": {}
    }
    
    # Check 1: Schema definition
    print(f"\n1. Schema Definition:")
    print(f"   Required keys: {SCHEMA_KEYS}")
    print(f"   Collection: {COLLECTION_NAME}")
    results["checks"]["schema_defined"] = len(SCHEMA_KEYS) == 8
    
    # Check 2: Adapter initialization
    print(f"\n2. Adapter Initialization:")
    try:
        adapter = RAGAdapter({"rag": {"enabled": True, "provider": "chroma"}})
        if adapter.chroma_collection:
            print(f"   ✅ ChromaDB connected")
            print(f"   Collection: {adapter.chroma_collection.name}")
            print(f"   Documents: {adapter.chroma_collection.count()}")
            results["checks"]["chroma_connected"] = True
        else:
            print(f"   ❌ ChromaDB not connected")
            results["checks"]["chroma_connected"] = False
    except Exception as e:
        print(f"   ❌ Failed to initialize: {e}")
        results["checks"]["chroma_connected"] = False
        adapter = None
    
    # Check 3: Test document addition with all fields
    print(f"\n3. Test Document Addition:")
    if adapter and adapter.chroma_collection:
        test_doc = {
            "source": "test_doc.pdf",
            "path": "/path/to/test_doc.pdf",
            "doc_hash": "abc123def456",
            "mtime": int(datetime.now().timestamp()),
            "chunk_no": 0,
            "total_chunks": 1,
            "type": "screenplay",
            "lang": "en"
        }
        
        success = adapter.add_document(
            text="Test content for schema validation",
            metadata=test_doc
        )
        
        if success:
            print(f"   ✅ Document added with all fields")
            results["checks"]["add_with_schema"] = True
            
            # Verify it was stored correctly
            doc_id = f"{test_doc['doc_hash']}#c{test_doc['chunk_no']}"
            try:
                result = adapter.chroma_collection.get(ids=[doc_id])
                if result and result['metadatas']:
                    stored_meta = result['metadatas'][0]
                    print(f"   ✅ Metadata stored correctly")
                    
                    # Check all fields
                    for key in SCHEMA_KEYS:
                        if key in stored_meta:
                            print(f"      - {key}: ✓")
                        else:
                            print(f"      - {key}: ✗ MISSING")
                    
                    results["checks"]["all_fields_stored"] = all(
                        key in stored_meta for key in SCHEMA_KEYS
                    )
                else:
                    print(f"   ❌ Could not retrieve stored document")
                    results["checks"]["all_fields_stored"] = False
                    
                # Clean up test document
                adapter.chroma_collection.delete(ids=[doc_id])
                
            except Exception as e:
                print(f"   ❌ Error verifying storage: {e}")
                results["checks"]["all_fields_stored"] = False
        else:
            print(f"   ❌ Failed to add document")
            results["checks"]["add_with_schema"] = False
    else:
        print(f"   ⚠️  Skipped (no adapter)")
        results["checks"]["add_with_schema"] = False
        results["checks"]["all_fields_stored"] = False
    
    # Check 4: Citation format
    print(f"\n4. Citation Format:")
    if adapter:
        test_snippet = {
            "source": "data/pdfs/Casablanca.pdf",
            "meta": {
                "chunk_no": 42,
                "total_chunks": 148,
                "page": 37
            }
        }
        
        citation = adapter.cite(test_snippet)
        print(f"   Input: {test_snippet}")
        print(f"   Citation: {citation}")
        
        # Verify format includes chunk info
        has_chunk_info = "c42/148" in citation or "42/148" in citation
        has_page_info = "p.37" in citation or "page 37" in citation
        
        if has_chunk_info:
            print(f"   ✅ Chunk info included")
        else:
            print(f"   ❌ Chunk info missing")
            
        if has_page_info:
            print(f"   ✅ Page info included")
        else:
            print(f"   ⚠️  Page info missing (optional)")
        
        results["checks"]["citation_format"] = has_chunk_info
    else:
        print(f"   ⚠️  Skipped (no adapter)")
        results["checks"]["citation_format"] = False
    
    # Check 5: Retrieve with metadata
    print(f"\n5. Retrieve with Metadata:")
    if adapter and adapter.chroma_collection and adapter.chroma_collection.count() > 0:
        try:
            results_list = adapter.retrieve("test query", k=3)
            if results_list:
                print(f"   Retrieved {len(results_list)} results")
                
                # Check first result has all metadata
                first = results_list[0]
                meta = first.get('metadata', {})
                
                print(f"   Checking first result metadata:")
                for key in SCHEMA_KEYS:
                    if key in meta:
                        print(f"      - {key}: ✓")
                    else:
                        print(f"      - {key}: ✗ MISSING")
                
                results["checks"]["retrieve_has_metadata"] = all(
                    key in meta for key in SCHEMA_KEYS
                )
            else:
                print(f"   ⚠️  No results returned")
                results["checks"]["retrieve_has_metadata"] = False
        except Exception as e:
            print(f"   ❌ Retrieve failed: {e}")
            results["checks"]["retrieve_has_metadata"] = False
    else:
        print(f"   ⚠️  Skipped (no documents)")
        results["checks"]["retrieve_has_metadata"] = False
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for v in results["checks"].values() if v)
    total = len(results["checks"])
    
    print(f"Checks passed: {passed}/{total}")
    
    for check, passed in results["checks"].items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")
    
    # Overall status
    if passed == total:
        print(f"\n✅ SCHEMA FULLY ALIGNED!")
        results["status"] = "aligned"
    elif passed >= total - 1:
        print(f"\n⚠️  SCHEMA MOSTLY ALIGNED (minor issues)")
        results["status"] = "mostly_aligned"
    else:
        print(f"\n❌ SCHEMA NOT ALIGNED!")
        results["status"] = "not_aligned"
    
    return results

def main():
    results = verify_schema_alignment()
    
    # Save report
    report_dir = Path("reports/fix_v3/v32_r3_corrections")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / "phase_02_schema_alignment.json"
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📊 Report saved to: {report_path}")
    
    return 0 if results["status"] == "aligned" else 1

if __name__ == "__main__":
    sys.exit(main())