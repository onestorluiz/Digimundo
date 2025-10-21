#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bench com overlay de codebook por arquivo: mapeia top-N nomes (CAIXA ALTA) para glifos curtos.
Gera results/compression/benchmark_overlay.csv (reductions).
"""
from __future__ import annotations
import re, csv, json, argparse
from pathlib import Path
import tiktoken
from collections import Counter
from src.digilang.canon_strict import canon_strict
from src.digilang.encoder import DigiLangEncoder

UP = re.compile(r"^[A-Z][A-Z0-9 '\.-]{1,17}$")
GLYPHS=[ "§"+c for c in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") ]

def find_names(text:str, k:int=8):
    c=Counter()
    for l in text.upper().splitlines():
        s=l.strip()
        if UP.match(s) and s not in {"INT.","EXT.","CUT TO:","FADE IN:","CUT TO","FADE IN"}:
            c[s]+=1
    return [n for n,_ in c.most_common(k)]

def build_overlay(names:list):
    m={}
    for i,n in enumerate(names):
        if i<len(GLYPHS): m[n]=GLYPHS[i]
    return m

def apply_overlay(text:str, m:dict):
    t=text
    for k,v in m.items():
        t = t.replace(k, v)
    return t

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data_dir", default="data/screenplay_synth")
    ap.add_argument("--tpd_path", default="data/tpd/default/token_dict.json")
    ap.add_argument("--max_files", type=int, default=10)
    ap.add_argument("--max_chars", type=int, default=60000)
    ap.add_argument("--topn", type=int, default=8)
    args=ap.parse_args()

    enc = tiktoken.get_encoding("cl100k_base")
    tok = lambda s: len(enc.encode(s))
    files_all=sorted(Path(args.data_dir).rglob("*.txt"))
    files=files_all[:args.max_files] if args.max_files and len(files_all)>args.max_files else files_all

    encdr = DigiLangEncoder(use_tpd=True, token_dict_path=args.tpd_path, tpd_policy="per_work")

    rows=[]
    for p in files:
        raw=p.read_text(encoding="utf-8", errors="ignore")
        if args.max_chars and len(raw)>args.max_chars: raw=raw[:args.max_chars]
        base = canon_strict(raw)
        names = find_names(base, k=args.topn)
        overlay = build_overlay(names)
        base_ov = apply_overlay(base, overlay)
        comp,_ = encdr.encode(base_ov, preserve_headers=False)
        rows.append(dict(file=str(p), before=tok(base), after=tok(comp), reduction=1.0 - tok(comp)/max(1,tok(base)), names=len(names)))
    out=Path("results/compression"); out.mkdir(parents=True, exist_ok=True)
    with (out/"benchmark_overlay.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=["file","before","after","reduction","names"]); w.writeheader()
        for r in rows: w.writerow(r)
    print("[OK] overlay bench -> results/compression/benchmark_overlay.csv (mean_reduction=%.4f)" % (sum(r["reduction"] for r in rows)/len(rows) if rows else 0.0))

if __name__=="__main__":
    main()