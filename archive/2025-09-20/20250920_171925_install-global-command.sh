#!/bin/bash

# ============================================
# INSTALADOR DO ELECTRON FIX GLOBAL
# ============================================
# Este script instala o comando 'electron-fix' globalmente
# permitindo executar de qualquer lugar do sistema
# ============================================

echo "╔══════════════════════════════════════════╗"
echo "║     INSTALADOR DO ELECTRON FIX GLOBAL    ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Diretório do projeto
PROJECT_DIR="/Users/clubproducoes/Digimundo/digimundo_starter"

# Criar script global
GLOBAL_SCRIPT="/usr/local/bin/electron-fix"

# Conteúdo do script global
cat > /tmp/electron-fix-temp << 'EOF'
#!/bin/bash

# ELECTRON FIX - Comando Global
# Execute de qualquer lugar: electron-fix [opção]

PROJECT_DIR="/Users/clubproducoes/Digimundo/digimundo_starter"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Verificar diretório
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Projeto não encontrado em: $PROJECT_DIR${NC}"
    exit 1
fi

# Navegar para o projeto
cd "$PROJECT_DIR"

# Executar comando
case "$1" in
    "")
        # Menu interativo
        exec bash "$PROJECT_DIR/run-electron-fix.sh"
        ;;
    
    "diagnose")
        echo -e "${BLUE}🔍 Diagnóstico...${NC}"
        node "$PROJECT_DIR/electron-autofix.js" --diagnose-only
        ;;
    
    "fix")
        echo -e "${BLUE}🔧 Corrigindo...${NC}"
        node "$PROJECT_DIR/electron-autofix.js" --fix-only
        ;;
    
    "monitor")
        echo -e "${BLUE}📊 Monitor contínuo...${NC}"
        node "$PROJECT_DIR/electron-autofix.js"
        ;;
    
    "start")
        echo -e "${BLUE}🚀 Iniciando Electron...${NC}"
        npm run dev
        ;;
    
    "clean")
        echo -e "${BLUE}🗑️ Limpando...${NC}"
        rm -rf electron-logs/ node_modules/.cache/ ~/.electron/
        npm cache clean --force
        echo -e "${GREEN}✅ Limpo!${NC}"
        ;;
    
    "report")
        if [ -f "electron-logs/report.json" ]; then
            cat electron-logs/report.json | python3 -m json.tool
        else
            echo -e "${RED}Sem relatório${NC}"
        fi
        ;;
    
    "help"|"--help"|"-h")
        echo "Uso: electron-fix [comando]"
        echo ""
        echo "Comandos:"
        echo "  diagnose  - Apenas diagnóstico"
        echo "  fix       - Diagnóstico + Correções"
        echo "  monitor   - Monitor contínuo"
        echo "  start     - Iniciar Electron normal"
        echo "  clean     - Limpar cache e logs"
        echo "  report    - Ver último relatório"
        echo "  help      - Esta ajuda"
        echo ""
        echo "Sem comando: Menu interativo"
        ;;
    
    *)
        echo -e "${RED}Comando inválido: $1${NC}"
        echo "Use: electron-fix help"
        ;;
esac
EOF

# Instalar comando global
echo "🔧 Instalando comando global..."
echo "   Isso pode pedir sua senha de administrador"
echo ""

sudo mv /tmp/electron-fix-temp "$GLOBAL_SCRIPT"
sudo chmod +x "$GLOBAL_SCRIPT"

if [ -f "$GLOBAL_SCRIPT" ]; then
    echo "✅ Comando instalado com sucesso!"
    echo ""
    echo "📝 Agora você pode usar de qualquer lugar:"
    echo ""
    echo "  electron-fix           # Menu interativo"
    echo "  electron-fix diagnose  # Apenas diagnóstico"
    echo "  electron-fix fix       # Diagnóstico + Correções"
    echo "  electron-fix monitor   # Monitor contínuo"
    echo "  electron-fix start     # Iniciar Electron"
    echo "  electron-fix clean     # Limpar cache"
    echo "  electron-fix report    # Ver relatório"
    echo "  electron-fix help      # Ajuda"
    echo ""
else
    echo "❌ Falha na instalação"
    exit 1
fi