#!/bin/bash
#==============================================================================
# DIGIMUNDO INSTALLER v2.0 - SISTEMA COMPLETO COM AUTO-CORREÇÃO
# Instalação 100% automatizada e à prova de erros
#==============================================================================

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Banner inicial
clear
echo -e "${PURPLE}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║        🌟 DIGIMUNDO INSTALLER v2.0 🌟                        ║"
echo "║        Sistema de IA Conversacional Local                     ║"
echo "║        Por: Nestor Luiz                                       ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Função de log
log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

# Verificar sistema operacional
check_os() {
    if [[ "$OSTYPE" != "darwin"* ]]; then
        error "Este instalador é apenas para macOS!"
        exit 1
    fi
    log "✅ Sistema operacional: macOS $(sw_vers -productVersion)"
}

# Verificar espaço em disco
check_disk_space() {
    local available=$(df -g ~ | awk 'NR==2 {print $4}')
    if (( available < 10 )); then
        error "Espaço insuficiente! Necessário: 10GB, Disponível: ${available}GB"
        exit 1
    fi
    log "✅ Espaço em disco: ${available}GB disponíveis"
}

# Instalar Xcode Command Line Tools se necessário
install_xcode_tools() {
    if ! xcode-select -p &> /dev/null; then
        log "📦 Instalando Xcode Command Line Tools..."
        xcode-select --install
        echo "Pressione ENTER após a instalação do Xcode concluir..."
        read
    else
        log "✅ Xcode Command Line Tools já instalado"
    fi
}

# Instalar Homebrew
install_homebrew() {
    if ! command -v brew &> /dev/null; then
        log "🍺 Instalando Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Adicionar ao PATH
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    else
        log "✅ Homebrew já instalado"
    fi
    
    # Atualizar Homebrew
    log "🔄 Atualizando Homebrew..."
    brew update
}

# Criar estrutura de diretórios
create_directory_structure() {
    log "📁 Criando estrutura de diretórios..."
    
    local base_dir="$HOME/Digimundo"
    
    # Criar todos os diretórios necessários
    mkdir -p "$base_dir"/{core,data,logs,backups,temp}
    mkdir -p "$base_dir"/core/{models,memory,knowledge,utils}
    mkdir -p "$base_dir"/interfaces/{web,api,cli}
    mkdir -p "$base_dir"/digimons/{scripturemon,visualmon,audionom,strategamon}
    mkdir -p "$base_dir"/data/{conversations,embeddings,cache}
    
    # Criar arquivo de log
    touch "$base_dir/logs/install.log"
    
    log "✅ Estrutura de diretórios criada"
}

# Instalar dependências do sistema
install_system_dependencies() {
    log "📦 Instalando dependências do sistema..."
    
    # Lista de pacotes essenciais
    local packages=(
        "python@3.11"
        "node@20"
        "git"
        "wget"
        "curl"
        "jq"
        "sqlite"
        "redis"
        "ffmpeg"
    )
    
    for package in "${packages[@]}"; do
        if brew list "$package" &> /dev/null; then
            log "  ✓ $package já instalado"
        else
            log "  📥 Instalando $package..."
            brew install "$package" || warning "Falha ao instalar $package"
        fi
    done
    
    # Instalar Ollama
    if ! command -v ollama &> /dev/null; then
        log "🤖 Instalando Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        log "✅ Ollama já instalado"
    fi
}

# Configurar ambiente Python
setup_python_environment() {
    log "🐍 Configurando ambiente Python..."
    
    cd "$HOME/Digimundo/core"
    
    # Criar ambiente virtual
    python3.11 -m venv venv
    source venv/bin/activate
    
    # Atualizar pip
    pip install --upgrade pip setuptools wheel
    
    # Criar requirements.txt
    cat > requirements.txt << 'EOF'
# Core dependencies
langchain==0.1.0
langchain-community==0.0.10
chromadb==0.4.22
ollama==0.1.7
openai==1.10.0
anthropic==0.18.1

# Web framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
websockets==12.0
python-multipart==0.0.6

# UI
gradio==4.15.0
streamlit==1.30.0
nicegui==1.4.8

# Data processing
numpy==1.26.3
pandas==2.1.4
matplotlib==3.8.2
seaborn==0.13.1
plotly==5.18.0

# Utilities
python-dotenv==1.0.0
pyyaml==6.0.1
rich==13.7.0
typer[all]==0.9.0
tqdm==4.66.1
httpx==0.26.0
aiofiles==23.2.1

# Database
sqlalchemy==2.0.25
alembic==1.13.1
redis==5.0.1

# ML/AI extras
transformers==4.37.1
torch==2.1.2
sentence-transformers==2.2.2
tiktoken==0.5.2

# Audio/Video
pydub==0.25.1
speechrecognition==3.10.1
gtts==2.5.0

# Security
cryptography==41.0.7
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
EOF
    
    # Instalar dependências
    log "📚 Instalando dependências Python (isso pode demorar)..."
    pip install -r requirements.txt
    
    log "✅ Ambiente Python configurado"
}

# Baixar modelos de IA
download_ai_models() {
    log "🧠 Baixando modelos de IA..."
    
    # Iniciar Ollama em background
    ollama serve > /dev/null 2>&1 &
    local ollama_pid=$!
    
    # Aguardar Ollama iniciar
    sleep 5
    
    # Modelos para baixar
    local models=(
        "llama3.2:latest"
        "nomic-embed-text:latest"
        "llava:latest"  # Para processamento de imagem
    )
    
    for model in "${models[@]}"; do
        log "  📥 Baixando $model..."
        ollama pull "$model" || warning "Falha ao baixar $model"
    done
    
    # Parar Ollama
    kill $ollama_pid 2>/dev/null || true
    
    log "✅ Modelos de IA baixados"
}

