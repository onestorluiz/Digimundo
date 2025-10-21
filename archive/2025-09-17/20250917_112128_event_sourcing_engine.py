"""
Event Sourcing Engine - Sistema completo de event sourcing
Silicon Valley-grade implementation com CQRS, snapshots e replay
"""
import time
import asyncio
import json
import pickle
import hashlib
import uuid
import sqlite3
import threading
import weakref
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable, Union, Type
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict, deque
from contextlib import contextmanager
import logging
from datetime import datetime, timedelta
import inspect
import copy
try:
    import msgpack
except ImportError:
    try:
        import msgpack_python as msgpack
    except ImportError:
        msgpack = None
try:
    import lz4.frame
except ImportError:
    lz4 = None
logger = logging.getLogger(__name__)

class EventType(Enum):
    """Tipos de eventos do sistema"""
    CREATED = 'created'
    UPDATED = 'updated'
    DELETED = 'deleted'
    RESTORED = 'restored'
    STATE_CHANGED = 'state_changed'
    STATE_TRANSITIONED = 'state_transitioned'
    COMMAND_EXECUTED = 'command_executed'
    COMMAND_FAILED = 'command_failed'
    COMMAND_COMPENSATED = 'command_compensated'
    SNAPSHOT_TAKEN = 'snapshot_taken'
    REPLAY_STARTED = 'replay_started'
    REPLAY_COMPLETED = 'replay_completed'
    MEMORY_STORED = 'memory_stored'
    MEMORY_RETRIEVED = 'memory_retrieved'
    MEMORY_CONSOLIDATED = 'memory_consolidated'
    QUANTUM_COLLAPSED = 'quantum_collapsed'
    QUANTUM_ENTANGLED = 'quantum_entangled'
    QUANTUM_MEASURED = 'quantum_measured'

