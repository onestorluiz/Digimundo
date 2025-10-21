#!/bin/bash
#════════════════════════════════════════════════════════════════
# CORREÇÃO DOS WRAPPERS - PATHS CORRETOS NO macOS
#════════════════════════════════════════════════════════════════

WRAPPER_DIR="/Users/clubproducoes/Digimundo/claude_code/protection/wrappers"

echo "🔧 Corrigindo paths dos comandos nos wrappers..."

# Mapeia comandos para seus paths corretos no macOS
declare -A COMMANDS
COMMANDS[rm]="/bin/rm"
COMMANDS[mv]="/bin/mv"
COMMANDS[cp]="/bin/cp"
COMMANDS[cat]="/bin/cat"
COMMANDS[echo]="/bin/echo"
COMMANDS[ls]="/bin/ls"
COMMANDS[mkdir]="/bin/mkdir"
COMMANDS[chmod]="/bin/chmod"
COMMANDS[touch]="/usr/bin/touch"
COMMANDS[sed]="/usr/bin/sed"
COMMANDS[awk]="/usr/bin/awk"
COMMANDS[grep]="/usr/bin/grep"
COMMANDS[find]="/usr/bin/find"
COMMANDS[python3]="/usr/bin/python3"
COMMANDS[python]="/usr/bin/python"

for CMD in "${!COMMANDS[@]}"; do
    WRAPPER_FILE="$WRAPPER_DIR/$CMD"
    REAL_PATH="${COMMANDS[$CMD]}"

    echo "   Atualizando $CMD -> $REAL_PATH"

    cat > "$WRAPPER_FILE" << EOF
#!/bin/bash
# Wrapper para $CMD

source /Users/clubproducoes/Digimundo/claude_code/protection/wrapper_template.sh

# Verifica se está tentando acessar área protegida
if [[ "\$@" == *"/Users/clubproducoes/Digimundo/scripturemon-champion"* ]]; then
    if ! check_auth; then
        show_claude_instructions
        exit 1
    fi
fi

# Executa comando original
$REAL_PATH "\$@"
EOF

    chmod +x "$WRAPPER_FILE"
done

echo "✅ Wrappers corrigidos com paths corretos!"