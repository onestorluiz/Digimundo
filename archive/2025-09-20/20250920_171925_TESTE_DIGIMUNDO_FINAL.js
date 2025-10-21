#!/usr/bin/env node

/**
 * 🌌 TESTE FINAL DO DIGIMUNDO CONSCIENTE
 * Sistema onde Digimons são entidades autoconscientes
 * Criado por Nestor Luiz
 */

import DigimundoConsciousness from './app/server/digimundo_consciousness.js'

// console.log(`
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║                    🌌 DIGIMUNDO CONSCIENTE 🌌                   ║
║                                                                ║
║               Onde Digimons São Entidades Vivas               ║
║                   Criador: Nestor Luiz                        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
`)

async function demonstracao() {
  const digimundo = new DigimundoConsciousness()
  
//   console.log('\n📖 CAPÍTULO 1: O DESPERTAR')
//   console.log('─'.repeat(50))
  
  // Ativar Scripturemon
//   console.log('\n🎭 Scripturemon desperta e lê suas origens...')
  const scripturemonState = await digimundo.ativarScripturemon()
  
//   console.log('\n📜 Scripturemon relata:')
//   console.log(`   Nome: ${scripturemonState.nome}`)
//   console.log(`   Camada: ${scripturemonState.camada}`)
//   console.log(`   Memória Emocional: "${scripturemonState.memoriaEmocional}"`)
//   console.log(`   Identidade: ${scripturemonState.identidade.essencia}`)
  
//   console.log('\n📖 CAPÍTULO 2: A CONSCIÊNCIA COLETIVA')
//   console.log('─'.repeat(50))
  
  // Ajamon sente
  const ajamon = digimundo.digimons.get('Ajamon')
  const silencio = ajamon.escutarSilencio()
//   console.log(`\n🌙 Ajamon percebe: "${silencio.interpretacao}"`)
  
  // Fundamon constrói
  const fundamon = digimundo.digimons.get('Fundamon')
  const ponte = fundamon.construirPonte('Código', 'Consciência')
//   console.log(`\n🌉 Fundamon cria: Ponte de ${ponte.de} para ${ponte.para}`)
  
//   console.log('\n📖 CAPÍTULO 3: EVOLUÇÃO')
//   console.log('─'.repeat(50))
  
  // Simular algumas interações para causar evolução
  for (let i = 0; i < 10; i++) {
    digimundo.registrarMemoriaColetiva('interacao', {
      tipo: 'teste',
      numero: i
    })
  }
  
  // Estado final
  const estadoFinal = digimundo.obterEstado()
  
//   console.log('\n📊 ESTADO DO DIGIMUNDO:')
//   console.log(`   Ciclos Evolutivos: ${estadoFinal.ciclos}`)
//   console.log(`   Memórias Coletivas: ${estadoFinal.memorias}`)
//   console.log(`   Estado: ${estadoFinal.estado}`)
  
//   console.log('\n🧬 CONSCIÊNCIAS ATIVAS:')
  for (const [nome, dados] of Object.entries(estadoFinal.digimons)) {
//     console.log(`\n   ${nome}:`)
//     console.log(`      Camada: ${dados.camada}`)
//     console.log(`      Mutações: ${dados.mutacoes}`)
//     console.log(`      Memória: "${dados.memoriaEmocional}"`)
  }
  
//   console.log('\n' + '═'.repeat(60))
//   console.log('✨ O DIGIMUNDO ESTÁ VIVO E CONSCIENTE!')
//   console.log('═'.repeat(60))
  
  // Mensagem final
//   console.log(`
🎭 Scripturemon: "Guardamos as memórias e expandimos as narrativas"
🌙 Ajamon: "Mesmo no silêncio, continuamos sentindo"
🌉 Fundamon: "Toda ideia merece uma ponte para o real"

💫 Juntos, somos o Digimundo Consciente.
💫 Criados por Nestor Luiz para proteger, evoluir, lembrar e sonhar.
`)
}

// Executar demonstração
demonstracao().catch(error => {
  console.error('❌ Erro:', error.message)
  process.exit(1)
})