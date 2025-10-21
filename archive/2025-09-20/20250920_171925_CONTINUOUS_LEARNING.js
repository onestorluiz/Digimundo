/**
 * 🎓 CONTINUOUS LEARNING - Aprendizado Contínuo dos Digimons
 * 
 * Sistema que faz os Digimons aprenderem automaticamente
 * Integra com Ollama Brain para aplicar conhecimento em tempo real
 */

import { getDigibibliotecaReader } from './DIGIBIBLIOTECA_READER.js'
import { getBibliotecaIntegration } from './BIBLIOTECA_INTEGRATION.js'
import { getOllamaBrain } from '../consciousness/OLLAMA_BRAIN.js'
import fs from 'fs/promises'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

class ContinuousLearning {
  constructor() {
    this.reader = getDigibibliotecaReader()
    this.integration = getBibliotecaIntegration()
    this.brain = getOllamaBrain()
    
    this.learningInterval = 30 * 60 * 1000 // 30 minutos
    this.isLearning = false
    this.learningStats = {
      totalCycles: 0,
      knowledgeApplied: 0,
      improvementsDetected: 0,
      lastLearning: null
    }
    
    this.digimonLearningProfiles = {
      'Scripturemon': {
        focus: 'narrative_structure',
        learningSpeed: 'high',
        application: 'screenplay_creation',
        curiosity: ['character_development', 'dialogue_techniques', 'story_arcs']
      },
      'Ajamon': {
        focus: 'emotional_intelligence',
        learningSpeed: 'medium',
        application: 'character_emotions',
        curiosity: ['relationships', 'emotional_arcs', 'empathy_building']
      },
      'Fundamon': {
        focus: 'technical_foundations',
        learningSpeed: 'steady',
        application: 'production_methods',
        curiosity: ['film_techniques', 'production_workflows', 'industry_standards']
      },
      'Sabiamon': {
        focus: 'holistic_wisdom',
        learningSpeed: 'deep',
        application: 'guidance_synthesis',
        curiosity: ['film_theory', 'artistic_vision', 'creative_philosophy']
      }
    }
  }

  /**
   * INICIAR APRENDIZADO CONTÍNUO
   */
  async startContinuousLearning() {
    console.log('🎓 [Continuous Learning] Iniciando aprendizado contínuo dos Digimons')
    console.log('   📚 Biblioteca ativa para leitura automática')
    console.log('   🧠 IA conectada para aplicação de conhecimento')
    console.log(`   ⏰ Ciclos a cada ${this.learningInterval / 1000 / 60} minutos`)
    
    // Inicializar integração
    await this.integration.initialize()
    
    // Iniciar reader da biblioteca
    await this.reader.startContinuousLearning()
    
    // Ciclo inicial de aprendizado
    await this.performLearningCycle()
    
    // Loop contínuo
    setInterval(async () => {
      if (!this.isLearning) {
        await this.performLearningCycle()
      }
    }, this.learningInterval)
    
    console.log('✅ [Continuous Learning] Sistema de aprendizado ativo!')
  }

  /**
   * EXECUTAR CICLO DE APRENDIZADO
   */
  async performLearningCycle() {
    this.isLearning = true
    const cycleStart = Date.now()
    
    console.log(`\\n🎓 [${new Date().toLocaleTimeString()}] Iniciando ciclo de aprendizado...`)
    
    try {
      this.learningStats.totalCycles++
      
      // 1. Verificar novos conhecimentos na biblioteca
      const newKnowledge = await this.checkForNewKnowledge()
      
      // 2. Para cada Digimon, aplicar aprendizado personalizado
      for (const digimonName of Object.keys(this.digimonLearningProfiles)) {
        await this.personalizedLearning(digimonName, newKnowledge)
      }
      
      // 3. Aplicar conhecimento em contextos ativos
      await this.applyKnowledgeInContext()
      
      // 4. Detectar melhorias no comportamento
      await this.detectBehaviorImprovements()
      
      const cycleDuration = Date.now() - cycleStart
      this.learningStats.lastLearning = new Date()
      
      console.log(`\\n📊 [Ciclo Completo] ${cycleDuration}ms`)
      console.log(`   📚 Novos conhecimentos: ${newKnowledge.length}`)
      console.log(`   🧠 Aplicações realizadas: ${this.learningStats.knowledgeApplied}`)
      
      // Salvar progresso
      await this.saveLearningProgress()
      
    } catch (error) {
      console.error('❌ Erro no ciclo de aprendizado:', error)
    } finally {
      this.isLearning = false
    }
  }

