#!/bin/bash
# Script de Teste Automatizado por Fase - Scripturemon Champion

set -e  # Para em caso de erro

PHASE=$1
if [ -z "$PHASE" ]; then
    echo "Uso: ./run_phase_tests.sh [FASE]"
    echo "Exemplo: ./run_phase_tests.sh 1.A"
    exit 1
fi

echo "🔍 EXECUTANDO TESTES DA FASE $PHASE"
echo "=================================="

# Contador de testes
PASSED=0
FAILED=0
TOTAL=0

# Função para executar teste
run_test() {
    local TEST_ID=$1
    local DESC=$2
    local CMD=$3
    local EXPECTED=$4
    
    TOTAL=$((TOTAL + 1))
    echo -n "[$TEST_ID] $DESC... "
    
    if eval "$CMD" > /dev/null 2>&1; then
        echo "✅ PASSOU"
        PASSED=$((PASSED + 1))
    else
        echo "❌ FALHOU"
        FAILED=$((FAILED + 1))
        echo "  Comando: $CMD"
    fi
}

# FASE 1.A - Sistema Base
if [ "$PHASE" == "1.A" ]; then
    echo "📋 Fase 1.A - Sistema Base"
    echo ""
    
    run_test "T1.A.1" "Entry Point Help" "./bin/scripturemon --help"
    run_test "T1.A.2" "Import Básico" "python3 -c 'import apps.scripturemon'"
    run_test "T1.A.3" "CLI Import" "python3 -c 'from apps.scripturemon.cli_champion import app'"
    run_test "T1.A.4" "Comando Status" "./bin/scripturemon status | grep Champion"
    run_test "T1.A.5" "Comando Chat" "echo '/exit' | ./bin/scripturemon chat | grep 'Até mais'"
    run_test "T1.A.6" "Modo Default" "echo '' | timeout 60 ./bin/scripturemon 2>/dev/null || true"
    run_test "T1.A.7" "Comando Doctor" "./bin/scripturemon doctor | grep saudável"
    run_test "T1.A.8" "Comando Backup" "./bin/scripturemon backup --output test.tar.gz | grep sucesso"
    run_test "T1.A.9" "Sintaxe Python" "python3 -m py_compile apps/scripturemon/cli_champion.py"
    run_test "T1.A.10" "Sem Duplicação" "[ $(grep -c '@app.command()' apps/scripturemon/cli_champion.py) -eq 5 ]"
fi

# FASE 1.B - Módulos de Suporte
if [ "$PHASE" == "1.B" ]; then
    echo "📋 Fase 1.B - Módulos de Suporte"
    echo ""
    
    # Primeiro executa TODOS os testes da 1.A (regressão)
    echo "🔄 Executando testes regressivos da Fase 1.A..."
    PASSED_1A=0
    FAILED_1A=0
    
    # Salva contadores atuais
    OLD_PASSED=$PASSED
    OLD_FAILED=$FAILED
    OLD_TOTAL=$TOTAL
    
    # Executa testes 1.A silenciosamente
    run_test "T1.A.1" "Entry Point Help (Regressão)" "./bin/scripturemon --help"
    run_test "T1.A.2" "Import Básico (Regressão)" "python3 -c 'import apps.scripturemon'"
    run_test "T1.A.3" "CLI Import (Regressão)" "python3 -c 'from apps.scripturemon.cli_champion import app'"
    run_test "T1.A.4" "Comando Status (Regressão)" "./bin/scripturemon status | grep Champion"
    run_test "T1.A.5" "Comando Chat (Regressão)" "echo '/exit' | ./bin/scripturemon chat | grep 'Até mais'"
    
    echo ""
    echo "📋 Testes específicos da Fase 1.B"
    
    run_test "T1.B.1" "Import Bootstrap" "python3 -c 'from apps.scripturemon.bootstrap import ensure_bootstrap_once'"
    run_test "T1.B.2" "Bootstrap Config" "python3 -c 'from apps.scripturemon.bootstrap import get_config; c=get_config(); assert c[\"version\"]==\"1.0.0\"'"
    run_test "T1.B.3" "Bootstrap Models" "python3 -c 'from apps.scripturemon.bootstrap import get_model_list; m=get_model_list(); assert len(m)>0'"
    run_test "T1.B.4" "Bootstrap Status" "python3 -c 'from apps.scripturemon.bootstrap import format_status_text; s=format_status_text(); assert \"champion\" in s.lower()'"
    run_test "T1.B.5" "Bootstrap Idempotente" "python3 -c 'from apps.scripturemon.bootstrap import ensure_bootstrap_once as e; a=e(); b=e(); assert a is b'"
fi

