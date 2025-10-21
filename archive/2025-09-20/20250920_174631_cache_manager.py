"""
Cache Manager - Sistema de cache otimizado para produção.
Suporta múltiplos backends e estratégias de invalidação.
"""

import time
import hashlib
import json
import pickle
from pathlib import Path
from typing import Any, Optional, Dict, Callable
from functools import wraps
from threading import Lock
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Gerenciador de cache com suporte a múltiplas estratégias.
    Otimizado para Mac Studio M3 Ultra com 96GB RAM.
    """

    def __init__(self, cache_dir: Optional[Path] = None,
                 max_memory_items: int = 10000,
                 ttl_seconds: int = 3600):
        """
        Inicializa o cache manager.

        Args:
            cache_dir: Diretório para cache em disco
            max_memory_items: Máximo de itens em memória
            ttl_seconds: Time-to-live padrão em segundos
        """
        self.cache_dir = cache_dir or Path.home() / '.scripturemon_cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Cache em memória (aproveitando os 96GB)
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        self.max_memory_items = max_memory_items
        self.ttl_seconds = ttl_seconds

        # Lock para thread safety
        self.lock = Lock()

        # Estatísticas
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'disk_hits': 0,
            'disk_misses': 0
        }

        logger.info(f"CacheManager initialized with dir={cache_dir}, max_items={max_memory_items}")

    def _generate_key(self, *args, **kwargs) -> str:
        """Gera chave única baseada nos argumentos."""
        key_data = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()

    def _is_expired(self, timestamp: float, ttl: Optional[int] = None) -> bool:
        """Verifica se um item expirou."""
        ttl = ttl or self.ttl_seconds
        return time.time() - timestamp > ttl

    def get(self, key: str) -> Optional[Any]:
        """
        Busca item no cache.

        Args:
            key: Chave do cache

        Returns:
            Valor cached ou None
        """
        with self.lock:
            # Primeiro tenta memória
            if key in self.memory_cache:
                entry = self.memory_cache[key]
                if not self._is_expired(entry['timestamp']):
                    self.stats['hits'] += 1
                    # Atualiza LRU
                    entry['last_access'] = time.time()
                    return entry['value']
                else:
                    # Remove item expirado
                    del self.memory_cache[key]

            # Depois tenta disco
            disk_path = self.cache_dir / f"{key}.pkl"
            if disk_path.exists():
                try:
                    with open(disk_path, 'rb') as f:
                        entry = pickle.load(f)

                    if not self._is_expired(entry['timestamp']):
                        self.stats['disk_hits'] += 1
                        # Promove para memória se houver espaço
                        if len(self.memory_cache) < self.max_memory_items:
                            entry['last_access'] = time.time()
                            self.memory_cache[key] = entry
                        return entry['value']
                    else:
                        # Remove arquivo expirado
                        disk_path.unlink()
                except Exception as e:
                    logger.warning(f"Failed to load cache from disk: {e}")

            self.stats['misses'] += 1
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Armazena item no cache.

        Args:
            key: Chave do cache
            value: Valor a armazenar
            ttl: Time-to-live opcional
        """
        with self.lock:
            entry = {
                'value': value,
                'timestamp': time.time(),
                'last_access': time.time(),
                'ttl': ttl or self.ttl_seconds
            }

            # Eviction se necessário
            if len(self.memory_cache) >= self.max_memory_items:
                self._evict_lru()

            # Armazena em memória
            self.memory_cache[key] = entry

            # Também persiste em disco para itens importantes
            if ttl and ttl > 3600:  # Persiste itens com TTL > 1 hora
                try:
                    disk_path = self.cache_dir / f"{key}.pkl"
                    with open(disk_path, 'wb') as f:
                        pickle.dump(entry, f)
                except Exception as e:
                    logger.warning(f"Failed to persist cache to disk: {e}")

    def _evict_lru(self) -> None:
        """Evict least recently used item."""
        if not self.memory_cache:
            return

        # Encontra item menos recentemente usado
        lru_key = min(self.memory_cache.keys(),
                     key=lambda k: self.memory_cache[k]['last_access'])

        del self.memory_cache[lru_key]
        self.stats['evictions'] += 1

        # Remove do disco também se existir
        disk_path = self.cache_dir / f"{lru_key}.pkl"
        if disk_path.exists():
            disk_path.unlink()

    def invalidate(self, key: str) -> None:
        """Invalida um item específico do cache."""
        with self.lock:
            if key in self.memory_cache:
                del self.memory_cache[key]

            disk_path = self.cache_dir / f"{key}.pkl"
            if disk_path.exists():
                disk_path.unlink()

    def clear(self) -> None:
        """Limpa todo o cache."""
        with self.lock:
            self.memory_cache.clear()

            # Remove todos os arquivos de cache
            for cache_file in self.cache_dir.glob("*.pkl"):
                cache_file.unlink()

            logger.info("Cache cleared")

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache."""
        with self.lock:
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = self.stats['hits'] / total_requests if total_requests > 0 else 0

            return {
                **self.stats,
                'memory_items': len(self.memory_cache),
                'hit_rate': f"{hit_rate * 100:.2f}%",
                'disk_files': len(list(self.cache_dir.glob("*.pkl")))
            }

    def cached(self, ttl: Optional[int] = None):
        """
        Decorator para cachear resultados de funções.

        Args:
            ttl: Time-to-live opcional

        Usage:
            @cache_manager.cached(ttl=3600)
            def expensive_function(param1, param2):
                return compute_result()
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Gera chave baseada na função e argumentos
                cache_key = f"{func.__module__}.{func.__name__}_{self._generate_key(*args, **kwargs)}"

                # Tenta buscar do cache
                cached_value = self.get(cache_key)
                if cached_value is not None:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return cached_value

                # Computa e armazena
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)

                return result

            return wrapper
        return decorator


