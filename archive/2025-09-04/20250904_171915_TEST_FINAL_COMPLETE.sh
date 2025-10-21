#!/bin/bash

echo "🏁 TESTE FINAL COMPLETO - SCRIPTUREMON ULTIMATE"
echo "================================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contador de testes
PASSED=0
FAILED=0
TOTAL=0

# Função para executar teste
run_test() {
    local test_name="$1"
    local test_cmd="$2"
    local expected="$3"
    
    TOTAL=$((TOTAL + 1))
    echo -e "\n${BLUE}TEST $TOTAL: $test_name${NC}"
    echo "Comando: $test_cmd"
    
    # Executar comando
    output=$(eval "$test_cmd" 2>&1)
    
    # Verificar resultado
    if echo "$output" | grep -q "$expected"; then
        echo -e "${GREEN}✅ PASSED${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}❌ FAILED${NC}"
        echo "Output: $output"
        FAILED=$((FAILED + 1))
    fi
}

echo "🔄 Preparando ambiente de teste..."
cd /Users/clubproducoes/Digimundo/scripturemon-validation

# TEST 1: Redis Auto-Start
run_test "Redis Auto-Start" \
    "python3 -c \"from apps.scripturemon.redis_on_demand import ensure_redis; print('OK' if ensure_redis() else 'FAIL')\"" \
    "OK"

# TEST 2: Digilang Import
run_test "Digilang Import" \
    "python3 -c \"from apps.scripturemon.digilang_integration import get_digilang; d = get_digilang(); print('OK' if d else 'FAIL')\"" \
    "OK"

# TEST 3: Memory Manager
run_test "Memory Manager" \
    "python3 -c \"from apps.scripturemon.memory_manager import UnifiedMemoryManager; m = UnifiedMemoryManager(); print('OK')\"" \
    "OK"

# TEST 4: Cinema Knowledge
run_test "Cinema Knowledge" \
    "python3 -c \"from apps.scripturemon.cinema_knowledge import get_cinema_knowledge; c = get_cinema_knowledge(); print('OK' if c.get_stats()['total_pdfs'] > 0 else 'FAIL')\"" \
    "OK"

# TEST 5: Comando help
run_test "Comando help" \
    "echo 'help' | timeout 5 python3 bin/scripturemon.fixed --batch --commands help" \
    "Comandos disponíveis"

# TEST 6: Comando status
run_test "Comando status" \
    "echo 'status' | timeout 5 python3 bin/scripturemon.fixed --batch --commands status" \
    "SISTEMAS ATIVOS"

# TEST 7: Processamento de prompt simples
run_test "Prompt simples" \
    "echo 'Olá' | timeout 10 python3 bin/scripturemon.fixed --batch --commands 'Olá'" \
    "Scripturemon"

# TEST 8: Verificar português
run_test "Resposta em português" \
    "echo 'O que você faz?' | timeout 10 python3 bin/scripturemon.fixed --batch --commands 'O que você faz?'" \
    "roteiro"

# TEST 9: Memory L1-L4
run_test "Memory Layers L1-L4" \
    "python3 -c \"from apps.scripturemon.memory_manager import UnifiedMemoryManager; m = UnifiedMemoryManager(); m.store_l1_core('test'); print('OK')\"" \
    "OK"

# TEST 10: Smart Model Triggers
run_test "Smart Model Triggers" \
    "python3 -c \"exec('''
import sys
sys.path.insert(0, '.')
from bin.scripturemon_fixed import ScripturemonMaxCapacity
s = ScripturemonMaxCapacity()
result = s._should_use_deep_model('análise profunda')
print('OK' if result else 'FAIL')
''')\" 2>/dev/null" \
    "OK"

# Resumo Final
echo ""
echo "================================================="
echo "📊 RESULTADO FINAL:"
echo "================================================="
echo -e "${GREEN}✅ PASSED: $PASSED/$TOTAL${NC}"
echo -e "${RED}❌ FAILED: $FAILED/$TOTAL${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 TODOS OS TESTES PASSARAM!${NC}"
    echo "Sistema está 100% funcional!"
else
    echo -e "${YELLOW}⚠️ Alguns testes falharam${NC}"
    echo "Verifique os logs acima para detalhes"
fi

echo ""
echo "================================================="
echo "✅ Teste finalizado"