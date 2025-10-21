
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set
import re
from .rag_api import RAGService
from .memory_store import Doc
from .snippet_utils import compress_extractive_tfidf, best_snippet_by_query, _tokens

@dataclass
class HierPro3Config:
    w_beat: float = 0.46
    w_scene: float = 0.30
    w_act: float = 0.16
    w_global: float = 0.08
    decay_base: float = 0.7
    proximity_gain: float = 0.6
    mmr_lambda: float = 0.72
    k_beat: int = 5
    k_scene: int = 3
    k_act: int = 2
    k_global: int = 1
    weight_amp: float = 0.25  # amplificação por peso do beat (suposta pelo id dyn_)

def index_hierarchical(rag: RAGService, scenes: List, beats: List, acts: Dict[str, tuple]):
    # beats
    for b in beats:
        rag.index(Doc(id=f"beat_{b.id}", text=b.text, ns="script_beat", meta={"scene_index": str(b.scene_index), "idx_in_scene": str(b.idx_in_scene), "weight": str(b.weight)}))
    # scenes
    for i, sc in enumerate(scenes, start=1):
        rag.index(Doc(id=f"scene_{i}", text=sc.text, ns="script_scene", meta={"title": sc.title, "scene_index": str(i)}))
    # acts
    for act_id, (start_line, end_line) in acts.items():
        buf = []
        for i, sc in enumerate(scenes, start=1):
            if sc.start_line >= start_line and sc.end_line <= end_line:
                buf.append(sc.text)
        rag.index(Doc(id=act_id, text="\\n\\n".join(buf), ns="script_act", meta={"range": f"{start_line}-{end_line}"}))
    # global
    rag.index(Doc(id="global1", text="\\n\\n".join(sc.text for sc in scenes), ns="script_global", meta={"src":"all"}))

def _normalize_hits(hits):
    if not hits: return {}
    m = max((s for _, s in hits), default=1.0) or 1.0
    return {d: (s/m) for d, s in hits}

def _combine_hits_max(hit_lists):
    out = {}
    for hits in hit_lists:
        norm = _normalize_hits(hits)
        for d, s in norm.items():
            out[d] = max(out.get(d, 0.0), s)
    return out

def _mmr_select(candidates: Dict[str,float], get_text, lam=0.72, k=3):
    selected = []
    tokens = {d: set(_tokens(get_text(d) or "")) for d in candidates.keys()}
    def jacc(a,b):
        A,B = tokens[a], tokens[b]
        inter = len(A & B); union = len(A | B) or 1
        return inter/union
    pool = dict(candidates)
    while pool and len(selected) < k:
        best, best_val = None, -1e9
        for d, rel in pool.items():
            div = 0.0
            if selected:
                div = max(jacc(d, s) for s in selected)
            val = lam*rel - (1-lam)*div
            if val > best_val:
                best, best_val = d, val
        selected.append(best)
        pool.pop(best, None)
    return selected

def _scene_index_from_beat(doc_id: str) -> int | None:
    m = re.search(r"beat_(?:dyn_)?(\\d+)_\\d+", doc_id)
    return int(m.group(1)) if m else None

def hierarchical_search(rag: RAGService, queries: List[str], focus_scene_index: int | None, cfg: HierPro3Config, features: dict, anchors: Set[str]) -> List[Tuple[str,str,float]]:
    items = []
    # beats
    beat_hits = _combine_hits_max([rag.search(q, ns="script_beat", k=15) for q in queries])
    boosted = {}
    for d, s in beat_hits.items():
        # weight amp (heurística via id dyn_)
        wnorm = 0.66 if "dyn_" in d else 0.33
        # proximity by scene
        if focus_scene_index is not None:
            si = _scene_index_from_beat(d) or focus_scene_index
            dist = abs(si - focus_scene_index)
            prox = 1.0 + cfg.proximity_gain * (cfg.decay_base ** dist)
        else:
            prox = 1.0
        # anchor-aware boost: se texto do beat contiver âncoras do excerto
        txt = (rag.get_text(d) or "").lower()
        anchor_hit = any(a in txt for a in anchors) if anchors else False
        anchor_boost = 1.10 if (features.get("graph_boost", True) and anchor_hit) else 1.0
        boosted[d] = s * prox * (1.0 + cfg.weight_amp * wnorm) * anchor_boost
    sel = _mmr_select(boosted, rag.get_text, lam=cfg.mmr_lambda, k=cfg.k_beat) if features.get("mmr", True) \
          else sorted(boosted, key=lambda x: boosted[x], reverse=True)[:cfg.k_beat]
    items += [("beat", d, cfg.w_beat * boosted[d]) for d in sel]
    # scenes
    scene_hits = _combine_hits_max([rag.search(q, ns="script_scene", k=8) for q in queries])
    scene_sel = sorted(scene_hits, key=lambda x: scene_hits[x], reverse=True)[:cfg.k_scene]
    items += [("scene", d, cfg.w_scene * scene_hits[d]) for d in scene_sel]
    # acts
    act_hits = _combine_hits_max([rag.search(q, ns="script_act", k=5) for q in queries])
    act_sel = sorted(act_hits, key=lambda x: act_hits[x], reverse=True)[:cfg.k_act]
    items += [("act", d, cfg.w_act * act_hits[d]) for d in act_sel]
    # global
    glob_hits = _combine_hits_max([rag.search(q, ns="script_global", k=1) for q in queries])
    if glob_hits:
        d = sorted(glob_hits, key=lambda x: glob_hits[x], reverse=True)[:cfg.k_global]
        items += [("global", x, cfg.w_global * glob_hits[x]) for x in d]
    items.sort(key=lambda x: x[2], reverse=True)
    return items[: (cfg.k_beat + cfg.k_scene + cfg.k_act + cfg.k_global)]

def build_blocks(rag: RAGService, docs, excerpt: str, features: dict):
    blocks = []
    from .snippet_utils import compress_extractive_tfidf, best_snippet_by_query, make_queries
    q0 = make_queries(excerpt)[0] if make_queries(excerpt) else excerpt[:64]
    for level, doc_id, _ in docs:
        txt = rag.get_text(doc_id) or ""
        if features.get("tfidf", True):
            snip = compress_extractive_tfidf(txt, q0, max_chars=420, redundancy=0.6)
        else:
            snip = best_snippet_by_query(txt, q0, win_chars=420, step=140)
        blocks.append(f"[{level}:{doc_id}]\\n{snip}")
    return blocks
