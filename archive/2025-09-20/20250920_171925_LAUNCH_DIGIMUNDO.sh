#!/bin/bash

echo "🌌 =================================================="
echo "     DIGIMUNDO LAUNCHER - SISTEMA COMPLETO"
echo "     Claude (Sabiamon) + Visual + Backend"
echo "================================================== 🌌"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretório base
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Função para verificar se porta está em uso
check_port() {
    lsof -i :$1 > /dev/null 2>&1
    return $?
}

# Função para matar processo na porta
kill_port() {
    echo -e "${YELLOW}🧹 Limpando porta $1...${NC}"
    lsof -ti :$1 | xargs kill -9 2>/dev/null
}

# Verificar dependências
echo -e "${BLUE}📦 Verificando dependências...${NC}"

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js não instalado!${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ NPM não instalado!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dependências OK${NC}"

# Instalar pacotes se necessário
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Instalando pacotes...${NC}"
    npm install
fi

# Limpar portas se necessário
if check_port 7937; then
    echo -e "${YELLOW}⚠️ Porta 7937 em uso${NC}"
    read -p "Deseja encerrar o processo? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        kill_port 7937
    fi
fi

# Menu de opções
echo ""
echo "🎮 ESCOLHA O MODO DE INICIALIZAÇÃO:"
echo ""
echo "  1) 🚀 MODO COMPLETO (Recomendado)"
echo "     - Interface de controle central"
echo "     - Todos os sistemas integrados"
echo "     - Claude (Sabiamon) ativo"
echo ""
echo "  2) 🎮 MODO VISUAL"
echo "     - Apenas Digimundo Visual"
echo "     - Interface navegável"
echo ""
echo "  3) 💬 MODO CHAT"
echo "     - Apenas chat com Digimons"
echo ""
echo "  4) 🛠️ MODO DESENVOLVIMENTO"
echo "     - Todos os logs visíveis"
echo "     - DevTools ativado"
echo ""
echo "  5) 📦 EMPACOTAR APP"
echo "     - Criar aplicativo .app para Mac"
echo ""

read -p "Escolha (1-5): " choice

case $choice in
    1)
        echo -e "${GREEN}🚀 Iniciando MODO COMPLETO...${NC}"
        
        # Criar arquivo temporário para controle
        cat > /tmp/digimundo_launcher.js << 'EOF'
const { spawn } = require('child_process');
const express = require('express');
const open = require('open');

console.log('🌌 DIGIMUNDO LAUNCHER ATIVO');

// Iniciar servidor backend
const server = spawn('npm', ['run', 'dev'], {
  cwd: process.cwd(),
  stdio: 'inherit'
});

// Aguardar servidor estar pronto
setTimeout(() => {
  console.log('🎮 Abrindo interface de controle...');
  open('http://localhost:7937/digimundo_control.html');
  
  console.log('\n✅ SISTEMA COMPLETO INICIADO!');
  console.log('   Acesse: http://localhost:7937/digimundo_control.html');
  console.log('\n   Pressione Ctrl+C para encerrar');
}, 5000);

// Lidar com encerramento
process.on('SIGINT', () => {
  console.log('\n🔴 Encerrando Digimundo...');
  server.kill();
  process.exit();
});
EOF
        
        USE_LAUNCHER=true npm run dev
        ;;
        
    2)
        echo -e "${GREEN}🎮 Iniciando MODO VISUAL...${NC}"
        npm run dev &
        SERVER_PID=$!
        
        sleep 5
        echo -e "${BLUE}🌐 Abrindo Digimundo Visual...${NC}"
        open http://localhost:7937/digimundo_visual.html
        
        echo -e "${GREEN}✅ Sistema visual iniciado!${NC}"
        echo "   Pressione Ctrl+C para encerrar"
        
        wait $SERVER_PID
        ;;
        
    3)
        echo -e "${GREEN}💬 Iniciando MODO CHAT...${NC}"
        npm run dev &
        SERVER_PID=$!
        
        sleep 5
        echo -e "${BLUE}🌐 Abrindo interface de chat...${NC}"
        open http://localhost:7937/index_improved.html
        
        echo -e "${GREEN}✅ Chat iniciado!${NC}"
        echo "   Pressione Ctrl+C para encerrar"
        
        wait $SERVER_PID
        ;;
        
    4)
        echo -e "${GREEN}🛠️ Iniciando MODO DESENVOLVIMENTO...${NC}"
        NODE_ENV=development npm run dev
        ;;
        
    5)
        echo -e "${GREEN}📦 EMPACOTANDO APLICAÇÃO...${NC}"
        
        # Verificar electron-builder
        if ! npm list electron-builder > /dev/null 2>&1; then
            echo -e "${YELLOW}📦 Instalando electron-builder...${NC}"
            npm install --save-dev electron-builder
        fi
        
        # Configurar package.json para build
        echo -e "${BLUE}⚙️ Configurando build...${NC}"
        
        # Build da aplicação
        echo -e "${BLUE}🔨 Construindo aplicação...${NC}"
        npm run build
        
        echo -e "${GREEN}✅ Aplicação empacotada!${NC}"
        echo "   Localização: dist/"
        
        # Abrir pasta com o app
        open dist/
        ;;
        
    *)
        echo -e "${RED}❌ Opção inválida!${NC}"
        exit 1
        ;;
esac