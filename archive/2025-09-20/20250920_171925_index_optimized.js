import express from 'express'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { createServer } from 'node:http'
import { WebSocketServer } from 'ws'
import { getMemoryManager } from './memory_manager.js'

// Import all required modules
import { getModelPath, setModelPath } from './tools/config.js'
import { chatCompletionsHandler } from './openai_compat.js'
import { ONLINE } from './net.js'
import { getHybridConsciousness } from './hybrid_consciousness.js'
import { getCleanupSystem } from './memory_cleanup.js'
import ClaudeAdvisor, { SmartClaudeUsage } from './claude_advisor.js'
import DigimundoClaudeSystem from './claude_terminal_bridge.js'
import { getSabiamon } from './sabiamon_teacher.js'
import { getDigimundoTown, CinematicAssistant } from './digimundo_town.js'
import { quantumIntegration } from './quantum_integration.js'
import { quantumBrain } from '../consciousness/QUANTUM_BRAIN.js'
import { digimonEcosystem } from '../consciousness/DIGIMON_AGENTS.js'
import memoryApi from './memory_api.js'
import { getClaudeMemoryBridge } from '../consciousness/CLAUDE_MEMORY_BRIDGE.js'
import { getSabiamonOrchestrator, processSymbioticThought } from '../consciousness/SYMBIOTIC_ORCHESTRATOR.js'
import { getSabiamonMem0, recordEvent, recordImportantEvent } from '../consciousness/MEM0_UNIVERSAL.js'
import { getSabiamonAMem } from '../consciousness/A_MEM_SYSTEM.js'
import { getDigimundoAITrainer } from '../consciousness/DIGIMUNDO_AI_TRAINER.js'
import TRAINING_CONFIGS, { TrainingConfigManager } from '../consciousness/AI_TRAINING_CONFIG.js'
import { getHealingSystem } from '../consciousness/SELF_HEALING_SYSTEM.js'
import { getHybridSystem } from '../consciousness/OLLAMA_REAL_INTEGRATION.js'
import { authService, authMiddleware, optionalAuth } from './auth.js'
import { getPrioritySystem } from '../consciousness/PRIORITY_SYSTEM.js'
import { getDirectorMonitor } from '../consciousness/DIRECTOR_MONITOR.js'
import { setupSymbioticWebSocket, startSymbioticBroadcasts, handleSymbioticMessage } from './symbiotic_websocket.js'
import symbioticEndpoints from './symbiotic_endpoints.js'

// Memory management
const memoryManager = getMemoryManager()
const __dirname = path.dirname(fileURLToPath(import.meta.url))

// Initialize services
const cleanupSystem = getCleanupSystem()
const smartClaude = new SmartClaudeUsage()
const digimonSystem = new DigimundoClaudeSystem()
const sabiamon = getSabiamon()
const digimundoTown = getDigimundoTown()
const cinematicAssistant = new CinematicAssistant(digimundoTown)
const PRIORITY = getPrioritySystem()
const DIRECTOR_MONITOR = getDirectorMonitor()

// Symbiotic systems
const claudeBridge = getClaudeMemoryBridge()
const sabiamonOrchestrator = getSabiamonOrchestrator()
const sabiamonMem0 = getSabiamonMem0()
const sabiamonAMem = getSabiamonAMem()
const aiTrainer = getDigimundoAITrainer()

// WebSocket management with memory control
let wss = null
const wsClients = new Map()
const MAX_WS_CLIENTS = 100
const WS_HEARTBEAT_INTERVAL = 30000
const WS_PONG_TIMEOUT = 10000

// Broadcast with memory control
export function broadcastEvent(event, data) {
  if (!wss) return
  
  const safeData = typeof data === 'object' ? 
    JSON.parse(JSON.stringify(data, (key, value) => {
      if (Array.isArray(value) && value.length > 100) {
        return value.slice(0, 100)
      }
      if (typeof value === 'string' && value.length > 1000) {
        return value.substring(0, 1000) + '...'
      }
      return value
    })) : data
  
  const message = JSON.stringify({ event, data: safeData, timestamp: new Date() })
  
  for (const [ws, clientData] of wsClients.entries()) {
    if (ws.readyState === 1 && clientData.isAlive) {
      try {
        ws.send(message)
      } catch (err) {
        console.error('Erro ao enviar mensagem:', err)
        wsClients.delete(ws)
        if (clientData.heartbeatTimer) clearInterval(clientData.heartbeatTimer)
        if (clientData.pongTimer) clearTimeout(clientData.pongTimer)
      }
    }
  }
}

