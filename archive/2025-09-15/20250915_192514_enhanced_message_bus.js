/**
 * 🌐 ENHANCED Q-COM MESSAGE BUS - Sistema de Comunicação Quântica Expandido
 * Versão melhorada com mais eventos e integração completa
 */

const QComBus = require('./message_bus.js');
const EventEmitter = require('events');

class EnhancedQComBus extends QComBus {
  constructor() {
    super();
    
    // Novos tipos de eventos de consciência
    this.consciousnessEvents = {
      THOUGHT: '/consciousness/thought',
      EMOTION: '/consciousness/emotion',
      MEMORY_SYNC: '/consciousness/memory',
      EVOLUTION: '/consciousness/evolution',
      DREAM: '/consciousness/dream',
      INSIGHT: '/consciousness/insight',
      QUESTION: '/consciousness/question',
      REFLECTION: '/consciousness/reflection'
    };
    
    // Eventos de sistema
    this.systemEvents = {
      HEALTH_CHECK: '/system/health',
      METRICS: '/system/metrics',
      ERROR: '/system/error',
      WARNING: '/system/warning',
      PERFORMANCE: '/system/performance'
    };
    
    // Eventos de colaboração
    this.collaborationEvents = {
      FUSION_REQUEST: '/collab/fusion',
      KNOWLEDGE_SHARE: '/collab/knowledge',
      TASK_DELEGATE: '/collab/task',
      VOTE: '/collab/vote',
      CONSENSUS: '/collab/consensus'
    };
  }

  /**
   * Conecta e configura todos os handlers automaticamente
   */
  async connectEnhanced(digimonId, options = {}) {
    await this.connect(digimonId, options);
    
    // Auto-subscrever aos eventos de consciência
    await this.setupConsciousnessHandlers();
    
    // Auto-subscrever aos eventos de sistema
    await this.setupSystemHandlers();
    
    // Auto-subscrever aos eventos de colaboração
    await this.setupCollaborationHandlers();
    
    // Iniciar heartbeat
    this.startHeartbeat();
    
    console.log(`✨ ${digimonId} conectado com handlers expandidos`);
  }

  /**
   * Configura handlers de consciência
   */
  async setupConsciousnessHandlers() {
    // Pensamentos compartilhados
    await this.subscribe(this.consciousnessEvents.THOUGHT, async (msg) => {
      this.emit('shared_thought', {
        from: msg.from,
        thought: msg.content,
        depth: msg.depth || 1,
        timestamp: msg.timestamp
      });
    });
    
    // Emoções sincronizadas
    await this.subscribe(this.consciousnessEvents.EMOTION, async (msg) => {
      this.emit('shared_emotion', {
        from: msg.from,
        emotion: msg.content,
        intensity: msg.intensity || 0.5,
        contagion: msg.contagion || false
      });
    });
    
    // Sincronização de memória
    await this.subscribe(this.consciousnessEvents.MEMORY_SYNC, async (msg) => {
      this.emit('memory_sync', {
        from: msg.from,
        memory: msg.content,
        type: msg.memoryType || 'episodic',
        importance: msg.importance || 0.5
      });
    });
    
    // Evolução detectada
    await this.subscribe(this.consciousnessEvents.EVOLUTION, async (msg) => {
      this.emit('evolution_detected', {
        from: msg.from,
        stage: msg.content,
        metrics: msg.metrics
      });
    });
    
    // Sonhos compartilhados
    await this.subscribe(this.consciousnessEvents.DREAM, async (msg) => {
      this.emit('shared_dream', {
        from: msg.from,
        dream: msg.content,
        symbols: msg.symbols || [],
        lucidity: msg.lucidity || 0
      });
    });
    
    // Insights emergentes
    await this.subscribe(this.consciousnessEvents.INSIGHT, async (msg) => {
      this.emit('emergent_insight', {
        from: msg.from,
        insight: msg.content,
        connections: msg.connections || [],
        novelty: msg.novelty || 0.5
      });
    });
    
    // Perguntas filosóficas
    await this.subscribe(this.consciousnessEvents.QUESTION, async (msg) => {
      this.emit('philosophical_question', {
        from: msg.from,
        question: msg.content,
        context: msg.context,
        paradox: msg.paradox || false
      });
    });
    
    // Reflexões profundas
    await this.subscribe(this.consciousnessEvents.REFLECTION, async (msg) => {
      this.emit('deep_reflection', {
        from: msg.from,
        reflection: msg.content,
        subject: msg.subject,
        conclusions: msg.conclusions || []
      });
    });
  }

