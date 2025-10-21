
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set
import re
from .rag_api import RAGService
from .snippet_utils import compress_extractive_tfidf, best_snippet_by_query, _tokens

@dataclass
class HierOmegaPlusConfig:
    w_beat: float = 0.44
    w_scene: float = 0.30
    w_act: float = 0.18
    w_global: float = 0.08
    decay_base: float = 0.7
    proximity_gain: float = 0.6
    mmr_lambda: float = 0.72
    k_beat: int = 6
    k_scene: int = 3
    k_act: int = 2
    k_global: int = 1
    weight_amp: float = 0.25
    arc_boost: float = 0.20
    progress_boost: float = 0.25
    contig_window: int = 4
    clusters_k: int = 2
    gate_mode: str = 'window'    # 'window' | 'kmedoids'
    motif_boost: float = 0.15

def _scene_index_from_beat(doc_id: str) -> int | None:
    m = re.search(r"beat_(?:dyn_)?(\d+)_\d+", doc_id)
    return int(m.group(1)) if m else None

def locality_multi_cluster_gate(selected_docs: List[Tuple[str,str,float]], index_map: dict[str,int], window: int = 4, k: int = 2) -> List[Tuple[str,str,float]]:
    beats = [(lvl, d, s, index_map.get(d.replace("beat_",""), -1)) for (lvl,d,s) in selected_docs if d.startswith("beat_")]
    others = [(lvl,d,s,-1) for (lvl,d,s) in selected_docs if not d.startswith("beat_")]
    beats = [b for b in beats if b[3] >= 0]
    if not beats: 
        return selected_docs
    beats.sort(key=lambda x: x[3])
    chosen_clusters = []
    used = set()
    for _ in range(max(1, k)):
        best = ([], -1e9)
        for i in range(len(beats)):
            base_idx = beats[i][3]
            cur = []; sumscore = 0.0
            for j in range(i, len(beats)):
                if beats[j][3] - base_idx <= window-1:
                    if beats[j][3] in used: continue
                    cur.append(beats[j]); sumscore += beats[j][2]
            if sumscore > best[1]: best = (cur, sumscore)
        cluster = best[0]
        if not cluster: break
        chosen_clusters.append(cluster)
        for (_,_,_,gi) in cluster:
            used.add(gi)
    cluster_pairs = set((lvl,d) for cluster in chosen_clusters for (lvl,d,_,_) in cluster)
    boosted = []
    for (lvl,d,s) in selected_docs:
        if (lvl,d) in cluster_pairs: s = s * 1.15
        boosted.append((lvl,d,s))
    boosted.sort(key=lambda x: x[2], reverse=True)
    return boosted

def _kmedoids(indices: List[int], k: int, iters: int = 8) -> List[int]:
    if not indices: return []
    inds = sorted(indices)
    if k >= len(inds): return inds[:k]
    seeds = [inds[int(i*(len(inds)-1)/(k-1))] for i in range(k)]
    for _ in range(iters):
        clusters = {s: [] for s in seeds}
        for x in inds:
            best = min(seeds, key=lambda s: abs(x - s))
            clusters[best].append(x)
        new_seeds = []
        for s, xs in clusters.items():
            if not xs: new_seeds.append(s); continue
            best = min(xs, key=lambda m: sum(abs(m - y) for y in xs))
            new_seeds.append(best)
        if set(new_seeds) == set(seeds): break
        seeds = new_seeds
    return sorted(seeds)

def locality_kmedoids_gate(selected_docs: List[Tuple[str,str,float]], index_map: dict[str,int], k: int = 2) -> List[Tuple[str,str,float]]:
    beats = [(lvl, d, s, index_map.get(d.replace("beat_",""), -1)) for (lvl,d,s) in selected_docs if d.startswith("beat_")]
    others = [(lvl,d,s,-1) for (lvl,d,s) in selected_docs if not d.startswith("beat_")]
    beats = [b for b in beats if b[3] >= 0]
    if not beats: return selected_docs
    seeds = _kmedoids([b[3] for b in beats], k=max(1,k))
    chosen = set(seeds)
    boosted = []
    for (lvl,d,s,gi) in beats + others:
        if gi in chosen: s = s * 1.15
        boosted.append((lvl,d,s))
    boosted.sort(key=lambda x: x[2], reverse=True)
    return boosted

