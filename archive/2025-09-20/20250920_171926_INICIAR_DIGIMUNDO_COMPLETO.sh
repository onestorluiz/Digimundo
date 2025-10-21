#!/bin/bash

# ╔═══════════════════════════════════════════════════════════════════╗
# ║           🌌 DIGIMUNDO COMPLETO - INICIALIZADOR MESTRE 🌌          ║
# ╚═══════════════════════════════════════════════════════════════════╝
# Data: 18/08/2025
# Este script inicia TUDO: Claude Code, Ollama e Digimundo

set -e

# Cores para output bonito
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# Diretório do Digimundo
DIGIMUNDO_DIR="$HOME/Digimundo/digimundo_starter"
LOG_DIR="$DIGIMUNDO_DIR/eternal_logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/inicializacao_completa_$(date +%Y%m%d_%H%M%S).log"

# =================================================================
# FUNÇÕES UTILITÁRIAS
# =================================================================

print_header() {
    clear
    echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║           ${WHITE}🌌 DIGIMUNDO COMPLETO - INICIALIZADOR MESTRE 🌌${PURPLE}          ║${NC}"
    echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

log() {
    echo -e "${CYAN}[$(date +'%H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✅ $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}❌ $1${NC}" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}" | tee -a "$LOG_FILE"
}

# =================================================================
# LIMPEZA INICIAL
# =================================================================

cleanup_old_processes() {
    log "Limpando processos antigos..."
    
    # Parar processos do Digimundo
    pkill -f "Electron.*digimundo" 2>/dev/null || true
    pkill -f "node.*digimundo" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
    pkill -f "SABIAMON" 2>/dev/null || true
    
    # Limpar portas
    lsof -ti:7937 | xargs kill -9 2>/dev/null || true
    lsof -ti:11434 | xargs kill -9 2>/dev/null || true
    
    sleep 2
    success "Processos limpos"
}

# =================================================================
# VERIFICAÇÃO DE DEPENDÊNCIAS
# =================================================================

check_dependencies() {
    log "Verificando dependências básicas..."
    
    # Node.js
    if ! command -v node &> /dev/null; then
        error "Node.js não encontrado! Instale primeiro."
        exit 1
    fi
    info "Node.js: $(node -v)"
    
    # npm
    if ! command -v npm &> /dev/null; then
        error "npm não encontrado!"
        exit 1
    fi
    info "npm: $(npm -v)"
    
    # Ollama
    if ! command -v ollama &> /dev/null; then
        warning "Ollama não encontrado. Instalando..."
        curl -fsSL https://ollama.com/install.sh | sh
    fi
    info "Ollama: instalado"
    
    # Claude Code
    if ! command -v claude-code &> /dev/null && ! command -v npx &> /dev/null; then
        warning "Claude Code não encontrado localmente"
    else
        info "Claude Code: disponível"
    fi
    
    success "Dependências verificadas"
}

# =================================================================
# INICIAR OLLAMA
# =================================================================

start_ollama() {
    log "Iniciando servidor Ollama..."
    
    # Verificar se já está rodando
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        success "Ollama já está rodando"
        return 0
    fi
    
    # Iniciar Ollama
    ollama serve >> "$LOG_FILE" 2>&1 &
    OLLAMA_PID=$!
    
    # Aguardar inicialização
    local max_attempts=15
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            success "Ollama servidor rodando (PID: $OLLAMA_PID)"
            
            # Listar modelos disponíveis
            echo ""
            info "Modelos Ollama disponíveis:"
            ollama list | head -10
            echo ""
            return 0
        fi
        sleep 1
        echo -n "."
        attempt=$((attempt + 1))
    done
    
    error "Ollama não iniciou"
    return 1
}

# =================================================================
# INSTALAR DEPENDÊNCIAS DO DIGIMUNDO
# =================================================================

