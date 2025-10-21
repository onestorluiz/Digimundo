#!/bin/bash

# 🚀 INICIAR REDIS MANUALMENTE

echo "🔴 Iniciando Redis..."

# Verificar se já está rodando
if pgrep -x "redis-server" > /dev/null; then
    echo "⚠️  Redis já está rodando!"
    echo "    PID: $(pgrep redis-server)"
else
    # Iniciar Redis em background
    redis-server --daemonize yes
    sleep 1
    
    if pgrep -x "redis-server" > /dev/null; then
        echo "✅ Redis iniciado com sucesso!"
        echo "   PID: $(pgrep redis-server)"
        echo "   Porta: 6379"
    else
        echo "❌ Erro ao iniciar Redis"
    fi
fi

echo ""
echo "📊 Para verificar: redis-cli ping"
echo "🛑 Para parar: ./STOP_REDIS.sh"