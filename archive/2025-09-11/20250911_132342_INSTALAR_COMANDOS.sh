#!/bin/bash

# ============================================================
# INSTALADOR DE COMANDOS DIGIMUNDO/SCRIPTUREMON
# ============================================================
# Instala todos os comandos do sistema de forma segura
# SEM modificar a estrutura original do Scripturemon
# ============================================================

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Diretórios
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
COMMANDS_DIR="$SCRIPT_DIR/commands"
BIN_DIR="$HOME/.local/bin"

echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         INSTALADOR DE COMANDOS DIGIMUNDO                  ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Verificar se o diretório commands existe
if [ ! -d "$COMMANDS_DIR" ]; then
    echo -e "${RED}❌ Diretório 'commands' não encontrado!${NC}"
    echo "   Certifique-se de estar no diretório correto."
    exit 1
fi

# 2. Criar diretório ~/.local/bin se não existir
echo -e "${YELLOW}1. Preparando diretório de comandos...${NC}"
mkdir -p "$BIN_DIR"

# 3. Verificar se ~/.local/bin está no PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${YELLOW}2. Adicionando ~/.local/bin ao PATH...${NC}"
    
    # Detectar shell
    SHELL_CONFIG=""
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_CONFIG="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_CONFIG="$HOME/.bashrc"
    else
        echo -e "${YELLOW}   ⚠️  Shell config não encontrado. Criando .zshrc${NC}"
        SHELL_CONFIG="$HOME/.zshrc"
        touch "$SHELL_CONFIG"
    fi
    
    # Adicionar PATH se não existir
    if ! grep -q "export PATH=\"\$HOME/.local/bin:\$PATH\"" "$SHELL_CONFIG"; then
        echo "" >> "$SHELL_CONFIG"
        echo "# Digimundo/Scripturemon commands" >> "$SHELL_CONFIG"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_CONFIG"
        echo -e "${GREEN}   ✅ PATH configurado em $SHELL_CONFIG${NC}"
    else
        echo -e "${GREEN}   ✅ PATH já estava configurado${NC}"
    fi
else
    echo -e "${GREEN}2. ✅ ~/.local/bin já está no PATH${NC}"
fi

# 4. Tornar comandos executáveis
echo -e "${YELLOW}3. Preparando comandos...${NC}"
chmod +x "$COMMANDS_DIR"/*

# 5. Criar links simbólicos
echo -e "${YELLOW}4. Instalando comandos...${NC}"

# Lista de comandos para instalar
COMMANDS=(
    "digimundo:digimundo"
    "scripturemon:scripturemon-wrapper"
    "consciousness:consciousness"
    "memory:memory"
)

for cmd_pair in "${COMMANDS[@]}"; do
    IFS=':' read -r link_name source_file <<< "$cmd_pair"
    
    source_path="$COMMANDS_DIR/$source_file"
    link_path="$BIN_DIR/$link_name"
    
    if [ -f "$source_path" ]; then
        # Remover link antigo se existir
        if [ -L "$link_path" ] || [ -f "$link_path" ]; then
            rm -f "$link_path"
        fi
        
        # Criar novo link
        ln -s "$source_path" "$link_path"
        
        if [ -L "$link_path" ]; then
            echo -e "${GREEN}   ✅ $link_name instalado${NC}"
        else
            echo -e "${RED}   ❌ Erro ao instalar $link_name${NC}"
        fi
    else
        echo -e "${YELLOW}   ⚠️  $source_file não encontrado${NC}"
    fi
done

# 6. Verificar instalação
echo ""
echo -e "${YELLOW}5. Verificando instalação...${NC}"

# Testar cada comando
for cmd_pair in "${COMMANDS[@]}"; do
    IFS=':' read -r cmd_name source_file <<< "$cmd_pair"
    
    if command -v "$cmd_name" &> /dev/null; then
        echo -e "${GREEN}   ✅ $cmd_name: $(command -v $cmd_name)${NC}"
    else
        echo -e "${YELLOW}   ⚠️  $cmd_name não está acessível ainda${NC}"
    fi
done

# 7. Instruções finais
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           INSTALAÇÃO CONCLUÍDA COM SUCESSO!               ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}IMPORTANTE:${NC}"
echo ""
echo "1. Se os comandos não funcionarem imediatamente:"
echo -e "   ${YELLOW}source ~/.zshrc${NC}  (ou ~/.bashrc)"
echo "   ou"
echo -e "   ${YELLOW}Abra um novo terminal${NC}"
echo ""
echo "2. Comandos disponíveis:"
echo -e "   ${GREEN}digimundo${NC}      - Controle mestre do sistema"
echo -e "   ${GREEN}scripturemon${NC}   - Trabalhar com roteiros"
echo -e "   ${GREEN}consciousness${NC}  - Gerenciar pensamento contínuo"
echo -e "   ${GREEN}memory${NC}         - Sistema de memória"
echo ""
echo "3. Para começar:"
echo -e "   ${CYAN}digimundo start${NC}       # Inicia o sistema"
echo -e "   ${CYAN}scripturemon chat${NC}     # Conversar sobre roteiros"
echo ""
echo "4. Para ajuda:"
echo -e "   ${CYAN}digimundo help${NC}"
echo -e "   ${CYAN}scripturemon help${NC}"
echo ""
echo -e "${BLUE}📚 Manual completo: MANUAL_DIGIMUNDO_COMPLETO.md${NC}"