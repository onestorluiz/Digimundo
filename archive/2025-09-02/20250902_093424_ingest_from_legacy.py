#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import argparse, json, shutil, hashlib

def sha(p:Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(131072), b""): h.update(b)
    return h.hexdigest()

def copy_unique(src:Path, dst:Path, kind:str, limit:int=0)->list[dict]:
    dst.mkdir(parents=True, exist_ok=True)
    items=[]
    seen=set()
    files=[*src.rglob("*.txt")]
    if limit: files=files[:limit]
    for p in files:
        try:
            dig=sha(p)
            if dig in seen: continue
            seen.add(dig)
            out = dst/p.name
            if not out.exists(): shutil.copy2(p, out)
            items.append({"kind":kind,"src":str(p),"dst":str(out),"sha":dig})
        except: pass
    return items

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--legacy_root", default="")
    ap.add_argument("--limit", type=int, default=0)
    args=ap.parse_args()

    # Descoberta heurística
    root = Path(args.legacy_root) if args.legacy_root else None
    if not root or not root.exists():
        cands = [Path.home()/"Computadores"/"Digimundo"/"digimons"/"scripturemon",
                 Path.home()/"Digimundo"/"digimons"/"scripturemon"]
        root = next((c for c in cands if c.exists()), None)

    if not root:
        print("[WARN] legacy root não encontrado"); return

    cinema = root/"CINEMA_KNOWLEDGE"
    translations = cinema/"02_TRADUCOES_DIGILANG"
    books_dir = root/"books"
    scripts_dir= root/"scripts"

    DEST = Path("data/user_corpus")
    out_books   = copy_unique(translations if translations.exists() else books_dir, DEST/"books", "book", args.limit)
    out_scripts = copy_unique(scripts_dir if scripts_dir.exists() else translations, DEST/"scripts", "script", args.limit)

    manifest = {"root": str(root), "books": out_books, "scripts": out_scripts}
    (DEST/"manifest_legacy.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[OK] ingest legacy -> {DEST} | books={len(out_books)} scripts={len(out_scripts)}")

if __name__=="__main__": main()