import json
import re
import tiktoken
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from .slug import slugify
from .apps.scripturemon.digilang_advanced.vocab_schema import Vocab
from .ids import to_baseN
from .token_trie import TokenTrie, FastTokenTrie
from .token_trie_simple import TokenTrie as SimpleTokenTrie

def canonicalize(text: str, domain: str='auto') -> str:
    """
    Canonicalize text for better token matching.
    Normalizes quotes, dashes, and domain-specific patterns.
    """
    t = text
    t = t.replace('–', '-').replace('—', '-')
    t = t.replace(', \'"\').replace(', '"')
    t = t.replace("'", "'").replace("'", "'")
    t = t.replace('‘', "'").replace('’', "'")
    t = t.replace('“', '"').replace('”', '"')
    t = t.replace('…', '...')
    if domain == 'auto':
        if 'INT.' in t.upper() or 'EXT.' in t.upper() or 'CUT TO:' in t.upper():
            domain = 'screenplay'
        elif any((word in t.lower() for word in ['thou', 'thee', 'thy', 'hath', 'doth'])):
            domain = 'shakespeare'
    if domain == 'screenplay':
        t = re.sub('\\bInt\\.', 'INT.', t)
        t = re.sub('\\bExt\\.', 'EXT.', t)
        t = re.sub('\\bint\\.', 'INT.', t, flags=re.IGNORECASE)
        t = re.sub('\\bext\\.', 'EXT.', t, flags=re.IGNORECASE)
        for pattern, replacement in [('Cut to:', 'CUT TO:'), ('Fade in:', 'FADE IN:'), ('Fade out:', 'FADE OUT:'), ('Dissolve to:', 'DISSOLVE TO:'), ('Smash cut:', 'SMASH CUT:')]:
            t = re.sub(pattern, replacement, t, flags=re.IGNORECASE)
    elif domain == 'shakespeare':
        replacements = [("'tis", 'tis'), ("'twas", 'twas'), ("'twere", 'twere'), ("'twixt", 'twixt'), ("o'er", 'oer'), ("e'er", 'eer'), ("ne'er", 'neer'), ("'gainst", 'gainst'), ("i'", 'i'), ("th'", 'the'), ("t'", 'to'), ("'fore", 'fore'), ("'neath", 'neath'), ("'midst", 'midst'), ("'mongst", 'mongst'), ("'round", 'round')]
        for old, new in replacements:
            t = re.sub('\\b' + re.escape(old) + '\\b', new, t, flags=re.IGNORECASE)
        t = re.sub('\\bshalt\\b', 'shall', t, flags=re.IGNORECASE)
        t = re.sub('\\bwilt\\b', 'will', t, flags=re.IGNORECASE)
        t = re.sub('\\bhath\\b', 'has', t, flags=re.IGNORECASE)
        t = re.sub('\\bdoth\\b', 'does', t, flags=re.IGNORECASE)
        t = re.sub('\\bcanst\\b', 'can', t, flags=re.IGNORECASE)
    return t

