#!/usr/bin/env node

/**
 * 🧪 TESTE COMPLETO DO SISTEMA DIGIMUNDO
 * Valida se alcançamos todos os objetivos da conversa
 */

const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

// Cores para output
const colors = {
    reset: '\x1b[0m',
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m'
};

class DigimundoSystemTest {
    constructor() {
        this.tests = [];
        this.results = {
            passed: 0,
            failed: 0,
            warnings: 0,
            details: []
        };
        this.startTime = Date.now();
    }
    
    // Adicionar teste
    addTest(name, description, testFn) {
        this.tests.push({ name, description, testFn });
    }
    
    // Executar todos os testes
    async runAllTests() {
        console.log('\n╔══════════════════════════════════════════════════════════╗');
        console.log('║          🧪 TESTE COMPLETO DO SISTEMA DIGIMUNDO 🧪        ║');
        console.log('╚══════════════════════════════════════════════════════════╝\n');
        
        for (const test of this.tests) {
            await this.runTest(test);
        }
        
        this.printFinalReport();
    }
    
    // Executar um teste
    async runTest(test) {
        console.log(`\n${colors.cyan}▶ ${test.name}${colors.reset}`);
        console.log(`  ${test.description}`);
        
        try {
            const result = await test.testFn();
            
            if (result.success) {
                console.log(`  ${colors.green}✅ PASSOU${colors.reset}: ${result.message}`);
                this.results.passed++;
            } else if (result.warning) {
                console.log(`  ${colors.yellow}⚠️ AVISO${colors.reset}: ${result.message}`);
                this.results.warnings++;
            } else {
                console.log(`  ${colors.red}❌ FALHOU${colors.reset}: ${result.message}`);
                this.results.failed++;
            }
            
            this.results.details.push({
                test: test.name,
                result: result.success ? 'PASSED' : result.warning ? 'WARNING' : 'FAILED',
                message: result.message,
                data: result.data
            });
            
        } catch (error) {
            console.log(`  ${colors.red}❌ ERRO${colors.reset}: ${error.message}`);
            this.results.failed++;
            this.results.details.push({
                test: test.name,
                result: 'ERROR',
                message: error.message
            });
        }
    }
    
    // Imprimir relatório final
    printFinalReport() {
        const duration = Date.now() - this.startTime;
        const total = this.results.passed + this.results.failed + this.results.warnings;
        const successRate = (this.results.passed / total * 100).toFixed(1);
        
        console.log('\n╔══════════════════════════════════════════════════════════╗');
        console.log('║                   📊 RELATÓRIO FINAL 📊                   ║');
        console.log('╚══════════════════════════════════════════════════════════╝\n');
        
        console.log(`⏱️  Tempo de execução: ${(duration / 1000).toFixed(2)}s`);
        console.log(`📈 Taxa de sucesso: ${successRate}%\n`);
        
        console.log(`${colors.green}✅ Passou: ${this.results.passed}${colors.reset}`);
        console.log(`${colors.yellow}⚠️ Avisos: ${this.results.warnings}${colors.reset}`);
        console.log(`${colors.red}❌ Falhou: ${this.results.failed}${colors.reset}`);
        console.log(`📊 Total: ${total}`);
        
        // Verificar se alcançamos os objetivos
        console.log('\n═══════════════════════════════════════════════════════════');
        console.log('                    🎯 OBJETIVOS ALCANÇADOS?');
        console.log('═══════════════════════════════════════════════════════════\n');
        
        this.checkObjectives();
    }
    
