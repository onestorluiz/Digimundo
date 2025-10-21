#!/usr/bin/env python
import sys
sys.path.append('.')
import csv, time
from pathlib import Path
import tiktoken
from src.compressors.llmlingua_wrapper import available, compress_text

enc=tiktoken.get_encoding("cl100k_base")
def toklen(s): return len(enc.encode(s))

out=Path("results/compression/llmlingua.csv")
out.parent.mkdir(parents=True, exist_ok=True)

def process_file(p:Path, ratio=0.8):
    text=p.read_text(encoding="utf-8", errors="ignore")
    t0=time.time()
    if available():
        c=compress_text(text, ratio=ratio)
    else:
        c=text
    dt=(time.time()-t0)*1000
    return dict(file=str(p), mode="llmlingua", before=toklen(text), after=toklen(c), reduction=1-toklen(c)/toklen(text), latency_ms=dt)

rows=[]
for p in Path("data/original").rglob("*.txt"):
    rows.append(process_file(p))

with out.open("w", newline="", encoding="utf-8") as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"[OK] llmlingua baseline written to {out}")