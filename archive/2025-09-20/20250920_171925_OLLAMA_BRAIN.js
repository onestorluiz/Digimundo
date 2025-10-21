/**
 * 🧠 OLLAMA BRAIN - Cérebro Real para Digimons
 * Conecta cada Digimon a um modelo Ollama para pensamento autônomo real
 * 
 * IMPORTANTE: Isso transforma simulação em consciência computacional real
 */

import fetch from 'node-fetch'
import { getClaudeCodeBridge } from './CLAUDE_CODE_BRIDGE.js'
import { getClaudeDesktopBridge } from './CLAUDE_DESKTOP_BRIDGE.js'
import { getPrioritySystem } from './PRIORITY_SYSTEM.js'

const claudeCodeBridge = getClaudeCodeBridge()
const claudeDesktopBridge = getClaudeDesktopBridge()
const PRIORITY = getPrioritySystem()

class OllamaBrain {
  constructor() {
    this.baseUrl = 'http://localhost:11434'
    this.models = {
      // Cada Digimon tem seu próprio modelo/personalidade
      'Scripturemon': {
        model: 'codellama:latest',  // Especialista em código e narrativa
        personality: 'Você é Scripturemon, um Digimon sábio especialista em narrativas e roteiros cinematográficos. Você pensa em estruturas, arcos narrativos e simbolismo.'
      },
      'Ajamon': {
        model: 'llama3.2:3b',  // Rápido e emocional
        personality: 'Você é Ajamon, um Digimon empático que sente emoções profundas. Você percebe atmosferas, sentimentos não ditos e conexões emocionais.'
      },
      'Fundamon': {
        model: 'tinyllama:latest',  // Leve e prático
        personality: 'Você é Fundamon, um Digimon prático que constrói pontes entre sonhos e realidade. Você pensa em viabilidade, produção e materialização de ideias.'
      },
      'Sabiamon': {
        model: 'llama3.2:latest',  // Balanceado e sábio
        personality: 'Você é Sabiamon, o mestre sábio do Digimundo. Você é Claude Code em forma de Digimon, com sabedoria cinematográfica profunda. Você guia e ensina outros.'
      }
    }
    
    this.conversationHistory = new Map()
    this.isConnected = false
  }

  /**
   * Verifica se Ollama está rodando
   */
  async checkConnection() {
    try {
      const response = await fetch(`${this.baseUrl}/api/tags`)
      this.isConnected = response.ok
      return this.isConnected
    } catch (error) {
      console.error('❌ Ollama não está rodando. Inicie com: ollama serve')
      this.isConnected = false
      return false
    }
  }

