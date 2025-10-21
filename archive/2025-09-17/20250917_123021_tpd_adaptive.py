from __future__ import annotations
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Tuple
import json, time, math, hashlib, tiktoken
from .apps.scripturemon.digilang.tokenizer_utils import ENC_NAME, get_single_token_strings
Enc = tiktoken.get_encoding(ENC_NAME)

def tokenize(text: str) -> List[int]:
    return Enc.encode(text)

def detokenize(ids: List[int]) -> str:
    return Enc.decode(ids)

def mine_token_ngrams(ids: List[int], n_min=2, n_max=8) -> Counter:
    c = Counter()
    L = len(ids)
    for n in range(n_min, n_max + 1):
        for i in range(L - n + 1):
            c[tuple(ids[i:i + n])] += 1
    return c

def score_candidates(counter: Counter) -> List[Tuple[Tuple[int, ...], int, int]]:
    out = []
    for ngram, freq in counter.items():
        if freq < 3:
            continue
        gain = (len(ngram) - 1) * freq
        if gain <= 0:
            continue
        out.append((ngram, freq, gain))
    out.sort(key=lambda x: (-x[2], -len(x[0]), -x[1]))
    return out

def build_glyph_pool(K: int, reserved: set | None=None) -> List[str]:
    reserved = reserved or set()
    pool = []
    for s in get_single_token_strings(max_candidates=K * 5):
        if s not in reserved:
            pool.append(s)
        if len(pool) >= K:
            break
    return pool

def select_dictionary(cands, K: int, overlap_guard: float=0.6) -> Dict[Tuple[int, ...], str]:
    selected = {}
    occupied = defaultdict(int)

    def occ_ratio(ngram):
        h = (ngram[0], len(ngram))
        return occupied[h] / max(1, sum((1 for _ in [ngram])))
    for ngram, freq, gain in cands:
        h = (ngram[0], len(ngram))
        if occupied[h] / max(1, 1) > overlap_guard:
            continue
        selected[ngram] = None
        occupied[h] += 1
        if len(selected) >= K:
            break
    return selected

def build_tpd_for_corpus(corpus_dir: str, K: int=1200, n_min: int=2, n_max: int=8, freq_min: int=3, reserved_glyphs: set | None=None) -> Dict[str, List[int]]:
    texts = []
    for p in Path(corpus_dir).rglob('*.txt'):
        try:
            t = p.read_text(encoding='utf-8', errors='ignore')
            texts.append(t)
        except:
            pass
    full = '\n\n'.join(texts)
    ids = tokenize(full)
    counter = mine_token_ngrams(ids, n_min, n_max)
    counter = Counter({k: v for k, v in counter.items() if v >= freq_min})
    cands = score_candidates(counter)
    sel = select_dictionary(cands, K)
    pool = build_glyph_pool(K + 200, reserved_glyphs or set())
    mapping = {}
    i = 0
    for ngram in sel.keys():
        if i >= len(pool):
            break
        mapping[pool[i]] = list(ngram)
        i += 1
    return mapping

def save_token_dict(mapping: Dict[str, List[int]], out_path: str, meta: dict):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    payload = {'meta': meta, 'map': mapping}
    Path(out_path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')