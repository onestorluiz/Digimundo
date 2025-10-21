/**
 * 🛡️ SISTEMA DE SEGURANÇA PARA PRODUÇÃO
 * Implementação completa de segurança para o Digimundo
 */

import helmet from 'helmet'
import rateLimit from 'express-rate-limit'
import Joi from 'joi'
import cors from 'cors'
import compression from 'compression'

class SecuritySystem {
  constructor() {
    this.rateLimitStore = new Map()
    this.suspiciousIPs = new Set()
    this.blockedIPs = new Set()
  }

  // Configuração do Helmet
  getHelmetConfig() {
    return helmet({
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          scriptSrc: ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
          imgSrc: ["'self'", "data:", "blob:"],
          connectSrc: ["'self'", "ws:", "wss:"],
          fontSrc: ["'self'"],
          frameSrc: ["'self'"],
          mediaSrc: ["'self'"],
          objectSrc: ["'none'"],
          baseUri: ["'self'"],
          formAction: ["'self'"],
          frameAncestors: ["'none'"],
          upgradeInsecureRequests: []
        },
        reportOnly: false
      },
      crossOriginEmbedderPolicy: false,
      crossOriginOpenerPolicy: { policy: "same-origin-allow-popups" },
      crossOriginResourcePolicy: { policy: "cross-origin" },
      dnsPrefetchControl: { allow: false },
      frameguard: { action: 'deny' },
      hidePoweredBy: true,
      hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
      },
      ieNoOpen: true,
      noSniff: true,
      originAgentCluster: true,
      permittedCrossDomainPolicies: false,
      referrerPolicy: { policy: "no-referrer" },
      xssFilter: true
    })
  }

  // Rate Limiting avançado
  createRateLimiters() {
    const limiters = {
      // Rate limit geral
      general: rateLimit({
        windowMs: 15 * 60 * 1000, // 15 minutos
        max: 1000, // máximo 1000 requests por IP
        message: {
          error: 'Muitas requisições, tente novamente em 15 minutos',
          code: 'RATE_LIMIT_EXCEEDED'
        },
        standardHeaders: true,
        legacyHeaders: false,
        handler: (req, res) => {
          this.suspiciousIPs.add(req.ip)
          res.status(429).json({
            error: 'Rate limit exceeded',
            retryAfter: Math.round(req.rateLimit.resetTime / 1000)
          })
        }
      }),

      // Rate limit para APIs de IA (mais restritivo)
      aiAPI: rateLimit({
        windowMs: 5 * 60 * 1000, // 5 minutos
        max: 100, // máximo 100 requests por IP
        message: {
          error: 'Limite de uso da API de IA excedido',
          code: 'AI_RATE_LIMIT_EXCEEDED'
        },
        keyGenerator: (req) => {
          return req.user?.id || req.ip
        }
      }),

      // Rate limit para autenticação
      auth: rateLimit({
        windowMs: 15 * 60 * 1000, // 15 minutos
        max: 5, // máximo 5 tentativas por IP
        skipSuccessfulRequests: true,
        handler: (req, res) => {
          this.suspiciousIPs.add(req.ip)
          res.status(429).json({
            error: 'Muitas tentativas de login, aguarde 15 minutos',
            code: 'AUTH_RATE_LIMIT_EXCEEDED'
          })
        }
      }),

      // Rate limit para WebSocket
      websocket: rateLimit({
        windowMs: 1 * 60 * 1000, // 1 minuto
        max: 60, // máximo 60 conexões por minuto
        message: 'Limite de conexões WebSocket excedido'
      })
    }

    return limiters
  }

  // CORS configurado corretamente
  getCorsConfig() {
    const allowedOrigins = [
      'http://localhost:7937',
      'http://127.0.0.1:7937',
      'file://',
      'app://'
    ]

    // Em produção, adicionar domínios específicos
    if (process.env.NODE_ENV === 'production') {
      if (process.env.ALLOWED_ORIGINS) {
        allowedOrigins.push(...process.env.ALLOWED_ORIGINS.split(','))
      }
    }

    return cors({
      origin: function (origin, callback) {
        // Permitir requests sem origin (mobile apps, Electron, etc.)
        if (!origin) return callback(null, true)
        
        if (allowedOrigins.includes(origin) || origin.startsWith('file://')) {
          return callback(null, true)
        }
        
        const error = new Error('Bloqueado por política CORS')
        error.status = 403
        callback(error)
      },
      credentials: true,
      methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
      allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
      exposedHeaders: ['X-Cache', 'X-RateLimit-Remaining', 'X-Response-Time']
    })
  }

  // Compressão Gzip
  getCompressionConfig() {
    return compression({
      level: 6,
      threshold: 1024,
      filter: (req, res) => {
        if (req.headers['x-no-compression']) {
          return false
        }
        return compression.filter(req, res)
      }
    })
  }

  // Schemas de validação Joi
  getValidationSchemas() {
    return {
      // Login
      login: Joi.object({
        username: Joi.string().alphanum().min(3).max(30).required(),
        password: Joi.string().min(6).max(128).required()
      }),

      // Registro
      register: Joi.object({
        username: Joi.string().alphanum().min(3).max(30).required(),
        password: Joi.string().min(6).max(128).required(),
        role: Joi.string().valid('user', 'admin').default('user')
      }),

      // Prompt para IA
      aiPrompt: Joi.object({
        prompt: Joi.string().min(1).max(10000).required(),
        context: Joi.string().max(5000).optional(),
        source: Joi.string().max(100).optional(),
        model: Joi.string().max(100).optional()
      }),

      // Interação com Digimon
      digimonInteraction: Joi.object({
        digimon: Joi.string().min(1).max(50).required(),
        message: Joi.string().min(1).max(1000).required(),
        type: Joi.string().valid('question', 'command', 'conversation').default('conversation')
      }),

      // Treinamento de IA
      aiTraining: Joi.object({
        digimonName: Joi.string().min(1).max(50).required(),
        personalityData: Joi.object().required(),
        baseModel: Joi.string().max(100).optional()
      })
    }
  }

  // Middleware de validação
  validate(schema) {
    return (req, res, next) => {
      const { error, value } = schema.validate(req.body, {
        abortEarly: false,
        stripUnknown: true
      })

      if (error) {
        const errors = error.details.map(detail => ({
          field: detail.path.join('.'),
          message: detail.message,
          value: detail.context?.value
        }))

        return res.status(400).json({
          error: 'Dados de entrada inválidos',
          details: errors,
          code: 'VALIDATION_ERROR'
        })
      }

      req.validatedBody = value
      next()
    }
  }

  // Middleware anti-bruteforce
  antiBruteForce() {
    return (req, res, next) => {
      const ip = req.ip
      const key = `bf:${ip}`
      
      if (this.blockedIPs.has(ip)) {
        return res.status(403).json({
          error: 'IP bloqueado por atividade suspeita',
          code: 'IP_BLOCKED'
        })
      }

      // Contar tentativas falhadas
      if (req.path.includes('/auth/login') && req.method === 'POST') {
        res.on('finish', () => {
          if (res.statusCode === 401) {
            const attempts = (this.rateLimitStore.get(key) || 0) + 1
            this.rateLimitStore.set(key, attempts)
            
            // Bloquear após 10 tentativas falhadas
            if (attempts >= 10) {
              this.blockedIPs.add(ip)
              console.warn(`🚨 IP ${ip} bloqueado por tentativas de força bruta`)
            }
          } else if (res.statusCode === 200) {
            // Limpar contador em login bem-sucedido
            this.rateLimitStore.delete(key)
          }
        })
      }

      next()
    }
  }

  // Middleware de sanitização
  sanitizeInput() {
    return (req, res, next) => {
      // Função recursiva para sanitizar objetos
      const sanitize = (obj) => {
        if (typeof obj === 'string') {
          return obj
            .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
            .replace(/javascript:/gi, '')
            .replace(/on\w+\s*=\s*["'][^"']*["']/gi, '')
            .trim()
        }
        
        if (typeof obj === 'object' && obj !== null) {
          const sanitized = {}
          for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
              sanitized[key] = sanitize(obj[key])
            }
          }
          return sanitized
        }
        
        return obj
      }

      if (req.body) {
        req.body = sanitize(req.body)
      }
      
      if (req.query) {
        req.query = sanitize(req.query)
      }

      next()
    }
  }

  // Middleware de logging de segurança
  securityLogger() {
    return (req, res, next) => {
      const startTime = Date.now()
      
      res.on('finish', () => {
        const duration = Date.now() - startTime
        const logData = {
          timestamp: new Date().toISOString(),
          ip: req.ip,
          method: req.method,
          url: req.url,
          userAgent: req.get('User-Agent'),
          statusCode: res.statusCode,
          duration,
          user: req.user?.id || 'anonymous'
        }

        // Log eventos suspeitos
        if (res.statusCode === 401 || res.statusCode === 403 || res.statusCode === 429) {
          console.warn('🚨 Evento de segurança:', logData)
        }

        // Log requests lentos
        if (duration > 5000) {
          console.warn('⏱️ Request lento:', logData)
        }
      })

      next()
    }
  }

  // Obter todos os middlewares configurados
  getAllMiddlewares() {
    const schemas = this.getValidationSchemas()
    const limiters = this.createRateLimiters()

    return {
      helmet: this.getHelmetConfig(),
      cors: this.getCorsConfig(),
      compression: this.getCompressionConfig(),
      rateLimiters: limiters,
      validation: {
        login: this.validate(schemas.login),
        register: this.validate(schemas.register),
        aiPrompt: this.validate(schemas.aiPrompt),
        digimonInteraction: this.validate(schemas.digimonInteraction),
        aiTraining: this.validate(schemas.aiTraining)
      },
      security: {
        antiBruteForce: this.antiBruteForce(),
        sanitizeInput: this.sanitizeInput(),
        securityLogger: this.securityLogger()
      }
    }
  }

  // Status de segurança
  getSecurityStatus() {
    return {
      blockedIPs: Array.from(this.blockedIPs),
      suspiciousIPs: Array.from(this.suspiciousIPs),
      rateLimitAttempts: this.rateLimitStore.size,
      securityLevel: 'high',
      timestamp: new Date().toISOString()
    }
  }
}

// Singleton
let securityInstance = null

export function getSecuritySystem() {
  if (!securityInstance) {
    securityInstance = new SecuritySystem()
  }
  return securityInstance
}

export const securitySystem = getSecuritySystem()
export default securitySystem