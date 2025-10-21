/**
 * 🔌 RESILIENT WEBSOCKET - WebSocket com Fallback Automático
 * Implementa reconexão automática e fallback para long-polling
 */

const WebSocket = require('ws');
const http = require('http');
const EventEmitter = require('events');

class ResilientWebSocket extends EventEmitter {
  constructor(url, options = {}) {
    super();
    
    this.url = url;
    this.options = {
      reconnectInterval: options.reconnectInterval || 5000,
      maxReconnectAttempts: options.maxReconnectAttempts || 10,
      heartbeatInterval: options.heartbeatInterval || 30000,
      fallbackAfterAttempts: options.fallbackAfterAttempts || 3,
      longPollingInterval: options.longPollingInterval || 1000,
      ...options
    };
    
    this.ws = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.mode = 'websocket'; // 'websocket' ou 'longpolling'
    this.messageQueue = [];
    this.longPollingActive = false;
    this.lastMessageId = 0;
    
    // Métricas
    this.metrics = {
      totalConnections: 0,
      totalReconnections: 0,
      fallbacksTriggered: 0,
      messagesReceived: 0,
      messagesSent: 0,
      currentMode: 'websocket'
    };
  }

  /**
   * Conecta com estratégia resiliente
   */
  async connect() {
    console.log('🔌 Iniciando conexão resiliente...');
    
    try {
      await this.connectWebSocket();
    } catch (error) {
      console.log('⚠️ WebSocket falhou, tentando fallback...');
      await this.fallbackToLongPolling();
    }
    
    return this.isConnected;
  }

