#!/bin/bash

echo "🤖 INSTALADOR CLAUDE CODE PARA DIGIMUNDO"
echo "========================================"
echo ""

# Método 1: Instalação local no projeto
echo "📦 Tentando instalação local no projeto..."
npm install @anthropic-ai/claude-code --save-dev

if [ $? -eq 0 ]; then
    echo "✅ Claude Code instalado localmente!"
    
    # Criar wrapper script
    cat > claude-code-local << 'EOF'
#!/bin/bash
node_modules/.bin/claude-code "$@"
EOF
    chmod +x claude-code-local
    
    echo "✅ Wrapper criado: ./claude-code-local"
    echo ""
    echo "🔐 Para autenticar:"
    echo "   ./claude-code-local auth login"
else
    echo "⚠️ Instalação local falhou"
    echo ""
    echo "📝 Método alternativo - Instalação manual:"
    echo ""
    echo "1. Abra um novo terminal"
    echo "2. Execute com sudo (se necessário):"
    echo "   sudo npm install -g @anthropic-ai/claude-code"
    echo ""
    echo "3. Depois autentique:"
    echo "   claude-code auth login"
    echo ""
    echo "💡 Ou use npx (sem instalação):"
    echo "   npx @anthropic-ai/claude-code auth login"
fi

echo ""
echo "📋 Verificando status..."

# Verificar se está disponível
if command -v claude-code &> /dev/null; then
    echo "✅ Claude Code global encontrado"
    claude-code --version
elif [ -f "./node_modules/.bin/claude-code" ]; then
    echo "✅ Claude Code local encontrado"
    ./node_modules/.bin/claude-code --version
elif command -v npx &> /dev/null; then
    echo "💡 Use npx para executar:"
    echo "   npx @anthropic-ai/claude-code [comando]"
else
    echo "❌ Claude Code não disponível"
fi