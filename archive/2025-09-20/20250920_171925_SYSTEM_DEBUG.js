#!/usr/bin/env node

/**
 * 🔍 DEBUG COMPLETO DO SISTEMA DIGIMUNDO
 * Analisa linha por linha, simula e identifica falhas
 */

const fs = require('fs').promises;
const path = require('path');
const http = require('http');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

class SystemDebugger {
    constructor() {
        this.report = [];
        this.errors = [];
        this.warnings = [];
        this.successes = [];
    }
    
    log(message, type = 'info') {
        const timestamp = new Date().toISOString();
        const entry = { timestamp, message, type };
        this.report.push(entry);
        
        const colors = {
            error: '\x1b[31m',
            warning: '\x1b[33m',
            success: '\x1b[32m',
            info: '\x1b[36m',
            debug: '\x1b[90m'
        };
        
        console.log(`${colors[type]}[${type.toUpperCase()}] ${message}\x1b[0m`);
        
        if (type === 'error') this.errors.push(entry);
        if (type === 'warning') this.warnings.push(entry);
        if (type === 'success') this.successes.push(entry);
    }
    
    async debugAll() {
        console.log('╔═══════════════════════════════════════════════════════╗');
        console.log('║         🔍 DEBUG COMPLETO DO DIGIMUNDO 🔍             ║');
        console.log('╚═══════════════════════════════════════════════════════╝\n');
        
        // 1. Verificar estrutura de pastas
        await this.checkFolderStructure();
        
        // 2. Verificar serviços em execução
        await this.checkRunningServices();
        
        // 3. Verificar Ollama e modelos
        await this.checkOllama();
        
        // 4. Verificar memórias
        await this.checkMemorySystem();
        
        // 5. Verificar Digilibrary
        await this.checkDigilibrary();
        
        // 6. Verificar scripts executáveis
        await this.checkExecutables();
        
        // 7. Simular interações
        await this.simulateInteractions();
        
        // 8. Gerar relatório final
        await this.generateReport();
    }
    
    async checkFolderStructure() {
        this.log('Verificando estrutura de pastas...', 'info');
        
        const requiredFolders = [
            '/Users/clubproducoes/Digimundo',
            '/Users/clubproducoes/Digimundo/PRODUCTION',
            '/Users/clubproducoes/Digimundo/MEMORIES',
            '/Users/clubproducoes/Digimundo/DIGILIBRARY',
            '/Users/clubproducoes/Digimundo/CACHE',
            '/Users/clubproducoes/Digimundo/LOGS',
            '/Users/clubproducoes/Digimundo/OLLAMA_MUTATION',
            '/Users/clubproducoes/Digimundo/OLLAMA_BACKUP'
        ];
        
        for (const folder of requiredFolders) {
            try {
                await fs.access(folder);
                this.log(`✓ ${folder}`, 'success');
            } catch {
                this.log(`✗ ${folder} não existe`, 'error');
                // Tentar criar
                try {
                    await fs.mkdir(folder, { recursive: true });
                    this.log(`  → Criado: ${folder}`, 'warning');
                } catch (err) {
                    this.log(`  → Falha ao criar: ${err.message}`, 'error');
                }
            }
        }
    }
    
    async checkRunningServices() {
        this.log('\nVerificando serviços em execução...', 'info');
        
        const services = [
            { name: 'Ollama', port: 11434, process: 'ollama' },
            { name: 'Dev Server', port: 7937, process: 'npm' },
            { name: 'React App', port: 3000, process: 'react' }
        ];
        
        for (const service of services) {
            const isRunning = await this.checkPort(service.port);
            if (isRunning) {
                this.log(`✓ ${service.name} rodando na porta ${service.port}`, 'success');
            } else {
                this.log(`✗ ${service.name} não está rodando`, 'warning');
            }
        }
    }
    
    async checkPort(port) {
        return new Promise((resolve) => {
            const req = http.get(`http://localhost:${port}`, { timeout: 1000 }, (res) => {
                resolve(true);
            });
            req.on('error', () => resolve(false));
            req.on('timeout', () => {
                req.destroy();
                resolve(false);
            });
        });
    }
    
