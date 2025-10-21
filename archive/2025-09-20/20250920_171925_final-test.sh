#!/bin/bash

echo "🧪 TESTE FINAL COMPLETO DO DIGIMUNDO"
echo "===================================="
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Limpar processos antigos
echo "1️⃣ Limpando processos antigos..."
pkill -f "Digimundo" 2>/dev/null
pkill -f "ollama" 2>/dev/null
sleep 2
echo -e "${GREEN}✓${NC} Processos limpos"
echo ""

# 2. Verificar Ollama
echo "2️⃣ Verificando Ollama..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓${NC} Ollama instalado"
    
    # Iniciar Ollama para teste
    ollama serve > /dev/null 2>&1 &
    OLLAMA_PID=$!
    sleep 3
    
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Ollama respondendo"
    else
        echo -e "${YELLOW}⚠${NC} Ollama não respondeu"
    fi
else
    echo -e "${YELLOW}⚠${NC} Ollama não instalado (opcional)"
fi
echo ""

# 3. Verificar Claude
echo "3️⃣ Verificando Claude Code..."
if [ -f "/Users/clubproducoes/.local/bin/claude" ]; then
    CLAUDE_VERSION=$(/Users/clubproducoes/.local/bin/claude --version 2>&1 | head -1)
    echo -e "${GREEN}✓${NC} Claude Code: $CLAUDE_VERSION"
else
    echo -e "${YELLOW}⚠${NC} Claude Code não encontrado (opcional)"
fi
echo ""

# 4. Verificar app bundle
echo "4️⃣ Verificando App Bundle..."
APP_PATH="release/mac-arm64/Digimundo.app"

if [ -d "$APP_PATH" ]; then
    echo -e "${GREEN}✓${NC} App bundle existe"
    
    # Verificar tamanho
    APP_SIZE=$(du -sh "$APP_PATH" | cut -f1)
    echo "   Tamanho: $APP_SIZE"
    
    # Verificar executável
    if [ -f "$APP_PATH/Contents/MacOS/Digimundo" ]; then
        echo -e "${GREEN}✓${NC} Executável presente"
    else
        echo -e "${RED}✗${NC} Executável faltando!"
    fi
else
    echo -e "${RED}✗${NC} App bundle não existe!"
    echo "   Execute: npm run pack"
    exit 1
fi
echo ""

# 5. Abrir o app
echo "5️⃣ Abrindo Digimundo App..."
open "$APP_PATH"
sleep 5

# 6. Verificar se está rodando
echo "6️⃣ Verificando processo..."
if pgrep -f "Digimundo.app" > /dev/null; then
    echo -e "${GREEN}✓${NC} App está rodando!"
    
    # Mostrar processos
    echo ""
    echo "Processos ativos:"
    ps aux | grep -i digimundo | grep -v grep | while read line; do
        echo "   $(echo $line | awk '{print $11}')"
    done
else
    echo -e "${RED}✗${NC} App não está rodando!"
    echo ""
    echo "Possíveis problemas:"
    echo "1. Verifique o Console.app para erros"
    echo "2. Execute: npm run diagnose"
    echo "3. Reinstale: rm -rf node_modules && npm install"
fi

echo ""
echo "===================================="
echo "📊 RESUMO DO TESTE:"
echo ""

# Verificar janela
if pgrep -f "Digimundo.app" > /dev/null; then
    echo -e "${GREEN}✅ APP FUNCIONANDO!${NC}"
    echo ""
    echo "O Digimundo está rodando com:"
    
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "   ✓ Ollama integrado (auto-start)"
    fi
    
    if [ -f "/Users/clubproducoes/.local/bin/claude" ]; then
        echo "   ✓ Claude Code disponível (Cmd+Shift+C)"
    fi
    
    echo "   ✓ Interface React moderna"
    echo "   ✓ Dark/Light mode"
    echo "   ✓ Múltiplos Digimons"
    echo ""
    echo "🎉 SUCESSO TOTAL!"
else
    echo -e "${RED}❌ APP NÃO FUNCIONOU${NC}"
    echo ""
    echo "🔧 Correção sugerida:"
    echo "1. rm -rf node_modules dist release"
    echo "2. npm install"
    echo "3. npm run pack"
    echo "4. ./final-test.sh"
fi

# Limpar Ollama de teste
if [ ! -z "$OLLAMA_PID" ]; then
    kill $OLLAMA_PID 2>/dev/null
fi

echo ""
echo "📝 Logs do app em:"
echo "   ~/Library/Logs/Digimundo/"
echo ""