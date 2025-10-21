#!/usr/bin/env node

/**
 * 🔍 TESTE DE DIAGNÓSTICO DO ELECTRON
 * Verifica todos os problemas conhecidos
 */

import { createRequire } from 'module'
import fs from 'fs'
import { spawn } from 'child_process'
import path from 'path'

const require = createRequire(import.meta.url)

// Cores
const RED = '\x1b[31m'
const GREEN = '\x1b[32m'
const YELLOW = '\x1b[33m'
const BLUE = '\x1b[34m'
const RESET = '\x1b[0m'

console.log(`${BLUE}========================================${RESET}`)
console.log(`${BLUE}   DIAGNÓSTICO COMPLETO DO ELECTRON${RESET}`)
console.log(`${BLUE}========================================${RESET}\n`)

let errors = []
let warnings = []
let success = []

// ========================================
// TESTE 1: MÓDULOS PROBLEMÁTICOS
// ========================================
console.log(`${YELLOW}[TESTE 1] Verificando módulos CommonJS/ESM...${RESET}`)

try {
    // Testar jsonwebtoken
    const jwt = require('jsonwebtoken')
    success.push('✅ jsonwebtoken carregado via require')
} catch (e) {
    errors.push(`❌ jsonwebtoken: ${e.message}`)
}

try {
    // Testar bcrypt
    const bcrypt = require('bcrypt')
    success.push('✅ bcrypt carregado via require')
} catch (e) {
    errors.push(`❌ bcrypt: ${e.message}`)
}

// ========================================
// TESTE 2: PERMISSÕES DE ARQUIVO
// ========================================
console.log(`${YELLOW}[TESTE 2] Verificando permissões...${RESET}`)

try {
    fs.writeFileSync('.test_permission.pid', 'test')
    fs.unlinkSync('.test_permission.pid')
    success.push('✅ Permissões de escrita OK')
} catch (e) {
    errors.push(`❌ Permissão negada: ${e.message}`)
}

// ========================================
// TESTE 3: ESTRUTURA DE ARQUIVOS
// ========================================
console.log(`${YELLOW}[TESTE 3] Verificando arquivos essenciais...${RESET}`)

const essentialFiles = [
    'app/main.js',
    'app/server/index.js',
    'app/server/auth.js',
    'app/renderer/index.html',
    'package.json'
]

essentialFiles.forEach(file => {
    if (fs.existsSync(file)) {
        success.push(`✅ ${file} existe`)
    } else {
        errors.push(`❌ ${file} não encontrado`)
    }
})

// ========================================
// TESTE 4: PACKAGE.JSON
// ========================================
console.log(`${YELLOW}[TESTE 4] Verificando package.json...${RESET}`)

try {
    const pkg = JSON.parse(fs.readFileSync('package.json', 'utf-8'))
    
    if (pkg.type === 'module') {
        warnings.push('⚠️ package.json tem "type": "module" (pode causar problemas com CommonJS)')
    }
    
    if (!pkg.dependencies.jsonwebtoken) {
        errors.push('❌ jsonwebtoken não está nas dependências')
    } else {
        success.push('✅ jsonwebtoken nas dependências')
    }
    
    if (!pkg.dependencies.bcrypt) {
        errors.push('❌ bcrypt não está nas dependências')
    } else {
        success.push('✅ bcrypt nas dependências')
    }
    
} catch (e) {
    errors.push(`❌ Erro ao ler package.json: ${e.message}`)
}

// ========================================
// TESTE 5: PROCESSOS ZUMBIS
// ========================================
console.log(`${YELLOW}[TESTE 5] Verificando processos Electron...${RESET}`)

const checkProcesses = spawn('pgrep', ['-f', 'Electron'], { shell: true })
let electronPids = ''

checkProcesses.stdout.on('data', (data) => {
    electronPids += data.toString()
})

