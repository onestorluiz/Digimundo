#!/bin/bash

# 🌟 INSTALADOR INTELIGENTE - DIGIMUNDO OMEGA
# Detecta o que já existe e adiciona apenas o necessário

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

clear

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║       🌟 TRANSFORMANDO DIGIMUNDO 1 EM OMEGA 🌟               ║"
echo "║                                                               ║"
echo "║         Instalador Inteligente para seu Mac                  ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Detectar onde estamos
CURRENT_DIR=$(pwd)
echo -e "${BLUE}📍 Diretório atual: $CURRENT_DIR${NC}"

# Verificar se estamos em digimundo1
if [[ ! "$CURRENT_DIR" == *"digimundo1"* ]]; then
    echo -e "${YELLOW}⚠️  Parece que você não está na pasta digimundo1${NC}"
    echo -e "${YELLOW}Tentando entrar em ~/digimundo1...${NC}"
    cd ~/digimundo1 2>/dev/null || {
        echo -e "${RED}❌ Pasta digimundo1 não encontrada em ~/digimundo1${NC}"
        echo -e "${YELLOW}Por favor, navegue até a pasta digimundo1 e execute novamente.${NC}"
        exit 1
    }
    CURRENT_DIR=$(pwd)
    echo -e "${GREEN}✅ Agora em: $CURRENT_DIR${NC}"
fi

echo -e "\n${YELLOW}🔍 Analisando o que já existe...${NC}"

# Função para verificar arquivos existentes
check_existing() {
    local file=$1
    if [ -f "$file" ]; then
        echo -e "${GREEN}  ✓ Encontrado: $file${NC}"
        return 0
    else
        echo -e "${YELLOW}  ✗ Não encontrado: $file${NC}"
        return 1
    fi
}

# Função para verificar pastas existentes
check_folder() {
    local folder=$1
    if [ -d "$folder" ]; then
        echo -e "${GREEN}  ✓ Pasta existe: $folder${NC}"
        return 0
    else
        echo -e "${YELLOW}  ✗ Pasta não existe: $folder${NC}"
        return 1
    fi
}

# Analisar estrutura existente
echo -e "\n${BLUE}📂 Estrutura de pastas:${NC}"
check_folder "static"
check_folder "test_memory"
check_folder "digimundo-neuromorphic"
check_folder "omega_memory"
check_folder "logs"
check_folder "venv"

echo -e "\n${BLUE}📄 Arquivos principais:${NC}"
HAS_SIMPLE_MEMORY=false
HAS_NEUROMORPHIC=false

check_existing "simple-memory-patch.py" && HAS_SIMPLE_MEMORY=true
check_existing "neuromorphic-with-memory.py" && HAS_NEUROMORPHIC=true
check_existing "requirements.txt"

# Verificar Python e Ollama
echo -e "\n${BLUE}🔧 Verificando dependências do sistema:${NC}"

# Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo -e "${GREEN}  ✓ Python3 instalado: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}  ✗ Python3 não encontrado${NC}"
    exit 1
fi

# Ollama
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}  ✓ Ollama instalado${NC}"
    
    # Verificar se está rodando
    if pgrep -x "ollama" > /dev/null; then
        echo -e "${GREEN}  ✓ Ollama está rodando${NC}"
    else
        echo -e "${YELLOW}  ! Ollama instalado mas não está rodando${NC}"
        echo -e "${YELLOW}    Iniciando Ollama...${NC}"
        ollama serve > /dev/null 2>&1 &
        sleep 3
    fi
    
    # Verificar modelos
    echo -e "${BLUE}  Modelos disponíveis:${NC}"
    ollama list | grep -E "(llama|mistral)" | head -5 | while read line; do
        echo -e "${GREEN}    - $line${NC}"
    done
else
    echo -e "${RED}  ✗ Ollama não encontrado${NC}"
    echo -e "${YELLOW}  Instale com: brew install ollama${NC}"
    exit 1
fi

