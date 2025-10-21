#!/usr/bin/env python3
"""
V3.1 DELTA — RAG real com ChromaDB (se disponível).

Uso:
  CHROMA_PATH=./data/chroma python tools/fix_v3/rag_real.py --docs data/pdfs --out reports/fix_v3/rag_real.json
"""
import argparse, json, os, re
from pathlib import Path

def find_docs(root: Path, exts=(".pdf",".txt",".md"), max_docs=None):
    docs = [p for p in root.rglob("*") if p.suffix.lower() in exts]
    if max_docs:
        return docs[:max_docs]
    return docs

def run(out_path: Path, docs_root: Path):
    out = {"mode": "chroma", "ok": False, "docs_indexed": 0, "samples": []}
    dbpath = os.environ.get("CHROMA_PATH", str(Path("data/chroma").resolve()))
    try:
        import chromadb  # type: ignore
        client = chromadb.PersistentClient(path=dbpath)
        coll = client.get_or_create_collection("v3_1_docs")
        docs = find_docs(docs_root) if docs_root.exists() else []
        # ingest minimal: store filenames + simple content for txt/md; for PDFs, store path only (stub content)
        added = 0
        for i, p in enumerate(docs):
            doc_id = f"doc_{i}_{p.name}"
            try:
                text = p.read_text(encoding="utf-8", errors="ignore") if p.suffix.lower() in (".txt",".md") else f"PDF:{p.name}"
            except Exception:
                text = f"{p.name}"
            coll.add(ids=[doc_id], documents=[text], metadatas=[{"source": str(p)}])
            added += 1
        out["docs_indexed"] = added
        # simple queries: use parts of filenames
        for p in docs[:3]:
            q = re.sub(r"[_\-.]+"," ", p.stem)[:40]
            res = coll.query(query_texts=[q], n_results=5)
            out["samples"].append({
                "query": q,
                "top_sources": [m.get("source") for m in (res.get("metadatas") or [[]])[0]]
            })
        out["ok"] = True
    except Exception as e:
        out["error"] = str(e)
        out["ok"] = False

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[rag_real] gravado: {out_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default="data/pdfs")
    ap.add_argument("--out", default="reports/fix_v3/rag_real.json")
    args = ap.parse_args()
    run(Path(args.out), Path(args.docs))