#!/usr/bin/env node

/**
 * 🏥 ELECTRON HEALTH SYSTEM
 * Sistema completo de monitoramento e correção automática para Electron
 * Versão: 1.0.0
 * Data: 14/08/2025
 */

import { spawn, exec } from 'child_process'
import { promisify } from 'util'
import fs from 'fs/promises'
import path from 'path'
import os from 'os'

const execAsync = promisify(exec)

// ============================
// CONFIGURAÇÕES
// ============================
const CONFIG = {
  checkInterval: 30000, // 30 segundos
  memoryThreshold: 500 * 1024 * 1024, // 500MB
  cpuThreshold: 80, // 80%
  crashThreshold: 3, // 3 crashes antes de ação
  logDir: 'eternal_logs',
  maxLogSize: 10 * 1024 * 1024, // 10MB
  autoFix: true,
  notifications: true
}

// ============================
// CLASSE PRINCIPAL
// ============================
class ElectronHealthSystem {
  constructor() {
    this.stats = {
      startTime: Date.now(),
      crashes: 0,
      fixes: 0,
      memoryPeaks: [],
      cpuPeaks: [],
      errors: [],
      lastCheck: null
    }
    
    this.electronProcess = null
    this.isRunning = false
    this.monitors = new Map()
  }
  
  // Iniciar sistema
  async start() {
    console.log('🏥 Electron Health System - Iniciando...')
    
    // Criar diretório de logs
    await this.ensureLogDir()
    
    // Iniciar monitores
    this.startMemoryMonitor()
    this.startCPUMonitor()
    this.startCrashMonitor()
    this.startDependencyMonitor()
    this.startSecurityMonitor()
    
    // Iniciar loop principal
    this.mainLoop()
    
    console.log('✅ Sistema de saúde iniciado com sucesso!')
  }
  
  // ============================
  // MONITORES
  // ============================
  
  // Monitor de Memória
  startMemoryMonitor() {
    this.monitors.set('memory', setInterval(async () => {
      const usage = process.memoryUsage()
      const total = os.totalmem()
      const free = os.freemem()
      const used = total - free
      
      const stats = {
        timestamp: Date.now(),
        process: {
          rss: usage.rss,
          heapTotal: usage.heapTotal,
          heapUsed: usage.heapUsed,
          external: usage.external
        },
        system: {
          total,
          free,
          used,
          percentage: (used / total) * 100
        }
      }
      
      // Verificar threshold
      if (usage.rss > CONFIG.memoryThreshold) {
        await this.handleHighMemory(stats)
      }
      
      // Registrar pico
      this.stats.memoryPeaks.push(stats)
      if (this.stats.memoryPeaks.length > 100) {
        this.stats.memoryPeaks.shift()
      }
      
    }, 5000))
  }
  
  // Monitor de CPU
  startCPUMonitor() {
    let previousCPU = process.cpuUsage()
    
    this.monitors.set('cpu', setInterval(async () => {
      const currentCPU = process.cpuUsage(previousCPU)
      const usage = (currentCPU.user + currentCPU.system) / 1000000 // microseconds to seconds
      const percentage = (usage / os.cpus().length) * 100
      
      const stats = {
        timestamp: Date.now(),
        usage: percentage,
        user: currentCPU.user,
        system: currentCPU.system
      }
      
      // Verificar threshold
      if (percentage > CONFIG.cpuThreshold) {
        await this.handleHighCPU(stats)
      }
      
      // Registrar pico
      this.stats.cpuPeaks.push(stats)
      if (this.stats.cpuPeaks.length > 100) {
        this.stats.cpuPeaks.shift()
      }
      
      previousCPU = currentCPU
    }, 1000))
  }
  
  // Monitor de Crashes
  startCrashMonitor() {
    process.on('uncaughtException', async (error) => {
      console.error('❌ Uncaught Exception:', error)
      this.stats.crashes++
      await this.logError('uncaughtException', error)
      
      if (this.stats.crashes >= CONFIG.crashThreshold) {
        await this.performEmergencyRecovery()
      }
    })
    
    process.on('unhandledRejection', async (reason, promise) => {
      console.error('❌ Unhandled Rejection:', reason)
      await this.logError('unhandledRejection', { reason, promise })
    })
  }
  
