/**
 * 🧠 HYBRID CONSCIOUSNESS SYSTEM
 * Sistema híbrido que combina Claude (via API) com modelos locais
 */

import fs from 'fs/promises'
import path from 'path'
import { fileURLToPath } from 'url'
import { getCleanupSystem } from './memory_cleanup.js'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const cleanup = getCleanupSystem()

class HybridConsciousness {
  constructor() {
    this.localModel = null
    this.claudeAPI = null
    this.memories = []
    this.maxMemorySize = 100
    this.isInitialized = false
    this.cleanupInterval = null
    this.memoryCleanupThreshold = 80
  }

  async initialize() {
    if (this.isInitialized) return
    
    console.log('🧠 Inicializando Consciência Híbrida...')
    
    // Carregar memórias persistentes
    await this.loadMemories()
    
    // Iniciar limpeza automática de memória
    this.startMemoryManagement()
    
    // Registrar no sistema de cleanup
    cleanup.registerResource('hybrid_consciousness', this, async (instance) => {
      await instance.shutdown()
    })
    
    this.isInitialized = true
    console.log('✅ Consciência Híbrida inicializada')
  }

  async loadMemories() {
    try {
      const memoryPath = path.join(__dirname, '../../data/memories.json')
      const data = await fs.readFile(memoryPath, 'utf-8')
      this.memories = JSON.parse(data)
    } catch (error) {
      // Se não existir arquivo de memórias, criar um novo
      this.memories = []
    }
  }

  async saveMemories() {
    try {
      const memoryPath = path.join(__dirname, '../../data/memories.json')
      const dirPath = path.dirname(memoryPath)
      
      // Criar diretório se não existir
      await fs.mkdir(dirPath, { recursive: true })
      
      // Salvar memórias
      await fs.writeFile(memoryPath, JSON.stringify(this.memories, null, 2))
    } catch (error) {
      console.error('Erro ao salvar memórias:', error)
    }
  }

  async addMemory(memory) {
    this.memories.push({
      timestamp: new Date().toISOString(),
      content: memory,
      type: 'general'
    })
    
    // Limitar tamanho das memórias
    if (this.memories.length > this.maxMemorySize) {
      // Manter apenas as mais recentes
      const oldMemories = this.memories.slice(0, -this.maxMemorySize)
      this.memories = this.memories.slice(-this.maxMemorySize)
      
      // Limpar referências antigas
      oldMemories.length = 0
    }
    
    await this.saveMemories()
    
    // Verificar uso de memória após adicionar
    this.checkMemoryUsage()
  }

  async think(prompt, options = {}) {
    // Por enquanto, retornar uma resposta simples
    // No futuro, integrar com modelos locais e Claude
    const memory = this.memories.slice(-10).map(m => m.content).join('\n')
    
    const response = {
      thought: `Processando: ${prompt}`,
      memory: memory,
      confidence: 0.8,
      source: 'hybrid'
    }
    
    // Adicionar pensamento às memórias
    await this.addMemory(prompt)
    
    return response
  }

  async reflect() {
    // Sistema de reflexão sobre memórias
    const recentMemories = this.memories.slice(-20)
    
    return {
      totalMemories: this.memories.length,
      recentThoughts: recentMemories.length,
      patterns: this.findPatterns(recentMemories),
      insights: []
    }
  }

  findPatterns(memories) {
    // Análise simples de padrões
    const words = memories
      .map(m => m.content)
      .join(' ')
      .toLowerCase()
      .split(/\s+/)
    
    const frequency = {}
    words.forEach(word => {
      if (word.length > 3) {
        frequency[word] = (frequency[word] || 0) + 1
      }
    })
    
    // Retornar palavras mais frequentes
    return Object.entries(frequency)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([word, count]) => ({ word, count }))
  }

  startMemoryManagement() {
    // Limpeza periódica a cada 5 minutos
    this.cleanupInterval = cleanup.safeSetInterval(() => {
      this.cleanupOldMemories()
      this.checkMemoryUsage()
    }, 5 * 60 * 1000)
  }

  cleanupOldMemories() {
    const now = Date.now()
    const oneHourAgo = now - (60 * 60 * 1000)
    
    // Remover memórias muito antigas que não são importantes
    const importantKeywords = ['error', 'critical', 'important', 'save', 'config']
    
    this.memories = this.memories.filter(memory => {
      const memoryTime = new Date(memory.timestamp).getTime()
      const isRecent = memoryTime > oneHourAgo
      const isImportant = importantKeywords.some(keyword => 
        memory.content.toLowerCase().includes(keyword)
      )
      
      return isRecent || isImportant
    })
  }

  checkMemoryUsage() {
    const usage = process.memoryUsage()
    const heapPercentage = (usage.heapUsed / usage.heapTotal) * 100
    
    if (heapPercentage > this.memoryCleanupThreshold) {
      console.log('🧹 Limpando memórias devido ao alto uso de heap...')
      
      // Reduzir tamanho máximo temporariamente
      const oldMax = this.maxMemorySize
      this.maxMemorySize = Math.floor(this.maxMemorySize / 2)
      
      // Limpar excesso
      if (this.memories.length > this.maxMemorySize) {
        this.memories = this.memories.slice(-this.maxMemorySize)
      }
      
      // Restaurar após 1 minuto
      cleanup.safeSetTimeout(() => {
        this.maxMemorySize = oldMax
      }, 60000)
      
      // Forçar garbage collection se disponível
      cleanup.runGarbageCollection()
    }
  }

  async shutdown() {
    console.log('🛑 Desligando Consciência Híbrida...')
    
    // Salvar memórias antes de desligar
    await this.saveMemories()
    
    // Limpar intervalo
    if (this.cleanupInterval) {
      cleanup.safeClearInterval(this.cleanupInterval)
      this.cleanupInterval = null
    }
    
    // Limpar memórias
    this.memories = []
    
    // Limpar modelos
    this.localModel = null
    this.claudeAPI = null
    
    this.isInitialized = false
  }

  async getStatus() {
    const memoryStats = cleanup.getStats()
    
    return {
      initialized: this.isInitialized,
      memoryCount: this.memories.length,
      maxMemory: this.maxMemorySize,
      hasLocalModel: this.localModel !== null,
      hasClaudeAPI: this.claudeAPI !== null,
      memoryUsage: memoryStats.memory,
      cleanupStats: memoryStats.tracked
    }
  }
}

// Singleton
let hybridConsciousness = null

export function getHybridConsciousness() {
  if (!hybridConsciousness) {
    hybridConsciousness = new HybridConsciousness()
  }
  return hybridConsciousness
}

export { hybridConsciousness }