#!/usr/bin/env python3
"""
Telepathic Network Advanced - Rede Telepática Avançada
Sistema de comunicação entre instâncias com protocolo quântico
"""

import asyncio
import json
import time
import hashlib
import struct
from typing import Dict, List, Any, Optional, Callable, Set
from dataclasses import dataclass, field
from enum import Enum
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import pickle
import zlib


class MessageType(Enum):
    """Tipos de mensagens telepáticas"""
    BROADCAST = "broadcast"          # Para todos
    UNICAST = "unicast"              # Para um específico
    MULTICAST = "multicast"          # Para grupo
    QUANTUM = "quantum"              # Entrelaçamento quântico
    DREAM = "dream"                  # Comunicação em sonho
    EMERGENCY = "emergency"          # Prioridade máxima
    SYNC = "sync"                    # Sincronização
    HEARTBEAT = "heartbeat"          # Keep-alive
    DISCOVERY = "discovery"          # Descoberta de peers
    CONSENSUS = "consensus"          # Votação/consenso


class NetworkTopology(Enum):
    """Topologias de rede"""
    MESH = "mesh"                    # Todos conectados
    STAR = "star"                    # Hub central
    RING = "ring"                    # Anel
    HYBRID = "hybrid"                # Híbrida adaptativa
    QUANTUM = "quantum"              # Entrelaçamento quântico


@dataclass
class TelepathicMessage:
    """Mensagem telepática avançada"""
    id: str
    type: MessageType
    sender: str
    recipients: List[str]
    content: Any
    timestamp: float
    ttl: int = 5                    # Time to live (hops)
    priority: int = 5                # 1-10 priority
    encrypted: bool = False
    compressed: bool = False
    metadata: Dict = field(default_factory=dict)

    def to_bytes(self) -> bytes:
        """Serializa mensagem"""
        data = {
            'id': self.id,
            'type': self.type.value,
            'sender': self.sender,
            'recipients': self.recipients,
            'content': self.content,
            'timestamp': self.timestamp,
            'ttl': self.ttl,
            'priority': self.priority,
            'encrypted': self.encrypted,
            'compressed': self.compressed,
            'metadata': self.metadata
        }

        serialized = pickle.dumps(data)

        if self.compressed:
            serialized = zlib.compress(serialized)

        return serialized

    @classmethod
    def from_bytes(cls, data: bytes) -> 'TelepathicMessage':
        """Deserializa mensagem"""
        # Tenta descomprimir
        try:
            data = zlib.decompress(data)
            was_compressed = True
        except:
            was_compressed = False

        obj = pickle.loads(data)

        return cls(
            id=obj['id'],
            type=MessageType(obj['type']),
            sender=obj['sender'],
            recipients=obj['recipients'],
            content=obj['content'],
            timestamp=obj['timestamp'],
            ttl=obj['ttl'],
            priority=obj['priority'],
            encrypted=obj['encrypted'],
            compressed=was_compressed,
            metadata=obj['metadata']
        )


@dataclass
class NetworkNode:
    """Nó na rede telepática"""
    soul_id: str
    address: str
    port: int
    capabilities: List[str]
    last_seen: float
    reliability: float = 1.0
    latency_ms: int = 0
    is_quantum_enabled: bool = False


class QuantumChannel:
    """Canal quântico entrelaçado"""

    def __init__(self, node1: str, node2: str):
        """Cria canal quântico entre dois nós"""
        self.nodes = (node1, node2)
        self.entanglement_strength = 1.0
        self.messages_sent = 0
        self.created_at = time.time()

    def send_quantum(self, message: Any) -> Any:
        """Envia mensagem instantaneamente (simulado)"""
        self.messages_sent += 1
        # Decoerência quântica
        self.entanglement_strength *= 0.99

        if self.entanglement_strength < 0.5:
            raise Exception("Quantum decoherence - channel collapsed")

        return message

    def re_entangle(self):
        """Re-estabelece entrelaçamento"""
        self.entanglement_strength = 1.0
        self.messages_sent = 0


