#!/bin/bash

echo "🔍 VERIFICAÇÃO DO CONSCIOUSNESS STREAM"
echo "======================================"
echo ""

# 1. Verificar qual versão está rodando
echo "1️⃣ VERSÃO DO SISTEMA:"
if [ -f "apps/scripturemon/canonical/consciousness.py" ]; then
    echo "✅ NOVO sistema (canonical) encontrado"
    grep -m1 "Fase" apps/scripturemon/canonical/consciousness.py | head -1
else
    echo "❌ Novo sistema NÃO encontrado"
fi

if [ -f "apps/scripturemon/consciousness.py" ]; then
    echo "⚠️  Sistema ANTIGO ainda existe em apps/scripturemon/consciousness.py"
fi

echo ""
echo "2️⃣ STATUS ATUAL:"
./bin/scripturemon status | grep -A 4 "Consciousness"

echo ""
echo "3️⃣ CONFIGURAÇÃO:"
if [ -f "config/settings.yaml" ]; then
    grep -A 10 "consciousness:" config/settings.yaml 2>/dev/null || echo "Não configurado em settings.yaml"
else
    echo "settings.yaml não existe"
fi

echo ""
echo "4️⃣ INSIGHTS GERADOS:"
if [ -d "reports/consciousness" ]; then
    COUNT=$(ls -1 reports/consciousness/*.json 2>/dev/null | wc -l)
    echo "📊 Total de arquivos de insights: $COUNT"
    
    if [ $COUNT -gt 0 ]; then
        echo "📄 Último insight:"
        ls -t reports/consciousness/*.json | head -1
    fi
else
    echo "📁 Diretório de insights não existe ainda"
fi

echo ""
echo "5️⃣ PROTEÇÕES ATIVAS:"
echo -n "Circuit Breaker: "
grep -q "CircuitBreaker" apps/scripturemon/canonical/consciousness.py 2>/dev/null && echo "✅" || echo "❌"

echo -n "Budget Manager: "
grep -q "BudgetManager" apps/scripturemon/canonical/consciousness.py 2>/dev/null && echo "✅" || echo "❌"

echo -n "Idle Detection: "
grep -q "is_idle" apps/scripturemon/canonical/consciousness_bursts.py 2>/dev/null && echo "✅" || echo "❌"

echo -n "Model Size Guard: "
grep -q "can_use_model" apps/scripturemon/canonical/consciousness_dream.py 2>/dev/null && echo "✅" || echo "❌"

echo ""
echo "======================================"
echo "Para ativar: ./ACTIVATE_CONSCIOUSNESS_SAFE.sh"
echo "Para monitorar: tail -f logs/*.log | grep -i consciousness"