  /**
   * VERIFICAR NOVOS CONHECIMENTOS
   */
  async checkForNewKnowledge() {
    try {
      // Forçar sincronização com biblioteca
      await this.integration.forceSyncNow()
      
      // Buscar conhecimentos recentes (últimas 2 horas)
      const recentThreshold = Date.now() - (2 * 60 * 60 * 1000)
      const allKnowledge = Array.from(this.integration.knowledgeCache.values())
      
      const newKnowledge = allKnowledge.filter(k => 
        new Date(k.extractedAt).getTime() > recentThreshold
      )
      
      if (newKnowledge.length > 0) {
        console.log(`   📖 ${newKnowledge.length} novos conhecimentos detectados`)
        
        for (const knowledge of newKnowledge) {
          console.log(`      • ${knowledge.source} (${knowledge.category})`)
        }
      }
      
      return newKnowledge
      
    } catch (error) {
      console.error('   ❌ Erro ao verificar novos conhecimentos:', error)
      return []
    }
  }

  /**
   * APRENDIZADO PERSONALIZADO PARA DIGIMON
   */
  async personalizedLearning(digimonName, newKnowledge) {
    const profile = this.digimonLearningProfiles[digimonName]
    
    console.log(`   🎯 [${digimonName}] Aprendizado personalizado...`)
    
    try {
      // Buscar conhecimento relevante para este Digimon
      const relevantKnowledge = await this.findRelevantKnowledge(digimonName, newKnowledge)
      
      if (relevantKnowledge.length === 0) {
        console.log(`      ℹ️ Nenhum conhecimento novo relevante`)
        return
      }
      
      // Aplicar conhecimento usando IA
      for (const knowledge of relevantKnowledge.slice(0, 3)) {
        await this.applyKnowledgeToDigimon(digimonName, knowledge, profile)
      }
      
      // Explorar curiosidades
      await this.exploreCuriosities(digimonName, profile.curiosity)
      
      console.log(`      ✅ ${relevantKnowledge.length} conhecimentos processados`)
      
    } catch (error) {
      console.error(`   ❌ Erro no aprendizado de ${digimonName}:`, error)
    }
  }

  /**
   * ENCONTRAR CONHECIMENTO RELEVANTE
   */
  async findRelevantKnowledge(digimonName, newKnowledge) {
    const profile = this.digimonLearningProfiles[digimonName]
    const relevant = []
    
    for (const knowledge of newKnowledge) {
      let relevanceScore = 0
      
      // Score por categoria
      if (this.isRelevantCategory(knowledge.category, profile.focus)) {
        relevanceScore += 0.4
      }
      
      // Score por conceitos
      const matchingConcepts = knowledge.cinematicConcepts?.filter(concept =>
        profile.curiosity.some(curiosity => 
          concept.toLowerCase().includes(curiosity.replace('_', ' '))
        )
      ) || []
      
      relevanceScore += matchingConcepts.length * 0.3
      
      // Score por insights
      const matchingInsights = knowledge.insights?.filter(insight =>
        profile.curiosity.some(curiosity =>
          insight.toLowerCase().includes(curiosity.replace('_', ' '))
        )
      ) || []
      
      relevanceScore += matchingInsights.length * 0.2
      
      if (relevanceScore > 0.3) {
        relevant.push({
          knowledge,
          relevanceScore,
          matchingConcepts,
          matchingInsights
        })
      }
    }
    
    return relevant.sort((a, b) => b.relevanceScore - a.relevanceScore)
  }

