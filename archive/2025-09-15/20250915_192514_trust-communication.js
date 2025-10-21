/**
 * 🤝 Trust-Based Agent Communication System
 * Sistema de comunicação entre agentes baseado em confiança dinâmica
 * Implementa reputação, consenso e alocação inteligente de tarefas
 */

const EventEmitter = require('events');
const crypto = require('crypto');

class TrustCommunicationSystem extends EventEmitter {
    constructor() {
        super();
        this.agents = new Map();
        this.trustMatrix = new Map(); // Matriz de confiança entre agentes
        this.reputationScores = new Map();
        this.communicationChannels = new Map();
        this.consensusProtocols = new Map();
        this.taskAllocationHistory = [];
        
        // Configurações do sistema
        this.config = {
            initialTrust: 0.5,
            trustDecayRate: 0.01,
            trustGrowthRate: 0.05,
            minimumTrustThreshold: 0.3,
            consensusThreshold: 0.67,
            reputationWeight: 0.7,
            performanceWeight: 0.3
        };
        
        // Métricas do sistema
        this.metrics = {
            totalMessages: 0,
            successfulCommunications: 0,
            failedCommunications: 0,
            consensusReached: 0,
            consensusFailed: 0,
            averageTrustLevel: 0.5
        };
        
        this.initialize();
    }
    
    async initialize() {
        console.log('\n🤝 Inicializando Sistema de Comunicação Baseado em Confiança...');
        
        // Configurar protocolos de consenso
        this.setupConsensusProtocols();
        
        // Configurar canais de comunicação
        this.setupCommunicationChannels();
        
        // Iniciar monitoramento de confiança
        this.startTrustMonitoring();
        
        console.log('✅ Sistema de comunicação confiável ativo!');
    }
    
    // Registrar novo agente no sistema
    registerAgent(agent) {
        const agentInfo = {
            id: agent.id,
            name: agent.name,
            capabilities: agent.capabilities || new Set(),
            status: 'active',
            registeredAt: Date.now(),
            performance: {
                tasksCompleted: 0,
                successRate: 1.0,
                averageResponseTime: 0
            }
        };
        
        this.agents.set(agent.id, agentInfo);
        
        // Inicializar confiança com outros agentes
        this.initializeTrust(agent.id);
        
        // Calcular reputação inicial
        this.calculateReputation(agent.id);
        
        console.log(`✅ Agente ${agent.name} registrado no sistema de confiança`);
        
        this.emit('agent-registered', agentInfo);
        
        return agentInfo;
    }
    
    // Inicializar matriz de confiança para novo agente
    initializeTrust(agentId) {
        if (!this.trustMatrix.has(agentId)) {
            this.trustMatrix.set(agentId, new Map());
        }
        
        // Confiança inicial com todos os outros agentes
        for (const [otherId] of this.agents) {
            if (otherId !== agentId) {
                // Confiança bidirecional
                this.trustMatrix.get(agentId).set(otherId, this.config.initialTrust);
                
                if (!this.trustMatrix.has(otherId)) {
                    this.trustMatrix.set(otherId, new Map());
                }
                this.trustMatrix.get(otherId).set(agentId, this.config.initialTrust);
            }
        }
    }
    
    // Enviar mensagem entre agentes
    async sendMessage(fromId, toId, message) {
        this.metrics.totalMessages++;
        
        // Verificar confiança
        const trustLevel = this.getTrust(fromId, toId);
        
        if (trustLevel < this.config.minimumTrustThreshold) {
            console.warn(`⚠️ Comunicação bloqueada: confiança baixa (${trustLevel.toFixed(2)})`);
            this.metrics.failedCommunications++;
            return {
                success: false,
                reason: 'Low trust level',
                trustLevel
            };
        }
        
        // Criar envelope seguro
        const envelope = this.createSecureEnvelope(fromId, toId, message, trustLevel);
        
        // Escolher canal baseado na confiança
        const channel = this.selectChannel(trustLevel);
        
        try {
            // Transmitir mensagem
            const response = await this.transmit(envelope, channel);
            
            // Atualizar confiança baseado no sucesso
            this.updateTrust(fromId, toId, response.quality);
            
            this.metrics.successfulCommunications++;
            
            return {
                success: true,
                response,
                channel,
                trustLevel
            };
        } catch (error) {
            console.error(`❌ Erro na comunicação: ${error.message}`);
            
            // Reduzir confiança após falha
            this.decreaseTrust(fromId, toId);
            
            this.metrics.failedCommunications++;
            
            return {
                success: false,
                error: error.message,
                trustLevel
            };
        }
    }
    
