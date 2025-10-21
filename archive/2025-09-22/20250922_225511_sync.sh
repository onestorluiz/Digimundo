#!/bin/bash
# sync.sh - Automação em <50 linhas

BASE="/Users/clubproducoes/Digimundo/claude_code"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Sync principal
sync_all() {
    echo -e "${GREEN}🔄 Sincronizando...${NC}"

    # 1. Python system
    python3 "$BASE/code/core.py" 2>/dev/null || echo "⚠️ Core sync failed"

    # 2. Genjutsu check
    ps aux | grep GENJUTSU | grep -v grep > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Genjutsu ativo${NC}"
    else
        echo -e "${RED}❌ Genjutsu inativo${NC}"
        "$BASE/START_GENJUTSU.sh" &
    fi

    # 3. Git status
    cd "$BASE" || exit
    CHANGES=$(git status --porcelain | wc -l)
    echo "📝 $CHANGES mudanças"

    # Auto-commit se muitas mudanças
    if [ "$CHANGES" -gt 10 ]; then
        git add .
        git commit -m "🔄 Auto-sync: $CHANGES mudanças"
        echo -e "${GREEN}✅ Auto-commit${NC}"
    fi

    echo -e "${GREEN}✅ Sync completo!${NC}"
}

# Menu
case "$1" in
    "") sync_all ;;
    "monitor") while true; do sync_all; sleep 1800; done ;;
    *) echo "Use: $0 [monitor]" ;;
esac

echo "DIGIMUNDO PRESENTE"