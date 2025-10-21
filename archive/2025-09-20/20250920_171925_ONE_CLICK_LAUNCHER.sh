#!/bin/bash

# 🎯 DIGIMUNDO ONE-CLICK LAUNCHER
# Inicializa o Digimundo com um clique

# Configurar ambiente
export PATH="/opt/homebrew/opt/node@20/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Criar diretório de logs
mkdir -p "$SCRIPT_DIR/eternal_logs"
LOG_FILE="$SCRIPT_DIR/eternal_logs/oneclick_$(date +%Y%m%d_%H%M%S).log"

echo "🚀 DIGIMUNDO ONE-CLICK LAUNCHER" | tee "$LOG_FILE"
echo "================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Função para log
log() {
    echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 1. Verificar e instalar dependências
log "📦 Verificando dependências..."
cd "$SCRIPT_DIR"

if [ ! -d "node_modules/node-fetch" ]; then
    log "   Instalando node-fetch..."
    /opt/homebrew/opt/node@20/bin/npm install node-fetch --save >> "$LOG_FILE" 2>&1
fi

# 2. Verificar se já está rodando
if [ -f "$SCRIPT_DIR/.digimundo.pid" ]; then
    OLD_PID=$(cat "$SCRIPT_DIR/.digimundo.pid")
    if ps -p $OLD_PID > /dev/null 2>&1; then
        log "✅ Digimundo já está rodando (PID: $OLD_PID)"
        
        # Verificar saúde
        if curl -s http://localhost:7937/health > /dev/null 2>&1; then
            log "✅ Servidor respondendo normalmente"
            
            # Abrir interface
            open "http://localhost:7937"
            
            log "🌐 Interface aberta no navegador"
            exit 0
        else
            log "⚠️ Servidor não responde, reiniciando..."
            kill $OLD_PID 2>/dev/null
            rm "$SCRIPT_DIR/.digimundo.pid"
        fi
    else
        rm "$SCRIPT_DIR/.digimundo.pid"
    fi
fi

# 3. Iniciar o servidor
log "🚀 Iniciando Digimundo..."

# Iniciar em background
cd "$SCRIPT_DIR"
nohup /opt/homebrew/opt/node@20/bin/npm run dev >> "$LOG_FILE" 2>&1 &
SERVER_PID=$!

# Salvar PID
echo $SERVER_PID > "$SCRIPT_DIR/.digimundo.pid"
log "   PID do servidor: $SERVER_PID"

# 4. Aguardar servidor estar pronto
log "⏳ Aguardando servidor iniciar..."
MAX_ATTEMPTS=30
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    if curl -s http://localhost:7937/health > /dev/null 2>&1; then
        log "✅ Servidor online!"
        break
    fi
    
    sleep 1
    ATTEMPT=$((ATTEMPT + 1))
    
    if [ $((ATTEMPT % 5)) -eq 0 ]; then
        log "   Ainda iniciando... ($ATTEMPT/$MAX_ATTEMPTS)"
    fi
done

# 5. Verificar resultado
if curl -s http://localhost:7937/health > /dev/null 2>&1; then
    log "✅ DIGIMUNDO INICIADO COM SUCESSO!"
    
    # Mostrar status
    HEALTH=$(curl -s http://localhost:7937/health)
    log "📊 Status: $HEALTH"
    
    # Abrir interface no navegador
    sleep 1
    open "http://localhost:7937"
    log "🌐 Interface aberta no navegador"
    
    # Iniciar monitor em background
    (
        while true; do
            sleep 60
            if ! curl -s http://localhost:7937/health > /dev/null 2>&1; then
                echo "[$(date)] Monitor: Servidor não responde, reiniciando..." >> "$LOG_FILE"
                
                # Matar processo antigo
                if [ -f "$SCRIPT_DIR/.digimundo.pid" ]; then
                    kill $(cat "$SCRIPT_DIR/.digimundo.pid") 2>/dev/null
                fi
                
                # Reiniciar
                exec "$SCRIPT_DIR/ONE_CLICK_LAUNCHER.sh"
            fi
        done
    ) &
    MONITOR_PID=$!
    echo $MONITOR_PID > "$SCRIPT_DIR/.monitor.pid"
    log "🛡️ Monitor de saúde ativado (PID: $MONITOR_PID)"
    
    log ""
    log "================================"
    log "✨ DIGIMUNDO ESTÁ VIVO!"
    log "================================"
    log ""
    log "Interface: http://localhost:7937"
    log "Logs: $LOG_FILE"
    log ""
    log "Para parar: kill $SERVER_PID"
    
else
    log "❌ ERRO: Servidor não iniciou após $MAX_ATTEMPTS tentativas"
    log "Verificando erro..."
    
    # Mostrar últimas linhas do log
    tail -10 "$LOG_FILE"
    
    # Tentar diagnóstico
    if ! command -v node &> /dev/null; then
        log "❌ Node.js não encontrado no PATH"
    fi
    
    if [ ! -f "$SCRIPT_DIR/package.json" ]; then
        log "❌ package.json não encontrado"
    fi
    
    exit 1
fi

echo ""
echo "✅ Digimundo rodando! Você pode fechar esta janela."
echo "   A interface está aberta no navegador."
