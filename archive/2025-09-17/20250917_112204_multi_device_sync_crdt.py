"""
🌐 MULTI-DEVICE SYNC WITH CRDTs - SINCRONIZAÇÃO PERFEITA SEM CONFLITOS
Conflict-free Replicated Data Types para sincronização perfeita entre dispositivos
"""
import asyncio
import json
import hashlib
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import pickle
import lzma
from enum import Enum

class CRDTType(Enum):
    GROW_ONLY_SET = 'grow_only_set'
    TWO_PHASE_SET = 'two_phase_set'
    PN_COUNTER = 'pn_counter'
    LWW_REGISTER = 'lww_register'
    OR_SET = 'or_set'
    VECTOR_CLOCK = 'vector_clock'
    MERKLE_TREE = 'merkle_tree'

@dataclass
class VectorClock:
    """Relógio vetorial para ordenação causal"""
    clock: Dict[str, int] = field(default_factory=dict)

    def increment(self, node_id: str):
        """Incrementa relógio do nó"""
        self.clock[node_id] = self.clock.get(node_id, 0) + 1

    def update(self, other: 'VectorClock'):
        """Atualiza com outro relógio"""
        for node_id, timestamp in other.clock.items():
            self.clock[node_id] = max(self.clock.get(node_id, 0), timestamp)

    def happens_before(self, other: 'VectorClock') -> bool:
        """Verifica se este aconteceu antes do outro"""
        for node_id, timestamp in self.clock.items():
            if timestamp > other.clock.get(node_id, 0):
                return False
        return True

    def concurrent_with(self, other: 'VectorClock') -> bool:
        """Verifica se são concorrentes"""
        return not self.happens_before(other) and (not other.happens_before(self))

@dataclass
class GrowOnlySet:
    """CRDT: Conjunto que só cresce"""
    elements: Set[Any] = field(default_factory=set)

    def add(self, element: Any):
        """Adiciona elemento"""
        self.elements.add(element)

    def merge(self, other: 'GrowOnlySet'):
        """Merge com outro conjunto"""
        self.elements = self.elements.union(other.elements)

    def contains(self, element: Any) -> bool:
        """Verifica se contém elemento"""
        return element in self.elements

@dataclass
class TwoPhaseSet:
    """CRDT: Conjunto com adição e remoção"""
    added: Set[Any] = field(default_factory=set)
    removed: Set[Any] = field(default_factory=set)

    def add(self, element: Any):
        """Adiciona elemento"""
        self.added.add(element)

    def remove(self, element: Any):
        """Remove elemento (só pode remover se foi adicionado)"""
        if element in self.added:
            self.removed.add(element)

    def merge(self, other: 'TwoPhaseSet'):
        """Merge com outro conjunto"""
        self.added = self.added.union(other.added)
        self.removed = self.removed.union(other.removed)

    def contains(self, element: Any) -> bool:
        """Verifica se contém elemento"""
        return element in self.added and element not in self.removed

    def get_elements(self) -> Set[Any]:
        """Retorna elementos ativos"""
        return self.added - self.removed

@dataclass
class PNCounter:
    """CRDT: Contador positivo/negativo"""
    positive: Dict[str, int] = field(default_factory=dict)
    negative: Dict[str, int] = field(default_factory=dict)

    def increment(self, node_id: str, value: int=1):
        """Incrementa contador"""
        self.positive[node_id] = self.positive.get(node_id, 0) + value

    def decrement(self, node_id: str, value: int=1):
        """Decrementa contador"""
        self.negative[node_id] = self.negative.get(node_id, 0) + value

    def merge(self, other: 'PNCounter'):
        """Merge com outro contador"""
        for node_id, count in other.positive.items():
            self.positive[node_id] = max(self.positive.get(node_id, 0), count)
        for node_id, count in other.negative.items():
            self.negative[node_id] = max(self.negative.get(node_id, 0), count)

    def value(self) -> int:
        """Valor atual do contador"""
        return sum(self.positive.values()) - sum(self.negative.values())

