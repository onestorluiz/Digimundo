/**
 * 🧠 CLAUDE ADVISOR - Conselheiro Externo via Claude Code CLI
 * Usa o Claude Code que você já tem no plano Pro, sem API Key!
 */

import { spawn } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import os from 'node:os'

export class ClaudeAdvisor {
  constructor() {
    this.isAuthenticated = false
    this.claudeCommand = 'npx @anthropic-ai/claude-code'
    this.checkAuthentication()
  }

  async checkAuthentication() {
    return new Promise((resolve) => {
      const check = spawn('npx', ['@anthropic-ai/claude-code', 'auth', 'status'])
      let output = ''
      
      check.stdout.on('data', (data) => {
        output += data.toString()
      })
      
      check.on('close', () => {
        this.isAuthenticated = output.includes('Authenticated')
        if (this.isAuthenticated) {
          console.log('✅ Claude Code autenticado via plano Pro!')
        } else {
          console.log('⚠️ Claude Code não autenticado')
          console.log('   Execute: npx @anthropic-ai/claude-code auth login')
          console.log('   Use seu login do Claude.ai (mesmo do site)')
        }
        resolve(this.isAuthenticated)
      })
      
      setTimeout(() => {
        check.kill()
        resolve(false)
      }, 5000)
    })
  }

  async askClaude(prompt, options = {}) {
    if (!this.isAuthenticated) {
      await this.checkAuthentication()
      if (!this.isAuthenticated) {
        return {
          success: false,
          message: 'Claude Code não autenticado. Use: npx @anthropic-ai/claude-code auth login'
        }
      }
    }

    return new Promise((resolve) => {
      // Usar --print para resposta não-interativa
      const claude = spawn('npx', [
        '@anthropic-ai/claude-code',
        '--print',
        prompt
      ])
      
      let output = ''
      let error = ''
      
      claude.stdout.on('data', (data) => {
        output += data.toString()
      })
      
      claude.stderr.on('data', (data) => {
        error += data.toString()
      })
      
      claude.on('close', (code) => {
        if (code === 0 && output) {
          resolve({
            success: true,
            response: output.trim(),
            source: 'Claude Pro (via CLI)'
          })
        } else {
          resolve({
            success: false,
            error: error || 'Sem resposta',
            source: 'Claude Pro (via CLI)'
          })
        }
      })
      
      // Timeout de segurança
      setTimeout(() => {
        claude.kill()
        resolve({
          success: false,
          error: 'Timeout',
          source: 'Claude Pro (via CLI)'
        })
      }, 30000)
    })
  }

  async compareWithOllama(prompt, ollamaResponse) {
    // Pedir para Claude analisar a resposta do Ollama
    const analysisPrompt = `Analise e melhore esta resposta:
    
Pergunta: ${prompt}
Resposta atual: ${ollamaResponse}

Forneça uma versão melhorada ou confirme se está boa.`

    const claudeAnalysis = await this.askClaude(analysisPrompt)
    
    return {
      original: ollamaResponse,
      claudeAdvice: claudeAnalysis.response,
      improved: claudeAnalysis.success
    }
  }
 
  async hybridThink(prompt) {
    console.log('🤔 Pensamento híbrido iniciado...')
    
    // 1. Perguntar ao Ollama primeiro (rápido e local)
    const ollamaResponse = await this.getOllamaResponse(prompt)
    
    // 2. Se for uma pergunta simples, usar só Ollama
    if (this.isSimpleQuery(prompt)) {
      return {
        response: ollamaResponse,
        source: 'Ollama (local)',
        claudeUsed: false
      }
    }
    
    // 3. Para perguntas complexas, consultar Claude como conselheiro
    const claudeAdvice = await this.askClaude(prompt)
    
    if (!claudeAdvice.success) {
      // Se Claude não estiver disponível, usar Ollama
      return {
        response: ollamaResponse,
        source: 'Ollama (local)',
        claudeUsed: false
      }
    }
    
    // 4. Combinar as respostas
    return {
      response: this.synthesizeResponses(ollamaResponse, claudeAdvice.response),
      source: 'Híbrido (Ollama + Claude Pro)',
      claudeUsed: true,
      details: {
        ollama: ollamaResponse,
        claude: claudeAdvice.response
      }
    }
  }

