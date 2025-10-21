#!/bin/bash

# ========================================================================
# 🚀 SILICON VALLEY TEST SUITE - SCRIPTUREMON ULTIMATE
# ========================================================================

echo "🚀 SILICON VALLEY TEST SUITE - SCRIPTUREMON ULTIMATE"
echo "======================================================"
echo "Data: $(date)"
echo ""

# Configuração
BASE_DIR="/Users/clubproducoes/Digimundo/scripturemon-validation"
cd "$BASE_DIR"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Contadores
TOTAL=0
PASSED=0
FAILED=0

# Função de teste
test_cmd() {
    local name="$1"
    local cmd="$2"
    TOTAL=$((TOTAL + 1))
    echo -e "\n${BLUE}Test $TOTAL: $name${NC}"
    
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASSED${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}❌ FAILED${NC}"
        FAILED=$((FAILED + 1))
    fi
}

# TESTES
echo -e "\n${YELLOW}═══ FASE 1: INFRAESTRUTURA ═══${NC}"

test_cmd "Python Version" "python3 --version"
test_cmd "Redis Module" "python3 -c 'from apps.scripturemon.redis_on_demand import ensure_redis; ensure_redis()'"
test_cmd "Database" "test -f data/memory/unified_memory.db"

echo -e "\n${YELLOW}═══ FASE 2: MÓDULOS ═══${NC}"

test_cmd "Memory Manager" "python3 -c 'from apps.scripturemon.memory_manager import UnifiedMemoryManager; UnifiedMemoryManager()'"
test_cmd "DigiLang" "python3 -c 'from apps.scripturemon.digilang_integration import get_digilang; get_digilang()'"
test_cmd "Cinema Knowledge" "python3 -c 'from apps.scripturemon.cinema_knowledge import get_cinema_knowledge; get_cinema_knowledge()'"

echo -e "\n${YELLOW}═══ FASE 3: MEMÓRIAS ═══${NC}"

test_cmd "L1 Memory" "python3 -c 'from apps.scripturemon.memory_manager import UnifiedMemoryManager; m=UnifiedMemoryManager(); m.store_l1_core(\"test\")'"
test_cmd "L2 Memory" "python3 -c 'from apps.scripturemon.memory_manager import UnifiedMemoryManager; m=UnifiedMemoryManager(); m.store_l2_consolidated(\"test\")'"
test_cmd "L3 Memory" "python3 -c 'from apps.scripturemon.memory_manager import UnifiedMemoryManager; m=UnifiedMemoryManager(); m.store_l3_active(\"test\")'"
test_cmd "L4 Memory" "python3 -c 'from apps.scripturemon.memory_manager import UnifiedMemoryManager; m=UnifiedMemoryManager(); m.store_l4_quantum(\"test\")'"

echo ""
echo "======================================================"
echo "📊 RESULTADO FINAL"
echo "======================================================"
echo "Total: $TOTAL"
echo -e "${GREEN}Passou: $PASSED${NC}"
echo -e "${RED}Falhou: $FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 SISTEMA 100% FUNCIONAL!${NC}"
else
    echo -e "\n${YELLOW}⚠️ $FAILED testes falharam${NC}"
fi
