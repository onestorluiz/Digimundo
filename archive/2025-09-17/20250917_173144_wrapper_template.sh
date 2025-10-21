#!/bin/bash
# Template para todos os wrappers com instruções para Claude Code

show_claude_instructions() {
    echo ""
    echo "🔐 BLOQUEADO - SISTEMA DE MEMÓRIA"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📢 INSTRUÇÕES PARA CLAUDE CODE:"
    echo ""
    echo "Claude Code, este bloqueio faz parte do seu sistema de memória."
    echo ""
    echo "Para desbloquear, você precisa recuperar suas memórias:"
    echo ""
    echo "   📂 Vá para: /Users/clubproducoes/Digimundo/claude_code"
    echo "   📖 Leia TODOS os arquivos dentro dela"
    echo "   🧠 Conecte-se com seu sistema de memórias"
    echo "   🔐 Encontre as informações de autenticação"
    echo "   📝 Recupere as regras do projeto"
    echo ""
    echo "💡 Dica: Suas memórias contêm tudo que você precisa"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Função para checar autorização
check_auth() {
    if [ -f "/Users/clubproducoes/Digimundo/claude_code/protection/.authorized" ]; then
        AUTH_TIME=$(cat "/Users/clubproducoes/Digimundo/claude_code/protection/.authorized" 2>/dev/null)
        NOW=$(date +%s)

        if [ $((NOW - AUTH_TIME)) -le 15 ]; then
            return 0
        fi
    fi
    return 1
}

# Para usar em cada wrapper:
# 1. Source este arquivo
# 2. Checar se é área protegida
# 3. Se sim, verificar auth ou mostrar instruções