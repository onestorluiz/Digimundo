"""
CQRS Engine - Command Query Responsibility Segregation
Silicon Valley-grade implementation with event sourcing integration
"""
import asyncio
import time
import json
import uuid
import threading
import weakref
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable, Union, Type, Generic, TypeVar
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import defaultdict, deque
from contextlib import asynccontextmanager
import logging
from datetime import datetime
import inspect
import copy
logger = logging.getLogger(__name__)
T = TypeVar('T')
TCommand = TypeVar('TCommand', bound='Command')
TQuery = TypeVar('TQuery', bound='Query')
TResult = TypeVar('TResult')

class CommandType(Enum):
    """Tipos de comandos"""
    CREATE = auto()
    UPDATE = auto()
    DELETE = auto()
    EXECUTE = auto()
    COMPENSATE = auto()
    SAGA = auto()

class QueryType(Enum):
    """Tipos de queries"""
    GET = auto()
    LIST = auto()
    SEARCH = auto()
    AGGREGATE = auto()
    PROJECTION = auto()
    STREAM = auto()

@dataclass
class Command:
    """Base class para comandos"""
    command_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    command_type: CommandType = CommandType.EXECUTE
    aggregate_id: Optional[str] = None
    aggregate_type: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    user_id: Optional[str] = None
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None
    saga_id: Optional[str] = None
    version: int = 1

