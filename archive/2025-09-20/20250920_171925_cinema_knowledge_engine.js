#!/usr/bin/env node

/**
 * 🎬 CINEMA KNOWLEDGE ENGINE
 * 
 * Sistema inteligente de aprendizado cinematográfico que:
 * - Extrai regras e padrões de livros e roteiros
 * - Compreende estruturas narrativas profundamente
 * - Gera insights acionáveis para criação
 * - Evolui com cada novo material
 */

import fs from 'fs/promises'
import path from 'path'
import { fileURLToPath } from 'url'
import EventEmitter from 'events'
import crypto from 'crypto'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// Padrões cinematográficos conhecidos
const KNOWN_STRUCTURES = {
  THREE_ACT: {
    name: 'Three Act Structure',
    acts: [
      { name: 'Setup', percentage: 25, purpose: 'Establish world, characters, conflict' },
      { name: 'Confrontation', percentage: 50, purpose: 'Rising action, complications, development' },
      { name: 'Resolution', percentage: 25, purpose: 'Climax, falling action, denouement' }
    ]
  },
  HEROS_JOURNEY: {
    name: "Hero's Journey",
    stages: [
      'Ordinary World', 'Call to Adventure', 'Refusal of Call',
      'Meeting the Mentor', 'Crossing Threshold', 'Tests, Allies, Enemies',
      'Approach', 'Ordeal', 'Reward', 'Road Back',
      'Resurrection', 'Return with Elixir'
    ]
  },
  SAVE_THE_CAT: {
    name: 'Save the Cat Beat Sheet',
    beats: [
      { beat: 'Opening Image', page: 1 },
      { beat: 'Theme Stated', page: 5 },
      { beat: 'Set-Up', pages: '1-10' },
      { beat: 'Catalyst', page: 12 },
      { beat: 'Debate', pages: '12-25' },
      { beat: 'Break into Two', page: 25 },
      { beat: 'B Story', page: 30 },
      { beat: 'Fun and Games', pages: '30-55' },
      { beat: 'Midpoint', page: 55 },
      { beat: 'Bad Guys Close In', pages: '55-75' },
      { beat: 'All Is Lost', page: 75 },
      { beat: 'Dark Night of the Soul', pages: '75-85' },
      { beat: 'Break into Three', page: 85 },
      { beat: 'Finale', pages: '85-110' },
      { beat: 'Final Image', page: 110 }
    ]
  }
}

class CinemaKnowledgeEngine extends EventEmitter {
  constructor() {
    super()
    
    // Base de conhecimento
    this.knowledge = {
      rules: new Map(),
      patterns: new Map(),
      structures: new Map(),
      characters: new Map(),
      dialogues: new Map(),
      scenes: new Map(),
      themes: new Map()
    }
    
    // Índice de busca semântica
    this.semanticIndex = new Map()
    
    // Estatísticas
    this.stats = {
      materialsProcessed: 0,
      rulesExtracted: 0,
      patternsIdentified: 0,
      insightsGenerated: 0
    }
    
    // Cache de processamento
    this.processingCache = new Map()
  }
  
  /**
   * INICIALIZAR ENGINE
   */
  async initialize() {
    console.log(`
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                 🎬 CINEMA KNOWLEDGE ENGINE 🎬                   ║
║                                                                  ║
║           Transforming stories into understanding...            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    `)
    
    // Carregar conhecimento existente
    await this.loadExistingKnowledge()
    
    // Inicializar estruturas conhecidas
    this.initializeKnownStructures()
    
    console.log('✅ Cinema Knowledge Engine initialized')
    console.log(`📚 Knowledge base: ${this.knowledge.rules.size} rules, ${this.knowledge.patterns.size} patterns`)
  }
  
