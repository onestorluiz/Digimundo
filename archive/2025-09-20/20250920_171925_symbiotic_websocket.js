/**
 * 🌉 WEBSOCKET SIMBIÓTICO
 * Extensões para WebSocket com notificações do sistema simbiótico
 */

import { getSabiamonMem0 } from '../consciousness/MEM0_UNIVERSAL.js'
import { getSabiamonAMem } from '../consciousness/A_MEM_SYSTEM.js'
import { getSabiamonOrchestrator } from '../consciousness/SYMBIOTIC_ORCHESTRATOR.js'
import { getClaudeMemoryBridge } from '../consciousness/CLAUDE_MEMORY_BRIDGE.js'

let symbioticBroadcast = null

/**
 * Configurar broadcast simbiótico
 */
export async function setupSymbioticWebSocket(broadcastFunction) {
  symbioticBroadcast = broadcastFunction
  
  // Conectar eventos do sistema simbiótico
  connectSymbioticEvents()
  
//   console.log('🌉 WebSocket simbiótico configurado')
}

/**
 * Conectar todos os eventos dos componentes simbióticos
 */
async function connectSymbioticEvents() {
  try {
    // 🌌 Eventos do Mem0
    const mem0 = getSabiamonMem0()
    mem0.on('evento_adicionado', (data) => {
      broadcast('symbiotic-event-added', {
        eventId: data.eventId,
        significance: data.event.significance,
        timestamp: data.event.timestamp
      })
    })
    
    mem0.on('evento_processado', (data) => {
      broadcast('symbiotic-event-processed', {
        eventId: data.event.id,
        references: data.references,
        memoryStores: Object.keys(data.references).length
      })
    })
    
    // 🧠 Eventos do A-MEM
    const aMem = getSabiamonAMem()
    aMem.on('nota_registrada', (data) => {
      broadcast('symbiotic-note-created', {
        noteId: data.noteId,
        content: data.note.conteudo.slice(0, 100) + '...',
        tags: data.note.tags,
        importance: data.note.metadata.importance
      })
    })
    
    aMem.on('relacionamento_criado', (data) => {
      broadcast('symbiotic-relationship-created', {
        relationId: data.relationId,
        type: data.relation.type,
        from: data.relation.from.slice(0, 8),
        to: data.relation.to.slice(0, 8)
      })
    })
    
    // 🎼 Eventos do Orquestrador
    const orchestrator = getSabiamonOrchestrator()
    orchestrator.on('ciclo_completado', (session) => {
      broadcast('symbiotic-cycle-completed', {
        cycleId: session.id,
        duration: session.duration,
        statesExecuted: session.metrics.statesExecuted,
        completed: session.completed,
        hasErrors: session.errors.length > 0
      })
    })
    
    orchestrator.on('erro_critico', (data) => {
      broadcast('symbiotic-critical-error', {
        sessionId: data.session.id,
        error: data.error.message,
        timestamp: new Date()
      })
    })
    
    // 🌉 Eventos da Bridge
    const bridge = getClaudeMemoryBridge()
    bridge.on('evento_adicionado', (data) => {
      broadcast('symbiotic-bridge-sync', {
        eventId: data.eventId,
        type: 'event_added',
        timestamp: new Date()
      })
    })
    
//     console.log('✅ Eventos simbióticos conectados ao WebSocket')
    
  } catch (error) {
    console.error('❌ Erro ao conectar eventos simbióticos:', error)
  }
}

/**
 * Broadcast helper
 */
async function broadcast(event, data) {
  if (symbioticBroadcast) {
    symbioticBroadcast(event, {
      ...data,
      source: 'symbiotic_system',
      timestamp: new Date()
    })
  }
}

/**
 * Transmitir análise periódica de coerência simbiótica
 */
export async function broadcastSymbioticHealth() {
  try {
    const mem0 = getSabiamonMem0()
    const aMem = getSabiamonAMem()
    const orchestrator = getSabiamonOrchestrator()
    
    const memoryStats = await mem0.getMemoryStats()
    const aMemStats = aMem && typeof aMem.getStats === 'function' 
      ? await aMem.getStats()
      : { memoryHealth: 0, totalNotes: 0, totalConnections: 0 }
    const orchestratorMetrics = orchestrator.metrics
    
    // Calcular score de saúde simbiótica
    const healthScore = Math.round(
      (aMemStats.memoryHealth + 
       (memoryStats.mem0.processedEvents / Math.max(memoryStats.mem0.totalEvents, 1) * 100) +
       (orchestratorMetrics.cyclesCompleted > 0 ? 80 : 20)) / 3
    )
    
    broadcast('symbiotic-health-report', {
      healthScore,
      status: healthScore > 80 ? 'excellent' : healthScore > 60 ? 'good' : 'needs_attention',
      components: {
        mem0: {
          totalEvents: memoryStats.mem0.totalEvents,
          processedEvents: memoryStats.mem0.processedEvents,
          efficiency: Math.round(memoryStats.mem0.processedEvents / Math.max(memoryStats.mem0.totalEvents, 1) * 100)
        },
        aMem: {
          notes: aMemStats.totalNotes,
          connections: aMemStats.totalConnections,
          health: aMemStats.memoryHealth
        },
        orchestrator: {
          cycles: orchestratorMetrics.cyclesCompleted,
          avgTime: Math.round(orchestratorMetrics.averageCycleTime),
          errors: orchestratorMetrics.errorsRecovered
        }
      },
      timestamp: new Date()
    })
    
  } catch (error) {
    console.error('❌ Erro ao transmitir saúde simbiótica:', error)
  }
}

