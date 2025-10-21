#!/bin/bash
# Ativa TODAS as proteções

export PATH="/Users/clubproducoes/Digimundo/claude_code/protection/wrappers:$PATH"
source /Users/clubproducoes/Digimundo/claude_code/protection/global_interceptor.sh
source /Users/clubproducoes/Digimundo/claude_code/protection/redirect_aliases.sh

echo "✅ Proteção definitiva ATIVADA!"
echo "   • Wrappers de comando: OK"
echo "   • Interceptador global: OK"
echo "   • Aliases de proteção: OK"
echo "   • Monitor filesystem: OK"