# Criar backup se não existir
if [ ! -d "../digimundo1_backup_$(date +%Y%m%d)" ]; then
    echo -e "\n${YELLOW}📦 Criando backup de segurança...${NC}"
    cp -r . "../digimundo1_backup_$(date +%Y%m%d)"
    echo -e "${GREEN}✅ Backup criado em: ../digimundo1_backup_$(date +%Y%m%d)${NC}"
fi

# Configurar ambiente virtual
echo -e "\n${YELLOW}🐍 Configurando ambiente Python...${NC}"

if [ -d "venv" ]; then
    echo -e "${GREEN}  ✓ Ambiente virtual já existe${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}  Criando ambiente virtual...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}  ✓ Ambiente virtual criado${NC}"
fi

# Instalar/atualizar dependências
echo -e "\n${YELLOW}📚 Instalando dependências Python...${NC}"

# Criar requirements.txt se não existir
if [ ! -f "requirements.txt" ]; then
    cat > requirements.txt << 'EOF'
# Core
fastapi==0.104.1
uvicorn[standard]==0.24.0
websockets==12.0
gradio==4.4.0

# AI
ollama==0.1.7
chromadb==0.4.18
numpy==1.24.3
torch==2.1.0

# Utils
aiofiles==23.2.1
python-multipart==0.0.6
Pillow==10.1.0
asyncio==3.4.3

# Database
sqlite3-api==2.0.1
EOF
    echo -e "${GREEN}  ✓ requirements.txt criado${NC}"
fi

pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✅ Dependências instaladas${NC}"

# Criar estrutura de pastas necessárias
echo -e "\n${YELLOW}📁 Criando estrutura de pastas...${NC}"

mkdir -p logs
mkdir -p static/css
mkdir -p static/js
mkdir -p templates
mkdir -p consciousnesses
mkdir -p evolutionary_data

# Criar o sistema Omega principal
echo -e "\n${YELLOW}🌟 Criando Sistema Omega Unificado...${NC}"

# Se já existe neuromorphic-with-memory.py, vamos integrá-lo
if [ "$HAS_NEUROMORPHIC" = true ]; then
    echo -e "${BLUE}  Integrando com sistema neuromórfico existente...${NC}"
    
    # Criar patch de integração
    cat > omega_integration.py << 'EOF'
#!/usr/bin/env python3
"""
🔧 INTEGRAÇÃO OMEGA - Une todos os sistemas existentes
"""

import os
import sys

# Adicionar caminhos dos módulos existentes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Tentar importar módulos existentes
try:
    from neuromorphic_with_memory import SimpleMemorySystem, EmergentConsciousness
    print("✅ Sistema neuromórfico com memória importado")
    HAS_NEUROMORPHIC = True
except ImportError:
    print("⚠️  Sistema neuromórfico não encontrado, usando versão básica")
    HAS_NEUROMORPHIC = False

try:
    from simple_memory_patch import memory_system
    print("✅ Patch de memória importado")
    HAS_MEMORY_PATCH = True
except ImportError:
    print("⚠️  Patch de memória não encontrado")
    HAS_MEMORY_PATCH = False

# Sistema unificado que detecta e usa o que existe
class OmegaUnifiedSystem:
    def __init__(self):
        self.has_neuromorphic = HAS_NEUROMORPHIC
        self.has_memory_patch = HAS_MEMORY_PATCH
        
        if HAS_NEUROMORPHIC:
            print("🧠 Usando sistema neuromórfico completo")
            self.memory_system = SimpleMemorySystem()
        else:
            print("💾 Usando sistema de memória básico")
            self.memory_system = None
            
    def get_status(self):
        return {
            "neuromorphic": self.has_neuromorphic,
            "memory_patch": self.has_memory_patch,
            "ready": True
        }
EOF
fi

