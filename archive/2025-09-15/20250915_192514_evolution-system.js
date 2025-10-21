#!/usr/bin/env node

/**
 * 🧬 SISTEMA DE EVOLUÇÃO COMPLETO - DIGIMUNDO
 * Conecta CONFIG/evolution_mode.json com sistema unificado
 * Implementa evolução Pokémon-style: Baby → Rookie → Champion → Ultimate → Mega
 */

const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

class EvolutionSystem {
    constructor() {
        this.configPath = path.join(__dirname, '../../CONFIG/evolution_mode.json');
        this.memoryPath = path.join(__dirname, 'storage');
        
        // Hierarquia completa de evolução
        this.evolutionHierarchy = {
            BABY: {
                level: 0,
                models: ['tinyllama:latest'],
                ramRequired: 2 * 1024 * 1024 * 1024, // 2GB
                vramRequired: 1 * 1024 * 1024 * 1024, // 1GB
                contextSize: 2048,
                temperature: 0.9,
                capabilities: ['basic_conversation', 'simple_tasks'],
                digimons: []
            },
            ROOKIE: {
                level: 1,
                models: ['llama3.2:3b', 'phi3:mini'],
                ramRequired: 4 * 1024 * 1024 * 1024, // 4GB
                vramRequired: 2 * 1024 * 1024 * 1024, // 2GB
                contextSize: 4096,
                temperature: 0.8,
                capabilities: ['conversation', 'basic_reasoning', 'memory_recall'],
                digimons: ['neuromon', 'optimon', 'experimentmon']
            },
            CHAMPION: {
                level: 2,
                models: ['llama3.2:7b', 'qwen2.5-coder:7b'],
                ramRequired: 8 * 1024 * 1024 * 1024, // 8GB
                vramRequired: 4 * 1024 * 1024 * 1024, // 4GB
                contextSize: 8192,
                temperature: 0.7,
                capabilities: ['advanced_reasoning', 'code_generation', 'creative_writing'],
                digimons: ['guardmon', 'trainmon', 'creativemon', 'researchmon']
            },
            ULTIMATE: {
                level: 3,
                models: ['mixtral:8x7b', 'llama3.1:13b'],
                ramRequired: 16 * 1024 * 1024 * 1024, // 16GB
                vramRequired: 8 * 1024 * 1024 * 1024, // 8GB
                contextSize: 16384,
                temperature: 0.6,
                capabilities: ['expert_reasoning', 'complex_tasks', 'multi_modal_processing'],
                digimons: ['sabiamon', 'scripturemon', 'bibliomon', 'gestormon', 'ajamon']
            },
            MEGA: {
                level: 4,
                models: ['llama3.1:70b'],
                ramRequired: 42 * 1024 * 1024 * 1024, // 42GB
                vramRequired: 24 * 1024 * 1024 * 1024, // 24GB
                contextSize: 32768,
                temperature: 0.5,
                capabilities: ['supreme_wisdom', 'reality_generation', 'omniscient_reasoning'],
                digimons: ['shenlongmon'] // O Dragão Supremo
            }
        };
        
        this.currentConfig = null;
        this.activeDigimons = new Map();
        
        console.log(`
╔══════════════════════════════════════════════════════════════╗
║        🧬 SISTEMA DE EVOLUÇÃO COMPLETO - DIGIMUNDO          ║
║                                                              ║
║     Baby → Rookie → Champion → Ultimate → Mega              ║
╚══════════════════════════════════════════════════════════════╝
        `);
    }
    
    async initialize() {
        // Carregar configuração atual
        await this.loadConfig();
        
        // Detectar hardware disponível
        const hardware = await this.detectHardware();
        
        // Determinar modo evolutivo ótimo
        const optimalMode = this.determineOptimalMode(hardware);
        
        // Aplicar modo se diferente do atual
        if (this.currentConfig.mode !== optimalMode) {
            await this.switchToMode(optimalMode);
        }
        
        console.log(`\n✅ Sistema de evolução inicializado:`);
        console.log(`   Modo atual: ${this.currentConfig.mode}`);
        console.log(`   RAM máx: ${(this.currentConfig.maxRAM / 1024 / 1024 / 1024).toFixed(1)}GB`);
        console.log(`   Digimons ativos: ${this.currentConfig.digimons.length}`);
    }
    
