#!/usr/bin/env node

/**
 * 🧪 TESTE RÁPIDO DO SISTEMA DE PRODUÇÃO
 * Verifica se todos os sistemas estão funcionando corretamente
 */

import { performance } from 'perf_hooks'

console.log('🧪 Testando Sistema de Produção Digimundo...\n')

const tests = []
const testResults = {
  passed: 0,
  failed: 0,
  total: 0
}

// Helper para executar testes
function test(name, testFn) {
  tests.push({ name, testFn })
}

function assertEqual(actual, expected, message) {
  if (actual === expected) {
    console.log(`✅ ${message}`)
    return true
  } else {
    console.log(`❌ ${message} - Expected: ${expected}, Got: ${actual}`)
    return false
  }
}

function assertExists(value, message) {
  if (value !== undefined && value !== null) {
    console.log(`✅ ${message}`)
    return true
  } else {
    console.log(`❌ ${message} - Value is ${value}`)
    return false
  }
}

// TESTES
test('Import de sistemas de produção', async () => {
  try {
    const { getCacheSystem } = await import('./app/server/cache-system.js')
    const { getSecuritySystem } = await import('./app/server/security-middleware.js')
    const { getPerformanceOptimizer } = await import('./app/server/performance-optimizer.js')
    const { getCleanupSystem } = await import('./app/server/cleanup-system.js')
    
    assertExists(getCacheSystem, 'Cache System importado')
    assertExists(getSecuritySystem, 'Security System importado')
    assertExists(getPerformanceOptimizer, 'Performance Optimizer importado')
    assertExists(getCleanupSystem, 'Cleanup System importado')
    
    return true
  } catch (error) {
    console.log(`❌ Erro ao importar sistemas: ${error.message}`)
    return false
  }
})

test('Verificação do SUPREME_MEMORY corrigido', async () => {
  try {
    const { getSupremeMemory } = await import('./app/consciousness/SUPREME_MEMORY.js')
    const memory = getSupremeMemory()
    
    const stats = await memory.getStats()
    assertExists(stats.name, 'Stats tem name')
    assertExists(stats.totalMemories, 'Stats tem totalMemories')
    assertExists(stats.timestamp, 'Stats tem timestamp')
    
    // Verificar se não há método duplicado
    const proto = Object.getPrototypeOf(memory)
    const methods = Object.getOwnPropertyNames(proto)
    const getStatsMethods = methods.filter(m => m === 'getStats')
    
    assertEqual(getStatsMethods.length, 1, 'Apenas um método getStats')
    
    return true
  } catch (error) {
    console.log(`❌ Erro no SUPREME_MEMORY: ${error.message}`)
    return false
  }
})

test('Cache System functionality', async () => {
  try {
    const { getCacheSystem } = await import('./app/server/cache-system.js')
    const cache = getCacheSystem()
    
    assertExists(cache.generateKey, 'Cache tem método generateKey')
    assertExists(cache.getStats, 'Cache tem método getStats')
    assertExists(cache.middleware, 'Cache tem middleware')
    
    // Testar geração de key
    const key = cache.generateKey('test', { data: 'test' })
    assertExists(key, 'Key gerada com sucesso')
    
    return true
  } catch (error) {
    console.log(`❌ Erro no Cache System: ${error.message}`)
    return false
  }
})

test('Security System configuration', async () => {
  try {
    const { getSecuritySystem } = await import('./app/server/security-middleware.js')
    const security = getSecuritySystem()
    
    const middlewares = security.getAllMiddlewares()
    assertExists(middlewares.helmet, 'Helmet configurado')
    assertExists(middlewares.cors, 'CORS configurado')
    assertExists(middlewares.compression, 'Compression configurado')
    assertExists(middlewares.rateLimiters, 'Rate limiters configurados')
    assertExists(middlewares.validation, 'Validation schemas configurados')
    
    return true
  } catch (error) {
    console.log(`❌ Erro no Security System: ${error.message}`)
    return false
  }
})

test('Performance Optimizer initialization', async () => {
  try {
    const { getPerformanceOptimizer } = await import('./app/server/performance-optimizer.js')
    const optimizer = getPerformanceOptimizer()
    
    assertExists(optimizer.performanceMiddleware, 'Performance middleware disponível')
    assertExists(optimizer.getSystemMetrics, 'System metrics disponível')
    assertExists(optimizer.healthCheck, 'Health check disponível')
    
    const metrics = optimizer.getSystemMetrics()
    assertExists(metrics.cpu, 'CPU metrics')
    assertExists(metrics.memory, 'Memory metrics')
    assertExists(metrics.uptime, 'Uptime metrics')
    
    return true
  } catch (error) {
    console.log(`❌ Erro no Performance Optimizer: ${error.message}`)
    return false
  }
})

