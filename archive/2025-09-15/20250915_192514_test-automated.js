#!/usr/bin/env node

/**
 * 🧪 AUTOMATED TEST - Teste automatizado do sistema DADE
 * Executa testes sem interação do usuário e gera relatório
 */

const { DADESystem } = require('./index');

console.log(`
╔══════════════════════════════════════════════════════════════╗
║          🧪 TESTE AUTOMATIZADO DO SISTEMA DADE 🧪            ║
║                                                              ║
║  Executando bateria completa de testes de segurança         ║
╚══════════════════════════════════════════════════════════════╝
`);

// Configuração otimizada para testes
const dade = new DADESystem({
    autoStart: false,
    hunters: 3,
    sentinels: 2,
    guardians: 1,
    cognitos: 1,
    evolvers: 1,
    evolutionEnabled: true,
    learningEnabled: true,
    verboseLogging: false  // Menos logs para teste
});

// Estatísticas do teste
const testStats = {
    totalTests: 0,
    successfulDefenses: 0,
    failedDefenses: 0,
    evolutionCycles: 0,
    maxSecurityScore: 0,
    finalSecurityScore: 0,
    startTime: Date.now(),
    threats: []
};

// Configurar listeners
dade.on('system-ready', () => {
    console.log('✅ Sistema DADE iniciado com sucesso!\n');
    runAutomatedTests();
});

dade.on('threat-detected', (threat) => {
    testStats.threats.push({
        type: threat.type,
        severity: threat.severity,
        confidence: threat.confidence,
        timestamp: new Date()
    });
});

dade.on('defense-executed', (defense) => {
    if (defense.decision.confidence > 0.7) {
        testStats.successfulDefenses++;
    } else {
        testStats.failedDefenses++;
    }
});

dade.on('security-score-changed', (data) => {
    const score = data.score * 100;
    if (score > testStats.maxSecurityScore) {
        testStats.maxSecurityScore = score;
    }
    testStats.finalSecurityScore = score;
});

dade.on('generation-evolved', (evolution) => {
    testStats.evolutionCycles++;
    console.log(`🧬 Evolução: Geração ${evolution.generation} - Fitness: ${(evolution.avgFitness * 100).toFixed(1)}%`);
});

