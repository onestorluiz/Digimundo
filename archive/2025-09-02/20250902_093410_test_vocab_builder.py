import json, tiktoken, os
from pathlib import Path

def test_vocab_single_token_values():
    enc = tiktoken.get_encoding("cl100k_base")
    vocab = json.loads(Path("src/digilang/vocab.json").read_text(encoding="utf-8"))
    for k,v in vocab["symbols"].items():
        assert len(enc.encode(v)) == 1, f"symbol {k} not 1-token"
    for k,v in vocab["entity_prefix"].items():
        assert len(enc.encode(v)) == 1, f"entity_prefix {k} not 1-token"
    for phrase,sym in vocab["mwe_map"].items():
        assert len(enc.encode(sym)) == 1, f"MWE symbol for '{phrase}' not 1-token"
    for ch in vocab["num_alphabet"]:
        assert len(enc.encode(ch)) == 1, "num_alphabet item not 1-token"