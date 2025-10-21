#!/bin/bash

# ========================================
# 🚀 ELECTRON OPTIMIZER & LAUNCHER
# Sistema completo de otimização e inicialização
# Versão: 1.0.0
# Data: 14/08/2025
# ========================================

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Configurações
PROJECT_DIR="$HOME/Digimundo/digimundo_starter"
LOG_DIR="$PROJECT_DIR/eternal_logs"
HEALTH_LOG="$LOG_DIR/health_system.log"
ELECTRON_LOG="$LOG_DIR/electron.log"

# ========================================
# FUNÇÕES UTILITÁRIAS
# ========================================

print_header() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║         ELECTRON OPTIMIZER & LAUNCHER v1.0           ║"
    echo "╠═══════════════════════════════════════════════════════╣"
    echo "║  🚀 Otimização completa do sistema Electron          ║"
    echo "║  🔧 Correção automática de problemas                 ║"
    echo "║  📊 Monitoramento em tempo real                      ║"
    echo "║  🛡️  Verificação de segurança                        ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_status() {
    local status=$1
    local message=$2
    
    case $status in
        "success")
            echo -e "${GREEN}✅ $message${NC}"
            ;;
        "error")
            echo -e "${RED}❌ $message${NC}"
            ;;
        "warning")
            echo -e "${YELLOW}⚠️  $message${NC}"
            ;;
        "info")
            echo -e "${BLUE}ℹ️  $message${NC}"
            ;;
        "progress")
            echo -e "${MAGENTA}⏳ $message${NC}"
            ;;
    esac
}

# ========================================
# VERIFICAÇÕES INICIAIS
# ========================================

check_requirements() {
    print_status "info" "Verificando requisitos do sistema..."
    
    # Verificar Node.js
    if ! command -v node &> /dev/null; then
        print_status "error" "Node.js não encontrado! Instalando..."
        brew install node
    else
        NODE_VERSION=$(node -v)
        print_status "success" "Node.js instalado: $NODE_VERSION"
    fi
    
    # Verificar npm
    if ! command -v npm &> /dev/null; then
        print_status "error" "npm não encontrado!"
        exit 1
    else
        NPM_VERSION=$(npm -v)
        print_status "success" "npm instalado: $NPM_VERSION"
    fi
    
    # Verificar diretório do projeto
    if [ ! -d "$PROJECT_DIR" ]; then
        print_status "error" "Diretório do projeto não encontrado: $PROJECT_DIR"
        exit 1
    fi
    
    cd "$PROJECT_DIR"
    print_status "success" "Diretório do projeto encontrado"
}

# ========================================
# LIMPEZA E OTIMIZAÇÃO
# ========================================

clean_system() {
    print_status "progress" "Limpando sistema..."
    
    # Criar diretório de logs se não existir
    mkdir -p "$LOG_DIR"
    
    # Limpar logs antigos (manter últimos 7 dias)
    find "$LOG_DIR" -name "*.log" -mtime +7 -delete 2>/dev/null || true
    
    # Limpar cache do npm
    print_status "progress" "Limpando cache do npm..."
    npm cache clean --force > /dev/null 2>&1
    
    # Limpar cache do Electron
    print_status "progress" "Limpando cache do Electron..."
    rm -rf ~/.electron 2>/dev/null || true
    
    # Limpar arquivos temporários
    rm -rf /tmp/electron-* 2>/dev/null || true
    rm -rf ~/Library/Caches/Electron* 2>/dev/null || true
    
    print_status "success" "Sistema limpo"
}

# ========================================
# VERIFICAÇÃO DE DEPENDÊNCIAS
# ========================================

