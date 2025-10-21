#!/bin/bash

# Setup do Ecossistema Producer-Director ScriptureMon
# Mantém SCRIPTUREMON como Diretor, renomeia os outros

echo "🎬 CONFIGURANDO ECOSSISTEMA SCRIPTUREMON"
echo "========================================"

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Criar Producermon
echo -e "${YELLOW}1. Criando PRODUCERMON (Orquestrador)...${NC}"
if ollama list | grep -q "producermon"; then
    echo -e "${GREEN}✓ Producermon já existe${NC}"
else
    ollama create producermon:latest -f apps/scripturemon/modelfiles/Modelfile_producermon
    echo -e "${GREEN}✓ Producermon criado${NC}"
fi

# 2. Renomear modelos existentes (mas manter Scripturemon)
echo -e "${YELLOW}2. Renomeando Digimons (preservando SCRIPTUREMON)...${NC}"

# Tier 1 - Rápidos
if ollama list | grep -q "scripturemon-gpu-stable"; then
    ollama cp scripturemon-gpu-stable:latest speedmon:latest 2>/dev/null
    echo -e "${GREEN}✓ SPEEDMON criado${NC}"
fi

if ollama list | grep -q "scripturemon-ptbr"; then
    ollama cp scripturemon-ptbr:latest brazilmon:latest 2>/dev/null
    echo -e "${GREEN}✓ BRAZILMON criado${NC}"
fi

if ollama list | grep -q "scripturemon-cpu"; then
    ollama cp scripturemon-cpu:latest steadymon:latest 2>/dev/null
    echo -e "${GREEN}✓ STEADYMON criado${NC}"
fi

if ollama list | grep -q "scripturemon-hybrid"; then
    ollama cp scripturemon-hybrid:latest balancemon:latest 2>/dev/null
    echo -e "${GREEN}✓ BALANCEMON criado${NC}"
fi

# Tier 3 - Processador
if ollama list | grep -q "deepseek-r1:32b"; then
    ollama cp deepseek-r1:32b reasonmon:latest 2>/dev/null
    echo -e "${GREEN}✓ REASONMON criado${NC}"
fi

# SCRIPTUREMON permanece com nome original!
echo -e "${GREEN}✓ SCRIPTUREMON mantido como Diretor Final${NC}"

# 3. Verificar modelos disponíveis
echo -e "${YELLOW}3. Verificando ecossistema...${NC}"
echo ""
echo "TIER 0 - Orquestrador:"
ollama list | grep -E "producermon" || echo "  ⚠️ Producermon não encontrado"

echo ""
echo "TIER 1 - Rápidos:"
ollama list | grep -E "speedmon|brazilmon|steadymon|balancemon"

echo ""
echo "TIER 2 - Especialistas:"
ollama list | grep -E "neuromon|sabiamon|debugmon|evolvemon"

echo ""
echo "TIER 3 - Processador:"
ollama list | grep -E "reasonmon|deepseek-r1:32b"

echo ""
echo "TIER 4 - Diretor Final:"
ollama list | grep -E "scripturemon-ultimate|scripturemon-deepseek"

# 4. Manter Producermon sempre ativo
echo ""
echo -e "${YELLOW}4. Ativando Producermon permanente...${NC}"
ollama run producermon:latest --keepalive -1 &
PRODUCER_PID=$!
echo -e "${GREEN}✓ Producermon ativo (PID: $PRODUCER_PID)${NC}"

# 5. Teste rápido
echo ""
echo -e "${YELLOW}5. Teste do ecossistema...${NC}"

python3 -c "
from apps.scripturemon.producer_director_system import ProducerDirectorSystem
import sys

try:
    system = ProducerDirectorSystem()
    print('✅ Sistema Producer-Director inicializado')

    # Teste simples
    result = system.orchestrate('Teste rápido do sistema')
    if result and len(result) > 10:
        print('✅ Orquestração funcionando')
    else:
        print('⚠️ Resposta vazia ou muito curta')

except Exception as e:
    print(f'❌ Erro: {e}')
    sys.exit(1)
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ ECOSSISTEMA PRONTO!${NC}"
else
    echo -e "${RED}❌ Problemas detectados${NC}"
fi

echo ""
echo "========================================"
echo "🎬 HIERARQUIA DO ECOSSISTEMA:"
echo ""
echo "  PRODUCERMON (Produtor)"
echo "       ↓"
echo "  Digimons Especializados"
echo "       ↓"
echo "  SCRIPTUREMON (Diretor Final)"
echo ""
echo "Use: python3 -m apps.scripturemon.producer_director_system 'sua pergunta'"
echo "========================================="