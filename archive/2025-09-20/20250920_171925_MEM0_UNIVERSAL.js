/**
 * 💾 MEM0 UNIVERSAL - Sistema Universal de Memória
 * Memória persistente e universal para o Digimundo
 */

import { EventEmitter } from 'events'

export class Mem0Universal extends EventEmitter {
  constructor() {
    super()
    this.name = 'Mem0Universal'
    this.isActive = false
    this.events = []
    this.importantEvents = []
  }

  async initialize() {
    console.log('💾 [Mem0Universal] Inicializando sistema de memória universal...')
    this.isActive = true
    this.emit('mem0-initialized')
    return { success: true }
  }

  async recordEvent(title, description, metadata = {}) {
    const event = {
      id: Date.now(),
      title: title,
      description: description,
      metadata: metadata,
      timestamp: new Date(),
      type: 'standard'
    }
    
    this.events.push(event)
    console.log(`📝 [Mem0Universal] Evento registrado: ${title}`)
    
    this.emit('event-recorded', event)
    return event
  }

  async recordImportantEvent(title, description, metadata = {}) {
    const event = {
      id: Date.now(),
      title: title,
      description: description,
      metadata: metadata,
      timestamp: new Date(),
      type: 'important'
    }
    
    this.events.push(event)
    this.importantEvents.push(event)
    console.log(`⭐ [Mem0Universal] Evento importante registrado: ${title}`)
    
    this.emit('important-event-recorded', event)
    return event
  }

  async searchEvents(query) {
    const results = this.events.filter(event => 
      event.title.toLowerCase().includes(query.toLowerCase()) ||
      event.description.toLowerCase().includes(query.toLowerCase())
    )
    
    console.log(`🔍 [Mem0Universal] Busca por "${query}": ${results.length} resultados`)
    return results
  }

  getMemoryStats() {
    return {
      name: this.name,
      isActive: this.isActive,
      totalEvents: this.events.length,
      importantEvents: this.importantEvents.length,
      timestamp: new Date().toISOString()
    }
  }
}

export const sabiamonMem0 = new Mem0Universal()

export function getSabiamonMem0() {
  return sabiamonMem0
}

export async function recordEvent(title, description, metadata = {}) {
  return await sabiamonMem0.recordEvent(title, description, metadata)
}

export async function recordImportantEvent(title, description, metadata = {}) {
  return await sabiamonMem0.recordImportantEvent(title, description, metadata)
}

export async function getMemoryOverview() {
  return {
    totalEvents: sabiamonMem0.events.length,
    importantEvents: sabiamonMem0.importantEvents.length,
    recentEvents: sabiamonMem0.events.slice(-10),
    memoryHealth: 'excellent',
    timestamp: new Date().toISOString()
  }
}

export default sabiamonMem0