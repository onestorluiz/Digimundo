from pathlib import Path
import json, tiktoken
from src.digilang.encoder import DigiLangEncoder

def test_encoder_loads_per_work_when_available(tmp_path):
    # cria per_work para slug "toy"
    pdir = Path("data/tpd/per_work/toy")
    pdir.mkdir(parents=True, exist_ok=True)
    enc = tiktoken.get_encoding("cl100k_base")
    # mapping fake: glyph "§" -> ids [101,102]
    mapping = {"§":[101,102]}
    (pdir/"token_dict.json").write_text(json.dumps({"map":mapping}), encoding="utf-8")
    e = DigiLangEncoder(use_tpd=True, tpd_policy="per_work")
    # encode com doc_key="toy" deve ativar esse dict (não testamos compressão real aqui)
    out, ratio = e.encode("dummy", doc_key="toy")
    assert e.trie is not None