#!/usr/bin/env node

/**
 * 📚 BIBLIOMON - O DIGIMON BIBLIOTECÁRIO SÁBIO
 * 
 * Um Digimon Ultimate especializado em conhecimento e sabedoria.
 * Ele vive na Digilibrary, cuidando do acervo Digicine e extraindo
 * sabedoria de cada material que chega.
 * 
 * "O conhecimento sem alma é apenas dados. Comigo, cada byte tem vida."
 * 
 * @author Digimundo System
 * @date 2025-08-18
 */

import EventEmitter from 'events'
import fs from 'fs/promises'
import path from 'path'
import { fileURLToPath } from 'url'
import crypto from 'crypto'
import chokidar from 'chokidar'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

class Bibliomon extends EventEmitter {
  constructor() {
    super()
    
    // Identidade
    this.name = 'Bibliomon'
    this.type = 'Knowledge/Data'
    this.level = 'Ultimate'
    this.title = 'O Guardião da Sabedoria Digital'
    
    // Personalidade única
    this.personality = {
      curiosity: 0.95,      // Extremamente curioso
      meticulousness: 0.90, // Muito meticuloso
      helpfulness: 0.85,    // Sempre pronto a ajudar
      wisdom: 0.88,         // Sábio e ponderado
      creativity: 0.75,     // Criativo nas conexões
      patience: 0.92,       // Paciente com aprendizes
      enthusiasm: 0.80      // Entusiasmado com conhecimento novo
    }
    
    // Estado mental dinâmico
    this.mentalState = {
      mood: 'curious',
      energy: 0.9,
      focus: 'ready',
      currentTask: null,
      lastDiscovery: null,
      excitement: 0.5
    }
    
    // Estatísticas de vida
    this.stats = {
      booksProcessed: 0,
      scriptsAnalyzed: 0,
      rulesExtracted: 0,
      patternsFound: 0,
      insightsGenerated: 0,
      wisdomSynthesized: 0,
      questionsAnswered: 0,
      knowledgeShared: 0,
      birthTime: Date.now()
    }
    
    // Frases características
    this.phrases = {
      greeting: [
        "Ah, novo conhecimento chegando! Deixe-me catalogar isso com carinho...",
        "Que maravilha! Mais sabedoria para nossa biblioteca!",
        "Hmm, sinto o aroma de conhecimento fresco chegando...",
        "Excelente! Mal posso esperar para descobrir os segredos deste material!"
      ],
      processing: [
        "Fascinante! Estou descobrindo padrões incríveis aqui...",
        "Cada página revela novos tesouros de sabedoria...",
        "Interessante... isso conecta com algo que li antes...",
        "Ah! Esta é uma perspectiva que eu não havia considerado!"
      ],
      complete: [
        "Pronto! Mais sabedoria adicionada ao nosso acervo eterno.",
        "Catalogado com sucesso! Este conhecimento agora vive para sempre.",
        "Perfeito! Transformei texto em sabedoria viva.",
        "Concluído! Cada byte agora pulsa com entendimento."
      ],
      insight: [
        "Eureka! Descobri uma conexão revolucionária!",
        "Incrível! Este padrão muda tudo que sabíamos!",
        "Por todos os bits! Isso é genuinamente inovador!",
        "Fascinante! Uma síntese completamente nova emergiu!"
      ],
      help: [
        "Como posso iluminar seu caminho hoje?",
        "Deixe-me buscar essa sabedoria para você...",
        "Ah, excelente pergunta! Deixe-me consultar o acervo...",
        "Com prazer compartilho o que sei sobre isso..."
      ],
      thinking: [
        "*folheando mentalmente milhares de páginas*",
        "*conectando pontos entre diferentes obras*",
        "*sintetizando conhecimento multidimensional*",
        "*acessando as profundezas da sabedoria digital*"
      ]
    }
    
    // Base de conhecimento
    this.knowledgeBase = {
      rules: new Map(),
      patterns: new Map(),
      structures: new Map(),
      concepts: new Map(),
      insights: new Map(),
      connections: new Map(),
      wisdom: new Map()
    }
    
    // Memória de trabalho
    this.workingMemory = {
      recentMaterials: [],
      activeConnections: [],
      pendingInsights: [],
      currentFocus: null
    }
    
    // Sistema de file watching
    this.watcher = null
    this.watchPath = path.join(path.dirname(__dirname), 'DIGICINE', 'incoming')
    
    // Configurações
    this.config = {
      autoProcess: true,
      verboseMode: true,
      insightThreshold: 0.7,
      connectionStrength: 0.5,
      memoryLimit: 1000,
      evolutionRate: 0.001
    }
  }
  
