#!/usr/bin/env python3
"""
Patch para adicionar lógica de retry com fallback para Redis
"""

import time
import redis

def get_redis_with_fallback(timeout=0.5, max_attempts=5, sleep_time=1.5):
    """
    Tenta conectar ao Redis com retry e fallback para FakeRedis
    
    Args:
        timeout: Timeout de conexão em segundos
        max_attempts: Número máximo de tentativas
        sleep_time: Tempo de espera entre tentativas
    
    Returns:
        Redis client (real ou fake)
    """
    for attempt in range(max_attempts):
        try:
            r = redis.Redis(
                host="127.0.0.1", 
                port=6379, 
                socket_connect_timeout=timeout,
                decode_responses=True
            )
            r.ping()
            print(f"✅ Redis conectado na tentativa {attempt + 1}")
            return r
        except Exception as e:
            if attempt < max_attempts - 1:
                print(f"⏳ Redis não disponível, tentativa {attempt + 1}/{max_attempts}...")
                time.sleep(sleep_time)
    
    # Fallback para FakeRedis
    print("⚠️ Redis não disponível após 5 tentativas. Usando FakeRedis (memória local)")
    try:
        import fakeredis
        return fakeredis.FakeRedis(decode_responses=True)
    except ImportError:
        print("❌ FakeRedis não instalado. Instalando...")
        import subprocess
        subprocess.run(["pip", "install", "fakeredis"], check=True)
        import fakeredis
        return fakeredis.FakeRedis(decode_responses=True)


# Função helper para aplicar em classes existentes
def patch_redis_connection(obj, attr_name="redis"):
    """
    Aplica o patch de Redis com fallback em um objeto
    
    Args:
        obj: Objeto que precisa de conexão Redis
        attr_name: Nome do atributo Redis no objeto
    """
    redis_client = get_redis_with_fallback()
    setattr(obj, attr_name, redis_client)
    return redis_client


if __name__ == "__main__":
    # Teste
    print("🔍 Testando conexão Redis com fallback...")
    redis_client = get_redis_with_fallback()
    
    # Teste de operações básicas
    try:
        redis_client.set("test_key", "test_value")
        value = redis_client.get("test_key")
        print(f"✅ Teste OK: {value}")
        
        # Info sobre o tipo de Redis
        if hasattr(redis_client, '__module__'):
            if 'fakeredis' in redis_client.__module__:
                print("📌 Usando FakeRedis (memória local)")
            else:
                print("📌 Usando Redis real")
    except Exception as e:
        print(f"❌ Erro no teste: {e}")