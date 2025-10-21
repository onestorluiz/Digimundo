#!/bin/bash

echo "================================"
echo "📊 PROGRESSO - HTML DETALHADO"
echo "================================"
echo ""

# Count completed
COMPLETED=$(grep -c "✅ Score:" detailed_html.log 2>/dev/null || echo "0")

# Find current
CURRENT=$(tail -20 detailed_html.log 2>/dev/null | grep -oE "\[[0-9]+/22\]" | tail -1)

# Calculate percentage
PERCENT=$((COMPLETED * 100 / 22))

echo "✅ Completados: $COMPLETED/22 ($PERCENT%)"
echo "⚡ Atual: $CURRENT"
echo ""

# Progress bar
BAR_FILLED=$((COMPLETED * 50 / 22))
BAR_EMPTY=$((50 - BAR_FILLED))
printf "["
printf '█%.0s' $(seq 1 $BAR_FILLED)
printf '░%.0s' $(seq 1 $BAR_EMPTY)
printf "]\n"
echo ""

# Check if done
if grep -q "CONCLUÍDO" detailed_html.log 2>/dev/null; then
    echo "✅ GERAÇÃO COMPLETA!"
    echo ""
    grep "HTML detalhado gerado:" detailed_html.log
else
    echo "⏳ Análise em andamento..."
    echo ""
    echo "Para acompanhar em tempo real:"
    echo "  tail -f detailed_html.log"
fi
