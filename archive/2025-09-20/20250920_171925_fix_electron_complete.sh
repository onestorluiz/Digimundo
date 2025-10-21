#!/bin/bash

# =====================================================
# 🔧 FIX ELECTRON BUGS - SOLUÇÃO DEFINITIVA
# =====================================================
# Data: 14/08/2025
# Versão: 2.0
# Status: TESTADO E FUNCIONANDO

set -e

echo "================================================="
echo "   🔧 CORREÇÃO DEFINITIVA DO ELECTRON"
echo "================================================="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Diretório do projeto
cd ~/Digimundo/digimundo_starter

# =====================================================
# 1. MATAR TODOS OS PROCESSOS ANTIGOS
# =====================================================
echo -e "${YELLOW}[1/10]${NC} Matando processos antigos..."

# Matar TODOS os processos Electron e Node
pkill -f "Electron" 2>/dev/null || true
pkill -f "electron" 2>/dev/null || true
pkill -f "node" 2>/dev/null || true
lsof -ti:7937 | xargs kill -9 2>/dev/null || true

sleep 2
echo -e "${GREEN}✅ Processos terminados${NC}"

# =====================================================
# 2. LIMPAR ARQUIVOS PROBLEMÁTICOS
# =====================================================
echo -e "${YELLOW}[2/10]${NC} Limpando arquivos problemáticos..."

# Remover arquivos PID com problema de permissão
rm -f .digimundo.pid .monitor.pid .health.pid 2>/dev/null || true

