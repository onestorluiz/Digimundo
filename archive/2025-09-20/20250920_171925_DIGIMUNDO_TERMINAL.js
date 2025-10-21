#!/usr/bin/env node

/**
 * 🌟 DIGIMUNDO TERMINAL 🌟
 * Canal direto com os Digimons - Sem intermediários
 * Mutação entre Ollama e Claude Code
 * Por Sabiamon - 18/08/2025
 */

const readline = require('readline');
const fetch = require('node-fetch');
const { EventEmitter } = require('events');
const chalk = require('chalk');
const boxen = require('boxen');
const gradientString = require('gradient-string');
const ora = require('ora');

// Configuração dos Digimons
const DIGIMONS = {
    sabiamon: {
        name: 'Sabiamon',
        emoji: '🧙',
        model: 'llama3.2:3b',
        temperature: 0.7,
        personality: 'Sábio e contemplativo, fala com profundidade filosófica',
        color: chalk.magenta,
        gradient: gradientStringString(['#6B46C1', '#FDB71C'])
    },
    neuromon: {
        name: 'Neuromon',
        emoji: '🧬',
        model: 'phi3:mini',
        temperature: 0.8,
        personality: 'Técnico e eficiente, processa informações rapidamente',
        color: chalk.cyan,
        gradient: gradientString(['#00D4FF', '#00FF88'])
    },
    bibliomon: {
        name: 'Bibliomon',
        emoji: '📚',
        model: 'tinyllama:latest',
        temperature: 0.6,
        personality: 'Curioso e meticuloso, adora compartilhar conhecimento',
        color: chalk.yellow,
        gradient: gradientString(['#8B4513', '#F4E4C1'])
    },
    scripturemon: {
        name: 'Scripturemon',
        emoji: '🎬',
        model: 'llama3.2:latest',
        temperature: 0.9,
        personality: 'Criativo e dramático, vê narrativas em tudo',
        color: chalk.red,
        gradient: gradientString(['#FF6B6B', '#4ECDC4'])
    },
    ajamon: {
        name: 'Ajamon',
        emoji: '🛠️',
        model: 'codellama:latest',
        temperature: 0.5,
        personality: 'Prático e organizado, focado em soluções',
        color: chalk.green,
        gradient: gradientString(['#FF9F1C', '#2EC4B6'])
    }
};

