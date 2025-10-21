#!/bin/bash

# =====================================================
# 🚨 CORREÇÃO RÁPIDA DE EMERGÊNCIA
# =====================================================

echo "🚨 CORREÇÃO DE EMERGÊNCIA INICIADA..."
echo ""

# 1. MATAR TUDO
echo "1️⃣ Matando todos os processos..."
pkill -f "Electron" 2>/dev/null || true
pkill -f "electron" 2>/dev/null || true  
pkill -f "node" 2>/dev/null || true
pkill -f "npm" 2>/dev/null || true
lsof -ti:7937 | xargs kill -9 2>/dev/null || true
sleep 2

# 2. LIMPAR ARQUIVOS PROBLEMÁTICOS
echo "2️⃣ Limpando arquivos problemáticos..."
cd ~/Digimundo/digimundo_starter
rm -f .*.pid 2>/dev/null || true
rm -f *.pid 2>/dev/null || true
rm -rf eternal_logs/*.log 2>/dev/null || true

# 3. VERIFICAR O PROBLEMA REAL
echo "3️⃣ Verificando o problema real..."
echo ""

# Testar se consegue importar os módulos
node -e "
console.log('Testando módulos...');
try {
  const path = require('path');
  console.log('✅ require funciona');
} catch(e) {
  console.log('❌ require não funciona:', e.message);
}

import('module').then(m => {
  const { createRequire } = m;
  const require = createRequire(import.meta.url);
  try {
    const jwt = require('jsonwebtoken');
    console.log('✅ jsonwebtoken carregado');
  } catch(e) {
    console.log('❌ jsonwebtoken erro:', e.message);
  }
}).catch(e => {
  console.log('❌ Erro no import:', e.message);
});
" 2>&1

echo ""
echo "4️⃣ Verificando package.json..."
if grep -q '"type": "module"' package.json; then
    echo "⚠️ package.json tem type: module"
    echo "Isso causa incompatibilidade com require()"
fi

echo ""
echo "5️⃣ Solução: Vamos criar um starter que funciona..."

# Criar um starter simples que funciona
cat > start_electron_simple.js << 'EOF'
#!/usr/bin/env node

// Starter simples sem ESM
const { spawn } = require('child_process');
const path = require('path');

console.log('🚀 Iniciando Electron (modo compatível)...\n');

// Remover temporariamente o type: module
const fs = require('fs');
const packagePath = path.join(__dirname, 'package.json');
const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf-8'));

if (pkg.type === 'module') {
    console.log('⚠️ Removendo temporariamente "type": "module"...');
    delete pkg.type;
    fs.writeFileSync(packagePath, JSON.stringify(pkg, null, 2));
}

// Iniciar Electron
const electron = spawn('npx', ['electron', '.'], {
    stdio: 'inherit',
    shell: true,
    cwd: __dirname
});

electron.on('error', (err) => {
    console.error('❌ Erro ao iniciar:', err);
});

electron.on('exit', (code) => {
    console.log(`Electron finalizado com código: ${code}`);
    
    // Restaurar type: module se necessário
    if (code === 0) {
        pkg.type = 'module';
        fs.writeFileSync(packagePath, JSON.stringify(pkg, null, 2));
    }
});
EOF

chmod +x start_electron_simple.js

echo ""
echo "✅ Starter criado!"
echo ""
echo "================================================"
echo "         USE ESTE COMANDO PARA INICIAR:"
echo "================================================"
echo ""
echo "  node start_electron_simple.js"
echo ""
echo "================================================"
echo ""

# Perguntar se quer iniciar agora
read -p "Deseja iniciar agora? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    node start_electron_simple.js
fi
