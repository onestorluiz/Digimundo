#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, csv, time
from pathlib import Path
import tiktoken
from src.digilang.encoder import DigiLangEncoder

ap = argparse.ArgumentParser()
ap.add_argument("--data_dir", default="data/original", help="Directory of .txt files to compress")
ap.add_argument("--tpd_path", default="data/tpd/default/token_dict.json", help="Token dict path (default)")
ap.add_argument("--tpd_policy", default="default", choices=["default","per_work"], help="Use per-work TPD when available")
ap.add_argument("--ablation", default="canon+tpd", choices=["none","canon","canon+tpd","canon+tpd+symbols"])
ap.add_argument("--vocab_path", default="src/digilang/vocab.json")
args = ap.parse_args()

enc = tiktoken.get_encoding("cl100k_base")
DATA_DIR = Path(args.data_dir)
OUT = Path("results/compression/benchmark_simple.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

def toklen(s:str)->int: return len(enc.encode(s))

encoder = DigiLangEncoder(
    use_tpd=("tpd" in args.ablation),
    token_dict_path=args.tpd_path,
    tpd_policy=args.tpd_policy
)

rows=[]
for p in DATA_DIR.rglob("*.txt"):
    text = p.read_text(encoding="utf-8", errors="ignore")
    t0 = time.time()
    if args.ablation == "none":
        comp = text
    else:
        # Se per_work, passamos doc_key automaticamente (slug = stem)
        if args.tpd_policy == "per_work":
            comp, ratio = encoder.encode(text, doc_key=p.stem)
        else:
            comp, ratio = encoder.encode(text)
    dt = (time.time()-t0)*1000.0
    before = toklen(text); after = toklen(comp)
    rows.append(dict(
        file=str(p),
        mode=args.ablation,
        tpd_policy=args.tpd_policy,
        tokens_before=before,
        tokens_after=after,
        reduction=1 - (after/before if before else 1.0),
        latency_ms=dt
    ))

with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"[OK] compression benchmark -> {OUT}")

# (fim)