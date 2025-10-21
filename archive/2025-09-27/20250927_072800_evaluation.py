
import statistics, json
from pathlib import Path
from .locality import locality_metrics
def evaluate(outputs: dict, run_dir: Path | None = None) -> dict:
    scores = []; details = {}
    for sid, data in outputs.items():
        if sid.startswith("__"): continue
        ev = data.get("evidence", {}) or {}
        has_ev = int(bool(ev.get("script_offset")) and bool(ev.get("rag_doc_id")) and bool(ev.get("baseline_metric")))
        q = float(data.get("quality", 0.0))
        faith_model = 0.5 * has_ev + 0.5 * (1.0 if q >= 0.7 else (q if q>=0 else 0.0))
        payload = data.get("payload", {}) or {}
        nonempty = sum(1 for v in payload.values() if (v is not None and v != "" and v != []))
        total = max(1, len(payload))
        relev = nonempty / total
        s = {"quality": q, "faithfulness": faith_model, "relevancy": relev}
        scores.append((sid, s)); details[sid] = s
    q_avg = statistics.fmean(s["quality"] for _, s in scores) if scores else 0.0
    f_avg_model = statistics.fmean(s["faithfulness"] for _, s in scores) if scores else 0.0
    r_avg = statistics.fmean(s["relevancy"] for _, s in scores) if scores else 0.0
    loc = locality_metrics(run_dir) if run_dir else {"locality_coherence": 0.0}
    spot = {}
    if run_dir and (run_dir / "spot_check.json").exists():
        import json as _json
        spot = _json.loads((run_dir / "spot_check.json").read_text(encoding="utf-8"))
    support = float(spot.get("support_ratio_w", spot.get("support_ratio", 0.0)))
    f_avg = 0.5*f_avg_model + 0.5*support
    prod = 0.4*(f_avg) + 0.3*(r_avg) + 0.3*(loc.get("locality_coherence",0.0) or 0.0)
    return {"macro": {"quality": q_avg, "faithfulness": f_avg, "faith_model": f_avg_model, "support_ratio": support, "relevancy": r_avg, "locality_coherence": loc.get("locality_coherence",0.0), "production_score": prod}, "details": details}
def _bar_svg(value: float, width: int = 100, height: int = 10) -> str:
    v = max(0.0, min(1.0, value)); w = int(width * v)
    return (f"<svg width='{width}' height='{height}' xmlns='http://www.w3.org/2000/svg'>"
            f"<rect x='0' y='0' width='{width}' height='{height}' fill='#f0f2f6'/>"
            f"<rect x='0' y='0' width='{w}' height='{height}' fill='#5b8ff9'/>"
            f"</svg>")
def write_html_report(path: str, inputs: dict, outputs: dict, evalres: dict, run_dir: Path):
    import json as _json
    from .locality import write_timeline_html, write_timeline_specialists_html, write_timeline_motifs_html
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    css = ("body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:24px;}"
           ".hdr{display:flex;gap:8px;align-items:center;}"
           ".kpi{padding:10px 14px;border:1px solid #eee;border-radius:10px;}"
           "pre{background:#f8f9fb;padding:12px;border-radius:8px;overflow:auto;}"
           "h2{margin-top:28px;}table{border-collapse:collapse;width:100%;}"
           "th,td{padding:8px 10px;border-bottom:1px solid #eee;text-align:left;}"
           ".sid{font-weight:600;}")
    nav = ("<div style='position:sticky;top:0;background:white;padding:8px 0;'>"
           "<a href='#scores'>Scores</a> · <a href='#local'>Coerência Local</a> · <a href='#prod'>Production</a> · <a href='#spot'>Spot‑Check</a> · <a href='#inputs'>Entradas</a> · <a href='#outputs'>Saídas</a>"
           "</div>")
    macro = evalres.get("macro", {}); rows = []
    for sid, s in evalres.get("details", {}).items():
        rows.append(
            f"<tr><td class='sid'>{sid}</td>"
            f"<td>{s['quality']:.2f}<div>"+_bar_svg(s['quality'])+"</div></td>"
            f"<td>{s['faithfulness']:.2f}<div>"+_bar_svg(s['faithfulness'])+"</div></td>"
            f"<td>{s['relevancy']:.2f}<div>"+_bar_svg(s['relevancy'])+"</div></td>"
            "</tr>"
        )
    outputs_json = _json.dumps(outputs, ensure_ascii=False, indent=2)
    inputs_json = _json.dumps(inputs, ensure_ascii=False, indent=2)
    timeline_path = write_timeline_html(run_dir)
    timeline_specs = write_timeline_specialists_html(run_dir)
    timeline_motifs = write_timeline_motifs_html(run_dir)
    html = (
        "<!doctype html><html><head><meta charset='utf-8'><title>Scripturemon Report</title>"
        f"<style>{css}</style></head><body>"
        "<div class='hdr'><h1 style='margin:0;'>Scripturemon — Execution Report (HΩ++)</h1></div>" + nav +
        "<div style='display:flex;gap:12px;margin:16px 0;'>"
        f"<div class='kpi'><b>Quality (avg)</b><div>{macro.get('quality',0.0):.2f}</div></div>"
        f"<div class='kpi'><b>Faithfulness</b><div>{macro.get('faithfulness',0.0):.2f}</div></div>"
        f"<div class='kpi'><b>Relevancy</b><div>{macro.get('relevancy',0.0):.2f}</div></div>"
        f"<div class='kpi'><b>Locality</b><div>{macro.get('locality_coherence',0.0):.2f}</div></div>"
        f"<div class='kpi'><b>Production</b><div>{macro.get('production_score',0.0):.2f}</div></div>"
        "</div>"
        "<h2 id='scores'>Scores por especialista</h2>"
        "<table><thead><tr><th>Especialista</th><th>Quality</th><th>Faithfulness</th><th>Relevancy</th></tr></thead><tbody>"
        + "".join(rows) + "</tbody></table>"
        "<h2 id='local'>Coerência Local</h2>"
        f"<p><a href='{Path(timeline_path).name}'>Timeline (beats por cena)</a> · "
        f"<a href='{Path(timeline_specs).name}'>Timeline por Especialista</a> · "
        f"<a href='{Path(timeline_motifs).name}'>Timeline por Motivos</a></p>"
        "<h2 id='spot'>Spot‑Check de Citação</h2>"
        f"<p>support_ratio (ponderado) = {macro.get('support_ratio',0.0):.2f}</p>"
        "<h2 id='prod'>Production Score</h2>"
        f"<p>production_score = 0.4*faithfulness + 0.3*relevancy + 0.3*locality = {macro.get('production_score',0.0):.2f}</p>"
        "<h2 id='inputs'>Entradas</h2><details open><summary>ver/ocultar</summary><pre>" + inputs_json + "</pre></details>"
        "<h2 id='outputs'>Saídas (JSON)</h2><details><summary>ver/ocultar</summary><pre>" + outputs_json + "</pre></details>"
        "</body></html>"
    )
    p.write_text(html, encoding="utf-8")