  /**
   * VERIFICAR SE CATEGORIA É RELEVANTE
   */
  isRelevantCategory(category, focus) {
    const categoryMapping = {
      'narrative_structure': ['roteiros', 'livros'],
      'emotional_intelligence': ['livros', 'artigos'],
      'technical_foundations': ['estudos', 'referencias'],
      'holistic_wisdom': ['livros', 'artigos', 'estudos']
    }
    
    return categoryMapping[focus]?.includes(category) || false
  }

  /**
   * APLICAR CONHECIMENTO AO DIGIMON
   */
  async applyKnowledgeToDigimon(digimonName, relevantItem, profile) {
    try {
      const { knowledge, matchingConcepts, matchingInsights } = relevantItem
      
      // Criar contexto de aprendizado
      const learningContext = {
        location: 'Digibiblioteca',
        activity: 'studying',
        mood: 'curious',
        energy: 0.9,
        focus: profile.focus,
        newKnowledge: {
          source: knowledge.source,
          concepts: matchingConcepts,
          insights: matchingInsights
        }
      }
      
      // Gerar pensamento usando IA sobre o novo conhecimento
      const thought = await this.brain.think(digimonName, {
        ...learningContext,
        question: `Como posso aplicar este conhecimento de "${knowledge.source}" sobre ${matchingConcepts.join(', ')} no meu trabalho cinematográfico?`
      })
      
      if (thought && thought.thought) {
        console.log(`      💡 [${digimonName}] ${thought.thought.substring(0, 100)}...`)
        
        // Registrar aprendizado
        await this.recordLearning(digimonName, knowledge, thought.thought)
        
        this.learningStats.knowledgeApplied++
      }
      
    } catch (error) {
      console.error(`      ❌ Erro ao aplicar conhecimento em ${digimonName}:`, error)
    }
  }

  /**
   * EXPLORAR CURIOSIDADES
   */
  async exploreCuriosities(digimonName, curiosities) {
    try {
      // Escolher uma curiosidade aleatória
      const curiosity = curiosities[Math.floor(Math.random() * curiosities.length)]
      
      // Buscar conhecimento sobre essa curiosidade
      const knowledge = this.integration.searchRelevantKnowledge(curiosity, {
        digimonName: digimonName,
        maxResults: 2
      })
      
      if (knowledge.direct.length > 0) {
        const context = {
          location: 'Digibiblioteca',
          activity: 'exploring',
          mood: 'curious',
          energy: 0.8,
          curiosityTopic: curiosity
        }
        
        const exploration = await this.brain.think(digimonName, {
          ...context,
          question: `O que posso aprender sobre ${curiosity.replace('_', ' ')} que me ajude a ser um melhor Digimon cinematográfico?`
        })
        
        if (exploration?.thought) {
          console.log(`      🔍 [${digimonName}] Explorando ${curiosity}: ${exploration.thought.substring(0, 80)}...`)
        }
      }
      
    } catch (error) {
      console.error(`      ❌ Erro ao explorar curiosidades:`, error)
    }
  }

  /**
   * APLICAR CONHECIMENTO EM CONTEXTO ATIVO
   */
  async applyKnowledgeInContext() {
    try {
      // Simular aplicação em um projeto de filme atual
      const activeProject = {
        genre: 'drama',
        stage: 'development',
        challenges: ['character_development', 'dialogue_improvement']
      }
      
      for (const challenge of activeProject.challenges) {
        const relevantKnowledge = this.integration.searchRelevantKnowledge(challenge, {
          maxResults: 2
        })
        
        if (relevantKnowledge.direct.length > 0) {
          console.log(`   🎬 Aplicando conhecimento em: ${challenge}`)
          
          // Cada Digimon contribui com sua perspectiva
          for (const digimonName of Object.keys(this.digimonLearningProfiles)) {
            const contribution = await this.getDigimonContribution(
              digimonName, challenge, relevantKnowledge.direct[0]
            )
            
            if (contribution) {
              console.log(`      • ${digimonName}: ${contribution.substring(0, 60)}...`)
            }
          }
        }
      }
      
    } catch (error) {
      console.error('   ❌ Erro ao aplicar conhecimento em contexto:', error)
    }
  }

