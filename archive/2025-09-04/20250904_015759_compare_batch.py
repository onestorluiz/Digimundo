from __future__ import annotations
from pathlib import Path
from typing import List, Tuple, Dict
import csv

from .compare_search import nearest_to
from .compare_core import _read_text, _split_scenes
from .compare_search import _feat_vec as _feat_vec_from_search  # reuso

def _list_docs(root:Path, limit:int=60)->List[Path]:
    exts={".txt",".md",".fountain",".fdx",".pdf"}
    docs=[]
    for p in sorted(root.rglob("*")):
        if p.is_dir(): continue
        if p.suffix.lower() in exts: docs.append(p)
        if len(docs)>=limit: break
    return docs

def batch_matrix(root:Path, outdir:Path, limit:int=60)->Path:
    docs=_list_docs(root, limit=limit)
    if not docs: 
        out=outdir/"matrix.csv"; outdir.mkdir(parents=True, exist_ok=True)
        out.write_text("A,B,dist\n", encoding="utf-8"); return out

    # pré-computa vetores
    vecs={}
    for p in docs:
        vecs[str(p)]=_feat_vec_from_search(_read_text(p))

    # distância ponderada da compare_search (com pesos aprendidos, se houver)
    from .compare_search import _dist as dist
    outdir.mkdir(parents=True, exist_ok=True)
    out=outdir/"matrix.csv"
    with open(out,"w",encoding="utf-8",newline="") as f:
        w=csv.writer(f); w.writerow(["A","B","dist"])
        for i,a in enumerate(docs):
            for j,b in enumerate(docs):
                if j<=i: continue
                w.writerow([str(a), str(b), f"{dist(vecs[str(a)], vecs[str(b) ]):.6f}"])
    return out

def rank_against(ref:Path, root:Path, outdir:Path, topk:int=15)->Path:
    outdir.mkdir(parents=True, exist_ok=True)
    res = nearest_to(ref, root, topk=topk)
    out = outdir/f"rank_{ref.stem}.csv"
    with open(out,"w",encoding="utf-8",newline="") as f:
        w=csv.writer(f); w.writerow(["path","dist"])
        for p,d in res: w.writerow([p, f"{d:.6f}"])
    return out