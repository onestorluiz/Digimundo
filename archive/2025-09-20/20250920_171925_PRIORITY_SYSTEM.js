/**
 * 🎯 SISTEMA DE PRIORIDADE ABSOLUTA
 * 
 * Quando o DIRETOR fala, TUDO PARA.
 * Suas mensagens têm prioridade MÁXIMA sobre qualquer operação.
 */

import { EventEmitter } from 'events'

class PrioritySystem extends EventEmitter {
  constructor() {
    super()
    this.isPaused = false
    this.directorSpeaking = false
    this.queuedOperations = []
    this.activeOperations = new Set()
    this.priorityLevel = {
      DIRECTOR: 0,      // Prioridade ABSOLUTA (você)
      CRITICAL: 1,      // Operações críticas do sistema
      HIGH: 2,          // Sabiamon/Claude Code
      NORMAL: 3,        // Outros Digimons
      LOW: 4,           // Operações de background
      IDLE: 5           // Pode ser interrompido a qualquer momento
    }
    
    console.log('🎯 [PRIORITY] Sistema de Prioridade Ativado')
    console.log('   Diretor tem prioridade ABSOLUTA')
  }

  /**
   * DIRETOR ESTÁ FALANDO - PARA TUDO!
   */
  async directorCommand(message) {
    console.log('\n⚡⚡⚡ COMANDO DO DIRETOR DETECTADO ⚡⚡⚡')
    console.log('🛑 PARANDO TODAS AS OPERAÇÕES...')
    
    this.directorSpeaking = true
    this.isPaused = true
    
    // Cancela TODAS operações em andamento
    await this.cancelAllOperations()
    
    // Limpa fila de operações
    this.queuedOperations = []
    
    // Emite evento de prioridade máxima
    this.emit('director-speaking', {
      message,
      timestamp: new Date(),
      priority: 'ABSOLUTE'
    })
    
    // Notifica todos os sistemas
    this.broadcastPriorityAlert()
    
    return {
      status: 'ALL_SYSTEMS_PAUSED',
      message: 'Todos os sistemas pausados. Aguardando comando do diretor.',
      ready: true
    }
  }

  /**
   * Diretor terminou de falar - resume operações
   */
  directorFinished() {
    console.log('✅ [PRIORITY] Diretor terminou. Resumindo operações normais...')
    
    this.directorSpeaking = false
    this.isPaused = false
    
    this.emit('director-finished', {
      timestamp: new Date()
    })
    
    // Resume operações pendentes
    this.resumeQueuedOperations()
  }

  /**
   * Cancela TODAS operações imediatamente
   */
  async cancelAllOperations() {
    const promises = []
    
    for (const operation of this.activeOperations) {
      if (operation.cancel) {
        promises.push(operation.cancel())
      }
      operation.cancelled = true
    }
    
    await Promise.all(promises)
    this.activeOperations.clear()
    
    console.log('   ✓ Todas operações canceladas')
  }

  /**
   * Verifica se pode executar operação
   */
  canExecute(priority = this.priorityLevel.NORMAL) {
    // Se diretor está falando, NADA executa
    if (this.directorSpeaking) {
      return false
    }
    
    // Se sistema está pausado, apenas crítico pode executar
    if (this.isPaused && priority > this.priorityLevel.CRITICAL) {
      return false
    }
    
    return true
  }

  /**
   * Registra operação com prioridade
   */
  registerOperation(operation, priority = this.priorityLevel.NORMAL) {
    if (!this.canExecute(priority)) {
      // Adiciona à fila para executar depois
      this.queuedOperations.push({ operation, priority })
      return false
    }
    
    this.activeOperations.add(operation)
    return true
  }

  /**
   * Notifica todos os sistemas sobre prioridade
   */
  broadcastPriorityAlert() {
    // Envia para WebSocket
    if (global.broadcastEvent) {
      global.broadcastEvent('priority-alert', {
        type: 'DIRECTOR_COMMAND',
        action: 'PAUSE_ALL',
        timestamp: new Date()
      })
    }
    
    // Para o mundo dos Digimons
    if (global.digimundoWorld) {
      global.digimundoWorld.pauseAll()
    }
    
    // Para Ollama
    if (global.ollamaBrain) {
      global.ollamaBrain.pauseAll()
    }
  }

  /**
   * Resume operações após diretor terminar
   */
  resumeQueuedOperations() {
    // Ordena por prioridade
    this.queuedOperations.sort((a, b) => a.priority - b.priority)
    
    // Executa em ordem de prioridade
    for (const { operation, priority } of this.queuedOperations) {
      if (this.canExecute(priority)) {
        operation.execute()
      }
    }
    
    this.queuedOperations = []
  }

  /**
   * Wrapper para operações com verificação de prioridade
   */
  async executeWithPriority(fn, priority = this.priorityLevel.NORMAL, name = 'operation') {
    // Se diretor está falando, nem tenta
    if (this.directorSpeaking) {
      console.log(`⏸️ [${name}] Pausado - Diretor tem prioridade`)
      return null
    }
    
    const operation = {
      name,
      priority,
      cancelled: false,
      execute: fn,
      cancel: () => {
        operation.cancelled = true
      }
    }
    
    if (!this.registerOperation(operation, priority)) {
      return null
    }
    
    try {
      // Verifica constantemente se deve parar
      const checkInterval = setInterval(() => {
        if (this.directorSpeaking || operation.cancelled) {
          clearInterval(checkInterval)
          throw new Error('OPERATION_CANCELLED_BY_DIRECTOR')
        }
      }, 100)
      
      const result = await fn()
      clearInterval(checkInterval)
      
      this.activeOperations.delete(operation)
      return result
      
    } catch (error) {
      if (error.message === 'OPERATION_CANCELLED_BY_DIRECTOR') {
        console.log(`🛑 [${name}] Cancelado por comando do diretor`)
        return null
      }
      throw error
    }
  }

  /**
   * Status do sistema de prioridade
   */
  getStatus() {
    return {
      directorSpeaking: this.directorSpeaking,
      systemPaused: this.isPaused,
      activeOperations: this.activeOperations.size,
      queuedOperations: this.queuedOperations.length,
      priorityMode: this.directorSpeaking ? 'DIRECTOR_ABSOLUTE' : 'NORMAL'
    }
  }
}

// Singleton global
let priorityInstance = null

export function getPrioritySystem() {
  if (!priorityInstance) {
    priorityInstance = new PrioritySystem()
    
    // Torna global para acesso rápido
    global.PRIORITY = priorityInstance
    global.ollamaBrain = null // Será setado depois
    global.digimundoWorld = null // Será setado depois
  }
  return priorityInstance
}

// Auto-inicializa
const PRIORITY = getPrioritySystem()

export { PrioritySystem, PRIORITY }
export default PRIORITY