# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
from datetime import datetime
import hashlib, json, shutil, threading, time, os

ROOT = Path.home()/".scripturemon"/"soul"
ROOT.mkdir(parents=True, exist_ok=True)
RUN = {"on": False}

def _checksum(dirp:Path)->str:
    h=hashlib.sha256()
    for p in sorted(dirp.rglob("*")):
        if p.is_file() and p.name!="checksum.sha256":
            h.update(p.read_bytes())
    return h.hexdigest()

def _snapshot(dst:Path):
    dst.mkdir(parents=True, exist_ok=True)
    # copia fontes de estado conhecidas (consciência, persona, memória local)
    sources = [
        Path.home()/".scripturemon"/"consciousness.json",
        Path("configs")/ "persona/active.json",
        Path("data")/ "user_corpus",
    ]
    for s in sources:
        if s.exists():
            if s.is_dir(): shutil.copytree(s, dst/s.name, dirs_exist_ok=True)
            else: shutil.copy2(s, dst/s.name)
    (dst/"checksum.sha256").write_text(_checksum(dst), encoding="utf-8")

def backup_once()->str:
    ts=datetime.now().strftime("%Y%m%d_%H%M%S")
    dst=ROOT/f"checkpoint_{ts}"
    tmp=dst.with_suffix(".tmp")
    if tmp.exists(): shutil.rmtree(tmp)
    _snapshot(tmp)
    tmp.rename(dst)
    # mantém últimos 10
    xs=sorted(ROOT.glob("checkpoint_*"), reverse=True)
    for p in xs[10:]:
        shutil.rmtree(p, ignore_errors=True)
    return str(dst)

def _loop(interval_s:int):
    while RUN["on"]:
        time.sleep(interval_s)
        if RUN["on"]:
            try: backup_once()
            except: pass

def backup_auto_start(interval_min:int=5):
    RUN["on"]=True
    t=threading.Thread(target=_loop, args=(interval_min*60,), daemon=True)
    t.start()

def backup_auto_stop(): RUN["on"]=False