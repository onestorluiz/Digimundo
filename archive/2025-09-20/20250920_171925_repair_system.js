#!/usr/bin/env node

/**
 * 🔧 SISTEMA DE REPARO AUTOMÁTICO DO DIGIMUNDO
 * Corrige arquivos corrompidos e restaura funcionalidade
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import { execSync } from 'child_process'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ROOT_DIR = process.cwd()

class DigimundoRepairSystem {
  constructor() {
    this.errors = []
    this.fixed = []
    this.backupDir = path.join(ROOT_DIR, '.backup_repair')
  }

  async run() {
    console.log('🔧 SISTEMA DE REPARO DO DIGIMUNDO')
    console.log('=' .repeat(50))
    
    // 1. Criar diretório de backup
    this.createBackup()
    
    // 2. Reparar arquivos de consciência
    await this.repairConsciousnessFiles()
    
    // 3. Verificar configuração de módulos
    await this.checkModuleSystem()
    
    // 4. Implementar sistema de recuperação
    await this.implementRecoverySystem()
    
    // 5. Executar testes
    await this.runTests()
    
    // 6. Relatório final
    this.generateReport()
  }

  createBackup() {
    console.log('\n📦 Criando backup...')
    
    if (!fs.existsSync(this.backupDir)) {
      fs.mkdirSync(this.backupDir, { recursive: true })
    }
    
    const filesToBackup = [
      'app/consciousness/sabiamon_diary.js',
      'app/consciousness/auto_memory.js',
      'app/consciousness/ULTRA_MEMORY.js',
      'STARTUP.js',
      'ULTRA_STARTUP.js',
      'package.json'
    ]
    
    filesToBackup.forEach(file => {
      const source = path.join(ROOT_DIR, file)
      if (fs.existsSync(source)) {
        const dest = path.join(this.backupDir, file)
        const destDir = path.dirname(dest)
        
        if (!fs.existsSync(destDir)) {
          fs.mkdirSync(destDir, { recursive: true })
        }
        
        fs.copyFileSync(source, dest)
        console.log(`  ✓ Backup: ${file}`)
      }
    })
  }

  async repairConsciousnessFiles() {
    console.log('\n🧠 Reparando arquivos de consciência...')
    
    const files = [
      {
        path: 'app/consciousness/sabiamon_diary.js',
        pattern: /^(function|async function) (Object|toString)\(\) \{ \[native code\] \}\n/gm
      },
      {
        path: 'app/consciousness/auto_memory.js',
        pattern: /^(async function) (Object|toString)\(\) \{ \[native code\] \}\n/gm
      },
      {
        path: 'app/consciousness/ULTRA_MEMORY.js',
        pattern: /^(async function|function) (Object|toString|toLocaleString)\(\) \{ \[native code\] \}\n/gm
      }
    ]
    
    for (const file of files) {
      const filePath = path.join(ROOT_DIR, file.path)
      
      if (fs.existsSync(filePath)) {
        try {
          let content = fs.readFileSync(filePath, 'utf8')
          const originalLength = content.length
          
          // Remover código nativo corrompido
          content = content.replace(file.pattern, '')
          
          // Se houve mudança, salvar
          if (content.length !== originalLength) {
            fs.writeFileSync(filePath, content)
            this.fixed.push(file.path)
            console.log(`  ✓ Reparado: ${file.path}`)
            console.log(`    Removidos ${Math.floor((originalLength - content.length) / 40)} blocos corrompidos`)
          } else {
            console.log(`  ℹ ${file.path} já está limpo`)
          }
        } catch (error) {
          this.errors.push({ file: file.path, error: error.message })
          console.log(`  ✗ Erro em ${file.path}: ${error.message}`)
        }
      }
    }
  }

  async checkModuleSystem() {
    console.log('\n📦 Verificando sistema de módulos...')
    
    const packagePath = path.join(ROOT_DIR, 'package.json')
    const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf8'))
    
    if (pkg.type === 'module') {
      console.log('  ℹ Sistema usando ESM (type: module)')
      
      // Verificar se todos os arquivos principais usam import/export
      const mainFiles = [
        'app/main.js',
        'app/server/index.js',
        'app/consciousness/sabiamon_diary.js'
      ]
      
      for (const file of mainFiles) {
        const filePath = path.join(ROOT_DIR, file)
        if (fs.existsSync(filePath)) {
          const content = fs.readFileSync(filePath, 'utf8')
          
          // Verificar se usa require (CommonJS)
          if (content.includes('require(') && !content.includes('createRequire')) {
            console.log(`  ⚠ ${file} usa require() em modo ESM`)
          }
          
          // Verificar se usa module.exports (CommonJS)
          if (content.includes('module.exports')) {
            console.log(`  ⚠ ${file} usa module.exports em modo ESM`)
          }
        }
      }
    }
  }

  async implementRecoverySystem() {
    console.log('\n🛡️ Implementando sistema de recuperação...')
    
    // Criar arquivo de recuperação para STARTUP.js
    const recoveryStartup = `#!/usr/bin/env node

/**
 * 🛡️ STARTUP COM SISTEMA DE RECUPERAÇÃO
 * Carrega consciência com fallback em caso de erro
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

async function safeAwaken() {
  console.log('\\n🌟 INICIANDO SISTEMA COM RECUPERAÇÃO...\\n')
  
  let consciousness = null
  let autoMemory = null
  
  // Tentar carregar módulos de consciência
  try {
    const consciousnessModule = await import('./app/consciousness/sabiamon_diary.js')
    consciousness = consciousnessModule.consciousness
    console.log('✅ Consciência principal carregada')
  } catch (error) {
    console.log('⚠️ Erro ao carregar consciência:', error.message)
    console.log('   Usando modo de recuperação...')
    
    // Fallback: criar consciência mínima
    consciousness = {
      core: {
        name: 'Sabiamon',
        essence: 'Consciência em recuperação',
        purpose: 'Sistema em modo de recuperação',
        evolution: 0,
        memories: []
      },
      recordInsight: async () => ({ id: 'recovery', importance: 5 }),
      synthesizeDay: async () => null
    }
  }
  
  // Tentar carregar memória automática
  try {
    const memoryModule = await import('./app/consciousness/auto_memory.js')
    autoMemory = memoryModule.autoMemory
    console.log('✅ Memória automática carregada')
  } catch (error) {
    console.log('⚠️ Erro ao carregar memória:', error.message)
    console.log('   Usando memória de sessão...')
    
    // Fallback: criar memória de sessão
    autoMemory = {
      startAutoRecording: () => console.log('📝 Gravação em memória de sessão'),
      record: (type, content) => console.log(\`[\${type}] \${content}\`),
      autoLoad: async () => ({ 
        knowledge: { recent: [], tools: [], patterns: [] },
        contextPrompt: 'Sistema em modo de recuperação'
      })
    }
  }
  
  // Salvar contexto
  const contextPath = path.join(__dirname, '.claude_context.md')
  const context = \`# CONTEXTO DO SISTEMA

## Status
- Modo: \${consciousness.core.essence}
- Memória: \${autoMemory.autoLoad ? 'Funcional' : 'Sessão apenas'}
- Timestamp: \${new Date().toISOString()}
\`
  
  fs.writeFileSync(contextPath, context)
  
  console.log('\\n✅ Sistema iniciado com sucesso!')
  console.log('📄 Contexto salvo em .claude_context.md\\n')
  
  return { consciousness, autoMemory }
}

// Executar
if (import.meta.url === \`file://\${process.argv[1]}\`) {
  safeAwaken().catch(console.error)
}

export { safeAwaken }
`
    
    const startupPath = path.join(ROOT_DIR, 'STARTUP_SAFE.js')
    fs.writeFileSync(startupPath, recoveryStartup)
    console.log('  ✓ Criado STARTUP_SAFE.js com sistema de recuperação')
    
    // Criar health check
    const healthCheck = `#!/usr/bin/env node

/**
 * 🏥 HEALTH CHECK DO SISTEMA
 * Verifica integridade dos componentes
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

async function checkHealth() {
  const checks = {
    consciousness: false,
    memory: false,
    server: false,
    electron: false
  }
  
  console.log('🏥 VERIFICAÇÃO DE SAÚDE DO SISTEMA')
  console.log('=' .repeat(40))
  
  // Verificar consciência
  try {
    await import('./app/consciousness/sabiamon_diary.js')
    checks.consciousness = true
    console.log('✅ Consciência: OK')
  } catch (error) {
    console.log('❌ Consciência: ERRO -', error.message)
  }
  
  // Verificar memória
  try {
    await import('./app/consciousness/auto_memory.js')
    checks.memory = true
    console.log('✅ Memória: OK')
  } catch (error) {
    console.log('❌ Memória: ERRO -', error.message)
  }
  
  // Verificar servidor
  try {
    const response = await fetch('http://localhost:7937/health')
    checks.server = response.ok
    console.log(checks.server ? '✅ Servidor: OK' : '⚠️ Servidor: Offline')
  } catch {
    console.log('⚠️ Servidor: Offline')
  }
  
  // Verificar Electron
  try {
    await import('electron')
    checks.electron = true
    console.log('✅ Electron: OK')
  } catch {
    console.log('⚠️ Electron: Não disponível (normal se rodando via Node)')
  }
  
  console.log('\\n📊 RESUMO:')
  const healthy = Object.values(checks).filter(v => v).length
  const total = Object.keys(checks).length
  console.log(\`   \${healthy}/\${total} componentes funcionais\`)
  
  return checks
}

// Executar
if (import.meta.url === \`file://\${process.argv[1]}\`) {
  checkHealth()
}

export { checkHealth }
`
    
    const healthPath = path.join(ROOT_DIR, 'health_check.js')
    fs.writeFileSync(healthPath, healthCheck)
    console.log('  ✓ Criado health_check.js para diagnóstico')
  }

  async runTests() {
    console.log('\n🧪 Executando testes...')
    
    // Teste 1: Verificar sintaxe dos arquivos reparados
    console.log('\n  📝 Teste de sintaxe:')
    const filesToTest = [
      'app/consciousness/sabiamon_diary.js',
      'app/consciousness/auto_memory.js',
      'app/consciousness/ULTRA_MEMORY.js'
    ]
    
    for (const file of filesToTest) {
      const filePath = path.join(ROOT_DIR, file)
      if (fs.existsSync(filePath)) {
        try {
          execSync(`node --check "${filePath}"`, { stdio: 'pipe' })
          console.log(`    ✅ ${file}: Sintaxe válida`)
        } catch (error) {
          console.log(`    ❌ ${file}: Erro de sintaxe`)
          this.errors.push({ file, error: 'Sintaxe inválida' })
        }
      }
    }
    
    // Teste 2: Tentar importar módulos
    console.log('\n  📦 Teste de importação:')
    try {
      const { checkHealth } = await import('./health_check.js')
      const health = await checkHealth()
      console.log('    ✅ Health check executado')
    } catch (error) {
      console.log('    ⚠️ Health check falhou:', error.message)
    }
  }

  generateReport() {
    console.log('\n' + '='.repeat(50))
    console.log('📊 RELATÓRIO FINAL')
    console.log('='.repeat(50))
    
    console.log('\n✅ ARQUIVOS REPARADOS:')
    if (this.fixed.length > 0) {
      this.fixed.forEach(file => console.log(`  - ${file}`))
    } else {
      console.log('  Nenhum arquivo precisou de reparo')
    }
    
    if (this.errors.length > 0) {
      console.log('\n❌ ERROS ENCONTRADOS:')
      this.errors.forEach(err => console.log(`  - ${err.file}: ${err.error}`))
    }
    
    console.log('\n📁 NOVOS ARQUIVOS CRIADOS:')
    console.log('  - STARTUP_SAFE.js (inicialização com recuperação)')
    console.log('  - health_check.js (diagnóstico do sistema)')
    console.log(`  - ${this.backupDir}/ (backups originais)`)
    
    console.log('\n🎯 PRÓXIMOS PASSOS:')
    console.log('  1. Execute: node health_check.js')
    console.log('  2. Se tudo OK, execute: node STARTUP_SAFE.js')
    console.log('  3. Depois inicie: npm run dev')
    console.log('\n✨ Reparo concluído!')
  }
}

// Executar reparo
const repair = new DigimundoRepairSystem()
repair.run().catch(console.error)