#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

def main():
    p = Path("reports/compression_strategy.json")
    if not p.exists():
        print("[ERR] reports/compression_strategy.json not found"); sys.exit(2)
    data = json.loads(p.read_text(encoding="utf-8"))
    # Se existir prod.make.inc, preferimos bench-prod (conjunto decidido)
    if Path("configs/prod.make.inc").exists():
        print("[RUN] make bench-prod")
        subprocess.run(["make","bench-prod"], check=False)
        print("[OK] strategy-run-prod done")
        return
    targets = (data.get("recommendation") or {}).get("make_targets", [])
    if not targets:
        print("[WARN] no make_targets; nothing to run"); return
    for t in targets:
        print(f"[RUN] make {t}")
        try:
            subprocess.run(["make", t], check=False)
        except Exception as e:
            print("[WARN] failed:", t, e)
    print("[OK] strategy-run-prod done")

if __name__=="__main__":
    main()