#!/bin/bash
echo "🧪 Testando ecossistema Scripturemon..."

# Teste 1: Ollama
echo -n "1. Ollama: "
if ollama list > /dev/null 2>&1; then
    echo "✅"
else
    echo "❌"
fi

# Teste 2: Modelo
echo -n "2. Modelo: "
if ollama list | grep -q "scripturemon"; then
    echo "✅"
else
    echo "❌"
fi

# Teste 3: RAG
echo -n "3. RAG API: "
if curl -s http://localhost:8092/health | grep -q "ok"; then
    echo "✅"
else
    echo "❌"
fi

# Teste 4: Redis
echo -n "4. Redis: "
if redis-cli ping > /dev/null 2>&1; then
    echo "✅"
else
    echo "❌"
fi

# Teste 5: Memórias
echo -n "5. Memórias: "
if [ -f "memory/crystals.db" ]; then
    echo "✅"
else
    echo "❌"
fi

echo ""
echo "🎯 Para testar interativamente:"
echo "   python scripts/scripturemon_interactive.py"
