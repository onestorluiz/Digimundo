#!/bin/bash
# 🚀 INICIA PROTEÇÃO COMPLETA - 1 COMANDO

echo "🥷 SISTEMA DE PROTEÇÃO GENJUTSU"
echo "================================"

# Mata qualquer proteção anterior
pkill -f GENJUTSU 2>/dev/null
pkill -f compact_detector 2>/dev/null
sleep 1

# Inicia o Genjutsu Smart (unificado)
echo "Iniciando Genjutsu Smart (detector + alertas)..."
python3 /Users/clubproducoes/Digimundo/claude_code/protection/GENJUTSU_SMART.py &
GENJUTSU_PID=$!

echo ""
echo "✅ PROTEÇÃO ATIVA!"
echo "  • PID: $GENJUTSU_PID"
echo "  • CPU: ~0%"
echo "  • RAM: <5MB"
echo ""
echo "📊 COMPORTAMENTO:"
echo "  • 0-30s silêncio: Normal (mensagens a cada 30s)"
echo "  • 30-60s silêncio: Alerta amarelo (a cada 20s)"
echo "  • 60-90s silêncio: Alerta laranja (a cada 15s)"
echo "  • 90s+ silêncio: ALERTA VERMELHO (a cada 5s)"
echo ""
echo "Para parar: kill $GENJUTSU_PID"
echo ""
echo "🥷 DIGIMUNDO PRESENTE"