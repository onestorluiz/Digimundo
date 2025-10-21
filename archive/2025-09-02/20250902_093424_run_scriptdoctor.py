#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gera 'coverage' de roteiro com Ollama (Mistral) local.
Saída: reports/scriptdoctor/coverage_<name>.md
Se 'ollama' não existir, grava TODO com prompt completo.
"""
from __future__ import annotations
import argparse, json, subprocess, os
from pathlib import Path
from src.scriptdoctor.analysis import features

def load_kb():
    p=Path("data/kb/beat_sheet.json")
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"beats":[]}

TEMPLATE = """You are **ScriptDoctor**, a professional script analyst.
Task: produce coverage with STRUCTURE, CHARACTERS, DIALOGUE, PACING, and 3 concrete FIXES.
Use the heuristics and beats as guides, but ground your notes in the script text.

HEURISTICS:
{heur}

SCRIPT (BEGIN)
{script}
SCRIPT (END)

Instructions:
- First give a 1-paragraph LOGLINE.
- Then sections: STRUCTURE, CHARACTERS, DIALOGUE, PACING (bullet points).
- Map story to beats (Opening, Catalyst, Break-2, Midpoint, Break-3, Finale) with page estimates.
- End with "TOP 3 FIXES" (actionable, specific).
"""

def run():
    ap=argparse.ArgumentParser()
    ap.add_argument("--script_path", default="", help="arquivo .txt do roteiro")
    ap.add_argument("--model", default=os.environ.get("OLLAMA_MODEL","mistral:instruct"))
    args=ap.parse_args()

    # escolhe arquivo
    sp = Path(args.script_path) if args.script_path else None
    if not sp or not sp.exists():
        cands=list(Path("data/screenplay_synth").rglob("*.txt")) or list(Path("data/original").rglob("*.txt"))
        if not cands:
            print("[WARN] no screenplay found"); return
        sp=cands[0]
    text=sp.read_text(encoding="utf-8", errors="ignore")
    kb=load_kb()
    heur=json.dumps(features(text, kb), ensure_ascii=False, indent=2)

    prompt=TEMPLATE.format(heur=heur, script=text[:150000])  # 150k chars cap

    outdir=Path("reports/scriptdoctor"); outdir.mkdir(parents=True, exist_ok=True)
    outfile=outdir/f"coverage_{sp.stem}.md"

    try:
        # tenta stdin (evita arg longo)
        res = subprocess.run(["ollama","run",args.model], input=prompt, capture_output=True, text=True, timeout=300)
        if res.returncode==0 and res.stdout.strip():
            outfile.write_text(res.stdout, encoding="utf-8")
            print(f"[OK] coverage -> {outfile}")
            return
        else:
            raise RuntimeError(res.stderr)
    except Exception as e:
        todo = outdir/f"TODO_ollama_{sp.stem}.md"
        todo.write_text("# Run this with Ollama:\n\n```\nollama run "+args.model+" <<'PROMPT'\n"+prompt+"\nPROMPT\n```", encoding="utf-8")
        print(f"[SKIP] ollama not available; wrote prompt -> {todo}")

if __name__=="__main__":
    run()