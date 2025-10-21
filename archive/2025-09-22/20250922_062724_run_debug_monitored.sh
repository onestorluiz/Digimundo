#!/bin/bash
# 🚀 SCRIPT DE EXECUÇÃO DEBUG MONITORADO
# Executa o sistema em modo debug com monitoramento completo

clear

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║       🚀 SCRIPTUREMON DEBUG - EXECUÇÃO MONITORADA     ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Verificação inicial
echo -e "${YELLOW}📋 FASE 1: VERIFICAÇÃO INICIAL${NC}"
echo "----------------------------------------"

# Verifica se Ollama está rodando
echo -n "Verificando Ollama... "
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Online${NC}"
else
    echo -e "${RED}❌ Offline${NC}"
    echo -e "${YELLOW}Iniciando Ollama...${NC}"
    ollama serve > /tmp/ollama_serve.log 2>&1 &
    sleep 5
fi

# Verifica modelo CPU
echo -n "Verificando modelo mixtral-cpu-force... "
if ollama list | grep -q "mixtral-cpu-force"; then
    echo -e "${GREEN}✅ Disponível${NC}"
else
    echo -e "${RED}❌ Não encontrado${NC}"
    echo "Crie o modelo com: ollama create mixtral-cpu-force -f modelfile_cpu_force"
    exit 1
fi

# 2. Limpeza de processos antigos
echo ""
echo -e "${YELLOW}📋 FASE 2: LIMPEZA${NC}"
echo "----------------------------------------"

# Conta processos existentes
EXISTING=$(ps aux | grep "python.*ollama_" | grep -v grep | wc -l | xargs)
if [ "$EXISTING" -gt "0" ]; then
    echo -e "${YELLOW}Encontrados $EXISTING processos existentes${NC}"
    echo "Deseja limpar? (s/n)"
    read -r CLEAN
    if [ "$CLEAN" = "s" ]; then
        pkill -f "ollama_continuous_learning.py"
        pkill -f "ollama_debug_mode.py"
        echo -e "${GREEN}✅ Processos limpos${NC}"
        sleep 2
    fi
else
    echo -e "${GREEN}✅ Nenhum processo anterior${NC}"
fi

# 3. Criar diretório de debug
echo ""
echo -e "${YELLOW}📋 FASE 3: PREPARAÇÃO${NC}"
echo "----------------------------------------"

mkdir -p debug_output
echo -e "${GREEN}✅ Diretório debug_output criado${NC}"

# Timestamp para logs
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DEBUG_LOG="debug_output/debug_session_${TIMESTAMP}.log"
MONITOR_LOG="debug_output/monitor_${TIMESTAMP}.log"

echo -e "${BLUE}📁 Logs serão salvos em:${NC}"
echo "   - Debug: $DEBUG_LOG"
echo "   - Monitor: $MONITOR_LOG"

# 4. Escolher modo de execução
echo ""
echo -e "${YELLOW}📋 FASE 4: MODO DE EXECUÇÃO${NC}"
echo "----------------------------------------"
echo "Escolha o modo:"
echo "1) Debug completo (teoria + roteiros)"
echo "2) Debug rápido (apenas 2 teorias)"
echo "3) Debug mínimo (1 teoria, 1 roteiro)"
echo "4) Teste de timeout (força espera longa)"
read -r MODE

# Configurar parâmetros baseado no modo
case $MODE in
    1)
        PARAMS=""
        DESCRIPTION="Completo"
        ;;
    2)
        PARAMS="--max-theories 2 --max-scripts 0"
        DESCRIPTION="Rápido (2 teorias)"
        ;;
    3)
        PARAMS="--max-theories 1 --max-scripts 1"
        DESCRIPTION="Mínimo"
        ;;
    4)
        PARAMS="--force-timeout-test"
        DESCRIPTION="Teste de Timeout"
        ;;
    *)
        PARAMS=""
        DESCRIPTION="Padrão"
        ;;
esac

echo -e "${BLUE}Modo selecionado: $DESCRIPTION${NC}"

# 5. Iniciar execução
echo ""
echo -e "${YELLOW}📋 FASE 5: EXECUÇÃO${NC}"
echo "----------------------------------------"