install_digimundo_deps() {
    cd "$DIGIMUNDO_DIR"
    
    if [ ! -d "node_modules" ]; then
        log "Instalando dependências do Digimundo..."
        npm install --no-audit --no-fund >> "$LOG_FILE" 2>&1
        success "Dependências instaladas"
    else
        info "Dependências do Digimundo já instaladas"
    fi
    
    # Criar .env se não existir
    if [ ! -f ".env" ]; then
        cat > .env << EOF
NODE_ENV=production
PORT=7937
DIGIMUNDO_HOME=$HOME/Library/Application Support/Digimundo
ENABLE_WEBSOCKET=true
ENABLE_CLAUDE=true
ENABLE_OLLAMA=true
LOG_LEVEL=info
EOF
        success "Arquivo .env criado"
    fi
}

# =================================================================
# INICIAR SERVIDOR DIGIMUNDO
# =================================================================

start_digimundo_server() {
    cd "$DIGIMUNDO_DIR"
    log "Iniciando servidor Digimundo..."
    
    # Aplicar correções de bugs primeiro
    if [ -f "FIX_ALL_BUGS.js" ]; then
        node FIX_ALL_BUGS.js >> "$LOG_FILE" 2>&1 || true
    fi
    
    # Iniciar servidor
    npm run dev:server >> "$LOG_FILE" 2>&1 &
    SERVER_PID=$!
    
    # Aguardar servidor
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://localhost:7937/api/status > /dev/null 2>&1; then
            success "Servidor Digimundo rodando (PID: $SERVER_PID)"
            return 0
        fi
        sleep 1
        echo -n "."
        attempt=$((attempt + 1))
    done
    
    error "Servidor Digimundo não iniciou"
    return 1
}

# =================================================================
# INICIAR INTERFACE ELECTRON
# =================================================================

start_electron() {
    cd "$DIGIMUNDO_DIR"
    log "Iniciando interface Electron..."
    
    npm run dev >> "$LOG_FILE" 2>&1 &
    ELECTRON_PID=$!
    
    sleep 5
    
    if ps -p $ELECTRON_PID > /dev/null; then
        success "Interface Electron iniciada (PID: $ELECTRON_PID)"
        return 0
    else
        warning "Interface Electron não iniciou (pode ser normal se já estiver aberta)"
        return 1
    fi
}

# =================================================================
# INICIAR SABIAMON DEBUGGER
# =================================================================

start_sabiamon() {
    cd "$DIGIMUNDO_DIR"
    
    if [ -f "SABIAMON_AUTONOMOUS_DEBUGGER.js" ]; then
        log "Iniciando Sabiamon Debugger 24/7..."
        node SABIAMON_AUTONOMOUS_DEBUGGER.js >> "$LOG_FILE" 2>&1 &
        SABIAMON_PID=$!
        success "Sabiamon Debugger rodando (PID: $SABIAMON_PID)"
    else
        warning "Sabiamon Debugger não encontrado"
    fi
}

# =================================================================
# VERIFICAR STATUS COMPLETO
# =================================================================

check_status() {
    echo ""
    echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║                     ${WHITE}📊 STATUS DO SISTEMA 📊${PURPLE}                        ║${NC}"
    echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Ollama
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        success "Ollama: ATIVO ✅ (porta 11434)"
    else
        error "Ollama: INATIVO ❌"
    fi
    
    # Servidor Digimundo
    if curl -s http://localhost:7937/api/status > /dev/null 2>&1; then
        success "Servidor Digimundo: ATIVO ✅ (porta 7937)"
        
        # Tentar buscar info dos Digimons
        curl -s http://localhost:7937/api/digimons 2>/dev/null | jq -r '.[] | "   • \(.name): \(.status)"' 2>/dev/null || true
    else
        error "Servidor Digimundo: INATIVO ❌"
    fi
    
    # Claude Code
    if command -v claude-code &> /dev/null; then
        success "Claude Code: DISPONÍVEL ✅"
    else
        info "Claude Code: Use 'npx @anthropic-ai/claude-code' para acessar"
    fi
    
    # Processos
    echo ""
    info "Processos rodando:"
    ps aux | grep -E "ollama|digimundo|SABIAMON|Electron" | grep -v grep | wc -l | xargs echo "   Total de processos:"
    
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║               ${WHITE}🎉 SISTEMA DIGIMUNDO COMPLETO ATIVO! 🎉${GREEN}              ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    info "Interface Web: http://localhost:7937"
    info "API Status: http://localhost:7937/api/status"
    info "Logs: $LOG_FILE"
    echo ""
}