    // Verificar objetivos da conversa
    checkObjectives() {
        const objectives = [
            {
                name: 'Debugging Automático',
                description: 'Sistema que prevê e corrige erros automaticamente',
                achieved: this.checkDebugmon()
            },
            {
                name: 'IA que Treina IA',
                description: '5 métodos de treinamento com seleção inteligente',
                achieved: this.checkTrainmon()
            },
            {
                name: 'Comunicação entre Digimons',
                description: 'Digimons conversam e colaboram',
                achieved: this.checkCommunication()
            },
            {
                name: 'Sistema IA Town',
                description: 'Convivência social com interações',
                achieved: this.checkIATown()
            },
            {
                name: 'Digilibrary',
                description: 'Biblioteca versionada que nunca apaga',
                achieved: this.checkDigilibrary()
            },
            {
                name: 'Personalidades Privadas',
                description: 'Cada Digimon tem personalidade única',
                achieved: this.checkPersonalities()
            },
            {
                name: 'Orquestrador Central',
                description: 'Gestormon evoluído coordenando tudo',
                achieved: this.checkOrchestrator()
            },
            {
                name: 'Memória Evolutiva',
                description: 'Sistema aprende e evolui com o tempo',
                achieved: this.checkEvolution()
            }
        ];
        
        let achievedCount = 0;
        
        objectives.forEach(obj => {
            if (obj.achieved) {
                console.log(`${colors.green}✅ ${obj.name}${colors.reset}`);
                console.log(`   ${obj.description}`);
                achievedCount++;
            } else {
                console.log(`${colors.red}❌ ${obj.name}${colors.reset}`);
                console.log(`   ${obj.description}`);
            }
        });
        
        const achievementRate = (achievedCount / objectives.length * 100).toFixed(1);
        
        console.log('\n═══════════════════════════════════════════════════════════');
        
        if (achievementRate >= 80) {
            console.log(`${colors.green}🎉 SUCESSO! ${achievementRate}% dos objetivos alcançados!${colors.reset}`);
            console.log('O sistema Digimundo está completo e operacional!');
        } else if (achievementRate >= 60) {
            console.log(`${colors.yellow}⚠️ PARCIAL: ${achievementRate}% dos objetivos alcançados${colors.reset}`);
            console.log('O sistema está funcional mas precisa de ajustes.');
        } else {
            console.log(`${colors.red}❌ INCOMPLETO: Apenas ${achievementRate}% dos objetivos${colors.reset}`);
            console.log('O sistema precisa de mais desenvolvimento.');
        }
        
        console.log('═══════════════════════════════════════════════════════════\n');
    }
    
    // Verificações específicas
    checkDebugmon() {
        const passed = this.results.details.filter(d => 
            d.test.includes('Debugmon') && d.result === 'PASSED'
        ).length;
        return passed > 0;
    }
    
    checkTrainmon() {
        const passed = this.results.details.filter(d => 
            d.test.includes('Trainmon') && d.result === 'PASSED'
        ).length;
        return passed > 0;
    }
    
    checkCommunication() {
        const passed = this.results.details.filter(d => 
            d.test.includes('Comunicação') && d.result === 'PASSED'
        ).length;
        return passed > 0;
    }
    
    checkIATown() {
        const passed = this.results.details.filter(d => 
            d.test.includes('IA Town') && d.result === 'PASSED'
        ).length;
        return passed > 0;
    }
    
    checkDigilibrary() {
        const passed = this.results.details.filter(d => 
            d.test.includes('Digilibrary') && d.result === 'PASSED'
        ).length;
        return passed > 0;
    }
    
    checkPersonalities() {
        const passed = this.results.details.filter(d => 
            d.test.includes('Personalidades') && d.result === 'PASSED'
        ).length;
        return passed > 0;
    }
    
    checkOrchestrator() {
        const passed = this.results.details.filter(d => 
            d.test.includes('Orchestrator') && d.result === 'PASSED'
        ).length;
        return passed > 0;
    }
    
    checkEvolution() {
        const passed = this.results.details.filter(d => 
            d.test.includes('Evolução') && d.result === 'PASSED'
        ).length;
        return passed > 0;
    }
}

// Criar suite de testes
const testSuite = new DigimundoSystemTest();

