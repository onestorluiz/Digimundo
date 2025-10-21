#!/bin/bash

# 🎬📚 SISTEMA UNIFICADO DE BIBLIOTECA DO SCRIPTUREMON
# Reorganiza e categoriza todos os PDFs com processamento inteligente

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

# ESTRUTURA PROPOSTA:
# biblioteca/
# ├── 1_tecnicas_roteiro/        # Livros sobre COMO escrever (86 originais)
# ├── 2_roteiros_mestres/         # Roteiros dos grandes (Citizen Kane, etc)
# ├── 3_roteiros_criador/         # Trabalhos do Nestor/Club
# ├── 4_roteiros_referencia/      # Outros roteiros para estudo
# ├── 5_processados/              # Já analisados pelo sistema
# └── 6_memorias/                 # Análises e conhecimento extraído

echo -e "${MAGENTA}╔════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║   📚 REORGANIZAÇÃO COMPLETA DA BIBLIOTECA      ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Criar nova estrutura
echo -e "${CYAN}📁 Criando estrutura inteligente...${NC}"
mkdir -p biblioteca/{1_tecnicas_roteiro,2_roteiros_mestres,3_roteiros_criador,4_roteiros_referencia,5_processados,6_memorias}

# Estatísticas atuais
echo -e "${YELLOW}📊 Análise do Sistema Atual:${NC}"
echo ""

