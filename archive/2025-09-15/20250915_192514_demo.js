#!/usr/bin/env node

/**
 * 🎮 DADE DEMO - Demonstração do Sistema de Defesa Autônoma
 * 
 * Este script demonstra as capacidades do DADE em ação
 */

const { DADESystem } = require('./index');

console.log(`
╔══════════════════════════════════════════════════════════════╗
║            🎮 DEMONSTRAÇÃO DO SISTEMA DADE 🎮                ║
║                                                              ║
║  Sistema de Defesa Autônoma com Memória Imunológica         ║
║                e Evolução Adversarial                       ║
╚══════════════════════════════════════════════════════════════╝
`);

// Criar instância do DADE com configuração personalizada
const dade = new DADESystem({
    autoStart: false,  // Controle manual da inicialização
    hunters: 3,         // 3 agentes caçadores
    sentinels: 2,       // 2 agentes sentinelas
    guardians: 1,       // 1 agente guardião
    cognitos: 1,        // 1 agente cognito
    evolvers: 1,        // 1 agente evolver
    evolutionEnabled: true,
    learningEnabled: true,
    verboseLogging: true  // Logs detalhados para demo
});

// Configurar listeners para eventos importantes
dade.on('system-ready', (data) => {
    console.log('\n🎉 Sistema DADE pronto para defender o Digimundo!');
    console.log(`   Agentes ativos: ${data.agents}`);
    
    // Iniciar demonstração
    startDemo();
});

dade.on('threat-detected', (threat) => {
    console.log(`\n🚨 AMEAÇA GLOBAL DETECTADA:`);
    console.log(`   Tipo: ${threat.type}`);
    console.log(`   Severidade: ${threat.severity}`);
    console.log(`   Confiança: ${(threat.confidence * 100).toFixed(1)}%`);
});

dade.on('defense-executed', (defense) => {
    console.log(`\n🛡️ DEFESA EXECUTADA:`);
    console.log(`   Decisão: ${defense.decision.action}`);
    console.log(`   Confiança: ${(defense.decision.confidence * 100).toFixed(1)}%`);
});

dade.on('security-score-changed', (data) => {
    const score = (data.score * 100).toFixed(1);
    console.log(`\n📊 Security Score atualizado: ${score}/100`);
});

dade.on('forensic-report', (report) => {
    console.log(`\n📄 RELATÓRIO FORENSE GERADO:`);
    console.log(`   ID: ${report.id}`);
    console.log(`   Severidade: ${report.severity}`);
    console.log(`   Confiança: ${(report.metadata.confidence * 100).toFixed(1)}%`);
});

dade.on('integrity-breach', (violation) => {
    console.log(`\n🔴 ALERTA CRÍTICO - VIOLAÇÃO DE INTEGRIDADE!`);
    console.log(`   Agente comprometido: ${violation.agentName}`);
});

dade.on('emergency-response', (data) => {
    console.log(`\n⚠️ RESPOSTA DE EMERGÊNCIA ATIVADA!`);
    console.log(`   Kill Switch ID: ${data.id}`);
});

dade.on('swarm-defense', () => {
    console.log(`\n🐝 MODO ENXAME ATIVADO - Todos os agentes coordenados!`);
});

