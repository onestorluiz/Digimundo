#!/usr/bin/env python
import argparse, time
from pathlib import Path
from src.digilang.tpd_greedy_lazy import build_tpd_greedy_lazy_for_corpus, save_token_dict

ap=argparse.ArgumentParser()
ap.add_argument("--corpus", default="data/screenplay_synth")
ap.add_argument("--outdir", default="data/tpd/greedy_lazy")
ap.add_argument("--K", type=int, default=1500)
ap.add_argument("--nmin", type=int, default=2)
ap.add_argument("--nmax", type=int, default=8)
ap.add_argument("--fmin", type=int, default=3)
ap.add_argument("--time_budget_s", type=float, default=30.0)
args=ap.parse_args()

mapping = build_tpd_greedy_lazy_for_corpus(args.corpus, K=args.K, n_min=args.nmin, n_max=args.nmax, freq_min=args.fmin, time_budget_s=args.time_budget_s)
meta={"tokenizer":"cl100k_base","K":args.K,"n":[args.nmin,args.nmax],"fmin":args.fmin,"built_at":time.time(),"strategy":"greedy_lazy"}
Path(args.outdir).mkdir(parents=True, exist_ok=True)
save_token_dict(mapping, Path(args.outdir)/"token_dict.json", meta)
print(f"[OK] Greedy LAZY TPD -> {args.outdir}/token_dict.json (K={args.K})")