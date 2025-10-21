from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Dict, List
from datetime import datetime

class VocabMeta(BaseModel):
    tokenizer: str = "cl100k_base"
    version: str = "v1-tokenaware"
    built_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    seed: int = 42
    budgets: Dict[str, int]
    notes: str = ""

class Vocab(BaseModel):
    meta: VocabMeta
    # Símbolos fixos por função narrativa/cinematográfica
    symbols: Dict[str, str]   # ex: {"ACT_1":"◜", "BEAT_CLIMAX":"◈", "INT":"▣", ...}
    # Padrões para prefixos de entidade (cada um 1 token)
    entity_prefix: Dict[str, str]  # ex: {"PERSONA":"⒫","LOCAL":"⒧","OBJ":"⒪","MOTIF":"⒨","EVENT":"⒠"}
    # Alfabeto numérico compacto (cada char 1 token) p/ IDs base-N
    num_alphabet: List[str]
    # Mapeamento de MWEs -> símbolo 1-token
    mwe_map: Dict[str, str]