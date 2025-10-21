#!/bin/bash

# SCRIPTUREMON - VERSÃO SIMPLIFICADA E FUNCIONAL
# Este script garante que o sistema funcione corretamente

cd /Users/clubproducoes/Digimundo/scripturemon-validation

# Verificar e iniciar Redis se necessário
if ! redis-cli ping 2>/dev/null | grep -q "PONG"; then
    echo "🔴 Iniciando Redis..."
    /opt/homebrew/bin/redis-server --daemonize yes
    sleep 1
fi

# Verificar Python
if [ -f ".venv/bin/python" ]; then
    PY=".venv/bin/python"
else
    echo "❌ Ambiente virtual não encontrado!"
    exit 1
fi

# Processar comando
case "${1:-chat}" in
    status)
        echo "📊 STATUS DO SISTEMA"
        $PY -m apps.scripturemon.cli2 status
        ;;
    
    help)
        echo "🎬 SCRIPTUREMON - Comandos disponíveis:"
        echo "  status  - Verificar status do sistema"
        echo "  chat    - Iniciar chat interativo"
        echo "  analyze - Analisar roteiro"
        echo "  doctor  - Diagnóstico completo"
        ;;
    
    analyze)
        if [ -z "$2" ]; then
            echo "❌ Uso: scripturemon analyze <arquivo>"
            exit 1
        fi
        $PY -m apps.scripturemon.cli2 analyze "$2"
        ;;
    
    chat|*)
        echo "🎬 SCRIPTUREMON CHAT"
        echo "===================="
        echo "💡 Comandos: /help, /status, /quit"
        echo ""
        $PY -m apps.scripturemon.cli2 chat
        ;;
esac