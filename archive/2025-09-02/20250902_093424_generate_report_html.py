#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64, io
from pathlib import Path
import pandas as pd

# Fallback: se matplotlib não estiver disponível, seguimos sem mini‑gráficos inline
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception:
    matplotlib = None
    plt = None

REPORTS = Path("reports")
DIST = Path("dist")
PDF = REPORTS / "report.pdf"
FIGS = REPORTS / "figures"
RESULTS_COMP = Path("results/compression")
RESULTS_TEL = Path("results/telepathy")
REPORTS.mkdir(parents=True, exist_ok=True)
FIGS.mkdir(parents=True, exist_ok=True)

def read_csvs_glob(globdir: Path):
    dfs=[]
    if not globdir.exists():
        return dfs
    for p in globdir.glob("*.csv"):
        try:
            df = pd.read_csv(p)
            df["__source__"] = p.name
            dfs.append(df)
        except Exception:
            pass
    return dfs

def embed_png_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'<img alt="{path.name}" style="max-width:100%;height:auto;border:1px solid #ddd" src="data:image/png;base64,{b64}"/>'

def _fig_to_data_uri(fig) -> str:
    if plt is None:
        return ""
    buf = io.BytesIO()
    try:
        fig.tight_layout()
    except Exception:
        pass
    fig.savefig(buf, format="png", dpi=120)
    plt.close(fig)
    return f'<img style="max-width:100%;height:auto;border:1px solid #ddd" src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode("ascii")}"/>'

def inline_hist(series, title: str):
    """Histograma inline (fallback) para distribuição de reduction por modo."""
    if plt is None:
        return ""
    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        return ""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(s, bins=20)
    ax.set_title(title)
    ax.set_xlabel("reduction")
    ax.set_ylabel("count")
    return _fig_to_data_uri(fig)

def inline_bar(categories, values, title: str, ylabel: str):
    """Bar chart inline genérico (ex.: métricas de telepathy)."""
    if plt is None:
        return ""
    x = list(categories)
    y = pd.to_numeric(values, errors="coerce").fillna(0).tolist()
    if not x:
        return ""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(range(len(x)), y)
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels([str(v) for v in x], rotation=20, ha="right")
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    return _fig_to_data_uri(fig)

def inline_boxplot_by_group(values, groups, title: str, ylabel: str):
    """Boxplot inline por grupo (ex.: integrity_score por dataset)."""
    if plt is None:
        return ""
    df = pd.DataFrame({"v": pd.to_numeric(values, errors="coerce"),
                       "g": groups})
    df = df.dropna()
    if df.empty:
        return ""
    order = list(df["g"].dropna().unique())
    data = [df.loc[df["g"]==g, "v"].tolist() for g in order]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.boxplot(data, labels=[str(g) for g in order], showmeans=True)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    return _fig_to_data_uri(fig)

def table_html(df: pd.DataFrame, max_rows: int = 200) -> str:
    if len(df) > max_rows:
        df = df.head(max_rows)
    return df.to_html(index=False, escape=False)

