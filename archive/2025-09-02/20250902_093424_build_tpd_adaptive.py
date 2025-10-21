#!/usr/bin/env python
import sys
sys.path.append('.')
import json, time, argparse, hashlib
from pathlib import Path
from src.digilang.tpd_adaptive import build_tpd_for_corpus, save_token_dict

ap=argparse.ArgumentParser()
ap.add_argument("--corpus", default="data/original")
ap.add_argument("--outdir", default="data/tpd/default")
ap.add_argument("--K", type=int, default=1200)
ap.add_argument("--nmin", type=int, default=2)
ap.add_argument("--nmax", type=int, default=8)
ap.add_argument("--fmin", type=int, default=3)
args=ap.parse_args()

outdir=Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
mapping = build_tpd_for_corpus(args.corpus, K=args.K, n_min=args.nmin, n_max=args.nmax, freq_min=args.fmin)
meta={"tokenizer":"cl100k_base","K":args.K,"n":[args.nmin,args.nmax],"fmin":args.fmin,"built_at":time.time()}
save_token_dict(mapping, outdir/"token_dict.json", meta)
print(f"[OK] TPD built at {outdir}/token_dict.json")