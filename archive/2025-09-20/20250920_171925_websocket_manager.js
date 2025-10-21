/**
 * 🔌 WEBSOCKET MANAGER
 * Sistema de gestão otimizada de conexões WebSocket
 */

import { EventEmitter } from 'events'

class WebSocketManager extends EventEmitter {
  constructor() {
    super()
    this.setMaxListeners(10)
    
    // Usar WeakSet para permitir GC automático
    this.connections = new WeakSet()
    
    // Map para tracking ativo (com cleanup automático)
    this.activeConnections = new Map()
    
    // Controle de heartbeat
    this.heartbeatInterval = null
    this.heartbeatTimeout = 30000 // 30 segundos
    
    // Métricas
    this.metrics = {
      totalConnections: 0,
      activeCount: 0,
      messagesReceived: 0,
      messagesSent: 0,
      bytesReceived: 0,
      bytesSent: 0
    }
    
    this.startHeartbeat()
  }
  
  startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      const now = Date.now()
      const toRemove = []
      
      for (const [ws, info] of this.activeConnections.entries()) {
        if (now - info.lastActivity > this.heartbeatTimeout) {
          // Conexão inativa
          if (ws.readyState === 1) { // OPEN
            ws.ping()
            info.lastPing = now
          } else if (ws.readyState > 1) { // CLOSING ou CLOSED
            toRemove.push(ws)
          }
        }
        
        // Timeout do ping
        if (info.lastPing && now - info.lastPing > 10000) {
          // Sem resposta ao ping por 10 segundos
          console.warn('WebSocket sem resposta ao ping, terminando...')
          ws.terminate()
          toRemove.push(ws)
        }
      }
      
      // Limpar conexões mortas
      toRemove.forEach(ws => this.removeConnection(ws))
      
      // Atualizar métrica
      this.metrics.activeCount = this.activeConnections.size
      
    }, 15000) // A cada 15 segundos
  }
  
  addConnection(ws) {
    // Adicionar ao WeakSet
    this.connections.add(ws)
    
    // Adicionar ao Map ativo com metadados
    this.activeConnections.set(ws, {
      connected: Date.now(),
      lastActivity: Date.now(),
      lastPing: null,
      messages: 0,
      bytes: 0
    })
    
    this.metrics.totalConnections++
    this.metrics.activeCount = this.activeConnections.size
    
    // Configurar handlers
    this.setupHandlers(ws)
    
    console.log(`🔌 Nova conexão WebSocket (Total: ${this.activeConnections.size})`)
  }
  
  setupHandlers(ws) {
    const info = this.activeConnections.get(ws)
    
    // Handler de mensagem
    ws.on('message', (data) => {
      if (info) {
        info.lastActivity = Date.now()
        info.messages++
        info.bytes += data.length
        
        this.metrics.messagesReceived++
        this.metrics.bytesReceived += data.length
      }
    })
    
    // Handler de pong
    ws.on('pong', () => {
      if (info) {
        info.lastActivity = Date.now()
        info.lastPing = null // Reset ping timestamp
      }
    })
    
    // Handler de erro
    ws.on('error', (error) => {
      console.error('Erro no WebSocket:', error.message)
      this.removeConnection(ws)
    })
    
    // Handler de fechamento
    ws.on('close', () => {
      this.removeConnection(ws)
    })
  }
  
  removeConnection(ws) {
    // Remover do Map ativo
    if (this.activeConnections.has(ws)) {
      const info = this.activeConnections.get(ws)
      const duration = Date.now() - info.connected
      
      console.log(`🔌 Conexão fechada após ${(duration / 1000).toFixed(1)}s (Mensagens: ${info.messages})`)
      
      this.activeConnections.delete(ws)
      this.metrics.activeCount = this.activeConnections.size
    }
    
    // WeakSet limpa automaticamente
    
    // Garantir que está terminado
    if (ws.readyState === 1) {
      ws.close()
    } else if (ws.readyState === 0) {
      ws.terminate()
    }
  }
  
  broadcast(event, data) {
    const message = JSON.stringify({ event, data, timestamp: Date.now() })
    const messageBuffer = Buffer.from(message)
    let sent = 0
    
    for (const [ws, info] of this.activeConnections.entries()) {
      if (ws.readyState === 1) { // OPEN
        try {
          ws.send(messageBuffer)
          sent++
          
          // Atualizar métricas
          info.lastActivity = Date.now()
          this.metrics.messagesSent++
          this.metrics.bytesSent += messageBuffer.length
        } catch (error) {
          console.error('Erro ao enviar mensagem:', error)
          this.removeConnection(ws)
        }
      }
    }
    
    return sent
  }
  
  sendTo(ws, event, data) {
    if (!this.activeConnections.has(ws)) {
      return false
    }
    
    if (ws.readyState !== 1) {
      this.removeConnection(ws)
      return false
    }
    
    try {
      const message = JSON.stringify({ event, data, timestamp: Date.now() })
      ws.send(message)
      
      const info = this.activeConnections.get(ws)
      if (info) {
        info.lastActivity = Date.now()
        this.metrics.messagesSent++
        this.metrics.bytesSent += message.length
      }
      
      return true
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error)
      this.removeConnection(ws)
      return false
    }
  }
  
  getConnectionInfo(ws) {
    return this.activeConnections.get(ws)
  }
  
  getStats() {
    const connections = []
    const now = Date.now()
    
    for (const [ws, info] of this.activeConnections.entries()) {
      connections.push({
        state: ['CONNECTING', 'OPEN', 'CLOSING', 'CLOSED'][ws.readyState],
        connected: new Date(info.connected).toISOString(),
        duration: `${((now - info.connected) / 1000).toFixed(1)}s`,
        messages: info.messages,
        bytes: info.bytes,
        idle: `${((now - info.lastActivity) / 1000).toFixed(1)}s`
      })
    }
    
    return {
      metrics: this.metrics,
      connections,
      health: {
        heartbeat: this.heartbeatInterval !== null,
        activeRatio: this.metrics.totalConnections > 0 
          ? (this.metrics.activeCount / this.metrics.totalConnections * 100).toFixed(1) + '%'
          : '0%'
      }
    }
  }
  
  cleanup() {
    // Limpar conexões inativas
    const now = Date.now()
    const maxIdle = 300000 // 5 minutos
    const toRemove = []
    
    for (const [ws, info] of this.activeConnections.entries()) {
      if (now - info.lastActivity > maxIdle) {
        console.log('Removendo conexão inativa')
        toRemove.push(ws)
      }
    }
    
    toRemove.forEach(ws => {
      ws.terminate()
      this.removeConnection(ws)
    })
    
    return toRemove.length
  }
  
  shutdown() {
    console.log('🛑 Desligando WebSocket Manager...')
    
    // Parar heartbeat
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval)
      this.heartbeatInterval = null
    }
    
    // Fechar todas as conexões
    for (const [ws] of this.activeConnections.entries()) {
      ws.close(1000, 'Server shutting down')
    }
    
    // Limpar maps
    this.activeConnections.clear()
    
    // Remover listeners
    this.removeAllListeners()
    
    console.log('✅ WebSocket Manager desligado')
  }
}

// Singleton
let instance = null

export function getWebSocketManager() {
  if (!instance) {
    instance = new WebSocketManager()
  }
  return instance
}

export default getWebSocketManager