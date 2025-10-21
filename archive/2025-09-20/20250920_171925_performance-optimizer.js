/**
 * ⚡ OTIMIZADOR DE PERFORMANCE PARA PRODUÇÃO
 * Sistema completo de otimização para máxima performance
 */

import { promisify } from 'util'
import { pipeline } from 'stream'
import { createReadStream, createWriteStream } from 'fs'
import { gzip, gunzip } from 'zlib'
import cluster from 'cluster'
import os from 'os'

class PerformanceOptimizer {
  constructor() {
    this.connectionPools = new Map()
    this.streamCache = new Map()
    this.performanceMetrics = {
      requests: 0,
      avgResponseTime: 0,
      errors: 0,
      startTime: Date.now()
    }
  }

  // Connection Pooling para Database
  createConnectionPool(config = {}) {
    const defaultConfig = {
      min: 2,
      max: parseInt(process.env.CONNECTION_POOL_SIZE) || 20,
      acquireTimeoutMillis: 30000,
      idleTimeoutMillis: 30000,
      reapIntervalMillis: 1000,
      createRetryIntervalMillis: 200,
      createTimeoutMillis: 30000
    }

    const poolConfig = { ...defaultConfig, ...config }
    
    // Pool para SQLite (simulado - em produção usar pool real)
    const pool = {
      config: poolConfig,
      connections: [],
      available: [],
      pending: [],
      
      async acquire() {
        if (this.available.length > 0) {
          return this.available.pop()
        }
        
        if (this.connections.length < poolConfig.max) {
          const connection = await this.createConnection()
          this.connections.push(connection)
          return connection
        }
        
        // Aguardar conexão disponível
        return new Promise((resolve) => {
          this.pending.push(resolve)
        })
      },
      
      release(connection) {
        if (this.pending.length > 0) {
          const resolve = this.pending.shift()
          resolve(connection)
        } else {
          this.available.push(connection)
        }
      },
      
      async createConnection() {
        // Simulação - em produção implementar conexão real
        return {
          id: Math.random().toString(36),
          createdAt: Date.now(),
          query: async (sql, params) => {
            // Simulação de query
            await new Promise(resolve => setTimeout(resolve, Math.random() * 100))
            return { rows: [], meta: {} }
          }
        }
      },
      
      async destroy() {
        this.connections.forEach(conn => {
          // Fechar conexões
        })
        this.connections = []
        this.available = []
        this.pending = []
      }
    }

    this.connectionPools.set('default', pool)
    return pool
  }

  // Stream Processing para dados grandes
  createStreamProcessor() {
    const pipelineAsync = promisify(pipeline)
    
    return {
      // Processar arquivo com streams
      async processLargeFile(inputPath, outputPath, transform) {
        const readStream = createReadStream(inputPath, { highWaterMark: 64 * 1024 })
        const writeStream = createWriteStream(outputPath)
        const gzipStream = gzip()
        
        await pipelineAsync(
          readStream,
          transform,
          gzipStream,
          writeStream
        )
      },
      
      // Stream de compressão
      createCompressionStream() {
        return gzip({
          level: 6,
          chunkSize: 32 * 1024,
          windowBits: 15,
          memLevel: 8
        })
      },
      
      // Stream de descompressão
      createDecompressionStream() {
        return gunzip({
          chunkSize: 32 * 1024
        })
      },
      
      // Processor de dados de IA em streaming
      async processAIDataStream(dataStream, processor) {
        const chunks = []
        
        for await (const chunk of dataStream) {
          try {
            const processed = await processor(chunk)
            chunks.push(processed)
            
            // Liberar memória a cada 1000 chunks
            if (chunks.length % 1000 === 0) {
              global.gc && global.gc()
            }
          } catch (error) {
            console.error('Erro no processamento de chunk:', error)
          }
        }
        
        return chunks
      }
    }
  }

