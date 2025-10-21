from __future__ import annotations
import re
from typing import List, Dict

def scene_len(scene:str)->int: return len(scene or "")
def dialogue_ratio(scene:str)->float:
    ups = len(re.findall(r'(?m)^[ \t]*[A-Z][A-Z0-9 .\'\-()]{2,30}[ \t]*', scene or ""))
    lines = max(1, len((scene or "").splitlines()))
    return min(1.0, ups/lines)
def novelty(a:str,b:str)->float:
    import math
    A=set(re.findall(r"[a-z']+", (a or "").lower()))
    B=set(re.findall(r"[a-z']+", (b or "").lower()))
    if not A or not B: return 0.5
    inter=len(A&B); uni=len(A|B)
    return 1.0 - inter/max(1,uni)  # 0..1; maior => mais novidade

def energy_curve(scenes:List[str])->List[Dict]:
    out=[]
    prev=""
    for i,sc in enumerate(scenes):
        out.append({
            "idx": i,
            "len": scene_len(sc),
            "dialogue": dialogue_ratio(sc),
            "novelty": novelty(prev, sc),
            "energy": 0.4*dialogue_ratio(sc) + 0.3*novelty(prev, sc) + 0.3*min(1.0, scene_len(sc)/1200.0)
        })
        prev = sc
    return out

def pacing_warnings(curve:List[Dict])->List[str]:
    warns=[]
    # platôs longos (baixa variação)
    for i in range(2, len(curve)):
        e0, e1, e2 = curve[i-2]["energy"], curve[i-1]["energy"], curve[i]["energy"]
        if abs(e0-e1)<0.05 and abs(e1-e2)<0.05:
            warns.append(f"Plateau de energia em cenas {i-2}-{i} (variação < 0.05)")
            break
    return warns