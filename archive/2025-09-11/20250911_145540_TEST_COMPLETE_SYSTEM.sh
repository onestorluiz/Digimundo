#!/bin/bash

# ============================================================
# BATERIA COMPLETA DE TESTES - SCRIPTUREMON v1.0.0-vFinal
# ============================================================
# Testa TODOS os comandos e verifica versões
# Data: 2025-09-11
# ============================================================

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Diretórios
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RESULTS_DIR="$SCRIPT_DIR/test_results_$(date +%Y%m%d_%H%M%S)"

# Criar diretório de resultados
mkdir -p "$RESULTS_DIR"

# Arquivo de log
LOG_FILE="$RESULTS_DIR/test_complete.log"
REPORT_FILE="$RESULTS_DIR/test_report.md"

# Função de log
log() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

# Função para testar comando
test_command() {
    local cmd="$1"
    local desc="$2"
    local expected="$3"
    
    log "\n${YELLOW}Testando: $desc${NC}"
    log "Comando: $cmd"
    
    # Executar comando e capturar saída
    output=$($cmd 2>&1)
    exit_code=$?
    
    # Verificar se contém string esperada
    if [[ "$output" == *"$expected"* ]]; then
        log "${GREEN}✅ PASSOU${NC} - Encontrou: '$expected'"
        echo "✅ $desc" >> "$REPORT_FILE"
        return 0
    else
        log "${RED}❌ FALHOU${NC} - Não encontrou: '$expected'"
        log "Saída recebida: ${output:0:200}..."
        echo "❌ $desc - Esperava '$expected'" >> "$REPORT_FILE"
        return 1
    fi
}

# Função para verificar versão Python
check_python_version() {
    log "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
    log "${CYAN}VERIFICANDO VERSÃO DO SCRIPTUREMON${NC}"
    log "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    
    python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')
from apps.scripturemon import get_version, __version__
print(f'Versão via get_version(): {get_version()}')
print(f'Versão via __version__: {__version__}')

# Verificar se é a versão correta
if __version__ == '1.0.0-vFinal':
    print('✅ VERSÃO CORRETA!')
else:
    print(f'❌ VERSÃO INCORRETA: {__version__}')
    sys.exit(1)
" | tee -a "$LOG_FILE"
}

# Início dos testes
echo "# RELATÓRIO DE TESTES - SCRIPTUREMON" > "$REPORT_FILE"
echo "Data: $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

log "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
log "${BLUE}║         BATERIA COMPLETA DE TESTES SCRIPTUREMON           ║${NC}"
log "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
log ""
log "Início: $(date)"
log "Diretório: $PROJECT_ROOT"
log "Resultados: $RESULTS_DIR"
log ""

# ============================================================
# TESTE 1: Verificar Versão
# ============================================================
check_python_version

# ============================================================
# TESTE 2: Comandos Instalados
# ============================================================
log "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
log "${CYAN}TESTANDO COMANDOS INSTALADOS${NC}"
log "${CYAN}═══════════════════════════════════════════════════════════${NC}"

echo "## Comandos Instalados" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Verificar se comandos existem
for cmd in digimundo scripturemon consciousness memory; do
    if command -v $cmd &> /dev/null; then
        log "${GREEN}✅ $cmd instalado:${NC} $(command -v $cmd)"
        echo "✅ $cmd: $(command -v $cmd)" >> "$REPORT_FILE"
    else
        log "${RED}❌ $cmd não encontrado${NC}"
        echo "❌ $cmd não encontrado" >> "$REPORT_FILE"
    fi
done

# ============================================================
# TESTE 3: Comando DIGIMUNDO
# ============================================================
log "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
log "${CYAN}TESTANDO COMANDO DIGIMUNDO${NC}"
log "${CYAN}═══════════════════════════════════════════════════════════${NC}"

echo "" >> "$REPORT_FILE"
echo "## Testes do Comando Digimundo" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

test_command "digimundo help" \
    "digimundo help" \
    "DIGIMUNDO - Sistema Completo"

test_command "digimundo status" \
    "digimundo status" \
    "STATUS DO DIGIMUNDO"

# ============================================================
# TESTE 4: Comando CONSCIOUSNESS
# ============================================================
log "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
log "${CYAN}TESTANDO COMANDO CONSCIOUSNESS${NC}"
log "${CYAN}═══════════════════════════════════════════════════════════${NC}"

