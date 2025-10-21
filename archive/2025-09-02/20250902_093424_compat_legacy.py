#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
import os, sys, tempfile, subprocess, shlex

PY = os.environ.get("PYTHON", sys.executable)
CLI = ["-m", "apps.scripturemon.cli"]

def run_cli(args:list[str])->int:
    return subprocess.call([PY, *CLI, *args])

def make(*targets:str)->int:
    return subprocess.call(["make", *targets])

def _set_env(mode:str):
    # Ajusta defaults de estratégia rapidamente
    if mode=="classic":
        os.environ.setdefault("DL_CANON_MODE","strict")
        os.environ.setdefault("DL_PRESERVE_HEADERS","true")
    elif mode=="brutal":
        os.environ.setdefault("DL_CANON_MODE","aggressive")
        os.environ.setdefault("DL_PRESERVE_HEADERS","false")
    elif mode=="natural":
        os.environ.setdefault("DL_CANON_MODE","aggressive")
        os.environ.setdefault("DL_PRESERVE_HEADERS","true")
    elif mode=="ultimate":
        os.environ.setdefault("DL_CANON_MODE","aggressive")
        os.environ.setdefault("DL_PRESERVE_HEADERS","false")
        os.environ.setdefault("OVERLAY_SCOPE","acts")

def main():
    argv = sys.argv[1:]
    if not argv:
        # comportamento padrão: abrir/gerar relatório
        make("report-html-with-strategy")
        return 0
    a0 = argv[0]

    # Flags de modo (compat)
    if a0 in ("--classic","--brutal","--natural","--ultimate"):
        _set_env(a0.lstrip("-"))
        # encadeia em compress + report
        make("bench-all-nano"); make("report-html-with-strategy"); return 0

    # Subcomandos comum do legado
    if a0 == "setup":
        make("setup"); make("data"); make("strategy-apply-hard"); return 0
    if a0 == "status":
        subprocess.call([PY,"scripts/validate_all.py"]); make("report-html-with-strategy"); return 0
    if a0 == "help" or a0 == "--help" or a0 == "-h":
        return run_cli(["--help"])
    if a0 == "test":
        for t in ("exp1","exp2","exp3","exp4"): make(t)
        subprocess.call([PY,"scripts/validate_all.py"]); return 0
    if a0 == "analyze":
        # aceita texto direto (legacy) — salva em temp e roda doctor
        text = " ".join(argv[1:]) if len(argv)>1 else ""
        if not text.strip(): 
            print("[WARN] analyze sem texto"); return 1
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write(text); f.flush(); tmp = f.name
        return run_cli(["doctor", tmp])

    # fallback: delega 1:1 para nova CLI (compat de nomes)
    return run_cli(argv)

if __name__ == "__main__":
    sys.exit(main())