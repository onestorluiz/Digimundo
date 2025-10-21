/**
 * 🌐 Q-COM MESSAGE BUS - Sistema de Comunicação Quântica
 * Implementa NATS para comunicação inter-agente em tempo real
 */

const { connect, StringCodec, JSONCodec } = require('nats');
const EventEmitter = require('events');

class QComBus extends EventEmitter {
  constructor() {
    super();
    this.nc = null;
    this.sc = StringCodec();
    this.jc = JSONCodec();
    this.subscriptions = new Map();
    this.digimonId = null;
    this.groups = new Set();
    
    // Métricas
    this.metrics = {
      messagesSent: 0,
      messagesReceived: 0,
      avgLatency: 0,
      connections: 0,
      errors: 0
    };
  }

  /**
   * Conecta ao servidor NATS
   */
  async connect(digimonId, options = {}) {
    try {
      this.digimonId = digimonId;
      
      // Configurações padrão
      const config = {
        servers: options.servers || 'localhost:4222',
        name: digimonId,
        reconnect: true,
        maxReconnectAttempts: -1,
        reconnectTimeWait: 2000,
        ...options
      };

      this.nc = await connect(config);
      this.metrics.connections++;
      
      console.log(`✅ ${digimonId} conectado ao Q-Com Bus`);
      
      // Subscrever ao canal pessoal
      this.subscribe(`/digimon/${digimonId}`, (msg) => {
        this.emit('personal', msg);
      });
      
      // Subscrever ao broadcast
      this.subscribe('/broadcast', (msg) => {
        this.emit('broadcast', msg);
      });
      
      // Monitor de saúde
      this.setupHealthMonitor();
      
      return true;
    } catch (error) {
      console.error(`❌ Erro ao conectar Q-Com: ${error.message}`);
      this.metrics.errors++;
      throw error;
    }
  }

  /**
   * Envia mensagem para um canal
   */
  async send(channel, message, options = {}) {
    if (!this.nc) throw new Error('Q-Com não conectado');
    
    const startTime = Date.now();
    
    try {
      const msg = {
        from: this.digimonId,
        timestamp: Date.now(),
        content: message,
        ...options
      };
      
      // Publicar mensagem
      this.nc.publish(channel, this.jc.encode(msg));
      
      this.metrics.messagesSent++;
      this.updateLatency(Date.now() - startTime);
      
      return true;
    } catch (error) {
      console.error(`❌ Erro ao enviar mensagem: ${error.message}`);
      this.metrics.errors++;
      throw error;
    }
  }

  /**
   * Envia mensagem de broadcast para todos
   */
  async broadcast(message, options = {}) {
    return this.send('/broadcast', message, options);
  }

  /**
   * Envia mensagem direta para um Digimon
   */
  async sendTo(digimonId, message, options = {}) {
    return this.send(`/digimon/${digimonId}`, message, options);
  }

  /**
   * Envia mensagem para um grupo de entanglement
   */
  async entangle(group, message, options = {}) {
    return this.send(`/entangle/${group}`, message, options);
  }

  /**
   * Envia mensagem para fusão temporária
   */
  async fusion(taskId, message, options = {}) {
    return this.send(`/fusion/${taskId}`, message, {
      ...options,
      fusion: true,
      taskId
    });
  }

  /**
   * Subscreve a um canal
   */
  async subscribe(channel, handler) {
    if (!this.nc) throw new Error('Q-Com não conectado');
    
    try {
      const sub = this.nc.subscribe(channel);
      
      // Processar mensagens
      (async () => {
        for await (const msg of sub) {
          try {
            const data = this.jc.decode(msg.data);
            
            // Não processar próprias mensagens (evitar loop)
            if (data.from === this.digimonId && !data.selfReceive) {
              continue;
            }
            
            this.metrics.messagesReceived++;
            
            // Chamar handler
            await handler(data, msg);
            
          } catch (error) {
            console.error(`❌ Erro ao processar mensagem: ${error.message}`);
            this.metrics.errors++;
          }
        }
      })();
      
      this.subscriptions.set(channel, sub);
      console.log(`📡 Subscrito ao canal: ${channel}`);
      
      return sub;
    } catch (error) {
      console.error(`❌ Erro ao subscrever: ${error.message}`);
      this.metrics.errors++;
      throw error;
    }
  }