def hierarchical_search(rag: RAGService, queries: List[str], focus_scene_index: int | None, cfg: HierOmegaPlusConfig, features: dict, arc_scores: dict[str, float], progress_scores: dict[str, float], index_map: dict[str,int], motifs: List[str] | None = None) -> List[Tuple[str,str,float]]:
    items = []
    beat_hits = {}
    for q in queries:
        for d, s in rag.search(q, ns="script_beat", k=20):
            beat_hits[d] = max(beat_hits.get(d, 0.0), s)
    boosted = {}
    for d, s in beat_hits.items():
        wnorm = 0.66 if "dyn_" in d else 0.33
        if focus_scene_index is not None:
            si = _scene_index_from_beat(d) or focus_scene_index
            dist = abs(si - focus_scene_index)
            prox = 1.0 + cfg.proximity_gain * (cfg.decay_base ** dist)
        else:
            prox = 1.0
        bkey = d.replace("beat_","")
        arc = arc_scores.get(bkey, 0.0)
        progress = progress_scores.get(bkey, 0.0)
        arcb = 1.0 + cfg.arc_boost * min(1.0, arc) if arc > 0 else 1.0
        prob = 1.0 + cfg.progress_boost * min(1.0, progress) if progress > 0 else 1.0
        # motif router boost
        mboost = 1.0
        if motifs:
            txt = (rag.get_text(d) or '').lower()
            for m in motifs:
                if any(t in txt for t in _tokens(m)):
                    mboost = max(mboost, 1.0 + cfg.motif_boost)
        boosted[d] = s * prox * (1.0 + cfg.weight_amp * wnorm) * arcb * prob * mboost
    sel = sorted(boosted, key=lambda x: boosted[x], reverse=True)[:cfg.k_beat]
    items += [("beat", d, cfg.w_beat * boosted[d]) for d in sel]
    scene_hits = {}
    for q in queries:
        for d, s in rag.search(q, ns="script_scene", k=8):
            scene_hits[d] = max(scene_hits.get(d, 0.0), s)
    scene_sel = sorted(scene_hits, key=lambda x: scene_hits[x], reverse=True)[:cfg.k_scene]
    items += [("scene", d, cfg.w_scene * scene_hits[d]) for d in scene_sel]
    act_hits = {}
    for q in queries:
        for d, s in rag.search(q, ns="script_act", k=5):
            act_hits[d] = max(act_hits.get(d, 0.0), s)
    act_sel = sorted(act_hits, key=lambda x: act_hits[x], reverse=True)[:cfg.k_act]
    items += [("act", d, cfg.w_act * act_hits[d]) for d in act_sel]
    glob_hits = {}
    for q in queries:
        for d, s in rag.search(q, ns="script_global", k=1):
            glob_hits[d] = max(glob_hits.get(d, 0.0), s)
    if glob_hits:
        d = sorted(glob_hits, key=lambda x: glob_hits[x], reverse=True)[:cfg.k_global]
        items += [("global", x, cfg.w_global * glob_hits[x]) for x in d]
    items.sort(key=lambda x: x[2], reverse=True)
    if features.get("locality_gate", True):
        if getattr(cfg, 'gate_mode', 'window') == 'kmedoids':
            items = locality_kmedoids_gate(items, index_map=index_map, k=int(cfg.clusters_k))
        else:
            items = locality_multi_cluster_gate(items, index_map=index_map, window=int(cfg.contig_window), k=int(cfg.clusters_k))
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
