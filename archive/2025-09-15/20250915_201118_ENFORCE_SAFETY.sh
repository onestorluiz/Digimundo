#!/bin/bash
# SOURCE THIS FILE to enforce safety
# Add to ~/.zshrc: source /Users/clubproducoes/Digimundo/ENFORCE_SAFETY.sh

# Sobrescrever rm com função segura
rm() {
    echo "🛑 rm INTERCEPTADO!"
    echo "Use /Users/clubproducoes/Digimundo/safe_delete.sh ao invés"
    echo "Ou use /bin/rm se REALMENTE souber o que está fazendo"
    return 1
}

# Criar alias para comandos seguros
alias safe-delete='/Users/clubproducoes/Digimundo/safe_delete.sh'
alias check-rules='cat /Users/clubproducoes/Digimundo/NEVER_DELETE_RULES.md'

echo "⚠️ PROTEÇÕES ATIVADAS:"
echo "- rm está BLOQUEADO"
echo "- Use 'safe-delete' ao invés"
echo "- Use 'check-rules' para ver regras"