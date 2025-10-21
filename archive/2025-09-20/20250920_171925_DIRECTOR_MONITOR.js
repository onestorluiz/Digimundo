/**
 * 👁️ MONITOR DO DIRETOR - Detecta e prioriza TODAS suas interações
 * 
 * Este sistema monitora TODOS os canais de entrada para detectar
 * quando o diretor está interagindo com o sistema
 */

import { EventEmitter } from 'events'
import { getPrioritySystem } from './PRIORITY_SYSTEM.js'
import fs from 'fs'
import path from 'path'

const PRIORITY = getPrioritySystem()

class DirectorMonitor extends EventEmitter {
  constructor() {
    super()
    this.isDirectorActive = false
    this.lastDirectorActivity = null
    this.monitoringChannels = new Set()
    this.activeProcesses = new Map()
    
    // Timeout para considerar que diretor terminou (5 segundos)
    this.directorTimeout = 5000
    this.timeoutHandle = null
    
    console.log('👁️ [DIRECTOR MONITOR] Sistema de Monitoramento Ativo')
    console.log('   Monitorando TODOS os canais para atividade do diretor')
    
    this.setupMonitors()
  }

  /**
   * Configura monitores em TODOS os pontos de entrada
   */
  setupMonitors() {
    // Monitor 1: Terminal/CLI
    this.monitorTerminal()
    
    // Monitor 2: HTTP Requests
    this.monitorHTTP()
    
    // Monitor 3: WebSocket
    this.monitorWebSocket()
    
    // Monitor 4: Arquivos do sistema
    this.monitorFileSystem()
    
    // Monitor 5: Processos do sistema
    this.monitorProcesses()
  }

  /**
   * DETECTA ATIVIDADE DO DIRETOR
   */
  directorDetected(source, data) {
    console.log('\n🚨🚨🚨 DIRETOR DETECTADO 🚨🚨🚨')
    console.log(`📍 Fonte: ${source}`)
    console.log(`📝 Dados:`, data)
    
    // Cancela timeout anterior
    if (this.timeoutHandle) {
      clearTimeout(this.timeoutHandle)
    }
    
    if (!this.isDirectorActive) {
      this.isDirectorActive = true
      this.lastDirectorActivity = new Date()
      
      // PARA TUDO IMEDIATAMENTE
      this.stopEverything()
    }
    
    // Define novo timeout
    this.timeoutHandle = setTimeout(() => {
      this.directorFinished()
    }, this.directorTimeout)
    
    this.emit('director-detected', {
      source,
      data,
      timestamp: new Date()
    })
  }

  /**
   * PARA ABSOLUTAMENTE TUDO
   */
  async stopEverything() {
    console.log('🛑 PARANDO TODO O ECOSSISTEMA...')
    
    // 1. Para o sistema de prioridade
    await PRIORITY.directorCommand('MONITOR_DETECTED')
    
    // 2. Para todos os processos Node
    this.pauseAllNodeProcesses()
    
    // 3. Para Ollama
    this.pauseOllama()
    
    // 4. Para o Digimundo
    this.pauseDigimundo()
    
    // 5. Para WebSockets
    this.pauseWebSockets()
    
    // 6. Para qualquer processamento async
    this.pauseAsyncOperations()
    
    console.log('✅ ECOSSISTEMA COMPLETAMENTE PAUSADO')
    console.log('   Aguardando comandos do diretor...\n')
  }

  /**
   * Pausa TODOS os processos Node
   */
  pauseAllNodeProcesses() {
    if (global.process && global.process._getActiveHandles) {
      const handles = process._getActiveHandles()
      handles.forEach(handle => {
        if (handle.pause && typeof handle.pause === 'function') {
          handle.pause()
        }
      })
    }
    
    // Pausa event loop parcialmente
    if (global.setImmediate) {
      this.pausedImmediate = global.setImmediate
      global.setImmediate = () => {}
    }
  }

  /**
   * Pausa Ollama via comando
   */
  async pauseOllama() {
    try {
      // Envia sinal para pausar Ollama
      const { exec } = await import('child_process')
      exec('pkill -STOP ollama', (error) => {
        if (!error) {
          console.log('   ✓ Ollama pausado')
        }
      })
    } catch (e) {
      // Ignora se não conseguir
    }
    
    // Também pausa via objeto global
    if (global.ollamaBrain?.pauseAll) {
      global.ollamaBrain.pauseAll()
    }
  }

  /**
   * Pausa o mundo Digimundo
   */
  pauseDigimundo() {
    if (global.digimundoWorld?.pauseAll) {
      global.digimundoWorld.pauseAll()
      console.log('   ✓ Digimundo pausado')
    }
  }

  /**
   * Pausa WebSockets
   */
  pauseWebSockets() {
    if (global.wss) {
      global.wss.clients.forEach(client => {
        client.pause()
      })
      console.log('   ✓ WebSockets pausados')
    }
  }

  /**
   * Pausa operações async
   */
  pauseAsyncOperations() {
    // Sobrescreve temporariamente Promise.prototype.then
    if (!this.originalThen) {
      this.originalThen = Promise.prototype.then
      Promise.prototype.then = function(...args) {
        if (global.DIRECTOR_ACTIVE) {
          // Adia execução
          return new Promise(() => {})
        }
        return this.originalThen.apply(this, args)
      }
    }
    
    global.DIRECTOR_ACTIVE = true
  }

