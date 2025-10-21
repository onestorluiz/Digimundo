from .vector_store import VectorStore
import networkx as nx
from typing import List, Dict, Tuple

class HybridRAG:
    def __init__(self):
        self.vector_store = VectorStore()
        self.graph = nx.Graph()
        self.digilang_index = {}
    
    def index_documents(self, documents: List[str], digilang_docs: List[str] = None):
        """Index documents in all stores"""
        # Vector indexing
        self.vector_store.build_index(documents)
        
        # Graph indexing (simple co-occurrence)
        for i, doc in enumerate(documents):
            self.graph.add_node(i, text=doc[:100])
            
            # Connect similar documents
            for j in range(max(0, i-2), min(i+3, len(documents))):
                if i != j:
                    self.graph.add_edge(i, j, weight=1.0)
        
        # DigiLang symbolic indexing
        if digilang_docs:
            for i, doc in enumerate(digilang_docs):
                # Index by symbols present
                symbols = [s for s in doc if ord(s) > 127]  # Non-ASCII symbols
                for symbol in symbols:
                    if symbol not in self.digilang_index:
                        self.digilang_index[symbol] = []
                    self.digilang_index[symbol].append(i)
    
    def search(self, query: str, k: int = 10, use_rerank: bool = True) -> List[Dict]:
        """Hybrid search with optional narrative reranking"""
        # Get results from different methods
        vector_results = self.vector_store.search(query, k=k*2)
        
        # Combine and rerank
        combined_scores = {}
        for idx, dist, text in vector_results:
            combined_scores[idx] = {'score': 1.0 / (1.0 + dist), 'text': text}
        
        # Sort by score
        ranked = sorted(combined_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        return [{'id': idx, 'score': item['score'], 'text': item['text']} 
                for idx, item in ranked[:k]]