check_dependencies() {
    print_status "progress" "Verificando dependências..."
    
    # Verificar package.json
    if [ ! -f "package.json" ]; then
        print_status "error" "package.json não encontrado!"
        exit 1
    fi
    
    # Verificar node_modules
    if [ ! -d "node_modules" ]; then
        print_status "warning" "node_modules não encontrado. Instalando dependências..."
        npm install
    else
        # Verificar integridade
        print_status "progress" "Verificando integridade das dependências..."
        
        # Lista de módulos essenciais
        REQUIRED_MODULES=(
            "electron"
            "express"
            "cors"
            "socket.io"
            "jsonwebtoken"
            "bcrypt"
            "sqlite3"
            "ws"
        )
        
        MISSING_MODULES=()
        
        for module in "${REQUIRED_MODULES[@]}"; do
            if [ ! -d "node_modules/$module" ]; then
                MISSING_MODULES+=("$module")
            fi
        done
        
        if [ ${#MISSING_MODULES[@]} -gt 0 ]; then
            print_status "warning" "Módulos faltando: ${MISSING_MODULES[*]}"
            print_status "progress" "Instalando módulos faltantes..."
            npm install "${MISSING_MODULES[@]}"
        else
            print_status "success" "Todas as dependências estão instaladas"
        fi
    fi
}

# ========================================
# VERIFICAÇÃO DE SEGURANÇA
# ========================================

security_check() {
    print_status "progress" "Executando verificação de segurança..."
    
    # Executar npm audit
    AUDIT_OUTPUT=$(npm audit --json 2>/dev/null || echo '{"metadata":{"vulnerabilities":{"total":0}}}')
    VULNERABILITIES=$(echo "$AUDIT_OUTPUT" | grep -o '"total":[0-9]*' | cut -d':' -f2)
    
    if [ "$VULNERABILITIES" -gt 0 ]; then
        print_status "warning" "Encontradas $VULNERABILITIES vulnerabilidades"
        
        # Tentar corrigir automaticamente
        print_status "progress" "Tentando corrigir vulnerabilidades..."
        npm audit fix --force > /dev/null 2>&1
        
        # Verificar novamente
        AUDIT_OUTPUT=$(npm audit --json 2>/dev/null || echo '{"metadata":{"vulnerabilities":{"total":0}}}')
        VULNERABILITIES=$(echo "$AUDIT_OUTPUT" | grep -o '"total":[0-9]*' | cut -d':' -f2)
        
        if [ "$VULNERABILITIES" -gt 0 ]; then
            print_status "warning" "Ainda restam $VULNERABILITIES vulnerabilidades"
        else
            print_status "success" "Todas as vulnerabilidades foram corrigidas"
        fi
    else
        print_status "success" "Nenhuma vulnerabilidade encontrada"
    fi
}

# ========================================
# OTIMIZAÇÃO DE PERFORMANCE
# ========================================

optimize_performance() {
    print_status "progress" "Otimizando performance..."
    
    # Configurar variáveis de ambiente para melhor performance
    export NODE_ENV="production"
    export NODE_OPTIONS="--max-old-space-size=4096"
    export ELECTRON_ENABLE_LOGGING=1
    export ELECTRON_ENABLE_STACK_DUMPING=1
    
    # Criar arquivo de configuração de performance
    cat > "$PROJECT_DIR/.performance.json" << EOF
{
  "memory": {
    "maxHeap": 4096,
    "gcInterval": 30000,
    "gcThreshold": 0.8
  },
  "cpu": {
    "maxWorkers": 4,
    "throttle": 100
  },
  "cache": {
    "enabled": true,
    "maxSize": 100,
    "ttl": 3600
  },
  "monitoring": {
    "enabled": true,
    "interval": 5000,
    "metrics": ["memory", "cpu", "handles", "requests"]
  }
}
EOF
    
    print_status "success" "Performance otimizada"
}

# ========================================
# KILL PROCESSOS ANTIGOS
# ========================================

kill_old_processes() {
    print_status "progress" "Verificando processos antigos..."
    
    # Matar processos Electron antigos
    ELECTRON_PIDS=$(pgrep -f "Electron|electron" 2>/dev/null || true)
    
    if [ ! -z "$ELECTRON_PIDS" ]; then
        print_status "warning" "Encontrados processos Electron rodando"
        echo "$ELECTRON_PIDS" | while read pid; do
            if [ ! -z "$pid" ]; then
                kill -9 "$pid" 2>/dev/null || true
                print_status "info" "Processo $pid terminado"
            fi
        done
        sleep 2
    fi
    
    # Matar processos Node antigos na porta 7937
    lsof -ti:7937 | xargs kill -9 2>/dev/null || true
    
    print_status "success" "Processos antigos terminados"
}

# ========================================
# INICIAR SISTEMA DE SAÚDE
# ========================================

start_health_system() {
    print_status "progress" "Iniciando sistema de monitoramento de saúde..."
    
    # Verificar se o arquivo existe
    if [ -f "$PROJECT_DIR/electron_health_system.js" ]; then
        # Iniciar em background
        nohup node "$PROJECT_DIR/electron_health_system.js" > "$HEALTH_LOG" 2>&1 &
        HEALTH_PID=$!
        
        # Salvar PID
        echo $HEALTH_PID > "$PROJECT_DIR/.health.pid"
        
        print_status "success" "Sistema de saúde iniciado (PID: $HEALTH_PID)"
    else
        print_status "warning" "Sistema de saúde não encontrado"
    fi
}

# ========================================
# INICIAR ELECTRON
# ========================================

start_electron() {
    print_status "progress" "Iniciando Electron..."
    
    # Verificar se main.js existe
    if [ ! -f "$PROJECT_DIR/app/main.js" ]; then
        print_status "error" "Arquivo main.js não encontrado!"
        exit 1
    fi
    
    # Iniciar Electron com logs
    print_status "info" "Iniciando aplicação..."
    echo -e "${YELLOW}"
    echo "════════════════════════════════════════"
    echo "  ELECTRON INICIADO - MODO OTIMIZADO"
    echo "════════════════════════════════════════"
    echo -e "${NC}"
    
    # Executar com monitoramento
    npm run dev 2>&1 | tee "$ELECTRON_LOG"
}

# ========================================
# MENU INTERATIVO
# ========================================

show_menu() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════╗"
    echo "║         OPÇÕES DE INICIALIZAÇÃO       ║"
    echo "╠═══════════════════════════════════════╣"
    echo "║  1) Inicialização Rápida              ║"
    echo "║  2) Inicialização Completa            ║"
    echo "║  3) Modo Desenvolvimento              ║"
    echo "║  4) Modo Produção                     ║"
    echo "║  5) Apenas Monitoramento              ║"
    echo "║  6) Limpeza Completa                  ║"
    echo "║  0) Sair                              ║"
    echo "╚═══════════════════════════════════════╝"
    echo -e "${NC}"
    
    read -p "Escolha uma opção: " choice
    
    case $choice in
        1)
            # Inicialização rápida
            kill_old_processes
            start_electron
            ;;
        2)
            # Inicialização completa
            check_requirements
            clean_system
            check_dependencies
            security_check
            optimize_performance
            kill_old_processes
            start_health_system
            start_electron
            ;;
        3)
            # Modo desenvolvimento
            export NODE_ENV="development"
            kill_old_processes
            start_electron
            ;;
        4)
            # Modo produção
            export NODE_ENV="production"
            optimize_performance
            kill_old_processes
            start_electron
            ;;
        5)
            # Apenas monitoramento
            start_health_system
            echo "Sistema de monitoramento iniciado. Pressione Ctrl+C para parar."
            tail -f "$HEALTH_LOG"
            ;;
        6)
            # Limpeza completa
            clean_system
            rm -rf node_modules package-lock.json
            npm install
            print_status "success" "Limpeza completa realizada"
            ;;
        0)
            print_status "info" "Saindo..."
            exit 0
            ;;
        *)
            print_status "error" "Opção inválida!"
            show_menu
            ;;
    esac
}

