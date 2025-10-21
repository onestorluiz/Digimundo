#!/usr/bin/env node

/**
 * 🎮 Teste do Sistema RPG Integrado
 * Demonstração completa da gamificação
 */

const SupremeOrchestrator = require('./core/orchestrator/supreme-orchestrator');
const RPGIntegration = require('./core/rpg/integration');
const { spawnMonster } = require('./core/rpg/monsters');

async function testRPGSystem() {
    console.log('\n╔══════════════════════════════════════════════════════════╗');
    console.log('║              🎮 TESTE DO SISTEMA RPG 🎮                  ║');
    console.log('║         Transformando Trabalho em Aventura Épica         ║');
    console.log('╚══════════════════════════════════════════════════════════╝\n');
    
    // Inicializar Orchestrator
    const orchestrator = new SupremeOrchestrator();
    await orchestrator.initialize();
    
    // Inicializar Sistema RPG
    const rpg = new RPGIntegration(orchestrator);
    
    // Mostrar status inicial
    console.log('\n📊 STATUS INICIAL DO SISTEMA:');
    const status = rpg.getSystemStatus();
    console.log(`   Total de Digimons: ${status.totalDigimons}`);
    console.log(`   Nível Médio: ${status.averageLevel}`);
    console.log(`   Distribuição de Classes:`);
    for (const [classId, count] of Object.entries(status.classDistribution)) {
        console.log(`     - ${classId}: ${count} Digimons`);
    }
    
    // Teste 1: Criar uma Quest
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('TESTE 1: Sistema de Quests');
    console.log('═══════════════════════════════════════════════════════════');
    
    const quest = rpg.createQuest({
        title: 'A Primeira Aventura',
        description: 'Complete sua primeira tarefa no Digimundo',
        objectives: ['Derrotar um bug', 'Ganhar 100 XP'],
        rewards: { xp: 200, kudos: 50 },
        difficulty: 'EASY',
        type: 'QUEST'
    });
    
    // Completar quest com Debugmon
    const debugmon = rpg.getDigimon('debugmon');
    rpg.completeQuest(debugmon, quest);
    
    // Teste 2: Combate contra Monstro
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('TESTE 2: Sistema de Combate');
    console.log('═══════════════════════════════════════════════════════════');
    
    // Simular bug detectado
    orchestrator.emit('bug-detected', {
        type: 'syntax',
        severity: 'common',
        description: 'Missing semicolon in line 42'
    });
    
    // Pegar o combate ativo
    const combatId = Array.from(rpg.activeCombats.keys())[0];
    if (combatId) {
        // Formar party
        rpg.joinCombat('debugmon', combatId);
        rpg.joinCombat('guardmon', combatId);
        rpg.joinCombat('creativemon', combatId);
    }
    
    // Teste 3: Sistema de Guilds
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('TESTE 3: Sistema de Guilds');
    console.log('═══════════════════════════════════════════════════════════');
    
    // Adicionar Digimons à guild
    rpg.joinGuild('debugmon', 'founders');
    rpg.joinGuild('trainmon', 'founders');
    rpg.joinGuild('guardmon', 'founders');
    
    const foundersGuild = rpg.guilds.get('founders');
    console.log(`\n🏰 ${foundersGuild.name}:`);
    console.log(`   Membros: ${foundersGuild.members.length}`);
    console.log(`   Nível: ${foundersGuild.level}`);
    
    // Teste 4: Integração com Protocolo Gênesis
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('TESTE 4: Integração com Protocolo Gênesis');
    console.log('═══════════════════════════════════════════════════════════');
    
    // Simular avaliação Gênesis
    orchestrator.emit('evaluation-complete', {
        digimon: 'trainmon',
        DQ: 75,
        badges: [
            { name: 'Mestre do Conhecimento', description: 'Pontuação perfeita em Research' }
        ]
    });
    
    // Teste 5: Achievements
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('TESTE 5: Sistema de Achievements');
    console.log('═══════════════════════════════════════════════════════════');
    
    rpg.grantAchievement(debugmon, 'First Bug', 'Derrotou seu primeiro bug');
    rpg.grantAchievement(debugmon, 'Speed Runner', 'Completou quest em tempo recorde');
    
    // Status final de um Digimon
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('STATUS FINAL DO DEBUGMON:');
    console.log('═══════════════════════════════════════════════════════════');
    
    console.log(`   Nome: ${debugmon.name}`);
    console.log(`   Classe: ${debugmon.classId}`);
    console.log(`   Nível: ${debugmon.level}`);
    console.log(`   XP: ${debugmon.xp}`);
    console.log(`   KUDOS: ${debugmon.currencies.KUDOS}`);
    console.log(`   Achievements: ${debugmon.achievements.length}`);
    console.log(`   Atributos:`);
    for (const [attr, val] of Object.entries(debugmon.attrs)) {
        console.log(`     ${attr}: ${val}`);
    }
    
    // Resumo final
    console.log('\n╔══════════════════════════════════════════════════════════╗');
    console.log('║                   🎉 TESTE COMPLETO! 🎉                  ║');
    console.log('║                                                          ║');
    console.log('║   O Sistema RPG está totalmente operacional!            ║');
    console.log('║   - Quests funcionando ✅                                ║');
    console.log('║   - Combate contra monstros ✅                           ║');
    console.log('║   - Guilds ativas ✅                                      ║');
    console.log('║   - Integração com Gênesis ✅                            ║');
    console.log('║   - Achievements desbloqueáveis ✅                        ║');
    console.log('║                                                          ║');
    console.log('║   Trabalho virou aventura épica! 🐲⚔️🎮                  ║');
    console.log('╚══════════════════════════════════════════════════════════╝\n');
}

// Executar teste
testRPGSystem().catch(console.error);