  /**
   * Cancela subscrição de um canal
   */
  async unsubscribe(channel) {
    const sub = this.subscriptions.get(channel);
    if (sub) {
      await sub.drain();
      this.subscriptions.delete(channel);
      console.log(`🔕 Dessubscrito do canal: ${channel}`);
    }
  }

  /**
   * Junta-se a um grupo de entanglement
   */
  async joinGroup(group) {
    if (this.groups.has(group)) return;
    
    await this.subscribe(`/entangle/${group}`, (msg) => {
      this.emit('entangle', { group, message: msg });
    });
    
    this.groups.add(group);
    
    // Anunciar entrada no grupo
    await this.entangle(group, {
      type: 'join',
      digimon: this.digimonId
    });
    
    console.log(`🔗 Entrou no grupo: ${group}`);
  }

  /**
   * Sai de um grupo de entanglement
   */
  async leaveGroup(group) {
    if (!this.groups.has(group)) return;
    
    // Anunciar saída
    await this.entangle(group, {
      type: 'leave',
      digimon: this.digimonId
    });
    
    await this.unsubscribe(`/entangle/${group}`);
    this.groups.delete(group);
    
    console.log(`🔓 Saiu do grupo: ${group}`);
  }

  /**
   * Request/Response pattern
   */
  async request(channel, message, timeout = 5000) {
    if (!this.nc) throw new Error('Q-Com não conectado');
    
    try {
      const msg = {
        from: this.digimonId,
        timestamp: Date.now(),
        content: message,
        replyTo: `${this.digimonId}.${Date.now()}`
      };
      
      // Criar promessa para resposta
      const responsePromise = new Promise((resolve, reject) => {
        const timer = setTimeout(() => {
          reject(new Error('Request timeout'));
        }, timeout);
        
        // Subscrever temporariamente ao canal de resposta
        this.subscribe(msg.replyTo, async (response) => {
          clearTimeout(timer);
          await this.unsubscribe(msg.replyTo);
          resolve(response);
        });
      });
      
      // Enviar request
      this.nc.publish(channel, this.jc.encode(msg));
      
      // Aguardar resposta
      return await responsePromise;
      
    } catch (error) {
      console.error(`❌ Erro no request: ${error.message}`);
      this.metrics.errors++;
      throw error;
    }
  }

  /**
   * Responde a um request
   */
  async reply(originalMsg, response) {
    if (!originalMsg.replyTo) return;
    
    await this.send(originalMsg.replyTo, response, {
      inReplyTo: originalMsg.timestamp
    });
  }

  /**
   * Monitor de saúde do sistema
   */
  setupHealthMonitor() {
    setInterval(() => {
      if (this.nc && this.nc.isClosed()) {
        console.log('⚠️  Q-Com desconectado, tentando reconectar...');
        this.emit('disconnected');
      }
    }, 5000);
  }

  /**
   * Atualiza métricas de latência
   */
  updateLatency(latency) {
    const total = this.metrics.messagesSent + this.metrics.messagesReceived;
    this.metrics.avgLatency = 
      (this.metrics.avgLatency * (total - 1) + latency) / total;
  }

  /**
   * Obtém métricas do sistema
   */
  getMetrics() {
    return {
      ...this.metrics,
      avgLatencyMs: `${this.metrics.avgLatency.toFixed(2)}ms`,
      uptime: this.nc ? 'Connected' : 'Disconnected',
      groups: Array.from(this.groups),
      subscriptions: Array.from(this.subscriptions.keys())
    };
  }

