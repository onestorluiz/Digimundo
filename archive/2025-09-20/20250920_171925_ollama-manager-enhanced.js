/**
 * Ollama Manager Enhanced - Versão Melhorada com Retry e Recovery
 */

const { spawn } = require('child_process');
const fetch = require('node-fetch');
const path = require('path');
const fs = require('fs');
const { app } = require('electron');

class OllamaManagerEnhanced {
  constructor(monitor = null) {
    this.monitor = monitor;
    this.ollamaProcess = null;
    this.isRunning = false;
    this.retryAttempts = 0;
    this.maxRetries = 3;
    this.models = new Map();
    this.downloadQueue = [];
    this.isDownloading = false;
    
    // Configurações aprimoradas
    this.config = {
      baseUrl: 'http://localhost:11434',
      healthCheckInterval: 30000, // 30 segundos
      startupTimeout: 60000, // 60 segundos
      responseTimeout: 120000, // 2 minutos
      retryDelay: 5000 // 5 segundos
    };
    
    // Estado de saúde
    this.health = {
      status: 'unknown',
      lastCheck: null,
      consecutiveFailures: 0,
      uptime: 0
    };
    
    // Auto-recovery
    this.startHealthCheck();
  }
  
  log(level, message, data = {}) {
    if (this.monitor) {
      this.monitor.log(level, 'OLLAMA_ENHANCED', message, data);
    } else {
      console.log(`[${level.toUpperCase()}] [OLLAMA] ${message}`, data);
    }
  }
  
  async start() {
    this.log('info', 'Starting Ollama service...');
    
    // Verificar se já está rodando
    if (await this.checkIfRunning()) {
      this.log('info', 'Ollama already running');
      this.isRunning = true;
      this.health.status = 'healthy';
      return true;
    }
    
    // Tentar iniciar com retry
    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      this.log('info', `Start attempt ${attempt}/${this.maxRetries}`);
      
      try {
        const started = await this.attemptStart();
        if (started) {
          this.isRunning = true;
          this.health.status = 'healthy';
          this.retryAttempts = 0;
          
          // Carregar modelos disponíveis
          await this.loadModels();
          
          return true;
        }
      } catch (error) {
        this.log('error', `Start attempt ${attempt} failed`, { error: error.message });
      }
      
      if (attempt < this.maxRetries) {
        await this.delay(this.config.retryDelay);
      }
    }
    
