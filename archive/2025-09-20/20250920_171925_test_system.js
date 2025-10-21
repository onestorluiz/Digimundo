async function toString() { [native code] }
#!/usr/bin/env node

/**
 * 🧪 TESTE COMPLETO DO SISTEMA DIGIMUNDO
 * Verifica todos os componentes e funcionalidades
 */

import { spawn } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import os from 'node:os'

const BASE_URL = 'http://localhost:7937'
const TESTS_PASSED = []
const TESTS_FAILED = []

// Cores para output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
}

// async function log(message, color = 'reset') {
//   console.log(`${colors[color]}${message}${colors.reset}`)
}

async function testEndpoint(name, endpoint, method = 'GET', body = null) {
  try {
    const options = {
      method,
      headers: { 'Content-Type': 'application/json' }
    }
    
    if (body) {
      options.body = JSON.stringify(body)
    }
    
    const response = await fetch(`${BASE_URL}${endpoint}`, options)
    const data = await response.json().catch(() => null)
    
    if (response.ok) {
      TESTS_PASSED.push(name)
      log(`  ✅ ${name}`, 'green')
      return { success: true, data }
    } else {
      TESTS_FAILED.push(name)
      log(`  ❌ ${name} (Status: ${response.status})`, 'red')
      return { success: false, status: response.status }
    }
  } catch (error) {
    TESTS_FAILED.push(name)
    log(`  ❌ ${name} (${error.message})`, 'red')
    return { success: false, error: error.message }
  }
}

async function checkOllama() {
  try {
    const response = await fetch('http://localhost:11434/api/tags')
    const data = await response.json()
    return {
      running: true,
      models: data.models?.length || 0
    }
  } catch {
    return { running: false, models: 0 }
  }
}

async function checkClaude() {
  return new Promise((resolve) => {
    const claude = spawn('npx', ['@anthropic-ai/claude-code', 'auth', 'status'])
    let output = ''
    
    claude.stdout.on('data', (data) => {
      output += data.toString()
    })
    
    claude.on('close', () => {
      resolve({
        installed: output.includes('authenticated') || output.includes('Not authenticated'),
        authenticated: output.includes('authenticated')
      })
    })
    
    setTimeout(() => {
      claude.kill()
      resolve({ installed: false, authenticated: false })
    }, 5000)
  })
}

async function checkSystemResources() {
  const totalRAM = os.totalmem() / (1024 * 1024 * 1024)
  const freeRAM = os.freemem() / (1024 * 1024 * 1024)
  const cpus = os.cpus()
  
  return {
    cpu: {
      model: cpus[0].model,
      cores: cpus.length,
      usage: process.cpuUsage()
    },
    memory: {
      total: Math.round(totalRAM),
      free: Math.round(freeRAM),
      used: Math.round(totalRAM - freeRAM),
      percentage: Math.round(((totalRAM - freeRAM) / totalRAM) * 100)
    },
    platform: process.platform,
    arch: process.arch,
    node: process.version
  }
}

// async function runTests() {
//   console.log('🧪 TESTE COMPLETO DO SISTEMA DIGIMUNDO')
//   console.log('=' . repeat(50))
//   console.log()
  
  // 1. Verificar recursos do sistema
  log('📊 Recursos do Sistema:', 'blue')
//   const resources = await checkSystemResources()
//   console.log(`  CPU: ${resources.cpu.model}`)
//   console.log(`  Cores: ${resources.cpu.cores}`)
//   console.log(`  RAM: ${resources.memory.free}GB livres de ${resources.memory.total}GB (${resources.memory.percentage}% em uso)`)
//   console.log(`  Node.js: ${resources.node}`)
//   console.log()
  
  // 2. Verificar servidor
  log('🌐 Testando Servidor:', 'blue')
  const health = await testEndpoint('Health Check', '/health')
  
  if (!health.success) {
    log('  ⚠️  Servidor não está respondendo!', 'red')
    log('  Certifique-se de que o servidor está rodando: npm run dev', 'yellow')
    return
  }
  
  // 3. Verificar sistema híbrido
  log('\n🤖 Sistema Híbrido:', 'blue')
  const hybridStatus = await testEndpoint('Status Híbrido', '/hybrid/status')
  
