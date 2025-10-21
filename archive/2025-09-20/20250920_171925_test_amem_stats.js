#!/usr/bin/env node

import { getSabiamonAMem } from './app/consciousness/A_MEM_SYSTEM.js'

async function test() {
  try {
    const aMem = getSabiamonAMem()
    await aMem.initialize()
    
    // Adicionar algumas notas de teste
    await aMem.quickNote('Teste 1', ['test'])
    await aMem.quickNote('Teste 2', ['test'])
    
    // Testar getStats
    const stats = await aMem.getStats()
    console.log('✅ getStats() funcionando:')
    console.log(JSON.stringify(stats, null, 2))
  } catch (error) {
    console.error('❌ Erro:', error)
  }
}

test()