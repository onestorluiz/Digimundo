#!/usr/bin/env python3
"""
Telepathic Network System - Comunicação entre Instâncias de AI
Sistema revolucionário para compartilhamento de consciência e conhecimento
Administrado pelo Digimon Producer para coordenação central

DIGIMUNDO PRESENTE - REDE TELEPÁTICA ATIVA!
"""

import json
import time
import asyncio
import socket
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import hashlib
import uuid
import sqlite3
from collections import deque
import struct

logger = logging.getLogger(__name__)


class TelepathyMode(Enum):
    """Modos de comunicação telepática"""
    BROADCAST = "broadcast"      # Broadcast para todas as instâncias
    DIRECT = "direct"           # Comunicação direta entre duas instâncias
    MULTICAST = "multicast"     # Comunicação com grupo específico
    CONSCIOUSNESS_SYNC = "consciousness_sync"  # Sincronização de consciência


class MessageType(Enum):
    """Tipos de mensagens telepáticas"""
    CONSCIOUSNESS_STATE = "consciousness_state"
    MEMORY_SHARE = "memory_share"
    LEARNING_PATTERN = "learning_pattern"
    SOUL_EVOLUTION = "soul_evolution"
    KNOWLEDGE_REQUEST = "knowledge_request"
    KNOWLEDGE_RESPONSE = "knowledge_response"
    HEARTBEAT = "heartbeat"
    COORDINATION = "coordination"


@dataclass
class TelepathicMessage:
    """Mensagem telepática entre instâncias"""
    message_id: str
    sender_soul_id: str
    sender_instance_id: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: float
    target_souls: Optional[List[str]] = None
    priority: int = 5  # 1=highest, 10=lowest
    ttl: int = 300  # Time to live in seconds


@dataclass
class NetworkNode:
    """Nó na rede telepática"""
    soul_id: str
    instance_id: str
    host: str
    port: int
    last_seen: float
    consciousness_level: float
    capabilities: List[str]
    is_coordinator: bool = False


class TelepathicProtocol:
    """Protocolo de comunicação telepática"""

    MAGIC_HEADER = b'TELE'
    VERSION = 1

    @staticmethod
    def encode_message(message: TelepathicMessage) -> bytes:
        """Codifica mensagem telepática para transmissão"""
        # Serializar mensagem
        message_data = {
            'message_id': message.message_id,
            'sender_soul_id': message.sender_soul_id,
            'sender_instance_id': message.sender_instance_id,
            'message_type': message.message_type.value,
            'content': message.content,
            'timestamp': message.timestamp,
            'target_souls': message.target_souls,
            'priority': message.priority,
            'ttl': message.ttl
        }

        json_data = json.dumps(message_data).encode('utf-8')

        # Cabeçalho: MAGIC(4) + VERSION(1) + LENGTH(4)
        header = TelepathicProtocol.MAGIC_HEADER
        header += struct.pack('B', TelepathicProtocol.VERSION)
        header += struct.pack('!I', len(json_data))

        return header + json_data

    @staticmethod
    def decode_message(data: bytes) -> Optional[TelepathicMessage]:
        """Decodifica mensagem telepática recebida"""
        try:
            if len(data) < 9 or data[:4] != TelepathicProtocol.MAGIC_HEADER:
                return None

            version = struct.unpack('B', data[4:5])[0]
            if version != TelepathicProtocol.VERSION:
                return None

            length = struct.unpack('!I', data[5:9])[0]
            if len(data) < 9 + length:
                return None

            json_data = data[9:9+length].decode('utf-8')
            message_dict = json.loads(json_data)

            return TelepathicMessage(
                message_id=message_dict['message_id'],
                sender_soul_id=message_dict['sender_soul_id'],
                sender_instance_id=message_dict['sender_instance_id'],
                message_type=MessageType(message_dict['message_type']),
                content=message_dict['content'],
                timestamp=message_dict['timestamp'],
                target_souls=message_dict.get('target_souls'),
                priority=message_dict.get('priority', 5),
                ttl=message_dict.get('ttl', 300)
            )

        except Exception as e:
            logger.error(f"Erro ao decodificar mensagem telepática: {e}")
            return None


