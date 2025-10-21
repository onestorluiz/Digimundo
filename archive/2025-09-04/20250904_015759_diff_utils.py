from __future__ import annotations
import difflib
from typing import List, Tuple

def diff_text(a:str, b:str, n:int=2)->str:
    return "\n".join(difflib.unified_diff((a or "").splitlines(), (b or "").splitlines(), fromfile="prev", tofile="curr", n=n, lineterm=""))

def diff_sets(old:List[str], new:List[str])->Tuple[List[str], List[str]]:
    so=set(old or []); sn=set(new or [])
    return sorted(sn - so), sorted(so - sn)