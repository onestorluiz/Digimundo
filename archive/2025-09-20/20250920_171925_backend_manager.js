/**
 * 🔧 BACKEND MANAGER - DIGIMUNDO
 * Gerencia o servidor backend em processo separado
 */

const { spawn } = require('child_process');
const path = require('path');
const EventEmitter = require('events');
const fetch = require('node-fetch');

class BackendManager extends EventEmitter {
  constructor() {
    super();
    this.serverProcess = null;
    this.isRunning = false;
    this.port = process.env.DIGIMUNDO_PORT || 7937;
    this.retryCount = 0;
    this.maxRetries = 5;
  }

  /**
   * Inicia o servidor backend em processo separado
   */
  async start() {
    if (this.isRunning) {
      console.log('⚠️ Backend já está rodando');
      return true;
    }

    console.log('🚀 Iniciando servidor backend...');
    
    const serverPath = path.join(__dirname, '../server/index.js');
    
    // Spawn servidor como processo filho
    this.serverProcess = spawn('node', [
      '--expose-gc',
      '--max-old-space-size=2048',
      serverPath
    ], {
      env: {
        ...process.env,
        NODE_ENV: 'production',
        PORT: this.port,
        ELECTRON_RUN_AS_NODE: '1'
      },
      detached: false,
      stdio: ['ignore', 'pipe', 'pipe']
    });

    // Capturar logs do servidor
    this.serverProcess.stdout.on('data', (data) => {
      console.log(`[Backend]: ${data.toString()}`);
      this.emit('log', { level: 'info', message: data.toString() });
    });

    this.serverProcess.stderr.on('data', (data) => {
      console.error(`[Backend Error]: ${data.toString()}`);
      this.emit('log', { level: 'error', message: data.toString() });
    });

    // Monitorar término do processo
    this.serverProcess.on('exit', (code) => {
      console.log(`Backend terminou com código: ${code}`);
      this.isRunning = false;
      this.emit('exit', code);
      
      // Auto-restart se crashar
      if (code !== 0 && this.retryCount < this.maxRetries) {
        this.retryCount++;
        console.log(`🔄 Tentando reiniciar backend (${this.retryCount}/${this.maxRetries})...`);
        setTimeout(() => this.start(), 2000);
      }
    });

    // Aguardar servidor estar pronto
    const isReady = await this.waitForServer();
    
    if (isReady) {
      this.isRunning = true;
      this.retryCount = 0;
      this.emit('ready');
      console.log('✅ Backend iniciado com sucesso!');
    }
    
    return isReady;
  }

  /**
   * Aguarda servidor estar pronto
   */
  async waitForServer(maxAttempts = 30) {
    for (let i = 0; i < maxAttempts; i++) {
      try {
        const response = await fetch(`http://localhost:${this.port}/health`);
        if (response.ok) {
          return true;
        }
      } catch (e) {
        // Servidor ainda não está pronto
      }
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    return false;
  }

  /**
   * Para o servidor backend
   */
  async stop() {
    if (!this.serverProcess) {
      return;
    }

    console.log('🛑 Parando servidor backend...');
    
    return new Promise((resolve) => {
      // Tentar shutdown gracioso primeiro
      this.serverProcess.once('exit', () => {
        this.isRunning = false;
        this.serverProcess = null;
        console.log('✅ Backend parado');
        resolve();
      });

      // Enviar SIGTERM
      this.serverProcess.kill('SIGTERM');
      
      // Forçar kill após 5 segundos se não parar
      setTimeout(() => {
        if (this.serverProcess) {
          this.serverProcess.kill('SIGKILL');
        }
      }, 5000);
    });
  }

  /**
   * Reinicia o servidor backend
   */
  async restart() {
    console.log('🔄 Reiniciando backend...');
    await this.stop();
    await new Promise(resolve => setTimeout(resolve, 1000));
    return await this.start();
  }

  /**
   * Verifica status do servidor
   */
  async checkHealth() {
    try {
      const response = await fetch(`http://localhost:${this.port}/health`);
      return response.ok;
    } catch (e) {
      return false;
    }
  }

  /**
   * Obtém estatísticas de memória
   */
  async getMemoryStats() {
    try {
      const response = await fetch(`http://localhost:${this.port}/api/memory/stats`);
      if (response.ok) {
        return await response.json();
      }
    } catch (e) {
      console.error('Erro ao obter stats de memória:', e);
    }
    return null;
  }
}

module.exports = BackendManager;