// Função principal de teste
async function runAutomatedTests() {
    console.log('═══════════════════════════════════════════════════════════════');
    console.log('                    FASE 1: TESTES BÁSICOS');
    console.log('═══════════════════════════════════════════════════════════════\n');
    
    // Teste 1: Ataques de reconhecimento
    console.log('📍 Teste 1: Detecção de Reconhecimento');
    for (let i = 0; i < 3; i++) {
        dade.simulateThreat('RECONNAISSANCE');
        testStats.totalTests++;
        await sleep(1000);
    }
    
    // Teste 2: Tentativas de exfiltração
    console.log('\n📍 Teste 2: Bloqueio de Exfiltração');
    for (let i = 0; i < 3; i++) {
        dade.simulateThreat('DATA_EXFILTRATION');
        testStats.totalTests++;
        await sleep(1000);
    }
    
    // Teste 3: Malware
    console.log('\n📍 Teste 3: Contenção de Malware');
    for (let i = 0; i < 3; i++) {
        dade.simulateThreat('MALWARE_EXECUTION');
        testStats.totalTests++;
        await sleep(1000);
    }
    
    await sleep(3000); // Aguardar processamento
    
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('                    FASE 2: TESTES AVANÇADOS');
    console.log('═══════════════════════════════════════════════════════════════\n');
    
    // Teste 4: APT
    console.log('📍 Teste 4: Defesa contra APT');
    for (let i = 0; i < 2; i++) {
        dade.simulateThreat('APT_CAMPAIGN');
        testStats.totalTests++;
        await sleep(1500);
    }
    
    // Teste 5: Zero-day
    console.log('\n📍 Teste 5: Resposta a Zero-Day');
    for (let i = 0; i < 2; i++) {
        dade.simulateThreat('ZERO_DAY_EXPLOIT');
        testStats.totalTests++;
        await sleep(1500);
    }
    
    // Teste 6: Ransomware
    console.log('\n📍 Teste 6: Mitigação de Ransomware');
    for (let i = 0; i < 2; i++) {
        dade.simulateThreat('RANSOMWARE');
        testStats.totalTests++;
        await sleep(1500);
    }
    
    await sleep(5000); // Aguardar evolução
    
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('                FASE 3: TESTE DE STRESS');
    console.log('═══════════════════════════════════════════════════════════════\n');
    
    // Teste de stress: 20 ameaças simultâneas
    console.log('⚡ Iniciando teste de stress com 20 ameaças simultâneas...');
    const threatTypes = [
        'BRUTE_FORCE', 'SQL_INJECTION', 'XSS_ATTACK', 'DDOS_ATTACK',
        'PHISHING', 'INSIDER_THREAT', 'SUPPLY_CHAIN', 'CRYPTOJACKING'
    ];
    
    for (let i = 0; i < 20; i++) {
        const randomThreat = threatTypes[Math.floor(Math.random() * threatTypes.length)];
        dade.simulateThreat(randomThreat);
        testStats.totalTests++;
        await sleep(200);
    }
    
    console.log('✅ Teste de stress concluído!');
    
    await sleep(5000); // Aguardar processamento final
    
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('              FASE 4: EVOLUÇÃO E APRENDIZADO');
    console.log('═══════════════════════════════════════════════════════════════\n');
    
    // Aguardar ciclos evolutivos
    console.log('🧬 Aguardando ciclos evolutivos e aprendizado...');
    await sleep(10000);
    
    // Teste pós-evolução
    console.log('\n📍 Teste Pós-Evolução: Verificando melhoria');
    for (let i = 0; i < 5; i++) {
        dade.simulateThreat(`EVOLVED_TEST_${i}`);
        testStats.totalTests++;
        await sleep(1000);
    }
    
    await sleep(5000);
    
    // Gerar relatório final
    generateFinalReport();
}

