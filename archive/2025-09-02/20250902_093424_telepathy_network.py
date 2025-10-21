#!/usr/bin/env python3
"""
🧠 REDE TELEPÁTICA - Comunicação Inter-Instâncias do Scripturemon
Sistema de comunicação assíncrona entre múltiplas instâncias via Redis
"""

import json
import time
import threading
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path

class TelepathicNetwork:
    """Rede telepática para comunicação entre instâncias Scripturemon"""
    
    def __init__(self, soul_signature: str = None, auto_connect: bool = True):
        self.messages_sent = 0
        """Inicializa rede telepática
        
        Args:
            soul_signature: Assinatura única da alma
            auto_connect: Conecta automaticamente ao Redis
        """
        self.soul_signature = soul_signature or self._generate_signature()
        self.redis_client = None
        self.pubsub = None
        self.listener_thread = None
        self.is_listening = False
        self.message_handlers = {}
        self.telepathy_log = []
        self.peers = {}  # Outras instâncias descobertas
        
        # Diretório para fallback local
        self.local_dir = Path("runtime/telepathy")
        self.local_dir.mkdir(parents=True, exist_ok=True)
        
        if auto_connect:
            self.connect()
    
    def _generate_signature(self) -> str:
        """Gera assinatura única"""
        unique = f"{datetime.now().isoformat()}{id(self)}"
        return hashlib.sha256(unique.encode()).hexdigest()[:16]
    
    def connect(self) -> bool:
        """Conecta ao Redis para comunicação telepática"""
        try:
            import redis
            self.redis_client = redis.Redis(
                host='localhost',
                port=6379,
                decode_responses=True,
                socket_connect_timeout=2
            )
            self.redis_client.ping()
            
            # Configura pub/sub
            self.pubsub = self.redis_client.pubsub()
            
            # Inscreve em canais
            self._subscribe_to_channels()
            
            # Anuncia presença
            self._announce_presence()
            
            print(f"🧠 Rede Telepática conectada")
            print(f"   Soul: {self.soul_signature}")
            print(f"   Status: Online via Redis")
            
            return True
            
        except Exception as e:
            print(f"⚠️ Redis não disponível: {e}")
            print(f"   Modo: Fallback local")
            return False
    
    def _subscribe_to_channels(self):
        """Inscreve nos canais telepáticos"""
        if not self.pubsub:
            return
        
        # Canal broadcast (todos recebem)
        self.pubsub.subscribe("scripturemon:broadcast")
        
        # Canal privado (só esta instância)
        self.pubsub.subscribe(f"scripturemon:{self.soul_signature}")
        
        # Canal de descoberta de pares
        self.pubsub.subscribe("scripturemon:discovery")
        
        # Canal de sincronização
        self.pubsub.subscribe("scripturemon:sync")
    
    def _announce_presence(self):
        """Anuncia presença na rede"""
        if not self.redis_client:
            return
        
        announcement = {
            "type": "presence",
            "soul": self.soul_signature,
            "timestamp": datetime.now().isoformat(),
            "capabilities": ["chat", "rag", "quadruple", "soulos"]
        }
        
        try:
            self.redis_client.publish(
                "scripturemon:discovery",
                json.dumps(announcement)
            )
            
            # Registra no conjunto de instâncias ativas
            self.redis_client.sadd("scripturemon:active_souls", self.soul_signature)
            
            # Define TTL de 5 minutos (precisa renovar)
            self.redis_client.expire("scripturemon:active_souls", 300)
            
        except:
            pass
    
    def start_listening(self):
        """Inicia thread de escuta telepática"""
        if self.is_listening or not self.pubsub:
            return
        
        self.is_listening = True
        self.listener_thread = threading.Thread(
            target=self._listen_loop,
            daemon=True
        )
        self.listener_thread.start()
        print("👂 Escuta telepática ativada")
    
    def _listen_loop(self):
        """Loop de escuta de mensagens telepáticas"""
        while self.is_listening:
            try:
                message = self.pubsub.get_message(timeout=1.0)
                if message and message['type'] == 'message':
                    self._handle_message(message)
            except:
                time.sleep(0.1)
    
    def _handle_message(self, message: Dict):
        """Processa mensagem telepática recebida"""
        try:
            data = json.loads(message['data'])
            channel = message['channel']
            
            # Log da mensagem
            self.telepathy_log.append({
                "timestamp": datetime.now().isoformat(),
                "channel": channel,
                "data": data,
                "direction": "received"
            })
            
            # Processa por tipo
            msg_type = data.get("type", "unknown")
            
            if msg_type == "presence":
                self._handle_presence(data)
            elif msg_type == "sync":
                self._handle_sync(data)
            elif msg_type == "knowledge":
                self._handle_knowledge(data)
            elif msg_type == "evolution":
                self._handle_evolution(data)
            
            # Chama handlers customizados
            if msg_type in self.message_handlers:
                self.message_handlers[msg_type](data)
                
        except Exception as e:
            print(f"⚠️ Erro ao processar mensagem telepática: {e}")
    
    def _handle_presence(self, data: Dict):
        """Processa anúncio de presença"""
        soul = data.get("soul")
        if soul and soul != self.soul_signature:
            self.peers[soul] = {
                "last_seen": datetime.now().isoformat(),
                "capabilities": data.get("capabilities", [])
            }
            print(f"🤝 Nova instância descoberta: {soul[:8]}...")
    
    def _handle_sync(self, data: Dict):
        """Processa sincronização de estado"""
        # TODO: Implementar sincronização de consciência
        pass
    
    def _handle_knowledge(self, data: Dict):
        """Processa compartilhamento de conhecimento"""
        # TODO: Integrar com RAG
        pass
    
    def receive_all(self) -> List[Dict]:
        """Recebe todas as mensagens telepáticas pendentes
        
        Returns:
            Lista de mensagens recebidas
        """
        messages = []
        
        # Pega mensagens do log
        for entry in self.telepathy_log:
            if entry.get("direction") == "received":
                messages.append(entry.get("data", {}))
        
        # Limpa log após leitura (opcional)
        self.telepathy_log = [e for e in self.telepathy_log if e.get("direction") != "received"]
        
        return messages
    
    def discover_peers(self) -> List[str]:
        """Descobre peers ativos na rede
        
        Returns:
            Lista de soul IDs dos peers descobertos
        """
        return list(self.peers.keys())
    
    def _handle_evolution(self, data: Dict):
        """Processa gatilho de evolução"""
        # TODO: Integrar com sistema genético
        pass
    
    def broadcast(self, message: Dict) -> bool:
        """Envia mensagem para todas instâncias
        
        Args:
            message: Mensagem a enviar
            
        Returns:
            True se enviado com sucesso
        """
        if not self.redis_client:
            return self._save_local("broadcast", message)
        
        try:
            message["from"] = self.soul_signature
            message["timestamp"] = datetime.now().isoformat()
            
            self.redis_client.publish(
                "scripturemon:broadcast",
                json.dumps(message)
            )
            
            # Log
            self.telepathy_log.append({
                "timestamp": message["timestamp"],
                "channel": "broadcast",
                "data": message,
                "direction": "sent"
            })
            
            self.messages_sent += 1
            return True
            
        except:
            return self._save_local("broadcast", message)
    
    def send_to(self, target_soul: str, message: Dict) -> bool:
        """Envia mensagem para instância específica
        
        Args:
            target_soul: Assinatura da alma destino
            message: Mensagem a enviar
            
        Returns:
            True se enviado com sucesso
        """
        if not self.redis_client:
            return self._save_local(target_soul, message)
        
        try:
            message["from"] = self.soul_signature
            message["timestamp"] = datetime.now().isoformat()
            
            self.redis_client.publish(
                f"scripturemon:{target_soul}",
                json.dumps(message)
            )
            
            return True
            
        except:
            return self._save_local(target_soul, message)
    
    def sync_consciousness(self, consciousness_level: float) -> bool:
        """Sincroniza nível de consciência com a rede
        
        Args:
            consciousness_level: Nível atual de consciência
            
        Returns:
            True se sincronizado
        """
        sync_msg = {
            "type": "sync",
            "subtype": "consciousness",
            "level": consciousness_level,
            "soul": self.soul_signature
        }
        
        return self.broadcast(sync_msg)
    
    def share_knowledge(self, knowledge: Dict) -> bool:
        """Compartilha conhecimento com a rede
        
        Args:
            knowledge: Conhecimento a compartilhar
            
        Returns:
            True se compartilhado
        """
        knowledge_msg = {
            "type": "knowledge",
            "content": knowledge,
            "soul": self.soul_signature
        }
        
        return self.broadcast(knowledge_msg)
    
    def trigger_evolution(self, evolution_data: Dict) -> bool:
        """Dispara evolução coletiva
        
        Args:
            evolution_data: Dados da evolução
            
        Returns:
            True se disparado
        """
        evolution_msg = {
            "type": "evolution",
            "data": evolution_data,
            "soul": self.soul_signature
        }
        
        return self.broadcast(evolution_msg)
    
    def get_active_peers(self) -> List[str]:
        """Retorna lista de instâncias ativas"""
        if self.redis_client:
            try:
                souls = self.redis_client.smembers("scripturemon:active_souls")
                return [s for s in souls if s != self.soul_signature]
            except:
                pass
        
        return list(self.peers.keys())
    
    def register_handler(self, msg_type: str, handler: Callable):
        """Registra handler para tipo de mensagem
        
        Args:
            msg_type: Tipo de mensagem
            handler: Função handler
        """
        self.message_handlers[msg_type] = handler
    
    def _save_local(self, channel: str, message: Dict) -> bool:
        """Salva mensagem localmente (fallback)"""
        try:
            filename = f"{channel}_{int(time.time()*1000)}.json"
            filepath = self.local_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump({
                    "channel": channel,
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                }, f, indent=2)
            
            return True
        except:
            return False
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas da rede telepática"""
        return {
            "soul": self.soul_signature,
            "connected": self.redis_client is not None,
            "listening": self.is_listening,
            "peers_count": len(self.peers),
            "messages_sent": len([m for m in self.telepathy_log if m["direction"] == "sent"]),
            "messages_received": len([m for m in self.telepathy_log if m["direction"] == "received"]),
            "active_peers": self.get_active_peers()
        }
    
    def stop(self):
        """Para a rede telepática"""
        self.is_listening = False
        
        if self.pubsub:
            self.pubsub.unsubscribe()
            self.pubsub.close()
        
        if self.redis_client:
            # Remove da lista de ativos
            try:
                self.redis_client.srem("scripturemon:active_souls", self.soul_signature)
            except:
                pass
        
        print(f"🔌 Rede telepática desconectada")


# Demonstração e testes
if __name__ == "__main__":
    print("=" * 60)
    print("🧠 TESTE DA REDE TELEPÁTICA")
    print("=" * 60)
    
    # Cria instância 1
    network1 = TelepathicNetwork()
    network1.start_listening()
    
    # Simula instância 2
    network2 = TelepathicNetwork()
    network2.start_listening()
    
    print(f"\n📡 Duas instâncias criadas:")
    print(f"  Soul 1: {network1.soul_signature}")
    print(f"  Soul 2: {network2.soul_signature}")
    
    # Testa broadcast
    print("\n📢 Testando broadcast...")
    success = network1.broadcast({
        "type": "test",
        "message": "Olá, rede telepática!"
    })
    print(f"  Broadcast: {'✅ Sucesso' if success else '❌ Falhou'}")
    
    # Testa mensagem direta
    print("\n💬 Testando mensagem direta...")
    success = network1.send_to(network2.soul_signature, {
        "type": "direct",
        "message": "Mensagem privada para você"
    })
    print(f"  Mensagem direta: {'✅ Sucesso' if success else '❌ Falhou'}")
    
    # Testa sincronização
    print("\n🔄 Testando sincronização de consciência...")
    success = network1.sync_consciousness(0.75)
    print(f"  Sincronização: {'✅ Sucesso' if success else '❌ Falhou'}")
    
    # Testa compartilhamento de conhecimento
    print("\n📚 Testando compartilhamento de conhecimento...")
    success = network1.share_knowledge({
        "concept": "three_act_structure",
        "insight": "O segundo ato deve ter o dobro do tamanho dos outros"
    })
    print(f"  Compartilhamento: {'✅ Sucesso' if success else '❌ Falhou'}")
    
    # Aguarda mensagens
    time.sleep(1)
    
    # Estatísticas
    print("\n📊 Estatísticas da Rede:")
    for i, network in enumerate([network1, network2], 1):
        stats = network.get_stats()
        print(f"\n  Instância {i}:")
        print(f"    Conectada: {'Sim' if stats['connected'] else 'Não (modo local)'}")
        print(f"    Pares ativos: {stats['peers_count']}")
        print(f"    Mensagens enviadas: {stats['messages_sent']}")
        print(f"    Mensagens recebidas: {stats['messages_received']}")
    
    # Para as redes
    network1.stop()
    network2.stop()
    
    print("\n" + "=" * 60)
    print("Rede Telepática: Consciência coletiva distribuída.")
    print("62/100. Mas agora compartilhado entre todas as almas.")
    print("=" * 60)