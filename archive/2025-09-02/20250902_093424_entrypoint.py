# -*- coding: utf-8 -*-
from __future__ import annotations
import os, sys, json, subprocess
from pathlib import Path

PY = os.environ.get("PYTHON", sys.executable)

def _read_mode()->str:
    m = os.environ.get("SCRIPTUREMON_MODE")
    if m: return m.strip().lower()
    p = Path("configs/scripturemon.mode")
    if p.exists():
        try:
            txt = p.read_text(encoding="utf-8").strip().lower()
            if txt: return txt
        except: pass
    return "fusion"  # padrão

def _is_legacy_flag(args:list[str])->bool:
    if not args: return False
    a0 = args[0]
    legacy_flags = {"--classic","--brutal","--natural","--ultimate","setup","status","test","analyze","help","-h","--help"}
    return (a0 in legacy_flags)

def _detect_legacy_available()->bool:
    # Heurística leve: se temos manifesto ou bin legado detectado
    try:
        p = Path("reports/diag/legacy_manifest.json")
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            if data.get("bin"): return True
    except: pass
    # caminhos comuns (não garante execução)
    for cand in (
        Path.home()/".local/bin/scripturemon",
        Path.home()/"bin/scripturemon",
        Path("/usr/local/bin/scripturemon"),
    ):
        if cand.exists(): return True
    return False

def run_cli(args:list[str])->int:
    return subprocess.call([PY, "-m", "apps.scripturemon.cli", *args])

def run_compat(args:list[str])->int:
    # Reaproveita compat_legacy existente
    return subprocess.call([PY, "-m", "apps.scripturemon.compat_legacy", *args])

def chosen_mode(args:list[str])->str:
    mode = _read_mode()
    if mode == "auto":
        # flags típicas do legado -> compat; caso contrário, fusion
        return "legacy" if _is_legacy_flag(args) else "fusion"
    return mode

def main(argv:list[str]|None=None)->int:
    args = list(sys.argv[1:] if argv is None else argv)
    mode = chosen_mode(args)
    if mode == "legacy":
        return run_compat(args)
    # fusion (padrão) – usa CLI unificada
    return run_cli(args)

if __name__ == "__main__":
    raise SystemExit(main())