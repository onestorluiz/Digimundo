#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
import json, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(".")
CONF = ROOT/"configs"
REP  = ROOT/"reports"

MODE_TO_DEFAULTS = {
  "grid+acts":        {"DL_CANON_MODE":"aggressive","DL_PRESERVE_HEADERS":"false","OVERLAY_SCOPE":"acts"},
  "grid":             {"DL_CANON_MODE":"aggressive","DL_PRESERVE_HEADERS":"false","OVERLAY_SCOPE":"auto"},
  "overlay_by_act":   {"DL_CANON_MODE":"aggressive","DL_PRESERVE_HEADERS":"false","OVERLAY_SCOPE":"acts"},
  "overlay_ner":      {"DL_CANON_MODE":"aggressive","DL_PRESERVE_HEADERS":"false","OVERLAY_SCOPE":"global"},
  "overlay_adaptive": {"DL_CANON_MODE":"aggressive","DL_PRESERVE_HEADERS":"false","OVERLAY_SCOPE":"global"},
  "overlay":          {"DL_CANON_MODE":"strict","DL_PRESERVE_HEADERS":"false","OVERLAY_SCOPE":"global"},
  "baseline":         {"DL_CANON_MODE":"strict","DL_PRESERVE_HEADERS":"false","OVERLAY_SCOPE":"none"},
}

def main():
    strat_p = REP/"compression_strategy.json"
    if not strat_p.exists():
        print("[ERR] reports/compression_strategy.json not found"); sys.exit(2)
    data = json.loads(strat_p.read_text(encoding="utf-8"))
    rec  = data.get("recommendation", {})
    mode = rec.get("mode","baseline")
    targets = rec.get("make_targets",[]) or ["bench-all-nano"]

    defaults = MODE_TO_DEFAULTS.get(mode, MODE_TO_DEFAULTS["baseline"])
    # escreve prod.make.inc (Makefile inclui automaticamente)
    CONF.mkdir(parents=True, exist_ok=True)
    inc = CONF/"prod.make.inc"
    lines = []
    lines.append(f"# auto-generated {datetime.utcnow().isoformat()}Z")
    lines.append(f"PROD_TARGETS := {' '.join(targets)}")
    lines.append(f"export STRATEGY_MODE := {mode}")
    for k,v in defaults.items():
        lines.append(f"export {k} := {v}")
    inc.write_text("\n".join(lines)+"\n", encoding="utf-8")

    # reforça bench_default.env com os mesmos defaults (para runners que leem .env)
    envp = CONF/"bench_default.env"
    env = envp.read_text(encoding="utf-8").splitlines() if envp.exists() else []
    kv = {k: v for k,v in (line.split("=",1) for line in env if "=" in line and not line.strip().startswith("#"))}
    kv.setdefault("STRATEGY_MODE", mode)
    for k,v in defaults.items(): kv[k]=v
    kv_lines = [f"{k}={v}" for k,v in kv.items()]
    envp.write_text("\n".join(kv_lines)+"\n", encoding="utf-8")

    print("[OK] prod.make.inc -> configs/prod.make.inc")
    print("[OK] env defaults  -> configs/bench_default.env")

if __name__=="__main__":
    main()