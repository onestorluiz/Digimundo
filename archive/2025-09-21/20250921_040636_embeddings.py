from __future__ import annotations
import hashlib
from dataclasses import dataclass
from typing import List
try:
    import requests
except Exception:
    requests = None

@dataclass
class EmbeddingsConfig:
    model: str = "nomic-embed-text"
    endpoint: str = "http://127.0.0.1:11434/api/embeddings"
    timeout: int = 30

class OllamaEmbeddings:
    def __init__(self, cfg: EmbeddingsConfig = EmbeddingsConfig()):
        self.cfg = cfg
    def embed(self, texts: List[str]) -> List[List[float]]:
        if requests is None:
            return [self._hash_embed(t) for t in texts]
        out = []
        for t in texts:
            try:
                r = requests.post(self.cfg.endpoint, json={"model": self.cfg.model, "prompt": t}, timeout=self.cfg.timeout)
                vec = r.json().get("embedding", [])
                if not isinstance(vec, list) or not vec:
                    vec = self._hash_embed(t)
            except Exception:
                vec = self._hash_embed(t)
            out.append(vec)
        return out
    def _hash_embed(self, text: str, dim: int = 256) -> List[float]:
        h = hashlib.sha256(text.encode("utf-8")).digest()
        arr = [x/255.0 for x in h[:min(dim, len(h))]]
        if len(arr) < dim: arr += [0.0]*(dim - len(arr))
        return arr
