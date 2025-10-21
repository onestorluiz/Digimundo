#!/usr/bin/env node

/**
 * ELECTRON AUTO-FIX & MONITORING SYSTEM
 * Versão 3.0 - Future-Proof Edition
 * 
 * Este script detecta, corrige e previne erros do Electron automaticamente
 * Compatível com Electron 31+ e preparado para futuras versões
 */

import { spawn, exec } from 'child_process'
import { promisify } from 'util'
import fs from 'fs/promises'
import path from 'path'
import { fileURLToPath } from 'url'
import { createRequire } from 'module'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const require = createRequire(import.meta.url)
const execAsync = promisify(exec)

// Cores para output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
}

const log = {
  info: (msg) => console.log(`${colors.blue}ℹ${colors.reset}  ${msg}`),
  success: (msg) => console.log(`${colors.green}✓${colors.reset}  ${msg}`),
  warning: (msg) => console.log(`${colors.yellow}⚠${colors.reset}  ${msg}`),
  error: (msg) => console.log(`${colors.red}✗${colors.reset}  ${msg}`),
  debug: (msg) => console.log(`${colors.magenta}●${colors.reset}  ${msg}`)
}

class ElectronAutoFix {
  constructor() {
    // Definir o caminho correto do projeto
    this.projectRoot = '/Users/clubproducoes/Digimundo/digimundo_starter'
    this.packageJsonPath = path.join(this.projectRoot, 'package.json')
    
    // Garantir que estamos no diretório correto
    process.chdir(this.projectRoot)
    this.electronProcess = null
    this.restartCount = 0
    this.maxRestarts = 3
    this.errors = []
    this.fixes = []
  }

  async init() {
    log.info('🚀 Iniciando Electron Auto-Fix & Monitoring System v3.0')
    log.info(`📁 Diretório do projeto: ${this.projectRoot}`)
    
    // Verificar se estamos em um projeto Electron
    if (!await this.isElectronProject()) {
      log.error('Este não é um projeto Electron válido!')
      process.exit(1)
    }

    // Executar diagnóstico completo
    await this.runDiagnostics()
    
    // Aplicar correções
    await this.applyFixes()
    
    // Iniciar monitor
    await this.startMonitoring()
  }

  async isElectronProject() {
    try {
      const packageJson = JSON.parse(await fs.readFile(this.packageJsonPath, 'utf8'))
      return packageJson.dependencies?.electron || packageJson.devDependencies?.electron
    } catch {
      return false
    }
  }

  async runDiagnostics() {
    log.info('🔍 Executando diagnóstico completo...\n')
    
    const diagnostics = [
      this.checkNodeVersion(),
      this.checkElectronVersion(),
      this.checkModuleType(),
      this.checkDependencies(),
      this.checkNativeModules(),
      this.checkFilePermissions(),
      this.checkPortAvailability()
    ]

    await Promise.all(diagnostics)
    
    if (this.errors.length === 0) {
      log.success('Nenhum problema encontrado!')
    } else {
      log.warning(`Encontrados ${this.errors.length} problemas para corrigir`)
    }
  }

