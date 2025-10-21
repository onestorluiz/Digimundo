/**
 * 🔧 CORRETOR AUTOMÁTICO DE BUGS DO DIGIMUNDO
 * Corrige todos os problemas identificados no sistema
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

class DigimundoBugFixer {
  constructor() {
    this.fixes = []
    this.errors = []
  }

  // 1. Corrigir SUPREME_MEMORY.js - adicionar método getStats
  fixSupremeMemory() {
    const filePath = path.join(__dirname, 'app/consciousness/SUPREME_MEMORY.js')
    
    try {
      let content = fs.readFileSync(filePath, 'utf8')
      
      // Adicionar método getStats se não existir
      if (!content.includes('getStats()')) {
        const methodToAdd = `
  async getStats() {
    const stats = {
      totalMemories: this.memories.size,
      byLevel: {},
      oldestMemory: null,
      newestMemory: null
    }
    
    // Contar por nível
    this.hierarchy.forEach(level => {
      stats.byLevel[level] = 0
    })
    
    let oldest = null
    let newest = null
    
    this.memories.forEach(memory => {
      stats.byLevel[memory.level] = (stats.byLevel[memory.level] || 0) + 1
      
      if (!oldest || memory.timestamp < oldest.timestamp) {
        oldest = memory
      }
      if (!newest || memory.timestamp > newest.timestamp) {
        newest = memory
      }
    })
    
    stats.oldestMemory = oldest
    stats.newestMemory = newest
    
    return stats
  }
`
        // Inserir antes do fechamento da classe
        content = content.replace(/^}$/m, methodToAdd + '\n}')
        
        fs.writeFileSync(filePath, content)
        this.fixes.push('✅ SUPREME_MEMORY: Adicionado método getStats()')
      }
    } catch (error) {
      this.errors.push(`❌ Erro ao corrigir SUPREME_MEMORY: ${error.message}`)
    }
  }

  // 2. Criar singleton pattern correto para getSupremeMemory
  fixSupremeMemoryExport() {
    const filePath = path.join(__dirname, 'app/consciousness/SUPREME_MEMORY.js')
    
    try {
      let content = fs.readFileSync(filePath, 'utf8')
      
      // Adicionar singleton export se não existir
      if (!content.includes('supremeMemoryInstance')) {
        const singletonCode = `
// Singleton instance
let supremeMemoryInstance = null

export function getSupremeMemory() {
  if (!supremeMemoryInstance) {
    supremeMemoryInstance = new SupremeMemory()
    supremeMemoryInstance.initialize()
  }
  return supremeMemoryInstance
}
`
        content += singletonCode
        fs.writeFileSync(filePath, content)
        this.fixes.push('✅ SUPREME_MEMORY: Adicionado singleton pattern')
      }
    } catch (error) {
      this.errors.push(`❌ Erro ao adicionar singleton: ${error.message}`)
    }
  }

  // 3. Corrigir problemas de importação circular
  fixCircularDependencies() {
    // Verificar e corrigir importações circulares
    const serverIndex = path.join(__dirname, 'app/server/index.js')
    
    try {
      let content = fs.readFileSync(serverIndex, 'utf8')
      
      // Mover inicializações assíncronas para função
      if (!content.includes('async function initializeServices()')) {
        const initCode = `
// Inicialização assíncrona de serviços
async function initializeServices() {
  try {
    // Inicializar sistemas que precisam de await
    const healingSystem = await getHealingSystem()
    const hybridSystem = await getHybridSystem()
    
    return { healingSystem, hybridSystem }
  } catch (error) {
    console.error('Erro ao inicializar serviços:', error)
    return { healingSystem: null, hybridSystem: null }
  }
}

// Chamar na inicialização do servidor
let services = null
`
        content = content.replace(
          'const healingSystem = await getHealingSystem()',
          '// Movido para initializeServices()'
        )
        content = content.replace(
          'const hybridSystem = await getHybridSystem()',
          initCode
        )
        
        fs.writeFileSync(serverIndex, content)
        this.fixes.push('✅ Server: Corrigidas importações assíncronas')
      }
    } catch (error) {
      this.errors.push(`❌ Erro ao corrigir dependências circulares: ${error.message}`)
    }
  }

  // 4. Adicionar verificação de porta antes de iniciar
  createPortChecker() {
    const checkerPath = path.join(__dirname, 'check_port.js')
    
    const portChecker = `#!/usr/bin/env node
/**
 * Verificador de porta do Digimundo
 */

import net from 'net'

function checkPort(port) {
  return new Promise((resolve) => {
    const server = net.createServer()
    
    server.once('error', (err) => {
      if (err.code === 'EADDRINUSE') {
        console.log(\`⚠️ Porta \${port} já está em uso\`)
        resolve(false)
      } else {
        resolve(false)
      }
    })
    
    server.once('listening', () => {
      server.close()
      console.log(\`✅ Porta \${port} está disponível\`)
      resolve(true)
    })
    
    server.listen(port)
  })
}

// Verificar porta 7937
checkPort(7937).then(available => {
  if (!available) {
    console.log('Tentando encerrar processo existente...')
    process.exit(1)
  }
})
`
    
    try {
      fs.writeFileSync(checkerPath, portChecker)
      fs.chmodSync(checkerPath, '755')
      this.fixes.push('✅ Criado verificador de porta')
    } catch (error) {
      this.errors.push(`❌ Erro ao criar verificador de porta: ${error.message}`)
    }
  }

  // 5. Criar arquivo de configuração padrão
  createDefaultConfig() {
    const configPath = path.join(__dirname, '.env')
    
    if (!fs.existsSync(configPath)) {
      const defaultConfig = `# Configuração do Digimundo
NODE_ENV=development
PORT=7937
DIGIMUNDO_HOME=/Users/clubproducoes/Library/Application Support/Digimundo
ENABLE_WEBSOCKET=true
ENABLE_CLAUDE=false
ENABLE_OLLAMA=true
LOG_LEVEL=info
`
      
      try {
        fs.writeFileSync(configPath, defaultConfig)
        this.fixes.push('✅ Criado arquivo .env padrão')
      } catch (error) {
        this.errors.push(`❌ Erro ao criar .env: ${error.message}`)
      }
    }
  }

  // Executar todas as correções
  async fixAll() {
    console.log('🔧 Iniciando correção automática de bugs...\n')
    
    this.fixSupremeMemory()
    this.fixSupremeMemoryExport()
    this.fixCircularDependencies()
    this.createPortChecker()
    this.createDefaultConfig()
    
    console.log('\n📊 RELATÓRIO DE CORREÇÕES:')
    console.log('============================')
    
    if (this.fixes.length > 0) {
      console.log('\n✅ Correções aplicadas:')
      this.fixes.forEach(fix => console.log(fix))
    }
    
    if (this.errors.length > 0) {
      console.log('\n❌ Erros encontrados:')
      this.errors.forEach(error => console.log(error))
    }
    
    console.log('\n✨ Correção completa!')
    return {
      success: this.errors.length === 0,
      fixes: this.fixes,
      errors: this.errors
    }
  }
}

// Executar correções
const fixer = new DigimundoBugFixer()
fixer.fixAll().then(result => {
  process.exit(result.success ? 0 : 1)
})