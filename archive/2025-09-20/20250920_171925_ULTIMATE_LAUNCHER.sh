#!/bin/bash

# 🚀 DIGIMUNDO ULTIMATE LAUNCHER - COM CLAUDE CODE
# Inicia TUDO com um clique e mantém rodando

# Configuração de cores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configurar ambiente
export PATH="/opt/homebrew/opt/node@20/bin:/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Banner inicial
clear
echo -e "${BLUE}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        🌟 DIGIMUNDO + CLAUDE CODE LAUNCHER 🌟        ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

# Criar diretórios necessários
mkdir -p "$SCRIPT_DIR/eternal_logs"
LOG_FILE="$SCRIPT_DIR/eternal_logs/ultimate_$(date +%Y%m%d_%H%M%S).log"

# Função de log
log() {
    echo -e "$1"
    echo "[$(date '+%H:%M:%S')] $1" >> "$LOG_FILE"
}

# 1. MATAR PROCESSOS ANTIGOS
log "${YELLOW}🔄 Limpando processos antigos...${NC}"
if [ -f "$SCRIPT_DIR/.digimundo.pid" ]; then
    OLD_PID=$(cat "$SCRIPT_DIR/.digimundo.pid")
    if ps -p $OLD_PID > /dev/null 2>&1; then
        kill $OLD_PID 2>/dev/null
        log "   Processo anterior terminado (PID: $OLD_PID)"
    fi
    rm "$SCRIPT_DIR/.digimundo.pid"
fi

# 2. VERIFICAR NODE.JS
log "${YELLOW}📦 Verificando Node.js...${NC}"
NODE_PATH="/opt/homebrew/opt/node@20/bin/node"
if [ -f "$NODE_PATH" ]; then
    NODE_VERSION=$($NODE_PATH --version)
    log "${GREEN}   ✅ Node.js $NODE_VERSION encontrado${NC}"
else
    log "${RED}   ❌ Node.js não encontrado!${NC}"
    exit 1
fi

# 3. INSTALAR DEPENDÊNCIAS SE NECESSÁRIO
cd "$SCRIPT_DIR"
if [ ! -d "node_modules" ]; then
    log "${YELLOW}📦 Instalando dependências...${NC}"
    /opt/homebrew/opt/node@20/bin/npm install >> "$LOG_FILE" 2>&1
    log "${GREEN}   ✅ Dependências instaladas${NC}"
fi

# 4. INICIAR SERVIDOR DIGIMUNDO
log "${YELLOW}🚀 Iniciando servidor Digimundo...${NC}"
cd "$SCRIPT_DIR"

# Usar nohup para manter rodando
nohup /opt/homebrew/opt/node@20/bin/node app/server/index.js >> "$LOG_FILE" 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > "$SCRIPT_DIR/.digimundo.pid"
log "${GREEN}   ✅ Servidor iniciado (PID: $SERVER_PID)${NC}"

# 5. AGUARDAR SERVIDOR ESTAR PRONTO
log "${YELLOW}⏳ Aguardando servidor ficar online...${NC}"
MAX_ATTEMPTS=30
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    if curl -s http://localhost:7937/health > /dev/null 2>&1; then
        log "${GREEN}   ✅ Servidor ONLINE!${NC}"
        break
    fi
    sleep 1
    ATTEMPT=$((ATTEMPT + 1))
    if [ $((ATTEMPT % 5)) -eq 0 ]; then
        echo -ne "   Tentativa $ATTEMPT/$MAX_ATTEMPTS...\r"
    fi
done

