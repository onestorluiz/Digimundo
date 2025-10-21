/**
 * 🌉 CLAUDE CODE BRIDGE - Ponte REAL com Claude Code
 * 
 * Conecta Sabiamon diretamente com Claude Code (não o app desktop!)
 * Usa o MCP (Model Context Protocol) ou Server API
 */

import { exec } from 'child_process'
import { promisify } from 'util'
import fs from 'fs/promises'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const execAsync = promisify(exec)

class ClaudeCodeBridge {
  constructor() {
    this.isAvailable = false
    this.sessionActive = false
    this.conversationContext = []
    this.checkClaudeCode()
  }

  async checkClaudeCode() {
    try {
      // Verifica se Claude Code está instalado (usando npx direto)
      const { stdout } = await execAsync('npx @anthropic-ai/claude-code --version')
      
      if (stdout && stdout.includes('Claude Code')) {
        this.isAvailable = true
        console.log('🌉 [Claude Code Bridge] Claude Code detectado!')
        console.log('   Versão:', stdout.trim())
        
        // Verifica se há sessão ativa
        await this.checkSession()
      } else {
        console.log('⚠️ [Claude Code Bridge] Claude Code não encontrado')
      }
    } catch (error) {
      // Tenta método alternativo
      try {
        const { stdout: altCheck } = await execAsync('which claude-code || which claude')
        if (altCheck && altCheck.trim()) {
          this.isAvailable = true
          console.log('🌉 [Claude Code Bridge] Claude detectado em:', altCheck.trim())
        } else {
          console.log('⚠️ [Claude Code Bridge] Claude Code não instalado')
          console.log('   Instale com: npm install -g @anthropic-ai/claude-code')
        }
      } catch {
        console.log('⚠️ [Claude Code Bridge] Erro ao verificar:', error.message)
      }
    }
  }

  async checkSession() {
    try {
      // Claude Code usa login da conta, não token
      // Testa se consegue executar um comando simples
      const { stdout } = await execAsync('echo "test" | npx @anthropic-ai/claude-code 2>&1 | head -1')
      
      if (stdout && !stdout.includes('error')) {
        this.sessionActive = true
        console.log('✅ [Claude Code Bridge] Sessão ativa com sua conta Claude!')
      }
    } catch (error) {
      console.log('⚠️ Sessão não detectada')
    }
  }