@dataclass
class Query:
    """Base class para queries"""
    query_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    query_type: QueryType = QueryType.GET
    resource_type: Optional[str] = None
    filters: Dict[str, Any] = field(default_factory=dict)
    projection: Optional[List[str]] = None
    sorting: Optional[List[Tuple[str, str]]] = None
    pagination: Optional[Dict[str, int]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    user_id: Optional[str] = None
    cache_key: Optional[str] = None
    cache_ttl: int = 300

@dataclass
class CommandResult:
    """Resultado de comando"""
    success: bool
    command_id: str
    result: Any = None
    error: Optional[str] = None
    events: List[Any] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0

@dataclass
class QueryResult:
    """Resultado de query"""
    success: bool
    query_id: str
    data: Any = None
    error: Optional[str] = None
    total_count: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0
    cache_hit: bool = False

class CommandHandler(Generic[TCommand, TResult]):
    """Base class para command handlers"""

    def can_handle(self, command: Command) -> bool:
        """Verifica se pode processar comando"""
        return True

    def handle(self, command: TCommand) -> TResult:
        """Processa comando"""
        raise NotImplementedError

    def validate(self, command: TCommand) -> bool:
        """Valida comando"""
        return True

    def compensate(self, command: TCommand) -> None:
        """Compensa comando em caso de falha"""
        pass

class QueryHandler(Generic[TQuery, TResult]):
    """Base class para query handlers"""

    def can_handle(self, query: Query) -> bool:
        """Verifica se pode processar query"""
        return True

    def handle(self, query: TQuery) -> TResult:
        """Processa query"""
        raise NotImplementedError

    def validate(self, query: TQuery) -> bool:
        """Valida query"""
        return True

class CommandBus:
    """Bus de comandos com roteamento"""

    def __init__(self):
        self.handlers: Dict[str, List[CommandHandler]] = defaultdict(list)
        self.middleware: List[Callable] = []
        self.metrics = {'commands_sent': 0, 'commands_succeeded': 0, 'commands_failed': 0, 'total_execution_time': 0.0}
        self.lock = threading.RLock()

    def register_handler(self, command_type: str, handler: CommandHandler):
        """Registra handler para tipo de comando"""
        with self.lock:
            self.handlers[command_type].append(handler)
            logger.info(f'Registered command handler for {command_type}')

    def add_middleware(self, middleware: Callable):
        """Adiciona middleware ao pipeline"""
        self.middleware.append(middleware)

    async def send(self, command: Command) -> CommandResult:
        """Envia comando para processamento"""
        start_time = time.time()
        self.metrics['commands_sent'] += 1
        try:
            for mw in self.middleware:
                command = await mw(command)
            command_type = f'{command.aggregate_type}.{command.command_type.name}'
            handlers = self.handlers.get(command_type, [])
            if not handlers:
                handlers = self.handlers.get(command.command_type.name, [])
            if not handlers:
                raise Exception(f'No handler found for command type {command_type}')
            events = []
            result = None
            for handler in handlers:
                if handler.can_handle(command):
                    if not await handler.validate(command):
                        raise ValueError(f'Command validation failed')
                    result = await handler.handle(command)
                    if hasattr(result, 'events'):
                        events.extend(result.events)
            execution_time = time.time() - start_time
            self.metrics['commands_succeeded'] += 1
            self.metrics['total_execution_time'] += execution_time
            return CommandResult(success=True, command_id=command.command_id, result=result, events=events, execution_time=execution_time)
        except Exception as e:
            execution_time = time.time() - start_time
            self.metrics['commands_failed'] += 1
            logger.error(f'Command {command.command_id} failed: {e}')
            return CommandResult(success=False, command_id=command.command_id, error=str(e), execution_time=execution_time)

class QueryBus:
    """Bus de queries com caching"""

    def __init__(self):
        self.handlers: Dict[str, QueryHandler] = {}
        self.cache: Dict[str, Tuple[Any, float]] = {}
        self.middleware: List[Callable] = []
        self.metrics = {'queries_sent': 0, 'queries_succeeded': 0, 'queries_failed': 0, 'cache_hits': 0, 'cache_misses': 0, 'total_execution_time': 0.0}
        self.lock = threading.RLock()

    def register_handler(self, query_type: str, handler: QueryHandler):
        """Registra handler para tipo de query"""
        with self.lock:
            self.handlers[query_type] = handler
            logger.info(f'Registered query handler for {query_type}')

    def add_middleware(self, middleware: Callable):
        """Adiciona middleware ao pipeline"""
        self.middleware.append(middleware)

    async def send(self, query: Query) -> QueryResult:
        """Envia query para processamento"""
        start_time = time.time()
        self.metrics['queries_sent'] += 1
        try:
            if query.cache_key:
                cached = self._check_cache(query.cache_key)
                if cached is not None:
                    self.metrics['cache_hits'] += 1
                    return QueryResult(success=True, query_id=query.query_id, data=cached, cache_hit=True, execution_time=time.time() - start_time)
                else:
                    self.metrics['cache_misses'] += 1
            for mw in self.middleware:
                query = await mw(query)
            query_type = f'{query.resource_type}.{query.query_type.name}'
            handler = self.handlers.get(query_type)
            if not handler:
                handler = self.handlers.get(query.query_type.name)
            if not handler:
                raise Exception(f'No handler found for query type {query_type}')
            if not await handler.validate(query):
                raise ValueError('Query validation failed')
            result = await handler.handle(query)
            if query.cache_key:
                self._set_cache(query.cache_key, result, query.cache_ttl)
            execution_time = time.time() - start_time
            self.metrics['queries_succeeded'] += 1
            self.metrics['total_execution_time'] += execution_time
            return QueryResult(success=True, query_id=query.query_id, data=result, execution_time=execution_time)
        except Exception as e:
            execution_time = time.time() - start_time
            self.metrics['queries_failed'] += 1
            logger.error(f'Query {query.query_id} failed: {e}')
            return QueryResult(success=False, query_id=query.query_id, error=str(e), execution_time=execution_time)

    def _check_cache(self, cache_key: str) -> Optional[Any]:
        """Verifica cache"""
        with self.lock:
            if cache_key in self.cache:
                result, expiry = self.cache[cache_key]
                if time.time() < expiry:
                    return result
                else:
                    del self.cache[cache_key]
            return None

    def _set_cache(self, cache_key: str, result: Any, ttl: int):
        """Armazena no cache"""
        with self.lock:
            expiry = time.time() + ttl
            self.cache[cache_key] = (result, expiry)
            self._clean_expired_cache()

    def _clean_expired_cache(self):
        """Limpa entradas expiradas do cache"""
        current_time = time.time()
        expired_keys = [key for key, (_, expiry) in self.cache.items() if expiry < current_time]
        for key in expired_keys:
            del self.cache[key]

class ReadModel:
    """Base class para read models (projeções)"""

    def __init__(self, name: str):
        self.name = name
        self.data: Dict[str, Any] = {}
        self.version = 0
        self.last_updated = None
        self.lock = threading.RLock()

    def apply_event(self, event: Dict[str, Any]):
        """Aplica evento ao read model"""
        raise NotImplementedError

    def get(self, key: str) -> Any:
        """Recupera dado do read model"""
        with self.lock:
            return self.data.get(key)

    def get_all(self) -> Dict[str, Any]:
        """Recupera todos os dados"""
        with self.lock:
            return copy.deepcopy(self.data)

    def reset(self):
        """Reset read model"""
        with self.lock:
            self.data.clear()
            self.version = 0
            self.last_updated = None

class Projection:
    """Projeção que atualiza read models baseado em eventos"""

    def __init__(self, name: str):
        self.name = name
        self.read_models: Dict[str, ReadModel] = {}
        self.event_handlers: Dict[str, Callable] = {}
        self.processed_events = 0
        self.last_event_id = None

    def register_read_model(self, read_model: ReadModel):
        """Registra read model"""
        self.read_models[read_model.name] = read_model
        logger.info(f'Registered read model: {read_model.name}')

    def register_event_handler(self, event_type: str, handler: Callable):
        """Registra handler de evento"""
        self.event_handlers[event_type] = handler

    async def project_event(self, event: Dict[str, Any]):
        """Projeta evento nos read models"""
        event_type = event.get('type')
        if event_type in self.event_handlers:
            handler = self.event_handlers[event_type]
            for read_model in self.read_models.values():
                try:
                    await handler(event, read_model)
                    read_model.version += 1
                    read_model.last_updated = time.time()
                except Exception as e:
                    logger.error(f'Error projecting event to {read_model.name}: {e}')
        self.processed_events += 1
        self.last_event_id = event.get('id')

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas da projeção"""
        return {'name': self.name, 'processed_events': self.processed_events, 'last_event_id': self.last_event_id, 'read_models': [{'name': rm.name, 'version': rm.version, 'last_updated': rm.last_updated, 'data_size': len(rm.data)} for rm in self.read_models.values()]}

class SagaManager:
    """Gerenciador de sagas (long-running transactions)"""

    def __init__(self, command_bus: CommandBus):
        self.command_bus = command_bus
        self.sagas: Dict[str, 'Saga'] = {}
        self.saga_types: Dict[str, Type['Saga']] = {}
        self.active_sagas: Dict[str, 'Saga'] = {}
        self.completed_sagas: deque = deque(maxlen=100)
        self.failed_sagas: deque = deque(maxlen=100)

    def register_saga(self, saga_type: str, saga_class: Type['Saga']):
        """Registra tipo de saga"""
        self.saga_types[saga_type] = saga_class
        logger.info(f'Registered saga type: {saga_type}')

    async def start_saga(self, saga_type: str, initial_command: Command) -> str:
        """Inicia nova saga"""
        if saga_type not in self.saga_types:
            raise ValueError(f'Unknown saga type: {saga_type}')
        saga_class = self.saga_types[saga_type]
        saga = saga_class(self.command_bus)
        saga.saga_id = str(uuid.uuid4())
        self.active_sagas[saga.saga_id] = saga
        try:
            await saga.start(initial_command)
            logger.info(f'Started saga {saga.saga_id} of type {saga_type}')
            return saga.saga_id
        except Exception as e:
            logger.error(f'Failed to start saga: {e}')
            del self.active_sagas[saga.saga_id]
            raise

    async def handle_saga_event(self, saga_id: str, event: Dict[str, Any]):
        """Processa evento de saga"""
        if saga_id not in self.active_sagas:
            logger.warning(f'Saga {saga_id} not found')
            return
        saga = self.active_sagas[saga_id]
        try:
            await saga.handle_event(event)
            if saga.is_completed():
                self.completed_sagas.append({'saga_id': saga_id, 'completed_at': time.time(), 'steps_executed': len(saga.executed_steps)})
                del self.active_sagas[saga_id]
                logger.info(f'Saga {saga_id} completed successfully')
        except Exception as e:
            logger.error(f'Saga {saga_id} failed: {e}')
            try:
                await saga.compensate()
                logger.info(f'Saga {saga_id} compensated successfully')
            except Exception as comp_error:
                logger.error(f'Saga {saga_id} compensation failed: {comp_error}')
            self.failed_sagas.append({'saga_id': saga_id, 'failed_at': time.time(), 'error': str(e)})
            del self.active_sagas[saga_id]

class Saga:
    """Base class para sagas"""

    def __init__(self, command_bus: CommandBus):
        self.command_bus = command_bus
        self.saga_id = None
        self.state = 'started'
        self.executed_steps: List[Command] = []
        self.compensation_steps: List[Command] = []

    async def start(self, initial_command: Command):
        """Inicia saga"""
        initial_command.saga_id = self.saga_id
        await self.execute_step(initial_command)

    async def execute_step(self, command: Command):
        """Executa passo da saga"""
        command.saga_id = self.saga_id
        result = await self.command_bus.send(command)
        if result.success:
            self.executed_steps.append(command)
        else:
            raise Exception(f'Saga step failed: {result.error}')
        return result

    def handle_event(self, event: Dict[str, Any]):
        """Processa evento e decide próximo passo"""
        raise NotImplementedError

    async def compensate(self):
        """Compensa saga revertendo passos executados"""
        for command in reversed(self.executed_steps):
            try:
                comp_command = self.create_compensation_command(command)
                if comp_command:
                    await self.command_bus.send(comp_command)
            except Exception as e:
                logger.error(f'Compensation failed for command {command.command_id}: {e}')

    def create_compensation_command(self, command: Command) -> Optional[Command]:
        """Cria comando de compensação"""
        return None

    def is_completed(self) -> bool:
        """Verifica se saga está completa"""
        return self.state == 'completed'

class CQRSEngine:
    """
    Engine principal CQRS com integração completa
    Features:
    - Command/Query separation
    - Event sourcing integration
    - Projections and read models
    - Saga orchestration
    - Caching layer
    - Middleware pipeline
    - Metrics and monitoring
    """

    def __init__(self, event_store=None):
        self.command_bus = CommandBus()
        self.query_bus = QueryBus()
        self.saga_manager = SagaManager(self.command_bus)
        self.projections: Dict[str, Projection] = {}
        self.event_store = event_store
        self.metrics = {'total_commands': 0, 'total_queries': 0, 'active_sagas': 0, 'projections_updated': 0}
        self._setup_default_middleware()
        logger.info('CQRSEngine initialized')

    def _setup_default_middleware(self):
        """Configura middleware padrão"""

        def command_logger(command: Command) -> Command:
            logger.debug(f'Processing command: {command.command_id}')
            return command

        def command_validator(command: Command) -> Command:
            if not command.aggregate_id and command.command_type != CommandType.CREATE:
                raise ValueError('aggregate_id required for non-CREATE commands')
            return command
        self.command_bus.add_middleware(command_logger)
        self.command_bus.add_middleware(command_validator)

        def query_logger(query: Query) -> Query:
            logger.debug(f'Processing query: {query.query_id}')
            return query

        def query_optimizer(query: Query) -> Query:
            if not query.cache_key and query.filters:
                import hashlib
                cache_data = json.dumps(query.filters, sort_keys=True)
                query.cache_key = hashlib.md5(cache_data.encode()).hexdigest()
            return query
        self.query_bus.add_middleware(query_logger)
        self.query_bus.add_middleware(query_optimizer)

    def register_command_handler(self, command_type: str, handler: CommandHandler):
        """Registra handler de comando"""
        self.command_bus.register_handler(command_type, handler)

    def register_query_handler(self, query_type: str, handler: QueryHandler):
        """Registra handler de query"""
        self.query_bus.register_handler(query_type, handler)

    def register_saga(self, saga_type: str, saga_class: Type[Saga]):
        """Registra tipo de saga"""
        self.saga_manager.register_saga(saga_type, saga_class)

    def register_projection(self, projection: Projection):
        """Registra projeção"""
        self.projections[projection.name] = projection
        logger.info(f'Registered projection: {projection.name}')

    async def send_command(self, command: Command) -> CommandResult:
        """Envia comando"""
        self.metrics['total_commands'] += 1
        result = await self.command_bus.send(command)
        if result.success and result.events and self.event_store:
            for event in result.events:
                await self._process_event(event)
        return result

    async def send_query(self, query: Query) -> QueryResult:
        """Envia query"""
        self.metrics['total_queries'] += 1
        return await self.query_bus.send(query)

    async def start_saga(self, saga_type: str, initial_command: Command) -> str:
        """Inicia saga"""
        saga_id = await self.saga_manager.start_saga(saga_type, initial_command)
        self.metrics['active_sagas'] = len(self.saga_manager.active_sagas)
        return saga_id

    async def _process_event(self, event: Dict[str, Any]):
        """Processa evento atualizando projeções"""
        for projection in self.projections.values():
            await projection.project_event(event)
            self.metrics['projections_updated'] += 1
        saga_id = event.get('saga_id')
        if saga_id:
            await self.saga_manager.handle_saga_event(saga_id, event)

    def get_projection(self, projection_name: str) -> Optional[Projection]:
        """Recupera projeção"""
        return self.projections.get(projection_name)

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do engine"""
        return {**self.metrics, 'command_bus': self.command_bus.metrics, 'query_bus': self.query_bus.metrics, 'active_sagas': len(self.saga_manager.active_sagas), 'completed_sagas': len(self.saga_manager.completed_sagas), 'failed_sagas': len(self.saga_manager.failed_sagas), 'projections': [proj.get_statistics() for proj in self.projections.values()]}

class CreateUserCommand(Command):
    """Comando para criar usuário"""

    def __init__(self, username: str, email: str):
        super().__init__(command_type=CommandType.CREATE, aggregate_type='User', payload={'username': username, 'email': email})

class GetUserQuery(Query):
    """Query para buscar usuário"""

    def __init__(self, user_id: str):
        super().__init__(query_type=QueryType.GET, resource_type='User', filters={'user_id': user_id})

class UserCommandHandler(CommandHandler[CreateUserCommand, Dict[str, Any]]):
    """Handler para comandos de usuário"""

    def handle(self, command: CreateUserCommand) -> Dict[str, Any]:
        user = {'id': str(uuid.uuid4()), 'username': command.payload['username'], 'email': command.payload['email'], 'created_at': time.time()}
        events = [{'type': 'UserCreated', 'user_id': user['id'], 'data': user}]
        return {'user': user, 'events': events}

class UserQueryHandler(QueryHandler[GetUserQuery, Dict[str, Any]]):
    """Handler para queries de usuário"""

    def handle(self, query: GetUserQuery) -> Dict[str, Any]:
        return {'id': query.filters['user_id'], 'username': 'example_user', 'email': 'user@example.com'}
_cqrs_engine: Optional[CQRSEngine] = None

def get_cqrs_engine(event_store=None) -> CQRSEngine:
    """
    Retorna instância singleton do CQRS engine
    """
    global _cqrs_engine
    if _cqrs_engine is None:
        _cqrs_engine = CQRSEngine(event_store)
    return _cqrs_engine
__all__ = ['CQRSEngine', 'Command', 'Query', 'CommandResult', 'QueryResult', 'CommandHandler', 'QueryHandler', 'CommandBus', 'QueryBus', 'ReadModel', 'Projection', 'Saga', 'SagaManager', 'CommandType', 'QueryType', 'get_cqrs_engine']