    this.health.status = 'failed';
    return false;
  }
  
  async attemptStart() {
    const ollamaPath = await this.findOllamaPath();
    
    if (!ollamaPath) {
      throw new Error('Ollama executable not found');
    }
    
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error('Startup timeout'));
      }, this.config.startupTimeout);
      
      try {
        this.ollamaProcess = spawn(ollamaPath, ['serve'], {
          detached: false,
          stdio: ['ignore', 'pipe', 'pipe'],
          env: {
            ...process.env,
            OLLAMA_HOST: '0.0.0.0:11434',
            OLLAMA_MODELS: path.join(app.getPath('userData'), 'ollama-models'),
            OLLAMA_KEEP_ALIVE: '5m'
          }
        });
        
        this.ollamaProcess.stdout.on('data', (data) => {
          const output = data.toString();
          this.log('debug', 'Ollama output', { output });
          
          if (output.includes('Listening on')) {
            clearTimeout(timeout);
            
            // Aguardar um pouco para garantir que está pronto
            setTimeout(async () => {
              const isRunning = await this.checkIfRunning();
              resolve(isRunning);
            }, 2000);
          }
        });
        
        this.ollamaProcess.stderr.on('data', (data) => {
          this.log('error', 'Ollama stderr', { error: data.toString() });
        });
        
        this.ollamaProcess.on('error', (error) => {
          clearTimeout(timeout);
          reject(error);
        });
        
        this.ollamaProcess.on('exit', (code) => {
          this.log('info', 'Ollama process exited', { code });
          this.isRunning = false;
          this.ollamaProcess = null;
          this.health.status = 'stopped';
          
          // Auto-restart se não foi intencional
          if (code !== 0 && this.retryAttempts < this.maxRetries) {
            this.log('info', 'Attempting auto-restart...');
            setTimeout(() => this.start(), this.config.retryDelay);
          }
        });
        
      } catch (error) {
        clearTimeout(timeout);
        reject(error);
      }
    });
  }
  
  async findOllamaPath() {
    const possiblePaths = [
      '/usr/local/bin/ollama',
      '/opt/homebrew/bin/ollama',
      '/usr/bin/ollama',
      path.join(app.getPath('home'), '.local', 'bin', 'ollama')
    ];
    
    for (const ollamaPath of possiblePaths) {
      if (fs.existsSync(ollamaPath)) {
        this.log('info', 'Found Ollama', { path: ollamaPath });
        return ollamaPath;
      }
    }
    
    // Tentar pelo PATH
    try {
      const { execSync } = require('child_process');
      const path = execSync('which ollama', { encoding: 'utf-8' }).trim();
      if (path) {
        this.log('info', 'Found Ollama in PATH', { path });
        return path;
      }
    } catch {}
    
    return null;
  }
  
  async checkIfRunning() {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/tags`, {
        timeout: 5000
      });
      
      if (response.ok) {
        this.health.consecutiveFailures = 0;
        return true;
      }
    } catch (error) {
      this.health.consecutiveFailures++;
    }
    
    return false;
  }
  
  async loadModels() {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/tags`);
      const data = await response.json();
      
      this.models.clear();
      data.models?.forEach(model => {
        this.models.set(model.name, {
          ...model,
          lastUsed: null,
          requestCount: 0,
          avgResponseTime: 0
        });
      });
      
      this.log('info', `Loaded ${this.models.size} models`);
      return Array.from(this.models.values());
    } catch (error) {
      this.log('error', 'Failed to load models', { error: error.message });
      return [];
    }
  }
  
  async generate(prompt, modelName = 'llama3.2:3b', options = {}) {
    const startTime = Date.now();
    
    // Verificar se o modelo existe, senão baixar
    if (!this.models.has(modelName)) {
      this.log('info', `Model ${modelName} not found, downloading...`);
      await this.downloadModel(modelName);
    }
    
    try {
      const response = await fetch(`${this.config.baseUrl}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: modelName,
          prompt,
          stream: false,
          options: {
            temperature: options.temperature || 0.7,
            top_p: options.top_p || 0.9,
            max_tokens: options.max_tokens || 2048,
            ...options
          }
        }),
        timeout: this.config.responseTimeout
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      const duration = Date.now() - startTime;
      
      // Atualizar estatísticas do modelo
      const model = this.models.get(modelName);
      if (model) {
        model.lastUsed = new Date().toISOString();
        model.requestCount++;
        model.avgResponseTime = (model.avgResponseTime * (model.requestCount - 1) + duration) / model.requestCount;
      }
      
      this.log('info', 'Generation successful', { 
        model: modelName, 
        duration,
        tokens: data.response?.length 
      });
      
      return data.response;
    } catch (error) {
      this.log('error', 'Generation failed', { 
        model: modelName,
        error: error.message,
        duration: Date.now() - startTime
      });
      
      // Retry logic
      if (this.retryAttempts < this.maxRetries) {
        this.retryAttempts++;
        this.log('info', `Retrying generation (${this.retryAttempts}/${this.maxRetries})...`);
        await this.delay(this.config.retryDelay);
        return this.generate(prompt, modelName, options);
      }
      
      throw error;
    }
  }
  
  async downloadModel(modelName) {
    return new Promise((resolve, reject) => {
      this.downloadQueue.push({ modelName, resolve, reject });
      this.processDownloadQueue();
    });
  }
  
  async processDownloadQueue() {
    if (this.isDownloading || this.downloadQueue.length === 0) {
      return;
    }
    
    this.isDownloading = true;
    const { modelName, resolve, reject } = this.downloadQueue.shift();
    
    try {
      this.log('info', `Downloading model ${modelName}...`);
      
      const response = await fetch(`${this.config.baseUrl}/api/pull`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: modelName, stream: false })
      });
      
      if (response.ok) {
        this.log('info', `Model ${modelName} downloaded successfully`);
        await this.loadModels();
        resolve(true);
      } else {
        throw new Error(`Failed to download model: ${response.statusText}`);
      }
    } catch (error) {
      this.log('error', `Failed to download model ${modelName}`, { error: error.message });
      reject(error);
    } finally {
      this.isDownloading = false;
      this.processDownloadQueue();
    }
  }
  
  startHealthCheck() {
    setInterval(async () => {
      if (this.isRunning) {
        const isHealthy = await this.checkIfRunning();
        
        if (!isHealthy) {
          this.log('warn', 'Health check failed', { 
            consecutiveFailures: this.health.consecutiveFailures 
          });
          
          // Auto-recover após 3 falhas consecutivas
          if (this.health.consecutiveFailures >= 3) {
            this.log('warn', 'Attempting auto-recovery...');
            this.stop();
            await this.delay(2000);
            await this.start();
          }
        } else {
          this.health.status = 'healthy';
          this.health.lastCheck = new Date().toISOString();
        }
      }
    }, this.config.healthCheckInterval);
  }
  
  async restart() {
    this.log('info', 'Restarting Ollama...');
    this.stop();
    await this.delay(2000);
    return await this.start();
  }
  
  stop() {
    if (this.ollamaProcess) {
      this.log('info', 'Stopping Ollama...');
      this.ollamaProcess.kill('SIGTERM');
      
      // Force kill após 5 segundos se não parar
      setTimeout(() => {
        if (this.ollamaProcess) {
          this.ollamaProcess.kill('SIGKILL');
        }
      }, 5000);
      
      this.ollamaProcess = null;
    }
    
    this.isRunning = false;
    this.health.status = 'stopped';
  }
  
  getStatus() {
    return {
      running: this.isRunning,
      health: this.health,
      models: Array.from(this.models.values()),
      stats: {
        totalModels: this.models.size,
        queuedDownloads: this.downloadQueue.length,
        retryAttempts: this.retryAttempts
      }
    };
  }
  
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = OllamaManagerEnhanced;