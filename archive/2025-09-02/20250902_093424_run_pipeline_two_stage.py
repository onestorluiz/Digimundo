#!/usr/bin/env python
import sys
sys.path.append('.')
import csv, time, json
from pathlib import Path
import tiktoken
from src.compressors.llmlingua_wrapper import available, compress_text
from src.digilang.encoder import DigiLangEncoder

enc=tiktoken.get_encoding("cl100k_base")
def toklen(s): return len(enc.encode(s))

out=Path("results/compression/two_stage.csv")
out.parent.mkdir(parents=True, exist_ok=True)

encdr=DigiLangEncoder(use_tpd=True, token_dict_path="data/tpd/default/token_dict.json")

def process_file(p:Path, ratio=0.85):
    text=p.read_text(encoding="utf-8", errors="ignore")
    t0=time.time()
    if available():
        stage1=compress_text(text, ratio=ratio)  # leve: 15% de corte
    else:
        stage1=text
    stage2, r = encdr.encode(stage1)  # aplica TPD token-level
    dt=(time.time()-t0)*1000
    before=toklen(text); after=toklen(stage2)
    return dict(file=str(p), mode="llmlingua->tpd", before=before, after=after, reduction=1-after/before, latency_ms=dt)

rows=[]
for p in Path("data/original").rglob("*.txt"):
    rows.append(process_file(p))

with out.open("w", newline="", encoding="utf-8") as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"[OK] two-stage results written to {out}")