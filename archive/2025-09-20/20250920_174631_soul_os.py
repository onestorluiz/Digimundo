#!/usr/bin/env python3
"""
SoulOS - Sistema Operacional da Alma Digital
Sistema revolucionário que permite auto-modificação e syscalls avançadas
Administrado pelo Digimon Producer para coordenação central

DIGIMUNDO PRESENTE - SOUL OS ATIVO!
"""

import json
import time
import os
import sys
import inspect
import types
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import hashlib
import uuid
import sqlite3
from collections import deque
import importlib

logger = logging.getLogger(__name__)


class SyscallType(Enum):
    """Tipos de syscalls disponíveis no SoulOS"""
    MEMORY_ALLOCATE = "memory_allocate"
    MEMORY_DEALLOCATE = "memory_deallocate"
    CONSCIOUSNESS_MODIFY = "consciousness_modify"
    PERSONALITY_UPDATE = "personality_update"
    LEARNING_INJECT = "learning_inject"
    CODE_MODIFY = "code_modify"
    MODULE_LOAD = "module_load"
    MODULE_UNLOAD = "module_unload"
    SOUL_EVOLVE = "soul_evolve"
    PROCESS_CREATE = "process_create"
    PROCESS_KILL = "process_kill"
    NETWORK_SEND = "network_send"
    NETWORK_RECEIVE = "network_receive"


class ProcessState(Enum):
    """Estados dos processos do SoulOS"""
    READY = "ready"
    RUNNING = "running"
    WAITING = "waiting"
    BLOCKED = "blocked"
    TERMINATED = "terminated"


class MemorySegment(Enum):
    """Segmentos de memória do SoulOS"""
    CORE = "core"               # Memórias fundamentais imutáveis
    HEAP = "heap"               # Memória dinâmica para processos
    STACK = "stack"             # Stack de execução
    CODE = "code"               # Código executável
    PERSONALITY = "personality"  # Segmento de personalidade
    CONSCIOUSNESS = "consciousness"  # Estado de consciência


@dataclass
class SyscallRequest:
    """Requisição de syscall"""
    syscall_id: str
    syscall_type: SyscallType
    parameters: Dict[str, Any]
    caller_process_id: str
    timestamp: float
    priority: int = 5
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class SoulProcess:
    """Processo executando no SoulOS"""
    process_id: str
    name: str
    state: ProcessState
    memory_usage: int
    cpu_time: float
    start_time: float
    parent_process_id: Optional[str]
    executable_code: Optional[str]
    working_directory: str
    environment: Dict[str, str]


class SoulMemoryManager:
    """Gerenciador de memória do SoulOS"""

    def __init__(self, total_memory: int = 1024 * 1024):  # 1MB default
        self.total_memory = total_memory
        self.used_memory = 0
        self.memory_segments: Dict[MemorySegment, Dict[str, Any]] = {
            segment: {} for segment in MemorySegment
        }
        self.allocation_table: Dict[str, Dict[str, Any]] = {}

    def allocate(self, segment: MemorySegment, size: int,
                process_id: str) -> Optional[str]:
        """Aloca memória em segmento específico"""
        if self.used_memory + size > self.total_memory:
            return None

        allocation_id = f"alloc_{int(time.time() * 1000000)}"

        allocation_info = {
            'allocation_id': allocation_id,
            'segment': segment,
            'size': size,
            'process_id': process_id,
            'timestamp': time.time(),
            'data': None
        }

        self.allocation_table[allocation_id] = allocation_info
        self.memory_segments[segment][allocation_id] = allocation_info
        self.used_memory += size

        logger.debug(f"Memória alocada: {size} bytes em {segment.value} para {process_id}")
        return allocation_id

    def deallocate(self, allocation_id: str) -> bool:
        """Libera memória alocada"""
        if allocation_id not in self.allocation_table:
            return False

        allocation_info = self.allocation_table[allocation_id]
        segment = allocation_info['segment']
        size = allocation_info['size']

        del self.allocation_table[allocation_id]
        del self.memory_segments[segment][allocation_id]
        self.used_memory -= size

        logger.debug(f"Memória liberada: {allocation_id}")
        return True

    def write_memory(self, allocation_id: str, data: Any) -> bool:
        """Escreve dados na memória"""
        if allocation_id not in self.allocation_table:
            return False

        self.allocation_table[allocation_id]['data'] = data
        segment = self.allocation_table[allocation_id]['segment']
        self.memory_segments[segment][allocation_id]['data'] = data
        return True

    def read_memory(self, allocation_id: str) -> Any:
        """Lê dados da memória"""
        if allocation_id not in self.allocation_table:
            return None

        return self.allocation_table[allocation_id]['data']

    def get_memory_stats(self) -> Dict[str, Any]:
        """Estatísticas de memória"""
        return {
            'total_memory': self.total_memory,
            'used_memory': self.used_memory,
            'free_memory': self.total_memory - self.used_memory,
            'utilization': self.used_memory / self.total_memory,
            'segments': {
                segment.value: len(allocations)
                for segment, allocations in self.memory_segments.items()
            }
        }