  /**
   * PROCESSAR MATERIAL (Livro ou Roteiro)
   */
  async processMaterial(filePath, type = 'auto') {
    console.log(`\n📖 Processing: ${path.basename(filePath)}`)
    
    try {
      // Detectar tipo se auto
      if (type === 'auto') {
        type = await this.detectMaterialType(filePath)
      }
      
      // Ler conteúdo
      const content = await fs.readFile(filePath, 'utf-8')
      
      // Processar baseado no tipo
      let processed
      if (type === 'script') {
        processed = await this.processScript(content)
      } else if (type === 'book') {
        processed = await this.processBook(content)
      } else {
        processed = await this.processGeneric(content)
      }
      
      // Extrair conhecimento
      const extracted = await this.extractKnowledge(processed)
      
      // Armazenar conhecimento
      await this.storeKnowledge(extracted, filePath)
      
      // Gerar insights
      const insights = await this.generateInsights(extracted)
      
      // Atualizar estatísticas
      this.stats.materialsProcessed++
      this.stats.rulesExtracted += extracted.rules.length
      this.stats.patternsIdentified += extracted.patterns.length
      this.stats.insightsGenerated += insights.length
      
      // Emitir evento
      this.emit('material_processed', {
        file: filePath,
        type,
        extracted,
        insights
      })
      
      console.log(`✅ Processed successfully:`)
      console.log(`   - Rules extracted: ${extracted.rules.length}`)
      console.log(`   - Patterns found: ${extracted.patterns.length}`)
      console.log(`   - Insights generated: ${insights.length}`)
      
      return {
        success: true,
        extracted,
        insights
      }
      
    } catch (error) {
      console.error(`❌ Error processing ${filePath}:`, error)
      return {
        success: false,
        error: error.message
      }
    }
  }
  
  /**
   * PROCESSAR ROTEIRO
   */
  async processScript(content) {
    const processed = {
      type: 'script',
      scenes: [],
      characters: new Set(),
      dialogues: [],
      actions: [],
      structure: null
    }
    
    const lines = content.split('\n')
    let currentScene = null
    let currentCharacter = null
    
    for (const line of lines) {
      const trimmed = line.trim()
      
      // Detectar cabeçalho de cena
      if (/^(INT\.|EXT\.|INT\/EXT\.)/.test(trimmed)) {
        if (currentScene) {
          processed.scenes.push(currentScene)
        }
        currentScene = {
          heading: trimmed,
          content: [],
          characters: new Set()
        }
      }
      
      // Detectar personagem (linha em maiúsculas)
      else if (trimmed === trimmed.toUpperCase() && trimmed.length > 0 && !trimmed.includes('.')) {
        currentCharacter = trimmed
        processed.characters.add(currentCharacter)
        if (currentScene) {
          currentScene.characters.add(currentCharacter)
        }
      }
      
      // Detectar diálogo
      else if (currentCharacter && trimmed.length > 0) {
        processed.dialogues.push({
          character: currentCharacter,
          text: trimmed,
          scene: currentScene?.heading
        })
        if (currentScene) {
          currentScene.content.push({ type: 'dialogue', character: currentCharacter, text: trimmed })
        }
      }
      
      // Detectar ação
      else if (trimmed.length > 0 && !trimmed.startsWith('(')) {
        processed.actions.push(trimmed)
        if (currentScene) {
          currentScene.content.push({ type: 'action', text: trimmed })
        }
        currentCharacter = null
      }
    }
    
    // Adicionar última cena
    if (currentScene) {
      processed.scenes.push(currentScene)
    }
    
    // Analisar estrutura
    processed.structure = this.analyzeStructure(processed.scenes)
    
    return processed
  }
  
  /**
   * PROCESSAR LIVRO
   */
  async processBook(content) {
    const processed = {
      type: 'book',
      chapters: [],
      concepts: [],
      rules: [],
      examples: [],
      quotes: []
    }
    
    // Dividir em chunks para análise
    const chunks = this.chunkText(content, 1000)
    
    for (const chunk of chunks) {
      // Extrair conceitos
      const concepts = this.extractConcepts(chunk)
      processed.concepts.push(...concepts)
      
      // Extrair regras
      const rules = this.extractRules(chunk)
      processed.rules.push(...rules)
      
      // Extrair exemplos
      const examples = this.extractExamples(chunk)
      processed.examples.push(...examples)
      
      // Extrair citações importantes
      const quotes = this.extractQuotes(chunk)
      processed.quotes.push(...quotes)
    }
    
    return processed
  }
  
