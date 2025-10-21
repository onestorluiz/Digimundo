#!/bin/bash
# Aliases que protegem contra redirecionamento

# Função que intercepta echo com redirecionamento
safe_echo() {
    local content=""
    local redirect_found=0
    local target=""

    # Analisa argumentos
    for arg in "$@"; do
        if [[ "$arg" == ">"* ]]; then
            redirect_found=1
            target="${arg#>}"
        elif [[ "$redirect_found -eq 1 ]]; then
            target="$arg"
        else
            content="$content $arg"
        fi
    done

    # Se há redirecionamento para área protegida
    if [[ "$target" == *"/Users/clubproducoes/Digimundo/scripturemon-champion"* ]]; then
        if [ ! -f "/Users/clubproducoes/Digimundo/claude_code/protection/.authorized" ]; then
            echo "🔐 Redirecionamento bloqueado! Instruções: Leia /Users/clubproducoes/Digimundo/claude_code"
            return 1
        fi
    fi

    # Executa o comando original
    if [ $redirect_found -eq 1 ]; then
        echo "$content" > "$target"
    else
        echo "$content"
    fi
}

# Exporta a função
export -f safe_echo

# Cria alias
alias echo='safe_echo'