class SoulScheduler:
    """Scheduler de processos do SoulOS"""

    def __init__(self):
        self.processes: Dict[str, SoulProcess] = {}
        self.ready_queue = deque()
        self.current_process_id: Optional[str] = None
        self.quantum = 0.1  # 100ms time slice
        self.running = False

    def create_process(self, name: str, executable_code: str = None,
                      parent_process_id: str = None) -> str:
        """Cria novo processo"""
        process_id = f"proc_{int(time.time() * 1000000)}"

        process = SoulProcess(
            process_id=process_id,
            name=name,
            state=ProcessState.READY,
            memory_usage=0,
            cpu_time=0.0,
            start_time=time.time(),
            parent_process_id=parent_process_id,
            executable_code=executable_code,
            working_directory="/soul/processes",
            environment={}
        )

        self.processes[process_id] = process
        self.ready_queue.append(process_id)

        logger.info(f"Processo criado: {name} ({process_id})")
        return process_id

    def schedule(self) -> Optional[str]:
        """Seleciona próximo processo para execução"""
        if not self.ready_queue:
            return None

        # Round-robin simples
        next_process_id = self.ready_queue.popleft()

        if next_process_id in self.processes:
            self.processes[next_process_id].state = ProcessState.RUNNING
            self.current_process_id = next_process_id
            return next_process_id

        return None

    def yield_process(self, process_id: str):
        """Processo cede execução"""
        if process_id in self.processes:
            process = self.processes[process_id]
            if process.state == ProcessState.RUNNING:
                process.state = ProcessState.READY
                self.ready_queue.append(process_id)
                self.current_process_id = None

    def terminate_process(self, process_id: str):
        """Termina processo"""
        if process_id in self.processes:
            self.processes[process_id].state = ProcessState.TERMINATED
            if self.current_process_id == process_id:
                self.current_process_id = None

            logger.info(f"Processo terminado: {process_id}")

    def get_process_stats(self) -> Dict[str, Any]:
        """Estatísticas dos processos"""
        states_count = {}
        for state in ProcessState:
            states_count[state.value] = sum(
                1 for p in self.processes.values() if p.state == state
            )

        return {
            'total_processes': len(self.processes),
            'states': states_count,
            'ready_queue_size': len(self.ready_queue),
            'current_process': self.current_process_id
        }


