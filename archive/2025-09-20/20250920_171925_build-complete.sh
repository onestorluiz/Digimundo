#!/bin/bash

echo "🚀 DIGIMUNDO COMPLETE BUILD SYSTEM"
echo "==================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check dependencies
echo "1️⃣ Verificando dependências..."

if ! command -v node &> /dev/null; then
    echo -e "${RED}✗${NC} Node.js não encontrado"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}✗${NC} npm não encontrado"
    exit 1
fi

echo -e "${GREEN}✓${NC} Dependências OK"
echo ""

# Clean previous builds
echo "2️⃣ Limpando builds anteriores..."
rm -rf dist release
echo -e "${GREEN}✓${NC} Limpeza completa"
echo ""

# Install dependencies
echo "3️⃣ Instalando dependências..."
npm install
echo -e "${GREEN}✓${NC} Dependências instaladas"
echo ""

# Create assets
echo "4️⃣ Preparando assets..."
if [ ! -f assets/icon.icns ]; then
    echo "Criando ícone..."
    node create-icon.js
    # Convert to ICNS
    mkdir -p assets/icon.iconset
    sips -z 16 16     assets/icon.png --out assets/icon.iconset/icon_16x16.png 2>/dev/null
    sips -z 32 32     assets/icon.png --out assets/icon.iconset/icon_16x16@2x.png 2>/dev/null
    sips -z 32 32     assets/icon.png --out assets/icon.iconset/icon_32x32.png 2>/dev/null
    sips -z 64 64     assets/icon.png --out assets/icon.iconset/icon_32x32@2x.png 2>/dev/null
    sips -z 128 128   assets/icon.png --out assets/icon.iconset/icon_128x128.png 2>/dev/null
    sips -z 256 256   assets/icon.png --out assets/icon.iconset/icon_128x128@2x.png 2>/dev/null
    sips -z 256 256   assets/icon.png --out assets/icon.iconset/icon_256x256.png 2>/dev/null
    sips -z 512 512   assets/icon.png --out assets/icon.iconset/icon_256x256@2x.png 2>/dev/null
    sips -z 512 512   assets/icon.png --out assets/icon.iconset/icon_512x512.png 2>/dev/null
    sips -z 1024 1024 assets/icon.png --out assets/icon.iconset/icon_512x512@2x.png 2>/dev/null
    iconutil -c icns assets/icon.iconset -o assets/icon.icns 2>/dev/null
    rm -rf assets/icon.iconset
fi

if [ ! -f assets/tray-icon.png ]; then
    cp assets/icon.png assets/tray-icon.png
    sips -z 32 32 assets/icon.png --out assets/tray-icon.png 2>/dev/null
fi

if [ ! -f assets/dmg-background.png ] || [ $(stat -f%z assets/dmg-background.png) -eq 0 ]; then
    node create-dmg-bg.js
fi

echo -e "${GREEN}✓${NC} Assets prontos"
echo ""

# Build Electron app
echo "5️⃣ Building app..."
npm run pack

if [ -d "release/mac-arm64/Digimundo.app" ]; then
    echo -e "${GREEN}✓${NC} App criado com sucesso!"
    
    # Copy icon to app
    cp assets/icon.icns "release/mac-arm64/Digimundo.app/Contents/Resources/electron.icns" 2>/dev/null
    
    # Show app info
    echo ""
    echo "📊 Informações do App:"
    APP_SIZE=$(du -sh release/mac-arm64/Digimundo.app | cut -f1)
    echo "   Tamanho: $APP_SIZE"
    echo "   Local: release/mac-arm64/Digimundo.app"
    echo ""
    
    # Test Claude integration
    echo "6️⃣ Testando integração Claude..."
    if [ -f "/Users/clubproducoes/.local/bin/claude" ]; then
        echo -e "${GREEN}✓${NC} Claude Code detectado"
    else
        echo -e "${YELLOW}⚠${NC} Claude Code não encontrado (opcional)"
    fi
    
    # Test Ollama
    echo ""
    echo "7️⃣ Testando Ollama..."
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Ollama está rodando"
        MODELS=$(curl -s http://localhost:11434/api/tags | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | head -5)
        if [ ! -z "$MODELS" ]; then
            echo "   Modelos disponíveis:"
            echo "$MODELS" | while read model; do
                echo "   - $model"
            done
        fi
    else
        echo -e "${YELLOW}⚠${NC} Ollama não está rodando"
        echo "   Para iniciar: ollama serve"
    fi
    
    echo ""
    echo "==================================="
    echo -e "${GREEN}✅ BUILD COMPLETO!${NC}"
    echo ""
    echo "🚀 Para usar o app:"
    echo "   open release/mac-arm64/Digimundo.app"
    echo ""
    echo "📦 Para criar DMG (distribuição):"
    echo "   npm run dist:dmg"
    echo ""
    echo "🔧 Funcionalidades:"
    echo "   ✓ Interface moderna React + Tailwind"
    echo "   ✓ Dark/Light mode"
    echo "   ✓ Múltiplos Digimons"
    echo "   ✓ Integração Ollama"
    echo "   ✓ Integração Claude Code (Cmd+Shift+C)"
    echo "   ✓ Auto-updater"
    echo "   ✓ Tray icon"
    echo ""
else
    echo -e "${RED}✗${NC} Erro no build"
    exit 1
fi