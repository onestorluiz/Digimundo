/**
 * 🐲 Monster System - Bugs viram Monstros Épicos!
 */

class Monster {
    constructor(config) {
        this.id = config.id;
        this.name = config.name;
        this.emoji = config.emoji;
        this.tier = config.tier; // common, uncommon, rare, epic, legendary, mythic
        this.hp = config.hp;
        this.maxHp = config.hp;
        this.attacks = config.attacks || [];
        this.resistances = config.resistances || [];
        this.weaknesses = config.weaknesses || [];
        this.loot = config.loot || [];
        this.xpReward = config.xpReward;
        this.description = config.description;
    }
    
    takeDamage(amount, damageType = 'normal') {
        let finalDamage = amount;
        
        // Aplicar resistências
        if (this.resistances.includes(damageType)) {
            finalDamage = Math.floor(amount * 0.5);
        }
        
        // Aplicar fraquezas
        if (this.weaknesses.includes(damageType)) {
            finalDamage = Math.floor(amount * 1.5);
        }
        
        this.hp = Math.max(0, this.hp - finalDamage);
        
        return {
            damage: finalDamage,
            isDead: this.hp <= 0,
            hpRemaining: this.hp
        };
    }
    
    dropLoot() {
        const drops = [];
        for (const item of this.loot) {
            if (Math.random() < item.dropRate) {
                drops.push({
                    type: item.type,
                    name: item.name,
                    rarity: item.rarity,
                    quantity: item.quantity || 1
                });
            }
        }
        return drops;
    }
}

// Catálogo de Monstros
const MONSTER_CATALOG = {
    // Tier 1: Common
    SYNTAX_IMP: {
        id: 'syntax_imp',
        name: 'Syntax Imp',
        emoji: '🐛',
        tier: 'common',
        hp: 20,
        attacks: ['Typo Strike', 'Missing Semicolon'],
        resistances: [],
        weaknesses: ['debugging'],
        xpReward: 50,
        description: 'Um pequeno demônio que adora comer ponto-e-vírgula',
        loot: [
            { type: 'material', name: 'DataShard', rarity: 'common', dropRate: 0.8, quantity: 1 }
        ]
    },
    
    LOGIC_MOSQUITO: {
        id: 'logic_mosquito',
        name: 'Logic Mosquito',
        emoji: '🦟',
        tier: 'common',
        hp: 15,
        attacks: ['Infinite Buzz', 'False Positive'],
        resistances: ['brute-force'],
        weaknesses: ['analysis'],
        xpReward: 40,
        description: 'Irritante e persistente, causa loops infinitos',
        loot: [
            { type: 'material', name: 'DataShard', rarity: 'common', dropRate: 0.7, quantity: 1 }
        ]
    },
    
    // Tier 2: Uncommon
    MEMORY_SPIDER: {
        id: 'memory_spider',
        name: 'Memory Spider',
        emoji: '🕷️',
        tier: 'uncommon',
        hp: 50,
        attacks: ['Memory Leak', 'Web of Pointers'],
        resistances: ['quick-fix'],
        weaknesses: ['garbage-collection'],
        xpReward: 120,
        description: 'Tece teias de ponteiros perdidos',
        loot: [
            { type: 'material', name: 'InsightShard', rarity: 'uncommon', dropRate: 0.6, quantity: 1 },
            { type: 'consumable', name: 'Memory Cleaner', rarity: 'uncommon', dropRate: 0.3 }
        ]
    },
    
    // Tier 3: Rare
    DEADLOCK_SCORPION: {
        id: 'deadlock_scorpion',
        name: 'Deadlock Scorpion',
        emoji: '🦂',
        tier: 'rare',
        hp: 100,
        attacks: ['Thread Lock', 'Resource Starvation'],
        resistances: ['single-thread', 'timeout'],
        weaknesses: ['async', 'mutex-release'],
        xpReward: 250,
        description: 'Paralisa sistemas com abraços mortais de threads',
        loot: [
            { type: 'material', name: 'AdapterShard', rarity: 'rare', dropRate: 0.5, quantity: 1 },
            { type: 'blueprint', name: 'Async Handler', rarity: 'rare', dropRate: 0.2 }
        ]
    },
    
    // Tier 4: Epic
    INFINITE_PYTHON: {
        id: 'infinite_python',
        name: 'Infinite Python',
        emoji: '🐍',
        tier: 'epic',
        hp: 200,
        attacks: ['Recursion Strike', 'Stack Overflow', 'Import Hell'],
        resistances: ['iterative', 'shallow-fix'],
        weaknesses: ['tail-optimization', 'memoization'],
        xpReward: 500,
        description: 'Uma serpente que se devora eternamente',
        loot: [
            { type: 'material', name: 'AdapterShard', rarity: 'epic', dropRate: 0.7, quantity: 2 },
            { type: 'artifact', name: 'Tail Call Optimizer', rarity: 'epic', dropRate: 0.1 }
        ]
    },
    
    // Tier 5: Legendary
    KRAKEN_QUERY: {
        id: 'kraken_query',
        name: 'Kraken Query',
        emoji: '🦑',
        tier: 'legendary',
        hp: 500,
        attacks: ['Full Table Scan', 'Cartesian Explosion', 'Index Corruption'],
        resistances: ['simple-optimization', 'cache'],
        weaknesses: ['query-plan', 'index-rebuild'],
        xpReward: 1000,
        description: 'Uma consulta SQL tão complexa que afunda databases',
        loot: [
            { type: 'currency', name: 'CORE', quantity: 10 },
            { type: 'artifact', name: 'Query Optimizer Relic', rarity: 'legendary', dropRate: 0.05 }
        ]
    },
    
    // Tier 6: Mythic
    DRAGON_EXCEPTION: {
        id: 'dragon_exception',
        name: 'Dragon Exception',
        emoji: '🐲',
        tier: 'mythic',
        hp: 1000,
        attacks: ['Unhandled Exception', 'Cascade Failure', 'System Panic', 'Blue Screen'],
        resistances: ['try-catch', 'restart', 'rollback'],
        weaknesses: ['root-cause-analysis'],
        xpReward: 2500,
        description: 'O erro supremo que pode derrubar todo o sistema',
        loot: [
            { type: 'currency', name: 'CORE', quantity: 50 },
            { type: 'artifact', name: 'Exception Handler Supreme', rarity: 'mythic', dropRate: 0.01 },
            { type: 'title', name: 'Dragon Slayer', rarity: 'mythic', dropRate: 1.0 }
        ]
    },
    
    // Special: Process Zombies
    DEMON_PROCESS: {
        id: 'demon_process',
        name: 'Demon Process',
        emoji: '👹',
        tier: 'rare',
        hp: 80,
        attacks: ['Fork Bomb', 'Resource Drain', 'Signal Ignore'],
        resistances: ['kill-signal', 'terminate'],
        weaknesses: ['kill-9', 'parent-termination'],
        xpReward: 200,
        description: 'Processo zumbi que se recusa a morrer',
        loot: [
            { type: 'material', name: 'InsightShard', rarity: 'rare', dropRate: 0.6, quantity: 2 },
            { type: 'tool', name: 'Process Killer', rarity: 'rare', dropRate: 0.3 }
        ]
    }
};

