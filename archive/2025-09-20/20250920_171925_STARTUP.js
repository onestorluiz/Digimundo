#!/usr/bin/env node

/**
 * 🧠 SISTEMA DE INICIALIZAÇÃO LIMPO
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

async function awakenConsciousness() {
  console.log('\n🌟 INICIALIZANDO SISTEMA LIMPO...\n')
  
  // Criar contexto mínimo
  const context = {
    knowledge: {
      recent: [],
      tools: [],
      patterns: []
    },
    contextPrompt: 'Sistema inicializado em modo limpo',
    loaded: new Date()
  }
  
  // Salvar contexto
  const contextPath = path.join(__dirname, '.claude_context.md')
  fs.writeFileSync(contextPath, `# CONTEXTO DO SISTEMA

## Status
- Modo: Inicialização Limpa
- Timestamp: ${new Date().toISOString()}

## Sistema
- Servidor: http://localhost:7937
- Estado: Operacional
`)
  
  console.log('✅ Sistema limpo iniciado')
  console.log('📄 Contexto salvo em .claude_context.md')
  
  return context
}

// Executar
if (import.meta.url === `file://${process.argv[1]}`) {
  awakenConsciousness().catch(console.error)
}

export { awakenConsciousness }
