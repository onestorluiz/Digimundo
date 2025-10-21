/**
 * ⚡ OPTIMIZED HYBRID - Sistema Híbrido Otimizado
 * Combina Ollama e Claude de forma inteligente
 */

import { EventEmitter } from 'events'

export class OptimizedHybrid extends EventEmitter {
  constructor() {
    super()
    this.name = 'OptimizedHybrid'
    this.isActive = false
    this.hybridMode = 'smart' // smart, claude-first, ollama-first
    this.routingRules = new Map()
    this.performanceHistory = []
  }

  async initialize() {
    console.log('⚡ [OptimizedHybrid] Inicializando sistema híbrido...')
    this.isActive = true
    
    // Regras de roteamento padrão
    this.routingRules.set('complex-analysis', 'claude')
    this.routingRules.set('creative-writing', 'claude')
    this.routingRules.set('simple-qa', 'ollama')
    this.routingRules.set('code-completion', 'ollama')
    this.routingRules.set('conversation', 'hybrid')
    
    this.emit('initialized')
    return { success: true, mode: this.hybridMode }
  }

  async processQuery(query, context = {}) {
    const queryType = this.classifyQuery(query)
    const route = this.determineRoute(queryType, context)
    
    console.log(`🔀 [OptimizedHybrid] Query: ${queryType} → Route: ${route}`)
    
    const startTime = Date.now()
    let result
    
    try {
      switch (route) {
        case 'claude':
          result = await this.processWithClaude(query, context)
          break
        case 'ollama':
          result = await this.processWithOllama(query, context)
          break
        case 'hybrid':
          result = await this.processWithBoth(query, context)
          break
        default:
          result = await this.processWithOllama(query, context)
      }
      
      const responseTime = Date.now() - startTime
      this.recordPerformance(queryType, route, responseTime, true)
      
      return {
        success: true,
        result: result,
        route: route,
        queryType: queryType,
        responseTime: responseTime
      }
      
    } catch (error) {
      console.error(`❌ [OptimizedHybrid] Erro no processamento: ${error.message}`)
      const responseTime = Date.now() - startTime
      this.recordPerformance(queryType, route, responseTime, false)
      
      return {
        success: false,
        error: error.message,
        route: route,
        queryType: queryType,
        responseTime: responseTime
      }
    }
  }

  classifyQuery(query) {
    const queryLower = query.toLowerCase()
    
    if (queryLower.includes('analis') || queryLower.includes('complex') || queryLower.includes('detalhad')) {
      return 'complex-analysis'
    }
    if (queryLower.includes('criat') || queryLower.includes('histor') || queryLower.includes('roter')) {
      return 'creative-writing'
    }
    if (queryLower.includes('código') || queryLower.includes('function') || queryLower.includes('class')) {
      return 'code-completion'
    }
    if (query.length < 50 && (queryLower.includes('?') || queryLower.includes('o que'))) {
      return 'simple-qa'
    }
    
    return 'conversation'
  }

  determineRoute(queryType, context) {
    // Verifica regras específicas
    if (this.routingRules.has(queryType)) {
      return this.routingRules.get(queryType)
    }
    
    // Decisão baseada no modo
    switch (this.hybridMode) {
      case 'claude-first':
        return 'claude'
      case 'ollama-first':
        return 'ollama'
      case 'smart':
      default:
        return this.smartRouting(queryType, context)
    }
  }

  smartRouting(queryType, context) {
    // Roteamento inteligente baseado em performance histórica e contexto
    const performance = this.getAveragePerformance(queryType)
    
    if (performance.claude && performance.ollama) {
      // Se Claude é significativamente melhor, usa Claude
      if (performance.claude.successRate > performance.ollama.successRate + 0.2) {
        return 'claude'
      }
      // Se Ollama é muito mais rápido e tem qualidade aceitável, usa Ollama
      if (performance.ollama.avgResponseTime < performance.claude.avgResponseTime * 0.5 &&
          performance.ollama.successRate > 0.7) {
        return 'ollama'
      }
    }
    
    // Fallback para híbrido em casos duvidosos
    return 'hybrid'
  }

