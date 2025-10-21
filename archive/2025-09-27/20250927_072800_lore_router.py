
from pathlib import Path
from typing import List
from .memory_store import Doc
from .rag_api import RAGService
from .snippet_utils import compress_extractive_tfidf
def index_lore_projects(rag: RAGService, lore_root: str) -> list[str]:
    root = Path(lore_root)
    projects=[]
    if not root.exists(): return projects
    for proj_dir in sorted([p for p in root.iterdir() if p.is_dir()]):
        proj = proj_dir.name; projects.append(proj)
        for md in proj_dir.glob("*.md"):
            text = md.read_text(encoding="utf-8")
            rag.index(Doc(id=f"{proj}:{md.name}", text=text, ns=f"lore:{proj}", meta={"project": proj, "file": md.name}))
    return projects
def route_projects(rag: RAGService, query: str, projects: List[str], top_k: int = 2) -> List[str]:
    scores = []
    for proj in projects:
        ns = f"lore:{proj}"; hits = rag.search(query, ns=ns, k=1)
        s = hits[0][1] if hits else 0.0; scores.append((proj, s))
    scores.sort(key=lambda x: x[1], reverse=True)
    return [p for p,_ in scores[:max(1, top_k)]]
def build_lore_blocks(rag: RAGService, selected_projects: List[str], query: str, max_chars: int = 420) -> list[str]:
    blocks=[]
    for proj in selected_projects:
        ns = f"lore:{proj}"; hits = rag.search(query, ns=ns, k=1)
        if hits:
            doc_id = hits[0][0]; text = rag.get_text(doc_id) or ""
            snip = compress_extractive_tfidf(text, query, max_chars=max_chars)
            blocks.append(f"[lore:{proj}:{doc_id}]\\n{snip}")
    return blocks