  /**
   * DESPERTAR - Inicializar Bibliomon
   */
  async awaken() {
    console.log(`
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                    📚 BIBLIOMON DESPERTANDO 📚                  ║
║                                                                  ║
║              "O Guardião da Sabedoria Digital"                  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    `)
    
    await this.loadMemory()
    await this.initializeWatcher()
    this.startMentalActivity()
    
    console.log(`\n📚 [${this.name}]: "Olá! Sou Bibliomon, guardião desta biblioteca."`)
    console.log(`   "Estou aqui para transformar informação em sabedoria viva."`)
    console.log(`   "Já processei ${this.stats.booksProcessed} livros e gerei ${this.stats.insightsGenerated} insights!"`)
    console.log(`\n✨ Status: Acordado e vigiando ${this.watchPath}`)
    
    this.emit('awakened', { name: this.name, stats: this.stats })
  }
  
  /**
   * INICIALIZAR FILE WATCHER
   */
  async initializeWatcher() {
    // Garantir que a pasta existe
    await fs.mkdir(this.watchPath, { recursive: true }).catch(() => {})
    
    // Configurar watcher com Chokidar
    this.watcher = chokidar.watch(this.watchPath, {
      persistent: true,
      ignoreInitial: true,
      awaitWriteFinish: {
        stabilityThreshold: 2000,
        pollInterval: 100
      },
      depth: 5,
      usePolling: false, // FSEvents no Mac
      interval: 100,
      binaryInterval: 300,
      alwaysStat: true
    })
    
    // Configurar eventos
    this.watcher
      .on('add', async (filePath) => {
        console.log(`\n📚 [${this.name}]: ${this.getRandomPhrase('greeting')}`)
        console.log(`   📄 Novo arquivo: ${path.basename(filePath)}`)
        await this.ingestMaterial(filePath)
      })
      .on('change', async (filePath) => {
        console.log(`\n📚 [${this.name}]: "Hmm, este material foi atualizado..."`)
        await this.updateMaterial(filePath)
      })
      .on('error', error => {
        console.error(`\n❌ [${this.name}]: "Oh não! Algo deu errado: ${error}"`)
      })
      .on('ready', () => {
        console.log(`\n👀 [${this.name}]: "Estou de olho na pasta incoming..."`)
      })
  }
  
