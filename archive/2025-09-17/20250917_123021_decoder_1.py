import json
import re
import tiktoken
from pathlib import Path
from typing import Dict, List, Tuple
from .apps.scripturemon.digilang_advanced.vocab_schema import Vocab
from .ids import to_baseN

class DigiLangDecoder:

    def __init__(self, vocab_path: Path=None, use_tpd: bool=True, token_dict_path: str='data/tpd/default/token_dict.json'):
        if vocab_path is None:
            vocab_path = Path(__file__).parent / 'vocab.json'
        if not vocab_path.exists():
            from .build_vocab import build_vocab
            build_vocab('data/original', str(vocab_path))
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab_data = json.load(f)
            self.vocab = Vocab(**vocab_data)
        self.enc = tiktoken.get_encoding('cl100k_base')
        self.symbol_reverse = {v: k for k, v in self.vocab.symbols.items()}
        self.mwe_reverse = {v: k for k, v in self.vocab.mwe_map.items()}
        self.entity_reverse = {v: k for k, v in self.vocab.entity_prefix.items()}
        self.use_tpd = use_tpd
        self.glyph_to_ids = {}
        self.glyph_token_to_ids = {}
        self._glyph_layers = None
        if use_tpd and Path(token_dict_path).exists():
            try:
                from .multitpd import load_layers
                _, glyph_layers, _ = load_layers(token_dict_path)
                self._glyph_layers = glyph_layers
                if glyph_layers:
                    self.glyph_token_to_ids = glyph_layers[0]
            except Exception:
                with open(token_dict_path, 'r', encoding='utf-8') as f:
                    token_dict = json.load(f)
                self.glyph_to_ids = token_dict.get('map', {})
                for glyph, ids in self.glyph_to_ids.items():
                    glyph_token = self.enc.encode(glyph)
                    if len(glyph_token) == 1:
                        self.glyph_token_to_ids[glyph_token[0]] = ids

    def decode(self, text: str) -> str:
        """
        Decode DigiLang back to approximate natural language.
        Handles TPD glyphs, symbols, MWEs, and entities.
        """
        decoded = text
        token_ids = self.enc.encode(decoded)
        if hasattr(self, '_glyph_layers') and self._glyph_layers:
            for layer in reversed(self._glyph_layers):
                out = []
                for gid in token_ids:
                    if gid in layer:
                        out.extend(layer[gid])
                    else:
                        out.append(gid)
                token_ids = out
            decoded = self.enc.decode(token_ids)
        elif self.glyph_token_to_ids:
            out = []
            for gid in token_ids:
                out.extend(self.glyph_token_to_ids.get(gid, [gid]))
            token_ids = out
            decoded = self.enc.decode(token_ids)
        for prefix, entity_type in self.entity_reverse.items():
            pattern = re.escape(prefix) + '([' + ''.join((re.escape(c) for c in self.vocab.num_alphabet)) + ']+)'

            def decode_entity(match):
                id_chars = match.group(1)
                entity_id = 0
                base = len(self.vocab.num_alphabet)
                for char in id_chars:
                    if char in self.vocab.num_alphabet:
                        entity_id = entity_id * base + self.vocab.num_alphabet.index(char)
                return f'{entity_type} #{entity_id}'
            decoded = re.sub(pattern, decode_entity, decoded)
        for symbol, label in self.symbol_reverse.items():
            decoded = decoded.replace(symbol, label.replace('_', ' '))
        for symbol, phrase in self.mwe_reverse.items():
            decoded = decoded.replace(symbol, phrase)
        return decoded

    def decode_token_ids(self, token_ids: List[int]) -> str:
        """
        Decode a sequence of token IDs, expanding TPD glyphs.
        """
        if self.use_tpd and self.glyph_token_to_ids:
            expanded_ids = []
            for tid in token_ids:
                if tid in self.glyph_token_to_ids:
                    expanded_ids.extend(self.glyph_token_to_ids[tid])
                else:
                    expanded_ids.append(tid)
            return self.enc.decode(expanded_ids)
        else:
            return self.enc.decode(token_ids)