import tiktoken
import re
from typing import Tuple

class NaiveTiktokenCompressor:
    def __init__(self):
        self.encoder = tiktoken.get_encoding("cl100k_base")
        # Common English stopwords
        self.stopwords = set(['the', 'is', 'at', 'which', 'on', 'a', 'an', 
                             'as', 'are', 'was', 'were', 'been', 'be',
                             'have', 'has', 'had', 'do', 'does', 'did',
                             'will', 'would', 'could', 'should', 'may',
                             'might', 'must', 'can', 'shall', 'to', 'of',
                             'in', 'for', 'with', 'by', 'from', 'up',
                             'about', 'into', 'through', 'during', 'before',
                             'after', 'above', 'below', 'between', 'under'])
    
    def compress(self, text: str) -> Tuple[str, float]:
        """Remove stopwords to compress text"""
        original_tokens = len(self.encoder.encode(text))
        
        # Remove stopwords
        words = text.split()
        compressed_words = [w for w in words if w.lower() not in self.stopwords]
        compressed = ' '.join(compressed_words)
        
        compressed_tokens = len(self.encoder.encode(compressed))
        compression_ratio = 1 - (compressed_tokens / original_tokens) if original_tokens > 0 else 0
        
        return compressed, compression_ratio
    
    def decompress(self, text: str) -> str:
        """Cannot perfectly decompress - returns as-is"""
        return text