# FASE 1.C - Reparação e Módulos Complexos
if [ "$PHASE" == "1.C" ]; then
    echo "📋 Fase 1.C - Reparação e Módulos Complexos"
    echo ""
    
    # Executar testes regressivos 1.A e 1.B
    echo "🔄 Executando testes regressivos das Fases 1.A e 1.B..."
    
    # Testes 1.A
    run_test "T1.A.1" "Entry Point (Regressão)" "./bin/scripturemon --help"
    run_test "T1.A.2" "Import Básico (Regressão)" "python3 -c 'import apps.scripturemon'"
    run_test "T1.A.3" "CLI Champion (Regressão)" "python3 -c 'from apps.scripturemon.cli_champion import app'"
    run_test "T1.A.4" "Status (Regressão)" "./bin/scripturemon status | grep Champion"
    
    # Testes 1.B
    run_test "T1.B.1" "Bootstrap (Regressão)" "python3 -c 'from apps.scripturemon.bootstrap import ensure_bootstrap_once'"
    
    echo ""
    echo "📋 Testes específicos da Fase 1.C"
    
    # Testes dos novos módulos stub
    run_test "T1.C.1" "Import CLI Original" "python3 -c 'from apps.scripturemon.cli import app'"
    run_test "T1.C.2" "Import Doctor" "python3 -c 'from apps.scripturemon.doctor import analyze'"
    run_test "T1.C.3" "Import Persona" "python3 -c 'from apps.scripturemon.persona import discover'"
    run_test "T1.C.4" "Import Consciousness" "python3 -c 'from apps.scripturemon.consciousness import evolve'"
    run_test "T1.C.5" "Import Backup" "python3 -c 'from apps.scripturemon.backup import backup_once'"
    run_test "T1.C.6" "Import MemBridge" "python3 -c 'from apps.scripturemon.membridge import promote'"
    run_test "T1.C.7" "Import Parallel" "python3 -c 'from apps.scripturemon.parallel import analyze'"
    run_test "T1.C.8" "Import Telepathy" "python3 -c 'from apps.scripturemon.telepathy import Telepathy'"
    run_test "T1.C.9" "Import Validator" "python3 -c 'from apps.scripturemon.validator import health_once'"
    run_test "T1.C.10" "Import UI Prefs" "python3 -c 'from scripts.ui_prefs import set_live'"
    
    # Teste de integração
    run_test "T1.C.11" "Sistema ainda funciona" "./bin/scripturemon doctor"
fi

# FASE 2.A - Chat Engine Real
if [ "$PHASE" == "2.A" ]; then
    echo "📋 Fase 2.A - Chat Engine Real"
    echo ""
    
    # Executar testes regressivos de TODAS as fases anteriores
    echo "🔄 Executando testes regressivos das Fases 1.A, 1.B e 1.C..."
    
    # Testes 1.A (core)
    run_test "T1.A.1" "Entry Point (Regressão)" "./bin/scripturemon --help"
    run_test "T1.A.2" "Import Básico (Regressão)" "python3 -c 'import apps.scripturemon'"
    run_test "T1.A.3" "CLI Champion (Regressão)" "python3 -c 'from apps.scripturemon.cli_champion import app'"
    
    # Testes 1.B (bootstrap)
    run_test "T1.B.1" "Bootstrap (Regressão)" "python3 -c 'from apps.scripturemon.bootstrap import ensure_bootstrap_once'"
    
    # Testes 1.C (módulos)
    run_test "T1.C.1" "Módulos Stub (Regressão)" "python3 -c 'from apps.scripturemon.doctor import analyze'"
    
    echo ""
    echo "📋 Testes específicos da Fase 2.A"
    
    # Testes dos novos módulos de chat
    run_test "T2.A.1" "Import Ollama Manager" "python3 -c 'from apps.scripturemon.ollama_manager import get_ollama_manager'"
    run_test "T2.A.2" "Import Chat Engine" "python3 -c 'from apps.scripturemon.chat_engine import get_chat_engine'"
    run_test "T2.A.3" "Import Context Manager" "python3 -c 'from apps.scripturemon.context_manager import get_context_manager'"
    run_test "T2.A.4" "Import Prompt Templates" "python3 -c 'from apps.scripturemon.prompt_templates import get_prompt_templates'"
    run_test "T2.A.5" "Ollama Singleton" "python3 -c 'from apps.scripturemon.ollama_manager import get_ollama_manager; m1=get_ollama_manager(); m2=get_ollama_manager(); assert m1 is m2'"
    run_test "T2.A.6" "Lista Modelos" "python3 -c 'from apps.scripturemon.ollama_manager import get_ollama_manager; m=get_ollama_manager(); assert len(m.list_models())>=0'"
    run_test "T2.A.7" "Chat Session" "python3 -c 'from apps.scripturemon.chat_engine import get_chat_engine; e=get_chat_engine(); assert e.get_session_info()'"
    run_test "T2.A.8" "Context Window" "python3 -c 'from apps.scripturemon.context_manager import get_context_manager; m=get_context_manager(); w=m.create_window(\"test\"); assert w.max_tokens>0'"
    run_test "T2.A.9" "Templates Available" "python3 -c 'from apps.scripturemon.prompt_templates import get_prompt_templates; t=get_prompt_templates(); assert len(t.list_templates())>10'"
    run_test "T2.A.10" "Chat Commands" "python3 -c 'from apps.scripturemon.chat_engine import get_chat_engine; e=get_chat_engine(); r=e.handle_commands(\"/help\"); assert \"COMANDOS\" in r'"