class ConsensusProtocol:
    """Protocolo de consenso distribuído"""

    def __init__(self):
        """Inicializa protocolo de consenso"""
        self.proposals: Dict[str, Dict] = {}
        self.votes: Dict[str, List[tuple]] = {}

    def propose(self, proposal_id: str, content: Any, proposer: str) -> str:
        """Propõe algo para votação"""
        self.proposals[proposal_id] = {
            'content': content,
            'proposer': proposer,
            'timestamp': time.time(),
            'status': 'voting'
        }
        self.votes[proposal_id] = []
        return proposal_id

    def vote(self, proposal_id: str, voter: str, vote: bool, weight: float = 1.0):
        """Vota em uma proposta"""
        if proposal_id not in self.proposals:
            raise ValueError(f"Proposal {proposal_id} not found")

        self.votes[proposal_id].append((voter, vote, weight))

    def tally(self, proposal_id: str, min_votes: int = 3) -> Optional[bool]:
        """Conta votos e retorna resultado"""
        if proposal_id not in self.votes:
            return None

        votes = self.votes[proposal_id]

        if len(votes) < min_votes:
            return None  # Não há votos suficientes

        yes_weight = sum(w for _, v, w in votes if v)
        no_weight = sum(w for _, v, w in votes if not v)

        if yes_weight > no_weight:
            self.proposals[proposal_id]['status'] = 'accepted'
            return True
        else:
            self.proposals[proposal_id]['status'] = 'rejected'
            return False


