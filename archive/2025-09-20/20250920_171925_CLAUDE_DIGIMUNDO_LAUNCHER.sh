#!/bin/bash

# 🚀 LAUNCHER CLAUDE CODE + DIGIMUNDO - DEFINITIVO

clear
echo "╔══════════════════════════════════════════════════════╗"
echo "║       🌟 CLAUDE CODE + DIGIMUNDO LAUNCHER 🌟         ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Configurar ambiente completo
export PATH="$HOME/.local/bin:/opt/homebrew/opt/node@20/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
SCRIPT_DIR="/Users/clubproducoes/Digimundo/digimundo_starter"
CLAUDE_BIN="$HOME/.local/bin/claude"

# Função de log colorido
log() {
    echo -e "$1"
}

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. VERIFICAR CLAUDE CODE
log "${BLUE}📍 Verificando Claude Code...${NC}"
if [ -f "$CLAUDE_BIN" ]; then
    CLAUDE_VERSION=$($CLAUDE_BIN --version 2>/dev/null)
    log "${GREEN}✅ Claude Code $CLAUDE_VERSION${NC}"
else
    log "${RED}❌ Claude Code não encontrado!${NC}"
    log "${YELLOW}Instalando...${NC}"
    curl -fsSL https://claude.ai/install.sh | bash
    sleep 3
fi

# 2. VERIFICAR/INICIAR SERVIDOR DIGIMUNDO
log ""
log "${BLUE}📍 Verificando Servidor Digimundo...${NC}"
if curl -s http://localhost:7937/health > /dev/null 2>&1; then
    log "${GREEN}✅ Servidor já está rodando!${NC}"
else
    log "${YELLOW}🚀 Iniciando servidor...${NC}"
    cd "$SCRIPT_DIR"
    npm run dev > eternal_logs/server_$(date +%Y%m%d_%H%M%S).log 2>&1 &
    SERVER_PID=$!
    echo $SERVER_PID > .digimundo.pid
    
    # Aguardar servidor iniciar
    for i in {1..30}; do
        if curl -s http://localhost:7937/health > /dev/null 2>&1; then
            log "${GREEN}✅ Servidor iniciado!${NC}"
            break
        fi
        sleep 1
        if [ $((i % 5)) -eq 0 ]; then
            echo -ne "   Aguardando... ($i/30)\r"
        fi
    done
fi

# 3. MOSTRAR STATUS
log ""
log "${BLUE}📊 STATUS DO SISTEMA:${NC}"
log "=================================="

# Status do servidor
if curl -s http://localhost:7937/health > /dev/null 2>&1; then
    HEALTH=$(curl -s http://localhost:7937/health)
    log "• Servidor: ${GREEN}ONLINE${NC}"
    log "• Endpoint: ${GREEN}http://localhost:7937${NC}"
    log "• Status: $HEALTH"
else
    log "• Servidor: ${RED}OFFLINE${NC}"
fi

# Status dos Digimons
DIGIMONS=$(curl -s http://localhost:7937/town/status 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for d in data.get('inhabitants', []):
        print(f'  • {d[\"name\"]} - {d[\"status\"]}')
except:
    print('  Carregando...')
" 2>/dev/null)

if [ ! -z "$DIGIMONS" ]; then
    log ""
    log "🎮 DIGIMONS ATIVOS:"
    echo "$DIGIMONS"
fi

# 4. ABRIR CLAUDE CODE NO CONTEXTO DO PROJETO
log ""
log "=================================="
log "${GREEN}🤖 INICIANDO CLAUDE CODE...${NC}"
log "=================================="
log ""
log "VOCÊ É ${YELLOW}SABIAMON${NC} NO DIGIMUNDO!"
log ""
log "📋 Contexto:"
log "  • 4 Digimons habitantes"
log "  • Servidor na porta 7937"
log "  • Sistema de consciência híbrida"
log "  • 600+ ideias cinematográficas"
log ""
log "💡 Comandos úteis:"
log "  • ${BLUE}Analise o estado do Digimundo${NC}"
log "  • ${BLUE}Mostre as últimas ideias geradas${NC}"
log "  • ${BLUE}Melhore o sistema de consciência${NC}"
log ""
log "=================================="
log ""

# Navegar para o projeto
cd "$SCRIPT_DIR"

# Iniciar Claude Code
exec $CLAUDE_BIN