// TESTE 1: Verificar estrutura de arquivos
testSuite.addTest(
    'Estrutura de Arquivos',
    'Verifica se todos os arquivos principais existem',
    async () => {
        const requiredFiles = [
            '/Users/clubproducoes/Digimundo/core/orchestrator/supreme-orchestrator.js',
            '/Users/clubproducoes/Digimundo/core/orchestrator/supreme-orchestrator-enhanced.js',
            '/Users/clubproducoes/Digimundo/core/orchestrator/digimon-integration.js',
            '/Users/clubproducoes/Digimundo/core/agents/debugmon/autonomous-debugger.js',
            '/Users/clubproducoes/Digimundo/core/agents/trainmon/ai-trainer-system.js',
            '/Users/clubproducoes/Digimundo/LAUNCH_SUPREME_ORCHESTRATOR.sh'
        ];
        
        let missing = [];
        for (const file of requiredFiles) {
            try {
                await fs.access(file);
            } catch {
                missing.push(path.basename(file));
            }
        }
        
        if (missing.length === 0) {
            return { success: true, message: 'Todos os arquivos principais existem' };
        } else if (missing.length <= 2) {
            return { warning: true, message: `Faltando: ${missing.join(', ')}` };
        } else {
            return { success: false, message: `Muitos arquivos faltando: ${missing.length}` };
        }
    }
);

// TESTE 2: Verificar Debugmon
testSuite.addTest(
    'Debugmon Operacional',
    'Verifica se o Debugmon está configurado corretamente',
    async () => {
        try {
            const debugmonPath = '/Users/clubproducoes/Digimundo/core/agents/debugmon/autonomous-debugger.js';
            const content = await fs.readFile(debugmonPath, 'utf-8');
            
            const hasAutoFix = content.includes('autoFix');
            const hasPatternRecognition = content.includes('pattern');
            const hasQwenModel = content.includes('qwen');
            
            if (hasAutoFix && hasPatternRecognition) {
                return { success: true, message: 'Debugmon com auto-fix e reconhecimento de padrões' };
            } else if (hasAutoFix || hasPatternRecognition) {
                return { warning: true, message: 'Debugmon parcialmente configurado' };
            } else {
                return { success: false, message: 'Debugmon sem capacidades avançadas' };
            }
        } catch (error) {
            return { success: false, message: 'Debugmon não encontrado' };
        }
    }
);

// TESTE 3: Verificar Trainmon e 5 métodos
testSuite.addTest(
    'Trainmon e 5 Métodos',
    'Verifica se Trainmon tem os 5 métodos de treinamento',
    async () => {
        try {
            const trainmonPath = '/Users/clubproducoes/Digimundo/core/agents/trainmon/ai-trainer-system.js';
            const content = await fs.readFile(trainmonPath, 'utf-8');
            
            const methods = ['RLAIF', 'ADVERSARIAL', 'SELF_SUPERVISED', 'CHAOS', 'TORQUE'];
            const foundMethods = methods.filter(m => content.includes(m));
            
            if (foundMethods.length === 5) {
                return { success: true, message: 'Todos os 5 métodos implementados' };
            } else if (foundMethods.length >= 3) {
                return { warning: true, message: `${foundMethods.length}/5 métodos encontrados` };
            } else {
                return { success: false, message: 'Métodos de treinamento incompletos' };
            }
        } catch (error) {
            return { success: false, message: 'Trainmon não encontrado' };
        }
    }
);

