#!/usr/bin/env python3
"""
Performance tests with p95 and proper ms measurement
V3.2 R4.1 - Microfix version
"""
import sys
from pathlib import Path
import json
import time
from datetime import datetime
import statistics

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rag.adapter import RAGAdapter

def measure_operation(func, *args, **kwargs):
    """Measure operation time in milliseconds."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = (time.perf_counter() - start) * 1000  # Convert to ms once
    return elapsed, result

def calculate_p95(measurements):
    """Calculate 95th percentile from measurements."""
    if not measurements:
        return 0
    sorted_m = sorted(measurements)
    idx = int(len(sorted_m) * 0.95)
    if idx >= len(sorted_m):
        idx = len(sorted_m) - 1
    return sorted_m[idx]

def run_performance_tests():
    """Run cold and warm performance tests with p95."""
    
    print(f"\n{'='*60}")
    print(f"PERFORMANCE TESTS V3.2 R4.1 (with p95)")
    print(f"{'='*60}")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "backend": None,
        "collection": None,
        "series": {
            "cold": {},
            "warm": {}
        },
        "budgets": {
            "rag_retrieve_k8": {
                "cold": {"budget_ms": 1500, "within_budget": False},
                "warm": {"budget_ms": 400, "within_budget": False}
            },
            "pipeline_four_parts": {
                "budget_ms": 250,
                "within_budget": False
            }
        }
    }
    
    # Initialize adapter
    try:
        adapter = RAGAdapter({"rag": {"enabled": True, "provider": "chroma"}})
        results["backend"] = adapter.provider if hasattr(adapter, 'provider') else "unknown"
        if adapter.chroma_collection:
            results["collection"] = adapter.chroma_collection.name
        print(f"Backend: {results['backend']}")
        print(f"Collection: {results['collection']}")
    except Exception as e:
        print(f"❌ Failed to initialize adapter: {e}")
        return results
    
    # Test queries
    test_queries = [
        "screenplay three act structure",
        "character development techniques",
        "dialogue writing principles"
    ]
    
    # COLD SERIES (no warmup)
    print(f"\n{'='*40}")
    print("COLD SERIES (0 warmups + 3 measurements)")
    print(f"{'='*40}")
    
    cold_times = []
    for i, query in enumerate(test_queries):
        print(f"  Query {i+1}: '{query[:30]}...'")
        elapsed, _ = measure_operation(adapter.retrieve, query, k=8)
        cold_times.append(elapsed)
        print(f"    Time: {elapsed:.2f}ms")
    
    results["series"]["cold"] = {
        "measurements": cold_times,
        "avg_ms": statistics.mean(cold_times),
        "p95_ms": calculate_p95(cold_times),
        "max_ms": max(cold_times),
        "min_ms": min(cold_times)
    }
    
    print(f"\nCold avg: {results['series']['cold']['avg_ms']:.2f}ms")
    print(f"Cold p95: {results['series']['cold']['p95_ms']:.2f}ms")
    
    # WARM SERIES (with warmup)
    print(f"\n{'='*40}")
    print("WARM SERIES (3 warmups + 3 measurements)")
    print(f"{'='*40}")
    
    # Warmup
    print("  Warming up...")
    for query in test_queries:
        _ = adapter.retrieve(query, k=8)
    
    # Measurements
    warm_times = []
    for i, query in enumerate(test_queries):
        print(f"  Query {i+1}: '{query[:30]}...'")
        elapsed, _ = measure_operation(adapter.retrieve, query, k=8)
        warm_times.append(elapsed)
        print(f"    Time: {elapsed:.2f}ms")
    
    results["series"]["warm"] = {
        "measurements": warm_times,
        "avg_ms": statistics.mean(warm_times),
        "p95_ms": calculate_p95(warm_times),
        "max_ms": max(warm_times),
        "min_ms": min(warm_times)
    }
    
    print(f"\nWarm avg: {results['series']['warm']['avg_ms']:.2f}ms")
    print(f"Warm p95: {results['series']['warm']['p95_ms']:.2f}ms")
    
    # PIPELINE TEST (simulated 4-part pipeline)
    print(f"\n{'='*40}")
    print("PIPELINE TEST (4 parts)")
    print(f"{'='*40}")
    
    pipeline_times = []
    for i in range(5):  # Run 5 times for better p95
        start = time.perf_counter()
        
        # Part 1: Query expansion (simulated)
        time.sleep(0.001)
        
        # Part 2: Retrieve
        _ = adapter.retrieve("test query", k=4)
        
        # Part 3: Rerank (simulated)
        time.sleep(0.001)
        
        # Part 4: Format (simulated)
        time.sleep(0.001)
        
        elapsed = (time.perf_counter() - start) * 1000  # Convert to ms
        pipeline_times.append(elapsed)
        print(f"  Run {i+1}: {elapsed:.2f}ms")
    
    results["series"]["pipeline"] = {
        "measurements": pipeline_times,
        "avg_ms": statistics.mean(pipeline_times),
        "p95_ms": calculate_p95(pipeline_times),
        "max_ms": max(pipeline_times),
        "min_ms": min(pipeline_times)
    }
    
    print(f"\nPipeline avg: {results['series']['pipeline']['avg_ms']:.2f}ms")
    print(f"Pipeline p95: {results['series']['pipeline']['p95_ms']:.2f}ms")
    
    # Check budgets
    results["budgets"]["rag_retrieve_k8"]["cold"]["within_budget"] = \
        results["series"]["cold"]["avg_ms"] < results["budgets"]["rag_retrieve_k8"]["cold"]["budget_ms"]
    results["budgets"]["rag_retrieve_k8"]["cold"]["p95_within_budget"] = \
        results["series"]["cold"]["p95_ms"] < results["budgets"]["rag_retrieve_k8"]["cold"]["budget_ms"]
    
    results["budgets"]["rag_retrieve_k8"]["warm"]["within_budget"] = \
        results["series"]["warm"]["avg_ms"] < results["budgets"]["rag_retrieve_k8"]["warm"]["budget_ms"]
    results["budgets"]["rag_retrieve_k8"]["warm"]["p95_within_budget"] = \
        results["series"]["warm"]["p95_ms"] < results["budgets"]["rag_retrieve_k8"]["warm"]["budget_ms"]
    
    results["budgets"]["pipeline_four_parts"]["within_budget"] = \
        results["series"]["pipeline"]["avg_ms"] < results["budgets"]["pipeline_four_parts"]["budget_ms"]
    results["budgets"]["pipeline_four_parts"]["p95_within_budget"] = \
        results["series"]["pipeline"]["p95_ms"] < results["budgets"]["pipeline_four_parts"]["budget_ms"]
    
    # Summary
    print(f"\n{'='*60}")
    print(f"BUDGET CHECK")
    print(f"{'='*60}")
    
    print(f"RAG Retrieve k=8:")
    print(f"  Cold avg: {results['series']['cold']['avg_ms']:.2f}ms < {results['budgets']['rag_retrieve_k8']['cold']['budget_ms']}ms = {results['budgets']['rag_retrieve_k8']['cold']['within_budget']}")
    print(f"  Cold p95: {results['series']['cold']['p95_ms']:.2f}ms < {results['budgets']['rag_retrieve_k8']['cold']['budget_ms']}ms = {results['budgets']['rag_retrieve_k8']['cold']['p95_within_budget']}")
    print(f"  Warm avg: {results['series']['warm']['avg_ms']:.2f}ms < {results['budgets']['rag_retrieve_k8']['warm']['budget_ms']}ms = {results['budgets']['rag_retrieve_k8']['warm']['within_budget']}")
    print(f"  Warm p95: {results['series']['warm']['p95_ms']:.2f}ms < {results['budgets']['rag_retrieve_k8']['warm']['budget_ms']}ms = {results['budgets']['rag_retrieve_k8']['warm']['p95_within_budget']}")
    
    print(f"\nPipeline 4-parts:")
    print(f"  Avg: {results['series']['pipeline']['avg_ms']:.2f}ms < {results['budgets']['pipeline_four_parts']['budget_ms']}ms = {results['budgets']['pipeline_four_parts']['within_budget']}")
    print(f"  P95: {results['series']['pipeline']['p95_ms']:.2f}ms < {results['budgets']['pipeline_four_parts']['budget_ms']}ms = {results['budgets']['pipeline_four_parts']['p95_within_budget']}")
    
    return results

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Performance tests with p95")
    parser.add_argument("--out", default="reports/fix_v3/v32_r4_1_microfix/perf_summary.json",
                       help="Output file path")
    
    args = parser.parse_args()
    
    results = run_performance_tests()
    
    # Save reports
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Also save phase report
    phase_report = {
        "phase": "PHASE_B",
        "timestamp": results["timestamp"],
        "status": "completed",
        "backend": results["backend"],
        "collection": results["collection"],
        "performance": {
            "cold": {
                "avg_ms": results["series"]["cold"]["avg_ms"],
                "p95_ms": results["series"]["cold"]["p95_ms"]
            },
            "warm": {
                "avg_ms": results["series"]["warm"]["avg_ms"],
                "p95_ms": results["series"]["warm"]["p95_ms"]
            },
            "pipeline": {
                "avg_ms": results["series"]["pipeline"]["avg_ms"],
                "p95_ms": results["series"]["pipeline"]["p95_ms"]
            }
        },
        "budgets": results["budgets"],
        "deviation": [],
        "resistance": [],
        "reason": ["Performance measured with p95 percentiles"]
    }
    
    phase_path = out_path.parent / "phase_B_perf.json"
    with open(phase_path, 'w') as f:
        json.dump(phase_report, f, indent=2)
    
    print(f"\n📊 Reports saved to:")
    print(f"  - {out_path}")
    print(f"  - {phase_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())