class EventPriority(Enum):
    """Prioridade de processamento de eventos"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    DEFERRED = 5

@dataclass
class Event:
    """Representa um evento no sistema"""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = EventType.STATE_CHANGED
    aggregate_id: str = ''
    aggregate_type: str = ''
    timestamp: float = field(default_factory=time.time)
    version: int = 1
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    causation_id: Optional[str] = None
    correlation_id: Optional[str] = None
    priority: EventPriority = EventPriority.NORMAL

    def to_dict(self) -> Dict[str, Any]:
        """Converte evento para dicionário"""
        return {'event_id': self.event_id, 'event_type': self.event_type.value, 'aggregate_id': self.aggregate_id, 'aggregate_type': self.aggregate_type, 'timestamp': self.timestamp, 'version': self.version, 'data': self.data, 'metadata': self.metadata, 'causation_id': self.causation_id, 'correlation_id': self.correlation_id, 'priority': self.priority.value}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """Cria evento a partir de dicionário"""
        return cls(event_id=data['event_id'], event_type=EventType(data['event_type']), aggregate_id=data['aggregate_id'], aggregate_type=data['aggregate_type'], timestamp=data['timestamp'], version=data['version'], data=data.get('data', {}), metadata=data.get('metadata', {}), causation_id=data.get('causation_id'), correlation_id=data.get('correlation_id'), priority=EventPriority(data.get('priority', 3)))

@dataclass
class Snapshot:
    """Snapshot de estado de um agregado"""
    snapshot_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    aggregate_id: str = ''
    aggregate_type: str = ''
    version: int = 0
    state: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    compressed: bool = False
    checksum: str = ''

    def calculate_checksum(self) -> str:
        """Calcula checksum do snapshot"""
        data = json.dumps(self.state, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def compress(self) -> bytes:
        """Comprime snapshot"""
        if msgpack:
            data = msgpack.packb(self.state)
        else:
            data = pickle.dumps(self.state)
        if lz4:
            compressed = lz4.frame.compress(data)
        else:
            import zlib
            compressed = zlib.compress(data)
        self.compressed = True
        return compressed

    def decompress(self, data: bytes) -> Dict[str, Any]:
        """Descomprime snapshot"""
        if lz4:
            decompressed = lz4.frame.decompress(data)
        else:
            import zlib
            decompressed = zlib.decompress(data)
        if msgpack:
            self.state = msgpack.unpackb(decompressed, raw=False)
        else:
            self.state = pickle.loads(decompressed)
        self.compressed = False
        return self.state

class EventStore:
    """Armazenamento persistente de eventos"""

    def __init__(self, db_path: str='events.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.RLock()
        self._init_db()

    def _init_db(self):
        """Inicializa esquema do banco"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('\n                CREATE TABLE IF NOT EXISTS events (\n                    event_id TEXT PRIMARY KEY,\n                    event_type TEXT NOT NULL,\n                    aggregate_id TEXT NOT NULL,\n                    aggregate_type TEXT NOT NULL,\n                    timestamp REAL NOT NULL,\n                    version INTEGER NOT NULL,\n                    data TEXT,\n                    metadata TEXT,\n                    causation_id TEXT,\n                    correlation_id TEXT,\n                    priority INTEGER,\n                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n                )\n            ')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_aggregate ON events(aggregate_id, version)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON events(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_correlation ON events(correlation_id)')
            cursor.execute('\n                CREATE TABLE IF NOT EXISTS snapshots (\n                    snapshot_id TEXT PRIMARY KEY,\n                    aggregate_id TEXT NOT NULL,\n                    aggregate_type TEXT NOT NULL,\n                    version INTEGER NOT NULL,\n                    state BLOB NOT NULL,\n                    timestamp REAL NOT NULL,\n                    compressed INTEGER DEFAULT 0,\n                    checksum TEXT,\n                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n                )\n            ')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_snapshot_aggregate ON snapshots(aggregate_id, version DESC)')
            self.conn.commit()

    def append_event(self, event: Event) -> bool:
        """Adiciona evento ao store"""
        with self.lock:
            try:
                cursor = self.conn.cursor()
                cursor.execute('\n                    INSERT INTO events (\n                        event_id, event_type, aggregate_id, aggregate_type,\n                        timestamp, version, data, metadata,\n                        causation_id, correlation_id, priority\n                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\n                ', (event.event_id, event.event_type.value, event.aggregate_id, event.aggregate_type, event.timestamp, event.version, json.dumps(event.data), json.dumps(event.metadata), event.causation_id, event.correlation_id, event.priority.value))
                self.conn.commit()
                return True
            except Exception as e:
                logger.error(f'Failed to append event: {e}')
                self.conn.rollback()
                return False

    def get_events(self, aggregate_id: str, from_version: int=0, to_version: Optional[int]=None) -> List[Event]:
        """Recupera eventos de um agregado"""
        with self.lock:
            cursor = self.conn.cursor()
            if to_version:
                cursor.execute('\n                    SELECT * FROM events\n                    WHERE aggregate_id = ? AND version > ? AND version <= ?\n                    ORDER BY version\n                ', (aggregate_id, from_version, to_version))
            else:
                cursor.execute('\n                    SELECT * FROM events\n                    WHERE aggregate_id = ? AND version > ?\n                    ORDER BY version\n                ', (aggregate_id, from_version))
            events = []
            for row in cursor.fetchall():
                event = Event(event_id=row['event_id'], event_type=EventType(row['event_type']), aggregate_id=row['aggregate_id'], aggregate_type=row['aggregate_type'], timestamp=row['timestamp'], version=row['version'], data=json.loads(row['data'] or '{}'), metadata=json.loads(row['metadata'] or '{}'), causation_id=row['causation_id'], correlation_id=row['correlation_id'], priority=EventPriority(row['priority'] or 3))
                events.append(event)
            return events

    def save_snapshot(self, snapshot: Snapshot) -> bool:
        """Salva snapshot"""
        with self.lock:
            try:
                snapshot.checksum = snapshot.calculate_checksum()
                compressed_state = snapshot.compress()
                cursor = self.conn.cursor()
                cursor.execute('\n                    INSERT OR REPLACE INTO snapshots (\n                        snapshot_id, aggregate_id, aggregate_type,\n                        version, state, timestamp, compressed, checksum\n                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)\n                ', (snapshot.snapshot_id, snapshot.aggregate_id, snapshot.aggregate_type, snapshot.version, compressed_state, snapshot.timestamp, 1, snapshot.checksum))
                self.conn.commit()
                return True
            except Exception as e:
                logger.error(f'Failed to save snapshot: {e}')
                self.conn.rollback()
                return False

    def get_latest_snapshot(self, aggregate_id: str) -> Optional[Snapshot]:
        """Recupera último snapshot de um agregado"""
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('\n                SELECT * FROM snapshots\n                WHERE aggregate_id = ?\n                ORDER BY version DESC\n                LIMIT 1\n            ', (aggregate_id,))
            row = cursor.fetchone()
            if row:
                snapshot = Snapshot(snapshot_id=row['snapshot_id'], aggregate_id=row['aggregate_id'], aggregate_type=row['aggregate_type'], version=row['version'], timestamp=row['timestamp'], compressed=bool(row['compressed']), checksum=row['checksum'])
                if snapshot.compressed:
                    snapshot.decompress(row['state'])
                elif msgpack:
                    snapshot.state = msgpack.unpackb(row['state'], raw=False)
                else:
                    snapshot.state = pickle.loads(row['state'])
                return snapshot
            return None

