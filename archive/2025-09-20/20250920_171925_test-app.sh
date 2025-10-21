#!/bin/bash

echo "🧪 Testando Digimundo App..."
echo "================================"

# 1. Verificar estrutura do app
echo "✓ Verificando estrutura do app..."
if [ -d "release/mac-arm64/Digimundo.app" ]; then
    echo "  ✓ App bundle existe"
else
    echo "  ✗ App bundle não encontrado"
    exit 1
fi

# 2. Verificar ícone
echo "✓ Verificando ícone..."
if [ -f "release/mac-arm64/Digimundo.app/Contents/Resources/electron.icns" ]; then
    echo "  ✓ Ícone presente"
else
    echo "  ⚠️  Ícone padrão do Electron"
fi

# 3. Verificar Info.plist
echo "✓ Verificando Info.plist..."
if grep -q "Digimundo" release/mac-arm64/Digimundo.app/Contents/Info.plist; then
    echo "  ✓ Nome da aplicação configurado"
else
    echo "  ✗ Nome da aplicação não configurado"
fi

# 4. Verificar tamanho do app
echo "✓ Verificando tamanho do app..."
APP_SIZE=$(du -sh release/mac-arm64/Digimundo.app | cut -f1)
echo "  Tamanho: $APP_SIZE"

# 5. Verificar dependências
echo "✓ Verificando dependências críticas..."
if [ -f "release/mac-arm64/Digimundo.app/Contents/Resources/app/package.json" ]; then
    echo "  ✓ package.json presente"
else
    echo "  ⚠️  package.json não encontrado no bundle"
fi

echo ""
echo "================================"
echo "📋 Recomendações:"
echo ""
echo "1. Testar manualmente:"
echo "   - Abrir o app e verificar se a interface carrega"
echo "   - Testar envio de mensagens"
echo "   - Verificar mudança de tema (dark/light)"
echo "   - Testar seleção de diferentes Digimons"
echo ""
echo "2. Para distribuição:"
echo "   - Assinar o app com certificado Apple Developer"
echo "   - Criar DMG installer com: npm run dist:dmg"
echo "   - Testar auto-updater com servidor de staging"
echo ""
echo "3. Otimizações recomendadas:"
echo "   - Implementar lazy loading para modelos Ollama"
echo "   - Adicionar cache local para conversas"
echo "   - Implementar compressão de histórico"