#!/bin/bash
# 🚀 SETUP DOS MODELOS DEEPSEEK 70B

echo "🚀 SETUP DEEPSEEK 70B - ECO & DEDICATED"
echo "========================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Diretório base
BASE_DIR="/Users/clubproducoes/Digimundo/scripturemon-champion"
MODELFILE_DIR="$BASE_DIR/data/models/modelfiles"

# Verificar se Ollama está rodando
echo "🔍 Verificando Ollama..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${RED}❌ Ollama não está rodando!${NC}"
    echo "   Execute: ollama serve"
    exit 1
fi
echo -e "${GREEN}✅ Ollama está ativo${NC}"
echo ""

# Verificar se deepseek-r1:70b existe
echo "🔍 Verificando modelo base deepseek-r1:70b..."
if ! ollama list | grep -q "deepseek-r1:70b"; then
    echo -e "${YELLOW}⚠️ deepseek-r1:70b não encontrado${NC}"
    echo "   Você precisa baixar primeiro:"
    echo "   ollama pull deepseek-r1:70b"
    echo ""
    echo "   Isso vai baixar ~42GB. Deseja fazer agora? (s/n)"
    read -r response
    if [[ "$response" == "s" ]]; then
        ollama pull deepseek-r1:70b
    else
        echo "Abortando setup."
        exit 1
    fi
else
    echo -e "${GREEN}✅ deepseek-r1:70b encontrado${NC}"
fi
echo ""

# Criar modelos
echo "📦 CRIANDO MODELOS OTIMIZADOS..."
echo "================================="
echo ""

# 1. Modelo ECO
echo "1️⃣ Criando deeplearning-70b-eco..."
if [ -f "$MODELFILE_DIR/deeplearning-70b-eco.modelfile" ]; then
    ollama create deeplearning-70b-eco -f "$MODELFILE_DIR/deeplearning-70b-eco.modelfile"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ deeplearning-70b-eco criado!${NC}"
    else
        echo -e "${RED}❌ Erro ao criar deeplearning-70b-eco${NC}"
    fi
else
    echo -e "${RED}❌ Modelfile ECO não encontrado${NC}"
    echo "   Esperado em: $MODELFILE_DIR/deeplearning-70b-eco.modelfile"
fi
echo ""

# 2. Modelo DEDICATED
echo "2️⃣ Criando deeplearning-70b-dedicated..."
if [ -f "$MODELFILE_DIR/deeplearning-70b-dedicated.modelfile" ]; then
    ollama create deeplearning-70b-dedicated -f "$MODELFILE_DIR/deeplearning-70b-dedicated.modelfile"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ deeplearning-70b-dedicated criado!${NC}"
    else
        echo -e "${RED}❌ Erro ao criar deeplearning-70b-dedicated${NC}"
    fi
else
    echo -e "${RED}❌ Modelfile DEDICATED não encontrado${NC}"
    echo "   Esperado em: $MODELFILE_DIR/deeplearning-70b-dedicated.modelfile"
fi
echo ""

# Verificar modelos criados
echo "📋 VERIFICANDO MODELOS..."
echo "========================="
ollama list | grep -E "(deeplearning-70b|deepseek-r1:70b)" || echo "Nenhum modelo 70b encontrado"
echo ""

# Criar diretórios de log
echo "📁 CRIANDO ESTRUTURA DE LOGS..."
LOG_DIR="$BASE_DIR/data/logs/deep_learning_70b"
mkdir -p "$LOG_DIR"
echo -e "${GREEN}✅ Diretório de logs criado: $LOG_DIR${NC}"
echo ""

# Instruções finais
echo "✅ SETUP COMPLETO!"
echo "=================="
echo ""
echo "📚 PRÓXIMOS PASSOS:"
echo ""
echo "1. TESTE RÁPIDO (recomendado primeiro):"
echo "   python3 $BASE_DIR/scripts/active/test_70b_modes.py"
echo ""
echo "2. MONITORAR SISTEMA:"
echo "   python3 $BASE_DIR/scripts/active/monitor_70b.py watch"
echo ""
echo "3. PROCESSAR ROTEIRO COMPLETO:"
echo "   python3 $BASE_DIR/scripts/active/async_70b_processor.py"
echo ""
echo "⚠️ IMPORTANTE:"
echo "  • Modo ECO usa ~45GB RAM (seguro para uso contínuo)"
echo "  • Modo DEDICATED usa ~65GB RAM (máxima qualidade)"
echo "  • Primeira execução pode demorar para carregar modelo"
echo ""
echo "💡 DICA: Comece com modo ECO para testar!"
echo ""
echo "DIGIMUNDO PRESENTE 🥷"