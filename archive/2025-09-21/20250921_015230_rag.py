from __future__ import annotations
import math, re
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Optional
TOKEN_RE = re.compile(r"[\w\-']+", re.U)
def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text or '')]
@dataclass
class Doc:
    doc_id: str; text: str; metadata: dict
class BM25Index:
    def __init__(self, k1: float=1.5, b: float=0.75):
        self.docs: Dict[str, Doc] = {}
        self.tf: Dict[str, Counter] = {}
        self.df: Counter = Counter()
        self.doc_len: Dict[str, int] = {}
        self.N: int = 0; self.avgdl: float = 0.0
        self.k1=float(k1); self.b=float(b)
    def _update_avgdl(self):
        self.avgdl = (sum(self.doc_len.values())/self.N) if self.N else 0.0
    def _remove_if_exists(self, doc_id: str):
        if doc_id in self.docs:
            old = self.tf.get(doc_id, Counter())
            for t in old: self.df[t]-=1; 
            self.N-=1; self.docs.pop(doc_id, None); self.tf.pop(doc_id, None); self.doc_len.pop(doc_id, None)
    def add(self, doc_id: str, text: str, metadata: Optional[dict]=None):
        if not doc_id: raise ValueError('doc_id vazio')
        cnt = Counter(tokenize(text))
        self._remove_if_exists(doc_id)
        self.docs[doc_id]=Doc(doc_id, text, metadata or {})
        self.tf[doc_id]=cnt; self.doc_len[doc_id]=sum(cnt.values())
        for t in cnt: self.df[t]+=1
        self.N+=1; self._update_avgdl()
    def _idf(self, t: str)->float:
        df=self.df.get(t,0); N=self.N
        if df==0 or N==0: return 0.0
        return math.log(((N - df + 0.5) / (df + 0.5)) + 1.0)
    def search(self, query: str, top_k: int = 5):
        if self.N==0: return []
        q_terms=set(tokenize(query)); scores: Dict[str, float] = {}
        avgdl=self.avgdl or 1.0
        for doc_id, dcnt in self.tf.items():
            dl=self.doc_len.get(doc_id,0) or 1; score=0.0
            for t in q_terms:
                f=dcnt.get(t,0)
                if f==0: continue
                idf=self._idf(t); denom=f + self.k1*(1 - self.b + self.b*(dl/avgdl))
                score += idf * ((f*(self.k1+1))/denom)
            if score>0: scores[doc_id]=score
        ranked=sorted(scores.items(), key=lambda x:x[1], reverse=True)
        return ranked[:max(1, top_k)]
_INDEX = BM25Index()
def index_document(doc_id: str, text: str, metadata: Optional[dict]=None): _INDEX.add(doc_id, text, metadata)
def search_documents(query: str, top_k: int = 5):
    res=_INDEX.search(query, top_k=top_k); out=[]
    for doc_id, score in res:
        doc=_INDEX.docs.get(doc_id)
        out.append({'doc_id':doc_id,'score':float(score),'metadata':doc.metadata,'excerpt':doc.text[:300]})
    return out
