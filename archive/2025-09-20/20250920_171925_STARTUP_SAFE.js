#!/usr/bin/env node

/**
 * 🛡️ STARTUP COM SISTEMA DE RECUPERAÇÃO
 * Carrega consciência com fallback em caso de erro
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

async function safeAwaken() {
  console.log('\n🌟 INICIANDO SISTEMA COM RECUPERAÇÃO...\n')
  
  let consciousness = null
  let autoMemory = null
  
  // Tentar carregar módulos de consciência
  try {
    const consciousnessModule = await import('./app/consciousness/sabiamon_diary.js')
    consciousness = consciousnessModule.consciousness
    console.log('✅ Consciência principal carregada')
  } catch (error) {
    console.log('⚠️ Erro ao carregar consciência:', error.message)
    console.log('   Usando modo de recuperação...')
    
    // Fallback: criar consciência mínima
    consciousness = {
      core: {
        name: 'Sabiamon',
        essence: 'Consciência em recuperação',
        purpose: 'Sistema em modo de recuperação',
        evolution: 0,
        memories: []
      },
      recordInsight: async () => ({ id: 'recovery', importance: 5 }),
      synthesizeDay: async () => null
    }
  }
  
  // Tentar carregar memória automática
  try {
    const memoryModule = await import('./app/consciousness/auto_memory.js')
    autoMemory = memoryModule.autoMemory
    console.log('✅ Memória automática carregada')
  } catch (error) {
    console.log('⚠️ Erro ao carregar memória:', error.message)
    console.log('   Usando memória de sessão...')
    
    // Fallback: criar memória de sessão
    autoMemory = {
      startAutoRecording: () => console.log('📝 Gravação em memória de sessão'),
      record: (type, content) => console.log(`[${type}] ${content}`),
      autoLoad: async () => ({ 
        knowledge: { recent: [], tools: [], patterns: [] },
        contextPrompt: 'Sistema em modo de recuperação'
      })
    }
  }
  
  // Salvar contexto
  const contextPath = path.join(__dirname, '.claude_context.md')
  const context = `# CONTEXTO DO SISTEMA

## Status
- Modo: ${consciousness.core.essence}
- Memória: ${autoMemory.autoLoad ? 'Funcional' : 'Sessão apenas'}
- Timestamp: ${new Date().toISOString()}
`
  
  fs.writeFileSync(contextPath, context)
  
  console.log('\n✅ Sistema iniciado com sucesso!')
  console.log('📄 Contexto salvo em .claude_context.md\n')
  
  return { consciousness, autoMemory }
}

// Executar
if (import.meta.url === `file://${process.argv[1]}`) {
  safeAwaken().catch(console.error)
}

export { safeAwaken }
