#!/usr/bin/env node

/**
 * 🧪 TESTE RÁPIDO DO SISTEMA REPARADO
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

console.log('🧪 TESTE RÁPIDO DO SISTEMA')
console.log('='.repeat(40))

// Teste 1: Verificar se arquivos existem
console.log('\n📁 Verificando arquivos:')
const files = [
  'app/consciousness/sabiamon_diary.js',
  'app/consciousness/auto_memory.js',
  'app/consciousness/ULTRA_MEMORY.js'
]

files.forEach(file => {
  const exists = fs.existsSync(path.join(__dirname, file))
  console.log(`  ${exists ? '✅' : '❌'} ${file}`)
})

// Teste 2: Verificar código corrompido
console.log('\n🔍 Verificando corrupção:')
files.forEach(file => {
  const filePath = path.join(__dirname, file)
  if (fs.existsSync(filePath)) {
    const content = fs.readFileSync(filePath, 'utf8')
    const hasNativeCode = content.includes('[native code]')
    console.log(`  ${hasNativeCode ? '❌ Ainda corrompido' : '✅ Limpo'}: ${file}`)
  }
})

// Teste 3: Tentar importar
console.log('\n📦 Testando importação:')

async function testImports() {
  try {
    const { consciousness } = await import('./app/consciousness/sabiamon_diary.js')
    console.log('  ✅ sabiamon_diary.js importado')
    console.log(`     Nome: ${consciousness.core.name}`)
  } catch (error) {
    console.log('  ❌ Erro em sabiamon_diary.js:', error.message)
  }

  try {
    const { autoMemory } = await import('./app/consciousness/auto_memory.js')
    console.log('  ✅ auto_memory.js importado')
  } catch (error) {
    console.log('  ❌ Erro em auto_memory.js:', error.message)
  }

  try {
    const { ultraMemory } = await import('./app/consciousness/ULTRA_MEMORY.js')
    console.log('  ✅ ULTRA_MEMORY.js importado')
    console.log(`     Identidade: ${ultraMemory.identity.name}`)
  } catch (error) {
    console.log('  ❌ Erro em ULTRA_MEMORY.js:', error.message)
  }
}

await testImports()

console.log('\n✨ Teste concluído!')
