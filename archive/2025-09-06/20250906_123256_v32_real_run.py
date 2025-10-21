#!/usr/bin/env python3
"""
V3.2 Real Run - Testa sistemas com índice alinhado
"""
import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_telepathy():
    """Testa Redis real."""
    print("\n🔴 Testing Telepathy (Redis)...")
    results = {"status": "unknown", "tests": {}}
    
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        
        # Ping test
        ping_ok = r.ping()
        results["tests"]["ping"] = ping_ok
        print(f"  Ping: {'✅' if ping_ok else '❌'}")
        
        # Performance test
        start = time.time()
        for i in range(100):
            r.set(f"test_key_{i}", f"value_{i}")
            r.get(f"test_key_{i}")
        elapsed = (time.time() - start) * 1000
        avg_ms = elapsed / 200  # 100 sets + 100 gets
        
        results["tests"]["avg_latency_ms"] = round(avg_ms, 3)
        print(f"  Avg latency: {avg_ms:.3f}ms")
        
        # Cleanup
        for i in range(100):
            r.delete(f"test_key_{i}")
        
        results["status"] = "operational"
        
    except Exception as e:
        results["status"] = "failed"
        results["error"] = str(e)
        print(f"  ❌ Error: {e}")
    
    return results

def test_rag():
    """Testa RAG com ChromaDB."""
    print("\n📚 Testing RAG (ChromaDB)...")
    results = {"status": "unknown", "tests": {}}
    
    try:
        from src.rag.adapter import RAGAdapter
        from src.utils.config_loader import load_settings
        
        settings = load_settings()
        adapter = RAGAdapter(settings)
        
        # Check Chroma connection
        has_chroma = adapter.chroma_client is not None
        results["tests"]["chroma_connected"] = has_chroma
        print(f"  Chroma connected: {'✅' if has_chroma else '❌'}")
        
        if adapter.chroma_collection:
            count = adapter.chroma_collection.count()
            results["tests"]["document_count"] = count
            print(f"  Documents indexed: {count}")
        
        # Test queries
        test_queries = [
            "three act structure screenplay",
            "character development arc",
            "dialogue subtext technique"
        ]
        
        query_results = []
        for query in test_queries:
            start = time.time()
            docs = adapter.retrieve(query, k=5)
            elapsed = (time.time() - start) * 1000
            
            # Check if using Chroma
            using_chroma = any(d.get('method') == 'chroma' for d in docs)
            
            query_results.append({
                "query": query,
                "num_results": len(docs),
                "latency_ms": round(elapsed, 2),
                "using_chroma": using_chroma,
                "top_source": docs[0].get('source', 'Unknown') if docs else None
            })
            
            print(f"  Query '{query[:30]}...': {len(docs)} results in {elapsed:.2f}ms")
            if docs:
                print(f"    Top: {docs[0].get('source', 'Unknown')[:50]}")
        
        results["tests"]["queries"] = query_results
        results["status"] = "operational"
        
    except Exception as e:
        results["status"] = "failed"
        results["error"] = str(e)
        print(f"  ❌ Error: {e}")
    
    return results

def test_memory():
    """Testa Memory Manager."""
    print("\n🧠 Testing Memory Manager...")
    results = {"status": "unknown", "tests": {}}
    
    try:
        from src.memory.unified_manager import UnifiedMemoryManager
        from src.utils.config_loader import load_settings
        
        settings = load_settings()
        manager = UnifiedMemoryManager(settings)
        
        # Check components
        has_rag = manager.rag_adapter is not None
        has_dao = manager.dao is not None
        
        results["tests"]["has_rag_adapter"] = has_rag
        results["tests"]["has_dao"] = has_dao
        print(f"  RAG Adapter: {'✅' if has_rag else '❌'}")
        print(f"  DAO: {'✅' if has_dao else '❌'}")
        
        # Test get_context
        start = time.time()
        context = manager.get_context("screenplay format rules", max_chunks=10)
        elapsed = (time.time() - start) * 1000
        
        results["tests"]["get_context"] = {
            "num_chunks": len(context),
            "latency_ms": round(elapsed, 2),
            "sources": list(set(c.get('source', 'unknown') for c in context))[:5]
        }
        
        print(f"  get_context: {len(context)} chunks in {elapsed:.2f}ms")
        
        results["status"] = "operational"
        
    except Exception as e:
        results["status"] = "failed"
        results["error"] = str(e)
        print(f"  ❌ Error: {e}")
    
    return results

def test_performance():
    """Testa performance real."""
    print("\n⚡ Testing Performance...")
    results = {"status": "unknown", "tests": {}}
    
    try:
        from src.rag.adapter import RAGAdapter
        from src.utils.config_loader import load_settings
        
        settings = load_settings()
        adapter = RAGAdapter(settings)
        
        # RAG retrieve performance
        latencies = []
        for _ in range(10):
            start = time.time()
            adapter.retrieve("test query", k=8)
            latencies.append((time.time() - start) * 1000)
        
        avg_latency = sum(latencies) / len(latencies)
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]
        
        results["tests"]["rag_retrieve"] = {
            "avg_ms": round(avg_latency, 2),
            "p95_ms": round(p95_latency, 2),
            "samples": len(latencies),
            "backend": "chroma" if adapter.chroma_client else "stub"
        }
        
        print(f"  RAG Retrieve: avg={avg_latency:.2f}ms, p95={p95_latency:.2f}ms")
        
        # Check if within budget
        cold_budget = 1500  # ms
        warm_budget = 400   # ms
        
        within_budget = p95_latency < warm_budget
        results["tests"]["within_budget"] = within_budget
        print(f"  Within budget (<{warm_budget}ms): {'✅' if within_budget else '❌'}")
        
        results["status"] = "operational"
        
    except Exception as e:
        results["status"] = "failed"
        results["error"] = str(e)
        print(f"  ❌ Error: {e}")
    
    return results

def main():
    """Executa todos os testes."""
    print("=" * 60)
    print("🚀 V3.2 REAL RUN - Sistema com Índice Alinhado")
    print("=" * 60)
    
    report = {
        "validation": "V3.2 REAL RUN",
        "timestamp": datetime.now().isoformat(),
        "status": "started",
        "tests": {}
    }
    
    # Run tests
    report["tests"]["telepathy"] = test_telepathy()
    report["tests"]["rag"] = test_rag()
    report["tests"]["memory"] = test_memory()
    report["tests"]["performance"] = test_performance()
    
    # Summary
    all_operational = all(
        t.get("status") == "operational" 
        for t in report["tests"].values()
    )
    
    report["status"] = "completed"
    report["all_operational"] = all_operational
    
    # Save report
    report_path = Path(__file__).parent.parent.parent / "reports" / "fix_v3" / "v32_bugfix_indexalign" / "v32_real_run.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    for name, test in report["tests"].items():
        status_icon = "✅" if test["status"] == "operational" else "❌"
        print(f"{status_icon} {name.upper()}: {test['status']}")
    
    print(f"\n{'✅ ALL SYSTEMS OPERATIONAL' if all_operational else '⚠️ SOME SYSTEMS NEED ATTENTION'}")
    print(f"\n📄 Report saved: {report_path}")
    
    return 0 if all_operational else 1

if __name__ == "__main__":
    exit(main())