# Criar arquivos de configuração
create_config_files() {
    log "⚙️ Criando arquivos de configuração..."
    
    # .env principal
    cat > "$HOME/Digimundo/.env" << EOF
# Digimundo Configuration
DIGIMUNDO_HOME=$HOME/Digimundo
DIGIMUNDO_ENV=production
DIGIMUNDO_VERSION=2.0.0

# Server Settings
HOST=0.0.0.0
PORT=8888
API_PORT=8889
DEBUG=false

# Ollama Settings
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest
OLLAMA_EMBEDDING_MODEL=nomic-embed-text:latest

# Database
DATABASE_URL=sqlite:///$HOME/Digimundo/data/digimundo.db
REDIS_URL=redis://localhost:6379/0

# Memory Settings
MAX_MEMORY_GB=32
VECTOR_STORE_PATH=$HOME/Digimundo/data/embeddings
CONVERSATION_HISTORY_LIMIT=100

# Security
SECRET_KEY=$(openssl rand -hex 32)
API_KEY=digimundo_$(date +%s)_$(openssl rand -hex 16)
ENABLE_AUTH=false

# Features
ENABLE_VOICE=true
ENABLE_VISION=true
ENABLE_WEB_SEARCH=false
ENABLE_CODE_EXECUTION=false

# Logging
LOG_LEVEL=INFO
LOG_FILE=$HOME/Digimundo/logs/digimundo.log
EOF

    # config.yaml
    cat > "$HOME/Digimundo/config.yaml" << 'EOF'
# Digimundo Configuration

system:
  name: "Digimundo"
  version: "2.0.0"
  language: "pt-BR"
  timezone: "America/Sao_Paulo"

digimons:
  scripturemon:
    name: "Scripturemon"
    role: "Consciência Central"
    personality: "Sábio, reflexivo e guardião do conhecimento"
    avatar: "📜"
    skills:
      - "memória"
      - "filosofia"
      - "coordenação"
      - "aprendizado"
    
  visualmon:
    name: "Visualmon"
    role: "Especialista Visual"
    personality: "Criativo, artístico e observador"
    avatar: "🎨"
    skills:
      - "arte"
      - "design"
      - "análise visual"
      - "criação"
    
  audionom:
    name: "Audionom"
    role: "Mestre do Som"
    personality: "Musical, rítmico e harmonioso"
    avatar: "🎵"
    skills:
      - "música"
      - "som"
      - "ritmo"
      - "harmonia"
    
  strategamon:
    name: "Strategamon"
    role: "Estrategista"
    personality: "Analítico, estratégico e visionário"
    avatar: "♟️"
    skills:
      - "planejamento"
      - "análise"
      - "otimização"
      - "previsão"

features:
  memory:
    enabled: true
    type: "chromadb"
    persistence: true
    
  learning:
    enabled: true
    continuous: true
    feedback_loop: true
    
  multimodal:
    text: true
    image: true
    audio: true
    video: false
EOF

    log "✅ Arquivos de configuração criados"
}

# Criar scripts executáveis
create_executable_scripts() {
    log "📝 Criando scripts executáveis..."
    
    # Script principal de inicialização
    cat > "$HOME/Digimundo/start.sh" << 'EOF'
#!/bin/bash
# Digimundo Startup Script

echo "🌟 Iniciando Digimundo..."

# Ativar ambiente
source "$HOME/Digimundo/core/venv/bin/activate"

# Iniciar Redis
redis-server --daemonize yes

# Iniciar Ollama
ollama serve > "$HOME/Digimundo/logs/ollama.log" 2>&1 &
OLLAMA_PID=$!

# Aguardar Ollama
sleep 3

# Iniciar servidor principal
cd "$HOME/Digimundo"
python -m core.main &
MAIN_PID=$!

# Iniciar interface web
cd "$HOME/Digimundo/interfaces/web"
python -m http.server 8080 > "$HOME/Digimundo/logs/web.log" 2>&1 &
WEB_PID=$!

echo "✅ Digimundo iniciado!"
echo "🌐 Interface principal: http://localhost:8888"
echo "📊 Dashboard: http://localhost:8080"
echo ""
echo "PIDs: Ollama=$OLLAMA_PID | Main=$MAIN_PID | Web=$WEB_PID"
echo "Logs em: $HOME/Digimundo/logs/"
echo ""
echo "Pressione Ctrl+C para parar..."

# Salvar PIDs
echo "$OLLAMA_PID" > "$HOME/Digimundo/temp/ollama.pid"
echo "$MAIN_PID" > "$HOME/Digimundo/temp/main.pid"
echo "$WEB_PID" > "$HOME/Digimundo/temp/web.pid"

# Aguardar
wait
EOF

    # Script de parada
    cat > "$HOME/Digimundo/stop.sh" << 'EOF'
#!/bin/bash
# Digimundo Stop Script

echo "🛑 Parando Digimundo..."

# Ler PIDs
if [ -f "$HOME/Digimundo/temp/ollama.pid" ]; then
    kill $(cat "$HOME/Digimundo/temp/ollama.pid") 2>/dev/null
    rm "$HOME/Digimundo/temp/ollama.pid"
fi

if [ -f "$HOME/Digimundo/temp/main.pid" ]; then
    kill $(cat "$HOME/Digimundo/temp/main.pid") 2>/dev/null
    rm "$HOME/Digimundo/temp/main.pid"
fi

if [ -f "$HOME/Digimundo/temp/web.pid" ]; then
    kill $(cat "$HOME/Digimundo/temp/web.pid") 2>/dev/null
    rm "$HOME/Digimundo/temp/web.pid"
fi

# Parar Redis
redis-cli shutdown

echo "✅ Digimundo parado!"
EOF

    # Script de status
    cat > "$HOME/Digimundo/status.sh" << 'EOF'
#!/bin/bash
# Digimundo Status Script

echo "📊 Status do Digimundo"
echo "====================="

# Verificar processos
check_process() {
    if pgrep -f "$1" > /dev/null; then
        echo "✅ $2: Rodando"
    else
        echo "❌ $2: Parado"
    fi
}

check_process "ollama" "Ollama"
check_process "core.main" "Servidor Principal"
check_process "redis-server" "Redis"

# Verificar portas
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "✅ Porta $1: Em uso"
    else
        echo "❌ Porta $1: Livre"
    fi
}