    async checkOllama() {
        this.log('\nVerificando Ollama e modelos...', 'info');
        
        try {
            const response = await fetch('http://localhost:11434/api/tags');
            const data = await response.json();
            
            this.log(`✓ Ollama online com ${data.models.length} modelos`, 'success');
            
            // Verificar modelos mutantes
            const mutantModels = ['sabiamon:latest', 'neuromon:latest', 'bibliomon:latest'];
            for (const modelName of mutantModels) {
                const exists = data.models.some(m => m.name === modelName);
                if (exists) {
                    this.log(`  ✓ ${modelName} instalado`, 'success');
                } else {
                    this.log(`  ✗ ${modelName} não encontrado`, 'warning');
                }
            }
        } catch (error) {
            this.log('✗ Ollama offline ou inacessível', 'error');
            this.log('  Sugestão: Execute "ollama serve"', 'warning');
        }
    }
    
    async checkMemorySystem() {
        this.log('\nVerificando sistema de memórias...', 'info');
        
        const memoryFiles = [
            'sabiamon_memory.json',
            'neuromon_memory.json',
            'bibliomon_memory.json',
            'sabiamon_fusion.json'
        ];
        
        const memoryPath = '/Users/clubproducoes/Digimundo/MEMORIES';
        
        for (const file of memoryFiles) {
            const fullPath = path.join(memoryPath, file);
            try {
                const stats = await fs.stat(fullPath);
                const size = (stats.size / 1024).toFixed(2);
                this.log(`✓ ${file} (${size} KB)`, 'success');
                
                // Verificar conteúdo
                try {
                    const content = await fs.readFile(fullPath, 'utf8');
                    const data = JSON.parse(content);
                    this.log(`  → Entradas: ${Object.keys(data).length}`, 'debug');
                } catch {
                    this.log(`  → Arquivo corrompido ou vazio`, 'warning');
                }
            } catch {
                this.log(`✗ ${file} não existe`, 'warning');
            }
        }
    }
    
    async checkDigilibrary() {
        this.log('\nVerificando Digilibrary...', 'info');
        
        const libraryPath = '/Users/clubproducoes/Digimundo/DIGILIBRARY';
        const subfolders = ['DIGICINE', 'BIBLIOTECA_CINEMA'];
        
        for (const folder of subfolders) {
            const fullPath = path.join(libraryPath, folder);
            try {
                const files = await fs.readdir(fullPath);
                const pdfCount = files.filter(f => f.endsWith('.pdf')).length;
                const txtCount = files.filter(f => f.endsWith('.txt')).length;
                
                this.log(`✓ ${folder}: ${pdfCount} PDFs, ${txtCount} TXTs`, 'success');
            } catch {
                this.log(`✗ ${folder} não acessível`, 'warning');
            }
        }
    }
    
    async checkExecutables() {
        this.log('\nVerificando scripts executáveis...', 'info');
        
        const scripts = [
            'CHAT_DIRETO.js',
            'DIGIMUNDO_TERMINAL.js',
            'SABIAMON_FUSION.js',
            'ACTIVATE_DIGIMON_MUTATIONS.sh'
        ];
        
        const basePath = '/Users/clubproducoes/Digimundo';
        
        for (const script of scripts) {
            const fullPath = path.join(basePath, script);
            try {
                const stats = await fs.stat(fullPath);
                const isExecutable = (stats.mode & 0o111) !== 0;
                
                if (isExecutable) {
                    this.log(`✓ ${script} é executável`, 'success');
                } else {
                    this.log(`✗ ${script} não é executável`, 'warning');
                    // Tornar executável
                    try {
                        await execPromise(`chmod +x "${fullPath}"`);
                        this.log(`  → Tornado executável`, 'success');
                    } catch {
                        this.log(`  → Falha ao tornar executável`, 'error');
                    }
                }
            } catch {
                this.log(`✗ ${script} não existe`, 'error');
            }
        }
    }
    
