#!/bin/bash

# =================================================================
# SCRIPTUREMON - REORGANIZAÇÃO INTELIGENTE
# =================================================================
# Script para reorganizar toda a estrutura do Scripturemon
# de forma limpa, profissional e otimizada
# =================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        SCRIPTUREMON - REORGANIZAÇÃO INTELIGENTE           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# =================================================================
# FASE 1: BACKUP DE SEGURANÇA
# =================================================================
echo -e "${BLUE}[1/6] Criando backup de segurança...${NC}"

BACKUP_DIR="../scripturemon_backup_$(date +%Y%m%d_%H%M%S)"
if [ ! -d "$BACKUP_DIR" ]; then
    echo "  → Criando backup em $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
    
    # Backup apenas dos arquivos essenciais (não venv)
    rsync -av --exclude='venv_rag/' \
              --exclude='__pycache__/' \
              --exclude='*.pyc' \
              --exclude='.git/' \
              ./ "$BACKUP_DIR/" > /dev/null 2>&1
    
    echo -e "  ${GREEN}✓ Backup criado com sucesso${NC}"
else
    echo -e "  ${YELLOW}⚠ Backup já existe${NC}"
fi

# =================================================================
# FASE 2: CRIAR NOVA ESTRUTURA DE DIRETÓRIOS
# =================================================================
echo -e "${BLUE}[2/6] Criando estrutura organizada...${NC}"

# Estrutura principal
mkdir -p src/{core,models,scripts,genetics}
mkdir -p data/{roteiros,teoria,processados,cache}
mkdir -p config
mkdir -p memory/{L1_CORE,L2_CONSOLIDATED,L3_ACTIVE,L4_QUANTUM}
mkdir -p docs/{api,architecture,guides}
mkdir -p tests/unit
mkdir -p logs

echo -e "  ${GREEN}✓ Estrutura de diretórios criada${NC}"

# =================================================================
# FASE 3: MOVER CÓDIGO PRINCIPAL
# =================================================================
echo -e "${BLUE}[3/6] Reorganizando código principal...${NC}"

# Mover app RAG (usar a versão mais atualizada)
if [ -d "app" ]; then
    echo "  → Movendo sistema RAG..."
    mv app src/core/ 2>/dev/null || cp -r app src/core/
fi