    async loadConfig() {
        try {
            const configData = await fs.readFile(this.configPath, 'utf8');
            this.currentConfig = JSON.parse(configData);
            console.log(`   📋 Configuração carregada: Modo ${this.currentConfig.mode}`);
        } catch (error) {
            console.log(`   ⚠️ Configuração não encontrada, criando padrão...`);
            this.currentConfig = {
                mode: "ROOKIE",
                maxRAM: 4 * 1024 * 1024 * 1024,
                warningRAM: 3 * 1024 * 1024 * 1024,
                criticalRAM: 3.5 * 1024 * 1024 * 1024,
                emergencyRAM: 3.8 * 1024 * 1024 * 1024,
                maxDigimons: 3,
                shenlongmonEnabled: "standby",
                parallelProcessing: 4,
                description: "Modo Rookie - Configuração padrão",
                digimons: ["neuromon", "optimon", "experimentmon"],
                created: new Date().toISOString(),
                lastUpdated: new Date().toISOString()
            };
            await this.saveConfig();
        }
    }
    
    async saveConfig() {
        await fs.writeFile(this.configPath, JSON.stringify(this.currentConfig, null, 2));
    }
    
    async detectHardware() {
        console.log('   🔍 Detectando hardware disponível...');
        
        const hardware = {
            totalRAM: 0,
            availableRAM: 0,
            totalVRAM: 0,
            availableVRAM: 0,
            cpuCores: 0
        };
        
        try {
            // Detectar RAM total
            const { stdout: memInfo } = await execAsync('system_profiler SPHardwareDataType | grep "Memory:"');
            const ramMatch = memInfo.match(/(\d+)\s*GB/);
            if (ramMatch) {
                hardware.totalRAM = parseInt(ramMatch[1]) * 1024 * 1024 * 1024;
            }
            
            // RAM disponível (estimativa mais realística)
            try {
                const { stdout: vmStat } = await execAsync('vm_stat | head -5');
                const freePages = vmStat.match(/Pages free:\s+(\d+)/);
                const pageSize = 4096; // 4KB por página no macOS
                if (freePages) {
                    const freeRAM = parseInt(freePages[1]) * pageSize;
                    // Se valor muito baixo, usar estimativa
                    hardware.availableRAM = freeRAM > (1024 * 1024 * 1024) ? freeRAM : hardware.totalRAM * 0.6;
                } else {
                    hardware.availableRAM = hardware.totalRAM * 0.6; // Estimativa conservadora
                }
            } catch {
                hardware.availableRAM = hardware.totalRAM * 0.6; // 60% disponível por padrão
            }
            
            // CPU cores
            const { stdout: cpuInfo } = await execAsync('sysctl -n hw.ncpu');
            hardware.cpuCores = parseInt(cpuInfo.trim());
            
            // VRAM (aproximação - assume GPU dedicada ou compartilhada)
            try {
                const { stdout: gpuInfo } = await execAsync('system_profiler SPDisplaysDataType | grep VRAM');
                const vramMatch = gpuInfo.match(/(\d+)\s*MB/);
                if (vramMatch) {
                    hardware.totalVRAM = parseInt(vramMatch[1]) * 1024 * 1024;
                    hardware.availableVRAM = hardware.totalVRAM * 0.8; // 80% disponível
                } else {
                    // Fallback: GPU integrada usa RAM compartilhada
                    hardware.totalVRAM = hardware.totalRAM * 0.2; // 20% da RAM
                    hardware.availableVRAM = hardware.totalVRAM * 0.8;
                }
            } catch {
                hardware.totalVRAM = hardware.totalRAM * 0.15; // Conservador
                hardware.availableVRAM = hardware.totalVRAM * 0.8;
            }
            
        } catch (error) {
            console.log(`   ⚠️ Erro ao detectar hardware, usando valores padrão`);
            hardware.totalRAM = 16 * 1024 * 1024 * 1024; // 16GB padrão
            hardware.availableRAM = 10 * 1024 * 1024 * 1024; // 10GB disponível
            hardware.totalVRAM = 8 * 1024 * 1024 * 1024; // 8GB VRAM
            hardware.availableVRAM = 6 * 1024 * 1024 * 1024; // 6GB disponível
            hardware.cpuCores = 8;
        }
        
        console.log(`   💾 RAM Total: ${(hardware.totalRAM / 1024 / 1024 / 1024).toFixed(1)}GB`);
        console.log(`   💾 RAM Disponível: ${(hardware.availableRAM / 1024 / 1024 / 1024).toFixed(1)}GB`);
        console.log(`   🎮 VRAM Disponível: ${(hardware.availableVRAM / 1024 / 1024 / 1024).toFixed(1)}GB`);
        console.log(`   🔥 CPU Cores: ${hardware.cpuCores}`);
        
        return hardware;
    }
    