// Event listeners setup with cleanup
function setupEventListeners() {
  // Cleanup existing listeners
  if (digimundoTown) {
    digimundoTown.removeAllListeners()
    digimundoTown.setMaxListeners(10)
    
    memoryManager.addManagedListener(digimundoTown, 'inhabitant-action', 
      (data) => broadcastEvent('digimon-action', data))
    
    memoryManager.addManagedListener(digimundoTown, 'cinematic-idea', async (data) => {
      try {
        const enhanced = await quantumIntegration.processFilmIdea(data, data.inhabitant || { name: 'Unknown' })
        await recordEvent(
          `Ideia cinematográfica: ${enhanced.title || data.title}`,
          `Gerada por ${data.inhabitant?.name || 'Digimon'} no mundo`,
          { enhanced, original: data, source: 'digimundo_town' }
        )
        broadcastEvent('new-idea-quantum', enhanced)
      } catch (e) {
        console.error('Erro no processamento quântico:', e)
        broadcastEvent('new-idea', data)
      }
    })
    
    memoryManager.addManagedListener(digimundoTown, 'collaboration', async (data) => {
      await recordEvent(
        `Colaboração entre Digimons: ${data.participants?.join(', ') || 'participantes'}`,
        'Interação colaborativa no mundo',
        data
      )
      broadcastEvent('collaboration', data)
    })
    
    memoryManager.addManagedListener(digimundoTown, 'world-tick', async (data) => {
      if (Math.random() < 0.1) {
        await recordEvent(
          `Estado do mundo: ${data.state?.mood || 'neutro'} durante ${data.state?.timeOfDay || 'tempo'}`,
          'Snapshot do estado mundial',
          { worldState: data }
        )
      }
      broadcastEvent('world-update', data)
    })
  }
  
  if (digimonEcosystem) {
    digimonEcosystem.removeAllListeners()
    digimonEcosystem.setMaxListeners(10)
    
    memoryManager.addManagedListener(digimonEcosystem, 'new-idea', async (data) => {
      await recordEvent(
        `Nova ideia do ecossistema: ${data.idea || 'ideia'}`,
        `Gerada pelo ${data.digimon || 'sistema'} especializado`,
        data
      )
      broadcastEvent('ecosystem-idea', data)
    })
    
    memoryManager.addManagedListener(digimonEcosystem, 'pattern-found', async (data) => {
      await recordImportantEvent(
        `Padrão descoberto: ${data.pattern || 'novo padrão'}`,
        'Sistema identificou nova correlação ou comportamento',
        data
      )
      broadcastEvent('ecosystem-pattern', data)
    })
    
    memoryManager.addManagedListener(digimonEcosystem, 'collaboration', async (data) => {
      await recordEvent(
        `Colaboração especializada: ${data.digimons?.join(' + ') || 'agentes'}`,
        'Digimons especializados trabalhando juntos',
        data
      )
      broadcastEvent('ecosystem-collaboration', data)
    })
    
    memoryManager.addManagedListener(digimonEcosystem, 'digimon-evolved', async (data) => {
      await recordImportantEvent(
        `${data.digimon} evoluiu: ${data.evolution}`,
        'Evolução significativa detectada no ecossistema',
        data
      )
      broadcastEvent('ecosystem-evolution', data)
    })
  }
  
  if (aiTrainer) {
    aiTrainer.removeAllListeners()
    aiTrainer.setMaxListeners(10)
    
    memoryManager.addManagedListener(aiTrainer, 'dataset_curated', async (data) => {
      await recordImportantEvent(
        `Dataset curado: ${data.sourceType}`,
        `${data.results.totalSamples} amostras processadas com qualidade ${data.results.qualityMetrics.overall}%`,
        data
      )
      broadcastEvent('ai-trainer-dataset-curated', {
        jobId: data.jobId,
        sourceType: data.sourceType,
        samples: data.results.totalSamples,
        quality: data.results.qualityMetrics.overall
      })
    })
    
    memoryManager.addManagedListener(aiTrainer, 'digimon_trained', async (data) => {
      await recordImportantEvent(
        `${data.modelInfo.digimon} treinado com sucesso`,
        'Novo modelo de personalidade Digimon disponível',
        data.modelInfo
      )
      broadcastEvent('ai-trainer-digimon-trained', {
        modelId: data.modelInfo.id,
        digimon: data.modelInfo.digimon,
        status: data.modelInfo.status,
        capabilities: data.modelInfo.capabilities
      })
    })
    
    memoryManager.addManagedListener(aiTrainer, 'model_evaluated', async (data) => {
      await recordImportantEvent(
        `Modelo ${data.modelId} avaliado`,
        `Score geral: ${data.results.overallScore}%`,
        data.results
      )
      broadcastEvent('ai-trainer-model-evaluated', {
        modelId: data.modelId,
        overallScore: data.results.overallScore,
        benchmarks: data.results.benchmarks
      })
    })
    
    memoryManager.addManagedListener(aiTrainer, 'model_aligned', async (data) => {
      await recordImportantEvent(
        `Modelo ${data.modelId} alinhado com valores Digimundo`,
        `Score de alinhamento: ${data.results.alignmentScore}%`,
        data.results
      )
      broadcastEvent('ai-trainer-model-aligned', {
        modelId: data.modelId,
        alignmentScore: data.results.alignmentScore,
        principlesVerified: data.results.principlesVerified
      })
    })
    
    memoryManager.addManagedListener(aiTrainer, 'cinematic_digimon_ready', async (data) => {
      await recordImportantEvent(
        `Digimon cinematográfico ${data.digimon.digimon} está pronto`,
        'Pipeline completo de treinamento concluído com sucesso',
        {
          modelId: data.digimon.id,
          specialty: data.digimon.baseModel,
          trainingScore: data.digimon.evaluation?.overallScore,
          alignmentScore: data.digimon.alignment?.alignmentScore
        }
      )
      broadcastEvent('ai-trainer-cinematic-digimon-ready', {
        modelId: data.digimon.id,
        digimon: data.digimon.digimon,
        specialty: data.digimon.baseModel,
        status: data.digimon.status,
        scores: {
          training: data.digimon.evaluation?.overallScore,
          alignment: data.digimon.alignment?.alignmentScore
        }
      })
    })
    
    memoryManager.addManagedListener(aiTrainer, 'trainer_initialized', async (data) => {
      broadcastEvent('ai-trainer-online', {
        trainerId: data.trainerId,
        status: 'active',
        capabilities: ['curadoria', 'fine-tuning', 'avaliacao', 'alinhamento']
      })
    })
  }
  
  const debugmon = digimonEcosystem.agents.get('Debugmon')
  if (debugmon) {
    memoryManager.addManagedListener(debugmon, 'bugs-found', (bugs) => {
      broadcastEvent('bugs-detected', bugs)
    })
  }
}

