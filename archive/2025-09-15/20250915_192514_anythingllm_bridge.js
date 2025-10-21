/**
 * 🌉 ANYTHINGLLM BRIDGE - Integração com AnythingLLM
 * Conecta o AnythingLLM ao ecossistema Digimundo
 */

const http = require('http');
const EventEmitter = require('events');
const { spawn } = require('child_process');
const path = require('path');

class AnythingLLMBridge extends EventEmitter {
  constructor(options = {}) {
    super();
    
    this.config = {
      appPath: options.appPath || '/Users/clubproducoes/Digimundo/TOOLS/utilities/AnythingLLM.app',
      apiPort: options.apiPort || 3001, // Porta padrão do AnythingLLM
      autoStart: options.autoStart !== false,
      integrationMode: options.integrationMode || 'hybrid', // 'standalone', 'integrated', 'hybrid'
      ...options
    };
    
    this.process = null;
    this.isRunning = false;
    this.apiAvailable = false;
    
    // Métricas de integração
    this.metrics = {
      requests: 0,
      responses: 0,
      errors: 0,
      uptime: 0,
      lastInteraction: null
    };
    
    // Capacidades do AnythingLLM
    this.capabilities = {
      documentProcessing: true,
      vectorStorage: true,
      multiModel: true,
      ragSupport: true,
      webScraping: true
    };
  }

  /**
   * Inicializa o bridge
   */
  async initialize() {
    console.log('🌉 Inicializando AnythingLLM Bridge...');
    
    // Verificar se AnythingLLM está instalado
    const isInstalled = await this.checkInstallation();
    if (!isInstalled) {
      console.log('⚠️ AnythingLLM não encontrado no caminho especificado');
      return false;
    }
    
    // Auto-iniciar se configurado
    if (this.config.autoStart) {
      await this.start();
    }
    
    // Verificar API
    await this.checkAPI();
    
    if (this.apiAvailable) {
      console.log('✅ AnythingLLM Bridge pronto para uso');
      this.emit('ready');
    }
    
    return this.apiAvailable;
  }