class AggregateRoot:
    """Base class para agregados com event sourcing"""

    def __init__(self, aggregate_id: str=None, aggregate_type: str=None):
        self.aggregate_id = aggregate_id or str(uuid.uuid4())
        self.aggregate_type = aggregate_type or self.__class__.__name__
        self.version = 0
        self.uncommitted_events: List[Event] = []
        self.event_handlers: Dict[EventType, Callable] = {}
        self._register_handlers()

    def _register_handlers(self):
        """Registra handlers de eventos"""
        for name in dir(self):
            if name.startswith('handle_'):
                method = getattr(self, name)
                if callable(method):
                    event_name = name.replace('handle_', '').upper()
                    try:
                        event_type = EventType[event_name]
                        self.event_handlers[event_type] = method
                    except KeyError:
                        pass

    def apply_event(self, event: Event, is_new: bool=True):
        """Aplica evento ao agregado"""
        handler = self.event_handlers.get(event.event_type)
        if handler:
            handler(event)
        self.version = event.version
        if is_new:
            self.uncommitted_events.append(event)

    def raise_event(self, event_type: EventType, data: Dict[str, Any], metadata: Dict[str, Any]=None) -> Event:
        """Levanta novo evento"""
        event = Event(event_type=event_type, aggregate_id=self.aggregate_id, aggregate_type=self.aggregate_type, version=self.version + 1, data=data, metadata=metadata or {})
        self.apply_event(event, is_new=True)
        return event

    def mark_events_as_committed(self):
        """Marca eventos como commitados"""
        self.uncommitted_events.clear()

    def get_uncommitted_events(self) -> List[Event]:
        """Retorna eventos não commitados"""
        return self.uncommitted_events.copy()

    def load_from_history(self, events: List[Event]):
        """Carrega agregado a partir do histórico de eventos"""
        for event in events:
            self.apply_event(event, is_new=False)

    def get_state(self) -> Dict[str, Any]:
        """Retorna estado atual do agregado"""
        return {'aggregate_id': self.aggregate_id, 'aggregate_type': self.aggregate_type, 'version': self.version}

    def restore_from_snapshot(self, snapshot: Snapshot):
        """Restaura estado a partir de snapshot"""
        self.version = snapshot.version

