from typing import Dict, Any, List
from pathlib import Path
import json, math, re
DATA_DIR = Path('data'); (DATA_DIR / 'rag').mkdir(parents=True, exist_ok=True)
IDX_PATH = DATA_DIR / 'rag' / 'index.json'
TOKEN_RE = re.compile(r"[\w\-']+", re.U)
def _tok(t: str): return [x.lower() for x in TOKEN_RE.findall(t or '')]
class _RAGIndex:
    def __init__(self, path: Path = IDX_PATH):
        self.path = path; self.docs={}; self.df={}; self.N=0; self._load()
    def _load(self):
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text(encoding='utf-8'))
                self.docs = data.get('docs', {}); self.df = data.get('df', {}); self.N = data.get('N', 0)
            except Exception:
                self.docs = {}; self.df = {}; self.N = 0
    def _save(self):
        self.path.write_text(json.dumps({'docs': self.docs, 'df': self.df, 'N': self.N}, ensure_ascii=False, indent=2), encoding='utf-8')
    def index(self, doc_id: str, text: str, metadata: Dict[str, Any] | None = None):
        tokens = _tok(text); cnt = {}
        for t in tokens: cnt[t] = cnt.get(t,0)+1
        if doc_id in self.docs:
            old = self.docs[doc_id]['tf']
            for t in old.keys():
                self.df[t] = self.df.get(t,1) - 1
                if self.df[t] <= 0: self.df.pop(t, None)
        else:
            self.N += 1
        self.docs[doc_id] = {'text': text, 'tf': cnt, 'metadata': metadata or {}}
        for t in cnt.keys(): self.df[t] = self.df.get(t,0)+1
        self._save()
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        terms = set(_tok(query)); out=[]; avgdl = (sum(sum(x['tf'].values()) for x in self.docs.values())/max(1,self.N)) if self.N else 1.0
        for doc_id, d in self.docs.items():
            tf = d['tf']; dl=sum(tf.values()) or 1; score=0.0
            for t in terms:
                f = tf.get(t,0)
                if f==0: continue
                idf = math.log(((self.N - self.df.get(t,0) + 0.5) / (self.df.get(t,0) + 0.5)) + 1.0)
                denom = f + 1.5*(1 - 0.75 + 0.75*(dl / avgdl))
                score += idf * ((f*(1.5+1))/denom)
            if score>0:
                out.append({'doc_id': doc_id, 'score': score, 'metadata': d.get('metadata', {})})
        out.sort(key=lambda x: x['score'], reverse=True)
        return out[:max(1, top_k)]
_IDX = _RAGIndex()
def index_document(doc_id: str, text: str, metadata: Dict[str, Any] | None = None):
    _IDX.index(doc_id, text, metadata or {})
def search_documents(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    return _IDX.search(query, top_k=top_k)
