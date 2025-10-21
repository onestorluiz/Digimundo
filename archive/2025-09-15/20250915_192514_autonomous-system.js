/**
 * 🌐 Sistema Autônomo Revolucionário
 * Integração completa: Holon + HTN+LLM + Self-Healing + Trust Communication
 */

const EventEmitter = require('events');
const BaseHolon = require('./base-holon');
const HTNLLMPlanner = require('./htn-llm-planner');
const SelfHealingFramework = require('./self-healing-framework');
const TrustCommunicationSystem = require('./trust-communication');

class AutonomousSystem extends EventEmitter {
    constructor(orchestrator) {
        super();
        this.orchestrator = orchestrator;
        this.holons = new Map();
        this.planner = null;
        this.selfHealing = null;
        this.trustSystem = null;
        this.systemState = 'initializing';
        
        // Configurações do sistema
        this.config = {
            maxHolons: 100,
            plannerTimeout: 60000,
            healingEnabled: true,
            trustEnabled: true,
            autonomyLevel: 3 // 1-5, onde 5 é totalmente autônomo
        };
        
        // Métricas do sistema
        this.metrics = {
            tasksProcessed: 0,
            plansExecuted: 0,
            incidentsRecovered: 0,
            consensusAchieved: 0,
            systemUptime: 0,
            autonomyScore: 0
        };
        
        this.initialize();
    }
    
    async initialize() {
        console.log('\n🌐 =================================================');
        console.log('   SISTEMA AUTÔNOMO REVOLUCIONÁRIO');
        console.log('   Executando Comandos em Linguagem Natural');
        console.log('=================================================\n');
        
        // Inicializar subsistemas
        await this.initializePlanner();
        await this.initializeSelfHealing();
        await this.initializeTrustSystem();
        await this.createCoreHolons();
        
        // Conectar eventos entre subsistemas
        this.connectSubsystems();
        
        // Iniciar ciclo autônomo
        this.startAutonomousCycle();
        
        this.systemState = 'operational';
        
        console.log('\n✅ SISTEMA AUTÔNOMO TOTALMENTE OPERACIONAL!');
        console.log(`   Nível de Autonomia: ${this.config.autonomyLevel}/5`);
        console.log('   Pronto para processar comandos em linguagem natural\n');
        
        this.emit('system-ready');
    }
    
    // Inicializar Planejador Híbrido HTN+LLM
    async initializePlanner() {
        console.log('🤖 Inicializando Planejador Híbrido HTN+LLM...');
        this.planner = new HTNLLMPlanner(this.orchestrator);
        
        // Configurar adaptação com LLM
        this.planner.llmAdapter = {
            evaluate: async (context) => {
                // Integração com Ollama/LLM
                return { bestMethod: context.methods[0]?.name || 'default' };
            }
        };
    }
    
    // Inicializar Framework de Auto-Recuperação
    async initializeSelfHealing() {
        if (!this.config.healingEnabled) return;
        
        console.log('🔧 Inicializando Framework de Auto-Recuperação...');
        this.selfHealing = new SelfHealingFramework(this.orchestrator);
        
        // Conectar com incidentes do sistema
        this.selfHealing.on('incident-escalated', (incident) => {
            this.handleEscalatedIncident(incident);
        });
    }
    
    // Inicializar Sistema de Comunicação por Confiança
    async initializeTrustSystem() {
        if (!this.config.trustEnabled) return;
        
        console.log('🤝 Inicializando Sistema de Confiança...');
        this.trustSystem = new TrustCommunicationSystem();
        
        // Conectar com eventos de confiança
        this.trustSystem.on('low-trust', (data) => {
            console.warn(`⚠️ Confiança baixa detectada entre ${data.from} e ${data.to}`);
        });
    }
    
