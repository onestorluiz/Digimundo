#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Agrega resultados em CSVs mínimos dentro de reports/aggregates/:
- compression_summary.csv, compression_best_per_dataset.csv
- telepathy_summary.csv (v2/v3 se existirem)
- e2e_summary.csv
- rag_summary.csv
- memory_summary.csv
- roundtrip_summary.csv
+ manifest.json com a lista de arquivos gerados.
Logs curtos, tolerante a ausências.
"""
from __future__ import annotations
from pathlib import Path
import json
import pandas as pd
import numpy as np

ROOT = Path(".")
RESULTS = ROOT/"results"
AGG = ROOT/"reports/aggregates"
AGG.mkdir(parents=True, exist_ok=True)

def _read_csvs(dir_: Path):
    out=[]
    if dir_.exists():
        for p in dir_.glob("*.csv"):
            try:
                df = pd.read_csv(p)
                df["__source__"] = p.name
                out.append(df)
            except Exception:
                pass
    return out

def _infer_dataset(source: str) -> str:
    s=source.lower()
    if "screenplay" in s or "synth" in s: return "screenplay"
    return "original"

def agg_compression():
    dirc = RESULTS/"compression"
    dfs = _read_csvs(dirc)
    if not dfs: return []
    comp = pd.concat(dfs, ignore_index=True)
    comp = comp.rename(columns={"before":"tokens_before","after":"tokens_after"})
    if "__source__" in comp.columns and "dataset" not in comp.columns:
        comp["dataset"] = comp["__source__"].apply(_infer_dataset)
    if "reduction" not in comp.columns and {"tokens_before","tokens_after"} <= set(comp.columns):
        comp["reduction"] = 1 - (comp["tokens_after"]/comp["tokens_before"])
    comp["window_x"] = 1.0/(1.0 - comp["reduction"].clip(0,0.9999))
    grp = ["dataset"] + (["mode"] if "mode" in comp.columns else []) + (["tpd_policy"] if "tpd_policy" in comp.columns else [])
    summary = comp.groupby(grp, dropna=False).agg(
        n_files=("file","count") if "file" in comp.columns else ("reduction","count"),
        reduction_mean=("reduction","mean"),
        reduction_median=("reduction","median"),
        window_x_mean=("window_x","mean")
    ).reset_index().sort_values(["dataset","reduction_mean"], ascending=[True,False])
    out1 = AGG/"compression_summary.csv"; summary.round(6).to_csv(out1, index=False)

    # melhor por dataset
    best_rows=[]
    for ds, d in summary.groupby("dataset"):
        best_rows.append(d.sort_values("reduction_mean", ascending=False).head(1))
    best = pd.concat(best_rows, ignore_index=True) if best_rows else pd.DataFrame()
    out2 = AGG/"compression_best_per_dataset.csv"
    if not best.empty: best.round(6).to_csv(out2, index=False)
    return [out1] + ([out2] if out2.exists() else [])

def agg_telepathy():
    outs=[]
    v2 = RESULTS/"telepathy"/"telepathy_v2.csv"
    v3 = RESULTS/"telepathy"/"telepathy_v3.csv"
    rows=[]
    for p in [v2,v3]:
        if p.exists():
            try:
                df = pd.read_csv(p)
                if {"mode","bytes_mean"} <= set(df.columns):
                    base = df.loc[df["mode"]=="json_original","bytes_mean"]
                    base = float(base.iloc[0]) if len(base) else np.nan
                    for _,r in df.iterrows():
                        sav = np.nan
                        if r["mode"]!="json_original" and base==base and base>0:
                            sav = (base - float(r["bytes_mean"]))/base
                        rows.append(dict(source=p.name, mode=r["mode"], bytes_mean=float(r["bytes_mean"]), savings=sav,
                                         throughput=r.get("throughput_msgs_s", np.nan)))
            except Exception:
                pass
    if rows:
        tel = pd.DataFrame(rows)
        out = AGG/"telepathy_summary.csv"
        tel.round(6).to_csv(out, index=False); outs.append(out)
    return outs

def agg_e2e():
    p = RESULTS/"e2e"/"bench.csv"
    if not p.exists(): return []
    try:
        df = pd.read_csv(p)
        cols = [c for c in df.columns if c.endswith("_ms")]
        if not cols: return []
        summ = {f"{c}_mean": df[c].mean() for c in cols}
        summ.update({f"{c}_p50": df[c].median() for c in cols})
        summ.update({f"{c}_p95": df[c].quantile(0.95) for c in cols})
        summ["n_files"]=len(df)
        out = AGG/"e2e_summary.csv"
        pd.DataFrame([summ]).round(3).to_csv(out, index=False)
        return [out]
    except Exception:
        return []

def agg_rag():
    dirr = RESULTS/"rag"
    dfs = _read_csvs(dirr)
    if not dfs: return []
    rag = pd.concat(dfs, ignore_index=True)
    if "method" not in rag.columns: return []
    metrics = [c for c in rag.columns if any(m in c.lower() for m in ["ndcg","recall","mrr","prec"])]
    if not metrics: return []
    summ = rag.groupby("method")[metrics].mean().reset_index()
    out = AGG/"rag_summary.csv"; summ.round(6).to_csv(out, index=False)
    return [out]

def agg_memory():
    d = RESULTS/"memory"
    dfs = _read_csvs(d)
    if not dfs: return []
    mem = pd.concat(dfs, ignore_index=True)
    
    # Build summary dict with multiple retention metrics
    summary = {"n": len(mem)}
    cols = []
    if "retention" in mem.columns: cols.append(("retention","retention_mean"))
    if "retention_sem_tfidf" in mem.columns: cols.append(("retention_sem_tfidf","retention_sem_tfidf_mean"))
    if "retention_sem_bm25" in mem.columns: cols.append(("retention_sem_bm25","retention_sem_bm25_mean"))
    if "retention_sem_embed" in mem.columns: cols.append(("retention_sem_embed","retention_sem_embed_mean"))
    
    # Also handle legacy columns
    if not cols:
        col = "retention" if "retention" in mem.columns else ("accuracy" if "accuracy" in mem.columns else None)
        if not col: return []
        summary["retention_mean"] = float(pd.to_numeric(mem[col], errors="coerce").mean())
    else:
        for src_col, dest_col in cols:
            summary[dest_col] = float(pd.to_numeric(mem[src_col], errors="coerce").mean())
    
    out = AGG/"memory_summary.csv"
    pd.DataFrame([summary]).round(6).to_csv(out, index=False)
    return [out]

def agg_roundtrip():
    p = RESULTS/"compression"/"roundtrip_samples.csv"
    if not p.exists(): return []
    try:
        df = pd.read_csv(p)
    except Exception:
        return []
    cols = [c for c in ["integrity_score","entity_retain","header_retain","content_overlap","reduction"] if c in df.columns]
    if not cols: return []
    grp = ["dataset"] if "dataset" in df.columns else []
    summ = df.groupby(grp)[cols].agg(["count","mean","median","std"]).reset_index()
    # flatten MultiIndex
    summ.columns = ["_".join([c for c in col if c]).strip("_") for col in summ.columns.values]
    out = AGG/"roundtrip_summary.csv"; summ.round(6).to_csv(out, index=False)
    return [out]

def main():
    generated = []
    for fn in [agg_compression, agg_telepathy, agg_e2e, agg_rag, agg_memory, agg_roundtrip]:
        try:
            generated += fn()
        except Exception:
            pass
    manifest = {"files":[str(p) for p in generated]}
    (AGG/"manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[OK] aggregates -> {len(generated)} files in reports/aggregates")

if __name__ == "__main__":
    main()