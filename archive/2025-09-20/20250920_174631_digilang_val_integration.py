#!/usr/bin/env python3
"""
DigiLang Validation Integration - Full Implementation
Integrates the complete validation approach with our existing system
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import tiktoken
from dataclasses import dataclass

# Add validation src to path for imports
validation_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/src")
if str(validation_path) not in sys.path:
    sys.path.insert(0, str(validation_path))

# Import validation's complete system
try:
    from digilang.encoder import DigiLangEncoder as ValidationEncoder
    from digilang.decoder import DigiLangDecoder as ValidationDecoder
    from digilang.multitpd import load_layers, save_layers
    from digilang.tpd_greedy_lazy import build_tpd_greedy_lazy_for_corpus
    VALIDATION_AVAILABLE = True
except ImportError:
    VALIDATION_AVAILABLE = False
    print("Warning: Validation DigiLang not available")

# Import our existing systems
from .digilang_simple import DigiLangCompressor
from .digilang_manager import CompressionResult


@dataclass
class ValidationCompressionResult(CompressionResult):
    """Extended result with validation-specific metrics."""
    layers_applied: int = 0
    patterns_used: int = 0
    tpd_hits: int = 0


class DigiLangValidation:
    """
    Complete integration with validation's DigiLang system.
    This properly uses their multi-layer TPD approach.
    """

    def __init__(self,
                 tpd_path: str = None,
                 use_simple_patterns: bool = True,
                 use_multi_layer: bool = True):
        """
        Initialize with validation's complete system.

        Args:
            tpd_path: Path to TPD dictionary (defaults to validation's greedy_lazy)
            use_simple_patterns: Also apply our 87 PT/EN patterns
            use_multi_layer: Use multi-layer TPD compression
        """
        self.use_simple_patterns = use_simple_patterns
        self.use_multi_layer = use_multi_layer

        # Our simple compressor
        if use_simple_patterns:
            self.simple_compressor = DigiLangCompressor()

        # Validation's system
        if VALIDATION_AVAILABLE:
            # Use validation's greedy_lazy TPD by default
            if tpd_path is None:
                tpd_path = "/Users/clubproducoes/Digimundo/scripturemon-validation/data/tpd/greedy_lazy/token_dict.json"

            # Check if TPD exists
            if not Path(tpd_path).exists():
                print(f"Warning: TPD not found at {tpd_path}")
                tpd_path = "data/tpd/default/token_dict.json"  # Fallback

            # Initialize validation encoder/decoder
            self.val_encoder = ValidationEncoder(
                use_tpd=True,
                token_dict_path=tpd_path
            )
            self.val_decoder = ValidationDecoder(
                use_tpd=True,
                token_dict_path=tpd_path
            )

            # Load multi-layer info if available
            self.layers_info = None
            if Path(tpd_path).exists() and use_multi_layer:
                try:
                    self.tries, self.glyph_layers, self.meta = load_layers(tpd_path)
                    self.layers_info = {
                        'num_layers': len(self.tries),
                        'total_patterns': sum(len(t.patterns) for t in self.tries)
                    }
                except:
                    pass
        else:
            self.val_encoder = None
            self.val_decoder = None
            self.layers_info = None

        # Tokenizer for measurements
        self.enc = tiktoken.get_encoding("cl100k_base")

        # Statistics
        self.stats = {
            'total_compressions': 0,
            'total_tokens_saved': 0,
            'avg_compression': 0.0
        }

    def compress(self, text: str, preserve_headers: bool = True) -> ValidationCompressionResult:
        """
        Compress using validation's full approach.

        Args:
            text: Text to compress
            preserve_headers: Preserve screenplay headers (INT./EXT.)

        Returns:
            ValidationCompressionResult with metrics
        """
        original_text = text
        original_tokens = len(self.enc.encode(text))

        # Step 1: Apply our simple patterns first (if enabled)
        if self.use_simple_patterns and self.simple_compressor:
            text, _ = self.simple_compressor.compress(text)

        # Step 2: Apply validation's TPD compression
        if VALIDATION_AVAILABLE and self.val_encoder:
            # Use validation's encoder with all its features
            compressed_text, compression_ratio = self.val_encoder.encode(
                text,
                preserve_headers=preserve_headers,
                canonicalize_text=True  # Important for matching
            )
            text = compressed_text
        else:
            compression_ratio = 0.0

        # Calculate final metrics
        compressed_tokens = len(self.enc.encode(text))
        actual_ratio = 1 - (compressed_tokens / original_tokens) if original_tokens > 0 else 0

        # Update statistics
        self.stats['total_compressions'] += 1
        tokens_saved = original_tokens - compressed_tokens
        self.stats['total_tokens_saved'] += tokens_saved
        self.stats['avg_compression'] = self.stats['total_tokens_saved'] / (self.stats['total_compressions'] * original_tokens)

        # Create result
        return ValidationCompressionResult(
            original_text=original_text,
            compressed_text=text,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=actual_ratio,
            method_used="validation_full",
            metadata={
                'validation_ratio': compression_ratio,
                'layers_info': self.layers_info,
                'simple_patterns_used': self.use_simple_patterns,
                'preserve_headers': preserve_headers
            },
            layers_applied=self.layers_info['num_layers'] if self.layers_info else 1,
            patterns_used=self.layers_info['total_patterns'] if self.layers_info else 0
        )

    def decompress(self, compressed_text: str) -> str:
        """
        Decompress text using validation's decoder.

        Args:
            compressed_text: Compressed text

        Returns:
            Original text (approximately)
        """
        text = compressed_text

        # Step 1: Decompress with validation's decoder
        if VALIDATION_AVAILABLE and self.val_decoder:
            text = self.val_decoder.decode(text)

        # Step 2: Decompress our simple patterns
        if self.use_simple_patterns and self.simple_compressor:
            text = self.simple_compressor.decompress(text)

        return text

    def build_custom_tpd(self,
                         corpus_dir: str,
                         output_path: str,
                         K: int = 1500,
                         n_min: int = 2,
                         n_max: int = 8,
                         freq_min: int = 3):
        """
        Build a custom TPD from a corpus using validation's greedy-lazy algorithm.

        Args:
            corpus_dir: Directory with .txt files
            output_path: Where to save the TPD
            K: Number of patterns to select
            n_min/n_max: N-gram size range
            freq_min: Minimum frequency
        """
        if not VALIDATION_AVAILABLE:
            print("Validation system not available")
            return

        print(f"Building custom TPD from {corpus_dir}")
        print(f"Parameters: K={K}, n={n_min}-{n_max}, freq_min={freq_min}")

        # Use validation's builder
        mapping = build_tpd_greedy_lazy_for_corpus(
            corpus_dir=corpus_dir,
            K=K,
            n_min=n_min,
            n_max=n_max,
            freq_min=freq_min,
            time_budget_s=60.0  # 1 minute budget
        )

        print(f"Selected {len(mapping)} patterns")

        # Save the TPD
        meta = {
            "tokenizer": "cl100k_base",
            "K": K,
            "n_range": [n_min, n_max],
            "freq_min": freq_min,
            "algorithm": "greedy_lazy",
            "corpus": corpus_dir
        }

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        payload = {"meta": meta, "map": mapping}
        Path(output_path).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        print(f"Saved TPD to {output_path}")

        # Calculate potential savings
        total_gain = 0
        for glyph, ids in mapping.items():
            # Each replacement saves (len(ids) - 1) tokens
            total_gain += len(ids) - 1

        print(f"Average pattern length: {sum(len(ids) for ids in mapping.values()) / len(mapping):.1f} tokens")
        print(f"Maximum potential savings per use: {total_gain / len(mapping):.1f} tokens")

    def analyze_text(self, text: str) -> Dict:
        """
        Analyze how well text would compress with current TPD.

        Args:
            text: Text to analyze

        Returns:
            Analysis dictionary
        """
        tokens = self.enc.encode(text)
        original_count = len(tokens)

        # Simulate compression
        result = self.compress(text)

        # Analyze pattern matches
        pattern_matches = {}
        if self.layers_info and self.tries:
            for layer_idx, trie in enumerate(self.tries):
                matches = 0
                i = 0
                while i < len(tokens):
                    m = trie.longest_match(tokens, i)
                    if m:
                        matches += 1
                        i += m[0]  # Skip matched length
                    else:
                        i += 1
                pattern_matches[f"layer_{layer_idx}"] = matches

        return {
            'original_tokens': original_count,
            'compressed_tokens': result.compressed_tokens,
            'compression_ratio': result.compression_ratio,
            'tokens_saved': original_count - result.compressed_tokens,
            'pattern_matches': pattern_matches,
            'layers_info': self.layers_info,
            'reversible': True  # Validation's approach is reversible
        }

    def get_statistics(self) -> Dict:
        """Get compression statistics."""
        return {
            **self.stats,
            'validation_available': VALIDATION_AVAILABLE,
            'layers_info': self.layers_info,
            'simple_patterns': self.use_simple_patterns,
            'multi_layer': self.use_multi_layer
        }


# Convenience functions
def compress_with_validation(text: str) -> Tuple[str, float]:
    """
    Compress text using full validation approach.

    Returns:
        (compressed_text, compression_ratio)
    """
    compressor = DigiLangValidation()
    result = compressor.compress(text)
    return result.compressed_text, result.compression_ratio


def decompress_validation(compressed_text: str) -> str:
    """Decompress validation-compressed text."""
    compressor = DigiLangValidation()
    return compressor.decompress(compressed_text)


def analyze_compression_potential(text: str) -> Dict:
    """Analyze how well text would compress."""
    compressor = DigiLangValidation()
    return compressor.analyze_text(text)