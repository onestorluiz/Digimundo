#!/bin/bash

# 🧪 TESTE E CORREÇÃO DO CLAUDE CODE

echo "🔍 TESTANDO CLAUDE CODE..."
echo "=========================="
echo ""

# Configurar PATH
export PATH="$HOME/.local/bin:/opt/homebrew/opt/node@20/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

# Teste 1: Verificar instalação
echo "📍 Teste 1: Verificando instalação..."
if [ -f "$HOME/.local/bin/claude" ]; then
    echo "✅ Claude instalado em: $HOME/.local/bin/claude"
else
    echo "❌ Claude não encontrado"
    echo ""
    echo "🔧 Instalando Claude Code..."
    curl -fsSL https://claude.ai/install.sh | bash
    echo ""
fi

# Teste 2: Verificar link simbólico
echo ""
echo "📍 Teste 2: Verificando link simbólico..."
ls -la $HOME/.local/bin/claude

# Teste 3: Verificar versão
echo ""
echo "📍 Teste 3: Verificando versão..."
$HOME/.local/bin/claude --version

# Teste 4: Verificar PATH no shell atual
echo ""
echo "📍 Teste 4: PATH atual:"
echo $PATH | tr ':' '\n' | head -5

# Teste 5: Adicionar ao PATH permanentemente
echo ""
echo "📍 Teste 5: Configurando PATH permanentemente..."

# Para zsh
if [ -f "$HOME/.zshrc" ]; then
    if ! grep -q "/.local/bin" "$HOME/.zshrc"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
        echo "✅ PATH adicionado ao .zshrc"
    else
        echo "✅ PATH já configurado no .zshrc"
    fi
fi

# Para bash
if [ -f "$HOME/.bash_profile" ]; then
    if ! grep -q "/.local/bin" "$HOME/.bash_profile"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bash_profile"
        echo "✅ PATH adicionado ao .bash_profile"
    else
        echo "✅ PATH já configurado no .bash_profile"
    fi
fi

echo ""
echo "=========================="
echo "✅ CLAUDE CODE PRONTO!"
echo "=========================="
echo ""
echo "Para usar Claude Code:"
echo ""
echo "1. Em novo terminal:"
echo "   claude"
echo ""
echo "2. Com caminho completo:"
echo "   $HOME/.local/bin/claude"
echo ""
echo "3. No projeto Digimundo:"
echo "   cd ~/Digimundo/digimundo_starter && claude"
echo ""
