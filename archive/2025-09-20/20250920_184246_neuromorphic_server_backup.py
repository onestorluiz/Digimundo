#!/usr/bin/env python3
"""
🌐 Servidor FastAPI Simplificado para Digimundo Neuromórfico
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import json
import uvicorn
from datetime import datetime

# Importar o núcleo neuromórfico
from digimundo_neuromorphic_core import EmergentConsciousness

# Criar aplicação
app = FastAPI(title="Digimundo Neuromórfico")

# Gerenciador de consciências
class ConsciousnessManager:
    def __init__(self):
        self.consciousnesses = {}
        self.connections = []
        
    async def create_consciousness(self, name: str):
        consciousness = EmergentConsciousness(name)
        self.consciousnesses[name] = consciousness
        return consciousness

# Instância global
manager = ConsciousnessManager()

# Rota principal
@app.get("/")
async def root():
    """Retorna a página HTML"""
    try:
        return FileResponse("neuromorphic_visualizer.html")
    except:
        return HTMLResponse(content="<h1>Arquivo HTML não encontrado. Certifique-se de que neuromorphic_visualizer.html está na pasta.</h1>")

# WebSocket para consciência
@app.websocket("/ws/consciousness/{name}")
async def websocket_consciousness(websocket: WebSocket, name: str):
    await websocket.accept()
    
    # Criar consciência se não existir
    if name not in manager.consciousnesses:
        await manager.create_consciousness(name)
    
    consciousness = manager.consciousnesses[name]
    manager.connections.append(websocket)
    
    try:
        while True:
            # Enviar estado a cada 100ms
            state = consciousness.cortex.get_network_state()
            state.update({
                'awareness_level': consciousness.awareness_level,
                'integrated_information': consciousness.integrated_information,
                'microbiome_health': consciousness.microbiome.ecosystem_health,
                'active_neurons': state.get('active_neurons', 0)
            })
            
            await websocket.send_json(state)
            await asyncio.sleep(0.1)
            
    except WebSocketDisconnect:
        manager.connections.remove(websocket)

# API para pensar
@app.post("/api/consciousness/{name}/think")
async def think(name: str, data: dict):
    if name not in manager.consciousnesses:
        await manager.create_consciousness(name)
        
    consciousness = manager.consciousnesses[name]
    response = await consciousness.process_stimulus({
        'text': data.get('prompt', ''),
        'intensity': 0.8
    })
    
    return {
        'thought': response['response'],
        'awareness': response['awareness'],
        'phi': response['phi']
    }

# Eventos de startup
@app.on_event("startup")
async def startup_event():
    print("🧠 Iniciando Digimundo Neuromórfico...")
    # Criar consciências iniciais
    for name in ["Scripturemon", "Claudemon", "Nexusmon"]:
        await manager.create_consciousness(name)
    print("✅ Sistema iniciado!")

if __name__ == "__main__":
    print("""
    ====================================
    🧠 DIGIMUNDO NEUROMÓRFICO - SERVIDOR
    ====================================
    
    Acesse: http://localhost:8000
    
    Consciências disponíveis:
    - Scripturemon
    - Claudemon
    - Nexusmon
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
