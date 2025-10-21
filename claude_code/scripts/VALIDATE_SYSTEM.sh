#!/bin/bash
# 🔥 VALIDATE_SYSTEM.sh - Validação rápida do sistema UCHIMON
# Executa todas as verificações críticas em segundos

set -e

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  🔥 VALIDAÇÃO COMPLETA DO SISTEMA UCHIMON 🔥        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

BASE_DIR="/Users/clubproducoes/Digimundo/claude_code"
cd "$BASE_DIR" || exit 1

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# 1. Identidade
echo "1️⃣  Verificando identidade..."
if [ -f "🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh" ]; then
    PROJECT=$(grep 'PROJECT_NAME=' 🔥🔥🔥PROJECT_ID_UCHIMON🔥🔥🔥.sh | cut -d'=' -f2 | tr -d '"')
    echo -e "    ${GREEN}✅${NC} Identidade: $PROJECT"
else
    echo -e "    ${RED}❌${NC} PROJECT_ID não encontrado!"
    ERRORS=$((ERRORS + 1))
fi

# 2. Sistemas Python
echo "2️⃣  Verificando sistemas Python..."
SYSTEMS_COUNT=$(ls -1 systems/*.py 2>/dev/null | wc -l | tr -d ' ')
if [ "$SYSTEMS_COUNT" -ge 10 ]; then
    echo -e "    ${GREEN}✅${NC} Sistemas: $SYSTEMS_COUNT encontrados"
else
    echo -e "    ${YELLOW}⚠️${NC}  Sistemas: apenas $SYSTEMS_COUNT (esperado 10+)"
fi

# 3. LEIS
echo "3️⃣  Verificando LEIS..."
LEIS_COUNT=$(ls -1 🔥LEIS_UCHIMON🔥/*.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$LEIS_COUNT" -ge 17 ]; then
    echo -e "    ${GREEN}✅${NC} LEIS: $LEIS_COUNT encontradas"
else
    echo -e "    ${YELLOW}⚠️${NC}  LEIS: apenas $LEIS_COUNT (esperado 17+)"
fi

# 4. Conhecimentos
echo "4️⃣  Verificando MEMORY..."
CONHECIMENTOS=$(ls -1 MEMORY/conhecimentos/*.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$CONHECIMENTOS" -ge 10 ]; then
    echo -e "    ${GREEN}✅${NC} Conhecimentos: $CONHECIMENTOS arquivos"
else
    echo -e "    ${YELLOW}⚠️${NC}  Conhecimentos: $CONHECIMENTOS arquivos"
fi

# 5. Database
echo "5️⃣  Verificando database..."
if [ -f "MEMORY/claude_memory.db" ]; then
    DB_SIZE=$(stat -f%z MEMORY/claude_memory.db 2>/dev/null || stat -c%s MEMORY/claude_memory.db 2>/dev/null)
    if [ "$DB_SIZE" -gt 1000 ]; then
        echo -e "    ${GREEN}✅${NC} Database: $(echo "$DB_SIZE" | awk '{print int($1/1024)}')KB"
    else
        echo -e "    ${YELLOW}⚠️${NC}  Database muito pequeno"
    fi
else
    echo -e "    ${RED}❌${NC} Database não encontrado!"
    ERRORS=$((ERRORS + 1))
fi

# 6. Git Hooks
echo "6️⃣  Verificando git hooks..."
if [ -x ".git/hooks/pre-commit" ] && [ -x ".git/hooks/post-commit" ]; then
    echo -e "    ${GREEN}✅${NC} Git Hooks: Instalados e executáveis"
else
    echo -e "    ${RED}❌${NC} Git Hooks: NÃO instalados"
    ERRORS=$((ERRORS + 1))
fi

# 7. Git Status
echo "7️⃣  Verificando git..."
LAST_COMMIT=$(git log -1 --oneline 2>/dev/null | head -c 50)
if [ -n "$LAST_COMMIT" ]; then
    echo -e "    ${GREEN}✅${NC} Último commit: $LAST_COMMIT"
else
    echo -e "    ${YELLOW}⚠️${NC}  Git: sem commits"
fi

# 8. Genjutsu
echo "8️⃣  Verificando Genjutsu..."
if pgrep -f "GENJUTSU_UNIFIED.py" > /dev/null; then
    GENJUTSU_PID=$(pgrep -f "GENJUTSU_UNIFIED.py" | head -1)
    echo -e "    ${GREEN}✅${NC} Genjutsu: Ativo (PID: $GENJUTSU_PID)"
else
    echo -e "    ${YELLOW}⚠️${NC}  Genjutsu: Inativo (execute ./START_GENJUTSU.sh)"
fi

# 9. Testes
echo "9️⃣  Executando testes..."
if [ -d "venv" ]; then
    # Ativar venv e rodar testes
    source venv/bin/activate 2>/dev/null || true
    if command -v pytest &> /dev/null; then
        TEST_OUTPUT=$(pytest tests/ -q --tb=no 2>&1 | tail -1)
        if echo "$TEST_OUTPUT" | grep -q "passed"; then
            PASSED=$(echo "$TEST_OUTPUT" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+')
            echo -e "    ${GREEN}✅${NC} Testes: $PASSED passed"
        else
            echo -e "    ${RED}❌${NC} Testes: $TEST_OUTPUT"
            ERRORS=$((ERRORS + 1))
        fi
    else
        echo -e "    ${YELLOW}⚠️${NC}  pytest não instalado"
    fi
else
    echo -e "    ${YELLOW}⚠️${NC}  venv não encontrado"
fi

# 10. Memory System
echo "🔟 Verificando Memory System..."
if python3 systems/unified_memory_system.py 2>&1 | grep -q "UNIFIED MEMORY"; then
    MEMORIAS=$(python3 systems/unified_memory_system.py 2>&1 | grep "Claude DB:" | grep -oE '[0-9]+ memórias' | grep -oE '[0-9]+' || echo "0")
    if [ "$MEMORIAS" != "0" ]; then
        echo -e "    ${GREEN}✅${NC} Memory System: $MEMORIAS memórias"
    else
        echo -e "    ${GREEN}✅${NC} Memory System: operacional"
    fi
else
    echo -e "    ${RED}❌${NC} Memory System: erro ao executar"
    ERRORS=$((ERRORS + 1))
fi

# 1️⃣1️⃣ Distinção SCRIPTUREMON
echo "1️⃣1️⃣ Verificando distinção..."
if [ -f "../scripturemon-clean/🎬🎬🎬PROJECT_ID_SCRIPTUREMON🎬🎬🎬.sh" ]; then
    echo -e "    ${GREEN}✅${NC} Distinção: SCRIPTUREMON separado"
else
    echo -e "    ${YELLOW}⚠️${NC}  SCRIPTUREMON PROJECT_ID não encontrado"
fi

# 1️⃣2️⃣ Estrutura
echo "1️⃣2️⃣ Verificando estrutura..."
REQUIRED_DIRS=("systems" "tests" "MEMORY" "🔥LEIS_UCHIMON🔥" "livro_claude" "docs")
MISSING_DIRS=0
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo -e "    ${RED}❌${NC} Falta: $dir"
        MISSING_DIRS=$((MISSING_DIRS + 1))
        ERRORS=$((ERRORS + 1))
    fi
done
if [ "$MISSING_DIRS" -eq 0 ]; then
    echo -e "    ${GREEN}✅${NC} Estrutura: Todos os diretórios presentes"
fi

echo ""
echo "══════════════════════════════════════════════════════"

# Resultado Final
if [ "$ERRORS" -eq 0 ]; then
    echo -e "${GREEN}✅ SISTEMA 100% VALIDADO - PRONTO PARA USO${NC}"
    echo "Score: 12/12"
    exit 0
else
    echo -e "${RED}⚠️  VALIDAÇÃO COMPLETA COM $ERRORS ERRO(S)${NC}"
    echo "Score: $((12 - ERRORS))/12"
    exit 1
fi
