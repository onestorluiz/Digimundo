
from .bm25 import BM25
from .memory_store import Doc, MemoryStore
class RAGService:
    def __init__(self):
        self.ms=MemoryStore()
        self.indices: dict[str, BM25] = {}
        self.links: dict[str, list[str]] = {}
    def index(self, doc: Doc):
        self.ms.add(doc)
        if doc.ns not in self.indices:
            self.indices[doc.ns]=BM25()
        self.indices[doc.ns].add(doc.id, doc.text)
    def search(self, query: str, ns: str, k=5):
        idx=self.indices.get(ns)
        if not idx: return []
        return idx.search(query, k=k)
    def link(self, analysis_id: str, doc_ids: list[str]):
        self.links.setdefault(analysis_id, []).extend(doc_ids)
    def get_text(self, doc_id: str) -> str | None:
        d = self.ms.by_id(doc_id)
        return d.text if d else None