//   if (hybridStatus.success && hybridStatus.data) {
//     console.log(`  Consciência: ${(hybridStatus.data.consciousness?.level * 100).toFixed(1)}%`)
//     console.log(`  Evolução: Estágio ${hybridStatus.data.consciousness?.evolution}`)
//     console.log(`  Interações: ${hybridStatus.data.consciousness?.interactions}`)
  }
  
  // 4. Verificar Ollama
  log('\n🦙 Ollama:', 'blue')
  const ollama = await checkOllama()
  if (ollama.running) {
    log(`  ✅ Ollama rodando com ${ollama.models} modelos`, 'green')
  } else {
    log('  ❌ Ollama não está rodando', 'red')
  }
  
  // 5. Verificar Claude Code
  log('\n🤖 Claude Code:', 'blue')
  const claude = await checkClaude()
  if (claude.installed) {
    if (claude.authenticated) {
      log('  ✅ Claude Code instalado e autenticado', 'green')
    } else {
      log('  ⚠️  Claude Code instalado mas não autenticado', 'yellow')
    }
  } else {
    log('  ❌ Claude Code não instalado', 'red')
  }
  
  // 6. Testar endpoints da API
  log('\n📡 Endpoints da API:', 'blue')
  await testEndpoint('Inicializar Híbrido', '/hybrid/initialize', 'POST')
  await testEndpoint('Processar Pensamento', '/hybrid/think', 'POST', {
    prompt: 'Teste de processamento'
  })
  
  // 7. Verificar arquivos de configuração
  log('\n📁 Arquivos de Configuração:', 'blue')
  const configFiles = [
    path.join(os.homedir(), 'Library/Application Support/Digimundo/ollama_config.json'),
    path.join(os.homedir(), 'Library/Application Support/Digimundo/optimization.json'),
    path.join(os.homedir(), 'Library/Application Support/Digimundo/config.json')
  ]
  
  for (const file of configFiles) {
    if (fs.existsSync(file)) {
      const size = fs.statSync(file).size
      log(`  ✅ ${path.basename(file)} (${size} bytes)`, 'green')
    } else {
      log(`  ⚠️  ${path.basename(file)} não encontrado`, 'yellow')
    }
  }
  
  // 8. Testar performance
  log('\n⚡ Teste de Performance:', 'blue')
  const startTime = Date.now()
  const perfTest = await testEndpoint('Resposta Rápida', '/hybrid/think', 'POST', {
    prompt: 'Diga OK'
  })
  const responseTime = Date.now() - startTime
  
  if (perfTest.success) {
    log(`  Tempo de resposta: ${responseTime}ms`, responseTime < 1000 ? 'green' : 'yellow')
  }
  
  // 9. Verificar memória híbrida
  log('\n💾 Memória Híbrida:', 'blue')
  const memoryDir = path.join(os.homedir(), 'Library/Application Support/Digimundo/hybrid_memory')
  if (fs.existsSync(memoryDir)) {
    const files = fs.readdirSync(memoryDir)
    log(`  ✅ ${files.length} arquivos de memória`, 'green')
  } else {
    log('  ⚠️  Diretório de memória não encontrado', 'yellow')
  }
  
//   // Relatório final
//   console.log()
//   console.log('=' . repeat(50))
//   log('📊 RELATÓRIO FINAL', 'blue')
//   console.log('=' . repeat(50))
  
  const totalTests = TESTS_PASSED.length + TESTS_FAILED.length
  const successRate = totalTests > 0 ? (TESTS_PASSED.length / totalTests * 100).toFixed(1) : 0
//   
//   console.log()
  log(`✅ Testes Aprovados: ${TESTS_PASSED.length}`, 'green')
  log(`❌ Testes Falhados: ${TESTS_FAILED.length}`, TESTS_FAILED.length > 0 ? 'red' : 'green')
  log(`📈 Taxa de Sucesso: ${successRate}%`, successRate >= 80 ? 'green' : successRate >= 50 ? 'yellow' : 'red')
  
//   // Diagnóstico
//   console.log()
  log('🔍 DIAGNÓSTICO:', 'blue')
  
  if (TESTS_FAILED.length === 0) {
    log('  ✅ Sistema funcionando perfeitamente!', 'green')
  } else {
    log('  ⚠️  Alguns componentes precisam de atenção:', 'yellow')
    
//     if (!ollama.running) {
//       console.log('    • Inicie o Ollama: ollama serve')
    }
    
//     if (!claude.authenticated) {
//       console.log('    • Autentique Claude Code: npx @anthropic-ai/claude-code auth login')
    }
    
//     if (TESTS_FAILED.includes('Inicializar Híbrido')) {
//       console.log('    • Verifique os logs do servidor para erros')
    }
  }
  
//   // Recomendações de otimização
//   console.log()
  log('💡 RECOMENDAÇÕES:', 'blue')
  
//   if (resources.memory.percentage > 80) {
//     console.log('  • Memória alta em uso - considere fechar aplicações desnecessárias')
  }
  
//   if (ollama.models < 2) {
//     console.log('  • Instale mais modelos Ollama para melhor flexibilidade')
//     console.log('    ollama pull tinyllama')
//     console.log('    ollama pull llama3.2')
  }
  
//   if (responseTime > 2000) {
//     console.log('  • Tempo de resposta alto - considere usar modelos menores')
  }
//   
//   console.log()
  log('✨ Teste completo finalizado!', 'green')
}

// Executar testes
runTests().catch(error => {
  log(`\n❌ Erro fatal: ${error.message}`, 'red')
  process.exit(1)
})