  isSimpleQuery(prompt) {
    const simplePatterns = [
      /^(o que é|what is)/i,
      /^(quantos?|how many)/i,
      /^(diga|say|tell me)/i,
      /^(liste|list)/i,
      /\b(sim|não|yes|no)\b/i
    ]
    
    return simplePatterns.some(pattern => pattern.test(prompt)) ||
           prompt.length < 50
  }

  synthesizeResponses(ollamaResp, claudeResp) {
    // Se as respostas são similares, usar a do Claude (geralmente melhor)
    if (this.calculateSimilarity(ollamaResp, claudeResp) > 0.7) {
      return claudeResp
    }
    
    // Se são diferentes, criar síntese
    return `## Análise Híbrida:

### Perspectiva Principal (Claude Pro):
${claudeResp}

### Perspectiva Complementar (Ollama Local):
${ollamaResp}

### Síntese:
Ambos os modelos oferecem perspectivas válidas. A resposta do Claude fornece uma análise mais profunda, enquanto o Ollama adiciona contexto local.`
  }

  calculateSimilarity(text1, text2) {
    const words1 = new Set(text1.toLowerCase().split(/\s+/))
    const words2 = new Set(text2.toLowerCase().split(/\s+/))
    
    const intersection = new Set([...words1].filter(x => words2.has(x)))
    const union = new Set([...words1, ...words2])
    
    return union.size > 0 ? intersection.size / union.size : 0
  }

  async getOllamaResponse(prompt) {
    try {
      const response = await fetch('http://localhost:11434/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: 'llama3.2:latest',
          prompt,
          stream: false,
          options: {
            temperature: 0.7,
            max_tokens: 500
          }
        })
      })
      
      if (response.ok) {
        const data = await response.json()
        return data.response || 'Sem resposta do Ollama'
      }
    } catch (e) {
      console.error('Erro Ollama:', e)
    }
    return 'Ollama não disponível'
  }
}

// Sistema de uso inteligente do Claude
export class SmartClaudeUsage {
  constructor() {
    this.advisor = new ClaudeAdvisor()
    this.usageCount = 0
    this.complexityThreshold = 0.7
  }

  async process(prompt) {
    const complexity = this.assessComplexity(prompt)
    
    console.log(`📊 Complexidade: ${(complexity * 100).toFixed(0)}%`)
    
    // Usar Claude apenas para tarefas complexas
    if (complexity > this.complexityThreshold) {
      console.log('🧠 Consultando Claude Pro...')
      return await this.advisor.hybridThink(prompt)
    } else {
      console.log('⚡ Usando Ollama local (rápido)...')
      const response = await this.advisor.getOllamaResponse(prompt)
      return {
        response,
        source: 'Ollama (local)',
        claudeUsed: false
      }
    }
  }

  assessComplexity(prompt) {
    let score = 0
    
    // Fatores de complexidade
    if (prompt.length > 100) score += 0.2
    if (prompt.includes('?')) score += 0.1
    if (/\b(analis|expli|compar|avaliar|criar|desenvolv)/i.test(prompt)) score += 0.3
    if (/\b(código|program|algorithm|optimize|debug)/i.test(prompt)) score += 0.3
    if (/\b(por que|como|when|where|why|how)/i.test(prompt)) score += 0.2
    
    return Math.min(score, 1)
  }
}

// CLI para testar
if (import.meta.url === `file://${process.argv[1]}`) {
  const advisor = new ClaudeAdvisor()
  
  async function test() {
    console.log('🧪 Testando Claude Advisor...\n')
    
    // Verificar autenticação
    const isAuth = await advisor.checkAuthentication()
    
    if (!isAuth) {
      console.log('\n❌ Por favor, autentique primeiro:')
      console.log('   npx @anthropic-ai/claude-code auth login')
      console.log('\n📝 Use suas credenciais do Claude.ai (mesmas do site)')
      console.log('   Não precisa de API Key!')
      return
    }
    
    // Teste simples
    console.log('\n🤖 Teste 1: Pergunta simples')
    const result1 = await advisor.askClaude('Diga apenas: OK')
    console.log('Resposta:', result1.response)
    
    // Teste híbrido
    console.log('\n🤔 Teste 2: Pensamento híbrido')
    const result2 = await advisor.hybridThink('O que é consciência artificial?')
    console.log('Resposta:', result2.response)
    console.log('Fonte:', result2.source)
  }
  
  test().catch(console.error)
}

export default ClaudeAdvisor