from __future__ import annotations
from pathlib import Path
from typing import List
import re, time
from .compare_core import _read_text, _split_scenes, align_scenes
from .beats_detect import detect_beats

def apply_graft(A:Path, B:Path)->Path:
    rawA=_read_text(A); rawB=_read_text(B)
    scenesA=_split_scenes(rawA); scenesB=_split_scenes(rawB)
    align=align_scenes(scenesA, scenesB, thr=0.22)
    beatsB=detect_beats("\n\n".join(scenesB))
    # índice B -> índice A estimado
    mapBtoA={iB:iA for (iA,iB,sim) in align}
    # gera cópia anotada de A
    out=[]
    for i,sc in enumerate(scenesA):
        out.append(sc)
        # inserir após a cena, se houver beat mapeado para ela
        for b in beatsB:
            if mapBtoA.get(b["idx"], None)==i:
                out.append(f"\n[[GRAFT:{b['beat']} from {B.name}]]\n- Ajustar set-up/payoff para A\n- Preservar voz; importar estrutura/posição dramática\n")
    # fallback: beats sem mapeamento → acrescentar ao fim
    nomap=[b for b in beatsB if b["idx"] not in mapBtoA]
    if nomap:
        out.append("\n# GRAFT (nomap)\n")
        for b in nomap:
            out.append(f"[[GRAFT:{b['beat']}]] inserir nova cena no ato correspondente\n")
    out_text="\n\n".join(out)
    outdir=A.parent
    p=outdir/(f"{A.stem}_GRAFTED_{time.strftime('%Y%m%d-%H%M%S')}.txt")
    p.write_text(out_text, encoding="utf-8")
    return p