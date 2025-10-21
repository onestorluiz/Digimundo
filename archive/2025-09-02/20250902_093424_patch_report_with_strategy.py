#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Injeta um painel 'Production Strategy' no reports/index.html.
Le fontes: reports/compression_strategy.json, configs/prod.make.inc,
configs/bench_default.env/json e o TPD default aplicado.
Idempotente: substitui seção existente (id='production-strategy') se houver.
"""
from __future__ import annotations
import json, re, os, hashlib, glob, csv
from pathlib import Path
import sys; sys.path.insert(0, '.')
from scripts.embed_minicharts import sparkline, hbars, hist, heatmap_grid
from scripts.aggregate_perf import rollup as _perf_rollup
from datetime import datetime

ROOT = Path(".")
REPORTS = ROOT / "reports"
HTML = REPORTS / "index.html"
CONF = ROOT / "configs"
DEF_TPD = ROOT / "data/tpd/default/token_dict.json"

def sha256(path: Path) -> str:
    try:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(131072), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""

def load_json(path: Path) -> dict:
    if not path.exists(): return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def load_env(path: Path) -> dict:
    env = {}
    if not path.exists(): return env
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            k,v = line.split("=",1)
            env[k.strip()] = v.strip()
    except Exception:
        pass
    return env

def load_inc(path: Path) -> dict:
    data = {"PROD_TARGETS": []}
    if not path.exists(): return data
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("PROD_TARGETS") and ":=" in line:
                vals = line.split(":=",1)[1].strip().split()
                data["PROD_TARGETS"] = vals
            m = re.match(r"export\s+(\w+)\s*:=\s*(.+)$", line)
            if m:
                data[m.group(1)] = m.group(2)
    except Exception:
        pass
    return data

def render_panel(ctx: dict) -> str:
    # CSS mínimo inline para manter independência do gerador
    style = (
        "border:1px solid #e5e7eb;padding:12px 14px;border-radius:10px;"
        "margin:18px 0;background:#fafafa"
    )
    code = lambda s: f"<code>{s}</code>" if s else "<em>n/a</em>"
    bullets = " ".join(f"<code>{t}</code>" for t in ctx.get("prod_targets",[])[:10]) or "<em>n/a</em>"
    tpd_id = ctx.get("tpd_id") or "n/a"
    tpd_dst = ctx.get("tpd_dest") or "n/a"
    tpd_src = ctx.get("tpd_src") or "n/a"
    tpd_sha = ctx.get("tpd_sha")
    tpd_sha_short = (tpd_sha[:12]+"…") if tpd_sha else "n/a"
    applied_at = ctx.get("applied_at") or "n/a"
    mode = ctx.get("mode") or "n/a"
    canon = ctx.get("canon") or "n/a"
    pres = ctx.get("preserve") or "n/a"
    ovs  = ctx.get("overlay") or "n/a"
    gen_at = datetime.utcnow().isoformat()+"Z"
    persona = ctx.get("persona") or {}
    persona_name = persona.get("name") or "n/a"
    persona_brief = (persona.get("tagline") or persona.get("summary") or "")[:160]
    rt_mode = ctx.get("runtime_mode","n/a")
    cons = ctx.get("consciousness", {}).get("level", "n/a")
    memc = ctx.get("memory_counts", {})

    return f"""
