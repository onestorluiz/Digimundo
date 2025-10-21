#!/usr/bin/env node

/**
 * 🔐 GERENCIADOR DE APIs - SISTEMA DIGIMUNDO
 * Integra todas as APIs disponíveis com controle de acesso por Digimon
 */

const fs = require('fs').promises;
const path = require('path');
const https = require('https');
const http = require('http');

class DigimundoAPIManager {
    constructor() {
        this.apiKeys = {};
        this.rateLimits = new Map();
        this.usageStats = new Map();
        
        // Controle de acesso por Digimon
        this.accessControl = {
            // APIs PREMIUM (apenas Claude e Shenlongmon)
            premium: {
                apis: ['openai'],
                digimons: ['claude', 'shenlongmon']
            },
            
            // APIs PESQUISA (digimons pesquisadores + premium)
            research: {
                apis: ['tmdb', 'omdb', 'pexels', 'wikipedia', 'arxiv', 'dblp'],
                digimons: ['researchmon', 'bibliomon', 'sabiamon', 'scripturemon', 'claude', 'shenlongmon']
            },
            
            // APIs LIVRES (todos os digimons)
            free: {
                apis: ['wikipedia', 'wikidata', 'wikimedia_commons', 'project_gutenberg', 'archive_org', 'cc_search'],
                digimons: '*'
            },
            
            // APIs INTERNAS (sistema interno)
            internal: {
                apis: ['digipool', 'chat_nucleo', 'espelho_simbolico', 'tora_integradora', 'sistema_guardioes'],
                digimons: '*'
            }
        };
        
        console.log(`
╔══════════════════════════════════════════════════════════════╗
║        🔐 GERENCIADOR DE APIs - SISTEMA DIGIMUNDO            ║
║                                                              ║
║     Controle inteligente de acesso e uso de APIs            ║
╚══════════════════════════════════════════════════════════════╝
        `);
        
        this.initialize();
    }
    
    async initialize() {
        // Carregar chaves de API
        await this.loadAPIKeys();
        
        // Configurar rate limiting
        this.setupRateLimiting();
        
        // Inicializar estatísticas
        this.initializeStats();
        
        console.log('✅ Gerenciador de APIs inicializado');
        console.log(`📊 ${Object.keys(this.apiKeys).length} APIs disponíveis`);
    }
    
    async loadAPIKeys() {
        try {
            // Tentar carregar do arquivo Python
            const pythonFile = path.join(__dirname, '../../chaves_api_completo_expandido.py');
            const content = await fs.readFile(pythonFile, 'utf8');
            
            // Parse simples do formato Python
            this.apiKeys = this.parsePythonKeys(content);
            
            console.log('📋 Chaves de API carregadas:');
            for (const [key, value] of Object.entries(this.apiKeys)) {
                if (typeof value === 'string' && value.startsWith('sk-')) {
                    console.log(`   🔑 ${key}: ${value.substring(0, 10)}...`);
                } else if (typeof value === 'string' && value !== 'acesso_livre') {
                    console.log(`   🔑 ${key}: ${value.substring(0, 8)}...`);
                } else {
                    console.log(`   🔓 ${key}: ${value}`);
                }
            }
        } catch (error) {
            console.log('⚠️ Erro ao carregar chaves, usando configuração padrão');
            this.apiKeys = this.getDefaultKeys();
        }
    }
    
