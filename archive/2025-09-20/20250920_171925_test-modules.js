#!/usr/bin/env node

/**
 * TESTE RÁPIDO DOS MÓDULOS NATIVOS
 * Verifica se os módulos compilaram corretamente
 */

import { createRequire } from 'module'
const require = createRequire(import.meta.url)

console.log('🔍 TESTANDO MÓDULOS NATIVOS\n')
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')

// Testar bcrypt
console.log('\n1️⃣ Testando bcrypt:')
try {
  const bcrypt = require('bcrypt')
  const hash = bcrypt.hashSync('test', 10)
  const compare = bcrypt.compareSync('test', hash)
  if (compare) {
    console.log('✅ bcrypt funcionando perfeitamente!')
  } else {
    console.log('⚠️ bcrypt carregou mas não funciona corretamente')
  }
} catch (err) {
  console.log('❌ bcrypt com erro:', err.message)
}

// Testar sqlite3
console.log('\n2️⃣ Testando SQLite:')
try {
  // Tentar usar nosso wrapper
  const sqliteModule = await import('./app/utils/sqlite-wrapper.js')
  const { Database, sqliteInfo } = sqliteModule
  
  if (sqliteInfo.available) {
    console.log(`✅ SQLite disponível (usando ${sqliteInfo.module})`)
    
    // Teste básico
    const db = new Database(':memory:')
    console.log('✅ Banco de dados em memória criado')
  } else {
    console.log('❌ Nenhum driver SQLite disponível')
  }
} catch (err) {
  console.log('❌ Erro ao testar SQLite:', err.message)
}

// Testar jsonwebtoken
console.log('\n3️⃣ Testando jsonwebtoken:')
try {
  const jwt = require('jsonwebtoken')
  const token = jwt.sign({ test: true }, 'secret')
  const decoded = jwt.verify(token, 'secret')
  if (decoded.test === true) {
    console.log('✅ jsonwebtoken funcionando!')
  }
} catch (err) {
  console.log('❌ jsonwebtoken com erro:', err.message)
}

// Testar node-llama-cpp (opcional)
console.log('\n4️⃣ Testando node-llama-cpp (opcional):')
try {
  require('node-llama-cpp')
  console.log('✅ node-llama-cpp disponível')
} catch (err) {
  console.log('⚠️ node-llama-cpp não instalado (opcional)')
}

// Verificar Electron
console.log('\n5️⃣ Verificando Electron:')
try {
  const electronPath = require.resolve('electron')
  console.log('✅ Electron encontrado em:', electronPath)
  
  // Verificar versão
  const { version } = require('electron/package.json')
  console.log(`✅ Electron versão: ${version}`)
} catch (err) {
  console.log('❌ Electron não encontrado:', err.message)
}

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
console.log('✅ Teste concluído!\n')

// Resumo
console.log('📊 RESUMO:')
console.log('Use o comando abaixo para iniciar o Electron:')
console.log('\n  npm run dev')
console.log('\nOu use o monitor:')
console.log('\n  ./run-electron-fix.sh')
console.log('')