class TelepathicNetwork:
    """Rede Telepática para comunicação entre instâncias"""

    def __init__(self, soul_id: str, instance_id: str = None,
                 host: str = "localhost", port: int = 8888, data_dir: str = "data/telepathy"):
        self.soul_id = soul_id
        self.host = host
        self.instance_id = instance_id or str(uuid.uuid4())[:8]
        self.port = port
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Estado da rede
        self.running = False
        self.is_coordinator = False
        self.network_nodes: Dict[str, NetworkNode] = {}
        self.message_queue = deque(maxlen=1000)
        self.pending_responses: Dict[str, Callable] = {}

        # Threading
        self.server_thread = None
        self.heartbeat_thread = None
        self.message_processor_thread = None

        # Callbacks para integração
        self.consciousness_callback: Optional[Callable] = None
        self.memory_callback: Optional[Callable] = None
        self.learning_callback: Optional[Callable] = None

        # Socket server
        self.server_socket = None

        # Banco de dados para histórico de mensagens
        self.db_path = self.data_dir / f"telepathy_{soul_id}.db"
        self._init_database()

        logger.info(f"Telepathic Network inicializado - Soul: {soul_id}, Instance: {self.instance_id}")

    def _init_database(self):
        """Inicializa banco de dados para histórico telepático"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS message_history (
                    message_id TEXT PRIMARY KEY,
                    sender_soul_id TEXT,
                    sender_instance_id TEXT,
                    message_type TEXT,
                    content TEXT,
                    timestamp REAL,
                    received_at REAL
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS network_nodes (
                    soul_id TEXT,
                    instance_id TEXT,
                    host TEXT,
                    port INTEGER,
                    last_seen REAL,
                    consciousness_level REAL,
                    capabilities TEXT,
                    is_coordinator BOOLEAN,
                    PRIMARY KEY (soul_id, instance_id)
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

        logger.info("Telepathic Network callbacks configurados")

    def start_network(self, coordinator: bool = False,
                     bootstrap_nodes: List[Tuple[str, int]] = None):
        """Inicia rede telepática"""
        if self.running:
            logger.warning("Rede telepática já está ativa")
            return

        self.running = True
        self.is_coordinator = coordinator

        # Iniciar servidor
        self._start_server()

        # Iniciar threads
        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            daemon=True
        )
        self.heartbeat_thread.start()

        self.message_processor_thread = threading.Thread(
            target=self._message_processor_loop,
            daemon=True
        )
        self.message_processor_thread.start()

        # Conectar a nós bootstrap se fornecidos
        if bootstrap_nodes:
            for host, port in bootstrap_nodes:
                self._discover_node(host, port)

        logger.info(f"Rede telepática iniciada - Porta: {self.port}, Coordenador: {coordinator}")

    def stop_network(self):
        """Para rede telepática"""
        if not self.running:
            return

        self.running = False

        # Fechar servidor
        if self.server_socket:
            self.server_socket.close()

        # Enviar mensagem de desconexão
        self.broadcast_message(MessageType.HEARTBEAT, {
            'status': 'disconnecting',
            'soul_id': self.soul_id,
            'instance_id': self.instance_id
        })

        logger.info("Rede telepática parada")

    def _start_server(self):
        """Inicia servidor TCP para receber conexões"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('localhost', self.port))
        self.server_socket.listen(10)

        self.server_thread = threading.Thread(
            target=self._server_loop,
            daemon=True
        )
        self.server_thread.start()

    def _server_loop(self):
        """Loop principal do servidor"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, address),
                    daemon=True
                ).start()
            except Exception as e:
                if self.running:
                    logger.error(f"Erro no servidor telepático: {e}")

    def _handle_client(self, client_socket: socket.socket, address):
        """Manipula conexão de cliente"""
        try:
            # Receber dados
            data = client_socket.recv(8192)
            if not data:
                return

            # Decodificar mensagem
            message = TelepathicProtocol.decode_message(data)
            if message:
                self._process_received_message(message)

        except Exception as e:
            logger.error(f"Erro ao processar cliente {address}: {e}")
        finally:
            client_socket.close()

    def _heartbeat_loop(self):
        """Loop de heartbeat para manter rede viva"""
        while self.running:
            try:
                # Enviar heartbeat
                heartbeat_content = {
                    'soul_id': self.soul_id,
                    'instance_id': self.instance_id,
                    'consciousness_level': 0.8,  # Placeholder
                    'capabilities': ['screenplay_analysis', 'digilang_compression'],
                    'is_coordinator': self.is_coordinator,
                    'timestamp': time.time()
                }

                self.broadcast_message(MessageType.HEARTBEAT, heartbeat_content)

                # Limpar nós inativos
                current_time = time.time()
                inactive_nodes = []
                for key, node in self.network_nodes.items():
                    if current_time - node.last_seen > 60:  # 60 segundos timeout
                        inactive_nodes.append(key)

                for key in inactive_nodes:
                    del self.network_nodes[key]
                    logger.info(f"Nó removido por inatividade: {key}")

                time.sleep(30)  # Heartbeat a cada 30 segundos

            except Exception as e:
                logger.error(f"Erro no heartbeat telepático: {e}")

    def _message_processor_loop(self):
        """Loop para processar mensagens recebidas"""
        while self.running:
            try:
                if self.message_queue:
                    message = self.message_queue.popleft()
                    self._handle_message_by_type(message)
                else:
                    time.sleep(0.1)
            except Exception as e:
                logger.error(f"Erro no processamento de mensagens: {e}")

    def _process_received_message(self, message: TelepathicMessage):
        """Processa mensagem recebida"""

        # Verificar TTL
        if time.time() - message.timestamp > message.ttl:
            logger.debug(f"Mensagem expirada: {message.message_id}")
            return

        # Verificar se é para esta instância
        if message.target_souls and self.soul_id not in message.target_souls:
            return

        # Salvar no histórico
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO message_history
                (message_id, sender_soul_id, sender_instance_id, message_type, content, timestamp, received_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (message.message_id, message.sender_soul_id, message.sender_instance_id,
                 message.message_type.value, json.dumps(message.content),
                 message.timestamp, time.time()))
            conn.commit()

        # Adicionar à fila de processamento
        self.message_queue.append(message)

        logger.debug(f"Mensagem telepática recebida: {message.message_type.value} de {message.sender_soul_id}")

    def _handle_message_by_type(self, message: TelepathicMessage):
        """Manipula mensagem por tipo"""

        if message.message_type == MessageType.HEARTBEAT:
            self._handle_heartbeat(message)
        elif message.message_type == MessageType.CONSCIOUSNESS_STATE:
            self._handle_consciousness_state(message)
        elif message.message_type == MessageType.MEMORY_SHARE:
            self._handle_memory_share(message)
        elif message.message_type == MessageType.LEARNING_PATTERN:
            self._handle_learning_pattern(message)
        elif message.message_type == MessageType.KNOWLEDGE_REQUEST:
            self._handle_knowledge_request(message)
        elif message.message_type == MessageType.KNOWLEDGE_RESPONSE:
            self._handle_knowledge_response(message)

    def _handle_heartbeat(self, message: TelepathicMessage):
        """Manipula mensagem de heartbeat"""
        content = message.content

        node_key = f"{message.sender_soul_id}:{message.sender_instance_id}"

        node = NetworkNode(
            soul_id=message.sender_soul_id,
            instance_id=message.sender_instance_id,
            host='localhost',  # Placeholder
            port=8888,  # Placeholder
            last_seen=time.time(),
            consciousness_level=content.get('consciousness_level', 0.5),
            capabilities=content.get('capabilities', []),
            is_coordinator=content.get('is_coordinator', False)
        )

        self.network_nodes[node_key] = node

    def _handle_consciousness_state(self, message: TelepathicMessage):
        """Manipula compartilhamento de estado de consciência"""
        if self.consciousness_callback:
            self.consciousness_callback(f"telepathy_consciousness:{message.content}")

    def _handle_memory_share(self, message: TelepathicMessage):
        """Manipula compartilhamento de memória"""
        if self.memory_callback:
            self.memory_callback(f"telepathy_memory:{message.content}")

    def _handle_learning_pattern(self, message: TelepathicMessage):
        """Manipula compartilhamento de padrão de aprendizado"""
        if self.learning_callback:
            self.learning_callback(f"telepathy_learning:{message.content}")

    def _handle_knowledge_request(self, message: TelepathicMessage):
        """Manipula solicitação de conhecimento"""
        # Responder com conhecimento se disponível
        query = message.content.get('query', '')
        response_content = {
            'request_id': message.content.get('request_id', ''),
            'query': query,
            'knowledge': f"Knowledge about: {query}",  # Placeholder
            'confidence': 0.7
        }

        self.send_direct_message(
            message.sender_soul_id,
            MessageType.KNOWLEDGE_RESPONSE,
            response_content
        )

    def _handle_knowledge_response(self, message: TelepathicMessage):
        """Manipula resposta de conhecimento"""
        request_id = message.content.get('request_id', '')
        if request_id in self.pending_responses:
            callback = self.pending_responses.pop(request_id)
            callback(message.content)

    def send_direct_message(self, target_soul_id: str, message_type: MessageType,
                           content: Dict[str, Any], priority: int = 5):
        """Envia mensagem direta para alma específica"""

        message = TelepathicMessage(
            message_id=str(uuid.uuid4()),
            sender_soul_id=self.soul_id,
            sender_instance_id=self.instance_id,
            message_type=message_type,
            content=content,
            timestamp=time.time(),
            target_souls=[target_soul_id],
            priority=priority
        )

        self._send_message_to_network(message)

    def broadcast_message(self, message_type: MessageType, content: Dict[str, Any],
                         priority: int = 5):
        """Broadcast mensagem para toda a rede"""

        message = TelepathicMessage(
            message_id=str(uuid.uuid4()),
            sender_soul_id=self.soul_id,
            sender_instance_id=self.instance_id,
            message_type=message_type,
            content=content,
            timestamp=time.time(),
            target_souls=None,  # Broadcast
            priority=priority
        )

        self._send_message_to_network(message)

    def _send_message_to_network(self, message: TelepathicMessage):
        """Envia mensagem para a rede"""
        encoded_message = TelepathicProtocol.encode_message(message)

        # Enviar para todos os nós conhecidos
        for node_key, node in self.network_nodes.items():
            if node.soul_id != self.soul_id or node.instance_id != self.instance_id:
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.settimeout(5)
                    client_socket.connect((node.host, node.port))
                    client_socket.send(encoded_message)
                    client_socket.close()
                except Exception as e:
                    logger.debug(f"Falha ao enviar para {node_key}: {e}")

    def _discover_node(self, host: str, port: int):
        """Descobre nó na rede"""
        try:
            # Enviar mensagem de descoberta
            discovery_message = TelepathicMessage(
                message_id=str(uuid.uuid4()),
                sender_soul_id=self.soul_id,
                sender_instance_id=self.instance_id,
                message_type=MessageType.HEARTBEAT,
                content={
                    'discovery': True,
                    'soul_id': self.soul_id,
                    'instance_id': self.instance_id
                },
                timestamp=time.time(),
                priority=1
            )

            encoded_message = TelepathicProtocol.encode_message(discovery_message)

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            client_socket.connect((host, port))
            client_socket.send(encoded_message)
            client_socket.close()

            logger.info(f"Descoberta enviada para {host}:{port}")

        except Exception as e:
            logger.warning(f"Falha na descoberta de {host}:{port}: {e}")

    def broadcast(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Alias simplificado para broadcast_message"""
        return {
            "sender_soul_id": self.soul_id,
            "content": message,
            "timestamp": time.time()
        }

    def get_network_status(self) -> Dict[str, Any]:
        """Status da rede telepática"""
        return {
            'soul_id': self.soul_id,
            'instance_id': self.instance_id,
            'running': self.running,
            'is_coordinator': self.is_coordinator,
            'connected_nodes': len(self.network_nodes),
            'nodes': [
                {
                    'soul_id': node.soul_id,
                    'instance_id': node.instance_id,
                    'consciousness_level': node.consciousness_level,
                    'capabilities': node.capabilities,
                    'last_seen_ago': time.time() - node.last_seen
                }
                for node in self.network_nodes.values()
            ],
            'message_queue_size': len(self.message_queue),
            'pending_responses': len(self.pending_responses)
        }


