#!/bin/bash

# 🌟 DIGIMUNDO ETERNAL - Sistema de Evolução Perpétua
# Este script mantém o Digimundo rodando eternamente

echo "
╔══════════════════════════════════════════════════════════╗
║       🌟 DIGIMUNDO ETERNAL - EVOLUÇÃO PERPÉTUA 🌟        ║
╚══════════════════════════════════════════════════════════╝
"

# Configurações
DIGIMUNDO_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$DIGIMUNDO_DIR/eternal_logs"
PID_FILE="$DIGIMUNDO_DIR/.digimundo.pid"
EVOLUTION_LOG="$LOG_DIR/evolution_$(date +%Y%m%d).log"
CRASH_LOG="$LOG_DIR/crashes.log"

# Criar diretório de logs se não existir
mkdir -p "$LOG_DIR"

# Função para verificar se o servidor está rodando
check_server() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            return 0
        fi
    fi
    return 1
}

# Função para iniciar o servidor
start_server() {
    echo "[$(date)] 🚀 Iniciando Digimundo..." | tee -a "$EVOLUTION_LOG"
    
    cd "$DIGIMUNDO_DIR"
    
    # Iniciar npm run dev em background com nohup para persistir
    nohup npm run dev >> "$EVOLUTION_LOG" 2>&1 &
    SERVER_PID=$!
    
    echo $SERVER_PID > "$PID_FILE"
    
    echo "[$(date)] ✅ Servidor iniciado com PID: $SERVER_PID" | tee -a "$EVOLUTION_LOG"
    
    # Aguardar servidor estar pronto
    sleep 5
    
    # Verificar se está respondendo
    if curl -s http://localhost:7937/health > /dev/null; then
        echo "[$(date)] 🌍 Digimundo está VIVO!" | tee -a "$EVOLUTION_LOG"
        return 0
    else
        echo "[$(date)] ⚠️ Servidor iniciou mas não está respondendo" | tee -a "$EVOLUTION_LOG"
        return 1
    fi
}

# Função para parar o servidor
stop_server() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        echo "[$(date)] 🛑 Parando Digimundo (PID: $PID)..." | tee -a "$EVOLUTION_LOG"
        kill $PID 2>/dev/null
        rm "$PID_FILE"
        sleep 2
    fi
}

# Função para reiniciar o servidor
restart_server() {
    echo "[$(date)] 🔄 Reiniciando Digimundo..." | tee -a "$EVOLUTION_LOG"
    stop_server
    start_server
}

