#!/bin/bash
# Script de limpeza inteligente - DIGIMUNDO STYLE
# Timestamp único: 20250921_214934
# Preserva processo principal, mata órfãos

echo "🧹 Limpeza inteligente de processos Ollama..."

# Conta processos
OLLAMA_COUNT=$(ps aux | grep -E "(ollama serve|Ollama)" | grep -v grep | wc -l)

echo "📊 Encontrados $OLLAMA_COUNT processos Ollama"

if [ "$OLLAMA_COUNT" -gt 1 ]; then
    echo "⚠️ Múltiplas instâncias detectadas!"

    # Pega PID do mais antigo (principal)
    MAIN_PID=$(ps aux | grep -E "ollama serve" | grep -v grep | head -1 | awk '{print $2}')

    if [ ! -z "$MAIN_PID" ]; then
        echo "✅ Processo principal identificado: PID $MAIN_PID"

        # Lista órfãos
        echo "🔍 Processos órfãos a serem removidos:"
        ps aux | grep -E "(ollama serve|Ollama)" | grep -v grep | grep -v "$MAIN_PID" | awk '{print "  - PID", $2, $11}'

        # NÃO mata automaticamente - apenas informa
        echo ""
        echo "⚠️ Para limpar órfãos manualmente, execute:"
        echo "ps aux | grep -E 'ollama serve' | grep -v grep | grep -v $MAIN_PID | awk '{print \$2}' | xargs kill -9"
    fi
elif [ "$OLLAMA_COUNT" -eq 1 ]; then
    echo "✅ Apenas 1 processo Ollama (OK)"
else
    echo "⚠️ Nenhum processo Ollama encontrado"
    echo "💡 Iniciando Ollama..."
    ollama serve &
    sleep 2
    echo "✅ Ollama iniciado"
fi

echo "✅ Verificação completa"