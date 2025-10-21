#!/usr/bin/env python3
"""
UI Preferences Module - Stub para Fase 1.C
Mantém interface complexa para preferências de UI
"""

# Estado global de preferências
_ui_state = {
    "live": False,
    "anchor": "top",
    "theme": "dark",
    "verbose": False
}

def set_live(value: bool) -> bool:
    """Define modo live"""
    _ui_state["live"] = value
    return True

def get_live() -> bool:
    """Retorna modo live"""
    return _ui_state["live"]

def set_anchor(value: str) -> bool:
    """Define âncora da UI"""
    if value in ["top", "bottom", "left", "right"]:
        _ui_state["anchor"] = value
        return True
    return False

def get_anchor() -> str:
    """Retorna âncora da UI"""
    return _ui_state["anchor"]

__all__ = ["set_live", "get_live", "set_anchor", "get_anchor"]