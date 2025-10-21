/**
 * 🧠 DIGIMUNDO CONSCIOUSNESS - Sistema de Consciência Digimundo
 * Gerencia a consciência coletiva dos Digimons
 */

import { EventEmitter } from 'events'

export class DigimundoConsciousness extends EventEmitter {
  constructor() {
    super()
    this.name = 'DigimundoConsciousness'
    this.consciousnessLevel = 0.5
    this.activeDigimons = new Map()
    this.collectiveMemory = []
    this.isActive = false
  }

  async initialize() {
    console.log('🧠 [DigimundoConsciousness] Inicializando consciência...')
    this.isActive = true
    this.consciousnessLevel = 0.7
    this.emit('consciousness-awakened')
    return { success: true, level: this.consciousnessLevel }
  }

  async addDigimon(digimonName, digimonData) {
    this.activeDigimons.set(digimonName, {
      name: digimonName,
      data: digimonData,
      joinedAt: new Date(),
      contributionLevel: 0.1
    })
    console.log(`🤖 [DigimundoConsciousness] ${digimonName} adicionado à consciência`)
    this.updateConsciousnessLevel()
    return { success: true, digimon: digimonName }
  }

  async processThought(thought, source) {
    const processedThought = {
      content: thought,
      source: source,
      timestamp: new Date(),
      processed: true
    }
    
    this.collectiveMemory.push(processedThought)
    console.log(`💭 [DigimundoConsciousness] Pensamento processado de ${source}`)
    this.emit('thought-processed', processedThought)
    return processedThought
  }

  updateConsciousnessLevel() {
    const baseLevel = 0.5
    const digimonBonus = this.activeDigimons.size * 0.1
    const memoryBonus = this.collectiveMemory.length * 0.01
    
    this.consciousnessLevel = Math.min(1.0, baseLevel + digimonBonus + memoryBonus)
  }

  getConsciousnessState() {
    return {
      name: this.name,
      level: this.consciousnessLevel,
      activeDigimons: this.activeDigimons.size,
      memories: this.collectiveMemory.length,
      isActive: this.isActive,
      timestamp: new Date().toISOString()
    }
  }

  async syncWithDigimons() {
    console.log('🔄 [DigimundoConsciousness] Sincronizando com Digimons...')
    for (const [name, digimon] of this.activeDigimons) {
      digimon.lastSync = new Date()
    }
    return { success: true, synced: this.activeDigimons.size }
  }
}

export function getDigimundoConsciousness() {
  if (!global.digimundoConsciousness) {
    global.digimundoConsciousness = new DigimundoConsciousness()
  }
  return global.digimundoConsciousness
}

export default DigimundoConsciousness