#!/bin/bash

# ============================================
# FIX PARA MÓDULOS NATIVOS - SQLITE3 & NODE-LLAMA-CPP
# ============================================

echo "╔══════════════════════════════════════════╗"
echo "║   CORREÇÃO DE MÓDULOS NATIVOS ELECTRON   ║"
echo "╚══════════════════════════════════════════╝"
echo ""

PROJECT_DIR="/Users/clubproducoes/Digimundo/digimundo_starter"
cd "$PROJECT_DIR"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📁 Diretório: $PROJECT_DIR${NC}"
echo ""

# Função para verificar se um módulo está instalado
check_module() {
    if [ -d "node_modules/$1" ]; then
        echo -e "${GREEN}✅ $1 encontrado${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 não encontrado${NC}"
        return 1
    fi
}

# 1. Verificar estado atual
echo -e "${YELLOW}1️⃣ Verificando estado atual...${NC}"
check_module "sqlite3"
SQLITE_STATUS=$?
check_module "node-llama-cpp"
LLAMA_STATUS=$?
echo ""

# 2. Instalar electron-rebuild se necessário
if ! command -v electron-rebuild &> /dev/null; then
    echo -e "${YELLOW}2️⃣ Instalando electron-rebuild...${NC}"
    npm install --save-dev electron-rebuild
    echo ""
fi

# 3. Corrigir sqlite3
if [ $SQLITE_STATUS -ne 0 ]; then
    echo -e "${YELLOW}3️⃣ Instalando e compilando sqlite3...${NC}"
    
    # Remover versão antiga
    rm -rf node_modules/sqlite3
    
    # Tentar método 1: Instalação normal
    echo "Tentando instalação normal..."
    npm install sqlite3
    
    # Se falhar, tentar método 2: Build from source
    if [ ! -d "node_modules/sqlite3" ]; then
        echo "Tentando build from source..."
        npm install sqlite3 --build-from-source
    fi
    
    # Recompilar para Electron
    if [ -d "node_modules/sqlite3" ]; then
        echo "Recompilando para Electron..."
        npx electron-rebuild -f -w sqlite3
        echo -e "${GREEN}✅ sqlite3 instalado e compilado${NC}"
    else
        echo -e "${RED}❌ Falha ao instalar sqlite3${NC}"
        echo -e "${YELLOW}Instalando alternativa: better-sqlite3${NC}"
        npm install better-sqlite3
        npx electron-rebuild -f -w better-sqlite3
    fi
else
    echo -e "${YELLOW}3️⃣ Recompilando sqlite3 existente...${NC}"
    npx electron-rebuild -f -w sqlite3
fi
echo ""

# 4. Node-llama-cpp (opcional)
echo -e "${YELLOW}4️⃣ Verificando node-llama-cpp (opcional)...${NC}"
if [ $LLAMA_STATUS -ne 0 ]; then
    echo -e "${BLUE}node-llama-cpp não está instalado${NC}"
    echo "Este módulo é opcional para funcionalidades de LLM local"
    echo ""
    read -p "Deseja tentar instalar? (s/N): " install_llama
    
    if [[ $install_llama =~ ^[Ss]$ ]]; then
        echo "Instalando node-llama-cpp..."
        npm install node-llama-cpp --save-optional || {
            echo -e "${YELLOW}⚠️ node-llama-cpp não pôde ser instalado${NC}"
            echo "O Electron funcionará normalmente sem ele"
        }
    else
        echo "Pulando instalação de node-llama-cpp"
    fi
else
    echo -e "${GREEN}node-llama-cpp já está instalado${NC}"
    echo "Recompilando para Electron..."
    npx electron-rebuild -f -w node-llama-cpp || {
        echo -e "${YELLOW}⚠️ Recompilação falhou, mas não é crítico${NC}"
    }
fi
echo ""

# 5. Verificar outros módulos nativos
echo -e "${YELLOW}5️⃣ Verificando outros módulos nativos...${NC}"

# bcrypt
if [ -d "node_modules/bcrypt" ]; then
    echo "Recompilando bcrypt..."
    npx electron-rebuild -f -w bcrypt
    echo -e "${GREEN}✅ bcrypt recompilado${NC}"
fi

# sharp (se existir)
if [ -d "node_modules/sharp" ]; then
    echo "Recompilando sharp..."
    npx electron-rebuild -f -w sharp
    echo -e "${GREEN}✅ sharp recompilado${NC}"
fi
echo ""

# 6. Rebuild geral
echo -e "${YELLOW}6️⃣ Fazendo rebuild geral...${NC}"
npx electron-rebuild
echo ""

# 7. Verificação final
echo -e "${BLUE}7️⃣ Verificação final...${NC}"
echo ""

# Testar sqlite3
if [ -d "node_modules/sqlite3" ] || [ -d "node_modules/better-sqlite3" ]; then
    echo -e "${GREEN}✅ Banco de dados SQLite disponível${NC}"
else
    echo -e "${RED}❌ AVISO: Nenhum driver SQLite instalado${NC}"
fi

# Testar bcrypt
if [ -d "node_modules/bcrypt" ]; then
    node -e "try { require('bcrypt'); console.log('✅ bcrypt funcionando'); } catch(e) { console.log('❌ bcrypt com erro:', e.message); }"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Processo de correção concluído!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Próximos passos:"
echo "1. Execute o Electron normalmente: npm run dev"
echo "2. Ou use o monitor: ./run-electron-fix.sh"
echo ""