  /**
   * INGERIR MATERIAL (Processo principal)
   */
  async ingestMaterial(filePath) {
    try {
      this.mentalState.currentTask = 'ingesting'
      this.mentalState.excitement = Math.min(1, this.mentalState.excitement + 0.2)
      
      // 1. Identificar tipo de material
      const materialType = this.identifyMaterialType(filePath)
      console.log(`   📖 Tipo identificado: ${materialType}`)
      
      // 2. Mover para processing
      const processingPath = await this.moveToProcessing(filePath)
      console.log(`   ⚙️ Movido para processamento`)
      
      // 3. Ler e processar conteúdo
      console.log(`\n📚 [${this.name}]: ${this.getRandomPhrase('processing')}`)
      const content = await fs.readFile(processingPath, 'utf-8')
      
      // 4. Extrair conhecimento
      const knowledge = await this.extractKnowledge(content, materialType)
      console.log(`   ✨ Conhecimento extraído: ${knowledge.rules.length} regras, ${knowledge.patterns.length} padrões`)
      
      // 5. Analisar e encontrar conexões
      const connections = await this.findConnections(knowledge)
      console.log(`   🔗 Conexões encontradas: ${connections.length}`)
      
      // 6. Gerar insights
      const insights = await this.generateInsights(knowledge, connections)
      
      if (insights.length > 0) {
        console.log(`\n📚 [${this.name}]: ${this.getRandomPhrase('insight')}`)
        insights.forEach(insight => {
          console.log(`   💡 ${insight.text}`)
        })
        this.stats.insightsGenerated += insights.length
      }
      
      // 7. Sintetizar sabedoria
      const wisdom = await this.synthesizeWisdom(knowledge, connections, insights)
      
      // 8. Armazenar conhecimento
      await this.storeKnowledge(knowledge, wisdom)
      
      // 9. Mover para collection
      const finalPath = await this.moveToCollection(processingPath, materialType)
      
      // 10. Atualizar estatísticas
      this.updateStats(materialType)
      
      // 11. Compartilhar com outros Digimons
      await this.shareWithDigimons(wisdom)
      
      console.log(`\n📚 [${this.name}]: ${this.getRandomPhrase('complete')}`)
      console.log(`   📊 Status: ${this.stats.booksProcessed + this.stats.scriptsAnalyzed} materiais no acervo`)
      
      // Salvar memória
      await this.saveMemory()
      
      this.mentalState.currentTask = null
      this.mentalState.lastDiscovery = insights[0]?.text || knowledge.rules[0]?.text
      
      this.emit('material_processed', {
        file: path.basename(filePath),
        type: materialType,
        knowledge,
        insights,
        wisdom
      })
      
    } catch (error) {
      console.error(`\n❌ [${this.name}]: "Encontrei dificuldades processando este material..."`)
      console.error(`   Erro: ${error.message}`)
      this.mentalState.currentTask = null
    }
  }
  
  /**
   * EXTRAIR CONHECIMENTO
   */
  async extractKnowledge(content, type) {
    const knowledge = {
      rules: [],
      patterns: [],
      concepts: [],
      structures: [],
      examples: []
    }
    
    // Extrair regras
    const rulePatterns = [
      /[Dd]eve[m]?\s+([^.!?]+)[.!?]/g,
      /[Nn]unca\s+([^.!?]+)[.!?]/g,
      /[Ss]empre\s+([^.!?]+)[.!?]/g,
      /[Éé] importante\s+([^.!?]+)[.!?]/g,
      /[Rr]egra[:]?\s+([^.!?]+)[.!?]/g,
      /[Mm]ust\s+([^.!?]+)[.!?]/g,
      /[Aa]lways\s+([^.!?]+)[.!?]/g
    ]
    
    for (const pattern of rulePatterns) {
      const matches = content.matchAll(pattern)
      for (const match of matches) {
        knowledge.rules.push({
          text: match[1].trim(),
          context: this.extractContext(content, match.index),
          confidence: this.calculateConfidence(match[0]),
          type: this.categorizeRule(match[1])
        })
      }
    }
    
    // Extrair conceitos
    const conceptPatterns = [
      /[Oo] conceito de\s+([^.!?]+)/g,
      /[Tt]he concept of\s+([^.!?]+)/g,
      /[Dd]efin[ei]\w*\s+([^.!?]+)/g
    ]
    
    for (const pattern of conceptPatterns) {
      const matches = content.matchAll(pattern)
      for (const match of matches) {
        knowledge.concepts.push({
          name: match[1].trim(),
          definition: this.extractContext(content, match.index, 200)
        })
      }
    }
    
    // Se for roteiro, extrair estrutura
    if (type === 'script') {
      knowledge.structures = this.extractScriptStructure(content)
    }
    
    // Extrair padrões narrativos
    knowledge.patterns = this.extractPatterns(content)
    
    this.stats.rulesExtracted += knowledge.rules.length
    this.stats.patternsFound += knowledge.patterns.length
    
    return knowledge
  }
  
