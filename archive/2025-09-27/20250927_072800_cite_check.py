
import json, re, math
from pathlib import Path
def _tokens(s: str):
    return [t for t in re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+", (s or "").lower()) if len(t) > 2]
def _keywords_from_outputs(outputs: dict) -> set[str]:
    keys=set()
    logline = (outputs.get("logline",{}) or {}).get("payload",{}) or {}
    theme = (outputs.get("theme",{}) or {}).get("payload",{}) or {}
    for s in [logline.get("logline",""), theme.get("primary_theme","")] + theme.get("motifs",[]):
        for t in _tokens(s): keys.add(t)
    stop = set(["um","uma","de","da","do","e","o","a","para","com","que","por","nos","nas","dos","das","em","no","na","the","and","for","with"])
    return set([k for k in keys if k not in stop and not k.isdigit()])
def spot_check_support(run_dir: Path, outputs: dict) -> dict:
    kw = _keywords_from_outputs(outputs)
    if not kw:
        return {"support_ratio": 0.0, "support_ratio_w": 0.0, "found": [], "keywords": []}
    found=set(); blocks=[]; vocab=set()
    for f in run_dir.glob("retrieval_*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        text = "\\n".join(d.get("rag_blocks", []))
        blocks.append(text)
        vocab |= set(_tokens(text))
    N = max(1, len(blocks))
    def df(term): return sum(1 for b in blocks if term in set(_tokens(b)))
    weights = {t: (math.log((N + 1)/(df(t)+1)) + 1.0) for t in kw}
    for b in blocks:
        toks = set(_tokens(b))
        for t in kw:
            if t in toks: found.add(t)
    num = sum(weights[t] for t in found) if found else 0.0
    den = sum(weights.values()) if weights else 1.0
    ratio = len(found)/max(1,len(kw))
    wratio = num/max(1e-9, den)
    return {"support_ratio": round(ratio,3), "support_ratio_w": round(wratio,3), "found": sorted(found), "keywords": sorted(list(kw))}
