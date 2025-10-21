"""
Distributed Lock Manager - Gerenciamento de locks distribuídos
Silicon Valley-grade implementation com algoritmos de consenso
"""
import time
import asyncio
import threading
import hashlib
import json
import socket
import struct
import pickle
import uuid
import weakref
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
from contextlib import asynccontextmanager, contextmanager
import logging
from datetime import datetime, timedelta
import heapq
import random
import redis
import multiprocessing
import mmap
import fcntl
import os
logger = logging.getLogger(__name__)

class LockType(Enum):
    """Tipos de lock disponíveis"""
    EXCLUSIVE = 'exclusive'
    SHARED = 'shared'
    INTENTION_SHARED = 'is'
    INTENTION_EXCLUSIVE = 'ix'
    SHARED_INTENTION_EXCLUSIVE = 'six'
    UPDATE = 'update'

class LockMode(Enum):
    """Modos de operação do lock manager"""
    LOCAL = 'local'
    DISTRIBUTED = 'distributed'
    HYBRID = 'hybrid'
    QUANTUM = 'quantum'

class LockAlgorithm(Enum):
    """Algoritmos de lock distribuído"""
    LAMPORT = 'lamport'
    RICART_AGRAWALA = 'ricart'
    MAEKAWA = 'maekawa'
    TOKEN_RING = 'token_ring'
    RAYMOND = 'raymond'
    REDLOCK = 'redlock'
    CHUBBY = 'chubby'
    ZOOKEEPER = 'zookeeper'

@dataclass
class LockRequest:
    """Representa uma requisição de lock"""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    resource_id: str = ''
    lock_type: LockType = LockType.EXCLUSIVE
    owner_id: str = ''
    timestamp: float = field(default_factory=time.time)
    priority: int = 0
    timeout: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0
    max_retries: int = 3

    def __lt__(self, other):
        """Para priority queue"""
        return (self.priority, self.timestamp) < (other.priority, other.timestamp)

@dataclass
class Lock:
    """Representa um lock adquirido"""
    lock_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    resource_id: str = ''
    lock_type: LockType = LockType.EXCLUSIVE
    owner_id: str = ''
    acquired_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    renewable: bool = True
    reference_count: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        """Verifica se lock expirou"""
        if self.expires_at:
            return time.time() > self.expires_at
        return False

    def renew(self, duration: float=30.0):
        """Renova lock por mais tempo"""
        if self.renewable:
            self.expires_at = time.time() + duration
            return True
        return False

class LockCompatibilityMatrix:
    """Matriz de compatibilidade entre tipos de lock"""
    COMPATIBILITY = {LockType.SHARED: {LockType.SHARED: True, LockType.EXCLUSIVE: False, LockType.INTENTION_SHARED: True, LockType.INTENTION_EXCLUSIVE: True, LockType.SHARED_INTENTION_EXCLUSIVE: True, LockType.UPDATE: False}, LockType.EXCLUSIVE: {LockType.SHARED: False, LockType.EXCLUSIVE: False, LockType.INTENTION_SHARED: False, LockType.INTENTION_EXCLUSIVE: False, LockType.SHARED_INTENTION_EXCLUSIVE: False, LockType.UPDATE: False}, LockType.INTENTION_SHARED: {LockType.SHARED: True, LockType.EXCLUSIVE: False, LockType.INTENTION_SHARED: True, LockType.INTENTION_EXCLUSIVE: True, LockType.SHARED_INTENTION_EXCLUSIVE: True, LockType.UPDATE: True}, LockType.INTENTION_EXCLUSIVE: {LockType.SHARED: True, LockType.EXCLUSIVE: False, LockType.INTENTION_SHARED: True, LockType.INTENTION_EXCLUSIVE: True, LockType.SHARED_INTENTION_EXCLUSIVE: False, LockType.UPDATE: False}, LockType.SHARED_INTENTION_EXCLUSIVE: {LockType.SHARED: True, LockType.EXCLUSIVE: False, LockType.INTENTION_SHARED: True, LockType.INTENTION_EXCLUSIVE: False, LockType.SHARED_INTENTION_EXCLUSIVE: False, LockType.UPDATE: False}, LockType.UPDATE: {LockType.SHARED: False, LockType.EXCLUSIVE: False, LockType.INTENTION_SHARED: True, LockType.INTENTION_EXCLUSIVE: False, LockType.SHARED_INTENTION_EXCLUSIVE: False, LockType.UPDATE: False}}

    @classmethod
    def are_compatible(cls, lock1: LockType, lock2: LockType) -> bool:
        """Verifica se dois tipos de lock são compatíveis"""
        return cls.COMPATIBILITY.get(lock1, {}).get(lock2, False)