  // Auto-scaling baseado em CPU e memória
  setupAutoScaling() {
    if (!cluster.isPrimary) return

    const cpuThreshold = parseInt(process.env.CPU_THRESHOLD) || 70
    const memoryThreshold = parseInt(process.env.MEMORY_THRESHOLD) || 80
    const maxWorkers = os.cpus().length * 2
    let workers = []

    // Iniciar workers iniciais
    const initialWorkers = Math.min(4, os.cpus().length)
    for (let i = 0; i < initialWorkers; i++) {
      const worker = cluster.fork()
      workers.push(worker)
    }

    // Monitorar e ajustar workers
    setInterval(() => {
      const metrics = this.getSystemMetrics()
      
      if (metrics.cpu > cpuThreshold || metrics.memory > memoryThreshold) {
        // Escalar para cima
        if (workers.length < maxWorkers) {
          const worker = cluster.fork()
          workers.push(worker)
          console.log(`📈 Scaling UP: ${workers.length} workers (CPU: ${metrics.cpu}%, MEM: ${metrics.memory}%)`)
        }
      } else if (metrics.cpu < cpuThreshold * 0.5 && metrics.memory < memoryThreshold * 0.5) {
        // Escalar para baixo
        if (workers.length > 2) {
          const worker = workers.pop()
          worker.kill()
          console.log(`📉 Scaling DOWN: ${workers.length} workers (CPU: ${metrics.cpu}%, MEM: ${metrics.memory}%)`)
        }
      }
    }, 30000) // Verificar a cada 30 segundos

    // Substituir workers que morrerem
    cluster.on('exit', (worker, code, signal) => {
      console.log(`💀 Worker ${worker.process.pid} morreu. Reiniciando...`)
      const newWorker = cluster.fork()
      const index = workers.indexOf(worker)
      if (index > -1) {
        workers[index] = newWorker
      }
    })

    return workers
  }

  // Métricas do sistema
  getSystemMetrics() {
    const memUsage = process.memoryUsage()
    const loadAvg = os.loadavg()
    const totalMem = os.totalmem()
    const freeMem = os.freemem()

    return {
      cpu: (loadAvg[0] / os.cpus().length * 100).toFixed(2),
      memory: ((totalMem - freeMem) / totalMem * 100).toFixed(2),
      heap: {
        used: memUsage.heapUsed,
        total: memUsage.heapTotal,
        percentage: (memUsage.heapUsed / memUsage.heapTotal * 100).toFixed(2)
      },
      uptime: process.uptime(),
      loadAverage: loadAvg,
      timestamp: Date.now()
    }
  }

  // Middleware de performance
  performanceMiddleware() {
    return (req, res, next) => {
      const startTime = process.hrtime.bigint()
      
      // Otimizações por rota
      if (req.path.includes('/api/')) {
        res.set('Cache-Control', 'public, max-age=300') // 5min cache
      }
      
      if (req.path.includes('/static/')) {
        res.set('Cache-Control', 'public, max-age=31536000') // 1 ano
      }

      // Headers de performance
      res.set('X-DNS-Prefetch-Control', 'on')
      res.set('X-Preconnect', 'on')

      res.on('finish', () => {
        const endTime = process.hrtime.bigint()
        const duration = Number(endTime - startTime) / 1000000 // ms
        
        // Atualizar métricas
        this.performanceMetrics.requests++
        this.performanceMetrics.avgResponseTime = 
          (this.performanceMetrics.avgResponseTime + duration) / 2

        // Headers de debug
        res.set('X-Response-Time', `${duration.toFixed(2)}ms`)
        res.set('X-Worker-PID', process.pid.toString())

        // Log requests lentos
        if (duration > 1000) {
          console.warn(`🐌 Slow request: ${req.method} ${req.path} - ${duration.toFixed(2)}ms`)
        }
      })

      next()
    }
  }

