from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Tuple
import re, math, json

# Reuso de módulos existentes
from .beats_detect import detect_beats
from .character_graph import build_graph
from .pacing import energy_curve
from .themes import mine_motifs_by_act, theme_drift

# --- util: leitura em texto (txt/fountain/pdf fallback) ---
def _read_text(p:Path)->str:
    if not p.exists(): return ""
    if p.suffix.lower() in (".txt",".fountain",".fdx",".md"):
        try: return p.read_text(encoding="utf-8", errors="ignore")
        except Exception: return p.read_text(errors="ignore")
    if p.suffix.lower()==".pdf":
        try:
            import PyPDF2
            txt=[]; 
            with open(p,"rb") as f:
                r=PyPDF2.PdfReader(f)
                for page in r.pages: txt.append(page.extract_text() or "")
            return "\n".join(txt)
        except Exception:
            return ""
    # qualquer outro: tentativa bruta
    try: return p.read_text(encoding="utf-8", errors="ignore")
    except Exception: return ""
    
def _split_scenes(raw:str)->List[str]:
    if not raw: return []
    parts=re.split(r'(?m)^(INT\.|EXT\.|INT/EXT\.)', raw)
    if len(parts)<=1: return [raw]
    scenes=[]
    for i in range(0,len(parts),2):
        seg="".join(parts[i:i+2]).strip()
        if seg: scenes.append(seg)
    return scenes

# --- TF-IDF caseiro para alinhamento de cenas ---
def _tokenize(s:str)->List[str]:
    return re.findall(r"[a-z']+", (s or "").lower())

def _tfidf_vectors(scenes:List[str])->List[Dict[str,float]]:
    docs=[_tokenize(s) for s in scenes]
    df={}
    for d in docs:
        for t in set(d): df[t]=df.get(t,0)+1
    N=max(1,len(docs))
    vecs=[]
    for d in docs:
        tf={}
        for t in d: tf[t]=tf.get(t,0)+1
        v={}
        for t,c in tf.items():
            idf=math.log((N+1)/(1+df.get(t,1)))+1.0
            v[t]= (c/len(d)) * idf
        vecs.append(v)
    return vecs

def _cos(a:Dict[str,float], b:Dict[str,float])->float:
    if not a or not b: return 0.0
    inter=set(a.keys()) & set(b.keys())
    num=sum(a[t]*b[t] for t in inter)
    na=math.sqrt(sum(x*x for x in a.values())); nb=math.sqrt(sum(x*x for x in b.values()))
    if na*nb==0: return 0.0
    return num/(na*nb)

def align_scenes(A:List[str], B:List[str], thr:float=0.22)->List[Tuple[int,int,float]]:
    # Greedy monotônico simples (ordem preservada)
    VA=_tfidf_vectors(A); VB=_tfidf_vectors(B)
    jstart=0; pairs=[]
    for i,va in enumerate(VA):
        best_j=-1; best_sim=0.0
        for j in range(jstart, len(VB)):
            sim=_cos(va, VB[j])
            if sim>best_sim: best_sim, best_j = sim, j
        if best_j>=0 and best_sim>=thr:
            pairs.append((i,best_j,best_sim))
            jstart=best_j+1
    return pairs

# --- Features & Deltas ---
def _acts_from_scenes(scenes:List[str])->Dict[int,List[str]]:
    n=len(scenes)
    if n==0: return {1:[],2:[],3:[]}
    a1=int(0.33*n) or 1; a2=int(0.66*n) or 2
    return {1:scenes[:a1], 2:scenes[a1:a2], 3:scenes[a2:]}

def structure_features(scenes:List[str])->Dict:
    beats=detect_beats("\n\n".join(scenes))
    essentials = ["INCITING_INCIDENT","BREAK_INTO_2","MIDPOINT","ALL_IS_LOST","CLIMAX"]
    present = {b["beat"]:b for b in beats if b["beat"] in essentials}
    normpos = {k: (present[k]["idx"]/max(1,len(scenes)-1)) for k in present}
    return {"beats":beats, "present":list(present.keys()), "normpos":normpos, "n_scenes":len(scenes)}

def character_features(scenes:List[str])->Dict:
    g=build_graph(scenes)
    nodes=len(g.get("nodes",{})); edges=len(g.get("edges",{}))
    return {"nodes":nodes, "edges":edges}

def pacing_features(scenes:List[str])->Dict:
    cur=energy_curve(scenes)
    ev=[p["energy"] for p in cur] or [0.0]
    import statistics
    var=statistics.pvariance(ev) if len(ev)>1 else 0.0
    return {"variance":var, "energy":ev}

def theme_features(scenes:List[str])->Dict:
    acts=_acts_from_scenes(scenes)
    motifs=mine_motifs_by_act(acts, topk=10)
    drift=theme_drift(motifs.get(1,{}), motifs.get(2,{}), motifs.get(3,{}))
    return {"motifs":motifs, "drift":drift}

def scenes_features(scenes:List[str])->Dict:
    lens=[len(s or "") for s in scenes]
    import statistics as st
    return {"count":len(scenes), "avg_len": (st.mean(lens) if lens else 0), "median_len": (st.median(lens) if lens else 0)}

def compare_docs(pathA:Path, pathB:Path)->Dict:
    rawA=_read_text(pathA); rawB=_read_text(pathB)
    scenesA=_split_scenes(rawA); scenesB=_split_scenes(rawB)
    # features
    fa={"structure":structure_features(scenesA),
        "characters":character_features(scenesA),
        "pacing":pacing_features(scenesA),
        "theme":theme_features(scenesA),
        "scenes":scenes_features(scenesA)}
    fb={"structure":structure_features(scenesB),
        "characters":character_features(scenesB),
        "pacing":pacing_features(scenesB),
        "theme":theme_features(scenesB),
        "scenes":scenes_features(scenesB)}
    # deltas
    deltas={
      "beats_present_delta": sorted(list(set(fa["structure"]["present"]) ^ set(fb["structure"]["present"]))),
      "midpoint_pos_delta": abs(fa["structure"]["normpos"].get("MIDPOINT",0.0) - fb["structure"]["normpos"].get("MIDPOINT",0.0)),
      "char_nodes_delta": fb["characters"]["nodes"] - fa["characters"]["nodes"],
      "char_edges_delta": fb["characters"]["edges"] - fa["characters"]["edges"],
      "pacing_var_delta": fb["pacing"]["variance"] - fa["pacing"]["variance"],
      "theme_drift_delta": fb["theme"]["drift"] - fa["theme"]["drift"],
      "scene_count_delta": fb["scenes"]["count"] - fa["scenes"]["count"],
      "avg_len_delta": fb["scenes"]["avg_len"] - fa["scenes"]["avg_len"],
    }
    # alinhamento cena→cena
    align=align_scenes(scenesA, scenesB, thr=0.22)
    return {"A":str(pathA), "B":str(pathB), "featuresA":fa, "featuresB":fb, "deltas":deltas, "alignment":align}