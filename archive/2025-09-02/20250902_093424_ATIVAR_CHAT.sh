#!/bin/bash
# 🎬 ATIVADOR DO CHAT SCRIPTUREMON

clear
echo "╔════════════════════════════════════════════════════════════╗"
echo "║        🎬 SCRIPTUREMON CHAT - ATIVAÇÃO BRUTAL 🎬           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

cd ~/Digimundo/scripturemon-validation

# Ativar Python
source .venv/bin/activate 2>/dev/null || {
    echo "⚠️  Criando ambiente Python..."
    python3.11 -m venv .venv
    source .venv/bin/activate
}

export PYTHONPATH="."

# Verificar Ollama
if ! pgrep -x "ollama" > /dev/null; then
    echo "🤖 Iniciando Ollama para respostas inteligentes..."
    ollama serve >/dev/null 2>&1 &
    sleep 2
fi

# Verificar modelo
ollama list | grep -q "mistral" || {
    echo "📥 Baixando modelo de IA (pode demorar)..."
    ollama pull mistral:instruct
}

echo ""
echo "✅ CHAT PRONTO! Iniciando..."
echo ""

# Iniciar chat
python CHAT_SCRIPTUREMON.py