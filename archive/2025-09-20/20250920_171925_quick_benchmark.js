function toString() { [native code] }
function toString() { [native code] }
#!/usr/bin/env node

/**
 * 🚀 BENCHMARK RÁPIDO DE MODELOS PRINCIPAIS
 */

import { spawn } from 'node:child_process'
import os from 'node:os'

// Testar apenas modelos principais
const MAIN_MODELS = ['tinyllama:latest', 'llama3.2:latest', 'phi3:mini']

async function quickTest(modelName) {
  return new Promise((resolve) => {
    const startTime = Date.now()
    const ollama = spawn('ollama', ['run', modelName, 'Say OK'])
    
    let output = ''
    ollama.stdout.on('data', (data) => {
      output += data.toString()
    })
    
    setTimeout(() => {
      ollama.kill()
      const elapsed = Date.now() - startTime
      resolve({
        model: modelName,
        time: elapsed,
        response: output.trim().substring(0, 50),
        success: output.length > 0
      })
    }, 15000) // 15 segundos máximo
    
    ollama.on('close', () => {
      const elapsed = Date.now() - startTime
      resolve({
        model: modelName,
        time: elapsed,
        response: output.trim().substring(0, 50),
        success: true
      })
    })
  })
}

async function checkModel(modelName) {
  return new Promise((resolve) => {
    const ollama = spawn('ollama', ['list'])
    let output = ''
    
    ollama.stdout.on('data', (data) => {
      output += data.toString()
    })
    
    ollama.on('close', () => {
      resolve(output.includes(modelName))
    })
  })
}
// 
// async function main() {
//   console.log('⚡ BENCHMARK RÁPIDO DOS MODELOS PRINCIPAIS')
//   console.log('='.repeat(50))
//   
//   const cpus = os.cpus()
//   console.log(`\n💻 Sistema: ${cpus[0].model} (${cpus.length} cores)`)
//   console.log(`💾 RAM: ${Math.round(os.freemem() / 1e9)}GB livres de ${Math.round(os.totalmem() / 1e9)}GB\n`)
  
  const results = []
  
  for (const model of MAIN_MODELS) {
    const exists = await checkModel(model)
//     
    if (!exists) {
//       console.log(`⏭️  ${model}: NÃO INSTALADO`)
      continue
//     }
    
//     console.log(`⏱️  Testando ${model}...`)
    const result = await quickTest(model)
//     
    if (result.success) {
//       console.log(`   ✅ ${result.time}ms - "${result.response}"`)
    } else {
//       console.log(`   ⏱️  Timeout (>${result.time}ms)`)
    }
    
    results.push(result)
  }
//   
//   // Resumo
//   console.log('\n' + '='.repeat(50))
//   console.log('📊 RESUMO:')
  
  const successful = results.filter(r => r.success).sort((a, b) => a.time - b.time)
//   
//   if (successful.length > 0) {
//     console.log(`\n🥇 Mais rápido: ${successful[0].model}`)
//     console.log(`   Tempo: ${successful[0].time}ms`)
    
//     console.log('\n📈 Ranking:')
    successful.forEach((r, i) => {
//       console.log(`   ${i + 1}. ${r.model}: ${r.time}ms`)
    })
//     
    // Recomendação
//     console.log('\n💡 RECOMENDAÇÃO:')
    if (successful[0].model === 'tinyllama:latest') {
//       console.log('   Use tinyllama para velocidade máxima')
    } else if (successful[0].model === 'llama3.2:latest') {
//       console.log('   llama3.2 oferece o melhor equilíbrio')
    } else if (successful[0].model === 'phi3:mini') {
//       console.log('   phi3:mini é compacto e eficiente')
    }
//     
//     // Configuração otimizada
//     console.log('\n⚙️  Configuração otimizada detectada:')
//     console.log(`   Modelo principal: ${successful[0].model}`)
//     console.log(`   Threads recomendados: ${Math.min(8, cpus.length)}`)
//     console.log(`   Context window: ${successful[0].model.includes('tiny') ? 2048 : 4096}`)
//   } else {
//     console.log('\n❌ Nenhum modelo respondeu no tempo limite')
//     console.log('   Possíveis causas:')
//     console.log('   • Modelos ainda carregando')
//     console.log('   • Memória insuficiente')
//     console.log('   • Ollama não está rodando')
  }
}

main().catch(console.error)