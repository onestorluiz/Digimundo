# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import json, math, re, sqlite3, os
from collections import Counter

DBV_PATH = Path("data/memory/memvec.db")
DBV_PATH.parent.mkdir(parents=True, exist_ok=True)

def _conn():
    c = sqlite3.connect(str(DBV_PATH))
    c.execute("""CREATE TABLE IF NOT EXISTS memvec(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meta TEXT, text TEXT, vec TEXT, ts REAL
    )""")
    return c

# -------- Embedding backends --------
_model = None
def _try_load_model():
    global _model
    if _model is not None: return _model
    try:
        from sentence_transformers import SentenceTransformer
        name = os.environ.get("DL_EMB_MODEL","all-MiniLM-L6-v2")
        _model = SentenceTransformer(name)
    except Exception:
        _model = None
    return _model

def _tokens(text:str):
    return re.findall(r"[A-Za-z]{3,}", text.lower())

def _hashing_vec(text:str, dim:int=384):
    v = [0.0]*dim
    for t in _tokens(text):
        h = hash(t) % dim
        v[h] += 1.0
    # l2 normalize
    n = math.sqrt(sum(x*x for x in v)) or 1.0
    return [x/n for x in v]

def embed(text:str):
    m = _try_load_model()
    if m is not None:
        try:
            vec = m.encode([text], normalize_embeddings=True)[0].tolist()
            return vec
        except Exception:
            pass
    return _hashing_vec(text)

def cosine(a,b):
    s = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a)) or 1.0
    nb = math.sqrt(sum(y*y for y in b)) or 1.0
    return s/(na*nb)

# -------- API --------
def remember_embed(meta:str, text:str):
    vec = embed(text)
    c=_conn()
    import time
    c.execute("INSERT INTO memvec(meta,text,vec,ts) VALUES(?,?,?,?)",
              (meta, text, json.dumps(vec), time.time()))
    c.commit(); c.close()

def recall_embed(query:str, k:int=3):
    qv = embed(query)
    c=_conn()
    rows = c.execute("SELECT id,meta,text,vec,ts FROM memvec").fetchall()
    c.close()
    scored=[]
    for rid, meta, text, vecj, ts in rows:
        try:
            v = json.loads(vecj)
        except Exception:
            continue
        scored.append((cosine(qv, v), rid, meta, text))
    scored.sort(reverse=True)
    out=[]
    for s,rid,meta,text in scored[:k]:
        # Retorna tuplas (meta, text, score) para compatibilidade
        out.append((meta, text, float(s)))
    return out

# Classe wrapper para compatibilidade
class EmbedStore:
    """Wrapper class para compatibilidade com testes"""
    
    def __init__(self):
        pass
    
    def add(self, text: str, meta: dict):
        """Adiciona embedding ao store"""
        meta_str = json.dumps(meta) if isinstance(meta, dict) else str(meta)
        remember_embed(meta_str, text)
    
    def recall_embed(self, query: str, top_k: int = 3):
        """Busca embeddings similares"""
        return recall_embed(query, k=top_k)