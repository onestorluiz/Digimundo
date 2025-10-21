const { app, BrowserWindow, Menu, Tray, nativeImage, shell, ipcMain, dialog } = require('electron');
const path = require('path');
const { fileURLToPath } = require('url');
const StartupOptimizer = require('./startup-optimizer');
const { getTracing } = require('./tracing');
const { getResilienceOrchestrator } = require('./resilience-layer');
const { getAutoRecovery } = require('./auto-recovery');
const isDev = process.env.NODE_ENV === 'development';

// Initialize startup optimizer and tracing
const optimizer = new StartupOptimizer();
optimizer.applyAllOptimizations();
const tracing = getTracing();

// Lazy load heavy modules
const ClaudeIntegration = optimizer.lazyLoad('claude-integration', () => require('./claude-integration'));
const OllamaManager = optimizer.lazyLoad('ollama-manager', () => require('./ollama-manager'));
const DigimundoMonitor = optimizer.lazyLoad('monitoring', () => require('./monitoring'));

// Store global para preferências
const Store = require('electron-store');
const store = new Store({
  name: 'digimundo-config',
  defaults: {
    theme: 'system',
    alwaysOnTop: false,
    startMinimized: false,
    enableNotifications: true,
    selectedModel: 'llama3.2:3b',
    conversationHistory: []
  }
});

class DigimundoApp {
  constructor() {
    this.mainWindow = null;
    this.tray = null;
    this.isQuitting = false;
    this.optimizer = optimizer;
    this.tracing = tracing;
    this.resilience = getResilienceOrchestrator();
    this.recovery = getAutoRecovery();
    this.startupSpan = null;
    
    // Setup resilience health checks and auto-recovery
    this.setupHealthChecks();
    this.setupAutoRecovery();
    
    // Initialize tracing first
    this.initializeTracing();
    
    // Critical path - must be fast
    this.setupSingleInstance();
    this.setupAppHandlers();
    
    // Defer non-critical initialization
    this.optimizer.defer('monitor-init', () => {
      this.monitor = new DigimundoMonitor();
      this.monitor.log('info', 'MAIN', 'Digimundo started');
    }, 100);
    
    this.optimizer.defer('claude-init', () => {
      this.claude = new ClaudeIntegration();
    }, 200);
    
    this.optimizer.defer('ollama-init', () => {
      this.ollama = new OllamaManager(this.monitor);
      return this.startOllama();
    }, 500);
    
    this.optimizer.defer('cleanup-logs', () => {
      if (this.monitor?.cleanOldLogs) {
        this.monitor.cleanOldLogs();
      }
    }, 1000);
    
    // Setup IPC after critical path
    this.setupIPC();
  }
  
  async initializeTracing() {
    await this.tracing.initialize();
    this.startupSpan = this.tracing.traceStartup();
    this.optimizer.measureStartupTime('tracing-initialized');
  }
  
  setupHealthChecks() {
    // Add health checks for critical components
    this.resilience.addHealthCheck('ollama', async () => {
      try {
        const response = await fetch('http://localhost:11434/api/tags');
        return response.ok;
      } catch {
        return false;
      }
    }, 10000);
    
    this.resilience.addHealthCheck('renderer', () => {
      return this.mainWindow && !this.mainWindow.isDestroyed();
    }, 5000);
    
    this.resilience.addHealthCheck('memory', () => {
      const usage = process.memoryUsage();
      return usage.heapUsed < 500 * 1024 * 1024; // Less than 500MB
    }, 30000);
  }
  