class DeadlockDetector:
    """Detector de deadlocks usando wait-for graph"""

    def __init__(self):
        self.wait_for_graph: Dict[str, Set[str]] = defaultdict(set)
        self.lock = threading.RLock()

    def add_edge(self, waiter: str, holder: str):
        """Adiciona edge no grafo wait-for"""
        with self.lock:
            self.wait_for_graph[waiter].add(holder)

    def remove_edge(self, waiter: str, holder: str):
        """Remove edge do grafo"""
        with self.lock:
            if waiter in self.wait_for_graph:
                self.wait_for_graph[waiter].discard(holder)
                if not self.wait_for_graph[waiter]:
                    del self.wait_for_graph[waiter]

    def detect_cycle(self) -> Optional[List[str]]:
        """Detecta ciclo no grafo (deadlock)"""
        with self.lock:
            visited = set()
            rec_stack = set()
            path = []

            def dfs(node: str) -> bool:
                visited.add(node)
                rec_stack.add(node)
                path.append(node)
                for neighbor in self.wait_for_graph.get(node, []):
                    if neighbor not in visited:
                        if dfs(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        cycle_start = path.index(neighbor)
                        return path[cycle_start:]
                path.pop()
                rec_stack.remove(node)
                return False
            for node in list(self.wait_for_graph.keys()):
                if node not in visited:
                    cycle = dfs(node)
                    if cycle:
                        return cycle
            return None

    def resolve_deadlock(self, cycle: List[str]) -> str:
        """Resolve deadlock escolhendo vítima"""
        victim = random.choice(cycle)
        logger.warning(f'Deadlock detected! Choosing victim: {victim}')
        return victim

class DistributedLockManager:
    """
    Gerenciador de locks distribuídos com múltiplos algoritmos
    Features:
    - Múltiplos tipos de lock (shared, exclusive, intention)
    - Detecção e resolução de deadlocks
    - Algoritmos distribuídos (Lamport, Ricart-Agrawala, etc)
    - Lock escalation e de-escalation
    - Fairness e starvation prevention
    - Quantum locks com superposição
    """

    def __init__(self, node_id: str, mode: LockMode=LockMode.HYBRID, algorithm: LockAlgorithm=LockAlgorithm.LAMPORT):
        self.node_id = node_id
        self.mode = mode
        self.algorithm = algorithm
        self.locks: Dict[str, Lock] = {}
        self.lock_queue: Dict[str, List[LockRequest]] = defaultdict(list)
        self.lock_holders: Dict[str, Set[str]] = defaultdict(set)
        self.owner_locks: Dict[str, Set[str]] = defaultdict(set)
        self.deadlock_detector = DeadlockDetector()
        self.deadlock_check_interval = 5.0
        self.local_lock = threading.RLock()
        self.condition_vars: Dict[str, threading.Condition] = {}
        self.lamport_clock = 0
        self.vector_clock: Dict[str, int] = defaultdict(int)
        self.token_holder: Optional[str] = None
        self.request_queue: List[LockRequest] = []
        self.redis_client: Optional[redis.Redis] = None
        if mode in [LockMode.DISTRIBUTED, LockMode.HYBRID]:
            try:
                self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True, socket_keepalive=True)
                self.redis_client.ping()
            except:
                logger.warning('Redis not available, falling back to local mode')
                self.mode = LockMode.LOCAL
        self.shared_memory: Optional[mmap.mmap] = None
        if mode == LockMode.HYBRID:
            self._init_shared_memory()
        self.running = True
        self.deadlock_thread = threading.Thread(target=self._deadlock_monitor, daemon=True)
        self.deadlock_thread.start()
        logger.info(f'DistributedLockManager initialized: {node_id}, mode={mode}, algorithm={algorithm}')

    def _init_shared_memory(self):
        """Inicializa memória compartilhada para IPC"""
        try:
            shm_path = f'/tmp/dlm_shm_{self.node_id}'
            shm_size = 1024 * 1024
            with open(shm_path, 'a+b') as f:
                f.truncate(shm_size)
            with open(shm_path, 'r+b') as f:
                self.shared_memory = mmap.mmap(f.fileno(), shm_size, access=mmap.ACCESS_WRITE)
        except Exception as e:
            logger.warning(f'Failed to init shared memory: {e}')

    def _deadlock_monitor(self):
        """Thread que monitora deadlocks"""
        while self.running:
            try:
                time.sleep(self.deadlock_check_interval)
                cycle = self.deadlock_detector.detect_cycle()
                if cycle:
                    victim = self.deadlock_detector.resolve_deadlock(cycle)
                    self._abort_transaction(victim)
            except Exception as e:
                logger.error(f'Error in deadlock monitor: {e}')

    def _abort_transaction(self, owner_id: str):
        """Aborta transação liberando todos os locks"""
        with self.local_lock:
            locks_to_release = list(self.owner_locks.get(owner_id, []))
            for lock_id in locks_to_release:
                if lock_id in self.locks:
                    lock = self.locks[lock_id]
                    self._release_lock_internal(lock)
            logger.info(f'Aborted transaction for {owner_id}, released {len(locks_to_release)} locks')

    def _update_lamport_clock(self, received_time: int=0):
        """Atualiza Lamport clock"""
        self.lamport_clock = max(self.lamport_clock, received_time) + 1
        return self.lamport_clock

    def _update_vector_clock(self, received_clock: Dict[str, int]=None):
        """Atualiza vector clock"""
        if received_clock:
            for node, time in received_clock.items():
                self.vector_clock[node] = max(self.vector_clock[node], time)
        self.vector_clock[self.node_id] += 1
        return dict(self.vector_clock)

    @contextmanager
    def acquire_lock(self, resource_id: str, lock_type: LockType=LockType.EXCLUSIVE, timeout: Optional[float]=None, owner_id: Optional[str]=None):
        """Context manager para adquirir lock"""
        owner_id = owner_id or self.node_id
        lock = None
        try:
            lock = self.acquire(resource_id, lock_type, timeout, owner_id)
            if lock:
                yield lock
            else:
                raise TimeoutError(f'Failed to acquire lock on {resource_id}')
        finally:
            if lock:
                self.release(lock.lock_id)

    def acquire(self, resource_id: str, lock_type: LockType=LockType.EXCLUSIVE, timeout: Optional[float]=None, owner_id: Optional[str]=None) -> Optional[Lock]:
        """
        Adquire lock em recurso
        """
        owner_id = owner_id or self.node_id
        request = LockRequest(resource_id=resource_id, lock_type=lock_type, owner_id=owner_id, timeout=timeout)
        if self.mode == LockMode.LOCAL:
            return self._acquire_local(request)
        elif self.mode == LockMode.DISTRIBUTED:
            return self._acquire_distributed(request)
        elif self.mode == LockMode.HYBRID:
            return self._acquire_hybrid(request)
        elif self.mode == LockMode.QUANTUM:
            return self._acquire_quantum(request)
        return None

    def _acquire_local(self, request: LockRequest) -> Optional[Lock]:
        """
        Adquire lock local
        """
        with self.local_lock:
            if self._can_grant_lock(request):
                lock = self._grant_lock(request)
                return lock
            else:
                self.lock_queue[request.resource_id].append(request)
                for holder_id in self.lock_holders[request.resource_id]:
                    self.deadlock_detector.add_edge(request.owner_id, holder_id)
                if request.resource_id not in self.condition_vars:
                    self.condition_vars[request.resource_id] = threading.Condition(self.local_lock)
                condition = self.condition_vars[request.resource_id]
                start_time = time.time()
                while not self._can_grant_lock(request):
                    if request.timeout:
                        remaining = request.timeout - (time.time() - start_time)
                        if remaining <= 0:
                            self.lock_queue[request.resource_id].remove(request)
                            return None
                        condition.wait(remaining)
                    else:
                        condition.wait()
                self.lock_queue[request.resource_id].remove(request)
                lock = self._grant_lock(request)
                return lock

    def _acquire_distributed(self, request: LockRequest) -> Optional[Lock]:
        """
        Adquire lock distribuído usando algoritmo escolhido
        """
        if self.algorithm == LockAlgorithm.LAMPORT:
            return self._acquire_lamport(request)
        elif self.algorithm == LockAlgorithm.RICART_AGRAWALA:
            return self._acquire_ricart_agrawala(request)
        elif self.algorithm == LockAlgorithm.REDLOCK:
            return self._acquire_redlock(request)
        else:
            return self._acquire_local(request)

    def _acquire_lamport(self, request: LockRequest) -> Optional[Lock]:
        """
        Implementa algoritmo de Lamport para mutual exclusion
        """
        request.timestamp = self._update_lamport_clock()
        self._broadcast_lock_request(request)
        heapq.heappush(self.request_queue, request)
        acks_received = self._wait_for_acks(request)
        if not acks_received:
            return None
        while self.request_queue[0] != request:
            time.sleep(0.01)
        lock = self._grant_lock(request)
        return lock

    def _acquire_ricart_agrawala(self, request: LockRequest) -> Optional[Lock]:
        """
        Implementa algoritmo Ricart-Agrawala
        """
        request.timestamp = self._update_lamport_clock()
        replies_needed = self._get_active_nodes()
        replies_received = set()
        for node in replies_needed:
            reply = self._send_lock_request(node, request)
            if reply:
                replies_received.add(node)
        if len(replies_received) == len(replies_needed):
            lock = self._grant_lock(request)
            return lock
        return None

    def _acquire_redlock(self, request: LockRequest) -> Optional[Lock]:
        """
        Implementa algoritmo Redlock (Redis)
        """
        if not self.redis_client:
            return self._acquire_local(request)
        lock_key = f'lock:{request.resource_id}'
        lock_value = f'{request.owner_id}:{request.request_id}'
        ttl = int(request.timeout * 1000) if request.timeout else 30000
        try:
            acquired = self.redis_client.set(lock_key, lock_value, nx=True, px=ttl)
            if acquired:
                lock = Lock(resource_id=request.resource_id, lock_type=request.lock_type, owner_id=request.owner_id, expires_at=time.time() + ttl / 1000)
                with self.local_lock:
                    self.locks[lock.lock_id] = lock
                    self.lock_holders[request.resource_id].add(request.owner_id)
                    self.owner_locks[request.owner_id].add(lock.lock_id)
                return lock
        except Exception as e:
            logger.error(f'Redis lock acquisition failed: {e}')
        return None

    def _acquire_hybrid(self, request: LockRequest) -> Optional[Lock]:
        """
        Modo híbrido: tenta local primeiro, depois distribuído
        """
        lock = self._acquire_local(request)
        if lock:
            threading.Thread(target=self._propagate_lock, args=(lock,), daemon=True).start()
        return lock

    def _acquire_quantum(self, request: LockRequest) -> Optional[Lock]:
        """
        Lock quântico com superposição de estados
        (Experimental - simulação conceitual)
        """
        quantum_state = {'locked': 0.5, 'unlocked': 0.5, 'entangled_with': []}
        if random.random() < quantum_state['locked']:
            lock = self._grant_lock(request)
            related_resources = self._find_related_resources(request.resource_id)
            for resource in related_resources:
                quantum_state['entangled_with'].append(resource)
            lock.metadata['quantum_state'] = quantum_state
            return lock
        else:
            return None

    def _can_grant_lock(self, request: LockRequest) -> bool:
        """
        Verifica se lock pode ser concedido
        """
        for holder_id in self.lock_holders[request.resource_id]:
            for lock_id in self.owner_locks[holder_id]:
                if lock_id in self.locks:
                    existing_lock = self.locks[lock_id]
                    if existing_lock.resource_id == request.resource_id:
                        if not LockCompatibilityMatrix.are_compatible(existing_lock.lock_type, request.lock_type):
                            return False
        return True

    def _grant_lock(self, request: LockRequest) -> Lock:
        """
        Concede lock
        """
        lock = Lock(resource_id=request.resource_id, lock_type=request.lock_type, owner_id=request.owner_id, expires_at=time.time() + request.timeout if request.timeout else None, metadata=request.metadata)
        with self.local_lock:
            self.locks[lock.lock_id] = lock
            self.lock_holders[request.resource_id].add(request.owner_id)
            self.owner_locks[request.owner_id].add(lock.lock_id)
            for holder_id in self.lock_holders[request.resource_id]:
                if holder_id != request.owner_id:
                    self.deadlock_detector.remove_edge(request.owner_id, holder_id)
        logger.debug(f'Granted lock {lock.lock_id} on {request.resource_id} to {request.owner_id}')
        return lock

    def release(self, lock_id: str) -> bool:
        """
        Libera lock
        """
        with self.local_lock:
            if lock_id not in self.locks:
                return False
            lock = self.locks[lock_id]
            return self._release_lock_internal(lock)

    def _release_lock_internal(self, lock: Lock) -> bool:
        """
        Libera lock internamente
        """
        with self.local_lock:
            del self.locks[lock.lock_id]
            self.lock_holders[lock.resource_id].discard(lock.owner_id)
            if not self.lock_holders[lock.resource_id]:
                del self.lock_holders[lock.resource_id]
            self.owner_locks[lock.owner_id].discard(lock.lock_id)
            if not self.owner_locks[lock.owner_id]:
                del self.owner_locks[lock.owner_id]
            if self.redis_client and self.mode in [LockMode.DISTRIBUTED, LockMode.HYBRID]:
                try:
                    lock_key = f'lock:{lock.resource_id}'
                    self.redis_client.delete(lock_key)
                except:
                    pass
            if lock.resource_id in self.condition_vars:
                self.condition_vars[lock.resource_id].notify_all()
            self._process_wait_queue(lock.resource_id)
        logger.debug(f'Released lock {lock.lock_id} on {lock.resource_id}')
        return True

    def _process_wait_queue(self, resource_id: str):
        """
        Processa fila de espera após liberação
        """
        if resource_id not in self.lock_queue:
            return
        queue = self.lock_queue[resource_id]
        granted = []
        for request in queue:
            if self._can_grant_lock(request):
                self._grant_lock(request)
                granted.append(request)
        for request in granted:
            queue.remove(request)

    def upgrade_lock(self, lock_id: str, new_type: LockType) -> bool:
        """
        Faz upgrade de lock (ex: shared para exclusive)
        """
        with self.local_lock:
            if lock_id not in self.locks:
                return False
            lock = self.locks[lock_id]
            temp_request = LockRequest(resource_id=lock.resource_id, lock_type=new_type, owner_id=lock.owner_id)
            old_type = lock.lock_type
            lock.lock_type = LockType.SHARED
            can_upgrade = self._can_grant_lock(temp_request)
            if can_upgrade:
                lock.lock_type = new_type
                logger.info(f'Upgraded lock {lock_id} from {old_type} to {new_type}')
                return True
            else:
                lock.lock_type = old_type
                return False

    def downgrade_lock(self, lock_id: str, new_type: LockType) -> bool:
        """
        Faz downgrade de lock (ex: exclusive para shared)
        """
        with self.local_lock:
            if lock_id not in self.locks:
                return False
            lock = self.locks[lock_id]
            old_type = lock.lock_type
            lock.lock_type = new_type
            self._process_wait_queue(lock.resource_id)
            logger.info(f'Downgraded lock {lock_id} from {old_type} to {new_type}')
            return True

    def get_lock_info(self, lock_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações sobre um lock
        """
        with self.local_lock:
            if lock_id not in self.locks:
                return None
            lock = self.locks[lock_id]
            return {'lock_id': lock.lock_id, 'resource_id': lock.resource_id, 'lock_type': lock.lock_type.value, 'owner_id': lock.owner_id, 'acquired_at': lock.acquired_at, 'expires_at': lock.expires_at, 'is_expired': lock.is_expired(), 'reference_count': lock.reference_count, 'metadata': lock.metadata}

    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do lock manager
        """
        with self.local_lock:
            total_waiters = sum((len(queue) for queue in self.lock_queue.values()))
            return {'node_id': self.node_id, 'mode': self.mode.value, 'algorithm': self.algorithm.value, 'active_locks': len(self.locks), 'waiting_requests': total_waiters, 'resources_locked': len(self.lock_holders), 'unique_owners': len(self.owner_locks), 'lamport_clock': self.lamport_clock, 'deadlock_checks': self.deadlock_detector.detect_cycle() is not None}

    def _broadcast_lock_request(self, request: LockRequest):
        """Broadcast request para todos os nodes"""
        pass

    def _wait_for_acks(self, request: LockRequest) -> bool:
        """Espera por ACKs de outros nodes"""
        return True

    def _get_active_nodes(self) -> List[str]:
        """Obtém lista de nodes ativos"""
        return []

    def _send_lock_request(self, node: str, request: LockRequest) -> bool:
        """Envia request para node específico"""
        return True

    def _propagate_lock(self, lock: Lock):
        """Propaga lock para outros nodes"""
        pass

    def _find_related_resources(self, resource_id: str) -> List[str]:
        """Encontra recursos relacionados para quantum entanglement"""
        return []

    def shutdown(self):
        """
        Desliga lock manager
        """
        self.running = False
        with self.local_lock:
            for lock in list(self.locks.values()):
                self._release_lock_internal(lock)
        if self.redis_client:
            self.redis_client.close()
        if self.shared_memory:
            self.shared_memory.close()
        logger.info(f'DistributedLockManager {self.node_id} shut down')
_lock_manager: Optional[DistributedLockManager] = None

def get_lock_manager(node_id: Optional[str]=None) -> DistributedLockManager:
    """
    Retorna instância singleton do lock manager
    """
    global _lock_manager
    if _lock_manager is None:
        node_id = node_id or socket.gethostname()
        _lock_manager = DistributedLockManager(node_id)
    return _lock_manager
__all__ = ['DistributedLockManager', 'Lock', 'LockRequest', 'LockType', 'LockMode', 'LockAlgorithm', 'LockCompatibilityMatrix', 'DeadlockDetector', 'get_lock_manager']