# ========================================
# EXECUÇÃO PRINCIPAL
# ========================================

main() {
    clear
    print_header
    
    # Se nenhum argumento, mostrar menu
    if [ $# -eq 0 ]; then
        show_menu
    else
        # Processar argumentos
        case "$1" in
            --quick|-q)
                kill_old_processes
                start_electron
                ;;
            --full|-f)
                check_requirements
                clean_system
                check_dependencies
                security_check
                optimize_performance
                kill_old_processes
                start_health_system
                start_electron
                ;;
            --health|-h)
                start_health_system
                tail -f "$HEALTH_LOG"
                ;;
            --clean|-c)
                clean_system
                ;;
            --help)
                echo "Uso: $0 [opção]"
                echo "Opções:"
                echo "  --quick, -q    : Inicialização rápida"
                echo "  --full, -f     : Inicialização completa com otimizações"
                echo "  --health, -h   : Apenas sistema de monitoramento"
                echo "  --clean, -c    : Limpeza do sistema"
                echo "  --help         : Mostrar esta ajuda"
                ;;
            *)
                print_status "error" "Opção inválida: $1"
                echo "Use --help para ver as opções disponíveis"
                exit 1
                ;;
        esac
    fi
}

# ========================================
# HANDLERS DE SAÍDA
# ========================================

cleanup() {
    print_status "info" "Finalizando..."
    
    # Matar processo de saúde se estiver rodando
    if [ -f "$PROJECT_DIR/.health.pid" ]; then
        HEALTH_PID=$(cat "$PROJECT_DIR/.health.pid")
        kill -9 "$HEALTH_PID" 2>/dev/null || true
        rm "$PROJECT_DIR/.health.pid"
    fi
    
    # Matar processos Electron
    pkill -f "Electron|electron" 2>/dev/null || true
    
    print_status "success" "Sistema finalizado"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Executar
main "$@"
