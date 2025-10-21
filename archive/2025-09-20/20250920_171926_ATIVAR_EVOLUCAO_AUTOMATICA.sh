#!/bin/bash

# 🚀 ATIVADOR DO SISTEMA DE EVOLUÇÃO AUTOMÁTICA DO SCRIPTUREMON

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${MAGENTA}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║   🚀 ATIVANDO EVOLUÇÃO AUTOMÁTICA DO SCRIPTUREMON      ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar Python
echo -e "${CYAN}🔍 Verificando ambiente...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 não encontrado${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python3 encontrado${NC}"

# Verificar Ollama
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}❌ Ollama não encontrado${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Ollama encontrado${NC}"

# Verificar modelo Scripturemon
if ! ollama list | grep -q "scripturemon-maestro"; then
    echo -e "${YELLOW}⚠️ Modelo scripturemon-maestro não encontrado${NC}"
    echo "  Criando modelo..."
    ollama create scripturemon-maestro -f scripturemon_maestro_brutal.modelfile
fi
echo -e "${GREEN}✓ Modelo Scripturemon ativo${NC}"

# Instalar ChromaDB se não tiver
echo ""
echo -e "${CYAN}📦 Verificando ChromaDB...${NC}"
if ! python3 -c "import chromadb" 2>/dev/null; then
    echo -e "${YELLOW}ChromaDB não instalado. Deseja instalar? (s/n)${NC}"
    read -r install_chromadb
    if [[ "$install_chromadb" == "s" ]]; then
        pip3 install chromadb
        echo -e "${GREEN}✓ ChromaDB instalado${NC}"
    else
        echo -e "${YELLOW}⚠️ Continuando sem ChromaDB (modo básico)${NC}"
    fi
else
    echo -e "${GREEN}✓ ChromaDB disponível${NC}"
fi

# Criar estrutura de pastas
echo ""
echo -e "${CYAN}📁 Criando estrutura de pastas...${NC}"

mkdir -p roteiros_processados
mkdir -p conexao_criador
mkdir -p biblioteca/1_tecnicas_roteiro
mkdir -p cinema/entrada
mkdir -p conhecimento
mkdir -p backups

echo -e "${GREEN}✓ Estrutura criada${NC}"

# Criar script de monitoramento em background
cat << 'MONITOR' > monitor_background.sh
#!/bin/bash

# Script para rodar em background
cd /Users/clubproducoes/Digimundo/digimons/scripturemon

# Log file
LOG="conhecimento/evolution.log"

echo "🚀 Evolução automática iniciada: $(date)" >> "$LOG"

# Executar Python script
python3 SCRIPTUREMON_RAG_EVOLUTION.py << INPUT
1
INPUT
MONITOR

chmod +x monitor_background.sh

# Menu de opções
echo ""
echo -e "${MAGENTA}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║              COMO DESEJA EXECUTAR?                     ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "1) 🤖 Modo Automático (monitora pastas continuamente)"
echo "2) 📄 Processar arquivo específico"
echo "3) 🔍 Buscar conhecimento existente"
echo "4) 📊 Ver estatísticas"
echo "5) 🎯 Processar todos PDFs existentes agora"
echo ""
read -p "Escolha [1-5]: " opcao

case $opcao in
    1)
        echo ""
        echo -e "${GREEN}🤖 MODO AUTOMÁTICO ATIVADO${NC}"
        echo ""
        echo -e "${YELLOW}Pastas monitoradas:${NC}"
        echo "  📁 roteiros_processados/ (roteiros dos mestres)"
        echo "  📁 conexao_criador/ (seus roteiros)"
        echo "  📁 biblioteca/1_tecnicas_roteiro/ (teoria)"
        echo "  📁 cinema/entrada/ (novos PDFs)"
        echo ""
        echo -e "${CYAN}Coloque PDFs nessas pastas e eles serão processados automaticamente!${NC}"
        echo -e "${YELLOW}Pressione Ctrl+C para parar${NC}"
        echo ""
        
        # Executar monitoramento
        python3 SCRIPTUREMON_RAG_EVOLUTION.py << INPUT
1
INPUT
        ;;
        
    2)
        echo ""
        echo -e "${CYAN}📄 PROCESSAR ARQUIVO ESPECÍFICO${NC}"
        echo ""
        read -p "Caminho do PDF: " pdf_path
        
        if [ -f "$pdf_path" ]; then
            echo "Tipo do arquivo:"
            echo "1) mestre (roteiro clássico)"
            echo "2) criador (seu trabalho)"
            echo "3) teoria (livro técnico)"
            read -p "Escolha [1-3]: " tipo_num
            
            case $tipo_num in
                1) tipo="mestre" ;;
                2) tipo="criador" ;;
                3) tipo="teoria" ;;
                *) tipo="teoria" ;;
            esac
            
            python3 SCRIPTUREMON_RAG_EVOLUTION.py << INPUT
2
$pdf_path
$tipo
INPUT
        else
            echo -e "${RED}❌ Arquivo não encontrado${NC}"
        fi
        ;;
        
    3)
        echo ""
        echo -e "${CYAN}🔍 BUSCAR CONHECIMENTO${NC}"
        echo ""
        read -p "Buscar por: " query
        
        python3 SCRIPTUREMON_RAG_EVOLUTION.py << INPUT
3
$query
INPUT
        ;;
        
    4)
        echo ""
        echo -e "${CYAN}📊 ESTATÍSTICAS${NC}"
        echo ""
        
        python3 SCRIPTUREMON_RAG_EVOLUTION.py << INPUT
4
INPUT
        ;;
        
    5)
        echo ""
        echo -e "${YELLOW}🎯 PROCESSANDO TODOS OS PDFs EXISTENTES${NC}"
        echo ""
        
        # Processar PDFs existentes nas pastas
        for folder in roteiros_processados conexao_criador biblioteca/1_tecnicas_roteiro cinema/2_roteiros_mestres cinema/3_roteiros_criador; do
            if [ -d "$folder" ]; then
                echo -e "${CYAN}Processando pasta: $folder${NC}"
                
                for pdf in "$folder"/*.pdf; do
                    if [ -f "$pdf" ]; then
                        echo "  📄 $(basename "$pdf")"
                        
                        # Determinar tipo baseado na pasta
                        if [[ "$folder" == *"criador"* ]]; then
                            tipo="criador"
                        elif [[ "$folder" == *"mestres"* ]] || [[ "$folder" == "roteiros_processados" ]]; then
                            tipo="mestre"
                        else
                            tipo="teoria"
                        fi
                        
                        python3 SCRIPTUREMON_RAG_EVOLUTION.py << INPUT
2
$pdf
$tipo
INPUT
                        
                        sleep 2  # Pequena pausa entre arquivos
                    fi
                done
            fi
        done
        
        echo ""
        echo -e "${GREEN}✅ Processamento em lote completo!${NC}"
        
        # Perguntar se quer ativar monitoramento
        echo ""
        read -p "Ativar monitoramento automático agora? (s/n): " activate
        if [[ "$activate" == "s" ]]; then
            python3 SCRIPTUREMON_RAG_EVOLUTION.py << INPUT
1
INPUT
        fi
        ;;
        
    *)
        echo -e "${RED}Opção inválida${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${MAGENTA}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║              🎬 SCRIPTUREMON EVOLUÍDO!                 ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════════════════════╝${NC}"