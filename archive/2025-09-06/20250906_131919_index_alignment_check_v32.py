#!/usr/bin/env python3
"""
V3.2 R2 — Index Alignment Check
Verifies alignment between RAG Adapter, Chroma, and schema
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def check_alignment():
    """Check complete index alignment."""
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "phase": "FASE_2_ALIGNMENT",
        "checks": {},
        "alignment": {
            "adapter_backend": None,
            "collection_match": False,
            "schema_match": False
        },
        "smoke_tests": [],
        "status": "checking"
    }
    
    print("🔍 V3.2 R2 Index Alignment Check\n")
    
    # Import after sys.path update
    from src.rag.adapter import RAGAdapter, SCHEMA_KEYS, COLLECTION_NAME, CHROMA_PATH
    
    # 1. Check constants
    print("1️⃣ Checking adapter constants...")
    print(f"   COLLECTION_NAME: {COLLECTION_NAME}")
    print(f"   CHROMA_PATH: {CHROMA_PATH}")
    print(f"   SCHEMA_KEYS: {SCHEMA_KEYS}")
    report["checks"]["constants"] = {
        "collection_name": COLLECTION_NAME,
        "chroma_path": CHROMA_PATH,
        "schema_keys": SCHEMA_KEYS
    }
    
    # 2. Check ChromaDB directly
    print("\n2️⃣ Checking ChromaDB...")
    try:
        import chromadb
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        
        # List collections
        collections = client.list_collections()
        collection_names = [c.name for c in collections]
        print(f"   Available collections: {collection_names}")
        
        # Check our collection
        if COLLECTION_NAME in collection_names:
            collection = client.get_collection(COLLECTION_NAME)
            count = collection.count()
            print(f"   ✅ Collection '{COLLECTION_NAME}': {count} documents")
            
            # Sample metadata to check schema
            if count > 0:
                sample = collection.get(limit=1)
                if sample and sample.get('metadatas'):
                    meta_keys = list(sample['metadatas'][0].keys())
                    print(f"   Metadata keys: {meta_keys}")
                    
                    # Check schema match
                    missing = set(SCHEMA_KEYS) - set(meta_keys)
                    extra = set(meta_keys) - set(SCHEMA_KEYS)
                    
                    if not missing:
                        print(f"   ✅ Schema complete")
                        report["alignment"]["schema_match"] = True
                    else:
                        print(f"   ⚠️ Missing keys: {missing}")
                    
                    if extra:
                        print(f"   ℹ️ Extra keys: {extra}")
                    
                    report["checks"]["chroma"] = {
                        "status": "ok",
                        "collection": COLLECTION_NAME,
                        "count": count,
                        "schema": meta_keys,
                        "missing_keys": list(missing),
                        "extra_keys": list(extra)
                    }
        else:
            print(f"   ❌ Collection '{COLLECTION_NAME}' not found")
            report["checks"]["chroma"] = {
                "status": "error",
                "error": f"Collection {COLLECTION_NAME} not found"
            }
            
    except Exception as e:
        print(f"   ❌ ChromaDB error: {e}")
        report["checks"]["chroma"] = {
            "status": "error",
            "error": str(e)
        }
    
    # 3. Check RAG Adapter
    print("\n3️⃣ Checking RAG Adapter...")
    try:
        from src.utils.config_loader import load_settings
        
        settings = load_settings()
        adapter = RAGAdapter(settings)
        
        print(f"   Provider: {adapter.provider}")
        print(f"   Enabled: {adapter.enabled}")
        
        # Check Chroma connection
        if adapter.chroma_client:
            print(f"   ✅ Chroma client connected")
            if adapter.chroma_collection:
                print(f"   ✅ Collection: {adapter.chroma_collection.name}")
                report["alignment"]["adapter_backend"] = "chroma"
                report["alignment"]["collection_match"] = (adapter.chroma_collection.name == COLLECTION_NAME)
            else:
                print(f"   ⚠️ No collection initialized")
        else:
            print(f"   ❌ Chroma client not connected")
            report["alignment"]["adapter_backend"] = "none"
        
        # Smoke tests
        print("\n4️⃣ Running smoke tests...")
        test_queries = [
            "screenplay structure",
            "character development arc",
            "dialogue subtext technique"
        ]
        
        for query in test_queries:
            print(f"   Testing: '{query}'")
            results = adapter.retrieve(query, k=3)
            
            if results:
                # Check backend
                backend = results[0].get('meta', {}).get('adapter_backend', 'unknown')
                collection = results[0].get('meta', {}).get('collection', 'unknown')
                
                print(f"     ✅ {len(results)} results (backend: {backend}, collection: {collection})")
                
                # Check citation
                citation = adapter.cite(results[0])
                print(f"     Citation: {citation}")
                
                report["smoke_tests"].append({
                    "query": query,
                    "num_results": len(results),
                    "backend": backend,
                    "collection": collection,
                    "sample_citation": citation
                })
            else:
                print(f"     ⚠️ No results")
                report["smoke_tests"].append({
                    "query": query,
                    "num_results": 0
                })
        
        report["checks"]["adapter"] = {
            "status": "ok",
            "provider": adapter.provider,
            "enabled": adapter.enabled,
            "has_chroma": adapter.chroma_client is not None
        }
        
    except Exception as e:
        print(f"   ❌ Adapter error: {e}")
        report["checks"]["adapter"] = {
            "status": "error",
            "error": str(e)
        }
    
    # 5. Final verdict
    print("\n" + "="*50)
    print("📊 ALIGNMENT SUMMARY\n")
    
    is_aligned = (
        report["alignment"]["adapter_backend"] == "chroma" and
        report["alignment"]["collection_match"] and
        report["alignment"]["schema_match"]
    )
    
    if is_aligned:
        print("✅ SYSTEM FULLY ALIGNED")
        report["status"] = "aligned"
    else:
        print("⚠️ ALIGNMENT ISSUES DETECTED:")
        if report["alignment"]["adapter_backend"] != "chroma":
            print(f"  - Adapter backend: {report['alignment']['adapter_backend']} (expected: chroma)")
        if not report["alignment"]["collection_match"]:
            print(f"  - Collection mismatch")
        if not report["alignment"]["schema_match"]:
            print(f"  - Schema incomplete")
        report["status"] = "misaligned"
    
    # Save report
    report_path = Path(__file__).parent.parent.parent / 'reports' / 'fix_v3' / 'v32_r2_bugfix_align' / 'index_alignment.json'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n📄 Report saved: {report_path}")
    
    return report

if __name__ == "__main__":
    check_alignment()