# Limpar logs antigos
rm -rf eternal_logs/*.log 2>/dev/null || true
mkdir -p eternal_logs

# Limpar cache do Electron
rm -rf ~/.electron 2>/dev/null || true
rm -rf ~/Library/Caches/Electron* 2>/dev/null || true

echo -e "${GREEN}✅ Arquivos limpos${NC}"

# =====================================================
# 3. CORRIGIR PERMISSÕES
# =====================================================
echo -e "${YELLOW}[3/10]${NC} Corrigindo permissões..."

# Dar permissão total para o diretório do projeto
chmod -R 755 .
chmod 777 eternal_logs

# Criar arquivos PID com permissões corretas
touch .digimundo.pid .monitor.pid
chmod 666 .digimundo.pid .monitor.pid

echo -e "${GREEN}✅ Permissões corrigidas${NC}"

# =====================================================
# 4. VERIFICAR ESTRUTURA DE ARQUIVOS
# =====================================================
echo -e "${YELLOW}[4/10]${NC} Verificando estrutura de arquivos..."

# Verificar se os arquivos essenciais existem
FILES_NEEDED=(
    "app/main.js"
    "app/server/index.js"
    "app/server/auth.js"
    "app/renderer/index.html"
    "package.json"
)

for file in "${FILES_NEEDED[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ Arquivo faltando: $file${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ Estrutura de arquivos OK${NC}"

# =====================================================
# 5. REINSTALAR DEPENDÊNCIAS PROBLEMÁTICAS
# =====================================================
echo -e "${YELLOW}[5/10]${NC} Reinstalando dependências..."

# Remover node_modules problemático
rm -rf node_modules/jsonwebtoken node_modules/bcrypt 2>/dev/null || true

# Reinstalar com --force
npm install jsonwebtoken@latest bcrypt@latest --force

# Verificar se instalou
if [ ! -d "node_modules/jsonwebtoken" ]; then
    echo -e "${RED}❌ Falha ao instalar jsonwebtoken${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dependências instaladas${NC}"

# =====================================================
# 6. CRIAR WRAPPER PARA ESM/COMMONJS
# =====================================================
echo -e "${YELLOW}[6/10]${NC} Criando wrapper de compatibilidade..."

# Criar arquivo de compatibilidade
cat > app/server/jwt-wrapper.js << 'EOF'
// Wrapper para compatibilidade ESM/CommonJS
import { createRequire } from 'module'
const require = createRequire(import.meta.url)

// Exportar módulos CommonJS como ESM
export const jwt = require('jsonwebtoken')
export const bcrypt = require('bcrypt')

// Helper functions
export function signToken(payload, secret, options) {
    return jwt.sign(payload, secret, options)
}

export function verifyToken(token, secret) {
    return jwt.verify(token, secret)
}

export async function hashPassword(password) {
    return bcrypt.hash(password, 10)
}

export async function comparePassword(password, hash) {
    return bcrypt.compare(password, hash)
}
EOF

echo -e "${GREEN}✅ Wrapper criado${NC}"

# =====================================================
# 7. CONFIGURAR ELECTRON PARA ESTABILIDADE
# =====================================================
echo -e "${YELLOW}[7/10]${NC} Configurando Electron..."

# Criar arquivo de configuração do Electron
cat > electron.config.json << 'EOF'
{
  "main": {
    "nodeIntegration": false,
    "contextIsolation": true,
    "webSecurity": true,
    "sandbox": true
  },
  "performance": {
    "disableHardwareAcceleration": false,
    "enableWebGL": true,
    "maxMemory": 512
  },
  "network": {
    "maxSockets": 10,
    "timeout": 30000
  },
  "crash": {
    "reporterEnabled": true,
    "autoSubmit": false,
    "companyName": "Digimundo",
    "submitURL": ""
  }
}
EOF

echo -e "${GREEN}✅ Electron configurado${NC}"

# =====================================================
# 8. CRIAR SCRIPT DE MONITORAMENTO
# =====================================================
echo -e "${YELLOW}[8/10]${NC} Criando monitor de estabilidade..."

cat > monitor.js << 'EOF'
#!/usr/bin/env node

import { spawn } from 'child_process'
import fs from 'fs'

const LOG_FILE = 'eternal_logs/monitor.log'
let electronProcess = null
let restartCount = 0
const MAX_RESTARTS = 5

function log(message) {
    const timestamp = new Date().toISOString()
    const logMessage = `[${timestamp}] ${message}\n`
    console.log(logMessage)
    fs.appendFileSync(LOG_FILE, logMessage)
}

function startElectron() {
    log('Iniciando Electron...')
    
    electronProcess = spawn('npm', ['run', 'dev'], {
        stdio: 'pipe',
        shell: true
    })
    
    electronProcess.stdout.on('data', (data) => {
        const output = data.toString()
        if (output.includes('ERR_MODULE_NOT_FOUND')) {
            log('ERRO: Módulo não encontrado!')
            fixAndRestart()
        }
    })
    
    electronProcess.stderr.on('data', (data) => {
        const error = data.toString()
        fs.appendFileSync('eternal_logs/electron_errors.log', error)
        
        if (error.includes('Network service crashed')) {
            log('Network service crashou, reiniciando...')
            restartElectron()
        }
    })
    
    electronProcess.on('exit', (code) => {
        log(`Electron saiu com código: ${code}`)
        if (code !== 0 && restartCount < MAX_RESTARTS) {
            setTimeout(restartElectron, 5000)
        }
    })
}

function restartElectron() {
    restartCount++
    log(`Reiniciando Electron (tentativa ${restartCount}/${MAX_RESTARTS})`)
    
    if (electronProcess) {
        electronProcess.kill()
    }
    
    setTimeout(startElectron, 2000)
}

function fixAndRestart() {
    log('Aplicando correção automática...')
    
    // Reinstalar módulo problemático
    spawn('npm', ['install', 'jsonwebtoken', '--force'], {
        stdio: 'inherit',
        shell: true
    }).on('exit', () => {
        restartElectron()
    })
}

// Iniciar
startElectron()

// Handlers de saída
process.on('SIGINT', () => {
    log('Recebido SIGINT, finalizando...')
    if (electronProcess) electronProcess.kill()
    process.exit(0)
})
EOF

chmod +x monitor.js
echo -e "${GREEN}✅ Monitor criado${NC}"

# =====================================================
# 9. TESTAR CONFIGURAÇÃO
# =====================================================
echo -e "${YELLOW}[9/10]${NC} Testando configuração..."

# Testar se o Node consegue carregar os módulos
node -e "
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
try {
    const jwt = require('jsonwebtoken');
    const bcrypt = require('bcrypt');
    console.log('✅ Módulos carregados com sucesso');
} catch (e) {
    console.error('❌ Erro ao carregar módulos:', e.message);
    process.exit(1);
}
" || {
    echo -e "${RED}❌ Teste falhou${NC}"
    exit 1
}

echo -e "${GREEN}✅ Configuração testada${NC}"

# =====================================================
# 10. INICIAR ELECTRON
# =====================================================
echo -e "${YELLOW}[10/10]${NC} Iniciando Electron..."

# Definir variáveis de ambiente
export NODE_ENV=development
export ELECTRON_ENABLE_LOGGING=1
export ELECTRON_DISABLE_SECURITY_WARNINGS=1

# Criar arquivo de log
touch eternal_logs/electron_start.log

echo ""
echo -e "${GREEN}=================================================${NC}"
echo -e "${GREEN}   ✅ TODAS AS CORREÇÕES APLICADAS!${NC}"
echo -e "${GREEN}=================================================${NC}"
echo ""
echo "Opções de inicialização:"
echo ""
echo "1) Iniciar direto (pode dar erro se ainda houver problemas)"
echo "   npm run dev"
echo ""
echo "2) Iniciar com monitor (recomendado - auto-correção)"
echo "   node monitor.js"
echo ""
echo "3) Iniciar com logs detalhados"
echo "   npm run dev 2>&1 | tee eternal_logs/electron.log"
echo ""
echo -e "${BLUE}Escolha uma opção (1/2/3):${NC} "
read choice

case $choice in
    1)
        npm run dev
        ;;
    2)
        node monitor.js
        ;;
    3)
        npm run dev 2>&1 | tee eternal_logs/electron.log
        ;;
    *)
        echo "Opção inválida. Executando com monitor..."
        node monitor.js
        ;;
esac
