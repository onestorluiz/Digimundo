from __future__ import annotations
import os, re, html
from pathlib import Path
from typing import List, Dict, Any
from .qscore import qscore as _qscore

def _safe_id(s:str)->str:
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9]+','-', s)
    return s.strip('-') or 'k'

def _parse_ctx(ctx_text:str)->Dict[str,str]:
    """Extrai blocos [[K:...]] snippet -> {token: snippet}."""
    if not ctx_text: return {}
    blocks = {}
    for m in re.finditer(r'\[\[K:([^\]]+)\]\]\s*(.+?)(?=(\n\n\[\[K:)|\Z)', ctx_text, flags=re.S):
        token = m.group(1).strip()
        snippet = m.group(2).strip()
        blocks[token] = snippet
    return blocks

def _link_citations(text:str)->str:
    """Converte [[K:...]] em <a href="#k-...">[...]</a>."""
    def sub(m):
        token = m.group(1)
        aid = "k-" + _safe_id(token)
        label = html.escape(token)
        return f'<a class="cite" href="#{aid}">[{label}]</a>'
    return re.sub(r'\[\[K:([^\]]+)\]\]', sub, html.escape(text))

def export_overlay(session:Any, answer_text:str, ctx_text:str, ctx_cites:List[str], 
                   weights:List[float]|None, models:List[str]|None, qscore_val:float|None,
                   out_dir:Path|None=None)->Path:
    """Gera reports/overlay/index.html com overlay por Ato, citações, mix."""
    home = Path(os.environ.get("SCRIPTUREMON_HOME", Path(__file__).resolve().parents[2]))
    out_dir = out_dir or (home / "reports" / "overlay")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"

    # Sessão/segmentos (opcional)
    doc = getattr(session, "active_doc", None)
    segments = getattr(session, "segments", []) or []
    acts = {1:[],2:[],3:[]}
    for s in segments:
        a = s.get("act",2)
        acts.setdefault(a,[]).append(s)

    # Citações
    ctx_map = _parse_ctx(ctx_text or "")
    # HTML convertido
    answer_html = _link_citations(answer_text or "")
    # Model mix
    models = models or []
    weights = weights or []
    mix_rows = ""
    for name, w in zip(models, weights):
        bar = int(round(100*(w or 0.0)))
        mix_rows += f'<div class="mix-row"><span class="m">{html.escape(name)}</span><span class="bar" style="width:{bar}%;"></span><span class="pct">{bar}%</span></div>'

    # QScore
    if qscore_val is None:
        # fallback: estimar com evidências mínimas
        cites_count = sum(1 for _ in ctx_cites) if ctx_cites else 0
        qscore_val = _qscore(0.3, 0.3, 0.3, cites_count, len(answer_text or ""))

    # Build citations section
    cites_html = ""
    for token, snippet in ctx_map.items():
        aid = "k-" + _safe_id(token)
        cites_html += f'''
        <div class="cite-block" id="{aid}">
          <div class="token">[{html.escape(token)}]</div>
          <div class="snippet">{html.escape(snippet)}</div>
        </div>'''

    # Acts overview
    def _act_card(n):
        arr = acts.get(n,[])
        return f'''<div class="act-card"><h3>Act {n}</h3><div class="small">{len(arr)} segmentos</div></div>'''
    acts_html = _act_card(1) + _act_card(2) + _act_card(3)

    # Scenes (primeiras 12, se houver)
    scenes_html = ""
    for s in segments[:12]:
        txt = (s.get("text","") or "")
        scenes_html += f'<li>Act {s.get("act","?")} • scene#{s.get("idx","?")} • {len(txt)} chars</li>'

    # Minimal CSS (inline; sem libs)
    css = """
    :root { --fg:#e5e7eb; --bg:#0b0f17; --muted:#94a3b8; --accent:#7dd3fc; --green:#22c55e; --red:#ef4444; }
    * { box-sizing:border-box; }
    body { margin:0; font-family:system-ui,-apple-system,Segoe UI,Roboto,Inter,Arial; background:var(--bg); color:var(--fg); }
    header { padding:20px; border-bottom:1px solid #1f2937; }
    .title { font-size:20px; font-weight:700; }
    .muted { color:var(--muted); font-size:13px; }
    main { display:grid; grid-template-columns: 280px 1fr; gap:20px; padding:20px; }
    nav { border-right:1px solid #1f2937; padding-right:10px; }
    nav a { display:block; padding:6px 8px; color:var(--muted); text-decoration:none; border-radius:6px; }
    nav a:hover { color:var(--fg); background:#111827; }
    section { margin-bottom:26px; }
    h2 { font-size:16px; margin:10px 0; }
    .panel { background:#0f172a; border:1px solid #1f2937; border-radius:10px; padding:14px; }
    .mix-row { display:flex; align-items:center; gap:8px; margin:6px 0; }
    .mix-row .m { width:140px; font-size:13px; color:var(--muted); }
    .mix-row .bar { height:6px; background:linear-gradient(90deg, var(--accent), #38bdf8); border-radius:4px; display:inline-block; }
    .mix-row .pct { width:44px; text-align:right; font-size:12px; color:var(--muted); }
    .qscore { font-weight:700; color:var(--green); }
    .qscore.bad { color: var(--red); }
    .cite { color:#93c5fd; text-decoration:none; border-bottom:1px dotted #93c5fd; }
    .cite-block { padding:10px; border:1px solid #1f2937; border-radius:8px; margin:10px 0; background:#0b1324; }
    .cite-block .token { font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:12px; color:var(--muted); margin-bottom:6px; }
    .cite-block .snippet { white-space:pre-wrap; font-size:14px; line-height:1.35; }
    .answer { white-space:pre-wrap; line-height:1.45; }
    ul.scenes { margin:8px 0 0 18px; padding:0; }
    ul.scenes li { margin:4px 0; color:var(--muted); font-size:13px; }
    .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; }
    .act-card { background:#0b1324; border:1px solid #1f2937; border-radius:10px; padding:12px; }
    .small { color:var(--muted); font-size:12px; }
    footer { padding:20px; border-top:1px solid #1f2937; color:var(--muted); font-size:12px; }
    """

    qclass = "qscore" if qscore_val >= 60 else "qscore bad"
    doc_name = Path(doc).name if doc else "—"
    html_doc = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Scripturemon Overlay — {html.escape(doc_name)}</title>
