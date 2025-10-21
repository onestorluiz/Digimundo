/**
 * 🔬 SERVIDOR DE MÉTRICAS PROMETHEUS
 * Monitoramento profissional para produção
 */

import express from 'express'
import client from 'prom-client'
import os from 'os'
import process from 'process'

class MetricsServer {
  constructor() {
    this.app = express()
    this.register = new client.Registry()
    this.collectDefaultMetrics = client.collectDefaultMetrics
    this.setupMetrics()
  }

  setupMetrics() {
    // Coletar métricas padrão do Node.js
    this.collectDefaultMetrics({ 
      register: this.register,
      prefix: 'digimundo_',
      timeout: 10000
    })

    // Métricas customizadas do Digimundo
    this.httpRequestDuration = new client.Histogram({
      name: 'digimundo_http_request_duration_seconds',
      help: 'Duration of HTTP requests in seconds',
      labelNames: ['method', 'route', 'status_code'],
      buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10]
    })

    this.httpRequestTotal = new client.Counter({
      name: 'digimundo_http_requests_total',
      help: 'Total number of HTTP requests',
      labelNames: ['method', 'route', 'status_code']
    })

    this.aiModelInferences = new client.Counter({
      name: 'digimundo_ai_model_inferences_total',
      help: 'Total number of AI model inferences',
      labelNames: ['model', 'type', 'status']
    })

    this.aiModelLatency = new client.Histogram({
      name: 'digimundo_ai_model_latency_seconds',
      help: 'AI model inference latency in seconds',
      labelNames: ['model', 'type'],
      buckets: [0.1, 0.5, 1, 2, 5, 10, 30, 60]
    })

    this.cacheOperations = new client.Counter({
      name: 'digimundo_cache_operations_total',
      help: 'Total cache operations',
      labelNames: ['operation', 'result']
    })

    this.cacheHitRate = new client.Gauge({
      name: 'digimundo_cache_hit_rate',
      help: 'Cache hit rate percentage'
    })

    this.activeDigimons = new client.Gauge({
      name: 'digimundo_active_digimons',
      help: 'Number of active Digimons in the system'
    })

    this.memoryUsage = new client.Gauge({
      name: 'digimundo_memory_usage_bytes',
      help: 'Memory usage in bytes',
      labelNames: ['type']
    })

    this.cpuUsage = new client.Gauge({
      name: 'digimundo_cpu_usage_percent',
      help: 'CPU usage percentage'
    })

    this.websocketConnections = new client.Gauge({
      name: 'digimundo_websocket_connections',
      help: 'Number of active WebSocket connections'
    })

    this.errorRate = new client.Counter({
      name: 'digimundo_errors_total',
      help: 'Total number of errors',
      labelNames: ['type', 'component']
    })

