# -*- coding: utf-8 -*-
from __future__ import annotations
import re, json
from pathlib import Path
from collections import Counter

# Tentativa de spaCy; fallback heurístico se indisponível
try:
    import spacy
    try:
        _NLP = spacy.load("en_core_web_sm")
    except Exception:
        _NLP = spacy.blank("en")
        _NLP.add_pipe("sentencizer")
except Exception:
    spacy = None
    _NLP = None

# Heurística de uppercase típica de roteiros (linhas de personagem)
UP = re.compile(r"^[A-Z][A-Z0-9 '\.-]{1,17}$")
PAREN_SUFFIX = re.compile(r"\s*\((CONT'D|V\.O\.|O\.S\.)\)\s*$", re.I)

def _clean_char_line(s:str)->str:
    s = s.strip().upper()
    return PAREN_SUFFIX.sub("", s)

def _heuristic_persons(text:str, k:int=12)->list[str]:
    names=[]
    for l in text.splitlines():
        u=_clean_char_line(l)
        if UP.match(u) and u not in {"INT.","EXT.","CUT TO:","FADE IN:","CUT TO","FADE IN"}:
            names.append(u)
    cnt = Counter(names)
    return [n for n,_ in cnt.most_common(k)]

def _spacy_persons(text:str, k:int=12)->list[str]:
    if _NLP is None or spacy is None:
        return []
    _NLP.max_length = max(_NLP.max_length, len(text) + 1000)
    doc = _NLP(text)
    c = Counter()
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # normaliza em UPPER para casar com linhas de personagem
            token = ent.text.upper().strip()
            token = PAREN_SUFFIX.sub("", token)
            if 2 <= len(token) <= 18:
                c[token] += 1
    # mescla com heurística de linhas UPPER (prioriza interseção)
    heur = set(_heuristic_persons(text, k=3*k))
    merged = Counter()
    for name, freq in c.items():
        if name in heur:
            merged[name] += freq * 2  # boost se aparece como CHAR line
        else:
            merged[name] += freq
    # fallback: se spaCy vazio, usa heurística pura
    if not merged:
        return _heuristic_persons(text, k=k)
    return [n for n,_ in merged.most_common(k)]

def person_candidates(text:str, k:int=12)->list[str]:
    # tenta spaCy, cai para heurística
    ppl = _spacy_persons(text, k=k)
    if ppl:
        return ppl[:k]
    return _heuristic_persons(text, k=k)