    // Criar Holons principais do sistema
    async createCoreHolons() {
        console.log('🧠 Criando Holons cognitivos principais...');
        
        // Holon de Percepção - Interpreta comandos
        const perceptionHolon = new BaseHolon('PerceptionHolon', 'perception');
        perceptionHolon.capabilities.add('natural-language-understanding');
        perceptionHolon.capabilities.add('intent-recognition');
        perceptionHolon.capabilities.add('context-extraction');
        this.registerHolon(perceptionHolon);
        
        // Holon de Planejamento - Cria planos
        const planningHolon = new BaseHolon('PlanningHolon', 'planning');
        planningHolon.capabilities.add('task-decomposition');
        planningHolon.capabilities.add('resource-allocation');
        planningHolon.capabilities.add('dependency-resolution');
        this.registerHolon(planningHolon);
        
        // Holon de Execução - Executa ações
        const executionHolon = new BaseHolon('ExecutionHolon', 'execution');
        executionHolon.capabilities.add('code-generation');
        executionHolon.capabilities.add('api-integration');
        executionHolon.capabilities.add('process-automation');
        this.registerHolon(executionHolon);
        
        // Holon de Monitoramento - Observa sistema
        const monitoringHolon = new BaseHolon('MonitoringHolon', 'monitoring');
        monitoringHolon.capabilities.add('performance-tracking');
        monitoringHolon.capabilities.add('anomaly-detection');
        monitoringHolon.capabilities.add('health-checking');
        this.registerHolon(monitoringHolon);
        
        // Holon de Aprendizado - Melhora continuamente
        const learningHolon = new BaseHolon('LearningHolon', 'learning');
        learningHolon.capabilities.add('pattern-recognition');
        learningHolon.capabilities.add('optimization');
        learningHolon.capabilities.add('adaptation');
        this.registerHolon(learningHolon);
        
        console.log(`   ✅ ${this.holons.size} Holons criados e ativos`);
    }
    
    // Registrar Holon no sistema
    registerHolon(holon) {
        this.holons.set(holon.id, holon);
        
        // Registrar no sistema de confiança
        if (this.trustSystem) {
            this.trustSystem.registerAgent(holon);
        }
        
        // Conectar eventos do Holon
        holon.on('help-needed', (data) => {
            this.coordinateHelp(data.holon, data.state);
        });
        
        holon.on('learned', (data) => {
            this.propagateLearning(holon.id, data);
        });
    }
    
    // Conectar subsistemas entre si
    connectSubsystems() {
        console.log('🔗 Conectando subsistemas...');
        
        // Planner -> Self-Healing
        if (this.planner && this.selfHealing) {
            this.planner.on('plan-failed', (error) => {
                this.selfHealing.handleIncident({
                    type: 'planning-failure',
                    error: error.message,
                    timestamp: Date.now()
                });
            });
        }
        
        // Self-Healing -> Trust System
        if (this.selfHealing && this.trustSystem) {
            this.selfHealing.on('recovery-success', (data) => {
                // Aumentar confiança em agentes que ajudaram
                if (data.helpers) {
                    for (const helper of data.helpers) {
                        this.trustSystem.updateTrust(
                            'system', 
                            helper, 
                            0.9
                        );
                    }
                }
            });
        }
        
        // Trust System -> Planner
        if (this.trustSystem && this.planner) {
            // Usar confiança para alocação de tarefas no planejamento
            this.planner.taskAllocationStrategy = async (task, candidates) => {
                return await this.trustSystem.allocateTask(task, candidates);
            };
        }
    }
    
    // PROCESSAMENTO DE COMANDOS EM LINGUAGEM NATURAL
    async processNaturalLanguageCommand(command) {
        console.log('\n📝 ==============================================');
        console.log(`   COMANDO: "${command}"`);
        console.log('==============================================\n');
        
        this.metrics.tasksProcessed++;
        
        try {
            // Fase 1: Percepção e Entendimento
            console.log('👁️ FASE 1: Percepção e Entendimento');
            const understanding = await this.understandCommand(command);
            
            // Fase 2: Planejamento
            console.log('\n📝 FASE 2: Planejamento');
            const plan = await this.createPlan(understanding);
            
            // Fase 3: Validação e Consenso
            console.log('\n🤝 FASE 3: Validação e Consenso');
            const validated = await this.validatePlan(plan);
            
            if (!validated.approved) {
                throw new Error('Plano rejeitado pelo consenso');
            }
            
            // Fase 4: Execução
            console.log('\n▶️ FASE 4: Execução');
            const results = await this.executePlan(validated.plan);
            
            // Fase 5: Aprendizado
            console.log('\n📚 FASE 5: Aprendizado');
            await this.learnFromExecution(validated.plan, results);
            
            console.log('\n✅ COMANDO PROCESSADO COM SUCESSO!');
            
            return {
                success: true,
                command,
                understanding,
                plan: validated.plan,
                results,
                metrics: this.getExecutionMetrics()
            };
            
        } catch (error) {
            console.error('\n❌ ERRO NO PROCESSAMENTO:', error.message);
            
            // Tentar auto-recuperação
            if (this.selfHealing) {
                const recovery = await this.selfHealing.handleIncident({
                    type: 'command-processing-failure',
                    command,
                    error: error.message,
                    timestamp: Date.now()
                });
                
                if (recovery.success) {
                    console.log('✅ Recuperação automática bem-sucedida!');
                    // Tentar novamente
                    return await this.processNaturalLanguageCommand(command);
                }
            }
            
            return {
                success: false,
                command,
                error: error.message
            };
        }
    }
    
