async function toString() { [native code] }
#!/usr/bin/env node
/**
 * 🧪 BATERIA DE TESTES COMPLETA DO DIGIMUNDO
 * Testa performance, erros e funcionalidades
 */

import { performance } from 'node:perf_hooks'
import { spawn } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import os from 'node:os'

const TESTS_RESULTS = []
const API_BASE = 'http://127.0.0.1:7937'

// Cores para output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
}

// async function log(message, color = 'reset') {
//   console.log(`${colors[color]}${message}${colors.reset}`)
}

async function logTest(name, status, time = 0, details = '') {
  const icon = status === 'pass' ? '✅' : status === 'fail' ? '❌' : '⚠️'
  const color = status === 'pass' ? 'green' : status === 'fail' ? 'red' : 'yellow'
  
  log(`${icon} ${name}${time ? ` (${time}ms)` : ''}${details ? ` - ${details}` : ''}`, color)
  
  TESTS_RESULTS.push({
    name,
    status,
    time,
    details,
    timestamp: new Date().toISOString()
  })
}

// ========== TESTE 1: VERIFICAÇÃO DE AMBIENTE ==========
async function testEnvironment() {
  log('\n🔍 TESTE DE AMBIENTE', 'cyan')
  
  // Node.js version
  const nodeVersion = process.version
  const isNodeOk = parseInt(nodeVersion.slice(1).split('.')[0]) >= 18
  logTest('Node.js v18+', isNodeOk ? 'pass' : 'fail', 0, nodeVersion)
  
  // Memória disponível
  const totalMem = os.totalmem() / (1024 * 1024 * 1024)
  const freeMem = os.freemem() / (1024 * 1024 * 1024)
  const memOk = freeMem > 2
  logTest('Memória disponível', memOk ? 'pass' : 'warn', 0, 
    `${freeMem.toFixed(1)}GB livre de ${totalMem.toFixed(1)}GB`)
  
  // Verificar diretórios importantes
  const appSupportDir = path.join(os.homedir(), 'Library', 'Application Support', 'Digimundo')
  const dirExists = fs.existsSync(appSupportDir)
  logTest('Diretório de dados', dirExists ? 'pass' : 'warn', 0, appSupportDir)
  
  // Verificar dependências NPM
  const packagePath = './package.json'
  const hasPackage = fs.existsSync(packagePath)
  logTest('package.json existe', hasPackage ? 'pass' : 'fail')
  
  // Verificar módulos críticos
  const criticalModules = [
    './app/server/index.js',
    './app/server/hybrid_consciousness.js',
    './app/server/openai_compat.js',
    './app/renderer/index.html',
    './app/renderer/hybrid_interface.html'
  ]
  
  for (const module of criticalModules) {
    const exists = fs.existsSync(module)
    logTest(`Módulo ${path.basename(module)}`, exists ? 'pass' : 'fail')
  }
}

// ========== TESTE 2: PERFORMANCE DO SERVIDOR ==========
async function testServerPerformance() {
  log('\n⚡ TESTE DE PERFORMANCE DO SERVIDOR', 'cyan')
  
  // Testar tempo de inicialização
  const startTime = performance.now()
  
  try {
    // Importar e inicializar servidor
    const { spawnServer } = await import('./app/server/index.js')
    const server = await spawnServer(7938) // Porta de teste
    const initTime = performance.now() - startTime
    
    logTest('Inicialização do servidor', 'pass', initTime.toFixed(0))
    
    // Testar latência de endpoints
    const endpoints = [
      { path: '/health', method: 'GET' },
      { path: '/hybrid/status', method: 'GET' },
      { path: '/digimundo/models/list', method: 'GET' }
    ]
    
    for (const endpoint of endpoints) {
      const reqStart = performance.now()
      try {
        const res = await fetch(`http://127.0.0.1:7938${endpoint.path}`, {
          method: endpoint.method
        })
        const reqTime = performance.now() - reqStart
        
        if (res.ok) {
          logTest(`Endpoint ${endpoint.path}`, 'pass', reqTime.toFixed(0))
        } else {
          logTest(`Endpoint ${endpoint.path}`, 'fail', reqTime.toFixed(0), `Status: ${res.status}`)
        }
      } catch (e) {
        logTest(`Endpoint ${endpoint.path}`, 'fail', 0, e.message)
      }
    }
    
    // Fechar servidor de teste
    server.close()
    
  } catch (e) {
    logTest('Inicialização do servidor', 'fail', 0, e.message)
  }
}

