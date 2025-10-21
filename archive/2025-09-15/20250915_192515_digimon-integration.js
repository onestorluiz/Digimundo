#!/usr/bin/env node

/**
 * 🔗 DIGIMON INTEGRATION MODULE
 * Conecta todos os Digimons existentes ao Supreme Orchestrator
 */

const { EventEmitter } = require('events');
const fs = require('fs').promises;
const path = require('path');
const { spawn } = require('child_process');

class DigimonIntegration extends EventEmitter {
    constructor(orchestrator) {
        super();
        this.orchestrator = orchestrator;
        this.connectedDigimons = new Map();
        this.digimonProcesses = new Map();
    }
    
    // Conectar Debugmon existente
    async connectDebugmon() {
        const debugmonPath = '/Users/clubproducoes/Digimundo/core/agents/debugmon/autonomous-debugger.js';
        
        try {
            // Verificar se existe
            await fs.access(debugmonPath);
            
            // Criar wrapper para integração
            const wrapper = {
                name: 'Debugmon',
                path: debugmonPath,
                instance: null,
                
                // Interceptar eventos do Debugmon
                onErrorFound: (error) => {
                    this.orchestrator.emit('message-to-SupremeOrchestrator', {
                        from: 'Debugmon',
                        to: 'all',
                        content: {
                            type: 'ERROR_FOUND',
                            data: error
                        }
                    });
                },
                
                onAutoFixApplied: (fix) => {
                    // Escrever fix na Digilibrary
                    this.orchestrator.digilibrary.writeBook(
                        `Auto-fix: ${fix.type}`,
                        JSON.stringify(fix, null, 2),
                        'Debugmon'
                    );
                }
            };
            
            this.connectedDigimons.set('Debugmon', wrapper);
            console.log('✅ Debugmon conectado ao Orchestrator');
            
            return wrapper;
        } catch (error) {
            console.error('❌ Erro ao conectar Debugmon:', error.message);
            return null;
        }
    }
    
    // Conectar Trainmon existente
    async connectTrainmon() {
        const trainmonPath = '/Users/clubproducoes/Digimundo/core/agents/trainmon/ai-trainer-system.js';
        
        try {
            await fs.access(trainmonPath);
            
            const wrapper = {
                name: 'Trainmon',
                path: trainmonPath,
                instance: null,
                
                // Interceptar eventos de treinamento
                onTrainingComplete: (results) => {
                    // Compartilhar resultados com todos
                    this.orchestrator.broadcast('TRAINING_COMPLETE', results);
                    
                    // Atualizar métodos no orchestrator
                    if (results.method && results.score) {
                        const method = this.orchestrator.trainingMethods[results.method];
                        if (method) {
                            method.uses++;
                            method.score += results.score;
                        }
                    }
                },
                
                onBugGenerated: (bug) => {
                    // Notificar Debugmon sobre novo bug
                    this.orchestrator.emit('message-to-Debugmon', {
                        from: 'Trainmon',
                        to: 'Debugmon',
                        content: {
                            type: 'NEW_BUG_FOR_TRAINING',
                            data: bug
                        }
                    });
                }
            };
            
            this.connectedDigimons.set('Trainmon', wrapper);
            console.log('✅ Trainmon conectado ao Orchestrator');
            
            return wrapper;
        } catch (error) {
            console.error('❌ Erro ao conectar Trainmon:', error.message);
            return null;
        }
    }
    
    // Conectar Guardmon
    async connectGuardmon() {
        const guardmonPath = '/Users/clubproducoes/Digimundo/core/agents/guardmon/guardmon.js';
        
        try {
            await fs.access(guardmonPath);
            
            const wrapper = {
                name: 'Guardmon',
                path: guardmonPath,
                instance: null,
                
                onThreatDetected: (threat) => {
                    // Alertar todos sobre ameaça
                    this.orchestrator.priorityQueue.push({
                        from: 'Guardmon',
                        to: 'all',
                        content: {
                            type: 'SECURITY_THREAT',
                            data: threat
                        },
                        priority: 'HIGH'
                    });
                    
                    // Criar interação social urgente
                    this.orchestrator.iaTown.createSocialInteraction(
                        'Guardmon',
                        'Networkmon',
                        'COLLABORATION',
                        `Defendendo contra ${threat.type}`
                    );
                }
            };
            
            this.connectedDigimons.set('Guardmon', wrapper);
            console.log('✅ Guardmon conectado ao Orchestrator');
            
            return wrapper;
        } catch (error) {
            console.error('❌ Erro ao conectar Guardmon:', error.message);
            return null;
        }
    }
    