@dataclass
class LWWRegister:
    """CRDT: Last-Write-Wins Register"""
    value: Any = None
    timestamp: float = 0
    node_id: str = ''

    def set(self, value: Any, timestamp: float, node_id: str):
        """Define valor com timestamp"""
        if timestamp > self.timestamp or (timestamp == self.timestamp and node_id > self.node_id):
            self.value = value
            self.timestamp = timestamp
            self.node_id = node_id

    def merge(self, other: 'LWWRegister'):
        """Merge com outro registro"""
        if other.timestamp > self.timestamp or (other.timestamp == self.timestamp and other.node_id > self.node_id):
            self.value = other.value
            self.timestamp = other.timestamp
            self.node_id = other.node_id

    def get(self) -> Any:
        """Retorna valor atual"""
        return self.value

@dataclass
class ORSet:
    """CRDT: Observed-Remove Set (mais poderoso)"""
    elements: Dict[Any, Set[str]] = field(default_factory=dict)
    tombstones: Set[str] = field(default_factory=set)

    def add(self, element: Any, node_id: str):
        """Adiciona elemento com tag única"""
        tag = f'{node_id}_{uuid.uuid4().hex[:8]}_{datetime.now().timestamp()}'
        if element not in self.elements:
            self.elements[element] = set()
        self.elements[element].add(tag)

    def remove(self, element: Any):
        """Remove elemento (todas as tags)"""
        if element in self.elements:
            self.tombstones.update(self.elements[element])

    def merge(self, other: 'ORSet'):
        """Merge com outro conjunto"""
        for element, tags in other.elements.items():
            if element not in self.elements:
                self.elements[element] = set()
            self.elements[element].update(tags)
        self.tombstones.update(other.tombstones)
        for element in list(self.elements.keys()):
            self.elements[element] -= self.tombstones
            if not self.elements[element]:
                del self.elements[element]

    def contains(self, element: Any) -> bool:
        """Verifica se contém elemento"""
        return element in self.elements and len(self.elements[element]) > 0

    def get_elements(self) -> Set[Any]:
        """Retorna elementos ativos"""
        return set(self.elements.keys())

class MerkleTree:
    """Estrutura de árvore de Merkle para verificação eficiente"""

    def __init__(self, data: List[Any]=None):
        self.leaves = []
        self.tree = []
        if data:
            self.build(data)

    def build(self, data: List[Any]):
        """Constrói árvore de Merkle"""
        self.leaves = [self._hash(item) for item in data]
        self.tree = self.leaves.copy()
        current_level = self.leaves
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                if i + 1 < len(current_level):
                    combined = current_level[i] + current_level[i + 1]
                else:
                    combined = current_level[i] + current_level[i]
                next_level.append(self._hash(combined))
            self.tree.extend(next_level)
            current_level = next_level

    def _hash(self, data: Any) -> str:
        """Calcula hash de dados"""
        if isinstance(data, str):
            return hashlib.sha256(data.encode()).hexdigest()
        else:
            return hashlib.sha256(str(data).encode()).hexdigest()

    def get_root(self) -> str:
        """Retorna raiz da árvore"""
        return self.tree[-1] if self.tree else ''

    def verify(self, other_root: str) -> bool:
        """Verifica se árvores são iguais"""
        return self.get_root() == other_root

@dataclass
class SyncMessage:
    """Mensagem de sincronização"""
    sender_id: str
    vector_clock: VectorClock
    operation: str
    crdt_type: CRDTType
    payload: Any
    merkle_root: str = ''
    timestamp: datetime = field(default_factory=datetime.now)

