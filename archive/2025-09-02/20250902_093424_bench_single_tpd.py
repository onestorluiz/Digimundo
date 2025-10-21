#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bench mini para um token_dict específico, com limites anti-timeout.
Salva CSV distinto por tpd+dataset e imprime redução média.
"""
from __future__ import annotations
from pathlib import Path
import argparse, subprocess, shutil, sys
import pandas as pd

def run(cmd:list, timeout_s:int=180)->bool:
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout_s)
        return True
    except Exception:
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tpd_path", required=True, help="ex.: data/tpd/sweep_big/K3000-3000/token_dict.json")
    ap.add_argument("--data_dir", default="data/screenplay_synth", choices=["data/screenplay_synth","data/original"])
    ap.add_argument("--max_files", type=int, default=12)
    ap.add_argument("--max_chars", type=int, default=60000)
    args = ap.parse_args()

    tpd = Path(args.tpd_path).resolve()
    if not tpd.exists():
        print("[ERR] tpd not found:", tpd); sys.exit(2)

    cmd = [
        "./.venv/bin/python","scripts/run_compression_bench.py",
        "--data_dir", args.data_dir,
        "--tpd_path", str(tpd),
        "--max_files", str(args.max_files),
        "--max_chars", str(args.max_chars),
        "--preserve_headers","false",
        "--ablation","canon+tpd",
    ]
    ok = run(cmd, timeout_s=180)
    bench_csv = Path("results/compression/benchmark.csv")
    out_csv = Path("results/compression")/f"bench_{tpd.parent.name}_{Path(args.data_dir).name}_mini.csv"
    if bench_csv.exists():
        try: shutil.move(str(bench_csv), str(out_csv))
        except Exception: pass

    if out_csv.exists():
        try:
            df = pd.read_csv(out_csv)
            if "reduction" in df.columns:
                print(f"[OK] {out_csv.name} reduction_mean={df['reduction'].mean():.4f}")
                sys.exit(0)
        except Exception:
            pass
    print("[WARN] no results"); sys.exit(1)

if __name__ == "__main__":
    main()