  /**
   * PROCESSAR GENÉRICO
   */
  async processGeneric(content) {
    return {
      type: 'generic',
      content,
      chunks: this.chunkText(content, 500)
    }
  }
  
  /**
   * EXTRAIR CONHECIMENTO
   */
  async extractKnowledge(processed) {
    const extracted = {
      rules: [],
      patterns: [],
      structures: [],
      insights: [],
      techniques: []
    }
    
    // Extrair baseado no tipo
    if (processed.type === 'script') {
      // Extrair padrões de estrutura
      if (processed.structure) {
        extracted.structures.push(processed.structure)
      }
      
      // Extrair padrões de diálogo
      const dialoguePatterns = this.analyzeDialoguePatterns(processed.dialogues)
      extracted.patterns.push(...dialoguePatterns)
      
      // Extrair técnicas de cena
      const sceneTechniques = this.analyzeSceneTechniques(processed.scenes)
      extracted.techniques.push(...sceneTechniques)
      
    } else if (processed.type === 'book') {
      // Regras já extraídas
      extracted.rules = processed.rules
      
      // Identificar padrões nos conceitos
      const conceptPatterns = this.identifyConceptPatterns(processed.concepts)
      extracted.patterns.push(...conceptPatterns)
      
      // Extrair insights dos exemplos
      const exampleInsights = this.extractInsightsFromExamples(processed.examples)
      extracted.insights.push(...exampleInsights)
    }
    
    return extracted
  }
  
  /**
   * EXTRAIR REGRAS
   */
  extractRules(text) {
    const rules = []
    
    // Padrões de regras em português e inglês
    const rulePatterns = [
      /[Dd]eve[m]?\s+([^.!?]+)[.!?]/g,
      /[Nn]unca\s+([^.!?]+)[.!?]/g,
      /[Ss]empre\s+([^.!?]+)[.!?]/g,
      /[Éé] importante\s+([^.!?]+)[.!?]/g,
      /[Éé] essencial\s+([^.!?]+)[.!?]/g,
      /[Rr]egra\s*#?\d*:?\s*([^.!?]+)[.!?]/g,
      /[Pp]rincípio\s*#?\d*:?\s*([^.!?]+)[.!?]/g,
      /[Mm]ust\s+([^.!?]+)[.!?]/g,
      /[Ss]hould\s+([^.!?]+)[.!?]/g,
      /[Nn]ever\s+([^.!?]+)[.!?]/g,
      /[Aa]lways\s+([^.!?]+)[.!?]/g
    ]
    
    for (const pattern of rulePatterns) {
      const matches = text.matchAll(pattern)
      for (const match of matches) {
        const rule = {
          text: match[0],
          core: match[1],
          type: this.categorizeRule(match[0]),
          confidence: this.calculateRuleConfidence(match[0]),
          context: this.extractContext(text, match.index, 100)
        }
        rules.push(rule)
      }
    }
    
    return rules
  }
  
