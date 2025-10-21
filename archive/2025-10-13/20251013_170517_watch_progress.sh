#!/bin/bash
# Watch Progress Continuously
# Uso: ./watch_progress.sh [interval_seconds]

INTERVAL=${1:-30}  # Default: 30 segundos
CHECKPOINT_FILE="workspace/outputs/TE_ENCONTRO_EM_MIM__all_specialists_0014/2_logs/checkpoint.json"
PID=13666

echo "╔══════════════════════════════════════════════════════╗"
echo "║    SCRIPTUREMON - ACOMPANHAMENTO AUTOMÁTICO         ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Atualizando a cada $INTERVAL segundos"
echo "Pressione Ctrl+C para sair (análise continua rodando)"
echo ""

while true; do
    clear
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║    SCRIPTUREMON - ACOMPANHAMENTO AUTOMÁTICO         ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo ""
    date
    echo ""

    # Verificar se processo está rodando
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ Status: RODANDO (PID $PID)"

        # Stats do processo
        ps -p $PID -o etime,rss | tail -1 | awk '{
            printf "⏱️  Tempo: %s\n", $1
            printf "💾 Memória: %.1f GB\n", $2/1024/1024
        }'

        echo ""

        # Checkpoint
        if [ -f "$CHECKPOINT_FILE" ]; then
            COMPLETED=$(jq '.completed | length' "$CHECKPOINT_FILE")
            TOTAL=$(jq '.total_analyses' "$CHECKPOINT_FILE")
            FAILED=$(jq '.failed | length' "$CHECKPOINT_FILE")
            CURRENT_SPEC=$(jq -r '.current_specialist' "$CHECKPOINT_FILE")
            CURRENT_AUTH=$(jq -r '.current_author' "$CHECKPOINT_FILE")

            PERCENT=$(echo "scale=1; $COMPLETED * 100 / $TOTAL" | bc)

            echo "📊 Progresso: $COMPLETED/$TOTAL ($PERCENT%)"
            echo "❌ Falhas: $FAILED"
            echo "🔄 Atual: $CURRENT_SPEC × $CURRENT_AUTH"

            # Barra de progresso
            FILLED=$(echo "$COMPLETED * 50 / $TOTAL" | bc)
            EMPTY=$(echo "50 - $FILLED" | bc)

            printf "\n["
            for i in $(seq 1 $FILLED); do printf "█"; done
            for i in $(seq 1 $EMPTY); do printf "░"; done
            printf "] $PERCENT%%\n"
        fi
    else
        echo "❌ Status: PROCESSO NÃO ENCONTRADO"
        echo ""
        echo "A análise pode ter terminado ou falhado."
        echo "Verifique: ps aux | grep analyze_all_specialists"
        break
    fi

    echo ""
    echo "────────────────────────────────────────────────────────"
    echo "Próxima atualização em $INTERVAL segundos..."

    sleep $INTERVAL
done
