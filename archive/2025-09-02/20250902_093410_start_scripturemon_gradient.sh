#!/bin/bash
# Inicia Scripturemon com Gradient como cérebro

echo "🧠 INICIANDO SCRIPTUREMON COM GRADIENT (256K TOKENS)"
echo "Mac Studio M3 Ultra - 96GB RAM"
echo "================================================"

# Verificar se Ollama está rodando
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️ Iniciando Ollama..."
    ollama serve &
    sleep 3
fi

# Iniciar em modo chat com contexto configurado
echo "🚀 Iniciando chat com 256k tokens..."
ollama run scripturemon-gradient --num-ctx 256000