    // Criar envelope seguro para mensagem
    createSecureEnvelope(fromId, toId, message, trustLevel) {
        const timestamp = Date.now();
        const nonce = crypto.randomBytes(16).toString('hex');
        
        const envelope = {
            id: crypto.randomUUID(),
            from: fromId,
            to: toId,
            message,
            trustLevel,
            timestamp,
            nonce,
            signature: null
        };
        
        // Assinar mensagem se confiança for alta
        if (trustLevel > 0.7) {
            envelope.signature = this.signMessage(envelope);
        }
        
        return envelope;
    }
    
    // Assinar mensagem digitalmente
    signMessage(envelope) {
        const content = `${envelope.from}:${envelope.to}:${JSON.stringify(envelope.message)}:${envelope.timestamp}:${envelope.nonce}`;
        const hash = crypto.createHash('sha256').update(content).digest('hex');
        return hash;
    }
    
    // Verificar assinatura da mensagem
    verifySignature(envelope) {
        if (!envelope.signature) return true; // Sem assinatura para verificar
        
        const content = `${envelope.from}:${envelope.to}:${JSON.stringify(envelope.message)}:${envelope.timestamp}:${envelope.nonce}`;
        const hash = crypto.createHash('sha256').update(content).digest('hex');
        
        return hash === envelope.signature;
    }
    
    // Selecionar canal de comunicação baseado na confiança
    selectChannel(trustLevel) {
        if (trustLevel > 0.8) {
            return 'direct'; // Canal direto de alta velocidade
        } else if (trustLevel > 0.5) {
            return 'verified'; // Canal com verificação
        } else {
            return 'monitored'; // Canal monitorado com logs completos
        }
    }
    
    // Transmitir mensagem pelo canal
    async transmit(envelope, channel) {
        const channelHandler = this.communicationChannels.get(channel);
        
        if (!channelHandler) {
            throw new Error(`Canal ${channel} não disponível`);
        }
        
        return await channelHandler(envelope);
    }
    
    // Configurar canais de comunicação
    setupCommunicationChannels() {
        // Canal direto - alta velocidade, baixa segurança
        this.communicationChannels.set('direct', async (envelope) => {
            // Simular transmissão rápida
            await this.sleep(10);
            
            return {
                delivered: true,
                quality: 0.95,
                latency: 10
            };
        });
        
        // Canal verificado - velocidade média, segurança média
        this.communicationChannels.set('verified', async (envelope) => {
            // Verificar assinatura
            if (!this.verifySignature(envelope)) {
                throw new Error('Assinatura inválida');
            }
            
            await this.sleep(50);
            
            return {
                delivered: true,
                quality: 0.85,
                latency: 50,
                verified: true
            };
        });
        
        // Canal monitorado - baixa velocidade, alta segurança
        this.communicationChannels.set('monitored', async (envelope) => {
            // Log completo da mensagem
            console.log(`📡 [MONITORED] ${envelope.from} -> ${envelope.to}`);
            
            // Verificar integridade
            if (!this.verifySignature(envelope)) {
                throw new Error('Assinatura inválida');
            }
            
            // Verificar autorização
            if (!this.isAuthorized(envelope.from, envelope.to)) {
                throw new Error('Comunicação não autorizada');
            }
            
            await this.sleep(100);
            
            return {
                delivered: true,
                quality: 0.75,
                latency: 100,
                verified: true,
                logged: true
            };
        });
    }
    
