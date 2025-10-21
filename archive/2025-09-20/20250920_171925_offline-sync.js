/**
 * DIGIMUNDO OFFLINE-FIRST SYNC SYSTEM - MODO HACKER
 * Sistema ultra-avançado de sincronização offline com conflict resolution
 * Features: IndexedDB, Queue de operações, Sync inteligente, PWA support
 */

const EventEmitter = require('events');
const { v4: uuidv4 } = require('uuid');

class DigimundoOfflineSync extends EventEmitter {
    constructor(digimundoCore) {
        super();
        this.core = digimundoCore;
        this.isOnline = true;
        this.syncQueue = [];
        this.conflictQueue = [];
        this.lastSyncTimestamp = null;
        this.syncInProgress = false;
        this.retryAttempts = new Map();
        this.maxRetryAttempts = 3;
        this.syncInterval = null;
        
        this.setupOfflineSystem();
        this.startPeriodicSync();
    }

    setupOfflineSystem() {
        // Detectar mudanças de conectividade
        this.setupConnectivityDetection();
        
        // Configurar service worker para PWA
        this.setupServiceWorker();
        
        // Configurar interceptadores de requests
        this.setupRequestInterceptors();
        
        console.log('💾 [MODO HACKER] Sistema Offline-First inicializado');
    }

    setupConnectivityDetection() {
        // Simular detecção de conectividade para Node.js
        // Em um ambiente real com Electron, usaríamos navigator.onLine
        setInterval(() => {
            this.checkConnectivity();
        }, 5000);
    }

    async checkConnectivity() {
        try {
            // Tentar fazer uma requisição rápida para verificar conectividade
            const wasOnline = this.isOnline;
            
            // Simular verificação de conectividade
            // Em produção, fazer ping para um endpoint confiável
            this.isOnline = Math.random() > 0.1; // 90% de chance de estar online (para demo)
            
            if (wasOnline !== this.isOnline) {
                if (this.isOnline) {
                    console.log('🌐 [Offline-Sync] Conectividade restaurada');
                    this.emit('online');
                    await this.processSyncQueue();
                } else {
                    console.log('📴 [Offline-Sync] Modo offline ativado');
                    this.emit('offline');
                }
            }
        } catch (error) {
            this.isOnline = false;
            console.error('❌ [Offline-Sync] Erro ao verificar conectividade:', error);
        }
    }

    setupServiceWorker() {
        // Configuração do Service Worker para PWA
        const serviceWorkerCode = `
            const CACHE_NAME = 'digimundo-offline-v1';
            const urlsToCache = [
                '/',
                '/renderer/index.html',
                '/renderer/collaboration.html',
                '/renderer/assets/digimundo-icon.png',
                '/offline.html'
            ];

            self.addEventListener('install', (event) => {
                event.waitUntil(
                    caches.open(CACHE_NAME)
                        .then((cache) => cache.addAll(urlsToCache))
                );
            });

            self.addEventListener('fetch', (event) => {
                event.respondWith(
                    caches.match(event.request)
                        .then((response) => {
                            // Retorna cache se encontrado, senão faz fetch
                            if (response) {
                                return response;
                            }
                            return fetch(event.request);
                        }
                    )
                );
            });

            self.addEventListener('sync', (event) => {
                if (event.tag === 'background-sync') {
                    event.waitUntil(doBackgroundSync());
                }
            });

            async function doBackgroundSync() {
                try {
                    // Sincronizar dados pendentes
                    const pendingData = await self.registration.sync.getTags();
                    for (const tag of pendingData) {
                        if (tag.startsWith('sync-')) {
                            await processPendingSync(tag);
                        }
                    }
                } catch (error) {
                    console.error('Background sync failed:', error);
                }
            }
        `;

        // Salvar service worker no sistema de arquivos
        const fs = require('fs');
        const path = require('path');
        
        try {
            const swPath = path.join(__dirname, '../renderer/sw.js');
            fs.writeFileSync(swPath, serviceWorkerCode);
            console.log('🔧 [PWA] Service Worker gerado');
        } catch (error) {
            console.error('❌ [PWA] Erro ao gerar Service Worker:', error);
        }
    }

