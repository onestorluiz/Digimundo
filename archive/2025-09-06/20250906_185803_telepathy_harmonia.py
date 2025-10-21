#!/usr/bin/env python3
"""
TELEPATIA REDIS RITUAL - HARMONIA V3.2
Sistema completo de telepathy com healthcheck e throughput
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import threading
import queue

# Setup paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("harmonia.telepathy")


class TelepathyRitual:
    """Sistema ritual de telepatia Redis."""
    
    def __init__(self):
        self.redis_client = None
        self.redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
        self.degraded_mode = False
        self.stats = {
            'healthcheck': {},
            'pubsub': {},
            'fallback': {}
        }
        
    def connect(self) -> bool:
        """Conecta ao Redis com fallback para modo degradado."""
        try:
            import redis
            from urllib.parse import urlparse
            
            # Parse Redis URL
            parsed = urlparse(self.redis_url)
            host = parsed.hostname or 'localhost'
            port = parsed.port or 6379
            db = int(parsed.path[1:]) if parsed.path and len(parsed.path) > 1 else 0
            
            # Conectar
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2
            )
            
            # Test connection
            self.redis_client.ping()
            logger.info(f"✅ Conectado ao Redis: {host}:{port}/{db}")
            return True
            
        except ImportError:
            logger.warning("❌ redis-py não instalado - entrando em modo degradado")
            self.degraded_mode = True
            self.stats['fallback']['reason'] = "redis-py not installed"
            return False
            
        except Exception as e:
            logger.warning(f"❌ Falha ao conectar ao Redis: {e} - entrando em modo degradado")
            self.degraded_mode = True
            self.stats['fallback']['reason'] = str(e)
            return False
    
    def healthcheck(self) -> Dict[str, Any]:
        """Executa healthcheck completo do Redis."""
        health = {
            'timestamp': datetime.now().isoformat(),
            'redis_url': self.redis_url,
            'connected': False,
            'degraded_mode': self.degraded_mode,
            'latencies_ms': {}
        }
        
        if self.degraded_mode:
            health['fallback'] = {
                'mode': 'in-memory queue',
                'reason': self.stats['fallback'].get('reason', 'connection failed'),
                'capabilities': [
                    'local message passing',
                    'no persistence',
                    'no distributed pub/sub'
                ]
            }
            return health
        
        try:
            # PING latency
            ping_times = []
            for _ in range(10):
                start = time.perf_counter()
                self.redis_client.ping()
                ping_times.append((time.perf_counter() - start) * 1000)
            
            health['latencies_ms']['ping'] = {
                'avg_ms': sum(ping_times) / len(ping_times),
                'min_ms': min(ping_times),
                'max_ms': max(ping_times),
                'p95': sorted(ping_times)[int(len(ping_times) * 0.95)]
            }
            
            # SET latency
            set_times = []
            for i in range(10):
                key = f"healthcheck:test:{i}"
                value = f"value_{i}_{time.time()}"
                start = time.perf_counter()
                self.redis_client.set(key, value, ex=10)
                set_times.append((time.perf_counter() - start) * 1000)
            
            health['latencies_ms']['set'] = {
                'avg_ms': sum(set_times) / len(set_times),
                'min_ms': min(set_times),
                'max_ms': max(set_times),
                'p95': sorted(set_times)[int(len(set_times) * 0.95)]
            }
            
            # GET latency
            get_times = []
            for i in range(10):
                key = f"healthcheck:test:{i}"
                start = time.perf_counter()
                self.redis_client.get(key)
                get_times.append((time.perf_counter() - start) * 1000)
            
            health['latencies_ms']['get'] = {
                'avg_ms': sum(get_times) / len(get_times),
                'min_ms': min(get_times),
                'max_ms': max(get_times),
                'p95': sorted(get_times)[int(len(get_times) * 0.95)]
            }
            
            # Info adicional
            info = self.redis_client.info()
            health['server_info'] = {
                'version': info.get('redis_version', 'unknown'),
                'used_memory_mb': info.get('used_memory', 0) / (1024 * 1024),
                'connected_clients': info.get('connected_clients', 0),
                'total_commands_processed': info.get('total_commands_processed', 0)
            }
            
            health['connected'] = True
            
            # Cleanup
            for i in range(10):
                self.redis_client.delete(f"healthcheck:test:{i}")
            
        except Exception as e:
            health['error'] = str(e)
            logger.error(f"Erro no healthcheck: {e}")
        
        return health
    
    def pubsub_throughput_test(self, num_messages: int = 1000) -> Dict[str, Any]:
        """Testa throughput do pub/sub com múltiplas mensagens."""
        result = {
            'timestamp': datetime.now().isoformat(),
            'num_messages': num_messages,
            'degraded_mode': self.degraded_mode,
            'metrics': {}
        }
        
        if self.degraded_mode:
            # Modo degradado: usar queue local
            result['fallback'] = {
                'mode': 'local queue simulation',
                'note': 'Using threading.Queue for local pub/sub simulation'
            }
            
            # Simular com queue local
            local_queue = queue.Queue()
            latencies = []
            
            # Publisher thread
            def publisher():
                for i in range(num_messages):
                    msg = {
                        'id': i,
                        'timestamp': time.perf_counter(),
                        'data': f'message_{i}'
                    }
                    local_queue.put(msg)
            
            # Subscriber
            received = []
            def subscriber():
                while len(received) < num_messages:
                    try:
                        msg = local_queue.get(timeout=1)
                        recv_time = time.perf_counter()
                        latency = (recv_time - msg['timestamp']) * 1000
                        latencies.append(latency)
                        received.append(msg)
                    except queue.Empty:
                        break
            
            # Executar teste
            start_time = time.perf_counter()
            
            pub_thread = threading.Thread(target=publisher)
            sub_thread = threading.Thread(target=subscriber)
            
            sub_thread.start()
            time.sleep(0.1)  # Dar tempo para subscriber iniciar
            pub_thread.start()
            
            pub_thread.join()
            sub_thread.join()
            
            total_time = time.perf_counter() - start_time
            
            if latencies:
                sorted_latencies = sorted(latencies)
                result['metrics'] = {
                    'messages_sent': num_messages,
                    'messages_received': len(received),
                    'total_time_s': total_time,
                    'msgs_per_second': len(received) / total_time if total_time > 0 else 0,
                    'latency_ms': {
                        'avg_ms': sum(latencies) / len(latencies),
                        'min_ms': min(latencies),
                        'max_ms': max(latencies),
                        'p50': sorted_latencies[int(len(latencies) * 0.50)],
                        'p95': sorted_latencies[int(len(latencies) * 0.95)],
                        'p99': sorted_latencies[int(len(latencies) * 0.99)]
                    }
                }
            
            return result
        
        try:
            # Modo normal: usar Redis pub/sub
            channel = 'telepathy:throughput:test'
            pubsub = self.redis_client.pubsub()
            pubsub.subscribe(channel)
            
            # Limpar mensagens iniciais
            pubsub.get_message(timeout=0.1)
            
            latencies = []
            received_count = 0
            
            # Thread para receber mensagens
            def receiver():
                nonlocal received_count
                while received_count < num_messages:
                    msg = pubsub.get_message(timeout=1)
                    if msg and msg['type'] == 'message':
                        data = json.loads(msg['data'])
                        recv_time = time.perf_counter()
                        send_time = data['timestamp']
                        latency = (recv_time - send_time) * 1000
                        latencies.append(latency)
                        received_count += 1
            
            # Iniciar receiver
            receiver_thread = threading.Thread(target=receiver)
            receiver_thread.start()
            
            # Dar tempo para subscriber estar pronto
            time.sleep(0.1)
            
            # Enviar mensagens
            start_time = time.perf_counter()
            
            for i in range(num_messages):
                message = {
                    'id': i,
                    'timestamp': time.perf_counter(),
                    'data': f'telepathy_message_{i}',
                    'source': 'harmonia_v32'
                }
                self.redis_client.publish(channel, json.dumps(message))
                
                # Pequeno delay para não sobrecarregar
                if i % 100 == 0:
                    time.sleep(0.001)
            
            # Aguardar recepção
            receiver_thread.join(timeout=5)
            
            total_time = time.perf_counter() - start_time
            
            # Calcular métricas
            if latencies:
                sorted_latencies = sorted(latencies)
                result['metrics'] = {
                    'messages_sent': num_messages,
                    'messages_received': received_count,
                    'total_time_s': total_time,
                    'msgs_per_second': received_count / total_time if total_time > 0 else 0,
                    'latency_ms': {
                        'avg_ms': sum(latencies) / len(latencies),
                        'min_ms': min(latencies),
                        'max_ms': max(latencies),
                        'p50': sorted_latencies[int(len(latencies) * 0.50)],
                        'p95': sorted_latencies[int(len(latencies) * 0.95)],
                        'p99': sorted_latencies[min(int(len(latencies) * 0.99), len(latencies)-1)]
                    },
                    'channel': channel
                }
            
            # Cleanup
            pubsub.unsubscribe(channel)
            pubsub.close()
            
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Erro no teste de throughput: {e}")
        
        return result
    
    def generate_fallback_docs(self) -> Dict[str, Any]:
        """Gera documentação do modo degradado."""
        docs = {
            'timestamp': datetime.now().isoformat(),
            'fallback_modes': {
                'redis_unavailable': {
                    'trigger': 'Redis connection failed or redis-py not installed',
                    'behavior': 'Use in-memory queue for local message passing',
                    'limitations': [
                        'No persistence across restarts',
                        'No distributed pub/sub',
                        'Limited to single process',
                        'No atomic operations'
                    ],
                    'api_compatibility': {
                        'publish': 'Routes to local queue.put()',
                        'subscribe': 'Creates local queue listener',
                        'get/set': 'Uses dict in memory'
                    }
                },
                'performance_degradation': {
                    'trigger': 'Redis latency > 100ms',
                    'behavior': 'Batch operations and async processing',
                    'optimizations': [
                        'Batch writes every 100ms',
                        'Local cache for reads',
                        'Async pub/sub with acknowledgments'
                    ]
                }
            },
            'recovery_strategy': {
                'detection': 'Health check every 30s',
                'reconnection': 'Exponential backoff 1s -> 2s -> 4s -> 8s',
                'data_sync': 'Queue messages locally, flush on reconnect'
            },
            'usage_example': {
                'code': """
