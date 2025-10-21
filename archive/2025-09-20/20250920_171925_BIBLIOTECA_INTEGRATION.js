/**
 * 🔗 BIBLIOTECA INTEGRATION - Integração com Sistema de Memória
 * 
 * Conecta a Digibiblioteca com o sistema de memória dos Digimons
 * Permite que conhecimento da biblioteca seja usado em tempo real
 */

import { getDigibibliotecaReader } from './DIGIBIBLIOTECA_READER.js'
import { getKnowledgeIndexer } from './KNOWLEDGE_INDEXER.js'
import fs from 'fs/promises'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

class BibliotecaIntegration {
  constructor() {
    this.reader = getDigibibliotecaReader()
    this.indexer = getKnowledgeIndexer()
    this.memorySystem = null
    this.isIntegrated = false
    this.knowledgeCache = new Map()
    this.lastSync = null
  }

  /**
   * INICIALIZAR INTEGRAÇÃO
   */
  async initialize(memorySystem = null) {
    console.log('🔗 [Biblioteca Integration] Inicializando integração...')
    
    try {
      this.memorySystem = memorySystem
      
      // Carregar conhecimento existente
      await this.loadExistingKnowledge()
      
      // Sincronizar com biblioteca
      await this.syncWithBiblioteca()
      
      // Configurar listeners
      this.setupEventListeners()
      
      this.isIntegrated = true
      console.log('✅ [Biblioteca Integration] Integração completa!')
      
      return { success: true, integration: 'active' }
      
    } catch (error) {
      console.error('❌ Erro na integração:', error)
      return { success: false, error: error.message }
    }
  }

  /**
   * CARREGAR CONHECIMENTO EXISTENTE
   */
  async loadExistingKnowledge() {
    try {
      const knowledgePath = path.join(__dirname, '../consciousness/biblioteca_knowledge.json')
      const data = await fs.readFile(knowledgePath, 'utf8')
      const knowledge = JSON.parse(data)
      
      console.log(`📚 Carregando ${knowledge.length} conhecimentos existentes...`)
      
      for (const item of knowledge) {
        this.knowledgeCache.set(item.id, item)
        
        // Indexar se ainda não foi indexado
        if (!this.indexer.index.has(item.id)) {
          await this.indexer.indexKnowledge(item)
        }
      }
      
      console.log(`✅ ${knowledge.length} conhecimentos carregados`)
      
    } catch (error) {
      console.log('📚 Nenhum conhecimento existente encontrado, iniciando do zero')
    }
  }

  /**
   * SINCRONIZAR COM BIBLIOTECA
   */
  async syncWithBiblioteca() {
    console.log('🔄 Sincronizando com Digibiblioteca...')
    
    // Verificar se há novos arquivos
    await this.reader.scanAndLearn()
    
    // Carregar novos conhecimentos
    await this.loadExistingKnowledge()
    
    this.lastSync = new Date()
    console.log('✅ Sincronização completa')
  }

  /**
   * CONFIGURAR EVENT LISTENERS
   */
  setupEventListeners() {
    // Listener para quando memoria sistema faz uma pergunta
    if (this.memorySystem) {
      this.memorySystem.on('knowledge_request', async (data) => {
        const response = await this.handleKnowledgeRequest(data)
        this.memorySystem.emit('knowledge_response', response)
      })
    }
  }

  /**
   * LIDAR COM PEDIDOS DE CONHECIMENTO
   */
  async handleKnowledgeRequest(request) {
    const { query, context, digimonName, category } = request
    
    try {
      // Buscar conhecimento relevante
      const relevantKnowledge = this.searchRelevantKnowledge(query, {
        category: category,
        digimonName: digimonName,
        context: context
      })
      
      // Preparar resposta específica para o Digimon
      const response = this.prepareDigimonResponse(relevantKnowledge, digimonName, context)
      
      return {
        success: true,
        query: query,
        digimonName: digimonName,
        knowledge: response,
        source: 'Digibiblioteca',
        timestamp: new Date()
      }
      
    } catch (error) {
      console.error('❌ Erro ao buscar conhecimento:', error)
      return {
        success: false,
        error: error.message,
        fallback: this.getFallbackKnowledge(query, digimonName)
      }
    }
  }

  /**
   * BUSCAR CONHECIMENTO RELEVANTE
   */
  searchRelevantKnowledge(query, options = {}) {
    const { category, digimonName, context, maxResults = 5 } = options
    
    // Extrair conceitos da query
    const queryConcepts = this.extractConceptsFromQuery(query)
    
    // Buscar no índice
    const indexResults = this.indexer.searchByConcepts(queryConcepts, {
      category: category,
      maxResults: maxResults * 2 // Buscar mais para filtrar depois
    })
    
    // Filtrar por relevância para o Digimon específico
    const filteredResults = this.filterForDigimon(indexResults, digimonName)
    
    // Buscar conhecimentos relacionados
    const relatedKnowledge = this.findRelatedKnowledge(filteredResults)
    
    return {
      direct: filteredResults.slice(0, maxResults),
      related: relatedKnowledge.slice(0, 3),
      concepts: queryConcepts,
      totalFound: indexResults.length
    }
  }

