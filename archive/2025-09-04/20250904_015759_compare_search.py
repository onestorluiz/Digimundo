from __future__ import annotations
from pathlib import Path
import json, math
from typing import List, Tuple, Dict
from .compare_core import _read_text, _split_scenes
from .compare_core import structure_features, character_features, pacing_features, scenes_features, theme_features

# >>> ADIÇÃO: carregar pesos ensinados, se existirem
try:
    from .compare_teach import load_weights as _learn_weights
    _W_LEARNED = _learn_weights()  # fallback sem session
except Exception:
    _W_LEARNED = None

def _feat_vec(raw:str)->Dict[str,float]:
    sc=_split_scenes(raw)
    sf=structure_features(sc); cf=character_features(sc); pf=pacing_features(sc); tf=theme_features(sc); ss=scenes_features(sc)
    vec={
      "beats": len(sf["structure"]["present"]) if "structure" in sf else len(sf.get("present",[])),
      "nodes": cf["nodes"], "edges": cf["edges"],
      "pacing_var": pf["variance"],
      "themes_drift": tf["drift"],
      "scenes": ss["count"], "avglen": ss["avg_len"]
    }
    return vec

def _dist(a:Dict[str,float], b:Dict[str,float])->float:
    base={"beats":1.0,"nodes":0.6,"edges":0.6,"pacing_var":1.0,"themes_drift":1.0,"scenes":0.5,"avglen":0.4}
    w=_W_LEARNED or base
    return (
        w.get("beats",1.0)*abs(a.get("beats",0)-b.get("beats",0)) +
        w.get("nodes",0.6)*abs(a.get("nodes",0)-b.get("nodes",0)) +
        w.get("edges",0.6)*abs(a.get("edges",0)-b.get("edges",0)) +
        w.get("pacing_var",1.0)*abs(a.get("pacing_var",0)-b.get("pacing_var",0)) +
        w.get("themes_drift",1.0)*abs(a.get("themes_drift",0)-b.get("themes_drift",0)) +
        w.get("scenes",0.5)*abs(a.get("scenes",0)-b.get("scenes",0)) +
        w.get("avglen",0.4)*abs(a.get("avglen",0)-b.get("avglen",0))
    )

def nearest_to(path:Path, in_dir:Path, topk:int=5)->List[Tuple[str,float]]:
    rawA=_read_text(path); vA=_feat_vec(rawA)
    cands=[]
    if not in_dir.exists(): return []
    for p in in_dir.rglob("*"):
        if p.is_dir(): continue
        if p.suffix.lower() not in (".txt",".md",".fountain",".fdx",".pdf"): continue
        if p==path: continue
        rawB=_read_text(p); vB=_feat_vec(rawB)
        d=_dist(vA,vB)
        cands.append((str(p), d))
    cands.sort(key=lambda x: x[1])
    return cands[:topk]