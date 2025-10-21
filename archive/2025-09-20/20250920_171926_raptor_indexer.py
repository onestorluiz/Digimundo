from typing import List, Dict, Any
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from ..models.embeddings import EmbeddingModel
from ..models.ollama_client import OllamaLLM
from ..storage.vectorstore import get_vectorstore

_llm = OllamaLLM()

def raptor_build_tree(docs: List[str], level_size: int = 12, collection: str = "scripturemon_raptor") -> Dict[str, Any]:
    embedder = EmbeddingModel()
    X = embedder.embed(docs)
    n_clusters = max(2, len(docs)//level_size)
    clustering = AgglomerativeClustering(n_clusters=n_clusters, affinity="cosine", linkage="average")
    labels = clustering.fit_predict(X)

    parent_texts = []
    mapping = {}
    for c in range(n_clusters):
        group = [docs[i] for i in range(len(docs)) if labels[i]==c]
        summary = _llm.generate("Resuma criticamente (100-150 palavras) o seguinte conjunto de trechos de roteiro, focando estrutura e técnica:\n\n" + "\n---\n".join(group))
        parent_texts.append(summary)
        mapping[c] = [i for i in range(len(docs)) if labels[i]==c]

    store = get_vectorstore(collection)
    ids = [f"node:{i}" for i in range(len(parent_texts))]
    embs = embedder.embed(parent_texts).tolist()
    metas = [{"type":"raptor_parent","children":mapping[i]} for i in range(len(parent_texts))]
    store.add(ids, embs, parent_texts, metas)
    return {"n_parents": len(parent_texts), "mapping": mapping}
