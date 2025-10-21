#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sweep de configurações TPD stacked maiores para encontrar ótimos (C1/C2).
Presets: quick (3 configs), extended (7 configs), max (5 configs com até 5000+2000).
"""
from pathlib import Path
import subprocess, shutil, json, time, argparse, sys
import pandas as pd

ROOT = Path(__file__).parent.parent
RESULTS = ROOT/"results/compression"
DATASETS = [("screenplay", "data/screenplay_synth"), ("original", "data/original")]
TPD_DIR_DEFAULT = ROOT/"data/tpd/sweep_big"

def run(cmd:list, timeout_s:int|None=None):
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout_s)
        return True
    except Exception:
        return False

def combos_for(preset:str, tb:float):
    if preset=="extended":
        return [
            {"layers":"3000,3000","nmin":2,"nmax":10,"fmin":2,"time_budget_s":tb},
            {"layers":"3500,2500","nmin":2,"nmax":10,"fmin":2,"time_budget_s":tb},
            {"layers":"4000,2000","nmin":2,"nmax":10,"fmin":2,"time_budget_s":tb},
            {"layers":"3000,2000","nmin":2,"nmax":10,"fmin":2,"time_budget_s":tb},
            {"layers":"2500,2500","nmin":2,"nmax":10,"fmin":2,"time_budget_s":tb},
            {"layers":"4500,1500","nmin":2,"nmax":10,"fmin":2,"time_budget_s":tb},
            {"layers":"2000,4000","nmin":2,"nmax":10,"fmin":2,"time_budget_s":tb},
        ]
    if preset=="max":
        return [
            {"layers":"4000,3000","nmin":2,"nmax":12,"fmin":2,"time_budget_s":tb},
            {"layers":"3500,3500","nmin":2,"nmax":12,"fmin":2,"time_budget_s":tb},
            {"layers":"5000,2000","nmin":2,"nmax":12,"fmin":2,"time_budget_s":tb},
            {"layers":"4500,2500","nmin":2,"nmax":12,"fmin":2,"time_budget_s":tb},
            {"layers":"3000,4000","nmin":2,"nmax":12,"fmin":2,"time_budget_s":tb},
        ]
    # quick (default)
    return [
        {"layers":"3000,3000","nmin":2,"nmax":10,"fmin":2,"time_budget_s":tb},
        {"layers":"3500,2500","nmin":2,"nmax":10,"fmin":2,"time_budget_s":tb},
        {"layers":"4000,2000","nmin":2,"nmax":10,"fmin":2,"time_budget_s":tb},
    ]

def build_combo(cfg:dict, sweep_dir:Path) -> Path|None:
    """Constrói TPD stacked com a config; retorna path do token_dict.json ou None."""
    sweep_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "./.venv/bin/python","scripts/build_tpd_stacked.py",
        "--corpus","data/screenplay_synth","--outdir",str(sweep_dir),
        "--layers",cfg["layers"],
        "--nmin",str(cfg["nmin"]), "--nmax",str(cfg["nmax"]),
        "--fmin",str(cfg["fmin"]), "--time_budget_s",str(cfg["time_budget_s"])
    ]
    # se já existir, não falhe — apenas devolva o path
    cands_exist = sorted(sweep_dir.glob(f"K{cfg['layers'].replace(',','-')}*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if cands_exist:
        d=cands_exist[0]
        if (d/"token_dict.json").exists():
            return d/"token_dict.json"
    ok = run(cmd, timeout_s=int(cfg.get("time_budget_s",60))+60)
    if not ok:
        # tente localizar mesmo assim (pode ter sido criado)
        cands = sorted(sweep_dir.glob(f"K{cfg['layers'].replace(',','-')}*"), key=lambda p: p.stat().st_mtime, reverse=True)
        for d in cands:
            if (d/"token_dict.json").exists():
                return d/"token_dict.json"
        return None
    # encontra diretório recém-criado (por timestamp)
    cands = sorted(sweep_dir.glob(f"K{cfg['layers'].replace(',','-')}*"), key=lambda p: p.stat().st_mtime, reverse=True)
    for d in cands:
        if (d/"token_dict.json").exists():
            return d/"token_dict.json"
    return None

def bench_token_dict(tpd_path:Path, max_files:int=25, max_chars:int=120000):
    rows=[]
    for label, ddir in DATASETS:
        cmd = [
            "./.venv/bin/python","scripts/run_compression_bench.py",
            "--data_dir", ddir,
            "--tpd_path", str(tpd_path),
            "--max_files", str(max_files),
            "--max_chars", str(max_chars),
            "--preserve_headers", "false",
            "--ablation", "canon+tpd"
        ]
        ok = run(cmd, timeout_s=600)
        if not ok:
            print(f"[WARN] bench fail for {tpd_path} on {label}", file=sys.stderr)
        bench_csv = RESULTS/"benchmark.csv"
        out_csv = RESULTS/f"bench_{tpd_path.parent.name}_{label}.csv"
        if bench_csv.exists():
            try:
                shutil.move(str(bench_csv), str(out_csv))
                df = pd.read_csv(out_csv)
                df["dataset"] = label
                df["tpd"] = tpd_path.parent.name
                rows += df.to_dict("records")
            except Exception:
                pass
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", choices=["quick","extended","max"], default="quick")
    ap.add_argument("--time_budget_s", type=float, default=60.0)
    ap.add_argument("--sweep_dir", default=str(TPD_DIR_DEFAULT))
    ap.add_argument("--max_files", type=int, default=25)
    ap.add_argument("--max_chars", type=int, default=120000)
    ap.add_argument("--layers-only", default="", help="ex.: 3000,3000 (processa somente este combo)")
    ap.add_argument("--mode", choices=["both","build","bench"], default="both")
    args = ap.parse_args()
    COMBOS = combos_for(args.preset, args.time_budget_s)
    if args.layers_only:
        COMBOS = [dict(layers=args.layers_only, nmin=2, nmax=10, fmin=2, time_budget_s=args.time_budget_s)]
    sweep_dir = Path(args.sweep_dir)
    all_rows=[]
    for cfg in COMBOS:
        tpd = None
        if args.mode in ("build","both"):
            tpd = build_combo(cfg, sweep_dir)
        if args.mode in ("bench","both"):
            if tpd is None:
                # tenta localizar existente
                cands = sorted(sweep_dir.glob(f"K{cfg['layers'].replace(',','-')}*"))
                for d in cands:
                    if (d/"token_dict.json").exists():
                        tpd = d/"token_dict.json"; break
        if tpd:
            all_rows += bench_token_dict(tpd, max_files=args.max_files, max_chars=args.max_chars)
    
    if not all_rows:
        print("[WARN] nenhum resultado")
        return
    
    # Agregação
    df = pd.DataFrame(all_rows)
    
    # Médias por config
    agg = df.groupby(["dataset","tpd"], dropna=False).agg(
        digilang_ratio_mean=("digilang_ratio", "mean"),
        window_multiplier_mean=("window_multiplier", "mean"),
        n_files=("file", "count")
    ).reset_index()
    
    # Média geral por TPD
    overall = df.groupby("tpd").agg(
        digilang_ratio_mean=("digilang_ratio", "mean"),
        window_multiplier_mean=("window_multiplier", "mean")
    ).reset_index()
    overall = overall.sort_values("digilang_ratio_mean", ascending=False)
    
    # Salvar resumo
    out = Path("reports"); out.mkdir(parents=True, exist_ok=True)
    agg.to_csv(out/"summary_sweep_big.csv", index=False)
    
    # Melhor config
    if len(overall) > 0:
        best = overall.iloc[0]
        best_cfg = {
            "tpd": best["tpd"],
            "digilang_ratio_mean": best["digilang_ratio_mean"],
            "window_multiplier_mean": best["window_multiplier_mean"]
        }
        with (out/"best_configs_big.json").open("w", encoding="utf-8") as f:
            json.dump(best_cfg, f, indent=2)
        
        # Copiar melhor TPD para default
        src = (sweep_dir/best["tpd"]/"token_dict.json")
        dst = ROOT/"data/tpd/default/token_dict.json"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"[OK] default token_dict -> {dst} ({best['tpd']})")
    
    print(f"[OK] sweep ({args.preset}) -> reports/summary_sweep_big.csv | reports/best_configs_big.json")

if __name__ == "__main__":
    main()