  setupAutoRecovery() {
    // Register Ollama for auto-recovery
    this.recovery.registerComponent('ollama', {
      command: 'ollama',
      args: ['serve'],
      critical: true,
      autoRestart: true,
      healthCheck: async () => {
        try {
          const response = await fetch('http://localhost:11434/api/tags');
          return response.ok;
        } catch {
          return false;
        }
      }
    });
    
    // Listen to recovery events
    this.recovery.on('component-failed', (event) => {
      console.log(`🚨 Component failed: ${event.component}`);
      if (this.monitor) {
        this.monitor.log('error', 'AUTO_RECOVERY', `Component failed: ${event.component}`, { reason: event.reason });
      }
    });
    
    this.recovery.on('component-recovered', (event) => {
      console.log(`✅ Component recovered: ${event.component}`);
      if (this.monitor) {
        this.monitor.log('info', 'AUTO_RECOVERY', `Component recovered: ${event.component}`, { restarts: event.restartCount });
      }
    });
    
    this.recovery.on('critical-failure', (event) => {
      console.error(`💀 Critical failure: ${event.component} - ${event.reason}`);
      // Show user notification
      if (this.mainWindow) {
        this.mainWindow.webContents.send('critical-error', {
          component: event.component,
          reason: event.reason
        });
      }
    });
  }
  
  async startOllama() {
    const startTime = Date.now();
    this.monitor.log('info', 'OLLAMA', 'Starting Ollama automatically...');
    
    // Use resilience orchestrator for fault tolerance
    return await this.resilience.executeWithResilience('ollama-start', async () => {
      try {
      const started = await this.ollama.start();
      const duration = Date.now() - startTime;
      
      if (started) {
        this.monitor.trackOllamaOperation('start', true, duration);
        this.monitor.trackStartup('ollama', duration);
        
        // Notifica o renderer
        if (this.mainWindow) {
          this.mainWindow.webContents.send('ollama-status', { running: true });
        }
      } else {
        this.monitor.trackOllamaOperation('start', false, duration);
      }
      } catch (error) {
        this.monitor.trackError('OLLAMA', error, { operation: 'start' });
        throw error;
      }
    }, {
      retry: true,
      retryOptions: { maxAttempts: 3, delay: 2000 },
      circuitBreaker: true,
      fallback: async () => {
        console.log('⚠️ Ollama start failed, using offline mode');
        return false;
      }
    });
  }

  setupSingleInstance() {
    const gotTheLock = app.requestSingleInstanceLock();
    
    if (!gotTheLock) {
      app.quit();
    } else {
      app.on('second-instance', () => {
        if (this.mainWindow) {
          if (this.mainWindow.isMinimized()) this.mainWindow.restore();
          this.mainWindow.focus();
        }
      });
    }
  }

