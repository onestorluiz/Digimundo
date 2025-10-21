from typing import List, Tuple
from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self, model_name: str):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, docs: List[str], top_k: int = 8) -> List[Tuple[int, float]]:
        pairs = [(query, d) for d in docs]
        scores = self.model.predict(pairs)
        ranked = sorted(list(enumerate(scores)), key=lambda x: x[1], reverse=True)[:top_k]
        return ranked
