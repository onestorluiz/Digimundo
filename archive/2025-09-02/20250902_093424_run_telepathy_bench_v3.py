#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, csv, random
from pathlib import Path
import tiktoken
try:
    import lz4.frame as lz4f
except Exception:
    lz4f=None

from src.telepathy.wire_v2 import encode_frame, encode_json, encode_msgpack
from src.digilang.encoder import DigiLangEncoder

enc = tiktoken.get_encoding("cl100k_base")
tok = lambda s: len(enc.encode(s))

def load_msgs(n=5000):
    ds=list(Path("data/screenplay_synth").rglob("*.txt"))
    lines=[]
    for p in ds:
        lines += [l for l in p.read_text(encoding="utf-8", errors="ignore").splitlines() if l.strip()]
    msgs=[]
    last=None
    for l in lines:
        if l.isupper() and 2<=len(l)<=18:
            last=l
        else:
            if last:
                msgs.append(("MSG", last, "SYS", l))
    random.shuffle(msgs); return msgs[:n]

def main():
    msgs=load_msgs()
    encoder = DigiLangEncoder(use_tpd=True, token_dict_path="data/tpd/default/token_dict.json")
    out=Path("results/telepathy"); out.mkdir(parents=True, exist_ok=True)
    rows=[]
    for mode in ["json_original","frame_digilang","msgpack_digilang","frame_digilang_lz4"]:
        t0=time.time(); sizes=[]
        for op,frm,to,pay in msgs:
            if "digilang" in mode:
                pay,_ = encoder.encode(pay)
            if mode=="json_original":
                b = encode_json(op,frm,to,pay)
            elif mode=="frame_digilang":
                b = encode_frame(op,frm,to,pay)
            elif mode=="msgpack_digilang":
                b = encode_msgpack(op,frm,to,pay)
            elif mode=="frame_digilang_lz4":
                p = pay
                if lz4f:
                    p = lz4f.compress(p.encode("utf-8"))
                    # embute em base64-like? simples: hex (aumento pequeno)
                    import binascii
                    p = binascii.hexlify(p).decode("ascii")
                b = encode_frame(op,frm,to,p)
            sizes.append(len(b))
        dt=(time.time()-t0)*1000
        rows.append(dict(mode=mode, bytes_mean=sum(sizes)/len(sizes), throughput_msgs_s=len(msgs)/(dt/1000.0)))
    with (out/"telepathy_v3.csv").open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"[OK] telepathy_v3 -> {out/'telepathy_v3.csv'}")

if __name__=="__main__":
    main()