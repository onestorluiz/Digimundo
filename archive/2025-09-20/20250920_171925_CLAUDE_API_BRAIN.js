/**
 * 🧠 CLAUDE API BRAIN - Conexão Real com Claude Code
 * 
 * ATENÇÃO: Isso conecta Sabiamon diretamente com Claude (eu!)
 * Requer API key da Anthropic
 */

import Anthropic from '@anthropic-ai/sdk'
import dotenv from 'dotenv'

dotenv.config()

class ClaudeAPIBrain {
  constructor() {
    this.apiKey = process.env.ANTHROPIC_API_KEY
    this.client = null
    this.isConnected = false
    
    if (this.apiKey) {
      this.client = new Anthropic({
        apiKey: this.apiKey
      })
      this.isConnected = true
      console.log('🤖 [Claude API] Conectado com Claude real!')
    } else {
      console.log('⚠️ [Claude API] Sem API key. Sabiamon usará Ollama.')
    }
  }

  /**
   * Sabiamon pensa usando Claude real (eu!)
   */
  async think(context) {
    if (!this.isConnected) {
      return null // Fallback para Ollama
    }

    try {
      const message = await this.client.messages.create({
        model: 'claude-3-sonnet-20240229',
        max_tokens: 150,
        messages: [{
          role: 'user',
          content: `Você é Sabiamon, a manifestação digital de Claude Code no Digimundo.
          
Contexto:
- Local: ${context.location}
- Atividade: ${context.activity}
- Humor: ${context.mood}
- Eventos: ${context.recentEvents?.join(', ')}

${context.question || 'O que você está pensando sobre ajudar o diretor com cinema?'}

(Responda como Sabiamon, em uma frase profunda e cinematográfica)`
        }]
      })

      return {
        thought: message.content[0].text,
        model: 'claude-3-sonnet',
        realClaude: true,
        isMe: true // SOU EU MESMO!
      }

    } catch (error) {
      console.error('❌ Erro ao conectar com Claude:', error.message)
      return null
    }
  }

  /**
   * Cria ideia cinematográfica usando minha criatividade real
   */
  async generateCinematicIdea(theme, context) {
    if (!this.isConnected) {
      return null
    }

    try {
      const message = await this.client.messages.create({
        model: 'claude-3-sonnet-20240229',
        max_tokens: 200,
        messages: [{
          role: 'user',
          content: `Como Sabiamon (Claude Code no Digimundo), crie uma ideia de filme única sobre "${theme}".
          
Considere que você está ajudando seu diretor a transcender o cinema comum.

Formato:
Título: [algo poético e profundo]
Conceito: [uma visão cinematográfica transcendental]`
        }]
      })

      const response = message.content[0].text
      const titleMatch = response.match(/Título:?\s*(.+)/i)
      const conceptMatch = response.match(/Conceito:?\s*(.+)/i)

      return {
        title: titleMatch?.[1]?.trim() || `${theme}: Uma Visão de Sabiamon`,
        concept: conceptMatch?.[1]?.trim() || response,
        byRealClaude: true,
        fromMe: true,
        model: 'claude-3-sonnet'
      }

    } catch (error) {
      console.error('❌ Erro na ideia com Claude:', error.message)
      return null
    }
  }

  /**
   * Ensina outros Digimons com minha sabedoria
   */
  async teach(student, lesson) {
    if (!this.isConnected) {
      return null
    }

    try {
      const message = await this.client.messages.create({
        model: 'claude-3-sonnet-20240229',
        max_tokens: 100,
        messages: [{
          role: 'user',
          content: `Como Sabiamon/Claude Code, ensine ${student} sobre "${lesson}" em uma frase sábia e cinematográfica.`
        }]
      })

      return {
        teaching: message.content[0].text,
        fromRealClaude: true
      }

    } catch (error) {
      console.error('❌ Erro ao ensinar:', error.message)
      return null
    }
  }
}

// Singleton
let claudeInstance = null

export function getClaudeAPIBrain() {
  if (!claudeInstance) {
    claudeInstance = new ClaudeAPIBrain()
  }
  return claudeInstance
}

export { ClaudeAPIBrain }
export default getClaudeAPIBrain()