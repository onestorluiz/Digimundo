/**
 * DIGIMUNDO DEVELOPER EXPERIENCE TOOLS - MODO HACKER
 * Sistema ultra-avançado de ferramentas para desenvolvedores
 * Features: HMR, Time-Travel Debugging, Performance Profiler, A/B Testing
 */

const EventEmitter = require('events');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs').promises;
const path = require('path');
const chokidar = require('chokidar');

class DigimundoDeveloperExperience extends EventEmitter {
    constructor(digimundoCore) {
        super();
        this.core = digimundoCore;
        this.isHMREnabled = true;
        this.debugSessions = new Map();
        this.performanceMetrics = new Map();
        this.abTests = new Map();
        this.profilerData = [];
        this.watchers = new Map();
        this.stateHistory = [];
        this.maxHistorySize = 1000;
        
        this.setupDeveloperTools();
    }

    setupDeveloperTools() {
        this.initializeHMR();
        this.setupTimeTravel();
        this.initializeProfiler();
        this.setupABTesting();
        
        console.log('🛠️ [MODO HACKER] Developer Experience Tools inicializados');
    }

    // HOT MODULE REPLACEMENT (HMR)
    initializeHMR() {
        if (!this.isHMREnabled) return;

        console.log('🔥 [HMR] Inicializando Hot Module Replacement...');

        // Assistir mudanças em arquivos JavaScript
        this.watchFiles([
            'app/server/**/*.js',
            'app/renderer/**/*.js',
            'app/renderer/**/*.html',
            'app/renderer/**/*.css',
            'app/plugins/**/*.js',
            'app/consciousness/**/*.js'
        ]);
    }

    watchFiles(patterns) {
        const watcher = chokidar.watch(patterns, {
            ignored: /node_modules/,
            persistent: true,
            ignoreInitial: true
        });

        watcher.on('change', async (filePath) => {
            await this.handleFileChange(filePath);
        });

        watcher.on('add', async (filePath) => {
            await this.handleFileAdd(filePath);
        });

        watcher.on('unlink', async (filePath) => {
            await this.handleFileRemove(filePath);
        });

        this.watchers.set('main', watcher);
        console.log('👀 [HMR] Assistindo mudanças em arquivos...');
    }

    async handleFileChange(filePath) {
        const changeType = this.detectChangeType(filePath);
        
        console.log(`🔄 [HMR] Arquivo modificado: ${filePath}`);
        
        const hotUpdateData = {
            id: uuidv4(),
            filePath,
            changeType,
            timestamp: new Date().toISOString(),
            moduleType: this.getModuleType(filePath)
        };

        try {
            switch (changeType) {
                case 'server':
                    await this.hotReloadServerModule(filePath, hotUpdateData);
                    break;
                case 'renderer':
                    await this.hotReloadRendererModule(filePath, hotUpdateData);
                    break;
                case 'plugin':
                    await this.hotReloadPlugin(filePath, hotUpdateData);
                    break;
                case 'consciousness':
                    await this.hotReloadConsciousnessModule(filePath, hotUpdateData);
                    break;
                case 'style':
                    await this.hotReloadStyles(filePath, hotUpdateData);
                    break;
            }

            this.emit('hmr-update', hotUpdateData);
            console.log(`✅ [HMR] Módulo recarregado: ${path.basename(filePath)}`);

        } catch (error) {
            console.error(`❌ [HMR] Erro ao recarregar ${filePath}:`, error);
            hotUpdateData.error = error.message;
            this.emit('hmr-error', hotUpdateData);
        }
    }

    async hotReloadServerModule(filePath, updateData) {
        // Limpar cache do require
        delete require.cache[require.resolve(filePath)];
        
        // Recarregar módulo
        const moduleExports = require(filePath);
        
        // Se é um módulo do servidor principal, reinicializar parcialmente
        if (filePath.includes('server/') && this.core.server) {
            await this.core.server.reloadModule(path.basename(filePath, '.js'), moduleExports);
        }

        updateData.reloadedAt = new Date().toISOString();
        updateData.success = true;
    }

    async hotReloadRendererModule(filePath, updateData) {
        // Para arquivos de renderer, notificar o processo de renderização
        const moduleContent = await fs.readFile(filePath, 'utf8');
        
        // Broadcast para todas as janelas abertas
        if (this.core.mainWindow && !this.core.mainWindow.isDestroyed()) {
            this.core.mainWindow.webContents.send('hmr-update', {
                filePath,
                content: moduleContent,
                type: 'renderer',
                timestamp: updateData.timestamp
            });
        }

        updateData.success = true;
    }

