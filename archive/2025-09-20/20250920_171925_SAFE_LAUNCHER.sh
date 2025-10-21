#!/bin/bash

echo "🚀 LAUNCHER SEGURO DO DIGIMUNDO"
echo "================================"

# Matar processos antigos
echo "🔴 Limpando processos..."
pkill -f Electron 2>/dev/null || true
pkill -f "node.*digimundo" 2>/dev/null || true
pkill -f "npm.*dev" 2>/dev/null || true

# Limpar PIDs
rm -f .digimundo.pid .monitor.pid 2>/dev/null

echo "✅ Processos limpos"

# Iniciar sistema
echo "🌟 Iniciando sistema limpo..."
node STARTUP.js

echo "🖥️ Iniciando servidor..."
npm run dev:server &
SERVER_PID=$!
echo "   PID do servidor: $SERVER_PID"

# Aguardar servidor
echo "⏳ Aguardando servidor..."
sleep 5

# Verificar servidor
if curl -s http://localhost:7937/health > /dev/null; then
    echo "✅ Servidor rodando!"
else
    echo "❌ Servidor não respondeu"
    exit 1
fi

echo ""
echo "✨ SISTEMA PRONTO!"
echo "   Acesse: http://localhost:7937"
echo ""
echo "Para parar: Ctrl+C"

# Manter rodando
wait $SERVER_PID
