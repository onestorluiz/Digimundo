/**
 * 🧠 A-MEM SYSTEM - Sistema de Memória Semântica Agêntica
 * Sistema avançado de memória semântica e busca
 */

import { EventEmitter } from 'events'

export class AMemSystem extends EventEmitter {
  constructor() {
    super()
    this.name = 'AMemSystem'
    this.isActive = false
    this.notes = new Map()
    this.semanticIndex = new Map()
  }

  async initialize() {
    console.log('🧠 [AMemSystem] Inicializando sistema A-MEM...')
    this.isActive = true
    this.emit('amem-initialized')
    return { success: true }
  }

  async quickNote(content, tags = []) {
    const note = {
      id: Date.now(),
      content: content,
      tags: tags,
      timestamp: new Date(),
      semantic_score: this.calculateSemanticScore(content)
    }
    
    this.notes.set(note.id, note)
    this.indexSemanticContent(note)
    
    console.log(`📝 [AMemSystem] Nota rápida criada: ${content.substring(0, 50)}...`)
    
    this.emit('nota_registrada', { 
      noteId: note.id, 
      note: { 
        conteudo: note.content, 
        tags: note.tags, 
        metadata: { 
          importance: note.semantic_score 
        } 
      } 
    })
    return note
  }

  async quickSearch(query) {
    const results = []
    
    // Busca por conteúdo
    for (const [id, note] of this.notes) {
      if (note.content.toLowerCase().includes(query.toLowerCase())) {
        results.push({ ...note, relevance: this.calculateRelevance(note, query) })
      }
    }
    
    // Busca semântica
    const semanticResults = this.semanticSearch(query)
    results.push(...semanticResults)
    
    // Remove duplicatas e ordena por relevância
    const uniqueResults = results.filter((result, index, self) => 
      index === self.findIndex(r => r.id === result.id)
    ).sort((a, b) => (b.relevance || 0) - (a.relevance || 0))
    
    console.log(`🔍 [AMemSystem] Busca por "${query}": ${uniqueResults.length} resultados`)
    return uniqueResults
  }

  calculateSemanticScore(content) {
    // Simula cálculo de score semântico
    const words = content.split(' ')
    const complexity = words.length * 0.1
    const uniqueness = new Set(words).size / words.length
    return Math.min(1.0, complexity + uniqueness)
  }

  indexSemanticContent(note) {
    // Extrai palavras-chave para indexação semântica
    const words = note.content.toLowerCase().match(/\b\w+\b/g) || []
    const keywords = words.filter(word => word.length > 3)
    
    keywords.forEach(keyword => {
      if (!this.semanticIndex.has(keyword)) {
        this.semanticIndex.set(keyword, [])
      }
      this.semanticIndex.get(keyword).push(note.id)
    })
  }

  semanticSearch(query) {
    const queryWords = query.toLowerCase().match(/\b\w+\b/g) || []
    const candidateNotes = new Set()
    
    queryWords.forEach(word => {
      if (this.semanticIndex.has(word)) {
        this.semanticIndex.get(word).forEach(noteId => {
          candidateNotes.add(noteId)
        })
      }
    })
    
    return Array.from(candidateNotes).map(id => {
      const note = this.notes.get(id)
      return {
        ...note,
        relevance: this.calculateRelevance(note, query)
      }
    })
  }

  calculateRelevance(note, query) {
    const queryWords = query.toLowerCase().split(' ')
    const noteWords = note.content.toLowerCase().split(' ')
    
    let matchCount = 0
    queryWords.forEach(qWord => {
      if (noteWords.some(nWord => nWord.includes(qWord))) {
        matchCount++
      }
    })
    
    return matchCount / queryWords.length
  }

  getSystemStats() {
    return {
      name: this.name,
      isActive: this.isActive,
      totalNotes: this.notes.size,
      semanticIndex: this.semanticIndex.size,
      timestamp: new Date().toISOString()
    }
  }

  async getStats() {
    const totalNotes = this.notes.size
    const totalConnections = this.semanticIndex.size
    
    // Calcula saúde da memória baseado em métricas
    let memoryHealth = 100
    if (totalNotes === 0) memoryHealth = 0
    else if (totalNotes < 10) memoryHealth = 30
    else if (totalNotes < 50) memoryHealth = 60
    else if (totalNotes < 100) memoryHealth = 80
    
    return {
      name: this.name,
      isActive: this.isActive,
      totalNotes: totalNotes,
      totalConnections: totalConnections,
      memoryHealth: memoryHealth,
      semanticIndexSize: this.semanticIndex.size,
      notes: Array.from(this.notes.values()).slice(-10),
      timestamp: new Date().toISOString()
    }
  }
}

export const sabiamonAMem = new AMemSystem()

export function getSabiamonAMem() {
  return sabiamonAMem
}

export async function quickNote(content, tags = []) {
  return await sabiamonAMem.quickNote(content, tags)
}

export async function quickSearch(query) {
  return await sabiamonAMem.quickSearch(query)
}

export async function connectNotes(noteId1, noteId2, connectionType = 'related') {
  const note1 = sabiamonAMem.notes.get(noteId1)
  const note2 = sabiamonAMem.notes.get(noteId2)
  
  if (note1 && note2) {
    const connection = {
      id: Date.now(),
      note1: noteId1,
      note2: noteId2,
      type: connectionType,
      timestamp: new Date()
    }
    
    console.log(`🔗 [AMemSystem] Notas conectadas: ${noteId1} ↔ ${noteId2}`)
    return connection
  }
  
  return null
}

export default sabiamonAMem