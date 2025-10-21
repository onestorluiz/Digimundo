/**
 * 🤖 OLLAMA MANAGER
 * Gerencia o ciclo de vida do Ollama dentro do app
 * Inicia automaticamente, baixa modelos, monitora status
 */

const { spawn, exec } = require('child_process');
const { promisify } = require('util');
const path = require('path');
const fs = require('fs').promises;
const fetch = require('node-fetch');
const CacheManager = require('./cache-manager');

const execAsync = promisify(exec);

class OllamaManager {
  constructor(monitor = null) {
    this.monitor = monitor;
    this.cache = new CacheManager(monitor);
    this.ollamaProcess = null;
    this.isRunning = false;
    this.baseUrl = 'http://localhost:11434';
    this.requiredModels = [
      'llama3.2:3b',      // Modelo principal leve
      'tinyllama:latest', // Ultra leve para respostas rápidas
      'phi3:mini'         // Alternativa eficiente
    ];
    this.modelsReady = new Set();
    this.startupAttempts = 0;
    this.maxStartupAttempts = 3;
    this.retryCount = 0;
    this.maxRetries = 3;
  }

  /**
   * Verifica se Ollama já está rodando
   */
  async checkIfRunning() {
    try {
      const response = await fetch(`${this.baseUrl}/api/tags`);
      this.isRunning = response.ok;
      
      if (this.isRunning) {
        console.log('✅ Ollama já está rodando');
        
        // Verifica modelos disponíveis
        const data = await response.json();
        if (data.models) {
          data.models.forEach(model => {
            this.modelsReady.add(model.name);
          });
        }
      }
      
      return this.isRunning;
    } catch (error) {
      this.isRunning = false;
      return false;
    }
  }

  /**
   * Encontra o executável do Ollama
   */
  async findOllamaPath() {
    const possiblePaths = [
      '/usr/local/bin/ollama',
      '/opt/homebrew/bin/ollama',
      '/Applications/Ollama.app/Contents/MacOS/Ollama',
      '/Applications/Ollama.app/Contents/Resources/ollama',
      path.join(process.env.HOME, '.ollama/bin/ollama')
    ];

    // Tenta com which primeiro
    try {
      const { stdout } = await execAsync('which ollama');
      if (stdout.trim()) {
        console.log('📍 Ollama encontrado:', stdout.trim());
        return stdout.trim();
      }
    } catch {}

    // Verifica caminhos conhecidos
    for (const ollamaPath of possiblePaths) {
      try {
        await fs.access(ollamaPath);
        console.log('📍 Ollama encontrado:', ollamaPath);
        return ollamaPath;
      } catch {}
    }

    console.warn('⚠️ Ollama não encontrado no sistema');
    return null;
  }

  /**
   * Inicia o servidor Ollama
   */
  async start() {
    // Verifica se já está rodando
    if (await this.checkIfRunning()) {
      console.log('✅ Ollama já está ativo');
      await this.ensureModels();
      return true;
    }

    const ollamaPath = await this.findOllamaPath();
    if (!ollamaPath) {
      console.error('❌ Ollama não está instalado');
      console.log('📦 Instale com: brew install ollama');
      return false;
    }

    console.log('🚀 Iniciando Ollama...');
    
    return new Promise((resolve) => {
      // Inicia o processo do Ollama
      this.ollamaProcess = spawn(ollamaPath, ['serve'], {
        detached: false,
        stdio: ['ignore', 'pipe', 'pipe'],
        env: {
          ...process.env,
          OLLAMA_HOST: '127.0.0.1:11434',
          OLLAMA_MODELS: path.join(process.env.HOME, '.ollama/models'),
          OLLAMA_KEEP_ALIVE: '10m'
        }
      });

      // Log do output
      this.ollamaProcess.stdout.on('data', (data) => {
        const output = data.toString();
        if (output.includes('Listening on')) {
          console.log('✅ Ollama servidor iniciado');
          this.isRunning = true;
          
          // Aguarda um pouco e baixa modelos
          setTimeout(() => {
            this.ensureModels();
          }, 2000);
          
          resolve(true);
        }
      });

      this.ollamaProcess.stderr.on('data', (data) => {
        const error = data.toString();
        
        // Ignora avisos normais
        if (!error.includes('warning') && !error.includes('Listening')) {
          console.error('Ollama erro:', error);
        }
      });

      this.ollamaProcess.on('error', (err) => {
        console.error('❌ Falha ao iniciar Ollama:', err);
        this.isRunning = false;
        
        // Tenta novamente
        if (this.startupAttempts < this.maxStartupAttempts) {
          this.startupAttempts++;
          console.log(`🔄 Tentativa ${this.startupAttempts}/${this.maxStartupAttempts}...`);
          setTimeout(() => this.start(), 3000);
        }
        
        resolve(false);
      });

      this.ollamaProcess.on('exit', (code) => {
        console.log(`Ollama encerrado com código ${code}`);
        this.isRunning = false;
        this.ollamaProcess = null;
      });

      // Timeout de segurança
      setTimeout(() => {
        if (!this.isRunning) {
          console.warn('⏱️ Timeout ao iniciar Ollama');
          resolve(false);
        }
      }, 30000);
    });
  }