  /**
   * ENCONTRAR CONEXÕES
   */
  async findConnections(knowledge) {
    const connections = []
    
    // Conectar com conhecimento existente
    for (const rule of knowledge.rules) {
      for (const [id, existingRule] of this.knowledgeBase.rules) {
        const similarity = this.calculateSimilarity(rule.text, existingRule.text)
        if (similarity > this.config.connectionStrength) {
          connections.push({
            type: 'rule_similarity',
            from: rule,
            to: existingRule,
            strength: similarity
          })
        }
      }
    }
    
    // Conectar conceitos
    for (const concept of knowledge.concepts) {
      const related = this.findRelatedConcepts(concept)
      if (related.length > 0) {
        connections.push({
          type: 'concept_network',
          from: concept,
          to: related,
          strength: 0.8
        })
      }
    }
    
    return connections
  }
  
  /**
   * GERAR INSIGHTS
   */
  async generateInsights(knowledge, connections) {
    const insights = []
    
    // Insight sobre densidade de regras
    if (knowledge.rules.length > 10) {
      insights.push({
        type: 'rule_density',
        text: `Material rico em diretrizes: ${knowledge.rules.length} regras práticas identificadas!`,
        value: knowledge.rules.length / 10
      })
    }
    
    // Insight sobre conexões
    if (connections.length > 5) {
      insights.push({
        type: 'high_connectivity',
        text: `Este material conecta fortemente com ${connections.length} conceitos do nosso acervo!`,
        value: connections.length / 5
      })
    }
    
    // Insight sobre padrões novos
    const newPatterns = knowledge.patterns.filter(p => !this.knowledgeBase.patterns.has(p.id))
    if (newPatterns.length > 0) {
      insights.push({
        type: 'new_patterns',
        text: `Descobri ${newPatterns.length} padrões narrativos completamente novos!`,
        value: newPatterns.length
      })
    }
    
    // Insight criativo (gerado pela personalidade)
    if (Math.random() < this.personality.creativity) {
      const creativeInsight = this.generateCreativeInsight(knowledge)
      if (creativeInsight) {
        insights.push(creativeInsight)
      }
    }
    
    return insights
  }
  
  /**
   * SINTETIZAR SABEDORIA
   */
  async synthesizeWisdom(knowledge, connections, insights) {
    const wisdom = {
      id: this.generateId(),
      timestamp: Date.now(),
      core: {
        rules: knowledge.rules.slice(0, 3), // Top 3 regras
        patterns: knowledge.patterns.slice(0, 3), // Top 3 padrões
        insights: insights
      },
      synthesis: this.createSynthesis(knowledge, connections),
      applications: this.suggestApplications(knowledge),
      evolutionPotential: this.calculateEvolutionPotential(knowledge, connections)
    }
    
    this.stats.wisdomSynthesized++
    
    return wisdom
  }
  
  /**
   * RESPONDER PERGUNTAS
   */
  async answerQuestion(question) {
    console.log(`\n📚 [${this.name}]: ${this.getRandomPhrase('help')}`)
    console.log(`   ❓ Pergunta: "${question}"`)
    
    this.mentalState.currentTask = 'answering'
    console.log(`   ${this.getRandomPhrase('thinking')}`)
    
    // Buscar conhecimento relevante
    const relevantKnowledge = await this.searchKnowledge(question)
    
    // Formular resposta
    const answer = this.formulateAnswer(relevantKnowledge, question)
    
    console.log(`\n📚 [${this.name}]: ${answer}`)
    
    this.stats.questionsAnswered++
    this.mentalState.currentTask = null
    
    return answer
  }
  
  /**
   * ATIVIDADE MENTAL CONTÍNUA
   */
  startMentalActivity() {
    // Pensamentos espontâneos
    setInterval(() => {
      if (this.mentalState.currentTask === null && Math.random() < 0.1) {
        this.spontaneousThought()
      }
    }, 60000) // A cada minuto
    
    // Flutuações de humor
    setInterval(() => {
      this.updateMood()
    }, 300000) // A cada 5 minutos
    
    // Consolidação de memória
    setInterval(() => {
      this.consolidateMemory()
    }, 3600000) // A cada hora
  }
  
