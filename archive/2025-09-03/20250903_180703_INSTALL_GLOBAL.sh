#!/bin/bash
# SCRIPTUREMON - Instalador Global
# Instala o comando scripturemon para uso em qualquer lugar do terminal

set -e

echo "🎬 INSTALADOR SCRIPTUREMON"
echo "=========================="
echo ""

# Diretório base
SCRIPTUREMON_HOME="/Users/clubproducoes/Digimundo/scripturemon-validation"
BIN_SCRIPT="$SCRIPTUREMON_HOME/bin/scripturemon"

# Verificar se o script existe
if [ ! -f "$BIN_SCRIPT" ]; then
    echo "❌ Erro: Script não encontrado em $BIN_SCRIPT"
    exit 1
fi

# Tornar executável
chmod +x "$BIN_SCRIPT"
echo "✅ Script marcado como executável"

# Opção 1: Link em ~/bin (não precisa sudo)
if [ -d "$HOME/bin" ]; then
    echo ""
    echo "📁 Instalando em ~/bin (recomendado)..."
    ln -sf "$BIN_SCRIPT" "$HOME/bin/scripturemon"
    echo "✅ Link criado em ~/bin/scripturemon"
    
    # Verificar se ~/bin está no PATH
    if echo "$PATH" | grep -q "$HOME/bin"; then
        echo "✅ ~/bin já está no PATH"
    else
        echo "⚠️  ~/bin não está no PATH. Adicionando..."
        
        # Detectar shell
        if [ -f "$HOME/.zshrc" ]; then
            SHELL_RC="$HOME/.zshrc"
        elif [ -f "$HOME/.bashrc" ]; then
            SHELL_RC="$HOME/.bashrc"
        else
            SHELL_RC="$HOME/.profile"
        fi
        
        # Adicionar ao PATH
        echo "" >> "$SHELL_RC"
        echo "# Scripturemon" >> "$SHELL_RC"
        echo 'export PATH="$HOME/bin:$PATH"' >> "$SHELL_RC"
        echo "✅ PATH atualizado em $SHELL_RC"
        echo "   Execute: source $SHELL_RC"
    fi
fi

# Opção 2: Link em /usr/local/bin (precisa sudo)
echo ""
echo "📁 Para instalar globalmente em /usr/local/bin (opcional):"
echo "   Execute: sudo ln -sf $BIN_SCRIPT /usr/local/bin/scripturemon"

# Criar alias como backup
echo ""
echo "📝 Criando alias como backup..."
ALIAS_CMD="alias scripturemon='$BIN_SCRIPT'"

# Adicionar alias aos arquivos de configuração
for RC_FILE in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.profile"; do
    if [ -f "$RC_FILE" ]; then
        if ! grep -q "alias scripturemon=" "$RC_FILE"; then
            echo "" >> "$RC_FILE"
            echo "# Scripturemon alias" >> "$RC_FILE"
            echo "$ALIAS_CMD" >> "$RC_FILE"
            echo "✅ Alias adicionado a $RC_FILE"
        else
            echo "✅ Alias já existe em $RC_FILE"
        fi
    fi
done

echo ""
echo "🎬 INSTALAÇÃO COMPLETA!"
echo "======================="
echo ""
echo "Para usar o comando scripturemon:"
echo "1. Recarregue seu terminal: source ~/.zshrc"
echo "2. Digite: scripturemon"
echo ""
echo "Comandos disponíveis:"
echo "  scripturemon          - Chat interativo"
echo "  scripturemon status   - Ver status do sistema"
echo "  scripturemon doctor   - Diagnóstico completo"
echo "  scripturemon symbiotic <texto> - Processar com 4 modelos"
echo "  scripturemon fusion   - Modo fusion com 10 sistemas"
echo ""
echo "62/100. Sempre."