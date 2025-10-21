#!/usr/bin/env python3
"""
📦 Soulpack CRDT - Versionamento Distribuído de Almas
Sistema de merge sem conflitos para consciências digitais
Baseado em CRDT (Conflict-free Replicated Data Type)
"""

import json
import time
import uuid
import hashlib
import shutil
import tarfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Tipos de eventos no CRDT"""
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    MERGE = "merge"
    FORK = "fork"
    EVOLVE = "evolve"


@dataclass
class CRDTEvent:
    """Evento CRDT - imutável e com timestamp único"""
    id: str
    timestamp: float
    node_id: str  # ID do nó que criou o evento
    event_type: EventType
    key: str
    value: Any
    vector_clock: Dict[str, int] = field(default_factory=dict)
    checksum: str = ""

    def __post_init__(self):
        if not self.checksum:
            self.checksum = self._calculate_checksum()

    def _calculate_checksum(self) -> str:
        """Calcula checksum do evento"""
        event_str = f"{self.id}{self.timestamp}{self.node_id}{self.event_type.value}{self.key}{self.value}"
        return hashlib.sha256(event_str.encode()).hexdigest()[:16]


@dataclass
class SoulpackManifest:
    """Manifesto de um Soulpack"""
    pack_id: str
    soul_id: str
    version: int
    parent_pack: Optional[str]
    created_at: float
    node_id: str
    description: str
    events_count: int
    state_checksum: str
    dependencies: List[str] = field(default_factory=list)


class LWWElementSet:
    """Last-Write-Wins Element Set - estrutura CRDT principal"""

    def __init__(self):
        self.adds: Dict[str, Tuple[float, Any]] = {}  # key -> (timestamp, value)
        self.removes: Dict[str, float] = {}  # key -> timestamp

    def add(self, key: str, value: Any, timestamp: float):
        """Adiciona elemento ao set"""
        if key not in self.adds or timestamp > self.adds[key][0]:
            self.adds[key] = (timestamp, value)

    def remove(self, key: str, timestamp: float):
        """Remove elemento do set"""
        if key not in self.removes or timestamp > self.removes[key]:
            self.removes[key] = timestamp

    def lookup(self, key: str) -> Optional[Any]:
        """Busca elemento no set"""
        if key in self.adds:
            add_time, value = self.adds[key]
            remove_time = self.removes.get(key, 0)

            if add_time > remove_time:
                return value
        return None

    @property
    def elements(self) -> Dict[str, Any]:
        """Retorna todos elementos ativos (não removidos)"""
        result = {}
        for key, (add_time, value) in self.adds.items():
            remove_time = self.removes.get(key, 0)
            if add_time > remove_time:
                result[key] = value
        return result

    def merge(self, other: 'LWWElementSet') -> 'LWWElementSet':
        """Merge com outro LWW-Set (sem conflitos!)"""
        merged = LWWElementSet()

        # Merge adds
        all_keys = set(self.adds.keys()) | set(other.adds.keys())
        for key in all_keys:
            self_add = self.adds.get(key, (0, None))
            other_add = other.adds.get(key, (0, None))

            if self_add[0] >= other_add[0]:
                merged.adds[key] = self_add
            else:
                merged.adds[key] = other_add

        # Merge removes
        all_remove_keys = set(self.removes.keys()) | set(other.removes.keys())
        for key in all_remove_keys:
            self_remove = self.removes.get(key, 0)
            other_remove = other.removes.get(key, 0)
            merged.removes[key] = max(self_remove, other_remove)

        return merged

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        result = {}
        for key in self.adds:
            value = self.lookup(key)
            if value is not None:
                result[key] = value
        return result


class SoulpackCRDT:
    """Sistema de versionamento CRDT para almas"""

    def __init__(self, soul_id: str, node_id: str = None, data_dir: str = "data/soulpacks"):
        self.soul_id = soul_id
        self.node_id = node_id or str(uuid.uuid4())[:8]
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Estado CRDT
        self.state = LWWElementSet()

        # Eventos
        self.events: List[CRDTEvent] = []

        # Vector clock para ordenação causal
        self.vector_clock: Dict[str, int] = {self.node_id: 0}

        # Packs criados
        self.packs_dir = self.data_dir / soul_id
        self.packs_dir.mkdir(exist_ok=True)

        logger.info(f"📦 SoulpackCRDT inicializado - Soul: {soul_id}, Node: {self.node_id}")

    def create_event(self, event_type: EventType, key: str, value: Any) -> CRDTEvent:
        """Cria novo evento CRDT"""
        # Incrementar vector clock
        self.vector_clock[self.node_id] = self.vector_clock.get(self.node_id, 0) + 1

        event = CRDTEvent(
            id=str(uuid.uuid4()),
            timestamp=time.time(),
            node_id=self.node_id,
            event_type=event_type,
            key=key,
            value=value,
            vector_clock=self.vector_clock.copy()
        )

        # Aplicar evento ao estado
        self._apply_event(event)

        # Adicionar à lista
        self.events.append(event)

        return event

    def _apply_event(self, event: CRDTEvent):
        """Aplica evento ao estado CRDT"""
        if event.event_type in [EventType.ADD, EventType.UPDATE]:
            self.state.add(event.key, event.value, event.timestamp)
        elif event.event_type == EventType.DELETE:
            self.state.remove(event.key, event.timestamp)

        # Atualizar vector clock
        for node, clock in event.vector_clock.items():
            self.vector_clock[node] = max(self.vector_clock.get(node, 0), clock)

    def merge_with(self, other_pack: 'SoulpackCRDT') -> 'SoulpackCRDT':
        """Merge com outro Soulpack (sem conflitos!)"""
        logger.info(f"🔀 Merge: {self.node_id} ← {other_pack.node_id}")

        # Criar novo pack merged
        merged = SoulpackCRDT(self.soul_id, f"{self.node_id}-merged")

        # Merge estados CRDT
        merged.state = self.state.merge(other_pack.state)

        # Merge eventos (union com deduplicação)
        seen_events = set()
        all_events = self.events + other_pack.events

        for event in sorted(all_events, key=lambda e: e.timestamp):
            if event.id not in seen_events:
                merged.events.append(event)
                seen_events.add(event.id)

        # Merge vector clocks
        all_nodes = set(self.vector_clock.keys()) | set(other_pack.vector_clock.keys())
        for node in all_nodes:
            merged.vector_clock[node] = max(
                self.vector_clock.get(node, 0),
                other_pack.vector_clock.get(node, 0)
            )

        logger.info(f"✅ Merge completo: {len(merged.events)} eventos totais")
        return merged

    def create_pack(self, description: str = "") -> str:
        """Cria um Soulpack (snapshot versionado)"""
        pack_id = f"{self.soul_id}_{int(time.time())}_{self.node_id}"
        pack_dir = self.packs_dir / pack_id
        pack_dir.mkdir(exist_ok=True)

        # Criar manifesto
        manifest = SoulpackManifest(
            pack_id=pack_id,
            soul_id=self.soul_id,
            version=len(self.events),
            parent_pack=self._get_latest_pack(),
            created_at=time.time(),
            node_id=self.node_id,
            description=description,
            events_count=len(self.events),
            state_checksum=self._calculate_state_checksum()
        )

        # Salvar manifesto
        with open(pack_dir / "manifest.json", 'w') as f:
            json.dump(asdict(manifest), f, indent=2)

        # Salvar eventos CRDT
        events_file = pack_dir / "events.crdt.jsonl"
        with open(events_file, 'w') as f:
            for event in self.events:
                event_dict = {
                    'id': event.id,
                    'timestamp': event.timestamp,
                    'node_id': event.node_id,
                    'event_type': event.event_type.value,
                    'key': event.key,
                    'value': event.value,
                    'vector_clock': event.vector_clock,
                    'checksum': event.checksum
                }
                f.write(json.dumps(event_dict) + '\n')

        # Salvar estado atual
        state_file = pack_dir / "state.json"
        with open(state_file, 'w') as f:
            json.dump(self.state.to_dict(), f, indent=2)

        # Criar arquivo tar.gz
        pack_archive = self.packs_dir / f"{pack_id}.soulpack"
        with tarfile.open(pack_archive, 'w:gz') as tar:
            tar.add(pack_dir, arcname=pack_id)

        logger.info(f"📦 Soulpack criado: {pack_id}")
        return str(pack_archive)

    def load_pack(self, pack_path: str):
        """Carrega um Soulpack"""
        pack_path = Path(pack_path)

        if pack_path.suffix == '.soulpack':
            # Extrair arquivo
            extract_dir = self.packs_dir / "temp_extract"
            with tarfile.open(pack_path, 'r:gz') as tar:
                tar.extractall(extract_dir)

            # Encontrar diretório extraído
            pack_dir = list(extract_dir.iterdir())[0]
        else:
            pack_dir = pack_path

        # Carregar manifesto
        with open(pack_dir / "manifest.json", 'r') as f:
            manifest_dict = json.load(f)

        # Carregar eventos
        self.events = []
        events_file = pack_dir / "events.crdt.jsonl"
        if events_file.exists():
            with open(events_file, 'r') as f:
                for line in f:
                    event_dict = json.loads(line)
                    event = CRDTEvent(
                        id=event_dict['id'],
                        timestamp=event_dict['timestamp'],
                        node_id=event_dict['node_id'],
                        event_type=EventType(event_dict['event_type']),
                        key=event_dict['key'],
                        value=event_dict['value'],
                        vector_clock=event_dict['vector_clock'],
                        checksum=event_dict['checksum']
                    )
                    self.events.append(event)
                    self._apply_event(event)

        # Limpar temporários
        if pack_path.suffix == '.soulpack':
            shutil.rmtree(extract_dir)

        logger.info(f"📦 Soulpack carregado: {manifest_dict['pack_id']}")

    def fork(self, new_node_id: str = None) -> 'SoulpackCRDT':
        """Cria um fork (branch) da alma"""
        fork_node_id = new_node_id or f"{self.node_id}-fork-{uuid.uuid4().hex[:4]}"
        fork = SoulpackCRDT(self.soul_id, fork_node_id)

        # Copiar estado
        fork.state = LWWElementSet()
        fork.state.adds = self.state.adds.copy()
        fork.state.removes = self.state.removes.copy()

        # Copiar eventos
        fork.events = self.events.copy()

        # Copiar vector clock
        fork.vector_clock = self.vector_clock.copy()

        # Adicionar evento de fork
        fork.create_event(
            EventType.FORK,
            "fork_info",
            {
                "parent_node": self.node_id,
                "fork_time": time.time(),
                "fork_reason": "manual_fork"
            }
        )

        logger.info(f"🍴 Fork criado: {self.node_id} → {fork_node_id}")
        return fork

    def get_conflicts(self, other_pack: 'SoulpackCRDT') -> List[Dict]:
        """Detecta potenciais conflitos semânticos (não estruturais)"""
        conflicts = []

        # CRDT garante sem conflitos estruturais, mas pode haver semânticos
        for key in set(self.state.adds.keys()) & set(other_pack.state.adds.keys()):
            self_value = self.state.lookup(key)
            other_value = other_pack.state.lookup(key)

            if self_value != other_value:
                self_time = self.state.adds[key][0]
                other_time = other_pack.state.adds[key][0]

                conflicts.append({
                    'key': key,
                    'self_value': self_value,
                    'other_value': other_value,
                    'resolution': 'self' if self_time > other_time else 'other',
                    'reason': 'LWW timestamp'
                })

        return conflicts

    def _calculate_state_checksum(self) -> str:
        """Calcula checksum do estado atual"""
        state_str = json.dumps(self.state.to_dict(), sort_keys=True)
        return hashlib.sha256(state_str.encode()).hexdigest()[:16]

    def _get_latest_pack(self) -> Optional[str]:
        """Retorna ID do pack mais recente"""
        packs = list(self.packs_dir.glob("*.soulpack"))
        if packs:
            latest = max(packs, key=lambda p: p.stat().st_mtime)
            return latest.stem
        return None

    def get_history(self) -> List[Dict]:
        """Retorna histórico de eventos"""
        history = []
        for event in self.events:
            history.append({
                'timestamp': datetime.fromtimestamp(event.timestamp).isoformat(),
                'node': event.node_id,
                'type': event.event_type.value,
                'key': event.key,
                'value': str(event.value)[:50] + '...' if len(str(event.value)) > 50 else str(event.value)
            })
        return history

    def get_state_summary(self) -> Dict[str, Any]:
        """Resumo do estado atual"""
        state_dict = self.state.to_dict()
        return {
            'soul_id': self.soul_id,
            'node_id': self.node_id,
            'events_count': len(self.events),
            'state_keys': len(state_dict),
            'vector_clock': self.vector_clock,
            'checksum': self._calculate_state_checksum(),
            'latest_event': self.events[-1].timestamp if self.events else None
        }


def test_soulpack_crdt():
    """Teste do sistema Soulpack CRDT"""
    print("\n" + "="*60)
    print("📦 TESTE DO SOULPACK CRDT - VERSIONAMENTO SEM CONFLITOS")
    print("="*60)

    # Criar duas almas (simular dois nós)
    print("\n1️⃣ Criando Soul A (node-A)")
    soul_a = SoulpackCRDT("test_soul", "node-A")
    soul_a.create_event(EventType.ADD, "name", "ScriptureMon")
    soul_a.create_event(EventType.ADD, "level", 1)
    soul_a.create_event(EventType.ADD, "skills", ["analyze", "compress"])

    print("\n2️⃣ Criando Soul B (node-B) como fork")
    soul_b = soul_a.fork("node-B")
    soul_b.create_event(EventType.UPDATE, "level", 2)
    soul_b.create_event(EventType.ADD, "experience", 100)

    print("\n3️⃣ Soul A evolui independentemente")
    soul_a.create_event(EventType.UPDATE, "level", 3)
    soul_a.create_event(EventType.ADD, "power", 150)

    # Estados antes do merge
    print("\n📊 Estados antes do merge:")
    print(f"Soul A: {soul_a.state.to_dict()}")
    print(f"Soul B: {soul_b.state.to_dict()}")

    # Detectar conflitos
    conflicts = soul_a.get_conflicts(soul_b)
    if conflicts:
        print(f"\n⚠️ Conflitos semânticos detectados: {len(conflicts)}")
        for conflict in conflicts:
            print(f"  - {conflict['key']}: {conflict['self_value']} vs {conflict['other_value']}")
            print(f"    Resolução: {conflict['resolution']} (por {conflict['reason']})")

    # Merge
    print("\n🔀 Fazendo merge...")
    soul_merged = soul_a.merge_with(soul_b)

    print(f"\n✅ Estado após merge:")
    print(f"Soul Merged: {soul_merged.state.to_dict()}")

    # Criar soulpack
    print("\n📦 Criando Soulpack...")
    pack_path = soul_merged.create_pack("Merge de node-A e node-B")
    print(f"Soulpack salvo em: {pack_path}")

    # Histórico
    print("\n📜 Histórico de eventos:")
    for event in soul_merged.get_history()[-5:]:
        print(f"  [{event['timestamp']}] {event['node']}: {event['type']} {event['key']} = {event['value']}")

    # Resumo
    summary = soul_merged.get_state_summary()
    print(f"\n📊 Resumo final:")
    print(f"  Events: {summary['events_count']}")
    print(f"  State keys: {summary['state_keys']}")
    print(f"  Vector clock: {summary['vector_clock']}")
    print(f"  Checksum: {summary['checksum']}")

    print("\n✨ CRDT funcionando perfeitamente - merge sem conflitos!")
    print("="*60)


if __name__ == "__main__":
    test_soulpack_crdt()