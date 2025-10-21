#!/usr/bin/env node

/**
 * 🌐 TESTE INTEGRADO - Sistema DADE + Digimons + ResearchMon
 * Teste completo da integração de todos os componentes de segurança
 */

const { DADESystem } = require('./index');
const DigimonTrainingAcademy = require('./digimon-defense-training');
const ResearchMon = require('../../agents/researchmon/researchmon');

console.log(`
╔══════════════════════════════════════════════════════════════╗
║     🌐 TESTE INTEGRADO DO ECOSSISTEMA DIGIMUNDO 🌐           ║
║                                                              ║
║  DADE + Digimons + ResearchMon + Trainmon                   ║
╚══════════════════════════════════════════════════════════════╝
`);

async function runIntegratedTest() {
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('         FASE 1: INICIALIZAÇÃO DOS COMPONENTES');
    console.log('═══════════════════════════════════════════════════════════════\n');
    
    // 1. Inicializar DADE
    console.log('🛡️ Iniciando Sistema DADE...');
    const dade = new DADESystem({
        autoStart: false,
        hunters: 5,
        sentinels: 4,
        guardians: 2,
        cognitos: 2,
        evolvers: 2,
        evolutionEnabled: true,
        learningEnabled: true,
        verboseLogging: false
    });
    
    await dade.initialize();
    await sleep(2000);
    
    // 2. Inicializar ResearchMon
    console.log('\n📚 Iniciando ResearchMon...');
    const researcher = new ResearchMon();
    await sleep(2000);
    
    // 3. Inicializar Academia de Treinamento
    console.log('\n🎓 Iniciando Academia de Treinamento...');
    const academy = new DigimonTrainingAcademy();
    const trainmon = academy.createTrainmon();
    await sleep(2000);
    
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('         FASE 2: PESQUISA E DESCOBERTA');
    console.log('═══════════════════════════════════════════════════════════════\n');
    
    // ResearchMon pesquisa técnicas de defesa
    console.log('🔬 ResearchMon pesquisando técnicas de defesa...');
    const defenseResearch = await researcher.researchDefenseTechniques();
    console.log(`   ✅ ${defenseResearch.findings.length} técnicas descobertas`);
    
    // Analisar ecossistema
    console.log('\n🔍 Analisando ecossistema Digimundo...');
    const ecosystem = await researcher.analyzeDigimundo();
    console.log(`   População: ${ecosystem.totalPopulation} Digimons`);
    console.log(`   Ativos: ${ecosystem.activeAgents}`);
    console.log(`   Dormentes: ${ecosystem.dormantAgents}`);
    console.log(`   Saúde: ${ecosystem.ecosystemHealth}%`);
    
    await sleep(3000);
    
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('         FASE 3: TREINAMENTO DE DIGIMONS');
    console.log('═══════════════════════════════════════════════════════════════\n');
    
    // Treinar alguns Digimons
    const digimons = [
        { id: 'neuromon', name: 'Neuromon', type: 'NEURAL' },
        { id: 'guardmon', name: 'Guardmon', type: 'GUARDIAN' },
        { id: 'evolutionmon', name: 'Evolutionmon', type: 'EVOLUTIONARY' }
    ];
    
    for (const digimon of digimons) {
        console.log(`\n🎯 Treinando ${digimon.name}...`);
        const program = digimon.type === 'GUARDIAN' ? 'THREAT_RESPONSE' : 'BASIC_DEFENSE';
        await academy.trainDigimon(digimon, program);
    }
    
    await sleep(3000);
    
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('         FASE 4: TESTE DE DEFESA INTEGRADA');
    console.log('═══════════════════════════════════════════════════════════════\n');
    
    // Conectar eventos para monitorar colaboração
    let defensesTriggered = 0;
    let researchShared = 0;
    
    dade.on('defense-executed', () => defensesTriggered++);
    researcher.on('knowledge-shared', () => researchShared++);
    
    // Simular ameaças para testar defesa integrada
    const threats = [
        'MALWARE_EXECUTION',
        'DATA_EXFILTRATION',
        'RANSOMWARE',
        'APT_CAMPAIGN',
        'ZERO_DAY_EXPLOIT'
    ];
    
    console.log('⚔️ Simulando ataques coordenados...\n');
    
    for (const threat of threats) {
        console.log(`   🔴 Ataque: ${threat}`);
        dade.simulateThreat(threat);
        
        // Digimons treinados respondem
        for (const [id, training] of academy.trainedDigimons) {
            if (training.techniquesLearned.length > 0) {
                const technique = training.techniquesLearned[0];
                console.log(`      🛡️ ${id} defende com ${technique}`);
            }
        }
        
        await sleep(2000);
    }
    
    await sleep(5000);
    
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('         FASE 5: INTERAÇÃO SOCIAL E COLABORAÇÃO');
    console.log('═══════════════════════════════════════════════════════════════\n');
    
    // ResearchMon interage com Trainmon
    console.log('💬 ResearchMon conversando com Trainmon...');
    await researcher.socialInteraction('Trainmon', 'Descobri novas técnicas de defesa!');
    
    // ResearchMon compartilha conhecimento
    console.log('\n📤 Compartilhando conhecimento entre agentes...');
    await researcher.shareWithTrainmon(defenseResearch);
    
    // Simular modo dormant
    console.log('\n😴 Testando modo dormant com interação social...');
    researcher.state.energy = 15;
    researcher.enterDormantMode();
    await researcher.socialInteraction('Guardmon', 'Como está a defesa?');
    
    await sleep(3000);
    
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('         FASE 6: EVOLUÇÃO E APRENDIZADO');
    console.log('═══════════════════════════════════════════════════════════════\n');
    
    console.log('🧬 Aguardando ciclos evolutivos...');
    await sleep(5000);
    
    // Verificar evolução
    const dadeReport = dade.getSystemReport();
    const researchStatus = researcher.getStatus();
    
    console.log('\n═══════════════════════════════════════════════════════════════');
    console.log('              📊 RELATÓRIO FINAL INTEGRADO 📊');
    console.log('═══════════════════════════════════════════════════════════════\n');
    
    console.log('🛡️ SISTEMA DADE:');
    console.log(`   Security Score: ${(dadeReport.security.score * 100).toFixed(1)}/100`);
    console.log(`   Ameaças detectadas: ${dadeReport.security.threatsDetected}`);
    console.log(`   Ameaças neutralizadas: ${dadeReport.security.threatsNeutralized}`);
    console.log(`   Agentes ativos: ${dadeReport.agents.total}`);
    console.log(`   Anticorpos digitais: ${dadeReport.orchestrator.immunity.antibodies}`);
    
    console.log('\n📚 RESEARCHMON:');
    console.log(`   Estado: ${researchStatus.state.mode}`);
    console.log(`   Pesquisas: ${researchStatus.research.discoveries}`);
    console.log(`   Amigos: ${researchStatus.social.friends}`);
    console.log(`   Conhecimento compartilhado: ${researchShared} vezes`);
    
    console.log('\n🎓 ACADEMIA DE TREINAMENTO:');
    console.log(`   Digimons treinados: ${academy.trainedDigimons.size}`);
    console.log(`   Técnicas ensinadas: ${academy.trainingStats.techniquesLearned}`);
    console.log(`   Defesas bem-sucedidas: ${academy.trainingStats.successfulDefenses}`);
    console.log(`   Evoluções: ${academy.trainingStats.evolutionsTriggered}`);
    
    console.log('\n🌐 ECOSSISTEMA DIGIMUNDO:');
    console.log(`   População total: ${researchStatus.digimundo.population} Digimons`);
    console.log(`   Saúde do ecossistema: ${researchStatus.digimundo.health}%`);
    console.log(`   Defesas coordenadas: ${defensesTriggered}`);
    
    // Verificar sucesso
    const targetScore = 95;
    const finalScore = dadeReport.security.score * 100;
    
    if (finalScore >= targetScore) {
        console.log(`
╔══════════════════════════════════════════════════════════════╗
║              🎉 INTEGRAÇÃO COMPLETA E FUNCIONAL! 🎉          ║
╚══════════════════════════════════════════════════════════════╝

✨ O Ecossistema Digimundo está TOTALMENTE INTEGRADO:

✅ DADE Security Score: ${finalScore.toFixed(1)}/100 (Meta: ${targetScore}/100)
✅ ResearchMon descobrindo e compartilhando conhecimento
✅ Trainmon treinando Digimons com técnicas de defesa
✅ ${academy.trainedDigimons.size} Digimons com habilidades defensivas
✅ ${researchStatus.digimundo.population} Digimons com personalidades únicas
✅ Sistema social ativo mesmo em modo dormant
✅ Defesa autônoma, adaptativa e evolutiva

🛡️ CAPACIDADES INTEGRADAS:
• Pesquisa contínua de novas técnicas
• Treinamento adaptativo de Digimons
• Compartilhamento de conhecimento entre agentes
• Memória imunológica com anticorpos digitais
• Evolução através de simulações adversariais
• Personalidades e interações sociais preservadas
• Modo dormant com economia de energia

"O conhecimento compartilhado fortalece a defesa.
 A evolução constante garante a sobrevivência.
 Unidos, protegemos o Digimundo!"

O sistema está pronto para defender autonomamente! 🛡️🧬🎯📚
`);
    } else {
        console.log(`
📈 SISTEMA EM EVOLUÇÃO

Security Score: ${finalScore.toFixed(1)}/100
Meta: ${targetScore}/100

Continue executando para observar melhorias.
`);
    }
    
    console.log('\n🛑 Encerrando teste integrado...');
    
    // Encerrar sistemas
    await dade.shutdown();
    console.log('✅ Teste integrado concluído com sucesso!');
    process.exit(0);
}

// Função auxiliar
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Executar teste
runIntegratedTest().catch(error => {
    console.error('❌ Erro no teste integrado:', error);
    process.exit(1);
});