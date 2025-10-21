#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Grid adaptativo por arquivo:
  - canon: strict | aggressive
  - overlay: off | on (adaptativo)
Escolhe a configuração com maior redução (baseline = canon_strict(raw)).
Gera results/compression/grid_adaptive.csv e summary.
"""
from __future__ import annotations
from pathlib import Path
import argparse, csv, re, json
from collections import Counter
import tiktoken
from src.digilang.canon_strict import canon_strict
try:
    from src.digilang.canon_aggressive import canon_aggressive
except Exception:
    canon_aggressive = None
from src.digilang.encoder import DigiLangEncoder

UP = re.compile(r"^[A-Z][A-Z0-9 '\.-]{1,17}$")
GLYPHS=[ "§"+c for c in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") ]

def toklen(enc, s:str)->int: return len(enc.encode(s))

def find_names(text:str, k:int=8):
    c=Counter()
    for l in text.upper().splitlines():
        s=l.strip()
        if UP.match(s) and s not in {"INT.","EXT.","CUT TO:","FADE IN:","CUT TO","FADE IN"}:
            s = re.sub(r"\s*\((CONT'D|V\.O\.|O\.S\.)\)\s*$","",s)
            if s: c[s]+=1
    return [n for n,_ in c.most_common(k)]

def estimate(enc, base:str, names:list[str]):
    exp_tokens=0; mapping={}
    for i, n in enumerate(names):
        if i>=len(GLYPHS): break
        glyph = GLYPHS[i]
        gain = (toklen(enc, n) - toklen(enc, glyph))
        if gain>0:
            mapping[n]=glyph
            exp_tokens += gain
    return exp_tokens, mapping

def apply_overlay_linewise(text:str, mapping:dict[str,str])->str:
    out=[]
    for l in text.splitlines():
        u=l.strip().upper()
        if u in mapping:
            out.append(mapping[u])
        else:
            m = re.match(r"^([A-Z][A-Z0-9 '\.-]{1,17})\s*\((CONT'D|V\.O\.|O\.S\.)\)\s*$", u)
            if m and m.group(1) in mapping:
                out.append(mapping[m.group(1)])
            else:
                out.append(l)
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", default="data/screenplay_synth")
    ap.add_argument("--tpd_path", default="data/tpd/default/token_dict.json")
    ap.add_argument("--max_files", type=int, default=10)
    ap.add_argument("--max_chars", type=int, default=60000)
    ap.add_argument("--rel_threshold", type=float, default=0.03)
    ap.add_argument("--min_tokens", type=int, default=200)
    ap.add_argument("--legend_inline_eval", action="store_true",
                    help="calcula também redução com legenda inline para o melhor modo")
    args = ap.parse_args()

    enc = tiktoken.get_encoding("cl100k_base")
    tok = lambda s: len(enc.encode(s))
    files_all = sorted(Path(args.data_dir).rglob("*.txt"))
    files = files_all[:args.max_files] if args.max_files and len(files_all)>args.max_files else files_all

    encoder = DigiLangEncoder(use_tpd=True, token_dict_path=args.tpd_path, tpd_policy="per_work")

    rows=[]
    for p in files:
        raw = p.read_text(encoding="utf-8", errors="ignore")
        if args.max_chars and len(raw)>args.max_chars: raw = raw[:args.max_chars]

        base_strict = canon_strict(raw)
        base_aggr = canon_aggressive(raw) if canon_aggressive is not None else base_strict
        before_tok = tok(base_strict)  # baseline comum

        def eval_mode(canon_label:str, base_text:str, use_overlay:bool):
            text = base_text
            names = find_names(base_text, k=8) if use_overlay else []
            exp_gain, mapping = estimate(enc, base_text, names) if use_overlay else (0,{})
            decision = use_overlay and ((exp_gain/before_tok)>=args.rel_threshold or exp_gain>=args.min_tokens)
            if decision and mapping:
                text = apply_overlay_linewise(base_text, mapping)
            comp,_ = encoder.encode(text, preserve_headers=False)
            after = tok(comp)
            red = 1.0 - (after/max(1, before_tok))
            out = dict(after=after, reduction=red, overlay_applied=int(bool(decision and mapping)), names=len(mapping),
                       exp_gain_tokens=exp_gain, canon=canon_label)
            if args.legend_inline_eval and decision and mapping:
                legend = "#LEGEND " + "; ".join(f"{v}={k}" for k,v in mapping.items()) + "\n---\n"
                compL,_ = encoder.encode(legend + text, preserve_headers=False)
                afterL = tok(compL); out["after_inline"]=afterL
                out["reduction_inline"]=1.0 - (afterL/max(1,before_tok))
            return out

        # quatro combinações
        candidates = []
        candidates.append(("strict_noov", eval_mode("strict", base_strict, False)))
        candidates.append(("strict_ov",   eval_mode("strict", base_strict, True)))
        candidates.append(("aggr_noov",   eval_mode("aggressive", base_aggr, False)))
        candidates.append(("aggr_ov",     eval_mode("aggressive", base_aggr, True)))

        # escolhe melhor por redução
        best_key, best = max(candidates, key=lambda kv: kv[1]["reduction"])
        rows.append(dict(
            file=str(p), choice=best_key, canon=best["canon"], overlay_applied=best["overlay_applied"],
            names=best["names"], exp_gain_tokens=best["exp_gain_tokens"],
            before=before_tok, after=best["after"], reduction=best["reduction"],
            after_inline=best.get("after_inline", best["after"]),
            reduction_inline=best.get("reduction_inline", best["reduction"])
        ))

    outdir = Path("results/compression"); outdir.mkdir(parents=True, exist_ok=True)
    out = outdir/"grid_adaptive.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file","choice","canon","overlay_applied","names","exp_gain_tokens","before","after","reduction","after_inline","reduction_inline"])
        w.writeheader()
        for r in rows: w.writerow(r)

    mean = sum(r["reduction"] for r in rows)/len(rows) if rows else 0.0
    print(f"[OK] grid adaptive -> {out} (mean_reduction={mean:.4f})")

if __name__=="__main__":
    main()