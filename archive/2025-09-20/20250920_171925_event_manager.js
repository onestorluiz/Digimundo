/**
 * 🧹 EVENT MANAGER - GESTÃO CENTRALIZADA DE EVENT LISTENERS
 * Previne memory leaks gerenciando todos os listeners do sistema
 */

const EventEmitter = require('events');

class EventManager extends EventEmitter {
  constructor() {
    super();
    
    // Registro de todos os listeners ativos
    this.activeListeners = new Map();
    
    // Configuração de limites seguros
    this.setMaxListeners(50);
    
    // Monitoramento de leaks
    this.leakThreshold = 30;
    this.enableLeakDetection = true;
    
    // Auto-cleanup
    this.cleanupInterval = null;
    this.startAutoCleanup();
  }

  /**
   * Registra um listener com tracking
   */
  safeOn(eventName, listener, context = 'global') {
    // Criar ID único para o listener
    const listenerId = `${context}_${eventName}_${Date.now()}_${Math.random()}`;
    
    // Registrar no mapa
    if (!this.activeListeners.has(context)) {
      this.activeListeners.set(context, new Map());
    }
    
    const contextListeners = this.activeListeners.get(context);
    
    // Verificar se há muitos listeners para o mesmo evento
    const eventListeners = Array.from(contextListeners.values())
      .filter(l => l.eventName === eventName);
    
    if (eventListeners.length >= this.leakThreshold) {
      console.warn(`⚠️ Possível memory leak: ${eventListeners.length} listeners para "${eventName}" no contexto "${context}"`);
      
      // Auto-limpar listeners antigos
      if (this.enableLeakDetection) {
        this.cleanupOldListeners(context, eventName);
      }
    }
    
    // Wrapper do listener para tracking
    const wrappedListener = (...args) => {
      try {
        return listener(...args);
      } catch (error) {
        console.error(`Erro no listener ${listenerId}:`, error);
        this.removeListener(eventName, wrappedListener);
      }
    };
    
    // Armazenar informações do listener
    contextListeners.set(listenerId, {
      eventName,
      listener: wrappedListener,
      originalListener: listener,
      timestamp: Date.now(),
      context
    });
    
    // Adicionar listener
    this.on(eventName, wrappedListener);
    
    return listenerId;
  }

  /**
   * Registra um listener que será executado apenas uma vez
   */
  safeOnce(eventName, listener, context = 'global') {
    const listenerId = this.safeOn(eventName, (...args) => {
      listener(...args);
      this.safeOff(listenerId);
    }, context);
    
    return listenerId;
  }

  /**
   * Remove um listener específico
   */
  safeOff(listenerId) {
    // Procurar em todos os contextos
    for (const [context, contextListeners] of this.activeListeners) {
      if (contextListeners.has(listenerId)) {
        const listenerInfo = contextListeners.get(listenerId);
        
        // Remover o listener
        this.removeListener(listenerInfo.eventName, listenerInfo.listener);
        
        // Remover do registro
        contextListeners.delete(listenerId);
        
        // Limpar contexto vazio
        if (contextListeners.size === 0) {
          this.activeListeners.delete(context);
        }
        
        return true;
      }
    }
    
    return false;
  }

  /**
   * Remove todos os listeners de um contexto
   */
  removeContextListeners(context) {
    const contextListeners = this.activeListeners.get(context);
    
    if (!contextListeners) {
      return 0;
    }
    
    let removed = 0;
    
    for (const [listenerId, listenerInfo] of contextListeners) {
      this.removeListener(listenerInfo.eventName, listenerInfo.listener);
      removed++;
    }
    
    this.activeListeners.delete(context);
    
    console.log(`🧹 Removidos ${removed} listeners do contexto "${context}"`);
    
    return removed;
  }

  /**
   * Remove todos os listeners de um evento específico
   */
  removeEventListeners(eventName) {
    let removed = 0;
    
    for (const [context, contextListeners] of this.activeListeners) {
      const toRemove = [];
      
      for (const [listenerId, listenerInfo] of contextListeners) {
        if (listenerInfo.eventName === eventName) {
          this.removeListener(eventName, listenerInfo.listener);
          toRemove.push(listenerId);
          removed++;
        }
      }
      
      // Remover do registro
      toRemove.forEach(id => contextListeners.delete(id));
      
      // Limpar contexto vazio
      if (contextListeners.size === 0) {
        this.activeListeners.delete(context);
      }
    }
    
    console.log(`🧹 Removidos ${removed} listeners do evento "${eventName}"`);
    
    return removed;
  }

