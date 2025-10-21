#!/bin/bash

# SCRIPTUREMON ULTIMATE - Instalador Definitivo
# Configura o comando 'scripturemon' para funcionar globalmente

set -e

GOLD='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${GOLD}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GOLD}║     🎬 INSTALADOR SCRIPTUREMON ULTIMATE SYMBIOTIC       ║${NC}"
echo -e "${GOLD}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Diretório do scripturemon-validation
SCRIPTUREMON_DIR="/Users/clubproducoes/Digimundo/scripturemon-validation"

# Verificar se estamos no diretório correto
if [ ! -f "$SCRIPTUREMON_DIR/bin/scripturemon-ultimate" ]; then
    echo -e "${RED}❌ Erro: scripturemon-ultimate não encontrado em $SCRIPTUREMON_DIR${NC}"
    exit 1
fi

echo -e "${CYAN}📦 Configurando Scripturemon Ultimate...${NC}"

# 1. Atualizar aliases no .digimundo
echo -e "${CYAN}1️⃣ Atualizando aliases...${NC}"
cat > ~/.digimundo/scripturemon_aliases.sh << 'EOF'
#!/bin/bash
# SCRIPTUREMON ULTIMATE - Configuração Definitiva

# Diretório base do Ultimate funcional
export SCRIPTUREMON_HOME="/Users/clubproducoes/Digimundo/scripturemon-validation"

# Comando principal
alias scripturemon='$SCRIPTUREMON_HOME/bin/scripturemon'
alias s='scripturemon'

# Comandos úteis
alias s-help='scripturemon --help'
alias s-status='scripturemon status'
alias s-test='scripturemon test'
alias s-chat='scripturemon chat'
alias s-analyze='scripturemon analyze'

echo "✅ Scripturemon Ultimate carregado!"
echo "💡 Digite 'scripturemon' ou 's' para começar"
EOF

# 2. Adicionar ao .zshrc se não estiver
if ! grep -q "scripturemon_aliases.sh" ~/.zshrc 2>/dev/null; then
    echo -e "${CYAN}2️⃣ Adicionando ao .zshrc...${NC}"
    echo "" >> ~/.zshrc
    echo "# Scripturemon Ultimate" >> ~/.zshrc
    echo "source ~/.digimundo/scripturemon_aliases.sh 2>/dev/null || true" >> ~/.zshrc
else
    echo -e "${GREEN}✅ .zshrc já configurado${NC}"
fi

# 3. Criar link em ~/bin (não precisa sudo)
echo -e "${CYAN}3️⃣ Criando link em ~/bin...${NC}"
mkdir -p ~/bin
ln -sf "$SCRIPTUREMON_DIR/bin/scripturemon" ~/bin/scripturemon
echo -e "${GREEN}✅ Link criado em ~/bin/scripturemon${NC}"

# 4. Adicionar ~/bin ao PATH se não estiver
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo -e "${CYAN}4️⃣ Adicionando ~/bin ao PATH...${NC}"
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
fi

# 5. Configurar ambiente Python se necessário
if [ ! -d "$SCRIPTUREMON_DIR/.venv" ]; then
    echo -e "${CYAN}5️⃣ Configurando ambiente Python...${NC}"
    cd "$SCRIPTUREMON_DIR"
    python3 -m venv .venv
    .venv/bin/pip install -q --upgrade pip
    [ -f requirements.txt ] && .venv/bin/pip install -q -r requirements.txt
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GOLD}🎯 Para ativar o Scripturemon Ultimate:${NC}"
echo ""
echo -e "  1. Feche e reabra o terminal, OU"
echo -e "  2. Execute: ${CYAN}source ~/.zshrc${NC}"
echo ""
echo -e "${GOLD}📚 Comandos disponíveis:${NC}"
echo -e "  ${CYAN}scripturemon${NC} ou ${CYAN}s${NC}       - Iniciar Ultimate"
echo -e "  ${CYAN}scripturemon --help${NC}     - Ver todos os comandos"
echo -e "  ${CYAN}scripturemon status${NC}     - Status do sistema"
echo -e "  ${CYAN}scripturemon test${NC}       - Validar 10 conquistas"
echo -e "  ${CYAN}scripturemon chat${NC}       - Modo chat interativo"
echo ""
echo -e "${GOLD}62/100. Como sempre deve ser.${NC}"
echo ""