# Se existir versão no pesquisa_rag, usar essa (mais limpa)
if [ -d "/Users/clubproducoes/Digimundo/pesquisa_rag/digimundo_rag/app" ]; then
    echo "  → Usando versão RAG atualizada..."
    cp -r /Users/clubproducoes/Digimundo/pesquisa_rag/digimundo_rag/app/* src/core/app/ 2>/dev/null || true
fi

# Mover genetics (DNA imortal)
if [ -d "genetics" ]; then
    echo "  → Preservando DNA imortal..."
    mv genetics/* src/genetics/ 2>/dev/null || cp -r genetics/* src/genetics/
fi

# Mover scripts úteis
echo "  → Organizando scripts..."
for script in *.py; do
    if [[ -f "$script" ]]; then
        case "$script" in
            test_*.py|*_test.py)
                mv "$script" tests/ 2>/dev/null || true
                ;;
            SCRIPTUREMON_*.py)
                mv "$script" src/core/ 2>/dev/null || true
                ;;
            *)
                mv "$script" src/scripts/ 2>/dev/null || true
                ;;
        esac
    fi
done

echo -e "  ${GREEN}✓ Código reorganizado${NC}"

# =================================================================
# FASE 4: ORGANIZAR MODELFILES
# =================================================================
echo -e "${BLUE}[4/6] Organizando modelfiles...${NC}"

mkdir -p src/models/{current,archive,experimental}

# Identificar o modelfile principal (mais recente/completo)
MAIN_MODELFILE=""
for mf in scripturemon*.modelfile SCRIPTUREMON*.modelfile; do
    if [[ -f "$mf" ]]; then
        if [[ -z "$MAIN_MODELFILE" ]] || [[ "$mf" -nt "$MAIN_MODELFILE" ]]; then
            MAIN_MODELFILE="$mf"
        fi
    fi
done

if [[ -n "$MAIN_MODELFILE" ]]; then
    echo "  → Modelfile principal: $MAIN_MODELFILE"
    cp "$MAIN_MODELFILE" src/models/current/scripturemon_v1.0.modelfile
    
    # Arquivar outros
    for mf in *.modelfile; do
        if [[ -f "$mf" && "$mf" != "$MAIN_MODELFILE" ]]; then
            mv "$mf" src/models/archive/ 2>/dev/null || true
        fi
    done
fi

echo -e "  ${GREEN}✓ Modelfiles organizados${NC}"

# =================================================================
# FASE 5: CONSOLIDAR DADOS
# =================================================================
echo -e "${BLUE}[5/6] Consolidando dados...${NC}"

# Mover roteiros e cinema
if [ -d "cinema" ]; then
    echo "  → Consolidando biblioteca de roteiros..."
    find cinema -name "*.pdf" -exec mv {} data/roteiros/ \; 2>/dev/null || true
fi

if [ -d "biblioteca" ]; then
    cp -r biblioteca/* data/roteiros/ 2>/dev/null || true
fi

# Mover bases de conhecimento
if [ -d "conhecimento" ]; then
    echo "  → Preservando bases de conhecimento..."
    find conhecimento -name "*.db" -exec mv {} data/processados/ \; 2>/dev/null || true
    find conhecimento -name "*.json" -exec mv {} data/processados/ \; 2>/dev/null || true
fi

# Mover memórias
if [ -d "memoria" ] || [ -d "memory" ]; then
    echo "  → Consolidando sistema de memória..."
    find memoria memory -name "*.json" -exec cp {} memory/ \; 2>/dev/null || true
fi

echo -e "  ${GREEN}✓ Dados consolidados${NC}"

# =================================================================
# FASE 6: LIMPEZA DE TEMPORÁRIOS
# =================================================================
echo -e "${BLUE}[6/6] Limpeza de arquivos temporários...${NC}"

# Remover com segurança
echo "  → Removendo caches e temporários..."

# Lista de padrões para remover
TEMP_PATTERNS=(
    "__pycache__"
    "*.pyc"
    ".pytest_cache"
    "*.log"
    "quick_test_*.json"
    "test_results_*.md"
    "*_REPORT_*.md"
    "ocr_tmp"
    "cache.db*"
)

for pattern in "${TEMP_PATTERNS[@]}"; do
    find . -name "$pattern" -type f -delete 2>/dev/null || true
    find . -name "$pattern" -type d -exec rm -rf {} + 2>/dev/null || true
done

# Remover diretórios vazios
find . -type d -empty -delete 2>/dev/null || true

# Avisar sobre venv
if [ -d "venv_rag" ]; then
    SIZE=$(du -sh venv_rag | cut -f1)
    echo -e "  ${YELLOW}⚠ venv_rag encontrado (${SIZE})${NC}"
    echo -e "    Para remover: ${RED}rm -rf venv_rag${NC}"
    echo -e "    Para recriar: ${GREEN}python -m venv venv_rag && source venv_rag/bin/activate && pip install -r requirements.txt${NC}"
fi

echo -e "  ${GREEN}✓ Limpeza concluída${NC}"

# =================================================================
# CRIAR ESTRUTURA FINAL
# =================================================================

# Mover scripts .sh organizadamente
mkdir -p scripts/{automation,evolution,setup}

for script in *.sh; do
    if [[ -f "$script" && "$script" != "REORGANIZE_SCRIPTUREMON.sh" ]]; then
        case "$script" in
            *EVOLUTION*|*EVOLUCAO*)
                mv "$script" scripts/evolution/ 2>/dev/null || true
                ;;
            *SETUP*|*INSTALL*)
                mv "$script" scripts/setup/ 2>/dev/null || true
                ;;
            *)
                mv "$script" scripts/automation/ 2>/dev/null || true
                ;;
        esac
    fi
done

# =================================================================
# RESULTADO FINAL
# =================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              REORGANIZAÇÃO CONCLUÍDA!                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Mostrar nova estrutura
echo -e "${GREEN}Nova estrutura:${NC}"
echo "."
echo "├── src/"
echo "│   ├── core/        # Sistema RAG principal"
echo "│   ├── models/      # Modelfiles organizados"
echo "│   ├── scripts/     # Scripts Python"
echo "│   └── genetics/    # DNA imortal"
echo "├── data/"
echo "│   ├── roteiros/    # PDFs de roteiros"
echo "│   ├── teoria/      # Material teórico"
echo "│   ├── processados/ # Dados processados"
echo "│   └── cache/       # Cache temporário"
echo "├── config/          # Configurações"
echo "├── memory/          # Sistema de memória"
echo "├── docs/            # Documentação"
echo "├── tests/           # Testes"
echo "├── scripts/         # Scripts Shell"
echo "└── logs/            # Logs do sistema"

echo ""
echo -e "${YELLOW}Backup salvo em: $BACKUP_DIR${NC}"
echo ""
echo -e "${GREEN}✓ Scripturemon reorganizado com sucesso!${NC}"
echo ""
echo "Próximos passos:"
echo "  1. Revisar a nova estrutura"
echo "  2. Atualizar paths nos scripts se necessário"
echo "  3. Remover venv_rag se desejar (1.3GB)"
echo "  4. Executar testes para validar"