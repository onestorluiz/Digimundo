# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
from datetime import datetime

def main():
    ts=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        from apps.scripturemon.consciousness import read as _cread
        from apps.scripturemon.membridge import counts as _m_counts
        c=_cread(); m=_m_counts()
        row=f'{ts},{c.get("level","")},{c.get("count","")},{m.get("L1",0)},{m.get("L2",0)},{m.get("L3",0)}\n'
    except Exception:
        row=f'{ts},,,0,0,0\n'
    out=Path("reports/history"); out.mkdir(parents=True, exist_ok=True)
    p=out/"ultimate.csv"
    if not p.exists(): p.write_text("ts,level,count,L1,L2,L3\n",encoding="utf-8")
    with p.open("a",encoding="utf-8") as f: f.write(row)

if __name__=="__main__": main()