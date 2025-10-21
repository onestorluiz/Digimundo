#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gera cache JSONL com entidades PERSON por arquivo.
Saída: data/ner_cache/<dataset>.jsonl
"""
from __future__ import annotations
from pathlib import Path
import argparse, json, sys
from src.nlp.ner_offline import person_candidates

def iter_files(root:Path, max_files:int|None=None, max_chars:int|None=None):
    files = sorted(root.rglob("*.txt"))
    if max_files: files = files[:max_files]
    for p in files:
        t = p.read_text(encoding="utf-8", errors="ignore")
        if max_chars and len(t)>max_chars: t=t[:max_chars]
        yield p, t

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", default="data/screenplay_synth")
    ap.add_argument("--out", default="")
    ap.add_argument("--max_files", type=int, default=200)
    ap.add_argument("--max_chars", type=int, default=120000)
    args = ap.parse_args()
    root = Path(args.data_dir)
    if not root.exists():
        print("[WARN] data_dir not found:", root); sys.exit(0)
    outdir = Path("data/ner_cache"); outdir.mkdir(parents=True, exist_ok=True)
    out = Path(args.out) if args.out else outdir/(root.name + ".jsonl")
    with out.open("w", encoding="utf-8") as f:
        for p, text in iter_files(root, args.max_files, args.max_chars):
            persons = person_candidates(text, k=16)
            f.write(json.dumps({"file": str(p), "persons": persons}, ensure_ascii=False) + "\n")
    print(f"[OK] NER cache -> {out}")

if __name__=="__main__":
    main()