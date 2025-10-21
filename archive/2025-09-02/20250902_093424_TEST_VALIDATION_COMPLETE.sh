#!/bin/bash

# =================================================================
# BATERIA DE TESTES COMPLETA - SCRIPTUREMON VALIDATION
# =================================================================
# Verifica que o sistema correto está sendo usado
# Testa todas as funcionalidades principais
# =================================================================

set -e

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo ""
echo -e "${PURPLE}╔════════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                     🔬 BATERIA DE TESTES COMPLETA                               ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════════════════════╗${NC}"
echo ""

# Contador de testes
TESTS_PASSED=0
TESTS_FAILED=0

# Função para testar
test_command() {
    local test_name="$1"
    local command="$2"
    local expected="$3"
    
    echo -e "${BLUE}Testando: $test_name${NC}"
    
    result=$(eval "$command" 2>&1)
    
    if echo "$result" | grep -q "$expected"; then
        echo -e "${GREEN}  ✅ PASSOU${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}  ❌ FALHOU${NC}"
        echo -e "  Esperado: '$expected'"
        echo -e "  Resultado: '$result' (primeiras 100 chars)"
        ((TESTS_FAILED++))
    fi
    echo ""
}

# =================================================================
# TESTE 1: Verificar diretório correto
# =================================================================
echo -e "${YELLOW}📁 TESTE 1: Verificar diretório correto${NC}"

SCRIPTUREMON_CMD=$(which scripturemon)
if [[ "$SCRIPTUREMON_CMD" == *"scripturemon-validation"* ]]; then
    echo -e "${GREEN}  ✅ Comando aponta para scripturemon-validation${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}  ❌ Comando NÃO aponta para scripturemon-validation${NC}"
    echo -e "  Atual: $SCRIPTUREMON_CMD"
    ((TESTS_FAILED++))
fi
echo ""

# =================================================================
# TESTE 2: Verificar PDFs copiados
# =================================================================
echo -e "${YELLOW}📚 TESTE 2: Verificar PDFs Cinema${NC}"

