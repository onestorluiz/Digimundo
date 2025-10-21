
import re
from collections import Counter
TOKEN = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9']+")
def _tokens(s: str): return [t for t in TOKEN.findall(s) if len(t) > 2]
def detect_entities_topics(text: str) -> dict:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    char_lines = [l for l in lines if re.match(r"^[A-Z .'-]{2,}$", l)]
    chars = Counter([re.sub(r"[^A-Z .'-]", "", l).strip() for l in char_lines]).most_common(10)
    proper = re.findall(r"(?:[A-ZÁ-Ú][a-zá-ú]+(?:\s+[A-ZÁ-Ú][a-zá-ú]+){0,2})", text)
    prop_norm = [p.strip() for p in proper if len(p.split())<=3]
    props = Counter(prop_norm).most_common(20)
    toks = [t.lower() for t in _tokens(text)]
    stop = set(["uma","para","com","que","por","dos","das","nos","nas","ele","ela","eles","elas","você","voces","de","do","da","em","no","na","se","ao","aos","as","os","um","uma","e","o","a"])
    toks = [t for t in toks if t not in stop and not t.isdigit()]
    top_topics = [w for w,_ in Counter(toks).most_common(20)]
    return {"characters": [c for c,_ in chars], "proper": [p for p,_ in props], "topics": top_topics}
def queries_for_entities(entities: dict, max_q: int = 6) -> list[str]:
    qs = []
    for c in entities.get("characters", [])[:3]:
        if len(c) > 2: qs.append(c.title())
    for p in entities.get("proper", [])[:2]:
        qs.append(p)
    topics = entities.get("topics", [])[:6]
    for i in range(0, len(topics), 2):
        pair = topics[i:i+2]
        if pair: qs.append(" ".join(pair))
    seen=set(); out=[]
    for q in qs:
        if q not in seen: out.append(q); seen.add(q)
    return out[:max_q]
