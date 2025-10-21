/**
 * 🚀 SISTEMA DE CACHE REDIS PARA PRODUÇÃO
 * Cache inteligente para otimização de performance
 */

import Redis from 'redis'
import crypto from 'crypto'

class ProductionCacheSystem {
  constructor() {
    this.redis = null
    this.isConnected = false
    this.stats = {
      hits: 0,
      misses: 0,
      sets: 0,
      errors: 0
    }
    this.defaultTTL = parseInt(process.env.CACHE_TTL) || 300 // 5 minutes
  }

  async initialize() {
    try {
      this.redis = Redis.createClient({
        url: process.env.REDIS_URL || 'redis://localhost:6379',
        retry_strategy: (options) => {
          if (options.error && options.error.code === 'ECONNREFUSED') {
            return new Error('Redis server refused connection')
          }
          if (options.times_connected > 10) {
            return undefined
          }
          return Math.min(options.attempt * 100, 3000)
        }
      })

      this.redis.on('error', (err) => {
        this.stats.errors++
        if (process.env.LOG_LEVEL !== 'error') {
          console.error('Redis Error:', err)
        }
      })

      this.redis.on('connect', () => {
        this.isConnected = true
        if (process.env.LOG_LEVEL !== 'error') {
          console.log('✅ Redis Cache conectado')
        }
      })

      this.redis.on('disconnect', () => {
        this.isConnected = false
      })

      await this.redis.connect()
      return true
    } catch (error) {
      console.error('❌ Erro ao inicializar Redis Cache:', error)
      return false
    }
  }

  generateKey(prefix, data) {
    const hash = crypto.createHash('md5').update(JSON.stringify(data)).digest('hex')
    return `digimundo:${prefix}:${hash}`
  }

  async get(key) {
    if (!this.isConnected) return null

    try {
      const result = await this.redis.get(key)
      if (result) {
        this.stats.hits++
        return JSON.parse(result)
      } else {
        this.stats.misses++
        return null
      }
    } catch (error) {
      this.stats.errors++
      return null
    }
  }

  async set(key, value, ttl = this.defaultTTL) {
    if (!this.isConnected) return false

    try {
      await this.redis.setEx(key, ttl, JSON.stringify(value))
      this.stats.sets++
      return true
    } catch (error) {
      this.stats.errors++
      return false
    }
  }

  async delete(key) {
    if (!this.isConnected) return false

    try {
      await this.redis.del(key)
      return true
    } catch (error) {
      this.stats.errors++
      return false
    }
  }

  async flush() {
    if (!this.isConnected) return false

    try {
      await this.redis.flushAll()
      return true
    } catch (error) {
      this.stats.errors++
      return false
    }
  }

  // Cache específico para respostas de API
  async cacheAPIResponse(endpoint, params, response, ttl = 300) {
    const key = this.generateKey('api', { endpoint, params })
    return await this.set(key, response, ttl)
  }

  async getCachedAPIResponse(endpoint, params) {
    const key = this.generateKey('api', { endpoint, params })
    return await this.get(key)
  }

  // Cache para embeddings de IA
  async cacheEmbedding(text, embedding, ttl = 3600) {
    const key = this.generateKey('embedding', { text })
    return await this.set(key, embedding, ttl)
  }

  async getCachedEmbedding(text) {
    const key = this.generateKey('embedding', { text })
    return await this.get(key)
  }

  // Session storage
  async setSession(sessionId, data, ttl = 86400) { // 24h
    const key = `digimundo:session:${sessionId}`
    return await this.set(key, data, ttl)
  }

  async getSession(sessionId) {
    const key = `digimundo:session:${sessionId}`
    return await this.get(key)
  }

  async deleteSession(sessionId) {
    const key = `digimundo:session:${sessionId}`
    return await this.delete(key)
  }

  // Cache para modelos de IA
  async cacheModelResponse(modelId, prompt, response, ttl = 600) {
    const key = this.generateKey('model', { modelId, prompt })
    return await this.set(key, response, ttl)
  }

  async getCachedModelResponse(modelId, prompt) {
    const key = this.generateKey('model', { modelId, prompt })
    return await this.get(key)
  }

  // Cache para dados de Digimons
  async cacheDigimonData(digimonId, data, ttl = 1800) { // 30min
    const key = `digimundo:digimon:${digimonId}`
    return await this.set(key, data, ttl)
  }

  async getCachedDigimonData(digimonId) {
    const key = `digimundo:digimon:${digimonId}`
    return await this.get(key)
  }

  // Estatísticas do cache
  getStats() {
    const hitRate = this.stats.hits + this.stats.misses > 0 
      ? (this.stats.hits / (this.stats.hits + this.stats.misses) * 100).toFixed(2)
      : 0

    return {
      connected: this.isConnected,
      hitRate: `${hitRate}%`,
      ...this.stats,
      timestamp: new Date().toISOString()
    }
  }

  // Middleware para Express
  middleware() {
    return async (req, res, next) => {
      // Skip cache para métodos que modificam dados
      if (!['GET', 'HEAD'].includes(req.method)) {
        return next()
      }

      const cacheKey = this.generateKey('route', {
        path: req.path,
        query: req.query,
        user: req.user?.id
      })

      try {
        const cached = await this.get(cacheKey)
        if (cached) {
          res.set('X-Cache', 'HIT')
          return res.json(cached)
        }

        // Override res.json para cachear automaticamente
        const originalJson = res.json
        res.json = function(data) {
          // Cache apenas respostas de sucesso
          if (res.statusCode >= 200 && res.statusCode < 300) {
            cacheSystem.set(cacheKey, data, 300) // 5min cache
          }
          res.set('X-Cache', 'MISS')
          return originalJson.call(this, data)
        }

        next()
      } catch (error) {
        // Se cache falhar, continua sem cache
        next()
      }
    }
  }

  async healthCheck() {
    if (!this.isConnected) return { status: 'down', error: 'Not connected' }

    try {
      await this.redis.ping()
      return { 
        status: 'up', 
        stats: this.getStats(),
        memory: await this.redis.memory('usage') || 'unknown'
      }
    } catch (error) {
      return { status: 'down', error: error.message }
    }
  }
}

// Singleton instance
let cacheInstance = null

export function getCacheSystem() {
  if (!cacheInstance) {
    cacheInstance = new ProductionCacheSystem()
  }
  return cacheInstance
}

export const cacheSystem = getCacheSystem()
export default cacheSystem