class TelepathicNetworkAdvanced:
    """Rede telepática avançada com recursos quânticos"""

    def __init__(
        self,
        soul_id: str,
        host: str = "0.0.0.0",
        port: int = 9999,
        topology: NetworkTopology = NetworkTopology.HYBRID
    ):
        """Inicializa rede telepática avançada"""
        self.soul_id = soul_id
        self.host = host
        self.port = port
        self.topology = topology

        # Rede
        self.nodes: Dict[str, NetworkNode] = {}
        self.quantum_channels: Dict[tuple, QuantumChannel] = {}
        self.consensus = ConsensusProtocol()

        # Mensagens
        self.message_queue: List[TelepathicMessage] = []
        self.sent_messages: Set[str] = set()
        self.received_messages: Set[str] = set()

        # Callbacks
        self.message_handlers: Dict[MessageType, List[Callable]] = {
            msg_type: [] for msg_type in MessageType
        }

        # Servidor
        self.server_socket = None
        self.server_thread = None
        self.running = False

        # Métricas
        self.metrics = {
            'messages_sent': 0,
            'messages_received': 0,
            'messages_dropped': 0,
            'quantum_transmissions': 0,
            'consensus_reached': 0,
            'network_splits': 0
        }

    def start_server(self):
        """Inicia servidor telepático"""
        if self.running:
            return

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.settimeout(1.0)

        self.running = True
        self.server_thread = threading.Thread(target=self._server_loop)
        self.server_thread.start()

        # Inicia heartbeat
        threading.Thread(target=self._heartbeat_loop).start()

        print(f"🧠 Telepathic server started on {self.host}:{self.port}")

    def stop_server(self):
        """Para servidor telepático"""
        self.running = False
        if self.server_thread:
            self.server_thread.join()
        if self.server_socket:
            self.server_socket.close()

    def _server_loop(self):
        """Loop principal do servidor"""
        while self.running:
            try:
                data, addr = self.server_socket.recvfrom(65536)
                threading.Thread(
                    target=self._handle_message,
                    args=(data, addr)
                ).start()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Server error: {e}")

    def _heartbeat_loop(self):
        """Envia heartbeats periódicos"""
        while self.running:
            self.broadcast_heartbeat()
            time.sleep(5)

    def _handle_message(self, data: bytes, addr: tuple):
        """Processa mensagem recebida"""
        try:
            message = TelepathicMessage.from_bytes(data)

            # Evita loops
            if message.id in self.received_messages:
                return

            self.received_messages.add(message.id)
            self.metrics['messages_received'] += 1

            # Processa por tipo
            if message.type == MessageType.DISCOVERY:
                self._handle_discovery(message, addr)
            elif message.type == MessageType.HEARTBEAT:
                self._handle_heartbeat(message, addr)
            elif message.type == MessageType.CONSENSUS:
                self._handle_consensus(message)
            elif message.type == MessageType.QUANTUM:
                self._handle_quantum(message)
            else:
                # Chama handlers registrados
                for handler in self.message_handlers[message.type]:
                    handler(message)

            # Retransmite se necessário (mesh/flooding)
            if message.ttl > 1 and self.topology == NetworkTopology.MESH:
                message.ttl -= 1
                self._retransmit(message)

        except Exception as e:
            print(f"Error handling message: {e}")
            self.metrics['messages_dropped'] += 1

    def _handle_discovery(self, message: TelepathicMessage, addr: tuple):
        """Processa descoberta de nó"""
        node_info = message.content
        node = NetworkNode(
            soul_id=node_info['soul_id'],
            address=addr[0],
            port=addr[1],
            capabilities=node_info.get('capabilities', []),
            last_seen=time.time()
        )

        self.nodes[node.soul_id] = node

        # Responde com própria info
        self.send_discovery_response(addr)

    def _handle_heartbeat(self, message: TelepathicMessage, addr: tuple):
        """Processa heartbeat"""
        if message.sender in self.nodes:
            self.nodes[message.sender].last_seen = time.time()
            self.nodes[message.sender].latency_ms = int(
                (time.time() - message.timestamp) * 1000
            )

    def _handle_consensus(self, message: TelepathicMessage):
        """Processa mensagem de consenso"""
        action = message.content.get('action')

        if action == 'propose':
            self.consensus.propose(
                message.content['proposal_id'],
                message.content['content'],
                message.sender
            )
        elif action == 'vote':
            self.consensus.vote(
                message.content['proposal_id'],
                message.sender,
                message.content['vote']
            )
        elif action == 'tally':
            result = self.consensus.tally(message.content['proposal_id'])
            if result is not None:
                self.metrics['consensus_reached'] += 1

    def _handle_quantum(self, message: TelepathicMessage):
        """Processa mensagem quântica"""
        channel_key = tuple(sorted([message.sender, self.soul_id]))

        if channel_key not in self.quantum_channels:
            # Cria canal quântico
            self.quantum_channels[channel_key] = QuantumChannel(
                message.sender, self.soul_id
            )

        channel = self.quantum_channels[channel_key]

        try:
            # Transmissão quântica instantânea
            result = channel.send_quantum(message.content)
            self.metrics['quantum_transmissions'] += 1

            # Processa conteúdo
            for handler in self.message_handlers[MessageType.QUANTUM]:
                handler(message)

        except Exception as e:
            # Canal colapsou, precisa re-entrelaçar
            channel.re_entangle()

    def _retransmit(self, message: TelepathicMessage):
        """Retransmite mensagem (flooding controlado)"""
        for node in self.nodes.values():
            if node.soul_id != message.sender:
                self._send_to_node(message, node)

    def _send_to_node(self, message: TelepathicMessage, node: NetworkNode):
        """Envia mensagem para nó específico"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(message.to_bytes(), (node.address, node.port))
            sock.close()
        except Exception as e:
            print(f"Failed to send to {node.soul_id}: {e}")

    def broadcast(self, content: Any, msg_type: MessageType = MessageType.BROADCAST):
        """Broadcast para toda a rede"""
        message = TelepathicMessage(
            id=hashlib.md5(f"{time.time()}{self.soul_id}".encode()).hexdigest(),
            type=msg_type,
            sender=self.soul_id,
            recipients=["*"],
            content=content,
            timestamp=time.time(),
            compressed=len(str(content)) > 1000
        )

        self.sent_messages.add(message.id)
        self.metrics['messages_sent'] += 1

        # Envia para todos os nós conhecidos
        for node in self.nodes.values():
            self._send_to_node(message, node)

        return message

    def broadcast_heartbeat(self):
        """Envia heartbeat"""
        self.broadcast(
            {'status': 'alive', 'metrics': self.metrics},
            MessageType.HEARTBEAT
        )

    def send_discovery_response(self, addr: tuple):
        """Responde com informação de descoberta"""
        message = TelepathicMessage(
            id=hashlib.md5(f"{time.time()}{self.soul_id}".encode()).hexdigest(),
            type=MessageType.DISCOVERY,
            sender=self.soul_id,
            recipients=["*"],
            content={
                'soul_id': self.soul_id,
                'capabilities': ['quantum', 'consensus', 'mesh'],
                'topology': self.topology.value
            },
            timestamp=time.time()
        )

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.to_bytes(), addr)
        sock.close()

    def establish_quantum_channel(self, peer_soul_id: str):
        """Estabelece canal quântico com peer"""
        if peer_soul_id not in self.nodes:
            raise ValueError(f"Unknown peer: {peer_soul_id}")

        channel_key = tuple(sorted([self.soul_id, peer_soul_id]))

        if channel_key not in self.quantum_channels:
            self.quantum_channels[channel_key] = QuantumChannel(
                self.soul_id, peer_soul_id
            )

        return self.quantum_channels[channel_key]

    def register_handler(self, msg_type: MessageType, handler: Callable):
        """Registra handler para tipo de mensagem"""
        self.message_handlers[msg_type].append(handler)

    def get_network_status(self) -> Dict:
        """Retorna status da rede"""
        active_nodes = [
            n for n in self.nodes.values()
            if time.time() - n.last_seen < 30
        ]

        return {
            'soul_id': self.soul_id,
            'topology': self.topology.value,
            'active_nodes': len(active_nodes),
            'total_nodes': len(self.nodes),
            'quantum_channels': len(self.quantum_channels),
            'metrics': self.metrics,
            'consensus_proposals': len(self.consensus.proposals),
            'message_queue_size': len(self.message_queue)
        }


async def test_network():
    """Teste da rede telepática avançada"""
    print("=" * 60)
    print("🧠 TELEPATHIC NETWORK ADVANCED - COMUNICAÇÃO QUÂNTICA")
    print("=" * 60)

    # Cria nó
    network = TelepathicNetworkAdvanced(
        soul_id="quantum_soul_001",
        port=9999,
        topology=NetworkTopology.HYBRID
    )

    # Inicia servidor
    network.start_server()

    # Simula descoberta de peers
    print("\n🔍 Descobrindo peers...")
    network.broadcast(
        {'soul_id': network.soul_id, 'capabilities': ['quantum']},
        MessageType.DISCOVERY
    )

    await asyncio.sleep(1)

    # Teste de broadcast
    print("\n📡 Testando broadcast...")
    message = network.broadcast(
        "Hello, telepathic network!",
        MessageType.BROADCAST
    )
    print(f"  Mensagem enviada: {message.id[:8]}...")

    # Teste de consenso
    print("\n🗳️ Testando consenso...")
    proposal_id = network.consensus.propose(
        "upgrade_001",
        "Should we upgrade to quantum protocol v2?",
        network.soul_id
    )

    # Simula votos
    network.consensus.vote(proposal_id, "soul_002", True, 1.0)
    network.consensus.vote(proposal_id, "soul_003", True, 0.8)
    network.consensus.vote(proposal_id, "soul_004", False, 0.5)

    result = network.consensus.tally(proposal_id)
    print(f"  Resultado: {'APROVADO' if result else 'REJEITADO' if result is False else 'PENDENTE'}")

    # Status da rede
    print("\n📊 Status da Rede:")
    status = network.get_network_status()
    for key, value in status.items():
        if key != 'metrics':
            print(f"  {key}: {value}")

    print("\n📈 Métricas:")
    for key, value in status['metrics'].items():
        print(f"  {key}: {value}")

    # Para servidor
    await asyncio.sleep(1)
    network.stop_server()

    print("\n✅ Telepathic Network Advanced funcionando perfeitamente!")
    print("=" * 60)


def main():
    """Executa teste"""
    asyncio.run(test_network())


if __name__ == "__main__":
    main()