  /**
   * Tenta conectar via WebSocket
   */
  connectWebSocket() {
    return new Promise((resolve, reject) => {
      try {
        // Extrair host e porta da URL
        const urlParts = new URL(this.url.replace('ws://', 'http://'));
        
        this.ws = new WebSocket(this.url);
        
        // Timeout para conexão
        const timeout = setTimeout(() => {
          if (!this.isConnected) {
            this.ws.close();
            reject(new Error('WebSocket connection timeout'));
          }
        }, 10000);
        
        this.ws.on('open', () => {
          clearTimeout(timeout);
          this.isConnected = true;
          this.mode = 'websocket';
          this.reconnectAttempts = 0;
          this.metrics.totalConnections++;
          this.metrics.currentMode = 'websocket';
          
          console.log('✅ WebSocket conectado');
          this.emit('connected', { mode: 'websocket' });
          
          // Iniciar heartbeat
          this.startHeartbeat();
          
          // Processar fila de mensagens
          this.processMessageQueue();
          
          resolve(true);
        });
        
        this.ws.on('message', (data) => {
          this.metrics.messagesReceived++;
          
          try {
            const message = JSON.parse(data.toString());
            this.lastMessageId = message.id || this.lastMessageId + 1;
            this.emit('message', message);
          } catch (error) {
            this.emit('message', data.toString());
          }
        });
        
        this.ws.on('error', (error) => {
          console.error('❌ WebSocket erro:', error.message);
          this.emit('error', error);
          
          if (!this.isConnected) {
            clearTimeout(timeout);
            reject(error);
          }
        });
        
        this.ws.on('close', () => {
          this.isConnected = false;
          this.stopHeartbeat();
          
          console.log('🔌 WebSocket desconectado');
          this.emit('disconnected', { mode: 'websocket' });
          
          // Tentar reconectar
          this.handleReconnection();
        });
        
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Gerencia reconexão com estratégia de backoff
   */
  async handleReconnection() {
    if (this.reconnectAttempts >= this.options.maxReconnectAttempts) {
      console.log('⚠️ Máximo de tentativas alcançado');
      this.emit('max_reconnect_reached');
      return;
    }
    
    if (this.reconnectAttempts >= this.options.fallbackAfterAttempts && this.mode === 'websocket') {
      console.log('🔄 Mudando para long-polling...');
      await this.fallbackToLongPolling();
      return;
    }
    
    this.reconnectAttempts++;
    this.metrics.totalReconnections++;
    
    // Backoff exponencial
    const delay = Math.min(
      this.options.reconnectInterval * Math.pow(1.5, this.reconnectAttempts - 1),
      30000
    );
    
    console.log(`⏳ Reconectando em ${delay}ms (tentativa ${this.reconnectAttempts})...`);
    
    setTimeout(async () => {
      try {
        await this.connectWebSocket();
      } catch (error) {
        this.handleReconnection();
      }
    }, delay);
  }

  /**
   * Fallback para long-polling
   */
  async fallbackToLongPolling() {
    if (this.longPollingActive) return;
    
    this.mode = 'longpolling';
    this.longPollingActive = true;
    this.metrics.fallbacksTriggered++;
    this.metrics.currentMode = 'longpolling';
    
    console.log('📡 Modo long-polling ativado');
    this.emit('fallback', { mode: 'longpolling' });
    
    // Iniciar loop de polling
    this.startLongPolling();
    
    // Tentar reconectar WebSocket em background
    this.attemptWebSocketReconnectInBackground();
  }

  /**
   * Loop de long-polling
   */
  startLongPolling() {
    const poll = async () => {
      if (!this.longPollingActive) return;
      
      try {
        const messages = await this.fetchMessages();
        
        for (const message of messages) {
          this.metrics.messagesReceived++;
          this.lastMessageId = message.id || this.lastMessageId + 1;
          this.emit('message', message);
        }
        
      } catch (error) {
        console.error('❌ Erro no long-polling:', error.message);
        this.emit('error', error);
      }
      
      // Continuar polling
      if (this.longPollingActive) {
        setTimeout(poll, this.options.longPollingInterval);
      }
    };
    
    poll();
  }

  /**
   * Busca mensagens via HTTP (long-polling)
   */
  fetchMessages() {
    return new Promise((resolve, reject) => {
      const urlParts = new URL(this.url.replace('ws://', 'http://'));
      
      const options = {
        hostname: urlParts.hostname,
        port: urlParts.port,
        path: `/messages?since=${this.lastMessageId}`,
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      };
      
      const req = http.request(options, (res) => {
        let data = '';
        
        res.on('data', (chunk) => {
          data += chunk;
        });
        
        res.on('end', () => {
          try {
            const messages = JSON.parse(data);
            resolve(Array.isArray(messages) ? messages : [messages]);
          } catch (error) {
            resolve([]);
          }
        });
      });
      
      req.on('error', reject);
      req.setTimeout(30000, () => {
        req.destroy();
        resolve([]);
      });
      
      req.end();
    });
  }

  /**
   * Tenta reconectar WebSocket em background durante long-polling
   */
  attemptWebSocketReconnectInBackground() {
    const tryReconnect = async () => {
      if (!this.longPollingActive) return;
      
      try {
        console.log('🔄 Tentando reconectar WebSocket em background...');
        await this.connectWebSocket();
        
        // Se conseguiu, parar long-polling
        this.longPollingActive = false;
        console.log('✅ WebSocket reconectado! Saindo do long-polling');
        
      } catch (error) {
        // Tentar novamente em 30 segundos
        if (this.longPollingActive) {
          setTimeout(tryReconnect, 30000);
        }
      }
    };
    
    // Primeira tentativa em 10 segundos
    setTimeout(tryReconnect, 10000);
  }

  /**
   * Envia mensagem (funciona em ambos os modos)
   */
  send(data) {
    const message = typeof data === 'string' ? data : JSON.stringify(data);
    
    if (this.mode === 'websocket' && this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(message);
      this.metrics.messagesSent++;
      return true;
      
    } else if (this.mode === 'longpolling') {
      // Enviar via HTTP POST
      this.sendViaHttp(message);
      return true;
      
    } else {
      // Adicionar à fila
      this.messageQueue.push(message);
      console.log('📦 Mensagem adicionada à fila (sem conexão)');
      return false;
    }
  }

  /**
   * Envia mensagem via HTTP (fallback)
   */
  sendViaHttp(message) {
    const urlParts = new URL(this.url.replace('ws://', 'http://'));
    
    const options = {
      hostname: urlParts.hostname,
      port: urlParts.port,
      path: '/messages',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(message)
      }
    };
    
    const req = http.request(options, (res) => {
      if (res.statusCode === 200) {
        this.metrics.messagesSent++;
      }
    });
    
    req.on('error', (error) => {
      console.error('❌ Erro ao enviar via HTTP:', error.message);
      this.messageQueue.push(message);
    });
    
    req.write(message);
    req.end();
  }

  /**
   * Processa fila de mensagens após reconexão
   */
  processMessageQueue() {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      this.send(message);
    }
  }

  /**
   * Heartbeat para manter conexão viva
   */
  startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.ping();
      }
    }, this.options.heartbeatInterval);
  }

  /**
   * Para o heartbeat
   */
  stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  /**
   * Desconecta e limpa recursos
   */
  disconnect() {
    this.longPollingActive = false;
    this.stopHeartbeat();
    
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    
    this.isConnected = false;
    this.emit('disconnected', { mode: this.mode });
  }

  /**
   * Obtém métricas de conexão
   */
  getMetrics() {
    return {
      ...this.metrics,
      queueSize: this.messageQueue.length,
      reconnectAttempts: this.reconnectAttempts,
      isConnected: this.isConnected,
      uptime: this.isConnected ? Date.now() - this.connectedAt : 0
    };
  }

  /**
   * Verifica status da conexão
   */
  isAlive() {
    return this.isConnected || this.longPollingActive;
  }
}

