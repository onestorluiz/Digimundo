
from pathlib import Path
import json, statistics
from .engine import analyze_screenplay, DEFAULT_FEATURES
from .config_loader import load_config
from .snippet_utils import _tokens

VARIANTS = {
    "base": {"graph_boost": False, "locality_metric": False, "lore_route": False},
    "graph_only": {"graph_boost": True, "locality_metric": False, "lore_route": False},
    "locality_only": {"graph_boost": False, "locality_metric": True, "lore_route": False},
    "graph_locality": {"graph_boost": True, "locality_metric": True, "lore_route": False},
    "full": {"graph_boost": True, "locality_metric": True, "lore_route": True},
}

def _extract_metrics(run_dir: Path) -> dict:
    from .evaluation import evaluate
    ev = json.loads((run_dir/"evaluation.json").read_text(encoding="utf-8"))
    mac = ev.get("macro", {})
    return {"quality": mac.get("quality",0.0), "faithfulness": mac.get("faithfulness",0.0), "relevancy": mac.get("relevancy",0.0), "locality": mac.get("locality_coherence",0.0)}

def _line_svg(series, title):
    w=360; h=120; pad=10
    vals = series or [0.0]
    vmax = max(vals) if vals else 1.0
    vmax = max(vmax, 1e-6)
    step = (w - 2*pad) / max(1, len(vals)-1)
    pts = []
    for i, v in enumerate(vals):
        x = pad + i*step
        y = h - pad - (v / vmax) * (h - 2*pad)
        pts.append(f"{x:.1f},{y:.1f}")
    poly = " ".join(pts)
    return f"<div><b>{title}</b><svg width='{w}' height='{h}' xmlns='http://www.w3.org/2000/svg'><polyline fill='none' stroke='#5b8ff9' stroke-width='2' points='{poly}'/></svg></div>"

def run_ablation(script_text: str) -> dict:
    cfg = load_config(); out = {}
    names=[]; sq=[]; sf=[]; sr=[]; sl=[]
    for name, feats in VARIANTS.items():
        res = analyze_screenplay(script_text, preset="enterprise", reflect=True, autofix=False, max_workers=3, report=False, features=feats)
        runs = sorted(Path(cfg["paths"]["outputs"]).glob("*/evaluation.json"))
        run_dir = runs[-1].parent
        met = _extract_metrics(run_dir)
        out[name] = {"run_id": run_dir.name, "metrics": met}
        names.append(name); sq.append(met["quality"]); sf.append(met["faithfulness"]); sr.append(met["relevancy"]); sl.append(met["locality"])
    html = ["<!doctype html><meta charset='utf-8'><title>Scripturemon — Ablation (H+++)</title><style>body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:24px;} table{border-collapse:collapse;width:100%;} th,td{padding:8px 10px;border-bottom:1px solid #eee;text-align:left;} .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;}</style>"]
    html.append("<h1>Ablation — H+++ (scene-graph & locality)</h1>")
    html.append("<table><thead><tr><th>Variant</th><th>quality</th><th>faithfulness</th><th>relevancy</th><th>locality</th></tr></thead><tbody>")
    for k,v in out.items():
        m=v["metrics"]
        html.append(f"<tr><td>{k}</td><td>{m['quality']:.2f}</td><td>{m['faithfulness']:.2f}</td><td>{m['relevancy']:.2f}</td><td>{m['locality']:.2f}</td></tr>")
    html.append("</tbody></table>")
    html.append("<div class='grid'>"+_line_svg(sq, "Quality")+_line_svg(sl, "Locality")+"</div>")
    abp = Path(cfg["paths"]["outputs"]) / "_ablation_hppp.html"
    abp.write_text("".join(html), encoding="utf-8")
    (Path(cfg["paths"]["outputs"]) / "_ablation_hppp.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"html": str(abp), "json": str(Path(cfg['paths']['outputs']) / "_ablation_hppp.json")}
