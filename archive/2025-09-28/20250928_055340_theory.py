from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple
from pathlib import Path
import re

TOKEN_RE = re.compile(r"[\w\-']+", re.U)
def _tok(t: str) -> List[str]:
    return [x.lower() for x in TOKEN_RE.findall(t or "")]

class BM25:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.docs: Dict[str, str] = {}
        self.tf: Dict[str, Dict[str, int]] = {}
        self.df: Dict[str, int] = {}
        self.dl: Dict[str, int] = {}
        self.N=0; self.avgdl=0.0
    def _recalc(self): self.avgdl = (sum(self.dl.values())/self.N) if self.N else 0.0
    def add(self, doc_id: str, text: str):
        from collections import Counter
        cnt = Counter(_tok(text))
        if doc_id in self.docs:
            self.N -= 1
            for t in self.tf[doc_id].keys(): self.df[t] -= 1
        self.docs[doc_id]=text; self.tf[doc_id]=dict(cnt); self.dl[doc_id]=sum(cnt.values()); self.N+=1
        for t in cnt.keys(): self.df[t] = self.df.get(t,0)+1
        self._recalc()
    def _idf(self, t: str) -> float:
        import math
        df=self.df.get(t,0)
        if df==0 or self.N==0: return 0.0
        return math.log(((self.N - df + 0.5) / (df + 0.5)) + 1.0)
    def search(self, q: str, k: int = 5):
        terms=set(_tok(q)); scores: Dict[str,float]={}; avgdl=self.avgdl or 1.0
        for doc_id, cnt in self.tf.items():
            dl=self.dl.get(doc_id,1) or 1; sc=0.0
            for t in terms:
                f=cnt.get(t,0)
                if f==0: continue
                idf=self._idf(t); denom=f + self.k1*(1 - self.b + self.b*(dl/avgdl))
                sc += idf * ((f*(self.k1+1))/denom)
            if sc>0: scores[doc_id]=sc
        return sorted(scores.items(), key=lambda x:x[1], reverse=True)[:max(1,k)]

@dataclass
class TheoryHit: doc_id: str; score: float; excerpt: str

class TheoryComparator:
    def __init__(self, base: Path):
        self.base = base; self.base.mkdir(parents=True, exist_ok=True); self.index = BM25()
    def build(self) -> int:
        n=0
        for p in self.base.glob("*.txt"):
            txt = p.read_text(encoding="utf-8", errors="replace")
            self.index.add(p.name, txt); n+=1
        return n
    def compare(self, query: str, k: int = 5) -> List[TheoryHit]:
        hits = self.index.search(query, k=k); out: List[TheoryHit]=[]
        for doc_id, score in hits:
            txt = (self.base/doc_id).read_text(encoding="utf-8", errors="replace")
            out.append(TheoryHit(doc_id=doc_id, score=float(score), excerpt=txt[:400]))
        return out
