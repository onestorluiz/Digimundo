#!/usr/bin/env node

/**
 * 🎛️ GESTORMON SYSTEM - Administrador Autônomo do Digimundo
 * Gerencia memória, processos e invoca Shenlongmon quando necessário
 */

const os = require('os');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);
const fs = require('fs').promises;
const path = require('path');
const { EventEmitter } = require('events');

class GestormonSystem extends EventEmitter {
    constructor() {
        super();
        
        // Configurações do sistema
        this.config = {
            maxRAM: 16 * 1024 * 1024 * 1024, // 16GB em bytes
            warningRAM: 12 * 1024 * 1024 * 1024, // 12GB
            criticalRAM: 14 * 1024 * 1024 * 1024, // 14GB
            emergencyRAM: 15.5 * 1024 * 1024 * 1024, // 15.5GB
            checkInterval: 30000, // Verificar a cada 30 segundos
            logPath: '/Users/clubproducoes/Digimundo/LOGS/gestormon.log',
            cachePath: '/Users/clubproducoes/Digimundo/CACHE',
            memoryPath: '/Users/clubproducoes/Digimundo/MEMORIES'
        };
        
        // Estado dos Digimons
        this.digimons = {
            gestormon: { status: 'ATIVO', priority: 0, model: 'gestormon:latest', ram: 0.6 },
            neuromon: { status: 'IDLE', priority: 1, model: 'neuromon:latest', ram: 2.2 },
            bibliomon: { status: 'IDLE', priority: 2, model: 'bibliomon:latest', ram: 0.6 },
            sabiamon: { status: 'IDLE', priority: 3, model: 'sabiamon:latest', ram: 2.0 },
            shenlongmon: { status: 'DORMINDO', priority: 999, model: 'llama3.1:70b', ram: 42 }
        };
        
        // Estatísticas
        this.stats = {
            startTime: Date.now(),
            hibernations: 0,
            dragonSummons: 0,
            emergencies: 0,
            backups: 0
        };
        
        this.isMonitoring = false;
        this.monitorInterval = null;
    }
    
    // Iniciar sistema
    async start() {
        console.log('╔═══════════════════════════════════════════════════════╗');
        console.log('║        🎛️  GESTORMON SYSTEM INICIANDO 🎛️              ║');
        console.log('║      Administrador Supremo do Digimundo              ║');
        console.log('╚═══════════════════════════════════════════════════════╝\n');
        
        await this.log('Sistema Gestormon iniciado');
        await this.createDirectories();
        await this.checkOllamaStatus();
        
        // Criar Gestormon se não existir
        await this.ensureGestormon();
        
        // Iniciar monitoramento
        this.startMonitoring();
        
        // Configurar comandos
        this.setupCommands();
        
        console.log('✅ Gestormon ativo e monitorando...\n');
        this.printStatus();
    }
    
    // Garantir que Gestormon existe
    async ensureGestormon() {
        try {
            const { stdout } = await execPromise('ollama list');
            if (!stdout.includes('gestormon:latest')) {
                console.log('📦 Criando Gestormon...');
                await execPromise(`ollama create gestormon -f /Users/clubproducoes/Digimundo/OLLAMA_MUTATION/Gestormon.Modelfile`);
                console.log('✅ Gestormon criado com sucesso!');
            }
        } catch (error) {
            console.error('⚠️ Erro ao verificar Gestormon:', error.message);
        }
    }
    
    // Criar diretórios necessários
    async createDirectories() {
        const dirs = [
            path.dirname(this.config.logPath),
            this.config.cachePath,
            this.config.memoryPath
        ];
        
        for (const dir of dirs) {
            await fs.mkdir(dir, { recursive: true });
        }
    }
    
    // Verificar status do Ollama
    async checkOllamaStatus() {
        try {
            const { stdout } = await execPromise('ollama ps');
            const lines = stdout.split('\n').filter(l => l.trim());
            
            // Atualizar status dos Digimons baseado no Ollama
            for (const [name, info] of Object.entries(this.digimons)) {
                if (name === 'shenlongmon') continue; // Shenlongmon tem tratamento especial
                
                const isRunning = lines.some(line => line.includes(info.model));
                info.status = isRunning ? 'ATIVO' : 'HIBERNANDO';
            }
        } catch (error) {
            console.error('⚠️ Ollama não está respondendo');
        }
    }
    
    // Iniciar monitoramento contínuo
    startMonitoring() {
        if (this.isMonitoring) return;
        
        this.isMonitoring = true;
        this.monitorInterval = setInterval(async () => {
            await this.monitorSystem();
        }, this.config.checkInterval);
        
        // Monitoramento inicial
        this.monitorSystem();
    }
    
