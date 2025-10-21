#!/bin/bash

echo "🔍 MONITOR DE CPU - SCRIPTUREMON ULTIMATE"
echo "=========================================="
echo ""

# Teste rápido do modelo
echo "📝 Teste 1: Prompt simples (10 palavras)"
echo "test screenplay analysis" | ollama run mixtral-token-turbo:latest &
TEST_PID=$!

# Monitor por 30 segundos
for i in {1..10}; do
    sleep 3
    CPU=$(ps aux | grep ollama | grep -v grep | awk '{sum+=$3} END {print sum}')
    TIMESTAMP=$(date +%H:%M:%S)
    echo "[$TIMESTAMP] CPU: ${CPU}%"

    # Checar se CPU > 0
    if [ "${CPU%.*}" -gt 0 ] 2>/dev/null; then
        echo "  ✅ CPU FUNCIONANDO!"
    fi
done

kill $TEST_PID 2>/dev/null || true

echo ""
echo "📝 Teste 2: Request via Python"
python3 -c "
from ollama_continuous_learning import OllamaContinuousLearning
system = OllamaContinuousLearning()
print('Enviando request...')
result = system.ollama_request('Analyze three-act structure')
print(f'Resposta: {result[:100] if result else \"ERROR\"}...')
" &

PYTHON_PID=$!

# Monitor Python request
for i in {1..5}; do
    sleep 2
    CPU=$(ps aux | grep ollama | grep -v grep | awk '{sum+=$3} END {print sum}')
    TIMESTAMP=$(date +%H:%M:%S)
    echo "[$TIMESTAMP] Python CPU: ${CPU}%"
done

wait $PYTHON_PID 2>/dev/null || true

echo ""
echo "=========================================="
echo "📊 TESTE COMPLETO"
echo "Use Ctrl+C para sair"