  setupAppHandlers() {
    app.whenReady().then(async () => {
      this.optimizer.measureStartupTime('app-ready');
      
      // Critical: Create window first
      await this.tracing.tracePhase(this.startupSpan?.span, 'window-creation', () => {
        this.createWindow();
        this.optimizer.measureStartupTime('window-created');
      });
      
      // Defer non-critical UI elements
      this.optimizer.defer('create-tray', () => this.createTray(), 100);
      this.optimizer.defer('create-menu', () => this.createMenu(), 200);
      
      // Execute deferred tasks
      this.optimizer.defer('execute-deferred', () => {
        return this.optimizer.executeDeferredTasks();
      }, 300);
    });

    app.on('window-all-closed', () => {
      if (process.platform !== 'darwin') {
        app.quit();
      }
    });

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        this.createWindow();
      }
    });

    app.on('before-quit', async () => {
      this.isQuitting = true;
      
      // Para o Ollama ao fechar o app
      if (this.ollama) {
        console.log('🛑 Encerrando Ollama...');
        this.ollama.stop();
      }
      
      // Shutdown tracing
      await this.tracing.shutdown();
    });
  }

  createWindow() {
    const windowConfig = this.optimizer.getOptimizedWindowConfig();
    
    // Add sandbox and context isolation for security
    windowConfig.webPreferences.sandbox = true;
    windowConfig.webPreferences.contextIsolation = true;
    
    this.mainWindow = new BrowserWindow({
      ...windowConfig,
      title: 'Digimundo',
      icon: path.join(__dirname, '../../assets/icon.png')
    });

    // Load the app
    if (isDev && process.env.VITE_DEV_SERVER_URL) {
      this.mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL);
      this.mainWindow.webContents.openDevTools();
    } else {
      this.mainWindow.loadFile(path.join(__dirname, '../../dist/renderer/index.html'));
      // Abrir DevTools para debug
      this.mainWindow.webContents.openDevTools();
    }

    // Optimize renderer
    this.optimizer.optimizeRenderer(this.mainWindow);
    
    // Window events
    this.mainWindow.once('ready-to-show', () => {
      this.optimizer.measureStartupTime('window-ready');
      this.mainWindow.show();
      
      // End startup trace
      if (this.startupSpan) {
        const metrics = this.optimizer.getMetrics();
        this.startupSpan.end({
          'startup.total_ms': metrics.total,
          'startup.grade': metrics.grade,
          'startup.within_budget': metrics.withinBudget
        });
      }
      
      // Apply saved preferences after show
      setTimeout(() => {
        const alwaysOnTop = store.get('alwaysOnTop');
        if (alwaysOnTop) {
          this.mainWindow.setAlwaysOnTop(true);
        }
      }, 100);
    });

    this.mainWindow.on('close', (event) => {
      if (!this.isQuitting && process.platform === 'darwin') {
        event.preventDefault();
        this.mainWindow.hide();
      }
    });

    this.mainWindow.on('closed', () => {
      this.mainWindow = null;
    });
  }

  createTray() {
    try {
      const icon = nativeImage.createFromPath(
        path.join(__dirname, '../../assets/icon.png')
      );
      
      if (!icon.isEmpty()) {
        this.tray = new Tray(icon.resize({ width: 16, height: 16 }));
        this.tray.setToolTip('Digimundo');
        
        const contextMenu = Menu.buildFromTemplate([
          {
            label: 'Show App',
            click: () => {
              this.mainWindow.show();
            }
          },
          { type: 'separator' },
          {
            label: 'Quit',
            click: () => {
              this.isQuitting = true;
              app.quit();
            }
          }
        ]);
        
        this.tray.setContextMenu(contextMenu);
        
        this.tray.on('click', () => {
          if (this.mainWindow.isVisible()) {
            this.mainWindow.hide();
          } else {
            this.mainWindow.show();
          }
        });
      }
    } catch (error) {
      console.warn('Could not create tray icon:', error);
    }
  }

  createMenu() {
    const template = [
      {
        label: 'Digimundo',
        submenu: [
          {
            label: 'About Digimundo',
            click: () => {
              dialog.showMessageBox(this.mainWindow, {
                type: 'info',
                title: 'About Digimundo',
                message: 'Digimundo v2.0.0',
                detail: 'Your AI-powered creative companion with multiple Digimon personalities.',
                buttons: ['OK']
              });
            }
          },
          { type: 'separator' },
          {
            label: 'Preferences',
            accelerator: 'CmdOrCtrl+,',
            click: () => {
              this.mainWindow.webContents.send('open-preferences');
            }
          },
          { type: 'separator' },
          {
            label: 'Quit',
            accelerator: 'CmdOrCtrl+Q',
            click: () => {
              this.isQuitting = true;
              app.quit();
            }
          }
        ]
      },
      {
        label: 'Edit',
        submenu: [
          { role: 'undo' },
          { role: 'redo' },
          { type: 'separator' },
          { role: 'cut' },
          { role: 'copy' },
          { role: 'paste' },
          { role: 'selectAll' }
        ]
      },
      {
        label: 'View',
        submenu: [
          { role: 'reload' },
          { role: 'forceReload' },
          { role: 'toggleDevTools' },
          { type: 'separator' },
          { role: 'resetZoom' },
          { role: 'zoomIn' },
          { role: 'zoomOut' },
          { type: 'separator' },
          { role: 'togglefullscreen' },
          { type: 'separator' },
          {
            label: 'Always on Top',
            type: 'checkbox',
            checked: store.get('alwaysOnTop'),
            click: (menuItem) => {
              store.set('alwaysOnTop', menuItem.checked);
              this.mainWindow.setAlwaysOnTop(menuItem.checked);
            }
          }
        ]
      },
      {
        label: 'Tools',
        submenu: [
          {
            label: 'Open Claude Code',
            accelerator: 'CmdOrCtrl+Shift+C',
            click: async () => {
              try {
                await this.claude.openClaude({
                  projectPath: app.getPath('userData'),
                  message: 'Digimundo integration ready'
                });
              } catch (error) {
                dialog.showErrorBox('Claude Code', error.message);
              }
            }
          },
          { type: 'separator' },
          {
            label: 'Claude Status',
            click: async () => {
              const status = await this.claude.checkSession();
              dialog.showMessageBox(this.mainWindow, {
                type: 'info',
                title: 'Claude Code Status',
                message: this.claude.isAvailable ? 'Claude Code Available' : 'Claude Code Not Found',
                detail: `Path: ${this.claude.claudePath || 'Not installed'}\nSession: ${status ? 'Active' : 'Not logged in'}`,
                buttons: ['OK']
              });
            }
          }
        ]
      },
      {
        label: 'Help',
        submenu: [
          {
            label: 'Documentation',
            click: () => {
              shell.openExternal('https://github.com/clubproducoes/digimundo');
            }
          },
          {
            label: 'Report Issue',
            click: () => {
              shell.openExternal('https://github.com/clubproducoes/digimundo/issues');
            }
          }
        ]
      }
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
  }

  setupIPC() {
    // Store operations with circuit breakers
    ipcMain.handle('store:get', async (_, key) => {
      return await this.resilience.executeWithResilience('store-get', 
        () => store.get(key),
        { circuitBreaker: true, retry: false, fallback: () => null }
      );
    });
    
    ipcMain.handle('store:set', async (_, key, value) => {
      return await this.resilience.executeWithResilience('store-set',
        () => store.set(key, value),
        { circuitBreaker: true, retry: true, retryOptions: { maxAttempts: 2 } }
      );
    });
    
    ipcMain.handle('store:delete', async (_, key) => {
      return await this.resilience.executeWithResilience('store-delete',
        () => store.delete(key),
        { circuitBreaker: true, retry: false }
      );
    });

    // File operations
    ipcMain.handle('dialog:openFile', async () => {
      const result = await dialog.showOpenDialog(this.mainWindow, {
        properties: ['openFile'],
        filters: [
          { name: 'JSON', extensions: ['json'] },
          { name: 'All Files', extensions: ['*'] }
        ]
      });

      if (!result.canceled) {
        const fs = require('fs');
        const data = JSON.parse(fs.readFileSync(result.filePaths[0], 'utf-8'));
        return data;
      }
      return null;
    });

    // Ollama integration com auto-start
    ipcMain.handle('ollama:check', async () => {
      return await this.ollama.checkIfRunning();
    });

    ipcMain.handle('ollama:models', async () => {
      return await this.resilience.executeWithResilience('ollama-models',
        () => this.ollama.listModels(),
        {
          circuitBreaker: true,
          retry: true,
          retryOptions: { maxAttempts: 2 },
          fallback: () => [{ name: 'llama3.2:3b', size: 'N/A', cached: true }]
        }
      );
    });

    ipcMain.handle('ollama:generate', async (_, prompt, model) => {
      const startTime = Date.now();
      
      return await this.resilience.executeWithResilience('ollama-generate', async () => {
        try {
          // Garante que Ollama está rodando antes de gerar
          if (!this.ollama.isRunning) {
            await this.ollama.start();
          }
          const result = await this.ollama.generate(prompt, model);
          const duration = Date.now() - startTime;
          
          this.monitor.trackOllamaOperation('generate', true, duration, { model });
          this.monitor.trackPerformance('responseTime', duration);
          
          return result;
        } catch (error) {
          const duration = Date.now() - startTime;
          this.monitor.trackOllamaOperation('generate', false, duration, { model, error: error.message });
          this.monitor.trackError('OLLAMA', error, { operation: 'generate', model });
          throw error;
        }
      }, {
        circuitBreaker: true,
        retry: true,
        retryOptions: { maxAttempts: 3, delay: 1000 },
        bulkhead: true,
        bulkheadOptions: { maxConcurrent: 5, queueSize: 10 },
        fallback: async () => ({
          response: 'AI service temporarily unavailable. Please try again.',
          cached: true,
          model: 'fallback'
        })
      });
    });
    
    ipcMain.handle('ollama:status', async () => {
      return await this.ollama.getStatus();
    });
    
    ipcMain.handle('ollama:start', async () => {
      return await this.ollama.start();
    });
    
    ipcMain.handle('ollama:stop', async () => {
      this.ollama.stop();
      return true;
    });
    
    ipcMain.handle('ollama:restart', async () => {
      return await this.ollama.restart();
    });

    ipcMain.handle('ollama:chat', async (_, prompt, model) => {
      return await this.resilience.executeWithResilience('ollama-chat', async () => {
        const response = await fetch('http://localhost:11434/api/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            model: model || 'llama3.2:3b',
            prompt,
            stream: false
          })
        });
        const data = await response.json();
        return data.response;
      }, {
        circuitBreaker: true,
        retry: true,
        retryOptions: { maxAttempts: 2, delay: 500 },
        fallback: () => 'Chat service temporarily unavailable'
      });
    });

    // Claude Code integration
    ipcMain.handle('claude:status', async () => {
      return {
        available: this.claude.isAvailable,
        path: this.claude.claudePath,
        sessionActive: this.claude.sessionActive
      };
    });

    ipcMain.handle('claude:open', async (_, options) => {
      try {
        await this.claude.openClaude(options);
        return { success: true };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    ipcMain.handle('claude:send', async (_, prompt) => {
      try {
        const response = await this.claude.sendToClaude(prompt);
        return { success: true, response };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    ipcMain.handle('claude:install', async () => {
      try {
        const installed = await this.claude.installClaudeIfNeeded();
        return { success: installed };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    // Window controls
    ipcMain.handle('window:minimize', () => {
      if (this.mainWindow) this.mainWindow.minimize();
    });

    ipcMain.handle('window:maximize', () => {
      if (this.mainWindow) {
        if (this.mainWindow.isMaximized()) {
          this.mainWindow.unmaximize();
        } else {
          this.mainWindow.maximize();
        }
      }
    });

    ipcMain.handle('window:close', () => {
      if (this.mainWindow) this.mainWindow.close();
    });

    // App info
    ipcMain.handle('app:version', () => app.getVersion());
    ipcMain.handle('app:name', () => app.getName());
    
    // Endpoints de monitoramento
    ipcMain.handle('monitor:health', () => {
      return this.monitor.getHealthStatus();
    });
    
    ipcMain.handle('monitor:report', () => {
      return this.monitor.generateReport();
    });
    
    ipcMain.handle('monitor:metrics', () => {
      return this.monitor.metrics;
    });

    ipcMain.handle('dialog:saveFile', async (_, data) => {
      const result = await dialog.showSaveDialog(this.mainWindow, {
        defaultPath: `digimundo-export-${Date.now()}.json`,
        filters: [
          { name: 'JSON', extensions: ['json'] }
        ]
      });

      if (!result.canceled) {
        const fs = require('fs');
        fs.writeFileSync(result.filePath, JSON.stringify(data, null, 2));
        return true;
      }
      return false;
    });
  }
}

// Create and start the app instance
new DigimundoApp();

module.exports = DigimundoApp;