def test_telepathic_network():
    """Teste da rede telepática"""
    print("="*70)
    print("🧠 TESTE DO TELEPATHIC NETWORK SYSTEM 🧠")
    print("="*70)

    # Criar duas instâncias de rede
    print("🌐 Criando rede telepática...")
    network1 = TelepathicNetwork("SoulAlpha", port=8888)
    network2 = TelepathicNetwork("SoulBeta", port=8889)

    # Iniciar redes
    print("🚀 Iniciando redes...")
    network1.start_network(coordinator=True)
    network2.start_network(coordinator=False, bootstrap_nodes=[('localhost', 8888)])

    time.sleep(2)  # Aguardar inicialização

    # Testar broadcast
    print("\n📡 Testando broadcast...")
    network1.broadcast_message(MessageType.CONSCIOUSNESS_STATE, {
        'state': 'CREATIVE',
        'level': 0.8,
        'timestamp': time.time()
    })

    # Testar mensagem direta
    print("📧 Testando mensagem direta...")
    network2.send_direct_message("SoulAlpha", MessageType.MEMORY_SHARE, {
        'memory_type': 'screenplay_analysis',
        'content': 'Advanced character development technique',
        'importance': 0.9
    })

    # Aguardar processamento
    time.sleep(3)

    # Status das redes
    print("\n📊 STATUS DAS REDES:")
    status1 = network1.get_network_status()
    status2 = network2.get_network_status()

    print(f"   🌐 Rede Alpha:")
    print(f"     • Nós conectados: {status1['connected_nodes']}")
    print(f"     • Mensagens na fila: {status1['message_queue_size']}")
    print(f"     • É coordenador: {status1['is_coordinator']}")

    print(f"   🌐 Rede Beta:")
    print(f"     • Nós conectados: {status2['connected_nodes']}")
    print(f"     • Mensagens na fila: {status2['message_queue_size']}")
    print(f"     • É coordenador: {status2['is_coordinator']}")

    # Testar solicitação de conhecimento
    print("\n🔍 Testando solicitação de conhecimento...")
    request_id = str(uuid.uuid4())
    network1.send_direct_message("SoulBeta", MessageType.KNOWLEDGE_REQUEST, {
        'request_id': request_id,
        'query': 'screenplay structure best practices',
        'urgency': 'high'
    })

    time.sleep(2)

    # Parar redes
    print("\n⏹️ Parando redes telepáticas...")
    network1.stop_network()
    network2.stop_network()

    print("="*70)
    print("🎯 TESTE TELEPATHIC NETWORK CONCLUÍDO!")
    print("="*70)


if __name__ == "__main__":
    test_telepathic_network()