  /**
   * Limpa listeners antigos (mais de 1 hora)
   */
  cleanupOldListeners(context = null, eventName = null) {
    const oneHourAgo = Date.now() - (60 * 60 * 1000);
    let removed = 0;
    
    const contexts = context ? [context] : Array.from(this.activeListeners.keys());
    
    for (const ctx of contexts) {
      const contextListeners = this.activeListeners.get(ctx);
      if (!contextListeners) continue;
      
      const toRemove = [];
      
      for (const [listenerId, listenerInfo] of contextListeners) {
        // Filtrar por evento se especificado
        if (eventName && listenerInfo.eventName !== eventName) continue;
        
        // Remover se for antigo
        if (listenerInfo.timestamp < oneHourAgo) {
          this.removeListener(listenerInfo.eventName, listenerInfo.listener);
          toRemove.push(listenerId);
          removed++;
        }
      }
      
      // Remover do registro
      toRemove.forEach(id => contextListeners.delete(id));
      
      // Limpar contexto vazio
      if (contextListeners.size === 0) {
        this.activeListeners.delete(ctx);
      }
    }
    
    if (removed > 0) {
      console.log(`🧹 Auto-cleanup: ${removed} listeners antigos removidos`);
    }
    
    return removed;
  }

  /**
   * Inicia limpeza automática periódica
   */
  startAutoCleanup(intervalMs = 30 * 60 * 1000) { // 30 minutos
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
    }
    
    this.cleanupInterval = setInterval(() => {
      this.cleanupOldListeners();
      this.logStatus();
    }, intervalMs);
  }

  /**
   * Para limpeza automática
   */
  stopAutoCleanup() {
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
      this.cleanupInterval = null;
    }
  }

  /**
   * Obtém estatísticas dos listeners
   */
  getStats() {
    const stats = {
      totalListeners: 0,
      byContext: {},
      byEvent: {},
      oldestListener: null,
      newestListener: null
    };
    
    let oldestTime = Infinity;
    let newestTime = 0;
    
    for (const [context, contextListeners] of this.activeListeners) {
      stats.byContext[context] = contextListeners.size;
      stats.totalListeners += contextListeners.size;
      
      for (const listenerInfo of contextListeners.values()) {
        // Por evento
        if (!stats.byEvent[listenerInfo.eventName]) {
          stats.byEvent[listenerInfo.eventName] = 0;
        }
        stats.byEvent[listenerInfo.eventName]++;
        
        // Timestamps
        if (listenerInfo.timestamp < oldestTime) {
          oldestTime = listenerInfo.timestamp;
          stats.oldestListener = {
            context,
            event: listenerInfo.eventName,
            age: Date.now() - listenerInfo.timestamp
          };
        }
        
        if (listenerInfo.timestamp > newestTime) {
          newestTime = listenerInfo.timestamp;
          stats.newestListener = {
            context,
            event: listenerInfo.eventName,
            age: Date.now() - listenerInfo.timestamp
          };
        }
      }
    }
    
    return stats;
  }

  /**
   * Log do status atual
   */
  logStatus() {
    const stats = this.getStats();
    console.log('📊 Event Manager Status:');
    console.log(`   Total de listeners: ${stats.totalListeners}`);
    console.log(`   Contextos ativos: ${Object.keys(stats.byContext).length}`);
    console.log(`   Eventos monitorados: ${Object.keys(stats.byEvent).length}`);
    
    if (stats.totalListeners > 100) {
      console.warn('⚠️ Muitos listeners ativos! Considere limpeza manual.');
    }
  }

  /**
   * Limpa todos os listeners e para monitoramento
   */
  destroy() {
    console.log('🛑 Destruindo Event Manager...');
    
    // Parar auto-cleanup
    this.stopAutoCleanup();
    
    // Remover todos os listeners
    let totalRemoved = 0;
    for (const context of Array.from(this.activeListeners.keys())) {
      totalRemoved += this.removeContextListeners(context);
    }
    
    // Limpar listeners nativos
    this.removeAllListeners();
    
    console.log(`✅ Event Manager destruído. ${totalRemoved} listeners removidos.`);
  }
}

// Singleton
let instance = null;

module.exports = {
  getInstance: () => {
    if (!instance) {
      instance = new EventManager();
    }
    return instance;
  },
  
  EventManager
};