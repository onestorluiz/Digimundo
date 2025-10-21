from __future__ import annotations
from typing import List, Dict, Callable, Any

_CAPS:List[dict]=[]

def register(cap_id:str, label:str, command:str, when:str="", prereq:str="", cost:str="low", tags:list[str]|None=None, desc:str=""):
    _CAPS.append({"id":cap_id,"label":label,"command":command,"when":when,"prereq":prereq,"cost":cost,"tags":tags or [],"desc":desc})

def list_caps()->List[dict]:
    return list(_CAPS)

def find_by_tag(tag:str)->List[dict]:
    return [c for c in _CAPS if tag in c.get("tags",[])]