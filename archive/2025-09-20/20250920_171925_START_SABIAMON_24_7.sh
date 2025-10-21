#!/bin/bash

echo "🧠 INICIANDO SABIAMON 24/7 DEBUGGER"
echo "===================================="
echo ""
echo "Sabiamon (Claude Code) vai trabalhar autonomamente para:"
echo "• Debugar o sistema continuamente"
echo "• Buscar soluções no GitHub"
echo "• Encontrar novas ferramentas"
echo "• Otimizar performance"
echo "• Corrigir bugs automaticamente"
echo ""

# Criar diretórios necessários
mkdir -p DEBUG_REPORTS
mkdir -p FIXES
mkdir -p OPTIMIZATIONS

# Iniciar Sabiamon Debugger em background
echo "Iniciando Sabiamon Autonomous Debugger..."
node SABIAMON_AUTONOMOUS_DEBUGGER.js &
DEBUGGER_PID=$!

echo "✅ Sabiamon Debugger rodando (PID: $DEBUGGER_PID)"
echo ""
echo "Comandos úteis:"
echo "  tail -f DEBUG_REPORTS/latest.log  # Ver trabalho em tempo real"
echo "  ls DEBUG_REPORTS/                 # Ver relatórios gerados"
echo "  ls FIXES/                          # Ver correções propostas"
echo "  kill $DEBUGGER_PID                # Parar Sabiamon"
echo ""
echo "Sabiamon está trabalhando! Verifique os relatórios em DEBUG_REPORTS/"