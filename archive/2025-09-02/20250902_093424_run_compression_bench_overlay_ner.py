#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bench overlay usando NER offline (spaCy se disponível; senão heurística).
- Usa canon_aggressive se presente (ou strict).
- Substitui LINHAS DE PERSONAGEM (UPPER) pelos glifos mapeados via NER.
- Mede redução com e sem legenda inline; sidecar opcional.
Saída: results/compression/benchmark_overlay_ner.csv
"""
from __future__ import annotations
from pathlib import Path
import argparse, csv, re, json
import tiktoken
from src.digilang.encoder import DigiLangEncoder
from src.digilang.canon_strict import canon_strict
try:
    from src.digilang.canon_aggressive import canon_aggressive
except Exception:
    canon_aggressive = None
from src.nlp.ner_offline import person_candidates

UP = re.compile(r"^[A-Z][A-Z0-9 '\.-]{1,17}$")
PAREN = re.compile(r"\s*\((CONT'D|V\.O\.|O\.S\.)\)\s*$", re.I)
GLYPHS=[ "§"+c for c in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") ]

def clean_char(s:str)->str:
    return PAREN.sub("", s.strip().upper())

def apply_overlay_linewise(text:str, mapping:dict[str,str])->str:
    out=[]
    for l in text.splitlines():
        u=clean_char(l)
        if u in mapping and UP.match(u):
            out.append(mapping[u])
        else:
            out.append(l)
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", default="data/screenplay_synth")
    ap.add_argument("--tpd_path", default="data/tpd/default/token_dict.json")
    ap.add_argument("--max_files", type=int, default=12)
    ap.add_argument("--max_chars", type=int, default=60000)
    ap.add_argument("--legend", choices=["none","sidecar","inline"], default="sidecar")
    args = ap.parse_args()

    enc = tiktoken.get_encoding("cl100k_base")
    tok = lambda s: len(enc.encode(s))
    files_all = sorted(Path(args.data_dir).rglob("*.txt"))
    files = files_all[:args.max_files] if args.max_files and len(files_all)>args.max_files else files_all

    encdr = DigiLangEncoder(use_tpd=True, token_dict_path=args.tpd_path, tpd_policy="per_work")
    legend_dir = Path("results/compression/overlay_ner_legend"); legend_dir.mkdir(parents=True, exist_ok=True)

    rows=[]
    for p in files:
        raw = Path(p).read_text(encoding="utf-8", errors="ignore")
        if args.max_chars and len(raw)>args.max_chars: raw = raw[:args.max_chars]
        base = canon_aggressive(raw) if canon_aggressive is not None else canon_strict(raw)

        before = tok(base)
        # candidatos via NER
        ppl = person_candidates(base, k=12)
        mapping = {}
        for i, name in enumerate(ppl):
            if i>=len(GLYPHS): break
            mapping[name] = GLYPHS[i]

        # overlay
        text2 = apply_overlay_linewise(base, mapping) if mapping else base

        # (A) sem legenda
        comp,_ = encdr.encode(text2, preserve_headers=False)
        after = tok(comp)
        red = 1.0 - (after/max(1,before))

        # (B) com legenda inline (overhead real)
        after_inline = after; red_inline = red
        if mapping and args.legend in ("inline","sidecar"):
            legend = "#LEGEND " + "; ".join(f"{v}={k}" for k,v in mapping.items()) + "\n---\n"
            compL,_ = encdr.encode(legend + text2, preserve_headers=False)
            after_inline = tok(compL)
            red_inline = 1.0 - (after_inline/max(1,before))
            if args.legend == "sidecar":
                (legend_dir / f"{Path(p).stem}.legend.json").write_text(
                    json.dumps({"file": str(p), "mapping": mapping}, ensure_ascii=False, indent=2), encoding="utf-8"
                )

        rows.append(dict(file=str(p), before=before, after=after, reduction=red,
                         after_inline=after_inline, reduction_inline=red_inline,
                         names=len(mapping)))

    outdir = Path("results/compression"); outdir.mkdir(parents=True, exist_ok=True)
    out = outdir/"benchmark_overlay_ner.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file","before","after","reduction","after_inline","reduction_inline","names"])
        w.writeheader()
        for r in rows: w.writerow(r)
    mean = sum(r["reduction"] for r in rows)/len(rows) if rows else 0.0
    print(f"[OK] overlay NER -> {out} (mean_reduction={mean:.4f})")

if __name__=="__main__":
    main()