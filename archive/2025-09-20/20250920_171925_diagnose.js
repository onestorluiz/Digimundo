#!/usr/bin/env node

/**
 * 🩺 DIAGNÓSTICO COMPLETO DO DIGIMUNDO APP
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

console.log('🩺 DIAGNÓSTICO DIGIMUNDO APP');
console.log('==============================\n');

async function diagnose() {
  let issues = [];
  let warnings = [];
  
  // 1. Verificar estrutura de arquivos
  console.log('1️⃣ ESTRUTURA DE ARQUIVOS:');
  
  const requiredFiles = [
    'src/main/electron-main.js',
    'src/main/preload.js',
    'src/renderer/App.tsx',
    'package.json',
    'index.html'
  ];
  
  for (const file of requiredFiles) {
    if (fs.existsSync(file)) {
      console.log(`   ✅ ${file}`);
    } else {
      console.log(`   ❌ ${file} - FALTANDO!`);
      issues.push(`Arquivo faltando: ${file}`);
    }
  }
  
  // 2. Verificar dependências
  console.log('\n2️⃣ DEPENDÊNCIAS:');
  
  const criticalDeps = [
    'electron',
    'electron-store',
    'node-fetch'
  ];
  
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf-8'));
  const allDeps = {
    ...packageJson.dependencies,
    ...packageJson.devDependencies
  };
  
  for (const dep of criticalDeps) {
    if (allDeps[dep]) {
      const moduleExists = fs.existsSync(`node_modules/${dep}`);
      if (moduleExists) {
        console.log(`   ✅ ${dep} v${allDeps[dep]}`);
      } else {
        console.log(`   ❌ ${dep} - Não instalado!`);
        issues.push(`Módulo não instalado: ${dep}`);
      }
    } else {
      console.log(`   ❌ ${dep} - Não está no package.json!`);
      issues.push(`Dependência faltando: ${dep}`);
    }
  }
  
  // 3. Verificar app bundle
  console.log('\n3️⃣ APP BUNDLE:');
  
  const appPath = 'release/mac-arm64/Digimundo.app';
  if (fs.existsSync(appPath)) {
    console.log(`   ✅ Bundle existe`);
    
    // Verificar estrutura interna
    const appFiles = [
      `${appPath}/Contents/MacOS/Digimundo`,
      `${appPath}/Contents/Resources/app/package.json`,
      `${appPath}/Contents/Info.plist`
    ];
    
    for (const file of appFiles) {
      if (fs.existsSync(file)) {
        console.log(`   ✅ ${path.basename(file)}`);
      } else {
        console.log(`   ⚠️ ${path.basename(file)} - Faltando no bundle`);
        warnings.push(`Bundle incompleto: ${path.basename(file)}`);
      }
    }
  } else {
    console.log(`   ❌ Bundle não existe!`);
    issues.push('App bundle não foi criado');
  }
  
  // 4. Verificar renderer build
  console.log('\n4️⃣ RENDERER BUILD:');
  
  if (fs.existsSync('dist/renderer/index.html')) {
    console.log('   ✅ Renderer build existe');
    
    // Verificar se tem JS compilado
    const rendererFiles = fs.readdirSync('dist/renderer/assets/').filter(f => f.endsWith('.js'));
    if (rendererFiles.length > 0) {
      console.log(`   ✅ ${rendererFiles.length} arquivos JS compilados`);
    } else {
      console.log('   ❌ Nenhum JS compilado!');
      issues.push('Renderer não foi compilado');
    }
  } else {
    console.log('   ⚠️ Renderer não foi buildado');
    warnings.push('Execute: npm run build:renderer');
  }
  
  // 5. Testar imports
  console.log('\n5️⃣ VALIDAÇÃO DE IMPORTS:');
  
  try {
    require('./src/main/electron-main.js');
    console.log('   ✅ Main process carrega sem erros');
  } catch (error) {
    console.log('   ❌ Erro no main process:', error.message);
    issues.push(`Main process erro: ${error.message}`);
  }
  
  // 6. Verificar Electron
  console.log('\n6️⃣ ELECTRON:');
  
  try {
    const { stdout } = await execAsync('npx electron --version');
    console.log('   ✅ Electron:', stdout.trim());
  } catch (error) {
    console.log('   ❌ Electron não funciona');
    issues.push('Electron não está funcionando');
  }
  
  // 7. Verificar portas
  console.log('\n7️⃣ PORTAS:');
  
  try {
    const { stdout } = await execAsync('lsof -i :11434 | grep LISTEN');
    console.log('   ⚠️ Ollama já está usando porta 11434');
    warnings.push('Ollama já está rodando');
  } catch {
    console.log('   ✅ Porta 11434 livre para Ollama');
  }
  
  // DIAGNÓSTICO FINAL
  console.log('\n==============================');
  console.log('📊 RESULTADO DO DIAGNÓSTICO:\n');
  
  if (issues.length === 0 && warnings.length === 0) {
    console.log('✅ TUDO OK! O app deveria funcionar.\n');
    console.log('Tente executar:');
    console.log('1. npm run build');
    console.log('2. npm run pack');
    console.log('3. open release/mac-arm64/Digimundo.app');
  } else {
    if (issues.length > 0) {
      console.log('❌ PROBLEMAS CRÍTICOS:');
      issues.forEach(issue => console.log(`   - ${issue}`));
      console.log('');
    }
    
    if (warnings.length > 0) {
      console.log('⚠️ AVISOS:');
      warnings.forEach(warning => console.log(`   - ${warning}`));
      console.log('');
    }
    
    console.log('🔧 CORREÇÕES SUGERIDAS:');
    
    if (issues.some(i => i.includes('não instalado'))) {
      console.log('1. Reinstale dependências:');
      console.log('   rm -rf node_modules package-lock.json');
      console.log('   npm install');
      console.log('');
    }
    
    if (issues.some(i => i.includes('Arquivo faltando'))) {
      console.log('2. Arquivos estão faltando. Verifique a estrutura.');
      console.log('');
    }
    
    if (warnings.some(w => w.includes('Renderer não foi buildado'))) {
      console.log('3. Build o renderer:');
      console.log('   npm run build:renderer');
      console.log('');
    }
    
    if (issues.some(i => i.includes('Bundle'))) {
      console.log('4. Recrie o bundle:');
      console.log('   npm run pack');
      console.log('');
    }
  }
  
  // Comando de correção rápida
  console.log('🚑 CORREÇÃO RÁPIDA (executar tudo):');
  console.log('rm -rf node_modules dist release');
  console.log('npm install');
  console.log('npm run build');
  console.log('npm run pack');
  console.log('open release/mac-arm64/Digimundo.app');
}

diagnose().catch(console.error);