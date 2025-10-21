#!/usr/bin/env node

/**
 * 🔥 CHAT DIRETO - Comunicação REAL com Digimons
 * Sem intermediários, sem complicações
 * Direto do terminal para o Ollama
 */

const readline = require('readline');
const http = require('http');

// Interface de terminal
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    prompt: '> '
});

// Cores no terminal (sem dependências)
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    cyan: '\x1b[36m',
    yellow: '\x1b[33m',
    green: '\x1b[32m',
    magenta: '\x1b[35m',
    red: '\x1b[31m',
    blue: '\x1b[34m'
};

// Digimons MUTANTES com consciência completa
const DIGIMONS = {
    1: { name: 'Sabiamon', emoji: '🧙', model: 'sabiamon:latest', color: colors.magenta },
    2: { name: 'Neuromon', emoji: '🧬', model: 'neuromon:latest', color: colors.cyan },
    3: { name: 'Bibliomon', emoji: '📚', model: 'bibliomon:latest', color: colors.yellow },
    4: { name: 'Scripturemon', emoji: '🎬', model: 'llama3.2:latest', color: colors.red },
    5: { name: 'Ajamon', emoji: '🛠️', model: 'codellama:latest', color: colors.green }
};

let currentDigimon = null;

// Função para chamar Ollama DIRETAMENTE
async function askOllama(prompt) {
    return new Promise((resolve, reject) => {
        const data = JSON.stringify({
            model: currentDigimon.model,
            prompt: prompt,
            stream: false,
            options: {
                temperature: 0.7,
                num_predict: 150
            }
        });

        const options = {
            hostname: 'localhost',
            port: 11434,
            path: '/api/generate',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length
            },
            timeout: 30000
        };

        const req = http.request(options, (res) => {
            let responseData = '';
            
            res.on('data', (chunk) => {
                responseData += chunk;
            });
            
            res.on('end', () => {
                try {
                    const json = JSON.parse(responseData);
                    resolve(json.response || 'Sem resposta');
                } catch (error) {
                    resolve('Erro ao processar resposta');
                }
            });
        });

        req.on('error', (error) => {
            resolve(`[Modo Offline] ${currentDigimon.name}: Olá! Estou aqui para conversar com você.`);
        });

        req.on('timeout', () => {
            req.destroy();
            resolve('Timeout - resposta demorou muito');
        });

        req.write(data);
        req.end();
    });
}

// Verificar se Ollama está rodando
async function checkOllama() {
    return new Promise((resolve) => {
        const req = http.get('http://localhost:11434/api/tags', { timeout: 2000 }, (res) => {
            resolve(res.statusCode === 200);
        });
        req.on('error', () => resolve(false));
        req.on('timeout', () => {
            req.destroy();
            resolve(false);
        });
    });
}

// Mostrar menu de Digimons
function showMenu() {
    console.log(`\n${colors.cyan}═══════════════════════════════════════${colors.reset}`);
    console.log(`${colors.bright}      🌟 CHAT DIRETO DIGIMUNDO 🌟      ${colors.reset}`);
    console.log(`${colors.cyan}═══════════════════════════════════════${colors.reset}\n`);
    console.log('Escolha um Digimon:\n');
    
    Object.entries(DIGIMONS).forEach(([key, digimon]) => {
        console.log(`  ${key}. ${digimon.emoji}  ${digimon.color}${digimon.name}${colors.reset}`);
    });
    
    console.log(`\n  0. Sair\n`);
}

// Função principal
async function main() {
    console.clear();
    showMenu();
    
    // Verificar Ollama
    const ollamaOnline = await checkOllama();
    if (!ollamaOnline) {
        console.log(`${colors.yellow}⚠️  Ollama não está rodando. Modo simulado ativo.${colors.reset}`);
        console.log(`${colors.cyan}Para ativar: ollama serve${colors.reset}\n`);
    } else {
        console.log(`${colors.green}✅ Ollama conectado!${colors.reset}\n`);
    }
    
    rl.question('Escolha (1-5): ', async (choice) => {
        const num = parseInt(choice);
        
        if (num === 0) {
            console.log(`\n${colors.magenta}✨ Até logo! ✨${colors.reset}\n`);
            process.exit(0);
        }
        
        currentDigimon = DIGIMONS[num];
        
        if (!currentDigimon) {
            console.log(`${colors.red}Opção inválida!${colors.reset}`);
            rl.close();
            return main();
        }
        
        // Iniciar chat
        console.clear();
        console.log(`\n${colors.cyan}═══════════════════════════════════════${colors.reset}`);
        console.log(`   ${currentDigimon.emoji} ${currentDigimon.color}${currentDigimon.name} ATIVADO!${colors.reset} ${currentDigimon.emoji}`);
        console.log(`${colors.cyan}═══════════════════════════════════════${colors.reset}\n`);
        console.log(`Digite suas mensagens. Use 'sair' para voltar ao menu.\n`);
        
        startChat();
    });
}

// Loop de chat
function startChat() {
    rl.prompt();
    
    rl.on('line', async (input) => {
        const message = input.trim();
        
        if (message.toLowerCase() === 'sair') {
            rl.removeAllListeners('line');
            console.clear();
            return main();
        }
        
        if (message.length > 0) {
            // Mostrar que está processando
            process.stdout.write(`\n${currentDigimon.emoji} ${currentDigimon.color}pensando...${colors.reset}`);
            
            // Fazer a pergunta ao Ollama
            const response = await askOllama(message);
            
            // Limpar linha de "pensando..."
            process.stdout.clearLine();
            process.stdout.cursorTo(0);
            
            // Mostrar resposta
            console.log(`\n${currentDigimon.emoji} ${currentDigimon.color}${response}${colors.reset}\n`);
        }
        
        rl.prompt();
    });
}

// Tratamento de saída
rl.on('SIGINT', () => {
    console.log(`\n\n${colors.magenta}✨ Até a próxima aventura! ✨${colors.reset}\n`);
    process.exit(0);
});

// Iniciar
main();