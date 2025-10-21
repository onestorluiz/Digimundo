#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gera samples de round-trip (encode->decode) e métricas proxy de integridade semântica (C7):
- entity_retain: retenção de entidades (screenplay: PERSONAGENS; geral: nomes próprios)
- header_retain: retenção de headers e marcadores (INT./EXT./CUT TO:/FADE IN:)
- content_overlap: Jaccard de content-words (stopwords removidas)
- integrity_score = 0.5*entity + 0.2*header + 0.3*content
Saída: results/compression/roundtrip_samples.csv
"""

from __future__ import annotations
from pathlib import Path
import re, json, random, argparse
import tiktoken
from collections import Counter

# Imports do DigiLang
from src.digilang.encoder import DigiLangEncoder
from src.digilang.decoder import DigiLangDecoder

ENC = tiktoken.get_encoding("cl100k_base")
toklen = lambda s: len(ENC.encode(s))

STOPWORDS = {
  "the","and","a","an","to","of","in","on","for","at","by","with","as","from","that","this","it","is","are","was","were",
  "be","been","being","or","but","if","then","so","than","not","no","yes","you","your","i","we","they","he","she","his","her",
  "act","scene","page","into","out","up","down","over","under","again","there","here","about","after","before","between"
}

HEADER_PAT = re.compile(r"^(INT\.|EXT\.)\s+[A-Z0-9 _'\.&/()-]+?\s*[—–-]\s*(DAY|NIGHT|DAWN|DUSK|EVENING|MORNING|AFTERNOON|NOON|LATER|CONTINUOUS|SAME)\s*$")
CUT_PAT = re.compile(r"\bCUT TO:?\b")
FADE_PAT = re.compile(r"\bFADE IN:?\b")

def is_screenplay(text: str) -> bool:
    t = text.upper()
    if "INT." in t or "EXT." in t or "CUT TO:" in t or "FADE IN:" in t:
        return True
    return False

def extract_headers(text: str):
    lines = text.upper().splitlines()
    hdr = sum(1 for l in lines if HEADER_PAT.search(l.strip()))
    cut = len(CUT_PAT.findall(text))
    fade = len(FADE_PAT.findall(text))
    return {"header_lines": hdr, "cut_to": cut, "fade_in": fade, "total": hdr + cut + fade}

def extract_entities_screenplay(text: str, k: int = 32):
    # Linhas totalmente maiúsculas curtas (prováveis nomes de personagem)
    names = []
    for l in text.upper().splitlines():
        s = l.strip()
        if 2 <= len(s) <= 18 and s.isupper():
            if s in {"INT.","EXT.","CUT TO:","FADE IN:"}:
                continue
            # remove sufixos comuns (CONT'D), (V.O.), (O.S.)
            s = re.sub(r"\s*\((CONT'D|V\.O\.|O\.S\.)\)\s*$", "", s)
            if s: names.append(s)
    cnt = Counter(names)
    return set(n for n,_ in cnt.most_common(k))

def extract_entities_general(text: str, k: int = 32):
    # Sequências de palavras Capitalizadas (John, John Doe, New York)
    cands = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b", text)
    # Filtra termos triviais
    cands = [c for c in cands if c.lower() not in STOPWORDS and len(c) >= 3]
    cnt = Counter(cands)
    return set(n for n,_ in cnt.most_common(k))

def content_keywords(text: str, top_k: int = 200):
    toks = re.findall(r"[A-Za-z]{3,}", text.lower())
    toks = [t for t in toks if t not in STOPWORDS]
    cnt = Counter(toks)
    return set(w for w,_ in cnt.most_common(top_k))

def jaccard(a: set, b: set) -> float:
    if not a: return 0.0
    inter = len(a & b)
    uni = len(a | b)
    return inter/uni if uni>0 else 0.0

def retention_ratio(orig_count: int, dec_count: int) -> float:
    if orig_count <= 0: return 1.0
    return min(1.0, dec_count / orig_count)

def build_row(p: Path, encoder: DigiLangEncoder, decoder: DigiLangDecoder, preserve_headers: bool = True):
    raw = p.read_text(encoding="utf-8", errors="ignore")
    ds = "screenplay" if is_screenplay(raw) else "original"

    # Round-trip
    comp, _ = encoder.encode(raw, preserve_headers=preserve_headers, doc_key=p.stem if encoder.tpd_policy=="per_work" else None)
    try:
        dec = decoder.decode(comp, doc_key=p.stem if hasattr(decoder, "tpd_policy") and decoder.tpd_policy=="per_work" else None)
    except Exception:
        dec = comp  # fallback conservador

    # Métricas
    tb, ta = toklen(raw), toklen(comp)
    reduction = 1.0 - (ta/tb if tb>0 else 1.0)

    # Headers (case-insensitive)
    h0 = extract_headers(raw)
    h1 = extract_headers(dec)
    header_retain = retention_ratio(h0["total"], h1["total"])

    # Entidades (case-insensitive / normalizadas)
    if ds == "screenplay":
        e0 = extract_entities_screenplay(raw)
        e1 = extract_entities_screenplay(dec)
    else:
        e0 = extract_entities_general(raw)
        e1 = extract_entities_general(dec)
    entity_retain = jaccard(e0, e1)

    # Content overlap
    k0 = content_keywords(raw)
    k1 = content_keywords(dec)
    content_overlap = jaccard(k0, k1)

    # Score agregado
    integrity_score = 0.5*entity_retain + 0.2*header_retain + 0.3*content_overlap

    return {
        "file": str(p),
        "dataset": ds,
        "tokens_before": tb,
        "tokens_after": ta,
        "reduction": reduction,
        "entities_orig": len(e0),
        "entities_dec": len(e1),
        "entity_retain": entity_retain,
        "headers_orig": h0["total"],
        "headers_dec": h1["total"],
        "header_retain": header_retain,
        "content_overlap": content_overlap,
        "integrity_score": integrity_score
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", default="data/screenplay_synth")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="results/compression/roundtrip_samples.csv")
    ap.add_argument("--tpd_path", default="data/tpd/default/token_dict.json")
    ap.add_argument("--preserve_headers", type=lambda s: s.lower() in {"1","true","yes"}, default=True)
    ap.add_argument("--tpd_policy", default="per_work", choices=["default","per_work"])
    args = ap.parse_args()

    random.seed(args.seed)
    DATA = Path(args.data_dir)
    files = [p for p in DATA.rglob("*.txt")]
    if not files:
        print("[WARN] no .txt files in", DATA)
        return

    # Amostragem
    random.shuffle(files)
    files = files[:args.n]

    # Encoder/Decoder
    enc = DigiLangEncoder(use_tpd=True, token_dict_path=args.tpd_path, tpd_policy=args.tpd_policy)
    try:
        dec = DigiLangDecoder(use_tpd=True, token_dict_path=args.tpd_path, tpd_policy=args.tpd_policy)
    except TypeError:
        # compat: versões antigas sem tpd_policy
        dec = DigiLangDecoder(use_tpd=True, token_dict_path=args.tpd_path)

    # Gera linhas
    rows = []
    for p in files:
        try:
            rows.append(build_row(p, enc, dec, args.preserve_headers))
        except Exception as e:
            # continua robusto
            rows.append({"file": str(p), "error": str(e)})

    # Salva CSV
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    import csv
    keys = sorted({k for r in rows for k in r.keys()})
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader(); w.writerows(rows)
    print(f"[OK] roundtrip samples -> {out} ({len(rows)} rows)")

if __name__ == "__main__":
    main()