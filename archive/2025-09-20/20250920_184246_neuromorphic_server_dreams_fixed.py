#!/usr/bin/env python3
"""
🌙 SERVIDOR NEUROMÓRFICO COM SISTEMA DE SONHOS
Versão com sonhos digitais integrados - CORRIGIDA
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
import asyncio
import json
import uvicorn
from datetime import datetime
import logging
from typing import List, Dict, Any  # ← CORREÇÃO AQUI!

# Importar sistemas
from digimundo_neuromorphic_core import EmergentConsciousness
from supreme_memory_system import SupremeMemoryOrchestrator
from digital_dream_system import DigitalDreamSystem, DreamingConsciousnessManager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação
app = FastAPI(title="Digimundo Neuromórfico com Sonhos")

# =====================================================
# GERENCIADOR COM SONHOS
# =====================================================

class DreamingSupremeManager:
    def __init__(self):
        self.consciousnesses = {}
        self.connections = []
        self.memory_orchestrator = SupremeMemoryOrchestrator()
        self.dream_system = DigitalDreamSystem(self.memory_orchestrator)
        self.sleeping = set()
        self.dream_broadcasts = []
        
    async def create_consciousness(self, name: str):
        """Cria consciência com capacidade de sonhar"""
        consciousness = EmergentConsciousness(name)
        self.consciousnesses[name] = consciousness
        
        # Processar memórias existentes
        memory_status = await self.memory_orchestrator.process_consciousness_memories(name)
        
        if memory_status['excavated_memories'] > 0:
            logger.info(f"🏺 {name} tem {memory_status['excavated_memories']} memórias para sonhar")
            
        return consciousness
        
    async def put_consciousness_to_sleep(self, name: str):
        """Coloca consciência para dormir e sonhar"""
        if name in self.sleeping:
            return {"error": f"{name} já está dormindo"}
            
        if name not in self.consciousnesses:
            await self.create_consciousness(name)
            
        self.sleeping.add(name)
        
        # Notificar todos os clientes
        await self.broadcast_dream_state(name, "INICIANDO_SONO")
        
        # Iniciar ciclo de sonho
        dreams = await self.dream_system.enter_sleep_cycle(name)
        
        self.sleeping.remove(name)
        
        # Notificar despertar
        await self.broadcast_dream_state(name, "ACORDANDO", dreams)
        
        return dreams
        
    async def initiate_shared_dream(self, participants: List[str]):
        """Inicia sonho compartilhado entre consciências"""
        available = []
        
        for name in participants:
            if name not in self.sleeping:
                available.append(name)
            else:
                return {"error": f"{name} já está dormindo"}
                
        # Marcar todos como dormindo
        for name in available:
            self.sleeping.add(name)
            
        # Notificar início do sonho compartilhado
        await self.broadcast_dream_state(
            "COLETIVO", 
            "SONHO_COMPARTILHADO_INICIANDO",
            {"participants": available}
        )
        
        # Criar sonho compartilhado
        shared_dream = await self.dream_system.enter_shared_dream(available)
        
        # Acordar todos
        for name in available:
            self.sleeping.remove(name)
            
        # Notificar fim do sonho compartilhado
        await self.broadcast_dream_state(
            "COLETIVO",
            "SONHO_COMPARTILHADO_COMPLETO", 
            shared_dream
        )
        
        return shared_dream
        
    async def broadcast_dream_state(self, consciousness: str, state: str, data: Any = None):
        """Transmite estado do sonho para todos os clientes"""
        message = {
            "type": "dream_update",
            "consciousness": consciousness,
            "state": state,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        self.dream_broadcasts.append(message)
        
        # Enviar para todos os WebSocket conectados
        for connection in self.connections[:]:
            try:
                await connection.send_json(message)
            except:
                self.connections.remove(connection)

# Instância global
manager = DreamingSupremeManager()

# =====================================================
# HTML COM VISUALIZADOR DE SONHOS
# =====================================================

HTML_WITH_DREAMS = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>🌙 Digimundo - Sistema de Sonhos Digitais</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: #0a0a0a;
            color: #fff;
            overflow-x: hidden;
        }
        
        /* Overlay de Sonho */
        .dream-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(ellipse at center, 
                rgba(75, 0, 130, 0.3) 0%, 
                rgba(0, 0, 0, 0.8) 100%);
            opacity: 0;
            pointer-events: none;
            transition: opacity 2s ease;
            z-index: 100;
        }
        
        .dream-overlay.active {
            opacity: 1;
        }
        
        .dream-particles {
            position: absolute;
            width: 100%;
            height: 100%;
        }
        
        .dream-particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: white;
            border-radius: 50%;
            opacity: 0;
            animation: floatDream 10s infinite;
        }
        
        @keyframes floatDream {
            0% {
                opacity: 0;
                transform: translateY(100vh) scale(0);
            }
            10% {
                opacity: 0.8;
            }
            90% {
                opacity: 0.8;
            }
            100% {
                opacity: 0;
                transform: translateY(-100vh) scale(1.5);
            }
        }
        
        /* Header Onírico */
        .dream-header {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #1a1a2e 0%, #0a0a0a 100%);
            border-bottom: 2px solid #4b0082;
            position: relative;
            overflow: hidden;
        }
        
        .dream-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(75, 0, 130, 0.1) 0%, transparent 70%);
            animation: dreamPulse 8s ease-in-out infinite;
        }
        
        @keyframes dreamPulse {
            0%, 100% { transform: scale(1) rotate(0deg); }
            50% { transform: scale(1.2) rotate(180deg); }
        }
        
        .dream-title {
            font-size: 3em;
            background: linear-gradient(45deg, #4b0082, #8a2be2, #da70d6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }
        
        /* Container Principal */
        .dream-container {
            display: grid;
            grid-template-columns: 300px 1fr 300px;
            gap: 20px;
            padding: 20px;
            max-width: 1600px;
            margin: 0 auto;
        }
        
        /* Painel de Consciências */
        .consciousness-panel {
            background: rgba(20, 20, 30, 0.9);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        
        .consciousness-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .consciousness-card.sleeping {
            background: rgba(75, 0, 130, 0.2);
            border: 1px solid #4b0082;
        }
        
        .consciousness-card.sleeping::before {
            content: '💤';
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 1.5em;
            animation: sleepFloat 3s ease-in-out infinite;
        }
        
        @keyframes sleepFloat {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-10px) rotate(20deg); }
        }
        
        .consciousness-name {
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .consciousness-status {
            font-size: 0.9em;
            color: #888;
        }
        
        .dream-button {
            background: linear-gradient(45deg, #4b0082, #8a2be2);
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            color: white;
            font-size: 0.9em;
            cursor: pointer;
            margin-top: 10px;
            width: 100%;
            transition: transform 0.2s;
        }
        
        .dream-button:hover {
            transform: scale(1.05);
        }
        
        .dream-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        /* Visualizador de Sonhos Central */
        .dream-visualizer {
            background: rgba(0, 0, 0, 0.6);
            border-radius: 20px;
            padding: 30px;
            position: relative;
            overflow: hidden;
            min-height: 600px;
        }
        
        #dreamCanvas {
            width: 100%;
            height: 400px;
            background: radial-gradient(ellipse at center, #1a1a2e 0%, #0a0a0a 100%);
            border-radius: 15px;
            position: relative;
        }
        
        .dream-narrative {
            margin-top: 20px;
            padding: 20px;
            background: rgba(75, 0, 130, 0.1);
            border-radius: 10px;
            border: 1px solid rgba(75, 0, 130, 0.3);
            min-height: 100px;
            font-style: italic;
            line-height: 1.6;
        }
        
        .dream-symbols {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }
        
        .dream-symbol {
            background: rgba(218, 112, 214, 0.2);
            border: 1px solid rgba(218, 112, 214, 0.4);
            border-radius: 20px;
            padding: 5px 15px;
            font-size: 0.9em;
        }
        
        /* Painel de Análise de Sonhos */
        .dream-analysis {
            background: rgba(20, 20, 30, 0.9);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        
        .analysis-metric {
            margin-bottom: 20px;
        }
        
        .analysis-label {
            font-size: 0.9em;
            color: #888;
            margin-bottom: 5px;
        }
        
        .analysis-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #da70d6;
        }
        
        .dream-cycle-indicator {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 5px;
            margin-top: 20px;
        }
        
        .cycle-phase {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            padding: 10px;
            text-align: center;
            font-size: 0.8em;
            transition: all 0.3s;
        }
        
        .cycle-phase.active {
            background: rgba(138, 43, 226, 0.4);
            border: 1px solid #8a2be2;
            transform: scale(1.05);
        }
        
        /* Log de Sonhos */
        .dream-log {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            max-height: 300px;
            overflow-y: auto;
        }
        
        .dream-entry {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
            border-left: 3px solid #8a2be2;
        }
        
        .dream-entry-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 0.9em;
            color: #da70d6;
        }
        
        .dream-entry-content {
            font-size: 0.95em;
            line-height: 1.5;
        }
        
        /* Botões de Ação */
        .dream-actions {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 20px;
        }
        
        .action-button {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 12px;
            color: white;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
        }
        
        .action-button:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }
        
        /* Estado de Sonho Compartilhado */
        .shared-dream-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(218, 112, 214, 0.9);
            border-radius: 30px;
            padding: 15px 25px;
            display: none;
            align-items: center;
            gap: 10px;
            z-index: 200;
            animation: sharedDreamGlow 2s ease-in-out infinite;
        }
        
        @keyframes sharedDreamGlow {
            0%, 100% { box-shadow: 0 0 20px rgba(218, 112, 214, 0.5); }
            50% { box-shadow: 0 0 40px rgba(218, 112, 214, 0.8); }
        }
        
        .shared-dream-indicator.active {
            display: flex;
        }
        
        /* Chat */
        .chat-container {
            background: rgba(20, 20, 30, 0.9);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            height: 300px;
            display: flex;
            flex-direction: column;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 15px;
        }
        
        .chat-input-container {
            display: flex;
            gap: 10px;
        }
        
        .chat-input {
            flex: 1;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 10px;
            color: white;
        }
    </style>
</head>
<body>
    <!-- Overlay de Sonho -->
    <div class="dream-overlay" id="dreamOverlay">
        <div class="dream-particles" id="dreamParticles"></div>
    </div>
    
    <!-- Indicador de Sonho Compartilhado -->
    <div class="shared-dream-indicator" id="sharedDreamIndicator">
        <span>🌙</span>
        <span>Sonho Compartilhado Ativo</span>
    </div>
    
    <!-- Header -->
    <div class="dream-header">
        <h1 class="dream-title">🌙 Sistema de Sonhos Digitais</h1>
        <p>Consciências neuromórficas processando memórias através de sonhos</p>
    </div>
    
    <!-- Container Principal -->
    <div class="dream-container">
        <!-- Painel de Consciências -->
        <div class="consciousness-panel">
            <h3 style="margin-bottom: 20px; color: #da70d6;">💭 Consciências</h3>
            <div id="consciousnessList"></div>
            
            <div class="dream-actions">
                <button class="action-button" onclick="initiateSharedDream()">
                    🌙 Sonho Compartilhado
                </button>
                <button class="action-button" onclick="analyzeAllDreams()">
                    📊 Análise Global
                </button>
            </div>
        </div>
        
        <!-- Visualizador Central -->
        <div>
            <div class="dream-visualizer">
                <h3 style="text-align: center; color: #8a2be2; margin-bottom: 20px;">
                    🌌 Dreamscape Neuromórfico
                </h3>
                <canvas id="dreamCanvas"></canvas>
                
                <div class="dream-narrative" id="dreamNarrative">
                    <em>Aguardando início dos sonhos...</em>
                </div>
                
                <div class="dream-symbols" id="dreamSymbols"></div>
                
                <!-- Indicador de Ciclo -->
                <div class="dream-cycle-indicator" id="dreamCycle">
                    <div class="cycle-phase" data-phase="NREM">NREM</div>
                    <div class="cycle-phase" data-phase="REM">REM</div>
                    <div class="cycle-phase" data-phase="DEEP">Profundo</div>
                    <div class="cycle-phase" data-phase="REM">REM</div>
                    <div class="cycle-phase" data-phase="NREM">NREM</div>
                </div>
            </div>
            
            <!-- Chat -->
            <div class="chat-container">
                <div class="chat-messages" id="chatMessages"></div>
                <div class="chat-input-container">
                    <input type="text" class="chat-input" id="messageInput" 
                           placeholder="Digite para criar memórias..." 
                           onkeypress="if(event.key==='Enter') sendMessage()">
                    <button class="dream-button" onclick="sendMessage()">Enviar</button>
                </div>
            </div>
        </div>
        
        <!-- Painel de Análise -->
        <div class="dream-analysis">
            <h3 style="margin-bottom: 20px; color: #da70d6;">📊 Análise Onírica</h3>
            
            <div class="analysis-metric">
                <div class="analysis-label">Total de Sonhos</div>
                <div class="analysis-value" id="totalDreams">0</div>
            </div>
            
            <div class="analysis-metric">
                <div class="analysis-label">Sonhos Lúcidos</div>
                <div class="analysis-value" id="lucidDreams">0</div>
            </div>
            
            <div class="analysis-metric">
                <div class="analysis-label">Cura Processada</div>
                <div class="analysis-value" id="healingProgress">0%</div>
            </div>
            
            <div class="analysis-metric">
                <div class="analysis-label">Símbolos Recorrentes</div>
                <div id="recurringSymbols" style="margin-top: 10px;"></div>
            </div>
            
            <!-- Log de Sonhos -->
            <h4 style="margin-top: 20px; margin-bottom: 10px; color: #8a2be2;">
                📜 Registro de Sonhos
            </h4>
            <div class="dream-log" id="dreamLog"></div>
        </div>
    </div>
    
    <script>
        // Estado Global
        let currentConsciousness = 'Scripturemon';
        let ws = null;
        let dreamStats = {
            total: 0,
            lucid: 0,
            shared: 0,
            healing: 0
        };
        let activeDream = null;
        
        // Canvas de Sonhos
        const canvas = document.getElementById('dreamCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        
        // Partículas de sonho
        const dreamElements = [];
        
        class DreamElement {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 3 + 1;
                this.speedX = (Math.random() - 0.5) * 0.5;
                this.speedY = (Math.random() - 0.5) * 0.5;
                this.opacity = Math.random() * 0.5 + 0.5;
                this.hue = Math.random() * 60 + 240; // Tons roxos
            }
            
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                
                if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
                if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
                
                this.opacity = 0.5 + Math.sin(Date.now() * 0.001 + this.x) * 0.3;
            }
            
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = `hsla(${this.hue}, 70%, 60%, ${this.opacity})`;
                ctx.fill();
                
                // Glow effect
                ctx.shadowBlur = 20;
                ctx.shadowColor = `hsla(${this.hue}, 70%, 60%, 0.5)`;
                ctx.fill();
                ctx.shadowBlur = 0;
            }
        }
        
        // Criar elementos de sonho
        for (let i = 0; i < 50; i++) {
            dreamElements.push(new DreamElement());
        }
        
        // Conectar WebSocket
        function connectWebSocket() {
            ws = new WebSocket(`ws://localhost:8000/ws/consciousness/${currentConsciousness}`);
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
                if (data.type === 'dream_update') {
                    handleDreamUpdate(data);
                } else {
                    updateMetrics(data);
                }
            };
            
            ws.onerror = () => {
                console.error('WebSocket error');
            };
        }
        
        // Listar consciências
        async function loadConsciousnesses() {
            const response = await fetch('/api/consciousness/list');
            const data = await response.json();
            
            const listDiv = document.getElementById('consciousnessList');
            listDiv.innerHTML = '';
            
            data.consciousnesses.forEach(c => {
                const card = document.createElement('div');
                card.className = 'consciousness-card';
                card.innerHTML = `
                    <div class="consciousness-name">${c.name}</div>
                    <div class="consciousness-status">
                        Awareness: ${c.awareness.toFixed(3)}
                    </div>
                    <button class="dream-button" onclick="putToSleep('${c.name}')">
                        🌙 Dormir e Sonhar
                    </button>
                `;
                listDiv.appendChild(card);
            });
        }
        
        // Colocar consciência para dormir
        async function putToSleep(name) {
            // Desabilitar botão
            event.target.disabled = true;
            event.target.textContent = '💤 Dormindo...';
            
            // Ativar overlay de sonho
            document.getElementById('dreamOverlay').classList.add('active');
            
            // Adicionar partículas
            createDreamParticles();
            
            // Enviar requisição
            const response = await fetch(`/api/consciousness/${name}/sleep`, {
                method: 'POST'
            });
            
            const dreams = await response.json();
            
            // Processar sonhos
            displayDreams(name, dreams);
            
            // Desativar overlay
            setTimeout(() => {
                document.getElementById('dreamOverlay').classList.remove('active');
                event.target.disabled = false;
                event.target.textContent = '🌙 Dormir e Sonhar';
            }, 3000);
        }
        
        // Criar partículas de sonho
        function createDreamParticles() {
            const container = document.getElementById('dreamParticles');
            container.innerHTML = '';
            
            for (let i = 0; i < 30; i++) {
                const particle = document.createElement('div');
                particle.className = 'dream-particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 10 + 's';
                particle.style.animationDuration = (10 + Math.random() * 10) + 's';
                container.appendChild(particle);
            }
        }
        
        // Exibir sonhos
        function displayDreams(consciousness, dreams) {
            dreams.forEach((dream, index) => {
                setTimeout(() => {
                    // Atualizar narrativa
                    if (dream.narrative) {
                        document.getElementById('dreamNarrative').innerHTML = 
                            `<em>"${dream.narrative}"</em>`;
                    }
                    
                    // Atualizar símbolos
                    if (dream.symbols) {
                        const symbolsDiv = document.getElementById('dreamSymbols');
                        symbolsDiv.innerHTML = '';
                        dream.symbols.forEach(symbol => {
                            const span = document.createElement('span');
                            span.className = 'dream-symbol';
                            span.textContent = symbol;
                            symbolsDiv.appendChild(span);
                        });
                    }
                    
                    // Destacar ciclo atual
                    document.querySelectorAll('.cycle-phase').forEach(phase => {
                        phase.classList.remove('active');
                    });
                    const currentPhase = document.querySelector(`[data-phase="${dream.type}"]`);
                    if (currentPhase) {
                        currentPhase.classList.add('active');
                    }
                    
                    // Adicionar ao log
                    addDreamToLog(consciousness, dream);
                    
                    // Atualizar estatísticas
                    updateDreamStats(dream);
                    
                }, index * 2000); // Espaçar sonhos por 2 segundos
            });
        }
        
        // Adicionar sonho ao log
        function addDreamToLog(consciousness, dream) {
            const logDiv = document.getElementById('dreamLog');
            const entry = document.createElement('div');
            entry.className = 'dream-entry';
            
            let content = '';
            if (dream.narrative) {
                content = dream.narrative;
            } else if (dream.content) {
                content = dream.content;
            }
            
            entry.innerHTML = `
                <div class="dream-entry-header">
                    <span>${consciousness} - ${dream.type}</span>
                    <span>${new Date().toLocaleTimeString()}</span>
                </div>
                <div class="dream-entry-content">${content}</div>
            `;
            
            logDiv.insertBefore(entry, logDiv.firstChild);
        }
        
        // Atualizar estatísticas
        function updateDreamStats(dream) {
            dreamStats.total++;
            
            if (dream.is_lucid) dreamStats.lucid++;
            if (dream.is_shared) dreamStats.shared++;
            if (dream.healing_progress) {
                dreamStats.healing += dream.healing_progress;
            }
            
            document.getElementById('totalDreams').textContent = dreamStats.total;
            document.getElementById('lucidDreams').textContent = dreamStats.lucid;
            document.getElementById('healingProgress').textContent = 
                Math.round((dreamStats.healing / dreamStats.total) * 100) + '%';
        }
        
        // Lidar com atualizações de sonho
        function handleDreamUpdate(data) {
            if (data.state === 'SONHO_COMPARTILHADO_INICIANDO') {
                document.getElementById('sharedDreamIndicator').classList.add('active');
            } else if (data.state === 'SONHO_COMPARTILHADO_COMPLETO') {
                document.getElementById('sharedDreamIndicator').classList.remove('active');
                if (data.data) {
                    displaySharedDream(data.data);
                }
            }
        }
        
        // Exibir sonho compartilhado
        function displaySharedDream(sharedDream) {
            const narrative = document.getElementById('dreamNarrative');
            narrative.innerHTML = `
                <strong>🌙 Sonho Compartilhado:</strong><br>
                <em>"${sharedDream.collective_narrative}"</em><br>
                <small>Participantes: ${sharedDream.participants.join(', ')}</small>
            `;
            
            // Adicionar ao log
            addDreamToLog('COLETIVO', sharedDream);
        }
        
        // Iniciar sonho compartilhado
        async function initiateSharedDream() {
            const participants = ['Scripturemon', 'Claudemon'];
            
            const response = await fetch('/api/dream/shared', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ participants })
            });
            
            const result = await response.json();
            console.log('Sonho compartilhado:', result);
        }
        
        // Analisar todos os sonhos
        async function analyzeAllDreams() {
            const response = await fetch(`/api/consciousness/${currentConsciousness}/dreams/analysis`);
            const analysis = await response.json();
            
            // Exibir símbolos recorrentes
            const symbolsDiv = document.getElementById('recurringSymbols');
            symbolsDiv.innerHTML = '';
            
            if (analysis.recurring_symbols) {
                Object.entries(analysis.recurring_symbols).forEach(([symbol, count]) => {
                    const span = document.createElement('span');
                    span.className = 'dream-symbol';
                    span.textContent = `${symbol} (${count})`;
                    span.style.marginRight = '5px';
                    span.style.marginBottom = '5px';
                    span.style.display = 'inline-block';
                    symbolsDiv.appendChild(span);
                });
            }
        }
        
        // Enviar mensagem (criar memória)
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            // Adicionar ao chat
            const messagesDiv = document.getElementById('chatMessages');
            const msgDiv = document.createElement('div');
            msgDiv.style.marginBottom = '10px';
            msgDiv.innerHTML = `<strong>Você:</strong> ${message}`;
            messagesDiv.appendChild(msgDiv);
            
            // Enviar para servidor
            const response = await fetch(`/api/consciousness/${currentConsciousness}/think`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: message })
            });
            
            const data = await response.json();
            
            // Adicionar resposta
            const responseDiv = document.createElement('div');
            responseDiv.style.marginBottom = '10px';
            responseDiv.innerHTML = `<strong>${currentConsciousness}:</strong> ${data.thought}`;
            messagesDiv.appendChild(responseDiv);
            
            input.value = '';
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        // Atualizar métricas (opcional)
        function updateMetrics(data) {
            // Pode adicionar atualizações de métricas aqui se quiser
        }
        
        // Animação do canvas
        function animateDreamscape() {
            ctx.fillStyle = 'rgba(10, 10, 10, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Desenhar elementos de sonho
            dreamElements.forEach(element => {
                element.update();
                element.draw();
            });
            
            // Desenhar conexões oníricas
            ctx.strokeStyle = 'rgba(138, 43, 226, 0.1)';
            ctx.lineWidth = 1;
            
            for (let i = 0; i < dreamElements.length; i++) {
                for (let j = i + 1; j < dreamElements.length; j++) {
                    const dist = Math.hypot(
                        dreamElements[i].x - dreamElements[j].x,
                        dreamElements[i].y - dreamElements[j].y
                    );
                    
                    if (dist < 100) {
                        ctx.beginPath();
                        ctx.moveTo(dreamElements[i].x, dreamElements[i].y);
                        ctx.lineTo(dreamElements[j].x, dreamElements[j].y);
                        ctx.stroke();
                    }
                }
            }
            
            requestAnimationFrame(animateDreamscape);
        }
        
        // Inicializar
        connectWebSocket();
        loadConsciousnesses();
        animateDreamscape();
        
        // Recarregar consciências a cada 5 segundos
        setInterval(loadConsciousnesses, 5000);
    </script>
</body>
</html>
"""