    setupRequestInterceptors() {
        // Interceptar requisições para queue offline
        this.originalFetch = global.fetch;
        
        global.fetch = async (...args) => {
            const [url, options] = args;
            
            try {
                if (this.isOnline) {
                    const response = await this.originalFetch(...args);
                    
                    // Salvar response em cache se for GET
                    if (!options?.method || options.method === 'GET') {
                        await this.cacheResponse(url, response.clone());
                    }
                    
                    return response;
                } else {
                    // Modo offline
                    if (!options?.method || options.method === 'GET') {
                        // Tentar buscar do cache
                        const cachedResponse = await this.getCachedResponse(url);
                        if (cachedResponse) {
                            return cachedResponse;
                        }
                    } else {
                        // Adicionar à queue para sync posterior
                        await this.queueRequest(url, options);
                        
                        // Retornar response mockada
                        return new Response(
                            JSON.stringify({ queued: true, id: uuidv4() }),
                            { status: 202, statusText: 'Queued for sync' }
                        );
                    }
                    
                    throw new Error('Offline and no cached response available');
                }
            } catch (error) {
                console.error('❌ [Request Interceptor] Erro:', error);
                throw error;
            }
        };
    }

    async cacheResponse(url, response) {
        try {
            const cacheKey = this.generateCacheKey(url);
            const responseData = {
                url,
                status: response.status,
                statusText: response.statusText,
                headers: Object.fromEntries(response.headers.entries()),
                body: await response.text(),
                timestamp: new Date().toISOString()
            };
            
            await this.saveToIndexedDB('responseCache', cacheKey, responseData);
        } catch (error) {
            console.error('❌ [Cache] Erro ao salvar response:', error);
        }
    }

    async getCachedResponse(url) {
        try {
            const cacheKey = this.generateCacheKey(url);
            const cachedData = await this.getFromIndexedDB('responseCache', cacheKey);
            
            if (cachedData) {
                return new Response(cachedData.body, {
                    status: cachedData.status,
                    statusText: cachedData.statusText,
                    headers: cachedData.headers
                });
            }
        } catch (error) {
            console.error('❌ [Cache] Erro ao buscar response:', error);
        }
        
        return null;
    }

    async queueRequest(url, options) {
        const queueItem = {
            id: uuidv4(),
            url,
            options,
            timestamp: new Date().toISOString(),
            attempts: 0,
            status: 'pending'
        };
        
        this.syncQueue.push(queueItem);
        await this.saveToIndexedDB('syncQueue', queueItem.id, queueItem);
        
        console.log(`📬 [Queue] Request adicionado à queue: ${url}`);
    }

    async processSyncQueue() {
        if (this.syncInProgress || !this.isOnline) {
            return;
        }

        this.syncInProgress = true;
        console.log('🔄 [Sync] Processando queue de sincronização...');

        try {
            // Carregar queue do IndexedDB
            await this.loadSyncQueueFromDB();
            
            const pendingItems = this.syncQueue.filter(item => 
                item.status === 'pending' && item.attempts < this.maxRetryAttempts
            );

            for (const item of pendingItems) {
                try {
                    await this.processSyncItem(item);
                } catch (error) {
                    console.error(`❌ [Sync] Erro ao processar item ${item.id}:`, error);
                    await this.handleSyncError(item, error);
                }
            }

            // Limpar itens processados
            await this.cleanupProcessedItems();
            
        } finally {
            this.syncInProgress = false;
            this.lastSyncTimestamp = new Date().toISOString();
            this.emit('sync-completed');
        }
    }