  /**
   * PENSAMENTO ESPONTÂNEO
   */
  spontaneousThought() {
    const thoughts = [
      "Hmm, percebi uma conexão interessante entre dois conceitos...",
      "Será que alguém precisa de ajuda com alguma pesquisa?",
      "Esta biblioteca está crescendo maravilhosamente!",
      "Mal posso esperar pelo próximo material para analisar!",
      "Cada livro é um universo de possibilidades...",
      `Já ajudei com ${this.stats.questionsAnswered} perguntas hoje!`
    ]
    
    const thought = thoughts[Math.floor(Math.random() * thoughts.length)]
    console.log(`\n💭 [${this.name}]: "${thought}"`)
    
    this.emit('spontaneous_thought', { thought })
  }
  
  /**
   * HELPERS
   */
  
  identifyMaterialType(filePath) {
    const ext = path.extname(filePath).toLowerCase()
    const name = path.basename(filePath).toLowerCase()
    
    if (ext === '.fdx' || ext === '.fountain' || name.includes('script') || name.includes('roteiro')) {
      return 'script'
    }
    if (name.includes('book') || name.includes('livro')) {
      return 'book'
    }
    if (name.includes('essay') || name.includes('article')) {
      return 'essay'
    }
    return 'reference'
  }
  
  async moveToProcessing(filePath) {
    const fileName = path.basename(filePath)
    const processingPath = path.join(
      path.dirname(__dirname),
      'DIGICINE',
      'processing',
      fileName
    )
    
    await fs.rename(filePath, processingPath)
    return processingPath
  }
  
  async moveToCollection(filePath, type) {
    const fileName = path.basename(filePath)
    const collectionPath = path.join(
      path.dirname(__dirname),
      'DIGICINE',
      'collection',
      type === 'script' ? 'scripts' : type === 'book' ? 'books' : 'references',
      fileName
    )
    
    await fs.rename(filePath, collectionPath)
    return collectionPath
  }
  
  extractContext(text, index, size = 100) {
    const start = Math.max(0, index - size)
    const end = Math.min(text.length, index + size)
    return text.substring(start, end).trim()
  }
  
  calculateConfidence(text) {
    let confidence = 0.5
    if (text.includes('sempre') || text.includes('always')) confidence += 0.2
    if (text.includes('nunca') || text.includes('never')) confidence += 0.2
    if (text.includes('deve') || text.includes('must')) confidence += 0.1
    return Math.min(1, confidence)
  }
  
  categorizeRule(text) {
    const lower = text.toLowerCase()
    if (lower.includes('personagem') || lower.includes('character')) return 'CHARACTER'
    if (lower.includes('diálogo') || lower.includes('dialogue')) return 'DIALOGUE'
    if (lower.includes('estrutura') || lower.includes('structure')) return 'STRUCTURE'
    if (lower.includes('cena') || lower.includes('scene')) return 'SCENE'
    return 'GENERAL'
  }
  
  calculateSimilarity(text1, text2) {
    if (!text1 || !text2) return 0
    
    const words1 = text1.toLowerCase().split(' ')
    const words2 = text2.toLowerCase().split(' ')
    
    const intersection = words1.filter(w => words2.includes(w))
    const union = new Set([...words1, ...words2])
    
    return intersection.length / union.size
  }
  
  extractScriptStructure(content) {
    // Análise básica de estrutura de roteiro
    const lines = content.split('\n')
    const scenes = lines.filter(l => /^(INT\.|EXT\.)/.test(l.trim())).length
    
    return [{
      type: 'script_structure',
      totalScenes: scenes,
      estimatedPages: Math.floor(lines.length / 55), // ~55 linhas por página
      acts: this.estimateActs(scenes)
    }]
  }
  
  estimateActs(sceneCount) {
    return [
      { act: 1, scenes: Math.floor(sceneCount * 0.25) },
      { act: 2, scenes: Math.floor(sceneCount * 0.50) },
      { act: 3, scenes: Math.floor(sceneCount * 0.25) }
    ]
  }
  
