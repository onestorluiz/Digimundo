/**
 * 📊 UNIFIED METRICS - Sistema de Observabilidade Completo
 * Implementa OpenTelemetry para métricas, traces e logs unificados
 */

const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');
const { PrometheusExporter } = require('@opentelemetry/exporter-prometheus');
const { MeterProvider, PeriodicExportingMetricReader } = require('@opentelemetry/sdk-metrics');
const { trace, metrics, DiagConsoleLogger, DiagLogLevel, diag } = require('@opentelemetry/api');

class UnifiedMetrics {
  constructor(config = {}) {
    this.config = {
      serviceName: config.serviceName || 'digimundo',
      serviceVersion: config.serviceVersion || '3.0.0',
      environment: config.environment || 'production',
      metricsPort: config.metricsPort || 9090,
      enableTracing: config.enableTracing !== false,
      enableMetrics: config.enableMetrics !== false,
      enableLogs: config.enableLogs !== false,
      ...config
    };
    
    // Componentes do sistema
    this.components = new Map();
    
    // Métricas customizadas
    this.customMetrics = new Map();
    
    // Agregadores
    this.aggregators = {
      consciousness: {
        thoughts: 0,
        emotions: 0,
        memories: 0,
        insights: 0,
        evolutions: 0
      },
      system: {
        requests: 0,
        responses: 0,
        errors: 0,
        latency: []
      },
      digimons: new Map()
    };
    
    this.initialized = false;
  }