    // Verificar autorização para comunicação
    isAuthorized(fromId, toId) {
        const fromAgent = this.agents.get(fromId);
        const toAgent = this.agents.get(toId);
        
        return fromAgent && toAgent && 
               fromAgent.status === 'active' && 
               toAgent.status === 'active';
    }
    
    // Sistema de Consenso
    async reachConsensus(topic, participants, options = {}) {
        console.log(`\n🤝 Iniciando consenso sobre: ${topic}`);
        console.log(`   Participantes: ${participants.length}`);
        
        const protocol = options.protocol || 'weighted-voting';
        const timeout = options.timeout || 30000;
        
        const consensusHandler = this.consensusProtocols.get(protocol);
        
        if (!consensusHandler) {
            throw new Error(`Protocolo de consenso ${protocol} não disponível`);
        }
        
        try {
            const result = await consensusHandler({
                topic,
                participants,
                trustMatrix: this.trustMatrix,
                reputationScores: this.reputationScores,
                timeout
            });
            
            if (result.consensus) {
                console.log(`✅ Consenso alcançado: ${result.decision}`);
                this.metrics.consensusReached++;
                
                // Aumentar confiança entre participantes que concordaram
                this.reinforceTrust(result.agreementGroups);
            } else {
                console.log(`❌ Consenso não alcançado`);
                this.metrics.consensusFailed++;
            }
            
            return result;
        } catch (error) {
            console.error(`❌ Erro no protocolo de consenso: ${error.message}`);
            this.metrics.consensusFailed++;
            throw error;
        }
    }
    
    // Configurar protocolos de consenso
    setupConsensusProtocols() {
        // Votação ponderada por confiança
        this.consensusProtocols.set('weighted-voting', async (params) => {
            const { topic, participants, trustMatrix, reputationScores } = params;
            const votes = new Map();
            const weights = new Map();
            
            // Coletar votos
            for (const participantId of participants) {
                // Simular voto (em produção, seria uma chamada real ao agente)
                const vote = await this.collectVote(participantId, topic);
                votes.set(participantId, vote);
                
                // Calcular peso do voto baseado em reputação
                const reputation = reputationScores.get(participantId) || 0.5;
                weights.set(participantId, reputation);
            }
            
            // Contar votos ponderados
            const tally = new Map();
            let totalWeight = 0;
            
            for (const [participantId, vote] of votes) {
                const weight = weights.get(participantId);
                totalWeight += weight;
                
                const currentTally = tally.get(vote) || 0;
                tally.set(vote, currentTally + weight);
            }
            
            // Determinar vencedor
            let winner = null;
            let maxWeight = 0;
            
            for (const [option, weight] of tally) {
                if (weight > maxWeight) {
                    maxWeight = weight;
                    winner = option;
                }
            }
            
            // Verificar se atingiu threshold
            const percentage = maxWeight / totalWeight;
            const consensus = percentage >= this.config.consensusThreshold;
            
            // Identificar grupos de acordo
            const agreementGroups = [];
            for (const [p1, v1] of votes) {
                const group = [p1];
                for (const [p2, v2] of votes) {
                    if (p1 !== p2 && v1 === v2) {
                        group.push(p2);
                    }
                }
                if (group.length > 1) {
                    agreementGroups.push(group);
                }
            }
            
            return {
                consensus,
                decision: winner,
                confidence: percentage,
                votes: Array.from(votes.entries()),
                weights: Array.from(weights.entries()),
                agreementGroups
            };
        });
        
        // Consenso bizantino
        this.consensusProtocols.set('byzantine', async (params) => {
            const { topic, participants } = params;
            const rounds = 3;
            let proposals = new Map();
            
            for (let round = 1; round <= rounds; round++) {
                console.log(`   Round ${round}/${rounds}...`);
                
                // Coletar propostas
                for (const participantId of participants) {
                    const proposal = await this.collectProposal(participantId, topic, proposals);
                    proposals.set(participantId, proposal);
                }
                
                // Verificar convergência
                const values = Array.from(proposals.values());
                const uniqueValues = [...new Set(values)];
                
                if (uniqueValues.length === 1) {
                    // Consenso alcançado
                    return {
                        consensus: true,
                        decision: uniqueValues[0],
                        confidence: 1.0,
                        rounds: round
                    };
                }
            }
            
            // Não houve convergência
            return {
                consensus: false,
                decision: null,
                confidence: 0,
                rounds
            };
        });
        
        // Proof of Stake baseado em reputação
        this.consensusProtocols.set('reputation-stake', async (params) => {
            const { topic, participants, reputationScores } = params;
            
            // Selecionar líder baseado em reputação
            let leader = null;
            let maxReputation = 0;
            
            for (const participantId of participants) {
                const reputation = reputationScores.get(participantId) || 0;
                if (reputation > maxReputation) {
                    maxReputation = reputation;
                    leader = participantId;
                }
            }
            
            // Líder propõe decisão
            const proposal = await this.collectProposal(leader, topic);
            
            // Outros validam
            let approvals = 0;
            let totalStake = 0;
            
            for (const participantId of participants) {
                if (participantId === leader) continue;
                
                const reputation = reputationScores.get(participantId) || 0;
                totalStake += reputation;
                
                const approves = await this.validateProposal(participantId, proposal);
                if (approves) {
                    approvals += reputation;
                }
            }
            
            const approvalRate = totalStake > 0 ? approvals / totalStake : 0;
            const consensus = approvalRate >= this.config.consensusThreshold;
            
            return {
                consensus,
                decision: consensus ? proposal : null,
                leader,
                approvalRate,
                confidence: approvalRate
            };
        });
    }
    
