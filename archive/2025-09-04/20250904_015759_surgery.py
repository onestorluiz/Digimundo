from __future__ import annotations
from typing import List, Dict, Any

def build_surgery_plan(beats:List[Dict], curve:List[Dict], warns:List[str])->Dict[str,Any]:
    # heurísticas: fundir cenas curtas consecutivas; cortar platôs; reforçar beats
    cuts=[]; merges=[]
    for i in range(1,len(curve)):
        if curve[i]["len"]<300 and curve[i-1]["len"]<300:
            merges.append({"merge":[i-1,i],"reason":"duas cenas curtas consecutivas; fundir para ritmo"})
    for w in warns:
        cuts.append({"target":"plateau_zone","reason":w})
    anchors=[b for b in beats if b["beat"] in ("MIDPOINT","BREAK_INTO_2","ALL_IS_LOST","BREAK_INTO_3","CLIMAX")]
    plan={"anchors":anchors, "merges":merges, "cuts":cuts, "notes":["rever escalada de conflito entre midpoint e all_is_lost"]}
    return plan