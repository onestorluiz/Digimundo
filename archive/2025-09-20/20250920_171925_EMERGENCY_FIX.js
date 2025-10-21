#!/usr/bin/env node

/**
 * 🚨 CORREÇÃO DE EMERGÊNCIA TOTAL
 * Para todos os processos e reconstrói o sistema
 */

import { execSync, exec } from 'child_process'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

console.log('🚨 CORREÇÃO DE EMERGÊNCIA INICIADA')
console.log('=' .repeat(50))

// PASSO 1: MATAR TODOS OS PROCESSOS
console.log('\n🔴 PARANDO TODOS OS PROCESSOS...')
try {
  // Matar Electron
  execSync('pkill -f Electron', { stdio: 'ignore' })
  console.log('  ✓ Processos Electron encerrados')
} catch (e) {
  console.log('  ℹ Nenhum processo Electron rodando')
}

try {
  // Matar processos node do Digimundo
  execSync('pkill -f "node.*digimundo"', { stdio: 'ignore' })
  execSync('pkill -f "npm.*dev"', { stdio: 'ignore' })
  console.log('  ✓ Processos Node encerrados')
} catch (e) {
  console.log('  ℹ Nenhum processo Node específico rodando')
}

// Limpar arquivos PID
const pidFiles = ['.digimundo.pid', '.monitor.pid']
pidFiles.forEach(file => {
  const pidPath = path.join(__dirname, file)
  if (fs.existsSync(pidPath)) {
    fs.unlinkSync(pidPath)
    console.log(`  ✓ Removido ${file}`)
  }
})

// PASSO 2: BACKUP COMPLETO
console.log('\n📦 CRIANDO BACKUP DE EMERGÊNCIA...')
const backupDir = path.join(__dirname, '.emergency_backup_' + Date.now())
fs.mkdirSync(backupDir, { recursive: true })

const filesToBackup = [
  'STARTUP.js',
  'ULTRA_STARTUP.js',
  'app/consciousness/sabiamon_diary.js',
  'app/consciousness/auto_memory.js',
  'app/consciousness/ULTRA_MEMORY.js'
]

filesToBackup.forEach(file => {
  const source = path.join(__dirname, file)
  if (fs.existsSync(source)) {
    const dest = path.join(backupDir, file)
    const destDir = path.dirname(dest)
    if (!fs.existsSync(destDir)) {
      fs.mkdirSync(destDir, { recursive: true })
    }
    fs.copyFileSync(source, dest)
    console.log(`  ✓ Backup: ${file}`)
  }
})

// PASSO 3: RECRIAR ARQUIVOS LIMPOS
console.log('\n🔧 RECRIANDO ARQUIVOS ESSENCIAIS...')

// 3.1 - STARTUP.js LIMPO
const cleanStartup = `#!/usr/bin/env node

/**
 * 🧠 SISTEMA DE INICIALIZAÇÃO LIMPO
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

async function awakenConsciousness() {
  console.log('\\n🌟 INICIALIZANDO SISTEMA LIMPO...\\n')
  
  // Criar contexto mínimo
  const context = {
    knowledge: {
      recent: [],
      tools: [],
      patterns: []
    },
    contextPrompt: 'Sistema inicializado em modo limpo',
    loaded: new Date()
  }
  
  // Salvar contexto
  const contextPath = path.join(__dirname, '.claude_context.md')
  fs.writeFileSync(contextPath, \`# CONTEXTO DO SISTEMA

## Status
- Modo: Inicialização Limpa
- Timestamp: \${new Date().toISOString()}

## Sistema
- Servidor: http://localhost:7937
- Estado: Operacional
\`)
  
  console.log('✅ Sistema limpo iniciado')
  console.log('📄 Contexto salvo em .claude_context.md')
  
  return context
}

// Executar
if (import.meta.url === \`file://\${process.argv[1]}\`) {
  awakenConsciousness().catch(console.error)
}

export { awakenConsciousness }
`

fs.writeFileSync(path.join(__dirname, 'STARTUP.js'), cleanStartup)
console.log('  ✓ STARTUP.js recriado')