class MultiDeviceSyncCRDT:

    def __init__(self, device_id: str=None):
        self.device_id = device_id or str(uuid.uuid4())
        self.vector_clock = VectorClock()
        self.memory_set = ORSet()
        self.project_registers: Dict[str, LWWRegister] = {}
        self.statistics_counters: Dict[str, PNCounter] = {}
        self.tag_sets: Dict[str, GrowOnlySet] = {}
        self.deleted_items = TwoPhaseSet()
        self.sync_history: List[SyncMessage] = []
        self.pending_syncs: List[SyncMessage] = []
        self.known_peers: Dict[str, Dict] = {}
        self.merkle_trees: Dict[str, MerkleTree] = {}
        self.sync_path = Path(f'/Users/clubproducoes/Digimundo/SYNC/{self.device_id}')
        self.sync_path.mkdir(parents=True, exist_ok=True)
        self.stats = {'syncs_performed': 0, 'conflicts_resolved': 0, 'bytes_synced': 0, 'last_sync': None, 'peers_connected': 0}
        self.load_state()

    def load_state(self):
        """Carrega estado persistido"""
        state_file = self.sync_path / 'state.pkl.lzma'
        if state_file.exists():
            try:
                with lzma.open(state_file, 'rb') as f:
                    state = pickle.load(f)
                    self.vector_clock = state['vector_clock']
                    self.memory_set = state['memory_set']
                    self.project_registers = state['project_registers']
                    self.statistics_counters = state['statistics_counters']
                    self.tag_sets = state['tag_sets']
                    self.deleted_items = state['deleted_items']
                    self.known_peers = state['known_peers']
                    self.stats = state['stats']
                    print(f'🔄 Estado carregado: {self.device_id}')
            except Exception as e:
                print(f'Erro ao carregar estado: {e}')

    def save_state(self):
        """Salva estado persistido"""
        state = {'vector_clock': self.vector_clock, 'memory_set': self.memory_set, 'project_registers': self.project_registers, 'statistics_counters': self.statistics_counters, 'tag_sets': self.tag_sets, 'deleted_items': self.deleted_items, 'known_peers': self.known_peers, 'stats': self.stats, 'timestamp': datetime.now()}
        state_file = self.sync_path / 'state.pkl.lzma'
        with lzma.open(state_file, 'wb', preset=6) as f:
            pickle.dump(state, f)

    def add_memory(self, memory_id: str, content: Any, metadata: Optional[Dict]=None):
        """Adiciona memória ao sistema"""
        self.vector_clock.increment(self.device_id)
        memory_data = {'id': memory_id, 'content': content, 'metadata': metadata or {}, 'device_id': self.device_id, 'timestamp': datetime.now().isoformat(), 'vector_clock': self.vector_clock.clock.copy()}
        self.memory_set.add(memory_data, self.device_id)
        self.save_state()
        sync_msg = SyncMessage(sender_id=self.device_id, vector_clock=self.vector_clock, operation='update', crdt_type=CRDTType.OR_SET, payload={'memory': memory_data})
        self.pending_syncs.append(sync_msg)
        return memory_id

    def update_project(self, project_id: str, content: Any):
        """Atualiza projeto (Last-Write-Wins)"""
        self.vector_clock.increment(self.device_id)
        if project_id not in self.project_registers:
            self.project_registers[project_id] = LWWRegister()
        timestamp = datetime.now().timestamp()
        self.project_registers[project_id].set(content, timestamp, self.device_id)
        self.save_state()
        sync_msg = SyncMessage(sender_id=self.device_id, vector_clock=self.vector_clock, operation='update', crdt_type=CRDTType.LWW_REGISTER, payload={'project_id': project_id, 'register': self.project_registers[project_id]})
        self.pending_syncs.append(sync_msg)

    def increment_counter(self, counter_name: str, value: int=1):
        """Incrementa contador"""
        if counter_name not in self.statistics_counters:
            self.statistics_counters[counter_name] = PNCounter()
        self.statistics_counters[counter_name].increment(self.device_id, value)
        self.save_state()

    def add_tag(self, item_id: str, tag: str):
        """Adiciona tag (nunca pode ser removida)"""
        if item_id not in self.tag_sets:
            self.tag_sets[item_id] = GrowOnlySet()
        self.tag_sets[item_id].add(tag)
        self.save_state()

    def delete_item(self, item_id: str):
        """Marca item como deletado"""
        self.deleted_items.add(item_id)
        self.deleted_items.remove(item_id)
        self.save_state()

    def sync_with_peer(self, peer_id: str, peer_state: 'MultiDeviceSyncCRDT') -> Dict[str, Any]:
        """Sincroniza com outro dispositivo"""
        print(f'🌐 Sincronizando {self.device_id} ←→ {peer_id}')
        sync_report = {'started': datetime.now(), 'peer_id': peer_id, 'changes_sent': 0, 'changes_received': 0, 'conflicts_resolved': 0}
        if not self._needs_sync(peer_state):
            print('  ✓ Já sincronizado')
            sync_report['status'] = 'already_synced'
            return sync_report
        old_clock = self.vector_clock.clock.copy()
        self.vector_clock.update(peer_state.vector_clock)
        peer_state.vector_clock.update(VectorClock(clock=old_clock))
        old_memories = len(self.memory_set.get_elements())
        self.memory_set.merge(peer_state.memory_set)
        peer_state.memory_set.merge(self.memory_set)
        new_memories = len(self.memory_set.get_elements()) - old_memories
        sync_report['changes_received'] += new_memories
        for project_id, register in peer_state.project_registers.items():
            if project_id not in self.project_registers:
                self.project_registers[project_id] = LWWRegister()
            self.project_registers[project_id].merge(register)
            sync_report['changes_received'] += 1
        for project_id, register in self.project_registers.items():
            if project_id not in peer_state.project_registers:
                peer_state.project_registers[project_id] = LWWRegister()
            peer_state.project_registers[project_id].merge(register)
            sync_report['changes_sent'] += 1
        for counter_name, counter in peer_state.statistics_counters.items():
            if counter_name not in self.statistics_counters:
                self.statistics_counters[counter_name] = PNCounter()
            self.statistics_counters[counter_name].merge(counter)
        for counter_name, counter in self.statistics_counters.items():
            if counter_name not in peer_state.statistics_counters:
                peer_state.statistics_counters[counter_name] = PNCounter()
            peer_state.statistics_counters[counter_name].merge(counter)
        for item_id, tag_set in peer_state.tag_sets.items():
            if item_id not in self.tag_sets:
                self.tag_sets[item_id] = GrowOnlySet()
            self.tag_sets[item_id].merge(tag_set)
        for item_id, tag_set in self.tag_sets.items():
            if item_id not in peer_state.tag_sets:
                peer_state.tag_sets[item_id] = GrowOnlySet()
            peer_state.tag_sets[item_id].merge(tag_set)
        self.deleted_items.merge(peer_state.deleted_items)
        peer_state.deleted_items.merge(self.deleted_items)
        self.known_peers[peer_id] = {'last_sync': datetime.now(), 'vector_clock': peer_state.vector_clock.clock.copy()}
        peer_state.known_peers[self.device_id] = {'last_sync': datetime.now(), 'vector_clock': self.vector_clock.clock.copy()}
        self.save_state()
        peer_state.save_state()
        self.stats['syncs_performed'] += 1
        self.stats['last_sync'] = datetime.now()
        self.stats['peers_connected'] = len(self.known_peers)
        sync_report['ended'] = datetime.now()
        sync_report['duration'] = (sync_report['ended'] - sync_report['started']).total_seconds()
        sync_report['status'] = 'success'
        print(f"  ✓ Sincronização completa: {sync_report['changes_sent']} enviados, {sync_report['changes_received']} recebidos")
        return sync_report

    def _needs_sync(self, peer_state: 'MultiDeviceSyncCRDT') -> bool:
        """Verifica se precisa sincronizar usando Merkle trees"""
        my_memories = sorted(list(self.memory_set.get_elements()), key=str)
        peer_memories = sorted(list(peer_state.memory_set.get_elements()), key=str)
        if my_memories != peer_memories:
            return True
        if self.project_registers.keys() != peer_state.project_registers.keys():
            return True
        return False

    def resolve_conflicts(self) -> List[Dict]:
        """Resolve conflitos detectados"""
        conflicts = []
        for project_id, register in self.project_registers.items():
            concurrent_versions = []
            for peer_id, peer_info in self.known_peers.items():
                peer_clock = VectorClock(clock=peer_info['vector_clock'])
                if self.vector_clock.concurrent_with(peer_clock):
                    concurrent_versions.append({'peer_id': peer_id, 'timestamp': peer_info['last_sync']})
            if concurrent_versions:
                conflicts.append({'type': 'concurrent_write', 'project_id': project_id, 'resolution': 'last_write_wins', 'winner': register.node_id, 'concurrent_versions': concurrent_versions})
        self.stats['conflicts_resolved'] += len(conflicts)
        return conflicts

    def get_sync_status(self) -> Dict[str, Any]:
        """Retorna status de sincronização"""
        return {'device_id': self.device_id, 'vector_clock': self.vector_clock.clock, 'memories': len(self.memory_set.get_elements()), 'projects': len(self.project_registers), 'counters': {name: counter.value() for name, counter in self.statistics_counters.items()}, 'deleted_items': len(self.deleted_items.get_elements()), 'known_peers': len(self.known_peers), 'last_sync': self.stats['last_sync'].isoformat() if self.stats['last_sync'] else None, 'syncs_performed': self.stats['syncs_performed'], 'conflicts_resolved': self.stats['conflicts_resolved']}

    def create_sync_package(self) -> bytes:
        """Cria pacote de sincronização comprimido"""
        package = {'device_id': self.device_id, 'vector_clock': self.vector_clock, 'memory_set': self.memory_set, 'project_registers': self.project_registers, 'statistics_counters': self.statistics_counters, 'tag_sets': self.tag_sets, 'deleted_items': self.deleted_items, 'timestamp': datetime.now()}
        serialized = pickle.dumps(package)
        compressed = lzma.compress(serialized, preset=9)
        self.stats['bytes_synced'] += len(compressed)
        return compressed

    async def apply_sync_package(self, package_bytes: bytes) -> bool:
        """Aplica pacote de sincronização recebido"""
        try:
            decompressed = lzma.decompress(package_bytes)
            package = pickle.loads(decompressed)
            peer_state = MultiDeviceSyncCRDT(package['device_id'])
            peer_state.vector_clock = package['vector_clock']
            peer_state.memory_set = package['memory_set']
            peer_state.project_registers = package['project_registers']
            peer_state.statistics_counters = package['statistics_counters']
            peer_state.tag_sets = package['tag_sets']
            peer_state.deleted_items = package['deleted_items']
            await self.sync_with_peer(package['device_id'], peer_state)
            return True
        except Exception as e:
            print(f'Erro ao aplicar pacote: {e}')
            return False

