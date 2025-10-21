"""
Helper para conexão Redis com retry e fallback
"""

import time
import redis
from typing import Optional

_redis_instance: Optional[redis.Redis] = None

def get_redis_connection(force_new=False):
    """
    Obtém conexão Redis com retry e fallback para FakeRedis
    Usa singleton pattern para reutilizar conexão
    """
    global _redis_instance
    
    if _redis_instance and not force_new:
        try:
            _redis_instance.ping()
            return _redis_instance
        except:
            _redis_instance = None
    
    # Tenta conectar com retry
    for attempt in range(5):
        try:
            r = redis.Redis(
                host="127.0.0.1",
                port=6379,
                socket_connect_timeout=0.5,
                decode_responses=True
            )
            r.ping()
            _redis_instance = r
            return r
        except Exception:
            if attempt < 4:
                time.sleep(1.5)
    
    # Fallback para FakeRedis
    try:
        import fakeredis
        _redis_instance = fakeredis.FakeRedis(decode_responses=True)
        return _redis_instance
    except ImportError:
        # Se não tem fakeredis, retorna None e deixa o código lidar
        return None