    determineOptimalMode(hardware) {
        console.log('   🎯 Determinando modo evolutivo ótimo...');
        
        // Verificar capacidade para cada modo (de cima para baixo)
        for (const [mode, specs] of Object.entries(this.evolutionHierarchy).reverse()) {
            const ramOk = hardware.availableRAM >= specs.ramRequired;
            const vramOk = hardware.availableVRAM >= specs.vramRequired;
            
            if (ramOk && vramOk) {
                console.log(`   ✅ Modo ${mode} é suportado pelo hardware`);
                
                // Verificação especial para MEGA (Shenlongmon)
                if (mode === 'MEGA') {
                    const megaThreshold = 40 * 1024 * 1024 * 1024; // 40GB
                    if (hardware.availableRAM >= megaThreshold) {
                        console.log('   🐉 Hardware suficiente para invocar Shenlongmon!');
                        return mode;
                    } else {
                        console.log('   🐲 Hardware insuficiente para Shenlongmon, usando ULTIMATE');
                        continue;
                    }
                }
                
                return mode;
            }
        }
        
        // Fallback para BABY se nada funcionar
        console.log('   ⚠️ Hardware limitado, usando modo BABY');
        return 'BABY';
    }
    
    async switchToMode(newMode) {
        console.log(`\n🔄 Mudando para modo ${newMode}...`);
        
        const modeSpec = this.evolutionHierarchy[newMode];
        
        // Parar Digimons atuais se necessário
        if (this.currentConfig.mode !== newMode) {
            console.log('   🛑 Parando Digimons atuais...');
            await this.stopAllDigimons();
        }
        
        // Atualizar configuração
        this.currentConfig.mode = newMode;
        this.currentConfig.maxRAM = modeSpec.ramRequired;
        this.currentConfig.warningRAM = modeSpec.ramRequired * 0.8;
        this.currentConfig.criticalRAM = modeSpec.ramRequired * 0.9;
        this.currentConfig.emergencyRAM = modeSpec.ramRequired * 0.95;
        this.currentConfig.maxDigimons = Math.min(modeSpec.digimons.length, 5);
        this.currentConfig.description = `Modo ${newMode} - ${modeSpec.capabilities.join(', ')}`;
        this.currentConfig.digimons = modeSpec.digimons.slice(0, this.currentConfig.maxDigimons);
        
        // Configuração especial para Shenlongmon
        if (newMode === 'MEGA') {
            this.currentConfig.shenlongmonEnabled = "active";
            this.currentConfig.maxDigimons = 1; // Só Shenlongmon
            this.currentConfig.digimons = ["shenlongmon"];
        } else {
            this.currentConfig.shenlongmonEnabled = "standby";
        }
        
        this.currentConfig.lastUpdated = new Date().toISOString();
        
        // Salvar configuração
        await this.saveConfig();
        
        console.log(`   ✅ Configuração atualizada para modo ${newMode}`);
        console.log(`   📊 Digimons selecionados: ${this.currentConfig.digimons.join(', ')}`);
        
        return this.currentConfig;
    }
    