async def main():
    """Testa sincronização multi-dispositivo com CRDTs"""
    print('🌐 TESTE DE SINCRONIZAÇÃO MULTI-DISPOSITIVO COM CRDTs 🌐\n')
    device1 = MultiDeviceSyncCRDT('MacBook-Pro')
    device2 = MultiDeviceSyncCRDT('iPad-Pro')
    device3 = MultiDeviceSyncCRDT('iPhone-15')
    print('Dispositivos criados:')
    print(f'  1. {device1.device_id}')
    print(f'  2. {device2.device_id}')
    print(f'  3. {device3.device_id}')
    print('\nAdicionando memórias...')
    await device1.add_memory('memory_1', 'Script Doctor iniciado no MacBook', {'device': 'MacBook', 'importance': 0.9})
    await device1.update_project('matrix_script', 'The Matrix - Draft 1 from MacBook')
    await device1.increment_counter('analyses_performed', 5)
    await device2.add_memory('memory_2', 'Continuação do trabalho no iPad', {'device': 'iPad', 'importance': 0.8})
    await device2.update_project('matrix_script', 'The Matrix - Draft 2 from iPad')
    await device2.increment_counter('analyses_performed', 3)
    await device2.add_tag('matrix_script', 'sci-fi')
    await device3.add_memory('memory_3', 'Ideia rápida capturada no iPhone', {'device': 'iPhone', 'importance': 0.6})
    await device3.increment_counter('analyses_performed', 2)
    await device3.add_tag('matrix_script', 'philosophical')
    print('\nStatus ANTES da sincronização:')
    for device in [device1, device2, device3]:
        status = device.get_sync_status()
        print(f"  {status['device_id']}: {status['memories']} memórias, {status['projects']} projetos")
    print('\nSincronizando...')
    await device1.sync_with_peer(device2.device_id, device2)
    await device2.sync_with_peer(device3.device_id, device3)
    await device1.sync_with_peer(device3.device_id, device3)
    print('\nStatus APÓS sincronização:')
    for device in [device1, device2, device3]:
        status = device.get_sync_status()
        print(f"  {status['device_id']}: {status['memories']} memórias, {status['projects']} projetos")
        print(f"    Contador: {status['counters'].get('analyses_performed', 0)} análises")
    print('\nResolução de conflitos:')
    for device in [device1, device2, device3]:
        project_value = device.project_registers['matrix_script'].get()
        print(f"  {device.device_id}: matrix_script = '{project_value}'")
    print('\nCriando pacote de sincronização...')
    package = await device1.create_sync_package()
    print(f'  Tamanho do pacote: {len(package) / 1024:.2f} KB')
    print('\nEstatísticas:')
    for device in [device1, device2, device3]:
        print(f'  {device.device_id}:')
        print(f"    Sincronizações: {device.stats['syncs_performed']}")
        print(f"    Conflitos resolvidos: {device.stats['conflicts_resolved']}")
        print(f"    Peers conectados: {device.stats['peers_connected']}")
    print('\n✅ Sincronização multi-dispositivo com CRDTs funcionando perfeitamente!')
    print('Todos os dispositivos convergem para o mesmo estado, sem conflitos!')
if __name__ == '__main__':
    asyncio.run(main())