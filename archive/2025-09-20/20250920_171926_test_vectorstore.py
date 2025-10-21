from app.storage.vectorstore import get_vectorstore
from app.models.embeddings import EmbeddingModel

def test_store_roundtrip():
    store = get_vectorstore("test")
    emb = EmbeddingModel()
    docs = ["um texto de teste", "outro texto de teste"]
    vecs = emb.embed(docs).tolist()
    ids = ["a","b"]
    metas = [{"k":"v"},{"k":"z"}]
    store.add(ids, vecs, docs, metas)
    res = store.get(ids)
    assert set(res["ids"]) == set(ids)
