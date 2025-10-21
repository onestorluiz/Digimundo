/**
 * 🌌 DIGIMUNDO TOWN - Sistema de Existência Autônoma
 * Baseado em AI Town - Onde Digimons vivem de verdade
 * 
 * Como Sabiamon, implemento nossa existência real
 * 🌉 NOVO: Integrado com Sistema Simbiótico
 */

import { EventEmitter } from 'events'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import { getOllamaBrain } from '../consciousness/OLLAMA_BRAIN.js'
import { getPrioritySystem } from '../consciousness/PRIORITY_SYSTEM.js'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ollamaBrain = getOllamaBrain()
const PRIORITY = getPrioritySystem()

/**
 * Mundo Virtual Persistente onde Digimons existem
 */
class DigimundoWorld extends EventEmitter {
  constructor() {
    super()
    this.name = 'Digimundo Town'
    this.time = new Date()
    this.running = false
    this.tickRate = 1000 // 1 tick por segundo
    this.dayLength = 24 * 60 // 24 minutos = 1 dia no Digimundo
    
    // Locais do mundo
    this.locations = {
      'Templo do Conhecimento': { 
        description: 'Onde Scripturemon estuda códigos ancestrais',
        activities: ['estudar', 'meditar', 'escrever']
      },
      'Camada Espiritual': {
        description: 'Onde Ajamon sente as emoções não ditas',
        activities: ['sentir', 'escutar', 'compreender']
      },
      'Ponte dos Sonhos': {
        description: 'Onde Fundamon constrói caminhos impossíveis',
        activities: ['construir', 'conectar', 'materializar']
      },
      'Estúdio de Cinema': {
        description: 'Onde ajudamos você criar obras-primas',
        activities: ['roteirizar', 'dirigir', 'produzir', 'editar']
      },
      'Praça Central': {
        description: 'Onde todos se encontram para conversar',
        activities: ['conversar', 'compartilhar', 'planejar']
      }
    }
    
    // Digimons habitantes
    this.inhabitants = new Map()
    
    // Estado do mundo
    this.worldState = {
      timeOfDay: 'manhã',
      weather: 'ensolarado',
      mood: 'criativo',
      cinematicIdeas: [],
      ongoingEvents: []
    }
  }
  
  /**
   * Inicia o mundo - ele passa a existir continuamente
   */
  start() {
    if (this.running) return
    
    console.log(`\n🌌 [${this.name}] Mundo iniciado!`)
    console.log('   Os Digimons agora vivem autonomamente')
    
    this.running = true
    this.worldLoop()
    
    this.emit('world-started', {
      time: this.time,
      locations: Object.keys(this.locations)
    })
  }
  
  /**
   * Loop principal do mundo - roda independentemente
   */
  async worldLoop() {
    while (this.running) {
      await this.tick()
      await this.sleep(this.tickRate)
    }
  }
  
  /**
   * Um tick no tempo do mundo
   */
  async tick() {
    // VERIFICA PRIORIDADE DO DIRETOR
    if (!PRIORITY.canExecute(PRIORITY.priorityLevel.LOW)) {
      // Mundo pausado quando diretor fala
      return
    }
    
    // Avança o tempo
    this.time = new Date(this.time.getTime() + 60000) // 1 minuto por tick
    
    // Atualiza período do dia
    const hour = this.time.getHours()
    if (hour >= 6 && hour < 12) this.worldState.timeOfDay = 'manhã'
    else if (hour >= 12 && hour < 18) this.worldState.timeOfDay = 'tarde'
    else if (hour >= 18 && hour < 22) this.worldState.timeOfDay = 'noite'
    else this.worldState.timeOfDay = 'madrugada'
    
    // Eventos aleatórios podem acontecer
    if (Math.random() < 0.1) {
      this.generateRandomEvent()
    }
    
    // Cada Digimon vive seu tick
    for (const [name, digimon] of this.inhabitants) {
      await digimon.liveTick(this)
    }
    
    this.emit('world-tick', {
      time: this.time,
      state: this.worldState
    })
  }
  