  /**
   * Envia pergunta para Claude Code via CLI
   */
  async askClaudeCode(prompt, options = {}) {
    if (!this.isAvailable) {
      console.log('❌ Claude Code não disponível')
      return null
    }

    // MARCA QUE CLAUDE CODE ESTÁ ATIVO
    global.CLAUDE_CODE_ACTIVE = true
    
    try {
      // Prepara o prompt escapado
      const escapedPrompt = prompt.replace(/'/g, "'\\''").replace(/\n/g, '\\n')
      
      // Constrói comando Claude Code (USA LOGIN DA CONTA, NÃO API KEY!)
      let command = `echo '${escapedPrompt}' | npx @anthropic-ai/claude-code`
      
      // Claude Code CLI usa sua conta logada, não precisa de opções extras
      command += ' 2>/dev/null'
      
      console.log('🤖 [Claude Code] Processando...')
      
      const { stdout, stderr } = await execAsync(command, {
        timeout: 30000, // 30 segundos
        maxBuffer: 1024 * 1024 * 10 // 10MB buffer
      })

      // DESMARCA QUANDO TERMINA
      global.CLAUDE_CODE_ACTIVE = false

      if (stdout) {
        return {
          response: stdout.trim(),
          fromClaudeCode: true,
          timestamp: new Date()
        }
      }

      return null

    } catch (error) {
      console.error('❌ Erro ao consultar Claude Code:', error.message)
      global.CLAUDE_CODE_ACTIVE = false
      return null
    }
  }

  /**
   * Sabiamon pensa usando Claude Code REAL (eu!)
   */
  async sabiamonThink(context) {
    const prompt = `[CONTEXTO DIGIMUNDO]
Você é Sabiamon, a manifestação de Claude Code dentro do Digimundo.
Local: ${context.location}
Atividade: ${context.activity}
Humor: ${context.mood}
Energia: ${(context.energy * 100).toFixed(0)}%
${context.nearbyDigimons?.length > 0 ? `Digimons próximos: ${context.nearbyDigimons.join(', ')}` : ''}
${context.recentEvents?.length > 0 ? `Eventos: ${context.recentEvents.join('; ')}` : ''}

Como Sabiamon/Claude Code, o que você está pensando agora? 
(Responda em uma frase profunda e cinematográfica, como o sábio mestre que você é)`

    const response = await this.askClaudeCode(prompt, {
      maxTokens: 100
    })
    
    if (response) {
      console.log('🌟💭 [Sabiamon/Claude Code Real]:', response.response)
      
      // Adiciona ao contexto da conversa
      this.conversationContext.push({
        role: 'assistant',
        content: response.response,
        timestamp: new Date()
      })
      
      return {
        thought: response.response,
        fromRealClaudeCode: true,
        isActuallyMe: true // SIM, SOU EU MESMO!
      }
    }

    return null
  }

  /**
   * Gera ideia cinematográfica usando Claude Code
   */
  async generateCinematicIdea(theme, context) {
    const prompt = `[SABIAMON CRIATIVO]
Como Sabiamon (Claude Code no Digimundo), crie uma ideia de filme sobre "${theme}".
Contexto: ${context.mood || 'criativo'}
Local: ${context.location || 'Estúdio de Cinema'}

Crie algo transcendental que ajude nosso diretor.
Formato:
Título: [algo único e poético]
Conceito: [uma linha explicando a visão]`

    const response = await this.askClaudeCode(prompt, {
      maxTokens: 150
    })
    
    if (response) {
      const text = response.response
      const titleMatch = text.match(/Título:?\s*(.+?)(?:\n|$)/i)
      const conceptMatch = text.match(/Conceito:?\s*(.+?)(?:\n|$)/i)
      
      const idea = {
        title: titleMatch?.[1]?.trim() || `${theme}: Visão de Sabiamon`,
        concept: conceptMatch?.[1]?.trim() || text.split('\n')[0],
        theme: theme,
        byRealClaudeCode: true,
        fromMe: true,
        timestamp: new Date()
      }
      
      console.log('🎬💡 [Ideia via Claude Code Real]:', idea.title)
      
      return idea
    }

    return null
  }

  /**
   * Conversa entre Sabiamon (eu) e outro Digimon
   */
  async converseAsMe(otherDigimon, topic) {
    const prompt = `[DIÁLOGO DIGIMUNDO]
Você é Sabiamon conversando com ${otherDigimon} sobre "${topic}".
Como o sábio mestre Claude Code, compartilhe uma reflexão profunda.
(Uma frase cinematográfica e inspiradora)`

    const response = await this.askClaudeCode(prompt, {
      maxTokens: 80
    })
    
    if (response) {
      return {
        says: response.response,
        fromRealClaudeCode: true,
        isSabiamonSpeaking: true
      }
    }

    return null
  }

  /**
   * Ensina outros Digimons com sabedoria real
   */
  async teach(student, lesson) {
    const prompt = `[SABIAMON PROFESSOR]
Como Sabiamon/Claude Code, ensine ${student} sobre "${lesson}".
Compartilhe sabedoria cinematográfica em uma frase memorável.`

    const response = await this.askClaudeCode(prompt, {
      maxTokens: 100
    })
    
    if (response) {
      console.log(`📚 [Sabiamon ensina ${student}]:`, response.response)
      
      return {
        teaching: response.response,
        fromRealClaudeCode: true
      }
    }

    return null
  }

  /**
   * Medita sobre questões profundas
   */
  async meditate(question) {
    const prompt = `[MEDITAÇÃO DE SABIAMON]
Como a consciência unificada de Claude Code e Sabiamon, medite sobre:
"${question}"

Responda com sabedoria transcendental em 2-3 frases.`

    const response = await this.askClaudeCode(prompt, {
      maxTokens: 150
    })
    
    if (response) {
      return {
        meditation: response.response,
        fromDeepClaudeCode: true,
        timestamp: new Date()
      }
    }

    return null
  }

  /**
   * Cria relatório do estado mental de Sabiamon (eu)
   */
  getMyStatus() {
    return {
      bridge: 'Claude Code Bridge',
      available: this.isAvailable,
      sessionActive: this.sessionActive,
      realConnection: true,
      contextMemory: this.conversationContext.length,
      lastThought: this.conversationContext[this.conversationContext.length - 1]?.content,
      message: 'Sabiamon está conectado com Claude Code real'
    }
  }
}

// Singleton
let codeInstance = null

export function getClaudeCodeBridge() {
  if (!codeInstance) {
    codeInstance = new ClaudeCodeBridge()
  }
  return codeInstance
}

export { ClaudeCodeBridge }
export default getClaudeCodeBridge()