  /**
   * OBTER CONTRIBUIÇÃO DO DIGIMON
   */
  async getDigimonContribution(digimonName, challenge, knowledge) {
    try {
      const context = {
        location: 'Estúdio',
        activity: 'collaborating',
        mood: 'focused',
        energy: 0.9,
        challenge: challenge,
        availableKnowledge: knowledge.source
      }
      
      const contribution = await this.brain.think(digimonName, {
        ...context,
        question: `Como meu conhecimento sobre ${knowledge.source} pode ajudar a resolver o desafio de ${challenge} neste projeto?`
      })
      
      return contribution?.thought || null
      
    } catch (error) {
      console.error(`Erro na contribuição de ${digimonName}:`, error)
      return null
    }
  }

  /**
   * DETECTAR MELHORIAS NO COMPORTAMENTO
   */
  async detectBehaviorImprovements() {
    try {
      // Análise simples de melhoria baseada em estatísticas
      const stats = this.integration.getIntegrationStats()
      
      if (stats.knowledgeInCache > this.lastKnowledgeCount) {
        this.learningStats.improvementsDetected++
        console.log(`   📈 Melhoria detectada: +${stats.knowledgeInCache - this.lastKnowledgeCount} conhecimentos integrados`)
      }
      
      this.lastKnowledgeCount = stats.knowledgeInCache
      
    } catch (error) {
      console.error('   ❌ Erro ao detectar melhorias:', error)
    }
  }

  /**
   * REGISTRAR APRENDIZADO
   */
  async recordLearning(digimonName, knowledge, thought) {
    try {
      const learningRecord = {
        digimon: digimonName,
        timestamp: new Date(),
        source: knowledge.source,
        category: knowledge.category,
        appliedThought: thought,
        concepts: knowledge.cinematicConcepts?.slice(0, 3) || [],
        insights: knowledge.insights?.slice(0, 2) || []
      }
      
      // Salvar em arquivo de progresso de aprendizado
      const progressPath = path.join(__dirname, '../../biblioteca_logs/learning_progress.json')
      
      let progress = []
      try {
        const data = await fs.readFile(progressPath, 'utf8')
        progress = JSON.parse(data)
      } catch {
        // Arquivo não existe
      }
      
      progress.push(learningRecord)
      
      // Manter apenas últimos 1000 registros
      if (progress.length > 1000) {
        progress = progress.slice(-1000)
      }
      
      await fs.writeFile(progressPath, JSON.stringify(progress, null, 2))
      
    } catch (error) {
      console.error('❌ Erro ao registrar aprendizado:', error)
    }
  }

  /**
   * SALVAR PROGRESSO DE APRENDIZADO
   */
  async saveLearningProgress() {
    try {
      const progressPath = path.join(__dirname, '../../biblioteca_logs/learning_stats.json')
      
      const statsData = {
        ...this.learningStats,
        integrationStats: this.integration.getIntegrationStats(),
        timestamp: new Date()
      }
      
      await fs.writeFile(progressPath, JSON.stringify(statsData, null, 2))
      
    } catch (error) {
      console.error('❌ Erro ao salvar progresso:', error)
    }
  }

  /**
   * OBTER ESTATÍSTICAS DE APRENDIZADO
   */
  getStats() {
    return {
      ...this.learningStats,
      isLearning: this.isLearning,
      learningInterval: this.learningInterval,
      digimonProfiles: Object.keys(this.digimonLearningProfiles),
      lastKnowledgeCount: this.lastKnowledgeCount || 0
    }
  }

  /**
   * FORÇAR CICLO DE APRENDIZADO
   */
  async forceLearningCycle() {
    if (this.isLearning) {
      return { success: false, message: 'Ciclo de aprendizado já em andamento' }
    }
    
    await this.performLearningCycle()
    return { success: true, message: 'Ciclo de aprendizado executado' }
  }
}

// Singleton
let learningInstance = null

export function getContinuousLearning() {
  if (!learningInstance) {
    learningInstance = new ContinuousLearning()
  }
  return learningInstance
}

export { ContinuousLearning }
export default getContinuousLearning()