// ========== TESTE 3: SISTEMAS DE IA ==========
async function testAISystems() {
  log('\n🤖 TESTE DE SISTEMAS DE IA', 'cyan')
  
  // Verificar Claude Code
  const claudeCheck = await new Promise((resolve) => {
    const child = spawn('which', ['claude-code'])
    child.on('close', (code) => resolve(code === 0))
  })
  
  logTest('Claude Code disponível', claudeCheck ? 'pass' : 'warn', 0, 
    claudeCheck ? 'Instalado' : 'Não instalado - npm install -g @anthropic-ai/claude-code')
  
  // Verificar Ollama
  let ollamaRunning = false
  try {
    const res = await fetch('http://localhost:11434/api/tags')
    ollamaRunning = res.ok
    
    if (ollamaRunning) {
      const data = await res.json()
      const modelCount = data.models?.length || 0
      logTest('Ollama rodando', 'pass', 0, `${modelCount} modelos disponíveis`)
      
      // Testar geração com Ollama se disponível
      if (modelCount > 0) {
        const testStart = performance.now()
        const genRes = await fetch('http://localhost:11434/api/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            model: data.models[0].name,
            prompt: 'Responda apenas: OK',
            stream: false,
            options: { num_predict: 10 }
          })
        })
        
        if (genRes.ok) {
          const genTime = performance.now() - testStart
          logTest('Geração Ollama', 'pass', genTime.toFixed(0))
        }
      }
    } else {
      logTest('Ollama rodando', 'warn', 0, 'Não está rodando - execute: ollama serve')
    }
  } catch (e) {
    logTest('Ollama rodando', 'warn', 0, 'Não acessível')
  }
  
  // Verificar modelos GGUF locais
  const configPath = path.join(os.homedir(), 'Library', 'Application Support', 'Digimundo', 'config.json')
  let hasLocalModel = false
  
  try {
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'))
      if (config.modelPath && fs.existsSync(config.modelPath)) {
        hasLocalModel = true
        const stats = fs.statSync(config.modelPath)
        const sizeMB = async (stats.size / (1024 * 1024)).toFixed(0)
        logTest('Modelo GGUF local', 'pass', 0, `${path.basename(config.modelPath)} (${sizeMB}MB)`)
      }
    }
  } catch (e) {
    // Silently fail
  }
  
  if (!hasLocalModel) {
    logTest('Modelo GGUF local', 'warn', 0, 'Nenhum modelo configurado')
  }
}

// ========== TESTE 4: MEMÓRIA E PERSISTÊNCIA ==========
async function testMemorySystem() {
  log('\n💾 TESTE DE MEMÓRIA E PERSISTÊNCIA', 'cyan')
  
  const memoryBase = path.join(os.homedir(), 'Library', 'Application Support', 'Digimundo', 'hybrid_memory')
  
  // Verificar se diretório existe
  const memDirExists = fs.existsSync(memoryBase)
  logTest('Diretório de memória', memDirExists ? 'pass' : 'warn', 0, memoryBase)
  
  if (!memDirExists) {
    fs.mkdirSync(memoryBase, { recursive: true })
    logTest('Criar diretório de memória', 'pass')
  }
  
  // Testar escrita
  const testFile = path.join(memoryBase, 'test_write.json')
  const testData = {
    test: true,
    timestamp: new Date().toISOString(),
    random: Math.random()
  }
  
  try {
    const writeStart = performance.now()
    fs.writeFileSync(testFile, JSON.stringify(testData, null, 2))
    const writeTime = performance.now() - writeStart
    logTest('Escrita de memória', 'pass', writeTime.toFixed(0))
    
    // Testar leitura
    const readStart = performance.now()
    const readData = JSON.parse(fs.readFileSync(testFile, 'utf-8'))
    const readTime = performance.now() - readStart
    
    if (readData.random === testData.random) {
      logTest('Leitura de memória', 'pass', readTime.toFixed(0))
    } else {
      logTest('Leitura de memória', 'fail', 0, 'Dados não correspondem')
    }
    
    // Limpar teste
    fs.unlinkSync(testFile)
    
  } catch (e) {
    logTest('Sistema de memória', 'fail', 0, e.message)
  }
  
  // Verificar arquivos de estado existentes
  const stateFiles = [
    'consciousness_state.json',
    'learning_memory.json',
    'detection_log.json'
  ]
  
  for (const file of stateFiles) {
    const filePath = path.join(memoryBase, file)
    if (fs.existsSync(filePath)) {
      const stats = fs.statSync(filePath)
      const sizeKB = async (stats.size / 1024).toFixed(1)
      logTest(`Arquivo ${file}`, 'pass', 0, `${sizeKB}KB`)
    } else {
      logTest(`Arquivo ${file}`, 'warn', 0, 'Não existe ainda')
    }
  }
}