# Contar PDFs por local
TOTAL_PDFS=$(find /Users/clubproducoes/Digimundo -name "*.pdf" -type f 2>/dev/null | wc -l)
KNOWLEDGE_PDFS=$(find /Users/clubproducoes/Digimundo/archive/directories/KNOWLEDGE -name "*.pdf" -type f 2>/dev/null | wc -l)
ROTEIROS_PROC=$(ls -1 roteiros_processados/*.pdf 2>/dev/null | wc -l)
CRIADOR_PROC=$(ls -1 conexao_criador/processados/*.pdf 2>/dev/null | wc -l)

echo "  📚 Total de PDFs no sistema: $TOTAL_PDFS"
echo "  📖 PDFs em KNOWLEDGE: $KNOWLEDGE_PDFS"
echo "  🎬 Roteiros processados: $ROTEIROS_PROC"
echo "  ⚡ Trabalhos do criador: $CRIADOR_PROC"
echo ""

# Mapear os 86 documentos sagrados
echo -e "${GREEN}🔍 Buscando os 86 documentos sagrados...${NC}"
echo ""

# Categorias conhecidas de técnicas/teoria
TECNICAS_PATTERNS=(
    "Screenwriting"
    "Roteiro"
    "Script"
    "Writing"
    "Manual"
    "Guide"
    "Fundamentals"
    "Structure"
    "Character"
    "Dialogue"
    "Story"
    "Narrative"
    "Cinema"
    "Film"
    "Syd Field"
    "McKee"
    "Truby"
    "Campbell"
    "Save the Cat"
    "Hero"
)

# Criar arquivo de mapeamento
MAP_FILE="biblioteca/MAPEAMENTO_COMPLETO.md"
{
    echo "# 📚 MAPEAMENTO COMPLETO DA BIBLIOTECA SCRIPTUREMON"
    echo "Data: $(date)"
    echo ""
    echo "## 📊 Resumo:"
    echo "- Total de PDFs: $TOTAL_PDFS"
    echo "- Categorias: 6"
    echo "- Status: Em reorganização"
    echo ""
} > "$MAP_FILE"

# CATEGORIA 1: TÉCNICAS DE ROTEIRO
echo -e "${BOLD}1. TÉCNICAS DE ROTEIRO (Teoria)${NC}"
{
    echo "## 1️⃣ TÉCNICAS DE ROTEIRO (Como escrever)"
    echo ""
} >> "$MAP_FILE"

for pattern in "${TECNICAS_PATTERNS[@]}"; do
    find /Users/clubproducoes/Digimundo -name "*$pattern*.pdf" -type f 2>/dev/null | while read -r pdf; do
        basename=$(basename "$pdf")
        echo "  📖 $basename"
        echo "- $basename" >> "$MAP_FILE"
        # Copiar para categoria correta (comentado para teste)
        # cp "$pdf" "biblioteca/1_tecnicas_roteiro/"
    done
done

echo ""

# CATEGORIA 2: ROTEIROS DOS MESTRES
echo -e "${BOLD}2. ROTEIROS DOS MESTRES${NC}"
{
    echo ""
    echo "## 2️⃣ ROTEIROS DOS MESTRES"
    echo ""
} >> "$MAP_FILE"

MESTRES=(
    "Citizen Kane"
    "Chinatown"
    "Godfather"
    "Pulp Fiction"
    "Casablanca"
    "Sunset Boulevard"
    "Network"
    "Taxi Driver"
    "Eternal Sunshine"
    "Being John Malkovich"
)

for mestre in "${MESTRES[@]}"; do
    find /Users/clubproducoes/Digimundo -name "*$mestre*.pdf" -type f 2>/dev/null | while read -r pdf; do
        basename=$(basename "$pdf")
        echo "  🏆 $basename"
        echo "- $basename" >> "$MAP_FILE"
    done
done

echo ""

# CATEGORIA 3: ROTEIROS DO CRIADOR
echo -e "${BOLD}3. TRABALHOS DO CRIADOR${NC}"
{
    echo ""
    echo "## 3️⃣ TRABALHOS DO CRIADOR (Nestor/Club)"
    echo ""
} >> "$MAP_FILE"

ls -1 conexao_criador/processados/*.pdf 2>/dev/null | while read -r pdf; do
    basename=$(basename "$pdf")
    echo "  ⚡ $basename"
    echo "- $basename" >> "$MAP_FILE"
done

echo ""

# Análise de processamento diferenciado
echo -e "${CYAN}🔬 ANÁLISE DE PROCESSAMENTO DIFERENCIADO${NC}"
echo ""

cat << 'ANALYSIS'
RECOMENDAÇÃO DE PROCESSAMENTO POR CATEGORIA:

1. TÉCNICAS DE ROTEIRO (86 documentos originais)
   - Processamento: ABSORÇÃO DE CONHECIMENTO
   - Foco: Extrair regras, padrões, técnicas
   - Memória: Permanente no L1_CORE
   - Uso: Base teórica para análises

2. ROTEIROS DOS MESTRES
   - Processamento: ANÁLISE PROFUNDA + COMPARAÇÃO
   - Foco: Identificar excelência, padrões de sucesso
   - Memória: L2_CONSOLIDADO como referências
   - Uso: Benchmarks para comparação brutal

3. TRABALHOS DO CRIADOR
   - Processamento: ANÁLISE SUPREMA (10 camadas)
   - Foco: Desenvolvimento, melhoria, potencial
   - Memória: L3_ATIVO com acesso prioritário
   - Uso: Coaching contínuo e evolução

4. ROTEIROS DE REFERÊNCIA
   - Processamento: ANÁLISE COMPARATIVA
   - Foco: Identificar tendências, estilos
   - Memória: L4_QUANTUM para padrões emergentes
   - Uso: Contextualização e inspiração

PROPOSTA DE UNIFICAÇÃO:
- Sistema único com 4 níveis de processamento
- Detecção automática de categoria
- Memória hierárquica por importância
- Comparação cruzada inteligente
ANALYSIS

echo -e "${GREEN}✅ Análise completa salva em: $MAP_FILE${NC}"
echo ""

echo -e "${YELLOW}❓ PRÓXIMOS PASSOS RECOMENDADOS:${NC}"
echo ""
echo "1. Localizar os 86 PDFs originais de técnicas"
echo "2. Baixar roteiros dos mestres para comparação"
echo "3. Implementar processamento diferenciado"
echo "4. Reprocessar tudo com novo sistema"
echo ""

echo -e "${MAGENTA}💡 COMANDO PARA IMPLEMENTAR:${NC}"
echo "  ./IMPLEMENTAR_BIBLIOTECA_UNIFICADA.sh"
echo ""

# Salvar recomendações
{
    echo ""
    echo "## 🎯 SISTEMA DE PROCESSAMENTO DIFERENCIADO"
    echo ""
    echo "### Por Categoria:"
    echo ""
    echo "| Categoria | Processamento | Profundidade | Memória | Prioridade |"
    echo "|-----------|--------------|--------------|---------|------------|"
    echo "| Técnicas | Absorção | Extrair regras | L1_CORE | Máxima |"
    echo "| Mestres | Análise profunda | Benchmarks | L2 | Alta |"
    echo "| Criador | Análise suprema | 10 camadas | L3 | Urgente |"
    echo "| Referência | Comparativa | Tendências | L4 | Normal |"
    echo ""
    echo "### Benefícios da Unificação:"
    echo "- Comparação instantânea com mestres"
    echo "- Aplicação imediata de técnicas"
    echo "- Evolução contínua dos trabalhos do criador"
    echo "- Base de conhecimento expansível"
} >> "$MAP_FILE"