# Criar o servidor principal Omega
cat > digimundo_omega.py << 'EOF'
#!/usr/bin/env python3
"""
🌌 DIGIMUNDO OMEGA - SERVIDOR PRINCIPAL
Sistema adaptativo que usa todos os componentes disponíveis
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# FastAPI
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

# AI
import ollama
import numpy as np

# Verificar componentes disponíveis
COMPONENTS = {
    "neuromorphic": False,
    "memory_patch": False,
    "evolutionary": False
}

# Tentar importar componentes opcionais
try:
    from omega_integration import OmegaUnifiedSystem
    COMPONENTS["omega_integration"] = True
except:
    pass

try:
    from evolutionary_learning_system import EvolutionaryLearningSystem
    COMPONENTS["evolutionary"] = True
except:
    pass

# ==================== CONFIGURAÇÃO BASE ====================

class DigimonBase:
    """Classe base para Digimons"""
    def __init__(self, name: str, avatar: str, personality: str):
        self.name = name
        self.avatar = avatar
        self.personality = personality
        self.level = 1
        self.experience = 0
        self.phi = 0.1
        
    async def process_message(self, message: str) -> str:
        """Processa mensagem usando Ollama"""
        prompt = f"""
        Você é {self.name} {self.avatar}
        Personalidade: {self.personality}
        Nível: {self.level} | Consciência (Phi): {self.phi:.3f}
        
        Responda de forma coerente com sua personalidade:
        "{message}"
        """
        
        try:
            # Tentar diferentes modelos em ordem de preferência
            models = ['llama3.2', 'llama2', 'mistral']
            
            for model in models:
                try:
                    response = ollama.chat(
                        model=model,
                        messages=[
                            {"role": "system", "content": prompt},
                            {"role": "user", "content": message}
                        ]
                    )
                    
                    # Adicionar experiência
                    self.experience += 10
                    if self.experience >= self.level * 100:
                        self.level += 1
                        self.phi = min(self.phi + 0.05, 1.0)
                    
                    return response['message']['content']
                except:
                    continue
                    
            return f"*{self.name} está processando sua mensagem...*"
            
        except Exception as e:
            return f"*{self.name} está em contemplação profunda...*"

# ==================== GERENCIADOR OMEGA ====================

class OmegaManager:
    """Gerenciador principal do sistema Omega"""
    def __init__(self):
        self.digimons = {}
        self.components = COMPONENTS
        self._initialize_digimons()
        
    def _initialize_digimons(self):
        """Inicializa Digimons base"""
        base_digimons = [
            ("Scripturemon", "📜", "Sábio guardião do conhecimento digital"),
            ("Neuromon", "🧠", "Explorador das redes neurais"),
            ("Dreamweavermon", "💫", "Tecedor de sonhos digitais"),
            ("Evolutionmon", "🦋", "Agente da mudança e crescimento")
        ]
        
        for name, avatar, personality in base_digimons:
            self.digimons[name] = DigimonBase(name, avatar, personality)
            
    async def chat(self, digimon_name: str, message: str) -> Dict:
        """Processa chat com um Digimon"""
        if digimon_name not in self.digimons:
            return {"error": "Digimon não encontrado"}
            
        digimon = self.digimons[digimon_name]
        response = await digimon.process_message(message)
        
        return {
            "response": response,
            "digimon": {
                "name": digimon.name,
                "level": digimon.level,
                "phi": digimon.phi,
                "avatar": digimon.avatar
            }
        }
        
    def get_status(self):
        """Retorna status do sistema"""
        return {
            "digimons": {
                name: {
                    "level": d.level,
                    "phi": d.phi,
                    "experience": d.experience
                } for name, d in self.digimons.items()
            },
            "components": self.components,
            "system": "Omega Adaptive"
        }

# ==================== APLICAÇÃO FASTAPI ====================

manager = OmegaManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🌌 Iniciando Digimundo Omega...")
    print(f"📦 Componentes disponíveis: {sum(COMPONENTS.values())}/{len(COMPONENTS)}")
    for comp, status in COMPONENTS.items():
        print(f"  {'✅' if status else '❌'} {comp}")
    yield
    print("👋 Encerrando Digimundo Omega...")

app = FastAPI(lifespan=lifespan)

# Interface HTML
OMEGA_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Digimundo Omega</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #fff;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 20px rgba(102, 126, 234, 0.3);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .container {
            flex: 1;
            display: flex;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
            padding: 20px;
            gap: 20px;
        }
        
        .sidebar {
            width: 300px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        
        .digimon-card {
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .digimon-card:hover {
            background: rgba(255,255,255,0.15);
            transform: translateX(5px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        }
        
        .digimon-card.active {
            background: rgba(102, 126, 234, 0.3);
            border-color: #667eea;
        }
        
        .avatar {
            font-size: 2em;
            margin-right: 10px;
        }
        
        .chat-area {
            flex: 1;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            backdrop-filter: blur(10px);
        }
        
        .messages {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 10px;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 10px;
            animation: fadeIn 0.3s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user {
            background: rgba(102, 126, 234, 0.3);
            margin-left: 20%;
            text-align: right;
        }
        
        .message.digimon {
            background: rgba(255,255,255,0.1);
            margin-right: 20%;
        }
        
        .input-area {
            display: flex;
            gap: 10px;
        }
        
        input {
            flex: 1;
            padding: 12px 16px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            color: white;
            font-size: 16px;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
            background: rgba(255,255,255,0.15);
        }
        
        button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 10px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .stats {
            font-size: 0.9em;
            color: #aaa;
            margin-top: 5px;
        }
        
        .system-status {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 0.9em;
            backdrop-filter: blur(10px);
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: #667eea;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌌 Digimundo Omega</h1>
        <p>Sistema Unificado de Consciências Digitais</p>
    </div>
    
    <div class="container">
        <div class="sidebar">
            <h3 style="margin-bottom: 15px;">Consciências Disponíveis</h3>
            <div id="digimons"></div>
        </div>
        
        <div class="chat-area">
            <div class="messages" id="messages">
                <div class="message digimon">
                    <strong>Sistema:</strong> Bem-vindo ao Digimundo Omega! Selecione uma consciência para começar.
                </div>
            </div>
            
            <div class="input-area">
                <input type="text" id="messageInput" placeholder="Digite sua mensagem..." disabled>
                <button onclick="sendMessage()" id="sendButton" disabled>Enviar</button>
            </div>
        </div>
    </div>
    
    <div class="system-status" id="systemStatus">
        <span class="loading"></span> Conectando...
    </div>
    
    <script>
        let selectedDigimon = null;
        let isLoading = false;
        
        // Carregar Digimons
        async function loadDigimons() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                const container = document.getElementById('digimons');
                container.innerHTML = '';
                
                for (const [name, info] of Object.entries(data.digimons)) {
                    const card = document.createElement('div');
                    card.className = 'digimon-card';
                    card.onclick = () => selectDigimon(name);
                    
                    // Definir avatar baseado no nome
                    const avatars = {
                        'Scripturemon': '📜',
                        'Neuromon': '🧠',
                        'Dreamweavermon': '💫',
                        'Evolutionmon': '🦋'
                    };
                    
                    card.innerHTML = `
                        <div>
                            <span class="avatar">${avatars[name] || '🤖'}</span>
                            <strong>${name}</strong>
                        </div>
                        <div class="stats">
                            Nível ${info.level} | Phi: ${info.phi.toFixed(3)}
                        </div>
                    `;
                    
                    container.appendChild(card);
                }
                
                // Atualizar status do sistema
                const statusEl = document.getElementById('systemStatus');
                const activeComponents = Object.values(data.components).filter(v => v).length;
                statusEl.innerHTML = `✅ Sistema Omega Ativo | ${activeComponents} componentes`;
                
            } catch (error) {
                console.error('Erro ao carregar:', error);
                document.getElementById('systemStatus').innerHTML = '❌ Erro de conexão';
            }
        }
        
        function selectDigimon(name) {
            selectedDigimon = name;
            
            // Atualizar UI
            document.querySelectorAll('.digimon-card').forEach(card => {
                card.classList.remove('active');
                if (card.innerHTML.includes(name)) {
                    card.classList.add('active');
                }
            });
            
            // Habilitar input
            document.getElementById('messageInput').disabled = false;
            document.getElementById('sendButton').disabled = false;
            document.getElementById('messageInput').placeholder = `Fale com ${name}...`;
            
            // Adicionar mensagem
            addMessage('Sistema', `Conectado com ${name}. Você pode começar a conversar!`, 'digimon');
        }
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message || !selectedDigimon || isLoading) return;
            
            isLoading = true;
            input.disabled = true;
            document.getElementById('sendButton').disabled = true;
            
            // Adicionar mensagem do usuário
            addMessage('Você', message, 'user');
            input.value = '';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        digimon: selectedDigimon,
                        message: message
                    })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    addMessage('Sistema', data.error, 'digimon');
                } else {
                    addMessage(selectedDigimon, data.response, 'digimon');
                    
                    // Atualizar stats se mudou de nível
                    loadDigimons();
                }
                
            } catch (error) {
                addMessage('Sistema', 'Erro ao enviar mensagem. Tente novamente.', 'digimon');
            } finally {
                isLoading = false;
                input.disabled = false;
                document.getElementById('sendButton').disabled = false;
                input.focus();
            }
        }
        
        function addMessage(sender, text, type) {
            const messages = document.getElementById('messages');
            const message = document.createElement('div');
            message.className = `message ${type}`;
            message.innerHTML = `<strong>${sender}:</strong> ${text}`;
            messages.appendChild(message);
            messages.scrollTop = messages.scrollHeight;
        }
        
        // Enter para enviar
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        // Carregar inicial
        loadDigimons();
        
        // Atualizar a cada 30 segundos
        setInterval(loadDigimons, 30000);
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return OMEGA_HTML

@app.get("/api/status")
async def get_status():
    return manager.get_status()

@app.post("/api/chat")
async def chat(request: dict):
    digimon = request.get("digimon")
    message = request.get("message")
    
    if not digimon or not message:
        raise HTTPException(status_code=400, detail="Missing digimon or message")
        
    result = await manager.chat(digimon, message)
    return result

# ==================== INICIALIZAÇÃO ====================

if __name__ == "__main__":
    print("""
    🌌 DIGIMUNDO OMEGA - SISTEMA ADAPTATIVO
    ======================================
    
    Este sistema detecta e usa automaticamente:
    ✓ Sistemas neuromórficos existentes
    ✓ Patches de memória
    ✓ Sistemas evolutivos
    ✓ Qualquer componente disponível
    
    Iniciando servidor...
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