class DigiLangEncoder:

    def __init__(self, vocab_path: Path=None, use_tpd: bool=True, token_dict_path: str='data/tpd/default/token_dict.json', **kwargs):
        if vocab_path is None:
            vocab_path = Path(__file__).parent / 'vocab.json'
        if not vocab_path.exists():
            from .build_vocab import build_vocab
            build_vocab('data/original', str(vocab_path))
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab_data = json.load(f)
            self.vocab = Vocab(**vocab_data)
        self.enc = tiktoken.get_encoding('cl100k_base')
        self.use_tpd = use_tpd
        self.token_dict_path = token_dict_path
        self.tpd_policy = kwargs.get('tpd_policy', 'default')
        self.trie = None
        self.glyph_token_id = {}
        self._perwork_cache = {}
        self._load_tpd()
        self._tries = None
        self._glyph_layers = None

    def _load_vocab(self):
        pass

    def _load_tpd(self):
        p = Path(self.token_dict_path)
        self.trie = None
        self.glyph_token_id = {}
        self._tries = None
        self._glyph_layers = None
        if p.exists():
            try:
                from .multitpd import load_layers
                tries, glyph_layers, meta = load_layers(str(p))
                self._tries = tries
                self._glyph_layers = glyph_layers
                if tries:
                    self.trie = tries[0]
                if glyph_layers:
                    self.glyph_token_id = glyph_layers[0]
            except Exception:
                from .token_trie import TokenTrie
                data = json.loads(p.read_text(encoding='utf-8'))
                m = data.get('map', {})
                patterns = {tuple(v): k for k, v in m.items()}
                self.trie = TokenTrie(patterns)
                for glyph, ids in m.items():
                    gid = self.enc.encode(glyph)[0]
                    self.glyph_token_id[gid] = ids

    def _ensure_perwork(self, doc_key: str):
        """Carrega (e cacheia) trie + mapa para um slug específico, se existir."""
        slug = slugify(doc_key)
        if slug in self._perwork_cache:
            self.trie = self._perwork_cache[slug]['trie']
            self.glyph_token_id = self._perwork_cache[slug]['glyph_token_id']
            return True
        p = Path(f'data/tpd/per_work/{slug}/token_dict.json')
        if not p.exists():
            return False
        from .token_trie_simple import TokenTrie as SimpleTokenTrie
        data = json.loads(p.read_text(encoding='utf-8'))
        m = data.get('map', {})
        patterns = {tuple(v): k for k, v in m.items()}
        trie = SimpleTokenTrie(patterns)
        glyph_token_id = {}
        for glyph, ids in m.items():
            gid = self.enc.encode(glyph)[0]
            glyph_token_id[gid] = ids
        self._perwork_cache[slug] = {'trie': trie, 'glyph_token_id': glyph_token_id}
        self.trie = trie
        self.glyph_token_id = glyph_token_id
        return True

    def encode(self, text: str, preserve_headers: bool=True, canonicalize_text: bool=True, **kwargs) -> Tuple[str, float]:
        """
        Encode text to DigiLang using TPD and symbol replacement.
        Now works at token level for maximum efficiency.
        """
        doc_key = kwargs.get('doc_key')
        if self.use_tpd and self.tpd_policy == 'per_work' and doc_key:
            ok = self._ensure_perwork(doc_key)
            if not ok:
                pass
        original_tokens = len(self.enc.encode(text))
        if canonicalize_text:
            text = canonicalize(text, domain='auto')

        def compress_ids(ids):
            if self.use_tpd and self._tries:
                for trie in self._tries:
                    out_ids = []
                    i = 0
                    L = len(ids)
                    while i < L:
                        m = trie.longest_match(ids, i)
                        if m:
                            ln, glyph = m
                            gid = self.enc.encode(glyph)[0]
                            out_ids.append(gid)
                            i += ln
                        else:
                            out_ids.append(ids[i])
                            i += 1
                    ids = out_ids
            elif self.use_tpd and self.trie:
                out_ids = []
                i = 0
                while i < len(ids):
                    m = self.trie.longest_match(ids, i)
                    if m:
                        L, glyph = m
                        gid = self.enc.encode(glyph)[0]
                        out_ids.append(gid)
                        i += L
                    else:
                        out_ids.append(ids[i])
                        i += 1
                ids = out_ids
            return ids
        if preserve_headers:
            HEADER_PAT = re.compile('^(INT\\.|EXT\\.)\\s+[A-Z0-9 _\\-]+?\\s*-\\s*(DAY|NIGHT|DAWN|DUSK)$')
            CUT = 'CUT TO:'
            FADE = 'FADE IN:'
            lines = text.splitlines(True)
            token_ids = []
            for l in lines:
                u = l.upper().strip()
                if u == '':
                    token_ids.extend(self.enc.encode(l))
                    continue
                if HEADER_PAT.match(u) or CUT in u or FADE in u:
                    token_ids.extend(self.enc.encode(l))
                else:
                    token_ids.extend(compress_ids(self.enc.encode(l)))
        else:
            token_ids = self.enc.encode(text)
            token_ids = compress_ids(token_ids)
        text_after_tpd = self.enc.decode(token_ids)
        encoded = text_after_tpd
        for phrase, symbol in sorted(self.vocab.mwe_map.items(), key=lambda x: len(x[0]), reverse=True):
            pattern = '\\b' + re.escape(phrase) + '\\b'
            safe_symbol = symbol.replace('\\', '\\\\')
            encoded = re.sub(pattern, safe_symbol, encoded, flags=re.IGNORECASE)
        for label, symbol in self.vocab.symbols.items():
            variations = [label, label.replace('_', ' '), label.replace('_', '')]
            safe_symbol = symbol.replace('\\', '\\\\')
            for var in variations:
                encoded = re.sub('\\b' + re.escape(var) + '\\b', safe_symbol, encoded, flags=re.IGNORECASE)
        entity_pattern = '(PERSONA|LOCAL|OBJ|MOTIF|EVENT|TIME|THEME|SCENE)\\s*#(\\d+)'

        def encode_entity(match):
            entity_type = match.group(1)
            entity_id = int(match.group(2))
            if entity_type in self.vocab.entity_prefix:
                prefix = self.vocab.entity_prefix[entity_type]
                id_str = to_baseN(entity_id, self.vocab.num_alphabet)
                return prefix + id_str
            return match.group(0)
        encoded = re.sub(entity_pattern, encode_entity, encoded, flags=re.IGNORECASE)
        encoded = re.sub('\\s+', ' ', encoded)
        new_tokens = len(self.enc.encode(encoded))
        compression_ratio = 1 - new_tokens / original_tokens if original_tokens > 0 else 0
        return (encoded, compression_ratio)

    def encode_pure_tpd(self, text: str) -> Tuple[List[int], float]:
        """
        Pure token-level encoding with TPD only (no string operations).
        Returns token IDs and compression ratio.
        """
        text = canonicalize(text, domain='auto')
        original_ids = self.enc.encode(text)
        original_count = len(original_ids)
        if self.use_tpd and self.trie:
            encoded_ids = self.trie.encode_sequence(original_ids)
        else:
            encoded_ids = original_ids
        new_count = len(encoded_ids)
        compression_ratio = 1 - new_count / original_count if original_count > 0 else 0
        return (encoded_ids, compression_ratio)

    def encode_entity(self, entity_type: str, entity_id: int) -> str:
        """Encode entity as prefix + baseN ID"""
        if entity_type in self.vocab.entity_prefix:
            prefix = self.vocab.entity_prefix[entity_type]
            id_str = to_baseN(entity_id, self.vocab.num_alphabet)
            return prefix + id_str
        return f'{entity_type}#{entity_id}'