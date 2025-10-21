#!/bin/bash
# Script para redirecionamento seguro com verificação

PROTECTED="/Users/clubproducoes/Digimundo/scripturemon-champion"
AUTH_FILE="/Users/clubproducoes/Digimundo/claude_code/protection/.authorized"

safe_write() {
    local content="$1"
    local file="$2"

    # Verifica se é área protegida
    if [[ "$file" == "$PROTECTED"* ]]; then
        # Verifica autorização
        if [ ! -f "$AUTH_FILE" ]; then
            echo "🔐 Redirecionamento bloqueado!"
            echo "Use scripturemon-auth primeiro"
            return 1
        fi

        # Verifica se ainda é válida (15 segundos)
        AUTH_TIME=$(cat "$AUTH_FILE" 2>/dev/null)
        NOW=$(date +%s)

        if [ $((NOW - AUTH_TIME)) -gt 15 ]; then
            rm -f "$AUTH_FILE"
            echo "⏰ Sessão expirada!"
            return 1
        fi
    fi

    # Escreve o conteúdo
    echo "$content" > "$file"
}

# Exporta a função para uso
export -f safe_write
