"""
Cache Optimizer for OMEGA-ASCENT
LRU cache with size management and TTL
"""

import time
import json
import hashlib
from functools import lru_cache
from typing import Any, Optional
from pathlib import Path

class CacheOptimizer:
    """Advanced caching with memory management"""

    def __init__(self, max_size_mb: int = 512, ttl_seconds: int = 3600):
        self.max_size_mb = max_size_mb
        self.ttl_seconds = ttl_seconds
        self.cache = {}
        self.access_times = {}
        self.sizes = {}
        self.hits = 0
        self.misses = 0

    def _get_cache_key(self, key: str) -> str:
        """Generate cache key"""
        return hashlib.md5(key.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Get from cache with TTL check"""
        cache_key = self._get_cache_key(key)

        if cache_key in self.cache:
            # Check TTL
            if time.time() - self.access_times[cache_key] > self.ttl_seconds:
                del self.cache[cache_key]
                del self.access_times[cache_key]
                del self.sizes[cache_key]
                self.misses += 1
                return None

            self.hits += 1
            self.access_times[cache_key] = time.time()
            return self.cache[cache_key]

        self.misses += 1
        return None

    def set(self, key: str, value: Any, size_bytes: int = 0):
        """Set cache with size tracking"""
        cache_key = self._get_cache_key(key)

        # Check total size
        total_size_mb = sum(self.sizes.values()) / 1024 / 1024

        # Evict if needed
        while total_size_mb > self.max_size_mb and self.cache:
            # Remove oldest
            oldest_key = min(self.access_times, key=self.access_times.get)
            del self.cache[oldest_key]
            del self.access_times[oldest_key]
            del self.sizes[oldest_key]
            total_size_mb = sum(self.sizes.values()) / 1024 / 1024

        self.cache[cache_key] = value
        self.access_times[cache_key] = time.time()
        self.sizes[cache_key] = size_bytes

    def get_stats(self) -> dict:
        """Get cache statistics"""
        total_size_mb = sum(self.sizes.values()) / 1024 / 1024
        hit_rate = self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0

        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "items": len(self.cache),
            "size_mb": total_size_mb,
            "max_size_mb": self.max_size_mb
        }

    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.access_times.clear()
        self.sizes.clear()
        self.hits = 0
        self.misses = 0

# Global cache instance
cache = CacheOptimizer(max_size_mb=512, ttl_seconds=3600)