<section id="production-strategy" style="{style}">
  <h2 style="margin:0 0 8px 0">Production Strategy</h2>
  <table style="width:100%;border-collapse:collapse">
    <tr><th style="text-align:left;padding:4px 6px;width:220px">Mode</th><td style="padding:4px 6px">{code(mode)}</td></tr>
    <tr><th style="text-align:left;padding:4px 6px">Canon default</th><td style="padding:4px 6px">{code(canon)}</td></tr>
    <tr><th style="text-align:left;padding:4px 6px">Preserve headers</th><td style="padding:4px 6px">{code(pres)}</td></tr>
    <tr><th style="text-align:left;padding:4px 6px">Overlay scope</th><td style="padding:4px 6px">{code(ovs)}</td></tr>
    <tr><th style="text-align:left;padding:4px 6px">PROD_TARGETS</th><td style="padding:4px 6px">{bullets}</td></tr>
    <tr><th style="text-align:left;padding:4px 6px">TPD (id → dest)</th><td style="padding:4px 6px">{code(tpd_id)} → {code(tpd_dst)}</td></tr>
    <tr><th style="text-align:left;padding:4px 6px">TPD source</th><td style="padding:4px 6px">{code(tpd_src)}</td></tr>
    <tr><th style="text-align:left;padding:4px 6px">TPD sha256</th><td style="padding:4px 6px">{code(tpd_sha_short)}</td></tr>
    <tr><th style="text-align:left;padding:4px 6px">Runtime Mode</th><td style="padding:4px 6px">{code(rt_mode)}</td></tr>
    <tr><th style="text-align:left;padding:4px 6px">Consciousness</th><td style="padding:4px 6px">{cons}</td></tr>
    <tr><th style="text-align:left;padding:4px 6px">Memory L1-L4</th><td style="padding:4px 6px">{memc}</td></tr>
    <tr><th style="text-align:left;padding:4px 6px">Applied at</th><td style="padding:4px 6px">{applied_at}</td></tr>
    <tr><th style="text-align:left;padding:4px 6px">Persona</th><td style="padding:4px 6px"><strong>{persona_name}</strong> — {persona_brief}</td></tr>
  </table>
  <p style="margin:8px 0 0 0;color:#6b7280;font-size:12px">
    Auto‑gerado em {gen_at} a partir de <code>reports/compression_strategy.json</code>, 
    <code>configs/prod.make.inc</code> e <code>configs/bench_default.*</code>.
  </p>
</section>
<section id="ultimate-ui" style="{style}">
  <h2 style="margin:8px 0">Ultimate · Mini‑dash</h2>
  <div style="display:flex;gap:16px;flex-wrap:wrap">
    <div style="min-width:240px">
      <h3 style="margin:6px 0;font-size:14px">Consciência (sparkline)</h3>
      {ctx.get("cons_spark_svg","<em>n/a</em>")}
    </div>
    <div style="min-width:240px">
      <h3 style="margin:6px 0;font-size:14px">Memória L1‑L4 (contagens)</h3>
      {ctx.get("mem_bars_svg","<em>n/a</em>")}
    </div>
    <div style="min-width:260px">
      <h3 style="margin:6px 0;font-size:14px">Compressão — reduction (hist)</h3>
      {ctx.get("reduction_hist_svg","<em>n/a</em>")}
    </div>
  </div>
  <div style="margin-top:8px">
    <h3 style="margin:6px 0;font-size:14px">Telepatia — últimos eventos</h3>
    {ctx.get("telepathy_table_html","<em>sem dados</em>")}
  </div>
</section>
<section id="ultimate-performance" style="{style}">
  <h2 style="margin:8px 0">Ultimate · Performance</h2>
  <div style="display:flex;gap:16px;flex-wrap:wrap">
    <div style="min-width:240px">
      <h3 style="margin:6px 0;font-size:14px">Latência (ms)</h3>
      {ctx.get("perf_latency_svg","<em>n/a</em>")}
    </div>
    <div style="min-width:240px">
      <h3 style="margin:6px 0;font-size:14px">Throughput (req/s)</h3>
      {ctx.get("perf_rps_svg","<em>n/a</em>")}
    </div>
  </div>
</section>
<section id="ultimate-grid" style="{style}">
  <h2 style="margin:8px 0">Ultimate · Dataset × Modo</h2>
  <div style="min-width:260px">
    <h3 style="margin:6px 0;font-size:14px">Redução média (%)</h3>
    {ctx.get("grid_svg","<em>n/a</em>")}
  </div>