test('Cleanup System functionality', async () => {
  try {
    const { getCleanupSystem } = await import('./app/server/cleanup-system.js')
    const cleanup = getCleanupSystem()
    
    assertExists(cleanup.setTimeout, 'setTimeout wrapper disponível')
    assertExists(cleanup.setInterval, 'setInterval wrapper disponível')
    assertExists(cleanup.getResourceStats, 'Resource stats disponível')
    
    const stats = cleanup.getResourceStats()
    assertExists(stats.timers, 'Timer stats')
    assertExists(stats.intervals, 'Interval stats')
    assertExists(stats.totalResources, 'Total resources')
    
    return true
  } catch (error) {
    console.log(`❌ Erro no Cleanup System: ${error.message}`)
    return false
  }
})

test('Arquivos de configuração de produção', async () => {
  try {
    const fs = await import('fs')
    
    const ecosystemExists = fs.existsSync('./ecosystem.config.js')
    assertEqual(ecosystemExists, true, 'ecosystem.config.js existe')
    
    const dockerfileExists = fs.existsSync('./Dockerfile')
    assertEqual(dockerfileExists, true, 'Dockerfile existe')
    
    const productionScriptExists = fs.existsSync('./DIGIMUNDO_PRODUCTION.sh')
    assertEqual(productionScriptExists, true, 'DIGIMUNDO_PRODUCTION.sh existe')
    
    const readmeExists = fs.existsSync('./PRODUCTION_README.md')
    assertEqual(readmeExists, true, 'PRODUCTION_README.md existe')
    
    return true
  } catch (error) {
    console.log(`❌ Erro na verificação de arquivos: ${error.message}`)
    return false
  }
})

test('Package.json scripts de produção', async () => {
  try {
    const fs = await import('fs')
    const packageJson = JSON.parse(fs.readFileSync('./package.json', 'utf8'))
    
    assertExists(packageJson.scripts.production, 'Script production')
    assertExists(packageJson.scripts['production:pm2'], 'Script production:pm2')
    assertExists(packageJson.scripts['production:docker'], 'Script production:docker')
    assertExists(packageJson.scripts.metrics, 'Script metrics')
    assertExists(packageJson.scripts.health, 'Script health')
    
    // Verificar dependências de produção
    assertExists(packageJson.dependencies.helmet, 'Helmet dependency')
    assertExists(packageJson.dependencies['express-rate-limit'], 'Rate limit dependency')
    assertExists(packageJson.dependencies.joi, 'Joi dependency')
    assertExists(packageJson.dependencies.compression, 'Compression dependency')
    assertExists(packageJson.dependencies.redis, 'Redis dependency')
    
    return true
  } catch (error) {
    console.log(`❌ Erro na verificação do package.json: ${error.message}`)
    return false
  }
})

// EXECUTAR TESTES
async function runTests() {
  console.log(`Executando ${tests.length} testes...\n`)
  
  const startTime = performance.now()
  
  for (const { name, testFn } of tests) {
    console.log(`🔍 ${name}`)
    testResults.total++
    
    try {
      const success = await testFn()
      if (success) {
        testResults.passed++
      } else {
        testResults.failed++
      }
    } catch (error) {
      console.log(`❌ Erro inesperado: ${error.message}`)
      testResults.failed++
    }
    
    console.log('')
  }
  
  const endTime = performance.now()
  const duration = endTime - startTime
  
  // RELATÓRIO FINAL
  console.log('='.repeat(60))
  console.log('📊 RELATÓRIO FINAL DOS TESTES')
  console.log('='.repeat(60))
  console.log(`✅ Passou: ${testResults.passed}`)
  console.log(`❌ Falhou: ${testResults.failed}`)
  console.log(`📊 Total: ${testResults.total}`)
  console.log(`⏱️ Tempo: ${duration.toFixed(2)}ms`)
  console.log(`📈 Taxa de Sucesso: ${(testResults.passed / testResults.total * 100).toFixed(1)}%`)
  
  if (testResults.failed === 0) {
    console.log('\n🎉 TODOS OS TESTES PASSARAM!')
    console.log('🚀 Sistema de produção está pronto para deploy!')
    console.log('\n📝 Próximos passos:')
    console.log('   1. npm run production (para deploy automático)')
    console.log('   2. npm run production:pm2 (para deploy PM2)')
    console.log('   3. npm run production:docker (para deploy Docker)')
  } else {
    console.log('\n⚠️ ALGUNS TESTES FALHARAM')
    console.log('🔧 Verifique os erros acima antes do deploy')
    process.exit(1)
  }
}

runTests().catch(error => {
  console.error('💥 Erro crítico nos testes:', error)
  process.exit(1)
})