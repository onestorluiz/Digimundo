#!/bin/bash

# Test Phase 3.A - Integração Pipeline com CLI
# Testa integração do pipeline com comandos CLI

echo "════════════════════════════════════════════════════════════════"
echo "      TESTE FASE 3.A - INTEGRAÇÃO PIPELINE COM CLI"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Configuração
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Contadores
TESTS_PASSED=0
TESTS_FAILED=0

# Arquivo de teste
SAMPLE_SCRIPT="data/sample_script.txt"

# Cria arquivo de teste se não existir
if [ ! -f "$SAMPLE_SCRIPT" ]; then
    echo "Criando arquivo de teste..."
    mkdir -p data
    cat > "$SAMPLE_SCRIPT" << 'EOF'
INT. CASA - DIA

JOHN entra na sala.

JOHN
Olá mundo!

MARY
Bem-vindo!

FADE OUT.
EOF
fi

# Função para testar comando
test_command() {
    local description=$1
    local command=$2
    
    echo -n "Testing $description... "
    
    if eval "$command" > /dev/null 2>&1; then
        echo "✅ PASS"
        ((TESTS_PASSED++))
        return 0
    else
        echo "❌ FAIL"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Função para testar funcionalidade
test_functionality() {
    local test_name=$1
    local test_code=$2
    
    echo -n "Testing $test_name... "
    
    if python3 -c "$test_code" 2>/dev/null; then
        echo "✅ PASS"
        ((TESTS_PASSED++))
        return 0
    else
        echo "❌ FAIL"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo "🔍 FASE 3.A - Testando integração Pipeline-CLI..."
echo "────────────────────────────────────────────────────"

# Teste 1: Doctor module atualizado
echo ""
echo "🩺 [1/7] Doctor Module Integration"
test_functionality "Import doctor module" "
from apps.scripturemon.doctor import analyze, deep_analyze, export_analysis, validate_script
assert analyze is not None
assert export_analysis is not None
"

test_functionality "Doctor uses pipeline" "
from apps.scripturemon.doctor import analyze
from pathlib import Path
# Doctor deve ter imports do pipeline
import inspect
source = inspect.getsource(analyze)
assert 'pipeline_orchestrator' in source
assert 'get_pipeline_orchestrator' in source
"

# Teste 2: CLI atualizado
echo ""
echo "🎮 [2/7] CLI Champion Updates"
test_functionality "Import cli_champion" "
from apps.scripturemon.cli_champion import app
assert app is not None
"

test_functionality "CLI has analyze command" "
from apps.scripturemon.cli_champion import app
# Verifica se os comandos existem como funções decoradas
import inspect
members = dict(inspect.getmembers(app))
# Os comandos são registrados mas aparecem como None em registered_commands
# Verificamos se as funções existem no módulo
from apps.scripturemon import cli_champion
assert hasattr(cli_champion, 'analyze')
assert hasattr(cli_champion, 'doctor')
assert hasattr(cli_champion, 'batch')
"

test_functionality "CLI imports Rich" "
import apps.scripturemon.cli_champion as cli
assert hasattr(cli, 'Console')
assert hasattr(cli, 'Table')
"

# Teste 3: Comando status
echo ""
echo "📊 [3/7] Status Command"
test_command "Status basic" "./bin/scripturemon status"
test_command "Status shows v3.A" "./bin/scripturemon status | grep -q 'v3.A'"
test_command "Status shows pipeline" "./bin/scripturemon status | grep -q 'Pipeline'"

# Teste 4: Comando doctor
echo ""
echo "🔍 [4/7] Doctor Command"
test_command "Doctor system check" "./bin/scripturemon doctor"
test_command "Doctor validate sample" "./bin/scripturemon doctor $SAMPLE_SCRIPT --validate"
test_command "Doctor analyze sample" "./bin/scripturemon doctor $SAMPLE_SCRIPT"

# Teste 5: Comando analyze
echo ""
echo "📝 [5/7] Analyze Command"
test_command "Analyze help" "./bin/scripturemon analyze --help"
test_command "Analyze sample script" "./bin/scripturemon analyze $SAMPLE_SCRIPT"
test_command "Analyze with format json" "./bin/scripturemon analyze $SAMPLE_SCRIPT --format json | head -5 | grep -q '\"status\"'"

# Teste 6: Pipeline funcionando
echo ""
echo "🔧 [6/7] Pipeline Functionality"
test_functionality "Pipeline validation" "
from apps.scripturemon.pipeline_orchestrator import get_pipeline_orchestrator
orchestrator = get_pipeline_orchestrator()
validation = orchestrator.validate_pipeline()
assert validation['pipeline_ready'] == True
"

test_functionality "Pipeline processes script" "
from apps.scripturemon.pipeline_orchestrator import get_pipeline_orchestrator
orchestrator = get_pipeline_orchestrator()
result = orchestrator.analyze_script('INT. CASA - DIA\\nJOHN\\nTeste!')
assert result.success == True
assert len(result.stages_completed) == 4
"

test_functionality "Doctor uses real pipeline" "
from apps.scripturemon.doctor import analyze
from pathlib import Path
result = analyze(Path('$SAMPLE_SCRIPT'))
assert result['status'] == 'success'
assert 'score' in result
assert 'grade' in result
assert 'detailed_report' in result
"

# Teste 7: Exportação
echo ""
echo "💾 [7/7] Export Functionality"
test_functionality "Export analysis to JSON" "
from apps.scripturemon.doctor import export_analysis
from pathlib import Path
import tempfile
import json

with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
    output = Path(f.name)

result = export_analysis(
    Path('$SAMPLE_SCRIPT'),
    output,
    'json'
)

assert result['status'] == 'success'
assert output.exists()

# Verifica se é JSON válido
with open(output) as f:
    data = json.load(f)
    assert 'score_card' in data

output.unlink()  # Limpa arquivo temporário
"

test_functionality "Export to markdown" "
from apps.scripturemon.doctor import export_analysis
from pathlib import Path
import tempfile

with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as f:
    output = Path(f.name)

result = export_analysis(
    Path('$SAMPLE_SCRIPT'),
    output,
    'markdown'
)

assert result['status'] == 'success'
assert output.exists()
content = output.read_text()
assert '# Relatório' in content

output.unlink()
"

test_functionality "Export to HTML" "
from apps.scripturemon.doctor import export_analysis
from pathlib import Path
import tempfile

with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
    output = Path(f.name)

result = export_analysis(
    Path('$SAMPLE_SCRIPT'),
    output,
    'html'
)

assert result['status'] == 'success'
assert output.exists()
content = output.read_text()
assert '<html>' in content

output.unlink()
"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "                    RESUMO FASE 3.A"
echo "────────────────────────────────────────────────────────────────"
echo ""
echo "  ✅ Testes aprovados: $TESTS_PASSED"
echo "  ❌ Testes falhados: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "  🎉 FASE 3.A COMPLETA COM SUCESSO!"
    echo ""
    echo "  Integração Pipeline-CLI implementada:"
    echo "  • Doctor module usa pipeline real ✅"
    echo "  • CLI com comandos analyze e batch ✅"
    echo "  • Exportação HTML, Markdown, JSON ✅"
    echo "  • Interface Rich para output formatado ✅"
    echo "  • 100% compatível com pipeline de 4 estágios ✅"
    exit 0
else
    echo "  ⚠️  FASE 3.A COM PROBLEMAS"
    echo ""
    echo "  Verifique os erros acima e corrija antes de prosseguir."
    exit 1
fi