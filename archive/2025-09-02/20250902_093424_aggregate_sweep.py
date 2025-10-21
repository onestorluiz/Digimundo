#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Varre token_dicts em data/tpd/K*_n*/token_dict.json,
roda benchmark em data/original e data/screenplay_synth,
seleciona melhor por dataset e overall, atualiza default e salva sumários.
Enxuto para evitar OOM em ambiente de edição.
"""
import csv, os, subprocess, json, shutil
from pathlib import Path
import pandas as pd

TPD_ROOT = Path("data/tpd")
RESULTS_DIR = Path("results/compression")
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = [("original","data/original"), ("screenplay","data/screenplay_synth")]

def run_bench(tpd_json: Path, data_dir: str):
    out_csv = RESULTS_DIR / f"bench_{tpd_json.parent.name}_{'screenplay' if 'screenplay' in data_dir else 'original'}.csv"
    cmd = ["./.venv/bin/python","scripts/run_compression_bench.py","--data_dir",data_dir,"--tpd_path",str(tpd_json)]
    subprocess.run(cmd, check=True)
    bench_csv = RESULTS_DIR / "benchmark.csv"
    if bench_csv.exists():
        shutil.move(str(bench_csv), str(out_csv))
    return out_csv if out_csv.exists() else None

def avg_reduction(csv_path: Path) -> float:
    try:
        df = pd.read_csv(csv_path)
        if "reduction" in df.columns:
            return float(df["reduction"].mean())
    except Exception:
        pass
    return -1.0

def main():
    cands = list(TPD_ROOT.glob("K*_n*/token_dict.json"))
    if not cands:
        print("[WARN] no TPD candidates found in data/tpd/K*_n*/token_dict.json"); return
    if not Path("data/screenplay_synth").exists():
        subprocess.run(["./.venv/bin/python","scripts/build_screenplay_synthetic.py"], check=True)

    rows=[]
    for t in cands:
        for label, ddir in DATASETS:
            out = run_bench(t, ddir)
            rows.append({"tpd": t.parent.name, "dataset": label, "avg_reduction": avg_reduction(out) if out else -1})

    # best per dataset
    best={}
    for ds in {r["dataset"] for r in rows}:
        subset=[r for r in rows if r["dataset"]==ds and r["avg_reduction"]>=0]
        if subset:
            best[ds]=max(subset, key=lambda r: r["avg_reduction"])

    # overall by mean of available datasets
    overall={}
    agg={}
    for r in rows:
        if r["avg_reduction"]<0: continue
        agg.setdefault(r["tpd"], []).append(r["avg_reduction"])
    if agg:
        name, vals = max(agg.items(), key=lambda kv: sum(kv[1])/len(kv[1]))
        overall={"tpd":name, "avg_reduction": sum(vals)/len(vals)}

    # set default
    if overall:
        src = TPD_ROOT/overall["tpd"]/ "token_dict.json"
        dst = TPD_ROOT/"default"; dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst/"token_dict.json")
        print(f"[OK] default updated -> {dst}/token_dict.json")

    # save summaries
    df=pd.DataFrame(rows)
    df.to_csv(REPORTS_DIR/"summary_sweep.csv", index=False)
    with open(REPORTS_DIR/"best_configs.json","w",encoding="utf-8") as f:
        json.dump({"per_dataset":best,"overall":overall}, f, indent=2)
    print("[OK] summaries -> reports/summary_sweep.csv & reports/best_configs.json")

if __name__=="__main__":
    main()