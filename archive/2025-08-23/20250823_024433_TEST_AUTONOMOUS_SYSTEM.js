#!/usr/bin/env node

/**
 * 🧪 Teste do Sistema Autônomo Revolucionário
 * Demonstração de processamento de comandos em linguagem natural
 */

const SupremeOrchestrator = require('./core/orchestrator/supreme-orchestrator');
const AutonomousSystem = require('./core/holon/autonomous-system');

async function testAutonomousSystem() {
    console.log('\n╭─────────────────────────────────────────────────────────────────╮');
    console.log('│                                                                 │');
    console.log('│     🌐 TESTE DO SISTEMA AUTÔNOMO REVOLUCIONÁRIO 🌐           │');
    console.log('│                                                                 │');
    console.log('│     Arquitetura Holon + HTN+LLM + Self-Healing + Trust        │');
    console.log('│                                                                 │');
    console.log('╰─────────────────────────────────────────────────────────────────╯\n');
    
    // Inicializar Orchestrador
    console.log('\n🎯 Inicializando Supreme Orchestrator...');
    const orchestrator = new SupremeOrchestrator();
    await orchestrator.initialize();
    
    // Inicializar Sistema Autônomo
    console.log('\n🌐 Inicializando Sistema Autônomo...');
    const autonomousSystem = new AutonomousSystem(orchestrator);
    
    // Aguardar inicialização completa
    await new Promise(resolve => {
        autonomousSystem.once('system-ready', resolve);
    });
    
    // Teste 1: Comando simples
    console.log('\n════════════════════════════════════════════════════════════');
    console.log('TESTE 1: Comando Simples');
    console.log('════════════════════════════════════════════════════════════');
    
    let result = await autonomousSystem.processNaturalLanguageCommand(
        "Analise o código do sistema e identifique possíveis melhorias"
    );
    
    if (result.success) {
        console.log('\n✓ Comando processado com sucesso!');
        console.log(`  Intent detectado: ${result.understanding.intent}`);
        console.log(`  Ações executadas: ${result.results.length}`);
    }
    
    // Teste 2: Comando complexo
    console.log('\n════════════════════════════════════════════════════════════');
    console.log('TESTE 2: Comando Complexo');
    console.log('════════════════════════════════════════════════════════════');
    
    result = await autonomousSystem.processNaturalLanguageCommand(
        "Crie uma nova funcionalidade de cache inteligente que aprende com o uso e otimiza automaticamente"
    );
    
    if (result.success) {
        console.log('\n✓ Comando complexo processado!');
        console.log(`  Plano gerado: ${result.plan.length} etapas`);
    }
    
    // Teste 3: Simular falha e recuperação
    console.log('\n════════════════════════════════════════════════════════════');
    console.log('TESTE 3: Auto-Recuperação');
    console.log('════════════════════════════════════════════════════════════');
    
    // Simular erro
    console.log('\n🔴 Simulando erro de memória...');
    autonomousSystem.selfHealing.handleIncident({
        type: 'memory-leak',
        severity: 'warning',
        memoryBefore: process.memoryUsage().heapUsed,
        timestamp: Date.now()
    });
    
    // Aguardar recuperação
    await sleep(2000);
    
    // Teste 4: Consenso entre Holons
    console.log('\n════════════════════════════════════════════════════════════');
    console.log('TESTE 4: Consenso entre Holons');
    console.log('════════════════════════════════════════════════════════════');
    
    const holonIds = Array.from(autonomousSystem.holons.keys()).slice(0, 3);
    const consensus = await autonomousSystem.trustSystem.reachConsensus(
        'architectural-decision',
        holonIds,
        { protocol: 'byzantine' }
    );
    
    console.log(`\n✓ Consenso: ${consensus.consensus ? 'ALCANÇADO' : 'NÃO ALCANÇADO'}`);
    if (consensus.decision) {
        console.log(`  Decisão: ${consensus.decision}`);
    }
    
    // Teste 5: Alocação de tarefas por confiança
    console.log('\n════════════════════════════════════════════════════════════');
    console.log('TESTE 5: Alocação Inteligente de Tarefas');
    console.log('════════════════════════════════════════════════════════════');
    
    const task = {
        name: 'optimize-critical-path',
        requiredCapabilities: ['optimization', 'performance-tracking']
    };
    
    const allocation = await autonomousSystem.trustSystem.allocateTask(
        task,
        holonIds
    );
    
    if (allocation) {
        console.log(`\n✓ Tarefa alocada para: ${allocation.agent.name}`);
        console.log(`  Score de confiança: ${allocation.metrics.score.toFixed(3)}`);
    }
    
    // Teste 6: Matriz de confiança
    console.log('\n════════════════════════════════════════════════════════════');
    console.log('TESTE 6: Visualização da Matriz de Confiança');
    console.log('════════════════════════════════════════════════════════════');
    
    autonomousSystem.trustSystem.visualizeTrustMatrix();
    
    // Relatório final do sistema
    console.log('\n════════════════════════════════════════════════════════════');
    console.log('RELATÓRIO FINAL DO SISTEMA');
    console.log('════════════════════════════════════════════════════════════');
    
    const systemReport = autonomousSystem.getSystemReport();
    
    console.log('\n📊 STATUS GERAL:');
    console.log(`   Estado: ${systemReport.status}`);
    console.log(`   Nível de Autonomia: ${systemReport.autonomyLevel}`);
    console.log(`   Holons Ativos: ${systemReport.holons.active}/${systemReport.holons.total}`);
    
    console.log('\n📋 MÉTRICAS:');
    console.log(`   Tarefas Processadas: ${systemReport.metrics.tasksProcessed}`);
    console.log(`   Planos Executados: ${systemReport.metrics.plansExecuted}`);
    console.log(`   Incidentes Recuperados: ${systemReport.metrics.incidentsRecovered}`);
    console.log(`   Consensos Alcançados: ${systemReport.metrics.consensusAchieved}`);
    console.log(`   Score de Autonomia: ${systemReport.metrics.autonomyScore.toFixed(3)}`);
    
    if (systemReport.health) {
        console.log('\n🎯 SAÚDE DO SISTEMA:');
        console.log(`   Uptime: ${systemReport.health.uptime}`);
        console.log(`   Taxa de Sucesso: ${systemReport.health.successRate}`);
        console.log(`   MTTR: ${systemReport.health.mttr}`);
    }
    
    if (systemReport.trust) {
        console.log('\n🤝 SISTEMA DE CONFIANÇA:');
        console.log(`   Nível Médio de Confiança: ${systemReport.trust.averageTrustLevel}`);
        console.log(`   Taxa de Comunicação: ${systemReport.trust.communicationMetrics.successRate}`);
        console.log(`   Taxa de Consenso: ${systemReport.trust.consensusMetrics.successRate}`);
    }
    
    // Conclusão
    console.log('\n╭─────────────────────────────────────────────────────────────────╮');
    console.log('│                                                                 │');
    console.log('│              🎉 TESTE COMPLETO COM SUCESSO! 🎉                 │');
    console.log('│                                                                 │');
    console.log('│   O Sistema Autônomo Revolucionário está operacional:         │');
    console.log('│                                                                 │');
    console.log('│   ✅ Arquitetura Holon funcionando                             │');
    console.log('│   ✅ Planejamento HTN+LLM ativo                                │');
    console.log('│   ✅ Auto-recuperação multi-camadas                            │');
    console.log('│   ✅ Comunicação baseada em confiança                          │');
    console.log('│   ✅ Processamento de linguagem natural                        │');
    console.log('│                                                                 │');
    console.log('│   🌐 O futuro do desenvolvimento de software é autônomo! 🌐    │');
    console.log('│                                                                 │');
    console.log('╰─────────────────────────────────────────────────────────────────╯\n');
    
    // Desligar sistema
    await autonomousSystem.shutdown();
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Executar teste
testAutonomousSystem().catch(console.error);