  /**
   * Diretor terminou - resume tudo
   */
  directorFinished() {
    if (!this.isDirectorActive) return
    
    console.log('✅ [DIRECTOR MONITOR] Diretor terminou. Resumindo ecossistema...')
    
    this.isDirectorActive = false
    global.DIRECTOR_ACTIVE = false
    
    // Resume sistema de prioridade
    PRIORITY.directorFinished()
    
    // Resume Ollama
    this.resumeOllama()
    
    // Resume Digimundo
    this.resumeDigimundo()
    
    // Resume WebSockets
    this.resumeWebSockets()
    
    // Resume async
    this.resumeAsyncOperations()
    
    // Resume Node processes
    this.resumeNodeProcesses()
    
    console.log('🌟 Ecossistema retomado\n')
  }

  /**
   * Resume Ollama
   */
  async resumeOllama() {
    try {
      const { exec } = await import('child_process')
      exec('pkill -CONT ollama', (error) => {
        if (!error) {
          console.log('   ✓ Ollama retomado')
        }
      })
    } catch (e) {
      // Ignora
    }
    
    if (global.ollamaBrain?.resumeAll) {
      global.ollamaBrain.resumeAll()
    }
  }

  /**
   * Resume Digimundo
   */
  resumeDigimundo() {
    if (global.digimundoWorld?.resumeAll) {
      global.digimundoWorld.resumeAll()
    }
  }

  /**
   * Resume WebSockets
   */
  resumeWebSockets() {
    if (global.wss) {
      global.wss.clients.forEach(client => {
        if (client.resume) client.resume()
      })
    }
  }

  /**
   * Resume operações async
   */
  resumeAsyncOperations() {
    if (this.originalThen) {
      Promise.prototype.then = this.originalThen
      this.originalThen = null
    }
  }

  /**
   * Resume processos Node
   */
  resumeNodeProcesses() {
    if (this.pausedImmediate) {
      global.setImmediate = this.pausedImmediate
      this.pausedImmediate = null
    }
    
    if (global.process && global.process._getActiveHandles) {
      const handles = process._getActiveHandles()
      handles.forEach(handle => {
        if (handle.resume && typeof handle.resume === 'function') {
          handle.resume()
        }
      })
    }
  }

  /**
   * MONITORES ESPECÍFICOS
   */
  
  // Monitor Terminal/CLI
  monitorTerminal() {
    if (process.stdin) {
      process.stdin.on('data', (data) => {
        this.directorDetected('TERMINAL', data.toString())
      })
    }
  }
  
  // Monitor HTTP
  monitorHTTP() {
    // Será conectado ao Express
    this.monitoringChannels.add('HTTP')
  }
  
  // Monitor WebSocket
  monitorWebSocket() {
    // Será conectado ao WS server
    this.monitoringChannels.add('WEBSOCKET')
  }
  
  // Monitor Sistema de Arquivos
  monitorFileSystem() {
    // Monitora mudanças em arquivos chave
    const watchPaths = [
      path.join(process.cwd(), 'director_commands.txt'),
      path.join(process.cwd(), 'PRIORITY_OVERRIDE.txt')
    ]
    
    watchPaths.forEach(watchPath => {
      fs.watchFile(watchPath, { interval: 1000 }, (curr, prev) => {
        if (curr.mtime !== prev.mtime) {
          this.directorDetected('FILE_SYSTEM', `Arquivo modificado: ${watchPath}`)
        }
      })
    })
  }
  
  // Monitor Processos
  monitorProcesses() {
    // Monitora se Claude Code está ativo
    setInterval(() => {
      if (global.CLAUDE_CODE_ACTIVE) {
        this.directorDetected('CLAUDE_CODE', 'Claude Code está processando')
      }
    }, 500)
  }

  /**
   * Middleware para Express - detecta requests do diretor
   */
  expressMiddleware() {
    return (req, res, next) => {
      // Detecta se é request do diretor
      if (
        req.headers['x-director'] === 'true' ||
        req.path.includes('/director') ||
        req.body?.director === true ||
        req.query?.director === 'true'
      ) {
        this.directorDetected('HTTP_REQUEST', {
          method: req.method,
          path: req.path,
          body: req.body
        })
      }
      next()
    }
  }

  /**
   * Status do monitor
   */
  getStatus() {
    return {
      isDirectorActive: this.isDirectorActive,
      lastActivity: this.lastDirectorActivity,
      monitoringChannels: Array.from(this.monitoringChannels),
      activeProcesses: this.activeProcesses.size
    }
  }
}

// Singleton global e auto-inicialização
let monitorInstance = null

export function getDirectorMonitor() {
  if (!monitorInstance) {
    monitorInstance = new DirectorMonitor()
    
    // Torna global para acesso imediato
    global.DIRECTOR_MONITOR = monitorInstance
    
    // Marca quando Claude Code está ativo
    global.CLAUDE_CODE_ACTIVE = false
  }
  return monitorInstance
}

// Auto-inicializa
const DIRECTOR_MONITOR = getDirectorMonitor()

export { DirectorMonitor, DIRECTOR_MONITOR }
export default DIRECTOR_MONITOR