    // Coletar voto de um participante
    async collectVote(participantId, topic) {
        // Simular coleta de voto
        await this.sleep(100);
        
        // Em produção, isso seria uma chamada real ao agente
        const options = ['approve', 'reject', 'abstain'];
        return options[Math.floor(Math.random() * options.length)];
    }
    
    // Coletar proposta de um participante
    async collectProposal(participantId, topic, previousProposals = null) {
        // Simular coleta de proposta
        await this.sleep(150);
        
        // Em produção, agente analisaria propostas anteriores
        return `proposal-${Math.floor(Math.random() * 3)}`;
    }
    
    // Validar proposta
    async validateProposal(participantId, proposal) {
        // Simular validação
        await this.sleep(50);
        return Math.random() > 0.3; // 70% de aprovação
    }
    
    // Alocação de Tarefas baseada em Confiança
    async allocateTask(task, candidates) {
        console.log(`\n🎯 Alocando tarefa: ${task.name}`);
        
        const scores = new Map();
        
        for (const candidateId of candidates) {
            const agent = this.agents.get(candidateId);
            if (!agent) continue;
            
            // Calcular score baseado em vários fatores
            const reputation = this.reputationScores.get(candidateId) || 0.5;
            const performance = agent.performance.successRate;
            const availability = agent.status === 'active' ? 1.0 : 0.0;
            const capability = this.assessCapability(agent, task);
            
            // Score ponderado
            const score = 
                reputation * this.config.reputationWeight +
                performance * this.config.performanceWeight +
                availability * 0.2 +
                capability * 0.3;
            
            scores.set(candidateId, {
                score,
                reputation,
                performance,
                availability,
                capability
            });
        }
        
        // Ordenar por score
        const sorted = Array.from(scores.entries())
            .sort((a, b) => b[1].score - a[1].score);
        
        if (sorted.length === 0) {
            console.error('❌ Nenhum candidato disponível');
            return null;
        }
        
        // Selecionar melhor candidato
        const [selectedId, metrics] = sorted[0];
        const selectedAgent = this.agents.get(selectedId);
        
        console.log(`✅ Tarefa alocada para: ${selectedAgent.name}`);
        console.log(`   Score: ${metrics.score.toFixed(3)}`);
        console.log(`   Reputação: ${metrics.reputation.toFixed(2)}`);
        console.log(`   Performance: ${metrics.performance.toFixed(2)}`);
        
        // Registrar alocação
        this.taskAllocationHistory.push({
            task: task.name,
            allocatedTo: selectedId,
            score: metrics.score,
            timestamp: Date.now()
        });
        
        return {
            agent: selectedAgent,
            metrics,
            alternatives: sorted.slice(1, 4) // Top 3 alternativas
        };
    }
    