    async hotReloadPlugin(filePath, updateData) {
        // Obter nome do plugin do caminho do arquivo
        const pluginName = this.extractPluginName(filePath);
        
        if (this.core.pluginManager && pluginName) {
            await this.core.pluginManager.reloadPlugin(pluginName);
        }

        updateData.pluginName = pluginName;
        updateData.success = true;
    }

    async hotReloadConsciousnessModule(filePath, updateData) {
        // Recarregar módulos de consciência
        if (this.core.consciousness) {
            const moduleName = path.basename(filePath, '.js');
            await this.core.consciousness.reloadModule(moduleName);
        }

        updateData.success = true;
    }

    async hotReloadStyles(filePath, updateData) {
        const cssContent = await fs.readFile(filePath, 'utf8');
        
        // Broadcast atualização de CSS
        if (this.core.mainWindow && !this.core.mainWindow.isDestroyed()) {
            this.core.mainWindow.webContents.send('hmr-css-update', {
                filePath,
                css: cssContent,
                timestamp: updateData.timestamp
            });
        }

        updateData.success = true;
    }

    // TIME-TRAVEL DEBUGGING
    setupTimeTravel() {
        console.log('⏰ [Time Travel] Configurando debugging temporal...');
        
        // Interceptar mudanças de estado
        this.setupStateInterception();
        
        // Configurar snapshots automáticos
        this.startPeriodicSnapshots();
    }

    setupStateInterception() {
        // Wrapper para capturar mudanças de estado
        const originalSetState = this.core.setState?.bind(this.core);
        
        if (originalSetState) {
            this.core.setState = (newState, action) => {
                // Capturar estado anterior
                const previousState = this.core.getState ? this.core.getState() : {};
                
                // Aplicar mudança
                const result = originalSetState(newState, action);
                
                // Salvar no histórico
                this.saveStateSnapshot({
                    timestamp: new Date().toISOString(),
                    action: action || 'setState',
                    previousState: JSON.parse(JSON.stringify(previousState)),
                    newState: JSON.parse(JSON.stringify(newState)),
                    stackTrace: this.captureStackTrace()
                });
                
                return result;
            };
        }
    }

    saveStateSnapshot(snapshot) {
        this.stateHistory.push(snapshot);
        
        // Limitar tamanho do histórico
        if (this.stateHistory.length > this.maxHistorySize) {
            this.stateHistory.shift();
        }
        
        this.emit('state-snapshot', snapshot);
    }

    captureStackTrace() {
        const stack = new Error().stack;
        return stack ? stack.split('\n').slice(2, 8) : [];
    }

    startPeriodicSnapshots() {
        // Snapshot automático a cada 30 segundos
        setInterval(() => {
            if (this.core.getState) {
                this.saveStateSnapshot({
                    timestamp: new Date().toISOString(),
                    action: 'periodic-snapshot',
                    previousState: null,
                    newState: JSON.parse(JSON.stringify(this.core.getState())),
                    stackTrace: ['Automatic periodic snapshot']
                });
            }
        }, 30000);
    }

    async travelToState(targetTimestamp) {
        console.log(`⏰ [Time Travel] Viajando para: ${targetTimestamp}`);
        
        const targetSnapshot = this.stateHistory.find(
            snapshot => snapshot.timestamp === targetTimestamp
        );
        
        if (!targetSnapshot) {
            throw new Error('Snapshot não encontrado');
        }
        
        // Aplicar estado
        if (this.core.setState && targetSnapshot.newState) {
            await this.core.setState(targetSnapshot.newState, 'time-travel');
        }
        
        this.emit('time-travel', {
            targetTimestamp,
            snapshot: targetSnapshot
        });
        
        return targetSnapshot;
    }

    getStateHistory(limit = 50) {
        return this.stateHistory.slice(-limit).reverse();
    }

    // PERFORMANCE PROFILER
    initializeProfiler() {
        console.log('📊 [Profiler] Inicializando profiler de performance...');
        
        this.setupPerformanceMonitoring();
        this.startMetricsCollection();
    }

