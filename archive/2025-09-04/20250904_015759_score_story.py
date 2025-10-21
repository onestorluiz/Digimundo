from __future__ import annotations
import statistics
from typing import List, Dict, Any
from .qscore_storyiq import storyiq
from .pacing import energy_curve
from .themes import mine_motifs_by_act, theme_drift

def compute_storyiq(scenes:List[str], acts:dict, evidence:float, cites:int, char_net:int)->dict:
    curve = energy_curve(scenes)
    ev_vals = [p["energy"] for p in curve] or [0.0]
    var = statistics.pvariance(ev_vals) if len(ev_vals)>1 else 0.0
    motifs = mine_motifs_by_act(acts, topk=10)
    drift = theme_drift(motifs.get(1,{}), motifs.get(2,{}), motifs.get(3,{}))
    # diversidade de atos nas citações
    act_set=set()
    for a in (1,2,3):
        if motifs.get(a): act_set.add(a)
    act_spread = len(act_set)/3.0
    score = storyiq(evidence, cites, act_spread, char_net, var, drift)
    return {"score":score, "var_energy":var, "theme_drift":drift, "act_spread":act_spread}