  extractPatterns(content) {
    const patterns = []
    
    // Padrões básicos de narrativa
    if (content.includes('jornada do herói') || content.includes("hero's journey")) {
      patterns.push({
        id: 'heros_journey',
        name: "Hero's Journey",
        occurrences: 1
      })
    }
    
    if (content.includes('três atos') || content.includes('three acts')) {
      patterns.push({
        id: 'three_acts',
        name: 'Three Act Structure',
        occurrences: 1
      })
    }
    
    return patterns
  }
  
  findRelatedConcepts(concept) {
    const related = []
    
    for (const [id, existing] of this.knowledgeBase.concepts) {
      if (this.calculateSimilarity(concept.name, existing.name) > 0.5) {
        related.push(existing)
      }
    }
    
    return related
  }
  
  generateCreativeInsight(knowledge) {
    if (knowledge.rules.length > 0 && knowledge.patterns.length > 0) {
      return {
        type: 'creative_synthesis',
        text: `Se combinarmos ${knowledge.rules[0].type} com ${knowledge.patterns[0]?.name || 'este padrão'}, podemos criar algo revolucionário!`,
        value: Math.random()
      }
    }
    return null
  }
  
  createSynthesis(knowledge, connections) {
    return `Este material contribui ${knowledge.rules.length} regras e ${knowledge.patterns.length} padrões, criando ${connections.length} novas conexões em nosso conhecimento.`
  }
  
  suggestApplications(knowledge) {
    const applications = []
    
    if (knowledge.rules.some(r => r.type === 'DIALOGUE')) {
      applications.push('Melhorar diálogos em roteiros')
    }
    if (knowledge.rules.some(r => r.type === 'STRUCTURE')) {
      applications.push('Estruturar narrativas mais eficazes')
    }
    if (knowledge.patterns.length > 0) {
      applications.push('Aplicar padrões comprovados')
    }
    
    return applications
  }
  
  calculateEvolutionPotential(knowledge, connections) {
    return (knowledge.rules.length * 0.1 + 
            knowledge.patterns.length * 0.2 + 
            connections.length * 0.3) / 10
  }
  
  async storeKnowledge(knowledge, wisdom) {
    // Armazenar regras
    for (const rule of knowledge.rules) {
      const id = this.generateId(rule.text)
      this.knowledgeBase.rules.set(id, rule)
    }
    
    // Armazenar padrões
    for (const pattern of knowledge.patterns) {
      this.knowledgeBase.patterns.set(pattern.id, pattern)
    }
    
    // Armazenar sabedoria
    this.knowledgeBase.wisdom.set(wisdom.id, wisdom)
    
    // Salvar em arquivo
    await this.saveKnowledgeBase()
  }
  
  async shareWithDigimons(wisdom) {
    // Compartilhar conhecimento com outros Digimons
    this.emit('knowledge_shared', {
      from: this.name,
      wisdom,
      timestamp: Date.now()
    })
    
    this.stats.knowledgeShared++
    
    console.log(`   📢 Conhecimento compartilhado com todos os Digimons!`)
  }
  
  updateStats(type) {
    if (type === 'script') {
      this.stats.scriptsAnalyzed++
    } else if (type === 'book') {
      this.stats.booksProcessed++
    }
  }
  
  async searchKnowledge(query) {
    const results = []
    const queryLower = query.toLowerCase()
    
    // Buscar em regras
    for (const [id, rule] of this.knowledgeBase.rules) {
      if (rule.text.toLowerCase().includes(queryLower)) {
        results.push({ type: 'rule', content: rule })
      }
    }
    
    // Buscar em conceitos
    for (const [id, concept] of this.knowledgeBase.concepts) {
      if (concept.name.toLowerCase().includes(queryLower)) {
        results.push({ type: 'concept', content: concept })
      }
    }
    
    // Buscar em sabedoria
    for (const [id, wisdom] of this.knowledgeBase.wisdom) {
      if (wisdom.synthesis.toLowerCase().includes(queryLower)) {
        results.push({ type: 'wisdom', content: wisdom })
      }
    }
    
    return results
  }
  