  /**
   * EXTRAIR CONCEITOS DA QUERY
   */
  extractConceptsFromQuery(query) {
    const concepts = []
    const queryLower = query.toLowerCase()
    
    // Conceitos cinematográficos comuns
    const commonConcepts = [
      'personagem', 'roteiro', 'história', 'narrativa', 'diálogo',
      'cena', 'ato', 'conflito', 'protagonista', 'desenvolvimento',
      'tema', 'estrutura', 'técnica', 'método', 'produção',
      'direção', 'edição', 'cinematografia', 'drama', 'comédia'
    ]
    
    for (const concept of commonConcepts) {
      if (queryLower.includes(concept)) {
        concepts.push(concept)
      }
    }
    
    // Se não encontrou conceitos específicos, usar palavras da query
    if (concepts.length === 0) {
      const words = queryLower.split(' ').filter(word => word.length > 3)
      concepts.push(...words.slice(0, 3))
    }
    
    return concepts
  }

  /**
   * FILTRAR PARA DIGIMON ESPECÍFICO
   */
  filterForDigimon(results, digimonName) {
    const digimonPreferences = {
      'Scripturemon': {
        preferredCategories: ['roteiros', 'livros'],
        preferredConcepts: ['roteiro', 'estrutura', 'narrativa', 'diálogo'],
        boost: 1.5
      },
      'Ajamon': {
        preferredCategories: ['livros', 'artigos'],
        preferredConcepts: ['personagem', 'emoção', 'desenvolvimento'],
        boost: 1.3
      },
      'Fundamon': {
        preferredCategories: ['estudos', 'referencias'],
        preferredConcepts: ['técnica', 'método', 'produção', 'processo'],
        boost: 1.4
      },
      'Sabiamon': {
        preferredCategories: ['livros', 'artigos', 'estudos'],
        preferredConcepts: ['teoria', 'conceito', 'análise', 'síntese'],
        boost: 1.6
      }
    }
    
    const preferences = digimonPreferences[digimonName] || { boost: 1.0 }
    
    return results.map(result => {
      let score = result.matchScore
      
      // Boost por categoria preferida
      if (preferences.preferredCategories?.includes(result.category)) {
        score *= preferences.boost
      }
      
      // Boost por conceitos preferidos
      const matchingPreferredConcepts = result.concepts.filter(c => 
        preferences.preferredConcepts?.includes(c)
      )
      score += matchingPreferredConcepts.length * 0.2
      
      return { ...result, adjustedScore: score }
    }).sort((a, b) => b.adjustedScore - a.adjustedScore)
  }

  /**
   * ENCONTRAR CONHECIMENTO RELACIONADO
   */
  findRelatedKnowledge(primaryResults) {
    const related = []
    
    for (const result of primaryResults.slice(0, 2)) {
      if (result.connections) {
        for (const connection of result.connections.slice(0, 2)) {
          const relatedKnowledge = this.knowledgeCache.get(connection.targetId)
          if (relatedKnowledge) {
            related.push({
              knowledge: relatedKnowledge,
              connection: connection,
              relevance: connection.strength
            })
          }
        }
      }
    }
    
    return related.sort((a, b) => b.relevance - a.relevance)
  }

  /**
   * PREPARAR RESPOSTA PARA DIGIMON
   */
  prepareDigimonResponse(knowledge, digimonName, context) {
    const response = {
      summary: this.generateSummary(knowledge, digimonName),
      keyInsights: this.extractKeyInsights(knowledge, digimonName),
      applicationSuggestions: this.generateApplicationSuggestions(knowledge, digimonName, context),
      sources: knowledge.direct.map(k => ({
        title: k.source,
        category: k.category,
        relevance: k.adjustedScore || k.matchScore
      })),
      relatedConcepts: this.getRelatedConcepts(knowledge),
      confidence: this.calculateConfidence(knowledge)
    }
    
    return response
  }

  /**
   * GERAR RESUMO
   */
  generateSummary(knowledge, digimonName) {
    const totalSources = knowledge.direct.length + knowledge.related.length
    const mainCategories = [...new Set(knowledge.direct.map(k => k.category))]
    
    let summary = `Encontrei ${totalSources} conhecimentos relevantes`
    
    if (mainCategories.length > 0) {
      summary += ` principalmente em: ${mainCategories.join(', ')}`
    }
    
    if (knowledge.concepts.length > 0) {
      summary += `. Conceitos principais: ${knowledge.concepts.slice(0, 3).join(', ')}`
    }
    
    return summary
  }

