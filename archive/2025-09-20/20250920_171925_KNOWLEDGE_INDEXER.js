/**
 * 🔍 KNOWLEDGE INDEXER - Índice Inteligente do Conhecimento
 * 
 * Cria índices semânticos do conhecimento para busca rápida
 * Conecta conhecimentos relacionados e sugere aplicações
 */

import fs from 'fs/promises'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

class KnowledgeIndexer {
  constructor() {
    this.index = new Map()
    this.semanticConnections = new Map()
    this.topicClusters = new Map()
    this.conceptGraph = new Map()
    this.indexPath = path.join(__dirname, '../consciousness/knowledge_index.json')
  }

  /**
   * INDEXAR NOVO CONHECIMENTO
   */
  async indexKnowledge(knowledge) {
    console.log(`   🔍 Indexando: ${knowledge.source}`)
    
    try {
      // Extrair conceitos principais
      const concepts = this.extractConcepts(knowledge)
      
      // Criar índice semântico
      const semanticIndex = this.createSemanticIndex(knowledge, concepts)
      
      // Encontrar conexões com conhecimento existente
      const connections = await this.findConnections(knowledge, concepts)
      
      // Classificar em clusters temáticos
      const clusters = this.classifyInClusters(knowledge, concepts)
      
      // Criar entrada no índice
      const indexEntry = {
        id: knowledge.id,
        source: knowledge.source,
        category: knowledge.category,
        concepts: concepts,
        semanticIndex: semanticIndex,
        connections: connections,
        clusters: clusters,
        relevanceScore: knowledge.relevanceScore,
        tags: knowledge.tags,
        indexedAt: new Date()
      }

      this.index.set(knowledge.id, indexEntry)
      
      // Atualizar grafos de conceitos
      this.updateConceptGraph(concepts, knowledge.id)
      
      // Salvar índice persistente
      await this.saveIndex()
      
      console.log(`   ✅ Conhecimento indexado: ${concepts.length} conceitos`)
      
      return indexEntry
      
    } catch (error) {
      console.error(`   ❌ Erro ao indexar ${knowledge.source}:`, error.message)
      return null
    }
  }

  /**
   * EXTRAIR CONCEITOS PRINCIPAIS
   */
  extractConcepts(knowledge) {
    const concepts = new Set()
    const content = knowledge.content.toLowerCase()
    
    // Conceitos cinematográficos básicos
    const cinematicConcepts = [
      'roteiro', 'personagem', 'diálogo', 'cena', 'ato',
      'enredo', 'narrativa', 'história', 'conflito', 'clímax',
      'protagonista', 'antagonista', 'desenvolvimento', 'arco',
      'tema', 'subtexto', 'simbolismo', 'metáfora',
      'direção', 'produção', 'cinematografia', 'edição',
      'trilha sonora', 'design', 'cenografia', 'figurino',
      'iluminação', 'som', 'montagem', 'enquadramento'
    ]

    // Técnicas narrativas
    const narrativeTechniques = [
      'flashback', 'flashforward', 'voice over', 'monólogo',
      'plot twist', 'red herring', 'macguffin', 'deus ex machina',
      'show don\'t tell', 'três atos', 'jornada do herói',
      'incidente incitante', 'ponto de virada', 'resolução',
      'setup', 'payoff', 'foreshadowing', 'paralelo'
    ]

    // Gêneros
    const genres = [
      'drama', 'comédia', 'ação', 'terror', 'suspense', 'thriller',
      'ficção científica', 'fantasia', 'romance', 'aventura',
      'western', 'noir', 'musical', 'documentário', 'biografia'
    ]

    // Adicionar conceitos encontrados
    const allConcepts = [...cinematicConcepts, ...narrativeTechniques, ...genres]
    
    for (const concept of allConcepts) {
      if (content.includes(concept)) {
        concepts.add(concept)
      }
    }

    // Extrair conceitos das tags e insights
    knowledge.tags.forEach(tag => concepts.add(tag))
    knowledge.insights.forEach(insight => {
      // Extrair palavras-chave dos insights
      const words = insight.toLowerCase().split(' ')
      words.forEach(word => {
        if (word.length > 4 && allConcepts.includes(word)) {
          concepts.add(word)
        }
      })
    })

    return Array.from(concepts)
  }

