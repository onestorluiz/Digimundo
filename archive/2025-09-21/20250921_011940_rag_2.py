# RAG minimalista (stdlib): índice bag-of-words + cosseno
from __future__ import annotations
import math, json, re
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple, Iterable, Optional

TOKEN_RE = re.compile(r"[\w\-']+", re.U)

def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text or "")]

@dataclass
class Doc:
    doc_id: str
    text: str
    metadata: dict | None = None

class SimpleVectorIndex:
    def __init__(self):
        self.docs: Dict[str, Doc] = {}
        self.tf: Dict[str, Counter] = {}          # doc_id -> term counts
        self.df: Counter = Counter()              # term -> doc freq
        self.norm: Dict[str, float] = {}          # doc_id -> vector norm

    def add(self, doc_id: str, text: str, metadata: Optional[dict] = None):
        if not doc_id:
            raise ValueError("doc_id vazio")
        tokens = tokenize(text)
        cnt = Counter(tokens)
        # Atualiza estruturas
        self.docs[doc_id] = Doc(doc_id, text, metadata or {})
        self.tf[doc_id] = cnt
        for term in cnt:
            self.df[term] += 1
        # Norm (tf-only cosseno)
        self.norm[doc_id] = math.sqrt(sum((c*c) for c in cnt.values())) or 1.0

    def search(self, query: str, top_k: int = 5) -> list[tuple[str, float]]:
        q_cnt = Counter(tokenize(query))
        q_norm = math.sqrt(sum((c*c) for c in q_cnt.values())) or 1.0
        scores = []
        for doc_id, dcnt in self.tf.items():
            dot = sum(dcnt[t]*q_cnt.get(t, 0) for t in q_cnt)
            if not dot:
                continue
            score = dot / (self.norm[doc_id] * q_norm)
            scores.append((doc_id, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:max(1, top_k)]

# API de módulo (compatível com features.rag_system wrapper)
_INDEX = SimpleVectorIndex()

def index_document(doc_id: str, text: str, metadata: Optional[dict] = None):
    _INDEX.add(doc_id, text, metadata)

def search_documents(query: str, top_k: int = 5) -> list[dict]:
    res = _INDEX.search(query, top_k=top_k)
    out = []
    for doc_id, score in res:
        doc = _INDEX.docs.get(doc_id)
        out.append({"doc_id": doc_id, "score": float(score), "metadata": doc.metadata, "excerpt": doc.text[:300]})
    return out
