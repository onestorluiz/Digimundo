#!/bin/bash

# =================================================================
# 🚀 DIGIMUNDO ULTIMATE LAUNCHER - VERSÃO DEFINITIVA
# =================================================================
# Sistema completo de inicialização com todas as correções
# Data: 16/08/2025
# =================================================================

set -e  # Sair em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Diretório base
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Arquivo de log
LOG_DIR="$SCRIPT_DIR/eternal_logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/ultimate_$(date +%Y%m%d_%H%M%S).log"

# =================================================================
# FUNÇÕES UTILITÁRIAS
# =================================================================

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
# LIMPEZA E PREPARAÇÃO
# =================================================================

cleanup_processes() {
    log "Limpando processos antigos..."
    
    # Parar processos existentes
    pkill -f "Electron.*digimundo" 2>/dev/null || true
    pkill -f "node.*digimundo" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
    
    # Remover arquivos PID antigos
    rm -f "$SCRIPT_DIR/.digimundo.pid" 2>/dev/null || true
    rm -f "$SCRIPT_DIR/.monitor.pid" 2>/dev/null || true
    
    sleep 2
    success "Processos limpos"
}

check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        warning "Porta $port em uso, tentando liberar..."
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        sleep 1
    fi
    success "Porta $port disponível"
}

# =================================================================
# VERIFICAÇÃO DE DEPENDÊNCIAS
# =================================================================

check_dependencies() {
    log "Verificando dependências..."
    
    # Verificar Node.js
    if ! command -v node &> /dev/null; then
        error "Node.js não encontrado!"
        exit 1
    fi
    local node_version=$(node -v)
    info "Node.js: $node_version"
    
    # Verificar npm
    if ! command -v npm &> /dev/null; then
        error "npm não encontrado!"
        exit 1
    fi
    local npm_version=$(npm -v)
    info "npm: $npm_version"
    
    # Verificar node_modules
    if [ ! -d "$SCRIPT_DIR/node_modules" ]; then
        warning "node_modules não encontrado, instalando dependências..."
        npm install --no-audit --no-fund >> "$LOG_FILE" 2>&1
        success "Dependências instaladas"
    else
        success "Dependências verificadas"
    fi
    
    # Verificar Electron
    if [ ! -d "$SCRIPT_DIR/node_modules/electron" ]; then
        warning "Electron não encontrado, instalando..."
        npm install electron --save >> "$LOG_FILE" 2>&1
        success "Electron instalado"
    fi
}

# =================================================================
# CORREÇÃO DE BUGS CONHECIDOS
# =================================================================

fix_known_issues() {
    log "Aplicando correções de bugs conhecidos..."
    
    # Executar corretor automático se existir
    if [ -f "$SCRIPT_DIR/FIX_ALL_BUGS.js" ]; then
        node "$SCRIPT_DIR/FIX_ALL_BUGS.js" >> "$LOG_FILE" 2>&1 || true
    fi
    
    # Criar arquivo .env se não existir
    if [ ! -f "$SCRIPT_DIR/.env" ]; then
        cat > "$SCRIPT_DIR/.env" << EOF
NODE_ENV=development
PORT=7937
DIGIMUNDO_HOME=$HOME/Library/Application Support/Digimundo
ENABLE_WEBSOCKET=true
ENABLE_CLAUDE=false
ENABLE_OLLAMA=true
LOG_LEVEL=info
EOF
        success "Arquivo .env criado"
    fi
    
    success "Correções aplicadas"
}

# =================================================================
# INICIALIZAÇÃO DO SERVIDOR
# =================================================================

start_server() {
    log "Iniciando servidor backend..."
    
    # Iniciar servidor em background
    NODE_ENV=production npm run dev:server >> "$LOG_FILE" 2>&1 &
    local server_pid=$!
    echo $server_pid > "$SCRIPT_DIR/.server.pid"
    
    # Aguardar servidor estar pronto
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://localhost:7937/health > /dev/null 2>&1; then
            success "Servidor backend rodando (PID: $server_pid)"
            return 0
        fi
        sleep 1
        attempt=$((attempt + 1))
        echo -n "." | tee -a "$LOG_FILE"
    done
    
    error "Servidor não iniciou após ${max_attempts} segundos"
    return 1
}

# =================================================================
# INICIALIZAÇÃO DO ELECTRON
# =================================================================

start_electron() {
    log "Iniciando interface Electron..."
    
    # Iniciar Electron
    NODE_ENV=production npm run dev >> "$LOG_FILE" 2>&1 &
    local electron_pid=$!
    echo $electron_pid > "$SCRIPT_DIR/.electron.pid"
    
    sleep 3
    
    # Verificar se Electron está rodando
    if ps -p $electron_pid > /dev/null; then
        success "Interface Electron iniciada (PID: $electron_pid)"
        return 0
    else
        error "Falha ao iniciar Electron"
        return 1
    fi
}

# =================================================================
# MONITORAMENTO E HEALTH CHECK
# =================================================================