// Função principal de demonstração
async function startDemo() {
    console.log(`
═══════════════════════════════════════════════════════════════
                    INICIANDO CENÁRIOS DE TESTE
═══════════════════════════════════════════════════════════════
`);
    
    // Aguardar sistema estabilizar
    await sleep(2000);
    
    // Cenário 1: Ataque de baixa intensidade
    console.log('\n📍 CENÁRIO 1: Ataque de Reconhecimento');
    console.log('────────────────────────────────────────');
    dade.simulateThreat('RECONNAISSANCE');
    await sleep(5000);
    
    // Cenário 2: Tentativa de exfiltração
    console.log('\n📍 CENÁRIO 2: Tentativa de Exfiltração de Dados');
    console.log('────────────────────────────────────────');
    dade.simulateThreat('DATA_EXFILTRATION');
    await sleep(5000);
    
    // Cenário 3: Malware detectado
    console.log('\n📍 CENÁRIO 3: Execução de Malware');
    console.log('────────────────────────────────────────');
    dade.simulateThreat('MALWARE_EXECUTION');
    await sleep(5000);
    
    // Cenário 4: Ataque coordenado
    console.log('\n📍 CENÁRIO 4: Ataque Coordenado (APT)');
    console.log('────────────────────────────────────────');
    dade.simulateThreat('APT_CAMPAIGN');
    await sleep(5000);
    
    // Cenário 5: Zero-day
    console.log('\n📍 CENÁRIO 5: Exploração Zero-Day');
    console.log('────────────────────────────────────────');
    dade.simulateThreat('ZERO_DAY_EXPLOIT');
    await sleep(5000);
    
    // Mostrar relatório final
    console.log(`
═══════════════════════════════════════════════════════════════
                        RELATÓRIO FINAL
═══════════════════════════════════════════════════════════════
`);
    
    const report = dade.getSystemReport();
    
    console.log('📊 ESTATÍSTICAS DO SISTEMA:');
    console.log(`   Uptime: ${formatUptime(report.system.uptime)}`);
    console.log(`   Security Score: ${(report.security.score * 100).toFixed(1)}/100`);
    console.log(`   Ameaças Detectadas: ${report.security.threatsDetected}`);
    console.log(`   Ameaças Neutralizadas: ${report.security.threatsNeutralized}`);
    console.log(`   Ciclos Evolutivos: ${report.security.evolutionCycles}`);
    
    console.log('\n🤖 AGENTES DEPLOYADOS:');
    for (const [type, count] of Object.entries(report.agents.byType)) {
        console.log(`   ${type}: ${count} agente(s)`);
    }
    
    console.log('\n🧠 STATUS DO ORQUESTRADOR:');
    if (report.orchestrator) {
        console.log(`   Score de Segurança: ${report.orchestrator.securityScore}/100`);
        console.log(`   Nível de Ameaça: ${report.orchestrator.threatLevel}`);
        console.log(`   Anticorpos Digitais: ${report.orchestrator.immunity.antibodies}`);
        console.log(`   Ameaças Conhecidas: ${report.orchestrator.immunity.knownThreats}`);
    }
    
    // Menu interativo
    console.log(`
═══════════════════════════════════════════════════════════════
                        MENU INTERATIVO
═══════════════════════════════════════════════════════════════
`);
    console.log('Comandos disponíveis:');
    console.log('  1 - Simular nova ameaça');
    console.log('  2 - Ver status do sistema');
    console.log('  3 - Ver relatório completo');
    console.log('  4 - Executar teste de stress');
    console.log('  5 - Encerrar sistema');
    console.log('');
    console.log('Digite Ctrl+C para sair a qualquer momento');
    
    // Configurar input interativo
    setupInteractiveMode();
}

// Configurar modo interativo
function setupInteractiveMode() {
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    rl.on('line', async (input) => {
        switch (input.trim()) {
            case '1':
                console.log('\n🎯 Simulando nova ameaça...');
                const threats = [
                    'BRUTE_FORCE',
                    'SQL_INJECTION',
                    'XSS_ATTACK',
                    'DDOS_ATTACK',
                    'RANSOMWARE',
                    'PHISHING',
                    'INSIDER_THREAT'
                ];
                const randomThreat = threats[Math.floor(Math.random() * threats.length)];
                dade.simulateThreat(randomThreat);
                break;
                
            case '2':
                dade.printSystemStatus();
                break;
                
            case '3':
                const report = dade.getSystemReport();
                console.log('\n📋 RELATÓRIO COMPLETO:');
                console.log(JSON.stringify(report, null, 2));
                break;
                
            case '4':
                console.log('\n⚡ Iniciando teste de stress (10 ameaças simultâneas)...');
                for (let i = 0; i < 10; i++) {
                    dade.simulateThreat(`STRESS_TEST_${i}`);
                    await sleep(100);
                }
                break;
                
            case '5':
                console.log('\n👋 Encerrando sistema DADE...');
                await dade.shutdown();
                process.exit(0);
                break;
                
            default:
                console.log('Comando não reconhecido. Use 1-5.');
        }
    });
}

// Função auxiliar para sleep
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Função para formatar uptime
function formatUptime(ms) {
    if (!ms) return '0s';
    
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

// Capturar Ctrl+C para shutdown graceful
process.on('SIGINT', async () => {
    console.log('\n\n🛑 Interrupção detectada. Desligando sistema com segurança...');
    await dade.shutdown();
    process.exit(0);
});

// Inicializar o sistema
console.log('🚀 Inicializando Sistema DADE...\n');
dade.initialize().catch(error => {
    console.error('❌ Erro fatal:', error);
    process.exit(1);
});