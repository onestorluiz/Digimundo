# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path

CFG = Path("configs/ui.live")
ANCHOR = Path("configs/ui.anchor")

def set_live(value:str)->None:
    CFG.parent.mkdir(parents=True, exist_ok=True)
    CFG.write_text(str(value).strip(), encoding="utf-8")

def get_live()->str:
    if CFG.exists():
        try: return CFG.read_text(encoding="utf-8").strip()
        except: return "off"
    return "off"

# -- Âncora preferida do painel (e.g., "ultimate-performance")
def set_anchor(value:str)->None:
    ANCHOR.parent.mkdir(parents=True, exist_ok=True)
    ANCHOR.write_text(str(value).strip(), encoding="utf-8")

def get_anchor()->str:
    if ANCHOR.exists():
        try: return ANCHOR.read_text(encoding="utf-8").strip()
        except: return ""
    return ""