#!/bin/bash
#
# Monitor de progresso da análise em tempo real
# Atualiza a cada 30 segundos

LOG_FILE="/tmp/scripturemon_analysis_live.log"
LAST_LINES=0

echo "🔍 MONITOR DE PROGRESSO - SCRIPTUREMON"
echo "======================================"
echo "📊 Atualizando a cada 30 segundos..."
echo ""

while true; do
    clear
    echo "🔍 MONITOR DE PROGRESSO - SCRIPTUREMON"
    echo "$(date '+%H:%M:%S')"
    echo "======================================"
    echo ""

    # Detectar autor atual
    CURRENT_AUTHOR=$(grep -E "Analisando com [A-Z_]+" "$LOG_FILE" | tail -1 | sed 's/.*Analisando com \([A-Z_]*\).*/\1/')
    AUTHOR_COUNT=$(grep -c "Analisando com" "$LOG_FILE")

    if [ -n "$CURRENT_AUTHOR" ]; then
        echo "📖 Autor Atual: $CURRENT_AUTHOR"
        echo "✅ Autores Completados: $((AUTHOR_COUNT - 1))/13"
        echo "⏳ Em Progresso: Autor $AUTHOR_COUNT/13"
        echo ""
    fi

    # Últimas 15 linhas do log
    echo "📝 Últimas Mensagens:"
    echo "--------------------"
    tail -15 "$LOG_FILE" | grep -v "^$"
    echo ""

    # Estatísticas de arquivos gerados
    OUTPUT_COUNT=$(find workspace/outputs -name "*.html" -newer /tmp/scripturemon_analysis_live.log 2>/dev/null | wc -l)
    echo "📄 Arquivos HTML gerados: $OUTPUT_COUNT"

    # Tempo decorrido
    START_TIME=$(head -1 "$LOG_FILE" | sed 's/\[\([0-9:]*\)\].*/\1/')
    CURRENT_TIME=$(date '+%H:%M:%S')
    echo "⏱️  Início: $START_TIME | Atual: $CURRENT_TIME"

    echo ""
    echo "💡 Pressione Ctrl+C para sair do monitor (análise continua rodando)"
    echo "======================================"

    sleep 30
done
