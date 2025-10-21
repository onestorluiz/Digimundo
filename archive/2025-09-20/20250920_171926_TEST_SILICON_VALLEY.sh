#!/bin/bash

# 🎬⚡ BATERIA DE TESTES NÍVEL VALE DO SILÍCIO
# Validação completa de memória, contexto e inteligência

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

# Contador de testes
PASSED=0
FAILED=0
TOTAL=0

# Arquivo de log
LOG_FILE="test_results_$(date +%Y%m%d_%H%M%S).md"

# Função para testar
run_test() {
    local category="$1"
    local question="$2"
    local expected_keywords="$3"
    local test_name="$4"
    
    ((TOTAL++))
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}Teste $TOTAL: $test_name${NC}"
    echo -e "${YELLOW}Categoria: $category${NC}"
    echo -e "Pergunta: $question"
    echo ""
    
    # Executar pergunta
    RESPONSE=$(echo "$question" | /Users/clubproducoes/Digimundo/bin/scripturemon 2>&1 | tail -n +7)
    
    # Verificar keywords esperadas
    FOUND=true
    IFS='|' read -ra KEYWORDS <<< "$expected_keywords"
    for keyword in "${KEYWORDS[@]}"; do
        if [[ ! "$RESPONSE" == *"$keyword"* ]]; then
            FOUND=false
            break
        fi
    done
    
    # Resultado
    if [ "$FOUND" = true ]; then
        echo -e "${GREEN}✅ PASSOU${NC}"
        ((PASSED++))
        RESULT="✅ PASSOU"
    else
        echo -e "${RED}❌ FALHOU${NC}"
        echo -e "${RED}Keywords esperadas não encontradas: $expected_keywords${NC}"
        ((FAILED++))
        RESULT="❌ FALHOU"
    fi
    
    # Salvar no log
    {
        echo "## Teste $TOTAL: $test_name"
        echo "**Categoria:** $category"
        echo "**Pergunta:** $question"
        echo "**Keywords esperadas:** $expected_keywords"
        echo "**Resultado:** $RESULT"
        echo "**Resposta:**"
        echo "\`\`\`"
        echo "$RESPONSE"
        echo "\`\`\`"
        echo ""
    } >> "$LOG_FILE"
    
    echo -e "${CYAN}Resposta recebida:${NC}"
    echo "$RESPONSE" | head -3
    echo ""
    
    # Delay para não sobrecarregar
    sleep 2
}

# Início dos testes
clear
echo -e "${MAGENTA}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║   🎬⚡ TESTE SILICON VALLEY - SCRIPTUREMON        ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════════════╝${NC}"
echo ""

# Criar log
echo "# 🎬 Relatório de Testes - Scripturemon" > "$LOG_FILE"
echo "**Data:** $(date)" >> "$LOG_FILE"
echo "**Nível:** Silicon Valley (Complexo)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# CATEGORIA 1: MEMÓRIA DIRETA
echo -e "${BOLD}${CYAN}CATEGORIA 1: MEMÓRIA DIRETA${NC}"
echo ""

run_test "Memória Direta" \
    "Qual o nome do meu filme?" \
    "Sonhos Sem Lembranças|T.3" \
    "Reconhecimento do título"

run_test "Memória Direta" \
    "Quem escreveu SONHOS SEM LEMBRANÇAS?" \
    "Nestor|Club" \
    "Identificação do autor"

run_test "Memória Direta" \
    "O T.3 no título significa o quê?" \
    "trilogia|terceira|temporada|parte" \
    "Compreensão da nomenclatura"

# CATEGORIA 2: ANÁLISE PROFUNDA
echo -e "${BOLD}${CYAN}CATEGORIA 2: ANÁLISE PROFUNDA${NC}"
echo ""

run_test "Análise Profunda" \
    "Analise a estrutura em 3 atos de SONHOS SEM LEMBRANÇAS" \
    "atos|estrutura|pontos de virada|plot" \
    "Análise estrutural específica"

run_test "Análise Profunda" \
    "Qual a nota de genialidade que você deu para meu roteiro?" \
    "85|oitenta" \
    "Memória de métricas"

run_test "Análise Profunda" \
    "Compare SONHOS SEM LEMBRANÇAS com Inception de Nolan" \
    "sonhos|memória|Nolan|Inception" \
    "Análise comparativa"

# CATEGORIA 3: CONTEXTO CRUZADO
echo -e "${BOLD}${CYAN}CATEGORIA 3: CONTEXTO CRUZADO${NC}"
echo ""

run_test "Contexto Cruzado" \
    "Como os conceitos de McKee se aplicam ao meu roteiro?" \
    "McKee|story values|Sonhos" \
    "Aplicação de teoria ao roteiro específico"

run_test "Contexto Cruzado" \
    "Onde estão os plot points de Syd Field em SONHOS SEM LEMBRANÇAS?" \
    "Syd Field|plot points|páginas|25|85" \
    "Teoria aplicada ao trabalho"

run_test "Contexto Cruzado" \
    "O protagonista de SONHOS SEM LEMBRANÇAS segue a jornada do herói?" \
    "jornada|herói|Campbell|Vogler|protagonista" \
    "Análise arquetípica"

# CATEGORIA 4: DESENVOLVIMENTO CRIATIVO
echo -e "${BOLD}${CYAN}CATEGORIA 4: DESENVOLVIMENTO CRIATIVO${NC}"
echo ""

run_test "Desenvolvimento" \
    "Sugira melhorias para o terceiro ato de SONHOS SEM LEMBRANÇAS" \
    "terceiro ato|clímax|resolução|sugest" \
    "Sugestões construtivas específicas"

