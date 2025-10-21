import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

class VectorStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.encoder = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
    
    def build_index(self, documents: List[str]):
        """Build FAISS index from documents"""
        self.documents = documents
        embeddings = self.encoder.encode(documents)
        
        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings.astype('float32'))
    
    def search(self, query: str, k: int = 10) -> List[Tuple[int, float, str]]:
        """Search for k nearest documents"""
        if self.index is None:
            return []
        
        query_embedding = self.encoder.encode([query])
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                results.append((idx, float(dist), self.documents[idx]))
        
        return results