    // Conectar Optimon
    async connectOptimon() {
        const optimonPath = '/Users/clubproducoes/Digimundo/core/agents/optimon/optimon.js';
        
        try {
            await fs.access(optimonPath);
            
            const wrapper = {
                name: 'Optimon',
                path: optimonPath,
                instance: null,
                
                onOptimizationFound: (optimization) => {
                    // Compartilhar otimização
                    this.orchestrator.emit('message-to-all', {
                        from: 'Optimon',
                        to: 'all',
                        content: {
                            type: 'OPTIMIZATION_SUGGESTION',
                            data: optimization
                        }
                    });
                    
                    // Escrever na Digilibrary
                    this.orchestrator.digilibrary.writeBook(
                        `Otimização: ${optimization.area}`,
                        `Melhoria de ${optimization.improvement}%\n${optimization.details}`,
                        'Optimon'
                    );
                }
            };
            
            this.connectedDigimons.set('Optimon', wrapper);
            console.log('✅ Optimon conectado ao Orchestrator');
            
            return wrapper;
        } catch (error) {
            console.error('❌ Erro ao conectar Optimon:', error.message);
            return null;
        }
    }
    
    // Conectar Creativemon
    async connectCreativemon() {
        const creativemonPath = '/Users/clubproducoes/Digimundo/core/agents/creativemon/creativemon.js';
        
        try {
            await fs.access(creativemonPath);
            
            const wrapper = {
                name: 'Creativemon',
                path: creativemonPath,
                instance: null,
                
                onIdeaGenerated: (idea) => {
                    // Compartilhar ideia criativa
                    this.orchestrator.emit('message-to-Experimentmon', {
                        from: 'Creativemon',
                        to: 'Experimentmon',
                        content: {
                            type: 'NEW_IDEA_TO_TEST',
                            data: idea
                        }
                    });
                    
                    // Adicionar à memória privada
                    this.orchestrator.personalitySystem.addPrivateMemory(
                        'Creativemon',
                        `Tive uma ideia: ${idea.title}`,
                        'excited'
                    );
                }
            };
            
            this.connectedDigimons.set('Creativemon', wrapper);
            console.log('✅ Creativemon conectado ao Orchestrator');
            
            return wrapper;
        } catch (error) {
            console.error('❌ Erro ao conectar Creativemon:', error.message);
            return null;
        }
    }
    
    // Conectar todos os outros Digimons
    async connectRemainingDigimons() {
        const digimons = [
            'Oraclemon',
            'Networkmon', 
            'Experimentmon',
            'Emulamon',
            'Evolutionmon'
        ];
        
        for (const digimonName of digimons) {
            const digimonPath = `/Users/clubproducoes/Digimundo/core/agents/${digimonName.toLowerCase()}/${digimonName.toLowerCase()}.js`;
            
            try {
                await fs.access(digimonPath);
                
                const wrapper = {
                    name: digimonName,
                    path: digimonPath,
                    instance: null,
                    
                    // Handler genérico
                    onEvent: (eventType, data) => {
                        this.orchestrator.emit(`message-to-SupremeOrchestrator`, {
                            from: digimonName,
                            to: 'orchestrator',
                            content: {
                                type: eventType,
                                data
                            }
                        });
                    }
                };
                
                this.connectedDigimons.set(digimonName, wrapper);
                console.log(`✅ ${digimonName} conectado ao Orchestrator`);
                
            } catch (error) {
                console.warn(`⚠️ ${digimonName} não encontrado, criando stub`);
                
                // Criar stub para Digimons faltantes
                this.createDigimonStub(digimonName);
            }
        }
    }
    
    // Criar stub para Digimon faltante
    createDigimonStub(digimonName) {
        const stub = {
            name: digimonName,
            path: null,
            instance: null,
            isStub: true,
            
            respond: async (message) => {
                // Resposta genérica
                return {
                    from: digimonName,
                    response: `${digimonName} processando: ${message.type}`,
                    timestamp: new Date().toISOString()
                };
            }
        };
        
        this.connectedDigimons.set(digimonName, stub);
    }
    
    // Integrar todos os Digimons
    async integrateAll() {
        console.log('\n🔗 Iniciando integração dos Digimons...\n');
        
        // Conectar principais
        await this.connectDebugmon();
        await this.connectTrainmon();
        await this.connectGuardmon();
        await this.connectOptimon();
        await this.connectCreativemon();
        
        // Conectar restantes
        await this.connectRemainingDigimons();
        
        // Criar canais de comunicação
        this.setupCommunicationChannels();
        
        // Sincronizar com IA Town
        this.syncWithIATown();
        
        console.log(`\n✅ Integração completa: ${this.connectedDigimons.size} Digimons conectados\n`);
        
        return this;
    }
    
    // Configurar canais de comunicação
    setupCommunicationChannels() {
        // Canal de debug
        this.orchestrator.on('debug-channel', (message) => {
            const debugmon = this.connectedDigimons.get('Debugmon');
            if (debugmon && debugmon.onErrorFound) {
                debugmon.onErrorFound(message);
            }
        });
        
        // Canal de treinamento
        this.orchestrator.on('training-channel', (message) => {
            const trainmon = this.connectedDigimons.get('Trainmon');
            if (trainmon && trainmon.onTrainingComplete) {
                trainmon.onTrainingComplete(message);
            }
        });
        
        // Canal de segurança
        this.orchestrator.on('security-channel', (message) => {
            const guardmon = this.connectedDigimons.get('Guardmon');
            if (guardmon && guardmon.onThreatDetected) {
                guardmon.onThreatDetected(message);
            }
        });
        
        console.log('📡 Canais de comunicação configurados');
    }
    