monitor_system() {
    log "Iniciando monitoramento do sistema..."
    
    # Loop de monitoramento
    while true; do
        # Verificar servidor
        if [ -f "$SCRIPT_DIR/.server.pid" ]; then
            local server_pid=$(cat "$SCRIPT_DIR/.server.pid")
            if ! ps -p $server_pid > /dev/null 2>&1; then
                warning "Servidor parou, reiniciando..."
                start_server
            fi
        fi
        
        # Verificar Electron (opcional, pois pode ser fechado pelo usuário)
        if [ -f "$SCRIPT_DIR/.electron.pid" ]; then
            local electron_pid=$(cat "$SCRIPT_DIR/.electron.pid")
            if ! ps -p $electron_pid > /dev/null 2>&1; then
                info "Electron foi fechado"
                rm -f "$SCRIPT_DIR/.electron.pid"
            fi
        fi
        
        # Health check via API
        if ! curl -s http://localhost:7937/health > /dev/null 2>&1; then
            warning "Health check falhou, verificando..."
        fi
        
        sleep 10
    done
}

# =================================================================
# FUNÇÃO DE PARADA
# =================================================================

stop_all() {
    log "Parando Digimundo..."
    
    # Parar servidor
    if [ -f "$SCRIPT_DIR/.server.pid" ]; then
        kill $(cat "$SCRIPT_DIR/.server.pid") 2>/dev/null || true
        rm -f "$SCRIPT_DIR/.server.pid"
    fi
    
    # Parar Electron
    if [ -f "$SCRIPT_DIR/.electron.pid" ]; then
        kill $(cat "$SCRIPT_DIR/.electron.pid") 2>/dev/null || true
        rm -f "$SCRIPT_DIR/.electron.pid"
    fi
    
    # Parar monitor
    if [ -f "$SCRIPT_DIR/.monitor.pid" ]; then
        kill $(cat "$SCRIPT_DIR/.monitor.pid") 2>/dev/null || true
        rm -f "$SCRIPT_DIR/.monitor.pid"
    fi
    
    # Limpar processos restantes
    cleanup_processes
    
    success "Digimundo parado"
}

# =================================================================
# TRAP PARA LIMPEZA AO SAIR
# =================================================================

trap stop_all EXIT INT TERM

# =================================================================
# MENU PRINCIPAL
# =================================================================

show_menu() {
    echo ""
    echo -e "${PURPLE}╔═══════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║       🌌 DIGIMUNDO LAUNCHER 🌌        ║${NC}"
    echo -e "${PURPLE}╚═══════════════════════════════════════╝${NC}"
    echo ""
    echo "  1) Iniciar Completo (Servidor + Interface)"
    echo "  2) Apenas Servidor Backend"
    echo "  3) Apenas Interface Electron"
    echo "  4) Verificar Status"
    echo "  5) Parar Tudo"
    echo "  6) Ver Logs"
    echo "  7) Limpar e Reinstalar"
    echo "  0) Sair"
    echo ""
}

check_status() {
    echo ""
    echo -e "${CYAN}=== STATUS DO SISTEMA ===${NC}"
    
    # Verificar servidor
    if curl -s http://localhost:7937/health > /dev/null 2>&1; then
        success "Servidor: ONLINE"
        local health=$(curl -s http://localhost:7937/health)
        info "Health: $health"
    else
        error "Servidor: OFFLINE"
    fi
    
    # Verificar Electron
    if pgrep -f "Electron.*digimundo" > /dev/null; then
        success "Electron: RODANDO"
    else
        warning "Electron: PARADO"
    fi
    
    # Verificar processos
    echo ""
    echo -e "${CYAN}Processos relacionados:${NC}"
    ps aux | grep -E "(digimundo|Electron)" | grep -v grep | head -5 || echo "Nenhum processo encontrado"
}

# =================================================================
# EXECUÇÃO PRINCIPAL
# =================================================================

main() {
    clear
    
    # Se passar argumento direto
    if [ "$1" == "start" ]; then
        cleanup_processes
        check_port 7937
        check_dependencies
        fix_known_issues
        start_server
        start_electron
        info "Digimundo iniciado! Monitorando sistema..."
        monitor_system
        exit 0
    fi
    
    if [ "$1" == "stop" ]; then
        stop_all
        exit 0
    fi
    
    # Menu interativo
    while true; do
        show_menu
        read -p "Escolha uma opção: " choice
        
        case $choice in
            1)
                cleanup_processes
                check_port 7937
                check_dependencies
                fix_known_issues
                start_server
                start_electron
                info "Sistema completo iniciado!"
                ;;
            2)
                cleanup_processes
                check_port 7937
                check_dependencies
                fix_known_issues
                start_server
                ;;
            3)
                start_electron
                ;;
            4)
                check_status
                ;;
            5)
                stop_all
                ;;
            6)
                tail -50 "$LOG_FILE"
                ;;
            7)
                stop_all
                rm -rf node_modules package-lock.json
                npm install
                success "Sistema reinstalado"
                ;;
            0)
                stop_all
                exit 0
                ;;
            *)
                error "Opção inválida"
                ;;
        esac
        
        echo ""
        read -p "Pressione ENTER para continuar..."
    done
}

# Executar
main "$@"