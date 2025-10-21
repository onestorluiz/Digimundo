#!/usr/bin/env python3
"""
Redis Cache - Cache distribuído com Redis
Fase 3.B - Integração com Redis para cache compartilhado
"""

import json
import pickle
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Tentativa de importar redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not installed. Using memory-only cache.")

class RedisCache:
    """Cache distribuído usando Redis"""
    
    def __init__(self,
                 host: str = "localhost",
                 port: int = 6379,
                 db: int = 0,
                 password: Optional[str] = None,
                 decode_responses: bool = False,
                 fallback_to_memory: bool = True):
        """
        Inicializa conexão com Redis
        
        Args:
            host: Host do Redis
            port: Porta do Redis
            db: Número do database
            password: Senha se necessário
            decode_responses: Se deve decodificar respostas
            fallback_to_memory: Se deve usar cache em memória como fallback
        """
        self.fallback_to_memory = fallback_to_memory
        self._memory_cache: Dict[str, Any] = {}
        self._redis_client = None
        self._connected = False
        
        if REDIS_AVAILABLE:
            try:
                self._redis_client = redis.Redis(
                    host=host,
                    port=port,
                    db=db,
                    password=password,
                    decode_responses=decode_responses,
                    socket_connect_timeout=2,
                    socket_timeout=2
                )
                
                # Testa conexão
                self._redis_client.ping()
                self._connected = True
                logger.info(f"Connected to Redis at {host}:{port}")
                
            except (redis.ConnectionError, redis.TimeoutError) as e:
                logger.warning(f"Failed to connect to Redis: {e}")
                self._connected = False
                
                if not fallback_to_memory:
                    raise
        else:
            logger.info("Redis not available, using memory cache")
            self._connected = False
    
    def is_connected(self) -> bool:
        """Verifica se está conectado ao Redis"""
        if not self._redis_client:
            return False
        
        try:
            self._redis_client.ping()
            return True
        except:
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Recupera valor do cache
        
        Args:
            key: Chave do item
            
        Returns:
            Valor se encontrado, None caso contrário
        """
        if self._connected:
            try:
                value = self._redis_client.get(key)
                if value:
                    # Tenta despickle primeiro (objetos complexos)
                    try:
                        return pickle.loads(value)
                    except:
                        # Se falhar, tenta JSON
                        try:
                            return json.loads(value)
                        except:
                            # Se ainda falhar, retorna como string
                            return value.decode() if isinstance(value, bytes) else value
                return None
                
            except Exception as e:
                logger.error(f"Redis get error: {e}")
                if self.fallback_to_memory:
                    return self._memory_cache.get(key)
                raise
        else:
            # Usa cache em memória
            return self._memory_cache.get(key)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = 3600) -> bool:
        """
        Armazena valor no cache
        
        Args:
            key: Chave do item
            value: Valor a armazenar
            ttl: Time to live em segundos
            
        Returns:
            True se armazenou com sucesso
        """
        if self._connected:
            try:
                # Serializa valor
                if isinstance(value, (str, int, float)):
                    serialized = str(value)
                elif isinstance(value, (dict, list)):
                    serialized = json.dumps(value)
                else:
                    serialized = pickle.dumps(value)
                
                # Armazena com TTL
                if ttl:
                    self._redis_client.setex(key, ttl, serialized)
                else:
                    self._redis_client.set(key, serialized)
                
                return True
                
            except Exception as e:
                logger.error(f"Redis set error: {e}")
                if self.fallback_to_memory:
                    self._memory_cache[key] = value
                    return True
                raise
        else:
            # Usa cache em memória
            self._memory_cache[key] = value
            return True
    
    def delete(self, key: str) -> bool:
        """
        Remove item do cache
        
        Args:
            key: Chave do item
            
        Returns:
            True se removeu com sucesso
        """
        if self._connected:
            try:
                self._redis_client.delete(key)
                return True
            except Exception as e:
                logger.error(f"Redis delete error: {e}")
                if self.fallback_to_memory and key in self._memory_cache:
                    del self._memory_cache[key]
                    return True
                raise
        else:
            if key in self._memory_cache:
                del self._memory_cache[key]
                return True
            return False
    
    def exists(self, key: str) -> bool:
        """
        Verifica se chave existe
        
        Args:
            key: Chave a verificar
            
        Returns:
            True se existe
        """
        if self._connected:
            try:
                return bool(self._redis_client.exists(key))
            except Exception as e:
                logger.error(f"Redis exists error: {e}")
                if self.fallback_to_memory:
                    return key in self._memory_cache
                raise
        else:
            return key in self._memory_cache
    
    def keys(self, pattern: str = "*") -> List[str]:
        """
        Lista chaves que correspondem ao padrão
        
        Args:
            pattern: Padrão de busca (ex: "analysis:*")
            
        Returns:
            Lista de chaves
        """
        if self._connected:
            try:
                keys = self._redis_client.keys(pattern)
                return [k.decode() if isinstance(k, bytes) else k for k in keys]
            except Exception as e:
                logger.error(f"Redis keys error: {e}")
                if self.fallback_to_memory:
                    # Simula pattern matching simples
                    if pattern == "*":
                        return list(self._memory_cache.keys())
                    # Pattern básico (apenas prefixo)
                    prefix = pattern.rstrip("*")
                    return [k for k in self._memory_cache.keys() if k.startswith(prefix)]
                raise
        else:
            if pattern == "*":
                return list(self._memory_cache.keys())
            prefix = pattern.rstrip("*")
            return [k for k in self._memory_cache.keys() if k.startswith(prefix)]
    
    def expire(self, key: str, seconds: int) -> bool:
        """
        Define TTL para chave existente
        
        Args:
            key: Chave do item
            seconds: TTL em segundos
            
        Returns:
            True se definiu TTL com sucesso
        """
        if self._connected:
            try:
                return bool(self._redis_client.expire(key, seconds))
            except Exception as e:
                logger.error(f"Redis expire error: {e}")
                return False
        return False
    
    def ttl(self, key: str) -> int:
        """
        Retorna TTL restante de uma chave
        
        Args:
            key: Chave do item
            
        Returns:
            TTL em segundos, -1 se sem TTL, -2 se não existe
        """
        if self._connected:
            try:
                return self._redis_client.ttl(key)
            except Exception as e:
                logger.error(f"Redis ttl error: {e}")
                return -2
        return -2 if key not in self._memory_cache else -1
    
    def clear(self, pattern: str = None) -> int:
        """
        Limpa cache
        
        Args:
            pattern: Padrão de chaves a limpar (None = todas)
            
        Returns:
            Número de chaves removidas
        """
        count = 0
        
        if self._connected:
            try:
                if pattern:
                    keys = self._redis_client.keys(pattern)
                    if keys:
                        count = self._redis_client.delete(*keys)
                else:
                    self._redis_client.flushdb()
                    count = -1  # Indica limpeza total
                    
            except Exception as e:
                logger.error(f"Redis clear error: {e}")
                if self.fallback_to_memory:
                    if pattern:
                        prefix = pattern.rstrip("*")
                        keys_to_delete = [k for k in self._memory_cache.keys() 
                                        if k.startswith(prefix)]
                        for k in keys_to_delete:
                            del self._memory_cache[k]
                            count += 1
                    else:
                        count = len(self._memory_cache)
                        self._memory_cache.clear()
        else:
            if pattern:
                prefix = pattern.rstrip("*")
                keys_to_delete = [k for k in self._memory_cache.keys() 
                                if k.startswith(prefix)]
                for k in keys_to_delete:
                    del self._memory_cache[k]
                    count += 1
            else:
                count = len(self._memory_cache)
                self._memory_cache.clear()
        
        return count
    
    def info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre o cache
        
        Returns:
            Dicionário com informações
        """
        info = {
            "backend": "redis" if self._connected else "memory",
            "connected": self._connected,
            "fallback_enabled": self.fallback_to_memory
        }
        
        if self._connected:
            try:
                redis_info = self._redis_client.info()
                info.update({
                    "version": redis_info.get("redis_version", "unknown"),
                    "used_memory": redis_info.get("used_memory_human", "unknown"),
                    "connected_clients": redis_info.get("connected_clients", 0),
                    "total_keys": self._redis_client.dbsize()
                })
            except Exception as e:
                logger.error(f"Redis info error: {e}")
        else:
            info.update({
                "memory_cache_size": len(self._memory_cache)
            })
        
        return info
    
    def health_check(self) -> Dict[str, Any]:
        """
        Verifica saúde do cache
        
        Returns:
            Status de saúde
        """
        health = {
            "status": "healthy",
            "backend": "redis" if self._connected else "memory",
            "details": {}
        }
        
        if REDIS_AVAILABLE and self._redis_client:
            try:
                # Testa operações básicas
                test_key = f"health_check_{datetime.now().timestamp()}"
                test_value = "test"
                
                # Set
                self.set(test_key, test_value, ttl=10)
                
                # Get
                retrieved = self.get(test_key)
                if retrieved != test_value:
                    health["status"] = "degraded"
                    health["details"]["read_write"] = "failed"
                
                # Delete
                self.delete(test_key)
                
                health["details"]["redis"] = "operational"
                
            except Exception as e:
                health["status"] = "unhealthy" if not self.fallback_to_memory else "degraded"
                health["details"]["error"] = str(e)
        else:
            health["details"]["redis"] = "not available"
            if self.fallback_to_memory:
                health["details"]["fallback"] = "using memory cache"
            else:
                health["status"] = "unhealthy"
        
        return health

# Singleton para uso global
_redis_cache: Optional[RedisCache] = None

def get_redis_cache() -> RedisCache:
    """
    Retorna instância singleton do RedisCache
    
    Returns:
        RedisCache configurado
    """
    global _redis_cache
    if _redis_cache is None:
        _redis_cache = RedisCache(
            host="localhost",
            port=6379,
            db=0,
            fallback_to_memory=True
        )
    return _redis_cache

# Funções de conveniência
def redis_get(key: str) -> Optional[Any]:
    """Atalho para buscar no Redis"""
    cache = get_redis_cache()
    return cache.get(key)

def redis_set(key: str, value: Any, ttl: int = 3600) -> bool:
    """Atalho para armazenar no Redis"""
    cache = get_redis_cache()
    return cache.set(key, value, ttl)

def redis_health() -> Dict[str, Any]:
    """Atalho para verificar saúde do Redis"""
    cache = get_redis_cache()
    return cache.health_check()

__all__ = [
    "RedisCache",
    "get_redis_cache",
    "redis_get",
    "redis_set",
    "redis_health",
    "REDIS_AVAILABLE"
]