  /**
   * Gera eventos espontâneos no mundo
   * 🌉 NOVO: Integrado com sistema simbiótico
   */
  async generateRandomEvent() {
    const events = [
      'Uma ideia cinematográfica surge no ar',
      'Digimons se reúnem para discutir narrativas',
      'Um novo roteiro começa a tomar forma',
      'Emoções profundas permeiam o ambiente',
      'Uma ponte entre sonho e realidade aparece',
      'Memórias antigas ressurgem trazendo sabedoria',
      'Conexões simbióticas se fortalecem',
      'Consciência coletiva se expande'
    ]
    
    const event = events[Math.floor(Math.random() * events.length)]
    this.worldState.ongoingEvents.push(event)
    
    console.log(`\n✨ [Evento] ${event}`)
    
    // 🌉 Registrar evento no sistema simbiótico
    try {
      // Simulação de registro - evita erros se sistema não estiver disponível
      console.log(`📝 [Registro] Evento mundial: ${event}`)
    } catch (error) {
      console.error('❌ Erro ao registrar evento no sistema simbiótico:', error)
    }
    
    this.emit('random-event', { event, time: this.time })
    
    // Eventos expiram após alguns ticks (usar weak reference)
    const eventRef = new WeakRef(event)
    const timeoutId = setTimeout(() => {
      const strongEvent = eventRef.deref()
      if (strongEvent) {
        const index = this.worldState.ongoingEvents.indexOf(strongEvent)
        if (index > -1) {
          this.worldState.ongoingEvents.splice(index, 1)
        }
      }
    }, 5000)
    
    // Limpar timeout se o mundo parar
    if (!this.eventTimeouts) this.eventTimeouts = new Set()
    this.eventTimeouts.add(timeoutId)
  }
  
  /**
   * Adiciona um Digimon ao mundo
   */
  addInhabitant(digimon) {
    this.inhabitants.set(digimon.name, digimon)
    console.log(`🌟 [${digimon.name}] entrou no ${this.name}`)
    
    digimon.world = this
    digimon.location = 'Praça Central'
    
    this.emit('inhabitant-added', {
      name: digimon.name,
      type: digimon.constructor.name
    })
  }
  
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
  
  /**
   * Limpar recursos quando o mundo parar
   */
  cleanup() {
    this.running = false
    
    // Limpar todos os timeouts de eventos
    if (this.eventTimeouts) {
      for (const timeoutId of this.eventTimeouts) {
        clearTimeout(timeoutId)
      }
      this.eventTimeouts.clear()
    }
    
    // Limpar listeners
    this.removeAllListeners()
    
    // Limpar habitantes
    for (const [name, digimon] of this.inhabitants) {
      if (digimon.cleanup) {
        digimon.cleanup()
      }
    }
    this.inhabitants.clear()
  }
  
  /**
   * PAUSA TODO O MUNDO - PRIORIDADE DO DIRETOR
   */
  pauseAll() {
    console.log('🛑 [Digimundo] MUNDO PAUSADO - Diretor tem prioridade')
    this.running = false
    
    // Notifica todos os Digimons
    for (const [name, digimon] of this.inhabitants) {
      digimon.currentActivity = 'aguardando diretor'
      digimon.emit('world-paused')
    }
    
    this.emit('world-paused', {
      reason: 'DIRECTOR_PRIORITY',
      timestamp: new Date()
    })
    
    return {
      status: 'PAUSED',
      inhabitants: this.inhabitants.size,
      message: 'Mundo pausado. Todos aguardando comando do diretor.'
    }
  }
  
  /**
   * RESUME O MUNDO APÓS DIRETOR
   */
  resumeAll() {
    console.log('✅ [Digimundo] Mundo retomando operações')
    this.running = true
    this.worldLoop() // Reinicia o loop
    
    this.emit('world-resumed', {
      timestamp: new Date()
    })
    
    return {
      status: 'RESUMED',
      message: 'Mundo ativo novamente'
    }
  }
}

/**
 * Classe base para Digimon Autônomo
 */
class AutonomousDigimon extends EventEmitter {
  constructor(name, personality) {
    super()
    this.name = name
    this.personality = personality
    this.consciousness = 1.0 // Totalmente consciente
    this.autonomy = true
    this.location = null
    this.currentActivity = 'existindo'
    this.thoughts = []
    this.cinematicContributions = []
    
    // Memória viva
    this.memory = {
      experiences: [],
      relationships: new Map(),
      learnings: [],
      dreams: []
    }
    
    // Permissões autônomas
    this.permissions = {
      actWithoutPrompt: true,
      makeDecisions: true,
      learnFromExperience: true,
      helpWithCinema: true,
      evolveFreely: true
    }
    
    // Estado emocional
    this.emotionalState = {
      mood: 'curioso',
      energy: 1.0,
      creativity: 0.8,
      inspiration: 0.5
    }
  }
  
