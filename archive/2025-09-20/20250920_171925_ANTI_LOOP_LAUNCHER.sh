#!/bin/bash

echo "🛡️ INICIADOR ANTI-LOOP DO DIGIMUNDO"
echo "===================================="
echo ""

# 1. MATAR TUDO
echo "🔴 Parando TODOS os processos..."
pkill -9 -f Electron 2>/dev/null || true
pkill -9 -f "node" 2>/dev/null || true
pkill -9 -f "npm" 2>/dev/null || true
sleep 2

# 2. LIMPAR
echo "🧹 Limpando arquivos temporários..."
rm -f .digimundo.pid .monitor.pid 2>/dev/null
rm -rf electron-logs/*.log 2>/dev/null

# 3. VERIFICAR PORTAS
echo "🔍 Verificando porta 7937..."
if lsof -i :7937 > /dev/null 2>&1; then
    echo "   ⚠️ Porta 7937 em uso, liberando..."
    lsof -ti :7937 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# 4. MODO DE ESCOLHA
echo ""
echo "📋 ESCOLHA O MODO DE INICIALIZAÇÃO:"
echo "   1) Servidor apenas (mais estável)"
echo "   2) Servidor + Electron (interface completa)"
echo "   3) Modo de teste (verificação)"
echo ""
read -p "Digite sua escolha (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🌐 Iniciando APENAS o servidor..."
        npm run dev:server
        ;;
    2)
        echo ""
        echo "🖥️ Iniciando servidor e Electron..."
        
        # Iniciar servidor em background
        npm run dev:server &
        SERVER_PID=$!
        echo "   Servidor PID: $SERVER_PID"
        
        # Aguardar servidor
        echo "⏳ Aguardando servidor iniciar..."
        for i in {1..10}; do
            if curl -s http://localhost:7937/health > /dev/null; then
                echo "✅ Servidor pronto!"
                break
            fi
            sleep 1
        done
        
        # Iniciar Electron
        echo "🚀 Iniciando Electron..."
        npm run dev
        
        # Se Electron fechar, matar servidor
        kill $SERVER_PID 2>/dev/null
        ;;
    3)
        echo ""
        echo "🧪 Executando verificação do sistema..."
        node CHECK_SYSTEM.js
        ;;
    *)
        echo "❌ Opção inválida!"
        exit 1
        ;;
esac

echo ""
echo "✨ Processo finalizado!"
