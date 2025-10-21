#!/bin/bash

# ============================================
# COMANDOS ALTERNATIVOS PARA RECOMPILAÇÃO
# ============================================

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   COMANDOS MANUAIS PARA RECOMPILAÇÃO DOS MÓDULOS NATIVOS    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

PROJECT_DIR="/Users/clubproducoes/Digimundo/digimundo_starter"
cd "$PROJECT_DIR"

echo "📁 Diretório: $PROJECT_DIR"
echo ""
echo "Execute os comandos abaixo em sequência se o script automático falhar:"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  LIMPAR CACHE E REINSTALAR:"
echo ""
echo "   rm -rf node_modules/sqlite3"
echo "   rm -rf node_modules/node-llama-cpp"
echo "   rm -rf node_modules/bcrypt"
echo "   npm cache clean --force"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "2️⃣  INSTALAR electron-rebuild:"
echo ""
echo "   npm install --save-dev electron-rebuild"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "3️⃣  RECOMPILAR sqlite3:"
echo ""
echo "   npm install sqlite3 --build-from-source --runtime=electron --target=31.2.0 --dist-url=https://electronjs.org/headers"
echo ""
echo "   OU"
echo ""
echo "   npx electron-rebuild -f -w sqlite3"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "4️⃣  RECOMPILAR bcrypt:"
echo ""
echo "   npm uninstall bcrypt"
echo "   npm install bcrypt"
echo "   npx electron-rebuild -f -w bcrypt"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "5️⃣  RECOMPILAR node-llama-cpp (OPCIONAL):"
echo ""
echo "   npm uninstall node-llama-cpp"
echo "   npm install node-llama-cpp --build-from-source"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "6️⃣  ALTERNATIVA - Usar node-gyp diretamente:"
echo ""
echo "   cd node_modules/sqlite3"
echo "   npm run install --build-from-source --runtime=electron --target=31.2.0"
echo "   cd ../.."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "7️⃣  SE TUDO FALHAR - Reset completo:"
echo ""
echo "   rm -rf node_modules package-lock.json"
echo "   rm -rf ~/.npm ~/.electron"
echo "   npm cache clean --force"
echo "   npm install"
echo "   npx electron-rebuild"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Tentar executar automaticamente
read -p "Deseja executar a recompilação automática agora? (s/n): " resposta

if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
    echo ""
    echo "🔧 Iniciando recompilação automática..."
    echo ""
    
    # Instalar electron-rebuild
    echo "📦 Instalando electron-rebuild..."
    npm install --save-dev electron-rebuild
    
    # Recompilar sqlite3
    echo ""
    echo "🔧 Recompilando sqlite3..."
    rm -rf node_modules/sqlite3
    npm install sqlite3 --build-from-source --runtime=electron --target=31.2.0 --dist-url=https://electronjs.org/headers
    
    # Recompilar bcrypt
    echo ""
    echo "🔧 Recompilando bcrypt..."
    npx electron-rebuild -f -w bcrypt
    
    # Verificar se node-llama-cpp existe
    if [ -d "node_modules/node-llama-cpp" ]; then
        echo ""
        echo "🔧 Recompilando node-llama-cpp..."
        npx electron-rebuild -f -w node-llama-cpp
    fi
    
    echo ""
    echo "✅ Recompilação concluída!"
    echo ""
    echo "🚀 Agora execute:"
    echo "   npm run dev"
    echo "   ou"
    echo "   ./run-electron-fix.sh"
else
    echo ""
    echo "📝 Execute os comandos manualmente conforme necessário."
fi