# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import csv, json, math, glob

CAND_LAT = ["latency_ms","p95_ms","latency","duration_ms","duration","elapsed_ms"]
CAND_RPS = ["msgs_per_s","throughput_rps","rps","qps"]

def _read_csv_nums(path:Path)->tuple[list[float],list[float]]:
    lat, rps = [], []
    try:
        with path.open("r", encoding="utf-8") as f:
            rd = csv.DictReader(f)
            for row in rd:
                # latência
                vlat = None
                for k in CAND_LAT:
                    if k in row and row[k]:
                        try: vlat = float(row[k]); break
                        except: pass
                if vlat is not None and math.isfinite(vlat):
                    lat.append(vlat)
                # throughput
                vrps = None
                for k in CAND_RPS:
                    if k in row and row[k]:
                        try: vrps = float(row[k]); break
                        except: pass
                if vrps is None and vlat not in (None, 0):
                    try: vrps = 1000.0/float(vlat)  # 1/ms -> aprox rps
                    except: vrps = None
                if vrps is not None and math.isfinite(vrps):
                    rps.append(vrps)
    except Exception:
        pass
    return lat, rps

def rollup()->dict:
    lat_all, rps_all = [], []
    for p in glob.glob("results/telepathy/*.csv")+glob.glob("results/e2e/*.csv"):
        l,r = _read_csv_nums(Path(p))
        lat_all += l; rps_all += r
    return {"latency_ms": lat_all[-500:], "throughput_rps": rps_all[-500:]}

def main():
    out = Path("reports/history/perf.json"); out.parent.mkdir(parents=True, exist_ok=True)
    data = rollup()
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[OK] perf json -> {out}")

if __name__=="__main__": main()