#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Constrói TPD por arquivo: data/tpd/per_work/<slug>/token_dict.json
Por padrão usa greedy_lazy no corpus do próprio arquivo (melhor ajuste local).
"""
import argparse, time
from pathlib import Path
from src.digilang.slug import slugify
from src.digilang.tpd_greedy_lazy import tokenize, build_tpd_greedy_lazy_for_corpus, save_token_dict

ap=argparse.ArgumentParser()
ap.add_argument("--data_dir", default="data/screenplay_synth")
ap.add_argument("--out_root", default="data/tpd/per_work")
ap.add_argument("--K", type=int, default=600)
ap.add_argument("--nmin", type=int, default=2)
ap.add_argument("--nmax", type=int, default=8)
ap.add_argument("--fmin", type=int, default=2)
ap.add_argument("--time_budget_s", type=float, default=10.0)
args=ap.parse_args()

root = Path(args.out_root); root.mkdir(parents=True, exist_ok=True)
built=0
for p in Path(args.data_dir).rglob("*.txt"):
    slug = slugify(p.stem)
    outdir = root / slug
    outdir.mkdir(parents=True, exist_ok=True)
    # Constrói TPD usando **apenas** o conteúdo do arquivo
    # (salva como "corpus" de 1 doc)
    tmpdir = outdir / "_tmp_corpus"; tmpdir.mkdir(exist_ok=True)
    (tmpdir/"doc.txt").write_text(p.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")
    mapping = build_tpd_greedy_lazy_for_corpus(str(tmpdir), K=args.K, n_min=args.nmin, n_max=args.nmax, freq_min=args.fmin, time_budget_s=args.time_budget_s)
    meta={"tokenizer":"cl100k_base","K":args.K,"n":[args.nmin,args.nmax],"fmin":args.fmin,"built_at":time.time(),"strategy":"per_work_lazy"}
    save_token_dict(mapping, outdir/"token_dict.json", meta)
    # limpa tmp (opcional)
    try:
        (tmpdir/"doc.txt").unlink(); tmpdir.rmdir()
    except: pass
    built+=1
print(f"[OK] per-work TPD built: {built} dicts at {root}")