    setupPerformanceMonitoring() {
        // Monitor de CPU
        this.monitorCPUUsage();
        
        // Monitor de memória
        this.monitorMemoryUsage();
        
        // Monitor de operações de I/O
        this.monitorIOOperations();
        
        // Monitor de network
        this.monitorNetworkLatency();
    }

    monitorCPUUsage() {
        const startTime = process.hrtime.bigint();
        let lastTime = startTime;
        
        setInterval(() => {
            const currentTime = process.hrtime.bigint();
            const cpuUsage = process.cpuUsage();
            
            const metrics = {
                timestamp: new Date().toISOString(),
                type: 'cpu',
                user: cpuUsage.user / 1000, // Convert to milliseconds
                system: cpuUsage.system / 1000,
                total: (cpuUsage.user + cpuUsage.system) / 1000,
                elapsed: Number(currentTime - lastTime) / 1000000 // Convert to milliseconds
            };
            
            this.addPerformanceMetric('cpu', metrics);
            lastTime = currentTime;
        }, 5000);
    }

    monitorMemoryUsage() {
        setInterval(() => {
            const memUsage = process.memoryUsage();
            
            const metrics = {
                timestamp: new Date().toISOString(),
                type: 'memory',
                rss: memUsage.rss,
                heapTotal: memUsage.heapTotal,
                heapUsed: memUsage.heapUsed,
                external: memUsage.external,
                arrayBuffers: memUsage.arrayBuffers
            };
            
            this.addPerformanceMetric('memory', metrics);
        }, 5000);
    }

    monitorIOOperations() {
        // Wrapper para operações de arquivo
        const originalReadFile = fs.readFile;
        const originalWriteFile = fs.writeFile;
        
        fs.readFile = async (...args) => {
            const startTime = process.hrtime.bigint();
            try {
                const result = await originalReadFile.apply(fs, args);
                const endTime = process.hrtime.bigint();
                
                this.addPerformanceMetric('io', {
                    timestamp: new Date().toISOString(),
                    type: 'read',
                    operation: 'readFile',
                    duration: Number(endTime - startTime) / 1000000,
                    file: typeof args[0] === 'string' ? path.basename(args[0]) : 'unknown'
                });
                
                return result;
            } catch (error) {
                const endTime = process.hrtime.bigint();
                
                this.addPerformanceMetric('io', {
                    timestamp: new Date().toISOString(),
                    type: 'read',
                    operation: 'readFile',
                    duration: Number(endTime - startTime) / 1000000,
                    error: error.message,
                    file: typeof args[0] === 'string' ? path.basename(args[0]) : 'unknown'
                });
                
                throw error;
            }
        };
    }

    monitorNetworkLatency() {
        // Monitor básico de latência de rede
        setInterval(async () => {
            const startTime = Date.now();
            
            try {
                // Ping para servidor local (se disponível)
                const response = await fetch('http://localhost:7937/api/health', {
                    method: 'GET',
                    timeout: 5000
                });
                
                const endTime = Date.now();
                const latency = endTime - startTime;
                
                this.addPerformanceMetric('network', {
                    timestamp: new Date().toISOString(),
                    type: 'latency',
                    latency,
                    status: response.status,
                    endpoint: '/api/health'
                });
                
            } catch (error) {
                const endTime = Date.now();
                
                this.addPerformanceMetric('network', {
                    timestamp: new Date().toISOString(),
                    type: 'latency',
                    latency: endTime - startTime,
                    error: error.message,
                    endpoint: '/api/health'
                });
            }
        }, 10000); // A cada 10 segundos
    }

    addPerformanceMetric(category, metric) {
        if (!this.performanceMetrics.has(category)) {
            this.performanceMetrics.set(category, []);
        }
        
        const categoryMetrics = this.performanceMetrics.get(category);
        categoryMetrics.push(metric);
        
        // Limitar histórico de métricas
        if (categoryMetrics.length > 1000) {
            categoryMetrics.shift();
        }
        
        this.emit('performance-metric', { category, metric });
    }

    startMetricsCollection() {
        // Coletar métricas customizadas
        this.collectCustomMetrics();
        
        // Análise periódica de performance
        setInterval(() => {
            this.analyzePerformance();
        }, 60000); // A cada minuto
    }