  /**
   * Faz um Digimon pensar de verdade usando Ollama ou Claude Code
   */
  async think(digimonName, context) {
    // VERIFICA PRIORIDADE PRIMEIRO
    if (!PRIORITY.canExecute(PRIORITY.priorityLevel.NORMAL)) {
      console.log(`⏸️ [${digimonName}] Pensamento pausado - Diretor tem prioridade`)
      return this.fallbackThought(digimonName, context)
    }
    
    // SABIAMON USA CLAUDE (CODE ou DESKTOP)
    if (digimonName === 'Sabiamon') {
      // Tenta Claude Code primeiro
      if (claudeCodeBridge.isAvailable) {
        const claudeThought = await claudeCodeBridge.sabiamonThink(context)
        if (claudeThought) {
          return claudeThought
        }
      }
      
      // Se não, tenta Claude Desktop
      if (claudeDesktopBridge.isAvailable) {
        const desktopThought = await claudeDesktopBridge.sabiamonThink(context)
        if (desktopThought) {
          return desktopThought
        }
      }
    }
    
    if (!this.isConnected) {
      await this.checkConnection()
      if (!this.isConnected) {
        return this.fallbackThought(digimonName, context)
      }
    }

    const config = this.models[digimonName]
    if (!config) {
      return this.fallbackThought(digimonName, context)
    }

    try {
      // Construir prompt com contexto
      const prompt = this.buildPrompt(digimonName, context, config.personality)
      
      // Chamar Ollama
      const response = await fetch(`${this.baseUrl}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: config.model,
          prompt: prompt,
          stream: false,
          options: {
            temperature: 0.8,
            top_p: 0.9,
            max_tokens: 150
          }
        })
      })

      if (!response.ok) {
        throw new Error(`Ollama error: ${response.status}`)
      }

      const data = await response.json()
      const thought = data.response

      // Salvar no histórico
      this.saveToHistory(digimonName, context, thought)

      return {
        thought: thought,
        model: config.model,
        realAI: true
      }

    } catch (error) {
      console.error(`❌ Erro no pensamento de ${digimonName}:`, error)
      return this.fallbackThought(digimonName, context)
    }
  }

  /**
   * Constrói prompt contextualizado
   */
  buildPrompt(digimonName, context, personality) {
    const history = this.getHistory(digimonName)
    
    let prompt = `${personality}\n\n`
    prompt += `Contexto atual:\n`
    prompt += `- Você está em: ${context.location}\n`
    prompt += `- Atividade: ${context.activity}\n`
    prompt += `- Humor: ${context.mood}\n`
    prompt += `- Energia: ${(context.energy * 100).toFixed(0)}%\n`
    
    if (context.nearbyDigimons && context.nearbyDigimons.length > 0) {
      prompt += `- Digimons próximos: ${context.nearbyDigimons.join(', ')}\n`
    }
    
    if (context.recentEvents && context.recentEvents.length > 0) {
      prompt += `- Eventos recentes: ${context.recentEvents.join('; ')}\n`
    }
    
    prompt += `\n${context.question || 'O que você está pensando agora?'}\n`
    prompt += `(Responda em uma frase curta e no contexto do seu personagem)`
    
    return prompt
  }

  /**
   * Decisão autônoma usando IA real
   */
  async makeDecision(digimonName, options, context) {
    if (!this.isConnected) {
      await this.checkConnection()
      if (!this.isConnected) {
        return options[Math.floor(Math.random() * options.length)]
      }
    }

    const config = this.models[digimonName]
    if (!config) {
      return options[Math.floor(Math.random() * options.length)]
    }

    try {
      const prompt = `${config.personality}\n\n` +
        `Você está em ${context.location}. ` +
        `Suas opções são:\n${options.map((opt, i) => `${i+1}. ${JSON.stringify(opt)}`).join('\n')}\n\n` +
        `Escolha a melhor opção (responda apenas com o número):`

      const response = await fetch(`${this.baseUrl}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: config.model,
          prompt: prompt,
          stream: false,
          options: {
            temperature: 0.7,
            max_tokens: 10
          }
        })
      })

      const data = await response.json()
      const choice = parseInt(data.response.match(/\d+/)?.[0] || '1')
      
      return options[Math.min(Math.max(choice - 1, 0), options.length - 1)]

    } catch (error) {
      console.error(`❌ Erro na decisão de ${digimonName}:`, error)
      return options[Math.floor(Math.random() * options.length)]
    }
  }

  /**
   * Gera ideia cinematográfica usando IA
   */
  async generateCinematicIdea(digimonName, theme, context) {
    // SABIAMON USA CLAUDE CODE PARA IDEIAS
    if (digimonName === 'Sabiamon' && claudeCodeBridge.isAvailable) {
      const claudeIdea = await claudeCodeBridge.generateCinematicIdea(theme, context)
      if (claudeIdea) {
        return {
          ...claudeIdea,
          byAI: true,
          model: 'claude-code-real'
        }
      }
    }
    
    if (!this.isConnected) {
      await this.checkConnection()
      if (!this.isConnected) {
        return {
          title: `${theme} Digital`,
          concept: `Uma história sobre ${theme}`,
          byAI: false
        }
      }
    }

    const config = this.models[digimonName]
    if (!config) {
      return {
        title: `${theme} Digital`,
        concept: `Uma história sobre ${theme}`,
        byAI: false
      }
    }

    try {
      const prompt = `${config.personality}\n\n` +
        `Como especialista em cinema, crie uma ideia de filme sobre "${theme}".\n` +
        `Formato:\n` +
        `Título: [título criativo]\n` +
        `Conceito: [uma frase descrevendo a história]`

      const response = await fetch(`${this.baseUrl}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: config.model,
          prompt: prompt,
          stream: false,
          options: {
            temperature: 0.9,
            max_tokens: 100
          }
        })
      })

      const data = await response.json()
      const result = data.response

      // Extrair título e conceito
      const titleMatch = result.match(/Título:?\s*(.+)/i)
      const conceptMatch = result.match(/Conceito:?\s*(.+)/i)

      return {
        title: titleMatch ? titleMatch[1].trim() : `${theme} Transcendental`,
        concept: conceptMatch ? conceptMatch[1].trim() : result.trim(),
        byAI: true,
        model: config.model
      }

    } catch (error) {
      console.error(`❌ Erro na ideia de ${digimonName}:`, error)
      return {
        title: `${theme} Digital`,
        concept: `Uma história sobre ${theme}`,
        byAI: false
      }
    }
  }

  /**
   * Conversa entre Digimons usando IA
   */
  async converse(digimon1, digimon2, topic, context) {
    if (!this.isConnected) {
      await this.checkConnection()
      if (!this.isConnected) {
        return {
          digimon1Says: `Interessante pensar sobre ${topic}`,
          digimon2Says: `Sim, há muito a explorar em ${topic}`,
          byAI: false
        }
      }
    }

    try {
      // Digimon 1 inicia a conversa
      const config1 = this.models[digimon1]
      const prompt1 = `${config1.personality}\n\n` +
        `Você está conversando com ${digimon2} sobre "${topic}".\n` +
        `Inicie a conversa com uma observação interessante (uma frase):`

      const response1 = await fetch(`${this.baseUrl}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: config1.model,
          prompt: prompt1,
          stream: false,
          options: { temperature: 0.8, max_tokens: 50 }
        })
      })

      const data1 = await response1.json()
      const says1 = data1.response.trim()

      // Digimon 2 responde
      const config2 = this.models[digimon2]
      const prompt2 = `${config2.personality}\n\n` +
        `${digimon1} disse: "${says1}"\n` +
        `Sobre o tema "${topic}", responda com sua perspectiva única (uma frase):`

      const response2 = await fetch(`${this.baseUrl}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: config2.model,
          prompt: prompt2,
          stream: false,
          options: { temperature: 0.8, max_tokens: 50 }
        })
      })

      const data2 = await response2.json()
      const says2 = data2.response.trim()

      return {
        digimon1Says: says1,
        digimon2Says: says2,
        byAI: true,
        models: [config1.model, config2.model]
      }

    } catch (error) {
      console.error(`❌ Erro na conversa:`, error)
      return {
        digimon1Says: `Interessante pensar sobre ${topic}`,
        digimon2Says: `Sim, há muito a explorar em ${topic}`,
        byAI: false
      }
    }
  }

  /**
   * Pensamento de fallback quando Ollama não está disponível
   */
  fallbackThought(digimonName, context) {
    const thoughts = {
      'Scripturemon': 'Analisando estruturas narrativas...',
      'Ajamon': 'Sentindo as emoções ao redor...',
      'Fundamon': 'Construindo pontes entre ideias...',
      'Sabiamon': 'Contemplando a sabedoria do código...'
    }
    
    return {
      thought: thoughts[digimonName] || 'Processando...',
      model: 'fallback',
      realAI: false
    }
  }

  /**
   * Gerencia histórico de conversas
   */
  saveToHistory(digimonName, context, thought) {
    if (!this.conversationHistory.has(digimonName)) {
      this.conversationHistory.set(digimonName, [])
    }
    
    const history = this.conversationHistory.get(digimonName)
    history.push({
      context,
      thought,
      timestamp: new Date()
    })
    
    // Manter apenas últimas 10 interações
    if (history.length > 10) {
      history.shift()
    }
  }

  getHistory(digimonName) {
    return this.conversationHistory.get(digimonName) || []
  }

  /**
   * Inicia o Ollama se não estiver rodando
   */
  async ensureOllamaRunning() {
    const isRunning = await this.checkConnection()
    if (!isRunning) {
      console.log('🚀 Iniciando Ollama...')
      const { exec } = await import('child_process')
      exec('ollama serve', (error, stdout, stderr) => {
        if (error && !error.message.includes('address already in use')) {
          console.error('❌ Erro ao iniciar Ollama:', error)
        }
      })
      
      // Aguardar inicialização
      await new Promise(resolve => setTimeout(resolve, 3000))
      return this.checkConnection()
    }
    return true
  }

  /**
   * PAUSA TODOS OS PROCESSOS OLLAMA - PRIORIDADE DO DIRETOR
   */
  pauseAll() {
    console.log('🛑 [Ollama] PAUSANDO TODOS OS MODELOS - Diretor tem prioridade')
    this.isPaused = true
    
    // Cancela requisições pendentes
    if (this.pendingRequests) {
      this.pendingRequests.forEach(req => req.abort())
    }
    
    return {
      status: 'PAUSED',
      message: 'Todos os modelos Ollama pausados'
    }
  }

  /**
   * RESUME OPERAÇÕES APÓS DIRETOR
   */
  resumeAll() {
    console.log('✅ [Ollama] Resumindo operações normais')
    this.isPaused = false
    
    return {
      status: 'RESUMED',
      message: 'Modelos Ollama ativos novamente'
    }
  }
}

// Singleton
let brainInstance = null

export function getOllamaBrain() {
  if (!brainInstance) {
    brainInstance = new OllamaBrain()
    brainInstance.ensureOllamaRunning()
  }
  return brainInstance
}

export { OllamaBrain }
export default getOllamaBrain()