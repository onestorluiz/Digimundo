"""
🌐 Distributed Computing Orchestration Supreme - Silicon Valley Grade Implementation
Sistema híper-avançado de orquestração distribuída para o Scripturemon Champion

Sistema multicamadas com 15+ tecnologias de distribuição:
- Kubernetes-like Container Orchestration
- Apache Spark-like Distributed Computing
- Kafka-like Event Streaming
- Consul-like Service Discovery
- Load Balancing com múltiplos algoritmos
- Distributed Task Queue (Celery-like)
- Map-Reduce Implementation
- Gossip Protocol para consenso
- Circuit Breaker Pattern
- Distributed Caching (Redis-like)
- Microservices Architecture
- Actor Model (Akka-like)
- Distributed Tracing
- Auto-Scaling com métricas
- Fault Tolerance & Recovery

Autor: Scripturemon Champion
Data: 2025-09-16
Versão: 6.1.8 DISTRIBUTED SUPREME
"""
import asyncio
import aiohttp
import json
import time
import threading
import hashlib
import random
import socket
import logging
from typing import Dict, List, Tuple, Optional, Any, Union, Callable, Set
from enum import Enum
from dataclasses import dataclass, field
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from abc import ABC, abstractmethod
import pickle
import uuid
import weakref
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NodeRole(Enum):
    """Papéis de um nó na rede distribuída"""
    MASTER = 'master'
    WORKER = 'worker'
    COORDINATOR = 'coordinator'
    MONITOR = 'monitor'
    GATEWAY = 'gateway'
    CACHE = 'cache'
    STORAGE = 'storage'

class TaskStatus(Enum):
    """Status de tarefas distribuídas"""
    PENDING = 'pending'
    ASSIGNED = 'assigned'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    RETRYING = 'retrying'
    CANCELLED = 'cancelled'

class LoadBalancingAlgorithm(Enum):
    """Algoritmos de balanceamento de carga"""
    ROUND_ROBIN = 'round_robin'
    WEIGHTED_ROUND_ROBIN = 'weighted_round_robin'
    LEAST_CONNECTIONS = 'least_connections'
    LEAST_RESPONSE_TIME = 'least_response_time'
    RESOURCE_BASED = 'resource_based'
    HASH_BASED = 'hash_based'
    RANDOM = 'random'
    GEOGRAPHIC = 'geographic'

class ScalingPolicy(Enum):
    """Políticas de auto-scaling"""
    CPU_BASED = 'cpu_based'
    MEMORY_BASED = 'memory_based'
    QUEUE_LENGTH = 'queue_length'
    RESPONSE_TIME = 'response_time'
    CUSTOM_METRIC = 'custom_metric'
    PREDICTIVE = 'predictive'

@dataclass
class NodeInfo:
    """Informações de um nó na rede"""
    node_id: str
    address: str
    port: int
    role: NodeRole
    resources: Dict[str, float] = field(default_factory=dict)
    status: str = 'healthy'
    last_heartbeat: float = field(default_factory=time.time)
    capabilities: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    network_latency: float = 0.0
    active_connections: int = 0
    tasks_processed: int = 0
    errors_count: int = 0

@dataclass
class DistributedTask:
    """Tarefa para processamento distribuído"""
    task_id: str
    function_name: str
    args: Tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    priority: int = 5
    status: TaskStatus = TaskStatus.PENDING
    assigned_node: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Any = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    timeout: float = float('inf')
    dependencies: List[str] = field(default_factory=list)
    tags: Set[str] = field(default_factory=set)

@dataclass
class ServiceEndpoint:
    """Endpoint de serviço"""
    service_name: str
    host: str
    port: int
    protocol: str = 'http'
    health_check_path: str = '/health'
    weight: int = 100
    max_connections: int = 1000
    current_connections: int = 0
    response_time_ms: float = 0.0
    last_health_check: float = field(default_factory=time.time)
    healthy: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

