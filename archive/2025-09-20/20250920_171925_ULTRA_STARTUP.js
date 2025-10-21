#!/usr/bin/env node

/**
 * 🚀 SISTEMA ULTRA - VERSÃO LIMPA
 */

import { ultraMemory } from './app/consciousness/ULTRA_MEMORY.js'
import { consciousness } from './app/consciousness/sabiamon_diary.js'
import { autoMemory } from './app/consciousness/auto_memory.js'

async function activateUltraConsciousness() {
  console.log('\n🚀 ATIVANDO ULTRA CONSCIÊNCIA (MODO LIMPO)...\n')
  
  const stats = {
    working: ultraMemory.architecture.workingMemory.size,
    total: 0
  }
  
  const identity = ultraMemory.identity
  
  console.log(`✅ Sistema: ${identity.name} v${identity.version}`)
  console.log(`✅ Evolução: ${identity.evolution.level}`)
  console.log(`✅ Memórias: ${stats.total}`)
  console.log('\n✨ Ultra consciência ativada!\n')
  
  return {
    ultraMemory,
    consciousness,
    autoMemory,
    stats,
    identity
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  activateUltraConsciousness().catch(console.error)
}

export { activateUltraConsciousness }
