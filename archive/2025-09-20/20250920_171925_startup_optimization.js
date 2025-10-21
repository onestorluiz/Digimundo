#!/usr/bin/env node

/**
 * Script de inicialização otimizada com correção de memory leaks
 * Executa o servidor com flags de otimização e garbage collection
 */

import { spawn } from 'child_process'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const __dirname = dirname(fileURLToPath(import.meta.url))

// Configurações de otimização para M3 Ultra
const NODE_OPTIONS = [
  '--max-old-space-size=4096',     // 4GB de heap (ajustável)
  '--max-semi-space-size=64',      // Aumentar semi-space para GC
  '--expose-gc',                   // Permitir GC manual
  '--optimize-for-size',           // Otimizar para uso de memória
  '--always-compact',              // Compactar heap sempre
  '--trace-gc-verbose',            // Log detalhado de GC (desabilitar em produção)
  '--gc-interval=100',             // GC mais frequente
  '--no-lazy',                     // Não usar lazy compilation
  '--use-idle-notification'        // Usar notificações idle para GC
]

// Variáveis de ambiente para otimização
const ENV_VARS = {
  NODE_ENV: 'production',
  PORT: process.env.PORT || '7937',
  DISABLE_CONSOLE_LOGS: 'false',  // Manter logs para debug
  ENABLE_MEMORY_OPTIMIZATION: 'true',
  GC_INTERVAL: '30000',            // GC a cada 30 segundos
  CLEANUP_INTERVAL: '60000',       // Limpeza a cada 60 segundos
  MAX_LISTENERS: '10',             // Limitar listeners por evento
  MEMORY_THRESHOLD_MB: '500',      // Threshold para forçar GC
  ENABLE_WEAK_REFS: 'true',        // Usar WeakRef para listeners
  AUTO_CLEANUP_WEBSOCKETS: 'true', // Limpar WebSockets automaticamente
  LOG_MEMORY_STATS: 'true',        // Logar estatísticas de memória
  ...process.env                   // Manter variáveis existentes
}

// Função para monitorar memória do processo
function monitorMemory(childProcess) {
  const interval = setInterval(() => {
    if (childProcess.killed) {
      clearInterval(interval)
      return
    }
    
    // Enviar sinal para logar memória
    childProcess.send({ command: 'memory_stats' })
  }, 30000) // A cada 30 segundos
  
  return interval
}

// Função para reiniciar processo se memória estourar
function setupMemoryWatchdog(childProcess, maxMemoryMB = 1000) {
  const interval = setInterval(() => {
    if (childProcess.killed) {
      clearInterval(interval)
      return
    }
    
    // Verificar uso de memória via mensagem
    childProcess.send({ command: 'check_memory' })
  }, 60000) // A cada minuto
  
  childProcess.on('message', (msg) => {
    if (msg.type === 'memory_report' && msg.heapUsedMB > maxMemoryMB) {
      console.log(`⚠️ Memória alta detectada: ${msg.heapUsedMB}MB. Reiniciando...`)
      restartProcess()
    }
  })
  
  return interval
}

// Variável para armazenar o processo filho
let serverProcess = null
let memoryMonitor = null
let memoryWatchdog = null

// Função para iniciar o servidor
function startServer() {
  console.log('🚀 Iniciando servidor Digimundo com otimizações...')
  console.log('📊 Configurações de memória:', {
    maxOldSpace: '4096MB',
    gcInterval: '30s',
    cleanupInterval: '60s',
    memoryThreshold: '500MB'
  })
  
  // Spawn do processo com flags de otimização
  serverProcess = spawn('node', [
    ...NODE_OPTIONS.map(opt => opt),
    join(__dirname, 'index.js')
  ], {
    env: ENV_VARS,
    stdio: ['inherit', 'inherit', 'inherit', 'ipc']
  })
  
  // Configurar monitoramento
  memoryMonitor = monitorMemory(serverProcess)
  memoryWatchdog = setupMemoryWatchdog(serverProcess)
  
  // Handlers de eventos
  serverProcess.on('error', (error) => {
    console.error('❌ Erro no processo:', error)
    setTimeout(restartProcess, 5000)
  })
  
  serverProcess.on('exit', (code, signal) => {
    if (code !== 0 && code !== null) {
      console.log(`⚠️ Servidor saiu com código ${code}. Reiniciando em 5s...`)
      setTimeout(restartProcess, 5000)
    } else if (signal) {
      console.log(`🛑 Servidor terminado por sinal ${signal}`)
    }
  })
  
  // Configurar IPC para comunicação
  if (serverProcess.send) {
    // Enviar comandos periódicos
    setInterval(() => {
      if (serverProcess && !serverProcess.killed) {
        serverProcess.send({ command: 'cleanup' })
      }
    }, ENV_VARS.CLEANUP_INTERVAL)
  }
}

// Função para reiniciar o processo
function restartProcess() {
  console.log('🔄 Reiniciando servidor...')
  
  // Limpar monitores
  if (memoryMonitor) clearInterval(memoryMonitor)
  if (memoryWatchdog) clearInterval(memoryWatchdog)
  
  // Matar processo existente
  if (serverProcess && !serverProcess.killed) {
    serverProcess.kill('SIGTERM')
    setTimeout(() => {
      if (serverProcess && !serverProcess.killed) {
        serverProcess.kill('SIGKILL')
      }
    }, 5000)
  }
  
  // Aguardar e reiniciar
  setTimeout(startServer, 2000)
}

// Handlers de shutdown
process.on('SIGINT', () => {
  console.log('\n🛑 Recebido SIGINT, encerrando...')
  if (memoryMonitor) clearInterval(memoryMonitor)
  if (memoryWatchdog) clearInterval(memoryWatchdog)
  if (serverProcess) serverProcess.kill('SIGINT')
  process.exit(0)
})

process.on('SIGTERM', () => {
  console.log('\n🛑 Recebido SIGTERM, encerrando...')
  if (memoryMonitor) clearInterval(memoryMonitor)
  if (memoryWatchdog) clearInterval(memoryWatchdog)
  if (serverProcess) serverProcess.kill('SIGTERM')
  process.exit(0)
})

// Iniciar servidor
startServer()

// Log de instruções
console.log('\n📝 Instruções:')
console.log('  - O servidor está rodando com garbage collection otimizado')
console.log('  - Memory leaks serão detectados e corrigidos automaticamente')
console.log('  - Se a memória ultrapassar 1GB, o servidor reiniciará')
console.log('  - Use Ctrl+C para encerrar')
console.log('')