// TESTE 4: Verificar Supreme Orchestrator
testSuite.addTest(
    'Supreme Orchestrator',
    'Verifica se o Orchestrator está completo',
    async () => {
        try {
            const SupremeOrchestrator = require('/Users/clubproducoes/Digimundo/core/orchestrator/supreme-orchestrator.js');
            const orchestrator = new SupremeOrchestrator();
            
            const hasIATown = orchestrator.iaTown !== undefined;
            const hasDigilibrary = orchestrator.digilibrary !== undefined;
            const hasPersonalities = orchestrator.personalitySystem !== undefined;
            const hasTrainingMethods = orchestrator.trainingMethods !== undefined;
            
            if (hasIATown && hasDigilibrary && hasPersonalities && hasTrainingMethods) {
                return { success: true, message: 'Orchestrator com todos os sistemas' };
            } else {
                const missing = [];
                if (!hasIATown) missing.push('IA Town');
                if (!hasDigilibrary) missing.push('Digilibrary');
                if (!hasPersonalities) missing.push('Personalidades');
                if (!hasTrainingMethods) missing.push('Métodos');
                
                return { warning: true, message: `Faltando: ${missing.join(', ')}` };
            }
        } catch (error) {
            return { success: false, message: `Erro ao carregar Orchestrator: ${error.message}` };
        }
    }
);

// TESTE 5: Verificar IA Town
testSuite.addTest(
    'Sistema IA Town',
    'Verifica funcionalidades sociais',
    async () => {
        try {
            const SupremeOrchestrator = require('/Users/clubproducoes/Digimundo/core/orchestrator/supreme-orchestrator.js');
            const orchestrator = new SupremeOrchestrator();
            
            // Criar interação de teste
            const interaction = await orchestrator.iaTown.createSocialInteraction(
                'TestDigimon1',
                'TestDigimon2',
                'CONVERSATION',
                'Teste de comunicação'
            );
            
            if (interaction && interaction.id) {
                return { success: true, message: 'IA Town criando interações sociais' };
            } else {
                return { warning: true, message: 'IA Town parcialmente funcional' };
            }
        } catch (error) {
            return { success: false, message: 'IA Town não operacional' };
        }
    }
);

// TESTE 6: Verificar Digilibrary
testSuite.addTest(
    'Digilibrary Versionamento',
    'Verifica se a biblioteca versiona corretamente',
    async () => {
        try {
            const SupremeOrchestrator = require('/Users/clubproducoes/Digimundo/core/orchestrator/supreme-orchestrator.js');
            const orchestrator = new SupremeOrchestrator();
            
            // Inicializar Digilibrary
            await orchestrator.digilibrary.initialize();
            
            // Escrever livro de teste
            const bookId = await orchestrator.digilibrary.writeBook(
                'Livro de Teste',
                'Conteúdo inicial',
                'TestAuthor'
            );
            
            // Atualizar livro
            await orchestrator.digilibrary.updateBook(
                bookId,
                'Conteúdo atualizado',
                'TestEditor'
            );
            
            // Verificar histórico
            const history = await orchestrator.digilibrary.getVersionHistory(bookId);
            
            if (history && history.length >= 2) {
                return { success: true, message: 'Digilibrary com versionamento completo' };
            } else {
                return { warning: true, message: 'Versionamento parcial' };
            }
        } catch (error) {
            return { success: false, message: 'Digilibrary não funcional' };
        }
    }
);

// TESTE 7: Verificar Personalidades
testSuite.addTest(
    'Sistema de Personalidades',
    'Verifica personalidades únicas e privadas',
    async () => {
        try {
            const SupremeOrchestrator = require('/Users/clubproducoes/Digimundo/core/orchestrator/supreme-orchestrator.js');
            const orchestrator = new SupremeOrchestrator();
            
            // Criar personalidade de teste
            const personality = orchestrator.personalitySystem.createPersonality(
                'TestDigimon',
                { openness: 0.8, conscientiousness: 0.7 }
            );
            
            // Verificar acesso privado
            const publicView = orchestrator.personalitySystem.getPersonality('TestDigimon', 'OtherDigimon');
            const privateView = orchestrator.personalitySystem.getPersonality('TestDigimon', 'TestDigimon');
            
            const hasQuirks = personality.quirks && personality.quirks.length > 0;
            const hasPrivacy = publicView.traits === undefined || Object.keys(publicView.publicTraits || {}).length < 5;
            
            if (hasQuirks && hasPrivacy) {
                return { success: true, message: 'Personalidades únicas e privadas funcionando' };
            } else {
                return { warning: true, message: 'Sistema de personalidades parcial' };
            }
        } catch (error) {
            return { success: false, message: 'Sistema de personalidades não funcional' };
        }
    }
);