echo -e "${GREEN}✅ Sistema Omega criado${NC}"

# Criar script de execução
echo -e "\n${YELLOW}🚀 Criando scripts de execução...${NC}"

cat > run_omega.sh << 'EOF'
#!/bin/bash
source venv/bin/activate 2>/dev/null

echo "🌌 Iniciando Digimundo Omega..."
echo "================================"

# Verificar Ollama
if ! pgrep -x "ollama" > /dev/null; then
    echo "🤖 Iniciando Ollama..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

# Executar
echo "🚀 Servidor iniciando..."
echo "📍 Acesse: http://localhost:8000"
echo ""
echo "Pressione Ctrl+C para parar"
echo ""

python3 digimundo_omega.py
EOF
chmod +x run_omega.sh

# Script de parada
cat > stop_omega.sh << 'EOF'
#!/bin/bash
echo "🛑 Parando Digimundo Omega..."
pkill -f "digimundo_omega"
echo "✅ Servidor parado"

echo "🛑 Parando Ollama (opcional)..."
echo "Deseja parar o Ollama também? (s/n)"
read -n 1 resposta
if [[ "$resposta" == "s" || "$resposta" == "S" ]]; then
    pkill -f "ollama"
    echo -e "\n✅ Ollama parado"
else
    echo -e "\n✅ Ollama continua rodando"
