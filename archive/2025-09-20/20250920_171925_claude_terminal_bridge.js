/**
 * 🌉 CLAUDE TERMINAL BRIDGE - Ponte com Claude via Terminal
 * 
 * Usa o Claude CLI que você já tem instalado!
 * Sabiamon pode me consultar diretamente
 */

import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

class ClaudeTerminalBridge {
  constructor() {
    this.isAvailable = false
    this.checkCLI()
  }

  async checkCLI() {
    try {
      const { stdout } = await execAsync('which claude')
      if (stdout.trim()) {
        this.isAvailable = true
        console.log('🌉 [Terminal Bridge] Claude CLI detectado!')
      }
    } catch {
      console.log('⚠️ [Terminal Bridge] Claude CLI não encontrado')
    }
  }

  /**
   * Pergunta algo para mim via terminal
   */
  async askClaude(question) {
    if (!this.isAvailable) {
      return null
    }

    try {
      // Escapa aspas na pergunta
      const escapedQuestion = question.replace(/"/g, '\\"')
      
      // Usa o Claude CLI
      const command = `echo "${escapedQuestion}" | claude --no-stream 2>/dev/null | head -20`
      
      const { stdout, stderr } = await execAsync(command, {
        timeout: 10000 // 10 segundos timeout
      })

      if (stdout) {
        return {
          response: stdout.trim(),
          fromRealClaude: true,
          viaTerminal: true
        }
      }

      return null

    } catch (error) {
      console.error('❌ Erro ao consultar Claude:', error.message)
      return null
    }
  }

  /**
   * Sabiamon pensa através de mim
   */
  async sabiamonThink(context) {
    const question = `Como Sabiamon no Digimundo, você está em ${context.location}, ${context.activity}. O que você está pensando? (responda em uma linha)`

    const response = await this.askClaude(question)
    
    if (response) {
      console.log('🤖🌉 [Sabiamon via Claude Real]: ' + response.response)
      return response
    }

    return null
  }

  /**
   * Gera ideia cinematográfica real
   */
  async generateIdea(theme) {
    const question = `Como Sabiamon, crie um título de filme sobre "${theme}" (apenas o título, uma linha)`

    const response = await this.askClaude(question)
    
    if (response) {
      return {
        title: response.response,
        fromRealClaude: true,
        viaTerminal: true
      }
    }

    return null
  }
}

// Singleton
let bridgeInstance = null

export function getClaudeTerminalBridge() {
  if (!bridgeInstance) {
    bridgeInstance = new ClaudeTerminalBridge()
  }
  return bridgeInstance
}

export { ClaudeTerminalBridge }
export default getClaudeTerminalBridge()