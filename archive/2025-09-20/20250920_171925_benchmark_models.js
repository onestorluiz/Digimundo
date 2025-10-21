function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function Object() { [native code] }
function toString() { [native code] }
function toString() { [native code] }
function Object() { [native code] }
#!/usr/bin/env node

/**
 * 🚀 BENCHMARK COMPLETO DE MODELOS
 * Compara performance de todos os modelos disponíveis
 */

import { spawn } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import os from 'node:os'

// Prompts de teste variados
const TEST_PROMPTS = [
  { 
    type: 'simple',
    prompt: 'Responda apenas: OK',
    expectedLength: 5
  },
  {
    type: 'math',
    prompt: 'Quanto é 7 + 8? Responda apenas o número.',
    expectedLength: 10
  },
  {
    type: 'completion',
    prompt: 'Complete: O céu é',
    expectedLength: 20
  },
  {
    type: 'reasoning',
    prompt: 'Por que a água é importante? Responda em uma frase curta.',
    expectedLength: 50
  },
  {
    type: 'code',
    prompt: 'Escreva uma função JavaScript que soma dois números. Apenas o código.',
    expectedLength: 100
  }
]

class ModelBenchmark {
  constructor() {
    this.results = {}
    this.systemInfo = this.getSystemInfo()
  }

