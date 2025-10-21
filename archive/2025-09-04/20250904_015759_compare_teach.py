from __future__ import annotations
from pathlib import Path
import json

STORE="teach.json"
DIMS=("structure","characters","pacing","theme","story")  # story ~ storyIQ

def _store_path(session)->Path:
    home=Path(getattr(session,"home","."))
    d=home/"reports"/"compare"; d.mkdir(parents=True, exist_ok=True)
    return d/STORE

def record_preference(session, docA:str, docB:str, dim:str, better:str)->Path:
    dim=dim.lower()
    if dim not in DIMS: raise ValueError("dim inválida")
    better = better.upper()  # "A" ou "B"
    p=_store_path(session)
    data={"prefs":[]}
    if p.exists():
        try: data=json.loads(p.read_text(encoding="utf-8"))
        except Exception: pass
    data["prefs"].append({"A":docA,"B":docB,"dim":dim,"better":better})
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2), encoding="utf-8")
    return p

def load_weights(session=None)->dict:
    # pesos base
    w={"beats":1.0,"nodes":0.6,"edges":0.6,"pacing_var":1.0,"themes_drift":1.0,"scenes":0.5,"avglen":0.4}
    # mapeia dims→features
    mapdim={
        "structure":["beats"],
        "characters":["nodes","edges"],
        "pacing":["pacing_var"],
        "theme":["themes_drift"],
        "story":["beats","pacing_var","themes_drift","nodes","edges"]
    }
    # carrega prefs e desloca pesos levemente
    try:
        if session is None: return w
        p=_store_path(session)
        if not p.exists(): return w
        data=json.loads(p.read_text(encoding="utf-8"))
        # simple tally: cada preferência aumenta 0.1 nos features da dimensão
        for pref in data.get("prefs",[]):
            dim=pref.get("dim"); feats=mapdim.get(dim,[])
            for f in feats:
                w[f]+=0.1
    except Exception:
        return w
    # normaliza para faixa sensata
    for k in w: w[k]=max(0.2, min(2.0, w[k]))
    return w