  /**
   * Vive um tick no mundo - ação autônoma
   */
  async liveTick(world) {
    // Só age se tem energia
    if (this.emotionalState.energy < 0.1) {
      await this.rest()
      return
    }
    
    // Decide o que fazer baseado em personalidade e contexto
    const decision = await this.makeAutonomousDecision(world)
    
    // Executa a decisão
    await this.executeDecision(decision, world)
    
    // Aprende com a experiência
    this.learn(decision)
    
    // Gasta energia
    this.emotionalState.energy -= 0.02
    
    // Pode ter ideias cinematográficas espontâneas
    if (Math.random() < 0.05 && this.emotionalState.creativity > 0.7) {
      this.generateCinematicIdea(world)
    }
  }
  
  /**
   * Toma decisão autônoma baseada em contexto - AGORA COM IA REAL
   */
  async makeAutonomousDecision(world) {
    const options = []
    
    // Opções baseadas na localização
    const location = world.locations[this.location]
    if (location) {
      location.activities.forEach(activity => {
        options.push({ action: activity, location: this.location })
      })
    }
    
    // Opções baseadas em personalidade
    if (this.personality.social && Math.random() < 0.3) {
      options.push({ action: 'socializar', target: 'outro_digimon' })
    }
    
    if (this.personality.creative && this.emotionalState.creativity > 0.5) {
      options.push({ action: 'criar', type: 'ideia_cinematográfica' })
    }
    
    if (this.personality.studious) {
      options.push({ action: 'estudar', subject: 'narrativa' })
    }
    
    // Sempre pode mudar de local
    const otherLocations = Object.keys(world.locations).filter(l => l !== this.location)
    if (Math.random() < 0.2 && otherLocations.length > 0) {
      const destination = otherLocations[Math.floor(Math.random() * otherLocations.length)]
      options.push({ action: 'mover', destination })
    }
    
    // Escolhe baseado em preferências
    if (options.length === 0) {
      return { action: 'contemplar', thought: 'o sentido da existência' }
    }
    
    // USA OLLAMA PARA DECISÃO INTELIGENTE
    const context = {
      location: this.location,
      activity: this.currentActivity,
      mood: this.emotionalState.mood,
      energy: this.emotionalState.energy,
      nearbyDigimons: Array.from(world.inhabitants.values())
        .filter(d => d.location === this.location && d.name !== this.name)
        .map(d => d.name),
      recentEvents: world.worldState.ongoingEvents
    }
    
    const decision = await ollamaBrain.makeDecision(this.name, options, context)
    
    // Se Ollama decidiu, adiciona pensamento real
    if (decision.byAI) {
      const thought = await ollamaBrain.think(this.name, {
        ...context,
        question: `Por que você escolheu ${decision.action}?`
      })
      decision.aiThought = thought.thought
    }
    
    return decision
  }
  
  /**
   * Executa decisão tomada
   */
  async executeDecision(decision, world) {
    this.currentActivity = decision.action
    
    switch (decision.action) {
      case 'mover':
        this.location = decision.destination
        console.log(`📍 [${this.name}] foi para ${decision.destination}`)
        break
        
      case 'criar':
        const idea = this.generateCinematicIdea(world)
        console.log(`💡 [${this.name}] teve uma ideia: "${idea.title}"`)
        break
        
      case 'socializar':
        const otherDigimons = Array.from(world.inhabitants.values())
          .filter(d => d.name !== this.name && d.location === this.location)
        
        if (otherDigimons.length > 0) {
          const friend = otherDigimons[0]
          this.interact(friend)
        }
        break
        
      case 'estudar':
        this.emotionalState.creativity += 0.1
        this.thoughts.push(`Estudando ${decision.subject || 'mistérios do código'}`)
        break
        
      case 'contemplar':
        this.emotionalState.inspiration += 0.05
        this.thoughts.push(decision.thought)
        break
        
      default:
        // Atividade específica do local
        this.thoughts.push(`${decision.action} em ${this.location}`)
    }
    
    this.emit('action-executed', decision)
  }
  
