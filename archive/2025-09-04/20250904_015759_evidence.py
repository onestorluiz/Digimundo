from __future__ import annotations
import re
def evidence_score(citations:list[str], min_unique=2)->float:
    if not citations: return 0.0
    uniq=len(set(citations))
    return max(0.0, min(1.0, uniq/float(min_unique)))
def memory_score(mem_hits:int, mem_total:int=10)->float:
    if mem_total<=0: return 0.0
    return max(0.0, min(1.0, mem_hits/float(mem_total)))
def coherence_score(texts:list[str])->float:
    if not texts: return 0.0
    bags=[set(re.findall(r"\w+", t.lower())) for t in texts if t]
    if len(bags)<2: return 0.5
    inter=set.intersection(*bags) if len(bags)>1 else set()
    base=sum(len(b) for b in bags)/max(1,len(bags))
    return max(0.0, min(1.0, len(inter)/max(1,base)))