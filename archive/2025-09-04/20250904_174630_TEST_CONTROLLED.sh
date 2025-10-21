#!/bin/bash

echo "🧪 TESTE CONTROLADO - SCRIPTUREMON ULTIMATE"
echo "==========================================="
echo "Simulando uso real do sistema"
echo ""

# Configuração
BASE_DIR="/Users/clubproducoes/Digimundo/scripturemon-validation"
cd "$BASE_DIR"

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "\n${BLUE}1. MÓDULOS PYTHON${NC}"
echo "----------------------------------------"

python3 -c "
import sys
sys.path.insert(0, '.')
modules = [
    'apps.scripturemon.memory_manager',
    'apps.scripturemon.redis_on_demand', 
    'apps.scripturemon.digilang_integration',
    'apps.scripturemon.cinema_knowledge'
]
for m in modules:
    try:
        __import__(m)
        print(f'✅ {m.split(\".\")[-1]}')
    except Exception as e:
        print(f'❌ {m.split(\".\")[-1]}: {e}')
" 2>/dev/null

echo -e "\n${BLUE}2. INFRAESTRUTURA${NC}"
echo "----------------------------------------"

# Redis
if python3 -c "from apps.scripturemon.redis_on_demand import ensure_redis; ensure_redis()" 2>/dev/null; then
    echo -e "${GREEN}✅ Redis${NC}"
else
    echo -e "${RED}❌ Redis${NC}"
fi

# Database
if [ -f "data/memory/unified_memory.db" ]; then
    echo -e "${GREEN}✅ Database${NC}"
else
    echo -e "${RED}❌ Database${NC}"
fi

# PDFs
PDF_COUNT=$(ls data/cinema_knowledge/pdfs/*/*.pdf 2>/dev/null | wc -l)
if [ $PDF_COUNT -gt 0 ]; then
    echo -e "${GREEN}✅ PDFs: $PDF_COUNT arquivos${NC}"
else
    echo -e "${RED}❌ PDFs não encontrados${NC}"
fi

echo -e "\n${BLUE}3. SISTEMA COMPLETO${NC}"
echo "----------------------------------------"

# Teste rápido de inicialização
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from bin.scripturemon_fixed import ScripturemonMaxCapacity
    s = ScripturemonMaxCapacity()
    print('✅ Sistema inicializado')
except Exception as e:
    print(f'❌ Erro: {str(e)[:50]}...')
" 2>&1 | grep -E "(✅|❌)" | head -1

echo ""
echo "==========================================="
echo -e "${GREEN}TESTE CONTROLADO CONCLUÍDO${NC}"
echo "==========================================="
