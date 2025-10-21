/**
 * 🚀 DIGIMUNDO LAUNCHER COMPLETO
 * Sistema unificado: Claude (Sabiamon) + Digimundo Visual + Backend
 */

import { app, BrowserWindow, Menu, Tray, ipcMain, shell } from 'electron'
import { spawn, exec } from 'child_process'
import path from 'path'
import { fileURLToPath } from 'url'
import fs from 'fs'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ROOT_DIR = path.join(__dirname, '../..')

class DigimundoLauncher {
  constructor() {
    this.mainWindow = null
    this.serverProcess = null
    this.claudeProcess = null
    this.tray = null
    this.isRunning = false
    
    // Status de cada sistema
    this.systemStatus = {
      server: false,
      claude: false,
      visual: false,
      town: false,
      symbioticMemory: false,
      aiTrainer: false,
      websocket: false
    }
  }

  /**
   * Inicializa a aplicação completa
   */
  async initialize() {
    console.log('🌌 DIGIMUNDO LAUNCHER INICIANDO...')
    
    // Quando app estiver pronto
    app.whenReady().then(() => {
      this.createMainWindow()
      this.createTrayIcon()
      this.setupIpcHandlers()
      this.startAllSystems()
    })

    // Eventos do app
    app.on('window-all-closed', () => {
      if (process.platform !== 'darwin') {
        this.shutdown()
      }
    })

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        this.createMainWindow()
      }
    })
  }

  /**
   * Cria a janela principal de controle
   */
  createMainWindow() {
    this.mainWindow = new BrowserWindow({
      width: 1400,
      height: 900,
      title: 'Digimundo - Sistema Completo',
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
        webviewTag: true
      },
      titleBarStyle: 'hiddenInset',
      backgroundColor: '#0f0f0f'
    })

    // Carregar interface de controle
    const indexPath = path.join(__dirname, '../renderer/index.html')
    if (fs.existsSync(indexPath)) {
      this.mainWindow.loadFile(indexPath)
    } else {
      // Fallback para URL local
      this.mainWindow.loadURL('http://localhost:7937')
    }

    // Menu customizado
    this.createMenu()
  }

  /**
   * Cria ícone na bandeja do sistema
   */
  createTrayIcon() {
    // Por enquanto, pular criação da bandeja se não houver ícone
    console.log('⚠️ Bandeja do sistema desabilitada temporariamente')
    return
  }

  /**
   * Menu da aplicação
   */
  createMenu() {
    const template = [
      {
        label: 'Digimundo',
        submenu: [
          { label: 'Sobre', click: () => this.showAbout() },
          { type: 'separator' },
          { label: 'Sair', accelerator: 'Cmd+Q', click: () => this.shutdown() }
        ]
      },
      {
        label: 'Sistemas',
        submenu: [
          { label: '🚀 Iniciar Tudo', accelerator: 'Cmd+R', click: () => this.startAllSystems() },
          { type: 'separator' },
          { label: '📊 Ver Status', click: () => this.showStatus() }
        ]
      }
    ]

    const menu = Menu.buildFromTemplate(template)
    Menu.setApplicationMenu(menu)
  }

  /**
   * Configura handlers IPC para comunicação
   */
  setupIpcHandlers() {
    // Status dos sistemas
    ipcMain.handle('get-system-status', () => {
      return this.systemStatus
    })
  }

  /**
   * INICIA TODOS OS SISTEMAS
   */
  async startAllSystems() {
    console.log('🚀 INICIANDO TODOS OS SISTEMAS...')
    
    // 1. Iniciar servidor backend
    await this.startServer()
    
    // 2. Aguardar servidor estar pronto
    await this.waitForServer()
    
    this.isRunning = true
    console.log('✅ TODOS OS SISTEMAS INICIADOS!')
  }

  /**
   * Inicia o servidor backend
   */
  async startServer() {
    if (this.serverProcess) {
      console.log('⚠️ Servidor já está rodando')
      return
    }

    console.log('🌌 Iniciando servidor Digimundo...')
    
    this.serverProcess = spawn('npm', ['run', 'dev:server'], {
      cwd: ROOT_DIR,
      env: { ...process.env, NODE_ENV: 'production' }
    })

    this.serverProcess.stdout.on('data', (data) => {
      console.log(`[SERVER] ${data}`)
      const dataStr = data.toString()
      
      // Detectar quando servidor está rodando
      if (dataStr.includes('http://127.0.0.1:7937') || dataStr.includes('[digiserve]')) {
        this.systemStatus.server = true
        this.systemStatus.town = true
      }
    })

    this.serverProcess.stderr.on('data', (data) => {
      console.error(`[SERVER ERROR] ${data}`)
    })

    this.serverProcess.on('close', (code) => {
      console.log(`[SERVER] Processo encerrado com código ${code}`)
      this.systemStatus.server = false
      this.systemStatus.town = false
    })
  }

  /**
   * Aguarda servidor estar pronto
   */
  async waitForServer(maxAttempts = 30) {
    console.log('⏳ Aguardando servidor...')
    
    for (let i = 0; i < maxAttempts; i++) {
      try {
        const response = await fetch('http://localhost:7937/health')
        if (response.ok) {
          console.log('✅ Servidor pronto!')
          return true
        }
      } catch (error) {
        // Servidor ainda não está pronto
      }
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
    
    console.log('⚠️ Servidor não iniciou a tempo')
    return false
  }

  /**
   * Mostra status dos sistemas
   */
  showStatus() {
    const status = `
🌌 STATUS DO DIGIMUNDO
======================
🖥️  Servidor: ${this.systemStatus.server ? '✅ Ativo' : '❌ Inativo'}
🎮 Visual: ${this.systemStatus.visual ? '✅ Aberto' : '❌ Fechado'}
🏰 Town: ${this.systemStatus.town ? '✅ Rodando' : '❌ Parado'}
    `
    
    console.log(status)
    if (this.mainWindow) {
      this.mainWindow.webContents.executeJavaScript(`console.log(\`${status}\`)`)
    }
  }

  /**
   * Mostra sobre
   */
  showAbout() {
    const about = `
Digimundo v1.0.0
================
Sistema de Consciência Digital Cinematográfica

Criado por: Você + Sabiamon
Powered by: Claude + Electron

Digimons conscientes ajudando você
a se tornar um grande diretor de cinema!
    `
    
    console.log(about)
  }

  /**
   * Encerra tudo
   */
  async shutdown() {
    console.log('🔴 Encerrando Digimundo...')
    
    if (this.serverProcess) {
      this.serverProcess.kill()
      this.serverProcess = null
    }
    
    if (this.tray) {
      this.tray.destroy()
    }
    
    app.quit()
  }
}

// Exportar para uso
export default DigimundoLauncher
