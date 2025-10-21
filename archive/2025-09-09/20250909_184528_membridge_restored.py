# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import json, sqlite3, time

# L1: memória de trabalho (processo)
_L1:list[dict]=[]

def l1_add(item:dict):
    _L1.append({"t":time.time(),"data":item})
    if len(_L1)>100: _L1.pop(0)

def l2_store(item:dict, path:Path=Path("runtime/l2_shortterm.json")):
    arr=[]
    if path.exists():
        try: arr=json.loads(path.read_text(encoding="utf-8"))
        except: arr=[]
    arr.append({"t":time.time(),"data":item})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(arr[-1000:], indent=2), encoding="utf-8")

def l3_store(item:dict, db:Path=Path("runtime/l3_longterm.sqlite")):
    db.parent.mkdir(parents=True, exist_ok=True)
    con=sqlite3.connect(str(db))
    con.execute("create table if not exists mem (ts real, kind text, payload text)")
    con.execute("insert into mem values (?,?,?)", (time.time(), item.get("kind","note"), json.dumps(item)))
    con.commit(); con.close()

def promote(item:dict, importance:float=0.5):
    # heurística: importa para L3 se importance>=0.5; L2 sempre
    l1_add(item); l2_store(item)
    if importance>=0.5: l3_store(item)

def counts()->dict:
    c2=0
    p=Path("runtime/l2_shortterm.json")
    if p.exists():
        try: c2=len(json.loads(p.read_text(encoding="utf-8")))
        except: c2=0
    c3=0
    db=Path("runtime/l3_longterm.sqlite")
    if db.exists():
        try:
            import sqlite3
            con=sqlite3.connect(str(db))
            c3=con.execute("select count(*) from mem").fetchone()[0]
            con.close()
        except: c3=0
    return {"L1":len(_L1), "L2":c2, "L3":c3, "L4":"n/a"}

# Alias for compatibility with MemoryLocator
class MemoryBridge:
    """Bridge class for membridge functions"""
    
    def __init__(self):
        pass
    
    def save(self, content: str, memory_type: str = "general", **kwargs) -> bool:
        """Save using promote"""
        try:
            promote({"content": content, "type": memory_type}, importance=kwargs.get("importance", 0.5))
            return True
        except:
            return False
    
    def save_memory(self, content: str, memory_type: str = "general", **kwargs) -> bool:
        """Alias for save"""
        return self.save(content, memory_type, **kwargs)
    
    def get_context(self, query: str, **kwargs) -> list:
        """Get context - returns empty as membridge is write-only"""
        return []
    
    def get_stats(self) -> dict:
        """Get stats using counts"""
        return counts()
