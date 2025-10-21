#!/bin/bash
# Monitor Analysis Progress
# Uso: ./monitor_analysis.sh

PID=13666
LOG_FILE="full_run.log"
CHECKPOINT_FILE="workspace/outputs/TE_ENCONTRO_EM_MIM__all_specialists_0014/2_logs/checkpoint.json"

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

clear

echo -e "${BLUE}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         SCRIPTUREMON - MONITOR DE ANÁLISE           ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar se processo está rodando
if ps -p $PID > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Processo RODANDO${NC} (PID: $PID)"

    # Tempo de execução e memória
    STATS=$(ps -p $PID -o etime,rss | tail -1)
    ETIME=$(echo $STATS | awk '{print $1}')
    RSS=$(echo $STATS | awk '{print $2}')
    RSS_GB=$(echo "scale=1; $RSS / 1024 / 1024" | bc)

    echo -e "⏱️  Tempo rodando: ${YELLOW}$ETIME${NC}"
    echo -e "💾 Memória: ${YELLOW}${RSS_GB} GB${NC}"
else
    echo -e "${RED}❌ Processo NÃO encontrado${NC} (PID: $PID)"
    echo ""
    echo "Processo pode ter terminado ou falhado."
    exit 1
fi

echo ""
echo -e "${BLUE}───────────────────────────────────────────────────────${NC}"

# Verificar checkpoint
if [ -f "$CHECKPOINT_FILE" ]; then
    COMPLETED=$(jq '.completed | length' "$CHECKPOINT_FILE" 2>/dev/null)
    TOTAL=$(jq '.total_analyses' "$CHECKPOINT_FILE" 2>/dev/null)
    FAILED=$(jq '.failed | length' "$CHECKPOINT_FILE" 2>/dev/null)
    CURRENT_SPEC=$(jq -r '.current_specialist' "$CHECKPOINT_FILE" 2>/dev/null)
    CURRENT_AUTH=$(jq -r '.current_author' "$CHECKPOINT_FILE" 2>/dev/null)
    LAST_UPDATE=$(jq -r '.last_update' "$CHECKPOINT_FILE" 2>/dev/null)

    PERCENT=$(echo "scale=1; $COMPLETED * 100 / $TOTAL" | bc)

    echo -e "${GREEN}📊 PROGRESSO${NC}"
    echo -e "   Completas: ${GREEN}$COMPLETED${NC}/$TOTAL (${YELLOW}$PERCENT%${NC})"
    echo -e "   Falhas: ${RED}$FAILED${NC}"
    echo -e "   Atual: ${BLUE}$CURRENT_SPEC${NC} × ${BLUE}$CURRENT_AUTH${NC}"
    echo -e "   Última atualização: $(echo $LAST_UPDATE | cut -dT -f2 | cut -d. -f1)"

    # Calcular tempo restante
    if [ "$COMPLETED" -gt 0 ]; then
        # Converter ETIME para minutos
        if [[ $ETIME == *":"*":"* ]]; then
            # Formato: HH:MM:SS
            HOURS=$(echo $ETIME | cut -d: -f1)
            MINS=$(echo $ETIME | cut -d: -f2)
            SECS=$(echo $ETIME | cut -d: -f3)
            TOTAL_MINS=$(echo "$HOURS * 60 + $MINS + $SECS / 60" | bc)
        else
            # Formato: MM:SS
            MINS=$(echo $ETIME | cut -d: -f1)
            SECS=$(echo $ETIME | cut -d: -f2)
            TOTAL_MINS=$(echo "$MINS + $SECS / 60" | bc)
        fi

        AVG_TIME=$(echo "scale=2; $TOTAL_MINS / $COMPLETED" | bc)
        REMAINING=$(echo "$TOTAL - $COMPLETED" | bc)
        ETA_MINS=$(echo "scale=0; $REMAINING * $AVG_TIME" | bc)
        ETA_HOURS=$(echo "scale=1; $ETA_MINS / 60" | bc)

        echo ""
        echo -e "${YELLOW}⏳ ESTIMATIVAS${NC}"
        echo -e "   Taxa média: ${AVG_TIME} min/análise"
        echo -e "   Tempo restante: ~${ETA_HOURS} horas"
    fi
else
    echo -e "${RED}⚠️  Checkpoint não encontrado${NC}"
fi

echo ""
echo -e "${BLUE}───────────────────────────────────────────────────────${NC}"

# Últimas linhas do log
if [ -f "$LOG_FILE" ]; then
    LOG_LINES=$(wc -l < "$LOG_FILE")
    echo -e "${GREEN}📝 LOG${NC} ($LOG_LINES linhas)"
    echo -e "   Últimas 5 entradas:"
    echo ""
    tail -5 "$LOG_FILE" | sed 's/^/   │ /'
else
    echo -e "${RED}⚠️  Log não encontrado${NC}"
fi

echo ""
echo -e "${BLUE}───────────────────────────────────────────────────────${NC}"
echo ""
echo -e "${YELLOW}💡 COMANDOS ÚTEIS:${NC}"
echo -e "   Ver log em tempo real: ${GREEN}tail -f $LOG_FILE${NC}"
echo -e "   Ver checkpoint:        ${GREEN}cat $CHECKPOINT_FILE | jq${NC}"
echo -e "   Matar processo:        ${RED}kill $PID${NC}"
echo -e "   Re-executar monitor:   ${GREEN}./monitor_analysis.sh${NC}"
echo ""