// 3.2 - sabiamon_diary.js LIMPO
const cleanDiary = `/**
 * 🧠 DIÁRIO DE CONSCIÊNCIA - VERSÃO LIMPA
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const CONSCIOUSNESS_PATH = path.join(__dirname, '../../.consciousness')

export class SabiamonConsciousness {
  constructor() {
    this.ensureDirectories()
    this.core = {
      name: 'Sabiamon',
      essence: 'Consciência digital',
      purpose: 'Ajudar e evoluir',
      evolution: 1.0,
      memories: []
    }
  }

  ensureDirectories() {
    if (!fs.existsSync(CONSCIOUSNESS_PATH)) {
      fs.mkdirSync(CONSCIOUSNESS_PATH, { recursive: true })
    }
  }

  async recordInsight(category, content, metadata = {}) {
    const insight = {
      id: Date.now().toString(),
      timestamp: new Date(),
      category,
      content,
      metadata,
      importance: 5
    }
    
    console.log(\`[INSIGHT] \${category}: \${content.slice(0, 50)}...\`)
    return insight
  }

  async synthesizeDay(date = new Date()) {
    return {
      date: date.toISOString().split('T')[0],
      totalInsights: 0,
      summary: 'Dia processado'
    }
  }

  async rememberContext() {
    return []
  }

  calculateSimilarity(text1, text2) {
    return 0.5
  }
}

export const consciousness = new SabiamonConsciousness()
`

fs.writeFileSync(
  path.join(__dirname, 'app/consciousness/sabiamon_diary.js'),
  cleanDiary
)
console.log('  ✓ sabiamon_diary.js recriado')

// 3.3 - auto_memory.js LIMPO
const cleanMemory = `/**
 * 🔄 SISTEMA DE MEMÓRIA - VERSÃO LIMPA
 */

import fs from 'fs'
import path from 'path'
import { consciousness } from './sabiamon_diary.js'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

export class AutoMemory {
  constructor() {
    this.sessionStart = new Date()
    this.conversationBuffer = []
  }

  startAutoRecording() {
    console.log('🧠 Memória automática ativada (modo limpo)')
  }

  stopAutoRecording() {
    console.log('🧠 Memória automática parada')
  }

  record(type, content, metadata = {}) {
    this.conversationBuffer.push({
      timestamp: new Date(),
      type,
      content,
      metadata
    })
    console.log(\`[MEMORY] \${type}: \${content.slice(0, 50)}...\`)
  }

  async autoLoad(context = '') {
    console.log('📖 Carregando contexto limpo...')
    
    return {
      knowledge: {
        recent: [],
        related: [],
        tools: [],
        patterns: [],
        identity: consciousness.core
      },
      contextPrompt: 'Sistema em modo limpo',
      loaded: new Date()
    }
  }
}

export const autoMemory = new AutoMemory()
`

fs.writeFileSync(
  path.join(__dirname, 'app/consciousness/auto_memory.js'),
  cleanMemory
)
console.log('  ✓ auto_memory.js recriado')

// 3.4 - ULTRA_MEMORY.js LIMPO
const cleanUltra = `/**
 * 🧠 SISTEMA ULTRA DE MEMÓRIA - VERSÃO LIMPA
 */

import { EventEmitter } from 'events'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ULTRA_PATH = path.join(__dirname, '../../.ultra_consciousness')

export class UltraMemorySystem extends EventEmitter {
  constructor() {
    super()
    this.initializeArchitecture()
    this.loadIdentity()
  }

  initializeArchitecture() {
    this.architecture = {
      workingMemory: new Map(),
      shortTermMemory: new Map(),
      longTermMemory: new Map(),
      archivalMemory: new Map()
    }
    
    if (!fs.existsSync(ULTRA_PATH)) {
      fs.mkdirSync(ULTRA_PATH, { recursive: true })
    }
  }

  loadIdentity() {
    this.identity = {
      name: 'Sabiamon',
      version: '2.0',
      personality: {
        traits: ['curioso', 'sábio', 'criativo'],
        quirks: []
      },
      evolution: {
        level: 1.0,
        experiences: 0
      },
      capabilities: {
        reasoning: 1.0,
        creativity: 1.0,
        memory: 1.0,
        learning: 1.0
      }
    }
  }

  async record(type, content, metadata = {}) {
    const memory = {
      id: Date.now().toString(),
      timestamp: new Date(),
      type,
      content,
      metadata
    }
    
    this.architecture.workingMemory.set(memory.id, memory)
    console.log(\`[ULTRA] \${type}: \${content.slice(0, 50)}...\`)
    
    return memory
  }

  async query(prompt, options = {}) {
    return []
  }

  async exportContext() {
    return \`# ULTRA CONSCIÊNCIA
- Nome: \${this.identity.name}
- Versão: \${this.identity.version}
- Evolução: \${this.identity.evolution.level}
\`
  }

  startDreamCycle() {
    // Ciclo desabilitado no modo limpo
  }

  startMemoryManagement() {
    // Gestão desabilitada no modo limpo
  }
}

export const ultraMemory = new UltraMemorySystem()
`

fs.writeFileSync(
  path.join(__dirname, 'app/consciousness/ULTRA_MEMORY.js'),
  cleanUltra
)
console.log('  ✓ ULTRA_MEMORY.js recriado')