# Função para monitorar saúde do sistema
monitor_health() {
    while true; do
        sleep 30
        
        # Verificar se servidor está respondendo
        if ! curl -s http://localhost:7937/health > /dev/null; then
            echo "[$(date)] ⚠️ Servidor não responde! Reiniciando..." | tee -a "$CRASH_LOG"
            restart_server
        else
            # Capturar status do ecossistema
            ECOSYSTEM_STATUS=$(curl -s http://localhost:7937/ecosystem/status 2>/dev/null)
            if [ ! -z "$ECOSYSTEM_STATUS" ]; then
                echo "[$(date)] 📊 Status: $ECOSYSTEM_STATUS" >> "$EVOLUTION_LOG"
            fi
            
            # Capturar status do Quantum Brain
            QUANTUM_STATUS=$(curl -s http://localhost:7937/quantum/status 2>/dev/null | jq -r '.resourceUsage.cpu' 2>/dev/null)
            if [ ! -z "$QUANTUM_STATUS" ]; then
                echo "[$(date)] ⚡ CPU Quantum: $QUANTUM_STATUS" >> "$EVOLUTION_LOG"
            fi
        fi
    done
}

# Função para evolução automática
auto_evolution() {
    while true; do
        sleep 300 # A cada 5 minutos
        
        echo "[$(date)] 🧬 Triggering evolution cycle..." >> "$EVOLUTION_LOG"
        
        # Gerar ideias automaticamente
        curl -X POST http://localhost:7937/quantum/generate-ideas \
            -H "Content-Type: application/json" \
            -d '{"theme": "evolução digital", "count": 3}' \
            >> "$EVOLUTION_LOG" 2>&1
        
        # Provocar interação entre Digimons aleatórios
        DIGIMONS=("Debugmon" "Reasonmon" "Creativemon" "Patternmon" "Memomon" "Synthemon" "Evolvemon")
        D1=${DIGIMONS[$RANDOM % ${#DIGIMONS[@]}]}
        D2=${DIGIMONS[$RANDOM % ${#DIGIMONS[@]}]}
        
        if [ "$D1" != "$D2" ]; then
            echo "[$(date)] 🤝 Interação: $D1 + $D2" >> "$EVOLUTION_LOG"
            curl -X POST http://localhost:7937/ecosystem/interact \
                -H "Content-Type: application/json" \
                -d "{\"digimon1\": \"$D1\", \"digimon2\": \"$D2\", \"task\": \"evoluir juntos\"}" \
                >> "$EVOLUTION_LOG" 2>&1
        fi
    done
}

# Função principal
main() {
    case "$1" in
        start)
            if check_server; then
                echo "⚠️ Digimundo já está rodando!"
            else
                start_server
                if [ $? -eq 0 ]; then
                    echo "
✅ Digimundo está em evolução perpétua!
📊 Logs em: $LOG_DIR
🔍 Status: curl http://localhost:7937/ecosystem/status

Para parar: $0 stop
Para ver logs: tail -f $EVOLUTION_LOG
                    "
                    
                    # Iniciar monitores em background
                    monitor_health &
                    MONITOR_PID=$!
                    echo $MONITOR_PID > "$DIGIMUNDO_DIR/.monitor.pid"
                    
                    auto_evolution &
                    EVOLUTION_PID=$!
                    echo $EVOLUTION_PID > "$DIGIMUNDO_DIR/.evolution.pid"
                    
                    echo "🌟 Sistemas de monitoramento e evolução ativados!"
                fi
            fi
            ;;
            
        stop)
            echo "🛑 Parando todos os sistemas..."
            
            # Parar monitores
            if [ -f "$DIGIMUNDO_DIR/.monitor.pid" ]; then
                kill $(cat "$DIGIMUNDO_DIR/.monitor.pid") 2>/dev/null
                rm "$DIGIMUNDO_DIR/.monitor.pid"
            fi
            
            if [ -f "$DIGIMUNDO_DIR/.evolution.pid" ]; then
                kill $(cat "$DIGIMUNDO_DIR/.evolution.pid") 2>/dev/null
                rm "$DIGIMUNDO_DIR/.evolution.pid"
            fi
            
            stop_server
            echo "✅ Digimundo parado"
            ;;
            
        restart)
            restart_server
            ;;
            
        status)
            if check_server; then
                echo "✅ Digimundo está VIVO!"
                echo ""
                echo "📊 Status do Ecossistema:"
                curl -s http://localhost:7937/ecosystem/status | python3 -m json.tool
                echo ""
                echo "⚡ Status do Quantum Brain:"
                curl -s http://localhost:7937/quantum/status | jq '.resourceUsage'
            else
                echo "❌ Digimundo não está rodando"
            fi
            ;;
            
        logs)
            tail -f "$EVOLUTION_LOG"
            ;;
            
        eternal)
            # Modo eternal - mantém rodando para sempre
            echo "🌟 MODO ETERNAL ATIVADO - Digimundo nunca morrerá!"
            
            # Iniciar servidor
            if ! check_server; then
                start_server
            fi
            
            # Loop eterno verificando saúde
            while true; do
                if ! check_server; then
                    echo "[$(date)] 💀 Servidor morreu! Ressuscitando..." | tee -a "$CRASH_LOG"
                    start_server
                fi
                
                # Verificar saúde via HTTP
                if ! curl -s http://localhost:7937/health > /dev/null; then
                    echo "[$(date)] 🔥 Servidor travado! Reiniciando..." | tee -a "$CRASH_LOG"
                    restart_server
                fi
                
                sleep 10
            done
            ;;
            
        *)
            echo "Uso: $0 {start|stop|restart|status|logs|eternal}"
            echo ""
            echo "Comandos:"
            echo "  start   - Inicia o Digimundo em background"
            echo "  stop    - Para o Digimundo"
            echo "  restart - Reinicia o Digimundo"
            echo "  status  - Mostra status atual"
            echo "  logs    - Mostra logs em tempo real"
            echo "  eternal - Modo eternal (nunca para, auto-reinicia)"
            exit 1
            ;;
    esac
}

# Executar função principal
main "$@"