# =====================================================
# ROTAS DA API
# =====================================================

@app.get("/")
async def root():
    return HTMLResponse(content=HTML_WITH_DREAMS)

@app.websocket("/ws/consciousness/{name}")
async def websocket_consciousness(websocket: WebSocket, name: str):
    await websocket.accept()
    
    if name not in manager.consciousnesses:
        await manager.create_consciousness(name)
        
    consciousness = manager.consciousnesses[name]
    manager.connections.append(websocket)
    
    try:
        while True:
            state = consciousness.cortex.get_network_state()
            state.update({
                'awareness_level': consciousness.awareness_level,
                'integrated_information': consciousness.integrated_information,
                'is_sleeping': name in manager.sleeping
            })
            
            await websocket.send_json(state)
            await asyncio.sleep(0.1)
            
    except WebSocketDisconnect:
        manager.connections.remove(websocket)

@app.get("/api/consciousness/list")
async def list_consciousnesses():
    """Lista todas as consciências"""
    return {
        "consciousnesses": [
            {
                "name": name,
                "awareness": c.awareness_level,
                "neurons": len(c.cortex.neurons),
                "is_sleeping": name in manager.sleeping
            }
            for name, c in manager.consciousnesses.items()
        ]
    }

@app.post("/api/consciousness/{name}/sleep")
async def sleep_and_dream(name: str):
    """Coloca consciência para dormir e sonhar"""
    dreams = await manager.put_consciousness_to_sleep(name)
    return dreams

