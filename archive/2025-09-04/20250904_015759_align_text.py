from __future__ import annotations
from pathlib import Path
import html, re
from typing import List, Dict
from .beats_detect import detect_beats

def annotate_beats(raw_text:str)->str:
    if not raw_text: return ""
    beats = detect_beats(raw_text)
    # Inserir cabeçalho antes da cena alvo (heurística simples por índice)
    # Em fallback, marca com um cabeçalho de comentário.
    lines = raw_text.splitlines()
    idx2mark = {b["idx"]:"[[BEAT:{}]]".format(b["beat"]) for b in beats}
    out=[]
    sc_idx=-1
    for ln in lines:
        if re.match(r'^\s*(INT\.|EXT\.|INT/EXT\.)', ln):
            sc_idx += 1
            if sc_idx in idx2mark:
                out.append(idx2mark[sc_idx])
        out.append(ln)
    return "\n".join(out)

def export_annotated(session, annotated:str)->Dict[str,Path]:
    home = Path(getattr(session,"home","."))
    outdir = home/"reports"/"insights"
    outdir.mkdir(parents=True, exist_ok=True)
    txt = outdir/"annotated_beats.txt"
    htmlp = outdir/"annotated_beats.html"
    txt.write_text(annotated, encoding="utf-8")
    # HTML leve
    esc = html.escape(annotated).replace("[[BEAT:","<mark>[[BEAT:").replace("]]","]]</mark>")
    htmlp.write_text(f"<!doctype html><meta charset='utf-8'><pre>{esc}</pre>", encoding="utf-8")
    return {"txt":txt,"html":htmlp}