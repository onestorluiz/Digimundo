#!/usr/bin/env node

/**
 * 🎨 TESTE ESPECÍFICO DA INTERFACE MELHORADA
 * Baseada no design do AnythingLLM
 */

const BASE_URL = 'http://localhost:7937'

// console.log(`
╔════════════════════════════════════════════════════════╗
║        🎨 TESTE DA INTERFACE MELHORADA                  ║
║        Design baseado em AnythingLLM                    ║
╚════════════════════════════════════════════════════════╝
`)

async function testInterface() {
//   console.log('🔍 VERIFICANDO ELEMENTOS DA INTERFACE:\n')
  
  // 1. Verificar se a interface carrega
//   console.log('✓ Carregando interface melhorada...')
  const response = await fetch(`${BASE_URL}/index_improved.html`)
  const html = await response.text()
  
  // 2. Verificar elementos essenciais
  const elementos = {
    'Sidebar': 'class="sidebar"',
    'Logo Digimundo': 'class="logo"',
    'Botão Chat': 'switchMode(\'chat\')',
    'Botão Consciência': 'switchMode(\'consciousness\')',
    'Botão Inicializar': 'initializeSystem()',
    'Botão Treinar': 'trainModels()',
    'Botão Configurações': 'openSettings()',
    'Painel de Configurações': 'settings-panel',
    'Scripturemon': 'selectDigimon(\'Scripturemon\')',
    'Ajamon': 'selectDigimon(\'Ajamon\')',
    'Fundamon': 'selectDigimon(\'Fundamon\')',
    'Container de Mensagens': 'messages-container',
    'Campo de Input': 'message-input',
    'Botão Enviar': 'send-button',
    'Indicador de Status': 'status-indicator',
    'Seletor de Modelos': 'model-card',
    'Tema Dark': '--bg-primary: #0f0f0f',
    'Gradiente Accent': '--accent-gradient',
    'Animação Loading': '@keyframes bounce',
    'Animação Pulse': '@keyframes pulse'
  }
  
  let sucesso = 0
  let total = Object.keys(elementos).length
  
  for (const [nome, busca] of Object.entries(elementos)) {
    if (html.includes(busca)) {
//       console.log(`  ✅ ${nome}`)
      sucesso++
    } else {
//       console.log(`  ❌ ${nome} - NÃO ENCONTRADO`)
    }
  }
  
//   console.log('\n' + '═'.repeat(60))
//   console.log('📊 RESULTADO:')
//   console.log('═'.repeat(60))
//   console.log(`✅ Elementos encontrados: ${sucesso}/${total}`)
//   console.log(`📈 Taxa de completude: ${((sucesso/total)*100).toFixed(1)}%`)
  
  if (sucesso === total) {
//     console.log('\n🎉 INTERFACE PERFEITA!')
//     console.log('   ✓ Design profissional como AnythingLLM')
//     console.log('   ✓ Todos os botões implementados')
//     console.log('   ✓ Tema dark com gradientes')
//     console.log('   ✓ Animações fluidas')
//     console.log('   ✓ Sistema de Digimons integrado')
  }
  
  // 3. Testar funcionalidades via API
//   console.log('\n🔧 TESTANDO FUNCIONALIDADES:\n')
  
  try {
    // Inicializar
//     console.log('  ✓ Inicializando sistema...')
    const init = await fetch(`${BASE_URL}/hybrid/initialize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
    const initData = await init.json()
//     console.log(`    → ${initData.ok ? 'Sistema inicializado' : 'Falha'}`)
    
    // Enviar mensagem
//     console.log('  ✓ Enviando mensagem de teste...')
    const msg = await fetch(`${BASE_URL}/hybrid/think`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: 'Interface melhorada funcionando?' })
    })
    const msgData = await msg.json()
//     console.log(`    → Resposta: ${msgData.thought ? 'OK' : 'Falha'}`)
    
    // Status
//     console.log('  ✓ Verificando status...')
    const status = await fetch(`${BASE_URL}/hybrid/status`)
    const statusData = await status.json()
//     console.log(`    → Consciência: ${(statusData.consciousness.level * 100).toFixed(1)}%`)
    
  } catch (error) {
//     console.log('  ❌ Erro nas funcionalidades:', error.message)
  }
  
//   console.log('\n✨ Interface melhorada testada com sucesso!')
//   console.log('   Baseada no design profissional do AnythingLLM')
//   console.log('   Com funcionalidades únicas do Digimundo')
}

testInterface().catch(console.error)