// Servidor de exemplo para testes
function createTestServer(port = 8765) {
  const wss = new WebSocket.Server({ port });
  const messages = [];
  let messageId = 0;
  
  // WebSocket handler
  wss.on('connection', (ws) => {
    console.log('Cliente WebSocket conectado');
    
    ws.on('message', (data) => {
      const message = { id: ++messageId, data: data.toString(), timestamp: Date.now() };
      messages.push(message);
      
      // Broadcast
      wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify(message));
        }
      });
    });
  });
  
  // HTTP server para fallback
  const httpServer = http.createServer((req, res) => {
    res.setHeader('Content-Type', 'application/json');
    
    if (req.method === 'GET' && req.url.startsWith('/messages')) {
      // Long-polling GET
      const url = new URL(req.url, `http://${req.headers.host}`);
      const since = parseInt(url.searchParams.get('since') || '0');
      
      const newMessages = messages.filter(m => m.id > since);
      res.end(JSON.stringify(newMessages));
      
    } else if (req.method === 'POST' && req.url === '/messages') {
      // Fallback POST
      let body = '';
      req.on('data', chunk => body += chunk);
      req.on('end', () => {
        const message = { id: ++messageId, data: body, timestamp: Date.now() };
        messages.push(message);
        res.end(JSON.stringify({ success: true, id: message.id }));
      });
      
    } else {
      res.statusCode = 404;
      res.end(JSON.stringify({ error: 'Not found' }));
    }
  });
  
  httpServer.listen(port + 1);
  
  console.log(`🚀 Servidor de teste rodando:`);
  console.log(`   WebSocket: ws://localhost:${port}`);
  console.log(`   HTTP: http://localhost:${port + 1}`);
  
  return { wss, httpServer };
}

// Teste
if (require.main === module) {
  (async () => {
    console.log('🧪 TESTANDO RESILIENT WEBSOCKET\\n');
    
    // Criar servidor de teste
    const server = createTestServer(8765);
    
    // Criar cliente resiliente
    const client = new ResilientWebSocket('ws://localhost:8765', {
      fallbackAfterAttempts: 2,
      reconnectInterval: 2000
    });
    
    // Configurar listeners
    client.on('connected', (info) => {
      console.log(`✅ Cliente conectado via ${info.mode}`);
    });
    
    client.on('message', (msg) => {
      console.log(`📨 Mensagem recebida:`, msg);
    });
    
    client.on('fallback', (info) => {
      console.log(`⚠️ Fallback ativado: ${info.mode}`);
    });
    
    client.on('error', (error) => {
      console.log(`❌ Erro:`, error.message);
    });
    
    // Conectar
    await client.connect();
    
    // Enviar mensagens
    console.log('\\n📤 Enviando mensagens...');
    client.send({ type: 'test', content: 'Hello WebSocket!' });
    
    // Simular queda do WebSocket após 5 segundos
    setTimeout(() => {
      console.log('\\n💥 Simulando queda do WebSocket...');
      server.wss.close();
    }, 5000);
    
    // Enviar mensagem durante fallback
    setTimeout(() => {
      console.log('\\n📤 Enviando durante fallback...');
      client.send({ type: 'test', content: 'Hello Long-Polling!' });
    }, 8000);
    
    // Métricas após 15 segundos
    setTimeout(() => {
      console.log('\\n📊 Métricas finais:');
      console.log(client.getMetrics());
      
      process.exit(0);
    }, 15000);
  })();
}

module.exports = ResilientWebSocket;