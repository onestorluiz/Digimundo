
import re, difflib
from collections import Counter

def _tokens(s: str):
    return [t for t in re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+", s.lower()) if len(t) > 2]

def make_queries(excerpt: str, max_terms: int = 12) -> list[str]:
    toks = _tokens(excerpt)
    freqs = Counter(toks)
    top = [t for t,_ in freqs.most_common(max_terms)]
    q1 = " ".join(top)
    bigs = Counter([" ".join(pair) for pair in zip(toks, toks[1:])])
    q2 = " ".join(w for w,_ in bigs.most_common(max(4, max_terms//2)))
    q3 = excerpt[:64]
    uniq = [q for q in [q1, q2, q3] if q and q.strip()]
    seen=set(); out=[]
    for q in uniq:
        if q not in seen:
            out.append(q); seen.add(q)
    return out

def _windows(text: str, win_chars: int = 420, step: int = 140):
    n = len(text)
    if n <= win_chars:
        yield 0, n, text; return
    for i in range(0, n, step):
        j = min(n, i + win_chars); yield i, j, text[i:j]

def _score(seg: str, query: str) -> float:
    q = query.strip().lower()
    ratio = difflib.SequenceMatcher(a=q, b=seg.lower()).ratio() if q else 0.0
    qs = set(_tokens(query)); ss = set(_tokens(seg))
    ov = len(qs & ss) / max(1, len(qs or {''}))
    return 0.65*ratio + 0.35*ov

def _sentences(text: str):
    for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text):
        s = s.strip()
        if s: yield s

def _compress_to_sentences(text: str, query: str, max_chars: int = 420) -> str:
    toks_q = set(_tokens(query))
    parts = list(_sentences(text))
    if not parts: return text[:max_chars]
    scored = []
    for s in parts:
        ts = set(_tokens(s))
        ov = len(ts & toks_q) / max(1, len(toks_q or {''}))
        scored.append((ov, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    out = []; budget = max_chars
    for _, s in scored:
        add = len(s) + (1 if out else 0)
        if add <= budget:
            out.append(s); budget -= add
        if budget <= 0: break
    return (" ".join(out) if out else text[:max_chars])[:max_chars]

def best_snippet_by_query(text: str, query: str, win_chars: int = 420, step: int = 140) -> str:
    best = (0.0, text[:win_chars])
    for _, _, seg in _windows(text, win_chars, step):
        s = _score(seg, query)
        if s > best[0]: best = (s, seg)
    return _compress_to_sentences(best[1], query, max_chars=win_chars)

def compress_extractive_tfidf(text: str, query: str, max_chars: int = 420, redundancy: float = 0.6) -> str:
    S = list(_sentences(text))
    if not S: return text[:max_chars]
    # TF-IDF leve
    import math
    toks = [ _tokens(s) for s in S ]
    from collections import Counter
    df = Counter()
    for ts in toks:
        for t in set(ts): df[t] += 1
    vecs = []
    for ts in toks:
        tf = Counter(ts)
        v = {}
        for t, c in tf.items():
            idf = math.log((len(S) + 1) / (df[t] + 1)) + 1.0
            v[t] = (c / max(1,len(ts))) * idf
        vecs.append(v)
    q_tokens = set(_tokens(query))
    chosen = []; chosen_tokens = set()
    budget = max_chars; used = set()
    def score_sentence(v, q_tokens): return sum(vv for tt, vv in v.items() if tt in q_tokens)
    while len(chosen) < len(S):
        best_i, best_score = -1, -1e9
        for i, (s, v) in enumerate(zip(S, vecs)):
            if i in used: continue
            base = score_sentence(v, q_tokens) + 0.2 * sum(v.values())
            tok = set(_tokens(s))
            overlap = len(tok & chosen_tokens) / max(1, len(tok))
            score = base - redundancy * overlap
            if len(s) <= budget and score > best_score:
                best_i, best_score = i, score
        if best_i < 0: break
        chosen.append(S[best_i])
        chosen_tokens |= set(_tokens(S[best_i]))
        used.add(best_i)
        budget -= len(S[best_i]) + 1
        if budget <= 0: break
    if not chosen: return text[:max_chars]
    result = " ".join(chosen)
    return result[:max_chars]