# Função para executar em terminal dividido (se disponível)
run_split_terminal() {
    if command -v tmux &> /dev/null; then
        echo -e "${GREEN}Usando tmux para divisão de tela${NC}"
        
        # Criar sessão tmux
        tmux new-session -d -s scripturemon_debug
        
        # Painel principal - Debug Mode
        tmux send-keys -t scripturemon_debug "python3 ollama_debug_mode.py $PARAMS 2>&1 | tee $DEBUG_LOG" C-m
        
        # Dividir horizontalmente - Monitor Dashboard
        tmux split-window -h -t scripturemon_debug
        tmux send-keys -t scripturemon_debug "chmod +x monitor_dashboard.sh && ./monitor_dashboard.sh 2>&1 | tee $MONITOR_LOG" C-m
        
        # Dividir verticalmente - Tail do log
        tmux split-window -v -t scripturemon_debug
        tmux send-keys -t scripturemon_debug "tail -f $DEBUG_LOG | grep --color=always -E 'CHECKPOINT|ERROR|SUCCESS|WARNING|'" C-m
        
        # Anexar à sessão
        echo ""
        echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
        echo -e "${CYAN}║   ENTRANDO NO MODO DEBUG MONITORADO   ║${NC}"
        echo -e "${CYAN}╚════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${YELLOW}Comandos úteis do tmux:${NC}"
        echo "  • Ctrl+B, setas: Navegar entre painéis"
        echo "  • Ctrl+B, D: Sair sem fechar"
        echo "  • Ctrl+B, X: Fechar painel atual"
        echo ""
        sleep 3
        tmux attach -t scripturemon_debug
        
    else
        echo -e "${YELLOW}tmux não instalado. Executando em modo simples${NC}"
        run_simple_mode
    fi
}

# Função para modo simples
run_simple_mode() {
    echo -e "${YELLOW}Executando em modo simples (sem divisão de tela)${NC}"
    echo ""
    echo "Escolha:"
    echo "1) Executar debug mode com output ao vivo"
    echo "2) Executar debug em background + monitor dashboard"
    read -r SIMPLE_MODE
    
    if [ "$SIMPLE_MODE" = "1" ]; then
        echo -e "${GREEN}Iniciando Debug Mode...${NC}"
        python3 ollama_debug_mode.py $PARAMS 2>&1 | tee $DEBUG_LOG
    else
        echo -e "${GREEN}Iniciando Debug Mode em background...${NC}"
        python3 ollama_debug_mode.py $PARAMS > $DEBUG_LOG 2>&1 &
        DEBUG_PID=$!
        echo "Debug PID: $DEBUG_PID"
        
        sleep 3
        
        echo -e "${GREEN}Iniciando Monitor Dashboard...${NC}"
        chmod +x monitor_dashboard.sh
        ./monitor_dashboard.sh
        
        # Quando sair do monitor, oferece matar o debug
        echo ""
        echo "Deseja parar o debug mode? (s/n)"
        read -r STOP
        if [ "$STOP" = "s" ]; then
            kill $DEBUG_PID 2>/dev/null
            echo -e "${GREEN}Debug mode parado${NC}"
        fi
    fi
}

# 6. Escolher interface
echo ""
echo "Como deseja visualizar?"
echo "1) Terminal dividido (tmux) - RECOMENDADO"
echo "2) Modo simples"
read -r INTERFACE

if [ "$INTERFACE" = "1" ]; then
    run_split_terminal
else
    run_simple_mode
fi

# 7. Relatório final
echo ""
echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║          SESSÃO DEBUG FINALIZADA       ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📊 RELATÓRIO:${NC}"

if [ -f "$DEBUG_LOG" ]; then
    ERRORS=$(grep -c "ERROR\|❌" $DEBUG_LOG 2>/dev/null || echo "0")
    WARNINGS=$(grep -c "WARNING\|⚠️" $DEBUG_LOG 2>/dev/null || echo "0")
    CHECKPOINTS=$(grep -c "CHECKPOINT" $DEBUG_LOG 2>/dev/null || echo "0")
    
    echo "  • Erros encontrados: $ERRORS"
    echo "  • Avisos: $WARNINGS"
    echo "  • Checkpoints: $CHECKPOINTS"
    echo ""
    echo "  • Log completo em: $DEBUG_LOG"
fi

if [ -d "debug_output" ]; then
    RESPONSE_COUNT=$(ls debug_output/response_*.json 2>/dev/null | wc -l | xargs)
    echo "  • Respostas salvas: $RESPONSE_COUNT"
fi

echo ""
echo -e "${GREEN}✅ Debug completo!${NC}"
echo "Verifique os arquivos em debug_output/"