#!/bin/bash

# 🎬 Interface simples para alimentar Scripturemon com conhecimento

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
NC='\033[0m'

clear
echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   🎬 SCRIPTUREMON KNOWLEDGE FEEDER    ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════╝${NC}"
echo ""

# Menu principal
echo -e "${YELLOW}O que deseja fazer?${NC}"
echo ""
echo "1) 📥 Adicionar novo roteiro PDF"
echo "2) 📚 Processar todos os roteiros da pasta"
echo "3) 💬 Conversar sobre roteiro específico"
echo "4) 🧠 Ver memórias acumuladas"
echo "5) 🎯 Testar conhecimento absorvido"
echo "0) Sair"
echo ""

read -p "Escolha [0-5]: " choice

case $choice in
    1)
        echo -e "${GREEN}📥 Adicionar novo roteiro${NC}"
        echo "Arraste o arquivo PDF aqui ou digite o caminho:"
        read -r pdf_path
        
        # Remover aspas se houver
        pdf_path="${pdf_path//\"}"
        pdf_path="${pdf_path//\'}"
        
        if [ -f "$pdf_path" ]; then
            # Copiar para pasta de roteiros
            cp "$pdf_path" "roteiros/"
            filename=$(basename "$pdf_path")
            
            echo -e "${GREEN}✅ PDF copiado!${NC}"
            echo ""
            echo "Deseja que Scripturemon analise agora? (s/n)"
            read -r analyze
            
            if [[ "$analyze" == "s" || "$analyze" == "S" ]]; then
                scripturemon << EOF
🎬 ANALISAR ROTEIRO: roteiros/$filename

Faça uma análise completa incluindo:
- Estrutura narrativa e atos
- Desenvolvimento de personagens  
- Técnicas cinematográficas usadas
- Diálogos mais impactantes
- Temas centrais

Seja específico e detalhado como um roteirista profissional.
EOF
            fi
        else
            echo -e "${YELLOW}⚠️ Arquivo não encontrado${NC}"
        fi
        ;;
        
    2)
        echo -e "${GREEN}📚 Processando todos os roteiros...${NC}"
        ./ABSORVER_ROTEIROS.sh roteiros/
        ;;
        
    3)
        echo -e "${MAGENTA}💬 Conversar sobre roteiro${NC}"
        echo "Roteiros disponíveis:"
        ls -1 roteiros/*.pdf 2>/dev/null | sed 's|roteiros/||' | sed 's|.pdf||'
        echo ""
        echo "Sobre qual roteiro quer conversar?"
        read -r roteiro
        
        scripturemon "Vamos conversar sobre o roteiro de $roteiro. O que você aprendeu com ele?"
        ;;
        
    4)
        echo -e "${CYAN}🧠 Memórias acumuladas:${NC}"
        ls -la memoria/*.md 2>/dev/null || echo "Nenhuma memória ainda"
        echo ""
        echo "Ver alguma memória específica? (digite o nome ou Enter para pular)"
        read -r memoria
        if [ -n "$memoria" ]; then
            cat "memoria/$memoria" 2>/dev/null || echo "Memória não encontrada"
        fi
        ;;
        
    5)
        echo -e "${YELLOW}🎯 Testando conhecimento${NC}"
        scripturemon << EOF
TESTE DE CONHECIMENTO:

1. Cite 3 técnicas de roteiro que você conhece
2. Qual a estrutura clássica de 3 atos?
3. Dê exemplo de um plot twist eficaz
4. Como criar diálogos memoráveis?
5. Qual roteiro você mais admira e por quê?

Responda com base em todo seu conhecimento acumulado.
EOF
        ;;
        
    0)
        echo -e "${GREEN}Até logo! 🎬${NC}"
        exit 0
        ;;
        
    *)
        echo -e "${YELLOW}Opção inválida${NC}"
        ;;
esac

echo ""
echo -e "${CYAN}Pressione Enter para continuar...${NC}"
read