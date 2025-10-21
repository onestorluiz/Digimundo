#!/bin/bash

# =====================================================
# 🚀 INICIAR ELECTRON - GARANTIDO
# =====================================================

echo "🚀 INICIANDO ELECTRON - MODO GARANTIDO"
echo "======================================"
echo ""

cd ~/Digimundo/digimundo_starter

# 1. Matar tudo
pkill -f "Electron" 2>/dev/null || true
pkill -f "electron" 2>/dev/null || true
pkill -f "node" 2>/dev/null || true
sleep 1

# 2. Garantir que está em CommonJS
if grep -q '"type": "module"' package.json; then
    echo "🔧 Convertendo para CommonJS..."
    node fix_to_commonjs.js
fi

# 3. Iniciar
echo "🚀 Iniciando..."
npm run dev
