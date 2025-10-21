/**
 * Sistema de Cache Inteligente para Digimundo
 * Melhora performance e reduz latência
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { app } = require('electron');

class CacheManager {
  constructor(monitor = null) {
    this.monitor = monitor;
    this.cacheDir = path.join(app.getPath('userData'), 'cache');
    this.memoryCache = new Map();
    this.cacheStats = {
      hits: 0,
      misses: 0,
      evictions: 0
    };
    
    // Configurações
    this.config = {
      maxMemoryCacheSize: 100, // MB
      maxDiskCacheSize: 500, // MB
      ttl: 3600000, // 1 hora
      maxEntries: 1000,
      compressionThreshold: 1024 // bytes
    };
    
    this.currentMemorySize = 0;
    this.ensureCacheDirectory();
    this.startCleanupTimer();
  }
  
  ensureCacheDirectory() {
    if (!fs.existsSync(this.cacheDir)) {
      fs.mkdirSync(this.cacheDir, { recursive: true });
    }
  }
  
  generateKey(prompt, model, options = {}) {
    const data = JSON.stringify({ prompt, model, ...options });
    return crypto.createHash('sha256').update(data).digest('hex');
  }
  
  async get(prompt, model, options = {}) {
    const key = this.generateKey(prompt, model, options);
    
    // Verificar cache na memória primeiro
    if (this.memoryCache.has(key)) {
      const entry = this.memoryCache.get(key);
      
      if (!this.isExpired(entry)) {
        this.cacheStats.hits++;
        this.updateAccessTime(key);
        
        if (this.monitor) {
          this.monitor.trackPerformance('cacheHitRate', 
            this.cacheStats.hits / (this.cacheStats.hits + this.cacheStats.misses));
        }
        
        return entry.data;
      } else {
        this.memoryCache.delete(key);
        this.currentMemorySize -= entry.size;
      }
    }
    
    // Verificar cache em disco
    const diskEntry = await this.getDiskCache(key);
    if (diskEntry) {
      // Promover para memória se houver espaço
      if (this.canAddToMemory(diskEntry.size)) {
        this.memoryCache.set(key, diskEntry);
        this.currentMemorySize += diskEntry.size;
      }
      
      this.cacheStats.hits++;
      return diskEntry.data;
    }
    
    this.cacheStats.misses++;
    return null;
  }
  
  async set(prompt, model, response, options = {}) {
    const key = this.generateKey(prompt, model, options);
    const size = Buffer.byteLength(JSON.stringify(response));
    
    const entry = {
      key,
      prompt,
      model,
      data: response,
      timestamp: Date.now(),
      lastAccess: Date.now(),
      accessCount: 0,
      size
    };
    
    // Adicionar ao cache de memória se possível
    if (this.canAddToMemory(size)) {
      this.memoryCache.set(key, entry);
      this.currentMemorySize += size;
    } else {
      // Executar eviction se necessário
      await this.evictLRU(size);
      
      if (this.canAddToMemory(size)) {
        this.memoryCache.set(key, entry);
        this.currentMemorySize += size;
      }
    }
    
    // Sempre salvar em disco para persistência
    await this.setDiskCache(key, entry);
    
    return key;
  }
  
  canAddToMemory(size) {
    const maxSize = this.config.maxMemoryCacheSize * 1024 * 1024;
    return (this.currentMemorySize + size) <= maxSize;
  }
  
  async evictLRU(requiredSize) {
    const entries = Array.from(this.memoryCache.entries())
      .map(([key, value]) => ({ key, ...value }))
      .sort((a, b) => a.lastAccess - b.lastAccess);
    
    let freedSpace = 0;
    const toEvict = [];
    
    for (const entry of entries) {
      toEvict.push(entry.key);
      freedSpace += entry.size;
      
      if (freedSpace >= requiredSize) break;
    }
    
    for (const key of toEvict) {
      const entry = this.memoryCache.get(key);
      if (entry) {
        this.memoryCache.delete(key);
        this.currentMemorySize -= entry.size;
        this.cacheStats.evictions++;
      }
    }
  }
  
  async getDiskCache(key) {
    const cachePath = path.join(this.cacheDir, `${key}.json`);
    
    try {
      if (fs.existsSync(cachePath)) {
        const data = JSON.parse(fs.readFileSync(cachePath, 'utf-8'));
        
        if (!this.isExpired(data)) {
          return data;
        } else {
          // Remover cache expirado
          fs.unlinkSync(cachePath);
        }
      }
    } catch (error) {
      if (this.monitor) {
        this.monitor.trackError('CACHE', error, { operation: 'getDiskCache', key });
      }
    }
    
    return null;
  }
  
  async setDiskCache(key, entry) {
    const cachePath = path.join(this.cacheDir, `${key}.json`);
    
    try {
      fs.writeFileSync(cachePath, JSON.stringify(entry));
    } catch (error) {
      if (this.monitor) {
        this.monitor.trackError('CACHE', error, { operation: 'setDiskCache', key });
      }
    }
  }
  
  isExpired(entry) {
    return (Date.now() - entry.timestamp) > this.config.ttl;
  }
  
  updateAccessTime(key) {
    const entry = this.memoryCache.get(key);
    if (entry) {
      entry.lastAccess = Date.now();
      entry.accessCount++;
    }
  }
  
  // Análise inteligente de padrões de uso
  analyzeUsagePatterns() {
    const patterns = {
      mostUsedModels: new Map(),
      averagePromptLength: 0,
      peakUsageTimes: [],
      cacheEfficiency: 0
    };
    
    let totalPromptLength = 0;
    let promptCount = 0;
    
    for (const entry of this.memoryCache.values()) {
      // Contabilizar modelos mais usados
      const modelCount = patterns.mostUsedModels.get(entry.model) || 0;
      patterns.mostUsedModels.set(entry.model, modelCount + entry.accessCount);
      
      // Calcular tamanho médio de prompt
      totalPromptLength += entry.prompt.length;
      promptCount++;
    }
    
    patterns.averagePromptLength = promptCount > 0 ? totalPromptLength / promptCount : 0;
    patterns.cacheEfficiency = this.cacheStats.hits / (this.cacheStats.hits + this.cacheStats.misses);
    
    return patterns;
  }
  
  // Pré-carregar respostas populares
  async preloadPopularResponses() {
    const patterns = this.analyzeUsagePatterns();
    
    // Identificar prompts mais comuns
    const popularPrompts = [
      { prompt: "Olá! Como você está?", model: "llama3.2:3b" },
      { prompt: "Me ajude a entender", model: "llama3.2:3b" },
      { prompt: "O que você acha sobre", model: "llama3.2:3b" }
    ];
    
    // Pré-gerar respostas para prompts populares
    for (const item of popularPrompts) {
      const cached = await this.get(item.prompt, item.model);
      if (!cached) {
        // Aqui você poderia chamar o Ollama para gerar a resposta
        // e então armazená-la no cache
      }
    }
  }
  
  // Limpeza periódica
  startCleanupTimer() {
    setInterval(() => {
      this.cleanup();
    }, 3600000); // A cada hora
  }
  
  cleanup() {
    // Limpar entradas expiradas da memória
    for (const [key, entry] of this.memoryCache.entries()) {
      if (this.isExpired(entry)) {
        this.memoryCache.delete(key);
        this.currentMemorySize -= entry.size;
      }
    }
    
    // Limpar cache de disco
    const files = fs.readdirSync(this.cacheDir);
    for (const file of files) {
      const filePath = path.join(this.cacheDir, file);
      const stats = fs.statSync(filePath);
      
      // Remover arquivos com mais de 7 dias
      if (Date.now() - stats.mtimeMs > 7 * 24 * 60 * 60 * 1000) {
        fs.unlinkSync(filePath);
      }
    }
    
    if (this.monitor) {
      this.monitor.log('info', 'CACHE', 'Cleanup completed', {
        memoryEntries: this.memoryCache.size,
        memorySize: this.currentMemorySize,
        stats: this.cacheStats
      });
    }
  }
  
  // Estatísticas do cache
  getStats() {
    const hitRate = this.cacheStats.hits / (this.cacheStats.hits + this.cacheStats.misses);
    
    return {
      ...this.cacheStats,
      hitRate: hitRate || 0,
      memoryUsage: this.currentMemorySize,
      entriesInMemory: this.memoryCache.size,
      patterns: this.analyzeUsagePatterns()
    };
  }
  
  // Limpar todo o cache
  clear() {
    this.memoryCache.clear();
    this.currentMemorySize = 0;
    
    // Limpar disco
    const files = fs.readdirSync(this.cacheDir);
    for (const file of files) {
      fs.unlinkSync(path.join(this.cacheDir, file));
    }
    
    this.cacheStats = {
      hits: 0,
      misses: 0,
      evictions: 0
    };
    
    if (this.monitor) {
      this.monitor.log('info', 'CACHE', 'Cache cleared');
    }
  }
}

module.exports = CacheManager;