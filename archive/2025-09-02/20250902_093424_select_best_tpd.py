#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import json, shutil
import pandas as pd

ROOT = Path(".")
RESULTS = ROOT/"results/compression"
SWEEP_DIRS = [ROOT/"data/tpd/sweep_big", ROOT/"data/tpd/stacked"]

def main():
    rows=[]
    for p in RESULTS.glob("bench_K*_{original,screenplay,screenplay_synth}_*.csv"):
        pass  # brace doesn't work — keep simple loop below

    for p in RESULTS.glob("bench_K*_*_mini.csv"):
        parts = p.name.split("_")
        # bench_K3000-3000_screenplay_synth_mini.csv => tpd=K3000-3000 dataset=screenplay_synth
        tpd = parts[1]
        dataset = parts[2]
        try:
            df = pd.read_csv(p)
            if "reduction" in df.columns:
                rows.append({"tpd": tpd, "dataset": dataset, "avg_reduction": float(df["reduction"].mean())})
        except Exception:
            continue

    for p in RESULTS.glob("bench_K*_*.csv"):
        # também considera CSVs não-mini
        try:
            name = p.name
            tpd = name.split("_")[1]
            dataset = name.split("_")[2].split(".")[0]
            df = pd.read_csv(p)
            if "reduction" in df.columns:
                rows.append({"tpd": tpd, "dataset": dataset, "avg_reduction": float(df["reduction"].mean())})
        except Exception:
            continue

    if not rows:
        print("[WARN] no bench csvs found in results/compression"); return

    df = pd.DataFrame(rows)
    # média por tpd e por dataset
    by_tpd = df.groupby("tpd")["avg_reduction"].mean().sort_values(ascending=False)
    best_tpd = by_tpd.index[0]
    best_val = float(by_tpd.iloc[0])

    # localizar arquivo físico desse tpd
    src = None
    for d in SWEEP_DIRS:
        cand = d/best_tpd/"token_dict.json"
        if cand.exists():
            src = cand; break
    if src is None:
        print("[WARN] cannot locate token_dict for", best_tpd); return

    dst = ROOT/"data/tpd/default/token_dict.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    (ROOT/"reports").mkdir(exist_ok=True, parents=True)
    (ROOT/"reports/best_tpd.json").write_text(json.dumps({"best_tpd":best_tpd,"avg_reduction":best_val}, indent=2), encoding="utf-8")
    print(f"[OK] default token_dict <- {src}  (mean_reduction={best_val:.4f})")

if __name__=="__main__":
    main()