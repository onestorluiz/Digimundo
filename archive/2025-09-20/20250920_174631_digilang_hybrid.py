#!/usr/bin/env python3
"""
DigiLang Hybrid V4 - Sistema Multi-Camada
Combina TUDO que já desenvolvemos em um sistema unificado
"""

import json
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging

# Importar nossos módulos existentes
from .digilang_simple import DigiLangCompressor
from .digilang_advanced import DigiLangEncoder
from .digilang_manager import DigiLangManager, CompressionResult

logger = logging.getLogger(__name__)


class DigiLangHybrid:
    """
    Sistema híbrido de compressão em múltiplas camadas.
    Aproveita TODO o trabalho já feito, combinando:

    1. Simple Patterns (nossos 87 padrões PT/EN)
    2. TPD Patterns (validation - token-aware)
    3. Keywords Extraction (70% compressão quando extremo)
    4. Script Schema (estrutura compacta para roteiros)
    5. Smart Segmentation (só enviar o relevante)
    """

    def __init__(self,
                 mode: str = "balanced",
                 enable_tpd: bool = True,
                 enable_keywords: bool = False,
                 enable_schema: bool = True,
                 enable_segmentation: bool = True):
        """
        Initialize hybrid compressor.

        Args:
            mode: "conservative", "balanced", "aggressive", "extreme"
            enable_tpd: Use Token Pattern Dictionary from validation
            enable_keywords: Use keyword extraction (lossy)
            enable_schema: Use script schema compression
            enable_segmentation: Use smart segmentation
        """
        self.mode = mode
        self.enable_tpd = enable_tpd
        self.enable_keywords = enable_keywords
        self.enable_schema = enable_schema
        self.enable_segmentation = enable_segmentation

        # Statistics
        self.stats = {
            'layer1_simple': 0,
            'layer2_tpd': 0,
            'layer3_keywords': 0,
            'layer4_schema': 0,
            'layer5_segment': 0,
            'total_compressions': 0,
            'total_saved_tokens': 0
        }

        # LAYER 1: Simple Compressor (nossos 87 padrões)
        self.simple_compressor = DigiLangCompressor()

        # LAYER 2: Advanced TPD
        self.tpd_encoder = None
        if enable_tpd:
            self._init_tpd_encoder()

        # LAYER 3: Keywords Extractor
        self.keywords_extractor = None
        if enable_keywords:
            self._init_keywords_extractor()

        # LAYER 4: Script Schema
        self.script_schema = self._init_script_schema() if enable_schema else None

        # Cache
        self.cache = {}

    def _init_tpd_encoder(self):
        """Initialize TPD encoder with validation dictionary."""
        try:
            # Try to load TPD from validation
            tpd_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/data/tpd/greedy_lazy/token_dict.json")

            if tpd_path.exists():
                with open(tpd_path) as f:
                    tpd_data = json.load(f)
                    token_dict = tpd_data.get("map", {})

                self.tpd_encoder = DigiLangEncoder(token_dict=token_dict)
                logger.info(f"Loaded TPD with {len(token_dict)} patterns")
            else:
                # Fallback to advanced encoder without TPD
                self.tpd_encoder = DigiLangEncoder()
                logger.warning("TPD file not found, using basic advanced encoder")

        except Exception as e:
            logger.error(f"Failed to init TPD encoder: {e}")
            self.tpd_encoder = None

    def _init_keywords_extractor(self):
        """Initialize keyword extraction (lossy but high compression)."""
        # This would use NLTK or spaCy to extract keywords
        # For now, simple implementation
        pass

    def _init_script_schema(self) -> Dict[str, str]:
        """Initialize script schema patterns."""
        return {
            # Scene headers
            "INT.": "I:",
            "EXT.": "E:",
            "INT./EXT.": "IE:",
            " - DAY": "-D",
            " - NIGHT": "-N",
            " - CONTINUOUS": "-C",
            " - LATER": "-L",
            " - MOMENTS LATER": "-ML",

            # Transitions
            "FADE IN:": "FI:",
            "FADE OUT.": "FO.",
            "FADE TO BLACK.": "FTB.",
            "CUT TO:": "CT:",
            "DISSOLVE TO:": "DT:",
            "SMASH CUT:": "SC:",
            "MATCH CUT:": "MC:",
            "TIME CUT:": "TC:",

            # Common actions (PT)
            "entra em cena": ">>",
            "sai de cena": "<<",
            "olha para": "->",
            "vira-se para": "=>",
            "caminha para": "~>",
            "corre para": ">>",
            "senta-se": "[s]",
            "levanta-se": "[l]",
            "pega": "[p]",
            "abre": "[a]",
            "fecha": "[f]",

            # Parentheticals
            "(beat)": "(b)",
            "(pausa)": "(p)",
            "(sussurrando)": "(s)",
            "(gritando)": "(g)",
            "(rindo)": "(r)",
            "(chorando)": "(c)",
            "(off)": "(o)",
            "(V.O.)": "(vo)",
            "(O.S.)": "(os)",
            "(CONT'D)": "(cd)",
            "(continua)": "(c)",

            # Common phrases
            "Eu não sei": "ENS",
            "O que você": "OQV",
            "Por favor": "PF",
            "Com certeza": "CC",
            "Muito bem": "MB",
            "De acordo": "DA",
        }

    def compress(self,
                 text: str,
                 target_tokens: Optional[int] = None,
                 context: Optional[str] = None) -> CompressionResult:
        """
        Compress text using hybrid multi-layer approach.

        Args:
            text: Text to compress
            target_tokens: Target token count (will adjust aggressiveness)
            context: Optional context for segmentation

        Returns:
            CompressionResult with compressed text and metrics
        """
        # Check cache
        cache_key = hashlib.md5(f"{text}{self.mode}{target_tokens}".encode()).hexdigest()
        if cache_key in self.cache:
            return self.cache[cache_key]

        original_text = text
        original_tokens = self._estimate_tokens(text)

        # LAYER 5: Segmentation (if enabled and context provided)
        if self.enable_segmentation and context:
            text = self._segment_by_relevance(text, context)
            if len(text) < len(original_text) * 0.5:
                self.stats['layer5_segment'] += 1

        # LAYER 4: Script Schema (if enabled)
        if self.enable_schema and self.script_schema:
            for pattern, replacement in self.script_schema.items():
                text = text.replace(pattern, replacement)
            self.stats['layer4_schema'] += 1

        # LAYER 1: Simple Patterns (always applied)
        text, simple_ratio = self.simple_compressor.compress(text)
        self.stats['layer1_simple'] += 1

        # LAYER 2: TPD (if enabled and available)
        if self.enable_tpd and self.tpd_encoder:
            try:
                text = self.tpd_encoder.encode(text, canonicalize_text=False)
                self.stats['layer2_tpd'] += 1
            except:
                pass

        # LAYER 3: Keywords (only if aggressive mode or target requires)
        current_tokens = self._estimate_tokens(text)
        if self.enable_keywords and target_tokens:
            if current_tokens > target_tokens * 1.5:
                text = self._extract_keywords(text)
                self.stats['layer3_keywords'] += 1

        # Calculate final metrics
        compressed_tokens = self._estimate_tokens(text)
        compression_ratio = 1 - (compressed_tokens / original_tokens) if original_tokens > 0 else 0

        # Update stats
        self.stats['total_compressions'] += 1
        self.stats['total_saved_tokens'] += (original_tokens - compressed_tokens)

        # Create result
        result = CompressionResult(
            original_text=original_text,
            compressed_text=text,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=compression_ratio,
            method_used=f"hybrid_{self.mode}",
            metadata={
                'layers_applied': self._get_applied_layers(),
                'mode': self.mode,
                'reversible': not self.enable_keywords  # Keywords are lossy
            }
        )

        # Cache result
        self.cache[cache_key] = result

        return result

    def decompress(self, compressed_text: str) -> str:
        """
        Decompress text (reverse all reversible layers).

        Args:
            compressed_text: Compressed text

        Returns:
            Original text (or closest possible if keywords were used)
        """
        text = compressed_text

        # Reverse LAYER 2: TPD
        if self.tpd_encoder:
            try:
                text = self.tpd_encoder.decode(text)
            except:
                pass

        # Reverse LAYER 1: Simple Patterns
        text = self.simple_compressor.decompress(text)

        # Reverse LAYER 4: Script Schema
        if self.script_schema:
            # Create reverse mapping
            reverse_schema = {v: k for k, v in self.script_schema.items()}
            for pattern, replacement in reverse_schema.items():
                text = text.replace(pattern, replacement)

        # Note: Keywords extraction (LAYER 3) is NOT reversible
        # Note: Segmentation (LAYER 5) cannot be reversed without original

        return text

    def _segment_by_relevance(self, text: str, context: str) -> str:
        """
        Extract only relevant segments based on context.
        Simple implementation - can be enhanced with embeddings.
        """
        # Split into paragraphs or scenes
        segments = text.split('\n\n')

        # Simple keyword matching for now
        context_words = set(context.lower().split())
        relevant_segments = []

        for segment in segments:
            segment_words = set(segment.lower().split())
            if context_words & segment_words:  # Intersection
                relevant_segments.append(segment)

        # If too few segments, return original
        if len(relevant_segments) < len(segments) * 0.3:
            return text

        return '\n\n'.join(relevant_segments)

    def _extract_keywords(self, text: str, words_per_sentence: int = 4) -> str:
        """
        Extract keywords for extreme compression (lossy).
        Based on Stakelum (2023) method - 70% reduction.
        """
        lines = text.split('\n')
        compressed_lines = []

        for line in lines:
            if not line.strip():
                compressed_lines.append('')
                continue

            # Keep scene headers intact
            if any(marker in line for marker in ['INT.', 'EXT.', 'I:', 'E:']):
                compressed_lines.append(line)
                continue

            # Extract keywords from regular text
            words = line.split()
            if len(words) <= words_per_sentence:
                compressed_lines.append(line)
            else:
                # Simple keyword extraction (can be improved with NLTK/spaCy)
                # Keep: proper nouns, verbs, important nouns
                keywords = []
                for word in words:
                    if (word[0].isupper() or  # Proper nouns
                        len(word) > 5 or       # Longer words tend to be important
                        word in ['não', 'sim', 'mas', 'porque']):  # Key words
                        keywords.append(word)

                    if len(keywords) >= words_per_sentence:
                        break

                compressed_lines.append(' '.join(keywords))

        return '\n'.join(compressed_lines)

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count."""
        try:
            import tiktoken
            enc = tiktoken.get_encoding("cl100k_base")
            return len(enc.encode(text))
        except:
            # Fallback: rough estimate
            return len(text) // 4

    def _get_applied_layers(self) -> List[str]:
        """Get list of layers applied in last compression."""
        layers = []
        if self.stats['layer5_segment'] > 0:
            layers.append("segmentation")
        if self.stats['layer4_schema'] > 0:
            layers.append("schema")
        layers.append("simple_patterns")  # Always applied
        if self.stats['layer2_tpd'] > 0:
            layers.append("tpd")
        if self.stats['layer3_keywords'] > 0:
            layers.append("keywords")
        return layers

    def get_statistics(self) -> Dict[str, Any]:
        """Get compression statistics."""
        return {
            **self.stats,
            'cache_size': len(self.cache),
            'mode': self.mode,
            'layers_enabled': {
                'simple': True,
                'tpd': self.enable_tpd,
                'keywords': self.enable_keywords,
                'schema': self.enable_schema,
                'segmentation': self.enable_segmentation
            }
        }

    def auto_compress(self,
                      text: str,
                      max_tokens: int,
                      preserve_quality: bool = True) -> CompressionResult:
        """
        Automatically adjust compression to meet token target.

        Args:
            text: Text to compress
            max_tokens: Maximum allowed tokens
            preserve_quality: If True, avoid lossy compression

        Returns:
            Best possible compression within constraints
        """
        # Start conservative
        self.mode = "conservative"
        self.enable_keywords = False

        result = self.compress(text)

        # If already fits, return
        if result.compressed_tokens <= max_tokens:
            return result

        # Try balanced
        self.mode = "balanced"
        result = self.compress(text)

        if result.compressed_tokens <= max_tokens:
            return result

        # Try aggressive
        self.mode = "aggressive"
        result = self.compress(text)

        if result.compressed_tokens <= max_tokens:
            return result

        # Last resort: keywords (lossy)
        if not preserve_quality:
            self.enable_keywords = True
            self.mode = "extreme"
            result = self.compress(text)

        return result


# Convenience functions
def compress_hybrid(text: str,
                    mode: str = "balanced",
                    target_tokens: Optional[int] = None) -> Tuple[str, float]:
    """
    Compress text using hybrid approach.

    Returns:
        (compressed_text, compression_ratio)
    """
    compressor = DigiLangHybrid(mode=mode)
    result = compressor.compress(text, target_tokens=target_tokens)
    return result.compressed_text, result.compression_ratio


def decompress_hybrid(compressed_text: str) -> str:
    """Decompress hybrid-compressed text."""
    compressor = DigiLangHybrid()
    return compressor.decompress(compressed_text)