def main():
    sections = []

    # 1) Compressão — agregados
    comp_dfs = read_csvs_glob(RESULTS_COMP)
    if comp_dfs:
        comp = pd.concat(comp_dfs, ignore_index=True)
        comp = comp.rename(columns={"before":"tokens_before","after":"tokens_after"})
        if "mode" not in comp.columns and "__source__" in comp.columns:
            comp["mode"] = comp["__source__"].str.replace(".csv","",regex=False)

        grp_cols = ["mode"] + (["tpd_policy"] if "tpd_policy" in comp.columns else [])
        summary = comp.groupby(grp_cols, dropna=False).agg(
            avg_reduction=("reduction","mean"),
            p50_reduction=("reduction","median"),
            p95_latency=("latency_ms","max") if "latency_ms" in comp.columns else ("reduction","count")
        ).reset_index().sort_values("avg_reduction", ascending=False)

        sections.append("<h2>Compression — Summary</h2>")
        sections.append(table_html(summary.round(4)))

        # Mini‑charts inline (fallback) por modo, só se PNGs não existirem
        if "mode" in comp.columns and "reduction" in comp.columns:
            safe = lambda s: str(s).replace("/", "_").replace(" ", "_")
            added_any = False
            mini = []
            for mode, d in comp.groupby("mode"):
                png_path = FIGS / f"reduction_{safe(mode)}.png"
                if not png_path.exists():
                    img = inline_hist(d["reduction"], f"Reduction — {mode}")
                    if img:
                        mini.append(f"<h4>{mode}</h4>{img}")
                        added_any = True
            if added_any:
                sections.append("<h3>Mini‑Charts (inline fallback)</h3>")
                sections.extend(mini)
    else:
        sections.append("<p><em>No compression CSVs found in results/compression/</em></p>")

    # 2) Figuras já existentes (se geradas por plot_results.py / plot_telepathy.py)
    sections.append("<h2>Figures</h2>")
    for name in ["reduction_canon+tpd.png","reduction_llmlingua.png","telepathy_bytes_mean.png","telepathy_throughput.png"]:
        img = embed_png_if_exists(FIGS / name)
        if img:
            sections.append(f"<h4>{name}</h4>{img}")

    # 3) Telepathy v2
    tel_csv = RESULTS_TEL / "telepathy_v2.csv"
    if tel_csv.exists():
        tel = pd.read_csv(tel_csv)
        sections.append("<h2>Telepathy v2 — Summary</h2>")
        sections.append(table_html(tel.round(4)))
        # Fallback: se não houver PNGs de telepathy, embutir mini‑gráficos inline
        if matplotlib is not None:
            if not (FIGS / "telepathy_bytes_mean.png").exists() and "bytes_mean" in tel.columns:
                sections.append("<h4>Telepathy — Bytes (mean)</h4>")
                sections.append(inline_bar(tel["mode"], tel["bytes_mean"], "Wire payload size (mean)", "bytes"))
            if not (FIGS / "telepathy_throughput.png").exists() and "throughput_msgs_s" in tel.columns:
                sections.append("<h4>Telepathy — Throughput</h4>")
                sections.append(inline_bar(tel["mode"], tel["throughput_msgs_s"], "Throughput (approx)", "msgs/s"))
    else:
        sections.append("<h2>Telepathy v2</h2><p><em>No telepathy_v2.csv found.</em></p>")

    # 4) Round-Trip Integrity (C7)
    rt_csv = RESULTS_COMP / "roundtrip_samples.csv"
    sections.append("<h2>Round‑Trip Integrity (C7)</h2>")
    if rt_csv.exists():
        rt = pd.read_csv(rt_csv)
        # Tabela de estatísticas resumidas por dataset (quando houver)
        if "dataset" in rt.columns and "integrity_score" in rt.columns:
            summary = rt.groupby("dataset")["integrity_score"].agg(["count","mean","median","std"]).reset_index()
            sections.append(table_html(summary.round(4)))
        # Boxplot preferencial: usar PNG se existir; senão inline
        png = FIGS / "integrity_boxplot.png"
        if png.exists():
            sections.append(f"<h4>Integrity Score — Boxplot</h4>{embed_png_if_exists(png)}")
        elif matplotlib is not None and "integrity_score" in rt.columns:
            groups = rt["dataset"] if "dataset" in rt.columns else pd.Series(["all"]*len(rt))
            sections.append("<h4>Integrity Score — Boxplot</h4>")
            sections.append(inline_boxplot_by_group(rt["integrity_score"], groups, "Integrity Score by Dataset", "integrity_score"))
        # Histograma de entity_retain: usa PNG se existir; senão inline
        hist_png = FIGS / "entity_retain_hist.png"
        if hist_png.exists():
            sections.append(f"<h4>Entity Retain — Distribution</h4>{embed_png_if_exists(hist_png)}")
        elif matplotlib is not None and "entity_retain" in rt.columns:
            sections.append("<h4>Entity Retain — Distribution</h4>")
            sections.append(inline_hist(rt["entity_retain"], "Entity Retain"))
    else:
        sections.append("<p><em>No roundtrip_samples.csv found (run: make roundtrip-samples).</em></p>")

    pdf_link = f'<p><strong>Export:</strong> <a href="report.pdf">Download PDF</a></p>' if PDF.exists() else ''
    rel_zip = DIST / "scripturemon_release_latest.zip"
    rel_link = f'<p><strong>Release:</strong> <a href="../dist/scripturemon_release_latest.zip">Download Release ZIP</a></p>' if rel_zip.exists() else ''
    html = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"/>
<title>Scripturemon — Compression & Telepathy Report</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,'Helvetica Neue',Arial,sans-serif; margin:24px; line-height:1.45}}
h1,h2,h3{{margin: 0.6em 0 0.3em}}
table{{border-collapse:collapse; width:100%; margin:12px 0; font-size:14px}}
th,td{{border:1px solid #ddd; padding:6px 8px; vertical-align:top}}
th{{background:#f7f7f7; text-align:left}}
code{{background:#f2f2f2; padding:2px 4px; border-radius:4px}}
.small{{color:#666; font-size:13px}}
hr{{border:none; border-top:1px solid #eee; margin:24px 0}}
</style>
</head><body>
<h1>Scripturemon — Unified Report</h1>
{pdf_link}{rel_link}
<p class="small">This report aggregates compression benchmarks and telepathy v2 results. All data pulled from <code>results/</code> and figures from <code>reports/figures/</code>.</p>
{''.join(sections)}
<hr/>
<p class="small">Generated by <code>scripts/generate_report_html.py</code></p>
</body></html>"""
    (REPORTS / "index.html").write_text(html, encoding="utf-8")
    print("[OK] HTML report -> reports/index.html")

if __name__ == "__main__":
    main()