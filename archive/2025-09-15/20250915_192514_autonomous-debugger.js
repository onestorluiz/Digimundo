#!/usr/bin/env node

/**
 * 🐛 DEBUGMON - DIGIMON AUTÔNOMO DE DEBUGGING
 * Sistema inteligente de detecção e correção de erros
 * Usa IA real para análise e correção automática
 */

const { spawn, exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const path = require('path');
const { EventEmitter } = require('events');
const execAsync = promisify(exec);

class Debugmon extends EventEmitter {
    constructor() {
        super();
        this.name = 'Debugmon';
        this.emoji = '🐛';
        this.model = 'qwen2.5-coder:7b'; // Melhor modelo para debugging
        this.personality = `You are DEBUGMON, an expert debugging AI Digimon. Your mission is to:
1. Analyze code and find bugs automatically
2. Understand error messages and stack traces
3. Provide exact fixes with code
4. Learn from patterns to prevent future errors
5. Think step-by-step through problems

You are extremely intelligent and can predict potential errors before they happen.
Always provide the EXACT code fix, not just explanations.`;
        
        this.errorPatterns = new Map();
        this.learnedFixes = new Map();
        this.autoFixEnabled = true;
        this.watchedFiles = new Set();
        this.errorHistory = [];
        this.successfulFixes = 0;
        this.totalErrors = 0;
        
        this.initialize();
    }
    
    async initialize() {
        console.log(`
╔═══════════════════════════════════════════════════════════════╗
║              🐛 DEBUGMON AWAKENING... 🐛                     ║
║         Autonomous Debugging System Activated                  ║
╚═══════════════════════════════════════════════════════════════╝
        `);
        
        // Verificar se o modelo está instalado
        await this.ensureModelInstalled();
        
        // Iniciar monitoramento de erros
        this.startErrorMonitoring();
        
        // Carregar padrões de erro conhecidos
        await this.loadErrorPatterns();
        
        console.log(`
${this.emoji} Debugmon Online!
   Model: ${this.model}
   Auto-fix: ${this.autoFixEnabled ? 'ENABLED' : 'DISABLED'}
   Intelligence: MAXIMUM
   
Ready to debug anything! 🔍
        `);
    }
    
    /**
     * Garantir que o modelo está instalado
     */
    async ensureModelInstalled() {
        try {
            const { stdout } = await execAsync('ollama list');
            if (!stdout.includes('qwen2.5-coder')) {
                console.log('📦 Installing Qwen 2.5 Coder model...');
                await execAsync('ollama pull qwen2.5-coder:7b');
                console.log('✅ Model installed!');
            }
        } catch (error) {
            console.warn('⚠️  Could not verify model, trying alternative...');
            this.model = 'codellama:7b'; // Fallback
        }
    }
    
    /**
     * Analisar erro com IA
     */
    async analyzeError(error, context = {}) {
        this.totalErrors++;
        console.log(`\n${this.emoji} Debugmon analyzing error #${this.totalErrors}...`);
        
        // Construir prompt inteligente
        const prompt = this.buildDebugPrompt(error, context);
        
        try {
            // Chamar Ollama para análise
            const analysis = await this.callOllama(prompt);
            
            // Extrair solução
            const solution = this.extractSolution(analysis);
            
            // Aprender com o padrão
            this.learnFromError(error, solution);
            
            return {
                error: error.message || error,
                analysis,
                solution,
                confidence: this.calculateConfidence(solution),
                autoFixable: solution.code ? true : false
            };
        } catch (aiError) {
            console.error('❌ AI analysis failed:', aiError.message);
            return this.fallbackAnalysis(error);
        }
    }
    
    /**
     * Construir prompt de debugging inteligente
     */
    buildDebugPrompt(error, context) {
        let prompt = `${this.personality}\n\n`;
        
        prompt += `ERROR DETECTED:\n`;
        prompt += `Message: ${error.message || error}\n`;
        
        if (error.stack) {
            prompt += `\nStack Trace:\n${error.stack}\n`;
        }
        
        if (context.file) {
            prompt += `\nFile: ${context.file}\n`;
            if (context.line) {
                prompt += `Line: ${context.line}\n`;
            }
            if (context.code) {
                prompt += `\nCode Context:\n\`\`\`javascript\n${context.code}\n\`\`\`\n`;
            }
        }
        
        // Adicionar histórico de erros similares
        const similarErrors = this.findSimilarErrors(error);
        if (similarErrors.length > 0) {
            prompt += `\nSimilar errors fixed before:\n`;
            similarErrors.forEach(e => {
                prompt += `- ${e.error}: ${e.fix}\n`;
            });
        }
        
        prompt += `\nProvide:
1. Root cause analysis
2. EXACT code fix (if applicable)
3. Prevention strategy
4. Potential side effects

Format your response as:
CAUSE: [explanation]
FIX: [exact code]
PREVENT: [strategy]
RISKS: [potential issues]`;
        
        return prompt;
    }
    
    /**
     * Chamar Ollama para análise
     */
    async callOllama(prompt) {
        return new Promise((resolve, reject) => {
            const response = [];
            
            const ollama = spawn('ollama', ['run', this.model], {
                stdio: ['pipe', 'pipe', 'pipe']
            });
            
            ollama.stdout.on('data', (data) => {
                response.push(data.toString());
            });
            
            ollama.on('close', () => {
                resolve(response.join(''));
            });
            
            ollama.on('error', reject);
            
            // Enviar prompt
            ollama.stdin.write(prompt + '\n');
            ollama.stdin.end();
        });
    }
    
    /**
     * Extrair solução da resposta da IA
     */
    extractSolution(analysis) {
        const solution = {
            cause: '',
            code: null,
            prevention: '',
            risks: []
        };
        
        // Parse da resposta estruturada
        const lines = analysis.split('\n');
        let currentSection = null;
        let codeBuffer = [];
        let inCodeBlock = false;
        
        for (const line of lines) {
            if (line.startsWith('CAUSE:')) {
                currentSection = 'cause';
                solution.cause = line.substring(6).trim();
            } else if (line.startsWith('FIX:')) {
                currentSection = 'fix';
            } else if (line.startsWith('PREVENT:')) {
                currentSection = 'prevention';
                solution.prevention = line.substring(8).trim();
            } else if (line.startsWith('RISKS:')) {
                currentSection = 'risks';
                const risks = line.substring(6).trim();
                if (risks) solution.risks.push(risks);
            } else if (line.includes('```')) {
                inCodeBlock = !inCodeBlock;
                if (!inCodeBlock && codeBuffer.length > 0) {
                    solution.code = codeBuffer.join('\n');
                    codeBuffer = [];
                }
            } else if (inCodeBlock) {
                codeBuffer.push(line);
            } else if (currentSection) {
                // Adicionar ao campo atual
                switch (currentSection) {
                    case 'cause':
                        solution.cause += ' ' + line.trim();
                        break;
                    case 'prevention':
                        solution.prevention += ' ' + line.trim();
                        break;
                    case 'risks':
                        if (line.trim()) solution.risks.push(line.trim());
                        break;
                }
            }
        }
        
        return solution;
    }
    
    /**
     * Aplicar correção automaticamente
     */
    async autoFix(errorInfo, filePath) {
        if (!this.autoFixEnabled || !errorInfo.solution.code) {
            console.log('⚠️  Auto-fix not available for this error');
            return false;
        }
        
        console.log(`\n${this.emoji} Applying auto-fix...`);
        
        try {
            // Backup do arquivo original
            const backupPath = filePath + '.debugmon-backup';
            const originalContent = await fs.readFile(filePath, 'utf8');
            await fs.writeFile(backupPath, originalContent);
            
            // Aplicar fix
            if (errorInfo.solution.code.includes('REPLACE:')) {
                // Fix de substituição
                const [oldCode, newCode] = errorInfo.solution.code.split('WITH:');
                const fixed = originalContent.replace(
                    oldCode.replace('REPLACE:', '').trim(),
                    newCode.trim()
                );
                await fs.writeFile(filePath, fixed);
            } else {
                // Fix completo
                await fs.writeFile(filePath, errorInfo.solution.code);
            }
            
            console.log(`✅ Fix applied successfully!`);
            console.log(`   Backup saved at: ${backupPath}`);
            
            this.successfulFixes++;
            
            // Testar se o fix funcionou
            const testResult = await this.testFix(filePath);
            if (!testResult.success) {
                console.log('⚠️  Fix didn\'t work, reverting...');
                await fs.writeFile(filePath, originalContent);
                return false;
            }
            
            return true;
        } catch (error) {
            console.error('❌ Auto-fix failed:', error.message);
            return false;
        }
    }
    
    /**
     * Testar se o fix funcionou
     */
    async testFix(filePath) {
        try {
            // Tentar executar o arquivo
            const { stderr } = await execAsync(`node --check ${filePath}`);
            return { success: !stderr, error: stderr };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
    
    /**
     * Aprender com erros
     */
    learnFromError(error, solution) {
        const errorSignature = this.getErrorSignature(error);
        
        if (!this.errorPatterns.has(errorSignature)) {
            this.errorPatterns.set(errorSignature, []);
        }
        
        this.errorPatterns.get(errorSignature).push({
            timestamp: Date.now(),
            solution,
            success: solution.code ? true : false
        });
        
        // Salvar aprendizado
        this.saveKnowledge();
    }
    
    /**
     * Encontrar erros similares
     */
    findSimilarErrors(error) {
        const signature = this.getErrorSignature(error);
        const similar = [];
        
        for (const [sig, patterns] of this.errorPatterns) {
            if (this.calculateSimilarity(signature, sig) > 0.7) {
                const lastSuccess = patterns.filter(p => p.success).pop();
                if (lastSuccess) {
                    similar.push({
                        error: sig,
                        fix: lastSuccess.solution.code || lastSuccess.solution.cause
                    });
                }
            }
        }
        
        return similar.slice(0, 3); // Top 3 mais similares
    }
    
    /**
     * Calcular similaridade entre erros
     */
    calculateSimilarity(sig1, sig2) {
        const words1 = sig1.toLowerCase().split(/\s+/);
        const words2 = sig2.toLowerCase().split(/\s+/);
        const intersection = words1.filter(w => words2.includes(w));
        return intersection.length / Math.max(words1.length, words2.length);
    }
    
    /**
     * Gerar assinatura de erro
     */
    getErrorSignature(error) {
        const message = error.message || error.toString();
        // Remover números e caminhos específicos para generalizar
        return message
            .replace(/\/[^\s]+/g, '[PATH]')
            .replace(/\d+/g, '[NUM]')
            .replace(/0x[0-9a-f]+/gi, '[HEX]');
    }
    
    /**
     * Calcular confiança na solução
     */
    calculateConfidence(solution) {
        let confidence = 0;
        
        if (solution.cause) confidence += 30;
        if (solution.code) confidence += 40;
        if (solution.prevention) confidence += 20;
        if (solution.risks.length > 0) confidence += 10;
        
        return Math.min(confidence, 100);
    }
    
    /**
     * Análise fallback quando IA falha
     */
    fallbackAnalysis(error) {
        const message = error.message || error.toString();
        
        // Padrões conhecidos
        const knownPatterns = {
            'Cannot find module': {
                cause: 'Missing dependency',
                solution: { 
                    code: `npm install [module-name]`,
                    prevention: 'Check package.json dependencies'
                }
            },
            'SyntaxError': {
                cause: 'Syntax error in code',
                solution: {
                    prevention: 'Use a linter like ESLint'
                }
            },
            'TypeError': {
                cause: 'Type mismatch or undefined value',
                solution: {
                    prevention: 'Add type checking and null checks'
                }
            }
        };
        
        for (const [pattern, fix] of Object.entries(knownPatterns)) {
            if (message.includes(pattern)) {
                return {
                    error: message,
                    analysis: `Known pattern: ${pattern}`,
                    solution: fix.solution,
                    confidence: 60,
                    autoFixable: false
                };
            }
        }
        
        return {
            error: message,
            analysis: 'Unknown error pattern',
            solution: {},
            confidence: 0,
            autoFixable: false
        };
    }
    
    /**
     * Monitorar erros do sistema
     */
    startErrorMonitoring() {
        // Interceptar erros globais
        process.on('uncaughtException', async (error) => {
            console.error(`\n🚨 Uncaught Exception detected!`);
            const analysis = await this.analyzeError(error, {
                type: 'uncaughtException'
            });
            this.emit('error-analyzed', analysis);
        });
        
        process.on('unhandledRejection', async (reason) => {
            console.error(`\n🚨 Unhandled Rejection detected!`);
            const analysis = await this.analyzeError(reason, {
                type: 'unhandledRejection'
            });
            this.emit('error-analyzed', analysis);
        });
        
        // Monitorar logs de erro
        const originalError = console.error;
        console.error = (...args) => {
            originalError.apply(console, args);
            this.handleConsoleError(args);
        };
    }
    
    /**
     * Lidar com erros do console
     */
    async handleConsoleError(args) {
        const errorStr = args.map(a => String(a)).join(' ');
        if (errorStr.includes('Error') || errorStr.includes('error')) {
            const analysis = await this.analyzeError(new Error(errorStr));
            this.emit('error-analyzed', analysis);
        }
    }
    
    /**
     * Observar arquivo para erros
     */
    async watchFile(filePath) {
        console.log(`👁️  Watching: ${filePath}`);
        this.watchedFiles.add(filePath);
        
        const fs = require('fs');
        fs.watchFile(filePath, async (curr, prev) => {
            if (curr.mtime !== prev.mtime) {
                // Arquivo modificado, verificar erros
                await this.checkFileForErrors(filePath);
            }
        });
    }
    
    /**
     * Verificar arquivo por erros
     */
    async checkFileForErrors(filePath) {
        try {
            const { stderr } = await execAsync(`node --check ${filePath}`);
            if (stderr) {
                console.log(`\n⚠️  Error detected in ${path.basename(filePath)}`);
                const context = {
                    file: filePath,
                    code: await fs.readFile(filePath, 'utf8')
                };
                const analysis = await this.analyzeError(new Error(stderr), context);
                
                if (analysis.autoFixable && this.autoFixEnabled) {
                    await this.autoFix(analysis, filePath);
                }
            }
        } catch (error) {
            // Erro de sintaxe ou execução
            const context = {
                file: filePath,
                code: await fs.readFile(filePath, 'utf8')
            };
            const analysis = await this.analyzeError(error, context);
            
            if (analysis.autoFixable && this.autoFixEnabled) {
                await this.autoFix(analysis, filePath);
            }
        }
    }
    
    /**
     * Carregar padrões de erro conhecidos
     */
    async loadErrorPatterns() {
        const patternsFile = path.join(__dirname, 'error-patterns.json');
        try {
            const data = await fs.readFile(patternsFile, 'utf8');
            const patterns = JSON.parse(data);
            for (const [key, value] of Object.entries(patterns)) {
                this.errorPatterns.set(key, value);
            }
            console.log(`📚 Loaded ${this.errorPatterns.size} error patterns`);
        } catch {
            // Arquivo não existe ainda
            await this.saveKnowledge();
        }
    }
    
    /**
     * Salvar conhecimento aprendido
     */
    async saveKnowledge() {
        const patternsFile = path.join(__dirname, 'error-patterns.json');
        const knowledge = Object.fromEntries(this.errorPatterns);
        await fs.writeFile(patternsFile, JSON.stringify(knowledge, null, 2));
    }
    
    /**
     * Gerar relatório de debugging
     */
    generateReport() {
        const uptime = Math.round((Date.now() - this.startTime) / 1000);
        const successRate = this.totalErrors > 0 
            ? (this.successfulFixes / this.totalErrors * 100).toFixed(1)
            : 0;
        
        return {
            name: this.name,
            emoji: this.emoji,
            model: this.model,
            stats: {
                totalErrors: this.totalErrors,
                successfulFixes: this.successfulFixes,
                successRate: `${successRate}%`,
                uptime: `${uptime}s`,
                patternsLearned: this.errorPatterns.size,
                filesWatched: this.watchedFiles.size
            },
            recentErrors: this.errorHistory.slice(-5)
        };
    }
    
    /**
     * Interface de chat para debugging interativo
     */
    async chat(message) {
        const response = await this.callOllama(
            `${this.personality}\n\nUser: ${message}\n\nDebugmon:`
        );
        return response;
    }
}

// Singleton do Debugmon
let debugmonInstance = null;

function getDebugmon() {
    if (!debugmonInstance) {
        debugmonInstance = new Debugmon();
    }
    return debugmonInstance;
}

// Se executado diretamente
if (require.main === module) {
    const debugmon = getDebugmon();
    
    // Interface CLI
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
        prompt: '🐛 Debugmon> '
    });
    
    console.log('\n💬 Chat mode activated! Ask me anything about debugging.\n');
    console.log('Commands:');
    console.log('  /watch <file>  - Watch file for errors');
    console.log('  /analyze <error> - Analyze error message');
    console.log('  /report       - Show debugging report');
    console.log('  /autofix      - Toggle auto-fix');
    console.log('  /exit         - Exit\n');
    
    rl.prompt();
    
    rl.on('line', async (line) => {
        const input = line.trim();
        
        if (input.startsWith('/')) {
            const [cmd, ...args] = input.split(' ');
            
            switch (cmd) {
                case '/watch':
                    if (args[0]) {
                        await debugmon.watchFile(args[0]);
                    } else {
                        console.log('Usage: /watch <file>');
                    }
                    break;
                    
                case '/analyze':
                    if (args.length > 0) {
                        const error = args.join(' ');
                        const analysis = await debugmon.analyzeError(new Error(error));
                        console.log('\n📊 Analysis:', analysis);
                    }
                    break;
                    
                case '/report':
                    console.log('\n📊 Report:', debugmon.generateReport());
                    break;
                    
                case '/autofix':
                    debugmon.autoFixEnabled = !debugmon.autoFixEnabled;
                    console.log(`Auto-fix: ${debugmon.autoFixEnabled ? 'ENABLED' : 'DISABLED'}`);
                    break;
                    
                case '/exit':
                    console.log('👋 Goodbye!');
                    process.exit(0);
                    break;
                    
                default:
                    console.log('Unknown command');
            }
        } else if (input) {
            // Chat mode
            const response = await debugmon.chat(input);
            console.log(`\n${debugmon.emoji} ${response}\n`);
        }
        
        rl.prompt();
    });
}

module.exports = { Debugmon, getDebugmon };