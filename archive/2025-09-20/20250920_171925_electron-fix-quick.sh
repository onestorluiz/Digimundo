#!/bin/bash

# ============================================
# ELECTRON QUICK FIX - Execute de qualquer lugar!
# ============================================

# Cores para o terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# CAMINHO ABSOLUTO DO PROJETO (SEMPRE FUNCIONARÁ!)
PROJECT_DIR="/Users/clubproducoes/Digimundo/digimundo_starter"

echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   ELECTRON AUTO-FIX - EXECUÇÃO RÁPIDA    ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
echo ""

# Verificar se o diretório existe
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ ERRO: Diretório do projeto não encontrado!${NC}"
    echo -e "${RED}   Esperado: $PROJECT_DIR${NC}"
    exit 1
fi

# Mudar para o diretório do projeto
echo -e "${YELLOW}📁 Navegando para: $PROJECT_DIR${NC}"
cd "$PROJECT_DIR" || {
    echo -e "${RED}❌ Não foi possível acessar o diretório!${NC}"
    exit 1
}

# Verificar arquivos essenciais
echo -e "${YELLOW}🔍 Verificando arquivos essenciais...${NC}"

if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ package.json não encontrado!${NC}"
    exit 1
fi

if [ ! -f "electron-autofix.js" ]; then
    echo -e "${RED}❌ electron-autofix.js não encontrado!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Todos os arquivos encontrados!${NC}"
echo ""

# Executar com a opção escolhida
if [ "$1" == "--diagnose" ]; then
    echo -e "${BLUE}🔍 Executando apenas diagnóstico...${NC}"
    node electron-autofix.js --diagnose-only
    
elif [ "$1" == "--fix" ]; then
    echo -e "${BLUE}🔧 Executando diagnóstico e correções...${NC}"
    node electron-autofix.js --fix-only
    
elif [ "$1" == "--monitor" ]; then
    echo -e "${BLUE}📊 Iniciando monitor contínuo...${NC}"
    echo -e "${YELLOW}Pressione Ctrl+C para parar${NC}"
    node electron-autofix.js
    
elif [ "$1" == "--normal" ]; then
    echo -e "${BLUE}🚀 Iniciando Electron normal...${NC}"
    npm run dev
    
elif [ "$1" == "--clean" ]; then
    echo -e "${BLUE}🗑️  Limpando cache e logs...${NC}"
    rm -rf electron-logs/
    rm -rf node_modules/.cache/
    rm -rf ~/.electron/
    npm cache clean --force
    echo -e "${GREEN}✅ Limpeza concluída!${NC}"
    
elif [ "$1" == "--report" ]; then
    if [ -f "electron-logs/report.json" ]; then
        echo -e "${BLUE}📋 Último relatório:${NC}"
        cat electron-logs/report.json | python3 -m json.tool
    else
        echo -e "${RED}❌ Nenhum relatório encontrado${NC}"
    fi
    
elif [ "$1" == "--help" ] || [ -z "$1" ]; then
    echo "Uso: $0 [opção]"
    echo ""
    echo "Opções disponíveis:"
    echo "  --diagnose   🔍 Executar apenas diagnóstico"
    echo "  --fix        🔧 Diagnóstico + Correções automáticas"
    echo "  --monitor    📊 Sistema completo com monitor (padrão)"
    echo "  --normal     🚀 Iniciar Electron sem monitor"
    echo "  --clean      🗑️  Limpar cache e logs"
    echo "  --report     📋 Ver último relatório"
    echo "  --help       ❓ Mostrar esta ajuda"
    echo ""
    echo "Exemplo:"
    echo "  $0 --monitor"
    echo ""
    echo "Ou execute sem parâmetros para o menu interativo:"
    echo "  ./run-electron-fix.sh"
    
else
    echo -e "${RED}❌ Opção inválida: $1${NC}"
    echo "Use --help para ver as opções disponíveis"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Operação concluída!${NC}"
echo -e "${BLUE}📁 Executado em: $PROJECT_DIR${NC}"