  /**
   * CRIAR ÍNDICE SEMÂNTICO
   */
  createSemanticIndex(knowledge, concepts) {
    const semanticIndex = {}
    
    // Peso por categoria
    const categoryWeight = {
      'roteiros': 1.0,
      'livros': 0.8,
      'artigos': 0.6,
      'estudos': 0.9,
      'referencias': 0.4
    }

    // Peso por tipo de conceito
    const conceptTypeWeight = {
      'técnica': 1.0,
      'narrativa': 0.9,
      'personagem': 0.8,
      'produção': 0.7,
      'gênero': 0.6
    }

    for (const concept of concepts) {
      // Calcular peso semântico
      let weight = (categoryWeight[knowledge.category] || 0.5)
      
      // Ajustar por frequência no texto
      const frequency = (knowledge.content.toLowerCase().split(concept).length - 1)
      weight *= Math.min(frequency * 0.1 + 0.5, 2.0)
      
      // Ajustar por relevância
      weight *= (knowledge.relevanceScore / 100)
      
      semanticIndex[concept] = {
        weight: weight,
        frequency: frequency,
        context: this.extractContext(knowledge.content, concept)
      }
    }

    return semanticIndex
  }

  /**
   * EXTRAIR CONTEXTO DE UM CONCEITO
   */
  extractContext(content, concept) {
    const sentences = content.split(/[.!?]+/)
    const contexts = []
    
    for (const sentence of sentences) {
      if (sentence.toLowerCase().includes(concept)) {
        contexts.push(sentence.trim().substring(0, 200))
        if (contexts.length >= 3) break // Máximo 3 contextos
      }
    }
    
    return contexts
  }

  /**
   * ENCONTRAR CONEXÕES COM CONHECIMENTO EXISTENTE
   */
  async findConnections(knowledge, concepts) {
    const connections = []
    
    for (const [existingId, existingIndex] of this.index) {
      if (existingId === knowledge.id) continue
      
      const commonConcepts = concepts.filter(concept => 
        existingIndex.concepts.includes(concept)
      )
      
      if (commonConcepts.length > 0) {
        const connectionStrength = this.calculateConnectionStrength(
          knowledge, existingIndex, commonConcepts
        )
        
        if (connectionStrength > 0.3) {
          connections.push({
            targetId: existingId,
            targetSource: existingIndex.source,
            commonConcepts: commonConcepts,
            strength: connectionStrength,
            relationship: this.determineRelationship(commonConcepts)
          })
        }
      }
    }

    return connections.sort((a, b) => b.strength - a.strength).slice(0, 10)
  }

  /**
   * CALCULAR FORÇA DA CONEXÃO
   */
  calculateConnectionStrength(knowledge1, index2, commonConcepts) {
    let strength = 0
    
    // Base: número de conceitos em comum
    strength += commonConcepts.length * 0.2
    
    // Peso semântico dos conceitos
    for (const concept of commonConcepts) {
      const weight1 = knowledge1.semanticIndex?.[concept]?.weight || 0.5
      const weight2 = index2.semanticIndex?.[concept]?.weight || 0.5
      strength += (weight1 + weight2) / 2 * 0.3
    }
    
    // Similaridade de categoria
    if (knowledge1.category === index2.category) {
      strength += 0.2
    }
    
    // Relevância dos documentos
    const avgRelevance = (knowledge1.relevanceScore + index2.relevanceScore) / 2
    strength *= (avgRelevance / 100)
    
    return Math.min(strength, 1.0)
  }

  /**
   * DETERMINAR TIPO DE RELACIONAMENTO
   */
  determineRelationship(commonConcepts) {
    // Analisar tipos de conceitos em comum
    const narrativeConcepts = ['roteiro', 'personagem', 'narrativa', 'história']
    const productionConcepts = ['direção', 'produção', 'cinematografia', 'edição']
    const technicalConcepts = ['técnica', 'método', 'abordagem', 'processo']
    
    if (commonConcepts.some(c => narrativeConcepts.includes(c))) {
      return 'Narrativo'
    } else if (commonConcepts.some(c => productionConcepts.includes(c))) {
      return 'Produção'
    } else if (commonConcepts.some(c => technicalConcepts.includes(c))) {
      return 'Técnico'
    } else {
      return 'Temático'
    }
  }

