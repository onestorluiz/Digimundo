/**
 * 🧠 Base Holon - Unidade Autônoma Cognitiva
 * Implementa arquitetura cognitiva inspirada em sistemas biológicos
 * Cada Holon é simultaneamente um todo e uma parte
 */

const EventEmitter = require('events');
const crypto = require('crypto');

class BaseHolon extends EventEmitter {
    constructor(name, type = 'cognitive') {
        super();
        this.id = crypto.randomUUID();
        this.name = name;
        this.type = type;
        this.state = 'initializing';
        this.trustScores = new Map();
        this.capabilities = new Set();
        this.memory = new Map();
        this.goals = [];
        this.plans = [];
        this.cognitiveModules = {
            perception: null,
            memory: null,
            reasoning: null,
            action: null
        };
        
        // Métricas de desempenho
        this.metrics = {
            tasksCompleted: 0,
            successRate: 0,
            averageResponseTime: 0,
            autonomyLevel: 1,
            learningRate: 0
        };
        
        // Sistema de crenças e conhecimento
        this.beliefs = new Map();
        this.knowledge = new Map();
        
        this.initialize();
    }
    
    async initialize() {
        console.log(`🧠 Inicializando Holon: ${this.name}`);
        
        // Inicializar módulos cognitivos
        this.cognitiveModules.perception = new PerceptionModule(this);
        this.cognitiveModules.memory = new MemoryModule(this);
        this.cognitiveModules.reasoning = new ReasoningModule(this);
        this.cognitiveModules.action = new ActionModule(this);
        
        this.state = 'active';
        this.emit('initialized', { id: this.id, name: this.name });
    }
    
    // Percepção - Receber e processar informações do ambiente
    async perceive(input) {
        return await this.cognitiveModules.perception.process(input);
    }
    
    // Raciocínio - Processar informações e tomar decisões
    async reason(perception) {
        return await this.cognitiveModules.reasoning.process(perception);
    }
    
    // Ação - Executar decisões
    async act(decision) {
        return await this.cognitiveModules.action.execute(decision);
    }
    
    // Ciclo cognitivo completo
    async cognitiveCycle(input) {
        try {
            // 1. Perceber o ambiente
            const perception = await this.perceive(input);
            
            // 2. Atualizar memória
            await this.cognitiveModules.memory.store(perception);
            
            // 3. Raciocinar sobre a situação
            const decision = await this.reason(perception);
            
            // 4. Executar ação
            const result = await this.act(decision);
            
            // 5. Aprender com o resultado
            await this.learn(result);
            
            return result;
        } catch (error) {
            console.error(`❌ Erro no ciclo cognitivo de ${this.name}:`, error);
            return this.handleError(error);
        }
    }
    
    // Aprendizado - Melhorar com base em experiências
    async learn(experience) {
        // Atualizar crenças
        const belief = experience.success ? 'effective' : 'ineffective';
        this.beliefs.set(experience.action, belief);
        
        // Ajustar métricas
        this.metrics.tasksCompleted++;
        this.metrics.successRate = 
            (this.metrics.successRate * (this.metrics.tasksCompleted - 1) + 
            (experience.success ? 1 : 0)) / this.metrics.tasksCompleted;
        
        // Aumentar autonomia se taxa de sucesso for alta
        if (this.metrics.successRate > 0.8 && this.metrics.tasksCompleted > 10) {
            this.metrics.autonomyLevel = Math.min(5, this.metrics.autonomyLevel + 0.1);
        }
        
        this.emit('learned', { experience, metrics: this.metrics });
    }
    
    // Comunicação com outros Holons
    async communicate(targetHolon, message) {
        const trustScore = this.trustScores.get(targetHolon.id) || 0.5;
        
        if (trustScore < 0.3) {
            console.log(`⚠️ ${this.name} não confia em ${targetHolon.name} (trust: ${trustScore})`);
            return null;
        }
        
        const communication = {
            from: this.id,
            to: targetHolon.id,
            message,
            trustLevel: trustScore,
            timestamp: Date.now()
        };
        
        return await targetHolon.receiveMessage(communication);
    }
    
    // Receber mensagem de outro Holon
    async receiveMessage(communication) {
        const perception = await this.perceive({
            type: 'communication',
            data: communication
        });
        
        // Ajustar confiança baseado na qualidade da interação
        this.updateTrust(communication.from, perception.quality);
        
        return {
            acknowledged: true,
            response: await this.reason(perception)
        };
    }
    
