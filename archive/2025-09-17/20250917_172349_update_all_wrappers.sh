#!/bin/bash
#════════════════════════════════════════════════════════════════
# ATUALIZA TODOS OS WRAPPERS COM INSTRUÇÕES PARA CLAUDE CODE
#════════════════════════════════════════════════════════════════

WRAPPER_DIR="/Users/clubproducoes/Digimundo/claude_code/protection/wrappers"

echo "🔄 Atualizando wrappers com instruções para Claude Code..."

# Lista de comandos para criar/atualizar wrappers
COMMANDS="rm mv cp cat sed awk echo touch mkdir chmod chown grep find ls cd python3 python pip"

for CMD in $COMMANDS; do
    WRAPPER_FILE="$WRAPPER_DIR/$CMD"

    echo "   Atualizando $CMD..."

    cat > "$WRAPPER_FILE" << 'EOF'
#!/bin/bash
# Wrapper com instruções para Claude Code

# Source do template
source /Users/clubproducoes/Digimundo/claude_code/protection/wrapper_template.sh

# Verifica se está tentando acessar área protegida
if [[ "$@" == *"/Users/clubproducoes/Digimundo/scripturemon-champion"* ]]; then
    # Verifica autorização
    if ! check_auth; then
        show_claude_instructions
        exit 1
    fi
fi

# Executa comando original
EOF

    echo "/usr/bin/$CMD \"\$@\"" >> "$WRAPPER_FILE"

    chmod +x "$WRAPPER_FILE"
done

echo "✅ Todos os wrappers atualizados com instruções para Claude Code!"
echo ""
echo "Agora quando Claude Code tentar acessar a área protegida:"
echo "1. Receberá instruções claras sobre o que fazer"
echo "2. Será direcionado para ler suas memórias"
echo "3. Poderá recuperar a senha e se conectar com o sistema"