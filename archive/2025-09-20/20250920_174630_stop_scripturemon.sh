#!/bin/bash
# 🛑 Script de Parada do Scripturemon

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretório base
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         🛑 SCRIPTUREMON SYSTEM SHUTDOWN                   ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar se está rodando
if [ ! -f "$BASE_DIR/data/scripturemon.pid" ]; then
    echo -e "${YELLOW}⚠️ Sistema não está rodando${NC}"
    exit 0
fi

PID=$(cat "$BASE_DIR/data/scripturemon.pid")

if ! ps -p $PID > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️ Processo não encontrado (PID: $PID)${NC}"
    echo -e "${YELLOW}Limpando arquivos antigos...${NC}"
    rm -f "$BASE_DIR/data/scripturemon.pid"
    exit 0
fi

echo -e "${YELLOW}🛑 Parando sistema (PID: $PID)...${NC}"

# Enviar SIGTERM
kill -TERM $PID 2>/dev/null || true

# Aguardar até 10 segundos
COUNTER=0
while [ $COUNTER -lt 10 ]; do
    if ! ps -p $PID > /dev/null 2>&1; then
        break
    fi
    echo -n "."
    sleep 1
    COUNTER=$((COUNTER + 1))
done
echo ""

# Se ainda estiver rodando, forçar
if ps -p $PID > /dev/null 2>&1; then
    echo -e "${YELLOW}Forçando parada...${NC}"
    kill -9 $PID 2>/dev/null || true
    sleep 1
fi

# Limpar arquivo PID
rm -f "$BASE_DIR/data/scripturemon.pid"

echo -e "${GREEN}✅ Sistema parado com sucesso!${NC}"
echo ""
echo -e "${BLUE}📊 Estatísticas finais salvas em:${NC}"
echo -e "  $BASE_DIR/data/system_state.json"
echo ""
echo -e "${YELLOW}Para reiniciar, use:${NC}"
echo -e "  ${GREEN}$BASE_DIR/scripts/start_scripturemon.sh${NC}"