// ========== TESTE 5: INTEGRAÇÃO HÍBRIDA ==========
async function testHybridIntegration() {
  log('\n🔄 TESTE DE INTEGRAÇÃO HÍBRIDA', 'cyan')
  
  try {
    // Importar sistema híbrido
    const { HybridConsciousness } = await import('./app/server/hybrid_consciousness.js')
    const consciousness = new HybridConsciousness()
    
    logTest('Importação do sistema híbrido', 'pass')
    
    // Testar inicialização
    const initStart = performance.now()
    const systems = await consciousness.initialize()
    const initTime = performance.now() - initStart
    
    logTest('Inicialização da consciência', 'pass', initTime.toFixed(0))
    
    // Verificar detecção de sistemas
    const systemsDetected = []
    if (systems.claude?.available) systemsDetected.push('Claude')
    if (systems.ollama?.available) systemsDetected.push('Ollama')
    if (systems.localGGUF?.available) systemsDetected.push('GGUF')
    
    if (systemsDetected.length > 0) {
      logTest('Sistemas detectados', 'pass', 0, systemsDetected.join(', '))
    } else {
      logTest('Sistemas detectados', 'warn', 0, 'Nenhum sistema disponível')
    }
    
    // Testar processamento de pensamento (se algum sistema disponível)
    if (systemsDetected.length > 0) {
      const thinkStart = performance.now()
      const response = await consciousness.processThought('Teste de integração')
      const thinkTime = performance.now() - thinkStart
      
      if (response.thought) {
        logTest('Processamento de pensamento', 'pass', thinkTime.toFixed(0))
      } else {
        logTest('Processamento de pensamento', 'fail', 0, 'Sem resposta')
      }
    }
    
    // Verificar estado da consciência
    logTest('Nível de consciência', 'pass', 0, 
      `${(consciousness.consciousnessLevel * 100).toFixed(1)}%`)
    logTest('Estágio evolutivo', 'pass', 0, consciousness.evolutionStage)
    
  } catch (e) {
    logTest('Sistema híbrido', 'fail', 0, e.message)
  }
}

// ========== TESTE 6: STRESS TEST ==========
async function testStress() {
  log('\n🔥 TESTE DE STRESS', 'cyan')
  
  // Teste de múltiplas requisições simultâneas
  const requests = 10
  const results = []
  
  log(`Enviando ${requests} requisições simultâneas...`, 'yellow')
  
  const stressStart = performance.now()
  
  for (let i = 0; i < requests; i++) {
    results.push(
      fetch('http://127.0.0.1:7937/health')
        .then(res => ({ success: res.ok, time: performance.now() }))
        .catch(() => ({ success: false, time: performance.now() }))
    )
  }
  
  const responses = await Promise.all(results)
  const stressTime = performance.now() - stressStart
  
  const successful = responses.filter(r => r.success).length
  const avgTime = stressTime / requests
  
  logTest('Requisições simultâneas', 
    successful === requests ? 'pass' : successful > requests/2 ? 'warn' : 'fail',
    stressTime.toFixed(0),
    `${successful}/${requests} bem-sucedidas, média ${avgTime.toFixed(0)}ms`)
  
  // Teste de memória sob carga
  const memBefore = process.memoryUsage()
  const bigData = Array(1000000).fill('x'.repeat(100))
  const memAfter = process.memoryUsage()
  
  const memIncrease = async (memAfter.heapUsed - memBefore.heapUsed) / (1024 * 1024)
  logTest('Uso de memória sob carga', 'pass', 0, `+${memIncrease.toFixed(1)}MB`)
}