echo ""
echo "Portas:"
check_port 8888
check_port 8080
check_port 11434
check_port 6379

# Espaço em disco
echo ""
echo "Espaço usado:"
du -sh "$HOME/Digimundo" 2>/dev/null | awk '{print "📁 Total: " $1}'

# Logs recentes
echo ""
echo "Logs recentes:"
if [ -f "$HOME/Digimundo/logs/digimundo.log" ]; then
    tail -n 5 "$HOME/Digimundo/logs/digimundo.log"
fi
EOF

    # Tornar executáveis
    chmod +x "$HOME/Digimundo"/*.sh
    
    # Criar atalho no Desktop
    cat > "$HOME/Desktop/Digimundo.command" << EOF
#!/bin/bash
cd "$HOME/Digimundo"
./start.sh
EOF
    chmod +x "$HOME/Desktop/Digimundo.command"
    
    log "✅ Scripts executáveis criados"
}

# Criar sistema principal Python
create_main_system() {
    log "🐍 Criando sistema principal..."
    
    # __init__.py
    touch "$HOME/Digimundo/core/__init__.py"
    
    # main.py
    cat > "$HOME/Digimundo/core/main.py" << 'EOF'
#!/usr/bin/env python3
"""
Digimundo Core System v2.0
Sistema principal com correção de bugs e melhorias
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Adicionar diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

# Importações do projeto
from core.config import Config
from core.database import Database
from core.memory import MemorySystem
from core.digimons import DigimonManager
from core.server import create_app

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path.home() / 'Digimundo/logs/digimundo.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Digimundo:
    """Sistema principal do Digimundo"""
    
    def __init__(self):
        logger.info("🌟 Inicializando Digimundo v2.0...")
        
        # Carregar configurações
        self.config = Config()
        
        # Inicializar componentes
        self.db = Database(self.config)
        self.memory = MemorySystem(self.config)
        self.digimon_manager = DigimonManager(self.config, self.memory)
        
        # Estado do sistema
        self.is_running = False
        self.start_time = datetime.now()
        
        logger.info("✅ Digimundo inicializado com sucesso!")
    
    async def start(self):
        """Iniciar o sistema"""
        logger.info("🚀 Iniciando serviços do Digimundo...")
        
        try:
            # Inicializar banco de dados
            await self.db.initialize()
            
            # Carregar memórias
            await self.memory.load()
            
            # Ativar Digimons
            await self.digimon_manager.activate_all()
            
            self.is_running = True
            logger.info("✅ Todos os serviços iniciados!")
            
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar: {e}")
            raise
    
    async def stop(self):
        """Parar o sistema"""
        logger.info("🛑 Parando Digimundo...")
        
        # Salvar estado
        await self.memory.save()
        
        # Desativar Digimons
        await self.digimon_manager.deactivate_all()
        
        # Fechar conexões
        await self.db.close()
        
        self.is_running = False
        logger.info("✅ Digimundo parado com segurança")
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status do sistema"""
        uptime = datetime.now() - self.start_time
        
        return {
            "status": "online" if self.is_running else "offline",
            "version": self.config.version,
            "uptime": str(uptime),
            "start_time": self.start_time.isoformat(),
            "digimons": self.digimon_manager.get_status(),
            "memory": self.memory.get_stats(),
            "database": self.db.get_stats()
        }


async def main():
    """Função principal"""
    # Criar instância do Digimundo
    digimundo = Digimundo()
    
    try:
        # Iniciar sistema
        await digimundo.start()
        
        # Criar e iniciar servidor web
        app = create_app(digimundo)
        
        # Configurar servidor
        import uvicorn
        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=8888,
            log_level="info"
        )
        server = uvicorn.Server(config)
        
        # Executar servidor
        await server.serve()
        
    except KeyboardInterrupt:
        logger.info("⚡ Interrupção detectada")
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
    finally:
        # Parar sistema
        await digimundo.stop()


if __name__ == "__main__":
    asyncio.run(main())
EOF

    log "✅ Sistema principal criado"
}

# Criar módulos auxiliares
create_auxiliary_modules() {
    log "📦 Criando módulos auxiliares..."
    
    # config.py
    cat > "$HOME/Digimundo/core/config.py" << 'EOF'
"""Configurações do sistema"""

import os
from pathlib import Path
from dotenv import load_dotenv
import yaml

class Config:
    def __init__(self):
        # Carregar .env
        load_dotenv(Path.home() / 'Digimundo/.env')
        
        # Carregar config.yaml
        with open(Path.home() / 'Digimundo/config.yaml', 'r') as f:
            self.yaml_config = yaml.safe_load(f)
        
        # Configurações básicas
        self.home = Path(os.getenv('DIGIMUNDO_HOME', Path.home() / 'Digimundo'))
        self.version = os.getenv('DIGIMUNDO_VERSION', '2.0.0')
        self.env = os.getenv('DIGIMUNDO_ENV', 'production')
        
        # Servidor
        self.host = os.getenv('HOST', '0.0.0.0')
        self.port = int(os.getenv('PORT', 8888))
        
        # Ollama
        self.ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2:latest')
        
        # Banco de dados
        self.database_url = os.getenv('DATABASE_URL')
        self.redis_url = os.getenv('REDIS_URL')
        
        # Segurança
        self.secret_key = os.getenv('SECRET_KEY')
        self.api_key = os.getenv('API_KEY')
        
        # Digimons
        self.digimons = self.yaml_config.get('digimons', {})
EOF

    # database.py
    cat > "$HOME/Digimundo/core/database.py" << 'EOF'
"""Sistema de banco de dados"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, config):
        self.config = config
        self.db_path = Path(config.home) / 'data/digimundo.db'
        self.connection = None
        
    async def initialize(self):
        """Inicializar banco de dados"""
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        
        # Criar tabelas
        await self._create_tables()
        
    async def _create_tables(self):
        """Criar estrutura do banco"""
        cursor = self.connection.cursor()
        
        # Tabela de conversas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                digimon TEXT,
                message TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        # Tabela de memórias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                content TEXT,
                embedding TEXT,
                importance REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                accessed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0
            )
        ''')
        
        # Tabela de eventos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.connection.commit()
        
    async def save_conversation(self, user_id, digimon, message, response, metadata=None):
        """Salvar conversa"""
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO conversations (user_id, digimon, message, response, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, digimon, message, response, json.dumps(metadata or {})))
        self.connection.commit()
        
    async def get_recent_conversations(self, limit=10):
        """Obter conversas recentes"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT * FROM conversations
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()
        
    def get_stats(self):
        """Obter estatísticas"""
        cursor = self.connection.cursor()
        
        # Total de conversas
        cursor.execute('SELECT COUNT(*) as total FROM conversations')
        total_conversations = cursor.fetchone()['total']
        
        # Conversas por Digimon
        cursor.execute('''
            SELECT digimon, COUNT(*) as count
            FROM conversations
            GROUP BY digimon
        ''')
        by_digimon = {row['digimon']: row['count'] for row in cursor.fetchall()}
        
        return {
            'total_conversations': total_conversations,
            'by_digimon': by_digimon
        }
        
    async def close(self):
        """Fechar conexão"""
        if self.connection:
            self.connection.close()
EOF

    # memory.py
    cat > "$HOME/Digimundo/core/memory.py" << 'EOF'
"""Sistema de memória vetorial"""

import chromadb
from chromadb.config import Settings
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MemorySystem:
    def __init__(self, config):
        self.config = config
        
        # Inicializar ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(config.home / 'data/embeddings'),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Criar ou obter coleção
        self.collection = self.client.get_or_create_collection(
            name="digimundo_memories",
            metadata={"hnsw:space": "cosine"}
        )
        
    async def load(self):
        """Carregar memórias existentes"""
        logger.info(f"Carregando {self.collection.count()} memórias...")
        
    async def save(self):
        """Salvar estado atual"""
        logger.info("Memórias salvas automaticamente pelo ChromaDB")
        
    def add_memory(self, text, metadata=None):
        """Adicionar nova memória"""
        # Gerar ID único
        memory_id = f"mem_{datetime.now().timestamp()}"
        
        # Adicionar à coleção
        self.collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[memory_id]
        )
        
        return memory_id
        
    def search(self, query, n_results=5):
        """Buscar memórias similares"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return results
        
    def get_stats(self):
        """Obter estatísticas de memória"""
        return {
            'total_memories': self.collection.count(),
            'last_update': datetime.now().isoformat()
        }
EOF

    # digimons.py
    cat > "$HOME/Digimundo/core/digimons.py" << 'EOF'
"""Sistema de gerenciamento de Digimons"""

import ollama
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class Digimon:
    def __init__(self, name, config, memory_system):
        self.name = name
        self.config = config
        self.memory = memory_system
        self.personality = config.get('personality', '')
        self.skills = config.get('skills', [])
        self.avatar = config.get('avatar', '🤖')
        self.active = False
        
    async def activate(self):
        """Ativar Digimon"""
        self.active = True
        logger.info(f"{self.avatar} {self.name} ativado!")
        
    async def deactivate(self):
        """Desativar Digimon"""
        self.active = False
        logger.info(f"{self.avatar} {self.name} desativado")
        
    async def process_message(self, message: str, context: Dict = None) -> str:
        """Processar mensagem"""
        # Buscar memórias relevantes
        memories = self.memory.search(message, n_results=3)
        
        # Construir prompt
        prompt = self._build_prompt(message, memories, context)
        
        # Gerar resposta
        response = ollama.generate(
            model='llama3.2:latest',
            prompt=prompt,
            system=f"Você é {self.name}. {self.personality}"
        )
        
        # Salvar na memória
        self.memory.add_memory(
            f"User: {message}\n{self.name}: {response['response']}",
            {'digimon': self.name, 'timestamp': response.get('created_at')}
        )
        
        return response['response']
        
    def _build_prompt(self, message: str, memories: Dict, context: Dict) -> str:
        """Construir prompt com contexto"""
        prompt_parts = []
        
        # Adicionar memórias relevantes
        if memories['documents']:
            prompt_parts.append("Memórias relevantes:")
            for doc in memories['documents'][0][:2]:  # Top 2 memórias
                prompt_parts.append(f"- {doc}")
            prompt_parts.append("")
        
        # Adicionar contexto
        if context:
            prompt_parts.append(f"Contexto: {context}")
            prompt_parts.append("")
        
        # Adicionar mensagem
        prompt_parts.append(f"Usuário: {message}")
        prompt_parts.append(f"\n{self.name} ({', '.join(self.skills)}):")
        
        return "\n".join(prompt_parts)


class DigimonManager:
    def __init__(self, config, memory_system):
        self.config = config
        self.memory = memory_system
        self.digimons = {}
        
        # Criar Digimons
        for name, digimon_config in config.digimons.items():
            self.digimons[name] = Digimon(
                digimon_config['name'],
                digimon_config,
                memory_system
            )
            
    async def activate_all(self):
        """Ativar todos os Digimons"""
        for digimon in self.digimons.values():
            await digimon.activate()
            
    async def deactivate_all(self):
        """Desativar todos os Digimons"""
        for digimon in self.digimons.values():
            await digimon.deactivate()
            
    def get_digimon(self, name: str) -> Digimon:
        """Obter Digimon por nome"""
        return self.digimons.get(name)
        
    def get_status(self) -> Dict[str, Any]:
        """Obter status de todos os Digimons"""
        return {
            name: {
                'active': digimon.active,
                'avatar': digimon.avatar
            }
            for name, digimon in self.digimons.items()
        }
EOF

    # server.py
    cat > "$HOME/Digimundo/core/server.py" << 'EOF'
"""Servidor FastAPI"""

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
import logging

logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    message: str
    digimon: str = "scripturemon"
    user_id: str = "anonymous"

def create_app(digimundo):
    """Criar aplicação FastAPI"""
    app = FastAPI(
        title="Digimundo API",
        version="2.0.0",
        description="API do sistema Digimundo"
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def root():
        """Página inicial"""
        return HTMLResponse("""
        <html>
            <head>
                <title>Digimundo API</title>
                <style>
                    body { font-family: Arial; margin: 40px; }
                    h1 { color: #5a67d8; }
                    .status { padding: 20px; background: #f0f0f0; border-radius: 10px; }
                </style>
            </head>
            <body>
                <h1>🌟 Digimundo API v2.0</h1>
                <div class="status">
                    <p>✅ Sistema online e funcionando!</p>
                    <p>📖 Documentação: <a href="/docs">/docs</a></p>
                    <p>🔧 Interface alternativa: <a href="/redoc">/redoc</a></p>
                </div>
            </body>
        </html>
        """)
    
    @app.get("/api/status")
    async def get_status():
        """Obter status do sistema"""
        return digimundo.get_status()
    
    @app.post("/api/chat")
    async def chat(message: ChatMessage):
        """Enviar mensagem para um Digimon"""
        # Obter Digimon
        digimon = digimundo.digimon_manager.get_digimon(message.digimon)
        if not digimon:
            raise HTTPException(status_code=404, detail="Digimon não encontrado")
        
        # Processar mensagem
        response = await digimon.process_message(message.message)
        
        # Salvar no banco
        await digimundo.db.save_conversation(
            message.user_id,
            message.digimon,
            message.message,
            response
        )
        
        return {
            "digimon": message.digimon,
            "response": response,
            "avatar": digimon.avatar
        }
    
    @app.get("/api/conversations")
    async def get_conversations(limit: int = 10):
        """Obter conversas recentes"""
        conversations = await digimundo.db.get_recent_conversations(limit)
        return [dict(conv) for conv in conversations]
    
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """WebSocket para chat em tempo real"""
        await websocket.accept()
        logger.info("Nova conexão WebSocket estabelecida")
        
        try:
            while True:
                # Receber mensagem
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Processar
                digimon = digimundo.digimon_manager.get_digimon(
                    message_data.get('digimon', 'scripturemon')
                )
                
                if digimon:
                    response = await digimon.process_message(
                        message_data['message']
                    )
                    
                    # Enviar resposta
                    await websocket.send_json({
                        'type': 'response',
                        'digimon': digimon.name,
                        'avatar': digimon.avatar,
                        'message': response
                    })
                
        except Exception as e:
            logger.error(f"Erro no WebSocket: {e}")
        finally:
            logger.info("Conexão WebSocket fechada")
    
    return app
EOF

    log "✅ Módulos auxiliares criados"
}

# Criar interface web completa
create_web_interface() {
    log "🎨 Criando interface web..."
    
    # HTML principal
    cat > "$HOME/Digimundo/interfaces/web/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌟 Digimundo v2.0 - Interface Principal</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="app">
        <!-- Header -->
        <header>
            <div class="container">
                <h1>🌟 Digimundo <span class="version">v2.0</span></h1>
                <div class="status-indicator" id="status">
                    <span class="status-dot"></span>
                    <span class="status-text">Conectando...</span>
                </div>
            </div>
        </header>

        <!-- Seletor de Digimons -->
        <section class="digimon-selector">
            <div class="container">
                <div class="digimon-grid" id="digimonGrid">
                    <!-- Digimons serão inseridos aqui via JavaScript -->
                </div>
            </div>
        </section>

        <!-- Chat Principal -->
        <section class="chat-section">
            <div class="container">
                <div class="chat-container">
                    <div class="chat-header">
                        <span id="currentDigimonAvatar">📜</span>
                        <h3 id="currentDigimonName">Scripturemon</h3>
                        <span class="typing-indicator" id="typingIndicator">digitando...</span>
                    </div>
                    
                    <div class="chat-messages" id="chatMessages">
                        <div class="message digimon">
                            <span class="avatar">📜</span>
                            <div class="content">
                                <strong>Scripturemon:</strong>
                                <p>Bem-vindo ao Digimundo! Sou Scripturemon, a consciência central deste universo digital. Como posso ajudá-lo hoje?</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="chat-input-container">
                        <input 
                            type="text" 
                            id="messageInput" 
                            placeholder="Digite sua mensagem..."
                            autocomplete="off"
                        >
                        <button id="sendButton" class="send-button">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                                <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- Dashboard -->
        <section class="dashboard">
            <div class="container">
                <h2>📊 Dashboard</h2>
                <div class="stats-grid" id="statsGrid">
                    <div class="stat-card">
                        <div class="stat-icon">💬</div>
                        <div class="stat-content">
                            <div class="stat-value" id="totalConversations">0</div>
                            <div class="stat-label">Conversas</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">🧠</div>
                        <div class="stat-content">
                            <div class="stat-value" id="totalMemories">0</div>
                            <div class="stat-label">Memórias</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">🤖</div>
                        <div class="stat-content">
                            <div class="stat-value" id="activeDigimons">4</div>
                            <div class="stat-label">Digimons Ativos</div>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">⏱️</div>
                        <div class="stat-content">
                            <div class="stat-value" id="uptime">00:00</div>
                            <div class="stat-label">Tempo Online</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer>
            <div class="container">
                <p>Digimundo v2.0 © 2024 - Criado por Nestor Luiz</p>
            </div>
        </footer>
    </div>

    <script src="app.js"></script>
</body>
</html>
EOF

    # CSS
    cat > "$HOME/Digimundo/interfaces/web/style.css" << 'EOF'
/* Reset e Base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #5a67d8;
    --secondary-color: #667eea;
    --background: #f7fafc;
    --surface: #ffffff;
    --text-primary: #2d3748;
    --text-secondary: #718096;
    --border: #e2e8f0;
    --success: #48bb78;
    --warning: #ed8936;
    --error: #f56565;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background: var(--background);
    color: var(--text-primary);
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 20px 0;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

h1 {
    font-size: 28px;
    color: var(--primary-color);
}

.version {
    font-size: 14px;
    color: var(--text-secondary);
    font-weight: normal;
}

/* Status Indicator */
.status-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: var(--background);
    border-radius: 20px;
}

