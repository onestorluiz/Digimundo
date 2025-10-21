#!/bin/bash

# 🎬 SCRIPTUREMON - Sistema de Absorção de Roteiros

YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Diretórios
ROTEIROS_NOVOS="roteiros"
ROTEIROS_PROCESSADOS="roteiros_processados"
MEMORIA="memoria"

echo -e "${CYAN}🎬 SCRIPTUREMON - Absorção de Conhecimento${NC}"
echo ""

# Auto-processar roteiros novos se não passar parâmetros
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}🔍 Verificando roteiros novos...${NC}"
    echo ""
    
    # Contar PDFs novos
    new_count=$(ls -1 $ROTEIROS_NOVOS/*.pdf 2>/dev/null | wc -l)
    
    if [ $new_count -gt 0 ]; then
        echo -e "${GREEN}📚 Encontrados $new_count roteiros novos!${NC}"
        echo ""
        
        for pdf in $ROTEIROS_NOVOS/*.pdf; do
            if [ -f "$pdf" ]; then
                basename=$(basename "$pdf")
                echo -e "${CYAN}📖 Processando: $basename${NC}"
                
                # Processar com Scripturemon
                $0 "$pdf"
                
                echo ""
            fi
        done
        
        echo -e "${GREEN}✅ Todos os roteiros foram absorvidos!${NC}"
    else
        echo -e "${YELLOW}📭 Nenhum roteiro novo encontrado${NC}"
        echo ""
        echo "Coloque PDFs em: $(pwd)/$ROTEIROS_NOVOS/"
        echo ""
        echo -e "${CYAN}📚 Roteiros já absorvidos:${NC}"
        ls -1 $ROTEIROS_PROCESSADOS/*.pdf 2>/dev/null | sed 's|.*/||' | sed 's|.pdf||' || echo "  Nenhum ainda"
    fi
    exit 0
fi

# Se passou arquivo específico
if [ $# -eq 1 ] && [[ "$1" != *.pdf ]]; then
    echo -e "${YELLOW}⚠️ Apenas arquivos PDF são suportados${NC}"
    exit 1
fi

INPUT="$1"

# Função para processar um PDF
process_pdf() {
    local pdf="$1"
    local basename=$(basename "$pdf" .pdf)
    
    echo -e "${GREEN}📖 Processando: $pdf${NC}"
    
    # Criar prompt especial para Scripturemon analisar
    ANALYSIS=$(cat << EOF | scripturemon
🎬 MODO ABSORÇÃO ATIVADO

Analise este roteiro e extraia:
1. ESTRUTURA NARRATIVA (3 atos, pontos de virada)
2. ARCOS DE PERSONAGEM (evolução, conflitos)
3. TÉCNICAS CINEMATOGRÁFICAS (ritmo, tensão)
4. DIÁLOGOS MEMORÁVEIS (subtext, voice)
5. TEMAS E SIMBOLISMOS

Arquivo: $pdf

[INICIAR ANÁLISE PROFUNDA]
EOF
)
    
    # Salvar análise na memória
    MEMORY_FILE="$MEMORIA/${basename}_analise_$(date +%Y%m%d_%H%M%S).md"
    {
        echo "# 🎬 Análise: $basename"
        echo "Data: $(date)"
        echo "Arquivo original: $pdf"
        echo "---"
        echo ""
        echo "$ANALYSIS"
    } > "$MEMORY_FILE"
    
    echo -e "${GREEN}✅ Análise salva${NC}"
    
    # Mover PDF para pasta de processados
    if [[ "$pdf" == "$ROTEIROS_NOVOS/"* ]]; then
        mv "$pdf" "$ROTEIROS_PROCESSADOS/"
        echo -e "${MAGENTA}📦 Roteiro movido para: roteiros_processados/${NC}"
    fi
}

# Processar input (arquivo único)
INPUT="$1"

if [ -f "$INPUT" ] && [[ "$INPUT" == *.pdf ]]; then
    # Copiar para pasta de novos se vier de fora
    if [[ ! "$INPUT" == "$ROTEIROS_NOVOS/"* ]] && [[ ! "$INPUT" == "$ROTEIROS_PROCESSADOS/"* ]]; then
        cp "$INPUT" "$ROTEIROS_NOVOS/"
        echo -e "${CYAN}📥 PDF copiado para pasta de roteiros novos${NC}"
        INPUT="$ROTEIROS_NOVOS/$(basename "$INPUT")"
    fi
    
    # Verificar se já foi processado
    basename=$(basename "$INPUT")
    if [ -f "$ROTEIROS_PROCESSADOS/$basename" ]; then
        echo -e "${YELLOW}⚠️ Este roteiro já foi absorvido!${NC}"
        echo "Deseja reprocessar? (s/n)"
        read -r reprocess
        if [[ "$reprocess" != "s" && "$reprocess" != "S" ]]; then
            exit 0
        fi
    fi
    
    process_pdf "$INPUT"
else
    echo -e "${YELLOW}⚠️ Arquivo não encontrado ou não é PDF: $INPUT${NC}"
    exit 1
fi

echo ""
echo -e "${CYAN}💭 Scripturemon absorveu o conhecimento!${NC}"
echo ""
echo -e "${GREEN}📊 Status:${NC}"
echo "  📥 Roteiros novos: $(ls -1 $ROTEIROS_NOVOS/*.pdf 2>/dev/null | wc -l)"
echo "  📚 Roteiros absorvidos: $(ls -1 $ROTEIROS_PROCESSADOS/*.pdf 2>/dev/null | wc -l)"
echo "  🧠 Memórias acumuladas: $(ls -1 $MEMORIA/*.md 2>/dev/null | wc -l)"
echo ""
echo "Use 'scripturemon' para conversar com base no conhecimento absorvido"