#!/bin/bash

# ============================================
# RECOMPILAÇÃO MANUAL DOS MÓDULOS NATIVOS
# ============================================

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Diretório do projeto
PROJECT_DIR="/Users/clubproducoes/Digimundo/digimundo_starter"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        🔧 RECOMPILAÇÃO DOS MÓDULOS NATIVOS 🔧                ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Navegar para o projeto
cd "$PROJECT_DIR" || {
    echo -e "${RED}❌ Erro: Não foi possível acessar $PROJECT_DIR${NC}"
    exit 1
}

echo -e "${CYAN}📁 Diretório: $PROJECT_DIR${NC}"
echo ""

# Verificar versões
echo -e "${YELLOW}📊 Ambiente:${NC}"
echo -e "   Node.js: $(node -v)"
echo -e "   NPM: $(npm -v)"
echo -e "   Electron: $(npx electron --version 2>/dev/null || echo 'Não instalado')"
echo ""

# Verificar se electron-rebuild está instalado
echo -e "${YELLOW}🔍 Verificando electron-rebuild...${NC}"
if ! npm list electron-rebuild --depth=0 >/dev/null 2>&1; then
    echo -e "${CYAN}📦 Instalando electron-rebuild...${NC}"
    npm install --save-dev electron-rebuild
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ electron-rebuild instalado!${NC}"
    else
        echo -e "${RED}❌ Falha ao instalar electron-rebuild${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ electron-rebuild já está instalado${NC}"
fi
echo ""

# Função para recompilar módulo
recompile_module() {
    local module=$1
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}🔧 Recompilando $module...${NC}"
    
    # Verificar se o módulo existe
    if [ ! -d "node_modules/$module" ]; then
        echo -e "${YELLOW}⚠️  $module não está instalado. Instalando...${NC}"
        npm install $module
    fi
    
    # Tentar várias abordagens de recompilação
    echo -e "${BLUE}Método 1: electron-rebuild${NC}"
    npx electron-rebuild -f -w $module
    
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Método 1 falhou. Tentando método 2...${NC}"
        
        # Método 2: npm rebuild
        echo -e "${BLUE}Método 2: npm rebuild${NC}"
        npm rebuild $module --update-binary
        
        if [ $? -ne 0 ]; then
            echo -e "${YELLOW}Método 2 falhou. Tentando método 3...${NC}"
            
            # Método 3: Reinstalar completamente
            echo -e "${BLUE}Método 3: Reinstalação completa${NC}"
            rm -rf "node_modules/$module"
            npm install $module --build-from-source
            
            if [ $? -ne 0 ]; then
                echo -e "${RED}❌ Todos os métodos falharam para $module${NC}"
                return 1
            fi
        fi
    fi
    
    echo -e "${GREEN}✅ $module recompilado com sucesso!${NC}"
    return 0
}

# Recompilar sqlite3
recompile_module "sqlite3"
sqlite3_result=$?

# Recompilar node-llama-cpp (se estiver instalado)
if [ -d "node_modules/node-llama-cpp" ]; then
    recompile_module "node-llama-cpp"
    llama_result=$?
else
    echo -e "${YELLOW}ℹ️  node-llama-cpp não está instalado (opcional)${NC}"
    llama_result=0
fi

# Recompilar bcrypt
if [ -d "node_modules/bcrypt" ]; then
    recompile_module "bcrypt"
    bcrypt_result=$?
else
    bcrypt_result=0
fi

echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📊 RESUMO DA RECOMPILAÇÃO:${NC}"
echo ""

if [ $sqlite3_result -eq 0 ]; then
    echo -e "${GREEN}✅ sqlite3 - OK${NC}"
else
    echo -e "${RED}❌ sqlite3 - FALHOU${NC}"
fi

if [ $llama_result -eq 0 ]; then
    echo -e "${GREEN}✅ node-llama-cpp - OK${NC}"
else
    echo -e "${RED}❌ node-llama-cpp - FALHOU${NC}"
fi

if [ $bcrypt_result -eq 0 ]; then
    echo -e "${GREEN}✅ bcrypt - OK${NC}"
else
    echo -e "${RED}❌ bcrypt - FALHOU${NC}"
fi

echo ""

# Verificar se todos os módulos foram compilados
if [ $sqlite3_result -eq 0 ] && [ $llama_result -eq 0 ] && [ $bcrypt_result -eq 0 ]; then
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     ✅ TODOS OS MÓDULOS RECOMPILADOS COM SUCESSO! ✅         ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}🚀 Agora você pode executar:${NC}"
    echo -e "   ${YELLOW}npm run dev${NC}"
    echo -e "   ou"
    echo -e "   ${YELLOW}./run-electron-fix.sh${NC}"
else
    echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║     ⚠️  ALGUNS MÓDULOS FALHARAM NA RECOMPILAÇÃO ⚠️           ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}Sugestões:${NC}"
    echo -e "1. Tente executar: ${CYAN}npm cache clean --force${NC}"
    echo -e "2. Delete node_modules: ${CYAN}rm -rf node_modules${NC}"
    echo -e "3. Reinstale tudo: ${CYAN}npm install${NC}"
    echo -e "4. Execute este script novamente"
fi

echo ""