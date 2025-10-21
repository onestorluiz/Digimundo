from __future__ import annotations
import os, re, json
from pathlib import Path
from typing import List, Optional, Dict

RUNTIME = Path(os.environ.get("SCRIPTUREMON_HOME", Path(__file__).resolve().parents[2])) / "runtime"
RUNTIME.mkdir(parents=True, exist_ok=True)
INDEX = RUNTIME / "doc_index.json"

DEFAULT_DIRS = [
    Path.home() / "Digimundo",
    Path.home() / "Documents",
    Path.home() / "Documentos",
    Path(os.environ.get("SCRIPTUREMON_HOME",".")),
]

EXTS = {".pdf",".txt",".md",".fdx",".fountain"}

def _norm(s:str)->str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s]+"," ", s)
    s = re.sub(r"\s+"," ", s)
    return s

def build_index(extra_dirs:List[str]|None=None)->Dict:
    dirs = list(DEFAULT_DIRS)
    if extra_dirs:
        dirs += [Path(d) for d in extra_dirs if d]
    seen = {}
    for d in dirs:
        if not d or not d.exists(): continue
        for p in d.rglob("*"):
            if p.is_file() and p.suffix.lower() in EXTS and p.stat().st_size>0:
                key = _norm(p.stem)
                seen.setdefault(key, [])
                seen[key].append(str(p))
    INDEX.write_text(json.dumps(seen, ensure_ascii=False, indent=2), encoding="utf-8")
    return seen

def load_index()->Dict:
    if INDEX.exists():
        try:
            return json.loads(INDEX.read_text(encoding="utf-8"))
        except Exception:
            pass
    return build_index()

def find_by_name(name:str, extra_dirs:List[str]|None=None)->List[str]:
    idx = load_index() if extra_dirs is None else build_index(extra_dirs)
    q = _norm(name)
    # match estrito
    hits = idx.get(q, [])
    if hits: return hits
    # match parcial
    parts = q.split()
    cands = []
    for k, paths in idx.items():
        ok = all(part in k for part in parts)
        if ok: cands.extend(paths)
    return cands[:5]