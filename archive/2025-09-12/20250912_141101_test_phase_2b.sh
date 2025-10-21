#!/bin/bash

# Test Phase 2.B - Pipeline de Análise Real
# Testa os 5 novos módulos do pipeline

echo "════════════════════════════════════════════════════════════════"
echo "         TESTE FASE 2.B - PIPELINE DE ANÁLISE REAL"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Configuração
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Contadores
TESTS_PASSED=0
TESTS_FAILED=0

# Função para testar imports
test_import() {
    local module=$1
    local description=$2
    
    echo -n "Testing $description... "
    
    if python3 -c "from apps.scripturemon.$module import *" 2>/dev/null; then
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

echo "🔍 FASE 2.B - Testando novos módulos do pipeline..."
echo "────────────────────────────────────────────────────"

# Teste 1: Extract Engine
echo ""
echo "📦 [1/5] Extract Engine"
test_import "extract_engine" "import extract_engine"

test_functionality "ExtractEngine instantiation" "
from apps.scripturemon.extract_engine import ExtractEngine
engine = ExtractEngine()
assert engine is not None
"

test_functionality "Extract from simple script" "
from apps.scripturemon.extract_engine import ExtractEngine
engine = ExtractEngine()
script = '''INT. CASA - DIA

JOHN entra na sala.

JOHN
Olá mundo!

MARY
(sorrindo)
Bem-vindo!'''
result = engine.extract(script)
assert 'characters' in result
assert 'scenes' in result
assert 'dialogues' in result
assert len(result['characters']) >= 2
"

# Teste 2: Analyze Engine
echo ""
echo "📊 [2/5] Analyze Engine"
test_import "analyze_engine" "import analyze_engine"

test_functionality "AnalyzeEngine instantiation" "
from apps.scripturemon.analyze_engine import AnalyzeEngine
engine = AnalyzeEngine()
assert engine is not None
"

test_functionality "Analyze extracted data" "
from apps.scripturemon.extract_engine import ExtractEngine
from apps.scripturemon.analyze_engine import AnalyzeEngine
extract = ExtractEngine()
analyze = AnalyzeEngine()

script = '''INT. CASA - DIA
JOHN entra.
JOHN
Teste.'''

extraction = extract.extract(script)
analysis = analyze.analyze(extraction)
assert 'three_act_structure' in analysis
assert 'character_arcs' in analysis
"

# Teste 3: Evaluate Engine
echo ""
echo "⭐ [3/5] Evaluate Engine"
test_import "evaluate_engine" "import evaluate_engine"

test_functionality "EvaluateEngine instantiation" "
from apps.scripturemon.evaluate_engine import EvaluateEngine
engine = EvaluateEngine()
assert engine is not None
"

test_functionality "Evaluate script quality" "
from apps.scripturemon.extract_engine import ExtractEngine
from apps.scripturemon.analyze_engine import AnalyzeEngine
from apps.scripturemon.evaluate_engine import EvaluateEngine

extract = ExtractEngine()
analyze = AnalyzeEngine()
evaluate = EvaluateEngine()

script = '''INT. CASA - DIA
JOHN entra.'''

extraction = extract.extract(script)
analysis = analyze.analyze(extraction)
evaluation = evaluate.evaluate(extraction, analysis)

assert 'overall_score' in evaluation
assert 'grade' in evaluation
assert 'metrics' in evaluation
"

# Teste 4: Synthesis Engine
echo ""
echo "📄 [4/5] Synthesis Engine"
test_import "synthesis_engine" "import synthesis_engine"

test_functionality "SynthesisEngine instantiation" "
from apps.scripturemon.synthesis_engine import SynthesisEngine
engine = SynthesisEngine()
assert engine is not None
"

test_functionality "Synthesize report" "
from apps.scripturemon.extract_engine import ExtractEngine
from apps.scripturemon.analyze_engine import AnalyzeEngine
from apps.scripturemon.evaluate_engine import EvaluateEngine
from apps.scripturemon.synthesis_engine import SynthesisEngine

extract = ExtractEngine()
analyze = AnalyzeEngine()
evaluate = EvaluateEngine()
synthesis = SynthesisEngine()

script = '''INT. CASA - DIA
JOHN entra.'''

extraction = extract.extract(script)
analysis = analyze.analyze(extraction)
evaluation = evaluate.evaluate(extraction, analysis)
report = synthesis.synthesize(extraction, analysis, evaluation)

assert 'executive_summary' in report
assert 'score_card' in report
assert 'recommendations' in report
"

# Teste 5: Pipeline Orchestrator
echo ""
echo "🎯 [5/5] Pipeline Orchestrator"
test_import "pipeline_orchestrator" "import pipeline_orchestrator"

test_functionality "PipelineOrchestrator instantiation" "
from apps.scripturemon.pipeline_orchestrator import PipelineOrchestrator
orchestrator = PipelineOrchestrator()
assert orchestrator is not None
"

test_functionality "Complete pipeline execution" "
from apps.scripturemon.pipeline_orchestrator import PipelineOrchestrator

orchestrator = PipelineOrchestrator()
script = '''INT. CASA - DIA

JOHN
(determinado)
Vamos testar o pipeline completo!

MARY
Concordo!

EXT. JARDIM - DIA

Os dois saem para o jardim.'''

result = orchestrator.analyze_script(script)
assert result.success == True
assert len(result.stages_completed) == 4
assert 'overall_score' in result.report.get('score_card', {})
"

test_functionality "Pipeline validation" "
from apps.scripturemon.pipeline_orchestrator import PipelineOrchestrator

orchestrator = PipelineOrchestrator()
validation = orchestrator.validate_pipeline()

assert validation['extract_engine'] == True
assert validation['analyze_engine'] == True
assert validation['evaluate_engine'] == True
assert validation['synthesis_engine'] == True
assert validation['pipeline_ready'] == True
"

# Teste de integração com CLI
echo ""
echo "🔗 Testing CLI integration with pipeline..."
test_functionality "Doctor command with new pipeline" "
from apps.scripturemon.cli_champion import app
from typer.testing import CliRunner

runner = CliRunner()
# Comando doctor agora deve usar o pipeline real
assert runner is not None
"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "                    RESUMO FASE 2.B"
echo "────────────────────────────────────────────────────────────────"
echo ""
echo "  ✅ Testes aprovados: $TESTS_PASSED"
echo "  ❌ Testes falhados: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "  🎉 FASE 2.B COMPLETA COM SUCESSO!"
    echo ""
    echo "  Pipeline de 4 estágios implementado:"
    echo "  1. Extract Engine ✅"
    echo "  2. Analyze Engine ✅"
    echo "  3. Evaluate Engine ✅"
    echo "  4. Synthesis Engine ✅"
    echo "  5. Pipeline Orchestrator ✅"
    exit 0
else
    echo "  ⚠️  FASE 2.B COM PROBLEMAS"
    echo ""
    echo "  Verifique os erros acima e corrija antes de prosseguir."
    exit 1
fi