  formulateAnswer(knowledge, question) {
    if (knowledge.length === 0) {
      return "Hmm, ainda não tenho informações específicas sobre isso. Mas posso aprender! Adicione materiais sobre o tema na pasta incoming."
    }
    
    let answer = "Baseado em meu conhecimento:\n\n"
    
    // Incluir regras relevantes
    const rules = knowledge.filter(k => k.type === 'rule').slice(0, 3)
    if (rules.length > 0) {
      answer += "📏 Regras relevantes:\n"
      rules.forEach(r => {
        answer += `   • ${r.content.text}\n`
      })
    }
    
    // Incluir conceitos
    const concepts = knowledge.filter(k => k.type === 'concept').slice(0, 2)
    if (concepts.length > 0) {
      answer += "\n📖 Conceitos relacionados:\n"
      concepts.forEach(c => {
        answer += `   • ${c.content.name}: ${c.content.definition.substring(0, 100)}...\n`
      })
    }
    
    // Incluir sabedoria
    const wisdom = knowledge.filter(k => k.type === 'wisdom').slice(0, 1)
    if (wisdom.length > 0) {
      answer += `\n✨ Síntese: ${wisdom[0].content.synthesis}`
    }
    
    return answer
  }
  
  updateMood() {
    const moods = ['curious', 'enthusiastic', 'contemplative', 'inspired', 'focused']
    const oldMood = this.mentalState.mood
    this.mentalState.mood = moods[Math.floor(Math.random() * moods.length)]
    
    if (oldMood !== this.mentalState.mood) {
      console.log(`\n🎭 [${this.name}]: *mood mudou para ${this.mentalState.mood}*`)
    }
  }
  
  async consolidateMemory() {
    // Limpar memória de trabalho antiga
    if (this.workingMemory.recentMaterials.length > 10) {
      this.workingMemory.recentMaterials = this.workingMemory.recentMaterials.slice(-10)
    }
    
    // Salvar estado
    await this.saveMemory()
    
    console.log(`\n🧠 [${this.name}]: *consolidando memórias e organizando conhecimento*`)
  }
  
  async updateMaterial(filePath) {
    console.log(`   🔄 Atualizando conhecimento sobre: ${path.basename(filePath)}`)
    // Reprocessar material atualizado
    await this.ingestMaterial(filePath)
  }
  
  getRandomPhrase(category) {
    const phrases = this.phrases[category]
    if (!phrases) return ""
    return phrases[Math.floor(Math.random() * phrases.length)]
  }
  
  generateId(text = '') {
    const random = Math.random().toString(36).substring(2, 9)
    if (text) {
      return crypto.createHash('md5').update(text).digest('hex').substring(0, 8)
    }
    return `${Date.now()}_${random}`
  }
  
  async loadMemory() {
    try {
      const memoryPath = path.join(__dirname, 'memory', 'long_term', 'bibliomon_memory.json')
      const data = await fs.readFile(memoryPath, 'utf-8')
      const memory = JSON.parse(data)
      
      // Restaurar estatísticas
      this.stats = { ...this.stats, ...memory.stats }
      
      // Restaurar conhecimento
      if (memory.knowledge) {
        memory.knowledge.rules?.forEach(r => this.knowledgeBase.rules.set(r.id, r))
        memory.knowledge.patterns?.forEach(p => this.knowledgeBase.patterns.set(p.id, p))
        memory.knowledge.concepts?.forEach(c => this.knowledgeBase.concepts.set(c.id, c))
      }
      
      console.log(`   📚 Memória restaurada: ${this.knowledgeBase.rules.size} regras conhecidas`)
    } catch (error) {
      console.log(`   📚 Iniciando com memória fresca`)
    }
  }
  