</section>
""".strip()

def inject(html: str, panel: str) -> str:
    # substitui seção existente
    rx = re.compile(r'<section id="production-strategy"[\s\S]*?</section>', re.I)
    if rx.search(html):
        return rx.sub(panel, html, count=1)
    # injeta antes de </main>, senão antes de </body>, senão anexa
    for tag in ("</main>", "</body>"):
        i = html.lower().find(tag)
        if i != -1:
            return html[:i] + panel + "\n" + html[i:]
    return html + "\n" + panel + "\n"

def inject_menu_link(html: str) -> str:
    # já existe link?
    if re.search(r'href=["\']#production-strategy["\']', html, re.I):
        return html
    # 1) Tentativa: <nav id="toc"> com <ul>…</ul>
    m = re.search(r'(<nav[^>]*id=["\']toc["\'][^>]*>)([\s\S]*?)(</nav>)', html, re.I)
    if m:
        inner = m.group(2)
        # se houver <ul>, injeta <li>
        if re.search(r'<ul[^>]*>', inner, re.I):
            html = re.sub(
                r'(<nav[^>]*id=["\']toc["\'][^>]*>[\s\S]*?<ul[^>]*>)([\s\S]*?)(</ul>)',
                r'\1\2<li><a href="#production-strategy">Production Strategy</a></li>\3',
                html, count=1, flags=re.I
            )
            return html
        # senão, adiciona um <a> antes de </nav>
        return re.sub(r'(</nav>)',
                      r'<a href="#production-strategy">Production Strategy</a>\n\1',
                      html, count=1, flags=re.I)
    # 2) Qualquer <nav> genérico: adiciona um <a> antes do fechamento do primeiro </nav>
    if re.search(r'</nav>', html, re.I):
        return re.sub(r'(</nav>)',
                      r'<a href="#production-strategy">Production Strategy</a>\n\1',
                      html, count=1, flags=re.I)
    # 3) <div id="toc"> (TOC em div)
    if re.search(r'(<div[^>]*id=["\']toc["\'][^>]*>)', html, re.I):
        return re.sub(r'(<div[^>]*id=["\']toc["\'][^>]*>)',
                      r'\1<a href="#production-strategy">Production Strategy</a>',
                      html, count=1, flags=re.I)
    # 4) Fallback: cria mini‑nav antes de <main>, ou no topo do <body>
    mini = (
        '<nav id="strategy-nav" '
        'style="font-size:14px;padding:6px 8px;background:#111827;color:#e5e7eb;'
        'border-radius:8px;margin:12px 0;">'
        '<a href="#production-strategy" '
        'style="color:#93c5fd;text-decoration:none;margin-right:12px;">'
        'Production Strategy</a></nav>\n'
    )
    m = re.search(r'<main[^>]*>', html, re.I)
    if m:
        i = m.start()
        return html[:i] + mini + html[i:]
    m = re.search(r'<body[^>]*>', html, re.I)
    if m:
        i = m.end()
        return html[:i] + "\n" + mini + html[i:]
    # último recurso: prefixa no início
    return mini + html

def inject_sidebar_link(html: str) -> str:
    """
    Injeta link no menu lateral (TOC/aside) de forma idempotente.
    Alvos:
      - <aside id|class="toc|sidebar|sidenav|menu"> ... </aside>
      - <nav  id|class="toc"> ... </nav>
      - <aside> que contenha termos de figuras (figure/figures/gráficos/plots)
    Preferimos inserir dentro do primeiro <ul> como <li>, senão um <a> no topo.
    """
    # Já existe link em qualquer lugar?
    if re.search(r'href=["\']#production-strategy["\']', html, re.I):
        return html

    # 1) Tenta <aside ... class|id=(toc|sidebar|sidenav|menu)>
    aside_rx = re.compile(r'(<aside[^>]*?(?:id|class)=["\'][^"\']*(?:toc|sidebar|sidenav|menu)[^"\']*["\'][^>]*>)([\s\S]*?)(</aside>)', re.I)
    m = aside_rx.search(html)
    if not m:
        # 2) Tenta <nav ... class|id=toc>
        nav_toc_rx = re.compile(r'(<nav[^>]*?(?:id|class)=["\'][^"\']*toc[^"\']*["\'][^>]*>)([\s\S]*?)(</nav>)', re.I)
        m = nav_toc_rx.search(html)
    if not m:
        # 3) Tenta qualquer <aside> cujo conteúdo sugira seção de figuras/artefatos
        aside_any_rx = re.compile(r'(<aside[^>]*>)([\s\S]*?)(</aside>)', re.I)
        for mm in aside_any_rx.finditer(html):
            inner_lc = mm.group(2).lower()
            if any(t in inner_lc for t in ["figure", "figures", "gráfico", "gráficos", "plot", "plots", "artefacts", "artifacts"]):
                m = mm
                break
    if not m:
        return html  # sem aside/TOC detectado; nada a fazer

    head, inner, tail = m.groups()
    # Não duplicar se já houver link
    if re.search(r'href=["\']#production-strategy["\']', inner, re.I):
        return html

    # Se houver <ul>, inserir <li> antes de </ul>
    if re.search(r'<ul[^>]*>', inner, re.I):
        new_inner = re.sub(
            r'(<ul[^>]*>)([\s\S]*?)(</ul>)',
            r'\1\2<li><a href="#production-strategy">Production Strategy</a></li>\3',
            inner, count=1, flags=re.I
        )
    else:
        # Sem <ul>: adiciona anchor simples no topo do container
        new_inner = f'<a href="#production-strategy">Production Strategy</a>\n' + inner

    start, end = m.span()
    return html[:start] + head + new_inner + tail + html[end:]

def main():
    if not HTML.exists():
        print("[SKIP] reports/index.html not found"); return
    strat = load_json(REPORTS/"compression_strategy.json")
    env   = load_env(CONF/"bench_default.env")
    mfst  = load_json(CONF/"bench_default.json")
    inc   = load_inc(CONF/"prod.make.inc")
    from apps.scripturemon.persona import get_active as _persona_get

    ctx = {
        "mode": (strat.get("recommendation") or {}).get("mode"),
        "prod_targets": inc.get("PROD_TARGETS", []),
        "canon": inc.get("DL_CANON_MODE") or env.get("DL_CANON_MODE"),
        "preserve": inc.get("DL_PRESERVE_HEADERS") or env.get("DL_PRESERVE_HEADERS"),
        "overlay": inc.get("OVERLAY_SCOPE") or env.get("OVERLAY_SCOPE"),
        "tpd_id": (mfst.get("tpd") or {}).get("id"),
        "tpd_src": (mfst.get("tpd") or {}).get("source_path"),
        "tpd_dest": (mfst.get("tpd") or {}).get("dest_path") or str(DEF_TPD),
        "applied_at": (mfst.get("applied_at") or ""),
        "tpd_sha": sha256(Path((mfst.get("tpd") or {}).get("dest_path") or DEF_TPD))
    }
    ctx["persona"] = _persona_get()
    # Runtime mode: env ou arquivo
    rt = (os.environ.get("SCRIPTUREMON_MODE") or "").strip()
    if not rt:
        mp = Path("configs/scripturemon.mode")
        if mp.exists():
            try: rt = mp.read_text(encoding="utf-8").strip()
            except: rt = ""
    ctx["runtime_mode"] = rt or "fusion"
    # ultimate status (leve)
    try:
        from apps.scripturemon.consciousness import read as _cread
        from apps.scripturemon.membridge import counts as _m_counts
        ctx["consciousness"] = _cread()
        ctx["memory_counts"] = _m_counts()
    except Exception:
        ctx["consciousness"] = {}
        ctx["memory_counts"] = {}

    # -- Ultimate UI+: carregar dados e gerar SVG inline ----------------------
    # 1) Histórico para sparkline de Consciência
    hist_csv = Path("reports/history/ultimate.csv")
    cons_vals=[]
    if hist_csv.exists():
        try:
            import csv
            with hist_csv.open("r", encoding="utf-8") as f:
                rd=csv.DictReader(f)
                for r in rd:
                    try: cons_vals.append(float(r.get("level") or 0))
                    except: pass
        except Exception: pass
    if not cons_vals and ctx.get("consciousness",{}).get("level") is not None:
        cons_vals=[float(ctx["consciousness"]["level"])]
    ctx["cons_spark_svg"]=sparkline(cons_vals) if cons_vals else ""

    # 2) Barras L1-L3
    mc=ctx.get("memory_counts",{})
    labels=["L1","L2","L3"]; values=[float(mc.get("L1",0)), float(mc.get("L2",0)), float(mc.get("L3",0))]
    ctx["mem_bars_svg"]=hbars(labels, values)

    # 3) Hist de reduction (results/compression/*.csv)
    reductions=[]
    for p in glob.glob("results/compression/*.csv"):
        try:
            import pandas as _pd
            df=_pd.read_csv(p)
            col = "reduction" if "reduction" in df.columns else None
            if col: reductions += [float(x) for x in df[col].dropna().tolist()]
        except Exception:
            # fallback csv simples
            try:
                with open(p,"r",encoding="utf-8") as f:
                    head=f.readline()
                    if "reduction" in head:
                        idx=head.strip().split(",").index("reduction")
                        for line in f:
                            xs=line.strip().split(",")
                            if len(xs)>idx:
                                try: reductions.append(float(xs[idx]))
                                except: pass
            except: pass
    ctx["reduction_hist_svg"]=hist(reductions) if reductions else ""

    # 4) Telepatia — tabela curta dos últimos CSVs
    tel_rows=[]
    for p in sorted(glob.glob("results/telepathy/*.csv"))[-2:]:
        try:
            with open(p,"r",encoding="utf-8") as f:
                head=f.readline().strip().split(",")
                for i,line in enumerate(f):
                    if i>9: break
                    vals=line.strip().split(",")
                    tel_rows.append(dict(zip(head, vals)))
        except: pass
    if tel_rows:
        # monta HTML mínimo
        cols = list(tel_rows[0].keys())
        th = "".join(f"<th>{c}</th>" for c in cols[:4])
        trs=[]
        for r in tel_rows[:10]:
            tds="".join(f"<td>{(r.get(c,'') or '')[:32]}</td>" for c in cols[:4])
            trs.append(f"<tr>{tds}</tr>")
        ctx["telepathy_table_html"]=f"<table style='font-size:11px;border-collapse:collapse'><thead><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table>"
    else:
        ctx["telepathy_table_html"]=""

    # 5) Performance rollup -> sparklines
    try:
        perf=_perf_rollup()
        lat = [float(x) for x in perf.get("latency_ms", []) if x is not None]
        rps = [float(x) for x in perf.get("throughput_rps", []) if x is not None]
        ctx["perf_latency_svg"] = sparkline(lat) if lat else ""
        ctx["perf_rps_svg"]     = sparkline(rps) if rps else ""
    except Exception:
        ctx["perf_latency_svg"] = ctx["perf_rps_svg"] = ""

    # 6) Grid dataset×modo (reductions %) a partir de results/compression/*.csv
    #    Tenta usar colunas 'dataset' e 'ablation'; se ausentes, infere do nome do arquivo.
    ds_map = {}   # (dataset -> {ablation -> [pct...]})
    for p in glob.glob("results/compression/*.csv"):
        try:
            with open(p,"r",encoding="utf-8") as f:
                rd=csv.DictReader(f)
                # inferência branda
                dataset = "screenplay_synth" if "screenplay" in p else ("original" if "original" in p else "mixed")
                for row in rd:
                    abl = row.get("ablation") or "canon+tpd"
                    if "dataset" in row and row["dataset"]: dataset = row["dataset"]
                    red = row.get("reduction")
                    if red is None or red=="": continue
                    try:
                        pct = float(red)*100.0
                        ds_map.setdefault(dataset, {}).setdefault(abl, []).append(pct)
                    except: pass
        except Exception:
            pass
    if ds_map:
        ys = sorted(ds_map.keys())
        xs = sorted({a for m in ds_map.values() for a in m.keys()})
        grid = []
        for y in ys:
            row=[]
            for x in xs:
                vals = ds_map.get(y,{}).get(x,[])
                v = sum(vals)/len(vals) if vals else 0.0
                row.append(v)
            grid.append(row)
        ctx["grid_svg"] = heatmap_grid(xs, ys, grid)
    else:
        ctx["grid_svg"] = ""

    # 7) Preferências de UX: default refresh e âncora
    try:
        ctx["ux_default_refresh"] = _ui_get_live()
    except Exception:
        ctx["ux_default_refresh"] = "off"
    try:
        ctx["ux_default_anchor"] = _ui_get_anchor()
    except Exception:
        ctx["ux_default_anchor"] = ""

    # 5) Garantir link no menu
    try:
        html = Path("reports/index.html").read_text(encoding="utf-8", errors="ignore")
        if "#ultimate-ui" not in html:
            # a própria função de patch já vai inserir a seção; aqui só marcamos o link
            pass
    except Exception:
        pass

    panel = render_panel(ctx)

    html = HTML.read_text(encoding="utf-8", errors="ignore")
    new_html = inject(html, panel)
    new_html2 = inject_menu_link(new_html)
    new_html3 = inject_sidebar_link(new_html2)
    
    # 8) Injetar JS utilitário no final do documento
    #    - Se não houver hash, aplica âncora padrão (se existir)
    #    - Adiciona botão "Copiar URL" ao <nav> (inclui refresh default e hash)
    inject_ux = f"""