  /**
   * EXTRAIR CONCEITOS
   */
  extractConcepts(text) {
    const concepts = []
    
    // Padrões de conceitos
    const conceptPatterns = [
      /[Oo] conceito de\s+([^.!?]+)/g,
      /[Aa] ideia de\s+([^.!?]+)/g,
      /[Tt]he concept of\s+([^.!?]+)/g,
      /[Tt]he idea of\s+([^.!?]+)/g,
      /([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:é|is|significa|means)/g
    ]
    
    for (const pattern of conceptPatterns) {
      const matches = text.matchAll(pattern)
      for (const match of matches) {
        concepts.push({
          name: match[1].trim(),
          context: this.extractContext(text, match.index, 150)
        })
      }
    }
    
    return concepts
  }
  
  /**
   * EXTRAIR EXEMPLOS
   */
  extractExamples(text) {
    const examples = []
    
    // Padrões de exemplos
    const examplePatterns = [
      /[Pp]or exemplo[,:]?\s+([^.!?]+)/g,
      /[Ee]xemplo[:]?\s+([^.!?]+)/g,
      /[Ff]or example[,:]?\s+([^.!?]+)/g,
      /[Ff]or instance[,:]?\s+([^.!?]+)/g,
      /[Cc]onsidere\s+([^.!?]+)/g,
      /[Cc]onsider\s+([^.!?]+)/g
    ]
    
    for (const pattern of examplePatterns) {
      const matches = text.matchAll(pattern)
      for (const match of matches) {
        examples.push({
          text: match[1].trim(),
          fullContext: this.extractContext(text, match.index, 200)
        })
      }
    }
    
    return examples
  }
  
  /**
   * EXTRAIR CITAÇÕES
   */
  extractQuotes(text) {
    const quotes = []
    
    // Padrões de citações
    const quotePatterns = [
      /"([^"]+)"/g,
      /'([^']+)'/g,
      /"([^"]+)"/g,
      /«([^»]+)»/g
    ]
    
    for (const pattern of quotePatterns) {
      const matches = text.matchAll(pattern)
      for (const match of matches) {
        if (match[1].length > 20 && match[1].length < 300) {
          quotes.push({
            text: match[1],
            context: this.extractContext(text, match.index, 50)
          })
        }
      }
    }
    
    return quotes
  }
  
  /**
   * ANALISAR ESTRUTURA
   */
  analyzeStructure(scenes) {
    if (!scenes || scenes.length === 0) return null
    
    const totalScenes = scenes.length
    const structure = {
      totalScenes,
      acts: []
    }
    
    // Dividir em 3 atos (aproximado)
    const act1End = Math.floor(totalScenes * 0.25)
    const act2End = Math.floor(totalScenes * 0.75)
    
    structure.acts.push({
      number: 1,
      scenes: scenes.slice(0, act1End),
      percentage: (act1End / totalScenes) * 100
    })
    
    structure.acts.push({
      number: 2,
      scenes: scenes.slice(act1End, act2End),
      percentage: ((act2End - act1End) / totalScenes) * 100
    })
    
    structure.acts.push({
      number: 3,
      scenes: scenes.slice(act2End),
      percentage: ((totalScenes - act2End) / totalScenes) * 100
    })
    
    // Identificar pontos de virada
    structure.turningPoints = this.identifyTurningPoints(scenes)
    
    return structure
  }
  
  /**
   * IDENTIFICAR PONTOS DE VIRADA
   */
  identifyTurningPoints(scenes) {
    const turningPoints = []
    
    // Procurar por mudanças significativas
    for (let i = 1; i < scenes.length - 1; i++) {
      const prevCharCount = scenes[i - 1].characters.size
      const currCharCount = scenes[i].characters.size
      const nextCharCount = scenes[i + 1].characters.size
      
      // Mudança significativa no número de personagens
      if (Math.abs(currCharCount - prevCharCount) > 2 || 
          Math.abs(nextCharCount - currCharCount) > 2) {
        turningPoints.push({
          scene: i,
          type: 'character_shift',
          description: 'Significant change in character presence'
        })
      }
    }
    
    return turningPoints
  }
  
  /**
   * ANALISAR PADRÕES DE DIÁLOGO
   */
  analyzeDialoguePatterns(dialogues) {
    const patterns = []
    
    if (!dialogues || dialogues.length === 0) return patterns
    
    // Analisar comprimento médio
    const avgLength = dialogues.reduce((sum, d) => sum + d.text.length, 0) / dialogues.length
    patterns.push({
      type: 'dialogue_length',
      value: avgLength,
      insight: avgLength < 50 ? 'Concise dialogue style' : 'Verbose dialogue style'
    })
    
    // Analisar frequência de perguntas
    const questions = dialogues.filter(d => d.text.includes('?')).length
    const questionRatio = questions / dialogues.length
    patterns.push({
      type: 'question_frequency',
      value: questionRatio,
      insight: questionRatio > 0.3 ? 'High tension through questions' : 'Statement-driven dialogue'
    })
    
    return patterns
  }
  
  /**
   * ANALISAR TÉCNICAS DE CENA
   */
  analyzeSceneTechniques(scenes) {
    const techniques = []
    
    if (!scenes || scenes.length === 0) return techniques
    
    // Proporção interior/exterior
    const interiorScenes = scenes.filter(s => s.heading && s.heading.startsWith('INT.')).length
    const exteriorScenes = scenes.filter(s => s.heading && s.heading.startsWith('EXT.')).length
    
    techniques.push({
      type: 'location_balance',
      interior: interiorScenes,
      exterior: exteriorScenes,
      ratio: interiorScenes / (interiorScenes + exteriorScenes),
      insight: interiorScenes > exteriorScenes ? 'Character-focused narrative' : 'Action-oriented narrative'
    })
    
    return techniques
  }
  
  /**
   * GERAR INSIGHTS
   */
  async generateInsights(extracted) {
    const insights = []
    
    // Insight sobre regras
    if (extracted.rules && extracted.rules.length > 0) {
      const categories = {}
      extracted.rules.forEach(r => {
        categories[r.type] = (categories[r.type] || 0) + 1
      })
      
      const dominant = Object.entries(categories)
        .sort((a, b) => b[1] - a[1])[0]
      
      if (dominant) {
        insights.push({
          type: 'rule_focus',
          insight: `Strong emphasis on ${dominant[0]} rules (${dominant[1]} occurrences)`,
          actionable: `Consider applying ${dominant[0]} principles in your work`
        })
      }
    }
    
    // Insight sobre padrões
    if (extracted.patterns && extracted.patterns.length > 0) {
      insights.push({
        type: 'pattern_discovery',
        insight: `Discovered ${extracted.patterns.length} narrative patterns`,
        actionable: 'Use these patterns as templates for structure'
      })
    }
    
    // Insight sobre estrutura
    if (extracted.structures && extracted.structures.length > 0) {
      const structure = extracted.structures[0]
      if (structure.acts) {
        const act2Percentage = structure.acts[1]?.percentage || 0
        insights.push({
          type: 'structure_analysis',
          insight: `Act 2 comprises ${act2Percentage.toFixed(1)}% of the story`,
          actionable: act2Percentage < 45 ? 'Consider expanding the confrontation phase' : 'Well-balanced structure detected'
        })
      }
    }
    
    return insights
  }
  
  /**
   * ARMAZENAR CONHECIMENTO
   */
  async storeKnowledge(extracted, source) {
    // Armazenar regras
    if (extracted.rules) {
      extracted.rules.forEach(rule => {
        const id = this.generateId(rule.text)
        this.knowledge.rules.set(id, {
          ...rule,
          source,
          timestamp: Date.now()
        })
      })
    }
    
    // Armazenar padrões
    if (extracted.patterns) {
      extracted.patterns.forEach(pattern => {
        const id = this.generateId(JSON.stringify(pattern))
        this.knowledge.patterns.set(id, {
          ...pattern,
          source,
          timestamp: Date.now()
        })
      })
    }
    
    // Armazenar estruturas
    if (extracted.structures) {
      extracted.structures.forEach(structure => {
        const id = this.generateId(JSON.stringify(structure))
        this.knowledge.structures.set(id, {
          ...structure,
          source,
          timestamp: Date.now()
        })
      })
    }
    
    // Salvar em disco
    await this.saveKnowledgeBase()
  }
  
  /**
   * CONSULTAR CONHECIMENTO
   */
  async queryKnowledge(query) {
    console.log(`\n🔍 Querying: "${query}"`)
    
    const results = {
      rules: [],
      patterns: [],
      insights: [],
      recommendations: []
    }
    
    // Buscar regras relevantes
    for (const [id, rule] of this.knowledge.rules) {
      if (this.isRelevant(query, rule.text) || this.isRelevant(query, rule.core)) {
        results.rules.push(rule)
      }
    }
    
    // Buscar padrões relevantes
    for (const [id, pattern] of this.knowledge.patterns) {
      if (this.isRelevant(query, JSON.stringify(pattern))) {
        results.patterns.push(pattern)
      }
    }
    
    // Gerar recomendações baseadas nos resultados
    if (results.rules.length > 0) {
      results.recommendations.push({
        type: 'rules_based',
        text: `Apply these ${results.rules.length} rules to your work`,
        rules: results.rules.slice(0, 3)
      })
    }
    
    // Gerar insights
    if (results.patterns.length > 0) {
      results.insights.push({
        type: 'pattern_match',
        text: `Found ${results.patterns.length} relevant patterns for your query`
      })
    }
    
    return results
  }
  
  /**
   * HELPERS
   */
  
  detectMaterialType(filePath) {
    const ext = path.extname(filePath).toLowerCase()
    const basename = path.basename(filePath).toLowerCase()
    
    if (ext === '.fdx' || ext === '.fountain' || basename.includes('script') || basename.includes('roteiro')) {
      return 'script'
    }
    
    if (basename.includes('book') || basename.includes('livro')) {
      return 'book'
    }
    
    return 'generic'
  }
  
  chunkText(text, chunkSize) {
    const chunks = []
    const sentences = text.split(/[.!?]+/)
    
    let currentChunk = ''
    for (const sentence of sentences) {
      if (currentChunk.length + sentence.length > chunkSize) {
        if (currentChunk) chunks.push(currentChunk)
        currentChunk = sentence
      } else {
        currentChunk += sentence + '. '
      }
    }
    
    if (currentChunk) chunks.push(currentChunk)
    
    return chunks
  }
  
  extractContext(text, index, contextSize) {
    const start = Math.max(0, index - contextSize)
    const end = Math.min(text.length, index + contextSize)
    return text.substring(start, end).trim()
  }
  
  categorizeRule(ruleText) {
    const text = ruleText.toLowerCase()
    
    if (text.includes('personagem') || text.includes('character')) return 'CHARACTER'
    if (text.includes('diálogo') || text.includes('dialogue')) return 'DIALOGUE'
    if (text.includes('estrutura') || text.includes('structure')) return 'STRUCTURE'
    if (text.includes('cena') || text.includes('scene')) return 'SCENE'
    if (text.includes('conflito') || text.includes('conflict')) return 'CONFLICT'
    if (text.includes('ato') || text.includes('act')) return 'ACT'
    if (text.includes('tema') || text.includes('theme')) return 'THEME'
    
    return 'GENERAL'
  }
  
  calculateRuleConfidence(ruleText) {
    let confidence = 0.5
    
    // Palavras que aumentam confiança
    if (ruleText.includes('sempre') || ruleText.includes('always')) confidence += 0.2
    if (ruleText.includes('nunca') || ruleText.includes('never')) confidence += 0.2
    if (ruleText.includes('deve') || ruleText.includes('must')) confidence += 0.1
    if (ruleText.includes('essencial') || ruleText.includes('essential')) confidence += 0.15
    if (ruleText.includes('importante') || ruleText.includes('important')) confidence += 0.1
    
    return Math.min(1, confidence)
  }
  
  identifyConceptPatterns(concepts) {
    const patterns = []
    const conceptGroups = {}
    
    // Agrupar conceitos similares
    concepts.forEach(concept => {
      const key = concept.name.split(' ')[0].toLowerCase()
      if (!conceptGroups[key]) {
        conceptGroups[key] = []
      }
      conceptGroups[key].push(concept)
    })
    
    // Criar padrões dos grupos
    Object.entries(conceptGroups).forEach(([key, group]) => {
      if (group.length > 1) {
        patterns.push({
          type: 'concept_cluster',
          theme: key,
          concepts: group.map(g => g.name),
          frequency: group.length
        })
      }
    })
    
    return patterns
  }
  
  extractInsightsFromExamples(examples) {
    const insights = []
    
    if (examples.length > 5) {
      insights.push({
        type: 'example_rich',
        text: `Material contains ${examples.length} practical examples`,
        value: 'High practical value for learning'
      })
    }
    
    return insights
  }
  
  isRelevant(query, text) {
    if (!query || !text) return false
    
    const queryWords = query.toLowerCase().split(' ')
    const textLower = text.toLowerCase()
    
    return queryWords.some(word => textLower.includes(word))
  }
  
  generateId(text) {
    return crypto.createHash('md5').update(text).digest('hex').substring(0, 8)
  }
  
  initializeKnownStructures() {
    // Adicionar estruturas conhecidas ao conhecimento base
    Object.entries(KNOWN_STRUCTURES).forEach(([key, structure]) => {
      const id = this.generateId(key)
      this.knowledge.structures.set(id, {
        ...structure,
        source: 'built-in',
        timestamp: Date.now()
      })
    })
  }
  
  async loadExistingKnowledge() {
    try {
      const knowledgePath = path.join(__dirname, 'processed_knowledge', 'knowledge_base.json')
      const data = await fs.readFile(knowledgePath, 'utf-8')
      const loaded = JSON.parse(data)
      
      // Restaurar conhecimento
      if (loaded.rules) {
        loaded.rules.forEach(rule => {
          this.knowledge.rules.set(rule.id, rule)
        })
      }
      
      console.log(`📚 Loaded existing knowledge base`)
    } catch (error) {
      console.log(`📚 Starting with fresh knowledge base`)
    }
  }
  
  async saveKnowledgeBase() {
    try {
      const knowledgePath = path.join(__dirname, 'processed_knowledge', 'knowledge_base.json')
      
      const toSave = {
        rules: Array.from(this.knowledge.rules.values()),
        patterns: Array.from(this.knowledge.patterns.values()),
        structures: Array.from(this.knowledge.structures.values()),
        stats: this.stats,
        timestamp: Date.now()
      }
      
      await fs.writeFile(knowledgePath, JSON.stringify(toSave, null, 2))
      console.log(`💾 Knowledge base saved`)
    } catch (error) {
      console.error(`❌ Failed to save knowledge base:`, error)
    }
  }
  
  /**
   * OBTER ESTATÍSTICAS
   */
  getStats() {
    return {
      ...this.stats,
      knowledgeBase: {
        rules: this.knowledge.rules.size,
        patterns: this.knowledge.patterns.size,
        structures: this.knowledge.structures.size,
        characters: this.knowledge.characters.size,
        dialogues: this.knowledge.dialogues.size,
        scenes: this.knowledge.scenes.size,
        themes: this.knowledge.themes.size
      }
    }
  }
}

