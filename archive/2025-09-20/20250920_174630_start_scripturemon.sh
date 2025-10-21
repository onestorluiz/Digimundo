#!/bin/bash
# 🚀 Script de Inicialização do Scripturemon
# NÃO executa automaticamente no boot do Mac
# Deve ser executado manualmente quando quiser usar o sistema

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
echo -e "${BLUE}║         🎮 SCRIPTUREMON SYSTEM STARTUP                    ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar se já está rodando
if [ -f "$BASE_DIR/data/scripturemon.pid" ]; then
    PID=$(cat "$BASE_DIR/data/scripturemon.pid")
    if ps -p $PID > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️ Sistema já está rodando (PID: $PID)${NC}"
        echo -e "Use ${GREEN}$BASE_DIR/scripts/stop_scripturemon.sh${NC} para parar"
        exit 1
    else
        echo -e "${YELLOW}Removendo PID antigo...${NC}"
        rm -f "$BASE_DIR/data/scripturemon.pid"
    fi
fi

# Verificar Python
echo -e "${BLUE}🔍 Verificando dependências...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 não encontrado!${NC}"
    exit 1
fi

# Verificar Ollama
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}⚠️ Ollama não encontrado. Algumas funcionalidades estarão limitadas.${NC}"
else
    echo -e "${GREEN}✅ Ollama disponível${NC}"

    # Verificar se Ollama está rodando
    if ! pgrep -x "ollama" > /dev/null; then
        echo -e "${YELLOW}Iniciando Ollama...${NC}"
        ollama serve > /dev/null 2>&1 &
        sleep 2
    fi
fi

# Criar diretórios necessários
echo -e "${BLUE}📁 Criando estrutura de diretórios...${NC}"
mkdir -p "$BASE_DIR/data"
mkdir -p "$BASE_DIR/logs"
mkdir -p "$BASE_DIR/library/processed"
mkdir -p "$BASE_DIR/output"

# Iniciar sistema principal
echo -e "${BLUE}🚀 Iniciando Scripturemon System Manager...${NC}"
cd "$BASE_DIR"
export PYTHONPATH="$BASE_DIR"

# Iniciar em background com nohup
nohup python3 -m apps.scripturemon.system_manager start > "$BASE_DIR/logs/system_manager.log" 2>&1 &
MANAGER_PID=$!

# Aguardar inicialização
sleep 3

# Verificar se iniciou corretamente
if ps -p $MANAGER_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Sistema iniciado com sucesso!${NC}"
    echo ""
    echo -e "${BLUE}📦 Subsistemas ativos:${NC}"
    echo -e "  • Crystal Memory (Rules & Screenplay)"
    echo -e "  • RAG System (Retrieval Augmented Generation)"
    echo -e "  • Ollama Monitor"
    echo -e "  • File Watcher"
    echo ""
    echo -e "${YELLOW}📋 Comandos disponíveis:${NC}"
    echo -e "  ${GREEN}scripturemon status${NC} - Ver status do sistema"
    echo -e "  ${GREEN}scripturemon rag \"pergunta\"${NC} - Consultar roteiros"
    echo -e "  ${GREEN}scripturemon analyze arquivo.pdf${NC} - Analisar roteiro"
    echo -e "  ${GREEN}scripturemon stop-system${NC} - Parar o sistema"
    echo ""
    echo -e "${BLUE}📝 Logs em: $BASE_DIR/logs/${NC}"
    echo -e "${BLUE}🔗 PID: $MANAGER_PID${NC}"
else
    echo -e "${RED}❌ Falha ao iniciar o sistema!${NC}"
    echo -e "Verifique os logs em: $BASE_DIR/logs/system_manager.log"
    exit 1
fi