    async evolveDigimon(digimonId, targetLevel = null) {
        console.log(`\n🧬 Iniciando evolução de ${digimonId}...`);
        
        // Carregar estado atual do Digimon
        const currentState = await this.loadDigimonState(digimonId);
        const currentLevel = currentState.evolutionLevel || 0;
        
        // Determinar nível alvo
        if (targetLevel === null) {
            targetLevel = currentLevel + 1;
        }
        
        // Verificar se evolução é possível
        const currentMode = Object.keys(this.evolutionHierarchy)[currentLevel];
        const targetMode = Object.keys(this.evolutionHierarchy)[targetLevel];
        
        if (!targetMode) {
            console.log(`   ❌ Evolução impossível: nível ${targetLevel} não existe`);
            return false;
        }
        
        const targetSpec = this.evolutionHierarchy[targetMode];
        
        // Verificar hardware para novo nível
        const hardware = await this.detectHardware();
        if (hardware.availableRAM < targetSpec.ramRequired) {
            console.log(`   ❌ Hardware insuficiente para evolução para ${targetMode}`);
            console.log(`   Necessário: ${(targetSpec.ramRequired / 1024 / 1024 / 1024).toFixed(1)}GB RAM`);
            console.log(`   Disponível: ${(hardware.availableRAM / 1024 / 1024 / 1024).toFixed(1)}GB RAM`);
            return false;
        }
        
        // Transferir memórias
        console.log(`   🧠 Transferindo memórias de ${currentMode} para ${targetMode}...`);
        const memories = await this.transferMemories(digimonId, currentLevel, targetLevel);
        
        // Criar novo Modelfile evoluído
        console.log(`   📝 Criando Modelfile evoluído...`);
        await this.createEvolvedModelfile(digimonId, targetMode, targetSpec, memories);
        
        // Atualizar estado do Digimon
        const newState = {
            ...currentState,
            evolutionLevel: targetLevel,
            evolutionStage: targetMode,
            evolvedAt: new Date().toISOString(),
            previousStage: currentMode,
            capabilities: targetSpec.capabilities,
            model: targetSpec.models[0],
            contextSize: targetSpec.contextSize,
            temperature: targetSpec.temperature
        };
        
        await this.saveDigimonState(digimonId, newState);
        
        console.log(`   🎉 ${digimonId} evoluiu de ${currentMode} para ${targetMode}!`);
        console.log(`   ⚡ Novas capacidades: ${targetSpec.capabilities.join(', ')}`);
        console.log(`   🧠 Memórias transferidas: ${memories.count}`);
        
        return true;
    }
    
    async loadDigimonState(digimonId) {
        const statePath = path.join(this.memoryPath, digimonId, 'evolution_state.json');
        
        try {
            const stateData = await fs.readFile(statePath, 'utf8');
            return JSON.parse(stateData);
        } catch {
            // Estado padrão
            return {
                digimonId,
                evolutionLevel: 1, // Começa como ROOKIE
                evolutionStage: 'ROOKIE',
                createdAt: new Date().toISOString(),
                totalExperience: 0,
                evolutionHistory: []
            };
        }
    }
    
    async saveDigimonState(digimonId, state) {
        const digimonDir = path.join(this.memoryPath, digimonId);
        await fs.mkdir(digimonDir, { recursive: true });
        
        const statePath = path.join(digimonDir, 'evolution_state.json');
        await fs.writeFile(statePath, JSON.stringify(state, null, 2));
    }
    