    // Registrar todas as métricas
    this.register.registerMetric(this.httpRequestDuration)
    this.register.registerMetric(this.httpRequestTotal)
    this.register.registerMetric(this.aiModelInferences)
    this.register.registerMetric(this.aiModelLatency)
    this.register.registerMetric(this.cacheOperations)
    this.register.registerMetric(this.cacheHitRate)
    this.register.registerMetric(this.activeDigimons)
    this.register.registerMetric(this.memoryUsage)
    this.register.registerMetric(this.cpuUsage)
    this.register.registerMetric(this.websocketConnections)
    this.register.registerMetric(this.errorRate)
  }

  setupRoutes() {
    // Endpoint principal do Prometheus
    this.app.get('/metrics', async (req, res) => {
      res.set('Content-Type', this.register.contentType)
      res.end(await this.register.metrics())
    })

    // Health check específico para métricas
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'healthy',
        uptime: process.uptime(),
        timestamp: new Date().toISOString(),
        metrics_collected: this.register.getMetricsAsJSON().length
      })
    })

    // Status detalhado do sistema
    this.app.get('/status', (req, res) => {
      const memUsage = process.memoryUsage()
      const cpuUsage = os.loadavg()

      res.json({
        system: {
          platform: os.platform(),
          arch: os.arch(),
          nodeVersion: process.version,
          uptime: process.uptime(),
          hostname: os.hostname()
        },
        memory: {
          rss: memUsage.rss,
          heapTotal: memUsage.heapTotal,
          heapUsed: memUsage.heapUsed,
          external: memUsage.external,
          arrayBuffers: memUsage.arrayBuffers,
          free: os.freemem(),
          total: os.totalmem(),
          usage_percent: ((os.totalmem() - os.freemem()) / os.totalmem() * 100).toFixed(2)
        },
        cpu: {
          cores: os.cpus().length,
          load: cpuUsage,
          model: os.cpus()[0]?.model || 'unknown'
        },
        process: {
          pid: process.pid,
          ppid: process.ppid,
          title: process.title,
          argv: process.argv,
          env: {
            node_env: process.env.NODE_ENV,
            port: process.env.METRICS_PORT
          }
        }
      })
    })
  }

  // Atualizar métricas do sistema periodicamente
  startSystemMetricsCollection() {
    setInterval(() => {
      const memUsage = process.memoryUsage()
      
      // Atualizar métricas de memória
      this.memoryUsage.set({ type: 'rss' }, memUsage.rss)
      this.memoryUsage.set({ type: 'heap_total' }, memUsage.heapTotal)
      this.memoryUsage.set({ type: 'heap_used' }, memUsage.heapUsed)
      this.memoryUsage.set({ type: 'external' }, memUsage.external)

      // CPU usage (aproximado usando load average)
      const loadAvg = os.loadavg()[0] / os.cpus().length * 100
      this.cpuUsage.set(Math.min(100, loadAvg))

    }, 5000) // A cada 5 segundos
  }

  // Middleware para coletar métricas HTTP
  httpMetricsMiddleware() {
    return (req, res, next) => {
      const start = Date.now()
      
      res.on('finish', () => {
        const duration = (Date.now() - start) / 1000
        const labels = {
          method: req.method,
          route: req.route?.path || req.path,
          status_code: res.statusCode
        }

        this.httpRequestDuration.observe(labels, duration)
        this.httpRequestTotal.inc(labels)
      })

      next()
    }
  }

  // Métodos para registrar métricas específicas do Digimundo
  recordAIInference(model, type, duration, success = true) {
    this.aiModelInferences.inc({
      model,
      type,
      status: success ? 'success' : 'error'
    })

    if (success) {
      this.aiModelLatency.observe({ model, type }, duration)
    }
  }

  recordCacheOperation(operation, result) {
    this.cacheOperations.inc({ operation, result })
  }

  updateCacheHitRate(rate) {
    this.cacheHitRate.set(rate)
  }

  updateActiveDigimons(count) {
    this.activeDigimons.set(count)
  }

  updateWebSocketConnections(count) {
    this.websocketConnections.set(count)
  }

  recordError(type, component) {
    this.errorRate.inc({ type, component })
  }

  start(port = 9090) {
    this.setupRoutes()
    this.startSystemMetricsCollection()

    this.app.listen(port, '0.0.0.0', () => {
      console.log(`📊 Servidor de Métricas rodando na porta ${port}`)
      console.log(`📊 Métricas disponíveis em http://localhost:${port}/metrics`)
      console.log(`📊 Status do sistema em http://localhost:${port}/status`)
    })
  }
}

// Singleton instance
let metricsInstance = null

export function getMetricsServer() {
  if (!metricsInstance) {
    metricsInstance = new MetricsServer()
  }
  return metricsInstance
}

// Iniciar se executado diretamente
if (import.meta.url === `file://${process.argv[1]}`) {
  const metricsServer = getMetricsServer()
  const port = process.env.METRICS_PORT || 9090
  metricsServer.start(port)
}

export default getMetricsServer