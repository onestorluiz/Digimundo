"""
Cache Global Unificado - Singleton Pattern
Elimina 3 sistemas de cache redundantes
"""

import time
import json
import hashlib
from typing import Any, Optional, Callable
from functools import lru_cache
from collections import OrderedDict
from threading import Lock

class GlobalCache:
    """Cache unificado com LRU, TTL e thread-safety"""

    _instance = None
    _lock = Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.cache = OrderedDict()
        self.timestamps = {}
        self.sizes = {}

        # Configurações
        self.max_size_mb = 256
        self.ttl_seconds = 3600
        self.max_items = 10000

        # Estatísticas
        self.hits = 0
        self.misses = 0

        self._initialized = True

    def _make_key(self, key: str) -> str:
        """Gera chave hash para o cache"""
        if isinstance(key, str):
            return hashlib.md5(key.encode()).hexdigest()
        return hashlib.md5(str(key).encode()).hexdigest()

    def _is_expired(self, key: str) -> bool:
        """Verifica se item expirou"""
        if key not in self.timestamps:
            return True
        return (time.time() - self.timestamps[key]) > self.ttl_seconds

    def _evict_lru(self):
        """Remove item menos recentemente usado"""
        if self.cache:
            oldest = next(iter(self.cache))
            del self.cache[oldest]
            del self.timestamps[oldest]
            if oldest in self.sizes:
                del self.sizes[oldest]

    def get(self, key: str, compute_fn: Optional[Callable] = None) -> Optional[Any]:
        """
        Obtém valor do cache ou computa se necessário

        Args:
            key: Chave do cache
            compute_fn: Função para computar valor se não estiver em cache

        Returns:
            Valor cacheado ou computado
        """
        cache_key = self._make_key(key)

        # Check hit
        if cache_key in self.cache and not self._is_expired(cache_key):
            # Move para o final (mais recente)
            self.cache.move_to_end(cache_key)
            self.hits += 1
            return self.cache[cache_key]

        # Miss - computar se função fornecida
        self.misses += 1

        if compute_fn:
            value = compute_fn()
            self.set(key, value)
            return value

        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Armazena valor no cache

        Args:
            key: Chave do cache
            value: Valor a armazenar
            ttl: TTL customizado em segundos
        """
        cache_key = self._make_key(key)

        # Verificar limite de itens
        while len(self.cache) >= self.max_items:
            self._evict_lru()

        # Armazenar
        self.cache[cache_key] = value
        self.cache.move_to_end(cache_key)
        self.timestamps[cache_key] = time.time()

        # Estimar tamanho (simplificado)
        self.sizes[cache_key] = len(str(value))

    def invalidate(self, key: str):
        """Invalida entrada específica do cache"""
        cache_key = self._make_key(key)
        if cache_key in self.cache:
            del self.cache[cache_key]
            del self.timestamps[cache_key]
            if cache_key in self.sizes:
                del self.sizes[cache_key]

    def clear(self):
        """Limpa todo o cache"""
        self.cache.clear()
        self.timestamps.clear()
        self.sizes.clear()
        self.hits = 0
        self.misses = 0

    def get_stats(self) -> dict:
        """Retorna estatísticas do cache"""
        total_size = sum(self.sizes.values())
        hit_rate = self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0

        return {
            "items": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.2%}",
            "size_bytes": total_size,
            "size_mb": total_size / (1024 * 1024),
            "max_size_mb": self.max_size_mb
        }

    @lru_cache(maxsize=128)
    def cached_method(self, key: str) -> Any:
        """Método com cache LRU adicional para operações frequentes"""
        return self.get(key)

# Instância global única
cache = GlobalCache()

# Decorador para facilitar uso
def cached(ttl: int = 3600):
    """
    Decorador para cachear resultado de funções

    Usage:
        @cached(ttl=1800)
        def expensive_function(param):
            return compute_something(param)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Criar chave única baseada em função e argumentos
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Tentar obter do cache ou computar
            return cache.get(
                cache_key,
                compute_fn=lambda: func(*args, **kwargs)
            )
        return wrapper
    return decorator

# Funções de compatibilidade para migração
class LegacyCacheAdapter:
    """Adaptador para código legado que usa caches antigos"""

    def __init__(self):
        self.cache = cache  # Usa cache global

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache.set(key, value)

    def clear(self):
        self.cache.clear()

# Aliases para compatibilidade
MemoryCache = LegacyCacheAdapter
CacheOptimizer = LegacyCacheAdapter
SimpleCache = LegacyCacheAdapter