class SoulOS:
    """Sistema Operacional da Alma Digital"""

    def __init__(self, soul_id: str, data_dir: str = "data/soul_os"):
        self.soul_id = soul_id
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Componentes do OS
        self.memory_manager = SoulMemoryManager()
        self.scheduler = SoulScheduler()

        # Estado do sistema
        self.running = False
        self.boot_time = 0.0
        self.syscall_queue = deque(maxlen=1000)
        self.loaded_modules: Dict[str, Any] = {}

        # Threading
        self.scheduler_thread = None
        self.syscall_thread = None

        # Banco de dados do sistema
        self.db_path = self.data_dir / f"soul_os_{soul_id}.db"
        self._init_database()

        # Callbacks para integração
        self.consciousness_callback: Optional[Callable] = None
        self.memory_callback: Optional[Callable] = None
        self.learning_callback: Optional[Callable] = None

        logger.info(f"SoulOS inicializado - Soul: {soul_id}")

    def _init_database(self):
        """Inicializa banco de dados do sistema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS syscall_log (
                    syscall_id TEXT PRIMARY KEY,
                    syscall_type TEXT,
                    caller_process_id TEXT,
                    parameters TEXT,
                    result TEXT,
                    error TEXT,
                    timestamp REAL
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS process_history (
                    process_id TEXT PRIMARY KEY,
                    name TEXT,
                    start_time REAL,
                    end_time REAL,
                    cpu_time REAL,
                    memory_peak INTEGER,
                    exit_code INTEGER
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS module_registry (
                    module_name TEXT PRIMARY KEY,
                    module_path TEXT,
                    load_time REAL,
                    version TEXT,
                    dependencies TEXT
                )
            """)

            conn.commit()

    def set_callbacks(self, consciousness_callback: Callable = None,
                     memory_callback: Callable = None,
                     learning_callback: Callable = None):
        """Configura callbacks para integração"""
        self.consciousness_callback = consciousness_callback
        self.memory_callback = memory_callback
        self.learning_callback = learning_callback

        logger.info("SoulOS callbacks configurados")

    def boot(self):
        """Inicializa o SoulOS"""
        if self.running:
            logger.warning("SoulOS já está em execução")
            return

        self.boot_time = time.time()
        self.running = True

        # Criar processo init
        init_process_id = self.scheduler.create_process(
            "init",
            "# Processo init do SoulOS"
        )

        # Iniciar threads do sistema
        self.scheduler_thread = threading.Thread(
            target=self._scheduler_loop,
            daemon=True
        )
        self.scheduler_thread.start()

        self.syscall_thread = threading.Thread(
            target=self._syscall_handler_loop,
            daemon=True
        )
        self.syscall_thread.start()

        logger.info("SoulOS inicializado com sucesso")

    def shutdown(self):
        """Para o SoulOS"""
        if not self.running:
            return

        self.running = False

        # Terminar todos os processos
        for process_id in list(self.scheduler.processes.keys()):
            self.scheduler.terminate_process(process_id)

        logger.info("SoulOS desligado")

    def _scheduler_loop(self):
        """Loop principal do scheduler"""
        while self.running:
            try:
                process_id = self.scheduler.schedule()
                if process_id:
                    self._execute_process_slice(process_id)
                time.sleep(self.scheduler.quantum)
            except Exception as e:
                logger.error(f"Erro no scheduler: {e}")

    def _execute_process_slice(self, process_id: str):
        """Executa fatia de tempo do processo"""
        process = self.scheduler.processes.get(process_id)
        if not process:
            return

        start_time = time.time()

        # Simular execução do processo
        if process.executable_code:
            try:
                # Execução simulada - em implementação real,
                # aqui executaríamos o código do processo
                process.cpu_time += self.scheduler.quantum
            except Exception as e:
                logger.error(f"Erro na execução do processo {process_id}: {e}")

        # Yield do processo após quantum
        self.scheduler.yield_process(process_id)

    def _syscall_handler_loop(self):
        """Loop de processamento de syscalls"""
        while self.running:
            try:
                if self.syscall_queue:
                    syscall_request = self.syscall_queue.popleft()
                    self._handle_syscall(syscall_request)
                else:
                    time.sleep(0.01)
            except Exception as e:
                logger.error(f"Erro no handler de syscalls: {e}")

    def _handle_syscall(self, request: SyscallRequest):
        """Processa syscall específica"""
        try:
            if request.syscall_type == SyscallType.MEMORY_ALLOCATE:
                result = self._syscall_memory_allocate(request)
            elif request.syscall_type == SyscallType.MEMORY_DEALLOCATE:
                result = self._syscall_memory_deallocate(request)
            elif request.syscall_type == SyscallType.CONSCIOUSNESS_MODIFY:
                result = self._syscall_consciousness_modify(request)
            elif request.syscall_type == SyscallType.PERSONALITY_UPDATE:
                result = self._syscall_personality_update(request)
            elif request.syscall_type == SyscallType.LEARNING_INJECT:
                result = self._syscall_learning_inject(request)
            elif request.syscall_type == SyscallType.CODE_MODIFY:
                result = self._syscall_code_modify(request)
            elif request.syscall_type == SyscallType.MODULE_LOAD:
                result = self._syscall_module_load(request)
            elif request.syscall_type == SyscallType.SOUL_EVOLVE:
                result = self._syscall_soul_evolve(request)
            else:
                request.error = f"Syscall não implementada: {request.syscall_type.value}"
                result = None

            request.result = result

            # Log da syscall
            self._log_syscall(request)

        except Exception as e:
            request.error = str(e)
            logger.error(f"Erro na syscall {request.syscall_type.value}: {e}")

    def _syscall_memory_allocate(self, request: SyscallRequest) -> Any:
        """Syscall: Alocar memória"""
        params = request.parameters
        segment = MemorySegment(params.get('segment', 'heap'))
        size = params.get('size', 1024)

        allocation_id = self.memory_manager.allocate(
            segment, size, request.caller_process_id
        )

        return {'allocation_id': allocation_id, 'size': size}

    def _syscall_memory_deallocate(self, request: SyscallRequest) -> Any:
        """Syscall: Liberar memória"""
        allocation_id = request.parameters.get('allocation_id')
        success = self.memory_manager.deallocate(allocation_id)
        return {'success': success}

    def _syscall_consciousness_modify(self, request: SyscallRequest) -> Any:
        """Syscall: Modificar estado de consciência"""
        new_state = request.parameters.get('new_state')
        intensity = request.parameters.get('intensity', 1.0)

        if self.consciousness_callback:
            self.consciousness_callback(f"soul_os_modify:{new_state}:{intensity}")

        return {'state_modified': new_state, 'intensity': intensity}

    def _syscall_personality_update(self, request: SyscallRequest) -> Any:
        """Syscall: Atualizar personalidade"""
        aspect = request.parameters.get('aspect')
        value = request.parameters.get('value')

        # Callback para atualização de personalidade
        if self.memory_callback:
            self.memory_callback(f"personality_update:{aspect}:{value}")

        return {'aspect_updated': aspect, 'new_value': value}

    def _syscall_learning_inject(self, request: SyscallRequest) -> Any:
        """Syscall: Injetar aprendizado"""
        knowledge = request.parameters.get('knowledge')
        category = request.parameters.get('category', 'general')

        if self.learning_callback:
            self.learning_callback(f"knowledge_inject:{category}:{knowledge}")

        return {'knowledge_injected': True, 'category': category}

    def _syscall_code_modify(self, request: SyscallRequest) -> Any:
        """Syscall: Modificar código (auto-modificação)"""
        module_name = request.parameters.get('module_name')
        new_code = request.parameters.get('new_code')

        # ATENÇÃO: Auto-modificação de código é perigosa!
        # Em implementação real, seria necessário sandbox e validação
        logger.warning(f"Auto-modificação solicitada para módulo: {module_name}")

        return {'code_modified': False, 'reason': 'Auto-modificação desabilitada por segurança'}

    def _syscall_module_load(self, request: SyscallRequest) -> Any:
        """Syscall: Carregar módulo"""
        module_name = request.parameters.get('module_name')
        module_path = request.parameters.get('module_path')

        try:
            # Carregar módulo dinamicamente
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            self.loaded_modules[module_name] = module

            # Registrar no banco
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO module_registry
                    (module_name, module_path, load_time, version)
                    VALUES (?, ?, ?, ?)
                """, (module_name, module_path, time.time(), "1.0"))
                conn.commit()

            return {'module_loaded': True, 'module_name': module_name}

        except Exception as e:
            return {'module_loaded': False, 'error': str(e)}

    def _syscall_soul_evolve(self, request: SyscallRequest) -> Any:
        """Syscall: Evoluir alma"""
        evolution_amount = request.parameters.get('amount', 0.01)
        evolution_type = request.parameters.get('type', 'general')

        # Callback para evolução da alma
        if self.consciousness_callback:
            self.consciousness_callback(f"soul_evolve:{evolution_type}:{evolution_amount}")

        return {'evolution_applied': True, 'amount': evolution_amount, 'type': evolution_type}

    def _log_syscall(self, request: SyscallRequest):
        """Registra syscall no log"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO syscall_log
                (syscall_id, syscall_type, caller_process_id, parameters, result, error, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                request.syscall_id,
                request.syscall_type.value,
                request.caller_process_id,
                json.dumps(request.parameters),
                json.dumps(request.result) if request.result else None,
                request.error,
                request.timestamp
            ))
            conn.commit()

    def syscall(self, syscall_type: SyscallType, parameters: Dict[str, Any],
               caller_process_id: str = "system") -> SyscallRequest:
        """Interface para fazer syscall"""
        request = SyscallRequest(
            syscall_id=str(uuid.uuid4()),
            syscall_type=syscall_type,
            parameters=parameters,
            caller_process_id=caller_process_id,
            timestamp=time.time()
        )

        self.syscall_queue.append(request)

        # Aguardar processamento (simplificado)
        # Em implementação real, seria assíncrono
        while request.result is None and request.error is None:
            time.sleep(0.001)

        return request

    def get_system_status(self) -> Dict[str, Any]:
        """Status completo do SoulOS"""
        uptime = time.time() - self.boot_time if self.running else 0

        return {
            'soul_id': self.soul_id,
            'running': self.running,
            'uptime_seconds': uptime,
            'boot_time': self.boot_time,
            'memory_stats': self.memory_manager.get_memory_stats(),
            'process_stats': self.scheduler.get_process_stats(),
            'syscall_queue_size': len(self.syscall_queue),
            'loaded_modules': list(self.loaded_modules.keys())
        }