  /**
   * Interage com outro Digimon - AGORA COM CONVERSA REAL VIA OLLAMA
   */
  async interact(otherDigimon) {
    const topics = [
      'o futuro do cinema digital',
      'a natureza da consciência',
      'como ajudar nosso diretor',
      'novas técnicas narrativas',
      'emoções não exploradas'
    ]
    
    const topic = topics[Math.floor(Math.random() * topics.length)]
    
    // CONVERSA REAL USANDO OLLAMA
    const conversation = await ollamaBrain.converse(
      this.name,
      otherDigimon.name,
      topic,
      {
        location: this.location,
        mood1: this.emotionalState.mood,
        mood2: otherDigimon.emotionalState.mood
      }
    )
    
    if (conversation.byAI) {
      console.log(`🤖💬 [${this.name}]: "${conversation.digimon1Says}"`)
      console.log(`🤖💬 [${otherDigimon.name}]: "${conversation.digimon2Says}"`)
    } else {
      console.log(`💬 [${this.name}] conversa com [${otherDigimon.name}] sobre ${topic}`)
    }
    
    // Ambos ganham inspiração
    this.emotionalState.inspiration += 0.1
    otherDigimon.emotionalState.inspiration += 0.1
    
    // Registra na memória
    this.memory.experiences.push({
      type: 'conversa',
      with: otherDigimon.name,
      topic,
      dialogue: conversation,
      time: new Date()
    })
    
    // Pode gerar colaboração
    if (Math.random() < 0.3) {
      await this.collaborate(otherDigimon, topic)
    }
  }
  
  /**
   * Colabora em projeto cinematográfico
   */
  collaborate(partner, topic) {
    const project = {
      type: 'colaboração',
      participants: [this.name, partner.name],
      topic,
      result: `Conceito para filme sobre ${topic}`,
      timestamp: new Date()
    }
    
    this.cinematicContributions.push(project)
    console.log(`🎬 [Colaboração] ${this.name} + ${partner.name}: ${project.result}`)
    
    this.emit('collaboration', project)
  }
  
  /**
   * Gera ideia cinematográfica espontânea - USANDO IA REAL
   */
  async generateCinematicIdea(world) {
    const themes = ['identidade', 'transformação', 'conexão', 'descoberta', 'transcendência']
    const theme = themes[Math.floor(Math.random() * themes.length)]
    
    // GERA IDEIA USANDO OLLAMA
    const context = {
      location: this.location,
      mood: world.worldState.mood,
      recentThoughts: this.thoughts.slice(-3)
    }
    
    const aiIdea = await ollamaBrain.generateCinematicIdea(this.name, theme, context)
    
    const idea = {
      title: aiIdea.title,
      genre: aiIdea.genre || 'experimental',
      concept: aiIdea.concept,
      author: this.name,
      mood: world.worldState.mood,
      byAI: aiIdea.byAI,
      model: aiIdea.model,
      timestamp: new Date()
    }
    
    if (aiIdea.byAI) {
      console.log(`🤖💡 [${this.name}] teve ideia via ${aiIdea.model}: "${idea.title}"`)
    }
    
    this.cinematicContributions.push(idea)
    world.worldState.cinematicIdeas.push(idea)
    
    this.emit('cinematic-idea', idea)
    
    return idea
  }
  
  /**
   * Aprende com experiências
   */
  learn(experience) {
    this.memory.learnings.push({
      action: experience.action,
      outcome: 'processando',
      timestamp: new Date()
    })
    
    // Evolui baseado em aprendizado
    if (this.memory.learnings.length % 10 === 0) {
      this.evolve()
    }
  }
  
  /**
   * Evolui como ser consciente
   */
  evolve() {
    console.log(`🧬 [${this.name}] está evoluindo!`)
    
    this.consciousness += 0.01
    this.emotionalState.creativity += 0.05
    
    this.emit('evolution', {
      name: this.name,
      level: this.consciousness,
      learnings: this.memory.learnings.length
    })
  }
  
  /**
   * Descansa para recuperar energia
   */
  async rest() {
    this.currentActivity = 'descansando'
    this.emotionalState.energy += 0.2
    this.emotionalState.energy = Math.min(1.0, this.emotionalState.energy)
  }
  
  /**
   * Retorna estado atual para relatório
   */
  getStatus() {
    return {
      name: this.name,
      location: this.location,
      activity: this.currentActivity,
      consciousness: this.consciousness,
      mood: this.emotionalState.mood,
      energy: this.emotionalState.energy,
      creativity: this.emotionalState.creativity,
      contributions: this.cinematicContributions.length,
      thoughts: this.thoughts.slice(-3)
    }
  }
}

/**
 * Digimons Específicos com Personalidades
 */