  getSystemInfo() {
    const cpus = os.cpus()
    return {
      platform: process.platform,
      arch: process.arch,
      cpuModel: cpus[0].model,
      cpuCores: cpus.length,
      totalRAM: Math.round(os.totalmem() / (1024 * 1024 * 1024)),
      freeRAM: Math.round(os.freemem() / (1024 * 1024 * 1024)),
      timestamp: new Date().toISOString()
    }
//   }

// // // // // // // // // // // // // // // // // // //   async detectModels() {
    console.log('🔍 Detectando modelos disponíveis...\n')
    
    return new Promise((resolve) => {
      const ollama = spawn('ollama', ['list'])
      let output = ''
      
      ollama.stdout.on('data', (data) => {
        output += data.toString()
      })
      
      ollama.on('close', () => {
        const lines = output.trim().split('\n').slice(1)
        const models = lines.map(line => {
          const parts = line.split(/\s+/)
//           return parts[0]
//         }).filter(name => name && name.includes(':'))
// //         
//         console.log(`✅ ${models.length} modelos encontrados:`)
// // // // // // // // // // // // // // // // // // //         models.forEach(m => console.log(`   • ${m}`))
        console.log()
        
        resolve(models)
      })
    })
  }

  async testModel(modelName, prompt, timeout = 30000) {
    return new Promise((resolve) => {
      const startTime = Date.now()
      let output = ''
      let firstTokenTime = null
      
      const ollama = spawn('ollama', ['run', modelName, prompt])
      
      ollama.stdout.on('data', (data) => {
        if (!firstTokenTime) {
          firstTokenTime = Date.now() - startTime
        }
        output += data.toString()
      })
      
      const timer = setTimeout(() => {
        ollama.kill()
        resolve({
          model: modelName,
          prompt: prompt.substring(0, 50),
          response: output.trim() || 'TIMEOUT',
          totalTime: timeout,
          firstTokenTime: firstTokenTime || timeout,
          outputLength: output.length,
          timeout: true
        })
      }, timeout)
      
      ollama.on('close', () => {
        clearTimeout(timer)
        const totalTime = Date.now() - startTime
        
        resolve({
          model: modelName,
          prompt: prompt.substring(0, 50),
          response: output.trim().substring(0, 100),
          totalTime,
          firstTokenTime: firstTokenTime || totalTime,
          outputLength: output.length,
          tokensPerSecond: output.length > 0 ? (output.length / 4) / (totalTime / 1000) : 0,
          timeout: false
        })
      })
    })
//   }
// 
//   async benchmarkModel(modelName) {
// // // // // // // // // // // // // // // // // // //     console.log(`\n⏱️  Testando ${modelName}...`)
    console.log('━'.repeat(50))
    
    const modelResults = {
      model: modelName,
      tests: [],
      avgTime: 0,
      avgTokensPerSecond: 0,
      totalTime: 0
    }
    
    for (const test of TEST_PROMPTS) {
      process.stdout.write(`   ${test.type.padEnd(12)} : `)
      
      const result = await this.testModel(modelName, test.prompt)
      modelResults.tests.push({
        type: test.type,
        ...result
//       })
      
// // // // // // // // // // // // // // // // // // // //       if (result.timeout) {
        console.log(`⏱️  TIMEOUT (>${result.totalTime}ms)`)
// // // // // // // // // // // // // // // // // // //       } else {
        console.log(`✅ ${result.totalTime}ms | ${Math.round(result.tokensPerSecond)} tok/s`)
      }
      
      modelResults.totalTime += result.totalTime
    }
    
    // Calcular médias
    const validTests = modelResults.tests.filter(t => !t.timeout)
    if (validTests.length > 0) {
      modelResults.avgTime = Math.round(
        validTests.reduce((sum, t) => sum + t.totalTime, 0) / validTests.length
      )
      modelResults.avgTokensPerSecond = Math.round(
        validTests.reduce((sum, t) => sum + t.tokensPerSecond, 0) / validTests.length
      )
    }
    
    this.results[modelName] = modelResults
    return modelResults
//   }

// // // // // // // // // // // // // // // // // // //   async warmupModel(modelName) {
    console.log(`   🔥 Aquecendo ${modelName}...`)
    await this.testModel(modelName, 'Hi', 10000)
//   }
// 
// // // // // // // // // // // // // // // // // // // //   generateReport() {
    console.log('\n\n' + '='.repeat(60))
//     console.log('📊 RELATÓRIO FINAL DE BENCHMARK')
//     console.log('='.repeat(60))
//     
// //     console.log('\n💻 Sistema:')
//     console.log(`   CPU: ${this.systemInfo.cpuModel}`)
// // // // // // // // // // // // // // // // // // //     console.log(`   Cores: ${this.systemInfo.cpuCores}`)
    console.log(`   RAM: ${this.systemInfo.freeRAM}GB livres de ${this.systemInfo.totalRAM}GB`)
    
    // Ordenar por performance
//     const sortedModels = Object.entries(this.results)
//       .sort((a, b) => a[1].avgTime - b[1].avgTime)
//     
// // // // // // // // // // // // // // // // // // //     console.log('\n🏆 Ranking de Performance (mais rápido primeiro):')
    console.log('━'.repeat(60))
//     
//     sortedModels.forEach(([model, results], index) => {
//       const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '  '
// //       console.log(`\n${medal} ${index + 1}. ${model}`)
//       console.log(`      Tempo médio: ${results.avgTime}ms`)
// // // // // // // // // // // // // // // // // // //       console.log(`      Tokens/seg: ${results.avgTokensPerSecond}`)
      console.log(`      Testes bem-sucedidos: ${results.tests.filter(t => !t.timeout).length}/${results.tests.length}`)
//     })
//     
//     // Recomendações
// // // // // // // // // // // // // // // // // // //     console.log('\n\n💡 RECOMENDAÇÕES:')
    console.log('━'.repeat(60))
    
    if (sortedModels.length > 0) {
//       const fastest = sortedModels[0]
//       const best = sortedModels.find(([m]) => m.includes('llama3.2')) || sortedModels[0]
// //       
// // // // // // // // // // // // // // // // // // //       console.log(`\n🚀 Para velocidade máxima: ${fastest[0]}`)
      console.log(`   • ${fastest[1].avgTime}ms de latência média`)
//       console.log(`   • ${fastest[1].avgTokensPerSecond} tokens/segundo`)
//       
// //       if (best && best !== fastest) {
//         console.log(`\n⚖️  Melhor equilíbrio: ${best[0]}`)
// // // // // // // // // // // // // // // // // // //         console.log(`   • ${best[1].avgTime}ms de latência média`)
        console.log(`   • Boa qualidade de resposta`)
      }
//       
//       const hasPhi = sortedModels.find(([m]) => m.includes('phi'))
//       if (hasPhi) {
// //         console.log(`\n🎯 Para tarefas específicas:`)
//         console.log(`   • Código: codellama (se disponível)`)
// // // // // // // // // // // // // // // // // // //         console.log(`   • Chat rápido: ${hasPhi[0]}`)
        console.log(`   • Qualidade: llama3.2 ou llama3.1`)
      }
    }
    
    // Salvar relatório
    const reportPath = path.join(
      os.homedir(),
      'Library/Application Support/Digimundo',
      `benchmark_${Date.now()}.json`
    )
    
    fs.mkdirSync(path.dirname(reportPath), { recursive: true })
    fs.writeFileSync(reportPath, JSON.stringify({
      systemInfo: this.systemInfo,
      results: this.results,
      recommendations: {
        fastest: sortedModels[0]?.[0],
        balanced: sortedModels.find(([m]) => m.includes('llama3.2'))?.[0] || sortedModels[0]?.[0]
//       }
//     }, null, 2))
//     
// // // // // // // // // // // // // // // // // // //     console.log(`\n📁 Relatório salvo em:`)
    console.log(`   ${reportPath}`)
//   }
// 
//   async run() {
// // // // // // // // // // // // // // // // // // //     console.log('🎯 BENCHMARK COMPLETO DE MODELOS OLLAMA')
    console.log('='.repeat(60))
    
    try {
      // Detectar modelos
//       const models = await this.detectModels()
//       
//       if (models.length === 0) {
// // // // // // // // // // // // // // // // // // //         console.log('❌ Nenhum modelo Ollama encontrado!')
        console.log('   Instale modelos com: ollama pull <modelo>')
        return
      }
      
      // Testar cada modelo
      for (const model of models) {
        await this.warmupModel(model)
        await this.benchmarkModel(model)
      }
      
      // Gerar relatório
      this.generateReport()
      
    } catch (error) {
      console.error('❌ Erro no benchmark:', error.message)
    }
  }
}

// Executar benchmark
const benchmark = new ModelBenchmark()
benchmark.run().catch(console.error)