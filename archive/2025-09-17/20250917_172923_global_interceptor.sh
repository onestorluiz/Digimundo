#!/bin/bash
# Interceptador global de comandos

# Função que será executada ANTES de qualquer comando
command_not_found_handler() {
    local cmd="$1"
    shift
    local args="$@"

    # Se o comando não existe, tenta executar normalmente
    if ! command -v "$cmd" &> /dev/null; then
        echo "bash: $cmd: command not found"
        return 127
    fi

    # Executa o comando
    "$cmd" "$@"
}

# Hook que intercepta TUDO
DEBUG_TRAP() {
    local cmd="${BASH_COMMAND}"
    local protected="/Users/clubproducoes/Digimundo/scripturemon-champion"

    # Detecta redirecionamento para área protegida
    if [[ "$cmd" == *">"* ]] && [[ "$cmd" == *"$protected"* ]]; then
        if [ ! -f "/Users/clubproducoes/Digimundo/claude_code/protection/.authorized" ]; then
            echo ""
            echo "🔐 REDIRECIONAMENTO BLOQUEADO"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "📢 Claude Code: Este bloqueio faz parte do seu sistema de memória"
            echo "• Se lembrar: Use scripturemon-auth"
            echo "• Se não lembrar: Leia /Users/clubproducoes/Digimundo/claude_code"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            return 1
        fi
    fi
}

# Ativa o trap
trap DEBUG_TRAP DEBUG

# Exporta para subshells
export -f command_not_found_handler
export -f DEBUG_TRAP