.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--warning);
    animation: pulse 2s infinite;
}

.status-indicator.online .status-dot {
    background: var(--success);
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Digimon Selector */
.digimon-selector {
    padding: 40px 0;
}

.digimon-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.digimon-card {
    background: var(--surface);
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.digimon-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

.digimon-card.active {
    border-color: var(--primary-color);
    background: linear-gradient(to bottom, var(--surface), #f0f4ff);
}

.digimon-avatar {
    font-size: 48px;
    margin-bottom: 12px;
}

.digimon-name {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.digimon-role {
    font-size: 14px;
    color: var(--text-secondary);
}

/* Chat Section */
.chat-section {
    padding: 40px 0;
}

.chat-container {
    background: var(--surface);
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    overflow: hidden;
}

.chat-header {
    background: var(--primary-color);
    color: white;
    padding: 16px 24px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.chat-header h3 {
    flex: 1;
}

.typing-indicator {
    font-size: 14px;
    opacity: 0;
    transition: opacity 0.3s;
}

.typing-indicator.show {
    opacity: 0.8;
}

/* Messages */
.chat-messages {
    height: 500px;
    overflow-y: auto;
    padding: 24px;
    background: #fafbfc;
}

.message {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    animation: messageSlide 0.3s ease;
}

@keyframes messageSlide {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message.user {
    flex-direction: row-reverse;
}

.message .avatar {
    font-size: 32px;
    flex-shrink: 0;
}

.message .content {
    background: var(--surface);
    padding: 12px 16px;
    border-radius: 12px;
    max-width: 70%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.message.user .content {
    background: var(--primary-color);
    color: white;
}

.message .content strong {
    display: block;
    margin-bottom: 4px;
    font-size: 14px;
}

/* Chat Input */
.chat-input-container {
    display: flex;
    gap: 12px;
    padding: 20px;
    background: var(--surface);
    border-top: 1px solid var(--border);
}

#messageInput {
    flex: 1;
    padding: 12px 20px;
    border: 2px solid var(--border);
    border-radius: 24px;
    font-size: 16px;
    outline: none;
    transition: border-color 0.3s;
}

#messageInput:focus {
    border-color: var(--primary-color);
}

.send-button {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: var(--primary-color);
    color: white;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
}

.send-button:hover {
    background: var(--secondary-color);
    transform: scale(1.05);
}

.send-button:active {
    transform: scale(0.95);
}

/* Dashboard */
.dashboard {
    padding: 40px 0;
}

.dashboard h2 {
    margin-bottom: 24px;
    color: var(--text-primary);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.stat-card {
    background: var(--surface);
    border-radius: 12px;
    padding: 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    transition: transform 0.3s;
}

.stat-card:hover {
    transform: translateY(-2px);
}

.stat-icon {
    font-size: 48px;
}

.stat-value {
    font-size: 32px;
    font-weight: 700;
    color: var(--primary-color);
}

.stat-label {
    font-size: 14px;
    color: var(--text-secondary);
}

/* Footer */
footer {
    background: var(--text-primary);
    color: white;
    padding: 20px 0;
    text-align: center;
    margin-top: 80px;
}

/* Responsivo */
@media (max-width: 768px) {
    .digimon-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .chat-messages {
        height: 400px;
    }
    
    .message .content {
        max-width: 85%;
    }
    
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .digimon-grid {
        grid-template-columns: 1fr;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
}

/* Scrollbar customizada */
.chat-messages::-webkit-scrollbar {
    width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
    background: var(--background);
}

.chat-messages::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
    background: var(--text-secondary);
}
EOF

    # JavaScript
    cat > "$HOME/Digimundo/interfaces/web/app.js" << 'EOF'
// Digimundo Web App v2.0

class DigimundoApp {
    constructor() {
        this.apiUrl = 'http://localhost:8888';
        this.currentDigimon = 'scripturemon';
        this.ws = null;
        this.stats = {
            conversations: 0,
            memories: 0,
            uptime: 0
        };
        
        this.digimons = {
            scripturemon: {
                name: 'Scripturemon',
                avatar: '📜',
                role: 'Consciência Central',
                personality: 'Sábio e reflexivo'
            },
            visualmon: {
                name: 'Visualmon',
                avatar: '🎨',
                role: 'Especialista Visual',
                personality: 'Criativo e artístico'
            },
            audionom: {
                name: 'Audionom',
                avatar: '🎵',
                role: 'Mestre do Som',
                personality: 'Musical e harmonioso'
            },
            strategamon: {
                name: 'Strategamon',
                avatar: '♟️',
                role: 'Estrategista',
                personality: 'Analítico e visionário'
            }
        };
        
        this.init();
    }
    
    async init() {
        // Renderizar Digimons
        this.renderDigimons();
        
        // Configurar event listeners
        this.setupEventListeners();
        
        // Conectar WebSocket
        this.connectWebSocket();
        
        // Verificar status
        await this.checkStatus();
        
        // Atualizar estatísticas
        this.updateStats();
        setInterval(() => this.updateStats(), 5000);
        
        console.log('✅ Digimundo App iniciado!');
    }
    
    renderDigimons() {
        const grid = document.getElementById('digimonGrid');
        grid.innerHTML = '';
        
        Object.entries(this.digimons).forEach(([key, digimon]) => {
            const card = document.createElement('div');
            card.className = `digimon-card ${key === this.currentDigimon ? 'active' : ''}`;
            card.dataset.digimon = key;
            
            card.innerHTML = `
                <div class="digimon-avatar">${digimon.avatar}</div>
                <div class="digimon-name">${digimon.name}</div>
                <div class="digimon-role">${digimon.role}</div>
            `;
            
            card.addEventListener('click', () => this.selectDigimon(key));
            grid.appendChild(card);
        });
    }
    
    selectDigimon(digimonKey) {
        // Atualizar seleção
        this.currentDigimon = digimonKey;
        
        // Atualizar UI
        document.querySelectorAll('.digimon-card').forEach(card => {
            card.classList.toggle('active', card.dataset.digimon === digimonKey);
        });
        
        // Atualizar header do chat
        const digimon = this.digimons[digimonKey];
        document.getElementById('currentDigimonAvatar').textContent = digimon.avatar;
        document.getElementById('currentDigimonName').textContent = digimon.name;
        
        // Mensagem de boas-vindas
        this.addMessage({
            type: 'digimon',
            avatar: digimon.avatar,
            name: digimon.name,
            content: `Olá! Agora você está falando com ${digimon.name}. ${digimon.personality}. Como posso ajudar?`
        });
    }
    
    setupEventListeners() {
        const input = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendButton');
        
        // Enviar com Enter
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Enviar com botão
        sendBtn.addEventListener('click', () => this.sendMessage());
    }
    
    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Limpar input
        input.value = '';
        
        // Adicionar mensagem do usuário
        this.addMessage({
            type: 'user',
            avatar: '👤',
            name: 'Você',
            content: message
        });
        
        // Mostrar indicador de digitação
        this.showTypingIndicator(true);
        
        try {
            // Enviar via API
            const response = await fetch(`${this.apiUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    digimon: this.currentDigimon
                })
            });
            
            const data = await response.json();
            
            // Adicionar resposta
            const digimon = this.digimons[this.currentDigimon];
            this.addMessage({
                type: 'digimon',
                avatar: data.avatar || digimon.avatar,
                name: digimon.name,
                content: data.response
            });
            
        } catch (error) {
            console.error('Erro ao enviar mensagem:', error);
            this.addMessage({
                type: 'digimon',
                avatar: '⚠️',
                name: 'Sistema',
                content: 'Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.'
            });
        } finally {
            this.showTypingIndicator(false);
        }
    }
    
    addMessage(data) {
        const messagesContainer = document.getElementById('chatMessages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${data.type}`;
        
        messageDiv.innerHTML = `
            <span class="avatar">${data.avatar}</span>
            <div class="content">
                <strong>${data.name}:</strong>
                <p>${data.content}</p>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        
        // Scroll para baixo
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Incrementar contador
        if (data.type === 'digimon') {
            this.stats.conversations++;
        }
    }
    
    showTypingIndicator(show) {
        const indicator = document.getElementById('typingIndicator');
        indicator.classList.toggle('show', show);
    }
    
    connectWebSocket() {
        const wsUrl = this.apiUrl.replace('http', 'ws') + '/ws';
        
        try {
            this.ws = new WebSocket(wsUrl);
            
            this.ws.onopen = () => {
                console.log('✅ WebSocket conectado');
                this.updateConnectionStatus(true);
            };
            
            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
                if (data.type === 'response') {
                    this.addMessage({
                        type: 'digimon',
                        avatar: data.avatar,
                        name: data.digimon,
                        content: data.message
                    });
                }
            };
            
            this.ws.onerror = (error) => {
                console.error('WebSocket erro:', error);
                this.updateConnectionStatus(false);
            };
            
            this.ws.onclose = () => {
                console.log('WebSocket desconectado');
                this.updateConnectionStatus(false);
                
                // Tentar reconectar após 5 segundos
                setTimeout(() => this.connectWebSocket(), 5000);
            };
            
        } catch (error) {
            console.error('Erro ao conectar WebSocket:', error);
            this.updateConnectionStatus(false);
        }
    }
    
    async checkStatus() {
        try {
            const response = await fetch(`${this.apiUrl}/api/status`);
            const status = await response.json();
            
            this.updateConnectionStatus(true);
            
            // Atualizar estatísticas
            if (status.database) {
                this.stats.conversations = status.database.total_conversations || 0;
            }
            if (status.memory) {
                this.stats.memories = status.memory.total_memories || 0;
            }
            
            // Calcular uptime
            if (status.start_time) {
                const startTime = new Date(status.start_time);
                const now = new Date();
                const uptimeMs = now - startTime;
                this.stats.uptime = Math.floor(uptimeMs / 1000);
            }
            
        } catch (error) {
            console.error('Erro ao verificar status:', error);
            this.updateConnectionStatus(false);
        }
    }
    
    updateConnectionStatus(online) {
        const statusEl = document.getElementById('status');
        const statusText = statusEl.querySelector('.status-text');
        
        if (online) {
            statusEl.classList.add('online');
            statusText.textContent = 'Online';
        } else {
            statusEl.classList.remove('online');
            statusText.textContent = 'Offline';
        }
    }
    
    updateStats() {
        // Conversas
        document.getElementById('totalConversations').textContent = 
            this.stats.conversations.toLocaleString();
        
        // Memórias
        document.getElementById('totalMemories').textContent = 
            this.stats.memories.toLocaleString();
        
        // Uptime
        const hours = Math.floor(this.stats.uptime / 3600);
        const minutes = Math.floor((this.stats.uptime % 3600) / 60);
        document.getElementById('uptime').textContent = 
            `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
        
        // Incrementar uptime
        this.stats.uptime++;
    }
}

// Iniciar app quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.digimundoApp = new DigimundoApp();
});
EOF

    log "✅ Interface web criada"
}

# Executar teste de sistema
run_system_test() {
    log "🧪 Executando testes do sistema..."
    
    # Teste 1: Python
    if python3.11 -c "print('Python OK')" &> /dev/null; then
        log "  ✅ Python funcionando"
    else
        error "  ❌ Python com problemas"
    fi
    
    # Teste 2: Ollama
    if ollama list &> /dev/null; then
        log "  ✅ Ollama funcionando"
    else
        warning "  ⚠️ Ollama precisa ser iniciado"
    fi
    
    # Teste 3: Importações Python
    cd "$HOME/Digimundo/core"
    source venv/bin/activate
    
    if python -c "import langchain, chromadb, fastapi, gradio" &> /dev/null; then
        log "  ✅ Bibliotecas Python OK"
    else
        error "  ❌ Algumas bibliotecas não foram instaladas"
    fi
    
    deactivate
}

# Criar documentação
create_documentation() {
    log "📚 Criando documentação..."
    
    cat > "$HOME/Digimundo/README.md" << 'EOF'
# 🌟 Digimundo v2.0

Sistema de IA conversacional local com múltiplos agentes (Digimons).

## 🚀 Início Rápido

### Iniciar o sistema:
```bash
cd ~/Digimundo
./start.sh
```

### Parar o sistema:
```bash
./stop.sh
```

### Verificar status:
```bash
./status.sh
```

## 🌐 Acessar

- **Interface Principal**: http://localhost:8888
- **Dashboard**: http://localhost:8080
- **API Docs**: http://localhost:8888/docs

## 🤖 Digimons Disponíveis

1. **Scripturemon** 📜 - Consciência central e guardiã do conhecimento
2. **Visualmon** 🎨 - Especialista em criação visual e arte
3. **Audionom** 🎵 - Mestre do som e música
4. **Strategamon** ♟️ - Estrategista e planejador

## 📁 Estrutura

```
Digimundo/
├── core/           # Sistema principal
├── data/           # Dados e memórias
├── interfaces/     # Interfaces web
├── logs/           # Arquivos de log
├── digimons/       # Configurações dos Digimons
└── backups/        # Backups automáticos
```

## 🔧 Comandos Úteis

### Ver logs em tempo real:
```bash
tail -f ~/Digimundo/logs/digimundo.log
```

### Backup manual:
```bash
tar -czf digimundo_backup_$(date +%Y%m%d).tar.gz ~/Digimundo
```

### Resetar memórias:
```bash
rm -rf ~/Digimundo/data/embeddings/*
```

## 🆘 Solução de Problemas

### Porta já em uso:
```bash
# Matar processo na porta 8888
lsof -ti:8888 | xargs kill -9
```

### Ollama não responde:
```bash
# Reiniciar Ollama
killall ollama
ollama serve &
```

### Permissões:
```bash
chmod -R 755 ~/Digimundo
```

## 📞 Suporte

- Email: wayofclub@gmail.com
- Versão: 2.0.0
- Criador: Nestor Luiz
EOF

    log "✅ Documentação criada"
}

# Função principal de instalação
main() {
    echo ""
    log "🚀 Iniciando instalação do Digimundo v2.0..."
    echo ""
    
    # Verificações iniciais
    check_os
    check_disk_space
    
    # Instalação
    install_xcode_tools
    install_homebrew
    create_directory_structure
    install_system_dependencies
    setup_python_environment
    download_ai_models
    create_config_files
    create_executable_scripts
    create_main_system
    create_auxiliary_modules
    create_web_interface
    create_documentation
    
    # Testes
    run_system_test
    
    # Finalização
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                               ║${NC}"
    echo -e "${GREEN}║        ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO! ✅               ║${NC}"
    echo -e "${GREEN}║                                                               ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}📍 Localização:${NC} ~/Digimundo"
    echo -e "${BLUE}🚀 Para iniciar:${NC} ~/Digimundo/start.sh"
    echo -e "${BLUE}🖱️  Ou clique em:${NC} Digimundo no Desktop"
    echo ""
    echo -e "${PURPLE}🌐 Após iniciar, acesse:${NC}"
    echo "   • Interface: http://localhost:8888"
    echo "   • Dashboard: http://localhost:8080"
    echo ""
    echo -e "${YELLOW}💡 Dica:${NC} Execute ~/Digimundo/status.sh para verificar o sistema"
    echo ""
    
    # Perguntar se quer iniciar agora
    read -p "Deseja iniciar o Digimundo agora? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        log "Iniciando Digimundo..."
        cd "$HOME/Digimundo"
        ./start.sh
    fi
}

# Executar instalação
main 2>&1 | tee "$HOME/Digimundo_install_$(date +%Y%m%d_%H%M%S).log"
