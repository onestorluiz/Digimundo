from __future__ import annotations
import os, json, time, html
from pathlib import Path
from typing import List, Dict, Any

CSS = """
:root { --fg:#e5e7eb; --bg:#0b0f17; --muted:#94a3b8; --ok:#22c55e; --bad:#ef4444; --card:#0f172a; }
*{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--fg);font-family:system-ui,-apple-system,Segoe UI,Roboto,Inter,Arial}
header,footer{padding:16px;border-bottom:1px solid #1f2937}
h1{font-size:18px;margin:0} .muted{color:var(--muted);font-size:12px}
main{padding:16px;display:grid;gap:12px}
.card{background:var(--card); border:1px solid #1f2937; border-radius:10px; padding:12px}
.row{display:flex; gap:8px; align-items:center; flex-wrap:wrap}
.badge{padding:2px 6px; border:1px solid #1f2937; border-radius:999px; font-size:11px; color:var(--muted)}
.q{font-size:14px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:60vw}
.mixbar{height:6px; background:linear-gradient(90deg,#7dd3fc,#38bdf8); border-radius:4px; display:inline-block}
a{color:#93c5fd; text-decoration:none}
"""

def _home()->Path: return Path(os.environ.get("SCRIPTUREMON_HOME","."))
def _log()->Path: return _home()/ "runtime" / "logs" / "obs.jsonl"
def _outdir()->Path:
    p = _home()/ "reports" / "timeline"; p.mkdir(parents=True, exist_ok=True); return p

def _read_obs(N:int=200)->List[Dict[str,Any]]:
    p=_log()
    if not p.exists(): return []
    rows=[]
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            try: rows.append(json.loads(line))
            except: pass
    return rows[-N:]

def _fmt_ts(ts:float)->str:
    try:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
    except: return "—"

def build_timeline()->Path:
    outdir=_outdir()
    rows=_read_obs()
    cards=[]
    for r in rows:
        q = html.escape((r.get("q") or "")[:180])
        ts = _fmt_ts(r.get("ts", 0.0))
        models = r.get("models") or []
        weights = r.get("weights") or []
        mix = " | ".join(f"{m}:{w:.2f}" for m,w in zip(models,weights)) if models and weights else "—"
        cites = len(r.get("evi") or [])
        qscore = r.get("qscore") or ""
        cards.append(f'''
        <div class="card">
          <div class="row"><div class="badge">{ts}</div><div class="badge">cites:{cites}</div><div class="badge">mix:{html.escape(mix)}</div></div>
          <div class="q">{q}</div>
        </div>''')
    html_doc=f'''<!doctype html><html><head><meta charset="utf-8"/><title>Scripturemon — Timeline</title>
<style>{CSS}</style></head><body>
<header><h1>Scripturemon — Timeline</h1><div class="muted">Últimas {len(rows)} interações</div></header>
<main>{''.join(cards) or '<div class="muted">sem eventos (obs.jsonl vazio)</div>'}</main>
<footer class="muted">Gerado por Scripturemon — timeline.</footer>
</body></html>'''
    out = outdir/"index.html"
    out.write_text(html_doc, encoding="utf-8")
    return out