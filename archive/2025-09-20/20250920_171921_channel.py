"""
Telepathy Channel - Comunicação com Redis com fallback para fakeredis.
Garante operação mesmo sem Redis real disponível.
"""

import time
import logging
from typing import Optional, Dict, Any, Union
from datetime import datetime

# Configurar logger
logger = logging.getLogger(__name__)


def get_client(settings: Optional[Dict] = None) -> Any:
    """
    Obtém cliente Redis, com fallback para fakeredis se necessário.
    
    Args:
        settings: Configurações com redis.url e redis.timeout_sec
        
    Returns:
        Cliente Redis (real ou fake)
    """
    if not settings:
        settings = {}
    
    redis_config = settings.get('redis', {})
    redis_url = redis_config.get('url', 'redis://localhost:6379/0')
    timeout_sec = redis_config.get('timeout_sec', 0.5)
    redis_enabled = redis_config.get('enabled', True)
    
    # Se Redis desabilitado nas configurações, usar fakeredis direto
    if not redis_enabled:
        logger.info("Redis desabilitado nas configurações. Usando fakeredis.")
        return _get_fakeredis_client()
    
    # Tentar conectar ao Redis real
    try:
        import redis
        
        # Parse URL para obter host, port, db
        if redis_url.startswith('redis://'):
            # redis://localhost:6379/0
            parts = redis_url.replace('redis://', '').split('/')
            host_port = parts[0].split(':')
            host = host_port[0]
            port = int(host_port[1]) if len(host_port) > 1 else 6379
            db = int(parts[1]) if len(parts) > 1 else 0
        else:
            host, port, db = 'localhost', 6379, 0
        
        # Criar cliente com timeout
        client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
            socket_connect_timeout=timeout_sec,
            socket_timeout=timeout_sec
        )
        
        # Testar conexão com ping
        client.ping()
        
        logger.info(f"✅ Conectado ao Redis real em {host}:{port}/{db}")
        client._is_fake = False
        return client
        
    except ImportError:
        logger.warning("Redis não instalado. Usando fakeredis.")
        return _get_fakeredis_client()
        
    except Exception as e:
        logger.warning(f"Falha ao conectar ao Redis real: {e}. Usando fakeredis.")
        return _get_fakeredis_client()


def _get_fakeredis_client() -> Any:
    """
    Obtém cliente fakeredis para operação offline.
    
    Returns:
        Cliente fakeredis
    """
    try:
        import fakeredis
        
        client = fakeredis.FakeRedis(decode_responses=True)
        client._is_fake = True
        
        logger.info("📦 Usando fakeredis (modo offline)")
        return client
        
    except ImportError:
        # Se nem fakeredis estiver disponível, criar mock mínimo
        logger.error("fakeredis não instalado. Criando mock mínimo.")
        
        class MinimalRedisMock:
            """Mock mínimo para operação sem Redis."""
            
            def __init__(self):
                self._data = {}
                self._is_fake = True
                logger.info("🔌 Usando mock mínimo de Redis")
            
            def ping(self):
                return True
            
            def get(self, key):
                return self._data.get(key)
            
            def set(self, key, value, ex=None):
                self._data[key] = value
                return True
            
            def delete(self, *keys):
                for key in keys:
                    self._data.pop(key, None)
                return len(keys)
            
            def exists(self, key):
                return 1 if key in self._data else 0
            
            def keys(self, pattern='*'):
                if pattern == '*':
                    return list(self._data.keys())
                # Implementação simplificada de pattern matching
                import fnmatch
                return [k for k in self._data.keys() if fnmatch.fnmatch(k, pattern)]
            
            def hset(self, name, key, value):
                if name not in self._data:
                    self._data[name] = {}
                self._data[name][key] = value
                return 1
            
            def hget(self, name, key):
                if name in self._data and isinstance(self._data[name], dict):
                    return self._data[name].get(key)
                return None
            
            def hgetall(self, name):
                if name in self._data and isinstance(self._data[name], dict):
                    return self._data[name]
                return {}
            
            def lpush(self, name, *values):
                if name not in self._data:
                    self._data[name] = []
                for value in values:
                    self._data[name].insert(0, value)
                return len(self._data[name])
            
            def lrange(self, name, start, end):
                if name in self._data and isinstance(self._data[name], list):
                    if end == -1:
                        return self._data[name][start:]
                    return self._data[name][start:end+1]
                return []
            
            def dbsize(self):
                return len(self._data)
            
            def flushdb(self):
                self._data.clear()
                return True
        
        return MinimalRedisMock()