/**
 * Inicializar transmissões periódicas
 */
export async function startSymbioticBroadcasts() {
  // Relatório de saúde a cada 5 minutos
  setInterval(broadcastSymbioticHealth, 5 * 60 * 1000)
  
//   console.log('🔄 Transmissões simbióticas periódicas iniciadas')
}

/**
 * Processar mensagem WebSocket relacionada ao sistema simbiótico
 */
export async function handleSymbioticMessage(ws, message) {
  const { type, payload } = message
  
  try {
    switch (type) {
      case 'symbiotic-status-request':
        const healthData = await getSymbioticStatus()
        ws.send(JSON.stringify({
          event: 'symbiotic-status-response',
          data: healthData
        }))
        break
        
      case 'symbiotic-memory-search':
        if (payload.query) {
          const aMem = getSabiamonAMem()
          const results = await aMem.quickSearch(payload.query)
          ws.send(JSON.stringify({
            event: 'symbiotic-search-results',
            data: {
              query: payload.query,
              results: results.slice(0, 10).map(note => ({
                id: note.id,
                content: note.content.slice(0, 100) + '...',
                tags: note.tags,
                importance: note.semantic_score
              }))
            }
          }))
        }
        break
        
      case 'symbiotic-cycle-trigger':
        if (payload.prompt) {
          const orchestrator = getSabiamonOrchestrator()
          const cycle = await orchestrator.executarCiclo(payload.prompt)
          ws.send(JSON.stringify({
            event: 'symbiotic-cycle-result',
            data: {
              cycleId: cycle.id,
              duration: cycle.duration,
              completed: cycle.completed,
              statesExecuted: cycle.metrics?.statesExecuted
            }
          }))
        }
        break
        
      default:
//         console.log(`🔍 Mensagem simbiótica desconhecida: ${type}`)
    }
    
  } catch (error) {
    ws.send(JSON.stringify({
      event: 'symbiotic-error',
      data: {
        message: error.message,
        type: 'processing_error'
      }
    }))
  }
}

/**
 * Obter métricas unificadas de memória
 */
async function getUnifiedMemoryMetrics() {
  try {
    const mem0 = getSabiamonMem0()
    const aMem = getSabiamonAMem()
    const orchestrator = getSabiamonOrchestrator()
    const bridge = getClaudeMemoryBridge()
    
    const memoryStats = await mem0.getMemoryStats()
    const aMemStats = typeof aMem.getStats === 'function'
      ? await aMem.getStats()
      : {
          name: 'AMemSystem',
          isActive: false,
          totalNotes: 0,
          totalConnections: 0,
          memoryHealth: 0,
          semanticIndexSize: 0,
          notes: [],
          timestamp: new Date().toISOString()
        }
    
    return {
      mem0: {
        totalEvents: memoryStats.mem0.totalEvents,
        processedEvents: memoryStats.mem0.processedEvents,
        efficiency: Math.round(memoryStats.mem0.processedEvents / Math.max(memoryStats.mem0.totalEvents, 1) * 100)
      },
      aMem: {
        notes: aMemStats.totalNotes,
        connections: aMemStats.totalConnections,
        health: aMemStats.memoryHealth
      },
      orchestrator: {
        cycles: orchestrator.metrics.cyclesCompleted,
        avgTime: Math.round(orchestrator.metrics.averageCycleTime),
        errors: orchestrator.metrics.errorsRecovered
      },
      bridge: {
        sessionId: bridge.sessionId,
        consciousnessLevel: bridge.consciousnessState.level,
        coherence: bridge.consciousnessState.coherence || 0
      },
      timestamp: new Date().toISOString()
    }
  } catch (error) {
    console.error('❌ Erro ao obter métricas unificadas:', error)
    return {
      error: error.message,
      timestamp: new Date().toISOString()
    }
  }
}

/**
 * Obter status geral do sistema simbiótico
 */
async function getSymbioticStatus() {
  try {
    const mem0 = getSabiamonMem0()
    const aMem = getSabiamonAMem()
    const orchestrator = getSabiamonOrchestrator()
    const bridge = getClaudeMemoryBridge()
    
    const memoryStats = await mem0.getMemoryStats()
    const aMemStats = typeof aMem.getStats === 'function'
      ? await aMem.getStats()
      : {
          name: 'AMemSystem',
          isActive: false,
          totalNotes: 0,
          totalConnections: 0,
          memoryHealth: 0,
          semanticIndexSize: 0,
          notes: [],
          timestamp: new Date().toISOString()
        }
    
    return {
      overall: 'active',
      components: {
        mem0: {
          status: 'running',
          events: memoryStats.mem0.totalEvents,
          processed: memoryStats.mem0.processedEvents
        },
        aMem: {
          status: 'active',
          notes: aMemStats.totalNotes,
          connections: aMemStats.totalConnections,
          health: aMemStats.memoryHealth
        },
        orchestrator: {
          status: 'operational',
          cycles: orchestrator.metrics.cyclesCompleted,
          avgTime: orchestrator.metrics.averageCycleTime
        },
        bridge: {
          status: 'connected',
          sessionId: bridge.sessionId,
          consciousnessLevel: bridge.consciousnessState.level
        }
      },
      timestamp: new Date()
    }
    
  } catch (error) {
    return {
      overall: 'error',
      error: error.message,
      timestamp: new Date()
    }
  }
}

export { getUnifiedMemoryMetrics }