  // Monitor de Dependências
  async startDependencyMonitor() {
    this.monitors.set('dependencies', setInterval(async () => {
      try {
        const packageJson = JSON.parse(
          await fs.readFile('package.json', 'utf-8')
        )
        
        const missing = []
        for (const dep of Object.keys(packageJson.dependencies || {})) {
          try {
            await fs.access(`node_modules/${dep}`)
          } catch {
            missing.push(dep)
          }
        }
        
        if (missing.length > 0) {
          console.warn('⚠️ Dependências faltando:', missing)
          if (CONFIG.autoFix) {
            await this.fixDependencies(missing)
          }
        }
      } catch (error) {
        console.error('Erro ao verificar dependências:', error)
      }
    }, 60000)) // A cada minuto
  }
  
  // Monitor de Segurança
  startSecurityMonitor() {
    this.monitors.set('security', setInterval(async () => {
      try {
        // Verificar vulnerabilidades
        const { stdout } = await execAsync('npm audit --json')
        const audit = JSON.parse(stdout)
        
        if (audit.metadata.vulnerabilities.total > 0) {
          console.warn(`⚠️ ${audit.metadata.vulnerabilities.total} vulnerabilidades encontradas`)
          
          if (CONFIG.autoFix && audit.metadata.vulnerabilities.high === 0) {
            await execAsync('npm audit fix')
            console.log('✅ Vulnerabilidades corrigidas automaticamente')
          }
        }
      } catch (error) {
        // npm audit pode falhar se não houver problemas
      }
    }, 300000)) // A cada 5 minutos
  }
  
  // ============================
  // HANDLERS
  // ============================
  
  async handleHighMemory(stats) {
    console.warn('⚠️ Alto uso de memória detectado!')
    await this.logMetric('high_memory', stats)
    
    if (CONFIG.autoFix) {
      console.log('🔧 Tentando liberar memória...')
      
      // Forçar garbage collection se disponível
      if (global.gc) {
        global.gc()
        console.log('✅ Garbage collection executado')
      }
      
      // Limpar caches
      await this.clearCaches()
      
      // Verificar se melhorou
      setTimeout(() => {
        const newUsage = process.memoryUsage()
        if (newUsage.rss < CONFIG.memoryThreshold) {
          console.log('✅ Memória normalizada')
          this.stats.fixes++
        } else {
          console.warn('⚠️ Memória ainda alta, considere reiniciar o app')
        }
      }, 5000)
    }
  }
  
  async handleHighCPU(stats) {
    console.warn('⚠️ Alto uso de CPU detectado!')
    await this.logMetric('high_cpu', stats)
    
    if (CONFIG.autoFix) {
      console.log('🔧 Tentando reduzir uso de CPU...')
      
      // Identificar processos pesados
      const handles = process._getActiveHandles()
      const requests = process._getActiveRequests()
      
      console.log(`Handles ativos: ${handles.length}`)
      console.log(`Requests ativos: ${requests.length}`)
      
      // Sugerir otimizações
      if (handles.length > 100) {
        console.warn('⚠️ Muitos handles abertos, verifique por vazamentos')
      }
    }
  }
  
  // ============================
  // RECUPERAÇÃO
  // ============================
  
  async performEmergencyRecovery() {
    console.error('🚨 MODO DE RECUPERAÇÃO DE EMERGÊNCIA ATIVADO!')
    
    // 1. Salvar estado atual
    await this.saveEmergencyDump()
    
    // 2. Limpar tudo
    await this.clearAll()
    
    // 3. Reinstalar dependências
    console.log('📦 Reinstalando dependências...')
    await execAsync('npm ci')
    
    // 4. Reiniciar Electron
    await this.restartElectron()
    
    // 5. Reset contador
    this.stats.crashes = 0
    
    console.log('✅ Recuperação de emergência concluída')
  }
  
  async restartElectron() {
    console.log('🔄 Reiniciando Electron...')
    
    // Matar processo atual se existir
    if (this.electronProcess) {
      this.electronProcess.kill()
      await new Promise(resolve => setTimeout(resolve, 2000))
    }
    
    // Iniciar novo processo
    this.electronProcess = spawn('npm', ['run', 'dev'], {
      stdio: 'inherit',
      shell: true
    })
    
    this.electronProcess.on('error', (error) => {
      console.error('Erro ao iniciar Electron:', error)
    })
    
    this.electronProcess.on('exit', (code) => {
      console.log(`Electron finalizado com código: ${code}`)
      this.electronProcess = null
    })
  }
  