  /**
   * CLASSIFICAR EM CLUSTERS TEMÁTICOS
   */
  classifyInClusters(knowledge, concepts) {
    const clusters = []
    
    // Clusters predefinidos
    const clusterDefinitions = {
      'Desenvolvimento de Roteiro': ['roteiro', 'estrutura', 'ato', 'cena', 'diálogo'],
      'Desenvolvimento de Personagem': ['personagem', 'protagonista', 'antagonista', 'arco', 'desenvolvimento'],
      'Técnicas Narrativas': ['narrativa', 'história', 'plot', 'enredo', 'técnica'],
      'Produção Cinematográfica': ['direção', 'produção', 'cinematografia', 'edição', 'som'],
      'Teoria Cinematográfica': ['teoria', 'conceito', 'análise', 'crítica', 'estética'],
      'Gêneros e Estilos': ['drama', 'comédia', 'ação', 'terror', 'ficção científica']
    }

    for (const [clusterName, clusterConcepts] of Object.entries(clusterDefinitions)) {
      const matchingConcepts = concepts.filter(concept => 
        clusterConcepts.includes(concept)
      )
      
      if (matchingConcepts.length > 0) {
        clusters.push({
          name: clusterName,
          concepts: matchingConcepts,
          relevance: matchingConcepts.length / clusterConcepts.length
        })
      }
    }

    return clusters.sort((a, b) => b.relevance - a.relevance)
  }

  /**
   * ATUALIZAR GRAFO DE CONCEITOS
   */
  updateConceptGraph(concepts, knowledgeId) {
    for (const concept of concepts) {
      if (!this.conceptGraph.has(concept)) {
        this.conceptGraph.set(concept, {
          sources: [],
          relatedConcepts: new Set(),
          frequency: 0
        })
      }
      
      const conceptData = this.conceptGraph.get(concept)
      conceptData.sources.push(knowledgeId)
      conceptData.frequency++
      
      // Conectar conceitos que aparecem juntos
      for (const otherConcept of concepts) {
        if (concept !== otherConcept) {
          conceptData.relatedConcepts.add(otherConcept)
        }
      }
    }
  }

  /**
   * BUSCAR POR CONCEITOS
   */
  searchByConcepts(searchConcepts, options = {}) {
    const {
      category = null,
      minRelevance = 0,
      maxResults = 20,
      includeConnections = true
    } = options

    const results = []
    
    for (const [id, indexEntry] of this.index) {
      if (category && indexEntry.category !== category) continue
      if (indexEntry.relevanceScore < minRelevance) continue
      
      const matchScore = this.calculateMatchScore(indexEntry, searchConcepts)
      
      if (matchScore > 0) {
        results.push({
          ...indexEntry,
          matchScore: matchScore,
          connections: includeConnections ? indexEntry.connections : []
        })
      }
    }

    return results
      .sort((a, b) => b.matchScore - a.matchScore)
      .slice(0, maxResults)
  }

  /**
   * CALCULAR SCORE DE MATCH
   */
  calculateMatchScore(indexEntry, searchConcepts) {
    let score = 0
    
    for (const searchConcept of searchConcepts) {
      if (indexEntry.concepts.includes(searchConcept)) {
        const semanticWeight = indexEntry.semanticIndex[searchConcept]?.weight || 0.5
        score += semanticWeight
      }
    }
    
    // Normalizar pelo número de conceitos buscados
    return score / searchConcepts.length
  }