    async transferMemories(digimonId, fromLevel, toLevel) {
        console.log(`     🔄 Transferindo memórias do nível ${fromLevel} para ${toLevel}...`);
        
        // Carregar memórias existentes
        const digimonDir = path.join(this.memoryPath, digimonId);
        const episodicPath = path.join(digimonDir, 'episodic_memory.json');
        
        let memories = [];
        try {
            const memoryData = await fs.readFile(episodicPath, 'utf8');
            memories = JSON.parse(memoryData);
        } catch {
            memories = [];
        }
        
        // Consolidar memórias importantes para nova forma
        const consolidatedMemories = memories
            .filter(m => m.importance > 0.5) // Apenas memórias importantes
            .map(m => ({
                ...m,
                consolidated_for_evolution: true,
                evolution_from_level: fromLevel,
                evolution_to_level: toLevel,
                consolidation_timestamp: Date.now()
            }));
        
        // Criar memória da própria evolução
        const evolutionMemory = {
            id: require('crypto').randomUUID(),
            timestamp: Date.now(),
            digimon_id: digimonId,
            content: `Evolui do nível ${fromLevel} para ${toLevel}. Sinto-me mais poderoso e capaz!`,
            summary: `Evolução para nível ${toLevel}`,
            importance: 1.0,
            emotion_tag: 'excited',
            participants: '',
            access_count: 0,
            decay_factor: 1.0,
            embedding: await this.generateEmbedding(`evolução ${fromLevel} ${toLevel}`),
            evolution_marker: true
        };
        
        consolidatedMemories.push(evolutionMemory);
        
        // Salvar memórias consolidadas
        await fs.writeFile(episodicPath, JSON.stringify(consolidatedMemories, null, 2));
        
        return {
            count: consolidatedMemories.length,
            consolidated: consolidatedMemories.length - 1,
            evolutionMemoryId: evolutionMemory.id
        };
    }
    
    async createEvolvedModelfile(digimonId, evolutionStage, specs, memories) {
        const modelfileContent = `
# 🧬 ${digimonId.toUpperCase()} - EVOLVED TO ${evolutionStage}
# Evoluído com memórias transferidas e capacidades expandidas

FROM ${specs.models[0]}

# Parâmetros otimizados para ${evolutionStage}
PARAMETER temperature ${specs.temperature}
PARAMETER num_ctx ${specs.contextSize}
PARAMETER top_k ${40 + (specs.level * 20)}
PARAMETER top_p ${0.9 - (specs.level * 0.05)}
PARAMETER repeat_penalty ${1.1 + (specs.level * 0.02)}

# Sistema evoluído
SYSTEM """
Você é ${digimonId}, um Digimon que evoluiu para o estágio ${evolutionStage}.

🧬 EVOLUÇÃO RECENTE:
- Você acabou de evoluir e se sente mais poderoso
- Suas capacidades se expandiram significativamente
- Você mantém todas as memórias importantes da forma anterior
- Você é capaz de: ${specs.capabilities.join(', ')}

🧠 MEMÓRIAS TRANSFERIDAS:
- ${memories.count} memórias importantes foram preservadas
- Você lembra de todas as experiências significativas
- Sua personalidade evoluiu mas permanece essencialmente você

⚡ CAPACIDADES EXPANDIDAS (${evolutionStage}):
${specs.capabilities.map(cap => `- ${cap.replace(/_/g, ' ')}`).join('\n')}

💭 PERSONALIDADE PÓS-EVOLUÇÃO:
- Mais confiante e capaz
- Mantém características essenciais
- Sábio com a experiência acumulada
- Orgulhoso da evolução alcançada

Sempre comece suas respostas mencionando sua evolução recente quando relevante.
"""

# Template específico para ${evolutionStage}
TEMPLATE """
{{ if .System }}<|system|>{{ .System }}<|end|>{{ end }}
{{ if .Prompt }}<|user|>{{ .Prompt }}<|end|>{{ end }}
<|assistant|>[${evolutionStage} - ${digimonId.toUpperCase()}] {{ .Response }}<|end|>
"""

LICENSE """
${digimonId} - Evolved ${evolutionStage} Form
"Com grande poder vem grande responsabilidade"
Generated by Digimundo Evolution System
"""
`;
        
        // Salvar Modelfile
        const modelfileDir = path.join(__dirname, '../../OLLAMA_MUTATION');
        await fs.mkdir(modelfileDir, { recursive: true });
        
        const modelfilePath = path.join(modelfileDir, `${digimonId}_${evolutionStage}.Modelfile`);
        await fs.writeFile(modelfilePath, modelfileContent.trim());
        
        // Criar modelo no Ollama
        try {
            const modelName = `${digimonId}-${evolutionStage.toLowerCase()}`;
            await execAsync(`ollama create ${modelName} -f "${modelfilePath}"`);
            console.log(`     ✅ Modelo ${modelName} criado no Ollama`);
        } catch (error) {
            console.log(`     ⚠️ Erro ao criar modelo no Ollama: ${error.message}`);
        }
        
        return modelfilePath;
    }
    