class EventSourcingEngine:
    """
    Engine principal de event sourcing
    Features:
    - Event store persistente
    - Snapshots automáticos
    - Replay de eventos
    - Projections (read models)
    - Event bus com subscrições
    - Time travel (voltar no tempo)
    - Audit trail completo
    """

    def __init__(self, store_path: str='events.db', snapshot_frequency: int=100):
        self.event_store = EventStore(store_path)
        self.snapshot_frequency = snapshot_frequency
        self.aggregate_cache: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
        self.projection_cache: Dict[str, Any] = {}
        self.event_handlers: Dict[EventType, List[Callable]] = defaultdict(list)
        self.projection_handlers: Dict[str, Callable] = {}
        self.event_queue: asyncio.Queue = None
        self.processing = False
        self.metrics = {'events_processed': 0, 'snapshots_created': 0, 'replays_performed': 0, 'projections_updated': 0}
        logger.info(f'EventSourcingEngine initialized with snapshot frequency {snapshot_frequency}')

    def save_aggregate(self, aggregate: AggregateRoot) -> bool:
        """
        Salva eventos não commitados de um agregado
        """
        events = aggregate.get_uncommitted_events()
        if not events:
            return True
        success = True
        for event in events:
            if not self.event_store.append_event(event):
                success = False
                break
        if success:
            aggregate.mark_events_as_committed()
            if aggregate.version % self.snapshot_frequency == 0:
                self.create_snapshot(aggregate)
            for event in events:
                self._publish_event(event)
            self.aggregate_cache[aggregate.aggregate_id] = aggregate
            self.metrics['events_processed'] += len(events)
        return success

    def load_aggregate(self, aggregate_type: Type[AggregateRoot], aggregate_id: str) -> Optional[AggregateRoot]:
        """
        Carrega agregado a partir do event store
        """
        if aggregate_id in self.aggregate_cache:
            return self.aggregate_cache[aggregate_id]
        snapshot = self.event_store.get_latest_snapshot(aggregate_id)
        aggregate = aggregate_type(aggregate_id=aggregate_id)
        if snapshot:
            aggregate.restore_from_snapshot(snapshot)
            from_version = snapshot.version
        else:
            from_version = 0
        events = self.event_store.get_events(aggregate_id, from_version)
        if not events and (not snapshot):
            return None
        aggregate.load_from_history(events)
        self.aggregate_cache[aggregate_id] = aggregate
        return aggregate

    def create_snapshot(self, aggregate: AggregateRoot) -> bool:
        """
        Cria snapshot de um agregado
        """
        snapshot = Snapshot(aggregate_id=aggregate.aggregate_id, aggregate_type=aggregate.aggregate_type, version=aggregate.version, state=aggregate.get_state())
        success = self.event_store.save_snapshot(snapshot)
        if success:
            self.metrics['snapshots_created'] += 1
            event = Event(event_type=EventType.SNAPSHOT_TAKEN, aggregate_id=aggregate.aggregate_id, aggregate_type=aggregate.aggregate_type, version=aggregate.version, data={'snapshot_id': snapshot.snapshot_id})
            self._publish_event(event)
        return success

    def replay_events(self, aggregate_id: str, to_version: Optional[int]=None, to_timestamp: Optional[float]=None) -> Optional[AggregateRoot]:
        """
        Replay de eventos até versão ou timestamp específico
        """
        start_event = Event(event_type=EventType.REPLAY_STARTED, aggregate_id=aggregate_id, aggregate_type='System', data={'to_version': to_version, 'to_timestamp': to_timestamp})
        self._publish_event(start_event)
        events = self.event_store.get_events(aggregate_id, 0, to_version)
        if to_timestamp:
            events = [e for e in events if e.timestamp <= to_timestamp]
        if not events:
            return None
        aggregate_type_name = events[0].aggregate_type
        aggregate = AggregateRoot(aggregate_id=aggregate_id, aggregate_type=aggregate_type_name)
        aggregate.load_from_history(events)
        self.metrics['replays_performed'] += 1
        end_event = Event(event_type=EventType.REPLAY_COMPLETED, aggregate_id=aggregate_id, aggregate_type='System', data={'final_version': aggregate.version})
        self._publish_event(end_event)
        return aggregate

    def time_travel(self, aggregate_id: str, target_time: datetime) -> Optional[AggregateRoot]:
        """
        Viaja no tempo para estado do agregado em momento específico
        """
        timestamp = target_time.timestamp()
        return self.replay_events(aggregate_id, to_timestamp=timestamp)

    def subscribe(self, event_type: EventType, handler: Callable):
        """
        Inscreve handler para tipo de evento
        """
        self.event_handlers[event_type].append(handler)
        logger.info(f'Subscribed handler for {event_type}')

    def unsubscribe(self, event_type: EventType, handler: Callable):
        """
        Remove inscrição de handler
        """
        if handler in self.event_handlers[event_type]:
            self.event_handlers[event_type].remove(handler)

    def register_projection(self, projection_name: str, handler: Callable):
        """
        Registra projection (read model)
        """
        self.projection_handlers[projection_name] = handler
        logger.info(f'Registered projection: {projection_name}')

    def _publish_event(self, event: Event):
        """
        Publica evento para handlers
        """
        for handler in self.event_handlers.get(event.event_type, []):
            try:
                handler(event)
            except Exception as e:
                logger.error(f'Error in event handler: {e}')
        for name, handler in self.projection_handlers.items():
            try:
                current_state = self.projection_cache.get(name, {})
                new_state = handler(event, current_state)
                if new_state is not None:
                    self.projection_cache[name] = new_state
                    self.metrics['projections_updated'] += 1
            except Exception as e:
                logger.error(f'Error updating projection {name}: {e}')

    def start_async_processing(self):
        """
        Inicia processamento assíncrono de eventos
        """
        if self.processing:
            return
        self.event_queue = asyncio.Queue()
        self.processing = True
        asyncio.create_task(self._event_worker())
        logger.info('Async event processing started')

    async def _event_worker(self):
        """
        Worker assíncrono para processar eventos
        """
        while self.processing:
            try:
                event = await self.event_queue.get()
                self._publish_event(event)
                self.event_queue.task_done()
            except Exception as e:
                logger.error(f'Error in event worker: {e}')
                await asyncio.sleep(1)

    async def stop_async_processing(self):
        """
        Para processamento assíncrono
        """
        self.processing = False
        if self.event_queue:
            await self.event_queue.join()
        logger.info('Async event processing stopped')

    def get_event_history(self, aggregate_id: str, event_types: List[EventType]=None) -> List[Event]:
        """
        Recupera histórico de eventos com filtros
        """
        events = self.event_store.get_events(aggregate_id)
        if event_types:
            events = [e for e in events if e.event_type in event_types]
        return events

    def get_projection(self, projection_name: str) -> Any:
        """
        Recupera estado atual de uma projection
        """
        return self.projection_cache.get(projection_name)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do engine
        """
        return {**self.metrics, 'aggregates_cached': len(self.aggregate_cache), 'projections_active': len(self.projection_handlers), 'event_handlers_registered': sum((len(h) for h in self.event_handlers.values())), 'async_processing': self.processing}

class BankAccount(AggregateRoot):
    """
    Exemplo de agregado: Conta bancária
    """

    def __init__(self, aggregate_id: str=None):
        super().__init__(aggregate_id, 'BankAccount')
        self.balance = 0.0
        self.owner = ''
        self.transactions = []

    def open_account(self, owner: str, initial_balance: float=0.0):
        """
        Abre conta
        """
        self.raise_event(EventType.CREATED, {'owner': owner, 'initial_balance': initial_balance})

    def deposit(self, amount: float):
        """
        Depósito
        """
        if amount <= 0:
            raise ValueError('Amount must be positive')
        self.raise_event(EventType.UPDATED, {'operation': 'deposit', 'amount': amount})

    def withdraw(self, amount: float):
        """
        Saque
        """
        if amount <= 0:
            raise ValueError('Amount must be positive')
        if amount > self.balance:
            raise ValueError('Insufficient funds')
        self.raise_event(EventType.UPDATED, {'operation': 'withdraw', 'amount': amount})

    def handle_created(self, event: Event):
        """
        Handler para evento CREATED
        """
        self.owner = event.data['owner']
        self.balance = event.data['initial_balance']

    def handle_updated(self, event: Event):
        """
        Handler para evento UPDATED
        """
        operation = event.data.get('operation')
        amount = event.data.get('amount', 0)
        if operation == 'deposit':
            self.balance += amount
        elif operation == 'withdraw':
            self.balance -= amount
        self.transactions.append({'operation': operation, 'amount': amount, 'timestamp': event.timestamp})

    def get_state(self) -> Dict[str, Any]:
        """
        Retorna estado completo
        """
        state = super().get_state()
        state.update({'balance': self.balance, 'owner': self.owner, 'transactions': self.transactions})
        return state

    def restore_from_snapshot(self, snapshot: Snapshot):
        """
        Restaura de snapshot
        """
        super().restore_from_snapshot(snapshot)
        state = snapshot.state
        self.balance = state.get('balance', 0.0)
        self.owner = state.get('owner', '')
        self.transactions = state.get('transactions', [])
_engine_instance: Optional[EventSourcingEngine] = None

def get_event_sourcing_engine(store_path: str='events.db') -> EventSourcingEngine:
    """
    Retorna instância singleton do engine
    """
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = EventSourcingEngine(store_path)
    return _engine_instance
__all__ = ['EventSourcingEngine', 'EventStore', 'Event', 'EventType', 'EventPriority', 'Snapshot', 'AggregateRoot', 'BankAccount', 'get_event_sourcing_engine']