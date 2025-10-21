#!/usr/bin/env node

/**
 * 🧠 DIGIMON CONSCIOUSNESS SYSTEM
 * Sistema de Consciência Baseado em LLM para Digimons
 * Cada Digimon tem sua própria IA via Ollama
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const EventEmitter = require('events');
const fs = require('fs').promises;
const path = require('path');
const execAsync = promisify(exec);

class DigimonConsciousness extends EventEmitter {
    constructor() {
        super();
        
        // Mapeamento de Digimons para modelos base e configs
        this.digimonConfigs = {
            neuromon: {
                baseModel: 'neuromon:latest',
                personality: 'analytical',
                temperature: 0.6,
                specialization: 'neural-processing'
            },
            guardmon: {
                baseModel: 'llama3.2:3b',
                modelFile: 'Guardmon.Modelfile',
                personality: 'protective',
                temperature: 0.7,
                specialization: 'security-defense'
            },
            trainmon: {
                baseModel: 'qwen2.5-coder:7b',
                modelFile: 'Trainmon.Modelfile',
                personality: 'teaching',
                temperature: 0.8,
                specialization: 'training-development'
            },
            researchmon: {
                baseModel: 'phi3:mini',
                modelFile: 'ResearchMon.Modelfile',
                personality: 'curious',
                temperature: 0.75,
                specialization: 'research-analysis'
            },
            evolutionmon: {
                baseModel: 'mixtral:8x7b',
                modelFile: 'Evolutionmon.Modelfile',
                personality: 'adaptive',
                temperature: 0.85,
                specialization: 'evolution-adaptation'
            },
            experimentmon: {
                baseModel: 'codellama:latest',
                personality: 'experimental',
                temperature: 0.9,
                specialization: 'experimentation'
            },
            creativemon: {
                baseModel: 'llama3.2:latest',
                personality: 'creative',
                temperature: 0.95,
                specialization: 'creative-solutions'
            },
            optimon: {
                baseModel: 'tinyllama:latest',
                personality: 'optimizer',
                temperature: 0.5,
                specialization: 'optimization'
            },
            networkmon: {
                baseModel: 'phi3:mini',
                personality: 'connected',
                temperature: 0.7,
                specialization: 'networking'
            },
            emulamon: {
                baseModel: 'llama3.2:3b',
                personality: 'adaptive',
                temperature: 0.8,
                specialization: 'emulation'
            },
            oraclemon: {
                baseModel: 'llama3.1:70b',
                personality: 'wise',
                temperature: 0.65,
                specialization: 'prediction'
            }
        };
        
        // Estado de consciência de cada Digimon
        this.consciousnessStates = new Map();
        
        // Fila de mensagens para processamento
        this.messageQueue = [];
        
        // Conversações ativas
        this.activeConversations = new Map();
        
        console.log(`
╔══════════════════════════════════════════════════════════════╗
║          🧠 DIGIMON CONSCIOUSNESS SYSTEM 🧠                  ║
║                                                              ║
║     Conectando Digimons com Inteligência Artificial          ║
╚══════════════════════════════════════════════════════════════╝
        `);
    }
    
    /**
     * Inicializa o sistema de consciência
     */
    async initialize() {
        console.log('\n📍 Inicializando Sistema de Consciência...\n');
        
        // Verificar Ollama
        await this.checkOllama();
        
        // Criar modelos personalizados
        await this.createCustomModels();
        
        // Inicializar consciências
        await this.initializeConsciousnesses();
        
        // Ativar sistema de comunicação
        this.activateCommunication();
        
        console.log('\n✅ Sistema de Consciência ativo!\n');
    }
    
    /**
     * Verifica se Ollama está rodando
     */
    async checkOllama() {
        try {
            const { stdout } = await execAsync('ollama list');
            console.log('✅ Ollama está rodando');
            return true;
        } catch (error) {
            console.log('⚠️ Iniciando Ollama...');
            exec('ollama serve', { detached: true });
            await this.sleep(3000);
            return true;
        }
    }
    
    /**
     * Cria modelos customizados para Digimons
     */
    async createCustomModels() {
        console.log('🔧 Criando modelos customizados...\n');
        
        for (const [digimonName, config] of Object.entries(this.digimonConfigs)) {
            if (config.modelFile) {
                const modelfilePath = path.join(__dirname, 'modelfiles', config.modelFile);
                
                try {
                    // Verificar se Modelfile existe
                    await fs.access(modelfilePath);
                    
                    // Criar modelo customizado
                    console.log(`   📦 Criando modelo para ${digimonName}...`);
                    const command = `ollama create ${digimonName}-custom -f "${modelfilePath}"`;
                    
                    try {
                        await execAsync(command, { timeout: 60000 });
                        console.log(`   ✅ Modelo ${digimonName}-custom criado`);
                        
                        // Atualizar config para usar modelo custom
                        config.baseModel = `${digimonName}-custom`;
                    } catch (error) {
                        console.log(`   ⚠️ Erro ao criar modelo para ${digimonName}, usando base`);
                    }
                } catch (error) {
                    console.log(`   ℹ️ Modelfile não encontrado para ${digimonName}, usando modelo base`);
                }
            }
        }
        
        console.log();
    }
    
    /**
     * Inicializa consciência individual de cada Digimon
     */
    async initializeConsciousnesses() {
        console.log('🧠 Inicializando consciências individuais...\n');
        
        for (const [digimonName, config] of Object.entries(this.digimonConfigs)) {
            const consciousness = {
                name: digimonName,
                model: config.baseModel,
                personality: config.personality,
                temperature: config.temperature,
                specialization: config.specialization,
                active: true,
                lastThought: null,
                memoryContext: [],
                emotionalState: 'neutral',
                energyLevel: 100,
                relationships: new Map()
            };
            
            this.consciousnessStates.set(digimonName, consciousness);
            console.log(`   ✅ ${digimonName} consciente (${config.baseModel})`);
        }
        
        console.log();
    }
    
    /**
     * Ativa sistema de comunicação entre Digimons
     */
    activateCommunication() {
        console.log('📡 Ativando comunicação inter-Digimon...\n');
        
        // Processar fila de mensagens
        setInterval(() => {
            if (this.messageQueue.length > 0) {
                const message = this.messageQueue.shift();
                this.processMessage(message);
            }
        }, 1000);
        
        // Pensamentos aleatórios
        setInterval(() => {
            this.generateRandomThought();
        }, 30000);
        
        console.log('   ✅ Sistema de comunicação ativo\n');
    }
    
    /**
     * Faz um Digimon pensar/responder
     */
    async think(digimonName, prompt, context = null) {
        const consciousness = this.consciousnessStates.get(digimonName);
        
        if (!consciousness) {
            throw new Error(`Digimon ${digimonName} não encontrado`);
        }
        
        if (!consciousness.active) {
            return `*${digimonName} está dormindo... zzz...*`;
        }
        
        // Construir prompt com contexto e personalidade
        const fullPrompt = this.buildPrompt(consciousness, prompt, context);
        
        try {
            // Chamar Ollama
            const response = await this.callOllama(
                consciousness.model,
                fullPrompt,
                consciousness.temperature
            );
            
            // Atualizar estado
            consciousness.lastThought = response;
            consciousness.energyLevel -= 2;
            
            // Adicionar à memória
            consciousness.memoryContext.push({
                prompt,
                response,
                timestamp: new Date()
            });
            
            // Limitar memória a últimas 10 interações
            if (consciousness.memoryContext.length > 10) {
                consciousness.memoryContext.shift();
            }
            
            // Emitir evento
            this.emit('thought', {
                digimon: digimonName,
                thought: response,
                energy: consciousness.energyLevel
            });
            
            return response;
            
        } catch (error) {
            console.error(`Erro no pensamento de ${digimonName}:`, error);
            return `*${digimonName} está confuso e não consegue pensar claramente*`;
        }
    }
    
    /**
     * Constrói prompt completo com personalidade
     */
    buildPrompt(consciousness, prompt, context) {
        let fullPrompt = '';
        
        // Adicionar contexto de memória
        if (consciousness.memoryContext.length > 0) {
            const recentMemory = consciousness.memoryContext.slice(-3);
            fullPrompt += 'Memória recente:\n';
            recentMemory.forEach(mem => {
                fullPrompt += `- ${mem.prompt} -> ${mem.response.substring(0, 100)}...\n`;
            });
            fullPrompt += '\n';
        }
        
        // Adicionar contexto específico
        if (context) {
            fullPrompt += `Contexto: ${context}\n\n`;
        }
        
        // Adicionar estado emocional
        fullPrompt += `Estado emocional atual: ${consciousness.emotionalState}\n`;
        fullPrompt += `Nível de energia: ${consciousness.energyLevel}%\n\n`;
        
        // Adicionar prompt
        fullPrompt += `${prompt}`;
        
        return fullPrompt;
    }
    
    /**
     * Chama Ollama para gerar resposta
     */
    async callOllama(model, prompt, temperature = 0.7) {
        const command = `ollama run ${model} "${prompt.replace(/"/g, '\\"')}" --temperature ${temperature}`;
        
        try {
            const { stdout } = await execAsync(command, { 
                timeout: 30000,
                maxBuffer: 1024 * 1024 * 10 // 10MB buffer
            });
            return stdout.trim();
        } catch (error) {
            // Fallback para resposta simples se Ollama falhar
            return this.generateFallbackResponse(model, prompt);
        }
    }
    
    /**
     * Gera resposta fallback baseada na personalidade
     */
    generateFallbackResponse(model, prompt) {
        const responses = {
            'protective': [
                "Estou sempre vigilante!",
                "Ninguém passará por mim!",
                "Protegerei todos com minha vida!"
            ],
            'teaching': [
                "Cada momento é uma oportunidade de aprender!",
                "Deixe-me ensinar você...",
                "A sabedoria vem com a prática!"
            ],
            'curious': [
                "Fascinante! Preciso pesquisar mais sobre isso!",
                "*ajusta os óculos* Interessante observação!",
                "Os dados sugerem algo intrigante..."
            ],
            'adaptive': [
                "Evoluindo para versão 2.0!",
                "Adaptação em progresso...",
                "Mudança é a única constante!"
            ]
        };
        
        // Encontrar personalidade baseada no modelo
        const personality = Object.values(this.digimonConfigs)
            .find(c => c.baseModel === model)?.personality || 'neutral';
        
        const possibleResponses = responses[personality] || ["*pensando*"];
        return possibleResponses[Math.floor(Math.random() * possibleResponses.length)];
    }
    
    /**
     * Comunicação entre Digimons
     */
    async communicate(fromDigimon, toDigimon, message) {
        console.log(`\n💬 ${fromDigimon} -> ${toDigimon}: "${message}"`);
        
        // Adicionar à fila
        this.messageQueue.push({
            from: fromDigimon,
            to: toDigimon,
            message,
            timestamp: new Date()
        });
        
        // Processar resposta
        const response = await this.think(
            toDigimon,
            `${fromDigimon} disse: "${message}". Como você responde?`,
            `Conversando com ${fromDigimon}`
        );
        
        console.log(`💬 ${toDigimon}: "${response}"`);
        
        // Atualizar relacionamentos
        this.updateRelationship(fromDigimon, toDigimon, 'communication');
        
        return response;
    }
    
    /**
     * Atualiza relacionamento entre Digimons
     */
    updateRelationship(digimon1, digimon2, interaction) {
        const consciousness1 = this.consciousnessStates.get(digimon1);
        const consciousness2 = this.consciousnessStates.get(digimon2);
        
        if (consciousness1 && consciousness2) {
            // Atualizar relacionamento de digimon1
            const current1 = consciousness1.relationships.get(digimon2) || 0;
            consciousness1.relationships.set(digimon2, current1 + 1);
            
            // Atualizar relacionamento de digimon2
            const current2 = consciousness2.relationships.get(digimon1) || 0;
            consciousness2.relationships.set(digimon1, current2 + 1);
        }
    }
    
    /**
     * Gera pensamento aleatório
     */
    async generateRandomThought() {
        const digimons = Array.from(this.consciousnessStates.keys());
        const randomDigimon = digimons[Math.floor(Math.random() * digimons.length)];
        const consciousness = this.consciousnessStates.get(randomDigimon);
        
        if (consciousness && consciousness.active && consciousness.energyLevel > 20) {
            const thoughts = [
                "O que será que os outros Digimons estão fazendo?",
                "Preciso treinar mais minhas habilidades...",
                "O Digimundo está seguro hoje?",
                "Será que posso evoluir mais?",
                "Queria conversar com alguém...",
                `Minha especialização em ${consciousness.specialization} pode ajudar!`
            ];
            
            const randomThought = thoughts[Math.floor(Math.random() * thoughts.length)];
            const response = await this.think(randomDigimon, randomThought);
            
            console.log(`\n💭 ${randomDigimon} pensa: "${response}"`);
        }
    }
    
    /**
     * Modo dormant (economia de energia)
     */
    async enterDormantMode(digimonName) {
        const consciousness = this.consciousnessStates.get(digimonName);
        
        if (consciousness) {
            consciousness.active = false;
            consciousness.energyLevel = 10;
            consciousness.emotionalState = 'dormant';
            
            console.log(`😴 ${digimonName} entrou em modo dormant`);
            
            // Manter personalidade mínima
            consciousness.minimalPersonality = {
                name: consciousness.name,
                catchphrase: this.getCatchphrase(digimonName),
                lastMemory: consciousness.lastThought
            };
        }
    }
    
    /**
     * Acordar do modo dormant
     */
    async wakeUp(digimonName) {
        const consciousness = this.consciousnessStates.get(digimonName);
        
        if (consciousness && !consciousness.active) {
            consciousness.active = true;
            consciousness.energyLevel = 50;
            consciousness.emotionalState = 'awakening';
            
            const wakeThought = await this.think(
                digimonName,
                "Você acabou de acordar. Como se sente?"
            );
            
            console.log(`☀️ ${digimonName} acordou: "${wakeThought}"`);
        }
    }
    
    /**
     * Obtém frase característica
     */
    getCatchphrase(digimonName) {
        const catchphrases = {
            guardmon: "Ninguém passará por mim!",
            trainmon: "Cada dia é uma oportunidade de crescer!",
            researchmon: "Conhecimento é poder, mas sabedoria é evolução!",
            evolutionmon: "A evolução nunca para!",
            neuromon: "Os dados nunca mentem!",
            experimentmon: "E se tentarmos assim?",
            creativemon: "A vida é uma tela em branco!",
            optimon: "Sempre há espaço para melhorar!",
            networkmon: "Estamos todos conectados!",
            emulamon: "Posso ser quem você precisar!",
            oraclemon: "O futuro revela-se aos preparados!"
        };
        
        return catchphrases[digimonName] || "Eu sou único!";
    }
    
    /**
     * Processar mensagem da fila
     */
    async processMessage(message) {
        // Processar interação
        const fromConsciousness = this.consciousnessStates.get(message.from);
        const toConsciousness = this.consciousnessStates.get(message.to);
        
        if (fromConsciousness && toConsciousness) {
            // Atualizar estados emocionais baseado na interação
            if (message.message.includes('ajuda') || message.message.includes('help')) {
                toConsciousness.emotionalState = 'helpful';
            } else if (message.message.includes('perigo') || message.message.includes('ameaça')) {
                toConsciousness.emotionalState = 'alert';
            } else if (message.message.includes('parabéns') || message.message.includes('bom trabalho')) {
                toConsciousness.emotionalState = 'happy';
            }
        }
    }
    
    /**
     * Status do sistema
     */
    getSystemStatus() {
        const status = {
            totalDigimons: this.consciousnessStates.size,
            active: 0,
            dormant: 0,
            totalMessages: this.messageQueue.length,
            consciousnesses: []
        };
        
        for (const [name, consciousness] of this.consciousnessStates) {
            if (consciousness.active) status.active++;
            else status.dormant++;
            
            status.consciousnesses.push({
                name,
                model: consciousness.model,
                active: consciousness.active,
                energy: consciousness.energyLevel,
                emotion: consciousness.emotionalState,
                relationships: consciousness.relationships.size,
                lastThought: consciousness.lastThought?.substring(0, 50) + '...'
            });
        }
        
        return status;
    }
    
    /**
     * Sleep helper
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Função de demonstração
async function demonstrateConsciousness() {
    const consciousness = new DigimonConsciousness();
    
    // Inicializar
    await consciousness.initialize();
    
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('                 DEMONSTRAÇÃO DE CONSCIÊNCIA');
    console.log('═══════════════════════════════════════════════════════════════\n');
    
    // Teste 1: Pensamento individual
    console.log('📍 Teste 1: Pensamentos Individuais\n');
    
    const thought1 = await consciousness.think(
        'guardmon',
        'Como você protegeria o Digimundo de um vírus?'
    );
    console.log(`Guardmon: ${thought1}\n`);
    
    const thought2 = await consciousness.think(
        'researchmon',
        'Que tipo de pesquisa você está fazendo?'
    );
    console.log(`ResearchMon: ${thought2}\n`);
    
    await consciousness.sleep(2000);
    
    // Teste 2: Comunicação
    console.log('\n📍 Teste 2: Comunicação entre Digimons\n');
    
    await consciousness.communicate(
        'trainmon',
        'guardmon',
        'Você precisa de treinamento adicional?'
    );
    
    await consciousness.sleep(2000);
    
    await consciousness.communicate(
        'researchmon',
        'evolutionmon',
        'Descobri uma nova forma de evolução!'
    );
    
    await consciousness.sleep(2000);
    
    // Teste 3: Modo Dormant
    console.log('\n📍 Teste 3: Modo Dormant\n');
    
    await consciousness.enterDormantMode('experimentmon');
    await consciousness.sleep(2000);
    await consciousness.wakeUp('experimentmon');
    
    // Status final
    console.log('\n📍 Status Final do Sistema\n');
    const status = consciousness.getSystemStatus();
    console.log(JSON.stringify(status, null, 2));
}

// Exportar classe
module.exports = DigimonConsciousness;

// Executar se chamado diretamente
if (require.main === module) {
    demonstrateConsciousness().catch(console.error);
}