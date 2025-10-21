import time, json, random
from ..retrieval.hybrid import HybridRetriever

def benchmark_search(n: int = 20):
    retr = HybridRetriever()
    queries = [
        "incidente incitante em Chinatown",
        "padrões de midpoint em roteiros clássicos",
        "técnicas de não linearidade do Tarantino",
        "como construir um clímax com reversão"
    ]
    t0 = time.time()
    for i in range(n):
        q = random.choice(queries)
        retr.search(q)
    elapsed = time.time() - t0
    print(json.dumps({"queries": n, "total_seconds": elapsed, "avg_ms": 1000*elapsed/n}, indent=2))

if __name__ == "__main__":
    benchmark_search()