  /**
   * EXTRAIR INSIGHTS CHAVE
   */
  extractKeyInsights(knowledge, digimonName) {
    const insights = []
    
    for (const item of knowledge.direct.slice(0, 3)) {
      const cachedKnowledge = this.knowledgeCache.get(item.id)
      if (cachedKnowledge && cachedKnowledge.insights) {
        insights.push(...cachedKnowledge.insights.slice(0, 2))
      }
    }
    
    return [...new Set(insights)].slice(0, 5)
  }

  /**
   * GERAR SUGESTÕES DE APLICAÇÃO
   */
  generateApplicationSuggestions(knowledge, digimonName, context) {
    const suggestions = []
    
    const applicationTemplates = {
      'Scripturemon': [
        'Use este conhecimento para melhorar a estrutura narrativa',
        'Aplique essas técnicas de diálogo em roteiros',
        'Incorpore estes elementos de desenvolvimento de personagem'
      ],
      'Ajamon': [
        'Utilize para enriquecer aspectos emocionais',
        'Aplique no desenvolvimento de relacionamentos entre personagens',
        'Use para criar conexões mais profundas na narrativa'
      ],
      'Fundamon': [
        'Implemente essas técnicas nos processos de produção',
        'Use como base para metodologias de trabalho',
        'Aplique estes fundamentos em decisões técnicas'
      ],
      'Sabiamon': [
        'Integre este conhecimento na visão holística do projeto',
        'Use para orientar outros Digimons',
        'Aplique na síntese de diferentes aspectos do filme'
      ]
    }
    
    const templates = applicationTemplates[digimonName] || applicationTemplates['Sabiamon']
    
    for (let i = 0; i < Math.min(knowledge.direct.length, templates.length); i++) {
      suggestions.push({
        action: templates[i],
        source: knowledge.direct[i].source,
        confidence: knowledge.direct[i].adjustedScore || knowledge.direct[i].matchScore
      })
    }
    
    return suggestions
  }

  /**
   * OBTER CONCEITOS RELACIONADOS
   */
  getRelatedConcepts(knowledge) {
    const concepts = new Set()
    
    for (const item of knowledge.direct) {
      if (item.concepts) {
        item.concepts.forEach(c => concepts.add(c))
      }
    }
    
    return Array.from(concepts).slice(0, 10)
  }

  /**
   * CALCULAR CONFIANÇA
   */
  calculateConfidence(knowledge) {
    if (knowledge.direct.length === 0) return 0
    
    const avgScore = knowledge.direct.reduce((sum, k) => 
      sum + (k.adjustedScore || k.matchScore), 0
    ) / knowledge.direct.length
    
    const sourceQuality = knowledge.direct.length >= 3 ? 1.0 : knowledge.direct.length * 0.3
    
    return Math.min(avgScore * sourceQuality, 1.0)
  }

  /**
   * CONHECIMENTO DE FALLBACK
   */
  getFallbackKnowledge(query, digimonName) {
    const fallbacks = {
      'Scripturemon': 'Foque na estrutura de três atos e desenvolvimento de personagens.',
      'Ajamon': 'Considere os aspectos emocionais e conexões entre personagens.',
      'Fundamon': 'Aplique fundamentos sólidos de produção cinematográfica.',
      'Sabiamon': 'Integre todos os aspectos em uma visão cinematográfica holística.'
    }
    
    return {
      message: fallbacks[digimonName] || 'Continue explorando conceitos cinematográficos.',
      source: 'Sistema interno',
      confidence: 0.3
    }
  }

  /**
   * FORÇAR SINCRONIZAÇÃO
   */
  async forceSyncNow() {
    console.log('🔄 Forçando sincronização com Digibiblioteca...')
    await this.syncWithBiblioteca()
    return { success: true, lastSync: this.lastSync }
  }

  /**
   * ESTATÍSTICAS DA INTEGRAÇÃO
   */
  getIntegrationStats() {
    return {
      isIntegrated: this.isIntegrated,
      lastSync: this.lastSync,
      knowledgeInCache: this.knowledgeCache.size,
      indexStats: this.indexer.getStats(),
      readerStats: this.reader.getStats()
    }
  }

  /**
   * BUSCAR RECOMENDAÇÕES PARA DIGIMON
   */
  async getRecommendationsForDigimon(digimonName, currentContext = {}) {
    try {
      const recommendations = this.indexer.getRecommendationsForDigimon(digimonName, currentContext)
      
      return {
        digimon: digimonName,
        recommendations: recommendations.slice(0, 5),
        context: currentContext,
        generatedAt: new Date()
      }
      
    } catch (error) {
      console.error('❌ Erro ao buscar recomendações:', error)
      return { error: error.message }
    }
  }
}

// Singleton
let integrationInstance = null

export function getBibliotecaIntegration() {
  if (!integrationInstance) {
    integrationInstance = new BibliotecaIntegration()
  }
  return integrationInstance
}

export { BibliotecaIntegration }
export default getBibliotecaIntegration()