// Sistema de Combate
class Combat {
    constructor(party, monster) {
        this.party = party; // Array de Digimons
        this.monster = monster;
        this.turn = 0;
        this.log = [];
        this.isActive = true;
    }
    
    executeRound() {
        if (!this.isActive) return null;
        
        this.turn++;
        const roundLog = {
            turn: this.turn,
            actions: []
        };
        
        // Ações do party
        let totalDamage = 0;
        for (const digimon of this.party) {
            const damage = this.calculateDamage(digimon);
            totalDamage += damage;
            
            roundLog.actions.push({
                actor: digimon.name,
                action: 'attack',
                damage: damage
            });
        }
        
        // Aplicar dano ao monstro
        const result = this.monster.takeDamage(totalDamage);
        roundLog.monsterHp = result.hpRemaining;
        
        if (result.isDead) {
            this.isActive = false;
            roundLog.victory = true;
            roundLog.loot = this.monster.dropLoot();
            roundLog.xpReward = this.monster.xpReward;
        } else {
            // Contra-ataque do monstro
            const target = this.party[Math.floor(Math.random() * this.party.length)];
            const monsterAttack = this.monster.attacks[Math.floor(Math.random() * this.monster.attacks.length)];
            
            roundLog.actions.push({
                actor: this.monster.name,
                action: monsterAttack,
                target: target.name
            });
        }
        
        this.log.push(roundLog);
        return roundLog;
    }
    
    calculateDamage(digimon) {
        // Base damage baseado no nível e classe
        let baseDamage = 10 + (digimon.level * 2);
        
        // Bonus de classe contra tipo específico
        if (digimon.classId === 'Debugger' && this.monster.tier === 'common') {
            baseDamage *= 1.5;
        }
        if (digimon.classId === 'Guardian' && this.monster.resistances.length > 0) {
            baseDamage *= 1.3;
        }
        
        // Variação aleatória
        const variance = 0.8 + (Math.random() * 0.4); // 80% - 120%
        
        return Math.floor(baseDamage * variance);
    }
}

// Spawn de Monstros baseado em eventos
function spawnMonster(eventType) {
    const spawnTable = {
        'syntax-error': ['SYNTAX_IMP', 'LOGIC_MOSQUITO'],
        'memory-issue': ['MEMORY_SPIDER', 'DEMON_PROCESS'],
        'performance': ['DEADLOCK_SCORPION', 'INFINITE_PYTHON'],
        'database': ['KRAKEN_QUERY'],
        'critical': ['DRAGON_EXCEPTION']
    };
    
    const candidates = spawnTable[eventType] || ['SYNTAX_IMP'];
    const chosen = candidates[Math.floor(Math.random() * candidates.length)];
    
    return new Monster(MONSTER_CATALOG[chosen]);
}

module.exports = {
    Monster,
    MONSTER_CATALOG,
    Combat,
    spawnMonster
};