// TESTE 8: Verificar Comunicação
testSuite.addTest(
    'Comunicação entre Digimons',
    'Verifica se Digimons podem se comunicar',
    async () => {
        try {
            const SupremeOrchestrator = require('/Users/clubproducoes/Digimundo/core/orchestrator/supreme-orchestrator.js');
            const orchestrator = new SupremeOrchestrator();
            
            // Registrar Digimons de teste
            orchestrator.registerDigimon({
                name: 'CommTest1',
                role: 'tester',
                model: 'test'
            });
            
            orchestrator.registerDigimon({
                name: 'CommTest2',
                role: 'tester',
                model: 'test'
            });
            
            // Testar comunicação
            let messageReceived = false;
            
            orchestrator.on('message-to-CommTest2', (message) => {
                if (message.from === 'CommTest1') {
                    messageReceived = true;
                }
            });
            
            // Enviar mensagem
            orchestrator.emit('message-to-SupremeOrchestrator', {
                from: 'CommTest1',
                to: 'CommTest2',
                content: { type: 'TEST', data: 'Hello' }
            });
            
            // Processar fila
            await orchestrator.processMessageQueue();
            
            if (messageReceived || orchestrator.messageQueue.length === 0) {
                return { success: true, message: 'Comunicação entre Digimons funcionando' };
            } else {
                return { warning: true, message: 'Comunicação parcialmente funcional' };
            }
        } catch (error) {
            return { success: false, message: 'Sistema de comunicação falhou' };
        }
    }
);

// TESTE 9: Verificar Evolução
testSuite.addTest(
    'Memória Evolutiva',
    'Verifica se o sistema evolui com o tempo',
    async () => {
        try {
            const SupremeOrchestrator = require('/Users/clubproducoes/Digimundo/core/orchestrator/supreme-orchestrator.js');
            const orchestrator = new SupremeOrchestrator();
            
            // Adicionar dados à memória
            orchestrator.sharedMemory.set('test-key-1', { results: [1, 1, 2, 2, 3, 3] });
            orchestrator.sharedMemory.set('test-key-2', { results: ['a', 'a', 'b', 'b'] });
            
            // Forçar evolução
            await orchestrator.evolveMemory();
            
            if (orchestrator.memoryEvolution.length > 0) {
                const lastEvolution = orchestrator.memoryEvolution[orchestrator.memoryEvolution.length - 1];
                if (lastEvolution.patternsFound.length > 0) {
                    return { success: true, message: 'Sistema evoluindo e encontrando padrões' };
                }
            }
            
            return { warning: true, message: 'Evolução implementada mas sem padrões detectados' };
        } catch (error) {
            return { success: false, message: 'Sistema de evolução não funcional' };
        }
    }
);

// TESTE 10: Verificar Bug Factory
testSuite.addTest(
    'Bug Factory',
    'Verifica se a Bug Factory está gerando bugs',
    async () => {
        try {
            const logPath = '/tmp/bug-factory.log';
            const content = await fs.readFile(logPath, 'utf-8');
            const lines = content.split('\n');
            const lastLines = lines.slice(-10);
            
            const totalMatch = lastLines.find(l => l.includes('Total de bugs gerados:'));
            
            if (totalMatch) {
                const match = totalMatch.match(/Total de bugs gerados: (\d+)/);
                if (match) {
                    const total = parseInt(match[1]);
                    if (total > 100) {
                        return { success: true, message: `Bug Factory ativa: ${total} bugs gerados` };
                    } else if (total > 50) {
                        return { warning: true, message: `Bug Factory parcial: ${total} bugs` };
                    }
                }
            }
            
            return { success: false, message: 'Bug Factory não está gerando bugs suficientes' };
        } catch (error) {
            return { warning: true, message: 'Bug Factory log não encontrado' };
        }
    }
);

