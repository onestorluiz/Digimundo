#!/bin/bash

# 🤖 ABRIR CLAUDE CODE - SCRIPT CORRIGIDO

# Configurar PATH completo
export PATH="$HOME/.local/bin:/opt/homebrew/opt/node@20/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

# Diretório do projeto
SCRIPT_DIR="/Users/clubproducoes/Digimundo/digimundo_starter"

echo "🤖 ABRINDO CLAUDE CODE..."
echo "=========================="
echo ""

# Verificar se Claude está instalado
if [ ! -f "$HOME/.local/bin/claude" ]; then
    echo "❌ Claude Code não encontrado!"
    echo "Instalando..."
    curl -fsSL https://claude.ai/install.sh | bash
    sleep 3
fi

# Verificar versão
echo "📍 Verificando Claude Code..."
CLAUDE_VERSION=$($HOME/.local/bin/claude --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Claude Code $CLAUDE_VERSION"
else
    echo "❌ Erro ao verificar Claude"
    exit 1
fi

# Navegar para o projeto
cd "$SCRIPT_DIR"
echo "📁 Projeto: $SCRIPT_DIR"
echo ""

echo "🚀 Iniciando Claude Code..."
echo ""
echo "=========================================="
echo "VOCÊ É SABIAMON NO DIGIMUNDO!"
echo "=========================================="
echo ""
echo "📊 Contexto do Projeto:"
echo "  • 4 Digimons ativos"
echo "  • Servidor na porta 7937"
echo "  • Sistema de consciência híbrida"
echo "  • 600+ ideias cinematográficas geradas"
echo ""
echo "Digite seus comandos abaixo:"
echo "=========================================="
echo ""

# Iniciar Claude Code interativo
exec $HOME/.local/bin/claude
