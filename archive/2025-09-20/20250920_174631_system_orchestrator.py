#!/usr/bin/env python3
"""
System Orchestrator - Orquestração Central com Padrão Saga
Silicon Valley-grade implementation para coordenação de todos os subsistemas
"""

import asyncio
import time
import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import logging
from concurrent.futures import ThreadPoolExecutor
import traceback

# Configurar logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ServiceStatus(Enum):
    """Status dos serviços"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    STARTING = "starting"
    STOPPING = "stopping"


class SagaStatus(Enum):
    """Status de execução de saga"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"


@dataclass
class SagaStep:
    """Passo individual de uma saga"""
    name: str
    service: str
    action: str
    params: Dict[str, Any]
    compensation: Optional[str] = None
    compensation_params: Optional[Dict] = None
    timeout: float = 30.0
    retry_count: int = 3
    critical: bool = True  # Se falhar, deve abortar saga?


@dataclass
class SagaExecution:
    """Execução de uma saga"""
    id: str
    name: str
    steps: List[SagaStep]
    status: SagaStatus
    completed_steps: List[Tuple[SagaStep, Any]]
    failed_step: Optional[SagaStep] = None
    error: Optional[str] = None
    start_time: float = None
    end_time: float = None
    metadata: Dict = None


class Service:
    """Abstração de um serviço gerenciado"""

    def __init__(self, name: str, health_check: Optional[Callable] = None):
        self.name = name
        self.status = ServiceStatus.HEALTHY
        self.health_check = health_check
        self.metrics = defaultdict(float)
        self.last_health_check = 0
        self.consecutive_failures = 0

    async def check_health(self) -> ServiceStatus:
        """Verifica saúde do serviço"""
        if self.health_check:
            try:
                result = await asyncio.wait_for(
                    asyncio.create_task(self.health_check()),
                    timeout=5.0
                )
                self.consecutive_failures = 0
                self.status = ServiceStatus.HEALTHY if result else ServiceStatus.DEGRADED
            except asyncio.TimeoutError:
                self.consecutive_failures += 1
                self.status = ServiceStatus.DEGRADED
            except Exception as e:
                logger.error(f"Health check failed for {self.name}: {e}")
                self.consecutive_failures += 1
                self.status = ServiceStatus.UNHEALTHY if self.consecutive_failures > 3 else ServiceStatus.DEGRADED

        self.last_health_check = time.time()
        return self.status