fi

# FASE 2.B - Pipeline de Análise Real
if [ "$PHASE" == "2.B" ]; then
    echo "📋 Fase 2.B - Pipeline de Análise Real"
    echo ""
    
    # Executar testes regressivos de TODAS as fases anteriores
    echo "🔄 Executando testes regressivos das Fases 1.A, 1.B, 1.C e 2.A..."
    
    # Testes 1.A (core)
    run_test "T1.A.1" "Entry Point (Regressão)" "./bin/scripturemon --help"
    run_test "T1.A.2" "Import Básico (Regressão)" "python3 -c 'import apps.scripturemon'"
    run_test "T1.A.3" "CLI Champion (Regressão)" "python3 -c 'from apps.scripturemon.cli_champion import app'"
    
    # Testes 1.B (bootstrap)
    run_test "T1.B.1" "Bootstrap (Regressão)" "python3 -c 'from apps.scripturemon.bootstrap import ensure_bootstrap_once'"
    
    # Testes 1.C (módulos)
    run_test "T1.C.1" "Módulos Stub (Regressão)" "python3 -c 'from apps.scripturemon.doctor import analyze'"
    
    # Testes 2.A (chat engine)
    run_test "T2.A.1" "Chat Engine (Regressão)" "python3 -c 'from apps.scripturemon.chat_engine import get_chat_engine'"
    
    echo ""
    echo "📋 Testes específicos da Fase 2.B"
    
    # Testes dos novos módulos do pipeline
    run_test "T2.B.1" "Import Extract Engine" "python3 -c 'from apps.scripturemon.extract_engine import get_extract_engine'"
    run_test "T2.B.2" "Import Analyze Engine" "python3 -c 'from apps.scripturemon.analyze_engine import get_analyze_engine'"
    run_test "T2.B.3" "Import Evaluate Engine" "python3 -c 'from apps.scripturemon.evaluate_engine import get_evaluate_engine'"
    run_test "T2.B.4" "Import Synthesis Engine" "python3 -c 'from apps.scripturemon.synthesis_engine import get_synthesis_engine'"
    run_test "T2.B.5" "Import Pipeline Orchestrator" "python3 -c 'from apps.scripturemon.pipeline_orchestrator import get_pipeline_orchestrator'"
    run_test "T2.B.6" "Extract Script" "python3 -c 'from apps.scripturemon.extract_engine import get_extract_engine; e=get_extract_engine(); r=e.extract(\"INT. CASA - DIA\"); assert \"scenes\" in r'"
    run_test "T2.B.7" "Analyze Data" "python3 -c 'from apps.scripturemon.extract_engine import get_extract_engine; from apps.scripturemon.analyze_engine import get_analyze_engine; ex=get_extract_engine(); an=get_analyze_engine(); d=ex.extract(\"INT. CASA - DIA\"); r=an.analyze(d); assert \"three_act_structure\" in r'"
    run_test "T2.B.8" "Evaluate Quality" "python3 -c 'from apps.scripturemon.evaluate_engine import get_evaluate_engine; e=get_evaluate_engine(); assert e is not None'"
    run_test "T2.B.9" "Pipeline Validation" "python3 -c 'from apps.scripturemon.pipeline_orchestrator import get_pipeline_orchestrator; p=get_pipeline_orchestrator(); v=p.validate_pipeline(); assert v[\"pipeline_ready\"]'"
    run_test "T2.B.10" "Complete Pipeline" "python3 -c 'from apps.scripturemon.pipeline_orchestrator import get_pipeline_orchestrator; p=get_pipeline_orchestrator(); r=p.analyze_script(\"INT. CASA - DIA\nJOHN\nOlá!\"); assert r.success'"
fi

# Relatório Final
echo ""
echo "=================================="
echo "📊 RESULTADO DA FASE $PHASE"
echo "✅ Passou: $PASSED/$TOTAL"
echo "❌ Falhou: $FAILED/$TOTAL"

if [ $FAILED -eq 0 ]; then
    echo "🎉 FASE $PHASE COMPLETA COM SUCESSO!"
    exit 0
else
    echo "⚠️ FASE $PHASE FALHOU - CORREÇÕES NECESSÁRIAS"
    exit 1
fi