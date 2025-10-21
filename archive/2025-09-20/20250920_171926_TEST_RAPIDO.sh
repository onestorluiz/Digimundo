#!/bin/bash

# 🎬 TESTE RÁPIDO - VALIDAÇÃO DE MEMÓRIA

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
NC='\033[0m'

PASSED=0
FAILED=0

echo -e "${MAGENTA}╔═══════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║   🎬 TESTE RÁPIDO - SCRIPTUREMON          ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════╝${NC}"
echo ""

# Função de teste simplificada
test_question() {
    local question="$1"
    local expected="$2"
    local name="$3"
    
    echo -e "${CYAN}Teste: $name${NC}"
    echo "Pergunta: $question"
    
    # Executar diretamente
    RESPONSE=$(echo "$question" | ollama run scripturemon 2>&1)
    
    # Verificar resposta
    if [[ "$RESPONSE" == *"$expected"* ]]; then
        echo -e "${GREEN}✅ PASSOU${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ FALHOU - Esperava: '$expected'${NC}"
        echo "Resposta: $(echo "$RESPONSE" | head -1)"
        ((FAILED++))
    fi
    echo ""
}

# TESTES ESSENCIAIS
echo -e "${BOLD}CATEGORIA 1: MEMÓRIA BÁSICA${NC}"
echo ""

test_question \
    "qual o nome do meu filme?" \
    "Sonhos Sem Lembranças" \
    "Reconhecimento do título"

test_question \
    "quem é o autor de SONHOS SEM LEMBRANÇAS?" \
    "Nestor" \
    "Identificação do autor"

test_question \
    "qual nota você deu para meu roteiro?" \
    "85" \
    "Memória de métricas"

echo -e "${BOLD}CATEGORIA 2: ANÁLISE ESPECÍFICA${NC}"
echo ""

test_question \
    "quantos atos tem SONHOS SEM LEMBRANÇAS?" \
    "3" \
    "Estrutura conhecida"

test_question \
    "o que significa T.3 no título?" \
    "trilogia" \
    "Compreensão do título"

test_question \
    "qual o tema principal do meu filme?" \
    "sonhos" \
    "Conhecimento temático"

echo -e "${BOLD}CATEGORIA 3: CONTEXTO PROFUNDO${NC}"
echo ""

test_question \
    "compare meu roteiro com Inception" \
    "sonhos" \
    "Análise comparativa"

test_question \
    "você analisou meu roteiro em quantas camadas?" \
    "10" \
    "Memória do processo"

# RESULTADOS
echo -e "${MAGENTA}═══════════════════════════════════════${NC}"
echo -e "${BOLD}RESULTADOS:${NC}"
echo -e "${GREEN}Passou: $PASSED${NC}"
echo -e "${RED}Falhou: $FAILED${NC}"

TOTAL=$((PASSED + FAILED))
SCORE=$((PASSED * 100 / TOTAL))

echo -e "${BOLD}Score: ${SCORE}%${NC}"

if [ $SCORE -ge 80 ]; then
    echo -e "${GREEN}🏆 EXCELENTE! Memória funcionando perfeitamente!${NC}"
elif [ $SCORE -ge 60 ]; then
    echo -e "${YELLOW}👍 BOM! Memória parcialmente funcional.${NC}"
else
    echo -e "${RED}❌ PROBLEMA! Memória não está funcionando.${NC}"
fi