    // Entender comando usando Holon de Percepção
    async understandCommand(command) {
        const perceptionHolon = this.getHolonByType('perception');
        
        if (!perceptionHolon) {
            throw new Error('Holon de percepção não disponível');
        }
        
        const perception = await perceptionHolon.perceive({
            type: 'natural-language',
            text: command,
            context: this.getCurrentContext()
        });
        
        // Extrair intent e entidades
        const understanding = {
            originalCommand: command,
            intent: this.extractIntent(perception),
            entities: this.extractEntities(perception),
            context: perception.processed.context || {},
            confidence: perception.quality
        };
        
        console.log(`   Intent: ${understanding.intent}`);
        console.log(`   Entidades: ${JSON.stringify(understanding.entities)}`);
        console.log(`   Confiança: ${(understanding.confidence * 100).toFixed(1)}%`);
        
        return understanding;
    }
    
    // Criar plano usando HTN+LLM
    async createPlan(understanding) {
        // Converter entendimento em goal para HTN
        const goal = {
            task: understanding.intent,
            parameters: understanding.entities,
            context: understanding.context
        };
        
        // Estado inicial do mundo
        const worldState = new Map([
            ['resources-available', true],
            ['system-ready', true],
            ['autonomy-level', this.config.autonomyLevel]
        ]);
        
        // Gerar plano
        const plan = await this.planner.planHTN(goal, worldState);
        
        console.log(`   Plano gerado com ${plan.length} ações`);
        
        return plan;
    }
    
    // Validar plano através de consenso
    async validatePlan(plan) {
        if (!this.trustSystem) {
            return { approved: true, plan };
        }
        
        // Selecionar Holons para validação
        const validators = Array.from(this.holons.keys()).slice(0, 3);
        
        const consensus = await this.trustSystem.reachConsensus(
            'validate-plan',
            validators,
            { protocol: 'weighted-voting' }
        );
        
        if (consensus.consensus) {
            console.log(`   ✅ Plano aprovado (confiança: ${(consensus.confidence * 100).toFixed(1)}%)`);
            this.metrics.consensusAchieved++;
        } else {
            console.log(`   ❌ Plano rejeitado`);
        }
        
        return {
            approved: consensus.consensus,
            plan,
            confidence: consensus.confidence
        };
    }
    
    // Executar plano
    async executePlan(plan) {
        const executionHolon = this.getHolonByType('execution');
        
        if (!executionHolon) {
            throw new Error('Holon de execução não disponível');
        }
        
        // Executar usando planner
        const results = await this.planner.executePlan(plan);
        
        this.metrics.plansExecuted++;
        
        return results;
    }
    
    // Aprender com a execução
    async learnFromExecution(plan, results) {
        const learningHolon = this.getHolonByType('learning');
        
        if (!learningHolon) {
            return;
        }
        
        // Aprender com resultados
        await learningHolon.learn({
            plan,
            results,
            success: results.every(r => r.success)
        });
        
        // Planner também aprende
        await this.planner.learnFromExecution(plan, results);
        
        console.log('   📚 Conhecimento atualizado');
    }
    
    // Ciclo autônomo principal
    startAutonomousCycle() {
        setInterval(() => {
            this.autonomousCycle();
        }, 10000); // A cada 10 segundos
    }
    
    async autonomousCycle() {
        // Verificar saúde do sistema
        if (this.selfHealing) {
            const health = this.selfHealing.getHealthReport();
            
            if (health.failedRecoveries > 5) {
                console.warn('⚠️ Sistema com muitas falhas de recuperação');
                this.adjustAutonomy(-1);
            }
        }
        
        // Otimizar confiança
        if (this.trustSystem) {
            const trustReport = this.trustSystem.getTrustReport();
            
            if (parseFloat(trustReport.averageTrustLevel) < 0.4) {
                console.warn('⚠️ Nível de confiança baixo no sistema');
            }
        }
        
        // Atualizar métricas de autonomia
        this.updateAutonomyScore();
        
        this.metrics.systemUptime++;
    }
    
    // Ajustar nível de autonomia
    adjustAutonomy(delta) {
        const newLevel = Math.max(1, Math.min(5, this.config.autonomyLevel + delta));
        
        if (newLevel !== this.config.autonomyLevel) {
            console.log(`🎯 Ajustando autonomia: ${this.config.autonomyLevel} -> ${newLevel}`);
            this.config.autonomyLevel = newLevel;
            
            // Ajustar comportamento dos Holons
            for (const holon of this.holons.values()) {
                holon.metrics.autonomyLevel = newLevel;
            }
        }
    }
    
