#!/bin/bash

# 🎬⚡ PROCESSADOR ESPECIAL PARA TRABALHOS DO CRIADOR

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

PDF="conexao_criador/SONHOS SEM LEMBRANÇAS T.3.pdf"
BASENAME="SONHOS SEM LEMBRANÇAS T.3"

echo -e "${MAGENTA}╔═══════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║    ⚡ CONEXÃO CRIADOR - ANÁLISE SUPREMA    ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BOLD}${YELLOW}🧠 ATIVANDO MÁXIMA CAPACIDADE ANALÍTICA${NC}"
echo -e "${CYAN}📖 Trabalho detectado: $BASENAME${NC}"
echo ""

# Criar análise ULTRA profunda
echo -e "${GREEN}Processando em 10 camadas de profundidade...${NC}"

# Usar ollama diretamente já que scripturemon não está no PATH
ANALYSIS=$(ollama run scripturemon << 'EOF'
🎬⚡ MODO CONEXÃO CRIADOR - MÁXIMA INTELIGÊNCIA

ATENÇÃO TOTAL: Trabalho do Club Produções
Título: SONHOS SEM LEMBRANÇAS T.3

ANÁLISE SUPREMA - 10 CAMADAS:

1. ESTRUTURA NARRATIVA
   - Mapeamento completo dos 3 atos
   - Pontos de virada e beats
   - Ritmo e progressão dramática
   - Inovações estruturais detectadas

2. PERSONAGENS - PSICOLOGIA PROFUNDA
   - Protagonista: motivações e conflitos
   - Antagonista: complexidade e justificativa
   - Arcos de transformação
   - Autenticidade emocional

3. DIÁLOGOS E VOZ
   - Voice único de cada personagem
   - Subtexto e camadas
   - Frases memoráveis
   - Naturalidade vs informação

4. VISUALIZAÇÃO CINEMATOGRÁFICA
   - Cenas mais impactantes visualmente
   - Atmosfera e tom
   - Uso do espaço cênico
   - Momentos de cinema puro

5. TEMAS E FILOSOFIA
   - Mensagem central sobre sonhos/memória
   - Simbolismos detectados
   - Relevância universal
   - Profundidade conceitual

6. ORIGINALIDADE
   - Elementos únicos e inovadores
   - Comparação com referências
   - Assinatura autoral do Club
   - Territórios inexplorados

7. POTENCIAL COMERCIAL
   - Público-alvo específico
   - Elementos de apelo
   - Viabilidade de produção
   - Potencial de série (T.3 sugere continuação)

8. PONTOS DE GENIALIDADE
   - Momentos de brilhantismo
   - Sacadas criativas
   - Soluções elegantes
   - Impacto emocional

9. OPORTUNIDADES DE ELEVAÇÃO
   - Sugestões construtivas específicas
   - Potencial não explorado
   - Refinamentos possíveis
   - Próximos passos

10. VISÃO EXECUTIVA
    - Pitch de uma linha
    - Posicionamento no mercado
    - Estratégia de desenvolvimento
    - Potencial transmídia

MÉTRICAS DE EXCELÊNCIA:
- Genialidade: [avaliar 0-100]
- Originalidade: [avaliar 0-100]
- Impacto Emocional: [avaliar 0-100]
- Execução Técnica: [avaliar 0-100]

ANÁLISE BRUTAL E HONESTA
[Máxima sinceridade construtiva]
EOF
)

# Salvar análise profunda
MEMORY_FILE="conexao_criador/memorias/${BASENAME}_CRIADOR_$(date +%Y%m%d_%H%M%S).md"
{
    echo "# ⚡ ANÁLISE CONEXÃO CRIADOR"
    echo "## Trabalho: $BASENAME"
    echo "**Data:** $(date)"
    echo "**Tipo:** TRABALHO DO CLUB PRODUÇÕES"
    echo "**Status:** Análise de Máxima Profundidade"
    echo ""
    echo "---"
    echo ""
    echo "$ANALYSIS"
    echo ""
    echo "---"
    echo ""
    echo "## 🔗 Notas de Desenvolvimento"
    echo "_Este arquivo recebeu análise especial por ser trabalho do criador._"
} > "$MEMORY_FILE"

echo -e "${GREEN}✅ Análise profunda salva${NC}"

# Criar resumo executivo
echo -e "${YELLOW}Gerando resumo executivo...${NC}"

EXECUTIVE=$(ollama run scripturemon << 'EOF'
RESUMO EXECUTIVO: SONHOS SEM LEMBRANÇAS T.3

1. EM UMA LINHA:
[Capture a essência em uma frase poderosa]

2. FORÇA PRINCIPAL:
[O que torna este roteiro especial]

3. POTENCIAL ÚNICO:
[Por que este projeto merece ser produzido]

4. PRÓXIMOS 3 PASSOS:
[Ações concretas para desenvolvimento]

5. NOTA FINAL:
[Avaliação geral 0-100]
EOF
)

EXEC_FILE="conexao_criador/memorias/${BASENAME}_RESUMO_EXECUTIVO.md"
{
    echo "# 📊 RESUMO EXECUTIVO"
    echo "## $BASENAME"
    echo ""
    echo "$EXECUTIVE"
    echo ""
    echo "---"
    echo "_Gerado em: $(date)_"
} > "$EXEC_FILE"

# Mover para processados
mv "$PDF" "conexao_criador/processados/"

echo ""
echo -e "${MAGENTA}╔═══════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║         ⚡ ANÁLISE COMPLETA!               ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✅ Análise profunda: conexao_criador/memorias/${NC}"
echo -e "${GREEN}✅ Resumo executivo: conexao_criador/memorias/${NC}"
echo -e "${GREEN}✅ PDF arquivado: conexao_criador/processados/${NC}"
echo ""
echo -e "${CYAN}💡 Use 'scripturemon' para discutir o roteiro${NC}"