  /**
   * Garante que os modelos necessários estão baixados
   */
  async ensureModels() {
    console.log('🔍 Verificando modelos...');
    
    for (const model of this.requiredModels) {
      if (!this.modelsReady.has(model)) {
        await this.pullModel(model);
      }
    }
    
    console.log('✅ Todos os modelos prontos:', Array.from(this.modelsReady));
  }

  /**
   * Baixa um modelo específico
   */
  async pullModel(modelName) {
    console.log(`📥 Baixando modelo ${modelName}...`);
    
    try {
      const response = await fetch(`${this.baseUrl}/api/pull`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: modelName })
      });

      if (response.ok) {
        // Stream do progresso
        const reader = response.body.getReader();
        let lastProgress = 0;
        
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          const text = new TextDecoder().decode(value);
          const lines = text.split('\n').filter(l => l.trim());
          
          for (const line of lines) {
            try {
              const data = JSON.parse(line);
              
              if (data.completed && data.total) {
                const progress = Math.round((data.completed / data.total) * 100);
                if (progress > lastProgress + 10) {
                  console.log(`  ${modelName}: ${progress}%`);
                  lastProgress = progress;
                }
              }
              
              if (data.status === 'success') {
                console.log(`✅ Modelo ${modelName} baixado`);
                this.modelsReady.add(modelName);
              }
            } catch {}
          }
        }
      }
    } catch (error) {
      console.error(`❌ Erro ao baixar ${modelName}:`, error.message);
    }
  }

  /**
   * Lista modelos disponíveis
   */
  async listModels() {
    try {
      const response = await fetch(`${this.baseUrl}/api/tags`);
      const data = await response.json();
      return data.models || [];
    } catch (error) {
      return [];
    }
  }

  /**
   * Gera resposta usando Ollama
   */
  async generate(prompt, model = 'llama3.2:3b') {
    // Add tracing
    const { getTracing } = require('./tracing');
    const tracing = getTracing();
    const span = tracing?.traceOllamaOperation('generate', model);
    
    if (!this.isRunning) {
      await this.start();
    }
    
    // Verificar cache primeiro
    const cached = await this.cache.get(prompt, model);
    if (cached) {
      if (this.monitor) {
        this.monitor.log('info', 'OLLAMA', 'Response from cache', { model });
      }
      console.log('📦 Resposta do cache');
      span?.addEvent('cache_hit', { model });
      span?.end({ 'cache.hit': true });
      return cached;
    }

    try {
      const response = await fetch(`${this.baseUrl}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model,
          prompt,
          stream: false,
          options: {
            temperature: 0.7,
            top_p: 0.9,
            max_tokens: 2048
          }
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      const result = data.response;
      
      // Armazenar no cache
      if (result) {
        await this.cache.set(prompt, model, result);
        console.log('💾 Resposta salva no cache');
      }
      
      span?.end({ 'ollama.success': true, 'response.length': result?.length || 0 });
      return result;
    } catch (error) {
      span?.recordError(error);
      span?.end({ 'ollama.success': false });
      
      // Retry logic
      if (this.retryCount < this.maxRetries) {
        this.retryCount++;
        console.log(`🔄 Retry ${this.retryCount}/${this.maxRetries}...`);
        if (this.monitor) {
          this.monitor.log('warn', 'OLLAMA', `Retry ${this.retryCount}/${this.maxRetries}`, { error: error.message });
        }
        await new Promise(resolve => setTimeout(resolve, 2000));
        return this.generate(prompt, model);
      }
      
      console.error('Erro ao gerar resposta:', error);
      if (this.monitor) {
        this.monitor.trackError('OLLAMA', error, { operation: 'generate', model });
      }
      return null;
    }
  }

  /**
   * Para o servidor Ollama
   */
  stop() {
    if (this.ollamaProcess) {
      console.log('🛑 Encerrando Ollama...');
      
      // Tenta encerrar graciosamente
      this.ollamaProcess.kill('SIGTERM');
      
      // Force kill após 5 segundos
      setTimeout(() => {
        if (this.ollamaProcess) {
          this.ollamaProcess.kill('SIGKILL');
        }
      }, 5000);
      
      this.ollamaProcess = null;
      this.isRunning = false;
    }
  }

  /**
   * Reinicia o Ollama
   */
  async restart() {
    this.stop();
    await new Promise(resolve => setTimeout(resolve, 2000));
    return await this.start();
  }

  /**
   * Status completo do Ollama
   */
  async getStatus() {
    return {
      running: this.isRunning,
      url: this.baseUrl,
      models: Array.from(this.modelsReady),
      requiredModels: this.requiredModels,
      process: this.ollamaProcess ? 'active' : 'inactive',
      cacheStats: this.cache.getStats(),
      retryCount: this.retryCount
    };
  }
}

module.exports = OllamaManager;