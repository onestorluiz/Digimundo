#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Divide textos em janelas cujo orçamento de tokens pós-compressão (DigiLang+TPD) <= budget.
Saída: data/packed/<budget>/<arquivo>_partNN.txt
"""
import argparse
from pathlib import Path
import tiktoken
from src.digilang.encoder import DigiLangEncoder
from src.digilang.canon_strict import canon_strict

enc = tiktoken.get_encoding("cl100k_base")
toklen=lambda s: len(enc.encode(s))

def pack_text(text, encoder, budget:int):
    # greedy: cresce bloco até orçamento
    parts=[]; buf=""
    for para in text.split("\n\n"):
        candidate = (buf+"\n\n"+para) if buf else para
        comp,_ = encoder.encode(canon_strict(candidate))
        if toklen(comp) <= budget:
            buf = candidate
        else:
            if buf:
                parts.append(buf); buf = para
            else:
                parts.append(para)  # para muito grande
    if buf: parts.append(buf)
    return parts

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data_dir", default="data/screenplay_synth")
    ap.add_argument("--budget", type=int, default=4000)
    ap.add_argument("--out_dir", default=None)
    ap.add_argument("--tpd_path", default="data/tpd/default/token_dict.json")
    ap.add_argument("--tpd_policy", default="per_work")
    args=ap.parse_args()

    out_dir = Path(args.out_dir or f"data/packed/{args.budget}")
    out_dir.mkdir(parents=True, exist_ok=True)
    encdr = DigiLangEncoder(use_tpd=True, token_dict_path=args.tpd_path, tpd_policy=args.tpd_policy)
    for p in Path(args.data_dir).rglob("*.txt"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        parts = pack_text(text, encdr, args.budget)
        for i,part in enumerate(parts, start=1):
            out_path = out_dir/(p.stem+f"_part{i:02d}.txt")
            out_path.write_text(part, encoding="utf-8")
    print(f"[OK] packed -> {out_dir}")

if __name__=="__main__":
    main()