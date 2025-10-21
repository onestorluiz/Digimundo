from __future__ import annotations
import re, itertools
from typing import Dict, List, Tuple
from collections import Counter

UPCASE = re.compile(r'(?m)^[ \t]*([A-Z][A-Z0-9 .\'\-()]{2,30})[ \t]*')

def extract_names(scene:str)->List[str]:
    names=[]
    for m in UPCASE.finditer(scene or ""):
        cand=(m.group(1) or "").strip()
        if cand.startswith(("INT.","EXT.","INT/EXT.","FADE","CUT","DISSOLVE","MONTAGE")): continue
        if cand.endswith("TO:"): continue
        if len(cand)<2: continue
        names.append(cand)
    return sorted(list(set(names)))

def build_graph(scenes:List[str])->Dict:
    nodes=Counter(); edges=Counter()
    for sc in scenes:
        names=extract_names(sc)
        for n in names: nodes[n]+=1
        for a,b in itertools.combinations(sorted(names),2):
            edges[(a,b)] += 1
    return {"nodes":dict(nodes), "edges":{f"{a}|||{b}":w for (a,b),w in edges.items()}}

def export_gexf(graph:Dict, path:str)->str:
    from xml.sax.saxutils import escape
    nodes=graph.get("nodes",{}); edges=graph.get("edges",{})
    with open(path,"w",encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?><gexf version="1.3"><graph mode="static" defaultedgetype="undirected">')
        f.write('<nodes>')
        for i,(name,w) in enumerate(nodes.items()):
            f.write(f'<node id="{i}" label="{escape(name)}"><attvalues><attvalue for="weight" value="{w}"/></attvalues></node>')
        f.write('</nodes><edges>')
        eid=0
        # map names to ids
        idx={n:i for i,n in enumerate(nodes.keys())}
        for key,w in edges.items():
            a,b=key.split("|||")
            if a in idx and b in idx:
                f.write(f'<edge id="{eid}" source="{idx[a]}" target="{idx[b]}" weight="{w}"/>'); eid+=1
        f.write('</edges></graph></gexf>')
    return path