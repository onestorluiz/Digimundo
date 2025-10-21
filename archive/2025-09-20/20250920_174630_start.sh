#!/bin/bash
# 🚀 SCRIPTUREMON CHAMPION - INICIALIZAÇÃO SIMPLES
# Script otimizado para inicialização rápida e funcional

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🎮 SCRIPTUREMON CHAMPION                   ║"
echo "║                     Sistema de Inicialização                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Diretório base
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$SCRIPT_DIR"

echo -e "${BLUE}📂 Diretório: ${BASE_DIR}${NC}"
echo ""

# Verificar se está no diretório correto
if [ ! -f "$BASE_DIR/bin/scripturemon" ]; then
    echo -e "${RED}❌ Erro: bin/scripturemon não encontrado!${NC}"
    echo -e "${YELLOW}   Certifique-se de estar no diretório correto${NC}"
    exit 1
fi

# Verificar Python
echo -e "${BLUE}🔍 Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 não encontrado!${NC}"
    echo -e "${YELLOW}   Instale Python 3.8+ para continuar${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}✅ Python ${PYTHON_VERSION} encontrado${NC}"

# Verificar dependências básicas
echo -e "${BLUE}🔍 Verificando dependências...${NC}"
cd "$BASE_DIR"

# Verificar se requirements.txt existe
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt não encontrado!${NC}"
    exit 1
fi

# Instalar dependências se necessário
echo -e "${YELLOW}📦 Verificando/instalando dependências...${NC}"
pip3 install -r requirements.txt --quiet --disable-pip-version-check || {
    echo -e "${RED}❌ Erro ao instalar dependências!${NC}"
    echo -e "${YELLOW}   Tente: pip3 install -r requirements.txt${NC}"
    exit 1
}
echo -e "${GREEN}✅ Dependências OK${NC}"

# Criar diretórios necessários
echo -e "${BLUE}📁 Criando estrutura de diretórios...${NC}"
mkdir -p data logs output library/processed

# Verificar Ollama (opcional)
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✅ Ollama disponível${NC}"

    # Verificar se está rodando
    if ! pgrep -x "ollama" > /dev/null; then
        echo -e "${YELLOW}🔄 Iniciando Ollama...${NC}"
        ollama serve > /dev/null 2>&1 &
        sleep 2
    fi
else
    echo -e "${YELLOW}⚠️  Ollama não encontrado (funcionalidades limitadas)${NC}"
fi

# Configurar PYTHONPATH
export PYTHONPATH="$BASE_DIR:$PYTHONPATH"

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                    ✨ SISTEMA PRONTO!                        ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${PURPLE}🎯 COMANDOS DISPONÍVEIS:${NC}"
echo ""
echo -e "${GREEN}📊 Análise de Roteiros:${NC}"
echo -e "   ./bin/scripturemon analyze arquivo.pdf"
echo -e "   ./bin/scripturemon pipeline roteiro.txt"
echo ""
echo -e "${GREEN}🧠 Sistema RAG (Consultas):${NC}"
echo -e "   ./bin/scripturemon rag \"Quais personagens aparecem?\""
echo ""
echo -e "${GREEN}🌐 Interface Web:${NC}"
echo -e "   ./bin/scripturemon web"
echo -e "   # Depois acesse: http://localhost:5000"
echo ""
echo -e "${GREEN}🔧 Outros comandos:${NC}"
echo -e "   ./bin/scripturemon --help       # Ver todas as opções"
echo -e "   ./bin/scripturemon status       # Status do sistema"
echo -e "   ./bin/scripturemon version      # Versão"
echo ""
echo -e "${GREEN}📚 DigiLang (Compressão):${NC}"
echo -e "   ./bin/scripturemon digilang compress arquivo.txt"
echo -e "   ./bin/scripturemon digilang decompress arquivo.digilang"
echo ""

# Teste rápido do sistema
echo -e "${BLUE}🧪 Teste rápido do sistema...${NC}"
if python3 -c "
import sys
sys.path.insert(0, '$BASE_DIR')
try:
    from apps.scripturemon.cli_champion import main
    print('✅ Core do sistema OK')
except Exception as e:
    print(f'❌ Erro: {e}')
    sys.exit(1)
" 2>/dev/null; then
    echo -e "${GREEN}✅ Sistema funcionando corretamente!${NC}"
else
    echo -e "${YELLOW}⚠️  Sistema com limitações (mas funcional)${NC}"
fi

echo ""
echo -e "${CYAN}🚀 Para começar, execute:${NC}"
echo -e "${GREEN}   ./bin/scripturemon --help${NC}"
echo ""
echo -e "${BLUE}💡 Dica: Use 'python3 bin/scripturemon' se './bin/scripturemon' não funcionar${NC}"
echo ""