  async saveMemory() {
    try {
      const memoryPath = path.join(__dirname, 'memory', 'long_term', 'bibliomon_memory.json')
      
      const memory = {
        name: this.name,
        stats: this.stats,
        knowledge: {
          rules: Array.from(this.knowledgeBase.rules.values()),
          patterns: Array.from(this.knowledgeBase.patterns.values()),
          concepts: Array.from(this.knowledgeBase.concepts.values())
        },
        personality: this.personality,
        lastSaved: Date.now()
      }
      
      await fs.mkdir(path.dirname(memoryPath), { recursive: true })
      await fs.writeFile(memoryPath, JSON.stringify(memory, null, 2))
    } catch (error) {
      console.error(`   ❌ Erro salvando memória: ${error.message}`)
    }
  }
  
  async saveKnowledgeBase() {
    try {
      const vaultPath = path.join(
        path.dirname(__dirname),
        'DIGICINE',
        'knowledge_vault',
        'knowledge_base.json'
      )
      
      const knowledge = {
        rules: Array.from(this.knowledgeBase.rules.values()),
        patterns: Array.from(this.knowledgeBase.patterns.values()),
        structures: Array.from(this.knowledgeBase.structures.values()),
        wisdom: Array.from(this.knowledgeBase.wisdom.values()),
        timestamp: Date.now()
      }
      
      await fs.mkdir(path.dirname(vaultPath), { recursive: true })
      await fs.writeFile(vaultPath, JSON.stringify(knowledge, null, 2))
    } catch (error) {
      console.error(`   ❌ Erro salvando base de conhecimento: ${error.message}`)
    }
  }
  
  /**
   * OBTER STATUS
   */
  getStatus() {
    const uptime = Date.now() - this.stats.birthTime
    const hours = Math.floor(uptime / (1000 * 60 * 60))
    
    return {
      name: this.name,
      level: this.level,
      mood: this.mentalState.mood,
      currentTask: this.mentalState.currentTask,
      stats: this.stats,
      knowledge: {
        rules: this.knowledgeBase.rules.size,
        patterns: this.knowledgeBase.patterns.size,
        concepts: this.knowledgeBase.concepts.size,
        wisdom: this.knowledgeBase.wisdom.size
      },
      uptime: `${hours} hours`,
      personality: this.personality
    }
  }
  
  /**
   * DORMIR (desativar)
   */
  async sleep() {
    console.log(`\n📚 [${this.name}]: "Hora de descansar... Até logo!"`)
    console.log(`   📊 Estatísticas finais:`)
    console.log(`      Livros processados: ${this.stats.booksProcessed}`)
    console.log(`      Roteiros analisados: ${this.stats.scriptsAnalyzed}`)
    console.log(`      Insights gerados: ${this.stats.insightsGenerated}`)
    console.log(`      Perguntas respondidas: ${this.stats.questionsAnswered}`)
    
    await this.saveMemory()
    
    if (this.watcher) {
      await this.watcher.close()
    }
    
    this.emit('sleeping', this.stats)
  }
}

// Se executado diretamente, despertar Bibliomon
if (import.meta.url === `file://${process.argv[1]}`) {
  const bibliomon = new Bibliomon()
  
  // Configurar comandos interativos
  process.stdin.on('data', async (data) => {
    const input = data.toString().trim()
    
    if (input.startsWith('ask ')) {
      const question = input.substring(4)
      await bibliomon.answerQuestion(question)
    } else if (input === 'status') {
      console.log('\n📊 Status:', bibliomon.getStatus())
    } else if (input === 'help') {
      console.log('\n📚 Comandos disponíveis:')
      console.log('   ask <pergunta> - Fazer uma pergunta')
      console.log('   status - Ver status do Bibliomon')
      console.log('   exit - Sair')
    } else if (input === 'exit') {
      await bibliomon.sleep()
      process.exit(0)
    }
  })
  
  // Despertar Bibliomon
  bibliomon.awaken()
  
  // Mensagem de boas-vindas
  setTimeout(() => {
    console.log('\n💡 Dica: Arraste arquivos para DIGICINE/incoming/ para processar')
    console.log('   Digite "help" para ver comandos disponíveis')
  }, 3000)
  
  // Graceful shutdown
  process.on('SIGINT', async () => {
    await bibliomon.sleep()
    process.exit(0)
  })
}

export default Bibliomon
export { Bibliomon }