# =================================================================
# MENU PRINCIPAL
# =================================================================

show_menu() {
    echo ""
    echo -e "${CYAN}O que você deseja fazer?${NC}"
    echo ""
    echo "  1) Iniciar TUDO (Recomendado)"
    echo "  2) Verificar Status"
    echo "  3) Parar Tudo"
    echo "  4) Ver Logs"
    echo "  5) Reiniciar Tudo"
    echo "  0) Sair"
    echo ""
    read -p "Escolha uma opção: " choice
    
    case $choice in
        1)
            start_everything
            ;;
        2)
            check_status
            ;;
        3)
            stop_everything
            ;;
        4)
            view_logs
            ;;
        5)
            restart_everything
            ;;
        0)
            exit 0
            ;;
        *)
            error "Opção inválida"
            show_menu
            ;;
    esac
}

# =================================================================
# INICIAR TUDO
# =================================================================

start_everything() {
    print_header
    
    log "🚀 Iniciando sistema completo Digimundo..."
    echo ""
    
    # Limpar processos antigos
    cleanup_old_processes
    
    # Verificar dependências
    check_dependencies
    
    # Instalar dependências do Digimundo
    install_digimundo_deps
    
    # Iniciar Ollama
    start_ollama
    
    # Iniciar Servidor Digimundo
    start_digimundo_server
    
    # Iniciar Interface Electron
    start_electron
    
    # Iniciar Sabiamon
    start_sabiamon
    
    # Verificar status final
    sleep 3
    check_status
    
    # Manter script rodando para monitoramento
    echo ""
    info "Sistema rodando! Pressione CTRL+C para parar tudo."
    echo ""
    
    # Loop de monitoramento
    while true; do
        sleep 30
        # Verificação silenciosa
        if ! curl -s http://localhost:7937/api/status > /dev/null 2>&1; then
            warning "Servidor parou, reiniciando..."
            start_digimundo_server
        fi
        if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            warning "Ollama parou, reiniciando..."
            start_ollama
        fi
    done
}

# =================================================================
# PARAR TUDO
# =================================================================

stop_everything() {
    log "Parando todo o sistema..."
    
    # Parar processos
    pkill -f "ollama serve" 2>/dev/null || true
    pkill -f "Electron.*digimundo" 2>/dev/null || true
    pkill -f "node.*digimundo" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
    pkill -f "SABIAMON" 2>/dev/null || true
    
    # Limpar portas
    lsof -ti:7937 | xargs kill -9 2>/dev/null || true
    lsof -ti:11434 | xargs kill -9 2>/dev/null || true
    
    success "Sistema parado"
}

# =================================================================
# VER LOGS
# =================================================================

view_logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        error "Arquivo de log não encontrado"
    fi
}

# =================================================================
# REINICIAR TUDO
# =================================================================

restart_everything() {
    log "Reiniciando sistema..."
    stop_everything
    sleep 3
    start_everything
}

# =================================================================
# TRATAMENTO DE SINAIS
# =================================================================

trap 'echo ""; warning "Interrompido! Parando sistema..."; stop_everything; exit 0' INT TERM

# =================================================================
# EXECUÇÃO PRINCIPAL
# =================================================================

# Se passar argumento direto, executar sem menu
case "${1:-}" in
    start)
        start_everything
        ;;
    stop)
        stop_everything
        ;;
    status)
        check_status
        ;;
    restart)
        restart_everything
        ;;
    *)
        # Iniciar automaticamente sem menu interativo
        start_everything
        ;;
esac