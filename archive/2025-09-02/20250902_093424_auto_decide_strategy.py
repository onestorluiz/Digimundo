#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
import json, os, re, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(".")
COMP = ROOT/"results/compression"
REPORTS = ROOT/"reports"

CANDIDATE_FILES = [
    ("grid_adaptive_acts.csv",      "grid+acts"),
    ("grid_adaptive.csv",           "grid"),
    ("benchmark_overlay_by_act.csv","overlay_by_act"),
    ("benchmark_overlay_ner.csv",   "overlay_ner"),
    ("benchmark_overlay_adaptive.csv","overlay_adaptive"),
    ("benchmark_overlay.csv",       "overlay"),
    ("benchmark.csv",               "baseline"),
]

def read_mean_reduction(csv_path:Path)->tuple[float,int]:
    import pandas as pd
    try:
        df = pd.read_csv(csv_path)
        if "reduction" not in df.columns: return (float("nan"), 0)
        s = pd.to_numeric(df["reduction"], errors="coerce").dropna()
        return (float(s.mean()), int(s.size))
    except Exception:
        return (float("nan"), 0)

def collect_sources()->list[dict]:
    rows=[]
    for fname,label in CANDIDATE_FILES:
        p = COMP/fname
        if not p.exists(): continue
        mean,n = read_mean_reduction(p)
        if n>0:
            rows.append({"file": fname, "label": label, "mean_reduction": mean, "n": n})
    # também incluir mini benches por TPD como fontes auxiliares (sem rotular como modo)
    for p in COMP.glob("bench_K*_*_mini.csv"):
        mean,n = read_mean_reduction(p)
        if n>0:
            rows.append({"file": p.name, "label": "tpd_bench_mini", "mean_reduction": mean, "n": n})
    return rows

def best_overall(sources:list[dict])->dict|None:
    if not sources: return None
    # privilegiar grid+acts quando empate (ordem de peso)
    priority = { "grid+acts":3, "grid":2, "overlay_by_act":2, "overlay_ner":2, "overlay_adaptive":1, "overlay":1, "baseline":0, "tpd_bench_mini":0 }
    best = None
    for s in sources:
        if best is None:
            best = s; continue
        if s["mean_reduction"] > best["mean_reduction"] + 1e-9:
            best = s
        elif abs(s["mean_reduction"]-best["mean_reduction"])<=1e-9:
            if priority.get(s["label"],0) > priority.get(best["label"],0):
                best = s
    return best

def parse_tpd_from_name(name:str)->tuple[str,str]|None:
    # bench_K3000-3000_screenplay_synth_mini.csv  -> ("K3000-3000","screenplay_synth")
    m = re.match(r"bench_(K[0-9\-]+)_([a-z0-9_]+)_mini\.csv", name)
    if not m: return None
    return m.group(1), m.group(2)

def collect_tpd_stats()->dict:
    import pandas as pd
    rows=[]
    for p in COMP.glob("bench_K*_*_mini.csv"):
        parsed = parse_tpd_from_name(p.name)
        if not parsed: continue
        tpd, dataset = parsed
        try:
            df = pd.read_csv(p)
            if "reduction" not in df.columns: continue
            s = pd.to_numeric(df["reduction"], errors="coerce").dropna()
            if s.size==0: continue
            rows.append({"tpd":tpd, "dataset":dataset, "mean_reduction":float(s.mean()), "n":int(s.size)})
        except Exception:
            continue
    if not rows: return {"candidates":[]}

    # best overall + per dataset
    from collections import defaultdict
    by_tpd = defaultdict(list)
    by_ds  = defaultdict(list)
    for r in rows:
        by_tpd[r["tpd"]].append(r["mean_reduction"])
        by_ds[r["dataset"]].append((r["tpd"], r["mean_reduction"]))

    best_overall_tpd = max(((tpd,sum(vals)/len(vals)) for tpd,vals in by_tpd.items()), key=lambda kv: kv[1])
    per_dataset_best = {}
    for ds, arr in by_ds.items():
        per_dataset_best[ds] = max(arr, key=lambda kv: kv[1])

    # tentar localizar caminhos reais
    best_paths={}
    search_dirs=[ROOT/"data/tpd/sweep_big", ROOT/"data/tpd/stacked"]
    for tpd,_ in [best_overall_tpd] + list(per_dataset_best.values()):
        for d in search_dirs:
            cand = d/tpd/"token_dict.json"
            if cand.exists():
                best_paths[tpd] = str(cand); break

    return {
        "candidates": rows,
        "best_overall": {"tpd":best_overall_tpd[0], "mean_reduction":best_overall_tpd[1]},
        "per_dataset": {ds:{"tpd":tpd,"mean_reduction":mean} for ds,(tpd,mean) in per_dataset_best.items()},
        "paths": best_paths
    }

def recommended_make_targets(best_label:str)->list[str]:
    # recomendações mínimas, alinhadas aos targets existentes
    if best_label=="grid+acts":           return ["bench-grid-acts-nano"]
    if best_label=="grid":                return ["bench-grid-adaptive-nano"]
    if best_label=="overlay_by_act":      return ["bench-overlay-acts-nano"]
    if best_label=="overlay_ner":         return ["bench-overlay-ner-nano"]
    if best_label=="overlay_adaptive":    return ["bench-overlay-adaptive-nano"]
    if best_label=="overlay":             return ["bench-overlay-nano"]
    return ["bench-all-nano"]

def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    sources = collect_sources()
    best = best_overall(sources)
    tpd_stats = collect_tpd_stats()

    out = {
        "generated_at": datetime.utcnow().isoformat()+"Z",
        "sources_considered": sources,
        "best_overall_source": best,
        "tpd": tpd_stats,
        "recommendation": {
            "mode": (best or {}).get("label","unknown"),
            "make_targets": recommended_make_targets((best or {}).get("label","")),
            "notes": "Freeze this mode for production benches; use select_best_tpd.py to pin TPD; legend sidecar for reversibility."
        }
    }
    (REPORTS/"compression_strategy.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    # resumo humano
    def pct(x): 
        try: return f"{100.0*float(x):.1f}%"
        except: return "n/a"
    lines=[]
    lines.append("# Compression Strategy (auto-decide)\n")
    if best:
        lines.append(f"- **Best source**: `{best['file']}` ({best['label']}) · mean reduction **{pct(best['mean_reduction'])}** · n={best['n']}")
        mt = ", ".join(recommended_make_targets(best['label']))
        lines.append(f"- **Run targets**: `{mt}`")
    else:
        lines.append("- **Best source**: not found")
    if tpd_stats.get("candidates"):
        bo = tpd_stats["best_overall"]
        lines.append(f"- **Best TPD overall**: `{bo['tpd']}` · mean **{pct(bo['mean_reduction'])}**")
        path = tpd_stats.get("paths",{}).get(bo["tpd"])
        if path:
            lines.append(f"  - path: `{path}` (copy to `data/tpd/default/token_dict.json` if desired)")
    (REPORTS/"strategy_summary.md").write_text("\n".join(lines)+"\n", encoding="utf-8")

    print("[OK] strategy -> reports/compression_strategy.json")
    print("[OK] summary  -> reports/strategy_summary.md")

if __name__=="__main__":
    main()