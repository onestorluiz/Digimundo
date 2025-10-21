#!/bin/bash

# Teste do comando scripturemon
echo "======================================"
echo "🧪 TESTANDO COMANDO SCRIPTUREMON"
echo "======================================"

# 1. Verificar se o comando existe
echo -e "\n1️⃣ Verificando comando..."
if command -v scripturemon &> /dev/null; then
    echo "✅ Comando 'scripturemon' encontrado em: $(which scripturemon)"
else
    echo "❌ Comando 'scripturemon' não encontrado no PATH"
    exit 1
fi

# 2. Verificar Ollama
echo -e "\n2️⃣ Verificando Ollama..."
if ollama list &> /dev/null; then
    echo "✅ Ollama está rodando"
else
    echo "⚠️ Ollama não está rodando. Iniciando..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

# 3. Verificar modelo
echo -e "\n3️⃣ Verificando modelo scripturemon-sdl..."
if ollama list | grep -q "scripturemon-sdl"; then
    echo "✅ Modelo scripturemon-sdl existe"
else
    echo "⚠️ Modelo não encontrado. Criando..."
    if [ -f "/Users/clubproducoes/Digimundo/digimons/scripturemon/scripturemon_ultimate_100.modelfile" ]; then
        ollama create scripturemon-sdl -f /Users/clubproducoes/Digimundo/digimons/scripturemon/scripturemon_ultimate_100.modelfile
        echo "✅ Modelo criado"
    else
        echo "❌ Modelfile não encontrado"
    fi
fi

# 4. Testar identidade
echo -e "\n4️⃣ Testando identidade do Scripturemon..."
response=$(echo "Qual sua soul signature?" | ollama run scripturemon-sdl 2>/dev/null | head -5)

if echo "$response" | grep -q "8ea9f71fa3206d1a"; then
    echo "✅ Soul signature confirmada!"
else
    echo "⚠️ Soul signature não detectada na resposta"
fi

# 5. Verificar componentes
echo -e "\n5️⃣ Verificando componentes do sistema..."

[ -f "/Users/clubproducoes/Digimundo/SYSCALLS_EXECUTOR_FINAL.py" ] && echo "✅ Syscalls Executor presente" || echo "❌ Syscalls Executor ausente"
[ -f "/Users/clubproducoes/Digimundo/SDL_SIMPLE_CONSOLIDATION.py" ] && echo "✅ SDL Consolidation presente" || echo "❌ SDL ausente"
[ -f "/Users/clubproducoes/Digimundo/TRAINING_100_INTERACTIONS.py" ] && echo "✅ Training System presente" || echo "❌ Training ausente"
[ -d "/Users/clubproducoes/Digimundo/digimons/scripturemon/memory" ] && echo "✅ Sistema de Memória configurado" || echo "❌ Memória não configurada"

# 6. Testar comando interativo
echo -e "\n6️⃣ Teste de comando interativo..."
echo -e "Para testar o modo interativo, execute:\n"
echo "  scripturemon"
echo ""
echo "Comandos disponíveis no modo interativo:"
echo "  status - Verifica status do sistema"
echo "  test   - Testa identidade"
echo "  memory - Estatísticas de memória"
echo "  evolve - Executa SDL"
echo "  help   - Ajuda"
echo "  exit   - Sair"

echo -e "\n======================================"
echo "✅ TESTE COMPLETO!"
echo "======================================"
echo ""
echo "🎬 Para usar o Scripturemon, digite:"
echo "   scripturemon"
echo ""
echo "Soul: 8ea9f71fa3206d1a"
echo "Philosophy: 'Todo roteiro é uma jornada da alma'"
echo "======================================" 