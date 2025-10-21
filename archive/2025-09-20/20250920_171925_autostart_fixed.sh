#!/bin/bash

# Configurar PATH completo
export PATH="/opt/homebrew/opt/node@20/bin:/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
export NODE_PATH="/opt/homebrew/opt/node@20/bin/node"

# Diretório do projeto
SCRIPT_DIR="/Users/clubproducoes/Digimundo/digimundo_starter"
cd "$SCRIPT_DIR"

# Criar diretório de logs
mkdir -p "$SCRIPT_DIR/eternal_logs"
LOG_FILE="$SCRIPT_DIR/eternal_logs/autostart_$(date +%Y%m%d).log"

# Log inicial
echo "[$(date)] ========== AUTOSTART DIGIMUNDO ==========" >> "$LOG_FILE"
echo "[$(date)] Iniciando sistema..." >> "$LOG_FILE"

# Aguardar sistema estar pronto (30 segundos após boot)
sleep 30

# Função para iniciar servidor
start_server() {
    echo "[$(date)] Tentando iniciar servidor..." >> "$LOG_FILE"
    
    # Verificar se já está rodando
    if curl -s http://localhost:7937/health > /dev/null 2>&1; then
        echo "[$(date)] Servidor já está rodando" >> "$LOG_FILE"
        return 0
    fi
    
    # Limpar PID antigo
    rm -f "$SCRIPT_DIR/.digimundo.pid"
    
    # Iniciar servidor
    cd "$SCRIPT_DIR"
    /opt/homebrew/opt/node@20/bin/node app/server/index.js >> "$LOG_FILE" 2>&1 &
    SERVER_PID=$!
    
    echo $SERVER_PID > "$SCRIPT_DIR/.digimundo.pid"
    echo "[$(date)] Servidor iniciado com PID: $SERVER_PID" >> "$LOG_FILE"
    
    # Aguardar inicialização
    for i in {1..30}; do
        sleep 1
        if curl -s http://localhost:7937/health > /dev/null 2>&1; then
            echo "[$(date)] ✅ Servidor ONLINE!" >> "$LOG_FILE"
            return 0
        fi
    done
    
    echo "[$(date)] ⚠️ Servidor não respondeu após 30 segundos" >> "$LOG_FILE"
    return 1
}

# Tentar iniciar até 3 vezes
for attempt in {1..3}; do
    echo "[$(date)] Tentativa $attempt de 3..." >> "$LOG_FILE"
    if start_server; then
        echo "[$(date)] ✅ Digimundo iniciado com sucesso!" >> "$LOG_FILE"
        
        # Iniciar monitor
        (
            while true; do
                sleep 60
                if ! curl -s http://localhost:7937/health > /dev/null 2>&1; then
                    echo "[$(date)] Monitor: Servidor caiu, reiniciando..." >> "$LOG_FILE"
                    start_server
                fi
            done
        ) &
        echo $! > "$SCRIPT_DIR/.monitor.pid"
        echo "[$(date)] Monitor iniciado" >> "$LOG_FILE"
        
        exit 0
    fi
    
    # Aguardar antes de tentar novamente
    sleep 10
done

echo "[$(date)] ❌ Falha ao iniciar após 3 tentativas" >> "$LOG_FILE"
exit 1