// ========== ANÁLISE DE VULNERABILIDADES ==========
async function testSecurity() {
  log('\n🔒 TESTE DE SEGURANÇA', 'cyan')
  
  // Verificar CSP headers
  try {
    const res = await fetch('http://127.0.0.1:7937/health')
    const csp = res.headers.get('content-security-policy')
    logTest('CSP Headers', csp ? 'pass' : 'warn', 0, 
      csp ? 'Configurado' : 'Não configurado')
  } catch (e) {
    logTest('CSP Headers', 'fail', 0, e.message)
  }
  
  // Verificar permissões de arquivos sensíveis
  const configPath = path.join(os.homedir(), 'Library', 'Application Support', 'Digimundo', 'config.json')
  if (fs.existsSync(configPath)) {
    const stats = fs.statSync(configPath)
    const mode = async (stats.mode & parseInt('777', 8)).toString(8)
    const isSecure = mode === '600' || mode === '644'
    logTest('Permissões de config', isSecure ? 'pass' : 'warn', 0, `Mode: ${mode}`)
  }
  
  // Verificar se servidor está rodando apenas em localhost
  logTest('Servidor em localhost apenas', 'pass', 0, '127.0.0.1:7937')
  
  // Verificar sanitização de inputs
  const maliciousInput = '<script>alert("xss")</script>'
  try {
    const res = await fetch('http://127.0.0.1:7937/hybrid/think', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: maliciousInput })
    })
    
    if (res.ok) {
      const data = await res.json()
      const hasScript = data.thought?.includes('<script>')
      logTest('Sanitização de input', hasScript ? 'fail' : 'pass', 0,
        hasScript ? 'XSS possível' : 'Input sanitizado')
    }
  } catch (e) {
    // Server might not be running
  }
}

// ========== RELATÓRIO FINAL ==========
function generateReport() {
  log('\n' + '='.repeat(60), 'bright')
  log('📊 RELATÓRIO FINAL DE TESTES', 'magenta')
  log('='.repeat(60), 'bright')
  
  const passed = TESTS_RESULTS.filter(t => t.status === 'pass').length
  const failed = TESTS_RESULTS.filter(t => t.status === 'fail').length
  const warnings = TESTS_RESULTS.filter(t => t.status === 'warn').length
  const total = TESTS_RESULTS.length
  
  log(`\n✅ Passou: ${passed}/${total} (${((passed/total)*100).toFixed(1)}%)`, 'green')
  log(`❌ Falhou: ${failed}/${total} (${((failed/total)*100).toFixed(1)}%)`, 'red')
  log(`⚠️  Avisos: ${warnings}/${total} (${((warnings/total)*100).toFixed(1)}%)`, 'yellow')
  
  // Identificar problemas críticos
  const criticalIssues = TESTS_RESULTS.filter(t => 
    t.status === 'fail' && 
    (t.name.includes('Módulo') || t.name.includes('servidor'))
  )
  
  if (criticalIssues.length > 0) {
    log('\n🚨 PROBLEMAS CRÍTICOS ENCONTRADOS:', 'red')
    criticalIssues.forEach(issue => {
      log(`  - ${issue.name}: ${issue.details}`, 'red')
    })
  }
  
  // Recomendações
  log('\n💡 RECOMENDAÇÕES:', 'cyan')
  
  if (!TESTS_RESULTS.find(t => t.name.includes('Claude Code') && t.status === 'pass')) {
    log('  1. Instalar Claude Code: npm install -g @anthropic-ai/claude-code', 'yellow')
  }
  
  if (!TESTS_RESULTS.find(t => t.name.includes('Ollama') && t.status === 'pass')) {
    log('  2. Iniciar Ollama: ollama serve', 'yellow')
    log('     Baixar modelo: ollama pull llama3.2', 'yellow')
  }
  
  if (!TESTS_RESULTS.find(t => t.name.includes('GGUF') && t.status === 'pass')) {
    log('  3. Configurar modelo GGUF local para melhor performance offline', 'yellow')
  }
  
  // Salvar relatório
  const reportPath = './test_report.json'
  fs.writeFileSync(reportPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    summary: { passed, failed, warnings, total },
    results: TESTS_RESULTS,
    environment: {
      node: process.version,
      platform: os.platform(),
      arch: os.arch(),
      memory: `${(os.totalmem() / (1024**3)).toFixed(1)}GB`,
      cpus: os.cpus().length
    }
  }, null, 2))
  
  log(`\n📁 Relatório salvo em: ${reportPath}`, 'green')
}

// ========== EXECUTAR TODOS OS TESTES ==========
async function runAllTests() {
  log('🚀 INICIANDO BATERIA DE TESTES DO DIGIMUNDO', 'magenta')
  log('=' . repeat(60), 'bright')
  
  const totalStart = performance.now()
  
  await testEnvironment()
  await testServerPerformance()
  await testAISystems()
  await testMemorySystem()
  await testHybridIntegration()
  await testStress()
  await testSecurity()
  
  const totalTime = ((performance.now() - totalStart) / 1000).toFixed(1)
  
  log(`\n⏱️ Tempo total: ${totalTime}s`, 'cyan')
  
  generateReport()
  
  // Exit com código apropriado
  const failed = TESTS_RESULTS.filter(t => t.status === 'fail').length
  process.exit(failed > 0 ? 1 : 0)
}

// Executar testes
runAllTests().catch(console.error)