class ModelCache:
    """
    Cache especializado para modelos Ollama.
    Mantém modelos carregados em memória para acesso rápido.
    """

    def __init__(self, max_models: int = 4):
        """
        Inicializa cache de modelos.

        Args:
            max_models: Máximo de modelos em memória (4 é ideal para 96GB)
        """
        self.max_models = max_models
        self.loaded_models: Dict[str, Dict[str, Any]] = {}
        self.lock = Lock()
        self.access_count: Dict[str, int] = {}

        logger.info(f"ModelCache initialized for {max_models} models")

    def get_model(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Retorna modelo do cache se disponível."""
        with self.lock:
            if model_name in self.loaded_models:
                self.access_count[model_name] = self.access_count.get(model_name, 0) + 1
                return self.loaded_models[model_name]
            return None

    def cache_model(self, model_name: str, model_data: Dict[str, Any]) -> None:
        """Armazena modelo no cache."""
        with self.lock:
            # Evict se necessário
            if len(self.loaded_models) >= self.max_models:
                # Remove modelo menos usado
                lfu_model = min(self.loaded_models.keys(),
                              key=lambda k: self.access_count.get(k, 0))
                del self.loaded_models[lfu_model]
                logger.info(f"Evicted model {lfu_model} from cache")

            self.loaded_models[model_name] = model_data
            self.access_count[model_name] = 1
            logger.info(f"Cached model {model_name}")

    def clear(self) -> None:
        """Limpa cache de modelos."""
        with self.lock:
            self.loaded_models.clear()
            self.access_count.clear()
            logger.info("Model cache cleared")


# Singleton global
_cache_manager: Optional[CacheManager] = None
_model_cache: Optional[ModelCache] = None


def get_cache_manager() -> CacheManager:
    """Retorna instância singleton do cache manager."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def get_model_cache() -> ModelCache:
    """Retorna instância singleton do model cache."""
    global _model_cache
    if _model_cache is None:
        _model_cache = ModelCache()
    return _model_cache