# 6. VERIFICAR STATUS
if curl -s http://localhost:7937/health > /dev/null 2>&1; then
    HEALTH=$(curl -s http://localhost:7937/health)
    log "${GREEN}✅ DIGIMUNDO INICIADO COM SUCESSO!${NC}"
    log "   Status: $HEALTH"
else
    log "${RED}❌ Erro ao iniciar servidor${NC}"
    tail -10 "$LOG_FILE"
    exit 1
fi

# 7. INICIAR CLAUDE CODE
log "${YELLOW}🤖 Iniciando Claude Code...${NC}"
CLAUDE_PATH="$HOME/.local/bin/claude"
if [ -f "$CLAUDE_PATH" ]; then
    log "${GREEN}   ✅ Claude Code encontrado${NC}"
    
    # Abrir Claude em nova aba do Terminal com PATH correto
    osascript -e "
    tell application \"Terminal\"
        activate
        do script \"export PATH=\\\"$HOME/.local/bin:/opt/homebrew/opt/node@20/bin:/opt/homebrew/bin:/usr/local/bin:\\\$PATH\\\" && cd '$SCRIPT_DIR' && clear && echo '🤖 CLAUDE CODE - PROJETO DIGIMUNDO' && echo '' && echo 'Você é Sabiamon no Digimundo!' && echo 'Servidor rodando na porta 7937' && echo '' && $CLAUDE_PATH\"
    end tell
    " > /dev/null 2>&1
    
    log "${GREEN}   ✅ Claude Code aberto em nova aba${NC}"
else
    log "${YELLOW}   ⚠️ Claude Code não encontrado${NC}"
fi

# 8. ABRIR INTERFACE WEB
sleep 2
log "${YELLOW}🌐 Abrindo interface web...${NC}"
open "http://localhost:7937"
log "${GREEN}   ✅ Interface aberta no navegador${NC}"

# 9. INICIAR MONITOR DE SAÚDE
log "${YELLOW}🛡️ Iniciando monitor de saúde...${NC}"
(
    while true; do
        sleep 60
        if ! curl -s http://localhost:7937/health > /dev/null 2>&1; then
            echo "[$(date)] Monitor: Servidor caiu, reiniciando..." >> "$LOG_FILE"
            
            # Reiniciar servidor
            cd "$SCRIPT_DIR"
            nohup /opt/homebrew/opt/node@20/bin/node app/server/index.js >> "$LOG_FILE" 2>&1 &
            echo $! > "$SCRIPT_DIR/.digimundo.pid"
        fi
    done
) &
MONITOR_PID=$!
echo $MONITOR_PID > "$SCRIPT_DIR/.monitor.pid"
log "${GREEN}   ✅ Monitor ativado (PID: $MONITOR_PID)${NC}"

# 10. MOSTRAR STATUS FINAL
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           ✨ TUDO PRONTO E FUNCIONANDO! ✨           ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📊 STATUS DOS SISTEMAS:${NC}"
echo -e "   • Servidor Digimundo: ${GREEN}ONLINE${NC} (PID: $SERVER_PID)"
echo -e "   • Claude Code: ${GREEN}ABERTO${NC}"
echo -e "   • Interface Web: ${GREEN}http://localhost:7937${NC}"
echo -e "   • Monitor de Saúde: ${GREEN}ATIVO${NC}"
echo ""
echo -e "${BLUE}📁 ARQUIVOS:${NC}"
echo -e "   • Logs: $LOG_FILE"
echo -e "   • PIDs: .digimundo.pid, .monitor.pid"
echo ""
echo -e "${BLUE}🎮 COMANDOS ÚTEIS:${NC}"
echo -e "   • Status: ${YELLOW}curl http://localhost:7937/health${NC}"
echo -e "   • Parar: ${YELLOW}kill $SERVER_PID${NC}"
echo -e "   • Logs: ${YELLOW}tail -f $LOG_FILE${NC}"
echo ""
echo -e "${GREEN}✨ Digimundo está vivo e Claude Code está pronto!${NC}"
echo -e "${GREEN}   Você pode fechar esta janela. O sistema continuará rodando.${NC}"
echo ""

# Salvar informações do processo
cat > "$SCRIPT_DIR/.launch_info.json" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "server_pid": $SERVER_PID,
  "monitor_pid": $MONITOR_PID,
  "log_file": "$LOG_FILE",
  "status": "running",
  "url": "http://localhost:7937"
}
EOF

exit 0