    // Avaliar capacidade de um agente para uma tarefa
    assessCapability(agent, task) {
        if (!task.requiredCapabilities) return 1.0;
        
        let matchCount = 0;
        for (const required of task.requiredCapabilities) {
            if (agent.capabilities.has(required)) {
                matchCount++;
            }
        }
        
        return matchCount / task.requiredCapabilities.length;
    }
    
    // Calcular reputação de um agente
    calculateReputation(agentId) {
        const agent = this.agents.get(agentId);
        if (!agent) return 0;
        
        // Fatores de reputação
        const performanceScore = agent.performance.successRate;
        const reliabilityScore = 1 - (agent.performance.averageResponseTime / 10000); // Normalizado
        const trustScore = this.getAverageTrust(agentId);
        
        // Reputação ponderada
        const reputation = 
            performanceScore * 0.4 +
            reliabilityScore * 0.3 +
            trustScore * 0.3;
        
        this.reputationScores.set(agentId, reputation);
        
        return reputation;
    }
    
    // Obter confiança entre dois agentes
    getTrust(fromId, toId) {
        if (!this.trustMatrix.has(fromId)) {
            return this.config.initialTrust;
        }
        
        const trustMap = this.trustMatrix.get(fromId);
        return trustMap.get(toId) || this.config.initialTrust;
    }
    
    // Obter confiança média de um agente
    getAverageTrust(agentId) {
        if (!this.trustMatrix.has(agentId)) {
            return this.config.initialTrust;
        }
        
        const trustMap = this.trustMatrix.get(agentId);
        if (trustMap.size === 0) {
            return this.config.initialTrust;
        }
        
        let sum = 0;
        for (const trust of trustMap.values()) {
            sum += trust;
        }
        
        return sum / trustMap.size;
    }
    
    // Atualizar confiança após interação
    updateTrust(fromId, toId, quality) {
        const currentTrust = this.getTrust(fromId, toId);
        let newTrust;
        
        if (quality > 0.7) {
            // Interação bem-sucedida - aumentar confiança
            newTrust = Math.min(1.0, currentTrust + this.config.trustGrowthRate);
        } else if (quality < 0.3) {
            // Interação problemática - reduzir confiança
            newTrust = Math.max(0.0, currentTrust - this.config.trustDecayRate * 2);
        } else {
            // Interação neutra - decay leve
            newTrust = Math.max(0.0, currentTrust - this.config.trustDecayRate * 0.5);
        }
        
        this.setTrust(fromId, toId, newTrust);
        
        // Atualizar reputação
        this.calculateReputation(fromId);
        this.calculateReputation(toId);
    }
    
    // Diminuir confiança após falha
    decreaseTrust(fromId, toId) {
        const currentTrust = this.getTrust(fromId, toId);
        const newTrust = Math.max(0.0, currentTrust - this.config.trustDecayRate * 3);
        this.setTrust(fromId, toId, newTrust);
    }
    
    // Definir confiança entre dois agentes
    setTrust(fromId, toId, value) {
        if (!this.trustMatrix.has(fromId)) {
            this.trustMatrix.set(fromId, new Map());
        }
        
        this.trustMatrix.get(fromId).set(toId, value);
        
        // Emitir evento se confiança cair abaixo do threshold
        if (value < this.config.minimumTrustThreshold) {
            this.emit('low-trust', {
                from: fromId,
                to: toId,
                trustLevel: value
            });
        }
    }
    
