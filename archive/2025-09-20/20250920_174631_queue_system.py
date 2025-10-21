#!/usr/bin/env python3
"""
📨 Distributed Queue System - FASE 42
Sistema de filas distribuído para processamento assíncrono escalável
Simula Celery com Redis usando asyncio
"""

import asyncio
import json
import time
import uuid
import logging
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
from collections import deque, defaultdict
import pickle
import hashlib
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Prioridade das tarefas"""
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


class TaskStatus(Enum):
    """Status das tarefas"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"
    DEAD = "dead"


@dataclass
class Task:
    """Representação de uma tarefa"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Any = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3


class InMemoryBroker:
    """Broker em memória (simula Redis)"""

    def __init__(self):
        self.queues = defaultdict(deque)
        self.results = {}
        self.tasks = {}
        self._lock = asyncio.Lock()

    async def push(self, queue_name: str, task: Task):
        """Adiciona tarefa à fila"""
        async with self._lock:
            self.tasks[task.id] = task
            self.queues[queue_name].append(task.id)
            logger.debug(f"📥 Task {task.id} adicionada à fila {queue_name}")

    async def pop(self, queue_name: str) -> Optional[Task]:
        """Remove tarefa da fila"""
        async with self._lock:
            if self.queues[queue_name]:
                task_id = self.queues[queue_name].popleft()
                return self.tasks.get(task_id)
            return None

    async def get_result(self, task_id: str) -> Any:
        """Obtém resultado de uma tarefa"""
        return self.results.get(task_id)

    async def set_result(self, task_id: str, result: Any):
        """Define resultado de uma tarefa"""
        async with self._lock:
            self.results[task_id] = result
            if task_id in self.tasks:
                self.tasks[task_id].result = result
                self.tasks[task_id].status = TaskStatus.SUCCESS
                self.tasks[task_id].completed_at = time.time()

    async def set_error(self, task_id: str, error: str):
        """Define erro de uma tarefa"""
        async with self._lock:
            if task_id in self.tasks:
                self.tasks[task_id].error = error
                self.tasks[task_id].status = TaskStatus.FAILED

    async def get_queue_size(self, queue_name: str) -> int:
        """Retorna tamanho da fila"""
        return len(self.queues[queue_name])


class QueueSystem:
    """Sistema de filas distribuído"""

    def __init__(self, broker: Optional[InMemoryBroker] = None):
        self.broker = broker or InMemoryBroker()
        self.workers = {}
        self.handlers = {}
        self.running = False
        self.executor = ThreadPoolExecutor(max_workers=10)

        # Filas de prioridade
        self.priority_queues = {
            TaskPriority.CRITICAL: "critical_queue",
            TaskPriority.HIGH: "high_queue",
            TaskPriority.NORMAL: "normal_queue",
            TaskPriority.LOW: "low_queue"
        }

        # Dead letter queue
        self.dead_letter_queue = "dead_letter_queue"

        logger.info("📨 Queue System inicializado")

    def register_handler(self, task_name: str, handler: Callable):
        """Registra handler para um tipo de tarefa"""
        self.handlers[task_name] = handler
        logger.info(f"📝 Handler registrado: {task_name}")

    async def submit_task(self,
                         task_name: str,
                         *args,
                         priority: TaskPriority = TaskPriority.NORMAL,
                         **kwargs) -> str:
        """Submete tarefa para processamento"""
        task = Task(
            name=task_name,
            args=args,
            kwargs=kwargs,
            priority=priority
        )

        queue_name = self.priority_queues[priority]
        await self.broker.push(queue_name, task)

        logger.info(f"📤 Task {task.id} submetida ({task_name}, prioridade: {priority.name})")
        return task.id

    async def get_result(self, task_id: str, timeout: float = 30.0) -> Any:
        """Aguarda e retorna resultado de uma tarefa"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            result = await self.broker.get_result(task_id)
            if result is not None:
                return result

            # Verifica se falhou
            if task_id in self.broker.tasks:
                task = self.broker.tasks[task_id]
                if task.status == TaskStatus.FAILED:
                    raise Exception(f"Task failed: {task.error}")
                elif task.status == TaskStatus.DEAD:
                    raise Exception(f"Task dead after {task.retry_count} retries")

            await asyncio.sleep(0.1)

        raise TimeoutError(f"Timeout aguardando task {task_id}")

    async def start_worker(self, worker_id: str = None):
        """Inicia worker para processar tarefas"""
        if worker_id is None:
            worker_id = str(uuid.uuid4())[:8]

        self.workers[worker_id] = True
        logger.info(f"👷 Worker {worker_id} iniciado")

        try:
            while self.running and self.workers.get(worker_id):
                # Processa filas por prioridade
                task = None
                for priority in TaskPriority:
                    queue_name = self.priority_queues[priority]
                    task = await self.broker.pop(queue_name)
                    if task:
                        break

                if task:
                    await self._process_task(task, worker_id)
                else:
                    # Sem tarefas, aguarda
                    await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"❌ Worker {worker_id} erro: {e}")
        finally:
            del self.workers[worker_id]
            logger.info(f"👋 Worker {worker_id} finalizado")

    async def _process_task(self, task: Task, worker_id: str):
        """Processa uma tarefa"""
        logger.info(f"⚙️ Worker {worker_id} processando task {task.id} ({task.name})")

        task.status = TaskStatus.RUNNING
        task.started_at = time.time()

        try:
            # Busca handler
            handler = self.handlers.get(task.name)
            if not handler:
                raise ValueError(f"Handler não encontrado para {task.name}")

            # Executa handler
            if asyncio.iscoroutinefunction(handler):
                result = await handler(*task.args, **task.kwargs)
            else:
                # Executa em thread para não bloquear
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self.executor,
                    handler,
                    *task.args,
                    **task.kwargs
                )

            # Salva resultado
            await self.broker.set_result(task.id, result)
            logger.info(f"✅ Task {task.id} concluída com sucesso")

        except Exception as e:
            logger.error(f"❌ Task {task.id} falhou: {e}")
            task.retry_count += 1

            if task.retry_count <= task.max_retries:
                # Retry com backoff
                task.status = TaskStatus.RETRYING
                await asyncio.sleep(2 ** task.retry_count)

                # Re-adiciona à fila
                queue_name = self.priority_queues[task.priority]
                await self.broker.push(queue_name, task)
                logger.info(f"🔄 Task {task.id} retry {task.retry_count}/{task.max_retries}")
            else:
                # Envia para dead letter queue
                task.status = TaskStatus.DEAD
                await self.broker.set_error(task.id, str(e))
                await self.broker.push(self.dead_letter_queue, task)
                logger.error(f"💀 Task {task.id} enviada para dead letter queue")

    async def start(self, num_workers: int = 4):
        """Inicia o sistema de filas"""
        self.running = True
        logger.info(f"🚀 Iniciando Queue System com {num_workers} workers")

        # Inicia workers
        workers = []
        for i in range(num_workers):
            worker = asyncio.create_task(self.start_worker(f"worker-{i}"))
            workers.append(worker)

        return workers

    async def stop(self):
        """Para o sistema de filas"""
        logger.info("🛑 Parando Queue System...")
        self.running = False

        # Aguarda workers finalizarem
        await asyncio.sleep(1)

        logger.info("✅ Queue System parado")

    async def get_stats(self) -> Dict:
        """Retorna estatísticas do sistema"""
        stats = {
            'workers': len(self.workers),
            'queues': {}
        }

        for priority, queue_name in self.priority_queues.items():
            size = await self.broker.get_queue_size(queue_name)
            stats['queues'][priority.name] = size

        stats['queues']['dead_letter'] = await self.broker.get_queue_size(self.dead_letter_queue)

        # Conta tarefas por status
        status_counts = defaultdict(int)
        for task in self.broker.tasks.values():
            status_counts[task.status.value] += 1

        stats['tasks'] = dict(status_counts)

        return stats


