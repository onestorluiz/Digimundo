#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Grid adaptativo com overlay GLOBAL e por ATO:
  canon: strict | aggressive
  overlay: none | global | acts
Escolhe a melhor combinação por arquivo (maior redução).
Mede também "inline legend" do vencedor para overhead real.
Saída: results/compression/grid_adaptive_acts.csv
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
from src.nlp.ner_offline import person_candidates

UP = re.compile(r"^[A-Z][A-Z0-9 '\.-]{1,17}$")
PAREN = re.compile(r"\s*\((CONT'D|V\.O\.|O\.S\.)\)\s*$", re.I)
GLYPHS=[ "§"+c for c in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") ]

def clean_char(s:str)->str: return PAREN.sub("", s.strip().upper())
def toklen(enc, s:str)->int: return len(enc.encode(s))

def apply_overlay_linewise(text:str, mapping:dict[str,str])->str:
    out=[]
    for l in text.splitlines():
        u=clean_char(l)
        if u in mapping and UP.match(u):
            out.append(mapping[u])
        else:
            out.append(l)
    return "\n".join(out)

def nearest_nl(text:str, idx:int)->int:
    if idx<=0 or idx>=len(text): return idx
    left = text.rfind("\n", 0, idx)
    right = text.find("\n", idx)
    cand = [p for p in (left, right) if p != -1]
    if not cand: return idx
    return min(cand, key=lambda p: abs(p-idx))

def split_three_acts(text:str):
    n = len(text)
    c1 = nearest_nl(text, int(0.25*n))
    c2 = nearest_nl(text, int(0.75*n))
    c1 = max(0, min(c1, n)); c2 = max(c1, min(c2, n))
    return [text[:c1], text[c1:c2], text[c2:]], [0, c1, c2, n]

def names_to_mapping(names:list[str], k:int=12)->dict[str,str]:
    m={}
    for i, name in enumerate(names[:k]):
        if i>=len(GLYPHS): break
        m[name]=GLYPHS[i]
    return m

def estimate_gain(enc, base_text:str, mapping:dict[str,str])->int:
    # ganho aproximado: (tokens(name)-tokens(glyph)) * ocorrências como linha de personagem
    gain=0
    lines = [clean_char(l) for l in base_text.splitlines()]
    cnt = Counter(lines)
    for name, glyph in mapping.items():
        gain += max(0, toklen(enc,name)-toklen(enc,glyph)) * cnt.get(name,0)
    return gain

def legend_inline_for(mapping_or_acts:dict, scope:str)->str:
    if scope=="global":
        return "#LEGEND " + "; ".join(f"{v}={k}" for k,v in mapping_or_acts.items()) + "\n---\n"
    # acts
    def line(label, m): return f"{label}:" + (";".join(f"{v}={k}" for k,v in m.items()) if m else "")
    return "#LEGEND_ACTS " + " | ".join([line("A1", mapping_or_acts["A1"]),
                                         line("A2", mapping_or_acts["A2"]),
                                         line("A3", mapping_or_acts["A3"])]) + "\n---\n"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", default="data/screenplay_synth")
    ap.add_argument("--tpd_path", default="data/tpd/default/token_dict.json")
    ap.add_argument("--max_files", type=int, default=10)
    ap.add_argument("--max_chars", type=int, default=60000)
    ap.add_argument("--rel_threshold", type=float, default=0.03)
    ap.add_argument("--min_tokens", type=int, default=200)
    ap.add_argument("--legend_inline_eval", action="store_true",
                    help="calcula redução com legenda inline para o modo vencedor")
    ap.add_argument("--topn", type=int, default=12)
    args = ap.parse_args()

    enc_tok = tiktoken.get_encoding("cl100k_base")
    tok = lambda s: len(enc_tok.encode(s))
    files_all = sorted(Path(args.data_dir).rglob("*.txt"))
    files = files_all[:args.max_files] if args.max_files and len(files_all)>args.max_files else files_all

    encoder = DigiLangEncoder(use_tpd=True, token_dict_path=args.tpd_path, tpd_policy="per_work")

    rows=[]
    for p in files:
        raw = Path(p).read_text(encoding="utf-8", errors="ignore")
        if args.max_chars and len(raw)>args.max_chars: raw = raw[:args.max_chars]

        base_strict = canon_strict(raw)
        base_aggr = canon_aggressive(raw) if canon_aggressive is not None else base_strict
        before = tok(base_strict)  # baseline justo

        def eval_combo(canon_label:str, base_text:str, overlay_scope:str):
            # overlay_scope: "none" | "global" | "acts"
            text2 = base_text
            meta = {}
            if overlay_scope=="global":
                ppl = person_candidates(base_text, k=args.topn)
                mapping = names_to_mapping(ppl, k=args.topn)
                egain = estimate_gain(enc_tok, base_text, mapping)
                if (egain/max(1,before))>=args.rel_threshold or egain>=args.min_tokens:
                    text2 = apply_overlay_linewise(base_text, mapping)
                    meta = {"scope":"global","mapping":mapping, "egain":egain}
                else:
                    meta = {"scope":"global","mapping":{}, "egain":egain}
            elif overlay_scope=="acts":
                segs, _ = split_three_acts(base_text)
                acts_map = {}
                eg_total = 0
                applied = [0,0,0]
                ov_segs=[]
                for i, seg in enumerate(segs):
                    ppl = person_candidates(seg, k=min(8,args.topn))
                    mapping = names_to_mapping(ppl, k=min(8,args.topn))
                    eg = estimate_gain(enc_tok, seg, mapping)
                    rel = eg / max(1, tok(seg))
                    if (rel>=max(0.02, args.rel_threshold/1.5)) or eg>=max(120, args.min_tokens//2):
                        ov_segs.append(apply_overlay_linewise(seg, mapping))
                        acts_map[["A1","A2","A3"][i]] = mapping
                        applied[i]=1
                        eg_total += eg
                    else:
                        ov_segs.append(seg)
                        acts_map[["A1","A2","A3"][i]] = {}
                text2 = "".join(ov_segs)
                meta = {"scope":"acts","acts_map":acts_map, "egain":eg_total, "applied":applied}
            else:
                meta = {"scope":"none"}

            comp,_ = encoder.encode(text2, preserve_headers=False)
            after = tok(comp)
            red = 1.0 - (after/max(1,before))
            return dict(after=after, reduction=red, meta=meta, canon=canon_label, scope=overlay_scope)

        cands=[]
        for canon_label, base in [("strict", base_strict), ("aggressive", base_aggr)]:
            cands.append(("{}_none".format(canon_label),  eval_combo(canon_label, base, "none")))
            cands.append(("{}_global".format(canon_label),eval_combo(canon_label, base, "global")))
            cands.append(("{}_acts".format(canon_label),  eval_combo(canon_label, base, "acts")))

        best_key, best = max(cands, key=lambda kv: kv[1]["reduction"])

        # inline legend (overhead real) somente para o vencedor
        after_inline = best["after"]
        red_inline   = best["reduction"]
        if args.legend_inline_eval and best["meta"].get("scope") in ("global","acts"):
            if best["meta"]["scope"]=="global":
                legend = legend_inline_for(best["meta"]["mapping"], "global")
                text_inline = legend  # prefixo a ser somado ao texto já comprimido? medimos sobre entrada + legenda
            else:
                legend = legend_inline_for(best["meta"]["acts_map"], "acts")
                text_inline = legend
            # para medir overhead inline de forma consistente, re-encode legend+texto (base do melhor modo)
            # (reconstituímos a entrada do melhor modo rapidamente)
            # Simplificação: reprocessamos a variante base + overlay para inline
            # Nota: como acima, a redução é comparada contra "before"
            from_text = base_aggr if best["canon"]=="aggressive" else base_strict
            if best["scope"]=="global":
                if best["meta"]["mapping"]:
                    from_text = apply_overlay_linewise(from_text, best["meta"]["mapping"])
            elif best["scope"]=="acts":
                segs,_ = split_three_acts(from_text)
                m = best["meta"]["acts_map"]
                from_text = "".join([
                    apply_overlay_linewise(segs[0], m.get("A1",{})),
                    apply_overlay_linewise(segs[1], m.get("A2",{})),
                    apply_overlay_linewise(segs[2], m.get("A3",{})),
                ])
            compL,_ = encoder.encode(legend + from_text, preserve_headers=False)
            after_inline = tok(compL)
            red_inline   = 1.0 - (after_inline/max(1,before))

        row = dict(
            file=str(p), choice=best_key, canon=best["canon"], scope=best["scope"],
            before=before, after=best["after"], reduction=best["reduction"],
            after_inline=after_inline, reduction_inline=red_inline,
            names_global = len(best["meta"].get("mapping",{})),
            applied_A1 = (best["meta"].get("applied",[0,0,0])[0] if best["scope"]=="acts" else 0),
            applied_A2 = (best["meta"].get("applied",[0,0,0])[1] if best["scope"]=="acts" else 0),
            applied_A3 = (best["meta"].get("applied",[0,0,0])[2] if best["scope"]=="acts" else 0),
            egain_tokens = int(best["meta"].get("egain",0))
        )
        rows.append(row)

    outdir = Path("results/compression"); outdir.mkdir(parents=True, exist_ok=True)
    out = outdir/"grid_adaptive_acts.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file","choice","canon","scope","before","after","reduction","after_inline","reduction_inline",
                                          "names_global","applied_A1","applied_A2","applied_A3","egain_tokens"])
        w.writeheader()
        for r in rows: w.writerow(r)
    mean = sum(r["reduction"] for r in rows)/len(rows) if rows else 0.0
    print(f"[OK] grid_adaptive_acts -> {out} (mean_reduction={mean:.4f})")

if __name__=="__main__":
    main()