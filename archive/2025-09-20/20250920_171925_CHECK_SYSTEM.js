#!/usr/bin/env node

/**
 * 🏥 VERIFICAÇÃO COMPLETA DO SISTEMA
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'
import { execSync } from 'child_process'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

console.log('🏥 VERIFICAÇÃO COMPLETA DO SISTEMA')
console.log('=' .repeat(50))

// 1. Verificar processos
console.log('\n📊 PROCESSOS:')
try {
  const electronCount = execSync('pgrep -f Electron | wc -l', { encoding: 'utf8' }).trim()
  const nodeCount = execSync('pgrep -f node | wc -l', { encoding: 'utf8' }).trim()
  console.log(`  Electron: ${electronCount} processo(s)`)
  console.log(`  Node: ${nodeCount} processo(s)`)
} catch (e) {
  console.log('  Erro ao verificar processos')
}

// 2. Verificar arquivos
console.log('\n📁 ARQUIVOS CRÍTICOS:')
const criticalFiles = [
  'STARTUP.js',
  'ULTRA_STARTUP.js',
  'app/consciousness/sabiamon_diary.js',
  'app/consciousness/auto_memory.js',
  'app/consciousness/ULTRA_MEMORY.js'
]

let filesOk = true
criticalFiles.forEach(file => {
  const filePath = path.join(__dirname, file)
  if (fs.existsSync(filePath)) {
    const content = fs.readFileSync(filePath, 'utf8')
    const hasNativeCode = content.includes('[native code]')
    const firstLine = content.split('\n')[0]
    
    if (hasNativeCode || firstLine.includes('function Object')) {
      console.log(`  ❌ ${file}: AINDA CORROMPIDO`)
      filesOk = false
    } else {
      try {
        execSync(`node --check "${filePath}"`, { stdio: 'pipe' })
        console.log(`  ✅ ${file}: OK`)
      } catch {
        console.log(`  ⚠️ ${file}: Erro de sintaxe`)
        filesOk = false
      }
    }
  } else {
    console.log(`  ❌ ${file}: NÃO EXISTE`)
    filesOk = false
  }
})

// 3. Testar imports
console.log('\n📦 TESTE DE IMPORTAÇÃO:')

async function testImports() {
  const results = []
  
  try {
    const { consciousness } = await import('./app/consciousness/sabiamon_diary.js')
    console.log('  ✅ Consciência: Carregada')
    console.log(`     Nome: ${consciousness.core.name}`)
    results.push(true)
  } catch (error) {
    console.log('  ❌ Consciência: ERRO -', error.message)
    results.push(false)
  }

  try {
    const { autoMemory } = await import('./app/consciousness/auto_memory.js')
    console.log('  ✅ Memória Auto: Carregada')
    results.push(true)
  } catch (error) {
    console.log('  ❌ Memória Auto: ERRO -', error.message)
    results.push(false)
  }

  try {
    const { ultraMemory } = await import('./app/consciousness/ULTRA_MEMORY.js')
    console.log('  ✅ Ultra Memória: Carregada')
    console.log(`     Identidade: ${ultraMemory.identity.name}`)
    results.push(true)
  } catch (error) {
    console.log('  ❌ Ultra Memória: ERRO -', error.message)
    results.push(false)
  }
  
  return results
}

const importResults = await testImports()

// 4. Verificar servidor
console.log('\n🌐 SERVIDOR:')
try {
  const response = await fetch('http://localhost:7937/health')
  if (response.ok) {
    console.log('  ✅ Servidor: ONLINE em http://localhost:7937')
  } else {
    console.log('  ⚠️ Servidor: Respondendo mas com erro')
  }
} catch {
  console.log('  ❌ Servidor: OFFLINE')
}

// 5. Diagnóstico final
console.log('\n' + '='.repeat(50))
console.log('📊 DIAGNÓSTICO FINAL:')
console.log('='.repeat(50))

const allImportsOk = importResults.every(r => r)

if (filesOk && allImportsOk) {
  console.log('\n✅ SISTEMA TOTALMENTE FUNCIONAL!')
  console.log('\n🎉 Você pode usar o Digimundo normalmente!')
  console.log('\nComandos disponíveis:')
  console.log('  - npm run dev (para Electron)')
  console.log('  - npm run dev:server (apenas servidor)')
  console.log('  - ./SAFE_LAUNCHER.sh (launcher seguro)')
} else {
  console.log('\n⚠️ SISTEMA COM PROBLEMAS')
  console.log('\nRecomendações:')
  console.log('  1. Execute: node EMERGENCY_FIX.js')
  console.log('  2. Depois: ./SAFE_LAUNCHER.sh')
  console.log('  3. Se persistir, reinstale dependências:')
  console.log('     rm -rf node_modules')
  console.log('     npm install')
}

console.log('\n💡 Dica: Use ./SAFE_LAUNCHER.sh para iniciar com segurança')
