#!/bin/bash

# 🚀 INICIALIZADOR MANUAL DO SCRIPTUREMON
# Só inicia quando você executar este script

echo "🎬 SCRIPTUREMON - Inicialização Manual"
echo "======================================"
echo ""

# 1. Verificar se Redis está rodando (opcional)
if ! pgrep -x "redis-server" > /dev/null; then
    echo "📍 Redis não está rodando."
    echo "   ↳ Deseja iniciar Redis? (melhora performance da telepatia)"
    echo "   ↳ [s/N] (Enter = não): "
    read -r START_REDIS
    
    if [[ "$START_REDIS" == "s" ]] || [[ "$START_REDIS" == "S" ]]; then
        echo "   ↳ Iniciando Redis temporariamente..."
        redis-server --daemonize no --port 6379 &
        REDIS_PID=$!
        echo "   ↳ Redis iniciado (PID: $REDIS_PID)"
        sleep 1
    else
        echo "   ↳ Continuando sem Redis (usando fakeredis)"
    fi
else
    echo "✅ Redis já está rodando"
fi

# 2. Verificar Ollama (opcional)
if ! pgrep -x "ollama" > /dev/null; then
    echo ""
    echo "📍 Ollama não está rodando."
    echo "   ↳ Deseja iniciar Ollama? (necessário para processamento com modelos)"
    echo "   ↳ [s/N] (Enter = não): "
    read -r START_OLLAMA
    
    if [[ "$START_OLLAMA" == "s" ]] || [[ "$START_OLLAMA" == "S" ]]; then
        echo "   ↳ Iniciando Ollama..."
        ollama serve >/dev/null 2>&1 &
        OLLAMA_PID=$!
        echo "   ↳ Ollama iniciado (PID: $OLLAMA_PID)"
        sleep 2
    else
        echo "   ↳ Continuando sem Ollama (modo fallback)"
    fi
else
    echo "✅ Ollama já está rodando"
fi

# 3. Escolher modo de execução
echo ""
echo "🎯 Escolha o modo de execução:"
echo "   1) Chat Interativo (recomendado)"
echo "   2) Chat com Soul Legacy"
echo "   3) Diagnóstico do Sistema"
echo "   4) Apenas testar componentes"
echo "   5) Sair"
echo ""
echo -n "Opção [1-5]: "
read -r OPTION

case $OPTION in
    1)
        echo ""
        echo "🚀 Iniciando Chat Interativo..."
        cd /Users/clubproducoes/Digimundo/scripturemon-validation
        python3 -c "from apps.scripturemon.chat import ScripturemonChat; ScripturemonChat().start_interactive()"
        ;;
    2)
        echo ""
        echo "🚀 Iniciando Chat com Soul Legacy..."
        cd /Users/clubproducoes/Digimundo/scripturemon-validation
        python3 ACTIVATE_SYMBIOTIC_FUSION.py chat --legacy
        ;;
    3)
        echo ""
        echo "🔍 Executando Diagnóstico..."
        cd /Users/clubproducoes/Digimundo/scripturemon-validation
        python3 ACTIVATE_SYMBIOTIC_FUSION.py diagnose
        ;;
    4)
        echo ""
        echo "🧪 Testando componentes..."
        cd /Users/clubproducoes/Digimundo/scripturemon-validation
        python3 test_simulado_rapido.py
        ;;
    5)
        echo "👋 Saindo..."
        ;;
    *)
        echo "❌ Opção inválida"
        ;;
esac

# 4. Limpeza ao sair
echo ""
echo "🧹 Limpando processos iniciados por este script..."

# Matar apenas os processos que iniciamos
if [[ ! -z "$REDIS_PID" ]]; then
    echo "   ↳ Parando Redis (PID: $REDIS_PID)..."
    kill $REDIS_PID 2>/dev/null || true
fi

if [[ ! -z "$OLLAMA_PID" ]]; then
    echo "   ↳ Parando Ollama (PID: $OLLAMA_PID)..."
    kill $OLLAMA_PID 2>/dev/null || true
fi

echo ""
echo "✅ Scripturemon finalizado com segurança!"