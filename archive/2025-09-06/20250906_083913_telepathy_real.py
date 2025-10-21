#!/usr/bin/env python3
"""
V3.1 DELTA — Healthcheck em Redis REAL (se disponível).

Uso:
  REDIS_URL=redis://localhost:6379/0 python tools/fix_v3/telepathy_real.py --out reports/fix_v3/telepathy_real.json
"""
import argparse, json, os, time
from pathlib import Path

def measure(fn, rounds=5):
    times = []
    for _ in range(rounds):
        t0 = time.perf_counter()
        fn()
        times.append((time.perf_counter()-t0)*1000)
    return {
        "rounds": rounds,
        "avg_ms": round(sum(times)/len(times), 3),
        "all_ms": [round(x,3) for x in times]
    }

def run(out_path: Path):
    out = {"mode": "redis", "ok": False}
    url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    try:
        import redis  # type: ignore
        r = redis.Redis.from_url(url, socket_connect_timeout=0.5, socket_timeout=0.5)
        pong = r.ping()
        out["ping"] = bool(pong)
        # set/get microbench
        out["set_ms"] = measure(lambda: r.set("v3_1_probe", "1"))
        out["get_ms"] = measure(lambda: r.get("v3_1_probe"))
        out["ok"] = True
    except Exception as e:
        out["error"] = str(e)
        out["ok"] = False
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[telepathy_real] gravado: {out_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="reports/fix_v3/telepathy_real.json")
    args = ap.parse_args()
    run(Path(args.out))