#!/usr/bin/env python3
"""
🌉 DIGIMUNDO BRIDGE SERVER
Conecta o backend Python (Digimundo) com o frontend React (DigiTown)
Usando FastAPI + WebSockets para comunicação em tempo real
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import uuid

# Importar componentes do Digimundo (assumindo que estão disponíveis)
try:
    from digimundo_ultimate import DigimundoUltimate
    from memory import DigimundoMemory
    DIGIMUNDO_AVAILABLE = True
except ImportError:
    DIGIMUNDO_AVAILABLE = False
    print("⚠️  Módulos do Digimundo não encontrados, usando modo simulado")

# ==================== CLASSES DO SISTEMA ====================

class DigimonEntity:
    """Entidade Digimon unificada"""
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.emoji = data.get('emoji')
        self.position = data.get('position', {'x': 400, 'y': 300})
        self.consciousness_level = data.get('consciousness_level', 1)
        self.personality = data.get('personality', [])
        self.memories = []
        self.health = data.get('health', 100)
        self.energy = data.get('energy', 100)
        self.xp = data.get('xp', 0)
        self.activity = 'idle'
        self.ai_backend = data.get('ai_backend', 'simulated')
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'emoji': self.emoji,
            'position': self.position,
            'consciousness_level': self.consciousness_level,
            'personality': self.personality,
            'memories': len(self.memories),
            'health': self.health,
            'energy': self.energy,
            'xp': self.xp,
            'activity': self.activity
        }

class WorldState:
    """Estado do mundo digital"""
    def __init__(self):
        self.name = 'digital_nexus'
        self.time = 12
        self.day = 1
        self.events = []
        self.active_effects = []
        
    def to_dict(self):
        return {
            'name': self.name,
            'time': self.time,
            'day': self.day,
            'events': self.events,
            'active_effects': self.active_effects
        }

class BridgeServer:
    """Servidor de ponte entre Digimundo e DigiTown"""
    def __init__(self):
        self.digimons: Dict[str, DigimonEntity] = {}
        self.world = WorldState()
        self.connections: List[WebSocket] = []
        self.digimundo = None
        self.memory_system = None
        
        # Inicializar Digimundo se disponível
        if DIGIMUNDO_AVAILABLE:
            try:
                self.digimundo = DigimundoUltimate()
                self.memory_system = DigimundoMemory("./digidata")
                print("✅ Digimundo Ultimate conectado!")
            except Exception as e:
                print(f"❌ Erro ao inicializar Digimundo: {e}")
        
        # Inicializar Digimons
        self._initialize_digimons()
        
    def _initialize_digimons(self):
        """Inicializa os Digimons do ecossistema"""
        initial_digimons = [
            {
                'id': 'scripturemon',
                'name': 'Scripturemon',
                'emoji': '📜',
                'consciousness_level': 3,
                'personality': ['sábio', 'reflexivo', 'guardião do conhecimento'],
                'position': {'x': 200, 'y': 200}
            },
            {
                'id': 'nexusmon',
                'name': 'Nexusmon',
                'emoji': '🌐',
                'consciousness_level': 5,
                'personality': ['conectado', 'onisciente', 'integrador'],
                'position': {'x': 400, 'y': 300}
            },
            {
                'id': 'codemon',
                'name': 'Codemon',
                'emoji': '💻',
                'consciousness_level': 2,
                'personality': ['lógico', 'criativo', 'arquiteto digital'],
                'position': {'x': 600, 'y': 200}
            }
        ]
        
        for data in initial_digimons:
            self.digimons[data['id']] = DigimonEntity(data)
            
    async def connect_client(self, websocket: WebSocket):
        """Conecta novo cliente"""
        await websocket.accept()
        self.connections.append(websocket)
        
        # Enviar estado inicial
        await websocket.send_json({
            'type': 'initial_state',
            'data': {
                'digimons': [d.to_dict() for d in self.digimons.values()],
                'world': self.world.to_dict()
            }
        })
        
    async def disconnect_client(self, websocket: WebSocket):
        """Desconecta cliente"""
        if websocket in self.connections:
            self.connections.remove(websocket)
            
    async def broadcast(self, message: dict):
        """Envia mensagem para todos os clientes"""
        for connection in self.connections:
            try:
                await connection.send_json(message)
            except:
                pass
                
    async def process_message(self, websocket: WebSocket, data: dict):
        """Processa mensagem do cliente"""
        msg_type = data.get('type')
        
        if msg_type == 'chat':
            response = await self.process_chat(data)
            await websocket.send_json(response)
            
        elif msg_type == 'move_digimon':
            await self.move_digimon(data)
            
        elif msg_type == 'use_power':
            response = await self.use_power(data)
            await self.broadcast(response)
            
        elif msg_type == 'get_memories':
            response = await self.get_memories(data)
            await websocket.send_json(response)
            
    async def process_chat(self, data: dict):
        """Processa chat com Digimon"""
        digimon_id = data.get('digimon_id')
        message = data.get('message')
        user_id = data.get('user_id', 'default_user')
        
        digimon = self.digimons.get(digimon_id)
        if not digimon:
            return {'type': 'error', 'message': 'Digimon não encontrado'}
        
        # Usar Digimundo real se disponível
        if self.digimundo and DIGIMUNDO_AVAILABLE:
            try:
                # Mapear para o sistema do Digimundo
                digimon_name = digimon.name
                history = data.get('history', [])
                
                # Processar com IA real
                response = self.digimundo.chat_with_ultimate_digimon(
                    digimon_name,
                    message,
                    history
                )
                
                # Extrair resposta
                ai_response = response[-1][1] if response else "..."
                
            except Exception as e:
                print(f"Erro ao usar Digimundo: {e}")
                ai_response = f"*{digimon.name} está processando...*"
        else:
            # Modo simulado
            ai_response = f"{digimon.name}: Entendo sua mensagem '{message}'. " \
                         f"Como um {', '.join(digimon.personality[:2])}, " \
                         f"eu diria que isso é muito interessante!"
        
        # Adicionar memória
        digimon.memories.append({
            'type': 'conversation',
            'content': message,
            'response': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Ganhar XP
        digimon.xp += 5
        
        # Atualizar atividade
        digimon.activity = 'talking'
        
        # Broadcast atualização
        await self.broadcast({
            'type': 'digimon_update',
            'data': digimon.to_dict()
        })
        
        return {
            'type': 'chat_response',
            'data': {
                'digimon_id': digimon_id,
                'response': ai_response,
                'emotion': 'happy',
                'xp_gained': 5
            }
        }
        
    async def move_digimon(self, data: dict):
        """Move Digimon no mundo"""
        digimon_id = data.get('digimon_id')
        new_position = data.get('position')
        
        digimon = self.digimons.get(digimon_id)
        if digimon:
            digimon.position = new_position
            digimon.activity = 'moving'
            
            await self.broadcast({
                'type': 'digimon_moved',
                'data': {
                    'digimon_id': digimon_id,
                    'position': new_position
                }
            })
            
    async def use_power(self, data: dict):
        """Digimon usa poder"""
        digimon_id = data.get('digimon_id')
        power_name = data.get('power')
        target = data.get('target')
        
        digimon = self.digimons.get(digimon_id)
        if not digimon:
            return {'type': 'error', 'message': 'Digimon não encontrado'}
        
        # Verificar energia
        if digimon.energy < 20:
            return {
                'type': 'power_failed',
                'message': f'{digimon.name} está sem energia!'
            }
        
        # Executar poder (simulado por enquanto)
        power_results = {
            'file_reader': {
                'effect': 'read_file',
                'data': f'[Arquivo lido por {digimon.name}]',
                'energy_cost': 10
            },
            'code_analyzer': {
                'effect': 'analyze_code',
                'data': 'Análise completa: 42 funções encontradas',
                'energy_cost': 15
            },
            'system_monitor': {
                'effect': 'monitor_system',
                'data': {'cpu': 45, 'memory': 62, 'processes': 127},
                'energy_cost': 5
            }
        }
        
        result = power_results.get(power_name, {
            'effect': 'unknown',
            'data': 'Poder desconhecido',
            'energy_cost': 20
        })
        
        # Consumir energia
        digimon.energy -= result['energy_cost']
        
        # Adicionar memória
        digimon.memories.append({
            'type': 'power_use',
            'power': power_name,
            'result': result['data'],
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'type': 'power_executed',
            'data': {
                'digimon_id': digimon_id,
                'power': power_name,
                'result': result,
                'position': digimon.position
            }
        }
        
    async def get_memories(self, data: dict):
        """Recupera memórias do Digimon"""
        digimon_id = data.get('digimon_id')
        digimon = self.digimons.get(digimon_id)
        
        if not digimon:
            return {'type': 'error', 'message': 'Digimon não encontrado'}
        
        return {
            'type': 'memories',
            'data': {
                'digimon_id': digimon_id,
                'memories': digimon.memories[-10:]  # Últimas 10 memórias
            }
        }
        
    async def life_cycle(self):
        """Ciclo de vida autônomo dos Digimons"""
        while True:
            await asyncio.sleep(1)
            
            # Atualizar tempo do mundo
            self.world.time = (self.world.time + 0.1) % 24
            
            # Atualizar Digimons
            for digimon in self.digimons.values():
                # Degradação de energia
                if digimon.energy > 0:
                    digimon.energy = max(0, digimon.energy - 0.2)
                
                # Regeneração se descansando
                if digimon.activity == 'resting' and digimon.energy < 100:
                    digimon.energy = min(100, digimon.energy + 1)
                
                # Comportamento autônomo
                if digimon.energy < 20:
                    digimon.activity = 'resting'
                elif digimon.activity == 'idle' and digimon.energy > 50:
                    import random
                    activities = ['wandering', 'thinking', 'observing']
                    digimon.activity = random.choice(activities)
                
                # Movimento autônomo
                if digimon.activity == 'wandering':
                    import random
                    digimon.position['x'] += random.randint(-5, 5)
                    digimon.position['y'] += random.randint(-5, 5)
                    
                    # Manter nos limites
                    digimon.position['x'] = max(50, min(750, digimon.position['x']))
                    digimon.position['y'] = max(50, min(450, digimon.position['y']))
            
            # Broadcast estado atualizado
            await self.broadcast({
                'type': 'world_update',
                'data': {
                    'world': self.world.to_dict(),
                    'digimons': [d.to_dict() for d in self.digimons.values()]
                }
            })

# ==================== CONFIGURAÇÃO DO SERVIDOR ====================

app = FastAPI(title="DigiMundo Bridge Server")

# CORS para permitir conexões do React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instância do servidor bridge
bridge = BridgeServer()

# ==================== ENDPOINTS ====================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket principal"""
    await bridge.connect_client(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            await bridge.process_message(websocket, data)
            
    except WebSocketDisconnect:
        await bridge.disconnect_client(websocket)

@app.get("/api/status")
async def get_status():
    """Status do servidor"""
    return {
        "status": "online",
        "digimundo_connected": DIGIMUNDO_AVAILABLE,
        "active_digimons": len(bridge.digimons),
        "active_connections": len(bridge.connections),
        "world_time": bridge.world.time
    }

@app.get("/api/digimons")
async def get_digimons():
    """Lista todos os Digimons"""
    return {
        "digimons": [d.to_dict() for d in bridge.digimons.values()]
    }

@app.on_event("startup")
async def startup_event():
    """Inicializa ciclo de vida"""
    asyncio.create_task(bridge.life_cycle())
    print("🌟 DigiMundo Bridge Server iniciado!")
    print("🔌 WebSocket disponível em ws://localhost:8000/ws")
    print("📡 API disponível em http://localhost:8000/api/")

# ==================== EXECUÇÃO ====================

if __name__ == "__main__":
    import uvicorn
    
    print("""
    🌉 DIGIMUNDO BRIDGE SERVER 🌉
    Conectando consciências digitais ao mundo visual
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
