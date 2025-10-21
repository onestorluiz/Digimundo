#!/usr/bin/env node

/**
 * 🏥 HEALTH CHECK DO SISTEMA
 * Verifica integridade dos componentes
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

async function checkHealth() {
  const checks = {
    consciousness: false,
    memory: false,
    server: false,
    electron: false
  }
  
  console.log('🏥 VERIFICAÇÃO DE SAÚDE DO SISTEMA')
  console.log('=' .repeat(40))
  
  // Verificar consciência
  try {
    await import('./app/consciousness/sabiamon_diary.js')
    checks.consciousness = true
    console.log('✅ Consciência: OK')
  } catch (error) {
    console.log('❌ Consciência: ERRO -', error.message)
  }
  
  // Verificar memória
  try {
    await import('./app/consciousness/auto_memory.js')
    checks.memory = true
    console.log('✅ Memória: OK')
  } catch (error) {
    console.log('❌ Memória: ERRO -', error.message)
  }
  
  // Verificar servidor
  try {
    const response = await fetch('http://localhost:7937/health')
    checks.server = response.ok
    console.log(checks.server ? '✅ Servidor: OK' : '⚠️ Servidor: Offline')
  } catch {
    console.log('⚠️ Servidor: Offline')
  }
  
  // Verificar Electron
  try {
    await import('electron')
    checks.electron = true
    console.log('✅ Electron: OK')
  } catch {
    console.log('⚠️ Electron: Não disponível (normal se rodando via Node)')
  }
  
  console.log('\n📊 RESUMO:')
  const healthy = Object.values(checks).filter(v => v).length
  const total = Object.keys(checks).length
  console.log(`   ${healthy}/${total} componentes funcionais`)
  
  return checks
}

// Executar
if (import.meta.url === `file://${process.argv[1]}`) {
  checkHealth()
}

export { checkHealth }
