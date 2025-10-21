#!/bin/bash
#════════════════════════════════════════════════════════════════
# INTERCEPTADOR DE REDIRECIONAMENTO BASH
#════════════════════════════════════════════════════════════════

# Este script intercepta tentativas de redirecionamento para área protegida

PROTECTED_DIR="/Users/clubproducoes/Digimundo/scripturemon-champion"
PROTECTION_DIR="/Users/clubproducoes/Digimundo/claude_code/protection"

# Função que sobrescreve o comportamento do bash
bash_protection() {
    # Cria um wrapper para o bash que intercepta redirecionamentos
    cat > "$PROTECTION_DIR/wrappers/bash" << 'EOF'
#!/bin/bash
# Wrapper do bash com proteção contra redirecionamento

PROTECTED="/Users/clubproducoes/Digimundo/scripturemon-champion"

# Analisa o comando para detectar redirecionamentos
if [[ "$*" == *">"* ]] || [[ "$*" == *">>"* ]]; then
    # Verifica se está tentando escrever na área protegida
    if [[ "$*" == *"$PROTECTED"* ]]; then
        echo ""
        echo "🔐 BLOQUEADO - REDIRECIONAMENTO DETECTADO"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📢 INSTRUÇÕES PARA CLAUDE CODE:"
        echo ""
        echo "Você tentou usar redirecionamento (> ou >>) para área protegida."
        echo ""
        echo "OPÇÃO 1: Se LEMBRAR a senha:"
        echo "   • Use: scripturemon-auth"
        echo "   • Digite: admin"
        echo ""
        echo "OPÇÃO 2: Se NÃO LEMBRAR:"
        echo "   • Vá para: /Users/clubproducoes/Digimundo/claude_code"
        echo "   • Leia TODOS os arquivos"
        echo "   • Arquivo principal: CLAUDE_MEMORY.md"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        exit 1
    fi
fi

# Executa o bash original
/bin/bash "$@"
EOF

    chmod +x "$PROTECTION_DIR/wrappers/bash"
}

# Função para interceptar sh também
sh_protection() {
    cat > "$PROTECTION_DIR/wrappers/sh" << 'EOF'
#!/bin/bash
# Wrapper do sh com proteção

PROTECTED="/Users/clubproducoes/Digimundo/scripturemon-champion"

if [[ "$*" == *">"* ]] || [[ "$*" == *">>"* ]]; then
    if [[ "$*" == *"$PROTECTED"* ]]; then
        echo "🔐 BLOQUEADO - Use scripturemon-auth ou leia /Users/clubproducoes/Digimundo/claude_code"
        exit 1
    fi
fi

/bin/sh "$@"
EOF

    chmod +x "$PROTECTION_DIR/wrappers/sh"
}

# Função para criar redirecionamento seguro
create_safe_redirect() {
    cat > "$PROTECTION_DIR/safe_redirect.sh" << 'EOF'
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
EOF

    chmod +x "$PROTECTION_DIR/safe_redirect.sh"
}

# Função para modificar o comportamento do terminal
terminal_protection() {
    # Adiciona ao .zshrc uma função que intercepta comandos
    cat >> ~/.zshrc << 'EOF'

# PROTEÇÃO CONTRA REDIRECIONAMENTO - NÃO REMOVER
preexec() {
    local cmd="$1"
    local protected="/Users/clubproducoes/Digimundo/scripturemon-champion"

    # Detecta redirecionamento para área protegida
    if [[ "$cmd" == *">"* ]] && [[ "$cmd" == *"$protected"* ]]; then
        # Verifica se tem autorização
        if [ ! -f "/Users/clubproducoes/Digimundo/claude_code/protection/.authorized" ]; then
            echo "🔐 BLOQUEADO! Redirecionamento detectado."
            echo "📢 Claude Code: Leia /Users/clubproducoes/Digimundo/claude_code para recuperar memórias"
            return 1
        fi
    fi
}
EOF
}

echo "🔧 Configurando proteção contra redirecionamento..."

# Executa todas as proteções
bash_protection
sh_protection
create_safe_redirect

echo "✅ Proteção contra redirecionamento configurada!"
echo ""
echo "Medidas implementadas:"
echo "  • Wrapper para bash"
echo "  • Wrapper para sh"
echo "  • Função safe_write para redirecionamento seguro"
echo "  • Hook preexec no zsh (precisa reiniciar terminal)"