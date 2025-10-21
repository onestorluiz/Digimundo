
import math, re
from collections import defaultdict, Counter
TOKEN = re.compile(r"\w+", re.UNICODE)
class BM25:
    def __init__(self, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.N=0; self.avgdl=0.0
        self.doc_len={}; self.df=defaultdict(int); self.inv=defaultdict(dict); self.docs={}
    def add(self, doc_id: str, text: str):
        tokens=[t.lower() for t in TOKEN.findall(text)]
        tf=Counter(tokens); self.docs[doc_id]=text; self.doc_len[doc_id]=len(tokens)
        for t, c in tf.items(): self.inv[t][doc_id]=c
        for t in tf: self.df[t]+=1
        self.N=len(self.docs); self.avgdl=sum(self.doc_len.values())/max(1,self.N)
    def _score(self, qtokens, doc_id):
        score=0.0; dl=self.doc_len[doc_id]
        for t in qtokens:
            df=self.df.get(t,0)
            if df==0: continue
            idf = math.log(1 + (self.N - df + 0.5)/(df + 0.5))
            tf = self.inv[t].get(doc_id,0)
            denom = tf + self.k1 * (1 - self.b + self.b * dl/self.avgdl)
            score += idf * (tf * (self.k1+1)) / (denom + 1e-9)
        return score
    def search(self, query: str, k=5):
        qtokens=[t.lower() for t in TOKEN.findall(query)]
        cand=set()
        for t in qtokens: cand |= set(self.inv.get(t, {}).keys())
        scored=[(doc, self._score(qtokens, doc)) for doc in cand]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]