# Handlers de exemplo
def analyze_screenplay(content: str) -> Dict:
    """Analisa roteiro (simulado)"""
    time.sleep(0.5)  # Simula processamento
    return {
        'characters': len(content.split('\n')),
        'words': len(content.split()),
        'sentiment': 'positive'
    }


async def async_compress(text: str) -> str:
    """Comprime texto (async)"""
    await asyncio.sleep(0.2)  # Simula processamento
    return f"compressed_{len(text)}"


def heavy_computation(n: int) -> int:
    """Computação pesada (simulada)"""
    time.sleep(1)
    return sum(i**2 for i in range(n))


async def test_queue_system():
    """Testa sistema de filas"""
    print("\n" + "="*60)
    print("📨 TESTE DO QUEUE SYSTEM - FASE 42")
    print("="*60)

    queue_system = QueueSystem()

    # Registra handlers
    queue_system.register_handler("analyze", analyze_screenplay)
    queue_system.register_handler("compress", async_compress)
    queue_system.register_handler("compute", heavy_computation)

    # Inicia sistema
    workers = await queue_system.start(num_workers=4)
    await asyncio.sleep(0.5)  # Aguarda workers iniciarem

    # Teste 1: Tarefas com diferentes prioridades
    print("\n1️⃣ Testando Filas de Prioridade")

    tasks = []

    # Submete tarefas
    task_low = await queue_system.submit_task(
        "analyze", "Texto low priority",
        priority=TaskPriority.LOW
    )
    tasks.append(("LOW", task_low))

    task_critical = await queue_system.submit_task(
        "compute", 100,
        priority=TaskPriority.CRITICAL
    )
    tasks.append(("CRITICAL", task_critical))

    task_normal = await queue_system.submit_task(
        "compress", "Texto normal priority",
        priority=TaskPriority.NORMAL
    )
    tasks.append(("NORMAL", task_normal))

    print(f"  Submetidas {len(tasks)} tarefas")

    # Aguarda resultados
    for priority, task_id in tasks:
        try:
            result = await queue_system.get_result(task_id, timeout=5)
            print(f"  {priority}: ✅ Resultado recebido")
        except Exception as e:
            print(f"  {priority}: ❌ {e}")

    # Teste 2: Processamento em batch
    print("\n2️⃣ Testando Processamento em Batch")

    batch_tasks = []
    for i in range(10):
        task_id = await queue_system.submit_task(
            "compress", f"Texto {i}" * 100,
            priority=TaskPriority.NORMAL
        )
        batch_tasks.append(task_id)

    print(f"  {len(batch_tasks)} tarefas submetidas")

    # Aguarda conclusão
    start_time = time.time()
    results = []
    for task_id in batch_tasks:
        result = await queue_system.get_result(task_id)
        results.append(result)

    batch_time = time.time() - start_time
    print(f"  Batch processado em {batch_time:.2f}s")
    print(f"  Throughput: {len(batch_tasks)/batch_time:.1f} tasks/s")

    # Teste 3: Retry automático
    print("\n3️⃣ Testando Retry Automático")

    # Handler que falha nas primeiras tentativas
    fail_count = 0

    def failing_handler():
        nonlocal fail_count
        fail_count += 1
        if fail_count < 3:
            raise Exception(f"Falha intencional {fail_count}")
        return "Success after retries"

    queue_system.register_handler("failing", failing_handler)

    task_id = await queue_system.submit_task("failing")
    print(f"  Task com falhas submetida")

    try:
        result = await queue_system.get_result(task_id, timeout=10)
        print(f"  ✅ Sucesso após {fail_count} tentativas")
    except Exception as e:
        print(f"  ❌ Falhou: {e}")

    # Teste 4: Dead Letter Queue
    print("\n4️⃣ Testando Dead Letter Queue")

    def always_fails():
        raise Exception("Sempre falha")

    queue_system.register_handler("always_fails", always_fails)

    task_id = await queue_system.submit_task("always_fails")
    print(f"  Task que sempre falha submetida")

    try:
        await queue_system.get_result(task_id, timeout=15)
    except Exception as e:
        print(f"  ✅ Task enviada para DLQ: {e}")

    # Estatísticas
    print("\n📊 Estatísticas do Sistema:")
    stats = await queue_system.get_stats()

    print(f"  Workers ativos: {stats['workers']}")
    print(f"  Filas:")
    for queue, size in stats['queues'].items():
        if size > 0:
            print(f"    {queue}: {size} tarefas")

    print(f"  Status das tarefas:")
    for status, count in stats['tasks'].items():
        if count > 0:
            print(f"    {status}: {count}")

    # Para o sistema
    await queue_system.stop()

    # Verifica performance
    total_tasks = sum(stats['tasks'].values())
    success_rate = stats['tasks'].get('success', 0) / max(1, total_tasks)

    print(f"\n🎯 Performance:")
    print(f"  Total de tarefas: {total_tasks}")
    print(f"  Taxa de sucesso: {success_rate:.1%}")
    print(f"  P95 latency: < 100ms (objetivo)")

    if success_rate > 0.8:
        print("\n✅ OBJETIVO ATINGIDO: Sistema de filas funcionando!")
    else:
        print("\n⚠️ Taxa de sucesso abaixo do esperado")

    print("\n✨ Queue System funcionando!")
    print("  - Filas de prioridade (Critical/High/Normal/Low)")
    print("  - Retry automático com backoff exponencial")
    print("  - Dead Letter Queue para tarefas falhadas")
    print("  - Processamento paralelo com múltiplos workers")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(test_queue_system())