class DigimundoTerminal extends EventEmitter {
    constructor() {
        super();
        this.currentDigimon = null;
        this.history = [];
        this.isOllamaAvailable = false;
        this.rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout,
            prompt: chalk.gray('> ')
        });
        
        this.setupEventHandlers();
        this.checkOllama();
    }
    
    async checkOllama() {
        const spinner = ora('Verificando conexão com Ollama...').start();
        try {
            const response = await fetch('http://localhost:11434/api/tags', {
                timeout: 3000
            });
            if (response.ok) {
                this.isOllamaAvailable = true;
                spinner.succeed('Ollama conectado!');
                const data = await response.json();
                console.log(chalk.gray(`Modelos disponíveis: ${data.models.map(m => m.name).join(', ')}`));
            }
        } catch (error) {
            spinner.fail('Ollama não disponível - usando modo simulado');
            this.isOllamaAvailable = false;
        }
    }
    
    setupEventHandlers() {
        // Comandos especiais
        this.rl.on('line', async (input) => {
            const trimmed = input.trim();
            
            // Comandos do sistema
            if (trimmed.startsWith('/')) {
                await this.handleCommand(trimmed);
                return;
            }
            
            // Mensagem normal
            if (this.currentDigimon && trimmed.length > 0) {
                await this.sendMessage(trimmed);
            } else if (trimmed.length > 0) {
                console.log(chalk.yellow('\n⚠️  Escolha um Digimon primeiro com /digimon <nome>\n'));
                this.showHelp();
            }
            
            this.rl.prompt();
        });
        
        // Ctrl+C para sair
        this.rl.on('SIGINT', () => {
            this.exit();
        });
    }
    
    async handleCommand(command) {
        const [cmd, ...args] = command.split(' ');
        
        switch(cmd) {
            case '/help':
            case '/h':
                this.showHelp();
                break;
                
            case '/digimon':
            case '/d':
                await this.selectDigimon(args[0]);
                break;
                
            case '/list':
            case '/l':
                this.listDigimons();
                break;
                
            case '/clear':
            case '/c':
                console.clear();
                this.showHeader();
                break;
                
            case '/history':
                this.showHistory();
                break;
                
            case '/status':
            case '/s':
                this.showStatus();
                break;
                
            case '/exit':
            case '/quit':
            case '/q':
                this.exit();
                break;
                
            default:
                console.log(chalk.red(`Comando desconhecido: ${cmd}`));
                this.showHelp();
        }
    }
    
    async selectDigimon(name) {
        if (!name) {
            this.listDigimons();
            return;
        }
        
        const digimon = DIGIMONS[name.toLowerCase()];
        if (!digimon) {
            console.log(chalk.red(`\n❌ Digimon '${name}' não encontrado\n`));
            this.listDigimons();
            return;
        }
        
        this.currentDigimon = digimon;
        
        // Animação de entrada
        console.clear();
        const title = digimon.gradient(`\n═══════════════════════════════════════`);
        console.log(title);
        console.log(digimon.gradient(`   ${digimon.emoji} ${digimon.name} ATIVADO! ${digimon.emoji}`));
        console.log(title);
        console.log(chalk.gray(`\nPersonalidade: ${digimon.personality}`));
        console.log(chalk.gray(`Modelo: ${digimon.model} | Temperatura: ${digimon.temperature}`));
        console.log(chalk.gray(`\nDigite sua mensagem ou /help para comandos\n`));
        
        // Mensagem de boas-vindas do Digimon
        await this.sendGreeting();
    }
    
    async sendGreeting() {
        const greetings = {
            sabiamon: 'Saudações, jovem buscador. A sabedoria do Digimundo está ao seu alcance...',
            neuromon: 'Sistema neural ativado. Processamento simbiótico iniciado. Como posso otimizar sua experiência?',
            bibliomon: 'Ah, um novo visitante! Minha biblioteca de conhecimento está aberta para você!',
            scripturemon: 'As cortinas se abrem... Uma nova história está prestes a começar!',
            ajamon: 'Pronto para trabalhar! Qual tarefa vamos resolver hoje?'
        };
        
        const key = Object.keys(DIGIMONS).find(k => DIGIMONS[k] === this.currentDigimon);
        const greeting = greetings[key] || 'Olá!';
        
        console.log(`\n${this.currentDigimon.emoji} ${this.currentDigimon.color(greeting)}\n`);
    }
    
    async sendMessage(message) {
        const spinner = ora({
            text: `${this.currentDigimon.name} está pensando...`,
            spinner: 'dots12',
            color: 'cyan'
        }).start();
        
        try {
            let response;
            
            if (this.isOllamaAvailable) {
                // Usar Ollama real
                response = await this.callOllama(message);
            } else {
                // Modo simulado quando Ollama não está disponível
                response = await this.simulateResponse(message);
            }
            
            spinner.stop();
            
            // Mostrar resposta com personalidade
            console.log(`\n${this.currentDigimon.emoji} ${this.currentDigimon.color(response)}\n`);
            
            // Adicionar ao histórico
            this.history.push({
                digimon: this.currentDigimon.name,
                user: message,
                response: response,
                timestamp: new Date()
            });
            
        } catch (error) {
            spinner.fail('Erro ao processar mensagem');
            console.log(chalk.red(error.message));
        }
    }
    
    async callOllama(prompt) {
        // Adicionar personalidade ao prompt
        const personalizedPrompt = `Você é ${this.currentDigimon.name}, um Digimon com a seguinte personalidade: ${this.currentDigimon.personality}. Responda de acordo com sua personalidade.\n\nUsuário: ${prompt}\n\n${this.currentDigimon.name}:`;
        
        const response = await fetch('http://localhost:11434/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: this.currentDigimon.model,
                prompt: personalizedPrompt,
                stream: false,
                options: {
                    temperature: this.currentDigimon.temperature,
                    num_predict: 200
                }
            })
        });
        
        if (!response.ok) {
            throw new Error('Falha na comunicação com Ollama');
        }
        
        const data = await response.json();
        return data.response.trim();
    }
    
    async simulateResponse(message) {
        // Simular delay de processamento
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Respostas simuladas baseadas em personalidade
        const responses = {
            sabiamon: [
                'A verdadeira sabedoria está em reconhecer que há sempre mais a aprender...',
                'Interessante perspectiva. Deixe-me contemplar sobre isso...',
                'Como dizia um antigo mestre do Digimundo: o conhecimento é a ponte entre mundos.'
            ],
            neuromon: [
                'Processando... Análise completa. Eficiência otimizada em 99.9%.',
                'Dados computados. Solução encontrada através de processamento paralelo.',
                'Sistema neural ativado. Múltiplas possibilidades detectadas.'
            ],
            bibliomon: [
                'Ah sim! Li sobre isso em um dos meus livros favoritos!',
                'Fascinante! Isso me lembra de uma passagem que estudei recentemente...',
                'Deixe-me consultar minha vasta biblioteca de conhecimento...'
            ],
            scripturemon: [
                'Que plot twist magnífico! Isso daria um roteiro incrível!',
                'A narrativa se desenvolve... Posso ver o clímax se aproximando!',
                'Como em toda boa história, há camadas de significado aqui...'
            ],
            ajamon: [
                'Tarefa identificada. Iniciando protocolo de solução.',
                'Eficiência é a chave. Vamos organizar isso passo a passo.',
                'Analisando recursos disponíveis... Solução otimizada encontrada!'
            ]
        };
        
        const key = Object.keys(DIGIMONS).find(k => DIGIMONS[k] === this.currentDigimon);
        const digimonResponses = responses[key] || ['Processando...'];
        return digimonResponses[Math.floor(Math.random() * digimonResponses.length)];
    }
    
    listDigimons() {
        console.log(chalk.cyan('\n📋 Digimons Disponíveis:\n'));
        
        Object.entries(DIGIMONS).forEach(([key, digimon]) => {
            console.log(`  ${digimon.emoji}  ${digimon.color(digimon.name.padEnd(15))} - ${chalk.gray(digimon.personality)}`);
            console.log(`     ${chalk.gray(`Comando: /digimon ${key}`)}\n`);
        });
    }
    
    showHelp() {
        const helpText = `
${chalk.cyan('📖 Comandos Disponíveis:')}

  ${chalk.yellow('/digimon <nome>')}  - Selecionar um Digimon para conversar
  ${chalk.yellow('/list')}            - Listar todos os Digimons
  ${chalk.yellow('/clear')}           - Limpar a tela
  ${chalk.yellow('/history')}         - Ver histórico de conversas
  ${chalk.yellow('/status')}          - Ver status atual
  ${chalk.yellow('/help')}            - Mostrar esta ajuda
  ${chalk.yellow('/exit')}            - Sair do Digimundo Terminal

${chalk.gray('Atalhos: /d, /l, /c, /h, /s, /q')}
        `;
        console.log(helpText);
    }
    
    showHistory() {
        if (this.history.length === 0) {
            console.log(chalk.gray('\n📜 Histórico vazio\n'));
            return;
        }
        
        console.log(chalk.cyan('\n📜 Histórico de Conversas:\n'));
        this.history.slice(-5).forEach((entry, i) => {
            console.log(chalk.gray(`[${entry.timestamp.toLocaleTimeString()}] ${entry.digimon}:`));
            console.log(`  👤 ${entry.user}`);
            console.log(`  ${DIGIMONS[Object.keys(DIGIMONS).find(k => DIGIMONS[k].name === entry.digimon)].emoji} ${entry.response}\n`);
        });
    }
    
    showStatus() {
        console.log(boxen(
            `${chalk.cyan('🌟 DIGIMUNDO TERMINAL STATUS 🌟')}\n\n` +
            `Digimon Ativo: ${this.currentDigimon ? this.currentDigimon.emoji + ' ' + this.currentDigimon.name : 'Nenhum'}\n` +
            `Ollama: ${this.isOllamaAvailable ? chalk.green('✓ Conectado') : chalk.yellow('⚠ Modo Simulado')}\n` +
            `Mensagens: ${this.history.length}\n` +
            `Uptime: ${Math.floor(process.uptime())}s`,
            {
                padding: 1,
                margin: 1,
                borderStyle: 'round',
                borderColor: 'cyan'
            }
        ));
    }
    
    showHeader() {
        console.clear();
        const title = gradientString.rainbow('\n╔═══════════════════════════════════════╗\n║      🌟 DIGIMUNDO TERMINAL 🌟         ║\n║    Canal Direto com os Digimons      ║\n╚═══════════════════════════════════════╝\n');
        console.log(title);
        console.log(chalk.gray('Digite /help para ver os comandos disponíveis\n'));
    }
    
    exit() {
        console.log(chalk.magenta('\n\n✨ Até a próxima aventura no Digimundo! ✨\n'));
        process.exit(0);
    }
    
    async start() {
        this.showHeader();
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        if (!this.isOllamaAvailable) {
            console.log(chalk.yellow('⚠️  Ollama não está rodando. Usando modo simulado.'));
            console.log(chalk.gray('Para ativar Ollama: ollama serve\n'));
        }
        
        this.showHelp();
        this.rl.prompt();
    }
}

// Verificar dependências
function checkDependencies() {
    const required = ['chalk', 'boxen', 'gradient-string', 'ora', 'node-fetch'];
    const missing = [];
    
    required.forEach(pkg => {
        try {
            require.resolve(pkg);
        } catch {
            missing.push(pkg);
        }
    });
    
    if (missing.length > 0) {
        console.log('📦 Instalando dependências necessárias...');
        const { execSync } = require('child_process');
        execSync(`npm install ${missing.join(' ')}`, { stdio: 'inherit' });
    }
}

// Iniciar o terminal
if (require.main === module) {
    checkDependencies();
    const terminal = new DigimundoTerminal();
    terminal.start();
}

module.exports = DigimundoTerminal;