    // Sincronizar com IA Town
    syncWithIATown() {
        // Registrar todos os Digimons conectados na IA Town
        for (const [name, wrapper] of this.connectedDigimons) {
            // Criar interação inicial
            this.orchestrator.iaTown.createSocialInteraction(
                name,
                'Gestormon',
                'CONVERSATION',
                `${name} reportando para duty!`
            );
            
            // Adicionar ao distrito apropriado
            const role = this.orchestrator.digimons.get(name)?.role;
            if (role) {
                this.assignToDistrict(name, role);
            }
        }
        
        console.log('🏘️ Digimons sincronizados com IA Town');
    }
    
    // Atribuir Digimon a distrito
    assignToDistrict(digimonName, role) {
        const districtMap = {
            'debugger': 'DEFENSE',
            'trainer': 'OPTIMIZATION',
            'security': 'DEFENSE',
            'optimizer': 'OPTIMIZATION',
            'innovator': 'CREATIVITY',
            'predictor': 'WISDOM',
            'communicator': 'NETWORK',
            'tester': 'CREATIVITY',
            'simulator': 'NETWORK',
            'evolver': 'EVOLUTION',
            'analyzer': 'RESEARCH',
            'librarian': 'RESEARCH',
            'wise': 'WISDOM',
            'coder': 'RESEARCH',
            'helper': 'EVOLUTION'
        };
        
        const district = districtMap[role];
        if (district && this.orchestrator.iaTown.districts[district]) {
            if (!this.orchestrator.iaTown.districts[district].includes(digimonName)) {
                this.orchestrator.iaTown.districts[district].push(digimonName);
            }
        }
    }
    
    // Iniciar processo de um Digimon
    async startDigimonProcess(digimonName) {
        const wrapper = this.connectedDigimons.get(digimonName);
        if (!wrapper || wrapper.isStub || !wrapper.path) return;
        
        try {
            const process = spawn('node', [wrapper.path], {
                stdio: ['pipe', 'pipe', 'pipe', 'ipc']
            });
            
            process.on('message', (message) => {
                // Rotear mensagem para orchestrator
                this.orchestrator.emit(`message-from-${digimonName}`, message);
            });
            
            process.stdout.on('data', (data) => {
                console.log(`[${digimonName}] ${data.toString().trim()}`);
            });
            
            process.stderr.on('data', (data) => {
                console.error(`[${digimonName} ERROR] ${data.toString().trim()}`);
            });
            
            this.digimonProcesses.set(digimonName, process);
            
            console.log(`🚀 Processo ${digimonName} iniciado (PID: ${process.pid})`);
            
        } catch (error) {
            console.error(`❌ Erro ao iniciar ${digimonName}:`, error.message);
        }
    }
    
    // Parar processo de um Digimon
    async stopDigimonProcess(digimonName) {
        const process = this.digimonProcesses.get(digimonName);
        if (process) {
            process.kill('SIGTERM');
            this.digimonProcesses.delete(digimonName);
            console.log(`🛑 Processo ${digimonName} parado`);
        }
    }
    
    // Status da integração
    getIntegrationStatus() {
        const status = {
            connected: this.connectedDigimons.size,
            running: this.digimonProcesses.size,
            stubs: 0,
            real: 0
        };
        
        for (const wrapper of this.connectedDigimons.values()) {
            if (wrapper.isStub) {
                status.stubs++;
            } else {
                status.real++;
            }
        }
        
        return status;
    }
}

// Exportar
module.exports = DigimonIntegration;

// Se executado diretamente, fazer integração de teste
if (require.main === module) {
    console.log('🔗 Teste de Integração de Digimons\n');
    
    // Criar orchestrator mock para teste
    const mockOrchestrator = {
        emit: (event, data) => console.log(`[EMIT] ${event}:`, data),
        on: (event, handler) => console.log(`[LISTEN] ${event}`),
        broadcast: (type, data) => console.log(`[BROADCAST] ${type}:`, data),
        iaTown: {
            createSocialInteraction: () => {},
            districts: {
                RESEARCH: [],
                DEFENSE: [],
                OPTIMIZATION: [],
                CREATIVITY: [],
                WISDOM: [],
                NETWORK: [],
                EVOLUTION: []
            }
        },
        digilibrary: {
            writeBook: async () => 'book-test-123'
        },
        personalitySystem: {
            addPrivateMemory: () => {}
        },
        digimons: new Map(),
        priorityQueue: [],
        trainingMethods: {
            RLAIF: { score: 0, uses: 0 },
            ADVERSARIAL: { score: 0, uses: 0 },
            SELF_SUPERVISED: { score: 0, uses: 0 },
            CHAOS: { score: 0, uses: 0 },
            TORQUE: { score: 0, uses: 0 }
        }
    };
    
    const integration = new DigimonIntegration(mockOrchestrator);
    
    integration.integrateAll().then(() => {
        console.log('\nStatus da Integração:');
        console.log(JSON.stringify(integration.getIntegrationStatus(), null, 2));
    });
}