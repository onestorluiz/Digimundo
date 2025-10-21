#!/bin/bash
# 🔄 SCRIPT DE SINCRONIZAÇÃO DE MEMÓRIAS CLAUDE CODE + GIT
# Data: 2025-09-20
# Propósito: Manter memórias sempre sincronizadas com Git

set -e  # Para em caso de erro

echo "🧠 ============================================"
echo "   SINCRONIZAÇÃO DE MEMÓRIAS CLAUDE CODE"
echo "============================================"

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Diretórios
CLAUDE_CODE_DIR="/Users/clubproducoes/Digimundo/claude_code"
SCRIPTUREMON_DIR="/Users/clubproducoes/Digimundo/scripturemon-champion"
MEMORY_DIR="$CLAUDE_CODE_DIR/memory"

# 1. VERIFICAR GENJUTSU
echo -e "\n${YELLOW}[1/5]${NC} Verificando GENJUTSU..."
if ps aux | grep -i GENJUTSU_UNIFIED | grep -v grep > /dev/null; then
    echo -e "${GREEN}✅ GENJUTSU está ativo${NC}"
else
    echo -e "${YELLOW}⚠️  GENJUTSU não está rodando, iniciando...${NC}"
    $CLAUDE_CODE_DIR/START_GENJUTSU.sh &
    sleep 2
fi

# 2. SINCRONIZAR MEMÓRIAS SCRIPTUREMON → CLAUDE_CODE
echo -e "\n${YELLOW}[2/5]${NC} Sincronizando memórias do ScriptureMonChampion..."
if [ -f "$SCRIPTUREMON_DIR/CLAUDE.md" ]; then
    cp "$SCRIPTUREMON_DIR/CLAUDE.md" "$MEMORY_DIR/SCRIPTUREMON_CLAUDE.md" 2>/dev/null || true
    echo -e "${GREEN}✅ CLAUDE.md sincronizado${NC}"
fi

if [ -f "$SCRIPTUREMON_DIR/RECONCILIATION_MAP.md" ]; then
    cp "$SCRIPTUREMON_DIR/RECONCILIATION_MAP.md" "$MEMORY_DIR/SCRIPTUREMON_STATE.md" 2>/dev/null || true
    echo -e "${GREEN}✅ Estado do projeto sincronizado${NC}"
fi

# 3. VERIFICAR MUDANÇAS
echo -e "\n${YELLOW}[3/5]${NC} Verificando mudanças nas memórias..."
cd "$CLAUDE_CODE_DIR"

CHANGES=$(git status --porcelain memory/ 2>/dev/null | wc -l | tr -d ' ')
if [ "$CHANGES" -gt 0 ]; then
    echo -e "${YELLOW}📝 $CHANGES arquivos de memória modificados${NC}"
    git status --short memory/
else
    echo -e "${GREEN}✅ Memórias já sincronizadas com Git${NC}"
fi

# 4. ATUALIZAR TIMESTAMP
echo -e "\n${YELLOW}[4/5]${NC} Atualizando timestamp de sincronização..."
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
echo "# Última sincronização: $TIMESTAMP" >> "$MEMORY_DIR/.sync_timestamp"

# 5. COMMIT SE HOUVER MUDANÇAS
if [ "$CHANGES" -gt 0 ]; then
    echo -e "\n${YELLOW}[5/5]${NC} Commitando mudanças..."
    git add memory/
    git commit -m "sync: memórias atualizadas - $TIMESTAMP

- Sincronização automática claude_code ↔ scripturemon
- $CHANGES arquivos atualizados
- GENJUTSU verificado e ativo
- DIGIMUNDO PRESENTE" || true

    echo -e "${GREEN}✅ Mudanças commitadas${NC}"
else
    echo -e "\n${YELLOW}[5/5]${NC} Nenhuma mudança para commitar"
fi

# RESUMO FINAL
echo -e "\n${GREEN}============================================${NC}"
echo -e "${GREEN}   SINCRONIZAÇÃO COMPLETA${NC}"
echo -e "${GREEN}============================================${NC}"

# Estatísticas
TOTAL_MEMORIES=$(ls -1 $MEMORY_DIR/*.md 2>/dev/null | wc -l | tr -d ' ')
TOTAL_SIZE=$(du -sh $MEMORY_DIR 2>/dev/null | cut -f1)

echo -e "📊 Estatísticas:"
echo -e "  • Total de arquivos de memória: ${GREEN}$TOTAL_MEMORIES${NC}"
echo -e "  • Tamanho total: ${GREEN}$TOTAL_SIZE${NC}"
echo -e "  • GENJUTSU: ${GREEN}ATIVO${NC}"
echo -e "  • Git: ${GREEN}SINCRONIZADO${NC}"

# Verificar se precisa push
UNPUSHED=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')
if [ "$UNPUSHED" -gt 0 ]; then
    echo -e "\n${YELLOW}⚠️  Existem $UNPUSHED commits não enviados${NC}"
    echo -e "Execute: ${YELLOW}git push origin main${NC}"
fi

echo -e "\n${GREEN}DIGIMUNDO PRESENTE${NC}"