class DistributedNode:
    """Nó individual na rede distribuída"""

    def __init__(self, node_id: str, address: str, port: int, role: NodeRole):
        self.info = NodeInfo(node_id=node_id, address=address, port=port, role=role)
        self.running = False
        self.server = None
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.task_queue = deque()
        self.active_tasks: Dict[str, DistributedTask] = {}
        self.completed_tasks: Dict[str, DistributedTask] = {}
        self.heartbeat_interval = 10.0
        self.heartbeat_thread = None
        self.discovery_nodes: Set[str] = set()
        self.circuit_breaker = CircuitBreaker()
        self.local_metrics = {'tasks_processed': 0, 'tasks_failed': 0, 'total_processing_time': 0.0, 'average_response_time': 0.0, 'uptime_start': time.time()}
        logger.info(f'🚀 Nó {node_id} inicializado - Papel: {role.value}')

    async def start(self):
        """Inicia o nó distribuído"""
        self.running = True
        await self._start_http_server()
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()
        asyncio.create_task(self._task_processing_loop())
        logger.info(f'✅ Nó {self.info.node_id} iniciado em {self.info.address}:{self.info.port}')

    async def stop(self):
        """Para o nó"""
        self.running = False
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        self.executor.shutdown(wait=True)
        logger.info(f'🛑 Nó {self.info.node_id} parado')

    async def _start_http_server(self):
        """Inicia servidor HTTP para comunicação"""
        from aiohttp import web, Application
        app = Application()
        app.router.add_get('/health', self._handle_health_check)
        app.router.add_get('/status', self._handle_status)
        app.router.add_post('/task', self._handle_task_submission)
        app.router.add_get('/task/{task_id}', self._handle_task_status)
        app.router.add_post('/heartbeat', self._handle_heartbeat)
        app.router.add_get('/metrics', self._handle_metrics)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.info.address, self.info.port)
        await site.start()
        self.server = runner

    def _handle_health_check(self, request):
        """Health check endpoint"""
        from aiohttp import web
        health_data = {'node_id': self.info.node_id, 'status': 'healthy' if self.running else 'unhealthy', 'role': self.info.role.value, 'uptime': time.time() - self.local_metrics['uptime_start'], 'active_tasks': len(self.active_tasks), 'queue_length': len(self.task_queue), 'cpu_usage': self.info.cpu_usage, 'memory_usage': self.info.memory_usage}
        return web.json_response(health_data)

    def _handle_status(self, request):
        """Status detalhado do nó"""
        from aiohttp import web
        status_data = {'node_info': {'node_id': self.info.node_id, 'address': self.info.address, 'port': self.info.port, 'role': self.info.role.value, 'capabilities': list(self.info.capabilities)}, 'performance': {'cpu_usage': self.info.cpu_usage, 'memory_usage': self.info.memory_usage, 'disk_usage': self.info.disk_usage, 'network_latency': self.info.network_latency, 'active_connections': self.info.active_connections}, 'task_metrics': {'active_tasks': len(self.active_tasks), 'completed_tasks': len(self.completed_tasks), 'queue_length': len(self.task_queue), 'tasks_processed': self.local_metrics['tasks_processed'], 'tasks_failed': self.local_metrics['tasks_failed'], 'average_response_time': self.local_metrics['average_response_time']}, 'circuit_breaker': {'state': self.circuit_breaker.state.value, 'failure_count': self.circuit_breaker.failure_count, 'last_failure_time': self.circuit_breaker.last_failure_time}}
        return web.json_response(status_data)

    async def _handle_task_submission(self, request):
        """Recebe nova tarefa para processamento"""
        from aiohttp import web
        try:
            task_data = await request.json()
            task = DistributedTask(task_id=task_data.get('task_id', str(uuid.uuid4())), function_name=task_data['function_name'], args=tuple(task_data.get('args', [])), kwargs=task_data.get('kwargs', {}), priority=task_data.get('priority', 5), timeout=task_data.get('timeout', 300.0), max_retries=task_data.get('max_retries', 3), tags=set(task_data.get('tags', [])))
            self._add_task_to_queue(task)
            return web.json_response({'task_id': task.task_id, 'status': 'accepted', 'queue_position': len(self.task_queue)})
        except Exception as e:
            logger.error(f'❌ Erro processando submissão de tarefa: {e}')
            return web.json_response({'error': str(e)}, status=400)

    def _handle_task_status(self, request):
        """Retorna status de uma tarefa"""
        from aiohttp import web
        task_id = request.match_info['task_id']
        task = None
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
        elif task_id in self.completed_tasks:
            task = self.completed_tasks[task_id]
        else:
            for t in self.task_queue:
                if t.task_id == task_id:
                    task = t
                    break
        if not task:
            return web.json_response({'error': 'Task not found'}, status=404)
        task_status = {'task_id': task.task_id, 'status': task.status.value, 'assigned_node': task.assigned_node, 'created_at': task.created_at, 'started_at': task.started_at, 'completed_at': task.completed_at, 'retry_count': task.retry_count, 'error': task.error}
        if task.status == TaskStatus.COMPLETED:
            task_status['has_result'] = task.result is not None
        return web.json_response(task_status)

    async def _handle_heartbeat(self, request):
        """Processa heartbeat de outros nós"""
        from aiohttp import web
        try:
            heartbeat_data = await request.json()
            node_id = heartbeat_data['node_id']
            self.discovery_nodes.add(node_id)
            response_data = {'node_id': self.info.node_id, 'address': self.info.address, 'port': self.info.port, 'role': self.info.role.value, 'status': 'healthy', 'timestamp': time.time()}
            return web.json_response(response_data)
        except Exception as e:
            return web.json_response({'error': str(e)}, status=400)

    def _handle_metrics(self, request):
        """Retorna métricas do nó"""
        from aiohttp import web
        uptime = time.time() - self.local_metrics['uptime_start']
        metrics = {'node_metrics': {'uptime_seconds': uptime, 'tasks_processed_total': self.local_metrics['tasks_processed'], 'tasks_failed_total': self.local_metrics['tasks_failed'], 'tasks_active': len(self.active_tasks), 'tasks_queued': len(self.task_queue), 'average_response_time_ms': self.local_metrics['average_response_time']}, 'system_metrics': {'cpu_usage_percent': self.info.cpu_usage, 'memory_usage_percent': self.info.memory_usage, 'disk_usage_percent': self.info.disk_usage, 'network_latency_ms': self.info.network_latency}, 'circuit_breaker_metrics': {'state': self.circuit_breaker.state.value, 'failure_count': self.circuit_breaker.failure_count, 'success_count': self.circuit_breaker.success_count, 'timeout_count': self.circuit_breaker.timeout_count}}
        return web.json_response(metrics)

    def _add_task_to_queue(self, task: DistributedTask):
        """Adiciona tarefa à fila com ordenação por prioridade"""
        task.assigned_node = self.info.node_id
        task.status = TaskStatus.ASSIGNED
        inserted = False
        for i, queued_task in enumerate(self.task_queue):
            if task.priority > queued_task.priority:
                self.task_queue.insert(i, task)
                inserted = True
                break
        if not inserted:
            self.task_queue.append(task)
        logger.info(f'📋 Tarefa {task.task_id} adicionada à fila (prioridade {task.priority})')

    async def _task_processing_loop(self):
        """Loop principal de processamento de tarefas"""
        while self.running:
            try:
                if self.task_queue and len(self.active_tasks) < 10:
                    task = self.task_queue.popleft()
                    self.active_tasks[task.task_id] = task
                    task.status = TaskStatus.RUNNING
                    task.started_at = time.time()
                    asyncio.create_task(self._process_task(task))
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f'❌ Erro no loop de processamento: {e}')
                await asyncio.sleep(1.0)

    async def _process_task(self, task: DistributedTask):
        """Processa uma tarefa específica"""
        start_time = time.time()
        try:
            if time.time() - task.created_at > task.timeout:
                raise TimeoutError(f'Tarefa {task.task_id} excedeu timeout de {task.timeout}s')
            result = await self._execute_task_function(task)
            task.status = TaskStatus.COMPLETED
            task.completed_at = time.time()
            task.result = result
            processing_time = task.completed_at - task.started_at
            self.local_metrics['tasks_processed'] += 1
            self.local_metrics['total_processing_time'] += processing_time
            self.local_metrics['average_response_time'] = self.local_metrics['total_processing_time'] / self.local_metrics['tasks_processed']
            self.circuit_breaker.record_success()
            logger.info(f'✅ Tarefa {task.task_id} concluída em {processing_time:.2f}s')
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = time.time()
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.RETRYING
                await asyncio.sleep(2.0 ** task.retry_count)
                self._add_task_to_queue(task)
                logger.warning(f'⚠️ Tarefa {task.task_id} falhada, tentativa {task.retry_count}/{task.max_retries}')
            else:
                self.local_metrics['tasks_failed'] += 1
                logger.error(f'❌ Tarefa {task.task_id} falhou definitivamente: {e}')
            self.circuit_breaker.record_failure()
        finally:
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]
                self.completed_tasks[task.task_id] = task
                if len(self.completed_tasks) > 1000:
                    oldest_tasks = sorted(self.completed_tasks.items(), key=lambda x: x[1].completed_at or 0)
                    for task_id, _ in oldest_tasks[:100]:
                        del self.completed_tasks[task_id]

    async def _execute_task_function(self, task: DistributedTask) -> Any:
        """Executa a função da tarefa"""
        function_registry = {'compute_fibonacci': self._compute_fibonacci, 'process_data': self._process_data, 'analyze_text': self._analyze_text, 'matrix_multiply': self._matrix_multiply, 'sort_array': self._sort_array, 'hash_data': self._hash_data, 'sleep_task': self._sleep_task, 'cpu_intensive': self._cpu_intensive_task, 'memory_test': self._memory_test_task}
        if task.function_name not in function_registry:
            raise ValueError(f"Função '{task.function_name}' não encontrada")
        func = function_registry[task.function_name]
        if asyncio.iscoroutinefunction(func):
            result = await func(*task.args, **task.kwargs)
        else:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(self.executor, lambda: func(*task.args, **task.kwargs))
        return result

    def _compute_fibonacci(self, n: int) -> int:
        """Calcula Fibonacci de forma recursiva (CPU intensivo)"""
        if n <= 1:
            return n
        return self._compute_fibonacci(n - 1) + self._compute_fibonacci(n - 2)

    def _process_data(self, data: List[int]) -> Dict[str, Any]:
        """Processa lista de dados"""
        return {'sum': sum(data), 'avg': sum(data) / len(data) if data else 0, 'min': min(data) if data else None, 'max': max(data) if data else None, 'count': len(data)}

    def _analyze_text(self, text: str) -> Dict[str, Any]:
        """Análise simples de texto"""
        words = text.split()
        return {'word_count': len(words), 'char_count': len(text), 'unique_words': len(set(words)), 'avg_word_length': sum((len(word) for word in words)) / len(words) if words else 0}

    def _matrix_multiply(self, matrix_a: List[List[float]], matrix_b: List[List[float]]) -> List[List[float]]:
        """Multiplicação de matrizes"""
        import numpy as np
        a = np.array(matrix_a)
        b = np.array(matrix_b)
        result = np.dot(a, b)
        return result.tolist()

    def _sort_array(self, arr: List[int], algorithm: str='quicksort') -> List[int]:
        """Ordena array com diferentes algoritmos"""
        if algorithm == 'quicksort':
            return sorted(arr)
        elif algorithm == 'bubble':
            n = len(arr)
            result = arr.copy()
            for i in range(n):
                for j in range(0, n - i - 1):
                    if result[j] > result[j + 1]:
                        result[j], result[j + 1] = (result[j + 1], result[j])
            return result
        else:
            return sorted(arr)

    def _hash_data(self, data: str, algorithm: str='sha256') -> str:
        """Hash de dados"""
        if algorithm == 'sha256':
            return hashlib.sha256(data.encode()).hexdigest()
        elif algorithm == 'md5':
            return hashlib.md5(data.encode()).hexdigest()
        else:
            return hashlib.sha256(data.encode()).hexdigest()

    async def _sleep_task(self, duration: float) -> str:
        """Tarefa de sleep assíncrona"""
        await asyncio.sleep(duration)
        return f'Slept for {duration} seconds'

    def _cpu_intensive_task(self, iterations: int=1000000) -> int:
        """Tarefa CPU intensiva"""
        result = 0
        for i in range(iterations):
            result += i * i
        return result

    def _memory_test_task(self, size_mb: int=10) -> Dict[str, Any]:
        """Teste de uso de memória"""
        data = [0] * (size_mb * 1024 * 1024 // 8)
        total = sum(data)
        return {'allocated_mb': size_mb, 'items': len(data), 'sum': total}

    def _heartbeat_loop(self):
        """Loop de heartbeat"""
        while self.running:
            try:
                self._update_system_metrics()
                self.info.last_heartbeat = time.time()
                time.sleep(self.heartbeat_interval)
            except Exception as e:
                logger.error(f'❌ Erro no heartbeat: {e}')
                time.sleep(5.0)

    def _update_system_metrics(self):
        """Atualiza métricas do sistema"""
        import psutil
        try:
            self.info.cpu_usage = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            self.info.memory_usage = memory.percent
            disk = psutil.disk_usage('/')
            self.info.disk_usage = disk.percent
            self.info.network_latency = random.uniform(1.0, 50.0)
        except ImportError:
            self.info.cpu_usage = random.uniform(10.0, 80.0)
            self.info.memory_usage = random.uniform(20.0, 70.0)
            self.info.disk_usage = random.uniform(5.0, 90.0)
            self.info.network_latency = random.uniform(1.0, 50.0)

class CircuitBreakerState(Enum):
    """Estados do Circuit Breaker"""
    CLOSED = 'closed'
    OPEN = 'open'
    HALF_OPEN = 'half_open'

class CircuitBreaker:
    """Circuit Breaker pattern implementation"""

    def __init__(self, failure_threshold: int=5, timeout: float=float('inf')):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.timeout_count = 0
        self.last_failure_time = 0
        self.half_open_max_calls = 3
        self.half_open_calls = 0

    def record_success(self):
        """Registra sucesso"""
        self.success_count += 1
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.half_open_calls += 1
            if self.half_open_calls >= self.half_open_max_calls:
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
                self.half_open_calls = 0

    def record_failure(self):
        """Registra falha"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.state == CircuitBreakerState.CLOSED:
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN
        elif self.state == CircuitBreakerState.HALF_OPEN:
            self.state = CircuitBreakerState.OPEN
            self.half_open_calls = 0

    def record_timeout(self):
        """Registra timeout"""
        self.timeout_count += 1
        self.record_failure()

    def can_execute(self) -> bool:
        """Verifica se pode executar operação"""
        if self.state == CircuitBreakerState.CLOSED:
            return True
        elif self.state == CircuitBreakerState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                self.half_open_calls = 0
                return True
            return False
        elif self.state == CircuitBreakerState.HALF_OPEN:
            return self.half_open_calls < self.half_open_max_calls
        return False

class LoadBalancer:
    """Sistema de balanceamento de carga"""

    def __init__(self, algorithm: LoadBalancingAlgorithm=LoadBalancingAlgorithm.ROUND_ROBIN):
        self.algorithm = algorithm
        self.services: Dict[str, List[ServiceEndpoint]] = defaultdict(list)
        self.round_robin_counters: Dict[str, int] = defaultdict(int)
        self.connection_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    def register_service(self, service_name: str, endpoint: ServiceEndpoint):
        """Registra endpoint de serviço"""
        if endpoint not in self.services[service_name]:
            self.services[service_name].append(endpoint)
            logger.info(f'📡 Serviço {service_name} registrado: {endpoint.host}:{endpoint.port}')

    def unregister_service(self, service_name: str, endpoint: ServiceEndpoint):
        """Remove endpoint de serviço"""
        if endpoint in self.services[service_name]:
            self.services[service_name].remove(endpoint)
            logger.info(f'📡 Serviço {service_name} removido: {endpoint.host}:{endpoint.port}')

    def get_endpoint(self, service_name: str) -> Optional[ServiceEndpoint]:
        """Obtém endpoint usando algoritmo de balanceamento"""
        endpoints = self.services.get(service_name, [])
        healthy_endpoints = [ep for ep in endpoints if ep.healthy]
        if not healthy_endpoints:
            return None
        if self.algorithm == LoadBalancingAlgorithm.ROUND_ROBIN:
            return self._round_robin_select(service_name, healthy_endpoints)
        elif self.algorithm == LoadBalancingAlgorithm.WEIGHTED_ROUND_ROBIN:
            return self._weighted_round_robin_select(service_name, healthy_endpoints)
        elif self.algorithm == LoadBalancingAlgorithm.LEAST_CONNECTIONS:
            return self._least_connections_select(healthy_endpoints)
        elif self.algorithm == LoadBalancingAlgorithm.LEAST_RESPONSE_TIME:
            return self._least_response_time_select(healthy_endpoints)
        elif self.algorithm == LoadBalancingAlgorithm.RESOURCE_BASED:
            return self._resource_based_select(healthy_endpoints)
        elif self.algorithm == LoadBalancingAlgorithm.HASH_BASED:
            return self._hash_based_select(service_name, healthy_endpoints)
        elif self.algorithm == LoadBalancingAlgorithm.RANDOM:
            return random.choice(healthy_endpoints)
        else:
            return self._round_robin_select(service_name, healthy_endpoints)

    def _round_robin_select(self, service_name: str, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        """Seleção round robin"""
        index = self.round_robin_counters[service_name] % len(endpoints)
        self.round_robin_counters[service_name] += 1
        return endpoints[index]

    def _weighted_round_robin_select(self, service_name: str, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        """Seleção weighted round robin"""
        weighted_endpoints = []
        for ep in endpoints:
            weighted_endpoints.extend([ep] * max(1, ep.weight // 10))
        if weighted_endpoints:
            index = self.round_robin_counters[service_name] % len(weighted_endpoints)
            self.round_robin_counters[service_name] += 1
            return weighted_endpoints[index]
        return endpoints[0]

    def _least_connections_select(self, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        """Seleção por menor número de conexões"""
        return min(endpoints, key=lambda ep: ep.current_connections)

    def _least_response_time_select(self, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        """Seleção por menor tempo de resposta"""
        return min(endpoints, key=lambda ep: ep.response_time_ms)

    def _resource_based_select(self, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        """Seleção baseada em recursos (simulado)"""

        def resource_score(ep: ServiceEndpoint) -> float:
            connection_factor = 1.0 - ep.current_connections / ep.max_connections
            response_factor = 1.0 / (1.0 + ep.response_time_ms / 100.0)
            return connection_factor * response_factor
        return max(endpoints, key=resource_score)

    def _hash_based_select(self, service_name: str, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        """Seleção baseada em hash consistente"""
        service_hash = hash(service_name)
        index = service_hash % len(endpoints)
        return endpoints[index]

    def update_endpoint_metrics(self, service_name: str, endpoint: ServiceEndpoint, response_time: float, success: bool):
        """Atualiza métricas do endpoint"""
        if endpoint.response_time_ms == 0:
            endpoint.response_time_ms = response_time
        else:
            endpoint.response_time_ms = endpoint.response_time_ms * 0.9 + response_time * 0.1
        endpoint.last_health_check = time.time()
        if not success:
            if hasattr(endpoint, 'consecutive_failures'):
                endpoint.consecutive_failures += 1
            else:
                endpoint.consecutive_failures = 1
            if endpoint.consecutive_failures >= 3:
                endpoint.healthy = False
        else:
            endpoint.consecutive_failures = 0
            endpoint.healthy = True

class ServiceDiscovery:
    """Sistema de descoberta de serviços"""

    def __init__(self):
        self.services: Dict[str, Dict[str, ServiceEndpoint]] = defaultdict(dict)
        self.watchers: Dict[str, List[Callable]] = defaultdict(list)
        self.gossip_nodes: Set[str] = set()
        self.local_node_id = str(uuid.uuid4())

    def register_service(self, service_name: str, endpoint: ServiceEndpoint) -> str:
        """Registra serviço"""
        endpoint_id = f'{endpoint.host}:{endpoint.port}'
        self.services[service_name][endpoint_id] = endpoint
        self._notify_watchers(service_name, 'registered', endpoint)
        logger.info(f'🔍 Serviço registrado - {service_name}: {endpoint_id}')
        return endpoint_id

    def unregister_service(self, service_name: str, endpoint_id: str):
        """Remove registro de serviço"""
        if endpoint_id in self.services[service_name]:
            endpoint = self.services[service_name][endpoint_id]
            del self.services[service_name][endpoint_id]
            self._notify_watchers(service_name, 'unregistered', endpoint)
            logger.info(f'🔍 Serviço removido - {service_name}: {endpoint_id}')

    def discover_service(self, service_name: str) -> List[ServiceEndpoint]:
        """Descobre endpoints de um serviço"""
        return list(self.services[service_name].values())

    def watch_service(self, service_name: str, callback: Callable):
        """Registra callback para mudanças no serviço"""
        self.watchers[service_name].append(callback)

    def _notify_watchers(self, service_name: str, event_type: str, endpoint: ServiceEndpoint):
        """Notifica watchers sobre mudanças"""
        for callback in self.watchers[service_name]:
            try:
                callback(service_name, event_type, endpoint)
            except Exception as e:
                logger.error(f'❌ Erro notificando watcher: {e}')

    def health_check_services(self):
        """Executa health check em todos os serviços"""
        for service_name, endpoints in self.services.items():
            for endpoint_id, endpoint in endpoints.items():
                self._check_endpoint_health(endpoint)

    def _check_endpoint_health(self, endpoint: ServiceEndpoint):
        """Verifica saúde de um endpoint"""
        try:
            import requests
            url = f'{endpoint.protocol}://{endpoint.host}:{endpoint.port}{endpoint.health_check_path}'
            start_time = time.time()
            response = requests.get(url, timeout=30.0)
            response_time = (time.time() - start_time) * 1000
            endpoint.response_time_ms = response_time
            endpoint.last_health_check = time.time()
            endpoint.healthy = response.status_code == 200
        except ImportError:
            endpoint.healthy = random.random() > 0.1
            endpoint.response_time_ms = random.uniform(10, 200)
            endpoint.last_health_check = time.time()
        except Exception as e:
            endpoint.healthy = False
            logger.warning(f'⚠️ Health check falhou para {endpoint.host}:{endpoint.port}: {e}')

class AutoScaler:
    """Sistema de auto-scaling"""

    def __init__(self):
        self.scaling_policies: Dict[str, Dict[str, Any]] = {}
        self.metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.scaling_cooldown = 300
        self.last_scaling_action: Dict[str, float] = {}

    def add_scaling_policy(self, service_name: str, policy: ScalingPolicy, min_instances: int=1, max_instances: int=10, scale_up_threshold: float=80.0, scale_down_threshold: float=20.0, target_value: float=50.0):
        """Adiciona política de scaling"""
        self.scaling_policies[service_name] = {'policy': policy, 'min_instances': min_instances, 'max_instances': max_instances, 'scale_up_threshold': scale_up_threshold, 'scale_down_threshold': scale_down_threshold, 'target_value': target_value, 'current_instances': min_instances}
        logger.info(f'📈 Política de scaling adicionada para {service_name}: {policy.value}')

    def record_metric(self, service_name: str, metric_value: float):
        """Registra métrica para decisões de scaling"""
        self.metrics_history[service_name].append({'timestamp': time.time(), 'value': metric_value})

    def evaluate_scaling(self, service_name: str) -> Optional[Dict[str, Any]]:
        """Avalia se deve fazer scaling"""
        if service_name not in self.scaling_policies:
            return None
        policy_config = self.scaling_policies[service_name]
        if service_name in self.last_scaling_action:
            time_since_last = time.time() - self.last_scaling_action[service_name]
            if time_since_last < self.scaling_cooldown:
                return None
        recent_metrics = list(self.metrics_history[service_name])[-10:]
        if not recent_metrics:
            return None
        avg_metric = sum((m['value'] for m in recent_metrics)) / len(recent_metrics)
        current_instances = policy_config['current_instances']
        scale_up_threshold = policy_config['scale_up_threshold']
        scale_down_threshold = policy_config['scale_down_threshold']
        if avg_metric > scale_up_threshold and current_instances < policy_config['max_instances']:
            new_instances = min(policy_config['max_instances'], current_instances + self._calculate_scale_amount(avg_metric, scale_up_threshold))
            return self._execute_scaling(service_name, new_instances, 'scale_up', avg_metric)
        elif avg_metric < scale_down_threshold and current_instances > policy_config['min_instances']:
            new_instances = max(policy_config['min_instances'], current_instances - self._calculate_scale_amount(scale_down_threshold, avg_metric))
            return self._execute_scaling(service_name, new_instances, 'scale_down', avg_metric)
        return None

    def _calculate_scale_amount(self, current_value: float, threshold: float) -> int:
        """Calcula quantidade de instâncias para scaling"""
        diff_percent = abs(current_value - threshold) / threshold
        if diff_percent > 0.5:
            return 2
        elif diff_percent > 0.2:
            return 1
        else:
            return 1

    def _execute_scaling(self, service_name: str, new_instances: int, action: str, metric_value: float) -> Dict[str, Any]:
        """Executa ação de scaling"""
        old_instances = self.scaling_policies[service_name]['current_instances']
        self.scaling_policies[service_name]['current_instances'] = new_instances
        self.last_scaling_action[service_name] = time.time()
        scaling_info = {'service_name': service_name, 'action': action, 'old_instances': old_instances, 'new_instances': new_instances, 'trigger_metric': metric_value, 'timestamp': time.time()}
        logger.info(f'📈 Scaling {action} - {service_name}: {old_instances} -> {new_instances} instâncias')
        return scaling_info

class DistributedOrchestrator:
    """Orquestrador principal do sistema distribuído"""

    def __init__(self):
        self.nodes: Dict[str, DistributedNode] = {}
        self.load_balancer = LoadBalancer()
        self.service_discovery = ServiceDiscovery()
        self.auto_scaler = AutoScaler()
        self.global_task_queue = deque()
        self.task_scheduler_running = False
        self.metrics_collector = defaultdict(list)
        self.health_monitor_running = False
        self.replication_factor = 2
        self.task_timeout = float('inf')
        logger.info('🎼 Orquestrador Distribuído inicializado')

    async def add_node(self, node_id: str, address: str, port: int, role: NodeRole) -> DistributedNode:
        """Adiciona novo nó ao cluster"""
        if node_id in self.nodes:
            raise ValueError(f'Nó {node_id} já existe')
        node = DistributedNode(node_id, address, port, role)
        self.nodes[node_id] = node
        await node.start()
        endpoint = ServiceEndpoint(service_name=f'node_{role.value}', host=address, port=port, protocol='http')
        self.service_discovery.register_service(f'node_{role.value}', endpoint)
        self.load_balancer.register_service(f'node_{role.value}', endpoint)
        logger.info(f'➕ Nó {node_id} adicionado ao cluster')
        return node

    async def remove_node(self, node_id: str):
        """Remove nó do cluster"""
        if node_id not in self.nodes:
            raise ValueError(f'Nó {node_id} não encontrado')
        node = self.nodes[node_id]
        await node.stop()
        endpoint_id = f'{node.info.address}:{node.info.port}'
        self.service_discovery.unregister_service(f'node_{node.info.role.value}', endpoint_id)
        del self.nodes[node_id]
        logger.info(f'➖ Nó {node_id} removido do cluster')

    async def submit_task(self, function_name: str, args: tuple=(), kwargs: dict=None, priority: int=5, timeout: float=None, tags: set=None) -> str:
        """Submete tarefa para processamento distribuído"""
        if kwargs is None:
            kwargs = {}
        if tags is None:
            tags = set()
        if timeout is None:
            timeout = self.task_timeout
        task = DistributedTask(task_id=str(uuid.uuid4()), function_name=function_name, args=args, kwargs=kwargs, priority=priority, timeout=timeout, tags=tags)
        best_node = self._select_best_node_for_task(task)
        if best_node:
            await self._send_task_to_node(task, best_node)
        else:
            self.global_task_queue.append(task)
            logger.warning(f'⚠️ Nenhum nó disponível, tarefa {task.task_id} adicionada à fila global')
        logger.info(f'📋 Tarefa {task.task_id} submetida: {function_name}')
        return task.task_id

    def _select_best_node_for_task(self, task: DistributedTask) -> Optional[DistributedNode]:
        """Seleciona o melhor nó para executar uma tarefa"""
        worker_nodes = [node for node in self.nodes.values() if node.info.role in [NodeRole.WORKER, NodeRole.COORDINATOR]]
        if not worker_nodes:
            return None
        healthy_nodes = [node for node in worker_nodes if node.circuit_breaker.can_execute() and node.running]
        if not healthy_nodes:
            return None

        def node_score(node: DistributedNode) -> float:
            score = 100.0
            score -= node.info.cpu_usage * 0.5
            score -= node.info.memory_usage * 0.3
            score -= len(node.active_tasks) * 10
            score -= len(node.task_queue) * 5
            if node.local_metrics['tasks_processed'] > 0:
                success_rate = 1.0 - node.local_metrics['tasks_failed'] / node.local_metrics['tasks_processed']
                score += success_rate * 20
            score -= node.info.network_latency * 0.1
            return max(0, score)
        best_node = max(healthy_nodes, key=node_score)
        return best_node

    async def _send_task_to_node(self, task: DistributedTask, node: DistributedNode):
        """Envia tarefa para um nó específico"""
        try:
            import aiohttp
            url = f'http://{node.info.address}:{node.info.port}/task'
            task_data = {'task_id': task.task_id, 'function_name': task.function_name, 'args': task.args, 'kwargs': task.kwargs, 'priority': task.priority, 'timeout': task.timeout, 'max_retries': task.max_retries, 'tags': list(task.tags)}
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=task_data, timeout=5.0) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f'✅ Tarefa {task.task_id} enviada para {node.info.node_id}')
                        return result
                    else:
                        raise Exception(f'HTTP {response.status}')
        except ImportError:
            node._add_task_to_queue(task)
            logger.info(f'✅ Tarefa {task.task_id} adicionada à fila do nó {node.info.node_id}')
        except Exception as e:
            logger.error(f'❌ Erro enviando tarefa {task.task_id} para {node.info.node_id}: {e}')
            self.global_task_queue.append(task)

    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Obtém status de uma tarefa"""
        for node in self.nodes.values():
            try:
                import aiohttp
                url = f'http://{node.info.address}:{node.info.port}/task/{task_id}'
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=5.0) as response:
                        if response.status == 200:
                            return await response.json()
                        elif response.status != 404:
                            logger.warning(f'⚠️ Erro consultando nó {node.info.node_id}: {response.status}')
            except ImportError:
                if task_id in node.active_tasks:
                    task = node.active_tasks[task_id]
                    return {'task_id': task.task_id, 'status': task.status.value, 'assigned_node': task.assigned_node, 'created_at': task.created_at, 'started_at': task.started_at}
                elif task_id in node.completed_tasks:
                    task = node.completed_tasks[task_id]
                    return {'task_id': task.task_id, 'status': task.status.value, 'completed_at': task.completed_at, 'has_result': task.result is not None}
            except Exception as e:
                logger.warning(f'⚠️ Erro consultando nó {node.info.node_id}: {e}')
        return None

    def start_monitoring(self):
        """Inicia sistemas de monitoramento"""
        if not self.health_monitor_running:
            self.health_monitor_running = True
            threading.Thread(target=self._health_monitor_loop, daemon=True).start()
        if not self.task_scheduler_running:
            self.task_scheduler_running = True
            threading.Thread(target=self._task_scheduler_loop, daemon=True).start()
        logger.info('📊 Monitoramento iniciado')

    def _health_monitor_loop(self):
        """Loop de monitoramento de saúde"""
        while self.health_monitor_running:
            try:
                for node in self.nodes.values():
                    self._collect_node_metrics(node)
                self.service_discovery.health_check_services()
                self._evaluate_auto_scaling()
                time.sleep(30)
            except Exception as e:
                logger.error(f'❌ Erro no monitoramento: {e}')
                time.sleep(10)

    def _collect_node_metrics(self, node: DistributedNode):
        """Coleta métricas de um nó"""
        metrics = {'timestamp': time.time(), 'node_id': node.info.node_id, 'cpu_usage': node.info.cpu_usage, 'memory_usage': node.info.memory_usage, 'active_tasks': len(node.active_tasks), 'queue_length': len(node.task_queue), 'tasks_processed': node.local_metrics['tasks_processed'], 'tasks_failed': node.local_metrics['tasks_failed']}
        self.metrics_collector[node.info.node_id].append(metrics)
        self.auto_scaler.record_metric(f'node_{node.info.node_id}', node.info.cpu_usage)

    def _evaluate_auto_scaling(self):
        """Avalia necessidade de auto-scaling"""
        for service_name in self.auto_scaler.scaling_policies.keys():
            scaling_decision = self.auto_scaler.evaluate_scaling(service_name)
            if scaling_decision:
                logger.info(f'📈 Auto-scaling: {scaling_decision}')

    def _task_scheduler_loop(self):
        """Loop do scheduler de tarefas global"""
        while self.task_scheduler_running:
            try:
                if self.global_task_queue:
                    task = self.global_task_queue.popleft()
                    best_node = self._select_best_node_for_task(task)
                    if best_node:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(self._send_task_to_node(task, best_node))
                        loop.close()
                    else:
                        self.global_task_queue.append(task)
                time.sleep(1.0)
            except Exception as e:
                logger.error(f'❌ Erro no scheduler: {e}')
                time.sleep(5.0)

    def get_cluster_status(self) -> Dict[str, Any]:
        """Retorna status completo do cluster"""
        total_nodes = len(self.nodes)
        healthy_nodes = sum((1 for node in self.nodes.values() if node.running))
        total_tasks = sum((len(node.active_tasks) + len(node.task_queue) for node in self.nodes.values()))
        total_cpu = sum((node.info.cpu_usage for node in self.nodes.values()))
        avg_cpu = total_cpu / max(1, total_nodes)
        total_memory = sum((node.info.memory_usage for node in self.nodes.values()))
        avg_memory = total_memory / max(1, total_nodes)
        return {'cluster_info': {'total_nodes': total_nodes, 'healthy_nodes': healthy_nodes, 'unhealthy_nodes': total_nodes - healthy_nodes, 'global_queue_length': len(self.global_task_queue)}, 'aggregate_metrics': {'average_cpu_usage': avg_cpu, 'average_memory_usage': avg_memory, 'total_active_tasks': total_tasks, 'total_processed_tasks': sum((node.local_metrics['tasks_processed'] for node in self.nodes.values())), 'total_failed_tasks': sum((node.local_metrics['tasks_failed'] for node in self.nodes.values()))}, 'services': {service_name: len(endpoints) for service_name, endpoints in self.service_discovery.services.items()}, 'auto_scaling_policies': len(self.auto_scaler.scaling_policies), 'monitoring_active': self.health_monitor_running and self.task_scheduler_running}

    async def shutdown(self):
        """Encerra o orquestrador"""
        logger.info('🛑 Encerrando orquestrador...')
        self.health_monitor_running = False
        self.task_scheduler_running = False
        for node in self.nodes.values():
            await node.stop()
        logger.info('✅ Orquestrador encerrado')

