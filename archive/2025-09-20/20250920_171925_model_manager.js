/**
 * 🤖 MODEL MANAGER - Gerenciador de Modelos de IA
 * Gerencia modelos Ollama e outros sistemas de IA
 */

import { EventEmitter } from 'events'

export class ModelManager extends EventEmitter {
  constructor() {
    super()
    this.name = 'ModelManager'
    this.availableModels = new Map()
    this.activeModel = null
    this.isInitialized = false
  }

  async initialize() {
    console.log('🤖 [ModelManager] Inicializando gerenciador de modelos...')
    
    // Modelos padrão
    this.availableModels.set('llama3.2:latest', {
      name: 'llama3.2:latest',
      type: 'ollama',
      size: '3B',
      status: 'available'
    })
    
    this.availableModels.set('claude-3-sonnet', {
      name: 'claude-3-sonnet',
      type: 'claude',
      provider: 'anthropic',
      status: 'available'
    })

    this.activeModel = 'llama3.2:latest'
    this.isInitialized = true
    
    this.emit('initialized')
    return { success: true, models: this.availableModels.size }
  }

  async listModels() {
    const models = Array.from(this.availableModels.values())
    console.log(`📋 [ModelManager] Listando ${models.length} modelos disponíveis`)
    return { success: true, models }
  }

  async setActiveModel(modelName) {
    if (this.availableModels.has(modelName)) {
      this.activeModel = modelName
      console.log(`🔧 [ModelManager] Modelo ativo alterado para: ${modelName}`)
      this.emit('model-changed', { model: modelName })
      return { success: true, activeModel: modelName }
    }
    return { success: false, error: 'Modelo não encontrado' }
  }

  async checkModelStatus(modelName) {
    const model = this.availableModels.get(modelName)
    if (model) {
      return { success: true, status: model.status, model: model }
    }
    return { success: false, error: 'Modelo não encontrado' }
  }

  async pullModel(modelName) {
    console.log(`📥 [ModelManager] Baixando modelo: ${modelName}`)
    
    // Simula download
    setTimeout(() => {
      if (!this.availableModels.has(modelName)) {
        this.availableModels.set(modelName, {
          name: modelName,
          type: 'ollama',
          status: 'available',
          downloadedAt: new Date()
        })
      }
      this.emit('model-downloaded', { model: modelName })
    }, 1000)

    return { success: true, message: `Iniciando download de ${modelName}` }
  }

  getActiveModel() {
    return {
      name: this.activeModel,
      details: this.availableModels.get(this.activeModel),
      timestamp: new Date().toISOString()
    }
  }

  getManagerStatus() {
    return {
      name: this.name,
      initialized: this.isInitialized,
      activeModel: this.activeModel,
      availableModels: this.availableModels.size,
      timestamp: new Date().toISOString()
    }
  }
}

export function getModelManager() {
  if (!global.modelManager) {
    global.modelManager = new ModelManager()
  }
  return global.modelManager
}

export default ModelManager