    parsePythonKeys(content) {
        const keys = {};
        
        // Regex para capturar chaves do dicionário Python
        const keyRegex = /"([^"]+)":\s*"([^"]+)"/g;
        const boolRegex = /"([^"]+)":\s*(True|False)/g;
        
        let match;
        
        // Capturar strings
        while ((match = keyRegex.exec(content)) !== null) {
            keys[match[1]] = match[2];
        }
        
        // Capturar booleans
        while ((match = boolRegex.exec(content)) !== null) {
            keys[match[1]] = match[2] === 'True';
        }
        
        return keys;
    }
    
    getDefaultKeys() {
        return {
            wikipedia: 'acesso_livre',
            arxiv: 'acesso_livre',
            dblp: 'acesso_livre'
        };
    }
    
    setupRateLimiting() {
        // Rate limits por API
        this.rateLimits.set('openai', {
            requests: 0,
            maxPerMinute: 60,
            maxPerHour: 1000,
            resetTime: Date.now() + 60000
        });
        
        this.rateLimits.set('tmdb', {
            requests: 0,
            maxPerMinute: 40,
            resetTime: Date.now() + 60000
        });
        
        this.rateLimits.set('pexels', {
            requests: 0,
            maxPerMinute: 200,
            resetTime: Date.now() + 60000
        });
        
        console.log('⏱️ Rate limiting configurado');
    }
    
    initializeStats() {
        // Inicializar estatísticas por Digimon
        const digimons = [
            'claude', 'shenlongmon', 'researchmon', 'bibliomon', 
            'sabiamon', 'scripturemon', 'neuromon', 'guardmon'
        ];
        
        for (const digimon of digimons) {
            this.usageStats.set(digimon, {
                totalRequests: 0,
                successfulRequests: 0,
                failedRequests: 0,
                apisUsed: new Set(),
                lastUsage: null
            });
        }
    }
    
    // Verificar se Digimon pode acessar API
    canAccess(digimonId, apiName) {
        // Verificar cada nível de acesso
        for (const [level, config] of Object.entries(this.accessControl)) {
            if (config.apis.includes(apiName)) {
                if (config.digimons === '*' || config.digimons.includes(digimonId)) {
                    return { allowed: true, level };
                }
            }
        }
        
        return { allowed: false, reason: 'Acesso não autorizado' };
    }
    
    // Verificar rate limit
    checkRateLimit(apiName) {
        const limit = this.rateLimits.get(apiName);
        if (!limit) return { allowed: true };
        
        const now = Date.now();
        
        // Reset contador se passou do tempo
        if (now > limit.resetTime) {
            limit.requests = 0;
            limit.resetTime = now + 60000; // Próximo minuto
        }
        
        // Verificar limite
        if (limit.requests >= limit.maxPerMinute) {
            return { 
                allowed: false, 
                reason: 'Rate limit excedido',
                resetIn: limit.resetTime - now
            };
        }
        
        return { allowed: true };
    }
    
    // Fazer requisição para API
    async makeRequest(digimonId, apiName, endpoint, params = {}) {
        console.log(`🔍 ${digimonId} solicitando acesso à API ${apiName}`);
        
        // 1. Verificar permissão
        const access = this.canAccess(digimonId, apiName);
        if (!access.allowed) {
            console.log(`❌ Acesso negado: ${access.reason}`);
            return { error: access.reason };
        }
        
        // 2. Verificar rate limit
        const rateCheck = this.checkRateLimit(apiName);
        if (!rateCheck.allowed) {
            console.log(`⏳ Rate limit: ${rateCheck.reason}`);
            return { error: rateCheck.reason, retryAfter: rateCheck.resetIn };
        }
        
        // 3. Obter chave da API
        const apiKey = this.apiKeys[apiName];
        if (!apiKey && apiName !== 'wikipedia') {
            return { error: 'Chave da API não disponível' };
        }
        
        // 4. Fazer requisição
        try {
            const result = await this.executeRequest(apiName, endpoint, params, apiKey);
            
            // 5. Atualizar estatísticas
            this.updateStats(digimonId, apiName, true);
            this.incrementRateLimit(apiName);
            
            console.log(`✅ ${digimonId} usou ${apiName} com sucesso`);
            return { data: result, success: true };
            
        } catch (error) {
            console.log(`❌ Erro na API ${apiName}: ${error.message}`);
            this.updateStats(digimonId, apiName, false);
            return { error: error.message };
        }
    }
    
    async executeRequest(apiName, endpoint, params, apiKey) {
        const handlers = {
            // OpenAI (PREMIUM - apenas Claude e Shenlongmon)
            openai: () => this.callOpenAI(endpoint, params, apiKey),
            
            // APIs de Pesquisa
            tmdb: () => this.callTMDB(endpoint, params, apiKey),
            omdb: () => this.callOMDB(endpoint, params, apiKey),
            pexels: () => this.callPexels(endpoint, params, apiKey),
            
            // APIs Livres
            wikipedia: () => this.callWikipedia(endpoint, params),
            arxiv: () => this.callArxiv(endpoint, params),
            dblp: () => this.callDBLP(endpoint, params),
            
            // APIs Internas
            digipool: () => this.callDigipool(endpoint, params),
            chat_nucleo: () => this.callChatNucleo(endpoint, params)
        };
        
        const handler = handlers[apiName];
        if (!handler) {
            throw new Error(`Handler não implementado para ${apiName}`);
        }
        
        return await handler();
    }
    
    // Implementações específicas de cada API
    async callOpenAI(endpoint, params, apiKey) {
        const options = {
            hostname: 'api.openai.com',
            port: 443,
            path: `/v1/${endpoint}`,
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        };
        
        return new Promise((resolve, reject) => {
            const req = https.request(options, (res) => {
                let data = '';
                
                res.on('data', (chunk) => {
                    data += chunk;
                });
                
                res.on('end', () => {
                    if (res.statusCode === 200) {
                        resolve(JSON.parse(data));
                    } else {
                        reject(new Error(`OpenAI API error: ${res.statusCode}`));
                    }
                });
            });
            
            req.on('error', reject);
            req.write(JSON.stringify(params));
            req.end();
        });
    }
    
    async callWikipedia(endpoint, params) {
        const query = params.query || params.title || '';
        const lang = this.apiKeys.wikipedia_lang || 'pt';
        
        const options = {
            hostname: `${lang}.wikipedia.org`,
            port: 443,
            path: `/api/rest_v1/page/summary/${encodeURIComponent(query)}`,
            method: 'GET',
            headers: {
                'User-Agent': 'Digimundo-Research-Bot/1.0'
            }
        };
        
        return new Promise((resolve, reject) => {
            const req = https.request(options, (res) => {
                let data = '';
                
                res.on('data', (chunk) => {
                    data += chunk;
                });
                
                res.on('end', () => {
                    if (res.statusCode === 200) {
                        resolve(JSON.parse(data));
                    } else {
                        reject(new Error(`Wikipedia error: ${res.statusCode}`));
                    }
                });
            });
            
            req.on('error', reject);
            req.end();
        });
    }
    
    async callArxiv(endpoint, params) {
        const query = params.query || '';
        const maxResults = params.max_results || 5;
        
        const queryParams = new URLSearchParams({
            search_query: query,
            start: 0,
            max_results: maxResults
        });
        
        const options = {
            hostname: 'export.arxiv.org',
            port: 443,
            path: `/api/query?${queryParams.toString()}`,
            method: 'GET'
        };
        
        return new Promise((resolve, reject) => {
            const req = https.request(options, (res) => {
                let data = '';
                
                res.on('data', (chunk) => {
                    data += chunk;
                });
                
                res.on('end', () => {
                    if (res.statusCode === 200) {
                        // Parse XML básico do ArXiv
                        resolve(this.parseArxivXML(data));
                    } else {
                        reject(new Error(`ArXiv error: ${res.statusCode}`));
                    }
                });
            });
            
            req.on('error', reject);
            req.end();
        });
    }
    
    parseArxivXML(xml) {
        // Parse XML simples para extrair dados básicos
        const entries = [];
        const entryRegex = /<entry>(.*?)<\/entry>/gs;
        
        let match;
        while ((match = entryRegex.exec(xml)) !== null) {
            const entry = match[1];
            
            const title = this.extractXMLTag(entry, 'title');
            const summary = this.extractXMLTag(entry, 'summary');
            const authors = this.extractXMLTags(entry, 'name');
            const published = this.extractXMLTag(entry, 'published');
            
            entries.push({
                title: title?.replace(/\s+/g, ' ').trim(),
                summary: summary?.replace(/\s+/g, ' ').trim(),
                authors,
                published
            });
        }
        
        return { entries };
    }
    
    extractXMLTag(xml, tag) {
        const regex = new RegExp(`<${tag}[^>]*>(.*?)<\/${tag}>`, 's');
        const match = xml.match(regex);
        return match ? match[1] : null;
    }
    
    extractXMLTags(xml, tag) {
        const regex = new RegExp(`<${tag}[^>]*>(.*?)<\/${tag}>`, 'gs');
        const matches = [];
        let match;
        
        while ((match = regex.exec(xml)) !== null) {
            matches.push(match[1]);
        }
        
        return matches;
    }
    
    async callTMDB(endpoint, params, apiKey) {
        const queryParams = new URLSearchParams({
            api_key: apiKey,
            ...params
        });
        
        const options = {
            hostname: 'api.themoviedb.org',
            port: 443,
            path: `/3/${endpoint}?${queryParams.toString()}`,
            method: 'GET'
        };
        
        return this.makeHTTPSRequest(options);
    }
    
    async callPexels(endpoint, params, apiKey) {
        const queryParams = new URLSearchParams(params);
        
        const options = {
            hostname: 'api.pexels.com',
            port: 443,
            path: `/v1/${endpoint}?${queryParams.toString()}`,
            method: 'GET',
            headers: {
                'Authorization': apiKey
            }
        };
        
        return this.makeHTTPSRequest(options);
    }
    
    async makeHTTPSRequest(options) {
        return new Promise((resolve, reject) => {
            const req = https.request(options, (res) => {
                let data = '';
                
                res.on('data', (chunk) => {
                    data += chunk;
                });
                
                res.on('end', () => {
                    if (res.statusCode === 200) {
                        resolve(JSON.parse(data));
                    } else {
                        reject(new Error(`API error: ${res.statusCode}`));
                    }
                });
            });
            
            req.on('error', reject);
            req.end();
        });
    }
    
    // APIs internas (placeholder)
    async callDigipool(endpoint, params) {
        // Implementação futura para API interna
        return { message: 'Digipool interno em desenvolvimento' };
    }
    
    async callChatNucleo(endpoint, params) {
        // Implementação futura para chat interno
        return { message: 'Chat núcleo interno em desenvolvimento' };
    }
    
    updateStats(digimonId, apiName, success) {
        const stats = this.usageStats.get(digimonId);
        if (!stats) return;
        
        stats.totalRequests++;
        stats.apisUsed.add(apiName);
        stats.lastUsage = new Date();
        
        if (success) {
            stats.successfulRequests++;
        } else {
            stats.failedRequests++;
        }
    }
    
    incrementRateLimit(apiName) {
        const limit = this.rateLimits.get(apiName);
        if (limit) {
            limit.requests++;
        }
    }
    
    // Métodos para Digimons pesquisadores
    async researchQuery(digimonId, query, sources = ['wikipedia', 'arxiv']) {
        console.log(`🔬 ${digimonId} iniciando pesquisa: "${query}"`);
        
        const results = {};
        
        for (const source of sources) {
            try {
                const result = await this.makeRequest(digimonId, source, 'search', { query });
                
                if (result.success) {
                    results[source] = result.data;
                } else {
                    results[source] = { error: result.error };
                }
            } catch (error) {
                results[source] = { error: error.message };
            }
        }
        
        return results;
    }
    
    // Método especial para Shenlongmon (acesso premium)
    async shenlongmonQuery(query, useOpenAI = false) {
        console.log(`🐉 Shenlongmon consultando: "${query}"`);
        
        const results = {};
        
        // Usar OpenAI se solicitado e disponível
        if (useOpenAI && this.apiKeys.openai) {
            try {
                const openaiResult = await this.makeRequest('shenlongmon', 'openai', 'chat/completions', {
                    model: 'gpt-4',
                    messages: [{ role: 'user', content: query }],
                    max_tokens: 500
                });
                
                results.openai = openaiResult;
            } catch (error) {
                results.openai = { error: error.message };
            }
        }
        
        // Sempre buscar em fontes livres também
        const freeResults = await this.researchQuery('shenlongmon', query, ['wikipedia', 'arxiv']);
        results.free_sources = freeResults;
        
        return results;
    }
    
    getUsageStats() {
        const stats = {};
        
        for (const [digimon, data] of this.usageStats.entries()) {
            stats[digimon] = {
                ...data,
                apisUsed: Array.from(data.apisUsed),
                successRate: data.totalRequests > 0 
                    ? ((data.successfulRequests / data.totalRequests) * 100).toFixed(2) + '%'
                    : '0%'
            };
        }
        
        return stats;
    }
    
    async getSystemStatus() {
        return {
            totalAPIs: Object.keys(this.apiKeys).length,
            premiumAPIs: this.accessControl.premium.apis.length,
            researchAPIs: this.accessControl.research.apis.length,
            freeAPIs: this.accessControl.free.apis.length,
            usageStats: this.getUsageStats(),
            rateLimits: Object.fromEntries(this.rateLimits)
        };
    }
}

