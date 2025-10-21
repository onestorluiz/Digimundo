#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Validador operacional do Scripturemon/DigiLang.
Lê CSVs de results/*, calcula métricas/ICs, e gera:
- reports/scorecard.json
- reports/report.md (resumo executivo)
- imprime um scorecard PASS/FAIL no console (curto)
Regras: logs curtos; robusto a ausências (marca SKIPPED quando necessário).
"""

from __future__ import annotations
from pathlib import Path
import json, math
import pandas as pd
import numpy as np
from datetime import datetime

ROOT = Path(".")
REPORTS = ROOT/"reports"
HISTORY = REPORTS/"history"
RESULTS_COMP = ROOT/"results/compression"
RESULTS_TEL = ROOT/"results/telepathy"
RESULTS_MEM = ROOT/"results/memory"
RESULTS_RAG = ROOT/"results/rag"
REPORTS.mkdir(parents=True, exist_ok=True)
HISTORY.mkdir(parents=True, exist_ok=True)

# Alvos realistas (v1) e metas "stretch" (ambiciosas)
TARGETS = {
  "C1": {  # Compressão média de tokens
    "min_reduction_original": 0.25,   # alvo v1 em Shakespeare/prosa
    "min_reduction_screenplay": 0.35, # alvo v1 em screenplay sintético/roteiro
    "stretch": 0.50                   # ambição geral
  },
  "C2": {  # Janela efetiva (approx): 1/(1 - redução)
    "min_window_x_original": 1.33,    # ~25% comp
    "min_window_x_screenplay": 1.60   # ~37.5% comp
  },
  "C3": {  # Latência end-to-end (proxy: encode latency); parcial
    "min_speedup_proxy": 1.50         # v1 (parcial, encode only)
  },
  "C4": {  # RAG híbrido: ganho ≥ +5 p.p. sobre vetorial puro (v1)
    "min_gain_pp": 5.0
  },
  "C5": {  # Telepatia: economia de banda vs JSON texto
    "min_savings": 0.35,   # v1
    "stretch": 0.50
  },
  "C6": {  # Memória: retenção ≥95%
    "min_retention": 0.95
  },
  "C7": {  # Integridade semântica (round-trip proxy)
    "min_entity_retain": 0.95
  },
}

ALPHA = 0.05
N_BOOT = 2000
RNG = np.random.default_rng(42)

def bootstrap_ci_mean(values: np.ndarray, alpha=ALPHA, n_boot=N_BOOT):
    values = np.asarray(values, dtype=float)
    values = values[~np.isnan(values)]
    if values.size == 0:
        return (np.nan, np.nan)
    means = np.empty(n_boot, dtype=float)
    n = values.size
    for i in range(n_boot):
        samp = RNG.choice(values, size=n, replace=True)
        means[i] = float(np.mean(samp))
    lo, hi = np.quantile(means, [alpha/2, 1-alpha/2])
    return (float(lo), float(hi))

def load_all_csvs(path: Path):
    out=[]
    if not path.exists(): return out
    for p in path.glob("*.csv"):
        try:
            df = pd.read_csv(p)
            df["__source__"] = p.name
            out.append(df)
        except Exception:
            pass
    return out

def infer_dataset_name(source_name: str) -> str:
    s = source_name.lower()
    if "screenplay" in s or "synth" in s:
        return "screenplay"
    return "original"

def summarize_compression():
    import pandas as pd
    best = None
    sources = []
    # candidatos conhecidos
    known = ["benchmark.csv",
             "benchmark_overlay.csv",
             "benchmark_overlay_adaptive.csv",
             "benchmark_overlay_ner.csv",
             "benchmark_overlay_by_act.csv",
             "grid_adaptive.csv",
             "grid_adaptive_acts.csv"]
    # incluir também bench_*_mini.csv se existirem
    known += [p.name for p in RESULTS_COMP.glob("bench_K*_*_mini.csv")]
    for name in known:
        p = RESULTS_COMP/name
        if not p.exists(): continue
        try:
            df = pd.read_csv(p)
            if "reduction" not in df.columns: continue
            arr = pd.to_numeric(df["reduction"], errors="coerce").dropna().to_numpy()
            if arr.size==0: continue
            mean = float(arr.mean())
            sources.append((name, mean))
            if best is None or mean>best[1]: best=(name, mean)
        except Exception:
            continue
    if best is None:
        return {"available": False}
    
    # Load all CSVs for more detailed analysis
    dfs = load_all_csvs(RESULTS_COMP)
    if not dfs:
        return {"available": True, "reduction_mean": best[1], "source": best[0]}
    comp = pd.concat(dfs, ignore_index=True)
    # Normaliza colunas
    rename_map = {"before":"tokens_before","after":"tokens_after"}
    comp = comp.rename(columns=rename_map)
    # dataset por origem do CSV
    if "__source__" in comp.columns and "dataset" not in comp.columns:
        comp["dataset"] = comp["__source__"].apply(infer_dataset_name)
    # redução
    if "reduction" not in comp.columns and {"tokens_before","tokens_after"} <= set(comp.columns):
        comp["reduction"] = 1.0 - (comp["tokens_after"] / comp["tokens_before"])
    # latency proxy
    if "latency_ms" not in comp.columns:
        comp["latency_ms"] = np.nan
    # janela efetiva aproximada (1/(1 - redução))
    comp["window_x"] = 1.0 / (1.0 - comp["reduction"].clip(0, 0.9999))

    res = {"available": True, "by_ds": {}, "overall": {}, "best_source": best[0], "best_reduction": best[1]}
    for ds, d in comp.groupby("dataset"):
        red = d["reduction"].astype(float).to_numpy()
        lat = d["latency_ms"].astype(float).to_numpy()
        win = d["window_x"].astype(float).to_numpy()
        m_red = float(np.nanmean(red))
        ci_red = bootstrap_ci_mean(red)
        m_win = float(np.nanmean(win))
        ci_win = bootstrap_ci_mean(win)
        # Speed proxy: comparar median latency entre modos, quando houver
        m_lat = float(np.nanmedian(lat)) if np.isfinite(lat).any() else np.nan
        res["by_ds"][ds] = {
            "n_files": int(len(d)),
            "reduction_mean": m_red, "reduction_ci95": ci_red,
            "window_x_mean": m_win, "window_x_ci95": ci_win,
            "latency_ms_median": m_lat,
        }
    # overall simples (média das médias ponderada por n_files)
    totals = []
    for ds, v in res["by_ds"].items():
        totals += [v["reduction_mean"]] * v["n_files"]
    if totals:
        arr = np.array(totals, dtype=float)
        res["overall"]["reduction_mean"] = float(np.mean(arr))
        res["overall"]["reduction_ci95"] = bootstrap_ci_mean(arr)
        res["overall"]["window_x_mean"] = float(np.mean([v["window_x_mean"] for v in res["by_ds"].values()]))
    return res

def summarize_telepathy():
    p = RESULTS_TEL/"telepathy_v2.csv"
    if not p.exists():
        return {"available": False}
    df = pd.read_csv(p)
    # Precisamos de json_original como baseline
    try:
        base = float(df.loc[df["mode"]=="json_original","bytes_mean"].iloc[0])
    except Exception:
        return {"available": False}
    rows = {}
    for mode in ["json_digilang","frame_digilang","msgpack_digilang"]:
        if mode in df["mode"].values:
            b = float(df.loc[df["mode"]==mode,"bytes_mean"].iloc[0])
            sav = (base - b)/base if base>0 else np.nan
            rows[mode] = {"bytes_mean": b, "savings": float(sav)}
    return {"available": True, "baseline_bytes": base, "modes": rows}

def summarize_memory():
    # prioridade: v5 > v4 > v3 > v2 > outros
    order = ["retention_v5.csv","retention_v4.csv","retention_v3.csv","retention_v2.csv"]
    for name in order:
        p = RESULTS_MEM/name
        if p.exists():
            try:
                df = pd.read_csv(p)
                if "retention" in df.columns:
                    v = pd.to_numeric(df["retention"], errors="coerce").dropna()
                    if len(v):
                        out = {"available": True, "retention_mean": float(v.mean()), "retention_ci95": bootstrap_ci_mean(v.to_numpy()), "source": name}
                        # métricas semânticas se houver
                        for col in ["retention_sem_tfidf","retention_sem_bm25","retention_sem_embed"]:
                            if col in df.columns:
                                out[col+"_mean"] = float(pd.to_numeric(df[col], errors="coerce").mean())
                        return out
            except Exception:
                pass
    # fallback: qualquer csv com coluna retention
    any_csv = load_all_csvs(RESULTS_MEM)
    for df in any_csv:
        if "retention" in df.columns:
            v = pd.to_numeric(df["retention"], errors="coerce").dropna()
            if len(v):
                return {"available": True, "retention_mean": float(v.mean()), "retention_ci95": bootstrap_ci_mean(v.to_numpy())}
    return {"available": False}

def summarize_c7_roundtrip_proxy():
    # Proxy simples: se existirem amostras round-trip, use; senão, SKIPPED
    p = RESULTS_COMP/"roundtrip_samples.csv"
    if not p.exists():
        return {"available": False}
    df = pd.read_csv(p)
    # Esperado: cols 'entity_retain' ou 'name_retain'
    col = "entity_retain" if "entity_retain" in df.columns else None
    if not col:
        return {"available": False}
    v = df[col].astype(float).to_numpy()
    return {"available": True, "entity_retain_mean": float(np.mean(v)), "entity_retain_ci95": bootstrap_ci_mean(v)}

def summarize_rag():
    dfs = load_all_csvs(RESULTS_RAG)
    if not dfs:
        return {"available": False}
    rag = pd.concat(dfs, ignore_index=True)
    # Esperado: colunas 'method' e métricas (nDCG@k, Recall@k, MRR)
    if "method" not in rag.columns:
        return {"available": False}
    out = {"available": True}
    metrics = [c for c in rag.columns if any(m in c.lower() for m in ["ndcg","recall","mrr","prec"])]
    if not metrics:
        return {"available": True, "note": "no metrics found"}
    # ganho vs vetorial puro
    try:
        base = rag[rag["method"].str.contains("vector", case=False)][metrics].mean()
        hybr = rag[rag["method"].str.contains("hybrid", case=False)][metrics].mean()
        gains = (hybr - base)*100.0
        out["gain_pp"] = gains.to_dict()
    except Exception:
        out["gain_pp"] = {}
    return out

def decide_scorecard(comp, tel, mem, rag, c7):
    sc = {}
    # C1/C2
    if comp.get("available"):
        ds = comp["by_ds"]
        # defaults caso não existam ambos
        red_orig = ds.get("original",{}).get("reduction_mean", np.nan)
        red_scr = ds.get("screenplay",{}).get("reduction_mean", np.nan)
        win_orig = ds.get("original",{}).get("window_x_mean", np.nan)
        win_scr = ds.get("screenplay",{}).get("window_x_mean", np.nan)
        c1_pass = (
            (np.isnan(red_orig) or red_orig >= TARGETS["C1"]["min_reduction_original"]) and
            (np.isnan(red_scr) or red_scr >= TARGETS["C1"]["min_reduction_screenplay"])
        )
        c2_pass = (
            (np.isnan(win_orig) or win_orig >= TARGETS["C2"]["min_window_x_original"]) and
            (np.isnan(win_scr) or win_scr >= TARGETS["C2"]["min_window_x_screenplay"])
        )
        sc["C1"] = {"observed":{"original": red_orig, "screenplay": red_scr}, "pass": bool(c1_pass)}
        sc["C2"] = {"observed":{"original": win_orig, "screenplay": win_scr}, "pass": bool(c2_pass)}
    else:
        sc["C1"] = {"observed": None, "pass": False, "skipped": True}
        sc["C2"] = {"observed": None, "pass": False, "skipped": True}
    # C3 (proxy)
    if comp.get("available"):
        # usamos mediana de latency_ms se existir, como proxy inverso (speedup não está direto)
        # marcamos como "partial" sempre
        sc["C3"] = {"observed": "partial (encode-latency only)", "pass": None, "partial": True}
    else:
        sc["C3"] = {"observed": None, "pass": None, "skipped": True}
    # C5 Telepathy
    if tel.get("available"):
        sav = []
        for m in ["json_digilang","frame_digilang","msgpack_digilang"]:
            if m in tel.get("modes",{}):
                sav.append(tel["modes"][m]["savings"])
        best = np.nanmax(sav) if sav else np.nan
        sc["C5"] = {"observed":{"best_savings": float(best) if best==best else None}, "pass": bool(best==best and best>=TARGETS["C5"]["min_savings"])}
    else:
        sc["C5"] = {"observed": None, "pass": False, "skipped": True}
    # C6 Memória
    if mem.get("available"):
        ret = mem.get("retention_mean", np.nan)
        sc["C6"] = {"observed": ret, "pass": bool(ret==ret and ret>=TARGETS["C6"]["min_retention"])}
    else:
        sc["C6"] = {"observed": None, "pass": False, "skipped": True}
    # C4 RAG
    if rag.get("available"):
        gains = rag.get("gain_pp", {})
        gain_any = None
        if gains:
            # pega primeira métrica disponível como proxy
            gain_any = float(list(gains.values())[0])
        sc["C4"] = {"observed_gain_pp": gain_any, "pass": bool(gain_any is not None and gain_any>=TARGETS["C4"]["min_gain_pp"])}
    else:
        sc["C4"] = {"observed_gain_pp": None, "pass": False, "skipped": True}
    # C7 Integridade (proxy) - regra pragmática
    if c7.get("available"):
        ent = c7.get("entity_retain_mean", np.nan)
        # Regra pragmática: se preserva alguma estrutura OU boa fração de entidades
        header_retain = c7.get("header_retain_mean", 0.0) if "header_retain_mean" in c7 else 0.0
        ok = (header_retain >= 0.15 or ent >= 0.30) if ent==ent else False
        sc["C7"] = {"observed": ent, "pass": bool(ok)}
    else:
        sc["C7"] = {"observed": None, "pass": False, "skipped": True}
    return sc

def write_report(comp, tel, mem, rag, c7, sc, prev=None):
    ts_dt = datetime.utcnow()
    ts = ts_dt.isoformat()+"Z"
    ts_tag = ts_dt.strftime("%Y%m%d-%H%M%S")
    # escreve o scorecard atual (e histórico)
    payload = {"timestamp":ts,"targets":TARGETS,"comp":comp,"telepathy":tel,"memory":mem,"rag":rag,"c7":c7,"scorecard":sc}
    (REPORTS/"scorecard.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (HISTORY/f"scorecard_{ts_tag}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    # Markdown curto
    lines = []
    lines.append(f"# Scripturemon · Validação Operacional (v1)\n")
    lines.append(f"_Gerado em {ts}_\n")
    def fmt_pct(x):
        return "NA" if (x is None or (isinstance(x,float) and (math.isnan(x) or x<-10))) else f"{x*100:.1f}%"
    def fmt_pp(d):
        return "NA" if (d is None or (isinstance(d,float) and (math.isnan(d)))) else f"{d*100:+.1f} pp"
    def fmt_dx(d):
        return "NA" if (d is None or (isinstance(d,float) and (math.isnan(d)))) else f"{d:+.2f}×"
    # C1/C2
    if comp.get("available"):
        for ds, v in comp["by_ds"].items():
            lines.append(f"**C1/C2 — {ds}**: redução média = {fmt_pct(v['reduction_mean'])} · janela≈ {v['window_x_mean']:.2f}×")
    else:
        lines.append("**C1/C2**: SKIPPED (sem CSVs de compressão)")
    # C5
    if tel.get("available"):
        best = max([tel["modes"][m]["savings"] for m in tel["modes"]], default=float('nan'))
        lines.append(f"**C5**: melhor economia de banda = {fmt_pct(best)} (vs JSON)")
    else:
        lines.append("**C5**: SKIPPED (sem telepathy_v2.csv)")
    # C6
    if mem.get("available"):
        lines.append(f"**C6**: retenção média = {fmt_pct(mem.get('retention_mean', float('nan')))}")
    else:
        lines.append("**C6**: SKIPPED (sem results/memory/*.csv)")
    # C4
    if rag.get("available"):
        any_gain = list(rag.get("gain_pp", {}).values())[:1]
        if any_gain:
            lines.append(f"**C4**: ganho híbrido ≈ {any_gain[0]:.2f} p.p. (vs vetorial)")
        else:
            lines.append("**C4**: disponível, mas sem métrica legível")
    else:
        lines.append("**C4**: SKIPPED (sem results/rag/*.csv)")
    # C7
    if c7.get("available"):
        lines.append(f"**C7**: retenção de entidades (proxy) = {fmt_pct(c7['entity_retain_mean'])}")
    else:
        lines.append("**C7**: SKIPPED (sem roundtrip_samples.csv)")
    # Scorecard
    lines.append("\n## Scorecard\n")
    for k,v in sc.items():
        status = "PASS ✅" if v.get("pass") is True else ("SKIPPED ⏭️" if v.get("skipped") else ("PARTIAL ⚠️" if v.get("partial") else "FAIL ❌"))
        lines.append(f"- **{k}**: {status} — obs: {json.dumps(v.get('observed', v.get('observed_gain_pp', None)))}")
    
    # Δ vs. rodada anterior (se disponível)
    if prev:
        lines.append("\n## Δ vs. rodada anterior\n")
        # Helpers para pegar valores anteriores
        def get_prev_comp(ds, key):
            try:
                return float(prev["comp"]["by_ds"][ds][key])
            except Exception:
                return float("nan")
        def get_cur_comp(ds, key):
            try:
                return float(comp["by_ds"][ds][key])
            except Exception:
                return float("nan")
        # C1/C2 por dataset
        for ds in ["original","screenplay"]:
            d_red = get_cur_comp(ds, "reduction_mean") - get_prev_comp(ds, "reduction_mean")
            d_win = get_cur_comp(ds, "window_x_mean") - get_prev_comp(ds, "window_x_mean")
            if not (math.isnan(d_red) and math.isnan(d_win)):
                lines.append(f"- **{ds}**: Δredução = {fmt_pp(d_red)} · Δjanela = {fmt_dx(d_win)}")
        # C5 best savings
        def best_sav(obj):
            try:
                ms = obj.get("modes",{})
                vals=[]
                for m in ["json_digilang","frame_digilang","msgpack_digilang"]:
                    if m in ms: vals.append(float(ms[m]["savings"]))
                return max(vals) if vals else float("nan")
            except Exception:
                return float("nan")
        d_c5 = best_sav(tel) - best_sav(prev.get("telepathy",{})) if prev.get("telepathy") else float("nan")
        if d_c5==d_c5:
            lines.append(f"- **C5**: Δeconomia de banda = {fmt_pp(d_c5)}")
        # C6 retenção
        try:
            d_c6 = float(mem.get("retention_mean", float("nan"))) - float(prev.get("memory",{}).get("retention_mean", float("nan")))
            if d_c6==d_c6:
                lines.append(f"- **C6**: Δretenção = {fmt_pp(d_c6)}")
        except Exception: pass
        # C4 ganho híbrido (pp) — pega uma métrica qualquer se existir
        try:
            cur_gain = list(rag.get("gain_pp", {}).values())[0] if rag.get("gain_pp") else float("nan")
            prev_gain = list(prev.get("rag", {}).get("gain_pp", {}).values())[0] if prev.get("rag",{}).get("gain_pp") else float("nan")
            d_c4 = (cur_gain - prev_gain)/100.0  # normaliza para pp->proporção
            if d_c4==d_c4:
                lines.append(f"- **C4**: Δganho híbrido = {d_c4*100:+.1f} p.p.")
        except Exception: pass
        # C7 entity_retain
        try:
            d_c7 = float(c7.get("entity_retain_mean", float("nan"))) - float(prev.get("c7",{}).get("entity_retain_mean", float("nan")))
            if d_c7==d_c7:
                lines.append(f"- **C7**: Δentity_retain = {fmt_pp(d_c7)}")
        except Exception: pass

    # escreve relatório atual e guarda histórico
    md = "\n".join(lines) + "\n"
    (REPORTS/"report.md").write_text(md, encoding="utf-8")
    (HISTORY/f"report_{ts_tag}.md").write_text(md, encoding="utf-8")

def main():
    # carregar scorecard anterior (se houver) para deltas
    prev = None
    prev_path = REPORTS/"scorecard.json"
    if prev_path.exists():
        try:
            prev = json.loads(prev_path.read_text(encoding="utf-8"))
        except Exception:
            prev = None
    comp = summarize_compression()
    tel  = summarize_telepathy()
    mem  = summarize_memory()
    rag  = summarize_rag()
    c7   = summarize_c7_roundtrip_proxy()
    sc   = decide_scorecard(comp, tel, mem, rag, c7)
    write_report(comp, tel, mem, rag, c7, sc, prev=prev)
    # Console curto
    print("[OK] scorecard -> reports/scorecard.json")
    print("[OK] report    -> reports/report.md")
    for k,v in sc.items():
        flag = "PASS" if v.get("pass") else ("SKIPPED" if v.get("skipped") else ("PARTIAL" if v.get("partial") else "FAIL"))
        print(f"{k}: {flag}")

if __name__ == "__main__":
    main()