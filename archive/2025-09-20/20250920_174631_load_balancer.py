"""
Load Balancer - Distribui carga entre múltiplos modelos e recursos.
Otimizado para Mac Studio M3 Ultra com múltiplos modelos Ollama.
"""

import time
import random
from typing import List, Dict, Any, Optional, Callable
from threading import Lock, Thread
from queue import Queue, PriorityQueue
from dataclasses import dataclass, field
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass(order=True)
class Task:
    """Representa uma tarefa no balanceador."""
    priority: int
    task_id: str = field(compare=False)
    model: str = field(compare=False)
    payload: Any = field(compare=False)
    callback: Optional[Callable] = field(compare=False)
    timestamp: float = field(default_factory=time.time, compare=False)


class ModelPool:
    """
    Pool de modelos disponíveis.
    Gerencia estado e disponibilidade de cada modelo.
    """

    def __init__(self):
        """Inicializa o pool."""
        self.models = {}
        self.lock = Lock()

        # Estatísticas por modelo
        self.stats = defaultdict(lambda: {
            'requests': 0,
            'total_time': 0,
            'errors': 0,
            'last_used': 0
        })

    def register_model(self, model_name: str, capacity: int = 1):
        """
        Registra um modelo no pool.

        Args:
            model_name: Nome do modelo
            capacity: Capacidade simultânea
        """
        with self.lock:
            self.models[model_name] = {
                'capacity': capacity,
                'current_load': 0,
                'available': True,
                'health': 'healthy'
            }
            logger.info(f"Registered model {model_name} with capacity {capacity}")

    def get_available_model(self, preferred_model: Optional[str] = None) -> Optional[str]:
        """
        Retorna modelo disponível.

        Args:
            preferred_model: Modelo preferencial

        Returns:
            Nome do modelo ou None
        """
        with self.lock:
            # Tenta modelo preferencial primeiro
            if preferred_model and preferred_model in self.models:
                model_info = self.models[preferred_model]
                if (model_info['available'] and
                    model_info['current_load'] < model_info['capacity'] and
                    model_info['health'] == 'healthy'):
                    return preferred_model

            # Busca modelo com menor carga
            available_models = [
                (name, info) for name, info in self.models.items()
                if info['available'] and
                   info['current_load'] < info['capacity'] and
                   info['health'] == 'healthy'
            ]

            if not available_models:
                return None

            # Seleciona modelo com menor carga relativa
            best_model = min(
                available_models,
                key=lambda x: x[1]['current_load'] / x[1]['capacity']
            )

            return best_model[0]

    def acquire_model(self, model_name: str) -> bool:
        """
        Adquire slot em um modelo.

        Args:
            model_name: Nome do modelo

        Returns:
            True se adquirido com sucesso
        """
        with self.lock:
            if model_name not in self.models:
                return False

            model_info = self.models[model_name]

            if (model_info['available'] and
                model_info['current_load'] < model_info['capacity'] and
                model_info['health'] == 'healthy'):

                model_info['current_load'] += 1
                self.stats[model_name]['requests'] += 1
                self.stats[model_name]['last_used'] = time.time()
                return True

            return False

    def release_model(self, model_name: str, execution_time: float = 0):
        """
        Libera slot em um modelo.

        Args:
            model_name: Nome do modelo
            execution_time: Tempo de execução
        """
        with self.lock:
            if model_name in self.models:
                self.models[model_name]['current_load'] = max(
                    0,
                    self.models[model_name]['current_load'] - 1
                )

                if execution_time > 0:
                    self.stats[model_name]['total_time'] += execution_time

    def mark_unhealthy(self, model_name: str):
        """Marca modelo como não saudável."""
        with self.lock:
            if model_name in self.models:
                self.models[model_name]['health'] = 'unhealthy'
                logger.warning(f"Model {model_name} marked as unhealthy")

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do pool."""
        with self.lock:
            stats = {}
            for model_name, model_info in self.models.items():
                model_stats = self.stats[model_name].copy()

                # Calcula média de tempo
                if model_stats['requests'] > 0:
                    avg_time = model_stats['total_time'] / model_stats['requests']
                else:
                    avg_time = 0

                stats[model_name] = {
                    **model_info,
                    'total_requests': model_stats['requests'],
                    'avg_time': avg_time,
                    'errors': model_stats['errors'],
                    'utilization': model_info['current_load'] / model_info['capacity']
                }

            return stats


class LoadBalancer:
    """
    Balanceador de carga principal.
    Distribui tarefas entre modelos disponíveis.
    """

    def __init__(self, max_queue_size: int = 1000):
        """
        Inicializa o balanceador.

        Args:
            max_queue_size: Tamanho máximo da fila
        """
        self.model_pool = ModelPool()
        self.task_queue = PriorityQueue(maxsize=max_queue_size)
        self.running = True

        # Workers para processar tarefas
        self.workers = []
        self.num_workers = 4  # Ajustado para M3 Ultra

        # Estratégias de balanceamento
        self.strategies = {
            'round_robin': self._round_robin,
            'least_loaded': self._least_loaded,
            'weighted': self._weighted,
            'sticky': self._sticky
        }
        self.current_strategy = 'least_loaded'

        # Sessões sticky (para manter contexto)
        self.sticky_sessions = {}

        # Inicializa workers
        self._start_workers()

        logger.info(f"LoadBalancer initialized with {self.num_workers} workers")

    def _start_workers(self):
        """Inicia threads workers."""
        for i in range(self.num_workers):
            worker = Thread(
                target=self._worker_loop,
                name=f"lb-worker-{i}",
                daemon=True
            )
            worker.start()
            self.workers.append(worker)

    def _worker_loop(self):
        """Loop principal do worker."""
        while self.running:
            try:
                # Pega tarefa da fila (com timeout para permitir shutdown)
                task = self.task_queue.get(timeout=1)

                # Processa tarefa
                self._process_task(task)

            except:
                # Timeout ou fila vazia - continua
                continue

    def _process_task(self, task: Task):
        """
        Processa uma tarefa.

        Args:
            task: Tarefa a processar
        """
        start_time = time.time()
        model_name = None

        try:
            # Seleciona modelo usando estratégia atual
            strategy_func = self.strategies[self.current_strategy]
            model_name = strategy_func(task)

            if not model_name:
                logger.warning(f"No available model for task {task.task_id}")
                if task.callback:
                    task.callback(None, error="No available model")
                return

            # Adquire modelo
            if not self.model_pool.acquire_model(model_name):
                # Re-enfileira com prioridade maior
                task.priority = max(0, task.priority - 1)
                self.task_queue.put(task)
                return

            # Executa tarefa
            result = self._execute_on_model(model_name, task.payload)

            # Callback com resultado
            if task.callback:
                task.callback(result, error=None)

        except Exception as e:
            logger.error(f"Error processing task {task.task_id}: {e}")

            if model_name:
                self.model_pool.stats[model_name]['errors'] += 1

            if task.callback:
                task.callback(None, error=str(e))

        finally:
            # Libera modelo
            if model_name:
                execution_time = time.time() - start_time
                self.model_pool.release_model(model_name, execution_time)

    def _execute_on_model(self, model_name: str, payload: Any) -> Any:
        """
        Executa payload em modelo específico.

        Args:
            model_name: Nome do modelo
            payload: Dados a processar

        Returns:
            Resultado do processamento
        """
        # Importação lazy
        from .ollama_core import OllamaCore

        ollama = OllamaCore()

        # Extrai prompt do payload
        if isinstance(payload, dict):
            prompt = payload.get('prompt', str(payload))
        else:
            prompt = str(payload)

        # Gera resposta
        response = ollama.generate(prompt, model=model_name)

        return response

    def submit_task(self, model: str, payload: Any,
                   priority: int = 5,
                   callback: Optional[Callable] = None) -> str:
        """
        Submete tarefa para processamento.

        Args:
            model: Modelo preferencial
            payload: Dados a processar
            priority: Prioridade (0=máxima, 10=mínima)
            callback: Callback para resultado

        Returns:
            ID da tarefa
        """
        task_id = f"task_{time.time()}_{random.randint(1000, 9999)}"

        task = Task(
            priority=priority,
            task_id=task_id,
            model=model,
            payload=payload,
            callback=callback
        )

        self.task_queue.put(task)

        return task_id

    def register_models(self, models: List[Dict[str, Any]]):
        """
        Registra múltiplos modelos.

        Args:
            models: Lista de configurações de modelos
        """
        for model_config in models:
            self.model_pool.register_model(
                model_config['name'],
                model_config.get('capacity', 1)
            )

    # === Estratégias de Balanceamento ===

    def _round_robin(self, task: Task) -> Optional[str]:
        """Estratégia round-robin."""
        # Implementação simplificada
        return self.model_pool.get_available_model()

    def _least_loaded(self, task: Task) -> Optional[str]:
        """Estratégia least-loaded (padrão)."""
        return self.model_pool.get_available_model(task.model)

    def _weighted(self, task: Task) -> Optional[str]:
        """Estratégia weighted baseada em performance."""
        with self.model_pool.lock:
            candidates = []

            for name, info in self.model_pool.models.items():
                if (info['available'] and
                    info['current_load'] < info['capacity'] and
                    info['health'] == 'healthy'):

                    # Calcula peso baseado em performance
                    stats = self.model_pool.stats[name]
                    if stats['requests'] > 0:
                        avg_time = stats['total_time'] / stats['requests']
                        weight = 1.0 / (avg_time + 0.1)  # Evita divisão por zero
                    else:
                        weight = 1.0

                    candidates.append((name, weight))

            if not candidates:
                return None

            # Seleciona proporcionalmente ao peso
            total_weight = sum(w for _, w in candidates)
            rand = random.uniform(0, total_weight)

            cumulative = 0
            for name, weight in candidates:
                cumulative += weight
                if rand <= cumulative:
                    return name

            return candidates[-1][0]

    def _sticky(self, task: Task) -> Optional[str]:
        """Estratégia sticky session."""
        # Usa task_id como session_id
        session_id = task.task_id.split('_')[0]  # Extrai prefixo

        # Verifica se já tem sessão
        if session_id in self.sticky_sessions:
            model = self.sticky_sessions[session_id]
            if self.model_pool.get_available_model(model):
                return model

        # Nova sessão
        model = self.model_pool.get_available_model(task.model)
        if model:
            self.sticky_sessions[session_id] = model

        return model

    def set_strategy(self, strategy: str):
        """
        Define estratégia de balanceamento.

        Args:
            strategy: Nome da estratégia
        """
        if strategy in self.strategies:
            self.current_strategy = strategy
            logger.info(f"Load balancing strategy set to {strategy}")
        else:
            logger.warning(f"Unknown strategy {strategy}")

    def get_status(self) -> Dict[str, Any]:
        """Retorna status do balanceador."""
        return {
            'queue_size': self.task_queue.qsize(),
            'strategy': self.current_strategy,
            'workers': len(self.workers),
            'models': self.model_pool.get_stats()
        }

    def shutdown(self):
        """Encerra o balanceador."""
        logger.info("Shutting down LoadBalancer")
        self.running = False

        # Espera workers terminarem
        for worker in self.workers:
            worker.join(timeout=5)

        logger.info("LoadBalancer shutdown complete")


# Singleton global
_load_balancer: Optional[LoadBalancer] = None


def get_load_balancer() -> LoadBalancer:
    """Retorna instância singleton do load balancer."""
    global _load_balancer
    if _load_balancer is None:
        _load_balancer = LoadBalancer()

        # Registra modelos padrão
        default_models = [
            {'name': 'mistral:instruct', 'capacity': 2},
            {'name': 'llama3.2:latest', 'capacity': 2},
            {'name': 'phi3.5:latest', 'capacity': 2},
            {'name': 'gemma2:27b', 'capacity': 1}
        ]
        _load_balancer.register_models(default_models)

    return _load_balancer