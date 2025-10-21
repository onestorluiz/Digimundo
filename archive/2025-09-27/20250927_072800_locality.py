
import json
from pathlib import Path
def locality_metrics(run_dir: Path) -> dict:
    beats_meta = json.loads((run_dir / "beats_meta.json").read_text(encoding="utf-8")) if (run_dir / "beats_meta.json").exists() else {}
    total = int(beats_meta.get("total_beats", 0))
    idxs = set()
    for f in run_dir.glob("retrieval_*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        for b in d.get("rag_blocks", []):
            if b.startswith("[beat:"):
                head = b.split("]",1)[0].strip("[")
                bid = head.split(":",1)[1].replace("beat_","")
                idx = beats_meta.get("index_map", {}).get(bid) or beats_meta.get("index_map", {}).get(bid.replace("dyn_","dyn_"))
                if idx is not None:
                    idxs.add(int(idx))
    sel = sorted(list(idxs))
    if not sel:
        return {"locality_coherence": 0.0, "avg_gap": None, "selected": []}
    gaps = [sel[i+1]-sel[i] for i in range(len(sel)-1)]
    avg_gap = sum(gaps)/max(1,len(gaps)) if gaps else 0.0
    coh = 1.0 / (1.0 + avg_gap)
    return {"locality_coherence": round(coh,3), "avg_gap": round(avg_gap,3), "selected": sel}
def write_timeline_html(run_dir: Path) -> str:
    beats_meta = json.loads((run_dir / "beats_meta.json").read_text(encoding="utf-8"))
    total = int(beats_meta.get("total_beats", 0))
    by_scene = beats_meta.get("by_scene", {})
    sel = set()
    for f in run_dir.glob("retrieval_*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        for b in d.get("rag_blocks", []):
            if b.startswith("[beat:"):
                head = b.split("]",1)[0].strip("[")
                bid = head.split(":",1)[1].replace("beat_","")
                idx = beats_meta.get("index_map", {}).get(bid) or beats_meta.get("index_map", {}).get(bid.replace("dyn_","dyn_"))
                if idx is not None:
                    sel.add(int(idx))
    row_h=24; cell_w=10; pad=8
    scenes = sorted({int(k) for k in by_scene.keys()})
    h = pad*2 + row_h*max(1,len(scenes))
    w = pad*2 + 60 + cell_w*max(1,total)
    svg = [f"<svg width='{w}' height='{h}' xmlns='http://www.w3.org/2000/svg'>"]
    y=pad
    for s in scenes:
        svg.append(f"<text x='{4}' y='{y+14}' font-size='10' fill='#555'>Cena {s}</text>")
        for entry in by_scene[str(s)]:
            i = int(entry["global_index"])
            x = pad + 60 + i*cell_w
            fill = "#5b8ff9" if i in sel else "#e8ecf5"
            svg.append(f"<rect x='{x}' y='{y}' width='{cell_w-1}' height='{row_h-4}' fill='{fill}'/>")
        y += row_h
    svg.append("</svg>")
    html = ("<!doctype html><meta charset='utf-8'><title>Timeline</title>"
            "<style>body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:24px}</style>"
            "<h1>Timeline — Beats por Cena</h1>" + "".join(svg))
    out = run_dir / "timeline.html"
    out.write_text(html, encoding="utf-8")
    return str(out)
def write_timeline_specialists_html(run_dir: Path) -> str:
    beats_meta = json.loads((run_dir / "beats_meta.json").read_text(encoding="utf-8"))
    total = int(beats_meta.get("total_beats", 0))
    by_spec = {}
    for f in run_dir.glob("retrieval_*.json"):
        spec = f.stem.split("_",1)[1]
        d = json.loads(f.read_text(encoding="utf-8"))
        sel = set()
        for b in d.get("rag_blocks", []):
            if b.startswith("[beat:"):
                head = b.split("]",1)[0].strip("[")
                bid = head.split(":",1)[1].replace("beat_","")
                idx = beats_meta.get("index_map", {}).get(bid)
                if idx is not None:
                    sel.add(int(idx))
        by_spec[spec] = sorted(list(sel))
    row_h=22; cell_w=8; pad=8
    specs = sorted(by_spec.keys())
    h = pad*2 + row_h*max(1,len(specs))
    w = pad*2 + 120 + cell_w*max(1,total)
    svg = [f"<svg width='{w}' height='{h}' xmlns='http://www.w3.org/2000/svg'>"]
    y=pad
    for s in specs:
        svg.append(f"<text x='{4}' y='{y+14}' font-size='10' fill='#555'>{s}</text>")
        sel = set(by_spec[s])
        for i in range(total):
            x = pad + 120 + i*cell_w
            fill = "#5b8ff9" if i in sel else "#e8ecf5"
            svg.append(f"<rect x='{x}' y='{y}' width='{cell_w-1}' height='{row_h-4}' fill='{fill}'/>")
        y += row_h
    svg.append("</svg>")
    html = ("<!doctype html><meta charset='utf-8'><title>Timeline por Especialista</title>"
            "<style>body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:24px}</style>"
            "<h1>Timeline — Beats por Especialista</h1>" + "".join(svg))
    out = run_dir / "timeline_specialists.html"
    out.write_text(html, encoding="utf-8")
    return str(out)
def write_timeline_motifs_html(run_dir: Path) -> str:
    beats_meta = json.loads((run_dir / "beats_meta.json").read_text(encoding="utf-8"))
    total = int(beats_meta.get("total_beats", 0))
    beats_texts = json.loads((run_dir / "beats_texts.json").read_text(encoding="utf-8")) if (run_dir / "beats_texts.json").exists() else {}
    theme = json.loads((run_dir / "parsed_theme.json").read_text(encoding="utf-8")) if (run_dir / "parsed_theme.json").exists() else {}
    motifs = theme.get("payload", {}).get("motifs", []) if theme else []
    def toks(s): 
        import re
        return [t.lower() for t in re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+", s) if len(t)>2]
    rows = {}
    for m in motifs:
        mlow = m.lower()
        rows[mlow] = [0]*total
    index_map = beats_meta.get("index_map", {})
    for bid, txt in beats_texts.items():
        gi = index_map.get(bid)
        if gi is None: continue
        tset = set(toks(txt))
        for m in rows.keys():
            if any(t in tset for t in toks(m)):
                rows[m][gi] = 1
    row_h=20; cell_w=8; pad=8
    h = pad*2 + row_h*max(1,len(rows))
    w = pad*2 + 160 + cell_w*max(1,total)
    svg = [f"<svg width='{w}' height='{h}' xmlns='http://www.w3.org/2000/svg'>"]
    y=pad
    for m, arr in rows.items():
        svg.append(f"<text x='{4}' y='{y+14}' font-size='10' fill='#555'>{m}</text>")
        for i, v in enumerate(arr):
            x = pad + 160 + i*cell_w
            fill = "#5b8ff9" if v else "#e8ecf5"
            svg.append(f"<rect x='{x}' y='{y}' width='{cell_w-1}' height='{row_h-4}' fill='{fill}'/>")
        y += row_h
    svg.append("</svg>")
    html = ("<!doctype html><meta charset='utf-8'><title>Timeline por Motivos</title>"
            "<style>body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:24px}</style>"
            "<h1>Timeline — Trilhos Temáticos (Motifs)</h1>" + "".join(svg))
    out = run_dir / "timeline_motifs.html"
    out.write_text(html, encoding="utf-8")
    return str(out)