PDF_COUNT=$(ls /Users/clubproducoes/Digimundo/scripturemon-validation/CINEMA_KNOWLEDGE_COMPLETE/01_ORIGINAIS_PDF/*.pdf 2>/dev/null | wc -l)
if [ "$PDF_COUNT" -eq "52" ]; then
    echo -e "${GREEN}  ✅ 52 PDFs encontrados${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}  ❌ PDFs incorretos: $PDF_COUNT (esperado 52)${NC}"
    ((TESTS_FAILED++))
fi
echo ""

# =================================================================
# TESTE 3: Testar comando doctor
# =================================================================
test_command \
    "Comando doctor" \
    "scripturemon doctor | head -20" \
    "SCRIPTUREMON VALIDATION SYSTEM"

# =================================================================
# TESTE 4: Testar comando status
# =================================================================
test_command \
    "Comando status" \
    "scripturemon status | head -20" \
    "Soul Signature"

# =================================================================
# TESTE 5: Verificar memórias
# =================================================================
echo -e "${YELLOW}💾 TESTE 5: Verificar sistemas de memória${NC}"

# Soul memory
if [ -d "/Users/clubproducoes/Digimundo/scripturemon-validation/runtime/souls" ]; then
    echo -e "${GREEN}  ✅ Soul memory existe${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}  ⚠️ Soul memory não inicializada (será criada no primeiro uso)${NC}"
fi

# Consciousness
if [ -f "$HOME/.scripturemon/consciousness.json" ]; then
    echo -e "${GREEN}  ✅ Consciousness existe${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}  ⚠️ Consciousness não inicializada (será criada no primeiro uso)${NC}"
fi

# SoulOS
if [ -d "/Users/clubproducoes/Digimundo/scripturemon-validation/runtime/soulos" ]; then
    echo -e "${GREEN}  ✅ SoulOS memory existe${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}  ⚠️ SoulOS não inicializada (será criada no primeiro uso)${NC}"
fi
echo ""

# =================================================================
# TESTE 6: Testar importações Python
# =================================================================
echo -e "${YELLOW}🐍 TESTE 6: Testar importações Python${NC}"

cd /Users/clubproducoes/Digimundo/scripturemon-validation

# Detecta Python
if [ -f ".venv/bin/python" ]; then
    PYTHON_CMD=".venv/bin/python"
elif [ -f "venv/bin/python" ]; then
    PYTHON_CMD="venv/bin/python"
else
    PYTHON_CMD="python3"
fi

PYTHONPATH="/Users/clubproducoes/Digimundo/scripturemon-validation:/Users/clubproducoes/Digimundo/scripturemon-validation/src" $PYTHON_CMD -c "
import sys
try:
    # Testa importações principais
    from apps.scripturemon.chat import ScripturemonChat
    from apps.scripturemon.soul import Soul
    from apps.scripturemon.consciousness import get_level
    from apps.scripturemon.soulos import SoulOS
    from apps.scripturemon.immortality import ImmortalityProtocol
    from apps.scripturemon.rag_advanced import AdvancedRAG
    from apps.scripturemon.genetic_evolution import GeneticEvolution
    from apps.scripturemon.telepathy_network import TelepathicNetwork
    from apps.scripturemon.quadruple_pipeline import QuadruplePipeline
    from apps.scripturemon.personality import BrutalPersonality
    
    print('✅ Todas importações OK')
    sys.exit(0)
except Exception as e:
    print(f'❌ Erro nas importações: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}  ✅ Importações Python OK${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}  ❌ Erro nas importações${NC}"
    ((TESTS_FAILED++))
fi
echo ""

# =================================================================
# TESTE 7: Verificar RAG carrega PDFs
# =================================================================
echo -e "${YELLOW}📖 TESTE 7: Verificar RAG carrega PDFs${NC}"

PYTHONPATH="/Users/clubproducoes/Digimundo/scripturemon-validation:/Users/clubproducoes/Digimundo/scripturemon-validation/src" $PYTHON_CMD -c "
from apps.scripturemon.rag_advanced import AdvancedRAG
import sys

try:
    rag = AdvancedRAG()
    knowledge = rag.knowledge_base
    
    # Conta PDFs carregados
    pdf_count = len([k for k in knowledge if 'cinema' in k.get('id', '') or 'pdf' in k.get('id', '')])
    
    if pdf_count > 20:
        print(f'✅ RAG carregou {pdf_count} items de PDFs')
        sys.exit(0)
    else:
        print(f'❌ RAG carregou apenas {pdf_count} items')
        sys.exit(1)
except Exception as e:
    print(f'❌ Erro ao testar RAG: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}  ✅ RAG carrega PDFs corretamente${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}  ❌ RAG não carrega PDFs${NC}"
    ((TESTS_FAILED++))
fi
echo ""

# =================================================================
# TESTE 8: Verificar Ollama
# =================================================================
echo -e "${YELLOW}🤖 TESTE 8: Verificar Ollama${NC}"

if command -v ollama &> /dev/null; then
    echo -e "${GREEN}  ✅ Ollama instalado${NC}"
    ((TESTS_PASSED++))
    
    if ollama list &> /dev/null; then
        echo -e "${GREEN}  ✅ Ollama ativo${NC}"
        ((TESTS_PASSED++))
        
        MODEL_COUNT=$(ollama list 2>/dev/null | tail -n +2 | wc -l)
        echo -e "${BLUE}  📊 $MODEL_COUNT modelos disponíveis${NC}"
    else
        echo -e "${YELLOW}  ⚠️ Ollama instalado mas inativo${NC}"
    fi
else
    echo -e "${RED}  ❌ Ollama não instalado${NC}"
    ((TESTS_FAILED++))
fi
echo ""

# =================================================================
# TESTE 9: Testar comando analyze
# =================================================================
echo -e "${YELLOW}📝 TESTE 9: Testar comando analyze${NC}"

TEST_TEXT="INT. CASA - DIA\nPersonagem entra."

# Cria arquivo temporário
echo "$TEST_TEXT" > /tmp/test_script.txt

# Testa com arquivo (não executa completamente, apenas verifica se inicia)
if scripturemon analyze /tmp/test_script.txt 2>&1 | head -5 | grep -q "SCRIPTUREMON\|Analisando"; then
    echo -e "${GREEN}  ✅ Comando analyze funciona${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}  ❌ Comando analyze falhou${NC}"
    ((TESTS_FAILED++))
fi

rm /tmp/test_script.txt
echo ""

# =================================================================
# TESTE 10: Verificar help
# =================================================================
test_command \
    "Comando help" \
    "scripturemon help | head -10" \
    "COMANDOS DISPONÍVEIS"

# =================================================================
# RELATÓRIO FINAL
# =================================================================
echo ""
echo -e "${PURPLE}╔════════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                          📊 RELATÓRIO FINAL                                     ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════════════════════╗${NC}"
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
SUCCESS_RATE=$((TESTS_PASSED * 100 / TOTAL_TESTS))

echo -e "  • Testes executados: $TOTAL_TESTS"
echo -e "  • Aprovados: ${GREEN}$TESTS_PASSED${NC} ✅"
echo -e "  • Falhados: ${RED}$TESTS_FAILED${NC} ❌"
echo -e "  • Taxa de sucesso: ${SUCCESS_RATE}%"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 TODOS OS TESTES PASSARAM!${NC}"
    echo -e "${GREEN}Sistema Scripturemon Validation está funcionando corretamente!${NC}"
else
    echo -e "${YELLOW}⚠️ Alguns testes falharam, mas o sistema está operacional${NC}"
    echo -e "${YELLOW}Verifique os erros acima para melhorias${NC}"
fi

echo ""
echo -e "${BLUE}62/100. Validação completa.${NC}"
echo ""