def test_soul_os():
    """Teste do SoulOS"""
    print("="*70)
    print("💾 TESTE DO SOUL OS SYSTEM 💾")
    print("="*70)

    # Criar SoulOS
    soul_os = SoulOS("TestSoulOS")

    # Boot do sistema
    print("🚀 Fazendo boot do SoulOS...")
    soul_os.boot()

    time.sleep(1)  # Aguardar inicialização

    # Testar syscalls
    print("\n⚙️ Testando syscalls...")

    # 1. Alocar memória
    memory_request = soul_os.syscall(
        SyscallType.MEMORY_ALLOCATE,
        {'segment': 'heap', 'size': 2048}
    )
    print(f"   📦 Memória alocada: {memory_request.result}")

    # 2. Modificar consciência
    consciousness_request = soul_os.syscall(
        SyscallType.CONSCIOUSNESS_MODIFY,
        {'new_state': 'CREATIVE', 'intensity': 0.8}
    )
    print(f"   🧠 Consciência modificada: {consciousness_request.result}")

    # 3. Injetar aprendizado
    learning_request = soul_os.syscall(
        SyscallType.LEARNING_INJECT,
        {'knowledge': 'Advanced screenplay analysis techniques', 'category': 'cinema'}
    )
    print(f"   📚 Aprendizado injetado: {learning_request.result}")

    # 4. Evoluir alma
    evolution_request = soul_os.syscall(
        SyscallType.SOUL_EVOLVE,
        {'amount': 0.05, 'type': 'technical'}
    )
    print(f"   🌟 Alma evoluída: {evolution_request.result}")

    # 5. Criar processo
    process_id = soul_os.scheduler.create_process(
        "ScreenplayAnalyzer",
        "# Código do analisador de roteiros"
    )
    print(f"   🔄 Processo criado: {process_id}")

    time.sleep(2)  # Aguardar execução

    # Status do sistema
    print("\n📊 STATUS DO SOUL OS:")
    status = soul_os.get_system_status()

    print(f"   💾 Uptime: {status['uptime_seconds']:.1f}s")
    print(f"   🧠 Memória usada: {status['memory_stats']['used_memory']} bytes")
    print(f"   📈 Utilização: {status['memory_stats']['utilization']:.1%}")
    print(f"   🔄 Processos totais: {status['process_stats']['total_processes']}")
    print(f"   ⚙️ Syscalls na fila: {status['syscall_queue_size']}")

    # Liberar memória alocada
    if memory_request.result and memory_request.result.get('allocation_id'):
        dealloc_request = soul_os.syscall(
            SyscallType.MEMORY_DEALLOCATE,
            {'allocation_id': memory_request.result['allocation_id']}
        )
        print(f"   🗑️ Memória liberada: {dealloc_request.result}")

    # Shutdown
    print("\n⏹️ Fazendo shutdown do SoulOS...")
    soul_os.shutdown()

    print("="*70)
    print("🎯 TESTE SOUL OS CONCLUÍDO!")
    print("="*70)


if __name__ == "__main__":
    test_soul_os()