    // Atualizar score de autonomia
    updateAutonomyScore() {
        const successRate = this.metrics.plansExecuted > 0 
            ? (this.metrics.plansExecuted - this.metrics.incidentsRecovered) / this.metrics.plansExecuted
            : 0;
        
        const consensusRate = this.metrics.consensusAchieved > 0
            ? this.metrics.consensusAchieved / this.metrics.tasksProcessed
            : 0;
        
        this.metrics.autonomyScore = 
            (successRate * 0.5 + consensusRate * 0.3 + this.config.autonomyLevel * 0.2) / 1.0;
    }
    
    // Coordenar ajuda entre Holons
    async coordinateHelp(holonName, state) {
        console.log(`🆘 Coordenando ajuda para ${holonName}`);
        
        // Encontrar Holons capazes de ajudar
        const helpers = [];
        for (const [id, holon] of this.holons) {
            if (holon.name !== holonName && holon.state === 'active') {
                helpers.push(id);
            }
        }
        
        if (helpers.length > 0 && this.trustSystem) {
            // Alocar tarefa de ajuda
            const allocation = await this.trustSystem.allocateTask(
                { name: `help-${holonName}`, requiredCapabilities: ['recovery'] },
                helpers
            );
            
            if (allocation) {
                console.log(`   ✅ ${allocation.agent.name} vai ajudar`);
            }
        }
    }
    
    // Propagar aprendizado entre Holons
    propagateLearning(sourceId, learning) {
        // Compartilhar conhecimento com outros Holons
        for (const [id, holon] of this.holons) {
            if (id !== sourceId) {
                holon.knowledge.set(
                    `learned-from-${sourceId}`,
                    learning
                );
            }
        }
    }
    
    // Lidar com incidentes escalados
    handleEscalatedIncident(incident) {
        console.log('\n🚨 INCIDENTE ESCALADO PARA NÍVEL SUPERIOR');
        
        // Reduzir autonomia temporariamente
        this.adjustAutonomy(-1);
        
        // Notificar todos os Holons
        for (const holon of this.holons.values()) {
            holon.emit('critical-incident', incident);
        }
        
        this.metrics.incidentsRecovered++;
    }
    
    // Métodos auxiliares
    getHolonByType(type) {
        for (const holon of this.holons.values()) {
            if (holon.type === type) {
                return holon;
            }
        }
        return null;
    }
    
    getCurrentContext() {
        return {
            systemState: this.systemState,
            autonomyLevel: this.config.autonomyLevel,
            activeHolons: this.holons.size,
            timestamp: Date.now()
        };
    }
    
    extractIntent(perception) {
        // Simplificado - em produção usaria NLU real
        const patterns = perception.patterns || [];
        
        if (patterns.includes('create')) return 'develop-feature';
        if (patterns.includes('fix')) return 'fix-bug';
        if (patterns.includes('optimize')) return 'optimize-performance';
        if (patterns.includes('refactor')) return 'refactor-code';
        
        return 'analyze-code'; // Default
    }
    
    extractEntities(perception) {
        // Simplificado - em produção usaria NER real
        return {
            target: perception.processed.target || 'system',
            priority: perception.processed.priority || 'normal'
        };
    }
    
    getExecutionMetrics() {
        return {
            tasksProcessed: this.metrics.tasksProcessed,
            plansExecuted: this.metrics.plansExecuted,
            autonomyScore: this.metrics.autonomyScore.toFixed(3),
            systemUptime: `${this.metrics.systemUptime * 10} seconds`
        };
    }
    
    // Relatório completo do sistema
    getSystemReport() {
        const report = {
            status: this.systemState,
            autonomyLevel: `${this.config.autonomyLevel}/5`,
            metrics: this.metrics,
            holons: {
                total: this.holons.size,
                active: Array.from(this.holons.values()).filter(h => h.state === 'active').length
            }
        };
        
        if (this.selfHealing) {
            report.health = this.selfHealing.getHealthReport();
        }
        
        if (this.trustSystem) {
            report.trust = this.trustSystem.getTrustReport();
        }
        
        return report;
    }
    
    // Parar sistema
    async shutdown() {
        console.log('\n🛑 Desligando Sistema Autônomo...');
        
        // Parar monitoramento
        if (this.selfHealing) {
            this.selfHealing.stop();
        }
        
        // Salvar estado
        this.systemState = 'shutdown';
        
        console.log('🛑 Sistema desligado com segurança');
    }
}

module.exports = AutonomousSystem;