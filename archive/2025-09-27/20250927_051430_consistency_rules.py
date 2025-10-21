
import json, re
from pathlib import Path

def _get_path(obj, path: str):
    cur = obj
    for part in path.split('.'):
        if part.endswith(']'): part = part.split('[')[0]
        if isinstance(cur, dict): cur = cur.get(part, None)
        else: return None
    return cur

def _contains_any(val, needles):
    if val is None: return False
    if isinstance(val, list): s = " ".join(str(x).lower() for x in val)
    else: s = str(val).lower()
    return any(n in s for n in needles)

def _regex(val, pattern: str):
    s = " ".join(val) if isinstance(val, list) else str(val)
    try: return re.search(pattern, s) is not None
    except Exception: return False

def eval_rules(outputs: dict, rules_file: str) -> list[dict]:
    data = json.loads(Path(rules_file).read_text(encoding='utf-8'))
    issues = []
    for r in data.get("rules", []):
        ok = True
        for cond in r.get("when_all", []):
            path = cond.get("path"); 
            if "contains_any" in cond:
                if not _contains_any(_get_path(outputs, path), [x.lower() for x in cond["contains_any"]]):
                    ok = False; break
            if "regex" in cond:
                if not _regex(_get_path(outputs, path), cond["regex"]):
                    ok = False; break
        if ok:
            issues.append({"id": r.get("id"), "severity": r.get("severity","low"),
                           "autofix_reflect": bool(r.get("autofix_reflect", False)),
                           "guidance": r.get("guidance","")})
    return issues
