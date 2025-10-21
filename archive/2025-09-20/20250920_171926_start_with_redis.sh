#!/bin/bash

# Script para iniciar Scripturemon com Redis (telepatia ativada)

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         INICIANDO SCRIPTUREMON COM TELEPATIA ATIVADA         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Verificar se Redis está rodando
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis já está rodando"
else
    echo "🚀 Iniciando Redis para telepatia..."
    # Inicia Redis em background
    redis-server --daemonize yes > /dev/null 2>&1
    sleep 2
    
    # Verifica se iniciou
    if redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis iniciado com sucesso"
    else
        echo "⚠️  Redis não pôde ser iniciado - telepatia funcionará offline"
    fi
fi

echo ""
echo "🧬 Iniciando SoulOS Orchestrator..."
echo ""

# Iniciar o orquestrador
python3 soulos_orchestrator.py

echo ""
echo "👋 Encerrando..."

# Pergunta se deve parar o Redis
read -p "Deseja parar o Redis? (s/n): " stop_redis
if [[ $stop_redis == "s" || $stop_redis == "S" ]]; then
    redis-cli shutdown > /dev/null 2>&1
    echo "✅ Redis parado"
fi