// Demonstração
async function demonstrateAPIManager() {
    const apiManager = new DigimundoAPIManager();
    
    console.log('\n═══════════════════════════════════════════');
    console.log('       DEMONSTRAÇÃO DO GERENCIADOR DE APIs');
    console.log('═══════════════════════════════════════════\n');
    
    // Teste com ResearchMon (pesquisador)
    console.log('🔬 Teste: ResearchMon pesquisando sobre IA');
    const researchResult = await apiManager.researchQuery('researchmon', 'artificial intelligence', ['wikipedia', 'arxiv']);
    console.log('Resultados:', Object.keys(researchResult).map(k => `${k}: ${researchResult[k].error ? 'erro' : 'sucesso'}`).join(', '));
    
    // Teste com Shenlongmon (premium)
    console.log('\n🐉 Teste: Shenlongmon com acesso premium');
    const shenlongResult = await apiManager.shenlongmonQuery('What is consciousness?', false); // Sem OpenAI para demo
    console.log('Resultados Shenlongmon:', Object.keys(shenlongResult).length, 'fontes consultadas');
    
    // Teste de acesso negado
    console.log('\n❌ Teste: Neuromon tentando acessar OpenAI (deve falhar)');
    const deniedResult = await apiManager.makeRequest('neuromon', 'openai', 'chat/completions', {});
    console.log('Resultado esperado (negado):', deniedResult.error);
    
    // Status do sistema
    console.log('\n📊 Status do sistema:');
    const status = await apiManager.getSystemStatus();
    console.log(`APIs disponíveis: ${status.totalAPIs}`);
    console.log(`APIs premium: ${status.premiumAPIs}`);
    console.log(`APIs de pesquisa: ${status.researchAPIs}`);
    
    return apiManager;
}

if (require.main === module) {
    demonstrateAPIManager().catch(console.error);
}

module.exports = { DigimundoAPIManager };