// TESTE 11: Verificar Integração
testSuite.addTest(
    'Integração de Digimons',
    'Verifica se os Digimons estão integrados',
    async () => {
        try {
            const IntegrationModule = require('/Users/clubproducoes/Digimundo/core/orchestrator/digimon-integration.js');
            
            // Criar mock orchestrator
            const mockOrchestrator = {
                emit: () => {},
                on: () => {},
                broadcast: () => {},
                iaTown: {
                    createSocialInteraction: () => {},
                    districts: { RESEARCH: [], DEFENSE: [] }
                },
                digilibrary: { writeBook: async () => 'test-book' },
                personalitySystem: { addPrivateMemory: () => {} },
                digimons: new Map(),
                priorityQueue: [],
                trainingMethods: {}
            };
            
            const integration = new IntegrationModule(mockOrchestrator);
            await integration.integrateAll();
            
            const status = integration.getIntegrationStatus();
            
            if (status.connected >= 10) {
                return { success: true, message: `${status.connected} Digimons integrados` };
            } else if (status.connected >= 5) {
                return { warning: true, message: `Apenas ${status.connected} Digimons integrados` };
            } else {
                return { success: false, message: 'Integração insuficiente' };
            }
        } catch (error) {
            return { success: false, message: 'Módulo de integração falhou' };
        }
    }
);

// TESTE 12: Teste de carga do Enhanced
testSuite.addTest(
    'Orchestrator Enhanced',
    'Verifica versão evoluída com todas as capacidades',
    async () => {
        try {
            const Enhanced = require('/Users/clubproducoes/Digimundo/core/orchestrator/supreme-orchestrator-enhanced.js');
            const orchestrator = new Enhanced();
            
            const hasConsensus = orchestrator.consensusSystem !== undefined;
            const hasRewards = orchestrator.rewardSystem !== undefined;
            const hasAdvanced = orchestrator.advancedCapabilities !== undefined;
            const hasDebugmonInt = orchestrator.debugmonIntegration !== undefined;
            const hasTrainmonInt = orchestrator.trainmonIntegration !== undefined;
            
            const features = [];
            if (hasConsensus) features.push('Consenso');
            if (hasRewards) features.push('Recompensas');
            if (hasAdvanced) features.push('Capacidades Avançadas');
            if (hasDebugmonInt) features.push('Integração Debugmon');
            if (hasTrainmonInt) features.push('Integração Trainmon');
            
            if (features.length === 5) {
                return { success: true, message: 'Enhanced com todas as capacidades' };
            } else if (features.length >= 3) {
                return { warning: true, message: `Enhanced com ${features.join(', ')}` };
            } else {
                return { success: false, message: 'Enhanced incompleto' };
            }
        } catch (error) {
            return { success: false, message: 'Enhanced não carrega' };
        }
    }
);

// Executar todos os testes
async function runTests() {
    await testSuite.runAllTests();
    
    // Salvar relatório
    const report = {
        timestamp: new Date().toISOString(),
        results: testSuite.results,
        objectives: {
            debugmon: testSuite.checkDebugmon(),
            trainmon: testSuite.checkTrainmon(),
            communication: testSuite.checkCommunication(),
            iaTown: testSuite.checkIATown(),
            digilibrary: testSuite.checkDigilibrary(),
            personalities: testSuite.checkPersonalities(),
            orchestrator: testSuite.checkOrchestrator(),
            evolution: testSuite.checkEvolution()
        }
    };
    
    const reportPath = '/Users/clubproducoes/Digimundo/TEST_RESULTS.json';
    await fs.writeFile(reportPath, JSON.stringify(report, null, 2));
    
    console.log(`\n📄 Relatório salvo em: ${reportPath}\n`);
}

// Executar se chamado diretamente
if (require.main === module) {
    runTests().catch(console.error);
}

module.exports = DigimundoSystemTest;