<script id="script-ux-panel">
(function() {{
  try {{
    var DEF_ANCHOR = {json.dumps(ctx.get("ux_default_anchor",""))};
    var DEF_REFRESH = {json.dumps(ctx.get("ux_default_refresh","off"))};
    if (!location.hash && DEF_ANCHOR) {{
      var a = DEF_ANCHOR.startsWith("#") ? DEF_ANCHOR : ("#" + DEF_ANCHOR);
      location.hash = a;
    }}
    var nav = document.querySelector("nav") || document.body;
    var btn = document.createElement("button");
    btn.textContent = "Copiar URL";
    btn.style.cssText = "margin-left:8px;padding:4px 8px;font:12px system-ui;border-radius:6px;border:1px solid #ccc;background:#f6f6f6;cursor:pointer";
    btn.onclick = function() {{
      try {{
        var url = new URL(window.location.href);
        // aplica refresh default se não houver override na query
        if (!url.searchParams.get("refresh") && DEF_REFRESH && DEF_REFRESH !== "off") {{
          url.searchParams.set("refresh", DEF_REFRESH);
        }}
        // mantém hash atual
        var txt = url.toString();
        if (navigator.clipboard && navigator.clipboard.writeText) {{
          navigator.clipboard.writeText(txt).then(function() {{
            btn.textContent="Copiado!"; setTimeout(function(){{btn.textContent="Copiar URL";}}, 1200);
          }}).catch(function(){{ console.warn("clipboard fail"); }});
        }} else {{
          prompt("Copie a URL:", txt);
        }}
      }} catch(e) {{ console.warn(e); }}
    }};
    nav.appendChild(btn);
  }} catch(e) {{ console.warn("[ux-panel]", e); }}
}})();
</script>
"""
    
    if "script-ux-panel" not in new_html3:
        if "</body>" in new_html3.lower():
            new_html3 = re.sub(r"</body>", inject_ux + "\n</body>", new_html3, flags=re.I)
        else:
            new_html3 = new_html3 + "\n" + inject_ux
    
    if new_html3 != html:
        HTML.write_text(new_html3, encoding="utf-8")
        print("[OK] strategy panel+menu+sidebar -> reports/index.html")
    else:
        print("[OK] strategy panel (no changes)")

if __name__ == "__main__":
    main()