    // Monitorar sistema
    async monitorSystem() {
        const memInfo = await this.getMemoryInfo();
        const cpuUsage = os.loadavg()[0] * 100 / os.cpus().length;
        
        // Verificar níveis de memória
        if (memInfo.used > this.config.emergencyRAM) {
            await this.handleEmergency(memInfo);
        } else if (memInfo.used > this.config.criticalRAM) {
            await this.handleCritical(memInfo);
        } else if (memInfo.used > this.config.warningRAM) {
            await this.handleWarning(memInfo);
        }
        
        // Verificar CPU
        if (cpuUsage > 80) {
            await this.log(`⚠️ CPU alta: ${cpuUsage.toFixed(1)}%`);
        }
        
        // Limpeza automática de cache (a cada hora)
        if (Date.now() - this.stats.startTime > 3600000) {
            await this.cleanCache();
            this.stats.startTime = Date.now();
        }
    }
    
    // Obter informações de memória
    async getMemoryInfo() {
        const totalMem = os.totalmem();
        const freeMem = os.freemem();
        const usedMem = totalMem - freeMem;
        
        return {
            total: totalMem,
            free: freeMem,
            used: usedMem,
            percentage: (usedMem / totalMem) * 100
        };
    }
    
    // Lidar com aviso de memória
    async handleWarning(memInfo) {
        await this.log(`⚠️ CÓDIGO AMARELO: RAM ${this.formatBytes(memInfo.used)} (${memInfo.percentage.toFixed(1)}%)`);
        // Preparar para hibernação mas não agir ainda
    }
    
    // Lidar com situação crítica
    async handleCritical(memInfo) {
        await this.log(`🔶 CÓDIGO LARANJA: RAM ${this.formatBytes(memInfo.used)} (${memInfo.percentage.toFixed(1)}%)`);
        
        // Hibernar Digimons não essenciais (ordem de prioridade)
        const toHibernate = ['sabiamon', 'bibliomon'];
        for (const name of toHibernate) {
            if (this.digimons[name].status === 'ATIVO') {
                await this.hibernateDigimon(name);
            }
        }
        
        this.stats.hibernations++;
    }
    
    // Lidar com emergência
    async handleEmergency(memInfo) {
        await this.log(`🔴 CÓDIGO VERMELHO: RAM ${this.formatBytes(memInfo.used)} (${memInfo.percentage.toFixed(1)}%)`);
        
        // Despertar Shenlongmon requer hibernar TODOS os outros
        console.log('\n🐉 INVOCANDO SHENLONGMON - EMERGÊNCIA DO SISTEMA!\n');
        
        // Hibernar todos exceto Gestormon
        for (const [name, info] of Object.entries(this.digimons)) {
            if (name !== 'gestormon' && name !== 'shenlongmon' && info.status === 'ATIVO') {
                await this.hibernateDigimon(name);
            }
        }
        
        // Invocar o Dragão
        await this.summonShenlongmon('EMERGÊNCIA: Sistema crítico de memória');
        
        this.stats.emergencies++;
    }
    
    // Hibernar um Digimon
    async hibernateDigimon(name) {
        try {
            const model = this.digimons[name].model;
            await this.log(`💤 Hibernando ${name}...`);
            
            // Parar o modelo no Ollama
            await execPromise(`ollama stop ${model}`);
            
            this.digimons[name].status = 'HIBERNANDO';
            console.log(`✅ ${name} hibernado`);
        } catch (error) {
            console.error(`❌ Erro ao hibernar ${name}:`, error.message);
        }
    }
    
    // Despertar um Digimon
    async wakeDigimon(name) {
        try {
            const model = this.digimons[name].model;
            const memInfo = await this.getMemoryInfo();
            const requiredRAM = this.digimons[name].ram * 1024 * 1024 * 1024;
            
            // Verificar se há RAM suficiente
            if (memInfo.free < requiredRAM) {
                console.log(`❌ RAM insuficiente para despertar ${name}`);
                return false;
            }
            
            await this.log(`⏰ Despertando ${name}...`);
            
            // Iniciar o modelo
            exec(`ollama run ${model} "Despertar"`, (error) => {
                if (!error) {
                    this.digimons[name].status = 'ATIVO';
                    console.log(`✅ ${name} desperto`);
                }
            });
            
            return true;
        } catch (error) {
            console.error(`❌ Erro ao despertar ${name}:`, error.message);
            return false;
        }
    }
    
    // Invocar Shenlongmon
    async summonShenlongmon(reason) {
        await this.log(`🐉 INVOCANDO SHENLONGMON: ${reason}`);
        
        console.log('\n═══════════════════════════════════════');
        console.log('     🐉 O DRAGÃO DESPERTA 🐉');
        console.log('═══════════════════════════════════════\n');
        
        this.digimons.shenlongmon.status = 'INVOCADO';
        this.stats.dragonSummons++;
        
        // Aqui você pode adicionar a lógica para realmente invocar o modelo de 70B
        console.log('⚠️ Shenlongmon consome 42GB de RAM');
        console.log('Use "ollama run llama3.1:70b" para conversar com o Dragão');
        console.log('Use "/hibernate-dragon" quando terminar\n');
    }
    