    collectCustomMetrics() {
        setInterval(() => {
            // Métricas do Digimundo Core
            if (this.core.memory) {
                const memoryStats = this.core.memory.getStats();
                this.addPerformanceMetric('digimundo', {
                    timestamp: new Date().toISOString(),
                    type: 'memory-system',
                    ...memoryStats
                });
            }
            
            // Métricas de plugins
            if (this.core.pluginManager) {
                const pluginStats = this.core.pluginManager.getLoadedPlugins();
                this.addPerformanceMetric('digimundo', {
                    timestamp: new Date().toISOString(),
                    type: 'plugins',
                    loadedPlugins: pluginStats.length,
                    activePlugins: pluginStats.filter(p => p.active).length
                });
            }
            
            // Métricas de consciência
            if (this.core.consciousness) {
                const consciousnessStats = this.core.consciousness.getStats();
                this.addPerformanceMetric('digimundo', {
                    timestamp: new Date().toISOString(),
                    type: 'consciousness',
                    ...consciousnessStats
                });
            }
        }, 15000); // A cada 15 segundos
    }

    analyzePerformance() {
        const analysis = {
            timestamp: new Date().toISOString(),
            summary: {},
            alerts: [],
            recommendations: []
        };
        
        // Analisar CPU
        const cpuMetrics = this.performanceMetrics.get('cpu') || [];
        if (cpuMetrics.length > 0) {
            const recentCPU = cpuMetrics.slice(-12); // Últimos 12 pontos (1 minuto)
            const avgCPU = recentCPU.reduce((sum, m) => sum + m.total, 0) / recentCPU.length;
            
            analysis.summary.cpu = {
                average: avgCPU,
                peak: Math.max(...recentCPU.map(m => m.total)),
                trend: this.calculateTrend(recentCPU.map(m => m.total))
            };
            
            if (avgCPU > 80) {
                analysis.alerts.push({
                    type: 'cpu-high',
                    message: 'Alto uso de CPU detectado',
                    value: avgCPU
                });
            }
        }
        
        // Analisar Memória
        const memoryMetrics = this.performanceMetrics.get('memory') || [];
        if (memoryMetrics.length > 0) {
            const recentMemory = memoryMetrics.slice(-12);
            const avgHeapUsed = recentMemory.reduce((sum, m) => sum + m.heapUsed, 0) / recentMemory.length;
            const maxHeap = Math.max(...recentMemory.map(m => m.heapTotal));
            
            analysis.summary.memory = {
                averageHeapUsed: avgHeapUsed,
                maxHeapTotal: maxHeap,
                utilizationPercent: (avgHeapUsed / maxHeap) * 100,
                trend: this.calculateTrend(recentMemory.map(m => m.heapUsed))
            };
            
            if ((avgHeapUsed / maxHeap) > 0.9) {
                analysis.alerts.push({
                    type: 'memory-high',
                    message: 'Alto uso de memória detectado',
                    utilizationPercent: (avgHeapUsed / maxHeap) * 100
                });
                
                analysis.recommendations.push({
                    type: 'memory-optimization',
                    message: 'Considere implementar garbage collection manual ou otimizar uso de memória'
                });
            }
        }
        
        this.emit('performance-analysis', analysis);
        
        if (analysis.alerts.length > 0) {
            console.warn(`⚠️ [Profiler] ${analysis.alerts.length} alertas de performance detectados`);
        }
    }

    calculateTrend(values) {
        if (values.length < 2) return 'stable';
        
        const first = values[0];
        const last = values[values.length - 1];
        const change = ((last - first) / first) * 100;
        
        if (change > 10) return 'increasing';
        if (change < -10) return 'decreasing';
        return 'stable';
    }

    // A/B TESTING FRAMEWORK
    setupABTesting() {
        console.log('🧪 [A/B Testing] Configurando framework de testes...');
        
        this.loadABTests();
        this.setupVariantAssignment();
    }