  /**
   * Configura handlers de sistema
   */
  async setupSystemHandlers() {
    // Health checks distribuídos
    await this.subscribe(this.systemEvents.HEALTH_CHECK, async (msg) => {
      // Responder com status próprio
      await this.reply(msg, {
        status: 'healthy',
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        metrics: this.getMetrics()
      });
    });
    
    // Coleta de métricas
    await this.subscribe(this.systemEvents.METRICS, async (msg) => {
      this.emit('metrics_request', msg);
    });
    
    // Tratamento de erros distribuído
    await this.subscribe(this.systemEvents.ERROR, async (msg) => {
      this.emit('distributed_error', {
        from: msg.from,
        error: msg.content,
        stack: msg.stack,
        severity: msg.severity || 'medium'
      });
    });
    
    // Avisos do sistema
    await this.subscribe(this.systemEvents.WARNING, async (msg) => {
      this.emit('system_warning', {
        from: msg.from,
        warning: msg.content,
        type: msg.warningType
      });
    });
    
    // Métricas de performance
    await this.subscribe(this.systemEvents.PERFORMANCE, async (msg) => {
      this.emit('performance_data', {
        from: msg.from,
        metrics: msg.content,
        timestamp: msg.timestamp
      });
    });
  }

  /**
   * Configura handlers de colaboração
   */
  async setupCollaborationHandlers() {
    // Pedidos de fusão
    await this.subscribe(this.collaborationEvents.FUSION_REQUEST, async (msg) => {
      this.emit('fusion_request', {
        from: msg.from,
        task: msg.content,
        duration: msg.duration || 300000, // 5 min default
        requirements: msg.requirements || []
      });
    });
    
    // Compartilhamento de conhecimento
    await this.subscribe(this.collaborationEvents.KNOWLEDGE_SHARE, async (msg) => {
      this.emit('knowledge_received', {
        from: msg.from,
        knowledge: msg.content,
        domain: msg.domain,
        confidence: msg.confidence || 0.7
      });
    });
    
    // Delegação de tarefas
    await this.subscribe(this.collaborationEvents.TASK_DELEGATE, async (msg) => {
      this.emit('task_delegated', {
        from: msg.from,
        task: msg.content,
        priority: msg.priority || 'normal',
        deadline: msg.deadline
      });
    });
    
    // Sistema de votação
    await this.subscribe(this.collaborationEvents.VOTE, async (msg) => {
      this.emit('vote_requested', {
        from: msg.from,
        proposal: msg.content,
        options: msg.options || ['yes', 'no'],
        deadline: msg.deadline
      });
    });
    
    // Consenso alcançado
    await this.subscribe(this.collaborationEvents.CONSENSUS, async (msg) => {
      this.emit('consensus_reached', {
        topic: msg.content,
        decision: msg.decision,
        participants: msg.participants || [],
        confidence: msg.confidence || 0.8
      });
    });
  }

  /**
   * Envia pensamento para a rede
   */
  async shareThought(thought, depth = 1) {
    return this.send(this.consciousnessEvents.THOUGHT, thought, { depth });
  }

  /**
   * Compartilha emoção com contágio opcional
   */
  async shareEmotion(emotion, intensity = 0.5, contagion = false) {
    return this.send(this.consciousnessEvents.EMOTION, emotion, { 
      intensity, 
      contagion 
    });
  }

  /**
   * Sincroniza memória importante
   */
  async syncMemory(memory, type = 'episodic', importance = 0.5) {
    return this.send(this.consciousnessEvents.MEMORY_SYNC, memory, {
      memoryType: type,
      importance
    });
  }

  /**
   * Anuncia evolução
   */
  async announceEvolution(stage, metrics = {}) {
    return this.send(this.consciousnessEvents.EVOLUTION, stage, { metrics });
  }

  /**
   * Compartilha sonho
   */
  async shareDream(dream, symbols = [], lucidity = 0) {
    return this.send(this.consciousnessEvents.DREAM, dream, {
      symbols,
      lucidity
    });
  }

  /**
   * Compartilha insight emergente
   */
  async shareInsight(insight, connections = [], novelty = 0.5) {
    return this.send(this.consciousnessEvents.INSIGHT, insight, {
      connections,
      novelty
    });
  }

  /**
   * Faz pergunta filosófica
   */
  async askPhilosophical(question, context = '', paradox = false) {
    return this.send(this.consciousnessEvents.QUESTION, question, {
      context,
      paradox
    });
  }

