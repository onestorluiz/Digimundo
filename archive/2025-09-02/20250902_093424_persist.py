# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import sqlite3, time, re
from collections import Counter
import math

DB_PATH = Path("data/memory/mem.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def _conn():
    c = sqlite3.connect(str(DB_PATH))
    c.execute("""CREATE TABLE IF NOT EXISTS mem(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts REAL, text TEXT, meta TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS kv(
        k TEXT PRIMARY KEY,
        v TEXT,
        meta TEXT,
        ts REAL
    )""")
    return c

def _tokens(text:str):
    return re.findall(r"[A-Za-z]{3,}", text.lower())

def remember(text:str, meta:str=""):
    c=_conn(); c.execute("INSERT INTO mem(ts,text,meta) VALUES(?,?,?)",(time.time(), text, meta)); c.commit(); c.close()

def remember_kv(key:str, text:str, meta:str=""):
    c=_conn()
    c.execute("INSERT OR REPLACE INTO kv(k,v,meta,ts) VALUES(?,?,?,?)",(key, text, meta, time.time()))
    c.commit(); c.close()

def _idf(all_docs):
    N=len(all_docs); idf={}
    vocab=set(t for d in all_docs for t in d)
    for term in vocab:
        df=sum(1 for d in all_docs if term in d)
        idf[term]=math.log((N+1)/(df+1))+1.0
    return idf

def recall(query:str, k:int=5):
    c=_conn(); rows=c.execute("SELECT id,text,meta FROM mem ORDER BY id ASC").fetchall(); c.close()
    docs=[_tokens(r[1]) for r in rows]
    if not docs: return []
    idf=_idf(docs)
    tq=Counter(_tokens(query))
    scores=[]
    for (rid, text, meta), d in zip(rows, docs):
        s=0.0
        for term,tf in tq.items():
            if term in d: s += (tf*1.0)*idf.get(term,0.0)
        scores.append((s, rid, text, meta))
    scores.sort(reverse=True)
    return [{"id":rid,"text":text,"meta":meta,"score":s} for s,rid,text,meta in scores[:k]]

def recall_by_meta(meta:str, k:int=3):
    c=_conn()
    rows=c.execute("SELECT k,v,meta,ts FROM kv WHERE meta=? ORDER BY ts DESC LIMIT ?", (meta, k)).fetchall()
    c.close()
    return [{"key":r[0], "text":r[1], "meta":r[2], "ts":r[3]} for r in rows]

def recall_by_key(key:str):
    c=_conn()
    r = c.execute("SELECT k,v,meta,ts FROM kv WHERE k=?", (key,)).fetchone()
    c.close()
    return {"key":r[0], "text":r[1], "meta":r[2], "ts":r[3]} if r else None