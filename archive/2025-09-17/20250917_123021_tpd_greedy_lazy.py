from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter, defaultdict
import heapq, time, json, tiktoken
from .apps.scripturemon.digilang.tokenizer_utils import ENC_NAME, get_single_token_strings
Enc = tiktoken.get_encoding(ENC_NAME)

def tokenize(text: str) -> List[int]:
    return Enc.encode(text)

def detokenize(ids: List[int]) -> str:
    return Enc.decode(ids)

def mine_token_ngrams(ids: List[int], n_min: int=2, n_max: int=8, freq_min: int=3) -> Counter:
    c = Counter()
    L = len(ids)
    for n in range(n_min, n_max + 1):
        for i in range(L - n + 1):
            c[tuple(ids[i:i + n])] += 1
    return Counter({k: v for k, v in c.items() if v >= freq_min})

def head_index(ids: List[int]) -> Dict[int, List[int]]:
    idx = defaultdict(list)
    for i, tid in enumerate(ids):
        idx[tid].append(i)
    return idx

def find_positions(ids: List[int], ngram: Tuple[int, ...], idx_head: Dict[int, List[int]]) -> List[int]:
    head = ngram[0]
    cand = idx_head.get(head, [])
    L = len(ids)
    N = len(ngram)
    out = []
    for i in cand:
        if i + N <= L and tuple(ids[i:i + N]) == ngram:
            out.append(i)
    return out

def initial_candidates(counter: Counter) -> List[Tuple[int, Tuple[int, ...], int]]:
    heap = []
    for ngram, freq in counter.items():
        ub = (len(ngram) - 1) * freq
        if ub > 0:
            heapq.heappush(heap, (-ub, ngram, freq))
    return heap

def build_glyph_pool(K: int, reserved: set | None=None) -> List[str]:
    reserved = reserved or set()
    pool = []
    for s in get_single_token_strings(max_candidates=K * 6):
        if s not in reserved:
            pool.append(s)
        if len(pool) >= K:
            break
    return pool

def greedy_lazy(ids: List[int], counter: Counter, K: int=1500, n_min: int=2, n_max: int=8, freq_min: int=3, time_budget_s: float=30.0) -> Dict[Tuple[int, ...], str]:
    """
    Lazy-greedy: usa upper bounds no heap; quando um candidato vira top,
    recalcula ganho marginal exato (ignorando posições cobertas). Se ainda
    for top, seleciona; senão, volta ao heap com novo upper bound.
    """
    L = len(ids)
    covered = [False] * L
    idx_head = head_index(ids)
    heap = initial_candidates(counter)
    selected = {}
    t0 = time.time()
    while heap and len(selected) < K and (time.time() - t0 < time_budget_s):
        neg_ub, ngram, freq = heapq.heappop(heap)
        starts = find_positions(ids, ngram, idx_head)
        if not starts:
            continue
        N = len(ngram)
        gain_marg = 0
        usable = []
        for s in starts:
            if any(covered[s:s + N]):
                continue
            gain_marg += N - 1
            usable.append(s)
            if gain_marg > -neg_ub:
                break
        if gain_marg >= -neg_ub - 1:
            for s in usable:
                for j in range(s, s + N):
                    covered[j] = True
            selected[ngram] = ''
        elif gain_marg > 0:
            heapq.heappush(heap, (-gain_marg, ngram, freq))
    return selected

def build_tpd_greedy_lazy_for_corpus(corpus_dir: str, K: int=1500, n_min: int=2, n_max: int=8, freq_min: int=3, time_budget_s: float=30.0) -> Dict[str, List[int]]:
    texts = []
    for p in Path(corpus_dir).rglob('*.txt'):
        try:
            t = p.read_text(encoding='utf-8', errors='ignore')
            if t:
                texts.append(t)
        except:
            pass
    full = '\n\n'.join(texts)
    ids = tokenize(full)
    counter = mine_token_ngrams(ids, n_min, n_max, freq_min=freq_min)
    sel = greedy_lazy(ids, counter, K=K, n_min=n_min, n_max=n_max, freq_min=freq_min, time_budget_s=time_budget_s)
    pool = build_glyph_pool(len(sel) + 200)
    mapping = {}
    i = 0
    for ngram in sel.keys():
        glyph = pool[i]
        i += 1
        mapping[glyph] = list(ngram)
    return mapping

def save_token_dict(mapping: Dict[str, List[int]], out_path: str, meta: dict):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    payload = {'meta': meta, 'map': mapping}
    Path(out_path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')