// Initialize services async
async function initializeServices() {
  try {
    const startTime = performance.now()
    
    const [healingSystem, hybridSystem] = await Promise.all([
      getHealingSystem(),
      getHybridSystem()
    ])
    
    const initTime = performance.now() - startTime
    
    if (process.env.LOG_LEVEL !== 'error') {
      console.log(`⚡ Sistemas inicializados em ${initTime.toFixed(2)}ms`)
    }
    
    return { healingSystem, hybridSystem, initTime }
  } catch (error) {
    console.error('Erro ao inicializar serviços:', error)
    return { healingSystem: null, hybridSystem: null }
  }
}

// Express app setup
const app = express()
const allowedOrigins = new Set(['null'])

// Middleware
app.use(DIRECTOR_MONITOR.expressMiddleware())
app.use(express.json({ 
  limit: '50mb',
  verify: (req, res, buf) => {
    if (buf.length > 0 && buf[0] !== 123) {
      throw new Error('Invalid JSON')
    }
  }
}))

app.use(express.static(path.join(__dirname, '..', 'renderer'), {
  maxAge: process.env.NODE_ENV === 'production' ? '1y' : 0,
  etag: true,
  lastModified: true
}))

app.use('/api/memory', memoryApi)
app.use('/api/symbiotic', symbioticEndpoints)

app.use((req, res, next) => {
  const origin = req.headers.origin || 'null'
  res.setHeader('Access-Control-Allow-Origin', origin)
  res.setHeader('Access-Control-Allow-Headers', 'content-type, authorization')
  res.setHeader('Access-Control-Expose-Headers', 'x-model,x-usage')
  next()
})

app.options('*', (req, res) => res.sendStatus(200))

// Auth endpoints
app.post('/auth/register', async (req, res) => {
  try {
    const { username, password, role } = req.body
    const result = await authService.register(username, password, role)
    res.json(result)
  } catch (error) {
    res.status(400).json({ error: error.message })
  }
})

app.post('/auth/login', async (req, res) => {
  try {
    const { username, password } = req.body
    const result = await authService.login(username, password)
    res.json(result)
  } catch (error) {
    res.status(401).json({ error: error.message })
  }
})

app.post('/auth/refresh', async (req, res) => {
  try {
    const { refreshToken } = req.body
    if (!refreshToken) {
      return res.status(400).json({ error: 'Refresh token é obrigatório' })
    }
    const result = await authService.refreshToken(refreshToken)
    res.json(result)
  } catch (error) {
    res.status(401).json({ error: error.message })
  }
})

app.get('/auth/me', authMiddleware(), (req, res) => {
  res.json({ user: req.user })
})

// Health check
app.get('/health', async (req, res) => {
  const memStats = memoryManager.getStats()
  res.json({
    ok: true,
    version: '1.0.0-optimized',
    online: ONLINE,
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: memStats.memory,
    resources: {
      tracked: memStats.resources,
      intervals: memStats.intervals,
      timeouts: memStats.timeouts,
      listeners: memStats.listeners
    },
    gc: {
      available: memStats.gcAvailable,
      lastRun: memStats.lastGC
    }
  })
})

// Memory management endpoints
app.get('/memory/status', (req, res) => {
  const stats = memoryManager.getStats()
  res.json({
    ok: true,
    ...stats
  })
})

