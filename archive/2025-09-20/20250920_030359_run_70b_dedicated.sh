#!/bin/bash
# 🔥 SCRIPT COMPLETO PARA RODAR 70B DEDICATED

echo "=================================================="
echo "🔥 INICIANDO 70B DEDICATED COM MÁXIMA PERFORMANCE"
echo "=================================================="
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Diretório base
BASE_DIR="/Users/clubproducoes/Digimundo/scripturemon-champion"
cd "$BASE_DIR"

# 1. PREPARAR SISTEMA
echo "1️⃣ PREPARANDO SISTEMA (limpeza de memória)..."
echo "-------------------------------------------------"
python3 scripts/active/prepare_70b_dedicated.py

# Verificar se preparação foi bem sucedida
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Falha na preparação do sistema${NC}"
    echo "   Tente fechar mais aplicações manualmente"
    exit 1
fi

echo ""
echo "2️⃣ CONFIGURANDO POTÊNCIA MÁXIMA..."
echo "-------------------------------------------------"
python3 scripts/active/unified_power_system.py dedicated_70b

echo ""
echo "3️⃣ VERIFICANDO SISTEMA..."
echo "-------------------------------------------------"
python3 scripts/active/unified_power_system.py check

echo ""
echo "4️⃣ INICIANDO TESTE 70B DEDICATED..."
echo "-------------------------------------------------"
echo -e "${YELLOW}⚠️ ISSO PODE LEVAR 5-20 MINUTOS!${NC}"
echo "   O sistema processará com máxima qualidade"
echo ""
echo "Escolha o teste:"
echo "1. Teste rápido (cena pequena)"
echo "2. Teste completo (roteiro inteiro)"
echo ""
read -p "Opção (1 ou 2): " test_choice

if [ "$test_choice" == "2" ]; then
    # Teste completo
    echo ""
    echo "📝 Processando roteiro completo..."
    python3 scripts/active/async_70b_processor.py
else
    # Teste rápido
    echo ""
    echo "⚡ Executando teste rápido..."
    echo "2" | python3 scripts/active/test_70b_modes.py
fi

echo ""
echo "=================================================="
echo "✅ PROCESSO COMPLETO!"
echo "=================================================="
echo ""
echo "📊 Para monitorar em tempo real (outro terminal):"
echo "   python3 scripts/active/monitor_70b.py watch"
echo ""
echo "🔍 Para restaurar Spotlight depois:"
echo "   python3 scripts/active/prepare_70b_dedicated.py restore"
echo ""
echo -e "${GREEN}DIGIMUNDO PRESENTE 🥷${NC}"