
import re
from typing import Dict, List, Tuple
def default_state_lexicon() -> Dict[str, Dict[str, list]]:
    return {
        "aliança": {"formed": ["aliança formada","aliança selada","aliança","alliances","ally"],
                    "betrayed": ["traição","traído","quebrada","ruptura","rompida","betrayal","betrayed"]},
        "segredo": {"hidden": ["segredo","oculto","escondido","hidden","concealed"],
                    "revealed": ["revelado","descoberto","exposto","revealed","uncovered"]},
        "plano": {"planned": ["plano","estratégia","planejado","plan"],
                  "executing": ["executando","em ação","in motion","execute"],
                  "failed": ["falhou","fracassa","dá errado","fails","failed"]},
        "convicção": {"doubt": ["dúvida","hesita","hesitação","doubt","hesitates"],
                      "commit": ["decide","decisão","compromisso","commit","decides"]},
        "sacrifício": {"offered": ["sacrifício","renúncia","sacrifice"],
                       "fulfilled": ["consumado","realizado","cumprido","fulfilled"]}
    }
def infer_state_tags(text: str, lex: Dict[str, Dict[str, list]]) -> List[Tuple[str, str]]:
    t = (text or "").lower(); tags = []
    for motif, states in lex.items():
        for state, kws in states.items():
            if any(kw.lower() in t for kw in kws):
                tags.append((motif, state)); break
    return tags
def compute_arc_progress(beats_texts: Dict[str, str], arc_labels: List[str] | None = None, lexicon: Dict[str, Dict[str, list]] | None = None) -> Dict:
    if lexicon is None: lexicon = default_state_lexicon()
    arcs = [a.lower() for a in (arc_labels or [])]
    progress_scores = {bid: 0.0 for bid in beats_texts.keys()}
    events = []
    for bid, text in beats_texts.items():
        tags = infer_state_tags(text, lexicon)
        for motif, state in tags:
            if arcs and motif not in arcs: continue
            progress_scores[bid] += 1.0
            events.append({"beat_id": bid, "motif": motif, "state": state})
    return {"progress_scores": progress_scores, "events": events, "lexicon_used": list(lexicon.keys())}