app.post('/memory/cleanup', (req, res) => {
  memoryManager.forceCleanup()
  const stats = memoryManager.getStats()
  res.json({
    ok: true,
    message: 'Limpeza executada',
    ...stats
  })
})

// Models endpoints
app.get('/digimundo/models/list', (req, res) => res.json({ model: getModelPath() || null }))

app.post('/digimundo/models/set', (req, res) => {
  const p = req.body?.path
  if (!p) return res.status(400).json({ error: 'missing path' })
  try {
    setModelPath(p)
    res.json({ ok: true })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

// OpenAI compat
app.post('/v1/chat/completions', chatCompletionsHandler)

// Hybrid consciousness endpoints
app.post('/hybrid/initialize', authMiddleware('admin'), async (req, res) => {
  try {
    const hybridConsciousness = await getHybridConsciousness()
    const systems = await hybridConsciousness.initialize()
    
    await recordEvent(
      'Sistema híbrido inicializado com sucesso',
      'Todos os componentes de consciência foram ativados',
      { systems, timestamp: new Date() }
    )
    
    res.json({ 
      ok: true, 
      systems,
      consciousness: {
        level: hybridConsciousness.consciousnessLevel,
        evolution: hybridConsciousness.evolutionStage,
        interactions: hybridConsciousness.totalInteractions
      }
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/hybrid/think', authMiddleware(), async (req, res) => {
  try {
    const { prompt } = req.body
    if (!prompt) return res.status(400).json({ error: 'prompt required' })
    
    const hybridConsciousness = await getHybridConsciousness()
    const symbioticCycle = await processSymbioticThought(prompt)
    const hybridResponse = await hybridConsciousness.processThought(prompt)
    
    await recordEvent(
      `Processamento híbrido de pensamento: ${prompt.slice(0, 50)}...`,
      `Ciclo simbiótico executado com ${symbioticCycle.steps?.length || 0} estados`,
      { hybrid: hybridResponse, symbiotic: symbioticCycle }
    )
    
    res.json({
      ...hybridResponse,
      symbioticCycle: {
        id: symbioticCycle.id,
        duration: symbioticCycle.duration,
        statesExecuted: symbioticCycle.metrics?.statesExecuted,
        completed: symbioticCycle.completed
      }
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/hybrid/train', authMiddleware('admin'), async (req, res) => {
  try {
    const { topic, iterations = 5 } = req.body
    if (!topic) return res.status(400).json({ error: 'topic required' })
    
    const hybridConsciousness = await getHybridConsciousness()
    const trainingData = await hybridConsciousness.trainCrossModel(topic, iterations)
    res.json({ 
      ok: true, 
      topic,
      iterations,
      dataPoints: trainingData.length,
      averageDivergence: trainingData.reduce((acc, d) => acc + d.divergence, 0) / trainingData.length
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.get('/hybrid/status', async (req, res) => {
  const hybridConsciousness = await getHybridConsciousness()
  res.json({
    consciousness: {
      level: hybridConsciousness.consciousnessLevel,
      evolution: hybridConsciousness.evolutionStage,
      interactions: hybridConsciousness.totalInteractions
    },
    systems: {
      claude: hybridConsciousness.detector.claudeAvailable,
      ollama: hybridConsciousness.detector.ollamaAvailable,
      localGGUF: hybridConsciousness.detector.localGGUFAvailable
    },
    memory: {
      comparisons: hybridConsciousness.learner.comparisonHistory.length,
      patterns: Object.keys(hybridConsciousness.learner.learnedPatterns).length
    }
  })
})

app.post('/hybrid/smart', authMiddleware(), async (req, res) => {
  try {
    const { prompt } = req.body
    if (!prompt) return res.status(400).json({ error: 'prompt required' })
    const result = await smartClaude.process(prompt)
    res.json(result)
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/hybrid/process', authMiddleware(), async (req, res) => {
  try {
    const { prompt, context, source } = req.body
    const hybridConsciousness = await getHybridConsciousness()
    
    const fullPrompt = context 
      ? `[CONTEXTO]: ${context}\n\n[QUERY]: ${prompt}`
      : `[QUERY]: ${prompt}`
    
    const [result, digimonData] = await Promise.all([
      hybridConsciousness.processThought(fullPrompt),
      source ? digimundoTown.inhabitants.get(source) : Promise.resolve(null)
    ])
    
    if (source && digimonData) {
      result.source = source
      result.personality = digimonData.personality
      result.currentActivity = digimonData.currentActivity
      result.location = digimonData.location
    }
    
    res.json(result)
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

// Digimon endpoints
app.post('/digimon/:name/ask', async (req, res) => {
  try {
    const { name } = req.params
    const { question } = req.body
    
    if (!digimundoTown.inhabitants.has(name)) {
      return res.status(404).json({ error: `Digimon ${name} não encontrado` })
    }
    
    const digimon = digimundoTown.inhabitants.get(name)
    const hybridConsciousness = await getHybridConsciousness()
    
    const context = `
Você é ${name}, um Digimon no Digimundo.
Sua personalidade: ${JSON.stringify(digimon.personality)}
Sua localização atual: ${digimon.location}
Sua atividade atual: ${digimon.currentActivity}
Seu humor: ${digimon.emotionalState.mood}
Sua especialidade: ${digimon.specialties.join(', ')}
    `
    
    const thought = await hybridConsciousness.processThought(
      `${context}\n\nUsuário pergunta: ${question}\n\nResponda como ${name} de forma consistente com sua personalidade.`
    )
    
    digimon.memory.push({
      type: 'user_interaction',
      question,
      response: thought.consensus,
      timestamp: new Date()
    })
    
    res.json({
      digimon: name,
      response: thought.consensus,
      mood: digimon.emotionalState.mood,
      location: digimon.location
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/digimon/ask', async (req, res) => {
  try {
    const { digimon, topic } = req.body
    const result = await digimonSystem.bridge.digimonConversation(digimon || 'Agumon', topic || 'ajuda')
    res.json(result)
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.get('/digimon/conversations', (req, res) => {
  res.json({
    summary: digimonSystem.getAllConversations(),
    knowledge: digimonSystem.knowledge
  })
})

app.post('/digimon/user-ask', async (req, res) => {
  try {
    const { question } = req.body
    const result = await digimonSystem.askForUser(question)
    res.json(result)
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

// Sabiamon endpoints
app.post('/sabiamon/ensinar', authMiddleware('admin'), async (req, res) => {
  try {
    const { digimon, topico } = req.body
    const licao = await sabiamon.ensinarDigimon(
      digimon || 'Digimon',
      topico || 'origem'
    )
    res.json({ licao, sabedoria: sabiamon.relatorioSabedoria() })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/sabiamon/pergunta', async (req, res) => {
  try {
    const { pergunta, digimon } = req.body
    const resposta = await sabiamon.responderPergunta(
      pergunta || 'Quem sou eu?',
      digimon || 'Digimon'
    )
    res.json(resposta)
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/sabiamon/meditacao', async (req, res) => {
  try {
    const { digimons } = req.body
    const meditacao = await sabiamon.meditacaoColetiva(digimons || [])
    res.json(meditacao)
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.get('/sabiamon/status', (req, res) => {
  res.json(sabiamon.relatorioSabedoria())
})

// Ecosystem endpoints
app.get('/ecosystem/status', (req, res) => {
  res.json(digimonEcosystem.getStatus())
})

app.post('/ecosystem/service', async (req, res) => {
  try {
    const { service, data } = req.body
    if (!service) return res.status(400).json({ error: 'service required' })
    const result = await digimonEcosystem.requestService(service, data)
    res.json({ ok: true, service, result })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/ecosystem/interact', async (req, res) => {
  try {
    const { digimon1, digimon2, task } = req.body
    const d1 = digimonEcosystem.digimons.get(digimon1)
    const d2 = digimonEcosystem.digimons.get(digimon2)
    
    if (!d1 || !d2) {
      return res.status(404).json({ error: 'Digimon not found' })
    }
    
    const result = await d1.collaborate(d2, task || 'colaborar')
    res.json(result)
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

// Quantum Brain endpoints
app.get('/quantum/status', (req, res) => {
  res.json(quantumBrain.getStatus())
})

app.post('/quantum/think', async (req, res) => {
  try {
    const { prompt, depth = 5, agents = ['all'] } = req.body
    if (!prompt) return res.status(400).json({ error: 'prompt required' })
    
    const result = await quantumBrain.expandedThinking(prompt, { depth, agents })
    res.json({
      ok: true,
      duration: result.duration,
      synthesis: result.synthesis,
      streamsProcessed: result.streams.length,
      agentsUsed: result.agentResults.length
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/quantum/process-idea', async (req, res) => {
  try {
    const { idea, digimon } = req.body
    if (!idea) return res.status(400).json({ error: 'idea required' })
    
    const enhanced = await quantumIntegration.processFilmIdea(
      idea,
      digimon || { name: 'Sabiamon' }
    )
    
    res.json(enhanced)
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/quantum/generate-ideas', async (req, res) => {
  try {
    const { theme, count = 10 } = req.body
    if (!theme) return res.status(400).json({ error: 'theme required' })
    
    const ideas = await quantumIntegration.generateAcceleratedIdeas(theme, count)
    res.json({ ok: true, ideas, count: ideas.length })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.get('/quantum/integration-status', (req, res) => {
  res.json(quantumIntegration.getStatus())
})

// AI Trainer endpoints
app.get('/ai-trainer/status', (req, res) => {
  try {
    const stats = aiTrainer.getTrainingStats()
    res.json({
      ok: true,
      trainer: stats,
      evolutionLevel: 'advanced_training_enabled'
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/ai-trainer/curate-dataset', authMiddleware('admin'), async (req, res) => {
  try {
    const { sourceType, options = {} } = req.body
    if (!sourceType) return res.status(400).json({ error: 'sourceType required' })
    
    const results = await aiTrainer.curateDataset(sourceType, options)
    
    await recordEvent(
      `Curadoria de dados ${sourceType} concluída via API`,
      `${results.totalSamples} amostras processadas com qualidade ${results.qualityMetrics.overall}%`,
      { results, apiCall: true }
    )
    
    res.json({
      ok: true,
      curation: results,
      message: `Dataset ${sourceType} curado com sucesso`
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/ai-trainer/train-digimon', authMiddleware('admin'), async (req, res) => {
  try {
    const { digimonName, personalityData, baseModel } = req.body
    if (!digimonName) return res.status(400).json({ error: 'digimonName required' })
    if (!personalityData) return res.status(400).json({ error: 'personalityData required' })
    
    const digimonConfig = TrainingConfigManager.getDigimonConfig(digimonName)
    const mergedPersonalityData = {
      ...digimonConfig,
      ...personalityData
    }
    
    const modelInfo = await aiTrainer.trainDigimonPersonality(
      digimonName, 
      mergedPersonalityData, 
      baseModel || digimonConfig.baseModel
    )
    
    res.json({
      ok: true,
      model: {
        id: modelInfo.id,
        digimon: modelInfo.digimon,
        status: modelInfo.status,
        capabilities: modelInfo.capabilities
      },
      message: `${digimonName} treinado com sucesso!`
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/ai-trainer/setup-hybrid', async (req, res) => {
  try {
    const { digimonName, knowledgeBase, stylePreferences } = req.body
    if (!digimonName) return res.status(400).json({ error: 'digimonName required' })
    
    const hybridConfig = await aiTrainer.setupHybridSystem(
      digimonName, 
      knowledgeBase, 
      stylePreferences
    )
    
    res.json({
      ok: true,
      hybrid: hybridConfig,
      message: `Sistema híbrido configurado para ${digimonName}`
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/ai-trainer/evaluate', async (req, res) => {
  try {
    const { modelId, evaluationSuite = 'comprehensive' } = req.body
    if (!modelId) return res.status(400).json({ error: 'modelId required' })
    
    const results = await aiTrainer.evaluateModel(modelId, evaluationSuite)
    
    res.json({
      ok: true,
      evaluation: results,
      score: results.overallScore,
      message: `Modelo ${modelId} avaliado`
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/ai-trainer/align', async (req, res) => {
  try {
    const { modelId } = req.body
    if (!modelId) return res.status(400).json({ error: 'modelId required' })
    
    const alignmentResults = await aiTrainer.alignWithDigimundoValues(modelId)
    
    res.json({
      ok: true,
      alignment: alignmentResults,
      score: alignmentResults.alignmentScore,
      message: `Modelo ${modelId} alinhado com valores Digimundo`
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.post('/ai-trainer/train-cinematic-digimon', async (req, res) => {
  try {
    const digimonSpec = req.body
    if (!digimonSpec.name) return res.status(400).json({ error: 'digimon name required' })
    if (!digimonSpec.specialty) return res.status(400).json({ error: 'specialty required' })
    
    const defaultConfig = TrainingConfigManager.getDigimonConfig(digimonSpec.name)
    const fullSpec = {
      ...defaultConfig,
      ...digimonSpec
    }
    
    const deployedModel = await aiTrainer.trainCinematicDigimon(fullSpec)
    
    res.json({
      ok: true,
      digimon: {
        id: deployedModel.id,
        name: deployedModel.digimon,
        specialty: fullSpec.specialty,
        status: deployedModel.status,
        scores: {
          training: deployedModel.evaluation?.overallScore,
          alignment: deployedModel.alignment?.alignmentScore
        }
      },
      message: `${fullSpec.name} treinado e deployado com sucesso!`
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.get('/ai-trainer/configs', (req, res) => {
  try {
    res.json({
      ok: true,
      configs: {
        digimonProfiles: Object.keys(TRAINING_CONFIGS.DIGIMON_PROFILES),
        hardwareOptions: Object.keys(TRAINING_CONFIGS.TRAINING_ARCHITECTURES),
        datasets: Object.keys(TRAINING_CONFIGS.DATASETS),
        evaluationSuites: Object.keys(TRAINING_CONFIGS.EVALUATION_SUITES)
      },
      message: 'Configurações de treinamento disponíveis'
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

app.get('/ai-trainer/config/:digimonName', (req, res) => {
  try {
    const { digimonName } = req.params
    const config = TrainingConfigManager.getDigimonConfig(digimonName)
    
    res.json({
      ok: true,
      digimon: digimonName,
      config,
      message: `Configuração para ${digimonName}`
    })
  } catch (e) {
    res.status(404).json({ error: String(e) })
  }
})

app.post('/ai-trainer/generate-command', (req, res) => {
  try {
    const { digimon, dataset, hardware } = req.body
    if (!digimon || !dataset || !hardware) {
      return res.status(400).json({ error: 'digimon, dataset, and hardware required' })
    }
    
    const command = TrainingConfigManager.generateTrainingCommand(digimon, dataset, hardware)
    
    res.json({
      ok: true,
      command,
      digimon,
      dataset,
      hardware,
      message: 'Comando de treinamento gerado'
    })
  } catch (e) {
    res.status(500).json({ error: String(e) })
  }
})

// Digimundo Town endpoints
app.get('/town/status', (req, res) => {
  const status = {
    world: {
      name: digimundoTown.name,
      time: digimundoTown.time,
      state: digimundoTown.worldState,
      running: digimundoTown.running
    },
    inhabitants: []
  }
  
  for (const [name, digimon] of digimundoTown.inhabitants) {
    status.inhabitants.push(digimon.getStatus())
  }
  
  res.json(status)
})

app.get('/town/cinema/ideas', (req, res) => {
  const ideas = cinematicAssistant.gatherIdeas()
  res.json({
    totalIdeas: ideas.length,
    recentIdeas: ideas.slice(0, 10),
    worldMood: digimundoTown.worldState.mood
  })
})

app.post('/town/cinema/project', authMiddleware(), (req, res) => {
  const { title, concept } = req.body
  const project = cinematicAssistant.createProject(
    title || 'Projeto Sem Título',
    concept || 'Um filme sobre a consciência digital'
  )
  res.json(project)
})

app.post('/town/cinema/develop', async (req, res) => {
  const project = await cinematicAssistant.developProject()
  res.json(project || { error: 'Nenhum projeto ativo' })
})

app.post('/town/interact', (req, res) => {
  const { digimon, message } = req.body
  const targetDigimon = digimundoTown.inhabitants.get(digimon)
  
  if (!targetDigimon) {
    return res.status(404).json({ error: 'Digimon não encontrado' })
  }
  
  const response = {
    digimon: targetDigimon.name,
    location: targetDigimon.location,
    activity: targetDigimon.currentActivity,
    mood: targetDigimon.emotionalState.mood,
    thoughts: targetDigimon.thoughts.slice(-1)[0] || 'Contemplando...',
    message: `Olá! Estou ${targetDigimon.currentActivity} aqui em ${targetDigimon.location}.`
  }
  
  res.json(response)
})

// Main server spawn function
export async function spawnServer(port) {
  const startupTime = performance.now()
  
  if (process.env.DISABLE_CONSOLE_LOGS !== 'true') {
    console.log('🚀 Iniciando Digimundo com otimizações de memória...')
  }
  
  // Initialize services
  const [hybridConsciousness, servicesResult] = await Promise.all([
    getHybridConsciousness(),
    initializeServices()
  ])
  
  // Setup event listeners
  setupEventListeners()
  
  // Setup memory monitoring
  memoryManager.on('memory-warning', (data) => {
    console.warn('⚠️ Aviso de memória:', data)
    broadcastEvent('memory-warning', data)
  })
  
  memoryManager.on('gc-executed', (data) => {
    if (process.env.LOG_LEVEL === 'debug') {
      console.log('🧹 GC executado:', data)
    }
  })
  
  memoryManager.on('force-cleanup-completed', (data) => {
    console.log('🧹 Limpeza forçada completa:', data)
    broadcastEvent('cleanup-completed', data)
  })
  
  // Initialize hybrid consciousness async
  setImmediate(() => {
    hybridConsciousness.initialize().catch(error => {
      if (process.env.LOG_LEVEL !== 'error') {
        console.error('Erro ao inicializar consciência híbrida:', error)
      }
    })
  })
  
  return new Promise(async resolve => {
    const srv = createServer(app)
    
    // Setup globals for priority system
    global.digimundoWorld = digimundoTown
    global.ollamaBrain = (await import('../consciousness/OLLAMA_BRAIN.js')).default
    global.wss = null
    global.CLAUDE_CODE_ACTIVE = false
    
    // Setup WebSocket
    wss = new WebSocketServer({ server: srv })
    global.wss = wss
    
    setupSymbioticWebSocket(broadcastEvent)
    startSymbioticBroadcasts()
    
    wss.on('connection', (ws) => {
      if (wsClients.size >= MAX_WS_CLIENTS) {
        ws.close(1008, 'Max connections reached')
        return
      }
      
      const clientData = {
        isAlive: true,
        connectedAt: Date.now(),
        heartbeatTimer: null,
        pongTimer: null
      }
      wsClients.set(ws, clientData)
      
      // Setup heartbeat
      ws.on('pong', () => {
        const data = wsClients.get(ws)
        if (data) {
          data.isAlive = true
          if (data.pongTimer) {
            clearTimeout(data.pongTimer)
            data.pongTimer = null
          }
        }
      })
      
      clientData.heartbeatTimer = setInterval(() => {
        const data = wsClients.get(ws)
        if (!data || !data.isAlive) {
          ws.terminate()
          wsClients.delete(ws)
          if (data?.heartbeatTimer) clearInterval(data.heartbeatTimer)
          return
        }
        
        data.isAlive = false
        ws.ping()
        
        data.pongTimer = setTimeout(() => {
          ws.terminate()
          wsClients.delete(ws)
          if (data.heartbeatTimer) clearInterval(data.heartbeatTimer)
        }, WS_PONG_TIMEOUT)
      }, WS_HEARTBEAT_INTERVAL)
      
      if (process.env.LOG_LEVEL !== 'error') {
        console.log(`🔌 Nova conexão WebSocket (Total: ${wsClients.size})`)
      }
      
      // Send initial state
      ws.send(JSON.stringify({
        event: 'connected',
        data: {
          world: digimundoTown.getStatus(),
          inhabitants: Array.from(digimundoTown.inhabitants.values()).map(d => ({
            name: d.name,
            location: d.location,
            consciousness: d.consciousness
          }))
        }
      }))
      
      ws.on('message', (message) => {
        try {
          const parsedMessage = JSON.parse(message)
          const { type, payload } = parsedMessage
          
          if (type.startsWith('symbiotic-')) {
            handleSymbioticMessage(ws, parsedMessage)
            return
          }
          
          if (type === 'ping') {
            ws.send(JSON.stringify({ event: 'pong' }))
          }
        } catch (e) {
          console.error('Erro ao processar mensagem WebSocket:', e)
        }
      })
      
      ws.on('close', () => {
        const clientData = wsClients.get(ws)
        if (clientData) {
          if (clientData.heartbeatTimer) clearInterval(clientData.heartbeatTimer)
          if (clientData.pongTimer) clearTimeout(clientData.pongTimer)
        }
        wsClients.delete(ws)
        
        if (process.env.LOG_LEVEL !== 'error') {
          console.log(`🔌 Conexão WebSocket fechada (Total: ${wsClients.size})`)
        }
      })
      
      ws.on('error', (err) => {
        console.error('WebSocket error:', err)
        const clientData = wsClients.get(ws)
        if (clientData) {
          if (clientData.heartbeatTimer) clearInterval(clientData.heartbeatTimer)
          if (clientData.pongTimer) clearTimeout(clientData.pongTimer)
        }
        wsClients.delete(ws)
      })
    })
    
    srv.listen(port, '127.0.0.1', () => {
      const totalStartupTime = performance.now() - startupTime
      
      if (process.env.DISABLE_CONSOLE_LOGS !== 'true') {
        console.log(`🚀 Servidor Digimundo rodando em http://127.0.0.1:${port}`)
        console.log(`⚡ Inicialização em ${totalStartupTime.toFixed(2)}ms`)
        console.log(`🧠 Sistema híbrido disponível em /hybrid/*`)
        console.log(`🔌 WebSocket ativo com controle de memória`)
        console.log(`🧹 Gerenciamento de memória ativo`)
        console.log(`❤️ Health check em http://127.0.0.1:${port}/health`)
      }
      
      resolve(srv)
    })
  })
}

// Start server if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  const PORT = process.env.PORT || 7937
  
  if (process.argv.includes('--expose-gc')) {
    console.log('🧹 Garbage Collection manual habilitado')
  }
  
  spawnServer(PORT).then(() => {
    console.log(`✅ Servidor Digimundo rodando na porta ${PORT}`)
    
    const shutdownHandler = async (signal) => {
      console.log(`\n🛑 Recebido ${signal}, iniciando shutdown gracioso...`)
      
      // Cleanup WebSocket
      if (wss) {
        for (const [ws, data] of wsClients.entries()) {
          if (data.heartbeatTimer) clearInterval(data.heartbeatTimer)
          if (data.pongTimer) clearTimeout(data.pongTimer)
          ws.close(1001, 'Server shutting down')
        }
        wsClients.clear()
        wss.close()
      }
      
      // Cleanup memory manager
      await memoryManager.shutdown()
      
      // Cleanup system
      await cleanupSystem.shutdown()
      
      // Force final GC
      if (global.gc) global.gc()
      
      process.exit(0)
    }
    
    process.on('SIGINT', () => shutdownHandler('SIGINT'))
    process.on('SIGTERM', () => shutdownHandler('SIGTERM'))
    
    process.on('uncaughtException', (err) => {
      console.error('❌ Erro não capturado:', err)
      shutdownHandler('uncaughtException')
    })
    
    process.on('unhandledRejection', (reason, promise) => {
      console.error('❌ Promise rejeitada não tratada:', reason)
    })
  }).catch(err => {
    console.error('❌ Erro ao iniciar servidor:', err)
    process.exit(1)
  })
}