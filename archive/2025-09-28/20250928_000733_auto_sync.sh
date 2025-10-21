#!/bin/bash
# 🔄 AUTO-SYNC - Sincronização automática periódica

MEMORY_DIR="/Users/clubproducoes/Digimundo/claude_code/memory"
LOG_FILE="$MEMORY_DIR/sync/sync.log"

# Função de log
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "$1"
}

# Função de sincronização
sync_all() {
    log_message "🔄 Iniciando sincronização automática..."

    # 1. Sincronizar adapters
    cd "$MEMORY_DIR/core" || exit 1
    python3 adapters.py >> "$LOG_FILE" 2>&1

    if [ $? -eq 0 ]; then
        log_message "✅ Adapters sincronizados"
    else
        log_message "❌ Erro na sincronização de adapters"
    fi

    # 2. Verificar Genjutsu
    ps aux | grep GENJUTSU | grep -v grep > /dev/null
    if [ $? -eq 0 ]; then
        log_message "✅ Genjutsu ativo"
    else
        log_message "⚠️ Genjutsu inativo - tentando iniciar..."
        /Users/clubproducoes/Digimundo/claude_code/START_GENJUTSU.sh &
    fi

    # 3. Atualizar índice de conhecimento
    cd "$MEMORY_DIR/knowledge" || exit 1

    # Conta documentos
    RULE_COUNT=$(ls rules/*.md 2>/dev/null | wc -l)
    LEARN_COUNT=$(ls learnings/*.md 2>/dev/null | wc -l)
    DECISION_COUNT=$(ls decisions/*.md 2>/dev/null | wc -l)

    log_message "📚 Knowledge: $RULE_COUNT rules, $LEARN_COUNT learnings, $DECISION_COUNT decisions"

    # 4. Git status
    cd /Users/clubproducoes/Digimundo || exit 1
    CHANGES=$(git status --porcelain | wc -l)

    if [ "$CHANGES" -gt 0 ]; then
        log_message "📝 $CHANGES mudanças não commitadas"

        # Auto-commit se muitas mudanças
        if [ "$CHANGES" -gt 10 ]; then
            log_message "🎯 Auto-commit de $CHANGES mudanças..."
            git add .
            git commit -m "🔄 Auto-sync: $CHANGES mudanças acumuladas"
            log_message "✅ Auto-commit realizado"
        fi
    else
        log_message "✅ Repositório sincronizado"
    fi

    # 5. Calcular harmonia
    HARMONY=$(python3 -c "
from pathlib import Path
import sys
sys.path.insert(0, '$MEMORY_DIR/core')
try:
    from adapters import get_adapters
    adapters = get_adapters()
    results = adapters.sync_all()

    # Calcular score simples
    score = 75  # base
    if 'genjutsu' in results and results['genjutsu']['status'] == 'active':
        score += 10
    if 'scripturemon' in results and results['scripturemon']['insights'] > 50:
        score += 5
    if 'crystal' in results and results['crystal']['status'] == 'synced':
        score += 5

    print(min(score, 95))
except:
    print(75)
" 2>/dev/null)

    log_message "🌀 Harmonia: ${HARMONY}%"

    # Atualizar HARMONY.md
    sed -i '' "s/Harmonia Geral:.*/Harmonia Geral: ${HARMONY}%/" /Users/clubproducoes/Digimundo/claude_code/HARMONY.md
    sed -i '' "s/Última Verificação:.*/Última Verificação: $(date '+%Y-%m-%d %H:%M')/" /Users/clubproducoes/Digimundo/claude_code/HARMONY.md

    log_message "✅ Sincronização completa!"
    echo ""
}

# Função para rodar em loop
continuous_sync() {
    log_message "🚀 Auto-sync iniciado - sincronizando a cada 30 minutos"

    while true; do
        sync_all
        log_message "💤 Aguardando 30 minutos..."
        sleep 1800  # 30 minutos
    done
}

# Menu principal
case "$1" in
    "once")
        sync_all
        ;;
    "continuous")
        continuous_sync
        ;;
    "status")
        echo "📊 Status do Auto-sync"
        echo "====================="
        tail -20 "$LOG_FILE"
        ;;
    *)
        echo "🔄 AUTO-SYNC - Sistema de sincronização automática"
        echo ""
        echo "Uso:"
        echo "  $0 once       - Sincronizar uma vez"
        echo "  $0 continuous - Sincronizar continuamente (30min)"
        echo "  $0 status     - Ver último status"
        echo ""
        echo "Para adicionar ao cron (sincronização a cada hora):"
        echo "  crontab -e"
        echo "  0 * * * * $PWD/$0 once"
        ;;
esac