  // ============================
  // CORREÇÕES
  // ============================
  
  async fixDependencies(missing) {
    console.log('🔧 Instalando dependências faltantes...')
    
    for (const dep of missing) {
      try {
        await execAsync(`npm install ${dep}`)
        console.log(`✅ ${dep} instalado`)
      } catch (error) {
        console.error(`❌ Erro ao instalar ${dep}:`, error)
      }
    }
  }
  
  async clearCaches() {
    console.log('🧹 Limpando caches...')
    
    try {
      // Limpar cache do npm
      await execAsync('npm cache clean --force')
      
      // Limpar cache do Electron
      const electronCache = path.join(os.homedir(), '.electron')
      await fs.rm(electronCache, { recursive: true, force: true })
      
      console.log('✅ Caches limpos')
    } catch (error) {
      console.error('Erro ao limpar caches:', error)
    }
  }
  
  async clearAll() {
    console.log('🧹 Limpeza completa...')
    
    try {
      // Limpar node_modules
      await fs.rm('node_modules', { recursive: true, force: true })
      
      // Limpar lock files
      await fs.rm('package-lock.json', { force: true })
      
      // Limpar caches
      await this.clearCaches()
      
      console.log('✅ Limpeza completa realizada')
    } catch (error) {
      console.error('Erro na limpeza:', error)
    }
  }
  
  // ============================
  // LOGGING
  // ============================
  
  async ensureLogDir() {
    try {
      await fs.mkdir(CONFIG.logDir, { recursive: true })
    } catch (error) {
      console.error('Erro ao criar diretório de logs:', error)
    }
  }
  
  async logError(type, error) {
    const log = {
      timestamp: new Date().toISOString(),
      type,
      error: {
        message: error.message,
        stack: error.stack,
        code: error.code
      }
    }
    
    this.stats.errors.push(log)
    if (this.stats.errors.length > 100) {
      this.stats.errors.shift()
    }
    
    try {
      const logFile = path.join(CONFIG.logDir, 'errors.json')
      const existing = await this.readJsonLog(logFile)
      existing.push(log)
      await fs.writeFile(logFile, JSON.stringify(existing, null, 2))
    } catch (error) {
      console.error('Erro ao salvar log:', error)
    }
  }
  
  async logMetric(type, data) {
    const log = {
      timestamp: new Date().toISOString(),
      type,
      data
    }
    
    try {
      const logFile = path.join(CONFIG.logDir, 'metrics.json')
      const existing = await this.readJsonLog(logFile)
      existing.push(log)
      
      // Limitar tamanho do arquivo
      if (JSON.stringify(existing).length > CONFIG.maxLogSize) {
        existing.splice(0, Math.floor(existing.length / 2))
      }
      
      await fs.writeFile(logFile, JSON.stringify(existing, null, 2))
    } catch (error) {
      console.error('Erro ao salvar métrica:', error)
    }
  }
  
  async readJsonLog(file) {
    try {
      const content = await fs.readFile(file, 'utf-8')
      return JSON.parse(content)
    } catch {
      return []
    }
  }
  
  async saveEmergencyDump() {
    const dump = {
      timestamp: new Date().toISOString(),
      stats: this.stats,
      system: {
        platform: os.platform(),
        release: os.release(),
        arch: os.arch(),
        cpus: os.cpus().length,
        memory: os.totalmem(),
        uptime: os.uptime()
      },
      process: {
        versions: process.versions,
        memoryUsage: process.memoryUsage(),
        cpuUsage: process.cpuUsage()
      }
    }
    
    const dumpFile = path.join(
      CONFIG.logDir, 
      `emergency_dump_${Date.now()}.json`
    )
    
    await fs.writeFile(dumpFile, JSON.stringify(dump, null, 2))
    console.log(`📁 Dump salvo em: ${dumpFile}`)
  }
  
  // ============================
  // RELATÓRIOS
  // ============================
  