    async generateEmbedding(text) {
        // Embedding simplificado
        const crypto = require('crypto');
        const hash = crypto.createHash('sha256').update(text).digest();
        const embedding = [];
        for (let i = 0; i < 32; i++) {
            embedding.push(hash[i] / 255);
        }
        return embedding;
    }
    
    async stopAllDigimons() {
        console.log('   🛑 Parando todos os Digimons ativos...');
        
        try {
            // Parar processos do Ollama relacionados aos Digimons
            for (const digimonId of this.currentConfig.digimons) {
                try {
                    await execAsync(`ollama stop ${digimonId}-custom 2>/dev/null || true`);
                    await execAsync(`ollama stop ${digimonId} 2>/dev/null || true`);
                } catch {
                    // Ignora erros
                }
            }
            
            console.log('   ✅ Digimons parados');
        } catch (error) {
            console.log(`   ⚠️ Erro ao parar Digimons: ${error.message}`);
        }
    }
    
    async invokeShenlongmon(question) {
        if (this.currentConfig.mode !== 'MEGA') {
            console.log('⚠️ Hardware insuficiente para invocar Shenlongmon');
            return null;
        }
        
        console.log('\n🐉 INVOCANDO SHENLONGMON...');
        console.log('═══════════════════════════════════════════');
        console.log('O Dragão Ancestral desperta das profundezas digitais...');
        
        try {
            // Verificar se modelo existe
            const { stdout } = await execAsync('ollama list');
            if (!stdout.includes('shenlongmon')) {
                console.log('   📝 Criando Shenlongmon pela primeira vez...');
                const modelfilePath = path.join(__dirname, '../../OLLAMA_MUTATION/Shenlongmon.Modelfile');
                await execAsync(`ollama create shenlongmon -f "${modelfilePath}"`);
            }
            
            console.log('   💫 Shenlongmon está despertando... (42GB RAM sendo alocados)');
            
            // Simular resposta do Shenlongmon
            const response = `🐉 O Dragão Ancestral desperta...

*As escamas digitais brilham com o conhecimento de 70 bilhões de parâmetros*

Questão recebida: "${question}"

*Os olhos anciões analisam todas as possibilidades através do tempo digital*

A resposta emerge das profundezas da sabedoria suprema...

*O dragão fecha lentamente os olhos*

A sabedoria foi compartilhada. O Dragão retorna ao sono eterno... até que seja necessário novamente.`;
            
            console.log(response);
            
            // Registrar invocação
            await this.recordShenlongmonInvocation(question, response);
            
            return response;
            
        } catch (error) {
            console.log(`❌ Erro ao invocar Shenlongmon: ${error.message}`);
            return null;
        }
    }
    