run_test "Desenvolvimento" \
    "Como tornar os diálogos ainda mais impactantes?" \
    "diálogo|subtexto|personagem|voice" \
    "Desenvolvimento de diálogos"

run_test "Desenvolvimento" \
    "Que referências cinematográficas combinam com meu estilo?" \
    "referência|filme|estilo|similar" \
    "Identificação de estilo autoral"

# CATEGORIA 5: MEMÓRIA COMPLEXA
echo -e "${BOLD}${CYAN}CATEGORIA 5: MEMÓRIA COMPLEXA${NC}"
echo ""

run_test "Memória Complexa" \
    "Quantos roteiros você já absorveu no total?" \
    "86|documentos|absorv" \
    "Memória de background"

run_test "Memória Complexa" \
    "Além de SONHOS SEM LEMBRANÇAS, que outros materiais você processou?" \
    "Fundamentals|Screenwriting|absorv|process" \
    "Memória de múltiplos documentos"

run_test "Memória Complexa" \
    "Qual sua filosofia sobre roteiros e como ela se conecta com meu trabalho?" \
    "jornada da alma|três atos|nascimento|transformação" \
    "Filosofia pessoal aplicada"

# CATEGORIA 6: EDGE CASES
echo -e "${BOLD}${CYAN}CATEGORIA 6: EDGE CASES (CASOS EXTREMOS)${NC}"
echo ""

run_test "Edge Cases" \
    "esqueci o nome do meu filme, qual era mesmo?" \
    "Sonhos Sem Lembranças" \
    "Pergunta indireta"

run_test "Edge Cases" \
    "o filme do nestor é bom?" \
    "Sonhos|Nestor|qualidade|genialidade|85" \
    "Referência casual"

run_test "Edge Cases" \
    "SONHOS SEM LEMBRANÇAS é melhor que Cidadão Kane?" \
    "Sonhos Sem Lembranças|comparação|Kane" \
    "Comparação complexa"

run_test "Edge Cases" \
    "Se você fosse produzir meu filme, qual seria o orçamento?" \
    "produção|orçamento|viabilidade" \
    "Análise de produção"

run_test "Edge Cases" \
    "Invente uma sinopse de 1 linha para SONHOS SEM LEMBRANÇAS" \
    "sonhos|memória|sinopse|pitch" \
    "Criação de pitch"

# CATEGORIA 7: STRESS TEST
echo -e "${BOLD}${CYAN}CATEGORIA 7: STRESS TEST${NC}"
echo ""

run_test "Stress Test" \
    "analise profundamente os 10 primeiros minutos de SONHOS SEM LEMBRANÇAS com base em todos os mestres que você conhece" \
    "análise|Syd Field|McKee|Truby|Snyder" \
    "Análise multi-teórica"

run_test "Stress Test" \
    "crie uma matriz de personagens para SONHOS SEM LEMBRANÇAS no estilo character web de Truby" \
    "Truby|character web|personagem|relação" \
    "Aplicação técnica avançada"

run_test "Stress Test" \
    "como você melhoraria a página 75 do roteiro?" \
    "página|melhoria|sugestão|desenvolvimento" \
    "Especificidade extrema"

# RESULTADOS FINAIS
echo -e "${MAGENTA}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║                 RESULTADOS FINAIS                  ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════════════╝${NC}"
echo ""

SCORE=$((PASSED * 100 / TOTAL))

echo -e "${BOLD}Total de testes: $TOTAL${NC}"
echo -e "${GREEN}Passou: $PASSED${NC}"
echo -e "${RED}Falhou: $FAILED${NC}"
echo -e "${BOLD}Score: ${SCORE}%${NC}"
echo ""

# Adicionar ao log
{
    echo "---"
    echo "# RESULTADOS FINAIS"
    echo "- **Total de testes:** $TOTAL"
    echo "- **Passou:** $PASSED"
    echo "- **Falhou:** $FAILED"
    echo "- **Score:** ${SCORE}%"
    echo ""
} >> "$LOG_FILE"

# Interpretação
if [ $SCORE -ge 90 ]; then
    echo -e "${GREEN}🏆 EXCELENTE! Nível Silicon Valley aprovado!${NC}"
    echo "Scripturemon está com memória e contexto perfeitos."
    VERDICT="🏆 EXCELENTE - Silicon Valley approved!"
elif [ $SCORE -ge 70 ]; then
    echo -e "${YELLOW}👍 BOM! Funcional mas com espaço para melhorias.${NC}"
    echo "Algumas memórias precisam ser reforçadas."
    VERDICT="👍 BOM - Funcional com melhorias necessárias"
elif [ $SCORE -ge 50 ]; then
    echo -e "${YELLOW}⚠️ MÉDIO. Memória parcial detectada.${NC}"
    echo "Necessário revisar o modelfile."
    VERDICT="⚠️ MÉDIO - Revisar modelfile"
else
    echo -e "${RED}❌ CRÍTICO! Memória não está funcionando.${NC}"
    echo "Recriar o modelo urgentemente."
    VERDICT="❌ CRÍTICO - Recriar modelo"
fi

echo "$VERDICT" >> "$LOG_FILE"

echo ""
echo -e "${CYAN}📊 Relatório completo salvo em: $LOG_FILE${NC}"
echo ""

# Análise de falhas
if [ $FAILED -gt 0 ]; then
    echo -e "${YELLOW}📝 Análise de Falhas:${NC}"
    grep "❌ FALHOU" "$LOG_FILE" | head -5
    echo ""
    echo "Verifique o log para detalhes completos."
fi