def healthcheck(client: Any, timeout: Optional[float] = None) -> Dict[str, Any]:
    """
    Realiza healthcheck no cliente Redis.
    
    Args:
        client: Cliente Redis (real, fake ou mock)
        timeout: Timeout em segundos (usa settings se não fornecido)
        
    Returns:
        Dict com status e métricas
    """
    start_time = time.time()
    
    result = {
        'timestamp': datetime.now().isoformat(),
        'status': 'unknown',
        'is_fake': getattr(client, '_is_fake', False),
        'latency_ms': 0,
        'metrics': {}
    }
    
    try:
        # Testar ping (com timeout se aplicável)
        if timeout and hasattr(client, 'ping'):
            # Para Redis real, o timeout já foi configurado no cliente
            ping_result = client.ping()
        else:
            ping_result = client.ping() if hasattr(client, 'ping') else True
        
        if not ping_result:
            result['status'] = 'unhealthy'
            result['error'] = 'Ping failed'
            return result
        
        # Coletar métricas básicas
        try:
            # Tamanho do banco
            if hasattr(client, 'dbsize'):
                result['metrics']['db_size'] = client.dbsize()
            
            # Info do servidor (apenas Redis real)
            if not getattr(client, '_is_fake', False) and hasattr(client, 'info'):
                info = client.info()
                result['metrics']['used_memory'] = info.get('used_memory_human', 'N/A')
                result['metrics']['connected_clients'] = info.get('connected_clients', 0)
                result['metrics']['version'] = info.get('redis_version', 'unknown')
            
            # Teste de escrita/leitura
            test_key = f'healthcheck_{int(time.time())}'
            test_value = 'OK'
            
            client.set(test_key, test_value, ex=1)  # Expira em 1 segundo
            read_value = client.get(test_key)
            client.delete(test_key)
            
            if read_value != test_value:
                result['status'] = 'degraded'
                result['warning'] = 'Read/write test mismatch'
            else:
                result['status'] = 'healthy'
            
        except Exception as e:
            result['status'] = 'degraded'
            result['warning'] = f'Metrics collection failed: {str(e)}'
        
        # Calcular latência
        result['latency_ms'] = round((time.time() - start_time) * 1000, 2)
        
        # Status baseado na latência
        if result['status'] == 'healthy':
            if result['latency_ms'] > 100:
                result['status'] = 'degraded'
                result['warning'] = 'High latency detected'
        
    except Exception as e:
        result['status'] = 'unhealthy'
        result['error'] = str(e)
        result['latency_ms'] = round((time.time() - start_time) * 1000, 2)
    
    return result


def create_channel(settings: Optional[Dict] = None) -> 'TelepathyChannel':
    """
    Cria um canal de telepathy com cliente configurado.
    
    Args:
        settings: Configurações do sistema
        
    Returns:
        TelepathyChannel configurado
    """
    return TelepathyChannel(settings)


class TelepathyChannel:
    """
    Canal de comunicação telepática entre componentes.
    """
    
    def __init__(self, settings: Optional[Dict] = None):
        """
        Inicializa o canal.
        
        Args:
            settings: Configurações do sistema
        """
        self.settings = settings or {}
        self.client = get_client(settings)
        self._subscriptions = {}
        self.timeout_sec = settings.get('redis', {}).get('timeout_sec', 0.5)
    
    def publish(self, channel: str, message: str) -> bool:
        """
        Publica mensagem em um canal.
        
        Args:
            channel: Nome do canal
            message: Mensagem para publicar
            
        Returns:
            True se publicado com sucesso
        """
        try:
            if hasattr(self.client, 'publish'):
                self.client.publish(channel, message)
            else:
                # Mock: apenas registra
                logger.debug(f"Mock publish to {channel}: {message[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Erro ao publicar em {channel}: {e}")
            return False
    
    def subscribe(self, channel: str, callback: callable) -> None:
        """
        Inscreve-se em um canal com callback.
        
        Args:
            channel: Nome do canal
            callback: Função para processar mensagens
        """
        self._subscriptions[channel] = callback
        logger.info(f"Inscrito no canal: {channel}")
    
    def healthcheck(self) -> Dict[str, Any]:
        """
        Método wrapper para healthcheck - compatibilidade com harness.
        
        Returns:
            Dict com status do health check
        """
        # Usar função standalone passando nosso cliente
        return healthcheck(self.client, self.timeout_sec)
    
    def send(self, channel: str, message: Any) -> bool:
        """
        Envia mensagem (alias para publish) - compatibilidade.
        """
        if isinstance(message, dict):
            import json
            message = json.dumps(message)
        return self.publish(channel, message)
    
    def receive(self, channel: str, timeout: Optional[float] = None) -> Optional[Dict]:
        """
        Recebe mensagem de um canal.
        """
        try:
            # Simulação simples - retorna mensagem se foi enviada
            import json
            if hasattr(self.client, 'get'):
                msg = self.client.get(f"msg:{channel}")
                if msg:
                    self.client.delete(f"msg:{channel}")
                    return json.loads(msg) if msg.startswith('{') else {'content': msg}
            return None
        except:
            return None
    
    def get_backend_type(self) -> str:
        """
        Retorna tipo de backend em uso.
        """
        if getattr(self.client, '_is_fake', False):
            if hasattr(self.client, 'FakeRedis'):
                return 'fakeredis'
            return 'mock'
        return 'redis'
    
    def cleanup(self) -> bool:
        """
        Limpa recursos.
        """
        try:
            self._subscriptions.clear()
            return True
        except:
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtém status do canal.
        
        Returns:
            Status e métricas
        """
        health = healthcheck(self.client, self.settings.get('redis', {}).get('timeout_sec'))
        health['subscriptions'] = list(self._subscriptions.keys())
        return health
    
    def close(self):
        """Fecha o canal e libera recursos."""
        if hasattr(self.client, 'close'):
            self.client.close()
        self._subscriptions.clear()
        logger.info("Canal de telepathy fechado")