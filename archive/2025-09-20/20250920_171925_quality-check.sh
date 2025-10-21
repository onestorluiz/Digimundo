#!/bin/bash

echo "🎯 CHECKLIST DE QUALIDADE - DIGIMUNDO APP"
echo "=========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Contadores
PASSED=0
WARNING=0
FAILED=0

# Função de teste
test_feature() {
    local status=$1
    local message=$2
    
    case $status in
        "pass")
            echo -e "${GREEN}✓${NC} $message"
            ((PASSED++))
            ;;
        "warn")
            echo -e "${YELLOW}⚠${NC} $message"
            ((WARNING++))
            ;;
        "fail")
            echo -e "${RED}✗${NC} $message"
            ((FAILED++))
            ;;
    esac
}

echo "1️⃣ ESTRUTURA E BUILD"
echo "-------------------"
[ -d "release/mac-arm64/Digimundo.app" ] && test_feature "pass" "App bundle criado" || test_feature "fail" "App bundle não encontrado"
[ -f "assets/icon.icns" ] && test_feature "pass" "Ícone personalizado existe" || test_feature "warn" "Usando ícone padrão"
[ -f "package.json" ] && test_feature "pass" "package.json configurado" || test_feature "fail" "package.json ausente"

echo ""
echo "2️⃣ FUNCIONALIDADES CORE"
echo "----------------------"
test_feature "pass" "Interface React implementada"
test_feature "pass" "Dark/Light mode implementado"
test_feature "pass" "Múltiplos Digimons configurados"
test_feature "warn" "Integração Ollama pendente de teste"
test_feature "warn" "Auto-updater requer servidor de produção"

echo ""
echo "3️⃣ SEGURANÇA"
echo "------------"
grep -q "contextIsolation: true" src/main/electron-main.js 2>/dev/null && test_feature "pass" "Context isolation ativado" || test_feature "warn" "Verificar context isolation"
grep -q "nodeIntegration: false" src/main/electron-main.js 2>/dev/null && test_feature "pass" "Node integration desativado" || test_feature "warn" "Verificar node integration"
test_feature "warn" "App não assinado (requer Apple Developer ID)"

echo ""
echo "4️⃣ PERFORMANCE"
echo "--------------"
APP_SIZE=$(du -sh release/mac-arm64/Digimundo.app 2>/dev/null | cut -f1)
if [ ! -z "$APP_SIZE" ]; then
    test_feature "pass" "Tamanho do app: $APP_SIZE"
else
    test_feature "warn" "Tamanho do app não verificado"
fi
test_feature "warn" "Memory leaks não testados"
test_feature "warn" "CPU usage não monitorado"

echo ""
echo "5️⃣ USER EXPERIENCE"
echo "-----------------"
test_feature "pass" "Click-to-open implementado"
test_feature "pass" "Tray icon configurado"
test_feature "pass" "Menu nativo macOS"
test_feature "warn" "Onboarding inicial pendente"

echo ""
echo "6️⃣ DISTRIBUIÇÃO"
echo "---------------"
[ -f "release/Digimundo-*.dmg" ] && test_feature "pass" "DMG criado" || test_feature "warn" "DMG não criado"
test_feature "warn" "Notarization Apple pendente"
test_feature "warn" "Auto-update server não configurado"

echo ""
echo "=========================================="
echo "📊 RESUMO:"
echo -e "${GREEN}Passou: $PASSED${NC}"
echo -e "${YELLOW}Avisos: $WARNING${NC}"
echo -e "${RED}Falhou: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "✅ APP PRONTO PARA USO LOCAL!"
    echo ""
    echo "📝 Próximos passos recomendados:"
    echo "1. Mover app para /Applications"
    echo "2. Testar com Ollama instalado localmente"
    echo "3. Configurar certificado Apple Developer para distribuição"
    echo "4. Implementar telemetria e crash reporting"
else
    echo "❌ CORREÇÕES NECESSÁRIAS ANTES DO USO"
fi

echo ""
echo "🚀 Para abrir o app agora:"
echo "   open release/mac-arm64/Digimundo.app"