<style>{css}</style>
</head><body>
<header>
  <div class="title">Scripturemon Overlay — {html.escape(doc_name)}</div>
  <div class="muted">QScore: <span class="{qclass}">{qscore_val}</span> • Model Mix</div>
  <div class="panel" style="margin-top:10px">{mix_rows or '<div class="small muted">no model mix available</div>'}</div>
</header>
<main>
  <nav>
    <a href="#answer">Answer</a>
    <a href="#acts">Acts Overview</a>
    <a href="#scenes">Scenes (first 12)</a>
    <a href="#citations">Citations</a>
  </nav>
  <div>
    <section id="answer">
      <h2>Answer</h2>
      <div class="panel answer">{answer_html}</div>
    </section>
    <section id="acts">
      <h2>Acts Overview</h2>
      <div class="grid">{acts_html}</div>
    </section>
    <section id="scenes">
      <h2>Scenes</h2>
      <div class="panel"><ul class="scenes">{scenes_html or '<li class="small">no segments available</li>'}</ul></div>
    </section>
    <section id="citations">
      <h2>Citations</h2>
      <div class="panel">{cites_html or '<div class="small">no citations captured</div>'}</div>
    </section>
  </div>
</main>
<footer>Generated by Scripturemon — overlay export.</footer>
</body></html>
"""
    out_path.write_text(html_doc, encoding="utf-8")
    return out_path