checkProcesses.on('close', () => {
    if (electronPids.trim()) {
        const pids = electronPids.trim().split('\n')
        warnings.push(`⚠️ ${pids.length} processo(s) Electron rodando: ${pids.join(', ')}`)
    } else {
        success.push('✅ Nenhum processo Electron zumbi')
    }
    
    // ========================================
    // TESTE 6: PORTA 7937
    // ========================================
    console.log(`${YELLOW}[TESTE 6] Verificando porta 7937...${RESET}`)
    
    const checkPort = spawn('lsof', ['-ti:7937'], { shell: true })
    let portInUse = ''
    
    checkPort.stdout.on('data', (data) => {
        portInUse += data.toString()
    })
    
    checkPort.on('close', () => {
        if (portInUse.trim()) {
            warnings.push(`⚠️ Porta 7937 em uso por PID: ${portInUse.trim()}`)
        } else {
            success.push('✅ Porta 7937 livre')
        }
        
        // ========================================
        // TESTE 7: AUTH.JS
        // ========================================
        console.log(`${YELLOW}[TESTE 7] Verificando auth.js...${RESET}`)
        
        try {
            const authContent = fs.readFileSync('app/server/auth.js', 'utf-8')
            
            // Verificar se tem código corrompido
            if (authContent.includes('function Object() { [native code] }')) {
                errors.push('❌ auth.js está corrompido (contém código nativo)')
            } else {
                success.push('✅ auth.js sem corrupção')
            }
            
            // Verificar tipo de import
            if (authContent.includes('import jwt from')) {
                warnings.push('⚠️ auth.js usa ESM import direto (pode falhar)')
            }
            
            if (authContent.includes('createRequire')) {
                success.push('✅ auth.js usa createRequire (compatível)')
            }
            
        } catch (e) {
            errors.push(`❌ Erro ao verificar auth.js: ${e.message}`)
        }
        
        // ========================================
        // RELATÓRIO FINAL
        // ========================================
        console.log(`\n${BLUE}========================================${RESET}`)
        console.log(`${BLUE}           RELATÓRIO FINAL${RESET}`)
        console.log(`${BLUE}========================================${RESET}\n`)
        
        if (success.length > 0) {
            console.log(`${GREEN}SUCESSOS (${success.length}):${RESET}`)
            success.forEach(s => console.log(`  ${s}`))
            console.log()
        }
        
        if (warnings.length > 0) {
            console.log(`${YELLOW}AVISOS (${warnings.length}):${RESET}`)
            warnings.forEach(w => console.log(`  ${w}`))
            console.log()
        }
        
        if (errors.length > 0) {
            console.log(`${RED}ERROS (${errors.length}):${RESET}`)
            errors.forEach(e => console.log(`  ${e}`))
            console.log()
        }
        
        // ========================================
        // RECOMENDAÇÕES
        // ========================================
        console.log(`${BLUE}========================================${RESET}`)
        console.log(`${BLUE}           RECOMENDAÇÕES${RESET}`)
        console.log(`${BLUE}========================================${RESET}\n`)
        
        if (errors.length > 0) {
            console.log(`${RED}⚠️ ERROS CRÍTICOS DETECTADOS!${RESET}\n`)
            console.log('Execute o script de correção:')
            console.log(`${GREEN}bash fix_electron_complete.sh${RESET}\n`)
        } else if (warnings.length > 0) {
            console.log(`${YELLOW}⚠️ Alguns avisos foram detectados.${RESET}\n`)
            console.log('Recomenda-se executar:')
            console.log(`${GREEN}bash fix_electron_complete.sh${RESET}\n`)
        } else {
            console.log(`${GREEN}✅ Sistema aparentemente OK!${RESET}\n`)
            console.log('Você pode iniciar o Electron com:')
            console.log(`${GREEN}npm run dev${RESET}\n`)
        }
        
        // Score final
        const totalTests = success.length + warnings.length + errors.length
        const score = Math.round((success.length / totalTests) * 100)
        
        console.log(`${BLUE}Score de Saúde: ${score}%${RESET}`)
        
        if (score < 50) {
            console.log(`${RED}❌ Sistema em estado crítico${RESET}`)
        } else if (score < 80) {
            console.log(`${YELLOW}⚠️ Sistema precisa de atenção${RESET}`)
        } else {
            console.log(`${GREEN}✅ Sistema saudável${RESET}`)
        }
        
        process.exit(errors.length > 0 ? 1 : 0)
    })
})
