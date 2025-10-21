from typing import Dict, Any
import os, time, uuid
from .pdf_loader import extract_pdf_text_per_page
from .chunking import split_by_scenes, smart_chunk
from ..models.embeddings import EmbeddingModel
from ..retrieval.hybrid import HybridRetriever
from ..storage.memory_layers import append_l2
from ..config import load_config
from .analyzers import detect_structure, extract_techniques, brutal_score

_cfg = load_config()

def process_pdf(path: str, doc_type: str = "roteiro_criador") -> Dict[str, Any]:
    t0 = time.time()
    pages = extract_pdf_text_per_page(path)
    scenes = split_by_scenes(pages, _cfg.chunking.scene_markers) if _cfg.chunking.scene_split else [{"text":"\n".join(pages), "start_page":1, "end_page":len(pages)}]
    chunks = smart_chunk([s["text"] for s in scenes], _cfg.chunking.target_tokens, _cfg.chunking.overlap_tokens)

    embedder = EmbeddingModel()
    retriever = HybridRetriever(collection="scripturemon")
    ids = [f"{os.path.basename(path)}::{i}" for i in range(len(chunks))]
    vecs = embedder.embed(chunks)
    metas = [{"page_hint": scenes[min(i, len(scenes)-1)].get("start_page", 1), "source": path, "doc_type": doc_type} for i in range(len(chunks))]
    retriever.add(ids, vecs.tolist(), chunks, metas)

    full_text = "\n".join(pages)[:30000]
    structure = detect_structure(full_text)
    techs = extract_techniques(full_text)
    score = brutal_score(full_text)

    result = {
        "metadados": {
            "arquivo": path,
            "paginas": len(pages),
            "tipo": doc_type,
            "hash": str(uuid.uuid4())
        },
        "estrutura": structure,
        "tecnicas": techs,
        "avaliacao": score,
        "stats": {"processing_seconds": time.time() - t0, "chunks": len(chunks)}
    }
    append_l2({"ts": time.time(), "arquivo": path, "estrutura": structure, "tecnicas": techs[:10], "avaliacao": score})
    return result