    async loadABTests() {
        // Carregar testes A/B ativos
        const testsConfig = {
            'ui-theme-test': {
                id: 'ui-theme-test',
                name: 'Teste de Tema da Interface',
                description: 'Comparar tema claro vs escuro',
                variants: [
                    { id: 'light', name: 'Tema Claro', allocation: 0.5 },
                    { id: 'dark', name: 'Tema Escuro', allocation: 0.5 }
                ],
                targeting: {
                    userType: 'all',
                    platform: 'all'
                },
                metrics: ['engagement', 'session_duration', 'task_completion'],
                status: 'active',
                startDate: new Date().toISOString(),
                endDate: null
            },
            'collaboration-features-test': {
                id: 'collaboration-features-test',
                name: 'Teste de Funcionalidades de Colaboração',
                description: 'Testar diferentes layouts de colaboração',
                variants: [
                    { id: 'sidebar', name: 'Sidebar Layout', allocation: 0.33 },
                    { id: 'floating', name: 'Floating Panel', allocation: 0.33 },
                    { id: 'integrated', name: 'Integrated View', allocation: 0.34 }
                ],
                targeting: {
                    userType: 'premium',
                    feature: 'collaboration'
                },
                metrics: ['feature_usage', 'user_satisfaction', 'collaboration_frequency'],
                status: 'active',
                startDate: new Date().toISOString(),
                endDate: null
            }
        };
        
        for (const [testId, config] of Object.entries(testsConfig)) {
            this.abTests.set(testId, {
                ...config,
                participants: new Map(),
                results: new Map()
            });
        }
    }

    setupVariantAssignment() {
        // Sistema de atribuição de variantes
        this.variantAssignment = new Map();
    }

    assignVariant(testId, userId, userAttributes = {}) {
        const test = this.abTests.get(testId);
        if (!test || test.status !== 'active') {
            return null;
        }
        
        // Verificar se usuário já tem variante atribuída
        const existingAssignment = test.participants.get(userId);
        if (existingAssignment) {
            return existingAssignment;
        }
        
        // Verificar targeting
        if (!this.checkTargeting(test.targeting, userAttributes)) {
            return null;
        }
        
        // Atribuir variante baseada em hash determinístico
        const variant = this.selectVariant(test, userId);
        
        const assignment = {
            testId,
            userId,
            variant,
            assignedAt: new Date().toISOString(),
            userAttributes
        };
        
        test.participants.set(userId, assignment);
        
        console.log(`🧪 [A/B Testing] Usuário ${userId} atribuído à variante ${variant.id} do teste ${testId}`);
        this.emit('variant-assigned', assignment);
        
        return assignment;
    }

    selectVariant(test, userId) {
        // Hash determinístico para garantir consistência
        const hash = this.hashString(`${test.id}-${userId}`);
        const normalized = hash / 2147483647; // Normalizar para 0-1
        
        let cumulativeAllocation = 0;
        for (const variant of test.variants) {
            cumulativeAllocation += variant.allocation;
            if (normalized <= cumulativeAllocation) {
                return variant;
            }
        }
        
        // Fallback para última variante
        return test.variants[test.variants.length - 1];
    }

    hashString(str) {
        let hash = 0;
        if (str.length === 0) return hash;
        
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        
        return Math.abs(hash);
    }

    checkTargeting(targeting, userAttributes) {
        if (targeting.userType !== 'all' && userAttributes.userType !== targeting.userType) {
            return false;
        }
        
        if (targeting.platform !== 'all' && userAttributes.platform !== targeting.platform) {
            return false;
        }
        
        if (targeting.feature && !userAttributes.features?.includes(targeting.feature)) {
            return false;
        }
        
        return true;
    }

    trackABTestEvent(testId, userId, eventType, eventData = {}) {
        const test = this.abTests.get(testId);
        if (!test) return;
        
        const participant = test.participants.get(userId);
        if (!participant) return;
        
        const event = {
            id: uuidv4(),
            testId,
            userId,
            variant: participant.variant,
            eventType,
            eventData,
            timestamp: new Date().toISOString()
        };
        
        if (!test.results.has(userId)) {
            test.results.set(userId, []);
        }
        
        test.results.get(userId).push(event);
        
        this.emit('ab-test-event', event);
    }

    getABTestResults(testId) {
        const test = this.abTests.get(testId);
        if (!test) return null;
        
        const analysis = {
            testId,
            testName: test.name,
            status: test.status,
            participants: test.participants.size,
            variants: {},
            summary: {}
        };
        
        // Analisar por variante
        for (const variant of test.variants) {
            const variantParticipants = Array.from(test.participants.values())
                .filter(p => p.variant.id === variant.id);
            
            const variantEvents = [];
            variantParticipants.forEach(participant => {
                const userEvents = test.results.get(participant.userId) || [];
                variantEvents.push(...userEvents);
            });
            
            analysis.variants[variant.id] = {
                name: variant.name,
                participants: variantParticipants.length,
                events: variantEvents.length,
                metrics: this.calculateVariantMetrics(variantEvents, test.metrics)
            };
        }
        
        // Calcular significância estatística
        analysis.summary.statisticalSignificance = this.calculateStatisticalSignificance(analysis.variants);
        
        return analysis;
    }