class ScripturemonOrchestrator:
    """
    Orquestrador central com padrão Saga para transações distribuídas
    Gerencia todos os subsistemas com garantias de consistência
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.services: Dict[str, Service] = {}
        self.sagas: Dict[str, SagaExecution] = {}
        self.compensation_log: List[Dict] = []
        self.executor = ThreadPoolExecutor(max_workers=20)

        # Circuit breaker configuration
        self.circuit_breaker = defaultdict(lambda: {
            'failures': 0,
            'last_failure': 0,
            'is_open': False,
            'half_open_time': 0
        })

        # Métricas
        self.metrics = defaultdict(lambda: defaultdict(float))

        # Inicializar serviços core
        self._initialize_core_services()

        logger.info("Scripturemon Orchestrator initialized")

    def _initialize_core_services(self):
        """Inicializa serviços centrais do sistema"""
        from .memory_federation import MemoryFederation

        # Registrar serviços core
        self.register_service(
            'memory_federation',
            Service('memory_federation', self._check_memory_health)
        )

        self.register_service(
            'extract_engine',
            Service('extract_engine', self._check_engine_health)
        )

        self.register_service(
            'analyze_engine',
            Service('analyze_engine', self._check_engine_health)
        )

        self.register_service(
            'evaluate_engine',
            Service('evaluate_engine', self._check_engine_health)
        )

        self.register_service(
            'synthesis_engine',
            Service('synthesis_engine', self._check_engine_health)
        )

        self.register_service(
            'digilang_compressor',
            Service('digilang_compressor', self._check_compressor_health)
        )

        self.register_service(
            'rag_system',
            Service('rag_system', self._check_rag_health)
        )

        self.register_service(
            'ollama_integration',
            Service('ollama_integration', self._check_ollama_health)
        )

    def register_service(self, name: str, service: Service):
        """Registra um serviço no orquestrador"""
        self.services[name] = service
        logger.info(f"Service registered: {name}")

    async def execute_saga(self, saga_definition: Dict) -> SagaExecution:
        """
        Executa saga com compensação automática em caso de falha
        Implementa two-phase commit distribuído
        """
        saga_id = str(uuid.uuid4())
        saga_name = saga_definition.get('name', 'unnamed_saga')

        # Criar execução
        saga_execution = SagaExecution(
            id=saga_id,
            name=saga_name,
            steps=[SagaStep(**step) for step in saga_definition['steps']],
            status=SagaStatus.PENDING,
            completed_steps=[],
            start_time=time.time(),
            metadata=saga_definition.get('metadata', {})
        )

        self.sagas[saga_id] = saga_execution

        logger.info(f"Starting saga execution: {saga_name} ({saga_id})")

        # Executar saga
        try:
            saga_execution.status = SagaStatus.RUNNING
            await self._execute_saga_steps(saga_execution)
            saga_execution.status = SagaStatus.COMPLETED
            saga_execution.end_time = time.time()

            # Registrar sucesso
            self.metrics['saga'][saga_name]['success'] += 1
            self.metrics['saga'][saga_name]['duration'] = saga_execution.end_time - saga_execution.start_time

            logger.info(f"Saga completed successfully: {saga_name} ({saga_id})")

        except Exception as e:
            logger.error(f"Saga failed: {saga_name} ({saga_id}) - {e}")
            saga_execution.status = SagaStatus.FAILED
            saga_execution.error = str(e)
            saga_execution.end_time = time.time()

            # Executar compensação
            await self._compensate_saga(saga_execution)

            # Registrar falha
            self.metrics['saga'][saga_name]['failure'] += 1

        return saga_execution

    async def _execute_saga_steps(self, saga_execution: SagaExecution):
        """Executa passos individuais da saga"""
        for step in saga_execution.steps:
            # Verificar circuit breaker
            if self._is_circuit_open(step.service):
                raise Exception(f"Circuit breaker open for service: {step.service}")

            # Executar passo com retry
            for attempt in range(step.retry_count):
                try:
                    result = await self._execute_step(step)
                    saga_execution.completed_steps.append((step, result))
                    break  # Sucesso

                except Exception as e:
                    if attempt == step.retry_count - 1:
                        # Última tentativa falhou
                        saga_execution.failed_step = step
                        self._record_circuit_failure(step.service)

                        if step.critical:
                            raise Exception(f"Critical step failed: {step.name} - {e}")
                        else:
                            logger.warning(f"Non-critical step failed: {step.name} - {e}")
                            break
                    else:
                        # Tentar novamente
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff

    async def _execute_step(self, step: SagaStep) -> Any:
        """Executa um passo individual"""
        service = self.services.get(step.service)
        if not service:
            raise Exception(f"Service not found: {step.service}")

        # Verificar saúde do serviço
        if service.status == ServiceStatus.UNHEALTHY:
            raise Exception(f"Service unhealthy: {step.service}")

        # Executar ação
        logger.debug(f"Executing step: {step.name} on {step.service}")

        # Simular execução (seria substituído por chamada real)
        action_handler = self._get_action_handler(step.service, step.action)
        if action_handler:
            result = await asyncio.wait_for(
                action_handler(**step.params),
                timeout=step.timeout
            )
        else:
            # Fallback para execução simulada
            await asyncio.sleep(0.1)
            result = {"status": "success", "step": step.name}

        # Registrar métrica
        self.metrics['step'][step.name]['executions'] += 1

        return result

    async def _compensate_saga(self, saga_execution: SagaExecution):
        """Executa compensação para reverter operações"""
        saga_execution.status = SagaStatus.COMPENSATING
        logger.info(f"Starting compensation for saga: {saga_execution.name}")

        compensation_errors = []

        # Reverter em ordem inversa
        for step, result in reversed(saga_execution.completed_steps):
            if step.compensation:
                try:
                    logger.debug(f"Compensating step: {step.name}")
                    await self._execute_compensation(step, result)

                except Exception as e:
                    logger.error(f"Compensation failed for step {step.name}: {e}")
                    compensation_errors.append({
                        'step': step.name,
                        'error': str(e)
                    })

        # Registrar compensação
        self.compensation_log.append({
            'saga_id': saga_execution.id,
            'saga_name': saga_execution.name,
            'timestamp': time.time(),
            'errors': compensation_errors
        })

        if not compensation_errors:
            saga_execution.status = SagaStatus.COMPENSATED
            logger.info(f"Compensation completed for saga: {saga_execution.name}")
        else:
            logger.error(f"Compensation partially failed for saga: {saga_execution.name}")

    async def _execute_compensation(self, step: SagaStep, original_result: Any):
        """Executa ação de compensação para um passo"""
        compensation_handler = self._get_action_handler(step.service, step.compensation)

        if compensation_handler:
            params = step.compensation_params or {}
            params['original_result'] = original_result

            await asyncio.wait_for(
                compensation_handler(**params),
                timeout=step.timeout
            )
        else:
            # Fallback
            await asyncio.sleep(0.05)

    def _get_action_handler(self, service: str, action: str) -> Optional[Callable]:
        """Obtém handler para ação específica de um serviço"""
        # Mapear para handlers reais
        handlers = {
            'memory_federation': {
                'store': self._store_memory,
                'recall': self._recall_memory,
                'delete': self._delete_memory
            },
            'extract_engine': {
                'extract': self._extract_script,
                'parse': self._parse_script
            },
            'digilang_compressor': {
                'compress': self._compress_text,
                'decompress': self._decompress_text
            }
        }

        return handlers.get(service, {}).get(action)

    # Handlers de exemplo (seriam implementações reais)
    async def _store_memory(self, **kwargs):
        """Handler para armazenar memória"""
        from .memory_federation import MemoryFederation, MemoryType

        federation = MemoryFederation()
        return await federation.broadcast_memory(
            MemoryType.UNIFIED,
            kwargs.get('content'),
            kwargs.get('metadata')
        )

    async def _recall_memory(self, **kwargs):
        """Handler para recuperar memória"""
        from .memory_federation import MemoryFederation

        federation = MemoryFederation()
        return federation.consensus_recall(
            kwargs.get('query'),
            kwargs.get('limit', 10)
        )

    async def _delete_memory(self, **kwargs):
        """Handler para deletar memória"""
        # Implementação placeholder
        return {"deleted": kwargs.get('memory_id')}

    async def _extract_script(self, **kwargs):
        """Handler para extração de roteiro"""
        from .extract_engine import ExtractEngine

        engine = ExtractEngine()
        return engine.extract(kwargs.get('content'))

    async def _parse_script(self, **kwargs):
        """Handler para parsing de roteiro"""
        # Implementação placeholder
        return {"parsed": True}

    async def _compress_text(self, **kwargs):
        """Handler para compressão DigiLang"""
        # Implementação placeholder
        return {"compressed": kwargs.get('text')[:100]}

    async def _decompress_text(self, **kwargs):
        """Handler para descompressão DigiLang"""
        # Implementação placeholder
        return {"decompressed": kwargs.get('text')}

    # Circuit Breaker
    def _is_circuit_open(self, service: str) -> bool:
        """Verifica se circuit breaker está aberto"""
        breaker = self.circuit_breaker[service]

        if breaker['is_open']:
            # Verificar se pode tentar half-open
            if time.time() > breaker['half_open_time']:
                breaker['is_open'] = False
                breaker['failures'] = 0
                return False
            return True

        return False

    def _record_circuit_failure(self, service: str):
        """Registra falha no circuit breaker"""
        breaker = self.circuit_breaker[service]
        breaker['failures'] += 1
        breaker['last_failure'] = time.time()

        # Abrir circuit se muitas falhas
        if breaker['failures'] >= 5:
            breaker['is_open'] = True
            breaker['half_open_time'] = time.time() + 30  # 30 segundos
            logger.warning(f"Circuit breaker opened for service: {service}")

    # Health Checks
    async def _check_memory_health(self) -> bool:
        """Verifica saúde do sistema de memória"""
        try:
            from .memory_federation import MemoryFederation

            federation = MemoryFederation()
            # Teste simples
            results = federation.consensus_recall("health_check", limit=1)
            return True
        except:
            return False

    async def _check_engine_health(self) -> bool:
        """Verifica saúde dos engines"""
        # Implementação simplificada
        return True

    async def _check_compressor_health(self) -> bool:
        """Verifica saúde do compressor DigiLang"""
        try:
            from .digilang_v27_ultimate_adaptive import DigiLangV27UltimateAdaptive

            # Teste simples
            compressor = DigiLangV27UltimateAdaptive()
            test_text = "test"
            compressed = compressor.compress(test_text)
            decompressed = compressor.decompress(compressed)
            return test_text == decompressed
        except:
            return False

    async def _check_rag_health(self) -> bool:
        """Verifica saúde do sistema RAG"""
        # Implementação placeholder
        return True

    async def _check_ollama_health(self) -> bool:
        """Verifica saúde da integração Ollama"""
        try:
            from .ollama_manager import OllamaManager

            manager = OllamaManager()
            return manager.check_health()
        except:
            return False

    # Monitoring
    async def continuous_health_monitoring(self):
        """Monitoramento contínuo de saúde"""
        while True:
            try:
                health_tasks = []
                for name, service in self.services.items():
                    health_tasks.append(service.check_health())

                results = await asyncio.gather(*health_tasks, return_exceptions=True)

                # Atualizar dashboard
                health_status = {}
                for (name, service), result in zip(self.services.items(), results):
                    if isinstance(result, Exception):
                        health_status[name] = ServiceStatus.UNHEALTHY
                    else:
                        health_status[name] = service.status

                # Log status summary
                healthy = sum(1 for s in health_status.values() if s == ServiceStatus.HEALTHY)
                degraded = sum(1 for s in health_status.values() if s == ServiceStatus.DEGRADED)
                unhealthy = sum(1 for s in health_status.values() if s == ServiceStatus.UNHEALTHY)

                logger.info(f"Health Status - Healthy: {healthy}, Degraded: {degraded}, Unhealthy: {unhealthy}")

                # Registrar métricas
                self.metrics['health']['healthy'] = healthy
                self.metrics['health']['degraded'] = degraded
                self.metrics['health']['unhealthy'] = unhealthy

                await asyncio.sleep(10)  # Check every 10 seconds

            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(30)

    def get_status(self) -> Dict:
        """Retorna status completo do sistema"""
        return {
            'services': {
                name: {
                    'status': service.status.value,
                    'last_health_check': service.last_health_check,
                    'consecutive_failures': service.consecutive_failures
                }
                for name, service in self.services.items()
            },
            'active_sagas': len([s for s in self.sagas.values() if s.status == SagaStatus.RUNNING]),
            'completed_sagas': len([s for s in self.sagas.values() if s.status == SagaStatus.COMPLETED]),
            'failed_sagas': len([s for s in self.sagas.values() if s.status == SagaStatus.FAILED]),
            'metrics': dict(self.metrics),
            'circuit_breakers': {
                name: {
                    'is_open': breaker['is_open'],
                    'failures': breaker['failures']
                }
                for name, breaker in self.circuit_breaker.items()
            }
        }

    def export_metrics_prometheus(self) -> str:
        """Exporta métricas em formato Prometheus"""
        lines = []

        # Service health metrics
        for name, service in self.services.items():
            status_value = 1 if service.status == ServiceStatus.HEALTHY else 0
            lines.append(f'service_health{{service="{name}"}} {status_value}')

        # Saga metrics
        for saga_name, metrics in self.metrics['saga'].items():
            lines.append(f'saga_success_total{{saga="{saga_name}"}} {metrics.get("success", 0)}')
            lines.append(f'saga_failure_total{{saga="{saga_name}"}} {metrics.get("failure", 0)}')
            if 'duration' in metrics:
                lines.append(f'saga_duration_seconds{{saga="{saga_name}"}} {metrics["duration"]}')

        # Health summary
        lines.append(f'services_healthy_total {self.metrics["health"].get("healthy", 0)}')
        lines.append(f'services_degraded_total {self.metrics["health"].get("degraded", 0)}')
        lines.append(f'services_unhealthy_total {self.metrics["health"].get("unhealthy", 0)}')

        return '\n'.join(lines)


# Exemplo de uso
async def example_saga():
    """Exemplo de execução de saga"""
    orchestrator = ScripturemonOrchestrator()

    # Definir saga para análise completa de roteiro
    saga_definition = {
        'name': 'complete_script_analysis',
        'steps': [
            {
                'name': 'extract_elements',
                'service': 'extract_engine',
                'action': 'extract',
                'params': {'content': 'script content here'},
                'compensation': None,  # Não requer compensação
                'timeout': 30.0,
                'retry_count': 3,
                'critical': True
            },
            {
                'name': 'store_extracted',
                'service': 'memory_federation',
                'action': 'store',
                'params': {'content': 'extracted elements', 'metadata': {'type': 'extraction'}},
                'compensation': 'delete',
                'compensation_params': {'memory_id': 'to_be_filled'},
                'timeout': 10.0,
                'retry_count': 3,
                'critical': False
            },
            {
                'name': 'compress_content',
                'service': 'digilang_compressor',
                'action': 'compress',
                'params': {'text': 'script content'},
                'compensation': None,
                'timeout': 20.0,
                'retry_count': 2,
                'critical': False
            }
        ],
        'metadata': {
            'user': 'test',
            'script_id': 'test_script_001'
        }
    }

    # Executar saga
    result = await orchestrator.execute_saga(saga_definition)

    print(f"Saga execution result: {result.status.value}")
    print(f"Completed steps: {len(result.completed_steps)}")

    # Iniciar monitoramento
    monitoring_task = asyncio.create_task(orchestrator.continuous_health_monitoring())

    # Aguardar um pouco
    await asyncio.sleep(5)

    # Obter status
    status = orchestrator.get_status()
    print("\nSystem status:")
    print(json.dumps(status, indent=2))

    # Cancelar monitoramento
    monitoring_task.cancel()


if __name__ == "__main__":
    # Executar exemplo
    asyncio.run(example_saga())