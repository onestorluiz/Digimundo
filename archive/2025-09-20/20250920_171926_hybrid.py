from typing import List, Dict, Any
from rank_bm25 import BM25Okapi
import numpy as np
from ..models.embeddings import EmbeddingModel
from ..storage.vectorstore import get_vectorstore
from ..models.reranker import Reranker
from ..storage.cache import get_or_set
from ..config import load_config

_cfg = load_config()

class HybridRetriever:
    def __init__(self, collection: str = "scripturemon"):
        self.store = get_vectorstore(collection)
        self.embed = EmbeddingModel()
        self.reranker = Reranker(_cfg.reranker.model_name)
        self._bm25 = None
        self._bm25_docs = []
        self._bm25_ids = []

    def build_bm25(self, ids: List[str], docs: List[str]):
        tokenized = [d.lower().split() for d in docs]
        self._bm25 = BM25Okapi(tokenized)
        self._bm25_docs = tokenized
        self._bm25_ids = ids

    def add(self, ids: List[str], embeddings, docs: List[str], metadatas: List[dict]):
        self.store.add(ids, embeddings, docs, metadatas)
        self.build_bm25(ids, docs)

    def search(self, query: str, where: dict = None, top_k: int = None) -> List[Dict[str, Any]]:
        top_k = top_k or _cfg.rag.top_k

        def _factory():
            q_emb = self.embed.embed([query]).tolist()
            vec_res = self.store.query(q_emb, n_results=top_k, where=where)
            vec_docs = vec_res.get("documents", [[]])[0]
            vec_ids = vec_res.get("ids", [[]])[0]
            vec_md  = vec_res.get("metadatas", [[]])[0]

            bm_docs, bm_ids = [], []
            if self._bm25:
                scores = self._bm25.get_scores(query.lower().split())
                idxs = np.argsort(scores)[::-1][:_cfg.rag.hybrid_bm25_k]
                for i in idxs:
                    bm_docs.append(" ".join(self._bm25_docs[i]))
                    bm_ids.append(self._bm25_ids[i])

            combined = {i: {"id": i, "doc": d, "meta": m} for i, d, m in zip(vec_ids, vec_docs, vec_md)}
            for i, d in zip(bm_ids, bm_docs):
                if i not in combined:
                    combined[i] = {"id": i, "doc": d, "meta": {}}

            docs = [v["doc"] for v in combined.values()]
            ids  = [k for k in combined.keys()]
            rr = self.reranker.rerank(query, docs, top_k=_cfg.rag.rerank_top_k)
            ranked = [{"id": ids[idx], "doc": docs[idx], "score": float(score), "meta": combined[ids[idx]]["meta"]} for idx, score in rr]
            return ranked

        return get_or_set("hybrid_search", {"q": query, "where": where, "top_k": top_k}, _factory, expire=600)
