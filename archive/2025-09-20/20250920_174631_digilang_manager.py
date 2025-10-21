"""
DigiLang Manager - Unified interface for token compression
Integrates advanced DigiLang from validation with champion architecture
"""
import json
import hashlib
from pathlib import Path
from typing import Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging

# Import advanced DigiLang
from .digilang_advanced import DigiLangEncoder, canonicalize

# Keep compatibility with simple version
from .digilang_simple import DigiLangCompressor as SimpleCompressor

logger = logging.getLogger(__name__)


@dataclass
class CompressionResult:
    """Result of compression operation."""
    original_text: str
    compressed_text: str
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    method_used: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class DigiLangManager:
    """
    Unified DigiLang compression manager.
    Provides interface to both simple and advanced compression methods.
    """

    def __init__(self,
                 mode: str = "advanced",
                 cache_dir: Path = None,
                 vocab_path: Path = None):
        """
        Initialize DigiLang Manager.

        Args:
            mode: "simple", "advanced", or "auto"
            cache_dir: Directory for caching results
            vocab_path: Path to vocabulary for advanced mode
        """
        self.mode = mode
        self.cache_dir = cache_dir or Path.home() / ".scripturemon" / "digilang_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize compressors
        self.simple_compressor = SimpleCompressor()
        self.advanced_encoder = None

        # Try to initialize advanced encoder
        try:
            self.advanced_encoder = DigiLangEncoder(vocab_path=vocab_path)
            self.has_advanced = True
        except Exception as e:
            logger.warning(f"Could not initialize advanced encoder: {e}")
            self.has_advanced = False
            if mode == "advanced":
                mode = "simple"
                logger.info("Falling back to simple mode")

        # Statistics
        self.stats = {
            'total_processed': 0,
            'total_compressed': 0,
            'simple_count': 0,
            'advanced_count': 0,
            'cache_hits': 0,
            'average_ratio': 0.0
        }

    def compress(self,
                 text: str,
                 mode: str = None,
                 canonicalize_text: bool = True) -> CompressionResult:
        """
        Compress text using specified method.

        Args:
            text: Text to compress
            mode: Override default mode ("simple", "advanced", "auto")
            canonicalize_text: Whether to canonicalize text first

        Returns:
            CompressionResult with details
        """
        # Check cache
        cache_key = self._get_cache_key(text)
        cached = self._get_cached(cache_key)
        if cached:
            self.stats['cache_hits'] += 1
            return cached

        # Determine mode
        if mode is None:
            mode = self.mode

        if mode == "auto":
            # Auto-select based on text characteristics
            mode = self._auto_select_mode(text)

        # Apply compression
        if mode == "advanced" and self.has_advanced:
            result = self._compress_advanced(text, canonicalize_text)
            self.stats['advanced_count'] += 1
        else:
            result = self._compress_simple(text)
            self.stats['simple_count'] += 1

        # Update statistics
        self.stats['total_processed'] += 1
        self.stats['total_compressed'] += len(result.compressed_text)

        # Update average ratio
        n = self.stats['total_processed']
        old_avg = self.stats['average_ratio']
        self.stats['average_ratio'] = old_avg * (n-1)/n + result.compression_ratio/n

        # Cache result
        self._cache_result(cache_key, result)

        return result

    def _compress_simple(self, text: str) -> CompressionResult:
        """Apply simple compression."""
        compressed, ratio = self.simple_compressor.compress(text)

        # Estimate tokens (rough: 1 token ≈ 4 characters)
        original_tokens = len(text) // 4
        compressed_tokens = len(compressed) // 4

        return CompressionResult(
            original_text=text,
            compressed_text=compressed,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=ratio,
            method_used="simple",
            metadata={'patterns_applied': len(self.simple_compressor.patterns)}
        )

    def _compress_advanced(self, text: str, canonicalize_text: bool) -> CompressionResult:
        """Apply advanced token-aware compression."""
        # Canonicalize if requested
        if canonicalize_text:
            text_to_encode = canonicalize(text)
        else:
            text_to_encode = text

        # Encode
        compressed = self.advanced_encoder.encode(text_to_encode, canonicalize_text=False)

        # Calculate compression ratio
        ratio = self.advanced_encoder.get_compression_ratio(text, compressed)

        # Get token counts if tiktoken available
        if self.advanced_encoder.has_tiktoken:
            try:
                tokenizer = self.advanced_encoder.tokenizer
                original_tokens = len(tokenizer.encode(text))
                compressed_tokens = len(tokenizer.encode(compressed))
            except:
                original_tokens = len(text) // 4
                compressed_tokens = len(compressed) // 4
        else:
            original_tokens = len(text) // 4
            compressed_tokens = len(compressed) // 4

        return CompressionResult(
            original_text=text,
            compressed_text=compressed,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=ratio,
            method_used="advanced",
            metadata={
                'canonicalized': canonicalize_text,
                'has_tiktoken': self.advanced_encoder.has_tiktoken
            }
        )

    def decompress(self, compressed_text: str, method: str = None) -> str:
        """
        Decompress text.

        Args:
            compressed_text: Compressed text
            method: Method used for compression ("simple" or "advanced")

        Returns:
            Original text
        """
        if method == "advanced" and self.has_advanced:
            return self.advanced_encoder.decode(compressed_text)
        else:
            return self.simple_compressor.decompress(compressed_text)

    def _auto_select_mode(self, text: str) -> str:
        """Auto-select compression mode based on text characteristics."""
        # Use advanced for screenplays and long texts
        if len(text) > 5000:
            return "advanced" if self.has_advanced else "simple"

        # Check for screenplay markers
        if any(marker in text.upper() for marker in ["INT.", "EXT.", "FADE", "CUT TO:"]):
            return "advanced" if self.has_advanced else "simple"

        # Default to simple for short texts
        return "simple"

    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text."""
        return hashlib.md5(text.encode()).hexdigest()

    def _get_cached(self, cache_key: str) -> Optional[CompressionResult]:
        """Get cached compression result."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    return CompressionResult(
                        original_text=data['original_text'],
                        compressed_text=data['compressed_text'],
                        original_tokens=data['original_tokens'],
                        compressed_tokens=data['compressed_tokens'],
                        compression_ratio=data['compression_ratio'],
                        method_used=data['method_used'],
                        timestamp=datetime.fromisoformat(data['timestamp']),
                        metadata=data.get('metadata', {})
                    )
            except:
                pass
        return None

    def _cache_result(self, cache_key: str, result: CompressionResult):
        """Cache compression result."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump({
                    'original_text': result.original_text,
                    'compressed_text': result.compressed_text,
                    'original_tokens': result.original_tokens,
                    'compressed_tokens': result.compressed_tokens,
                    'compression_ratio': result.compression_ratio,
                    'method_used': result.method_used,
                    'timestamp': result.timestamp.isoformat(),
                    'metadata': result.metadata
                }, f)
        except:
            pass

    def get_statistics(self) -> Dict[str, Any]:
        """Get compression statistics."""
        return {
            **self.stats,
            'cache_size': len(list(self.cache_dir.glob("*.json"))),
            'mode': self.mode,
            'has_advanced': self.has_advanced
        }

    def optimize_for_context(self,
                           text: str,
                           max_tokens: int = 8000,
                           mode: str = None) -> str:
        """
        Optimize text to fit in limited context window.

        Args:
            text: Original text
            max_tokens: Maximum token limit
            mode: Compression mode to use

        Returns:
            Optimized text
        """
        # First try compression
        result = self.compress(text, mode=mode)

        if result.compressed_tokens <= max_tokens:
            return result.compressed_text

        # If still too large, use simple truncation from simple compressor
        return self.simple_compressor.optimize_for_context(text, max_tokens)


# Singleton instance
_manager: Optional[DigiLangManager] = None


def get_digilang_manager(mode: str = "auto") -> DigiLangManager:
    """Get singleton DigiLang manager instance."""
    global _manager
    if _manager is None:
        _manager = DigiLangManager(mode=mode)
    return _manager


def compress_text(text: str, mode: str = "auto") -> Tuple[str, float]:
    """
    Convenience function for text compression.

    Args:
        text: Text to compress
        mode: Compression mode

    Returns:
        (compressed_text, compression_ratio)
    """
    manager = get_digilang_manager(mode)
    result = manager.compress(text, mode=mode)
    return result.compressed_text, result.compression_ratio


def decompress_text(compressed: str, method: str = "auto") -> str:
    """
    Convenience function for text decompression.

    Args:
        compressed: Compressed text
        method: Method used for compression

    Returns:
        Original text
    """
    manager = get_digilang_manager()
    return manager.decompress(compressed, method)