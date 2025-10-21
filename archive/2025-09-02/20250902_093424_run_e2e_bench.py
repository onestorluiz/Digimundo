#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, csv
from pathlib import Path
import tiktoken
from src.digilang.canon_strict import canon_strict
from src.digilang.encoder import DigiLangEncoder
from src.digilang.decoder import DigiLangDecoder
from src.telepathy.wire_v2 import encode_frame

# TF-IDF leve sem sklearn (fallback simples)
def build_tfidf(corpus):
    from collections import Counter, defaultdict
    import math, re
    vocab=set(); docs=[]
    for t in corpus:
        toks=re.findall(r"[A-Za-z]{3,}", t.lower())
        c=Counter(toks); docs.append(c); vocab.update(c.keys())
    vocab=sorted(vocab); idf={}
    N=len(docs)
    for term in vocab:
        df = sum(1 for d in docs if term in d)
        idf[term]=math.log((N+1)/(df+1))+1.0
    return vocab, idf, docs

def tfidf_query(vocab, idf, docs, q):
    import re
    toks=re.findall(r"[A-Za-z]{3,}", q.lower())
    from collections import Counter; tq=Counter(toks)
    scores=[]
    for i,d in enumerate(docs):
        s=0.0
        for term,tf in tq.items():
            if term in d:
                s += (tf*1.0)*idf.get(term,0.0)
        scores.append((s,i))
    scores.sort(reverse=True)
    return scores[:3]

def main():
    DATA = Path("data/screenplay_synth")
    texts=[p.read_text(encoding="utf-8", errors="ignore") for p in DATA.rglob("*.txt")]
    if not texts:
        print("[WARN] no data"); return
    vocab,idf,docs = build_tfidf(texts)

    enc = tiktoken.get_encoding("cl100k_base")
    encoder = DigiLangEncoder(use_tpd=True, token_dict_path="data/tpd/default/token_dict.json", tpd_policy="per_work")
    decoder = DigiLangDecoder(use_tpd=True, token_dict_path="data/tpd/default/token_dict.json")

    out = Path("results/e2e/bench.csv"); out.parent.mkdir(parents=True, exist_ok=True)
    rows=[]
    sample_files = list(DATA.rglob("*.txt"))[:20]
    for p in sample_files:
        raw = p.read_text(encoding="utf-8", errors="ignore")
        t0=time.time()
        canon = canon_strict(raw); t1=time.time()
        comp, _ = encoder.encode(canon, doc_key=p.stem); t2=time.time()
        # retrieve (usar 1o parágrafo como query)
        query = canon.split("\n\n")[0][:500]
        top = tfidf_query(vocab,idf,docs, query); t3=time.time()
        # wire encode
        payload = comp[:1000]
        fr = encode_frame("MSG", "A", "B", payload); t4=time.time()
        # decode
        dec = decoder.decode(comp); t5=time.time()

        rows.append(dict(
            file=str(p),
            t_canon_ms=(t1-t0)*1000,
            t_encode_ms=(t2-t1)*1000,
            t_retr_ms=(t3-t2)*1000,
            t_wire_ms=(t4-t3)*1000,
            t_decode_ms=(t5-t4)*1000,
            t_total_ms=(t5-t0)*1000,
            tokens_in=len(enc.encode(raw)),
            tokens_out=len(enc.encode(comp))
        ))
    with out.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"[OK] e2e -> {out}")

if __name__=="__main__":
    main()