  /**
   * Verifica se AnythingLLM está instalado
   */
  async checkInstallation() {
    const fs = require('fs').promises;
    try {
      await fs.access(this.config.appPath);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Inicia o AnythingLLM
   */
  async start() {
    if (this.isRunning) {
      console.log('AnythingLLM já está rodando');
      return true;
    }
    
    try {
      console.log('🚀 Iniciando AnythingLLM...');
      
      // Comando para macOS
      const appExecutable = path.join(this.config.appPath, 'Contents', 'MacOS', 'AnythingLLM');
      
      this.process = spawn('open', ['-a', this.config.appPath], {
        detached: true,
        stdio: 'ignore'
      });
      
      this.process.unref();
      this.isRunning = true;
      
      // Aguardar inicialização
      await this.waitForAPI(30000); // 30 segundos timeout
      
      console.log('✅ AnythingLLM iniciado com sucesso');
      this.emit('started');
      return true;
      
    } catch (error) {
      console.error('❌ Erro ao iniciar AnythingLLM:', error);
      this.isRunning = false;
      return false;
    }
  }

  /**
   * Aguarda API ficar disponível
   */
  async waitForAPI(timeout = 30000) {
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      if (await this.checkAPI()) {
        return true;
      }
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
    
    throw new Error('Timeout aguardando API do AnythingLLM');
  }

  /**
   * Verifica se API está disponível
   */
  async checkAPI() {
    try {
      const response = await this.makeRequest('/api/ping', 'GET');
      this.apiAvailable = response !== null;
      return this.apiAvailable;
    } catch {
      this.apiAvailable = false;
      return false;
    }
  }

  /**
   * Faz requisição para API do AnythingLLM
   */
  makeRequest(endpoint, method = 'GET', data = null) {
    return new Promise((resolve, reject) => {
      const options = {
        hostname: 'localhost',
        port: this.config.apiPort,
        path: endpoint,
        method: method,
        headers: {
          'Content-Type': 'application/json'
        }
      };
      
      const req = http.request(options, (res) => {
        let responseData = '';
        
        res.on('data', (chunk) => {
          responseData += chunk;
        });
        
        res.on('end', () => {
          this.metrics.requests++;
          
          try {
            const parsed = JSON.parse(responseData);
            this.metrics.responses++;
            resolve(parsed);
          } catch {
            resolve(responseData);
          }
        });
      });
      
      req.on('error', (error) => {
        this.metrics.errors++;
        reject(error);
      });
      
      if (data) {
        req.write(JSON.stringify(data));
      }
      
      req.end();
    });
  }

  /**
   * INTEGRAÇÃO: Processa documento com AnythingLLM
   */
  async processDocument(documentPath, workspaceId = 'default') {
    if (!this.apiAvailable) {
      throw new Error('AnythingLLM API não disponível');
    }
    
    console.log(`📄 Processando documento: ${documentPath}`);
    
    try {
      const result = await this.makeRequest('/api/document/process', 'POST', {
        path: documentPath,
        workspace: workspaceId
      });
      
      this.metrics.lastInteraction = Date.now();
      this.emit('document_processed', result);
      
      return result;
    } catch (error) {
      console.error('❌ Erro ao processar documento:', error);
      throw error;
    }
  }

  /**
   * INTEGRAÇÃO: Busca vetorial
   */
  async vectorSearch(query, workspaceId = 'default', limit = 5) {
    if (!this.apiAvailable) {
      throw new Error('AnythingLLM API não disponível');
    }
    
    console.log(`🔍 Busca vetorial: "${query}"`);
    
    try {
      const result = await this.makeRequest('/api/workspace/search', 'POST', {
        query: query,
        workspace: workspaceId,
        limit: limit
      });
      
      this.metrics.lastInteraction = Date.now();
      this.emit('search_completed', result);
      
      return result;
    } catch (error) {
      console.error('❌ Erro na busca vetorial:', error);
      throw error;
    }
  }

  /**
   * INTEGRAÇÃO: Chat com contexto RAG
   */
  async chat(message, workspaceId = 'default', context = {}) {
    if (!this.apiAvailable) {
      throw new Error('AnythingLLM API não disponível');
    }
    
    console.log(`💬 Chat RAG: "${message}"`);
    
    try {
      const result = await this.makeRequest('/api/workspace/chat', 'POST', {
        message: message,
        workspace: workspaceId,
        mode: 'chat',
        ...context
      });
      
      this.metrics.lastInteraction = Date.now();
      this.emit('chat_response', result);
      
      return result;
    } catch (error) {
      console.error('❌ Erro no chat:', error);
      throw error;
    }
  }

  /**
   * INTEGRAÇÃO: Criar workspace para Digimon
   */
  async createDigimonWorkspace(digimonName, config = {}) {
    if (!this.apiAvailable) {
      throw new Error('AnythingLLM API não disponível');
    }
    
    console.log(`🏗️ Criando workspace para ${digimonName}`);
    
    try {
      const result = await this.makeRequest('/api/workspace/create', 'POST', {
        name: `digimundo-${digimonName}`,
        openAiModel: config.model || 'gpt-3.5-turbo',
        chatMode: 'chat',
        ...config
      });
      
      this.emit('workspace_created', { digimon: digimonName, workspace: result });
      
      return result;
    } catch (error) {
      console.error('❌ Erro ao criar workspace:', error);
      throw error;
    }
  }

  /**
   * INTEGRAÇÃO: Sincronizar com memória do Digimundo
   */
  async syncWithDigimundoMemory(memories, workspaceId = 'digimundo-main') {
    if (!this.apiAvailable) {
      throw new Error('AnythingLLM API não disponível');
    }
    
    console.log(`🔄 Sincronizando ${memories.length} memórias com AnythingLLM`);
    
    const results = [];
    
    for (const memory of memories) {
      try {
        // Converter memória para documento
        const doc = {
          title: `Memory-${memory.id || Date.now()}`,
          content: memory.content,
          metadata: {
            type: memory.type || 'episodic',
            timestamp: memory.timestamp,
            importance: memory.importance || 0.5,
            source: 'digimundo'
          }
        };
        
        const result = await this.makeRequest('/api/document/add', 'POST', {
          workspace: workspaceId,
          document: doc
        });
        
        results.push(result);
      } catch (error) {
        console.error(`❌ Erro ao sincronizar memória:`, error);
      }
    }
    
    this.emit('memory_synced', { total: memories.length, synced: results.length });
    
    return results;
  }

  /**
   * INTEGRAÇÃO: Usar AnythingLLM como backend RAG para Digimon
   */
  async enhanceDigimonWithRAG(digimonName, knowledge = []) {
    console.log(`🧬 Aprimorando ${digimonName} com RAG do AnythingLLM`);
    
    // Criar workspace dedicado
    const workspace = await this.createDigimonWorkspace(digimonName, {
      model: 'gpt-4',
      temperature: 0.7
    });
    
    // Adicionar conhecimento base
    if (knowledge.length > 0) {
      for (const doc of knowledge) {
        await this.processDocument(doc, workspace.id);
      }
    }
    
    // Retornar interface RAG
    return {
      workspace: workspace,
      
      ask: async (question) => {
        return await this.chat(question, workspace.id);
      },
      
      search: async (query) => {
        return await this.vectorSearch(query, workspace.id);
      },
      
      addKnowledge: async (content) => {
        return await this.makeRequest('/api/document/add', 'POST', {
          workspace: workspace.id,
          document: { content }
        });
      }
    };
  }

  /**
   * Para o AnythingLLM
   */
  async stop() {
    if (this.process) {
      // No macOS, precisamos encontrar e matar o processo
      const { exec } = require('child_process');
      
      return new Promise((resolve) => {
        exec('pkill -f AnythingLLM', (error) => {
          if (!error) {
            console.log('✅ AnythingLLM parado');
          }
          this.isRunning = false;
          this.apiAvailable = false;
          this.process = null;
          resolve();
        });
      });
    }
  }

  /**
   * Obtém métricas
   */
  getMetrics() {
    return {
      ...this.metrics,
      isRunning: this.isRunning,
      apiAvailable: this.apiAvailable,
      capabilities: this.capabilities
    };
  }

  /**
   * Obtém status completo
   */
  async getStatus() {
    const apiCheck = await this.checkAPI();
    
    return {
      installed: await this.checkInstallation(),
      running: this.isRunning,
      apiAvailable: apiCheck,
      metrics: this.getMetrics(),
      config: this.config
    };
  }
}

// Exemplo de uso
if (require.main === module) {
  (async () => {
    console.log('🧪 TESTANDO ANYTHINGLLM BRIDGE\\n');
    
    const bridge = new AnythingLLMBridge({
      autoStart: false // Não auto-iniciar para teste
    });
    
    // Verificar status
    const status = await bridge.getStatus();
    console.log('📊 Status:', status);
    
    if (status.installed) {
      console.log('\\n✅ AnythingLLM está instalado');
      
      // Se quiser testar a integração completa, descomente:
      /*
      await bridge.initialize();
      
      if (bridge.apiAvailable) {
        // Testar busca
        const results = await bridge.vectorSearch('consciousness');
        console.log('Resultados da busca:', results);
        
        // Criar workspace para Sabiamon
        const workspace = await bridge.createDigimonWorkspace('sabiamon');
        console.log('Workspace criado:', workspace);
      }
      */
    } else {
      console.log('\\n⚠️ AnythingLLM não está instalado');
      console.log('Para integração completa, instale o AnythingLLM');
    }
    
    console.log('\\n📝 Capacidades disponíveis:');
    console.log(bridge.capabilities);
    
    console.log('\\n✨ Bridge pode ser usado para:');
    console.log('- Processamento avançado de documentos');
    console.log('- Busca vetorial com embeddings');
    console.log('- RAG (Retrieval Augmented Generation)');
    console.log('- Criar workspaces dedicados para cada Digimon');
    console.log('- Sincronizar memórias do Digimundo');
  })();
}

module.exports = AnythingLLMBridge;