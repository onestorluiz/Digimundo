#!/bin/bash

echo "🚀 EXECUTANDO BATERIA DE TESTES SILICON VALLEY CONTROLADA"
echo "=========================================================="

# Garantir que Redis está rodando
if ! pgrep -x "redis-server" > /dev/null; then
    echo "⚠️ Iniciando Redis..."
    /opt/homebrew/bin/redis-server --daemonize yes
    sleep 2
fi

# Executar testes em modo controlado com timeout
echo ""
echo "📊 FASE 1: TESTES UNITÁRIOS"
echo "----------------------------"
timeout 30 python3 -c "
import sys
sys.path.insert(0, '.')
from SILICON_VALLEY_ULTIMATE_TEST_BATTERY import TesteSiliconValley
tester = TesteSiliconValley()
tester.test_unit_tests()
" 2>&1 | head -50

echo ""
echo "📊 FASE 2: TESTES DE INTEGRAÇÃO"
echo "--------------------------------"
timeout 30 python3 -c "
import sys
sys.path.insert(0, '.')
from SILICON_VALLEY_ULTIMATE_TEST_BATTERY import TesteSiliconValley
tester = TesteSiliconValley()
tester.test_integration()
" 2>&1 | head -50

echo ""
echo "📊 FASE 3: TESTE DE STRESS LEVE"
echo "--------------------------------"
timeout 30 python3 -c "
import sys
import asyncio
sys.path.insert(0, '.')
from SILICON_VALLEY_ULTIMATE_TEST_BATTERY import TesteSiliconValley
tester = TesteSiliconValley()
# Teste de stress mais leve
async def stress_leve():
    results = []
    for i in range(10):  # Apenas 10 requisições
        results.append(await tester._stress_single_request(i))
    return results
asyncio.run(stress_leve())
print('✅ Stress leve completado')
" 2>&1 | head -50

echo ""
echo "📊 FASE 4: VALIDAÇÃO DE DADOS"
echo "------------------------------"
timeout 30 python3 -c "
import sys
sys.path.insert(0, '.')
from SILICON_VALLEY_ULTIMATE_TEST_BATTERY import TesteSiliconValley
tester = TesteSiliconValley()
tester.test_data_integrity()
" 2>&1 | head -50

echo ""
echo "📊 FASE 5: TESTE DE RECUPERAÇÃO"
echo "--------------------------------"
timeout 30 python3 -c "
import sys
sys.path.insert(0, '.')
from SILICON_VALLEY_ULTIMATE_TEST_BATTERY import TesteSiliconValley
tester = TesteSiliconValley()
tester.test_recovery()
" 2>&1 | head -50

echo ""
echo "=========================================================="
echo "✅ BATERIA DE TESTES CONTROLADA CONCLUÍDA"
echo ""
echo "Executando teste final harmônico..."
python3 TEST_FINAL_HARMONICO.py