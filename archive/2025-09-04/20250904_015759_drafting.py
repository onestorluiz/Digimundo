from __future__ import annotations
from pathlib import Path
from typing import List, Dict
from .beats_detect import detect_beats

TEMPLATES={
 "MIDPOINT": "# MIDPOINT — Reversão Central\n- Objetivo aparente é invertido.\n- Nova informação muda as apostas.\n- Cena-chave: conflito direto com antagonista.\n",
 "ALL_IS_LOST": "# ALL IS LOST — Ruína\n- Perda simbólica do que sustentava o herói.\n- \"Dark Night of the Soul\" na sequência seguinte.\n- Cena curta, imagens fortes.\n",
 "CLIMAX": "# CLIMAX — Decisão Irreversível\n- Escolha moral do protagonista.\n- Paga elementos plantados (setups) do A1/A2.\n- Visualizar ação e consequência imediata.\n"
}

def draft_from_beats(scenes:List[str])->str:
    beats = detect_beats("\n\n".join(scenes or []))
    sel=[]
    # prioriza: midpoint, all_is_lost, climax — se existirem
    prio = ["MIDPOINT","ALL_IS_LOST","CLIMAX"]
    for p in prio:
        for b in beats:
            if b["beat"]==p:
                sel.append(TEMPLATES[p]); break
    if not sel:
        sel.append("# SEQUÊNCIA — Esqueleto\n- Intenção vs. Obstáculo\n- Virada visual e/ou reversão de poder\n- Botar risco pessoal na mesa\n")
    return "\n\n".join(sel)

def export_draft(session, text:str)->Path:
    outdir = Path(getattr(session,"home","."))/ "reports"/"drafts"
    outdir.mkdir(parents=True, exist_ok=True)
    from time import strftime
    p = outdir / f"draft_{strftime('%Y%m%d-%H%M%S')}.md"
    p.write_text(text, encoding="utf-8")
    return p