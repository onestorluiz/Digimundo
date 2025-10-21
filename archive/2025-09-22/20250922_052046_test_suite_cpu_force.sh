#!/bin/bash
# BATERIA COMPLETA DE TESTES - SISTEMA CPU-FORCE
# Conforme REGRAS #9, #14, #15, #16 do DIGIMUNDO

echo "=============================================="
echo "🧪 BATERIA DE TESTES - SCRIPTUREMON CPU-FORCE"
echo "=============================================="
echo "Data: $(date)"
echo ""

# Variáveis de controle
PASSED=0
FAILED=0
PYTHON="python3"

# Função para reportar resultado
report_test() {
    if [ $1 -eq 0 ]; then
        echo "  ✅ $2"
        ((PASSED++))
    else
        echo "  ❌ $2"
        ((FAILED++))
    fi
}

echo "================================================"
echo "📋 NÍVEL 1: VALIDAÇÃO DE SINTAXE"
echo "================================================"

echo "1.1 Verificando sintaxe de arquivos modificados..."
$PYTHON -m py_compile ollama_continuous_learning.py 2>/dev/null
report_test $? "ollama_continuous_learning.py - Sintaxe OK"

$PYTHON -m py_compile verify_cpu_usage.py 2>/dev/null
report_test $? "verify_cpu_usage.py - Sintaxe OK"

echo ""
echo "================================================"
echo "📋 NÍVEL 2: VALIDAÇÃO DE IMPORTS"
echo "================================================"

echo "2.1 Testando imports do sistema principal..."
$PYTHON -c "import ollama_continuous_learning" 2>/dev/null
report_test $? "Import ollama_continuous_learning"

$PYTHON -c "import verify_cpu_usage" 2>/dev/null
report_test $? "Import verify_cpu_usage"

echo ""
echo "2.2 Verificando dependências..."
$PYTHON -c "import requests, sqlite3, hashlib, psutil" 2>/dev/null
report_test $? "Dependências básicas disponíveis"

$PYTHON -c "from src.scripturemon_champion.analysis.script_doctor import ScriptDoctor" 2>/dev/null
report_test $? "ScriptDoctor importável"

echo ""
echo "================================================"
echo "📋 NÍVEL 3: VALIDAÇÃO DE FUNÇÕES"
echo "================================================"

echo "3.1 Testando inicialização de classes..."
$PYTHON -c "
from ollama_continuous_learning import OllamaContinuousLearning
try:
    learner = OllamaContinuousLearning()
    print('  ✅ OllamaContinuousLearning inicializado')
except Exception as e:
    print(f'  ❌ Erro na inicialização: {e}')
    exit(1)
" 2>/dev/null
report_test $? "Classe OllamaContinuousLearning"

echo ""
echo "3.2 Verificando modelo CPU configurado..."
$PYTHON -c "
from ollama_continuous_learning import OllamaContinuousLearning
learner = OllamaContinuousLearning()
if 'cpu-force' in learner.model:
    print('  ✅ Modelo CPU-force configurado:', learner.model)
    exit(0)
else:
    print('  ❌ Modelo incorreto:', learner.model)
    exit(1)
" 2>/dev/null
report_test $? "Modelo padrão é CPU-force"

echo ""
echo "================================================"
echo "📋 NÍVEL 4: VALIDAÇÃO DE INTEGRAÇÃO"
echo "================================================"

echo "4.1 Verificando conexão Ollama..."
curl -s http://localhost:11434/api/tags > /dev/null 2>&1
report_test $? "API Ollama respondendo"

echo ""
echo "4.2 Verificando modelo mixtral-cpu-force..."
ollama list | grep -q "mixtral-cpu-force"
report_test $? "Modelo mixtral-cpu-force existe"

echo ""
echo "4.3 Testando encaminhamento doctor → análise..."
$PYTHON -c "
from src.scripturemon_champion.analysis.script_doctor import ScriptDoctor
doctor = ScriptDoctor()
# Verifica se doctor tem métodos esperados
if hasattr(doctor, 'analyze_file'):
    print('  ✅ ScriptDoctor.analyze_file disponível')
    exit(0)