    // Atualizar confiança em outro Holon
    updateTrust(holonId, quality) {
        const currentTrust = this.trustScores.get(holonId) || 0.5;
        const adjustment = quality > 0.7 ? 0.05 : quality < 0.3 ? -0.05 : 0;
        const newTrust = Math.max(0, Math.min(1, currentTrust + adjustment));
        this.trustScores.set(holonId, newTrust);
    }
    
    // Tratamento de erros com auto-recuperação
    handleError(error) {
        console.log(`🔧 ${this.name} tentando auto-recuperação...`);
        
        // Estratégias de recuperação
        const strategies = [
            () => this.rollbackState(),
            () => this.requestHelp(),
            () => this.degradeGracefully()
        ];
        
        for (const strategy of strategies) {
            try {
                return strategy();
            } catch (e) {
                continue;
            }
        }
        
        return { error: true, message: 'Falha na auto-recuperação' };
    }
    
    rollbackState() {
        // Reverter para último estado conhecido bom
        const lastGoodState = this.memory.get('lastGoodState');
        if (lastGoodState) {
            this.state = lastGoodState;
            return { recovered: true, method: 'rollback' };
        }
        throw new Error('Sem estado válido para rollback');
    }
    
    requestHelp() {
        // Pedir ajuda a outros Holons
        this.emit('help-needed', { holon: this.name, state: this.state });
        return { recovered: true, method: 'external-help' };
    }
    
    degradeGracefully() {
        // Operar com capacidade reduzida
        this.state = 'degraded';
        this.capabilities.delete('advanced-reasoning');
        return { recovered: true, method: 'degraded-mode' };
    }
}

// Módulo de Percepção
class PerceptionModule {
    constructor(holon) {
        this.holon = holon;
        this.filters = [];
        this.patterns = new Map();
    }
    
    async process(input) {
        // Filtrar e normalizar entrada
        let processed = input;
        for (const filter of this.filters) {
            processed = await filter(processed);
        }
        
        // Identificar padrões
        const patterns = this.identifyPatterns(processed);
        
        // Avaliar qualidade da percepção
        const quality = this.assessQuality(processed);
        
        return {
            raw: input,
            processed,
            patterns,
            quality,
            timestamp: Date.now()
        };
    }
    
    identifyPatterns(data) {
        const identified = [];
        for (const [name, pattern] of this.patterns) {
            if (pattern.matches(data)) {
                identified.push(name);
            }
        }
        return identified;
    }
    
    assessQuality(data) {
        // Avaliar completude e confiabilidade dos dados
        const completeness = data && Object.keys(data).length > 0 ? 1 : 0;
        const confidence = data.confidence || 0.5;
        return (completeness + confidence) / 2;
    }
}

// Módulo de Memória
class MemoryModule {
    constructor(holon) {
        this.holon = holon;
        this.shortTerm = [];
        this.longTerm = new Map();
        this.workingMemory = new Map();
        this.episodicMemory = [];
        this.maxShortTerm = 7; // Número mágico de Miller
    }
    
    async store(data) {
        // Adicionar à memória de curto prazo
        this.shortTerm.unshift(data);
        if (this.shortTerm.length > this.maxShortTerm) {
            // Mover para memória de longo prazo se relevante
            const old = this.shortTerm.pop();
            if (this.isRelevant(old)) {
                this.consolidate(old);
            }
        }
        
        // Atualizar memória de trabalho
        this.workingMemory.set('current', data);
        
        // Registrar episódio se significativo
        if (this.isSignificant(data)) {
            this.episodicMemory.push({
                data,
                context: this.holon.state,
                timestamp: Date.now()
            });
        }
    }
    
    retrieve(query) {
        // Buscar em todas as memórias
        const results = [];
        
        // Memória de curto prazo
        for (const item of this.shortTerm) {
            if (this.matches(item, query)) {
                results.push({ source: 'short-term', data: item });
            }
        }
        
        // Memória de longo prazo
        for (const [key, value] of this.longTerm) {
            if (this.matches(value, query)) {
                results.push({ source: 'long-term', data: value });
            }
        }
        
        return results;
    }
    
