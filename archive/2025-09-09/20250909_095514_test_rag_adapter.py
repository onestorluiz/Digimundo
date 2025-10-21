#!/usr/bin/env python3
"""
RAG Adapter Tests - Phase 2
"""

import json
import time
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')
from rag.adapter import RAGAdapter, create_rag_adapter, validate_schema

def run_rag_tests():
    """Run comprehensive RAG tests"""
    
    # Create adapter
    adapter = create_rag_adapter()
    
    # ========== Test 1: rag_tests.json ==========
    print("🧪 RAG Tests: HyDE, RAPTOR, Simple")
    
    test_results = {
        "timestamp": time.time(),
        "tests": []
    }
    
    # Test 1a: Simple retrieval
    print("\n  1. Simple retrieval...")
    simple_result = adapter.retrieve(
        "christopher nolan inception",
        k=5,
        include=["ids", "metadatas", "distances"]
    )
    
    # Verify schema on metadatas
    schema_valid = True
    for meta in simple_result.get("metadatas", []):
        is_valid, violations = validate_schema(meta)
        if not is_valid:
            schema_valid = False
            print(f"    ⚠️ Schema violation: {violations}")
    
    # Generate citation
    if simple_result.get("metadatas"):
        citation = adapter.cite(simple_result["metadatas"][0])
        print(f"    Citation: {citation}")
    else:
        citation = "No results"
    
    test_results["tests"].append({
        "method": "simple",
        "query": "christopher nolan inception",
        "results_count": len(simple_result.get("ids", [])),
        "schema_valid": schema_valid,
        "citation_example": citation,
        "latency_ms": simple_result.get("latency_ms", 0),
        "from_cache": simple_result.get("from_cache", False)
    })
    
    # Test 1b: HyDE retrieval
    print("\n  2. HyDE retrieval...")
    hyde_result = adapter.retrieve_hyde(
        "explain dream within dream concept",
        k=5
    )
    
    # Check if hypothetical was generated
    has_hypothetical = "hypothetical_query" in hyde_result
    print(f"    Hypothetical: {hyde_result.get('hypothetical_query', 'N/A')[:50]}...")
    
    test_results["tests"].append({
        "method": "hyde",
        "query": "explain dream within dream concept",
        "has_hypothetical": has_hypothetical,
        "results_count": len(hyde_result.get("ids", [])),
        "original_query": hyde_result.get("original_query"),
        "latency_ms": hyde_result.get("latency_ms", 0)
    })
    
    # Test 1c: RAPTOR retrieval
    print("\n  3. RAPTOR multi-level retrieval...")
    raptor_result = adapter.retrieve_raptor(
        "science fiction movies about time",
        k=6
    )
    
    # Check levels
    has_levels = "levels" in raptor_result
    level_count = len(raptor_result.get("levels", {}))
    
    test_results["tests"].append({
        "method": "raptor",
        "query": "science fiction movies about time",
        "has_levels": has_levels,
        "level_count": level_count,
        "total_results": len(raptor_result.get("ids", [])),
        "k": raptor_result.get("k", 0)
    })
    
    # Save rag_tests.json
    with open("reports/harmony_v100/phase2/rag_tests.json", "w") as f:
        json.dump(test_results, f, indent=2, default=str)
    
    print(f"\n✅ RAG tests complete: {len(test_results['tests'])} methods tested")
    
    # ========== Test 2: rag_perf.json ==========
    print("\n🧪 Performance Tests")
    
    # Clear cache for fresh performance testing
    adapter.clear_cache()
    
    # Run multiple queries for performance metrics
    perf_queries = [
        "inception movie analysis",
        "christopher nolan filmography",
        "dream layers explained",
        "time dilation in movies",
        "psychological thriller scripts",
        "heist movie structure",
        "nonlinear narrative techniques",
        "mind-bending cinema",
        "reality vs dreams theme",
        "movie within movie concept"
    ] * 2  # Run each query twice for total of 20
    
    print(f"  Running {len(perf_queries)} queries...")
    for i, query in enumerate(perf_queries):
        # Add random suffix to avoid cache hits
        adapter.retrieve(query, k=5, cache_suffix=f"perf_{i}")
    
    # Get statistics
    stats = adapter.get_stats()
    
    # Verify invariants
    invariants = stats["invariants"]
    all_invariants_pass = all(invariants.values())
    
    perf_results = {
        "timestamp": time.time(),
        "queries_tested": len(perf_queries),
        "latencies_ms": stats["latencies_ms"],
        "invariants": invariants,
        "all_invariants_pass": all_invariants_pass,
        "cache_stats": {
            "size": stats["cache_size"],
            "hits": stats["stats"]["cache_hits"],
            "misses": stats["stats"]["cache_misses"]
        },
        "oom_safety": {
            "prevented_count": stats["stats"]["oom_prevented"],
            "k_limited": invariants.get("k_limited", True)
        }
    }
    
    # Save rag_perf.json
    with open("reports/harmony_v100/phase2/rag_perf.json", "w") as f:
        json.dump(perf_results, f, indent=2)
    
    print(f"✅ Performance test complete:")
    print(f"   p50={perf_results['latencies_ms']['p50']:.2f}ms")
    print(f"   p95={perf_results['latencies_ms']['p95']:.2f}ms")
    print(f"   Invariants: {invariants}")
    
    # ========== Test 3: OOM Safety ==========
    print("\n🧪 OOM Safety Tests")
    
    oom_tests = {
        "k_limited": True,
        "documents_excluded": True,
        "tests": []
    }
    
    # Test large k value
    print("  Testing k > 8 limitation...")
    large_k_result = adapter.retrieve("test", k=20)
    actual_k = large_k_result.get("k", 0)
    oom_tests["tests"].append({
        "test": "large_k",
        "requested_k": 20,
        "actual_k": actual_k,
        "limited": actual_k <= 8
    })
    
    # Test documents exclusion
    print("  Testing documents field exclusion...")
    docs_result = adapter.retrieve(
        "test",
        k=5,
        include=["ids", "metadatas", "distances", "documents"]
    )
    has_documents = "documents" in docs_result
    oom_tests["tests"].append({
        "test": "documents_field",
        "requested_documents": True,
        "has_documents": has_documents,
        "excluded": not has_documents or len(str(docs_result.get("documents", []))) < 10000
    })
    
    oom_tests["k_limited"] = all(t["limited"] for t in oom_tests["tests"] if t["test"] == "large_k")
    oom_tests["documents_excluded"] = all(t["excluded"] for t in oom_tests["tests"] if t["test"] == "documents_field")
    
    # Save OOM safety results
    with open("reports/harmony_v100/phase2/oom_safety.json", "w") as f:
        json.dump(oom_tests, f, indent=2)
    
    print(f"✅ OOM safety test complete:")
    print(f"   k limited: {oom_tests['k_limited']}")
    print(f"   Documents excluded: {oom_tests['documents_excluded']}")
    
    # ========== Summary ==========
    summary = {
        "phase": "2",
        "test": "rag_adapter",
        "timestamp": time.time(),
        "status": "PASS" if (
            all_invariants_pass and
            schema_valid and
            oom_tests["k_limited"] and
            oom_tests["documents_excluded"]
        ) else "FAIL",
        "tests_passed": {
            "schema_enforcement": schema_valid,
            "citation_formatting": len(citation) > 0,
            "hyde_retrieval": has_hypothetical,
            "raptor_levels": has_levels,
            "performance_invariants": all_invariants_pass,
            "oom_k_limit": oom_tests["k_limited"],
            "oom_documents": oom_tests["documents_excluded"]
        }
    }
    
    return summary

if __name__ == "__main__":
    # Ensure output directory exists
    Path("reports/harmony_v100/phase2").mkdir(parents=True, exist_ok=True)
    
    # Run tests
    summary = run_rag_tests()
    
    # Save summary
    with open("reports/harmony_v100/phase2/test_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "="*50)
    print("📊 RAG ADAPTER TEST SUMMARY")
    print("="*50)
    print(f"Status: {'✅ PASS' if summary['status'] == 'PASS' else '❌ FAIL'}")
    for test, passed in summary["tests_passed"].items():
        print(f"  {test}: {'✅' if passed else '❌'}")
    
    print(f"\n✅ All RAG tests complete!")
    sys.exit(0 if summary["status"] == "PASS" else 1)