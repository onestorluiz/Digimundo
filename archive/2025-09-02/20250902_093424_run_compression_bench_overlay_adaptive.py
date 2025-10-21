#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Overlay adaptativo por arquivo: estima economia de tokens ao mapear nomes
de personagem (linhas CAIXA ALTA) para glifos curtos; aplica apenas se o ganho
relativo >= threshold ou ganho absoluto >= min_tokens.
Saída: results/compression/benchmark_overlay_adaptive.csv
"""
from __future__ import annotations
import re, csv, argparse, json, os
from pathlib import Path
from collections import Counter
import tiktoken
from src.digilang.encoder import DigiLangEncoder
try:
    from src.digilang.canon_aggressive import canon_aggressive
except Exception:
    canon_aggressive = None
from src.digilang.canon_strict import canon_strict

UP = re.compile(r"^[A-Z][A-Z0-9 '\.-]{1,17}$")
# Usamos glifos curtos; se algum não for single-token, o estimador detecta
GLYPHS=[ "§"+c for c in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") ]

def toklen(enc, s:str)->int: return len(enc.encode(s))

def find_names(text:str, k:int=8):
    c=Counter()
    for l in text.upper().splitlines():
        s=l.strip()
        if UP.match(s) and s not in {"INT.","EXT.","CUT TO:","FADE IN:","CUT TO","FADE IN"}:
            s = re.sub(r"\s*\((CONT'D|V\.O\.|O\.S\.)\)\s*$","",s)
            if s: c[s]+=1
    return [(n, c[n]) for n in [n for n,_ in c.most_common(k)]]

def estimate_savings(enc, base:str, names:list[tuple[str,int]]):
    # Estima economia por substituir linhas inteiras com o nome por glifo
    exp_tokens = 0
    usable = []
    for i,(name, cnt) in enumerate(names):
        if i>=len(GLYPHS): break
        glyph = GLYPHS[i]
        before = toklen(enc, name)
        after  = toklen(enc, glyph)
        gain = (before - after) * cnt
        if gain>0:
            usable.append((name, glyph))
            exp_tokens += gain
    return exp_tokens, dict(usable)

def apply_overlay_linewise(text:str, mapping:dict[str,str])->str:
    out=[]
    for l in text.splitlines():
        u=l.strip().upper()
        if u in mapping:
            out.append(mapping[u])
        else:
            # remove parentético em linha de nome ex.: NAME (CONT'D)
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
    ap.add_argument("--canon_mode", choices=["strict","aggressive"], default="aggressive")
    ap.add_argument("--rel_threshold", type=float, default=0.03, help="ganho relativo mínimo (ex.: 0.03 = 3%)")
    ap.add_argument("--min_tokens", type=int, default=200, help="ganho absoluto mínimo em tokens")
    ap.add_argument("--legend", choices=["sidecar","inline","none"], default="sidecar",
                    help="onde salvar legenda: sidecar (JSON), inline (no texto), none")
    args = ap.parse_args()

    enc = tiktoken.get_encoding("cl100k_base")
    tok = lambda s: len(enc.encode(s))
    files_all = sorted(Path(args.data_dir).rglob("*.txt"))
    files = files_all[:args.max_files] if args.max_files and len(files_all)>args.max_files else files_all

    encoder = DigiLangEncoder(use_tpd=True, token_dict_path=args.tpd_path, tpd_policy="per_work")
    legend_dir = Path("results/compression/overlay_legend"); legend_dir.mkdir(parents=True, exist_ok=True)

    rows=[]
    for p in files:
        raw = p.read_text(encoding="utf-8", errors="ignore")
        if args.max_chars and len(raw)>args.max_chars: raw = raw[:args.max_chars]
        base = canon_aggressive(raw) if (args.canon_mode=="aggressive" and canon_aggressive is not None) else canon_strict(raw)

        before_tok = tok(base)
        names = find_names(base, k=8)
        exp_gain, mapping = estimate_savings(enc, base, names)
        rel_gain = exp_gain / max(1, before_tok)

        decision = (rel_gain >= args.rel_threshold) or (exp_gain >= args.min_tokens)
        text2 = apply_overlay_linewise(base, mapping) if decision else base

        # (A) Sem legenda embutida: métrica primária de compressão
        comp,_ = encoder.encode(text2, preserve_headers=False)
        after_tok = tok(comp)
        reduction = 1.0 - (after_tok / max(1, before_tok))

        # (B) Com legenda embutida (para medir overhead real, opcional)
        legend_entries = 0
        legend_bytes = 0
        after_inline = after_tok
        reduction_inline = reduction
        if decision and mapping and args.legend in ("inline","sidecar"):
            legend_text = "#LEGEND " + "; ".join(f"{v}={k}" for k,v in mapping.items()) + "\n---\n"
            legend_entries = len(mapping)
            legend_bytes = len(legend_text.encode("utf-8"))
            if args.legend == "inline":
                text_inline = legend_text + text2
                comp_inline,_ = encoder.encode(text_inline, preserve_headers=False)
                after_inline = tok(comp_inline)
                reduction_inline = 1.0 - (after_inline / max(1, before_tok))

        # Sidecar reversível
        if decision and mapping and args.legend == "sidecar":
            side = dict(file=str(p), mapping=mapping, canon=args.canon_mode)
            (legend_dir / f"{p.stem}.legend.json").write_text(json.dumps(side, ensure_ascii=False, indent=2), encoding="utf-8")

        rows.append(dict(
            file=str(p), before=before_tok, after=after_tok, reduction=reduction,
            names=len(mapping), exp_gain_tokens=exp_gain, rel_gain=rel_gain, applied=int(decision),
            legend_entries=legend_entries, legend_bytes=legend_bytes, 
            after_inline=after_inline, reduction_inline=reduction_inline
        ))

    outdir = Path("results/compression"); outdir.mkdir(parents=True, exist_ok=True)
    out = outdir/"benchmark_overlay_adaptive.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file","before","after","reduction","names","exp_gain_tokens","rel_gain","applied",
                                          "legend_mode","legend_entries","legend_bytes","after_inline","reduction_inline"])
        w.writeheader()
        for r in rows:
            r["legend_mode"] = args.legend
            r.setdefault("legend_entries", 0)
            r.setdefault("legend_bytes", 0)
            r.setdefault("after_inline", r.get("after"))
            r.setdefault("reduction_inline", r.get("reduction"))
            w.writerow(r)

    mean = sum(r["reduction"] for r in rows)/len(rows) if rows else 0.0
    print(f"[OK] overlay adaptive -> {out} (mean_reduction={mean:.4f})")

if __name__=="__main__":
    main()