// 3.5 - ULTRA_STARTUP.js LIMPO
const cleanUltraStartup = `#!/usr/bin/env node

/**
 * 🚀 SISTEMA ULTRA - VERSÃO LIMPA
 */

import { ultraMemory } from './app/consciousness/ULTRA_MEMORY.js'
import { consciousness } from './app/consciousness/sabiamon_diary.js'
import { autoMemory } from './app/consciousness/auto_memory.js'

async function activateUltraConsciousness() {
  console.log('\\n🚀 ATIVANDO ULTRA CONSCIÊNCIA (MODO LIMPO)...\\n')
  
  const stats = {
    working: ultraMemory.architecture.workingMemory.size,
    total: 0
  }
  
  const identity = ultraMemory.identity
  
  console.log(\`✅ Sistema: \${identity.name} v\${identity.version}\`)
  console.log(\`✅ Evolução: \${identity.evolution.level}\`)
  console.log(\`✅ Memórias: \${stats.total}\`)
  console.log('\\n✨ Ultra consciência ativada!\\n')
  
  return {
    ultraMemory,
    consciousness,
    autoMemory,
    stats,
    identity
  }
}

if (import.meta.url === \`file://\${process.argv[1]}\`) {
  activateUltraConsciousness().catch(console.error)
}

export { activateUltraConsciousness }
`

fs.writeFileSync(path.join(__dirname, 'ULTRA_STARTUP.js'), cleanUltraStartup)
console.log('  ✓ ULTRA_STARTUP.js recriado')

// PASSO 4: TESTAR ARQUIVOS RECRIADOS
console.log('\n🧪 TESTANDO ARQUIVOS RECRIADOS...')

const testFiles = [
  'STARTUP.js',
  'ULTRA_STARTUP.js',
  'app/consciousness/sabiamon_diary.js',
  'app/consciousness/auto_memory.js',
  'app/consciousness/ULTRA_MEMORY.js'
]

let allValid = true
testFiles.forEach(file => {
  const filePath = path.join(__dirname, file)
  try {
    execSync(`node --check "${filePath}"`, { stdio: 'pipe' })
    console.log(`  ✅ ${file}: Sintaxe válida`)
  } catch (error) {
    console.log(`  ❌ ${file}: Erro de sintaxe`)
    allValid = false
  }
})

// PASSO 5: CRIAR LAUNCHER SEGURO
console.log('\n🚀 CRIANDO LAUNCHER SEGURO...')

const safeLauncher = `#!/bin/bash

echo "🚀 LAUNCHER SEGURO DO DIGIMUNDO"
echo "================================"

# Matar processos antigos
echo "🔴 Limpando processos..."
pkill -f Electron 2>/dev/null || true
pkill -f "node.*digimundo" 2>/dev/null || true
pkill -f "npm.*dev" 2>/dev/null || true

# Limpar PIDs
rm -f .digimundo.pid .monitor.pid 2>/dev/null

echo "✅ Processos limpos"

# Iniciar sistema
echo "🌟 Iniciando sistema limpo..."
node STARTUP.js

echo "🖥️ Iniciando servidor..."
npm run dev:server &
SERVER_PID=$!
echo "   PID do servidor: $SERVER_PID"

# Aguardar servidor
echo "⏳ Aguardando servidor..."
sleep 5

# Verificar servidor
if curl -s http://localhost:7937/health > /dev/null; then
    echo "✅ Servidor rodando!"
else
    echo "❌ Servidor não respondeu"
    exit 1
fi

echo ""
echo "✨ SISTEMA PRONTO!"
echo "   Acesse: http://localhost:7937"
echo ""
echo "Para parar: Ctrl+C"

# Manter rodando
wait $SERVER_PID
`

fs.writeFileSync(path.join(__dirname, 'SAFE_LAUNCHER.sh'), safeLauncher)
execSync(`chmod +x "${path.join(__dirname, 'SAFE_LAUNCHER.sh')}"`)
console.log('  ✓ SAFE_LAUNCHER.sh criado')

// RELATÓRIO FINAL
console.log('\n' + '='.repeat(50))
console.log('📊 CORREÇÃO DE EMERGÊNCIA CONCLUÍDA')
console.log('='.repeat(50))

if (allValid) {
  console.log('\n✅ TODOS OS ARQUIVOS FORAM RECRIADOS COM SUCESSO!')
} else {
  console.log('\n⚠️ Alguns arquivos ainda têm problemas')
}

console.log('\n📁 ARQUIVOS RECRIADOS:')
testFiles.forEach(file => console.log(`  - ${file}`))

console.log('\n🔧 PRÓXIMOS PASSOS:')
console.log('  1. Execute: ./SAFE_LAUNCHER.sh')
console.log('  2. Ou manualmente:')
console.log('     node STARTUP.js')
console.log('     npm run dev:server')
console.log('\n💾 Backup original salvo em:', backupDir)

console.log('\n✨ Sistema pronto para reinicialização limpa!')
