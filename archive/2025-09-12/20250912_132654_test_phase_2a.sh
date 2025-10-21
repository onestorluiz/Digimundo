#!/bin/bash
#####################################
# Testes da Fase 2.A - Chat Engine Real
# Sistema: Scripturemon Champion
#####################################

set -e

echo "🧪 TESTES DA FASE 2.A - CHAT ENGINE REAL"
echo "=========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Contadores
PASSED=0
FAILED=0

# Função para testar
test_feature() {
    local test_name="$1"
    local test_cmd="$2"
    
    echo -n "[$test_name]... "
    
    if eval "$test_cmd" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASSOU${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ FALHOU${NC}"
        ((FAILED++))
    fi
}

# Teste T2.A.1: Import dos novos módulos
test_feature "T2.A.1 Import Ollama Manager" \
    "python3 -c 'from apps.scripturemon.ollama_manager import OllamaManager, get_ollama_manager'"

# Teste T2.A.2: Import Chat Engine
test_feature "T2.A.2 Import Chat Engine" \
    "python3 -c 'from apps.scripturemon.chat_engine import ChatEngine, get_chat_engine'"

# Teste T2.A.3: Import Context Manager
test_feature "T2.A.3 Import Context Manager" \
    "python3 -c 'from apps.scripturemon.context_manager import ContextManager, get_context_manager'"

# Teste T2.A.4: Import Prompt Templates
test_feature "T2.A.4 Import Prompt Templates" \
    "python3 -c 'from apps.scripturemon.prompt_templates import PromptTemplates, get_prompt_templates'"

# Teste T2.A.5: Ollama Manager singleton
test_feature "T2.A.5 Ollama Manager Singleton" \
    "python3 -c '
from apps.scripturemon.ollama_manager import get_ollama_manager
m1 = get_ollama_manager()
m2 = get_ollama_manager()
assert m1 is m2
'"

# Teste T2.A.6: Lista modelos
test_feature "T2.A.6 Listar Modelos" \
    "python3 -c '
from apps.scripturemon.ollama_manager import get_ollama_manager
manager = get_ollama_manager()
models = manager.list_models()
assert isinstance(models, list)
'"

# Teste T2.A.7: Chat Engine criação de sessão
test_feature "T2.A.7 Chat Session Creation" \
    "python3 -c '
from apps.scripturemon.chat_engine import get_chat_engine
engine = get_chat_engine()
info = engine.get_session_info()
assert \"session_id\" in info
'"

# Teste T2.A.8: Context Manager criação de janela
test_feature "T2.A.8 Context Window Creation" \
    "python3 -c '
from apps.scripturemon.context_manager import get_context_manager
manager = get_context_manager()
window = manager.create_window(\"test\")
assert window.max_tokens > 0
'"

# Teste T2.A.9: Templates disponíveis
test_feature "T2.A.9 Templates Available" \
    "python3 -c '
from apps.scripturemon.prompt_templates import get_prompt_templates
templates = get_prompt_templates()
available = templates.list_templates()
assert len(available) > 10
'"

# Teste T2.A.10: Comando help no chat
test_feature "T2.A.10 Chat Command Help" \
    "python3 -c '
from apps.scripturemon.chat_engine import get_chat_engine
engine = get_chat_engine()
response = engine.handle_commands(\"/help\")
assert \"COMANDOS\" in response
'"

echo ""
echo "=========================================="
echo "📊 RESULTADO DOS TESTES DA FASE 2.A"
echo "✅ Passou: $PASSED/10"
echo "❌ Falhou: $FAILED/10"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 FASE 2.A - TODOS OS TESTES PASSARAM!${NC}"
    exit 0
else
    echo -e "${RED}⚠️ FASE 2.A - ALGUNS TESTES FALHARAM${NC}"
    exit 1
fi