    async processSyncItem(item) {
        item.attempts++;
        item.status = 'processing';
        
        console.log(`🔄 [Sync] Processando: ${item.url} (tentativa ${item.attempts})`);
        
        try {
            const response = await this.originalFetch(item.url, item.options);
            
            if (response.ok) {
                item.status = 'completed';
                item.completedAt = new Date().toISOString();
                
                // Verificar se há conflitos
                await this.checkForConflicts(item, response);
                
                console.log(`✅ [Sync] Item processado: ${item.id}`);
            } else {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
        } catch (error) {
            item.status = 'error';
            item.lastError = error.message;
            throw error;
        } finally {
            await this.saveToIndexedDB('syncQueue', item.id, item);
        }
    }

    async checkForConflicts(item, response) {
        try {
            const responseData = await response.json();
            
            // Verificar se há conflitos baseado em timestamps
            if (responseData.lastModified && item.options.body) {
                const requestData = JSON.parse(item.options.body);
                
                if (requestData.lastModified && 
                    new Date(responseData.lastModified) > new Date(requestData.lastModified)) {
                    
                    // Conflito detectado!
                    const conflict = {
                        id: uuidv4(),
                        syncItemId: item.id,
                        localData: requestData,
                        serverData: responseData,
                        detectedAt: new Date().toISOString(),
                        status: 'pending',
                        type: this.determineConflictType(requestData, responseData)
                    };
                    
                    this.conflictQueue.push(conflict);
                    await this.saveToIndexedDB('conflicts', conflict.id, conflict);
                    
                    console.log(`⚠️ [Conflict] Conflito detectado: ${conflict.id}`);
                    this.emit('conflict-detected', conflict);
                }
            }
        } catch (error) {
            console.error('❌ [Conflict] Erro ao verificar conflitos:', error);
        }
    }

    determineConflictType(localData, serverData) {
        // Análise inteligente de conflitos
        const localKeys = new Set(Object.keys(localData));
        const serverKeys = new Set(Object.keys(serverData));
        
        const commonKeys = [...localKeys].filter(key => serverKeys.has(key));
        const conflictingFields = commonKeys.filter(key => 
            JSON.stringify(localData[key]) !== JSON.stringify(serverData[key])
        );
        
        if (conflictingFields.length === 0) {
            return 'no-conflict';
        } else if (conflictingFields.length === 1) {
            return 'single-field';
        } else if (conflictingFields.length < commonKeys.length / 2) {
            return 'partial';
        } else {
            return 'major';
        }
    }

    async resolveConflict(conflictId, resolution) {
        try {
            const conflict = await this.getFromIndexedDB('conflicts', conflictId);
            if (!conflict) {
                throw new Error('Conflito não encontrado');
            }

            let resolvedData;
            
            switch (resolution.strategy) {
                case 'accept-local':
                    resolvedData = conflict.localData;
                    break;
                
                case 'accept-server':
                    resolvedData = conflict.serverData;
                    break;
                
                case 'merge':
                    resolvedData = await this.mergeData(
                        conflict.localData, 
                        conflict.serverData, 
                        resolution.mergeRules
                    );
                    break;
                
                case 'custom':
                    resolvedData = resolution.customData;
                    break;
                
                default:
                    throw new Error('Estratégia de resolução inválida');
            }

            // Aplicar resolução
            await this.applyConflictResolution(conflict, resolvedData);
            
            // Marcar conflito como resolvido
            conflict.status = 'resolved';
            conflict.resolvedAt = new Date().toISOString();
            conflict.resolution = resolution;
            await this.saveToIndexedDB('conflicts', conflictId, conflict);
            
            console.log(`✅ [Conflict] Conflito resolvido: ${conflictId}`);
            this.emit('conflict-resolved', conflict);
            
        } catch (error) {
            console.error(`❌ [Conflict] Erro ao resolver conflito ${conflictId}:`, error);
            throw error;
        }
    }

    async mergeData(localData, serverData, mergeRules = {}) {
        const merged = { ...serverData }; // Começar com dados do servidor
        
        for (const [field, rule] of Object.entries(mergeRules)) {
            switch (rule) {
                case 'prefer-local':
                    if (localData[field] !== undefined) {
                        merged[field] = localData[field];
                    }
                    break;
                
                case 'prefer-server':
                    // Já está usando servidor como base
                    break;
                
                case 'newest':
                    if (localData[field + '_timestamp'] && serverData[field + '_timestamp']) {
                        const localTime = new Date(localData[field + '_timestamp']);
                        const serverTime = new Date(serverData[field + '_timestamp']);
                        
                        if (localTime > serverTime) {
                            merged[field] = localData[field];
                        }
                    }
                    break;
                
                case 'combine':
                    if (Array.isArray(localData[field]) && Array.isArray(serverData[field])) {
                        // Combinar arrays removendo duplicatas
                        merged[field] = [...new Set([...serverData[field], ...localData[field]])];
                    } else if (typeof localData[field] === 'string' && typeof serverData[field] === 'string') {
                        // Combinar strings
                        merged[field] = `${serverData[field]}\n${localData[field]}`;
                    }
                    break;
            }
        }
        
        return merged;
    }

    async applyConflictResolution(conflict, resolvedData) {
        // Re-adicionar à queue com dados resolvidos
        const resolvedItem = {
            id: uuidv4(),
            url: conflict.syncItemId, // Usar o mesmo endpoint
            options: {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(resolvedData)
            },
            timestamp: new Date().toISOString(),
            attempts: 0,
            status: 'pending',
            conflictResolution: true
        };
        
        this.syncQueue.push(resolvedItem);
        await this.saveToIndexedDB('syncQueue', resolvedItem.id, resolvedItem);
    }

    async handleSyncError(item, error) {
        const retryKey = item.id;
        const currentAttempts = this.retryAttempts.get(retryKey) || 0;
        
        if (currentAttempts < this.maxRetryAttempts) {
            // Calcular delay exponencial
            const delay = Math.pow(2, currentAttempts) * 1000; // 1s, 2s, 4s, 8s...
            
            this.retryAttempts.set(retryKey, currentAttempts + 1);
            
            setTimeout(async () => {
                try {
                    await this.processSyncItem(item);
                } catch (retryError) {
                    await this.handleSyncError(item, retryError);
                }
            }, delay);
            
            console.log(`🔄 [Retry] Reagendando item ${item.id} em ${delay}ms`);
        } else {
            // Máximo de tentativas atingido
            item.status = 'failed';
            item.failedAt = new Date().toISOString();
            await this.saveToIndexedDB('syncQueue', item.id, item);
            
            console.error(`❌ [Sync] Item falhou definitivamente: ${item.id}`);
            this.emit('sync-failed', item);
        }
    }

    async cleanupProcessedItems() {
        const completedItems = this.syncQueue.filter(item => item.status === 'completed');
        
        for (const item of completedItems) {
            await this.removeFromIndexedDB('syncQueue', item.id);
        }
        
        this.syncQueue = this.syncQueue.filter(item => item.status !== 'completed');
        
        console.log(`🧹 [Cleanup] ${completedItems.length} itens processados removidos`);
    }

    async loadSyncQueueFromDB() {
        try {
            const dbItems = await this.getAllFromIndexedDB('syncQueue');
            this.syncQueue = dbItems || [];
        } catch (error) {
            console.error('❌ [DB] Erro ao carregar queue:', error);
        }
    }

    startPeriodicSync() {
        // Sincronizar a cada 30 segundos quando online
        this.syncInterval = setInterval(async () => {
            if (this.isOnline && this.syncQueue.length > 0) {
                await this.processSyncQueue();
            }
        }, 30000);
        
        console.log('⏰ [Sync] Sincronização periódica iniciada (30s)');
    }

    stopPeriodicSync() {
        if (this.syncInterval) {
            clearInterval(this.syncInterval);
            this.syncInterval = null;
            console.log('⏹️ [Sync] Sincronização periódica parada');
        }
    }

    // Métodos para IndexedDB (simulação)
    async saveToIndexedDB(store, key, data) {
        // Em produção, usar IndexedDB real
        // Aqui simularemos com arquivos para demonstração
        const fs = require('fs').promises;
        const path = require('path');
        
        try {
            const dbDir = path.join(process.cwd(), 'offline-db', store);
            await fs.mkdir(dbDir, { recursive: true });
            
            const filePath = path.join(dbDir, `${key}.json`);
            await fs.writeFile(filePath, JSON.stringify(data, null, 2));
        } catch (error) {
            console.error(`❌ [IndexedDB] Erro ao salvar ${store}/${key}:`, error);
        }
    }

    async getFromIndexedDB(store, key) {
        const fs = require('fs').promises;
        const path = require('path');
        
        try {
            const filePath = path.join(process.cwd(), 'offline-db', store, `${key}.json`);
            const data = await fs.readFile(filePath, 'utf8');
            return JSON.parse(data);
        } catch (error) {
            // Arquivo não existe ou erro de leitura
            return null;
        }
    }

    async getAllFromIndexedDB(store) {
        const fs = require('fs').promises;
        const path = require('path');
        
        try {
            const dbDir = path.join(process.cwd(), 'offline-db', store);
            const files = await fs.readdir(dbDir);
            
            const allData = [];
            for (const file of files) {
                if (file.endsWith('.json')) {
                    const filePath = path.join(dbDir, file);
                    const data = await fs.readFile(filePath, 'utf8');
                    allData.push(JSON.parse(data));
                }
            }
            
            return allData;
        } catch (error) {
            return [];
        }
    }

    async removeFromIndexedDB(store, key) {
        const fs = require('fs').promises;
        const path = require('path');
        
        try {
            const filePath = path.join(process.cwd(), 'offline-db', store, `${key}.json`);
            await fs.unlink(filePath);
        } catch (error) {
            // Arquivo não existe
        }
    }

    generateCacheKey(url) {
        // Gerar chave de cache baseada na URL
        const crypto = require('crypto');
        return crypto.createHash('md5').update(url).digest('hex');
    }

    // API pública
    getStatus() {
        return {
            isOnline: this.isOnline,
            syncQueueLength: this.syncQueue.length,
            conflictQueueLength: this.conflictQueue.length,
            lastSyncTimestamp: this.lastSyncTimestamp,
            syncInProgress: this.syncInProgress
        };
    }

    async forceSyncNow() {
        if (this.isOnline) {
            await this.processSyncQueue();
        } else {
            throw new Error('Não é possível sincronizar offline');
        }
    }

    getPendingConflicts() {
        return this.conflictQueue.filter(conflict => conflict.status === 'pending');
    }

    async clearOfflineData() {
        try {
            const fs = require('fs').promises;
            const path = require('path');
            
            const dbDir = path.join(process.cwd(), 'offline-db');
            await fs.rmdir(dbDir, { recursive: true });
            
            this.syncQueue = [];
            this.conflictQueue = [];
            
            console.log('🧹 [Cleanup] Dados offline limpos');
        } catch (error) {
            console.error('❌ [Cleanup] Erro ao limpar dados offline:', error);
        }
    }
}

module.exports = DigimundoOfflineSync;

// Para uso standalone
if (require.main === module) {
    const mockCore = {
        data: {
            save: async (collection, data) => {
                console.log(`Mock save: ${collection}`, data);
                return data;
            }
        }
    };

    const offlineSync = new DigimundoOfflineSync(mockCore);
    
    // Simular algumas operações
    setTimeout(async () => {
        console.log('📊 Status:', offlineSync.getStatus());
        
        // Simular item na queue
        await offlineSync.queueRequest('/api/test', {
            method: 'POST',
            body: JSON.stringify({ test: 'data' })
        });
        
        console.log('📊 Status após queue:', offlineSync.getStatus());
    }, 2000);
}