  // Memory optimization
  optimizeMemory() {
    // Garbage collection otimizado
    if (global.gc) {
      setInterval(() => {
        global.gc()
      }, 60000) // A cada minuto
    }

    // Limpar caches antigos
    setInterval(() => {
      this.streamCache.clear()
    }, 300000) // A cada 5 minutos

    // Monitorar vazamentos de memória
    setInterval(() => {
      const usage = process.memoryUsage()
      if (usage.heapUsed > 500 * 1024 * 1024) { // 500MB
        console.warn('⚠️ High memory usage detected:', {
          heapUsed: `${Math.round(usage.heapUsed / 1024 / 1024)}MB`,
          heapTotal: `${Math.round(usage.heapTotal / 1024 / 1024)}MB`,
          external: `${Math.round(usage.external / 1024 / 1024)}MB`
        })
      }
    }, 30000)
  }

  // CPU optimization
  optimizeCPU() {
    // Processamento assíncrono para tarefas pesadas
    const heavyTaskQueue = []
    
    const processHeavyTasks = async () => {
      while (heavyTaskQueue.length > 0) {
        const task = heavyTaskQueue.shift()
        try {
          await task()
        } catch (error) {
          console.error('Erro em tarefa pesada:', error)
        }
        
        // Yield para outras operações
        await new Promise(resolve => setImmediate(resolve))
      }
    }

    setInterval(processHeavyTasks, 100)

    return {
      queueHeavyTask: (task) => {
        heavyTaskQueue.push(task)
      }
    }
  }

  // Health check avançado
  async healthCheck() {
    const metrics = this.getSystemMetrics()
    const pools = Array.from(this.connectionPools.entries())
    
    const health = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      metrics,
      performance: this.performanceMetrics,
      connectionPools: pools.map(([name, pool]) => ({
        name,
        active: pool.connections.length,
        available: pool.available.length,
        pending: pool.pending.length
      })),
      workers: cluster.workers ? Object.keys(cluster.workers).length : 1
    }

    // Verificar se está saudável
    if (metrics.cpu > 90 || metrics.memory > 95) {
      health.status = 'critical'
    } else if (metrics.cpu > 70 || metrics.memory > 80) {
      health.status = 'warning'
    }

    return health
  }

  // Inicializar todas as otimizações
  async initialize() {
    console.log('⚡ Inicializando otimizador de performance...')
    
    this.createConnectionPool()
    this.optimizeMemory()
    this.optimizeCPU()
    
    if (cluster.isPrimary && process.env.AUTO_SCALING === 'true') {
      this.setupAutoScaling()
    }

    console.log('✅ Otimizador de performance inicializado')
  }

  // Relatório de performance
  getPerformanceReport() {
    const uptime = process.uptime()
    const metrics = this.getSystemMetrics()
    
    return {
      uptime: `${Math.floor(uptime / 3600)}h ${Math.floor((uptime % 3600) / 60)}m`,
      requests: this.performanceMetrics.requests,
      avgResponseTime: `${this.performanceMetrics.avgResponseTime.toFixed(2)}ms`,
      requestsPerSecond: (this.performanceMetrics.requests / uptime).toFixed(2),
      errorRate: `${(this.performanceMetrics.errors / this.performanceMetrics.requests * 100).toFixed(2)}%`,
      systemMetrics: metrics,
      optimizations: {
        connectionPooling: 'enabled',
        streamProcessing: 'enabled',
        memoryOptimization: 'enabled',
        cpuOptimization: 'enabled',
        autoScaling: process.env.AUTO_SCALING === 'true' ? 'enabled' : 'disabled'
      }
    }
  }
}

// Singleton
let optimizerInstance = null

export function getPerformanceOptimizer() {
  if (!optimizerInstance) {
    optimizerInstance = new PerformanceOptimizer()
  }
  return optimizerInstance
}

export const performanceOptimizer = getPerformanceOptimizer()
export default performanceOptimizer