#!/usr/bin/env node

/**
 * TESTE REAL DO APP - Abre e verifica de verdade
 */

const { spawn, exec } = require('child_process');
const { promisify } = require('util');
const path = require('path');
const fs = require('fs');

const execAsync = promisify(exec);

class RealAppTester {
  constructor() {
    this.appPath = path.join(__dirname, 'release/mac-arm64/Digimundo.app');
    this.errors = [];
    this.appProcess = null;
  }
  
  async test() {
    console.log('🧪 TESTE REAL DO DIGIMUNDO APP');
    console.log('===============================\n');
    
    // 1. Limpar processos antigos
    console.log('1️⃣ Limpando processos antigos...');
    await this.killOldProcesses();
    
    // 2. Verificar se o app existe
    console.log('\n2️⃣ Verificando app bundle...');
    if (!fs.existsSync(this.appPath)) {
      console.error('❌ App não existe! Execute: npm run pack');
      return false;
    }
    console.log('✅ App bundle existe');
    
    // 3. Abrir o app e capturar logs
    console.log('\n3️⃣ Abrindo app e capturando logs...');
    const result = await this.openAppWithLogs();
    
    // 4. Analisar resultado
    console.log('\n4️⃣ Analisando resultado...');
    return this.analyzeResult(result);
  }
  
  async killOldProcesses() {
    try {
      await execAsync('pkill -f Digimundo 2>/dev/null');
    } catch {}
    
    // Aguardar processos terminarem
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  async openAppWithLogs() {
    return new Promise((resolve) => {
      const logs = [];
      const errors = [];
      let startupComplete = false;
      
      // Abrir app capturando saída
      this.appProcess = spawn('open', ['-W', '-n', '-a', this.appPath], {
        env: {
          ...process.env,
          ELECTRON_ENABLE_LOGGING: '1'
        }
      });
      
      // Também tentar capturar logs do Console.app
      const consoleProcess = spawn('log', [
        'stream',
        '--predicate',
        'process == "Digimundo"',
        '--level',
        'debug'
      ]);
      
      consoleProcess.stdout.on('data', (data) => {
        const log = data.toString();
        logs.push(log);
        
        // Detectar erros específicos
        if (log.includes('ERR_REQUIRE_ESM')) {
          errors.push('ES Module error detected');
          console.log('❌ Erro ES Module detectado!');
        }
        
        if (log.includes('Uncaught Exception')) {
          errors.push('Uncaught exception detected');
          console.log('❌ Exception não tratada!');
        }
        
        if (log.includes('successfully started') || log.includes('ready-to-show')) {
          startupComplete = true;
          console.log('✅ App iniciou com sucesso!');
        }
      });
      
      // Timeout de 10 segundos
      setTimeout(() => {
        consoleProcess.kill();
        
        // Verificar se o app está rodando
        exec('pgrep -f "Digimundo.app"', (err, stdout) => {
          const isRunning = !err && stdout.trim();
          
          resolve({
            success: isRunning && errors.length === 0,
            logs,
            errors,
            isRunning,
            startupComplete
          });
        });
      }, 10000);
    });
  }
  
  analyzeResult(result) {
    console.log('\n📊 RESULTADO DO TESTE REAL:');
    console.log('===========================\n');
    
    if (result.errors.length > 0) {
      console.log('❌ ERROS ENCONTRADOS:');
      result.errors.forEach(err => console.log(`   - ${err}`));
      console.log('');
    }
    
    console.log(`App rodando: ${result.isRunning ? '✅ SIM' : '❌ NÃO'}`);
    console.log(`Startup completo: ${result.startupComplete ? '✅ SIM' : '❌ NÃO'}`);
    console.log(`Erros detectados: ${result.errors.length}`);
    
    if (result.success) {
      console.log('\n🎉 APP FUNCIONANDO PERFEITAMENTE!');
      return true;
    } else {
      console.log('\n❌ APP COM PROBLEMAS!');
      
      if (result.errors.some(e => e.includes('ES Module'))) {
        console.log('\n🔧 Correção sugerida:');
        console.log('O erro de ES Module persiste. Vamos tentar:');
        console.log('1. Verificar todas as dependências');
        console.log('2. Usar dynamic imports onde necessário');
        console.log('3. Ou converter todo o projeto para CommonJS');
      }
      
      return false;
    }
  }
  
  async cleanup() {
    if (this.appProcess) {
      this.appProcess.kill();
    }
    await this.killOldProcesses();
  }
}

// Executar teste
async function main() {
  const tester = new RealAppTester();
  
  try {
    const success = await tester.test();
    
    if (!success) {
      console.log('\n🔍 VERIFICANDO LOGS DO SISTEMA...');
      
      // Verificar logs do sistema
      try {
        const { stdout } = await execAsync('tail -50 ~/Library/Logs/Digimundo/*.log 2>/dev/null');
        if (stdout) {
          console.log('\nÚltimos logs do app:');
          console.log(stdout);
        }
      } catch {}
      
      process.exit(1);
    }
  } finally {
    await tester.cleanup();
  }
}

main().catch(console.error);