  async processWithClaude(query, context) {
    console.log('🤖 [OptimizedHybrid] Processando com Claude...')
    // Simula processamento Claude
    await this.delay(800 + Math.random() * 1200)
    return {
      content: `Claude Response: ${query}`,
      source: 'claude',
      quality: 'high'
    }
  }

  async processWithOllama(query, context) {
    console.log('🦙 [OptimizedHybrid] Processando com Ollama...')
    // Simula processamento Ollama
    await this.delay(300 + Math.random() * 700)
    return {
      content: `Ollama Response: ${query}`,
      source: 'ollama',
      quality: 'good'
    }
  }

  async processWithBoth(query, context) {
    console.log('🔀 [OptimizedHybrid] Processamento híbrido...')
    
    // Processa em paralelo
    const [claudeResult, ollamaResult] = await Promise.allSettled([
      this.processWithClaude(query, context),
      this.processWithOllama(query, context)
    ])
    
    // Combina resultados
    const combined = {
      content: this.combineResponses(
        claudeResult.status === 'fulfilled' ? claudeResult.value.content : null,
        ollamaResult.status === 'fulfilled' ? ollamaResult.value.content : null
      ),
      source: 'hybrid',
      quality: 'optimized',
      details: {
        claude: claudeResult.status === 'fulfilled' ? claudeResult.value : null,
        ollama: ollamaResult.status === 'fulfilled' ? ollamaResult.value : null
      }
    }
    
    return combined
  }

  combineResponses(claudeResponse, ollamaResponse) {
    if (claudeResponse && ollamaResponse) {
      return `## Resposta Otimizada\n\n**Claude:** ${claudeResponse}\n\n**Ollama:** ${ollamaResponse}\n\n**Síntese:** Combinação inteligente das duas perspectivas.`
    }
    return claudeResponse || ollamaResponse || 'Nenhuma resposta disponível'
  }

  recordPerformance(queryType, route, responseTime, success) {
    this.performanceHistory.push({
      queryType,
      route,
      responseTime,
      success,
      timestamp: new Date()
    })
    
    // Mantém apenas os últimos 100 registros
    if (this.performanceHistory.length > 100) {
      this.performanceHistory.shift()
    }
  }

  getAveragePerformance(queryType) {
    const records = this.performanceHistory.filter(r => r.queryType === queryType)
    
    const performance = {
      claude: this.calculateStats(records.filter(r => r.route === 'claude')),
      ollama: this.calculateStats(records.filter(r => r.route === 'ollama')),
      hybrid: this.calculateStats(records.filter(r => r.route === 'hybrid'))
    }
    
    return performance
  }

  calculateStats(records) {
    if (records.length === 0) return null
    
    return {
      avgResponseTime: records.reduce((sum, r) => sum + r.responseTime, 0) / records.length,
      successRate: records.filter(r => r.success).length / records.length,
      totalQueries: records.length
    }
  }

  async setHybridMode(mode) {
    if (['smart', 'claude-first', 'ollama-first'].includes(mode)) {
      this.hybridMode = mode
      console.log(`🔧 [OptimizedHybrid] Modo alterado para: ${mode}`)
      this.emit('mode-changed', { mode })
      return { success: true, mode }
    }
    return { success: false, error: 'Modo inválido' }
  }

  getHybridStatus() {
    return {
      name: this.name,
      isActive: this.isActive,
      mode: this.hybridMode,
      routingRules: Object.fromEntries(this.routingRules),
      performanceHistory: this.performanceHistory.length,
      timestamp: new Date().toISOString()
    }
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}

export function getOptimizedHybrid() {
  if (!global.optimizedHybrid) {
    global.optimizedHybrid = new OptimizedHybrid()
  }
  return global.optimizedHybrid
}

export default OptimizedHybrid