#!/usr/bin/env python
import sys
sys.path.append('.')
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

Path("reports/figures").mkdir(parents=True, exist_ok=True)
dfs=[]
for p in Path("results/compression").glob("*.csv"):
    try:
        dfs.append(pd.read_csv(p).assign(source=p.name))
    except: pass
if not dfs:
    print("[WARN] no CSVs"); exit(0)
df=pd.concat(dfs, ignore_index=True)

# Scorecard simples por modo
summary=(df.groupby("mode")
           .agg(avg_reduction=("reduction","mean"),
                p95_latency=("latency_ms",lambda x: x.quantile(0.95) if len(x) > 0 else None))
           .reset_index())
summary.to_csv("reports/summary.csv", index=False)
print(summary)

# Histograma
for mode, d in df.groupby("mode"):
    plt.figure()
    d["reduction"].hist(bins=20)
    plt.title(f"Reduction distribution — {mode}")
    plt.xlabel("reduction"); plt.ylabel("count")
    plt.savefig(f"reports/figures/reduction_{mode}.png")
    plt.close()

print("[OK] plots -> reports/figures & reports/summary.csv")