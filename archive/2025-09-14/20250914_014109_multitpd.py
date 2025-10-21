#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import json, tiktoken
from typing import List, Dict, Tuple
from .token_trie import TokenTrie

ENC = tiktoken.get_encoding("cl100k_base")

def load_layers(token_dict_path:str):
    p = Path(token_dict_path)
    data = json.loads(p.read_text(encoding="utf-8"))
    if "layers" in data:  # novo formato
        layers = data["layers"]
    else:
        # compat: single map vira camada única
        layers = [{"map": data.get("map", {})}]
    # prepara estruturas por camada
    tries, glyph_maps = [], []
    for L in layers:
        m = L.get("map", {})
        patterns = {tuple(v): k for k,v in m.items()}
        tries.append(TokenTrie(patterns))
        glyph_token_id = {ENC.encode(g)[0]: v for g,v in m.items()}
        glyph_maps.append(glyph_token_id)
    meta = data.get("meta", {})
    return tries, glyph_maps, meta

def save_layers(layers:List[Dict[str, List[int]]], out_path:str, meta:dict):
    payload = {"layers": [{"map": M} for M in layers], "meta": meta}
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")