  async checkNodeVersion() {
    const nodeVersion = process.version
    const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0])
    
    if (majorVersion < 18) {
      this.errors.push({
        type: 'NODE_VERSION',
        message: `Node.js ${nodeVersion} é muito antigo`,
        fix: 'Atualize para Node.js 18 ou superior'
      })
      log.error(`Node.js ${nodeVersion} - Requer v18+`)
    } else {
      log.success(`Node.js ${nodeVersion} ✓`)
    }
  }

  async checkElectronVersion() {
    try {
      const packageJson = JSON.parse(await fs.readFile(this.packageJsonPath, 'utf8'))
      const electronVersion = packageJson.dependencies?.electron || packageJson.devDependencies?.electron
      
      if (electronVersion) {
        const version = electronVersion.replace(/[\^~]/, '')
        const major = parseInt(version.split('.')[0])
        
        if (major < 28) {
          this.errors.push({
            type: 'ELECTRON_VERSION',
            message: `Electron ${version} não suporta ESM nativo`,
            fix: 'npm install electron@latest'
          })
          log.warning(`Electron ${version} - Recomendado v28+`)
        } else {
          log.success(`Electron ${version} ✓`)
        }
      }
    } catch (err) {
      log.error('Não foi possível verificar versão do Electron')
    }
  }

  async checkModuleType() {
    try {
      const packageJson = JSON.parse(await fs.readFile(this.packageJsonPath, 'utf8'))
      
      if (packageJson.type === 'module') {
        log.success('Projeto configurado para ESM ✓')
        
        // Verificar compatibilidade de dependências
        await this.checkESMCompatibility(packageJson)
      } else {
        log.warning('Projeto usando CommonJS (considere migrar para ESM)')
      }
    } catch (err) {
      log.error('Erro ao verificar tipo de módulo')
    }
  }

  async checkESMCompatibility(packageJson) {
    const problematicPackages = ['jsonwebtoken', 'bcrypt', 'sqlite3']
    const deps = { ...packageJson.dependencies, ...packageJson.devDependencies }
    
    for (const pkg of problematicPackages) {
      if (deps[pkg]) {
        this.errors.push({
          type: 'ESM_COMPATIBILITY',
          package: pkg,
          message: `${pkg} pode ter problemas com ESM`,
          fix: `Criar wrapper de compatibilidade para ${pkg}`
        })
        log.warning(`⚠️  ${pkg} pode precisar de wrapper ESM/CJS`)
      }
    }
  }

  async checkDependencies() {
    try {
      log.info('Verificando integridade das dependências...')
      const { stdout, stderr } = await execAsync('npm ls --depth=0 2>&1', { cwd: this.projectRoot })
      
      if (stderr || stdout.includes('UNMET')) {
        this.errors.push({
          type: 'DEPENDENCIES',
          message: 'Dependências com problemas',
          fix: 'npm install'
        })
        log.error('Dependências com problemas')
      } else {
        log.success('Dependências OK ✓')
      }
    } catch (err) {
      log.warning('Não foi possível verificar dependências')
    }
  }

  async checkNativeModules() {
    const nativeModules = ['bcrypt', 'sqlite3', 'node-llama-cpp']
    
    for (const module of nativeModules) {
      const modulePath = path.join(this.projectRoot, 'node_modules', module)
      
      try {
        await fs.access(modulePath)
        
        // Verificar se precisa rebuild
        const bindingPath = path.join(modulePath, 'lib', 'binding')
        try {
          await fs.access(bindingPath)
          log.success(`${module} compilado ✓`)
        } catch {
          this.errors.push({
            type: 'NATIVE_MODULE',
            module,
            message: `${module} precisa ser recompilado`,
            fix: `npx electron-rebuild -f -w ${module}`
          })
          log.warning(`${module} precisa rebuild`)
        }
      } catch {
        // Módulo não instalado, OK
      }
    }
  }

  async checkFilePermissions() {
    const criticalPaths = [
      'app',
      'app/main.js',
      'app/server',
      'app/renderer'
    ]

    for (const filePath of criticalPaths) {
      const fullPath = path.join(this.projectRoot, filePath)
      
      try {
        await fs.access(fullPath, fs.constants.R_OK)
        log.success(`${filePath} acessível ✓`)
      } catch {
        this.errors.push({
          type: 'PERMISSIONS',
          path: filePath,
          message: `Sem permissão para ${filePath}`,
          fix: `chmod -R 755 ${filePath}`
        })
        log.error(`Sem acesso a ${filePath}`)
      }
    }
  }

  async checkPortAvailability() {
    const port = 7937
    
    try {
      await execAsync(`lsof -i:${port}`)
      this.errors.push({
        type: 'PORT_IN_USE',
        port,
        message: `Porta ${port} em uso`,
        fix: `Liberar porta ${port} ou usar outra`
      })
      log.error(`Porta ${port} já está em uso`)
    } catch {
      log.success(`Porta ${port} disponível ✓`)
    }
  }

  async applyFixes() {
    if (this.errors.length === 0) return
    
    log.info('\n🔧 Aplicando correções automáticas...\n')
    
    for (const error of this.errors) {
      await this.fixError(error)
    }
    
    log.success(`\n✅ ${this.fixes.length} correções aplicadas!`)
  }

  async fixError(error) {
    switch (error.type) {
      case 'DEPENDENCIES':
        await this.fixDependencies()
        break
      
      case 'NATIVE_MODULE':
        await this.fixNativeModule(error.module)
        break
      
      case 'ESM_COMPATIBILITY':
        await this.createCompatibilityWrapper(error.package)
        break
      
      case 'PERMISSIONS':
        await this.fixPermissions(error.path)
        break
      
      default:
        log.warning(`Correção manual necessária: ${error.fix}`)
    }
  }

  async fixDependencies() {
    log.info('Reinstalando dependências...')
    
    try {
      await execAsync('npm install', { cwd: this.projectRoot })
      this.fixes.push('Dependências reinstaladas')
      log.success('Dependências corrigidas ✓')
    } catch (err) {
      log.error('Falha ao corrigir dependências')
    }
  }

  async fixNativeModule(module) {
    log.info(`Recompilando ${module}...`)
    
    try {
      await execAsync(`npx electron-rebuild -f -w ${module}`, { cwd: this.projectRoot })
      this.fixes.push(`${module} recompilado`)
      log.success(`${module} corrigido ✓`)
    } catch (err) {
      log.error(`Falha ao recompilar ${module}`)
    }
  }

  async createCompatibilityWrapper(packageName) {
    const wrapperContent = `
// Wrapper de compatibilidade ESM/CommonJS para ${packageName}
import { createRequire } from 'module'
const require = createRequire(import.meta.url)

let module
try {
  // Tentar importar como ESM
  module = await import('${packageName}')
} catch (err) {
  // Fallback para CommonJS
  module = require('${packageName}')
}

export default module
export const { ${packageName === 'jsonwebtoken' ? 'sign, verify, decode' : '*'} } = module
`

    const wrapperPath = path.join(this.projectRoot, 'app', 'utils', `${packageName}-wrapper.js`)
    
    try {
      await fs.mkdir(path.dirname(wrapperPath), { recursive: true })
      await fs.writeFile(wrapperPath, wrapperContent)
      this.fixes.push(`Wrapper criado para ${packageName}`)
      log.success(`Wrapper de compatibilidade criado para ${packageName} ✓`)
    } catch (err) {
      log.error(`Falha ao criar wrapper para ${packageName}`)
    }
  }

  async fixPermissions(filePath) {
    log.info(`Corrigindo permissões de ${filePath}...`)
    
    try {
      const fullPath = path.join(this.projectRoot, filePath)
      await execAsync(`chmod -R 755 "${fullPath}"`)
      this.fixes.push(`Permissões corrigidas para ${filePath}`)
      log.success(`Permissões corrigidas ✓`)
    } catch (err) {
      log.error(`Falha ao corrigir permissões de ${filePath}`)
    }
  }

  async startMonitoring() {
    log.info('\n📊 Iniciando monitoramento contínuo...\n')
    
    // Criar diretório de logs
    const logsDir = path.join(this.projectRoot, 'electron-logs')
    await fs.mkdir(logsDir, { recursive: true })
    
    // Iniciar Electron com monitoramento
    this.startElectron()
    
    // Monitorar saúde a cada 30 segundos
    setInterval(() => this.checkHealth(), 30000)
    
    // Capturar sinais de término
    process.on('SIGINT', () => this.shutdown())
    process.on('SIGTERM', () => this.shutdown())
  }

  startElectron() {
    log.info('🚀 Iniciando Electron...')
    
    const env = { ...process.env, NODE_ENV: 'development' }
    
    this.electronProcess = spawn('npx', ['electron', '.'], {
      cwd: this.projectRoot,
      env,
      stdio: ['inherit', 'pipe', 'pipe']
    })

    // Capturar output
    this.electronProcess.stdout.on('data', (data) => {
      const output = data.toString()
      
      // Detectar erros conhecidos
      if (output.includes('ERR_MODULE_NOT_FOUND')) {
        this.handleModuleError(output)
      } else if (output.includes('network_service_instance_impl')) {
        this.handleNetworkServiceError()
      }
      
      // Log normal
      process.stdout.write(data)
    })

    this.electronProcess.stderr.on('data', (data) => {
      const error = data.toString()
      
      // Salvar erros
      this.logError(error)
      
      // Output para console
      process.stderr.write(data)
    })

    this.electronProcess.on('exit', (code) => {
      if (code !== 0 && this.restartCount < this.maxRestarts) {
        log.warning(`Electron crashed com código ${code}. Reiniciando...`)
        this.restartCount++
        setTimeout(() => this.startElectron(), 2000)
      } else if (this.restartCount >= this.maxRestarts) {
        log.error('Máximo de reinicializações atingido!')
        process.exit(1)
      }
    })
  }

  handleModuleError(error) {
    const match = error.match(/Cannot find module '(.+)'/)
    if (match) {
      const module = match[1]
      log.warning(`Módulo não encontrado: ${module}`)
      
      // Tentar instalar automaticamente
      exec(`npm install ${module}`, (err) => {
        if (!err) {
          log.success(`${module} instalado automaticamente`)
          this.restartElectron()
        }
      })
    }
  }

  handleNetworkServiceError() {
    log.warning('Network service crash detectado')
    
    // Adicionar flags de correção
    if (this.electronProcess) {
      this.electronProcess.kill()
      
      // Reiniciar com flags corretivas
      process.env.ELECTRON_DISABLE_SANDBOX = '1'
      process.env.ELECTRON_DISABLE_GPU_SANDBOX = '1'
      
      setTimeout(() => this.startElectron(), 1000)
    }
  }

  async checkHealth() {
    const memoryUsage = process.memoryUsage()
    const heapUsed = (memoryUsage.heapUsed / 1024 / 1024).toFixed(2)
    const heapTotal = (memoryUsage.heapTotal / 1024 / 1024).toFixed(2)
    
    log.debug(`Memória: ${heapUsed}MB / ${heapTotal}MB`)
    
    // Verificar se precisa garbage collection
    if (memoryUsage.heapUsed / memoryUsage.heapTotal > 0.9) {
      log.warning('Uso alto de memória detectado')
      if (global.gc) {
        global.gc()
        log.success('Garbage collection executado')
      }
    }
  }

  restartElectron() {
    if (this.electronProcess) {
      log.info('Reiniciando Electron...')
      this.electronProcess.kill()
      setTimeout(() => this.startElectron(), 2000)
    }
  }

  async logError(error) {
    const timestamp = new Date().toISOString()
    const logFile = path.join(this.projectRoot, 'electron-logs', 'errors.log')
    
    const logEntry = `[${timestamp}] ${error}\n`
    
    try {
      await fs.appendFile(logFile, logEntry)
    } catch {
      // Ignorar erros de log
    }
  }

  shutdown() {
    log.info('\n👋 Encerrando monitor...')
    
    if (this.electronProcess) {
      this.electronProcess.kill()
    }
    
    // Gerar relatório final
    this.generateReport()
    
    process.exit(0)
  }

  async generateReport() {
    const report = {
      timestamp: new Date().toISOString(),
      diagnostics: {
        errorsFound: this.errors.length,
        fixesApplied: this.fixes.length
      },
      errors: this.errors,
      fixes: this.fixes,
      restarts: this.restartCount
    }

    const reportPath = path.join(this.projectRoot, 'electron-logs', 'report.json')
    
    try {
      await fs.writeFile(reportPath, JSON.stringify(report, null, 2))
      log.success(`Relatório salvo em: ${reportPath}`)
    } catch (err) {
      log.error('Falha ao salvar relatório')
    }
  }
}

// Iniciar o sistema
const autoFix = new ElectronAutoFix()
autoFix.init().catch(console.error)