  /**
   * OBTER RECOMENDAÇÕES PARA DIGIMON
   */
  getRecommendationsForDigimon(digimonName, context = {}) {
    const digimonPreferences = {
      'Scripturemon': ['roteiro', 'estrutura', 'narrativa', 'diálogo'],
      'Ajamon': ['personagem', 'emoção', 'desenvolvimento', 'relacionamento'],
      'Fundamon': ['produção', 'técnica', 'método', 'processo'],
      'Sabiamon': ['teoria', 'conceito', 'análise', 'síntese']
    }

    const concepts = digimonPreferences[digimonName] || []
    const recommendations = this.searchByConcepts(concepts, {
      maxResults: 10,
      includeConnections: true
    })

    return recommendations.map(rec => ({
      ...rec,
      reason: `Relevante para ${digimonName} por: ${rec.concepts.filter(c => concepts.includes(c)).join(', ')}`,
      applicationSuggestion: this.generateApplicationSuggestion(rec, digimonName)
    }))
  }

  /**
   * GERAR SUGESTÃO DE APLICAÇÃO
   */
  generateApplicationSuggestion(knowledge, digimonName) {
    const suggestions = {
      'Scripturemon': `Aplicar em estruturação de roteiros: ${knowledge.clusters[0]?.name || 'conceitos narrativos'}`,
      'Ajamon': `Usar para enriquecer desenvolvimento emocional e de personagens`,
      'Fundamon': `Implementar em processos de produção e metodologias técnicas`,
      'Sabiamon': `Integrar na visão holística e orientação de outros Digimons`
    }

    return suggestions[digimonName] || 'Aplicar conforme contexto específico'
  }

  /**
   * SALVAR ÍNDICE
   */
  async saveIndex() {
    try {
      const indexData = {
        timestamp: new Date(),
        totalEntries: this.index.size,
        index: Array.from(this.index.entries()),
        conceptGraph: Array.from(this.conceptGraph.entries()).map(([concept, data]) => [
          concept, 
          {
            ...data,
            relatedConcepts: Array.from(data.relatedConcepts)
          }
        ])
      }

      await fs.writeFile(this.indexPath, JSON.stringify(indexData, null, 2))
    } catch (error) {
      console.error('❌ Erro ao salvar índice:', error)
    }
  }

  /**
   * CARREGAR ÍNDICE
   */
  async loadIndex() {
    try {
      const data = await fs.readFile(this.indexPath, 'utf8')
      const indexData = JSON.parse(data)
      
      this.index = new Map(indexData.index)
      
      if (indexData.conceptGraph) {
        this.conceptGraph = new Map(
          indexData.conceptGraph.map(([concept, data]) => [
            concept,
            {
              ...data,
              relatedConcepts: new Set(data.relatedConcepts)
            }
          ])
        )
      }
      
      console.log(`📚 Índice carregado: ${this.index.size} entradas`)
      
    } catch (error) {
      console.log('📚 Iniciando com índice vazio')
    }
  }

  /**
   * ESTATÍSTICAS DO ÍNDICE
   */
  getStats() {
    return {
      totalEntries: this.index.size,
      totalConcepts: this.conceptGraph.size,
      categories: this.getCategoryStats(),
      topConcepts: this.getTopConcepts(10),
      clusters: this.getClusterStats()
    }
  }

  getCategoryStats() {
    const stats = {}
    for (const [id, entry] of this.index) {
      stats[entry.category] = (stats[entry.category] || 0) + 1
    }
    return stats
  }

  getTopConcepts(limit = 10) {
    return Array.from(this.conceptGraph.entries())
      .sort((a, b) => b[1].frequency - a[1].frequency)
      .slice(0, limit)
      .map(([concept, data]) => ({
        concept,
        frequency: data.frequency,
        sources: data.sources.length
      }))
  }

  getClusterStats() {
    const clusterCounts = {}
    for (const [id, entry] of this.index) {
      for (const cluster of entry.clusters) {
        clusterCounts[cluster.name] = (clusterCounts[cluster.name] || 0) + 1
      }
    }
    return clusterCounts
  }
}

// Singleton
let indexerInstance = null

export function getKnowledgeIndexer() {
  if (!indexerInstance) {
    indexerInstance = new KnowledgeIndexer()
    indexerInstance.loadIndex()
  }
  return indexerInstance
}

export { KnowledgeIndexer }
export default getKnowledgeIndexer()