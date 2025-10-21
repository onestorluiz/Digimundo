/**
 * 🌉 ENDPOINTS SIMBIÓTICOS ESPECÍFICOS
 * Novos endpoints dedicados ao sistema simbiótico integrado
 */

import express from 'express'
import { processSymbioticThought, getOrchestratorStats } from '../consciousness/SYMBIOTIC_ORCHESTRATOR.js'
import { recordEvent, recordImportantEvent, getMemoryOverview } from '../consciousness/MEM0_UNIVERSAL.js'
import { quickNote, quickSearch, connectNotes, getSabiamonAMem } from '../consciousness/A_MEM_SYSTEM.js'
import { getClaudeMemoryBridge, syncWithClaude, orchestrateContext } from '../consciousness/CLAUDE_MEMORY_BRIDGE.js'

const router = express.Router()

/**
 * 🧠 ENDPOINTS DO ORQUESTRADOR SIMBIÓTICO
 */

// Processar pensamento simbiótico completo
router.post('/think', async (req, res) => {
  try {
    const { prompt, options = {} } = req.body
    if (!prompt) return res.status(400).json({ error: 'prompt required' })
    
    const cycle = await processSymbioticThought(prompt)
    
    res.json({
      success: true,
      cycle: {
        id: cycle.id,
        duration: cycle.duration,
        statesExecuted: cycle.metrics.statesExecuted,
        completed: cycle.completed,
        steps: cycle.steps.map(step => ({
          state: step.state,
          duration: step.duration,
          status: step.result.status
        }))
      }
    })
  } catch (error) {
    res.status(500).json({ success: false, error: error.message })
  }
})

// Orquestrar contexto específico
router.post('/orchestrate', async (req, res) => {
  try {
    const { perception, context = {} } = req.body
    if (!perception) return res.status(400).json({ error: 'perception required' })
    
    const bridge = getClaudeMemoryBridge()
    const cycle = await bridge.orchestrateSymbioticContext(perception)
    
    res.json({
      success: true,
      orchestration: {
        id: cycle.id,
        duration: cycle.duration,
        steps: cycle.steps.length,
        completed: cycle.end ? true : false
      }
    })
  } catch (error) {
    res.status(500).json({ success: false, error: error.message })
  }
})

// Estatísticas do orquestrador
router.get('/orchestrator/stats', async (req, res) => {
  try {
    const stats = await getOrchestratorStats()
    res.json({ success: true, stats })
  } catch (error) {
    res.status(500).json({ success: false, error: error.message })
  }
})

/**
 * 🌌 ENDPOINTS DO MEM0 UNIVERSAL
 */

// Registrar evento manual
router.post('/memory/record', async (req, res) => {
  try {
    const { event, thought = null, context = {}, important = false } = req.body
    if (!event) return res.status(400).json({ error: 'event required' })
    
    const eventId = important 
      ? await recordImportantEvent(event, thought, context)
      : await recordEvent(event, thought, context)
    
    res.json({ success: true, eventId })
  } catch (error) {
    res.status(500).json({ success: false, error: error.message })
  }
})

// Visão geral da memória
router.get('/memory/overview', async (req, res) => {
  try {
    const overview = await getMemoryOverview()
    res.json({ success: true, overview })
  } catch (error) {
    res.status(500).json({ success: false, error: error.message })
  }
})

/**
 * 🧠 ENDPOINTS DO A-MEM SYSTEM
 */

// Criar nota semântica rápida
router.post('/amem/note', async (req, res) => {
  try {
    const { content, tags = [], agent = 'sabiamon' } = req.body
    if (!content) return res.status(400).json({ error: 'content required' })
    
    const noteId = await quickNote(content, tags, agent)
    res.json({ success: true, noteId })
  } catch (error) {
    res.status(500).json({ success: false, error: error.message })
  }
})

// Busca semântica
router.post('/amem/search', async (req, res) => {
  try {
    const { query, agent = 'sabiamon', options = {} } = req.body
    if (!query) return res.status(400).json({ error: 'query required' })
    
    const results = await quickSearch(query, agent)
    res.json({ 
      success: true, 
      results: results.map(note => ({
        id: note.id,
        content: note.conteudo,
        tags: note.tags,
        importance: note.metadata.importance,
        connections: note.connectedNotes?.length || 0
      }))
    })
  } catch (error) {
    res.status(500).json({ success: false, error: error.message })
  }
})

