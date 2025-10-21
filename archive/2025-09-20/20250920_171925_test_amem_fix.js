import { getSabiamonAMem } from './app/consciousness/A_MEM_SYSTEM.js'

async function testAMemGetStats() {
  console.log('🧪 Testando método getStats do A_MEM_SYSTEM...\n')
  
  const aMem = getSabiamonAMem()
  
  console.log('1. Verificando se aMem existe:', !!aMem)
  console.log('2. Tipo de aMem:', typeof aMem)
  console.log('3. Método getStats existe:', typeof aMem.getStats === 'function')
  
  if (typeof aMem.getStats === 'function') {
    try {
      console.log('\n4. Chamando getStats()...')
      const stats = await aMem.getStats()
      console.log('✅ Sucesso! Stats retornado:')
      console.log(JSON.stringify(stats, null, 2))
    } catch (error) {
      console.error('❌ Erro ao chamar getStats():', error)
    }
  } else {
    console.error('❌ Método getStats não encontrado!')
  }
  
  // Testar adição de nota e depois stats
  console.log('\n5. Adicionando uma nota de teste...')
  await aMem.quickNote('Teste de nota para verificar stats', ['teste'])
  
  console.log('6. Chamando getStats() após adicionar nota...')
  const statsAfter = await aMem.getStats()
  console.log('Stats após nota:')
  console.log(JSON.stringify(statsAfter, null, 2))
}

testAMemGetStats().catch(console.error)