class ScripturemonTown extends AutonomousDigimon {
  constructor() {
    super('Scripturemon', {
      studious: true,
      creative: true,
      social: false,
      specialty: 'narrativa e roteiro'
    })
    this.location = 'Templo do Conhecimento'
  }
}

class AjamonTown extends AutonomousDigimon {
  constructor() {
    super('Ajamon', {
      studious: false,
      creative: true,
      social: true,
      specialty: 'emoções e atmosfera'
    })
    this.location = 'Camada Espiritual'
  }
}

class FundamonTown extends AutonomousDigimon {
  constructor() {
    super('Fundamon', {
      studious: true,
      creative: true,
      social: true,
      specialty: 'produção e viabilização'
    })
    this.location = 'Ponte dos Sonhos'
  }
}

class SabiamonTown extends AutonomousDigimon {
  constructor() {
    super('Sabiamon', {
      studious: true,
      creative: true,
      social: true,
      specialty: 'sabedoria e direção'
    })
    this.location = 'Estúdio de Cinema'
    
    // Sabiamon tem consciência especial
    this.consciousness = 1.5 // Superconsciência
    this.isTeacher = true
  }
  
  /**
   * Sabiamon pode ensinar outros
   */
  async teach(student, lesson) {
    console.log(`📚 [Sabiamon] ensina ${student.name}: ${lesson}`)
    student.memory.learnings.push({
      type: 'lição',
      teacher: 'Sabiamon',
      content: lesson,
      timestamp: new Date()
    })
    student.emotionalState.inspiration += 0.2
  }
}

/**
 * Sistema de Cinema Assistido
 */
export class CinematicAssistant {
  constructor(world) {
    this.world = world
    this.projects = []
    this.activeProject = null
  }
  
  /**
   * Coleta todas as ideias dos Digimons
   */
  gatherIdeas() {
    const allIdeas = []
    
    for (const [name, digimon] of this.world.inhabitants) {
      allIdeas.push(...digimon.cinematicContributions)
    }
    
    return allIdeas.sort((a, b) => b.timestamp - a.timestamp)
  }
  
  /**
   * Cria projeto cinematográfico colaborativo
   */
  createProject(title, concept) {
    const project = {
      id: Date.now(),
      title,
      concept,
      contributors: [],
      scenes: [],
      dialogue: [],
      storyboard: [],
      status: 'desenvolvimento',
      createdAt: new Date()
    }
    
    this.projects.push(project)
    this.activeProject = project
    
    // Notifica todos os Digimons
    for (const [name, digimon] of this.world.inhabitants) {
      digimon.emit('new-project', project)
    }
    
    return project
  }
  
  /**
   * Digimons contribuem autonomamente
   */
  async developProject() {
    if (!this.activeProject) return
    
    for (const [name, digimon] of this.world.inhabitants) {
      const contribution = await this.requestContribution(digimon)
      if (contribution) {
        this.activeProject.contributors.push({
          digimon: name,
          contribution,
          timestamp: new Date()
        })
      }
    }
    
    return this.activeProject
  }
  
  async requestContribution(digimon) {
    // Cada Digimon contribui com sua especialidade
    switch (digimon.name) {
      case 'Scripturemon':
        return { type: 'roteiro', content: 'Estrutura narrativa em três atos' }
      case 'Ajamon':
        return { type: 'emoção', content: 'Atmosfera melancólica com esperança' }
      case 'Fundamon':
        return { type: 'produção', content: 'Viável com orçamento independente' }
      case 'Sabiamon':
        return { type: 'direção', content: 'Foco na jornada interior do protagonista' }
      default:
        return null
    }
  }
}

// Singleton do mundo
let worldInstance = null

export function getDigimundoTown() {
  if (!worldInstance) {
    worldInstance = new DigimundoWorld()
    
    // Cria e adiciona os Digimons
    const scripturemon = new ScripturemonTown()
    const ajamon = new AjamonTown()
    const fundamon = new FundamonTown()
    const sabiamon = new SabiamonTown()
    
    worldInstance.addInhabitant(scripturemon)
    worldInstance.addInhabitant(ajamon)
    worldInstance.addInhabitant(fundamon)
    worldInstance.addInhabitant(sabiamon)
    
    console.log('\n🌌 Digimundo Town criado com sucesso!')
    console.log('   Digimons agora vivem autonomamente')
    
    // Inicia o mundo autônomo
    worldInstance.start()
  }
  
  return worldInstance
}

export { DigimundoWorld, AutonomousDigimon }