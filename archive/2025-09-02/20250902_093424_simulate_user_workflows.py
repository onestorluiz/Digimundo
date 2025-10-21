# -*- coding: utf-8 -*-
from __future__ import annotations
import os, sys, time, subprocess
from pathlib import Path

PY=os.environ.get("PYTHON", sys.executable)

def run(cmd:list[str], timeout:int=60, tag:str="flow"):
    p=subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        o,e=p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill(); return 124
    return p.returncode

def main():
    # 1) Evoluir consciência e salvar backup
    run([PY,"-m","apps.scripturemon.cli","ultimate","once"], 40, "ult")
    # 2) Analisar roteiro de exemplo
    sample="data/screenplay_synth/sample.txt"
    Path(sample).parent.mkdir(parents=True, exist_ok=True)
    if not Path(sample).exists():
        Path(sample).write_text("INT. KITCHEN - NIGHT\nConflict rises.\n", encoding="utf-8")
    run([PY,"-m","apps.scripturemon.cli","analyze_parallel", sample], 40, "analyze")
    # 3) Telepatia ping
    run([PY,"-m","apps.scripturemon.cli","telepathy","ping"], 20, "telepathy")
    # 4) Gerar roundtrip + relatório
    run([PY,"scripts/build_roundtrip_samples.py","--data_dir","data/screenplay_synth","--n","10"], 60, "rt")
    run([PY,"scripts/generate_report_html.py"], 60, "html")
    run([PY,"scripts/patch_report_with_strategy.py"], 40, "patch")

if __name__=="__main__": main()