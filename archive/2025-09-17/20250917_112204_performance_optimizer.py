"""
Performance Optimizer - Otimizações específicas para Mac Studio M3 Ultra.
Inclui paralelização, batching e gestão inteligente de recursos.
"""
import asyncio
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, Dict, Any, Callable, Optional, Union
from functools import wraps
import time
import logging
from threading import Semaphore
import multiprocessing as mp
logger = logging.getLogger(__name__)
M3_ULTRA_CORES = 24
M3_ULTRA_GPU_CORES = 60
M3_ULTRA_RAM_GB = 96

class PerformanceOptimizer:
    """
    Otimizador de performance para ScriptureMon.
    Maximiza uso do hardware M3 Ultra.
    """

    def __init__(self):
        """Inicializa o otimizador."""
        self.cpu_executor = ThreadPoolExecutor(max_workers=M3_ULTRA_CORES, thread_name_prefix='scripturemon-cpu')
        self.process_executor = ProcessPoolExecutor(max_workers=M3_ULTRA_CORES // 2)
        self.model_semaphore = Semaphore(4)
        self.memory_semaphore = Semaphore(8)
        self.batch_configs = {'embeddings': {'size': 32, 'timeout': 0.1}, 'sentiment': {'size': 64, 'timeout': 0.05}, 'ollama': {'size': 4, 'timeout': 0.5}}
        self.pending_batches = {}
        logger.info(f'PerformanceOptimizer initialized for M3 Ultra: {M3_ULTRA_CORES} cores, {M3_ULTRA_RAM_GB}GB RAM')

    def parallel_map(self, func: Callable, items: List[Any], max_workers: Optional[int]=None, use_processes: bool=False) -> List[Any]:
        """
        Executa função em paralelo sobre lista de itens.

        Args:
            func: Função a executar
            items: Lista de itens
            max_workers: Número máximo de workers
            use_processes: Usar processos ao invés de threads

        Returns:
            Lista de resultados
        """
        if not items:
            return []
        executor = self.process_executor if use_processes else self.cpu_executor
        if max_workers is None:
            max_workers = min(len(items), M3_ULTRA_CORES)
        start_time = time.time()
        try:
            futures = [executor.submit(func, item) for item in items]
            results = []
            for future in concurrent.futures.as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    logger.error(f'Error in parallel execution: {e}')
                    results.append(None)
            elapsed = time.time() - start_time
            logger.debug(f'Parallel map completed {len(items)} items in {elapsed:.2f}s')
            return results
        except Exception as e:
            logger.error(f'Parallel map failed: {e}')
            return [func(item) for item in items]

    def batch_process(self, batch_type: str, item: Any, processor: Callable) -> concurrent.futures.Future:
        """
        Adiciona item para processamento em batch.

        Args:
            batch_type: Tipo do batch
            item: Item a processar
            processor: Função processadora

        Returns:
            Future com resultado
        """
        if batch_type not in self.batch_configs:
            future = concurrent.futures.Future()
            result = processor([item])[0]
            future.set_result(result)
            return future
        config = self.batch_configs[batch_type]
        if batch_type not in self.pending_batches:
            self.pending_batches[batch_type] = {'items': [], 'futures': [], 'processor': processor, 'timer': None}
        batch = self.pending_batches[batch_type]
        future = concurrent.futures.Future()
        batch['items'].append(item)
        batch['futures'].append(future)
        if len(batch['items']) >= config['size']:
            self._process_batch(batch_type)
        elif batch['timer'] is None:
            batch['timer'] = self.cpu_executor.submit(self._batch_timeout, batch_type, config['timeout'])
        return future

    def _batch_timeout(self, batch_type: str, timeout: float):
        """Processa batch após timeout."""
        time.sleep(timeout)
        self._process_batch(batch_type)

    def _process_batch(self, batch_type: str):
        """Processa batch pendente."""
        if batch_type not in self.pending_batches:
            return
        batch = self.pending_batches.pop(batch_type)
        if not batch['items']:
            return
        try:
            results = batch['processor'](batch['items'])
            for future, result in zip(batch['futures'], results):
                future.set_result(result)
        except Exception as e:
            for future in batch['futures']:
                future.set_exception(e)

    def optimize_ollama_calls(self, models: List[str], prompts: List[str]) -> List[str]:
        """
        Otimiza chamadas para múltiplos modelos Ollama.

        Args:
            models: Lista de modelos
            prompts: Lista de prompts

        Returns:
            Lista de respostas
        """
        results = []
        model_groups = {}
        for model, prompt in zip(models, prompts):
            if model not in model_groups:
                model_groups[model] = []
            model_groups[model].append(prompt)
        futures = []
        for model, group_prompts in model_groups.items():
            with self.model_semaphore:
                future = self.cpu_executor.submit(self._process_model_group, model, group_prompts)
                futures.append((model, future))
        model_results = {}
        for model, future in futures:
            model_results[model] = future.result()
        for model, prompt in zip(models, prompts):
            group_results = model_results[model]
            results.append(group_results.pop(0))
        return results

    def _process_model_group(self, model: str, prompts: List[str]) -> List[str]:
        """Processa grupo de prompts para um modelo."""
        from .ollama_core import OllamaCore
        ollama = OllamaCore()
        results = []
        for prompt in prompts:
            try:
                response = ollama.generate(prompt, model=model)
                results.append(response)
            except Exception as e:
                logger.error(f'Error processing prompt with {model}: {e}')
                results.append(f'Error: {e}')
        return results

    def optimize_memory_access(self, operations: List[Callable]) -> List[Any]:
        """
        Otimiza acessos à memória agrupando operações.

        Args:
            operations: Lista de operações de memória

        Returns:
            Lista de resultados
        """
        results = []
        read_ops = []
        write_ops = []
        search_ops = []
        for op in operations:
            op_name = op.__name__ if hasattr(op, '__name__') else str(op)
            if 'read' in op_name or 'get' in op_name:
                read_ops.append(op)
            elif 'write' in op_name or 'save' in op_name:
                write_ops.append(op)
            else:
                search_ops.append(op)
        if read_ops:
            with self.memory_semaphore:
                read_results = self.parallel_map(lambda op: op(), read_ops)
                results.extend(read_results)
        if search_ops:
            with self.memory_semaphore:
                search_results = self.parallel_map(lambda op: op(), search_ops)
                results.extend(search_results)
        for write_op in write_ops:
            with self.memory_semaphore:
                results.append(write_op())
        return results

    def profile_function(self, func: Callable) -> Callable:
        """
        Decorator para profile de funções.

        Usage:
            @optimizer.profile_function
            def my_function():
                pass
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = self._get_memory_usage()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                memory_delta = self._get_memory_usage() - start_memory
                logger.info(f'Profile {func.__name__}: {elapsed:.3f}s, {memory_delta:.1f}MB')
                if elapsed > 1.0:
                    logger.warning(f'Slow function {func.__name__}: {elapsed:.3f}s')
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f'Function {func.__name__} failed after {elapsed:.3f}s: {e}')
                raise
        return wrapper

    def _get_memory_usage(self) -> float:
        """Retorna uso de memória em MB."""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        except:
            return 0

    async def async_parallel(self, coroutines: List) -> List[Any]:
        """
        Executa coroutines em paralelo.

        Args:
            coroutines: Lista de coroutines

        Returns:
            Lista de resultados
        """
        return await asyncio.gather(*coroutines, return_exceptions=True)

    def shutdown(self):
        """Encerra o otimizador."""
        self.cpu_executor.shutdown(wait=True)
        self.process_executor.shutdown(wait=True)
        logger.info('PerformanceOptimizer shutdown complete')

class BatchProcessor:
    """
    Processador de batches otimizado.
    """

    def __init__(self, batch_size: int=32, timeout: float=0.1):
        """
        Inicializa processador de batch.

        Args:
            batch_size: Tamanho do batch
            timeout: Timeout em segundos
        """
        self.batch_size = batch_size
        self.timeout = timeout
        self.pending_items = []
        self.pending_futures = []
        self.executor = ThreadPoolExecutor(max_workers=4)

    def add(self, item: Any) -> concurrent.futures.Future:
        """
        Adiciona item ao batch.

        Args:
            item: Item a processar

        Returns:
            Future com resultado
        """
        future = concurrent.futures.Future()
        self.pending_items.append(item)
        self.pending_futures.append(future)
        if len(self.pending_items) >= self.batch_size:
            self._process_batch()
        return future

    def _process_batch(self):
        """Processa batch pendente."""
        if not self.pending_items:
            return
        items = self.pending_items
        futures = self.pending_futures
        self.pending_items = []
        self.pending_futures = []
        self.executor.submit(self._do_process, items, futures)

    def _do_process(self, items: List[Any], futures: List[concurrent.futures.Future]):
        """Executa processamento do batch."""
        try:
            results = [self._process_item(item) for item in items]
            for future, result in zip(futures, results):
                future.set_result(result)
        except Exception as e:
            for future in futures:
                future.set_exception(e)

    def _process_item(self, item: Any) -> Any:
        """Processa item individual."""
        return item
_optimizer: Optional[PerformanceOptimizer] = None

def get_optimizer() -> PerformanceOptimizer:
    """Retorna instância singleton do optimizer."""
    global _optimizer
    if _optimizer is None:
        _optimizer = PerformanceOptimizer()
    return _optimizer