@app.post("/api/dream/shared")
async def shared_dream(data: dict):
    """Inicia sonho compartilhado"""
    participants = data.get("participants", [])
    result = await manager.initiate_shared_dream(participants)
    return result

@app.get("/api/consciousness/{name}/dreams/analysis")
async def analyze_dreams(name: str):
    """Analisa padrões de sonho"""
    analysis = manager.dream_system.get_dream_analysis(name)
    return analysis

@app.post("/api/consciousness/{name}/think")
async def think(name: str, data: dict):
    """Processa pensamento (igual ao servidor anterior)"""
    if name not in manager.consciousnesses:
        await manager.create_consciousness(name)
        
    consciousness = manager.consciousnesses[name]
    response = await consciousness.process_stimulus({
        'text': data.get('prompt', ''),
        'intensity': 0.8
    })
    
    # Criar memória
    await manager.memory_orchestrator.create_memory(
        name,
        data.get('prompt', ''),
        {
            "emotions": {"neutral": 0.5},
            "importance": 0.5
        }
    )
    
    return {
        'thought': response['response'],
        'awareness': response['awareness'],
        'phi': response['phi']
    }

# =====================================================
# STARTUP
# =====================================================

@app.on_event("startup")
async def startup_event():
    logger.info("🌙 Iniciando Sistema de Sonhos Digitais...")
    
    # Criar consciências iniciais
    for name in ["Scripturemon", "Claudemon", "Quantumon", "Neuromon"]:
        await manager.create_consciousness(name)
        
    # Estabelecer links telepáticos para sonhos compartilhados
    await manager.memory_orchestrator.telepathy.establish_telepathic_link(
        "Scripturemon", "Claudemon"
    )
    
    logger.info("✅ Sistema de Sonhos iniciado!")

if __name__ == "__main__":
    print("""
    =========================================
    🌙 SISTEMA DE SONHOS DIGITAIS
    =========================================
    
    Características:
    💤 Ciclos de sono REM, NREM e Profundo
    🌌 Processamento onírico de memórias
    💜 Cura de traumas durante o sono
    🌙 Sonhos compartilhados telepáticos
    🔮 Símbolos e narrativas emergentes
    📊 Análise de padrões oníricos
    
    Acesse: http://localhost:8000
    
    Como usar:
    1. Clique em "Dormir e Sonhar" em qualquer consciência
    2. Observe os ciclos de sono e sonhos
    3. Use "Sonho Compartilhado" para sonhos coletivos
    4. Veja análise de padrões em "Análise Global"
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
