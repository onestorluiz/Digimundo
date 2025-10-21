from __future__ import annotations
from pathlib import Path
from typing import Dict, List
from .compare_core import _read_text, _split_scenes, align_scenes
from .beats_detect import detect_beats

def graft_plan(pathA:Path, pathB:Path)->str:
    rawA=_read_text(pathA); rawB=_read_text(pathB)
    scenesA=_split_scenes(rawA); scenesB=_split_scenes(rawB)
    align=align_scenes(scenesA, scenesB, thr=0.22)
    beatsB=detect_beats("\n\n".join(scenesB))
    # mapeia beats de B para índices correspondentes em A via alinhamento inverso
    mapBtoA={}
    for iA,iB,sim in align:
        mapBtoA[iB]=iA
    lines=["# GRAFT PLAN (B→A)",
           f"A = {pathA.name}",
           f"B = {pathB.name}",
           ""]
    for b in beatsB:
        iB=b["idx"]; iA=mapBtoA.get(iB, None)
        tag=b["beat"]; conf=b.get("conf",0.5)
        if iA is not None:
            lines.append(f"## {tag} — aplicar em A.scene#{iA} (confB={conf:.2f})")
            lines.append("- Ajustar set-up/payoff para amarrar com A1/A2 de A")
            lines.append("- Preservar persona/protagonismo de A, apenas importar estrutura do beat")
        else:
            lines.append(f"## {tag} — sem mapeamento direto (confB={conf:.2f})")
            lines.append("- Inserir nova cena em ponto equivalente no Ato correspondente")
        lines.append("")
    return "\n".join(lines)