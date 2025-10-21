from __future__ import annotations
import statistics, re
from typing import Dict, List, Any
from .beats_detect import detect_beats
from .character_graph import build_graph
from .pacing import energy_curve
from .themes import mine_motifs_by_act, theme_drift
from .qscore_storyiq import storyiq

def _norm(x,a,b):
    try:
        return max(0.0, min(100.0, 100.0*(x-a)/max(1e-9,b-a)))
    except Exception:
        return 0.0

def compute_breakdown(scenes:List[str], acts:Dict[int,List[str]], ctx_cites:List[str]|None)->Dict[str,float]:
    # Structure: presença de beats essenciais (0..5)
    beats = detect_beats("\n\n".join(scenes or []))
    have = set(b["beat"] for b in beats)
    essentials = ["INCITING_INCIDENT","BREAK_INTO_2","MIDPOINT","ALL_IS_LOST","CLIMAX"]
    structure = _norm(sum(1 for e in essentials if e in have), 0, len(essentials))
    # Characters: tamanho da rede (nós + arestas) normalizado
    g = build_graph(scenes)
    char_size = len(g.get("nodes",{})) + len(g.get("edges",{}))
    characters = _norm(char_size, 2, 40)
    # Pacing: variância de energia (excesso é ruim; ideal ~0.15..0.30) -> proximidade ao "bom"
    curve = energy_curve(scenes or [])
    vals = [p["energy"] for p in curve] or [0.0]
    var = statistics.pvariance(vals) if len(vals)>1 else 0.0
    pacing = 100.0 - min(100.0, abs(var-0.22)/0.22*100.0)
    # Theme: (1 - drift) -> estabilidade temática
    motifs = mine_motifs_by_act(acts, topk=12)
    drift = theme_drift(motifs.get(1,{}), motifs.get(2,{}), motifs.get(3,{}))
    theme = max(0.0, min(100.0, (1.0-drift)*100.0))
    # StoryIQ: aproveita citações + diversidade de atos
    cites = len(ctx_cites or [])
    act_spread = sum(1 for a in (1,2,3) if motifs.get(a))/3.0
    story = storyiq(1.0 if cites>=2 else 0.3, cites, act_spread, min(len(g.get("nodes",{})),8), var, drift)
    return {"Structure":round(structure,1),"Characters":round(characters,1),"Pacing":round(pacing,1),"Theme":round(theme,1),"StoryIQ":round(story,1)}