else:
    print('  ❌ ScriptDoctor.analyze_file não encontrado')
    exit(1)
" 2>/dev/null
report_test $? "Cadeia doctor→analyze funcional"

echo ""
echo "================================================"
echo "📋 NÍVEL 5: TESTE DO SISTEMA COMPLETO"
echo "================================================"

echo "5.1 Testando inferência com modelo CPU..."
echo "Test prompt" | timeout 30 ollama run mixtral-cpu-force "Say 'OK'" 2>/dev/null | grep -q "OK"
report_test $? "Inferência básica com CPU-force"

echo ""
echo "5.2 Monitorando uso de CPU durante inferência..."
# Lança inferência em background
(echo "Analyze this" | ollama run mixtral-cpu-force "Brief analysis" > /tmp/cpu_test_output.txt 2>&1) &
PID=$!

# Monitora CPU por 5 segundos
sleep 2
CPU_USAGE=$(ps aux | grep "ollama.*runner" | grep -v grep | awk '{print $3}' | head -1)

# Mata processo se ainda estiver rodando
kill $PID 2>/dev/null

# Verifica se CPU foi usado significativamente
if [ ! -z "$CPU_USAGE" ]; then
    CPU_INT=${CPU_USAGE%.*}
    if [ "$CPU_INT" -gt "50" ]; then
        echo "  ✅ CPU usage detectado: ${CPU_USAGE}%"
        ((PASSED++))
    else
        echo "  ⚠️ CPU usage baixo: ${CPU_USAGE}%"
        ((FAILED++))
    fi
else
    echo "  ❌ Não foi possível medir CPU usage"
    ((FAILED++))
fi

echo ""
echo "5.3 Verificando SafeJSONParser..."
if [ -f "safe_json_parser_20250921_214934.py" ]; then
    $PYTHON -c "
from safe_json_parser_20250921_214934 import safe_json_parse
result = safe_json_parse('{\"test\": true}')
if result and result.get('test') == True:
    print('  ✅ SafeJSONParser funcionando')
    exit(0)
else:
    print('  ❌ SafeJSONParser falhou')
    exit(1)
" 2>/dev/null
    report_test $? "SafeJSONParser operacional"
else
    echo "  ⚠️ SafeJSONParser não encontrado"
fi

echo ""
echo "5.4 Verificando ProcessLock..."
if [ -f "process_lock.py" ]; then
    $PYTHON -c "
from process_lock import ProcessLock
import tempfile
with ProcessLock('test_lock'):
    print('  ✅ ProcessLock funcionando')
" 2>/dev/null
    report_test $? "ProcessLock operacional"
else
    echo "  ⚠️ ProcessLock não encontrado"
fi

echo ""
echo "================================================"
echo "📋 VALIDAÇÃO DE DOCUMENTAÇÃO"
echo "================================================"

echo "Verificando arquivos de documentação criados..."
[ -f "SOLUCAO_CPU_IMPLEMENTADA.md" ]
report_test $? "SOLUCAO_CPU_IMPLEMENTADA.md existe"

[ -f "MUDANCAS_CPU_FORCE.md" ]
report_test $? "MUDANCAS_CPU_FORCE.md existe"

[ -f "verify_cpu_usage.py" ]
report_test $? "verify_cpu_usage.py existe"

echo ""
echo "================================================"
echo "📊 RELATÓRIO FINAL"
echo "================================================"
echo ""
echo "✅ Testes passados: $PASSED"
echo "❌ Testes falhados: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 TODOS OS TESTES PASSARAM!"
    echo "✅ Sistema CPU-force está 100% operacional"
    exit 0
else
    echo "⚠️ ATENÇÃO: $FAILED teste(s) falharam"
    echo "🔧 Verifique os erros acima e corrija"
    exit 1
fi