    // Reforçar confiança entre grupos que concordaram
    reinforceTrust(agreementGroups) {
        for (const group of agreementGroups) {
            for (let i = 0; i < group.length; i++) {
                for (let j = i + 1; j < group.length; j++) {
                    // Aumentar confiança mútua
                    const trust1 = this.getTrust(group[i], group[j]);
                    const trust2 = this.getTrust(group[j], group[i]);
                    
                    this.setTrust(group[i], group[j], 
                        Math.min(1.0, trust1 + this.config.trustGrowthRate));
                    this.setTrust(group[j], group[i], 
                        Math.min(1.0, trust2 + this.config.trustGrowthRate));
                }
            }
        }
    }
    
    // Monitoramento contínuo de confiança
    startTrustMonitoring() {
        setInterval(() => {
            // Calcular média geral de confiança
            let totalTrust = 0;
            let count = 0;
            
            for (const [, trustMap] of this.trustMatrix) {
                for (const trust of trustMap.values()) {
                    totalTrust += trust;
                    count++;
                }
            }
            
            this.metrics.averageTrustLevel = count > 0 ? totalTrust / count : 0.5;
            
            // Aplicar decay natural
            this.applyTrustDecay();
            
            // Recalcular reputações
            for (const [agentId] of this.agents) {
                this.calculateReputation(agentId);
            }
        }, 60000); // A cada minuto
    }
    
    // Aplicar decay natural na confiança
    applyTrustDecay() {
        for (const [fromId, trustMap] of this.trustMatrix) {
            for (const [toId, trust] of trustMap) {
                // Decay leve em direção ao valor neutro
                const newTrust = trust > 0.5 
                    ? Math.max(0.5, trust - this.config.trustDecayRate * 0.1)
                    : Math.min(0.5, trust + this.config.trustDecayRate * 0.1);
                
                trustMap.set(toId, newTrust);
            }
        }
    }
    
    // Relatório do sistema de confiança
    getTrustReport() {
        const agentReports = [];
        
        for (const [agentId, agent] of this.agents) {
            agentReports.push({
                name: agent.name,
                reputation: (this.reputationScores.get(agentId) || 0).toFixed(3),
                averageTrust: this.getAverageTrust(agentId).toFixed(3),
                performance: agent.performance
            });
        }
        
        return {
            totalAgents: this.agents.size,
            averageTrustLevel: this.metrics.averageTrustLevel.toFixed(3),
            communicationMetrics: {
                total: this.metrics.totalMessages,
                successful: this.metrics.successfulCommunications,
                failed: this.metrics.failedCommunications,
                successRate: `${(this.metrics.successfulCommunications / 
                    Math.max(1, this.metrics.totalMessages) * 100).toFixed(2)}%`
            },
            consensusMetrics: {
                reached: this.metrics.consensusReached,
                failed: this.metrics.consensusFailed,
                successRate: `${(this.metrics.consensusReached / 
                    Math.max(1, this.metrics.consensusReached + this.metrics.consensusFailed) * 100).toFixed(2)}%`
            },
            agents: agentReports,
            recentAllocations: this.taskAllocationHistory.slice(-5)
        };
    }
    
    // Visualizar matriz de confiança
    visualizeTrustMatrix() {
        console.log('\n📊 MATRIZ DE CONFIANÇA:');
        console.log('   (valores de 0.0 a 1.0)\n');
        
        const agentNames = Array.from(this.agents.values()).map(a => a.name.slice(0, 8));
        
        // Cabeçalho
        console.log('        ' + agentNames.map(n => n.padEnd(10)).join(''));
        
        // Linhas
        for (const [fromId, fromAgent] of this.agents) {
            const row = [fromAgent.name.slice(0, 8).padEnd(8)];
            
            for (const [toId] of this.agents) {
                if (fromId === toId) {
                    row.push('   -      ');
                } else {
                    const trust = this.getTrust(fromId, toId);
                    row.push(`  ${trust.toFixed(2)}    `);
                }
            }
            
            console.log(row.join(''));
        }
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

module.exports = TrustCommunicationSystem;