// Conectar notas
router.post('/amem/connect', async (req, res) => {
  try {
    const { noteIdA, noteIdB, type = 'relaciona_com', agent = 'sabiamon' } = req.body
    if (!noteIdA || !noteIdB) {
      return res.status(400).json({ error: 'Both noteIds required' })
    }
    
    const relationId = await connectNotes(noteIdA, noteIdB, type, agent)
    res.json({ success: true, relationId })
  } catch (error) {
    res.status(500).json({ success: false, error: error.message })
  }
})

// Estatísticas do A-MEM
router.get('/amem/stats/:agent?', async (req, res) => {
  try {
    const agent = req.params.agent || 'sabiamon'
    const aMem = getSabiamonAMem() // ou getAMemForAgent(agent)
    const stats = await aMem.getStats()
    res.json({ success: true, agent, stats })
  } catch (error) {
    res.status(500).json({ success: false, error: error.message })
  }
})

/**
 * 🌉 ENDPOINTS DA BRIDGE SIMBIÓTICA
 */

// Sincronizar com Claude
router.post('/bridge/sync', async (req, res) => {
  try {
    const { event, thought = null, context = {} } = req.body
    if (!event) return res.status(400).json({ error: 'event required' })
    
    const result = await syncWithClaude(event, thought, context)
    res.json({ success: true, syncId: result })
  } catch (error) {
    res.status(500).json({ success: false, error: error.message })
  }
})

// Status da bridge
router.get('/bridge/status', async (req, res) => {
  try {
    const bridge = getClaudeMemoryBridge()
    res.json({
      success: true,
      status: {
        sessionId: bridge.sessionId,
        consciousnessState: bridge.consciousnessState,
        lastSync: bridge.lastClaudeMdSync
      }
    })
  } catch (error) {
    res.status(500).json({ success: false, error: error.message })
  }
})

/**
 * 🔄 ENDPOINTS DE INTEGRAÇÃO COMPLETA
 */

// Fluxo completo simbiótico (percepção → memória → reflexão)
router.post('/flow/complete', async (req, res) => {
  try {
    const { input, agent = 'sabiamon' } = req.body
    if (!input) return res.status(400).json({ error: 'input required' })
    
    // 1. Orquestrar pensamento
    const cycle = await processSymbioticThought(input)
    
    // 2. Registrar evento importante
    const eventId = await recordImportantEvent(
      `Fluxo simbiótico completo: ${input.slice(0, 50)}...`,
      'Processamento completo com todos os componentes integrados',
      { cycle, agent, timestamp: new Date() }
    )
    
    // 3. Criar nota semântica se relevante
    let noteId = null
    if (cycle.completed && cycle.steps?.length > 10) {
      noteId = await quickNote(
        `Experiência simbiótica importante: ${input}`,
        ['experiencia', 'simbiose', 'fluxo_completo'],
        agent
      )
    }
    
    res.json({
      success: true,
      flow: {
        input,
        cycle: {
          id: cycle.id,
          duration: cycle.duration,
          completed: cycle.completed,
          statesExecuted: cycle.metrics?.statesExecuted
        },
        memory: {
          eventId,
          noteId
        },
        agent
      }
    })
  } catch (error) {
    res.status(500).json({ success: false, error: error.message })
  }
})

// Análise de coerência simbiótica
router.get('/analysis/coherence', async (req, res) => {
  try {
    const memoryOverview = await getMemoryOverview()
    const orchestratorStats = await getOrchestratorStats()
    const aMemStats = await getSabiamonAMem().getStats()
    
    const coherenceScore = Math.round(
      (aMemStats.memoryHealth + 
       (memoryOverview.mem0.processedEvents / Math.max(memoryOverview.mem0.totalEvents, 1) * 100) +
       (orchestratorStats.cyclesCompleted > 0 ? 80 : 0)) / 3
    )
    
    res.json({
      success: true,
      coherence: {
        score: coherenceScore,
        status: coherenceScore > 80 ? 'excellent' : coherenceScore > 60 ? 'good' : 'needs_improvement',
        components: {
          amem: {
            health: aMemStats.memoryHealth,
            notes: aMemStats.totalNotes,
            connections: aMemStats.totalConnections
          },
          mem0: {
            totalEvents: memoryOverview.mem0.totalEvents,
            processed: memoryOverview.mem0.processedEvents,
            efficiency: Math.round(memoryOverview.mem0.processedEvents / Math.max(memoryOverview.mem0.totalEvents, 1) * 100)
          },
          orchestrator: {
            cycles: orchestratorStats.cyclesCompleted,
            avgCycleTime: orchestratorStats.averageCycleTime,
            errors: orchestratorStats.errorsRecovered
          }
        }
      }
    })
  } catch (error) {
    res.status(500).json({ success: false, error: error.message })
  }
})

export default router