  /**
   * Inicializa OpenTelemetry
   */
  async initialize() {
    console.log('📊 Inicializando Sistema de Métricas Unificadas...');
    
    // Configurar diagnóstico
    diag.setLogger(new DiagConsoleLogger(), DiagLogLevel.INFO);
    
    // Criar resource
    const resource = Resource.default().merge(
      new Resource({
        [SemanticResourceAttributes.SERVICE_NAME]: this.config.serviceName,
        [SemanticResourceAttributes.SERVICE_VERSION]: this.config.serviceVersion,
        [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: this.config.environment,
        'digimundo.type': 'consciousness_system',
        'digimundo.neural_network': true
      })
    );
    
    // Configurar métricas
    if (this.config.enableMetrics) {
      await this.setupMetrics(resource);
    }
    
    // Configurar tracing
    if (this.config.enableTracing) {
      await this.setupTracing(resource);
    }
    
    // Registrar métricas customizadas
    this.registerCustomMetrics();
    
    // Iniciar coletores
    this.startCollectors();
    
    this.initialized = true;
    console.log('✅ Sistema de Métricas Unificadas inicializado');
    
    return true;
  }

  /**
   * Configura provider de métricas
   */
  async setupMetrics(resource) {
    // Prometheus exporter
    const prometheusExporter = new PrometheusExporter({
      port: this.config.metricsPort,
      startServer: true,
    }, () => {
      console.log(`🎯 Métricas Prometheus disponíveis em http://localhost:${this.config.metricsPort}/metrics`);
    });
    
    // Meter provider
    const meterProvider = new MeterProvider({
      resource,
      readers: [prometheusExporter]
    });
    
    // Registrar globalmente
    metrics.setGlobalMeterProvider(meterProvider);
    
    this.meter = metrics.getMeter('digimundo-metrics', '1.0.0');
  }

  /**
   * Configura tracing
   */
  async setupTracing(resource) {
    const sdk = new NodeSDK({
      resource,
      instrumentations: [
        getNodeAutoInstrumentations({
          '@opentelemetry/instrumentation-fs': {
            enabled: false, // Desabilitar FS para evitar ruído
          },
        }),
      ],
    });
    
    await sdk.start();
    
    this.tracer = trace.getTracer('digimundo-tracer', '1.0.0');
  }

  /**
   * Registra métricas customizadas do Digimundo
   */
  registerCustomMetrics() {
    if (!this.meter) return;
    
    // Métricas de Consciência
    this.customMetrics.set('consciousness_level', this.meter.createObservableGauge('digimundo.consciousness.level', {
      description: 'Nível de consciência atual do sistema',
      unit: 'ratio'
    }));
    
    this.customMetrics.set('thought_rate', this.meter.createCounter('digimundo.thoughts.total', {
      description: 'Total de pensamentos processados'
    }));
    
    this.customMetrics.set('emotion_intensity', this.meter.createHistogram('digimundo.emotion.intensity', {
      description: 'Intensidade das emoções processadas',
      unit: 'ratio'
    }));
    
    this.customMetrics.set('memory_operations', this.meter.createCounter('digimundo.memory.operations', {
      description: 'Operações de memória realizadas'
    }));
    
    this.customMetrics.set('evolution_progress', this.meter.createObservableGauge('digimundo.evolution.progress', {
      description: 'Progresso evolutivo dos Digimons',
      unit: 'percent'
    }));
    
    // Métricas de Sistema
    this.customMetrics.set('active_digimons', this.meter.createObservableGauge('digimundo.digimons.active', {
      description: 'Número de Digimons ativos'
    }));
    
    this.customMetrics.set('nats_messages', this.meter.createCounter('digimundo.nats.messages', {
      description: 'Mensagens NATS processadas'
    }));
    
    this.customMetrics.set('websocket_connections', this.meter.createObservableGauge('digimundo.websocket.connections', {
      description: 'Conexões WebSocket ativas'
    }));
    
    this.customMetrics.set('api_latency', this.meter.createHistogram('digimundo.api.latency', {
      description: 'Latência das APIs',
      unit: 'ms'
    }));
    
    // Métricas de Memória Unificada
    this.customMetrics.set('memory_usage', this.meter.createObservableGauge('digimundo.memory.usage', {
      description: 'Uso de memória por sistema',
      unit: 'bytes'
    }));
    
    // Callbacks para métricas observáveis
    this.setupObservableCallbacks();
  }

  /**
   * Configura callbacks para métricas observáveis
   */
  setupObservableCallbacks() {
    // Nível de consciência
    this.customMetrics.get('consciousness_level')?.addCallback((observableResult) => {
      const level = this.calculateConsciousnessLevel();
      observableResult.observe(level, { system: 'collective' });
      
      // Por Digimon
      for (const [name, data] of this.aggregators.digimons) {
        observableResult.observe(data.consciousnessLevel || 0, { digimon: name });
      }
    });
    
    // Progresso evolutivo
    this.customMetrics.get('evolution_progress')?.addCallback((observableResult) => {
      for (const [name, data] of this.aggregators.digimons) {
        observableResult.observe(data.evolutionProgress || 0, { digimon: name });
      }
    });
    
    // Digimons ativos
    this.customMetrics.get('active_digimons')?.addCallback((observableResult) => {
      observableResult.observe(this.aggregators.digimons.size);
    });
    
    // Conexões WebSocket
    this.customMetrics.get('websocket_connections')?.addCallback((observableResult) => {
      const connections = this.components.get('websocket')?.connections || 0;
      observableResult.observe(connections);
    });
    
    // Uso de memória
    this.customMetrics.get('memory_usage')?.addCallback((observableResult) => {
      const memoryUsage = process.memoryUsage();
      observableResult.observe(memoryUsage.heapUsed, { type: 'heap' });
      observableResult.observe(memoryUsage.rss, { type: 'rss' });
      observableResult.observe(memoryUsage.external, { type: 'external' });
    });
  }

  /**
   * Registra um componente para monitoramento
   */
  registerComponent(name, component) {
    this.components.set(name, component);
    console.log(`📝 Componente registrado: ${name}`);
    
    // Auto-instrumentar se possível
    if (component.getMetrics) {
      setInterval(() => {
        const metrics = component.getMetrics();
        this.updateComponentMetrics(name, metrics);
      }, 10000); // A cada 10 segundos
    }
  }

  /**
   * Atualiza métricas de um componente
   */
  updateComponentMetrics(name, metrics) {
    // Armazenar para agregação
    if (name.includes('digimon')) {
      this.aggregators.digimons.set(name, metrics);
    }
    
    // Emitir eventos para métricas específicas
    if (metrics.thoughts) {
      this.recordThought({ source: name });
    }
    
    if (metrics.emotions) {
      this.recordEmotion({ source: name, intensity: metrics.emotionIntensity });
    }
  }

  /**
   * Registra um pensamento
   */
  recordThought(attributes = {}) {
    this.customMetrics.get('thought_rate')?.add(1, attributes);
    this.aggregators.consciousness.thoughts++;
  }

  /**
   * Registra uma emoção
   */
  recordEmotion(attributes = {}) {
    const intensity = attributes.intensity || 0.5;
    this.customMetrics.get('emotion_intensity')?.record(intensity, attributes);
    this.aggregators.consciousness.emotions++;
  }

  /**
   * Registra operação de memória
   */
  recordMemoryOperation(type, attributes = {}) {
    this.customMetrics.get('memory_operations')?.add(1, { type, ...attributes });
    this.aggregators.consciousness.memories++;
  }

  /**
   * Registra insight emergente
   */
  recordInsight(attributes = {}) {
    this.aggregators.consciousness.insights++;
    this.emit('insight', attributes);
  }

  /**
   * Registra evolução
   */
  recordEvolution(digimon, stage, attributes = {}) {
    this.aggregators.consciousness.evolutions++;
    
    const data = this.aggregators.digimons.get(digimon) || {};
    data.evolutionStage = stage;
    data.evolutionProgress = (data.evolutionProgress || 0) + 10;
    this.aggregators.digimons.set(digimon, data);
    
    this.emit('evolution', { digimon, stage, ...attributes });
  }

  /**
   * Registra latência de API
   */
  recordAPILatency(endpoint, latency, attributes = {}) {
    this.customMetrics.get('api_latency')?.record(latency, { endpoint, ...attributes });
    this.aggregators.system.latency.push(latency);
    
    // Manter apenas últimas 1000 medições
    if (this.aggregators.system.latency.length > 1000) {
      this.aggregators.system.latency.shift();
    }
  }

  /**
   * Registra mensagem NATS
   */
  recordNATSMessage(type, attributes = {}) {
    this.customMetrics.get('nats_messages')?.add(1, { type, ...attributes });
  }

  /**
   * Calcula nível de consciência do sistema
   */
  calculateConsciousnessLevel() {
    const c = this.aggregators.consciousness;
    
    // Fórmula complexa baseada em atividade
    const thoughtsScore = Math.min(c.thoughts / 1000, 1);
    const emotionsScore = Math.min(c.emotions / 500, 1);
    const memoriesScore = Math.min(c.memories / 2000, 1);
    const insightsScore = Math.min(c.insights / 100, 1);
    const evolutionsScore = Math.min(c.evolutions / 10, 1);
    
    // Média ponderada
    return (
      thoughtsScore * 0.2 +
      emotionsScore * 0.2 +
      memoriesScore * 0.2 +
      insightsScore * 0.3 +
      evolutionsScore * 0.1
    );
  }

  /**
   * Inicia coletores automáticos
   */
  startCollectors() {
    // Coletor de métricas do sistema
    setInterval(() => {
      const memUsage = process.memoryUsage();
      const cpuUsage = process.cpuUsage();
      
      // Auto-registrar
      this.aggregators.system.memory = memUsage;
      this.aggregators.system.cpu = cpuUsage;
      
    }, 5000);
  }

  /**
   * Cria um span de tracing
   */
  startSpan(name, attributes = {}) {
    if (!this.tracer) return null;
    
    return this.tracer.startSpan(name, {
      attributes: {
        'digimundo.component': attributes.component || 'unknown',
        ...attributes
      }
    });
  }

  /**
   * Obtém dashboard de métricas
   */
  getDashboard() {
    const avgLatency = this.aggregators.system.latency.length > 0
      ? this.aggregators.system.latency.reduce((a, b) => a + b, 0) / this.aggregators.system.latency.length
      : 0;
    
    return {
      consciousness: {
        level: this.calculateConsciousnessLevel(),
        ...this.aggregators.consciousness
      },
      system: {
        ...this.aggregators.system,
        avgLatency: avgLatency.toFixed(2) + 'ms',
        uptime: process.uptime(),
        memory: process.memoryUsage()
      },
      digimons: {
        active: this.aggregators.digimons.size,
        list: Array.from(this.aggregators.digimons.entries()).map(([name, data]) => ({
          name,
          ...data
        }))
      },
      components: Array.from(this.components.keys())
    };
  }

  /**
   * Exporta métricas em formato Prometheus
   */
  async exportPrometheus() {
    // Já está sendo exportado automaticamente na porta configurada
    return `http://localhost:${this.config.metricsPort}/metrics`;
  }

  /**
   * Emit helper (para EventEmitter)
   */
  emit(event, data) {
    // Placeholder - integraria com EventEmitter real
    console.log(`📊 Evento: ${event}`, data);
  }
}

// Singleton global
let globalMetrics = null;

/**
 * Obtém instância global de métricas
 */
function getMetrics(config = {}) {
  if (!globalMetrics) {
    globalMetrics = new UnifiedMetrics(config);
  }
  return globalMetrics;
}

// Auto-inicializar se executado diretamente
if (require.main === module) {
  (async () => {
    console.log('🧪 TESTANDO SISTEMA DE MÉTRICAS UNIFICADAS\\n');
    
    const metrics = getMetrics({
      serviceName: 'digimundo-test',
      metricsPort: 9090
    });
    
    await metrics.initialize();
    
    // Simular atividade
    console.log('\\n📈 Simulando atividade do sistema...');
    
    // Registrar Digimons
    metrics.aggregators.digimons.set('sabiamon', {
      consciousnessLevel: 0.8,
      evolutionProgress: 75,
      thoughts: 100,
      memories: 500
    });
    
    metrics.aggregators.digimons.set('neuromon', {
      consciousnessLevel: 0.7,
      evolutionProgress: 60,
      thoughts: 80,
      memories: 400
    });
    
    // Simular eventos
    for (let i = 0; i < 10; i++) {
      metrics.recordThought({ source: 'sabiamon' });
      metrics.recordEmotion({ source: 'neuromon', intensity: Math.random() });
      metrics.recordMemoryOperation('store', { type: 'episodic' });
      metrics.recordAPILatency('/api/chat', Math.random() * 100);
      metrics.recordNATSMessage('thought_shared');
    }
    
    metrics.recordInsight({ source: 'collective', novelty: 0.9 });
    metrics.recordEvolution('sabiamon', 'ultimate');
    
    // Mostrar dashboard
    console.log('\\n📊 Dashboard de Métricas:');
    console.log(JSON.stringify(metrics.getDashboard(), null, 2));
    
    console.log(`\\n🎯 Métricas Prometheus disponíveis em: ${await metrics.exportPrometheus()}`);
    
    console.log('\\n✨ Sistema de métricas rodando. Ctrl+C para parar.');
  })();
}

module.exports = { UnifiedMetrics, getMetrics };