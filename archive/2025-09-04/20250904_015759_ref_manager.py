from __future__ import annotations
from pathlib import Path
import json
def _path(session)->Path:
    home=Path(getattr(session,"home","."))
    d=home/"runtime"; d.mkdir(parents=True, exist_ok=True)
    return d/"ref.json"

def set_ref(session, path:str)->bool:
    p=_path(session)
    p.write_text(json.dumps({"ref":path},ensure_ascii=False,indent=2), encoding="utf-8")
    return True
def get_ref(session)->str|None:
    p=_path(session)
    if not p.exists(): return None
    try: return (json.loads(p.read_text(encoding="utf-8"))).get("ref")
    except Exception: return None
def clear_ref(session)->bool:
    p=_path(session)
    try:
        if p.exists(): p.unlink()
    except Exception: pass
    return True

# ADIÇÃO: pin on/off
def set_pin(session, on:bool)->bool:
    import json
    home=Path(getattr(session,"home","."))
    d=home/"runtime"; d.mkdir(parents=True, exist_ok=True)
    p=d/"ref.json"
    try:
        data=json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except Exception:
        data={}
    data["pin"]=bool(on)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2), encoding="utf-8")
    return True

def get_pin(session)->bool:
    import json
    home=Path(getattr(session,"home","."))
    p=home/"runtime"/"ref.json"
    if not p.exists(): return False
    try:
        data=json.loads(p.read_text(encoding="utf-8"))
        return bool(data.get("pin", False))
    except Exception:
        return False