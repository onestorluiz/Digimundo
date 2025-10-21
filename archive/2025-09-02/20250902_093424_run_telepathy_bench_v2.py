#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mede bytes/latência de telemetria com payloads ORIGINAIS vs COMPRIMIDOS (DigiLang+TPD).
Modos:
- json_original
- json_digilang
- frame_digilang       (wire minimal)
- msgpack_digilang
Publica em fakeredis (opcional) para medir latência de pub/sub (aprox).
"""
import time, random, statistics, json
from pathlib import Path
import tiktoken
try:
    import fakeredis
except Exception:
    fakeredis = None

from src.telepathy.wire_v2 import encode_frame, encode_json, encode_msgpack
from src.digilang.encoder import DigiLangEncoder

enc = tiktoken.get_encoding("cl100k_base")
tok = lambda s: len(enc.encode(s))

def load_messages_from_screenplay(n:int=1000) -> list[tuple[str,str,str]]:
    """(op, from, to, payload) extraídos do screenplay_synth"""
    ds = list(Path("data/screenplay_synth").rglob("*.txt"))
    lines=[]
    for p in ds:
        t = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        lines.extend([l for l in t if l.strip()])
    # coleta pares (PERSONAGEM, fala) heurístico
    msgs=[]
    last_speaker=None
    for i,l in enumerate(lines):
        if l.isupper() and 2<=len(l)<=18:
            last_speaker=l
        else:
            if last_speaker and l:
                # partner aleatório
                partner = last_speaker+"_B" if random.random()<0.5 else "SYS"
                msgs.append(("MSG", last_speaker, partner, l))
    random.shuffle(msgs)
    return msgs[:n] if len(msgs)>n else msgs

def bench_mode(msgs, mode:str, encoder:DigiLangEncoder|None):
    ser_sizes=[]; t_lat=[]
    # fakeredis opcional
    rpub=rsub=None
    if fakeredis:
        rpub = fakeredis.FakeRedis()
        rsub = fakeredis.FakeRedis()
        ch="wire"
        psub = rsub.pubsub(); psub.subscribe(ch)
    t0=time.time()
    for op,frm,to,payload in msgs:
        if mode=="json_original":
            b = encode_json(op,frm,to,payload)
        elif mode=="json_digilang":
            cp,_ = encoder.encode(payload) if encoder else (payload,0.0)
            b = encode_json(op,frm,to,cp)
        elif mode=="frame_digilang":
            cp,_ = encoder.encode(payload) if encoder else (payload,0.0)
            b = encode_frame(op,frm,to,cp)
        elif mode=="msgpack_digilang":
            cp,_ = encoder.encode(payload) if encoder else (payload,0.0)
            b = encode_msgpack(op,frm,to,cp)
        else:
            raise ValueError(mode)
        ser_sizes.append(len(b))
        if rpub:
            t1=time.time()
            rpub.publish(ch,b)
            # consumo mínimo
            _ = psub.get_message(ignore_subscribe_messages=True, timeout=0.0)
            t2=time.time()
            t_lat.append((t2-t1)*1000.0)
    dt=(time.time()-t0)*1000.0
    res = {
        "mode": mode,
        "n": len(msgs),
        "bytes_mean": statistics.mean(ser_sizes),
        "bytes_median": statistics.median(ser_sizes),
        "lat_mean_ms": statistics.mean(t_lat) if t_lat else None,
        "lat_p95_ms": (sorted(t_lat)[int(0.95*len(t_lat))] if t_lat else None),
        "throughput_msgs_s": (len(msgs) / (dt/1000.0)) if dt>0 else None
    }
    return res

def main():
    random.seed(42)
    msgs = load_messages_from_screenplay(n=5000)
    encoder = DigiLangEncoder(use_tpd=True, token_dict_path="data/tpd/default/token_dict.json")
    out = Path("results/telepathy"); out.mkdir(parents=True, exist_ok=True)

    modes = ["json_original","json_digilang","frame_digilang","msgpack_digilang"]
    rows=[]
    for m in modes:
        rows.append(bench_mode(msgs, m, encoder))
    # grava CSV
    import csv
    with (out/"telepathy_v2.csv").open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    print("[OK] telepathy_v2 -> results/telepathy/telepathy_v2.csv")

if __name__=="__main__":
    main()