echo "" >> "$REPORT_FILE"
echo "## Testes do Comando Consciousness" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

test_command "consciousness help" \
    "consciousness help" \
    "CONSCIOUSNESS - Pensamento Contínuo"

test_command "consciousness status" \
    "consciousness status" \
    "Status do ConsciousnessStream"

# ============================================================
# TESTE 5: Comando MEMORY
# ============================================================
log "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
log "${CYAN}TESTANDO COMANDO MEMORY${NC}"
log "${CYAN}═══════════════════════════════════════════════════════════${NC}"

echo "" >> "$REPORT_FILE"
echo "## Testes do Comando Memory" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

test_command "memory help" \
    "memory help" \
    "MEMORY - Sistema de Memória"

test_command "memory stats" \
    "memory stats" \
    "ESTATÍSTICAS DO SISTEMA DE MEMÓRIA"

# ============================================================
# TESTE 6: Verificar Módulos Python
# ============================================================
log "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
log "${CYAN}VERIFICANDO MÓDULOS PYTHON${NC}"
log "${CYAN}═══════════════════════════════════════════════════════════${NC}"

echo "" >> "$REPORT_FILE"
echo "## Módulos Python" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')

modules_to_check = [
    'apps.scripturemon',
    'apps.scripturemon.bootstrap',
    'apps.scripturemon.chat',
    'apps.scripturemon.cli',
    'apps.scripturemon.canonical.consciousness',
    'apps.scripturemon.canonical.memory_manager',
    'apps.scripturemon.soul',
    'apps.scripturemon.personality',
    'apps.scripturemon.cinema_knowledge'
]

print('Verificando módulos principais:')
failed = []
for module in modules_to_check:
    try:
        __import__(module)
        print(f'  ✅ {module}')
    except ImportError as e:
        print(f'  ❌ {module}: {e}')
        failed.append(module)

if not failed:
    print('\\n✅ TODOS OS MÓDULOS CARREGADOS COM SUCESSO!')
else:
    print(f'\\n❌ {len(failed)} módulos falharam')
    sys.exit(1)
" | tee -a "$LOG_FILE"

# ============================================================
# TESTE 7: Bootstrap do Sistema
# ============================================================
log "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
log "${CYAN}TESTANDO BOOTSTRAP DO SISTEMA${NC}"
log "${CYAN}═══════════════════════════════════════════════════════════${NC}"

echo "" >> "$REPORT_FILE"
echo "## Bootstrap do Sistema" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')

try:
    from apps.scripturemon.bootstrap import ensure_bootstrap_once, status_report
    
    # Bootstrap
    context = ensure_bootstrap_once()
    print('✅ Bootstrap executado com sucesso')
    
    # Status
    status = status_report()
    print(f'\\nStatus do sistema:')
    print(f'  Memory: {status.get(\"memory\", {}).get(\"functional\", False)}')
    print(f'  Telepathy: {status.get(\"telepathy\", {}).get(\"type\", \"unknown\")}')
    print(f'  Consciousness: {status.get(\"consciousness\", {}).get(\"enabled\", False)}')
    print(f'  Monitoring: {status.get(\"monitoring\", {}).get(\"enabled\", False)}')
    