// Se executado diretamente, rodar demonstração
if (import.meta.url === `file://${process.argv[1]}`) {
  const engine = new CinemaKnowledgeEngine()
  
  async function demo() {
    await engine.initialize()
    
    // Se um arquivo foi passado como argumento
    if (process.argv[2]) {
      const filePath = process.argv[2]
      console.log(`\n📖 Processing file: ${filePath}`)
      
      const result = await engine.processMaterial(filePath)
      
      if (result.success) {
        console.log('\n✨ Knowledge extracted successfully!')
        console.log('\n📊 Stats:', engine.getStats())
        
        // Fazer uma consulta de exemplo
        console.log('\n🔍 Example query: "dialogue"')
        const queryResult = await engine.queryKnowledge('dialogue')
        console.log('Results:', queryResult)
      }
    } else {
      console.log('\n📝 Usage: node cinema_knowledge_engine.js <file_path>')
      console.log('Example: node cinema_knowledge_engine.js raw_materials/books/save_the_cat.pdf')
      
      // Mostrar conhecimento existente
      const stats = engine.getStats()
      console.log('\n📊 Current knowledge base:', stats.knowledgeBase)
    }
  }
  
  demo().catch(console.error)
}

export default CinemaKnowledgeEngine
export { CinemaKnowledgeEngine, KNOWN_STRUCTURES }