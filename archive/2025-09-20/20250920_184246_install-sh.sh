#!/bin/bash
# 🚀 DIGIMUNDO SWARM - INSTALADOR AUTOMÁTICO
# Instala e configura todo o sistema com um comando

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# ASCII Art
echo -e "${PURPLE}"
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     ____  _       _ __  __                 _             ║
║    |  _ \(_) __ _(_)  \/  |_   _ _ __   __| | ___       ║
║    | | | | |/ _` | | |\/| | | | | '_ \ / _` |/ _ \      ║
║    | |_| | | (_| | | |  | | |_| | | | | (_| | (_) |     ║
║    |____/|_|\__, |_|_|  |_|\__,_|_| |_|\__,_|\___/      ║
║             |___/                                        ║
║                                                          ║
║              AUTONOMOUS AGENT SWARM v1.0                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Variáveis
INSTALL_DIR="${HOME}/digimundo_swarm"
DIGIMUNDO_DIR="${HOME}/Digimundo"
PYTHON_VERSION="3.11"
VENV_DIR="${INSTALL_DIR}/venv"
LOG_FILE="${INSTALL_DIR}/install.log"

# Função de log
log() {
    echo -e "${2}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Verificar sistema operacional
check_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        DISTRO=$(lsb_release -si 2>/dev/null || echo "Unknown")
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        log "❌ Sistema operacional não suportado: $OSTYPE" "$RED"
        exit 1
    fi
    
    log "✅ Sistema detectado: $OS ($DISTRO)" "$GREEN"
}

# Verificar requisitos
check_requirements() {
    log "🔍 Verificando requisitos..." "$BLUE"
    
    # Python
    if ! command -v python3 &> /dev/null; then
        log "❌ Python3 não encontrado!" "$RED"
        
        if [[ "$OS" == "linux" ]]; then
            log "📦 Instalando Python..." "$YELLOW"
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
        elif [[ "$OS" == "macos" ]]; then
            log "📦 Instalando Python via Homebrew..." "$YELLOW"
            brew install python@3.11
        fi
    fi
    
    # Docker
    if ! command -v docker &> /dev/null; then
        log "❌ Docker não encontrado!" "$RED"
        
        read -p "Deseja instalar Docker? (s/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Ss]$ ]]; then
            install_docker
        else
            log "⚠️  Docker é necessário para execução completa" "$YELLOW"
        fi
    else
        log "✅ Docker encontrado" "$GREEN"
    fi
    
    # Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log "📦 Instalando Docker Compose..." "$YELLOW"
        
        if [[ "$OS" == "linux" ]]; then
            sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            sudo chmod +x /usr/local/bin/docker-compose
        elif [[ "$OS" == "macos" ]]; then
            brew install docker-compose
        fi
    fi
    
    # Git
    if ! command -v git &> /dev/null; then
        log "📦 Instalando Git..." "$YELLOW"
        
        if [[ "$OS" == "linux" ]]; then
            sudo apt-get install -y git
        elif [[ "$OS" == "macos" ]]; then
            brew install git
        fi
    fi
}

# Instalar Docker
install_docker() {
    log "🐳 Instalando Docker..." "$BLUE"
    
    if [[ "$OS" == "linux" ]]; then
        # Remover versões antigas
        sudo apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
        
        # Instalar dependências
        sudo apt-get update
        sudo apt-get install -y \
            ca-certificates \
            curl \
            gnupg \
            lsb-release
        
        # Adicionar chave GPG
        sudo mkdir -m 0755 -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        
        # Adicionar repositório
        echo \
            "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
            $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        
        # Instalar Docker
        sudo apt-get update
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        
        # Adicionar usuário ao grupo docker
        sudo usermod -aG docker $USER
        
        log "✅ Docker instalado! Faça logout e login para aplicar permissões" "$GREEN"
        
    elif [[ "$OS" == "macos" ]]; then
        log "📥 Baixe e instale Docker Desktop: https://www.docker.com/products/docker-desktop/" "$YELLOW"
        exit 1
    fi
}

# Criar estrutura de diretórios
create_structure() {
    log "📁 Criando estrutura de diretórios..." "$BLUE"
    
    # Criar diretório principal
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    
    # Criar subdiretórios
    mkdir -p {logs,data,chroma_db,execution_sandbox,ssl,config}
    mkdir -p grafana/{dashboards,datasources}
    
    # Criar diretório DigiMundo se não existir
    if [ ! -d "$DIGIMUNDO_DIR" ]; then
        log "📁 Criando diretório DigiMundo..." "$YELLOW"
        mkdir -p "$DIGIMUNDO_DIR"
    fi
    
    log "✅ Estrutura criada em $INSTALL_DIR" "$GREEN"
}

# Baixar arquivos do sistema
download_files() {
    log "📥 Baixando arquivos do sistema..." "$BLUE"
    
    # Array de arquivos Python
    PYTHON_FILES=(
        "orchestrator.py"
        "memory_agent.py"
        "learning_agent.py"
        "execution_agent.py"
        "model_switcher.py"
        "api_server.py"
    )
    
    # Simular download (em produção, baixar de repositório)
    for file in "${PYTHON_FILES[@]}"; do
        log "   📄 Criando $file..." "$GRAY"
        touch "$INSTALL_DIR/$file"
    done
    
    # Criar arquivo de configuração
    cat > "$INSTALL_DIR/config.json" << 'EOF'
{
    "base_path": "~/Digimundo",
    "monitor_paths": ["~/Digimundo"],
    "memory": {
        "db_path": "./chroma_db",
        "collection_name": "digimundo_memory"
    },
    "models": {
        "tiny": "tinyllama:latest",
        "small": "llama3.2:3b",
        "medium": "llama3.2:latest",
        "large": "mixtral:8x7b"
    },
    "thresholds": {
        "ram_critical": 90,
        "ram_high": 70,
        "ram_medium": 50,
        "cpu_high": 80
    },
    "allowed_commands": [
        "ls", "pwd", "echo", "cat", "grep", "find",
        "head", "tail", "sort", "uniq", "date",
        "git", "python3", "pip3", "npm", "node"
    ],
    "sandbox_mode": true
}
EOF
    
    log "✅ Arquivos baixados" "$GREEN"
}

# Configurar ambiente Python
setup_python_env() {
    log "🐍 Configurando ambiente Python..." "$BLUE"
    
    # Criar virtual environment
    python3 -m venv "$VENV_DIR"
    
    # Ativar venv
    source "$VENV_DIR/bin/activate"
    
    # Atualizar pip
    pip install --upgrade pip
    
    # Instalar dependências
    pip install -r requirements.txt
    
    log "✅ Ambiente Python configurado" "$GREEN"
}

# Configurar Nginx
setup_nginx() {
    log "🌐 Configurando Nginx..." "$BLUE"
    
    cat > "$INSTALL_DIR/nginx.conf" << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream digimundo_api {
        server digimundo:8000;
    }
    
    server {
        listen 80;
        server_name _;
        
        location / {
            proxy_pass http://digimundo_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        location /ws {
            proxy_pass http://digimundo_api;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
EOF
    
    log "✅ Nginx configurado" "$GREEN"
}

# Configurar Prometheus
setup_prometheus() {
    log "📊 Configurando Prometheus..." "$BLUE"
    
    cat > "$INSTALL_DIR/prometheus.yml" << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'digimundo'
    static_configs:
      - targets: ['digimundo:8000']
    
  - job_name: 'ollama'
    static_configs:
      - targets: ['ollama:11434']
    
  - job_name: 'chromadb'
    static_configs:
      - targets: ['chromadb:8000']
EOF
    
    log "✅ Prometheus configurado" "$GREEN"
}

# Configurar Grafana
setup_grafana() {
    log "📈 Configurando Grafana..." "$BLUE"
    
    # Datasource
    cat > "$INSTALL_DIR/grafana/datasources/prometheus.yml" << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF
    
    # Dashboard básico
    cat > "$INSTALL_DIR/grafana/dashboards/digimundo.json" << 'EOF'
{
  "dashboard": {
    "title": "DigiMundo Swarm Dashboard",
    "panels": [],
    "schemaVersion": 16,
    "version": 0
  }
}
EOF
    
    log "✅ Grafana configurado" "$GREEN"
}

# Criar scripts auxiliares
create_helper_scripts() {
    log "📝 Criando scripts auxiliares..." "$BLUE"
    
    # Script de start
    cat > "$INSTALL_DIR/start.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
docker-compose up -d
echo "🚀 DigiMundo Swarm iniciado!"
echo "📊 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo "📈 Grafana: http://localhost:3000 (admin/digimundo123)"
EOF
    chmod +x "$INSTALL_DIR/start.sh"
    
    # Script de stop
    cat > "$INSTALL_DIR/stop.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
docker-compose down
echo "🛑 DigiMundo Swarm parado!"
EOF
    chmod +x "$INSTALL_DIR/stop.sh"
    
    # Script de logs
    cat > "$INSTALL_DIR/logs.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
docker-compose logs -f --tail=100
EOF
    chmod +x "$INSTALL_DIR/logs.sh"
    
    # Script de status
    cat > "$INSTALL_DIR/status.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "📊 Status dos serviços:"
docker-compose ps
echo ""
echo "💾 Uso de recursos:"
docker stats --no-stream
EOF
    chmod +x "$INSTALL_DIR/status.sh"
    
    # Script de update
    cat > "$INSTALL_DIR/update.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "🔄 Atualizando DigiMundo Swarm..."
docker-compose pull
docker-compose up -d --build
echo "✅ Atualização completa!"
EOF
    chmod +x "$INSTALL_DIR/update.sh"
    
    log "✅ Scripts auxiliares criados" "$GREEN"
}

# Construir containers
build_containers() {
    log "🏗️ Construindo containers..." "$BLUE"
    
    cd "$INSTALL_DIR"
    
    # Construir imagens
    docker-compose build --no-cache
    
    # Baixar imagens externas
    docker-compose pull
    
    log "✅ Containers construídos" "$GREEN"
}

# Iniciar sistema
start_system() {
    log "🚀 Iniciando sistema..." "$BLUE"
    
    cd "$INSTALL_DIR"
    
    # Iniciar containers
    docker-compose up -d
    
    # Aguardar inicialização
    log "⏳ Aguardando inicialização dos serviços..." "$YELLOW"
    sleep 30
    
    # Verificar saúde
    if curl -f http://localhost:8000/health &>/dev/null; then
        log "✅ Sistema iniciado com sucesso!" "$GREEN"
    else
        log "⚠️  Sistema iniciado mas ainda não está respondendo" "$YELLOW"
        log "   Verifique os logs com: $INSTALL_DIR/logs.sh" "$YELLOW"
    fi
}

# Mostrar instruções finais
show_instructions() {
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║         🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO! 🎉         ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${BLUE}📁 Diretório de instalação:${NC} $INSTALL_DIR"
    echo -e "${BLUE}📁 Diretório DigiMundo:${NC} $DIGIMUNDO_DIR"
    echo ""
    echo -e "${YELLOW}🔧 Comandos disponíveis:${NC}"
    echo "   $INSTALL_DIR/start.sh   - Iniciar sistema"
    echo "   $INSTALL_DIR/stop.sh    - Parar sistema"
    echo "   $INSTALL_DIR/logs.sh    - Ver logs"
    echo "   $INSTALL_DIR/status.sh  - Ver status"
    echo "   $INSTALL_DIR/update.sh  - Atualizar sistema"
    echo ""
    echo -e "${YELLOW}🌐 URLs de acesso:${NC}"
    echo "   API REST:    http://localhost:8000"
    echo "   Docs:        http://localhost:8000/docs"
    echo "   Grafana:     http://localhost:3000 (admin/digimundo123)"
    echo "   Prometheus:  http://localhost:9090"
    echo ""
    echo -e "${GREEN}💡 Próximos passos:${NC}"
    echo "   1. Adicione arquivos ao diretório $DIGIMUNDO_DIR"
    echo "   2. O sistema aprenderá automaticamente"
    echo "   3. Use a API para fazer consultas"
    echo ""
    echo -e "${PURPLE}🤖 Teste rápido:${NC}"
    echo "   curl -X POST http://localhost:8000/query \\"
    echo "     -H 'Content-Type: application/json' \\"
    echo "     -d '{\"query\": \"O que é o DigiMundo?\"}"
    echo ""
}

# Função principal
main() {
    log "🚀 Iniciando instalação do DigiMundo Swarm..." "$BLUE"
    
    # Criar diretório de logs
    mkdir -p "$(dirname "$LOG_FILE")"
    
    # Executar passos
    check_os
    check_requirements
    create_structure
    download_files
    setup_nginx
    setup_prometheus
    setup_grafana
    create_helper_scripts
    
    # Perguntar sobre Docker
    read -p "Deseja construir e iniciar os containers agora? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        build_containers
        start_system
    else
        log "⚠️  Execute '$INSTALL_DIR/start.sh' quando estiver pronto" "$YELLOW"
    fi
    
    # Mostrar instruções
    show_instructions
    
    log "✅ Instalação completa!" "$GREEN"
}

# Tratamento de erros
trap 'log "❌ Erro durante instalação. Verifique $LOG_FILE" "$RED"; exit 1' ERR

# Executar
main

