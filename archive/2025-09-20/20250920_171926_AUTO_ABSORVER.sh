#!/bin/bash

# 🎬 SCRIPTUREMON - Auto-Absorção Inteligente
# Roda automaticamente quando detecta PDFs novos

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
RED='\033[0;31m'
NC='\033[0m'

clear

echo -e "${CYAN}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     🎬 SCRIPTUREMON AUTO-ABSORÇÃO         ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════╝${NC}"
echo ""

# Verificar roteiros novos
NEW_COUNT=$(ls -1 roteiros/*.pdf 2>/dev/null | wc -l)
PROCESSED_COUNT=$(ls -1 roteiros_processados/*.pdf 2>/dev/null | wc -l)

echo -e "${YELLOW}📊 Status Atual:${NC}"
echo -e "  📥 Roteiros novos: ${GREEN}$NEW_COUNT${NC}"
echo -e "  📚 Roteiros absorvidos: ${CYAN}$PROCESSED_COUNT${NC}"
echo ""

if [ $NEW_COUNT -eq 0 ]; then
    echo -e "${YELLOW}📭 Nenhum roteiro novo para absorver${NC}"
    echo ""
    echo "Coloque PDFs em: $(pwd)/roteiros/"
    echo ""
    
    if [ $PROCESSED_COUNT -gt 0 ]; then
        echo -e "${CYAN}📚 Roteiros já absorvidos:${NC}"
        ls -1 roteiros_processados/*.pdf 2>/dev/null | sed 's|.*/||' | sed 's|.pdf||' | head -10
        
        if [ $PROCESSED_COUNT -gt 10 ]; then
            echo "  ... e mais $((PROCESSED_COUNT - 10)) roteiros"
        fi
    fi
    exit 0
fi

echo -e "${GREEN}🎯 Encontrados $NEW_COUNT roteiros novos para absorver!${NC}"
echo ""

# Mostrar lista de roteiros novos
echo -e "${CYAN}📋 Roteiros a processar:${NC}"
for pdf in roteiros/*.pdf; do
    if [ -f "$pdf" ]; then
        basename=$(basename "$pdf" .pdf)
        echo "  • $basename"
    fi
done

echo ""
echo -e "${YELLOW}Iniciar absorção? (s/n)${NC}"
read -r confirm

if [[ "$confirm" != "s" && "$confirm" != "S" ]]; then
    echo -e "${RED}Absorção cancelada${NC}"
    exit 0
fi

echo ""
echo -e "${MAGENTA}🧠 Iniciando processo de absorção...${NC}"
echo ""

# Processar cada roteiro
for pdf in roteiros/*.pdf; do
    if [ -f "$pdf" ]; then
        basename=$(basename "$pdf" .pdf)
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${GREEN}📖 Absorvendo: $basename${NC}"
        echo ""
        
        # Invocar Scripturemon para análise profunda
        ANALYSIS=$(scripturemon << EOF
🎬 MODO ABSORÇÃO PROFUNDA

Analise este roteiro: $basename

EXTRAIR E APRENDER:
1. ESTRUTURA (3 atos, pontos de virada, clímax)
2. PERSONAGENS (arcos, motivações, conflitos)
3. DIÁLOGOS (voice único, subtext, memoráveis)
4. TÉCNICAS (ritmo, tensão, transições)
5. TEMAS (mensagem central, simbolismos)

Absorva esses padrões para uso futuro.
[INICIAR ANÁLISE]
EOF
)
        
        # Salvar na memória
        MEMORY_FILE="memoria/${basename}_$(date +%Y%m%d_%H%M%S).md"
        {
            echo "# 🎬 Conhecimento Absorvido: $basename"
            echo "**Data:** $(date)"
            echo "**Arquivo:** $pdf"
            echo ""
            echo "---"
            echo ""
            echo "$ANALYSIS"
            echo ""
            echo "---"
            echo "_Status: Totalmente absorvido_"
        } > "$MEMORY_FILE"
        
        # Mover para processados
        mv "$pdf" "roteiros_processados/"
        
        echo ""
        echo -e "${GREEN}✅ Absorvido e arquivado!${NC}"
        echo -e "${MAGENTA}→ Memória salva em: memoria/${NC}"
        echo -e "${MAGENTA}→ PDF movido para: roteiros_processados/${NC}"
        echo ""
    fi
done

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Resumo final
NEW_NOW=$(ls -1 roteiros/*.pdf 2>/dev/null | wc -l)
PROCESSED_NOW=$(ls -1 roteiros_processados/*.pdf 2>/dev/null | wc -l)
MEMORIES=$(ls -1 memoria/*.md 2>/dev/null | wc -l)

echo -e "${GREEN}🎬 ABSORÇÃO COMPLETA!${NC}"
echo ""
echo -e "${CYAN}📊 Resumo Final:${NC}"
echo -e "  ✅ Roteiros absorvidos nesta sessão: $((PROCESSED_NOW - PROCESSED_COUNT))"
echo -e "  📚 Total de roteiros no conhecimento: $PROCESSED_NOW"
echo -e "  🧠 Total de memórias: $MEMORIES"
echo -e "  📥 Roteiros aguardando: $NEW_NOW"
echo ""

echo -e "${YELLOW}💡 Dica:${NC}"
echo "Use 'scripturemon' para conversar sobre os roteiros absorvidos"
echo "Exemplo: scripturemon 'compare os estilos narrativos que você conhece'"