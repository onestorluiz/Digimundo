
from dataclasses import dataclass
from typing import Dict
import re
from .script_indexer import format_offset
@dataclass
class TurningPoint:
    name: str; line: int; offset: str
def compute_structure(script_text: str, page_lines: int = 55) -> Dict:
    lines = script_text.splitlines(); n=len(lines)
    if n == 0: return {"turning_points": []}
    a = max(1, int(n*0.25)); b = max(1, int(n*0.50)); c = max(1, int(n*0.75))
    tp = [
        TurningPoint("Act I — Break into Act II", a, format_offset(a, a, page_lines)),
        TurningPoint("Midpoint", b, format_offset(b, b, page_lines)),
        TurningPoint("Act II — Break into Act III", c, format_offset(c, c, page_lines)),
    ]
    def is_header(l): return bool(re.match(r"^(INT\\.|EXT\\.)", l.strip()))
    def is_char(l): return bool(re.match(r"^[A-Z .'-]{2,}$", l.strip()))
    def action_density(start,end):
        seg = [x for x in lines[start-1:end] if x.strip()]
        act = [x for x in seg if not is_header(x) and not is_char(x)]
        return len(act)/max(1,len(seg))
    metrics = {"action_density":{"act1":action_density(1,a),"act2":action_density(a+1,c),"act3":action_density(c+1,n)}}
    return {"turning_points": [t.__dict__ for t in tp], "metrics": metrics, "lines": n}
