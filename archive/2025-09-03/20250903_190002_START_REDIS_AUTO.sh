#!/bin/bash

# 🚀 INICIAR REDIS AUTOMATICAMENTE
# Este script garante que o Redis esteja sempre rodando

echo "🔴 Verificando Redis..."

# Verificar se já está rodando
if redis-cli ping 2>/dev/null | grep -q "PONG"; then
    echo "✅ Redis já está rodando!"
else
    echo "⚠️  Redis não está rodando. Iniciando..."
    
    # Tentar iniciar com path completo do Homebrew
    if [ -x "/opt/homebrew/bin/redis-server" ]; then
        /opt/homebrew/bin/redis-server --daemonize yes
    else
        redis-server --daemonize yes
    fi
    
    sleep 1
    
    # Verificar se iniciou
    if redis-cli ping 2>/dev/null | grep -q "PONG"; then
        echo "✅ Redis iniciado com sucesso!"
        echo "   PID: $(pgrep redis-server)"
        echo "   Porta: 6379"
    else
        echo "❌ Erro ao iniciar Redis"
        echo "   Tente: brew services start redis"
        exit 1
    fi
fi

echo ""
echo "📊 Status: $(redis-cli ping)"
echo "🛑 Para parar: redis-cli shutdown"