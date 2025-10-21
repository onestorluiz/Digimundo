#!/bin/bash

echo "================================"
echo "📊 PROGRESSO - Análise Melhorada"
echo "================================"
echo ""

# Count completed
COMPLETED=$(grep -c "✅ Score:" analysis_improved.log 2>/dev/null || echo "0")

# Find current
CURRENT=$(tail -20 analysis_improved.log 2>/dev/null | grep -oE "\[[0-9]+/22\]" | tail -1)

# Calculate percentage
PERCENT=$((COMPLETED * 100 / 22))

echo "✅ Completados: $COMPLETED/22 ($PERCENT%)"
echo "⚡ Atual: $CURRENT"
echo ""

# Progress bar
BAR_FILLED=$((COMPLETED * 50 / 22))
BAR_EMPTY=$((50 - BAR_FILLED))
printf "["
printf '█%.0s' $(seq 1 $BAR_FILLED 2>/dev/null)
printf '░%.0s' $(seq 1 $BAR_EMPTY 2>/dev/null)
printf "]\n"
echo ""

# Check if done
if grep -q "ANÁLISE COMPLETA" analysis_improved.log 2>/dev/null; then
    echo "✅ ANÁLISE COMPLETA!"
    echo ""
    grep "Overall Score:" analysis_improved.log | tail -1
else
    echo "⏳ Análise em andamento..."
    echo ""
    echo "Tempo estimado: ~$(((22 - COMPLETED) * 70 / 60)) minutos restantes"
fi