except Exception as e:
    print(f'❌ Bootstrap falhou: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
" | tee -a "$LOG_FILE"

# ============================================================
# TESTE 8: ConsciousnessStream
# ============================================================
log "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
log "${CYAN}TESTANDO CONSCIOUSNESSSTREAM${NC}"
log "${CYAN}═══════════════════════════════════════════════════════════${NC}"

echo "" >> "$REPORT_FILE"
echo "## ConsciousnessStream" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')

try:
    from apps.scripturemon.canonical.consciousness import ConsciousnessStream
    
    # Criar instância
    cs = ConsciousnessStream()
    print(f'✅ ConsciousnessStream criado')
    print(f'  Enabled: {cs.enabled}')
    print(f'  Mode: {cs.mode}')
    print(f'  Circuit Breaker: {cs.circuit_breaker.is_open()}')
    
    # Verificar métodos
    methods = ['start', 'stop', 'should_run_burst', 'run_burst']
    for method in methods:
        if hasattr(cs, method):
            print(f'  ✅ Método {method} existe')
        else:
            print(f'  ❌ Método {method} não encontrado')
            
except Exception as e:
    print(f'❌ ConsciousnessStream falhou: {e}')
    import traceback
    traceback.print_exc()
" | tee -a "$LOG_FILE"

# ============================================================
# TESTE 9: Chat System
# ============================================================
log "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
log "${CYAN}TESTANDO SISTEMA DE CHAT${NC}"
log "${CYAN}═══════════════════════════════════════════════════════════${NC}"

echo "" >> "$REPORT_FILE"
echo "## Sistema de Chat" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')

try:
    from apps.scripturemon.chat import ScripturemonChat, ConversationHistory
    
    # Criar chat
    chat = ScripturemonChat()
    print('✅ ScripturemonChat criado')
    
    # Verificar componentes
    components = ['soul', 'personality', 'rag', 'quad_pipeline']
    for comp in components:
        if hasattr(chat, comp):
            print(f'  ✅ {comp} inicializado')
        else:
            print(f'  ⚠️  {comp} não encontrado')
    
    # Testar histórico
    history = ConversationHistory()
    history.add('teste', 'resposta')
    context = history.get_context()
    if 'teste' in context:
        print('  ✅ ConversationHistory funcionando')
    else:
        print('  ❌ ConversationHistory falhou')
        
except Exception as e:
    print(f'❌ Chat system falhou: {e}')
    import traceback
    traceback.print_exc()
" | tee -a "$LOG_FILE"

# ============================================================
# TESTE 10: Verificar Caminho Real do Scripturemon
# ============================================================
log "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
log "${CYAN}VERIFICANDO CAMINHO REAL DO SCRIPTUREMON${NC}"
log "${CYAN}═══════════════════════════════════════════════════════════${NC}"

echo "" >> "$REPORT_FILE"
echo "## Caminhos e Versões" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Verificar qual scripturemon está sendo usado
log "\n${YELLOW}Qual scripturemon está no PATH?${NC}"
which_scripturemon=$(which scripturemon 2>/dev/null)
if [ -n "$which_scripturemon" ]; then
    log "Scripturemon no PATH: $which_scripturemon"
    
    # Verificar se é link simbólico
    if [ -L "$which_scripturemon" ]; then
        real_path=$(readlink -f "$which_scripturemon")
        log "É um link simbólico para: $real_path"
    else
        log "É um arquivo direto"
    fi
    
    # Verificar conteúdo do arquivo
    log "\nPrimeiras linhas do arquivo:"
    head -20 "$which_scripturemon" | tee -a "$LOG_FILE"
else
    log "${RED}scripturemon não está no PATH${NC}"
fi

# ============================================================
# RESUMO FINAL
# ============================================================
log "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
log "${CYAN}RESUMO DOS TESTES${NC}"
log "${CYAN}═══════════════════════════════════════════════════════════${NC}"

echo "" >> "$REPORT_FILE"
echo "## Resumo" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Contar sucessos e falhas
success_count=$(grep -c "✅" "$REPORT_FILE")
failure_count=$(grep -c "❌" "$REPORT_FILE")

log "\n${GREEN}Testes bem-sucedidos: $success_count${NC}"
log "${RED}Testes falhados: $failure_count${NC}"

echo "- Testes bem-sucedidos: $success_count" >> "$REPORT_FILE"
echo "- Testes falhados: $failure_count" >> "$REPORT_FILE"

if [ $failure_count -eq 0 ]; then
    log "\n${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
    log "${GREEN}║           TODOS OS TESTES PASSARAM! 🎉                    ║${NC}"
    log "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo "" >> "$REPORT_FILE"
    echo "**✅ TODOS OS TESTES PASSARAM!**" >> "$REPORT_FILE"
else
    log "\n${RED}╔══════════════════════════════════════════════════════════╗${NC}"
    log "${RED}║           ALGUNS TESTES FALHARAM                          ║${NC}"
    log "${RED}╚══════════════════════════════════════════════════════════╝${NC}"
    echo "" >> "$REPORT_FILE"
    echo "**⚠️ ALGUNS TESTES FALHARAM**" >> "$REPORT_FILE"
fi

log "\nRelatórios salvos em:"
log "  Log completo: $LOG_FILE"
log "  Relatório: $REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "*Teste executado em $(date)*" >> "$REPORT_FILE"