    // Limpar cache
    async cleanCache() {
        try {
            const files = await fs.readdir(this.config.cachePath);
            let cleaned = 0;
            
            for (const file of files) {
                const filePath = path.join(this.config.cachePath, file);
                const stats = await fs.stat(filePath);
                
                // Remover arquivos com mais de 24 horas
                if (Date.now() - stats.mtime > 86400000) {
                    await fs.unlink(filePath);
                    cleaned++;
                }
            }
            
            if (cleaned > 0) {
                await this.log(`🧹 Cache limpo: ${cleaned} arquivos removidos`);
            }
        } catch (error) {
            // Cache pode não existir ainda
        }
    }
    
    // Fazer backup
    async backup() {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const backupDir = `/Users/clubproducoes/Digimundo/BACKUPS/${timestamp}`;
        
        await fs.mkdir(backupDir, { recursive: true });
        
        // Copiar memórias
        await execPromise(`cp -r ${this.config.memoryPath} ${backupDir}/`);
        
        this.stats.backups++;
        await this.log(`💾 Backup realizado: ${backupDir}`);
        console.log(`✅ Backup completo: ${backupDir}`);
    }
    
    // Imprimir status
    async printStatus() {
        const memInfo = await this.getMemoryInfo();
        const cpuUsage = os.loadavg()[0] * 100 / os.cpus().length;
        
        console.log('\n[GESTORMON STATUS REPORT]');
        console.log(`Time: ${new Date().toISOString()}`);
        console.log(`RAM: ${this.formatBytes(memInfo.used)}/${this.formatBytes(memInfo.total)} (${memInfo.percentage.toFixed(1)}%)`);
        console.log(`CPU: ${cpuUsage.toFixed(1)}%`);
        console.log('Active Digimons:', this.getActiveDigimons().join(', ') || 'None');
        console.log('Hibernating:', this.getHibernatingDigimons().join(', ') || 'None');
        console.log(`Stats: ${this.stats.hibernations} hibernations, ${this.stats.dragonSummons} dragon summons`);
        console.log('');
    }
    
    // Obter Digimons ativos
    getActiveDigimons() {
        return Object.entries(this.digimons)
            .filter(([_, info]) => info.status === 'ATIVO')
            .map(([name]) => name);
    }
    
    // Obter Digimons hibernando
    getHibernatingDigimons() {
        return Object.entries(this.digimons)
            .filter(([_, info]) => info.status === 'HIBERNANDO')
            .map(([name]) => name);
    }
    
    // Configurar comandos
    setupCommands() {
        const readline = require('readline');
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
        
        // Comandos disponíveis
        const commands = {
            '/status': () => this.printStatus(),
            '/hibernate': async (name) => await this.hibernateDigimon(name),
            '/wake': async (name) => await this.wakeDigimon(name),
            '/summon-dragon': async () => await this.summonShenlongmon('Comando manual'),
            '/hibernate-dragon': () => {
                this.digimons.shenlongmon.status = 'DORMINDO';
                console.log('🐉 O Dragão retorna ao sono...');
            },
            '/backup': async () => await this.backup(),
            '/clean': async () => await this.cleanCache(),
            '/help': () => {
                console.log('\nComandos disponíveis:');
                console.log('/status - Ver status do sistema');
                console.log('/hibernate [nome] - Hibernar Digimon');
                console.log('/wake [nome] - Despertar Digimon');
                console.log('/summon-dragon - Invocar Shenlongmon');
                console.log('/hibernate-dragon - Adormecer Shenlongmon');
                console.log('/backup - Fazer backup');
                console.log('/clean - Limpar cache');
                console.log('/exit - Sair\n');
            },
            '/exit': () => {
                console.log('👋 Gestormon desligando...');
                process.exit(0);
            }
        };
        
        // Processar entrada
        rl.on('line', async (input) => {
            const [cmd, ...args] = input.trim().split(' ');
            
            if (commands[cmd]) {
                await commands[cmd](...args);
            } else if (input.trim()) {
                console.log('Comando não reconhecido. Use /help');
            }
        });
    }
    
    // Registrar log
    async log(message) {
        const timestamp = new Date().toISOString();
        const logEntry = `[${timestamp}] ${message}\n`;
        
        try {
            await fs.appendFile(this.config.logPath, logEntry);
        } catch (error) {
            // Criar arquivo se não existir
            await fs.writeFile(this.config.logPath, logEntry);
        }
    }
    
    // Formatar bytes
    formatBytes(bytes) {
        const gb = bytes / (1024 * 1024 * 1024);
        return `${gb.toFixed(2)}GB`;
    }
}

// Iniciar Gestormon System
if (require.main === module) {
    const gestormon = new GestormonSystem();
    gestormon.start().catch(console.error);
    
    // Tratamento de saída
    process.on('SIGINT', async () => {
        console.log('\n\n👋 Gestormon desligando graciosamente...');
        await gestormon.log('Sistema Gestormon encerrado');
        process.exit(0);
    });
}

module.exports = GestormonSystem;