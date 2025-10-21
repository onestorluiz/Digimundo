
from typing import Set
def select_arcs_from_graph(scene_graph: dict, top_k: int = 2, allow_types: Set[str] | None = None) -> list[dict]:
    allow = allow_types or {"character","topic"}
    nodes = [n for n in scene_graph.get("nodes", []) if n.get("type") in allow]
    nodes.sort(key=lambda n: n.get("score", 0.0), reverse=True)
    return nodes[:max(1, top_k)]
def score_beats_for_arcs(beats: list[dict], text_by_beat: dict[str,str], arcs: list[dict]) -> dict:
    scores = {b["id"]: 0.0 for b in beats}
    anchors = []
    for a in arcs:
        t = "char" if a.get("type")=="character" else "topic"
        lab = a.get("label","")
        anchors.append((t, lab, float(a.get("score", 0.0))))
    for b in beats:
        bt = (text_by_beat.get(f"beat_{b['id']}") or "").lower()
        for t, lab, s in anchors:
            if not lab: continue
            if lab.lower() in bt:
                scores[b["id"]] += (1.0 + s * 0.2)
    return scores
