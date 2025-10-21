#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, time
from pathlib import Path
import tiktoken
from src.compressors.pctoolkit_wrapper import methods_available, compress_llmlingua, compress_pctoolkit

enc=tiktoken.get_encoding("cl100k_base")
def toklen(s): return len(enc.encode(s))

OUT = Path("results/compression/pctoolkit.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

def run_for_file(p:Path):
    text=p.read_text(encoding="utf-8", errors="ignore")
    rows=[]
    # LLMLingua
    t0=time.time()
    c = compress_llmlingua(text, ratio=0.85, preserve_entities=True)
    dt=(time.time()-t0)*1000
    rows.append(dict(file=str(p), mode="llmlingua", before=toklen(text), after=toklen(c), reduction=1-toklen(c)/toklen(text), latency_ms=dt, skipped=int(c==text)))
    # PCToolkit (placeholder defensive)
    t0=time.time()
    c2 = compress_pctoolkit(text, method="selective_context", strength=0.8)
    dt=(time.time()-t0)*1000
    rows.append(dict(file=str(p), mode="pctoolkit_selective", before=toklen(text), after=toklen(c2), reduction=1-toklen(c2)/toklen(text), latency_ms=dt, skipped=int(c2==text)))
    return rows

rows=[]
for p in Path("data/original").rglob("*.txt"):
    rows.extend(run_for_file(p))

with OUT.open("w", newline="", encoding="utf-8") as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"[OK] pctoolkit baselines -> {OUT}")