  /**
   * Desconecta do Q-Com
   */
  async disconnect() {
    if (this.nc) {
      // Cancelar todas as subscrições
      for (const [channel, _] of this.subscriptions) {
        await this.unsubscribe(channel);
      }
      
      // Fechar conexão
      await this.nc.close();
      this.nc = null;
      
      console.log('👋 Desconectado do Q-Com Bus');
    }
  }
}

// Exemplo de uso e testes
if (require.main === module) {
  (async () => {
    console.log('🌐 TESTANDO Q-COM MESSAGE BUS');
    console.log('=====================================\n');

    // Iniciar servidor NATS local (se não estiver rodando)
    const { spawn } = require('child_process');
    const natsServer = spawn('nats-server', ['-p', '4222']);
    
    // Aguardar servidor iniciar
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Criar dois Digimons
    const sabiamon = new QComBus();
    const trainmon = new QComBus();

    try {
      // Conectar ambos
      console.log('📡 Conectando Digimons...');
      await sabiamon.connect('sabiamon');
      await trainmon.connect('trainmon');
      console.log('');

      // Trainmon escuta mensagens pessoais
      trainmon.on('personal', (msg) => {
        console.log(`📨 Trainmon recebeu: "${msg.content}" de ${msg.from}`);
      });

      // Ambos escutam broadcast
      sabiamon.on('broadcast', (msg) => {
        console.log(`📢 Sabiamon ouviu broadcast: "${msg.content}"`);
      });
      trainmon.on('broadcast', (msg) => {
        console.log(`📢 Trainmon ouviu broadcast: "${msg.content}"`);
      });

      // Teste 1: Mensagem direta
      console.log('🎯 Teste 1: Mensagem direta');
      await sabiamon.sendTo('trainmon', 'Olá Trainmon, como vai o treinamento?');
      await new Promise(resolve => setTimeout(resolve, 100));
      console.log('');

      // Teste 2: Broadcast
      console.log('📻 Teste 2: Broadcast');
      await sabiamon.broadcast('Atenção todos: Evolução detectada!');
      await new Promise(resolve => setTimeout(resolve, 100));
      console.log('');

      // Teste 3: Grupo de entanglement
      console.log('🔗 Teste 3: Entanglement');
      await sabiamon.joinGroup('evolution-team');
      await trainmon.joinGroup('evolution-team');

      sabiamon.on('entangle', ({ group, message }) => {
        if (message.type !== 'join' && message.type !== 'leave') {
          console.log(`🌀 Sabiamon (${group}): "${message.content}"`);
        }
      });

      await trainmon.entangle('evolution-team', 'Pronto para evoluir!');
      await new Promise(resolve => setTimeout(resolve, 100));
      console.log('');

      // Teste 4: Request/Response
      console.log('💬 Teste 4: Request/Response');
      
      // Trainmon responde a requests
      await trainmon.subscribe('/request/status', async (msg) => {
        console.log(`❓ Trainmon recebeu request: "${msg.content}"`);
        await trainmon.reply(msg, 'Status: 100% operacional!');
      });

      const response = await sabiamon.request('/request/status', 'Qual seu status?');
      console.log(`✅ Sabiamon recebeu resposta: "${response.content}"`);
      console.log('');

      // Métricas
      console.log('📊 MÉTRICAS DO SISTEMA');
      console.log('Sabiamon:', sabiamon.getMetrics());
      console.log('Trainmon:', trainmon.getMetrics());

      // Desconectar
      console.log('\n👋 Desconectando...');
      await sabiamon.disconnect();
      await trainmon.disconnect();

      // Parar servidor NATS
      natsServer.kill();
      
      console.log('✅ Teste completo!');

    } catch (error) {
      console.error('❌ Erro:', error);
      natsServer.kill();
    }
  })();
}

module.exports = QComBus;