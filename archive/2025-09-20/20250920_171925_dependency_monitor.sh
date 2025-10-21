#!/bin/bash

# 🛡️ MONITOR DE DEPENDÊNCIAS - Previne erros de módulos faltantes

# Configuração
SCRIPT_DIR="/Users/clubproducoes/Digimundo/digimundo_starter"
NODE_BIN="/opt/homebrew/opt/node@20/bin/node"
NPM_BIN="/opt/homebrew/opt/node@20/bin/npm"
LOG_DIR="$SCRIPT_DIR/eternal_logs"
CHECK_INTERVAL=60  # Verificar a cada 60 segundos

# Criar diretório de logs
mkdir -p "$LOG_DIR"

# Função de log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_DIR/dependency_monitor.log"
}

# Função para verificar dependências
check_dependencies() {
    cd "$SCRIPT_DIR"
    
    # Lista de módulos críticos
    local modules=("jsonwebtoken" "bcrypt" "express" "cors" "socket.io" "sqlite3" "dotenv")
    local missing=()
    
    for module in "${modules[@]}"; do
        if [ ! -d "node_modules/$module" ]; then
            missing+=("$module")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        log "⚠️ Módulos faltantes detectados: ${missing[*]}"
        log "🔧 Instalando módulos automaticamente..."
        
        for module in "${missing[@]}"; do
            $NPM_BIN install "$module" --save >> "$LOG_DIR/auto_install.log" 2>&1
            if [ $? -eq 0 ]; then
                log "✅ $module instalado com sucesso"
            else
                log "❌ Erro ao instalar $module"
            fi
        done
        
        # Reiniciar Electron se necessário
        if pgrep -f "Electron.*digimundo" > /dev/null; then
            log "🔄 Reiniciando Electron..."
            pkill -f "Electron.*digimundo"
            sleep 2
            nohup $NPM_BIN run dev >> "$LOG_DIR/electron.log" 2>&1 &
            log "✅ Electron reiniciado"
        fi
    fi
}

# Iniciar monitoramento
log "🛡️ Monitor de dependências iniciado"

while true; do
    check_dependencies
    sleep $CHECK_INTERVAL
done
