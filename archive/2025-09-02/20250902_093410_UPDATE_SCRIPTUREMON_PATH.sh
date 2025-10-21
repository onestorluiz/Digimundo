#!/bin/bash

# Script para atualizar definitivamente o caminho do Scripturemon

echo "🔧 Atualizando configuração do Scripturemon..."

# 1. Atualizar aliases
cat > ~/.digimundo/scripturemon_aliases.sh << 'EOF'
#!/bin/bash
# SCRIPTUREMON ULTIMATE - Configuração DEFINITIVA

# Diretório correto do Scripturemon Ultimate
export SCRIPTUREMON_HOME="/Users/clubproducoes/Digimundo/scripturemon-validation"

# Comando principal
alias scripturemon='$SCRIPTUREMON_HOME/bin/scripturemon'
alias s='scripturemon'

# Comandos úteis
alias s-test='scripturemon test'
alias s-status='scripturemon status'
alias s-analyze='scripturemon analyze'
alias s-stop='scripturemon stop'
alias s-help='scripturemon --help'

echo "✅ Scripturemon Ultimate carregado!"
echo "💡 Digite 'scripturemon' ou 's' para começar"
EOF

# 2. Garantir que está no .zshrc
if ! grep -q "scripturemon_aliases.sh" ~/.zshrc 2>/dev/null; then
    echo "" >> ~/.zshrc
    echo "# Scripturemon Ultimate" >> ~/.zshrc
    echo "source ~/.digimundo/scripturemon_aliases.sh 2>/dev/null || true" >> ~/.zshrc
fi

# 3. Criar link em ~/bin
mkdir -p ~/bin
ln -sf /Users/clubproducoes/Digimundo/scripturemon-validation/bin/scripturemon ~/bin/scripturemon

# 4. Verificar PATH
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
fi

echo ""
echo "✅ Configuração atualizada!"
echo ""
echo "🎯 Para ativar as mudanças:"
echo "   1. Feche e reabra o terminal, OU"
echo "   2. Execute: source ~/.zshrc"
echo ""
echo "📚 Comandos disponíveis:"
echo "   scripturemon      - Menu interativo"
echo "   scripturemon test - Testar 10 sistemas"
echo "   scripturemon analyze \"texto\" - Analisar"
echo "   scripturemon status - Ver status"
echo "   scripturemon stop - Parar serviços"
echo ""
echo "62/100. Como sempre deve ser."