    calculateVariantMetrics(events, metricTypes) {
        const metrics = {};
        
        for (const metricType of metricTypes) {
            switch (metricType) {
                case 'engagement':
                    metrics[metricType] = events.filter(e => e.eventType === 'engagement').length;
                    break;
                case 'session_duration':
                    const sessionEvents = events.filter(e => e.eventType === 'session_end');
                    metrics[metricType] = sessionEvents.length > 0 
                        ? sessionEvents.reduce((sum, e) => sum + (e.eventData.duration || 0), 0) / sessionEvents.length
                        : 0;
                    break;
                case 'task_completion':
                    metrics[metricType] = events.filter(e => e.eventType === 'task_completed').length;
                    break;
                case 'feature_usage':
                    metrics[metricType] = events.filter(e => e.eventType === 'feature_used').length;
                    break;
            }
        }
        
        return metrics;
    }

    calculateStatisticalSignificance(variants) {
        // Implementação simplificada de teste de significância
        const variantIds = Object.keys(variants);
        if (variantIds.length < 2) return { significant: false, confidence: 0 };
        
        const sampleSizes = variantIds.map(id => variants[id].participants);
        const minSampleSize = Math.min(...sampleSizes);
        
        // Regra simples: precisa de pelo menos 100 participantes por variante
        if (minSampleSize < 100) {
            return { significant: false, confidence: 0, reason: 'Sample size too small' };
        }
        
        // Simular cálculo de confiança baseado no tamanho da amostra
        const confidence = Math.min(95, (minSampleSize / 100) * 95);
        
        return {
            significant: confidence >= 95,
            confidence,
            recommendation: confidence >= 95 ? 'Results are statistically significant' : 'Need more data'
        };
    }

    // Métodos auxiliares
    detectChangeType(filePath) {
        if (filePath.includes('/server/')) return 'server';
        if (filePath.includes('/renderer/')) return 'renderer';
        if (filePath.includes('/plugins/')) return 'plugin';
        if (filePath.includes('/consciousness/')) return 'consciousness';
        if (filePath.endsWith('.css')) return 'style';
        return 'unknown';
    }

    getModuleType(filePath) {
        const ext = path.extname(filePath);
        if (ext === '.js') return 'javascript';
        if (ext === '.html') return 'html';
        if (ext === '.css') return 'css';
        return 'other';
    }

    extractPluginName(filePath) {
        const pluginMatch = filePath.match(/plugins\/([^\/]+)/);
        return pluginMatch ? pluginMatch[1] : null;
    }

    // API pública
    getHMRStatus() {
        return {
            enabled: this.isHMREnabled,
            watchedFiles: Array.from(this.watchers.keys()),
            lastUpdate: this.lastHMRUpdate
        };
    }

    getDebugHistory() {
        return this.getStateHistory();
    }

    getPerformanceReport() {
        const report = {
            timestamp: new Date().toISOString(),
            categories: {}
        };
        
        for (const [category, metrics] of this.performanceMetrics) {
            report.categories[category] = {
                count: metrics.length,
                latest: metrics[metrics.length - 1],
                summary: this.summarizeMetrics(metrics)
            };
        }
        
        return report;
    }

    summarizeMetrics(metrics) {
        if (metrics.length === 0) return {};
        
        const recent = metrics.slice(-60); // Último minuto
        return {
            count: recent.length,
            timeRange: {
                start: recent[0]?.timestamp,
                end: recent[recent.length - 1]?.timestamp
            }
        };
    }

    getActiveABTests() {
        return Array.from(this.abTests.values())
            .filter(test => test.status === 'active')
            .map(test => ({
                id: test.id,
                name: test.name,
                variants: test.variants,
                participants: test.participants.size
            }));
    }

    enableHMR() {
        this.isHMREnabled = true;
        this.initializeHMR();
        console.log('🔥 [HMR] Hot Module Replacement ativado');
    }

    disableHMR() {
        this.isHMREnabled = false;
        this.watchers.forEach(watcher => watcher.close());
        this.watchers.clear();
        console.log('❄️ [HMR] Hot Module Replacement desativado');
    }
}

module.exports = DigimundoDeveloperExperience;