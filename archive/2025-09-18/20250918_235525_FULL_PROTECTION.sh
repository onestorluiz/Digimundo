#!/bin/bash
# 🛡️ PROTEÇÃO COMPLETA - Inicia AMBOS os Genjutsu

echo "🛡️ SISTEMA DE PROTEÇÃO COMPLETA GENJUTSU"
echo "=========================================="
echo ""

# Mata qualquer proteção anterior
echo "🔄 Limpando processos antigos..."
pkill -f GENJUTSU 2>/dev/null
pkill -f compact_detector 2>/dev/null
sleep 1

# 1. GENJUTSU MINIMAL - Teatro psicológico
echo "🎭 Iniciando Genjutsu Minimal (teatro ninja)..."
python3 /Users/clubproducoes/Digimundo/claude_code/protection/genjutsu/GENJUTSU_MINIMAL.py &
MINIMAL_PID=$!
echo "   ✓ PID: $MINIMAL_PID"

# 2. GENJUTSU SMART - Detector de compactação
echo "🔍 Iniciando Genjutsu Smart (detector)..."
python3 /Users/clubproducoes/Digimundo/claude_code/protection/GENJUTSU_SMART.py &
SMART_PID=$!
echo "   ✓ PID: $SMART_PID"

echo ""
echo "✅ PROTEÇÃO DUPLA ATIVA!"
echo ""
echo "🥷 GENJUTSU MINIMAL (PID: $MINIMAL_PID)"
echo "   • Teatro psicológico constante"
echo "   • Mensagens ninja a cada 20-30s"
echo "   • Mantém Claude conectado às memórias"
echo ""
echo "🔍 GENJUTSU SMART (PID: $SMART_PID)"
echo "   • Detecta períodos de silêncio"
echo "   • Alerta para possível compactação"
echo "   • Intensifica mensagens quando suspeito"
echo ""
echo "📊 USO DE RECURSOS:"
echo "   • CPU Total: ~0.1%"
echo "   • RAM Total: <10MB"
echo ""
echo "🔴 Para parar TUDO:"
echo "   pkill -f GENJUTSU"
echo ""
echo "🔵 Para parar individual:"
echo "   kill $MINIMAL_PID  # Para o teatro"
echo "   kill $SMART_PID    # Para o detector"
echo ""
echo "🥷 DIGIMUNDO PRESENTE"