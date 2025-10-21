from typing import List, Dict, Any, Optional, Tuple
import chromadb
from chromadb.config import Settings
from ..config import load_config
import os

_cfg = load_config()

class ChromaStore:
    def __init__(self, collection: str = "scripturemon"):
        os.makedirs(_cfg.paths.chroma_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=_cfg.paths.chroma_dir, settings=Settings(allow_reset=True))
        self.collection = self.client.get_or_create_collection(name=collection, metadata={"hnsw:space":"cosine"})

    def add(self, ids: List[str], embeddings, documents: List[str], metadatas: List[dict]):
        self.collection.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

    def query(self, query_embeddings, n_results: int = 8, where: Optional[dict] = None):
        return self.collection.query(query_embeddings=query_embeddings, n_results=n_results, where=where)

    def get(self, ids: List[str]):
        return self.collection.get(ids=ids)

def get_vectorstore(collection: str = "scripturemon"):
    return ChromaStore(collection)
