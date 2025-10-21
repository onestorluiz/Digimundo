
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set
import re

UPCASE = re.compile(r"^[A-Z .'-]{2,}$")
PROP = re.compile(r"(?:[A-ZÁ-Ú][a-zá-ú]+(?:\s+[A-ZÁ-Ú][a-zá-ú]+){0,2})")

def _chars_from_text(text: str) -> Set[str]:
    chars=set()
    for l in text.splitlines():
        if UPCASE.match(l.strip()):
            name = re.sub(r"[^A-Z .'-]", "", l.strip()).strip()
            if len(name) >= 2: chars.add(name)
    return chars

def _props_from_text(text: str) -> Set[str]:
    return set([p.strip() for p in PROP.findall(text)])

def build_scene_graph(beats: list, scenes_count: int) -> dict:
    nodes = {}; edges = []; node_degree = {}
    for b in beats:
        chars = _chars_from_text(b.text)
        props = _props_from_text(b.text)
        for c in chars:
            nid = f"char:{c}"; nodes.setdefault(nid, {"id": nid, "label": c, "type": "character"})
        for p in props:
            nid = f"topic:{p}"; nodes.setdefault(nid, {"id": nid, "label": p, "type": "topic"})
        C = list(chars)
        for i in range(len(C)):
            for j in range(i+1, len(C)):
                s, t = f"char:{C[i]}", f"char:{C[j]}"
                edges.append((s,t,1.0,"cooccur"))
        for c in chars:
            for p in props:
                edges.append((f"char:{c}", f"topic:{p}", 0.5, "mentions"))
    agg = {}
    for s,t,w,k in edges:
        key = (s,t,k)
        agg[key] = agg.get(key, 0.0) + w
    edges2 = [{"source": s, "target": t, "weight": w, "kind": k} for (s,t,k), w in agg.items()]
    for e in edges2:
        node_degree[e["source"]] = node_degree.get(e["source"], 0.0) + e["weight"]
        node_degree[e["target"]] = node_degree.get(e["target"], 0.0) + e["weight"]
    for nid, n in nodes.items():
        n["score"] = round(float(node_degree.get(nid, 0.0)), 3)
    return {"nodes": list(nodes.values()), "edges": edges2, "beats": [{"id": b.id, "scene": b.scene_index, "idx": b.idx_in_scene, "weight": b.weight} for b in beats], "scenes": scenes_count}
