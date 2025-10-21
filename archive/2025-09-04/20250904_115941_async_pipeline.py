#!/usr/bin/env python3
"""
⚡ ASYNC PIPELINE - Pipeline de Processamento Assíncrono ULTRA ROBUSTO
Sistema avançado com workers, queue management e backpressure
"""

import asyncio
import time
import json
import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from collections import deque
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import threading
import multiprocessing as mp
import queue

class TaskPriority(Enum):
    """Prioridades de tarefas"""
    CRITICAL = 0  # Máxima prioridade
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4  # Mínima prioridade

@dataclass
class Task:
    """Representação de uma tarefa no pipeline"""
    id: str
    priority: TaskPriority
    stage: str
    data: Any
    created_at: float
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    retries: int = 0
    max_retries: int = 3
    timeout: float = 30.0
    metadata: Dict = None

class AsyncPipeline:
    """Pipeline assíncrono multi-stage com processamento paralelo"""
    
    def __init__(self, max_workers: int = None, enable_multiprocessing: bool = True):
        """
        Inicializa pipeline ROBUSTO
        
        Args:
            max_workers: Número máximo de workers (None = auto)
            enable_multiprocessing: Habilitar processamento multi-processo
        """
        # Auto-detectar workers ideais
        if max_workers is None:
            cpu_count = mp.cpu_count()
            max_workers = min(32, cpu_count * 2)  # 2x CPUs, máximo 32
        
        self.max_workers = max_workers
        self.enable_multiprocessing = enable_multiprocessing
        
        # Filas por prioridade
        self.queues = {
            priority: asyncio.Queue(maxsize=1000)
            for priority in TaskPriority
        }
        
        # Stages do pipeline
        self.stages = {}
        self.stage_order = []
        
        # Workers e executors
        self.thread_executor = ThreadPoolExecutor(max_workers=max_workers)
        if enable_multiprocessing:
            self.process_executor = ProcessPoolExecutor(max_workers=max_workers // 2)
        else:
            self.process_executor = None
        
        # Estado e controle
        self.running = False
        self.workers = []
        self.tasks_in_flight = {}  # ID -> Task
        self.completed_tasks = deque(maxlen=10000)  # Últimas 10k tarefas
        
        # Estatísticas ROBUSTAS
        self.stats = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'failed_tasks': 0,
            'retried_tasks': 0,
            'avg_latency_ms': 0,
            'throughput_per_sec': 0,
            'queue_sizes': {},
            'stage_latencies': {},
            'worker_utilization': 0
        }
        
        # Backpressure control
        self.backpressure_threshold = 0.8  # 80% das filas cheias
        self.backpressure_active = False
        
        # Lock para thread safety
        self.lock = threading.Lock()
        
        print(f"⚡ Pipeline Assíncrono inicializado com {max_workers} workers")
    
    def add_stage(self, name: str, processor: Callable, 
                  parallelism: int = 1, use_multiprocessing: bool = False):
        """
        Adiciona stage ao pipeline
        
        Args:
            name: Nome do stage
            processor: Função processadora
            parallelism: Grau de paralelismo
            use_multiprocessing: Usar multiprocessing para CPU-bound
        """
        self.stages[name] = {
            'processor': processor,
            'parallelism': parallelism,
            'use_multiprocessing': use_multiprocessing,
            'active_tasks': 0,
            'total_processed': 0,
            'total_errors': 0,
            'avg_latency': 0
        }
        
        if name not in self.stage_order:
            self.stage_order.append(name)
        
        print(f"   Stage '{name}' adicionado (parallelism={parallelism})")
    
    async def submit(self, data: Any, priority: TaskPriority = TaskPriority.NORMAL,
                     metadata: Dict = None, timeout: float = 30.0) -> str:
        """
        Submete tarefa ao pipeline
        
        Returns:
            Task ID para rastreamento
        """
        # Verificar backpressure
        if self.backpressure_active:
            await self._wait_for_capacity()
        
        # Criar tarefa
        task = Task(
            id=str(uuid.uuid4()),
            priority=priority,
            stage=self.stage_order[0] if self.stage_order else 'default',
            data=data,
            created_at=time.time(),
            timeout=timeout,
            metadata=metadata or {}
        )
        
        # Adicionar à fila apropriada
        await self.queues[priority].put(task)
        
        with self.lock:
            self.tasks_in_flight[task.id] = task
            self.stats['total_tasks'] += 1
        
        return task.id
    
    async def submit_batch(self, items: List[Tuple[Any, TaskPriority]], 
                          metadata: Dict = None) -> List[str]:
        """Submete batch de tarefas"""
        task_ids = []
        
        for data, priority in items:
            task_id = await self.submit(data, priority, metadata)
            task_ids.append(task_id)
        
        return task_ids
    
    async def get_result(self, task_id: str, timeout: float = None) -> Optional[Any]:
        """
        Aguarda e retorna resultado da tarefa
        
        Args:
            task_id: ID da tarefa
            timeout: Timeout em segundos
        """
        start_time = time.time()
        
        while True:
            # Verificar se completou
            with self.lock:
                if task_id in self.tasks_in_flight:
                    task = self.tasks_in_flight[task_id]
                    if task.completed_at:
                        if task.error:
                            raise Exception(f"Task failed: {task.error}")
                        return task.result
            
            # Verificar em completed
            for task in self.completed_tasks:
                if task.id == task_id:
                    if task.error:
                        raise Exception(f"Task failed: {task.error}")
                    return task.result
            
            # Verificar timeout
            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError(f"Timeout waiting for task {task_id}")
            
            await asyncio.sleep(0.1)
    
    async def start(self):
        """Inicia o pipeline"""
        if self.running:
            return
        
        self.running = True
        
        # Iniciar workers para cada prioridade
        workers_per_priority = max(1, self.max_workers // len(TaskPriority))
        for priority in TaskPriority:
            for i in range(workers_per_priority):
                worker = asyncio.create_task(
                    self._worker(priority, f"worker-{priority.name}-{i}")
                )
                self.workers.append(worker)
        
        # Iniciar monitor
        monitor = asyncio.create_task(self._monitor())
        self.workers.append(monitor)
        
        print(f"🚀 Pipeline iniciado com {len(self.workers)} workers")
    
    async def stop(self):
        """Para o pipeline graciosamente"""
        self.running = False
        
        # Aguardar workers finalizarem
        await asyncio.gather(*self.workers, return_exceptions=True)
        
        # Shutdown executors
        self.thread_executor.shutdown(wait=True)
        if self.process_executor:
            self.process_executor.shutdown(wait=True)
        
        print("⛔ Pipeline parado")
    
    async def process_stage(self, task: Task, stage_name: str) -> Any:
        """
        Processa tarefa em um stage específico
        """
        stage = self.stages.get(stage_name)
        if not stage:
            raise ValueError(f"Stage '{stage_name}' não encontrado")
        
        processor = stage['processor']
        use_mp = stage['use_multiprocessing'] and self.enable_multiprocessing
        
        # Atualizar estatísticas
        stage['active_tasks'] += 1
        start_time = time.time()
        
        try:
            # Escolher executor
            if use_mp and self.process_executor:
                # CPU-bound: usar multiprocessing
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self.process_executor,
                    processor,
                    task.data
                )
            elif asyncio.iscoroutinefunction(processor):
                # Async function
                result = await processor(task.data)
            else:
                # Sync function: usar thread pool
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self.thread_executor,
                    processor,
                    task.data
                )
            
            # Atualizar latência
            latency = (time.time() - start_time) * 1000
            stage['avg_latency'] = (stage['avg_latency'] * 0.9) + (latency * 0.1)
            stage['total_processed'] += 1
            
            return result
            
        except Exception as e:
            stage['total_errors'] += 1
            raise e
        finally:
            stage['active_tasks'] -= 1
    
    async def _worker(self, priority: TaskPriority, worker_id: str):
        """Worker que processa tarefas de uma prioridade"""
        queue = self.queues[priority]
        
        while self.running:
            try:
                # Pegar tarefa com timeout
                try:
                    task = await asyncio.wait_for(queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue
                
                # Processar tarefa
                task.started_at = time.time()
                
                try:
                    # Processar através dos stages
                    result = task.data
                    for stage_name in self.stage_order:
                        # Criar cópia da task para o stage
                        stage_task = Task(
                            id=task.id,
                            priority=task.priority,
                            stage=stage_name,
                            data=result,
                            created_at=task.created_at,
                            metadata=task.metadata or {}
                        )
                        result = await self.process_stage(stage_task, stage_name)
                    
                    # Sucesso
                    task.result = result
                    task.completed_at = time.time()
                    
                    with self.lock:
                        self.stats['completed_tasks'] += 1
                        self.completed_tasks.append(task)
                        
                except Exception as e:
                    # Erro - tentar retry
                    task.error = str(e)
                    task.retries += 1
                    
                    if task.retries < task.max_retries:
                        # Re-enqueue com delay
                        await asyncio.sleep(2 ** task.retries)  # Exponential backoff
                        await queue.put(task)
                        
                        with self.lock:
                            self.stats['retried_tasks'] += 1
                    else:
                        # Falha definitiva
                        task.completed_at = time.time()
                        
                        with self.lock:
                            self.stats['failed_tasks'] += 1
                            self.completed_tasks.append(task)
                
                finally:
                    # Remover de in-flight se completou
                    if task.completed_at:
                        with self.lock:
                            self.tasks_in_flight.pop(task.id, None)
                
            except Exception as e:
                print(f"❌ Erro no worker {worker_id}: {e}")
                await asyncio.sleep(1)
    
    async def _monitor(self):
        """Monitor de estatísticas e backpressure"""
        last_completed = 0
        last_time = time.time()
        
        while self.running:
            await asyncio.sleep(5)  # Atualizar a cada 5 segundos
            
            try:
                # Calcular throughput
                now = time.time()
                completed = self.stats['completed_tasks']
                throughput = (completed - last_completed) / (now - last_time)
                self.stats['throughput_per_sec'] = throughput
                
                last_completed = completed
                last_time = now
                
                # Calcular tamanhos de filas
                total_queued = 0
                max_capacity = 0
                
                for priority, queue in self.queues.items():
                    size = queue.qsize()
                    self.stats['queue_sizes'][priority.name] = size
                    total_queued += size
                    max_capacity += queue.maxsize
                
                # Verificar backpressure
                utilization = total_queued / max(1, max_capacity)
                
                if utilization > self.backpressure_threshold:
                    if not self.backpressure_active:
                        self.backpressure_active = True
                        print(f"⚠️ Backpressure ativado (utilização: {utilization:.1%})")
                elif utilization < 0.6 and self.backpressure_active:
                    self.backpressure_active = False
                    print(f"✅ Backpressure desativado (utilização: {utilization:.1%})")
                
                # Calcular latência média
                if self.completed_tasks:
                    recent_tasks = list(self.completed_tasks)[-100:]
                    latencies = [
                        (t.completed_at - t.created_at) * 1000
                        for t in recent_tasks
                        if t.completed_at
                    ]
                    if latencies:
                        self.stats['avg_latency_ms'] = sum(latencies) / len(latencies)
                
                # Worker utilization
                active_workers = sum(
                    stage['active_tasks'] 
                    for stage in self.stages.values()
                )
                self.stats['worker_utilization'] = active_workers / max(1, self.max_workers)
                
            except Exception as e:
                print(f"❌ Erro no monitor: {e}")
    
    async def _wait_for_capacity(self):
        """Aguarda capacidade quando backpressure está ativo"""
        wait_time = 0.1
        max_wait = 10.0
        
        while self.backpressure_active and wait_time < max_wait:
            await asyncio.sleep(wait_time)
            wait_time = min(wait_time * 1.5, max_wait)
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do pipeline"""
        with self.lock:
            stats = dict(self.stats)
            
            # Adicionar estatísticas por stage
            stats['stages'] = {}
            for name, stage in self.stages.items():
                stats['stages'][name] = {
                    'active': stage['active_tasks'],
                    'processed': stage['total_processed'],
                    'errors': stage['total_errors'],
                    'avg_latency_ms': stage['avg_latency']
                }
            
            # Calcular taxa de sucesso
            total = stats['completed_tasks'] + stats['failed_tasks']
            if total > 0:
                stats['success_rate'] = f"{(stats['completed_tasks'] / total) * 100:.2f}%"
            else:
                stats['success_rate'] = "N/A"
            
            return stats
    
    def get_queue_sizes(self) -> Dict[str, int]:
        """Retorna tamanhos atuais das filas"""
        return {
            priority.name: queue.qsize()
            for priority, queue in self.queues.items()
        }


# Funções auxiliares para processamento

def cpu_intensive_processor(data: Any) -> Any:
    """Exemplo de processador CPU-intensive"""
    import hashlib
    
    # Simular processamento pesado
    for _ in range(1000):
        hashlib.sha256(str(data).encode()).hexdigest()
    
    return f"Processed: {data}"

async def async_io_processor(data: Any) -> Any:
    """Exemplo de processador I/O-bound assíncrono"""
    await asyncio.sleep(0.1)  # Simular I/O
    return f"IO processed: {data}"

def sync_processor(data: Any) -> Any:
    """Exemplo de processador síncrono"""
    time.sleep(0.05)  # Simular processamento
    return f"Sync processed: {data}"


# Pipeline singleton global
_pipeline = None

def get_pipeline() -> AsyncPipeline:
    """Retorna instância singleton do pipeline"""
    global _pipeline
    if _pipeline is None:
        _pipeline = AsyncPipeline()
    return _pipeline