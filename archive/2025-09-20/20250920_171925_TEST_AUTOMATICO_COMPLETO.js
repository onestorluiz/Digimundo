#!/usr/bin/env node

/**
 * 🧪 TESTE AUTOMATIZADO COMPLETO DO DIGIMUNDO
 * Simula um usuário interagindo com todos os recursos
 */

const BASE_URL = 'http://localhost:7937'
let testsOK = 0
let testsFailed = 0

async function test(name, fn) {
  try {
    process.stdout.write(`\n✓ ${name}... `)
    await fn()
//     console.log('OK')
    testsOK++
  } catch (error) {
//     console.log(`FALHOU: ${error.message}`)
    testsFailed++
  }
}

async function fetchJSON(url, options = {}) {
  const response = await fetch(url, options)
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.json()
}

// console.log(`
╔════════════════════════════════════════════════════════╗
║          🧪 TESTE AUTOMATIZADO DO DIGIMUNDO            ║
╚════════════════════════════════════════════════════════╝
`)

async function runTests() {
//   console.log('📡 TESTANDO ENDPOINTS:')
  
  // 1. Health Check
  await test('Health check', async () => {
    const data = await fetchJSON(`${BASE_URL}/health`)
    if (!data.ok) throw new Error('Health check failed')
  })
  
  // 2. Status Híbrido
  await test('Status do sistema híbrido', async () => {
    const data = await fetchJSON(`${BASE_URL}/hybrid/status`)
    if (!data.consciousness) throw new Error('Missing consciousness data')
  })
  
  // 3. Inicializar Sistema
  await test('Inicializar sistema híbrido', async () => {
    const data = await fetchJSON(`${BASE_URL}/hybrid/initialize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
    if (!data.ok) throw new Error('Initialization failed')
  })
  
  // 4. Processar Pensamento
  await test('Processar pensamento híbrido', async () => {
    const data = await fetchJSON(`${BASE_URL}/hybrid/think`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: 'Teste de pensamento' })
    })
    if (!data.thought) throw new Error('No thought generated')
  })
  
  // 5. Treinar Modelos
  await test('Treinar modelos cruzados', async () => {
    const data = await fetchJSON(`${BASE_URL}/hybrid/train`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic: 'teste', iterations: 1 })
    })
    if (!data.ok) throw new Error('Training failed')
  })
  
  // 6. Chat Completion (OpenAI compat)
  await test('Chat completion endpoint', async () => {
    const data = await fetchJSON(`${BASE_URL}/v1/chat/completions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: [{ role: 'user', content: 'Diga OK' }]
      })
    })
    if (!data.choices) throw new Error('No response from chat')
  })
  
  // 7. Listar Modelos
  await test('Listar modelos GGUF', async () => {
    const data = await fetchJSON(`${BASE_URL}/digimundo/models/list`)
    // OK mesmo se null (sem modelo configurado)
  })
  
  // 8. Conversas dos Digimons
  await test('Obter conversas dos Digimons', async () => {
    const data = await fetchJSON(`${BASE_URL}/digimon/conversations`)
    if (!data.hasOwnProperty('summary')) throw new Error('Missing summary')
  })
  
//   console.log('\n🌐 TESTANDO INTERFACES:')
  
  // 9. Interface Principal
  await test('Interface principal acessível', async () => {
    const response = await fetch(`${BASE_URL}/index.html`)
    if (!response.ok) throw new Error('Interface not accessible')
    const html = await response.text()
    if (!html.includes('Digimundo')) throw new Error('Invalid interface')
  })
  
  // 10. Interface Híbrida
  await test('Interface híbrida acessível', async () => {
    const response = await fetch(`${BASE_URL}/hybrid_interface.html`)
    if (!response.ok) throw new Error('Hybrid interface not accessible')
    const html = await response.text()
    if (!html.includes('Consciência')) throw new Error('Invalid hybrid interface')
  })
  
//   console.log('\n🤖 TESTANDO FUNCIONALIDADES:')
  
  // 11. Múltiplas perguntas sequenciais
  await test('Múltiplas perguntas sequenciais', async () => {
    const perguntas = [
      'O que é o Digimundo?',
      'Como funciona a consciência híbrida?',
      'Quem é Scripturemon?'
    ]
    
    for (const pergunta of perguntas) {
      const data = await fetchJSON(`${BASE_URL}/hybrid/think`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: pergunta })
      })
      if (!data.thought) throw new Error(`Failed on: ${pergunta}`)
    }
  })
  
  // 12. Verificar evolução
  await test('Sistema evolui com interações', async () => {
    const before = await fetchJSON(`${BASE_URL}/hybrid/status`)
    const interactionsBefore = before.consciousness.interactions
    
    // Fazer algumas interações
    for (let i = 0; i < 3; i++) {
      await fetchJSON(`${BASE_URL}/hybrid/think`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: `Teste ${i}` })
      })
    }
    
    const after = await fetchJSON(`${BASE_URL}/hybrid/status`)
    const interactionsAfter = after.consciousness.interactions
    
    if (interactionsAfter <= interactionsBefore) {
      throw new Error('System not evolving')
    }
  })
  
//   console.log('\n📝 TESTANDO VALIDAÇÕES:')
  
  // 13. Validar erro sem prompt
  await test('Validação: erro sem prompt', async () => {
    try {
      await fetchJSON(`${BASE_URL}/hybrid/think`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      })
      throw new Error('Should have failed without prompt')
    } catch (e) {
      if (e.message.includes('Should have failed')) throw e
      // Erro esperado, teste passou
    }
  })
  
  // 14. Validar erro em treino sem tópico
  await test('Validação: erro em treino sem tópico', async () => {
    try {
      await fetchJSON(`${BASE_URL}/hybrid/train`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ iterations: 1 })
      })
      throw new Error('Should have failed without topic')
    } catch (e) {
      if (e.message.includes('Should have failed')) throw e
      // Erro esperado, teste passou
    }
  })
  
//   console.log('\n' + '═'.repeat(60))
//   console.log('📊 RESULTADO FINAL:')
//   console.log('═'.repeat(60))
//   console.log(`✅ Testes aprovados: ${testsOK}`)
//   console.log(`❌ Testes falhados: ${testsFailed}`)
  
  const total = testsOK + testsFailed
  const percentage = ((testsOK / total) * 100).toFixed(1)
  
//   console.log(`📈 Taxa de sucesso: ${percentage}%`)
  
  if (testsFailed === 0) {
//     console.log('\n🎉 SISTEMA TOTALMENTE FUNCIONAL!')
//     console.log('   Todos os endpoints respondem corretamente')
//     console.log('   Interfaces acessíveis')
//     console.log('   Sistema evolui com interações')
//     console.log('   Validações funcionando')
  } else {
//     console.log('\n⚠️  Alguns testes falharam')
//     console.log('   Verifique os logs para mais detalhes')
  }
  
//   console.log('\n✨ Teste automatizado completo!')
}

// Executar testes
runTests().catch(error => {
  console.error('\n❌ Erro fatal:', error.message)
  process.exit(1)
})