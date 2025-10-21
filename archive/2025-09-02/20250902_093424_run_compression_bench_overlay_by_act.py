#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Overlay por ATO (A1/A2/A3) com legenda sidecar/inline.
- Divide o texto em 3 atos por frações 25% / 75% (ajustadas ao \n mais próximo)
- Para cada ato, detecta nomes de personagem e aplica codebook local (glifos §A, §B, ...)
- Mede redução sem legenda e com legenda inline (overhead real)
Saídas:
  - results/compression/benchmark_overlay_by_act.csv
  - results/compression/overlay_by_act_legend/<file>.legend.json (sidecar)
"""
from __future__ import annotations
from pathlib import Path
import argparse, csv, re, json
from collections import Counter
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
GLYPHS = ["§"+c for c in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")]

def clean_char(s:str)->str:
    return PAREN.sub("", s.strip().upper())

def nearest_nl(text:str, idx:int)->int:
    if idx<=0 or idx>=len(text): return idx
    left = text.rfind("\n", 0, idx)
    right = text.find("\n", idx)
    cand = [p for p in (left, right) if p != -1]
    if not cand: return idx
    return min(cand, key=lambda p: abs(p-idx))

def split_three_acts(text:str):
    n = len(text)
    cut1 = nearest_nl(text, int(0.25*n))
    cut2 = nearest_nl(text, int(0.75*n))
    cut1 = max(0, min(cut1, n))
    cut2 = max(cut1, min(cut2, n))
    return [text[:cut1], text[cut1:cut2], text[cut2:]], [0, cut1, cut2, n]

def apply_overlay_linewise(text:str, mapping:dict[str,str])->str:
    out=[]
    for l in text.splitlines():
        u=clean_char(l)
        if u in mapping and UP.match(u):
            out.append(mapping[u])
        else:
            out.append(l)
    return "\n".join(out)

def names_to_mapping(names:list[str])->dict[str,str]:
    m={}
    for i, name in enumerate(names):
        if i>=len(GLYPHS): break
        m[name]=GLYPHS[i]
    return m

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", default="data/screenplay_synth")
    ap.add_argument("--tpd_path", default="data/tpd/default/token_dict.json")
    ap.add_argument("--max_files", type=int, default=10)
    ap.add_argument("--max_chars", type=int, default=60000)
    ap.add_argument("--canon_mode", choices=["strict","aggressive"], default="aggressive")
    ap.add_argument("--legend", choices=["sidecar","inline","none"], default="sidecar")
    ap.add_argument("--topn", type=int, default=8, help="máx. nomes por ato")
    ap.add_argument("--rel_threshold", type=float, default=0.02, help="ganho relativo mínimo estimado (2%) para aplicar overlay por ato")
    ap.add_argument("--min_tokens", type=int, default=120, help="ganho absoluto mínimo estimado por ato")
    args = ap.parse_args()

    enc_tok = tiktoken.get_encoding("cl100k_base")
    tok = lambda s: len(enc_tok.encode(s))

    files_all = sorted(Path(args.data_dir).rglob("*.txt"))
    files = files_all[:args.max_files] if args.max_files and len(files_all)>args.max_files else files_all

    encdr = DigiLangEncoder(use_tpd=True, token_dict_path=args.tpd_path, tpd_policy="per_work")
    legend_dir = Path("results/compression/overlay_by_act_legend"); legend_dir.mkdir(parents=True, exist_ok=True)
    out_rows=[]

    for p in files:
        raw = Path(p).read_text(encoding="utf-8", errors="ignore")
        if args.max_chars and len(raw)>args.max_chars: raw = raw[:args.max_chars]
        base = canon_aggressive(raw) if (args.canon_mode=="aggressive" and canon_aggressive is not None) else canon_strict(raw)

        segs, idxs = split_three_acts(base)  # [A1, A2, A3], [0, c1, c2, n]
        before = tok(base)

        # Para cada ato, escolhe nomes (NER offline) e mapeia
        mappings = []
        applied = []
        exp_gains = []
        seg_after_tokens = []
        seg_after_tokens_inline = []

        seg_texts = []
        for seg in segs:
            seg_texts.append(seg)

        # estimativa de ganho por ato (simples: sum(gain por linha de nome))
        def estimate_gain(seg_text:str, names:list[str])->int:
            gain=0
            for i, n in enumerate(names):
                if i>=len(GLYPHS): break
                gain += (tok(n) - tok(GLYPHS[i])) * seg_text.upper().splitlines().count(n)
            return max(0, gain)

        # decide overlay por ato
        for i, seg in enumerate(segs):
            cand = person_candidates(seg, k=args.topn)  # NER local
            mapping = names_to_mapping(cand)
            egain = estimate_gain(seg, cand)
            rel = egain / max(1, tok(seg))
            do_apply = (rel >= args.rel_threshold) or (egain >= args.min_tokens)
            mappings.append(mapping if do_apply else {})
            applied.append(int(do_apply))
            exp_gains.append(int(egain))

        # aplica overlay por ato (independente)
        ov_segs = []
        for seg, m in zip(segs, mappings):
            ov_segs.append(apply_overlay_linewise(seg, m) if m else seg)
        ov_text = "".join(ov_segs)

        # (A) sem legenda
        comp,_ = encdr.encode(ov_text, preserve_headers=False)
        after = tok(comp)
        red = 1.0 - (after/max(1,before))

        # (B) com legenda inline (overhead real)
        after_inline = after; red_inline = red
        if args.legend in ("inline","sidecar"):
            # legenda compacta por ato
            def legend_line(act_label, m):
                if not m: return f"{act_label}:"
                items = ";".join(f"{v}={k}" for k,v in m.items())
                return f"{act_label}:{items}"
            L1 = legend_line("A1", mappings[0])
            L2 = legend_line("A2", mappings[1])
            L3 = legend_line("A3", mappings[2])
            legend_text = f"#LEGEND_ACTS {L1} | {L2} | {L3}\n---\n"
            compL,_ = encdr.encode(legend_text + ov_text, preserve_headers=False)
            after_inline = tok(compL)
            red_inline = 1.0 - (after_inline/max(1,before))

        # sidecar reversível com offsets dos atos
        if args.legend == "sidecar":
            side = dict(
                file=str(p),
                acts=dict(indexes=dict(a1_start=idxs[0], a2_start=idxs[1], a3_start=idxs[2], end=idxs[3]),
                          A1=mappings[0], A2=mappings[1], A3=mappings[2]),
                canon=args.canon_mode
            )
            (legend_dir / f"{Path(p).stem}.legend.json").write_text(json.dumps(side, ensure_ascii=False, indent=2), encoding="utf-8")

        out_rows.append(dict(
            file=str(p), before=before, after=after, reduction=red,
            after_inline=after_inline, reduction_inline=red_inline,
            applied_A1=applied[0], applied_A2=applied[1], applied_A3=applied[2],
            names_A1=len(mappings[0]), names_A2=len(mappings[1]), names_A3=len(mappings[2]),
            exp_gain_tokens_A1=exp_gains[0], exp_gain_tokens_A2=exp_gains[1], exp_gain_tokens_A3=exp_gains[2]
        ))

    outdir = Path("results/compression"); outdir.mkdir(parents=True, exist_ok=True)
    out = outdir/"benchmark_overlay_by_act.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "file","before","after","reduction","after_inline","reduction_inline",
            "applied_A1","applied_A2","applied_A3","names_A1","names_A2","names_A3",
            "exp_gain_tokens_A1","exp_gain_tokens_A2","exp_gain_tokens_A3"
        ])
        w.writeheader()
        for r in out_rows: w.writerow(r)
    mean = sum(r["reduction"] for r in out_rows)/len(out_rows) if out_rows else 0.0
    print(f"[OK] overlay_by_act -> {out} (mean_reduction={mean:.4f})")

if __name__=="__main__":
    main()