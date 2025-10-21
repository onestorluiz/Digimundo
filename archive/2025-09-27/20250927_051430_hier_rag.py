
from .rag_api import RAGService
from .memory_store import Doc
from .snippet_utils import compress_extractive_tfidf, best_snippet_by_query, _tokens
from dataclasses import dataclass
from typing import List, Dict, Tuple
import math, re

@dataclass
class HierConfig:
    w_scene: float = 0.65
    w_act: float = 0.25
    w_global: float = 0.10
    decay_base: float = 0.7   # proximity decay per scene distance
    proximity_gain: float = 0.5
    mmr_lambda: float = 0.72
    k_scene: int = 4
    k_act: int = 2
    k_global: int = 1

def index_hierarchical(rag: RAGService, scenes: List, acts: Dict[str, Tuple[int,int]]):
    # Index scenes into ns=script_scene
    for i, sc in enumerate(scenes, start=1):
        doc_id = f"scene_{i}"
        rag.index(Doc(id=doc_id, text=sc.text, ns="script_scene", meta={"title": sc.title, "scene_index": str(i)}))
    # Index acts into ns=script_act
    for act_id, (start_line, end_line) in acts.items():
        # Concatenate scene texts in range by approximating line boundaries
        # (we already have scenes; merge all scenes whose start_line within range)
        buf = []
        for i, sc in enumerate(scenes, start=1):
            if sc.start_line >= start_line and sc.end_line <= end_line:
                buf.append(sc.text)
        rag.index(Doc(id=act_id, text="\n\n".join(buf), ns="script_act", meta={"range": f"{start_line}-{end_line}"}))
    # Global doc
    global_text = "\n\n".join(sc.text for sc in scenes)
    rag.index(Doc(id="global1", text=global_text, ns="script_global", meta={"src":"all"}))

def _normalize_hits(hits: List[Tuple[str, float]]) -> Dict[str, float]:
    if not hits: return {}
    m = max((s for _, s in hits), default=1.0) or 1.0
    return {d: (s/m) for d, s in hits}

def _combine_hits_max(hit_lists: List[List[Tuple[str,float]]]) -> Dict[str, float]:
    out = {}
    for hits in hit_lists:
        norm = _normalize_hits(hits)
        for d, s in norm.items():
            out[d] = max(out.get(d, 0.0), s)
    return out

def _mmr_select(candidates: Dict[str, float], get_text, lam=0.72, k=3):
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

def _scene_index_from_id(doc_id: str) -> int | None:
    m = re.search(r"scene_(\d+)", doc_id)
    return int(m.group(1)) if m else None

def hierarchical_search(rag: RAGService, queries: List[str], focus_scene_index: int | None, cfg: HierConfig, features: dict) -> List[Tuple[str,str,float]]:
    # Return list of (level, doc_id, score)
    out = []
    # Scene level
    if features.get("hier", True):
        scene_hits = _combine_hits_max([rag.search(q, ns="script_scene", k=8) for q in queries])
        # proximity boost
        boosted = {}
        for d, s in scene_hits.items():
            if focus_scene_index is not None:
                idx = _scene_index_from_id(d)
                if idx is not None:
                    dist = abs(idx - focus_scene_index)
                    boost = 1.0 + cfg.proximity_gain * (cfg.decay_base ** dist)
                else:
                    boost = 1.0
            else:
                boost = 1.0
            boosted[d] = s * boost
        if features.get("mmr", True):
            sel = _mmr_select(boosted, rag.get_text, lam=cfg.mmr_lambda, k=cfg.k_scene)
        else:
            sel = sorted(boosted, key=lambda x: boosted[x], reverse=True)[:cfg.k_scene]
        out += [("scene", d, cfg.w_scene * boosted[d]) for d in sel]
        # Act level
        act_hits = _combine_hits_max([rag.search(q, ns="script_act", k=5) for q in queries])
        act_sel = (sorted(act_hits, key=lambda x: act_hits[x], reverse=True)[:cfg.k_act])
        out += [("act", d, cfg.w_act * act_hits[d]) for d in act_sel]
        # Global
        glob_hits = _combine_hits_max([rag.search(q, ns="script_global", k=1) for q in queries])
        if glob_hits:
            d = sorted(glob_hits, key=lambda x: glob_hits[x], reverse=True)[:cfg.k_global]
            out += [("global", x, cfg.w_global * glob_hits[x]) for x in d]
    else:
        # Non-hierarchical fallback: search in "script_scene" only (equiv. old 'script')
        base_hits = _combine_hits_max([rag.search(q, ns="script_scene", k=8) for q in queries])
        if features.get("mmr", True):
            sel = _mmr_select(base_hits, rag.get_text, lam=cfg.mmr_lambda, k=3)
        else:
            sel = sorted(base_hits, key=lambda x: base_hits[x], reverse=True)[:3]
        out += [("scene", d, base_hits[d]) for d in sel]
    # sort by score desc and keep top 3
    out.sort(key=lambda x: x[2], reverse=True)
    return out[:3]

def build_blocks(rag: RAGService, docs: List[Tuple[str,str,float]], excerpt: str, features: dict) -> List[str]:
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
