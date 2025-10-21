#!/bin/bash

# 🎯 VERIFICAÇÃO FINAL - CLAUDE CODE + DIGIMUNDO

clear
echo "╔══════════════════════════════════════════════════════╗"
echo "║         🔍 VERIFICAÇÃO FINAL DO SISTEMA              ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Claude Code
echo -e "${YELLOW}1. CLAUDE CODE:${NC}"
if [ -f "$HOME/.local/bin/claude" ]; then
    VERSION=$($HOME/.local/bin/claude --version 2>/dev/null)
    echo -e "   ${GREEN}✅ Instalado: $VERSION${NC}"
    echo "   📍 Local: ~/.local/bin/claude"
else
    echo -e "   ${RED}❌ Não instalado${NC}"
fi
echo ""

# 2. PATH
echo -e "${YELLOW}2. PATH CONFIGURADO:${NC}"
if grep -q "/.local/bin" ~/.zshrc 2>/dev/null; then
    echo -e "   ${GREEN}✅ .zshrc configurado${NC}"
else
    echo -e "   ${RED}❌ .zshrc não configurado${NC}"
fi
if grep -q "/.local/bin" ~/.bash_profile 2>/dev/null; then
    echo -e "   ${GREEN}✅ .bash_profile configurado${NC}"
else
    echo -e "   ${RED}❌ .bash_profile não configurado${NC}"
fi
echo ""

# 3. Servidor Digimundo
echo -e "${YELLOW}3. SERVIDOR DIGIMUNDO:${NC}"
if curl -s http://localhost:7937/health > /dev/null 2>&1; then
    echo -e "   ${GREEN}✅ Online na porta 7937${NC}"
    HEALTH=$(curl -s http://localhost:7937/health)
    echo "   📊 Status: $HEALTH"
else
    echo -e "   ${RED}❌ Offline${NC}"
fi
echo ""

# 4. Aplicativo Desktop
echo -e "${YELLOW}4. DIGIMUNDO.APP:${NC}"
if [ -f "$HOME/Desktop/Digimundo.app/Contents/MacOS/Digimundo" ]; then
    echo -e "   ${GREEN}✅ Instalado no Desktop${NC}"
    echo "   📱 Clique duplo para iniciar"
else
    echo -e "   ${RED}❌ Não encontrado${NC}"
fi
echo ""

# 5. LaunchAgent
echo -e "${YELLOW}5. INICIALIZAÇÃO AUTOMÁTICA:${NC}"
if launchctl list | grep -q "com.digimundo.autostart"; then
    echo -e "   ${GREEN}✅ LaunchAgent ativo${NC}"
    echo "   🔄 Inicia ao ligar o Mac"
else
    echo -e "   ${RED}❌ LaunchAgent não carregado${NC}"
fi
echo ""

# 6. Scripts disponíveis
echo -e "${YELLOW}6. SCRIPTS DISPONÍVEIS:${NC}"
SCRIPTS=(
    "CLAUDE_DIGIMUNDO_LAUNCHER.sh"
    "ULTIMATE_LAUNCHER.sh"
    "open_claude.sh"
    "test_claude.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ -f "/Users/clubproducoes/Digimundo/digimundo_starter/$script" ]; then
        echo -e "   ${GREEN}✅ $script${NC}"
    else
        echo -e "   ${RED}❌ $script${NC}"
    fi
done
echo ""

echo "╔══════════════════════════════════════════════════════╗"
echo "║                 📋 COMO USAR                         ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "🖱️  OPÇÃO 1 - Clique no Desktop:"
echo "   Duplo clique em Digimundo.app"
echo ""
echo "⌨️  OPÇÃO 2 - Terminal:"
echo "   cd ~/Digimundo/digimundo_starter"
echo "   bash CLAUDE_DIGIMUNDO_LAUNCHER.sh"
echo ""
echo "🤖 OPÇÃO 3 - Direto Claude:"
echo "   claude (em novo terminal)"
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║              ✅ SISTEMA PRONTO!                      ║"
echo "╚══════════════════════════════════════════════════════╝"