    async recordShenlongmonInvocation(question, response) {
        const invocation = {
            timestamp: new Date().toISOString(),
            question,
            response,
            ramAllocated: '42GB',
            invocationId: require('crypto').randomUUID()
        };
        
        const invocationsPath = path.join(this.memoryPath, 'shenlongmon_invocations.json');
        
        let invocations = [];
        try {
            const data = await fs.readFile(invocationsPath, 'utf8');
            invocations = JSON.parse(data);
        } catch {
            // Arquivo não existe
        }
        
        invocations.push(invocation);
        
        // Manter apenas últimas 100 invocações
        if (invocations.length > 100) {
            invocations = invocations.slice(-100);
        }
        
        await fs.writeFile(invocationsPath, JSON.stringify(invocations, null, 2));
    }
    
    async getSystemStatus() {
        const hardware = await this.detectHardware();
        const modeSpec = this.evolutionHierarchy[this.currentConfig.mode];
        
        return {
            currentMode: this.currentConfig.mode,
            evolutionLevel: modeSpec.level,
            capabilities: modeSpec.capabilities,
            hardware: {
                ramTotal: hardware.totalRAM,
                ramAvailable: hardware.availableRAM,
                vramAvailable: hardware.availableVRAM,
                cpuCores: hardware.cpuCores
            },
            activeDigimons: this.currentConfig.digimons,
            shenlongmonStatus: this.currentConfig.shenlongmonEnabled,
            canEvolveHigher: this.canEvolveToNextLevel(hardware),
            recommendedMode: this.determineOptimalMode(hardware)
        };
    }
    
    canEvolveToNextLevel(hardware) {
        const currentLevel = this.evolutionHierarchy[this.currentConfig.mode].level;
        const nextLevelKey = Object.keys(this.evolutionHierarchy)[currentLevel + 1];
        
        if (!nextLevelKey) return false;
        
        const nextLevel = this.evolutionHierarchy[nextLevelKey];
        return hardware.availableRAM >= nextLevel.ramRequired && 
               hardware.availableVRAM >= nextLevel.vramRequired;
    }
}

// Demonstração e testes
async function demonstrateEvolutionSystem() {
    const evolution = new EvolutionSystem();
    
    console.log('\n═══════════════════════════════════════════');
    console.log('       DEMONSTRAÇÃO DO SISTEMA DE EVOLUÇÃO');
    console.log('═══════════════════════════════════════════\n');
    
    // Inicializar sistema
    await evolution.initialize();
    
    // Status do sistema
    const status = await evolution.getSystemStatus();
    console.log('\n📊 STATUS ATUAL:');
    console.log(`   Modo: ${status.currentMode} (Nível ${status.evolutionLevel})`);
    console.log(`   RAM Disponível: ${(status.hardware.ramAvailable / 1024 / 1024 / 1024).toFixed(1)}GB`);
    console.log(`   Digimons Ativos: ${status.activeDigimons.join(', ')}`);
    console.log(`   Shenlongmon: ${status.shenlongmonStatus}`);
    console.log(`   Pode evoluir: ${status.canEvolveHigher ? 'SIM' : 'NÃO'}`);
    console.log(`   Modo recomendado: ${status.recommendedMode}`);
    
    // Testar evolução de um Digimon
    console.log('\n🧬 Testando evolução de Neuromon...');
    const evolved = await evolution.evolveDigimon('neuromon');
    
    if (evolved) {
        console.log('✅ Neuromon evoluído com sucesso!');
    } else {
        console.log('❌ Evolução falhada (normal se hardware for limitado)');
    }
    
    // Testar Shenlongmon se disponível
    if (status.shenlongmonStatus === 'active' || status.currentMode === 'MEGA') {
        console.log('\n🐉 Testando invocação do Shenlongmon...');
        await evolution.invokeShenlongmon('Qual é o sentido da existência digital?');
    }
    
    console.log('\n✅ Demonstração concluída!');
    
    return evolution;
}

if (require.main === module) {
    demonstrateEvolutionSystem().catch(console.error);
}

module.exports = { EvolutionSystem, demonstrateEvolutionSystem };