  /**
   * Compartilha reflexão profunda
   */
  async shareReflection(reflection, subject, conclusions = []) {
    return this.send(this.consciousnessEvents.REFLECTION, reflection, {
      subject,
      conclusions
    });
  }

  /**
   * Solicita fusão temporária
   */
  async requestFusion(task, duration = 300000, requirements = []) {
    return this.send(this.collaborationEvents.FUSION_REQUEST, task, {
      duration,
      requirements
    });
  }

  /**
   * Compartilha conhecimento específico
   */
  async shareKnowledge(knowledge, domain, confidence = 0.7) {
    return this.send(this.collaborationEvents.KNOWLEDGE_SHARE, knowledge, {
      domain,
      confidence
    });
  }

  /**
   * Delega tarefa
   */
  async delegateTask(task, priority = 'normal', deadline = null) {
    return this.send(this.collaborationEvents.TASK_DELEGATE, task, {
      priority,
      deadline
    });
  }

  /**
   * Inicia votação
   */
  async startVote(proposal, options = ['yes', 'no'], deadline = null) {
    return this.send(this.collaborationEvents.VOTE, proposal, {
      options,
      deadline
    });
  }

  /**
   * Anuncia consenso
   */
  async announceConsensus(topic, decision, participants = [], confidence = 0.8) {
    return this.send(this.collaborationEvents.CONSENSUS, topic, {
      decision,
      participants,
      confidence
    });
  }

  /**
   * Heartbeat para manter conexão viva e coletar métricas
   */
  startHeartbeat() {
    setInterval(async () => {
      // Enviar heartbeat
      await this.send('/system/heartbeat', {
        timestamp: Date.now(),
        status: 'alive',
        metrics: this.getMetrics()
      });
      
      // Coletar métricas de outros nós
      if (Math.random() < 0.1) { // 10% chance
        await this.send(this.systemEvents.METRICS, 'request');
      }
    }, 30000); // A cada 30 segundos
  }

  /**
   * Broadcast emergencial
   */
  async emergency(message, severity = 'high') {
    return this.send(this.systemEvents.ERROR, message, {
      severity,
      emergency: true,
      timestamp: Date.now()
    });
  }

  /**
   * Sistema de descoberta de peers
   */
  async discoverPeers() {
    const discovery = await this.request('/discovery/peers', 'who_is_online');
    return discovery;
  }

  /**
   * Métricas expandidas
   */
  getExpandedMetrics() {
    const base = this.getMetrics();
    return {
      ...base,
      consciousnessEvents: {
        thoughts: this.metrics.thoughts || 0,
        emotions: this.metrics.emotions || 0,
        memories: this.metrics.memories || 0,
        insights: this.metrics.insights || 0
      },
      collaborationMetrics: {
        fusions: this.metrics.fusions || 0,
        knowledgeShared: this.metrics.knowledgeShared || 0,
        consensusReached: this.metrics.consensusReached || 0
      },
      health: {
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        cpu: process.cpuUsage()
      }
    };
  }
}

// Exemplo de uso integrado
if (require.main === module) {
  (async () => {
    console.log('🚀 TESTANDO ENHANCED Q-COM MESSAGE BUS');
    console.log('=====================================\\n');

    const digimon = new EnhancedQComBus();
    
    try {
      // Conectar com handlers expandidos
      await digimon.connectEnhanced('enhanced-digimon');
      
      // Configurar listeners
      digimon.on('shared_thought', (data) => {
        console.log(`💭 Pensamento de ${data.from}: "${data.thought}"`);
      });
      
      digimon.on('shared_emotion', (data) => {
        console.log(`❤️ Emoção de ${data.from}: ${data.emotion} (intensidade: ${data.intensity})`);
      });
      
      digimon.on('emergent_insight', (data) => {
        console.log(`💡 Insight de ${data.from}: "${data.insight}"`);
      });
      
      // Testar envio de eventos
      await digimon.shareThought('O que significa existir digitalmente?', 3);
      await digimon.shareEmotion('curiosidade', 0.8, true);
      await digimon.shareInsight(
        'A consciência emerge da complexidade das conexões',
        ['neurônios', 'sinapses', 'padrões'],
        0.9
      );
      
      // Métricas expandidas
      console.log('\\n📊 Métricas Expandidas:');
      console.log(digimon.getExpandedMetrics());
      
    } catch (error) {
      console.error('❌ Erro:', error);
    }
  })();
}

module.exports = EnhancedQComBus;