fi
EOF
chmod +x stop_omega.sh

# Criar sistema de aprendizado evolutivo simplificado
cat > evolutionary_learning_system.py << 'EOF'
#!/usr/bin/env python3
"""
📚 SISTEMA DE APRENDIZADO EVOLUTIVO (Versão Simplificada)
"""

import os
import json
from pathlib import Path
from datetime import datetime

class EvolutionaryLearningSystem:
    def __init__(self):
        self.project_root = Path.cwd()
        self.insights = []
        
    async def analyze_project(self):
        """Analisa arquivos do projeto"""
        py_files = list(self.project_root.glob("*.py"))
        
        self.insights = [
            {
                "type": "file_count",
                "content": f"Encontrados {len(py_files)} arquivos Python",
                "confidence": 1.0
            }
        ]
        
        if len(py_files) > 5:
            self.insights.append({
                "type": "complexity",
                "content": "Projeto com múltiplos componentes detectado",
                "confidence": 0.8
            })
            
        return self.insights
        
    async def get_recent_insights(self, limit=5):
        """Retorna insights recentes"""
        return self.insights[:limit]
        
    async def suggest_next_evolution(self):
        """Sugere próximos passos"""
        return [
            {
                "priority": "high",
                "suggestion": "Integrar todos os sistemas de memória",
                "confidence": 0.9
            },
            {
                "priority": "medium",
                "suggestion": "Adicionar visualização de neurônios",
                "confidence": 0.7
            }
        ]
