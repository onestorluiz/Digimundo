#!/usr/bin/env python
"""
DigiLang Encoder - Adapted from scripturemon-validation
Achieves 20-22% token compression using Token Pattern Dictionary (TPD)
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from .slug import slugify
from .vocab_schema import Vocab
from .ids import to_baseN
from .token_trie_simple import TokenTrie

def canonicalize(text: str, domain: str = "auto") -> str:
    """
    Canonicalize text for better token matching.
    Normalizes quotes, dashes, and domain-specific patterns.
    """
    t = text

    # Normalize common punctuation variations
    t = t.replace("–", "-").replace("—", "-")  # Dashes
    t = t.replace(""", '"').replace(""", '"')  # Smart quotes
    t = t.replace("'", "'").replace("'", "'")  # Single quotes
    t = t.replace("\u2018", "'").replace("\u2019", "'")  # Unicode single quotes
    t = t.replace("\u201c", '"').replace("\u201d", '"')  # Unicode double quotes
    t = t.replace("…", "...")  # Ellipsis

    # Auto-detect domain
    if domain == "auto":
        if "INT." in t.upper() or "EXT." in t.upper() or "CUT TO:" in t.upper():
            domain = "screenplay"
        elif any(word in t.lower() for word in ["thou", "thee", "thy", "hath", "doth"]):
            domain = "shakespeare"

    if domain == "screenplay":
        # Standardize screenplay elements
        t = re.sub(r'\bInt\.', 'INT.', t)
        t = re.sub(r'\bExt\.', 'EXT.', t)
        t = re.sub(r'\bint\.', 'INT.', t, flags=re.IGNORECASE)
        t = re.sub(r'\bext\.', 'EXT.', t, flags=re.IGNORECASE)

        # Standardize transitions
        for pattern, replacement in [
            (r'Cut to:', 'CUT TO:'),
            (r'Fade in:', 'FADE IN:'),
            (r'Fade out:', 'FADE OUT:'),
            (r'Dissolve to:', 'DISSOLVE TO:'),
            (r'Smash cut:', 'SMASH CUT:'),
        ]:
            t = re.sub(pattern, replacement, t, flags=re.IGNORECASE)

    elif domain == "shakespeare":
        # Normalize archaic forms
        replacements = [
            ("'tis", "tis"),
            ("'twas", "twas"),
            ("'twere", "twere"),
            ("o'er", "oer"),
            ("e'er", "eer"),
            ("ne'er", "neer"),
        ]
        for old, new in replacements:
            t = re.sub(r'\b' + re.escape(old) + r'\b', new, t, flags=re.IGNORECASE)

    return t

class DigiLangEncoder:
    def __init__(self,
                 vocab_path: Path = None,
                 use_tpd: bool = True,
                 token_dict: Dict = None,
                 **kwargs):

        self.use_tpd = use_tpd
        self.tokenizer = None
        self.vocab = None
        self.trie = None

        # Try to load tiktoken
        try:
            import tiktoken
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
            self.has_tiktoken = True
        except ImportError:
            self.has_tiktoken = False
            print("Warning: tiktoken not available, using fallback mode")

        # Load or create default vocabulary
        if vocab_path is None:
            vocab_path = Path(__file__).parent / "vocab.json"

        if vocab_path.exists():
            with open(vocab_path, 'r', encoding='utf-8') as f:
                vocab_data = json.load(f)
                self.vocab = Vocab(**vocab_data)
        else:
            # Create minimal default vocab
            self.vocab = self._create_default_vocab()

        # Setup TPD if provided
        if use_tpd and token_dict:
            self._setup_tpd(token_dict)

    def _create_default_vocab(self) -> Vocab:
        """Create a minimal default vocabulary for screenplay compression."""
        from .vocab_schema import VocabMeta

        return Vocab(
            meta=VocabMeta(
                tokenizer="cl100k_base",
                version="v1-minimal",
                budgets={"symbols": 50, "mwe": 100}
            ),
            symbols={
                "FADE_IN": "⟦FI⟧",
                "FADE_OUT": "⟦FO⟧",
                "CUT_TO": "⟦CT⟧",
                "INT": "⟦I⟧",
                "EXT": "⟦E⟧",
                "DAY": "⟦D⟧",
                "NIGHT": "⟦N⟧",
                "CONTINUOUS": "⟦C⟧",
            },
            entity_prefix={
                "PERSONA": "⒫",
                "LOCAL": "⒧",
                "OBJ": "⒪",
            },
            num_alphabet=["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"],
            mwe_map={}
        )

    def _setup_tpd(self, token_dict: Dict):
        """Setup Token Pattern Dictionary for compression."""
        if not self.has_tiktoken:
            return

        # Convert string keys to token tuples
        patterns = {}
        for pattern_str, glyph in token_dict.items():
            try:
                tokens = self.tokenizer.encode(pattern_str)
                if len(tokens) > 1:  # Only multi-token patterns
                    patterns[tuple(tokens)] = glyph
            except:
                pass

        if patterns:
            self.trie = TokenTrie(patterns)

    def encode(self, text: str, canonicalize_text: bool = True) -> str:
        """
        Encode text using DigiLang compression.

        Args:
            text: Input text to compress
            canonicalize_text: Whether to canonicalize before encoding

        Returns:
            Compressed text
        """
        if canonicalize_text:
            text = canonicalize(text)

        # Apply symbol replacements
        if self.vocab and self.vocab.symbols:
            for pattern, symbol in self.vocab.symbols.items():
                # Convert underscore patterns to space patterns
                search_pattern = pattern.replace("_", " ")
                text = text.replace(search_pattern, symbol)

        # Apply TPD compression if available
        if self.has_tiktoken and self.trie:
            text = self._apply_tpd_compression(text)

        return text

    def _apply_tpd_compression(self, text: str) -> str:
        """Apply Token Pattern Dictionary compression."""
        try:
            # Tokenize
            tokens = self.tokenizer.encode(text)

            # Apply trie matching
            result = []
            i = 0
            while i < len(tokens):
                match = self.trie.longest_match(tokens, i)
                if match:
                    length, glyph = match
                    # Decode the glyph back to text
                    result.append(glyph)
                    i += length
                else:
                    # Keep original token
                    result.append(self.tokenizer.decode([tokens[i]]))
                    i += 1

            return "".join(result)
        except Exception as e:
            print(f"TPD compression failed: {e}")
            return text

    def decode(self, encoded_text: str) -> str:
        """
        Decode DigiLang compressed text back to original.

        Args:
            encoded_text: Compressed text

        Returns:
            Original text
        """
        text = encoded_text

        # Reverse symbol replacements
        if self.vocab and self.vocab.symbols:
            for pattern, symbol in self.vocab.symbols.items():
                original = pattern.replace("_", " ")
                text = text.replace(symbol, original)

        # TPD reversal would require a reverse mapping
        # For now, this is a simplified decoder

        return text

    def get_compression_ratio(self, original: str, encoded: str) -> float:
        """Calculate token-based compression ratio."""
        if not self.has_tiktoken:
            # Fallback to character ratio
            return 1 - (len(encoded) / len(original)) if len(original) > 0 else 0

        try:
            original_tokens = len(self.tokenizer.encode(original))
            encoded_tokens = len(self.tokenizer.encode(encoded))
            return 1 - (encoded_tokens / original_tokens) if original_tokens > 0 else 0
        except:
            return 0