#!/bin/bash
# 📊 DASHBOARD DE MONITORAMENTO AO VIVO - SCRIPTUREMON DEBUG MODE
# Para uso com ollama_debug_mode.py

clear

# Cores para terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuração
INTERVAL=2  # Atualizar a cada 2 segundos
LOG_FILE="debug_*.log"  # Log mais recente
OLLAMA_PORT=11434

# Função para obter CPU do Ollama
get_ollama_cpu() {
    ps aux | grep "ollama.*runner" | grep -v grep | awk '{print $3}' | head -1
}

# Função para obter PID do Ollama
get_ollama_pid() {
    ps aux | grep "ollama.*runner" | grep -v grep | awk '{print $2}' | head -1
}

# Função para obter uso de memória
get_memory() {
    vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//'
}

# Função para obter processos Python
get_python_processes() {
    ps aux | grep "python.*ollama_" | grep -v grep | wc -l | xargs
}

# Função para verificar status Ollama
check_ollama_status() {
    curl -s -o /dev/null -w "%{http_code}" http://localhost:$OLLAMA_PORT/api/tags
}

# Função para obter último checkpoint
get_last_checkpoint() {
    if [ -f "$(ls -t debug_*.log 2>/dev/null | head -1)" ]; then
        tail -100 "$(ls -t debug_*.log | head -1)" | grep "CHECKPOINT" | tail -1 | cut -d'#' -f2 | cut -d' ' -f1
    else
        echo "N/A"
    fi
}

# Função para desenhar barra de progresso
draw_progress_bar() {
    local percent=$1
    local width=30
    local filled=$((percent * width / 100))
    
    printf "["
    for ((i=0; i<filled; i++)); do
        printf "#"
    done
    for ((i=filled; i<width; i++)); do
        printf " "
    done
    printf "] %3d%%" "$percent"
}

# Loop principal
echo -e "${CYAN}=========================================="
echo -e "📊 DASHBOARD DE MONITORAMENTO - DEBUG MODE"
echo -e "==========================================${NC}"
echo ""
echo -e "${YELLOW}Pressione CTRL+C para sair${NC}"
echo ""

START_TIME=$(date +%s)

while true; do
    clear
    
    # Cabeçalho
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗"
    echo -e "║         📊 SCRIPTUREMON DEBUG - MONITORAMENTO AO VIVO      ║"
    echo -e "╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Tempo decorrido
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    ELAPSED_MIN=$((ELAPSED / 60))
    ELAPSED_SEC=$((ELAPSED % 60))
    
    echo -e "⏱️  ${BLUE}Tempo Decorrido:${NC} ${ELAPSED_MIN}m ${ELAPSED_SEC}s"
    echo -e "🕐 ${BLUE}Timestamp:${NC} $(date '+%H:%M:%S')"
    echo ""
    
    # Status do Ollama
    echo -e "${CYAN}═══ STATUS DO OLLAMA ═══${NC}"
    OLLAMA_STATUS=$(check_ollama_status)
    if [ "$OLLAMA_STATUS" = "200" ]; then
        echo -e "🟢 ${GREEN}API Status: ONLINE${NC}"
    else
        echo -e "🔴 ${RED}API Status: OFFLINE (Code: $OLLAMA_STATUS)${NC}"
    fi
    
    # CPU do Ollama
    CPU_USAGE=$(get_ollama_cpu)
    if [ -z "$CPU_USAGE" ]; then
        CPU_USAGE="0"
    fi
    
    # Converter vírgula para ponto se necessário
    CPU_USAGE_INT=$(echo "$CPU_USAGE" | sed 's/,/./g' | cut -d'.' -f1)
    
    # Cor baseada no uso
    if [ "$CPU_USAGE_INT" -gt "100" ]; then
        CPU_COLOR=$GREEN
        CPU_EMOJI="🔥"
    elif [ "$CPU_USAGE_INT" -gt "50" ]; then
        CPU_COLOR=$YELLOW
        CPU_EMOJI="⚡"
    else
        CPU_COLOR=$RED
        CPU_EMOJI="💤"
    fi
    
    echo -e "$CPU_EMOJI ${BLUE}CPU Usage:${NC} ${CPU_COLOR}${CPU_USAGE}%${NC}"
    
    # Barra de progresso para CPU
    if [ "$CPU_USAGE_INT" -gt "0" ]; then
        PROGRESS=$((CPU_USAGE_INT > 100 ? 100 : CPU_USAGE_INT))
        echo -n "   "
        draw_progress_bar $PROGRESS
        echo ""
    fi
    
    # PID do Ollama
    OLLAMA_PID=$(get_ollama_pid)
    if [ -n "$OLLAMA_PID" ]; then
        echo -e "🔧 ${BLUE}PID Ollama:${NC} $OLLAMA_PID"
    fi
    echo ""
    
    # Processos Python
    echo -e "${CYAN}═══ PROCESSOS EM EXECUÇÃO ═══${NC}"
    PYTHON_COUNT=$(get_python_processes)
    echo -e "🐍 ${BLUE}Processos Python:${NC} $PYTHON_COUNT"
    
    # Lista processos ativos
    if [ "$PYTHON_COUNT" -gt "0" ]; then
        echo -e "${BLUE}Detalhes:${NC}"
        ps aux | grep "python.*ollama_" | grep -v grep | awk '{printf "   PID %5s | CPU %5s%% | %s\n", $2, $3, $11}' | head -5
    fi
    echo ""
    
    # Memória
    echo -e "${CYAN}═══ RECURSOS DO SISTEMA ═══${NC}"
    MEM_FREE=$(get_memory)
    MEM_FREE_GB=$(echo "scale=1; ($MEM_FREE * 4096) / (1024*1024*1024)" | bc 2>/dev/null || echo "N/A")
    echo -e "💾 ${BLUE}Memória Livre:${NC} ${MEM_FREE_GB}GB"
    
    # Checkpoints
    echo ""
    echo -e "${CYAN}═══ ÚLTIMO CHECKPOINT ═══${NC}"
    LAST_CP=$(get_last_checkpoint)
    echo -e "🏁 ${BLUE}Checkpoint:${NC} #$LAST_CP"
    
    # Últimas linhas do log
    echo ""
    echo -e "${CYAN}═══ LOG AO VIVO (últimas 5 linhas) ═══${NC}"
    if [ -f "$(ls -t debug_*.log 2>/dev/null | head -1)" ]; then
        tail -5 "$(ls -t debug_*.log | head -1)" | while IFS= read -r line; do
            # Colorir baseado no conteúdo
            if echo "$line" | grep -q "ERROR\|❌"; then
                echo -e "${RED}$line${NC}"
            elif echo "$line" | grep -q "SUCCESS\|✅"; then
                echo -e "${GREEN}$line${NC}"
            elif echo "$line" | grep -q "WARNING\|⚠️"; then
                echo -e "${YELLOW}$line${NC}"
            else
                echo "$line"
            fi
        done
    else
        echo "Aguardando logs..."
    fi
    
    # Rodapé
    echo ""
    echo -e "${CYAN}══════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Atualizando a cada ${INTERVAL}s | CTRL+C para sair${NC}"
    
    sleep $INTERVAL
done