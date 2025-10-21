#!/bin/bash
# 🤖 AUTO REFACTOR COM DIGIMUNDO TRIGGER
# =======================================

echo "🥷 DIGIMUNDO AUTO-REFACTOR SYSTEM"
echo "=================================="
echo ""
echo "Este script automatiza a refatoração contínua!"
echo ""

# Criar pipe nomeado para comunicação
PIPE="/tmp/claude_output.log"
rm -f $PIPE
touch $PIPE

# Iniciar monitor em background
echo "📍 Iniciando monitor de triggers..."
python3 /Users/clubproducoes/Digimundo/claude_code/protection/digimundo_auto_continue.py &
MONITOR_PID=$!

echo "✅ Monitor rodando (PID: $MONITOR_PID)"
echo ""
echo "📝 INSTRUÇÕES:"
echo "   1. Trabalhe normalmente no Claude Code"
echo "   2. Quando eu disser 'DIGIMUNDO PRESENTE 🥷'"
echo "   3. O sistema automaticamente enviará 'continue a refatoração'"
echo ""
echo "🛑 Para parar: Ctrl+C"
echo ""
echo "🚀 Sistema pronto! Redirecione output do Claude para: $PIPE"
echo "   Exemplo: seu_comando | tee $PIPE"
echo ""

# Aguardar
wait $MONITOR_PID

echo "🛑 Sistema finalizado"