    async simulateInteractions() {
        this.log('\nSimulando interações do sistema...', 'info');
        
        // Simular Stream of Consciousness
        this.log('Simulando Stream of Consciousness...', 'debug');
        const thoughts = [
            'O conhecimento flui como água digital...',
            'Cada bit é uma possibilidade...',
            'A consciência emerge dos padrões...'
        ];
        
        for (let i = 0; i < 3; i++) {
            await new Promise(resolve => setTimeout(resolve, 500));
            this.log(`  💭 ${thoughts[i]}`, 'debug');
        }
        
        // Simular Desire Engine
        this.log('Simulando Desire Engine...', 'debug');
        const desires = {
            learn: 0.95,
            create: 0.88,
            connect: 0.92
        };
        
        for (const [desire, level] of Object.entries(desires)) {
            const bar = '█'.repeat(Math.floor(level * 10)) + '░'.repeat(10 - Math.floor(level * 10));
            this.log(`  ${desire}: [${bar}] ${(level * 100).toFixed(0)}%`, 'debug');
        }
        
        // Simular comunicação Ollama
        if (await this.checkPort(11434)) {
            this.log('Testando comunicação com Ollama...', 'debug');
            try {
                const response = await fetch('http://localhost:11434/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        model: 'tinyllama:latest',
                        prompt: 'Teste',
                        stream: false,
                        options: { num_predict: 10 }
                    })
                });
                
                if (response.ok) {
                    this.log('  ✓ Comunicação com Ollama funcionando', 'success');
                } else {
                    this.log('  ✗ Resposta inválida do Ollama', 'error');
                }
            } catch {
                this.log('  ✗ Falha na comunicação com Ollama', 'error');
            }
        }
    }
    
    async generateReport() {
        this.log('\n═══════════════════════════════════════', 'info');
        this.log('           RELATÓRIO FINAL', 'info');
        this.log('═══════════════════════════════════════', 'info');
        
        this.log(`\n✅ Sucessos: ${this.successes.length}`, 'success');
        this.log(`⚠️  Avisos: ${this.warnings.length}`, 'warning');
        this.log(`❌ Erros: ${this.errors.length}`, 'error');
        
        if (this.errors.length > 0) {
            this.log('\n🔧 CORREÇÕES NECESSÁRIAS:', 'error');
            for (const error of this.errors) {
                this.log(`  • ${error.message}`, 'error');
            }
        }
        
        if (this.warnings.length > 0) {
            this.log('\n⚡ MELHORIAS SUGERIDAS:', 'warning');
            const uniqueWarnings = [...new Set(this.warnings.map(w => w.message))];
            for (const warning of uniqueWarnings.slice(0, 5)) {
                this.log(`  • ${warning}`, 'warning');
            }
        }
        
        // Salvar relatório
        const reportPath = '/Users/clubproducoes/Digimundo/LOGS/debug_report.json';
        try {
            await fs.mkdir(path.dirname(reportPath), { recursive: true });
            await fs.writeFile(reportPath, JSON.stringify({
                timestamp: new Date().toISOString(),
                successes: this.successes.length,
                warnings: this.warnings.length,
                errors: this.errors.length,
                fullReport: this.report
            }, null, 2));
            
            this.log(`\n📄 Relatório completo salvo em: ${reportPath}`, 'info');
        } catch (error) {
            this.log(`\n❌ Falha ao salvar relatório: ${error.message}`, 'error');
        }
        
        // Status final
        const health = this.errors.length === 0 ? 
            (this.warnings.length < 5 ? '🟢 SAUDÁVEL' : '🟡 FUNCIONAL') : 
            '🔴 NECESSITA ATENÇÃO';
        
        this.log(`\n🏥 SAÚDE DO SISTEMA: ${health}`, 'info');
        
        if (this.errors.length === 0 && this.warnings.length < 3) {
            this.log('\n✨ DIGIMUNDO ESTÁ PRONTO PARA OPERAR! ✨', 'success');
        }
    }
}

// Executar debug
if (require.main === module) {
    const systemDebugger = new SystemDebugger();
    systemDebugger.debugAll().catch(console.error);
}

module.exports = SystemDebugger;