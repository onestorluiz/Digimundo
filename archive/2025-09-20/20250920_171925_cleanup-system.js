/**
 * 🧹 SISTEMA DE CLEANUP PARA PRODUÇÃO
 * Gerenciamento automático de recursos e event listeners
 */

class CleanupSystem {
  constructor() {
    this.timers = new Set()
    this.intervals = new Set()
    this.eventListeners = new Map()
    this.connections = new Set()
    this.isShuttingDown = false
  }

  // Registrar timer para cleanup automático
  registerTimer(timerId) {
    this.timers.add(timerId)
    return timerId
  }

  // Registrar interval para cleanup automático
  registerInterval(intervalId) {
    this.intervals.add(intervalId)
    return intervalId
  }

  // Registrar event listener para cleanup automático
  registerEventListener(target, event, listener) {
    const key = `${target.constructor.name}_${event}`
    if (!this.eventListeners.has(key)) {
      this.eventListeners.set(key, [])
    }
    this.eventListeners.get(key).push({ target, event, listener })
  }

  // Registrar conexão para cleanup automático
  registerConnection(connection) {
    this.connections.add(connection)
    return connection
  }

  // Wrapper para setTimeout com cleanup automático
  setTimeout(callback, delay) {
    const timerId = setTimeout(() => {
      this.timers.delete(timerId)
      callback()
    }, delay)
    return this.registerTimer(timerId)
  }

  // Wrapper para setInterval com cleanup automático
  setInterval(callback, interval) {
    const intervalId = setInterval(callback, interval)
    return this.registerInterval(intervalId)
  }

  // Wrapper para addEventListener com cleanup automático
  addEventListener(target, event, listener, options) {
    target.addEventListener(event, listener, options)
    this.registerEventListener(target, event, listener)
  }

  // Cleanup específico de timers
  clearAllTimers() {
    for (const timerId of this.timers) {
      clearTimeout(timerId)
    }
    this.timers.clear()
  }

  // Cleanup específico de intervals
  clearAllIntervals() {
    for (const intervalId of this.intervals) {
      clearInterval(intervalId)
    }
    this.intervals.clear()
  }

  // Cleanup específico de event listeners
  removeAllEventListeners() {
    for (const [key, listeners] of this.eventListeners) {
      for (const { target, event, listener } of listeners) {
        try {
          target.removeEventListener(event, listener)
        } catch (error) {
          console.warn(`Erro ao remover event listener ${key}:`, error)
        }
      }
    }
    this.eventListeners.clear()
  }

  // Cleanup específico de conexões
  closeAllConnections() {
    for (const connection of this.connections) {
      try {
        if (connection && typeof connection.close === 'function') {
          connection.close()
        } else if (connection && typeof connection.destroy === 'function') {
          connection.destroy()
        } else if (connection && typeof connection.end === 'function') {
          connection.end()
        }
      } catch (error) {
        console.warn('Erro ao fechar conexão:', error)
      }
    }
    this.connections.clear()
  }

  // Cleanup completo de todos os recursos
  cleanupAll() {
    if (this.isShuttingDown) return

    this.isShuttingDown = true
    
    console.log('🧹 Iniciando cleanup de recursos...')
    
    // Cleanup em ordem específica
    this.clearAllTimers()
    this.clearAllIntervals()
    this.removeAllEventListeners()
    this.closeAllConnections()
    
    console.log('✅ Cleanup de recursos concluído')
  }

  // Configurar handlers de shutdown
  setupGracefulShutdown() {
    const shutdownHandler = (signal) => {
      console.log(`🛑 Recebido sinal ${signal}, iniciando shutdown graceful...`)
      this.cleanupAll()
      
      // Dar tempo para cleanup antes de forçar saída
      setTimeout(() => {
        console.log('💀 Forçando saída do processo...')
        process.exit(0)
      }, 5000)
    }

    // Registrar handlers para diferentes sinais
    process.on('SIGTERM', () => shutdownHandler('SIGTERM'))
    process.on('SIGINT', () => shutdownHandler('SIGINT'))
    process.on('SIGUSR2', () => shutdownHandler('SIGUSR2')) // PM2 reload
    
    // Cleanup em caso de erro não tratado
    process.on('uncaughtException', (error) => {
      console.error('💥 Erro não tratado:', error)
      this.cleanupAll()
      process.exit(1)
    })

    process.on('unhandledRejection', (reason, promise) => {
      console.error('💥 Promise rejeitada não tratada:', reason)
      this.cleanupAll()
      process.exit(1)
    })

    console.log('🛡️ Handlers de shutdown graceful configurados')
  }

  // Monitorar recursos periodicamente
  startResourceMonitoring() {
    const monitoringInterval = this.setInterval(() => {
      const stats = this.getResourceStats()
      
      // Alertar se muitos recursos estão sendo usados
      if (stats.totalResources > 1000) {
        console.warn('⚠️ Muitos recursos ativos:', stats)
      }
      
      // Log periódico em modo de debug
      if (process.env.LOG_LEVEL === 'debug') {
        console.log('📊 Recursos ativos:', stats)
      }
    }, 60000) // A cada minuto

    return monitoringInterval
  }

  // Estatísticas de recursos
  getResourceStats() {
    return {
      timers: this.timers.size,
      intervals: this.intervals.size,
      eventListeners: Array.from(this.eventListeners.values()).reduce((sum, listeners) => sum + listeners.length, 0),
      connections: this.connections.size,
      totalResources: this.timers.size + this.intervals.size + this.connections.size,
      isShuttingDown: this.isShuttingDown,
      timestamp: new Date().toISOString()
    }
  }

  // Auto-cleanup de recursos órfãos
  performMaintenanceCleanup() {
    const before = this.getResourceStats()
    
    // Limpar timers que já executaram
    for (const timerId of this.timers) {
      if (!timerId._destroyed && timerId._idleTimeout <= 0) {
        this.timers.delete(timerId)
      }
    }
    
    // Limpar conexões fechadas
    for (const connection of this.connections) {
      if (connection.destroyed || connection.readyState === 'closed') {
        this.connections.delete(connection)
      }
    }
    
    const after = this.getResourceStats()
    
    if (before.totalResources !== after.totalResources) {
      console.log(`🧹 Maintenance cleanup: ${before.totalResources} -> ${after.totalResources} recursos`)
    }
  }

  // Inicializar sistema completo
  initialize() {
    this.setupGracefulShutdown()
    this.startResourceMonitoring()
    
    // Maintenance cleanup a cada 10 minutos
    this.setInterval(() => {
      this.performMaintenanceCleanup()
    }, 600000)
    
    console.log('🧹 Sistema de cleanup inicializado')
  }
}

// Singleton global
let cleanupInstance = null

export function getCleanupSystem() {
  if (!cleanupInstance) {
    cleanupInstance = new CleanupSystem()
  }
  return cleanupInstance
}

// Funções de conveniência globais
export const cleanupSystem = getCleanupSystem()

export const setTimeout = (callback, delay) => cleanupSystem.setTimeout(callback, delay)
export const setInterval = (callback, interval) => cleanupSystem.setInterval(callback, interval)
export const addEventListener = (target, event, listener, options) => cleanupSystem.addEventListener(target, event, listener, options)

export default cleanupSystem