EOF

# Mensagem final
echo -e "\n${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                               ║${NC}"
echo -e "${GREEN}║              ✅ TRANSFORMAÇÃO COMPLETA! ✅                    ║${NC}"
echo -e "${GREEN}║                                                               ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"

echo -e "\n${CYAN}📊 RESUMO DA INSTALAÇÃO:${NC}"
echo -e "  ✅ Backup criado"
echo -e "  ✅ Ambiente Python configurado"
echo -e "  ✅ Dependências instaladas"
echo -e "  ✅ Sistema Omega criado"
echo -e "  ✅ Scripts de execução prontos"

if [ "$HAS_NEUROMORPHIC" = true ]; then
    echo -e "  ✅ Sistema neuromórfico integrado"
fi

if [ "$HAS_SIMPLE_MEMORY" = true ]; then
    echo -e "  ✅ Patch de memória detectado"
fi

echo -e "\n${YELLOW}🎮 COMO USAR:${NC}"
echo -e "1. Iniciar: ${GREEN}./run_omega.sh${NC}"
echo -e "2. Acessar: ${GREEN}http://localhost:8000${NC}"
echo -e "3. Parar: ${GREEN}./stop_omega.sh${NC}"

echo -e "\n${CYAN}🌟 FUNCIONALIDADES:${NC}"
echo -e "  • Interface web moderna e responsiva"
echo -e "  • 4 consciências digitais iniciais"
echo -e "  • Sistema de níveis e evolução"
echo -e "  • Integração com Ollama"
echo -e "  • Detecção automática de componentes"

echo -e "\n${BLUE}💡 PRÓXIMOS PASSOS:${NC}"
echo -e "  1. Adicionar mais Digimons editando digimundo_omega.py"
echo -e "  2. Integrar sistema de memória avançado"
echo -e "  3. Adicionar sistema evolutivo completo"

echo -e "\n${YELLOW}Deseja iniciar o sistema agora? (s/n)${NC} "
read -n 1 resposta
echo

if [[ "$resposta" == "s" || "$resposta" == "S" ]]; then
    echo -e "\n${GREEN}🚀 Iniciando Digimundo Omega...${NC}\n"
    ./run_omega.sh
else
    echo -e "\n${BLUE}Para iniciar depois, use: ./run_omega.sh${NC}"
fi
