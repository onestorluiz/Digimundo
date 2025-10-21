# -*- coding: utf-8 -*-
from __future__ import annotations
import re, json, math
from collections import Counter

HEADER_PAT = re.compile(r"^(INT\.|EXT\.)\s+[A-Z0-9 _'\.&/()-]+?\s*[—–-]\s*(DAY|NIGHT|DAWN|DUSK|EVENING|MORNING|AFTERNOON|NOON|LATER|CONTINUOUS|SAME)\s*$")

def extract_headers(text:str):
    lines = text.upper().splitlines()
    return [l.strip() for l in lines if HEADER_PAT.search(l.strip())]

def extract_char_names(text:str, k:int=12):
    names=[]
    for l in text.upper().splitlines():
        s=l.strip()
        if 2<=len(s)<=18 and s.isupper() and s not in {"INT.","EXT.","CUT TO:","FADE IN:","CUT TO","FADE IN"}:
            s = re.sub(r"\s*\((CONT'D|V\.O\.|O\.S\.)\)\s*$","",s)
            if s: names.append(s)
    cnt=Counter(names)
    return [n for n,_ in cnt.most_common(k)]

def estimate_pages(text:str, chars_per_page:int=900):
    return max(1, int(math.ceil(len(text)/float(chars_per_page))))

def estimate_beats(n_pages:int, kb:dict):
    beats=[]
    for b in kb.get("beats",[]):
        page=max(1, int(round(b.get("fraction",0.0)*n_pages)))
        beats.append({"name":b["name"],"page":page,"desc":b["desc"]})
    return beats

def features(text:str, kb:dict):
    hdrs=extract_headers(text)
    chars=extract_char_names(text)
    pages=estimate_pages(text)
    beats=estimate_beats(pages, kb)
    diag=dict(
        num_headers=len(hdrs),
        top_headers=hdrs[:12],
        top_characters=chars,
        est_pages=pages,
        est_beats=beats
    )
    return diag