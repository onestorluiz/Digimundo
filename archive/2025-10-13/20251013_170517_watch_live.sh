#!/bin/bash
# Watch Analysis Live Output
# Uso: ./watch_live.sh

LOG_FILE="full_run.log"

echo "╔══════════════════════════════════════════════════════╗"
echo "║         SCRIPTUREMON - LOG EM TEMPO REAL            ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Monitorando: $LOG_FILE"
echo "Pressione Ctrl+C para sair (análise continua rodando)"
echo ""
echo "────────────────────────────────────────────────────────"
echo ""

# tail -f mostra últimas 10 linhas e continua seguindo
tail -f "$LOG_FILE"
