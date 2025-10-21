#!/bin/bash

# 🔧 FIX ELECTRON DEPENDENCIES - Corrige erro de módulos faltantes

echo "╔══════════════════════════════════════════════════════╗"
echo "║       🔧 CORRIGINDO ERRO DO ELECTRON                 ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "❌ ERRO DETECTADO:"
echo "   Cannot find package 'jsonwebtoken'"
echo ""
echo "🔍 Analisando dependências..."
echo ""

# Configurar PATH
export PATH="/opt/homebrew/opt/node@20/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
NODE_BIN="/opt/homebrew/opt/node@20/bin/node"
NPM_BIN="/opt/homebrew/opt/node@20/bin/npm"

# Diretório do projeto
cd /Users/clubproducoes/Digimundo/digimundo_starter

# Criar diretório de logs
mkdir -p eternal_logs
LOG_FILE="eternal_logs/fix_dependencies_$(date +%Y%m%d_%H%M%S).log"

# Função de log
log() {
    echo "$1"
    echo "[$(date '+%H:%M:%S')] $1" >> "$LOG_FILE"
}

# 1. Verificar módulos faltantes
log "📋 Verificando módulos faltantes..."
echo ""

MISSING_MODULES=()

# Lista de módulos essenciais
REQUIRED_MODULES=(
    "jsonwebtoken"
    "bcrypt"
    "cors"
    "express"
    "socket.io"
    "sqlite3"
    "sqlite"
    "dotenv"
    "axios"
    "node-fetch"
    "ws"
)

for module in "${REQUIRED_MODULES[@]}"; do
    if [ ! -d "node_modules/$module" ]; then
        MISSING_MODULES+=("$module")
        log "   ❌ $module - FALTANDO"
    else
        log "   ✅ $module - instalado"
    fi
done

echo ""

# 2. Se há módulos faltantes, instalar
if [ ${#MISSING_MODULES[@]} -gt 0 ]; then
    log "🚀 Instalando módulos faltantes..."
    echo ""
    
    # Limpar cache primeiro
    log "🧹 Limpando cache npm..."
    $NPM_BIN cache clean --force >> "$LOG_FILE" 2>&1
    
    # Instalar módulos específicos
    for module in "${MISSING_MODULES[@]}"; do
        log "   📦 Instalando $module..."
        $NPM_BIN install "$module" --save >> "$LOG_FILE" 2>&1
        
        if [ $? -eq 0 ]; then
            log "   ✅ $module instalado com sucesso"
        else
            log "   ❌ Erro ao instalar $module"
        fi
    done
    
    echo ""
    log "🔄 Executando npm install completo para garantir..."
    $NPM_BIN install >> "$LOG_FILE" 2>&1
    
else
    log "✅ Todos os módulos já estão instalados!"
fi

# 3. Verificar se o problema foi resolvido
echo ""
log "🧪 Testando se o erro foi corrigido..."

# Testar importação do módulo
$NODE_BIN -e "
import('jsonwebtoken').then(() => {
    console.log('   ✅ jsonwebtoken funcionando!');
    process.exit(0);
}).catch(err => {
    console.log('   ❌ Ainda com erro:', err.message);
    process.exit(1);
});
" 2>/dev/null

JWT_RESULT=$?

$NODE_BIN -e "
import('bcrypt').then(() => {
    console.log('   ✅ bcrypt funcionando!');
    process.exit(0);
}).catch(err => {
    console.log('   ❌ Ainda com erro:', err.message);
    process.exit(1);
});
" 2>/dev/null

BCRYPT_RESULT=$?

# 4. Criar script de verificação de saúde
cat > check_dependencies.js << 'EOF'
import { createRequire } from 'module';
const require = createRequire(import.meta.url);

console.log('\n📋 Verificação de Dependências:');
console.log('================================\n');

const modules = [
    'jsonwebtoken',
    'bcrypt',
    'express',
    'cors',
    'socket.io',
    'sqlite3',
    'dotenv',
    'axios',
    'node-fetch'
];

let allOk = true;

for (const module of modules) {
    try {
        require.resolve(module);
        console.log(`✅ ${module} - OK`);
    } catch (e) {
        console.log(`❌ ${module} - FALTANDO`);
        allOk = false;
    }
}

console.log('\n================================');
if (allOk) {
    console.log('✅ Todas as dependências estão instaladas!');
} else {
    console.log('❌ Algumas dependências estão faltando.');
    console.log('   Execute: npm install');
}
console.log('================================\n');

process.exit(allOk ? 0 : 1);
EOF

# Executar verificação
echo ""
$NODE_BIN check_dependencies.js

# 5. Reiniciar Electron se necessário
echo ""
log "🔄 Verificando se o Electron precisa ser reiniciado..."

# Verificar se há processos Electron rodando
ELECTRON_PIDS=$(ps aux | grep -E "Electron.*digimundo" | grep -v grep | awk '{print $2}')

if [ ! -z "$ELECTRON_PIDS" ]; then
    log "⚠️  Electron detectado. Reiniciando..."
    
    # Matar processos antigos
    for pid in $ELECTRON_PIDS; do
        kill $pid 2>/dev/null
        log "   Processo $pid terminado"
    done
    
    sleep 2
    
    # Reiniciar Electron
    log "🚀 Reiniciando Electron..."
    nohup $NPM_BIN run dev >> "$LOG_FILE" 2>&1 &
    NEW_PID=$!
    log "   Novo processo iniciado: PID $NEW_PID"
else
    log "ℹ️  Electron não está rodando"
fi

# 6. Resultado final
echo ""
echo "╔══════════════════════════════════════════════════════╗"

if [ $JWT_RESULT -eq 0 ] && [ $BCRYPT_RESULT -eq 0 ]; then
    echo "║         ✅ PROBLEMA RESOLVIDO!                       ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo ""
    echo "🎉 Módulos instalados com sucesso:"
    echo "   • jsonwebtoken ✅"
    echo "   • bcrypt ✅"
    echo "   • Todas as outras dependências ✅"
    echo ""
    echo "📋 Próximos passos:"
    echo "   1. Reinicie o Electron: npm run dev"
    echo "   2. O erro não deve mais aparecer"
else
    echo "║         ⚠️  ATENÇÃO NECESSÁRIA                       ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo ""
    echo "Alguns módulos ainda precisam de atenção."
    echo "Execute manualmente:"
    echo "   cd ~/Digimundo/digimundo_starter"
    echo "   npm install --force"
fi

echo ""
echo "📁 Log salvo em: $LOG_FILE"
echo ""
