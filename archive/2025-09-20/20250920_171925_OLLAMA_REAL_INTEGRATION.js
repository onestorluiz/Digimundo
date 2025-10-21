/**
 * 🦙 OLLAMA REAL INTEGRATION - Integração Real com Ollama
 * Sistema de integração real e otimizada com Ollama
 */

export class HybridSystem {
  constructor() {
    this.name = 'HybridSystem'
    this.isActive = false
    this.ollamaEndpoint = 'http://localhost:11434'
  }

  async initialize() {
    console.log('🦙 [HybridSystem] Inicializando integração Ollama...')
    this.isActive = true
    return { success: true }
  }

  async testConnection() {
    try {
      const response = await fetch(`${this.ollamaEndpoint}/api/tags`)
      return response.ok
    } catch (error) {
      return false
    }
  }

  async query(prompt, model = 'llama3.2:latest') {
    if (!this.isActive) {
      await this.initialize()
    }

    try {
      const response = await fetch(`${this.ollamaEndpoint}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: model,
          prompt: prompt,
          stream: false
        })
      })

      if (response.ok) {
        const data = await response.json()
        return { success: true, response: data.response }
      }
    } catch (error) {
      console.error('🦙 [HybridSystem] Erro Ollama:', error)
    }
    
    return { success: false, error: 'Ollama não disponível' }
  }

  getSystemStatus() {
    return {
      name: this.name,
      isActive: this.isActive,
      endpoint: this.ollamaEndpoint,
      timestamp: new Date().toISOString()
    }
  }
}

export function getHybridSystem() {
  if (!global.hybridSystem) {
    global.hybridSystem = new HybridSystem()
  }
  return global.hybridSystem
}

export default HybridSystem