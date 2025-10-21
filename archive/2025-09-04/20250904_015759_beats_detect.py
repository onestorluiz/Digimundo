from __future__ import annotations
import re, math
from typing import List, Dict, Any

# Fallbacks leves (usar segmentation oficial se existir)
try:
    from .segmentation import split_scenes, assign_acts
except Exception:
    def split_scenes(text:str):
        heads=[m.start() for m in re.finditer(r'(?m)^(INT\.|EXT\.|INT/EXT\.)', text or "")]
        if not heads: return [(0, text or "")]
        out=[]; n=len(text or "")
        for i,s in enumerate(heads):
            e=heads[i+1] if i+1<len(heads) else n
            out.append((s, (text or "")[s:e]))
        return out
    def assign_acts(scenes):
        n=len(scenes)
        thirds=[max(1,int(0.33*n)), max(2,int(0.66*n)), n]
        res=[]
        for i,(s,content) in enumerate(scenes):
            act = 1 if i<thirds[0] else (2 if i<thirds[1] else 3)
            res.append({"idx":i,"act":act,"text":content})
        return res

POS = set("win hope love justice succeed escape triumph help rescue resolve heal free unite".split())
NEG = set("lost die fail fear pain kill trap defeat betray collapse ruin doom break".split())

def _dialogue_ratio(scene:str)->float:
    # estimativa: linhas UPPERCASE curtas = personagens; parênteses = direções
    ups = len(re.findall(r'(?m)^[ \t]*[A-Z][A-Z0-9 .\'\-()]{2,30}', scene or ""))
    lines = max(1, len((scene or "").splitlines()))
    return min(1.0, ups/lines)

def _sentiment(scene:str)->float:
    toks=re.findall(r"[a-z']+", (scene or "").lower())
    if not toks: return 0.0
    p=sum(t in POS for t in toks); n=sum(t in NEG for t in toks)
    return (p - n)/max(1,(p+n))  # -1..+1

def detect_beats(script_text:str)->List[Dict[str,Any]]:
    scenes = [{"idx":i,"text":t} for i,(_,t) in enumerate(split_scenes(script_text or ""))]
    segs = assign_acts([(s["idx"], s["text"]) for s in scenes])
    # features por cena
    feats=[]
    for s in segs:
        dr=_dialogue_ratio(s["text"]); sv=_sentiment(s["text"])
        feats.append({"idx":s["idx"], "act":s["act"], "len":len(s["text"]), "dialogue":dr, "sent":sv})

    # heurísticas de beats (Save the Cat + Field + McKee)
    # -> inciting (A1 pico de variação de sentimento), break-into-2 (mudança), midpoint (pico de diálogo/len), all-is-lost/dark-night (sentimento muito negativo em A3-)
    beats=[]
    n=len(feats)
    if n==0: return beats
    # diffs de sentimento
    ds=[feats[i]["sent"]-feats[i-1]["sent"] for i in range(1,n)]
    # candidatos
    if ds:
        inc_idx = max(range(len(ds)), key=lambda i: abs(ds[i]))+1
        beats.append({"idx":inc_idx, "act":feats[inc_idx]["act"], "beat":"INCITING_INCIDENT", "conf":round(min(1.0,abs(ds[inc_idx-1])*0.9),2)})
    # midpoint por pico de len*dialogue em A2
    a2=[(i,f) for i,f in enumerate(feats) if f["act"]==2]
    if a2:
        mid_i = max(a2, key=lambda t: (t[1]["len"]* (0.6+0.8*t[1]["dialogue"])) )[0]
        beats.append({"idx":mid_i, "act":2, "beat":"MIDPOINT", "conf":0.7})
    # break-into-2: primeira cena de A2
    for i,f in enumerate(feats):
        if f["act"]==2: beats.append({"idx":i,"act":2,"beat":"BREAK_INTO_2","conf":0.6}); break
    # all-is-lost: mínimo de sentimento em A3- (ou fim de A2)
    a23=[(i,f) for i,f in enumerate(feats) if f["act"] in (2,3)]
    if a23:
        ail = min(a23, key=lambda t: t[1]["sent"])[0]
        beats.append({"idx":ail, "act":feats[ail]["act"], "beat":"ALL_IS_LOST","conf":0.65})
    # break-into-3: primeira cena A3
    for i,f in enumerate(feats):
        if f["act"]==3: beats.append({"idx":i,"act":3,"beat":"BREAK_INTO_3","conf":0.6}); break
    # climax: última cena
    beats.append({"idx":n-1, "act":feats[-1]["act"], "beat":"CLIMAX","conf":0.55})
    return beats

# framework mapping (apenas rótulos)
FRAMEWORKS = {
  "save_the_cat": ["OPENING_IMAGE","THEME_STATED","SETUP","INCITING_INCIDENT","DEBATE","BREAK_INTO_2","B_STORY","FUN_AND_GAMES","MIDPOINT","BAD_GUYS_CLOSE_IN","ALL_IS_LOST","DARK_NIGHT","BREAK_INTO_3","FINALE","FINAL_IMAGE"],
  "field_3act": ["INCITING_INCIDENT","PLOT_POINT_1","MIDPOINT","PLOT_POINT_2","CLIMAX","RESOLUTION"],
  "mckee": ["INCITING_INCIDENT","PROGRESSIVE_COMPLICATIONS","CRISIS","CLIMAX","RESOLUTION"]
}