    consolidate(data) {
        // Consolidar memória de curto para longo prazo
        const key = this.generateKey(data);
        const existing = this.longTerm.get(key);
        
        if (existing) {
            // Reforçar memória existente
            existing.strength = (existing.strength || 1) + 0.1;
            existing.lastAccess = Date.now();
        } else {
            this.longTerm.set(key, {
                data,
                strength: 1,
                created: Date.now(),
                lastAccess: Date.now()
            });
        }
    }
    
    isRelevant(data) {
        // Determinar se dados são relevantes para armazenamento
        return data.quality > 0.5 || data.patterns?.length > 0;
    }
    
    isSignificant(data) {
        // Determinar se evento é significativo para memória episódica
        return data.quality > 0.8 || data.outcome === 'success';
    }
    
    matches(item, query) {
        // Verificar se item corresponde à query
        if (typeof query === 'string') {
            return JSON.stringify(item).includes(query);
        }
        if (typeof query === 'object') {
            for (const [key, value] of Object.entries(query)) {
                if (item[key] !== value) return false;
            }
            return true;
        }
        return false;
    }
    
    generateKey(data) {
        // Gerar chave única para armazenamento
        return `${data.type || 'generic'}_${Date.now()}`;
    }
}

// Módulo de Raciocínio
class ReasoningModule {
    constructor(holon) {
        this.holon = holon;
        this.rules = [];
        this.heuristics = new Map();
    }
    
    async process(perception) {
        // Aplicar regras
        const ruleResults = this.applyRules(perception);
        
        // Aplicar heurísticas
        const heuristicResults = this.applyHeuristics(perception);
        
        // Combinar resultados
        const decision = this.synthesize(ruleResults, heuristicResults);
        
        // Avaliar confiança na decisão
        decision.confidence = this.evaluateConfidence(decision);
        
        return decision;
    }
    
    applyRules(perception) {
        const results = [];
        for (const rule of this.rules) {
            if (rule.condition(perception)) {
                results.push(rule.action);
            }
        }
        return results;
    }
    
    applyHeuristics(perception) {
        const results = [];
        for (const [name, heuristic] of this.heuristics) {
            const score = heuristic.evaluate(perception);
            if (score > heuristic.threshold) {
                results.push({
                    heuristic: name,
                    score,
                    action: heuristic.action
                });
            }
        }
        return results;
    }
    
    synthesize(rules, heuristics) {
        // Combinar resultados de regras e heurísticas
        if (rules.length > 0) {
            // Regras têm prioridade
            return {
                action: rules[0],
                source: 'rule-based',
                alternatives: heuristics.map(h => h.action)
            };
        }
        
        if (heuristics.length > 0) {
            // Usar heurística com maior score
            const best = heuristics.reduce((a, b) => a.score > b.score ? a : b);
            return {
                action: best.action,
                source: 'heuristic',
                score: best.score
            };
        }
        
        // Ação padrão
        return {
            action: 'observe',
            source: 'default'
        };
    }
    
    evaluateConfidence(decision) {
        // Avaliar confiança na decisão
        if (decision.source === 'rule-based') return 0.9;
        if (decision.source === 'heuristic') return decision.score || 0.7;
        return 0.5;
    }
}

// Módulo de Ação
class ActionModule {
    constructor(holon) {
        this.holon = holon;
        this.executors = new Map();
        this.history = [];
    }
    
    async execute(decision) {
        // Registrar decisão
        this.history.push({
            decision,
            timestamp: Date.now(),
            state: this.holon.state
        });
        
        // Encontrar executor apropriado
        const executor = this.executors.get(decision.action) || this.defaultExecutor;
        
        try {
            // Executar ação
            const result = await executor.call(this, decision);
            
            // Registrar resultado
            result.success = true;
            result.action = decision.action;
            
            return result;
        } catch (error) {
            console.error(`❌ Erro ao executar ${decision.action}:`, error);
            return {
                success: false,
                action: decision.action,
                error: error.message
            };
        }
    }
    
    async defaultExecutor(decision) {
        // Executor padrão para ações não registradas
        console.log(`🤖 ${this.holon.name} executando: ${decision.action}`);
        return {
            executed: decision.action,
            timestamp: Date.now()
        };
    }
    
    registerExecutor(action, executor) {
        this.executors.set(action, executor);
    }
}

module.exports = BaseHolon;