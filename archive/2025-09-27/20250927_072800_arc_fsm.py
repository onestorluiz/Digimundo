
from dataclasses import dataclass
from typing import Dict, List
@dataclass
class FSMEvent:
    beat_id: str
    state: str
    idx: int
ORDER = {
    "aliança": ["formed","betrayed"],
    "segredo": ["hidden","revealed"],
    "plano":   ["planned","executing","failed"],
    "convicção":["doubt","commit"],
    "sacrifício":["offered","fulfilled"]
}
def _state_rank(motif: str, state: str) -> int:
    seq = ORDER.get(motif, [])
    return seq.index(state) if state in seq else 999
def build_fsm(beats_texts: Dict[str,str], index_map: Dict[str,int], events: List[Dict]) -> Dict:
    by_motif: Dict[str, List[FSMEvent]] = {}
    for ev in events:
        bid = ev.get("beat_id")
        if bid not in index_map: continue
        mot = ev.get("motif"); st = ev.get("state")
        by_motif.setdefault(mot, []).append(FSMEvent(beat_id=bid, state=st, idx=index_map[bid]))
    fsm = {}
    for mot, lst in by_motif.items():
        lst.sort(key=lambda e: e.idx)
        comp = []
        for e in lst:
            if comp and comp[-1].idx == e.idx:
                prev = comp[-1]
                if _state_rank(mot, e.state) >= _state_rank(mot, prev.state):
                    comp[-1] = e
                continue
            comp.append(e)
        trans = []
        nodes = set()
        prev = None
        for e in comp:
            nodes.add(e.state)
            if prev and e.state != prev.state:
                trans.append({"from": prev.state, "to": e.state, "at_beat": e.beat_id, "delta": e.idx - prev.idx})
            prev = e
        fsm[mot] = {"states_order": ORDER.get(mot, []),
                    "nodes": sorted(list(nodes), key=lambda s: _state_rank(mot, s)),
                    "sequence": [{"beat_id": e.beat_id, "state": e.state, "idx": e.idx} for e in comp],
                    "transitions": trans}
    return {"fsm": fsm}