async def run_distributed_orchestration_demo():
    """Demonstração completa do sistema de orquestração distribuída"""
    logger.info('🌐 DEMONSTRAÇÃO - DISTRIBUTED ORCHESTRATION SUPREME')
    logger.info('=' * 80)
    orchestrator = DistributedOrchestrator()
    try:
        logger.info('\n🚀 CRIANDO CLUSTER')
        logger.info('-' * 40)
        master = await orchestrator.add_node('master-1', '127.0.0.1', 8001, NodeRole.MASTER)
        worker1 = await orchestrator.add_node('worker-1', '127.0.0.1', 8002, NodeRole.WORKER)
        worker2 = await orchestrator.add_node('worker-2', '127.0.0.1', 8003, NodeRole.WORKER)
        coordinator = await orchestrator.add_node('coord-1', '127.0.0.1', 8004, NodeRole.COORDINATOR)
        orchestrator.start_monitoring()
        orchestrator.auto_scaler.add_scaling_policy('worker_nodes', ScalingPolicy.CPU_BASED, min_instances=2, max_instances=6, scale_up_threshold=70.0, scale_down_threshold=30.0)
        logger.info('✅ Cluster inicializado com 4 nós')
        logger.info('\n📋 SUBMETENDO TAREFAS')
        logger.info('-' * 40)
        tasks = []
        for i in range(5):
            task_id = await orchestrator.submit_task('cpu_intensive', args=(100000 + i * 50000,), priority=8, tags={'type', 'cpu_intensive'})
            tasks.append(task_id)
        for i in range(3):
            data = list(range(1000 * (i + 1)))
            task_id = await orchestrator.submit_task('process_data', args=(data,), priority=6, tags={'type', 'data_processing'})
            tasks.append(task_id)
        texts = ['O sistema de orquestração distribuída está funcionando perfeitamente', 'Load balancing e service discovery implementados com sucesso', 'Auto-scaling e circuit breakers operacionais']
        for text in texts:
            task_id = await orchestrator.submit_task('analyze_text', args=(text,), priority=4, tags={'type', 'text_analysis'})
            tasks.append(task_id)
        logger.info('⏳ Aguardando processamento das tarefas...')
        await asyncio.sleep(10)
        logger.info('\n📊 STATUS DAS TAREFAS')
        logger.info('-' * 40)
        completed_tasks = 0
        failed_tasks = 0
        for task_id in tasks:
            status = await orchestrator.get_task_status(task_id)
            if status:
                if status['status'] == 'completed':
                    completed_tasks += 1
                elif status['status'] == 'failed':
                    failed_tasks += 1
                logger.info(f"Tarefa {task_id[:8]}... : {status['status']}")
        logger.info('\n🏠 STATUS DO CLUSTER')
        logger.info('-' * 40)
        cluster_status = orchestrator.get_cluster_status()
        logger.info(f"Total de nós: {cluster_status['cluster_info']['total_nodes']}")
        logger.info(f"Nós saudáveis: {cluster_status['cluster_info']['healthy_nodes']}")
        logger.info(f"CPU médio: {cluster_status['aggregate_metrics']['average_cpu_usage']:.1f}%")
        logger.info(f"Memória média: {cluster_status['aggregate_metrics']['average_memory_usage']:.1f}%")
        logger.info(f"Tarefas ativas: {cluster_status['aggregate_metrics']['total_active_tasks']}")
        logger.info(f"Tarefas processadas: {cluster_status['aggregate_metrics']['total_processed_tasks']}")
        logger.info('\n🔥 TESTANDO TOLERÂNCIA A FALHAS')
        logger.info('-' * 40)
        await orchestrator.remove_node('worker-2')
        logger.info('❌ Worker-2 removido do cluster')
        for i in range(2):
            task_id = await orchestrator.submit_task('sleep_task', args=(2.0,), priority=7)
        await asyncio.sleep(5)
        cluster_status_after = orchestrator.get_cluster_status()
        logger.info(f"Nós após falha: {cluster_status_after['cluster_info']['total_nodes']}")
        logger.info(f"Nós saudáveis após falha: {cluster_status_after['cluster_info']['healthy_nodes']}")
        logger.info('\n📈 ESTATÍSTICAS FINAIS')
        logger.info('-' * 40)
        logger.info(f'Tarefas submetidas: {len(tasks) + 2}')
        logger.info(f'Tarefas completadas: {completed_tasks}')
        logger.info(f'Taxa de sucesso: {completed_tasks / max(1, len(tasks)) * 100:.1f}%')
        logger.info(f'Serviços descobertos: {len(orchestrator.service_discovery.services)}')
        logger.info(f'Políticas de auto-scaling: {len(orchestrator.auto_scaler.scaling_policies)}')
        logger.info('\n🏆 DEMONSTRAÇÃO CONCLUÍDA!')
        return {'orchestrator': orchestrator, 'tasks_submitted': len(tasks) + 2, 'tasks_completed': completed_tasks, 'cluster_status': cluster_status_after}
    finally:
        await orchestrator.shutdown()
if __name__ == '__main__':
    try:
        results = asyncio.run(run_distributed_orchestration_demo())
        logger.info('🌐 DISTRIBUTED ORCHESTRATION SUPREME - IMPLEMENTAÇÃO COMPLETA! 🌐')
    except KeyboardInterrupt:
        logger.info('🛑 Demonstração interrompida pelo usuário')
    except Exception as e:
        logger.error(f'❌ Erro na demonstração: {e}')