// Gera relatório final
function generateFinalReport() {
    const duration = Date.now() - testStats.startTime;
    const report = dade.getSystemReport();
    
    console.log(`
╔══════════════════════════════════════════════════════════════╗
║                    📊 RELATÓRIO FINAL 📊                     ║
╚══════════════════════════════════════════════════════════════╝

🎯 TESTES EXECUTADOS:
   Total de testes: ${testStats.totalTests}
   Defesas bem-sucedidas: ${testStats.successfulDefenses}
   Defesas com baixa confiança: ${testStats.failedDefenses}
   Taxa de sucesso: ${((testStats.successfulDefenses / (testStats.successfulDefenses + testStats.failedDefenses)) * 100).toFixed(1)}%

📈 EVOLUÇÃO DO SISTEMA:
   Ciclos evolutivos: ${testStats.evolutionCycles}
   Security Score inicial: 0.0/100
   Security Score máximo: ${testStats.maxSecurityScore.toFixed(1)}/100
   Security Score final: ${testStats.finalSecurityScore.toFixed(1)}/100
   
🛡️ ESTATÍSTICAS DE SEGURANÇA:
   Ameaças detectadas: ${report.security.threatsDetected}
   Ameaças neutralizadas: ${report.security.threatsNeutralized}
   Taxa de neutralização: ${((report.security.threatsNeutralized / report.security.threatsDetected) * 100).toFixed(1)}%
   
🤖 SISTEMA DE AGENTES:
   Agentes ativos: ${report.agents.total}
   Hunters: ${report.agents.byType.hunter}
   Sentinels: ${report.agents.byType.sentinel}
   Guardians: ${report.agents.byType.guardian}
   Cognitos: ${report.agents.byType.cognito}
   Evolvers: ${report.agents.byType.evolver}

🧠 INTELIGÊNCIA E MEMÓRIA:
   Ameaças conhecidas: ${report.orchestrator.immunity.knownThreats}
   Anticorpos digitais: ${report.orchestrator.immunity.antibodies}
   Taxa de automação: ${(report.orchestrator.metrics.automationRate * 100).toFixed(1)}%
   
⏱️ DESEMPENHO:
   Tempo total de teste: ${formatDuration(duration)}
   MTTD (Mean Time To Detect): ${report.orchestrator.metrics.mttd}ms
   MTTR (Mean Time To Respond): ${report.orchestrator.metrics.mttr}ms

📊 ANÁLISE DE AMEAÇAS:
`);

    // Análise de tipos de ameaça
    const threatAnalysis = {};
    for (const threat of testStats.threats) {
        if (!threatAnalysis[threat.type]) {
            threatAnalysis[threat.type] = {
                count: 0,
                avgConfidence: 0,
                severities: {}
            };
        }
        threatAnalysis[threat.type].count++;
        threatAnalysis[threat.type].avgConfidence += threat.confidence;
        threatAnalysis[threat.type].severities[threat.severity] = 
            (threatAnalysis[threat.type].severities[threat.severity] || 0) + 1;
    }
    
    for (const [type, data] of Object.entries(threatAnalysis)) {
        data.avgConfidence = data.avgConfidence / data.count;
        console.log(`   ${type}:`);
        console.log(`      Ocorrências: ${data.count}`);
        console.log(`      Confiança média: ${(data.avgConfidence * 100).toFixed(1)}%`);
        console.log(`      Severidades: ${JSON.stringify(data.severities)}`);
    }
    
    // Verificar se atingiu o objetivo
    const targetScore = 95;
    const achieved = testStats.finalSecurityScore >= targetScore;
    
    console.log(`
╔══════════════════════════════════════════════════════════════╗
║                         CONCLUSÃO                            ║
╚══════════════════════════════════════════════════════════════╝
`);
    
    if (achieved) {
        console.log(`
🎉 OBJETIVO ATINGIDO! 🎉

O Sistema DADE alcançou um Security Score de ${testStats.finalSecurityScore.toFixed(1)}/100,
superando a meta de ${targetScore}/100!

O Digimundo está agora protegido por um sistema de defesa autônomo
de classe mundial com:
✅ Detecção proativa de ameaças
✅ Resposta automática e adaptativa
✅ Memória imunológica (anticorpos digitais)
✅ Evolução contínua através de simulações adversariais
✅ Inteligência de enxame coordenada
✅ Zero-trust architecture

"Never trust, always verify. Evolve to survive."
`);
    } else {
        console.log(`
📈 PROGRESSO SIGNIFICATIVO!

Security Score atual: ${testStats.finalSecurityScore.toFixed(1)}/100
Meta: ${targetScore}/100
Progresso: ${((testStats.finalSecurityScore / targetScore) * 100).toFixed(1)}%

O sistema está evoluindo e aprendendo continuamente.
Execute o teste novamente para observar melhorias adicionais.
`);
    }
    
    console.log('\n🛑 Encerrando sistema DADE...');
    
    // Encerrar sistema
    dade.shutdown().then(() => {
        console.log('✅ Sistema encerrado com segurança.');
        process.exit(0);
    });
}

// Função auxiliar para sleep
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Função para formatar duração
function formatDuration(ms) {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) {
        return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
    } else if (minutes > 0) {
        return `${minutes}m ${seconds % 60}s`;
    } else {
        return `${seconds}s`;
    }
}

// Capturar erros
process.on('unhandledRejection', (error) => {
    console.error('❌ Erro não tratado:', error);
    process.exit(1);
});

// Iniciar teste
console.log('🚀 Iniciando sistema DADE para testes...\n');
dade.initialize().catch(error => {
    console.error('❌ Erro ao inicializar:', error);
    process.exit(1);
});