# Auto-detects and handles fallback
from src.telepathy import TelepathyNetwork

network = TelepathyNetwork()
if network.degraded_mode:
    print("Running in degraded mode - using local queue")
    
# API remains the same
network.broadcast("evolution", {"level": 2})
messages = network.receive("evolution", timeout=1)
                """,
                'env_var': 'REDIS_URL=redis://localhost:6379/0'
            }
        }
        
        return docs


def main():
    """Executa ritual completo de telepatia."""
    
    # Inicializar
    ritual = TelepathyRitual()
    
    # Conectar
    connected = ritual.connect()
    
    # Executar healthcheck
    health = ritual.healthcheck()
    
    # Executar teste de throughput
    throughput = ritual.pubsub_throughput_test(1000)
    
    # Gerar documentação de fallback
    fallback_docs = ritual.generate_fallback_docs()
    
    # Salvar relatórios
    output_dir = Path("reports/harmonia_v32/telepathy")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Redis health
    with open(output_dir / "redis_health.json", 'w') as f:
        json.dump(health, f, indent=2)
    
    # Throughput
    with open(output_dir / "pubsub_throughput.json", 'w') as f:
        json.dump(throughput, f, indent=2)
    
    # Fallback documentation
    with open(output_dir / "fallback_strategy.json", 'w') as f:
        json.dump(fallback_docs, f, indent=2)
    
    # Log resumo
    if connected:
        logger.info(f"✅ Telepatia ativa! Latência média: {health['latencies_ms']['ping']['avg_ms']:.2f}ms")
        logger.info(f"✅ Throughput: {throughput['metrics']['msgs_per_second']:.0f} msgs/s")
    else:
        logger.info(f"⚠️ Modo degradado ativo - usando fallback local")
        if throughput.get('metrics'):
            logger.info(f"✅ Throughput local: {throughput['metrics']['msgs_per_second']:.0f} msgs/s")
    
    return {
        'connected': connected,
        'degraded_mode': ritual.degraded_mode,
        'health': health,
        'throughput': throughput
    }


if __name__ == "__main__":
    main()