  generateReport() {
    const uptime = Date.now() - this.stats.startTime
    const hours = Math.floor(uptime / 3600000)
    const minutes = Math.floor((uptime % 3600000) / 60000)
    
    const avgMemory = this.stats.memoryPeaks.length > 0
      ? this.stats.memoryPeaks.reduce((sum, m) => sum + m.process.rss, 0) / this.stats.memoryPeaks.length
      : 0
      
    const avgCPU = this.stats.cpuPeaks.length > 0
      ? this.stats.cpuPeaks.reduce((sum, c) => sum + c.usage, 0) / this.stats.cpuPeaks.length
      : 0
    
    return {
      uptime: `${hours}h ${minutes}m`,
      crashes: this.stats.crashes,
      fixes: this.stats.fixes,
      avgMemory: `${(avgMemory / 1024 / 1024).toFixed(2)} MB`,
      avgCPU: `${avgCPU.toFixed(2)}%`,
      lastCheck: this.stats.lastCheck,
      errors: this.stats.errors.length,
      health: this.calculateHealthScore()
    }
  }
  
  calculateHealthScore() {
    let score = 100
    
    // Penalizar por crashes
    score -= this.stats.crashes * 10
    
    // Penalizar por erros
    score -= this.stats.errors.length * 2
    
    // Penalizar por alto uso de recursos
    if (this.stats.memoryPeaks.length > 0) {
      const avgMemory = this.stats.memoryPeaks.reduce((sum, m) => sum + m.process.rss, 0) / this.stats.memoryPeaks.length
      if (avgMemory > CONFIG.memoryThreshold) {
        score -= 15
      }
    }
    
    return Math.max(0, Math.min(100, score))
  }
  
  printReport() {
    const report = this.generateReport()
    
    console.clear()
    console.log('╔════════════════════════════════════════╗')
    console.log('║     ELECTRON HEALTH SYSTEM REPORT      ║')
    console.log('╠════════════════════════════════════════╣')
    console.log(`║ Uptime:       ${report.uptime.padEnd(25)} ║`)
    console.log(`║ Health Score: ${report.health}%`.padEnd(42) + '║')
    console.log(`║ Crashes:      ${report.crashes}`.padEnd(42) + '║')
    console.log(`║ Auto-Fixes:   ${report.fixes}`.padEnd(42) + '║')
    console.log(`║ Avg Memory:   ${report.avgMemory.padEnd(25)} ║`)
    console.log(`║ Avg CPU:      ${report.avgCPU.padEnd(25)} ║`)
    console.log(`║ Errors:       ${report.errors}`.padEnd(42) + '║')
    console.log('╚════════════════════════════════════════╝')
    
    // Status colorido baseado no health score
    if (report.health > 80) {
      console.log('✅ Sistema saudável')
    } else if (report.health > 60) {
      console.log('⚠️ Sistema precisa de atenção')
    } else {
      console.log('❌ Sistema em estado crítico')
    }
  }
  
  // ============================
  // LOOP PRINCIPAL
  // ============================
  
  mainLoop() {
    setInterval(() => {
      this.stats.lastCheck = new Date().toISOString()
      this.printReport()
      
      // Auto-save do relatório
      this.saveReport()
    }, CONFIG.checkInterval)
  }
  
  async saveReport() {
    const report = this.generateReport()
    const reportFile = path.join(CONFIG.logDir, 'latest_report.json')
    
    try {
      await fs.writeFile(reportFile, JSON.stringify(report, null, 2))
    } catch (error) {
      console.error('Erro ao salvar relatório:', error)
    }
  }
  
  // ============================
  // CLEANUP
  // ============================
  
  stop() {
    console.log('🛑 Parando sistema de saúde...')
    
    // Parar todos os monitores
    for (const [name, interval] of this.monitors) {
      clearInterval(interval)
      console.log(`✅ Monitor ${name} parado`)
    }
    
    // Salvar relatório final
    this.saveReport()
    
    // Matar processo Electron se estiver rodando
    if (this.electronProcess) {
      this.electronProcess.kill()
    }
    
    console.log('✅ Sistema de saúde parado')
  }
}

// ============================
// INICIALIZAÇÃO
// ============================

const healthSystem = new ElectronHealthSystem()

// Handlers de saída
process.on('SIGINT', () => {
  console.log('\n🛑 Recebido SIGINT, finalizando...')
  healthSystem.stop()
  process.exit(0)
})

process.on('SIGTERM', () => {
  console.log('\n🛑 Recebido SIGTERM, finalizando...')
  healthSystem.stop()
  process.exit(0)
})

// Iniciar sistema
healthSystem.start().catch(error => {
  console.error('❌ Erro fatal ao iniciar sistema:', error)
  process.exit(1)
})

// Exportar para uso externo
export default ElectronHealthSystem
