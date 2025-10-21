#!/bin/bash

# =================================================================
# INSTALADOR DO COMANDO SCRIPTUREMON
# =================================================================

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         INSTALANDO COMANDO SCRIPTUREMON                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

SCRIPTUREMON_BIN="/Users/clubproducoes/Digimundo/digimons/scripturemon/bin/scripturemon"

# Verificar se o arquivo existe
if [ ! -f "$SCRIPTUREMON_BIN" ]; then
    echo "❌ Arquivo scripturemon não encontrado em $SCRIPTUREMON_BIN"
    exit 1
fi

# Tornar executável
chmod +x "$SCRIPTUREMON_BIN"

# Detectar shell do usuário
SHELL_NAME=$(basename "$SHELL")
SHELL_RC=""

case "$SHELL_NAME" in
    zsh)
        SHELL_RC="$HOME/.zshrc"
        ;;
    bash)
        SHELL_RC="$HOME/.bashrc"
        ;;
    *)
        echo "⚠️ Shell não reconhecido: $SHELL_NAME"
        SHELL_RC="$HOME/.profile"
        ;;
esac

# Criar ~/bin se não existir
mkdir -p ~/bin

# Criar link simbólico
ln -sf "$SCRIPTUREMON_BIN" ~/bin/scripturemon
echo "✅ Link criado em ~/bin/scripturemon"

# Adicionar ~/bin ao PATH se necessário
if ! echo "$PATH" | grep -q "$HOME/bin"; then
    echo "" >> "$SHELL_RC"
    echo "# Scripturemon - Analisador Brutal de Roteiros" >> "$SHELL_RC"
    echo "export PATH=\"\$HOME/bin:\$PATH\"" >> "$SHELL_RC"
    echo "✅ PATH atualizado em $SHELL_RC"
    echo ""
    echo "⚠️ IMPORTANTE: Execute este comando para ativar:"
    echo "   source $SHELL_RC"
else
    echo "✅ ~/bin já está no PATH"
fi

# Criar alias opcionais
echo "" >> "$SHELL_RC"
echo "# Aliases do Scripturemon" >> "$SHELL_RC"
echo "alias smon='scripturemon'" >> "$SHELL_RC"
echo "alias roteiro='scripturemon analyze'" >> "$SHELL_RC"
echo "alias brutal='scripturemon ask'" >> "$SHELL_RC"

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "COMANDOS DISPONÍVEIS:"
echo "  scripturemon         - CLI interativo"
echo "  smon                 - Atalho para scripturemon"
echo "  roteiro <pdf>        - Analisa roteiro"
echo "  brutal <pergunta>    - Pergunta brutal"
echo ""
echo "Para ativar AGORA, execute:"
echo "  source $SHELL_RC"
echo ""
echo "Depois disso, digite 'scripturemon' em qualquer lugar!"