from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json
from .embeddings import OllamaEmbeddings

@dataclass
class ProtoModel:
    prototypes: Dict[str, List[float]]
    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.prototypes), encoding="utf-8")
    @staticmethod
    def load(path: Path) -> "ProtoModel":
        return ProtoModel(prototypes=json.loads(path.read_text(encoding="utf-8")))

def _vec_add(a: List[float], b: List[float]) -> List[float]:
    n = max(len(a), len(b))
    a = a + [0.0]*(n-len(a)); b = b + [0.0]*(n-len(b))
    return [x+y for x,y in zip(a,b)]
def _vec_div(a: List[float], s: float) -> List[float]:
    return [x/s for x in a] if s>0 else a
def _cos(a: List[float], b: List[float]) -> float:
    n = min(len(a), len(b))
    if n==0: return 0.0
    dot = sum(a[i]*b[i] for i in range(n))
    na = sum(a[i]*a[i] for i in range(n)) ** 0.5
    nb = sum(b[i]*b[i] for i in range(n)) ** 0.5
    if na==0 or nb==0: return 0.0
    return dot/(na*nb)

class ProtoTrainer:
    def __init__(self, embedder: Optional[OllamaEmbeddings] = None):
        self.embedder = embedder or OllamaEmbeddings()
    def fit(self, labeled_texts: Dict[str, List[str]]) -> ProtoModel:
        protos = {}
        for label, texts in labeled_texts.items():
            vecs = self.embedder.embed(texts)
            if not vecs: continue
            acc = [0.0]*len(vecs[0])
            for v in vecs: acc = _vec_add(acc, v)
            protos[label] = _vec_div(acc, float(len(vecs)))
        return ProtoModel(prototypes=protos)
    def predict(self, model: ProtoModel, texts: List[str]) -> List[Tuple[str, float]]:
        vecs = self.embedder.embed(texts); out=[]
        for v in vecs:
            best,score="",-1.0
            for label, proto in model.prototypes.items():
                s=_cos(v, proto)
                if s>score: best,score=label,s
            out.append((best,score))
        return out
