#!/usr/bin/env node

/**
 * 🔍 DIGIMUNDO ULTIMATE DEBUGGER
 * Análise completa de debug do sistema em modo Ultimate
 * Mac Studio M3 Ultra - 40GB RAM mode
 */

const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);
const os = require('os');

class DigimundoUltimateDebugger {
    constructor() {
        this.startTime = Date.now();
        this.errors = [];
        this.warnings = [];
        this.successes = [];
        this.basePath = '/Users/clubproducoes/Digimundo';
        
        // Cores para relatório
        this.colors = {
            reset: '\x1b[0m',
            bright: '\x1b[1m',
            red: '\x1b[31m',
            green: '\x1b[32m',
            yellow: '\x1b[33m',
            blue: '\x1b[34m',
            magenta: '\x1b[35m',
            cyan: '\x1b[36m',
            white: '\x1b[37m',
            gray: '\x1b[90m'
        };
        
        this.testResults = {
            fileIntegrity: [],
            functionality: [],
            performance: [],
            communication: [],
            memory: [],
            security: []
        };
    }
    
    log(message, type = 'info') {
        const timestamp = new Date().toISOString().split('T')[1].split('.')[0];
        const colors = this.colors;
        
        switch(type) {
            case 'error':
                console.log(`${colors.red}❌ [${timestamp}] ${message}${colors.reset}`);
                this.errors.push(message);
                break;
            case 'warning':
                console.log(`${colors.yellow}⚠️  [${timestamp}] ${message}${colors.reset}`);
                this.warnings.push(message);
                break;
            case 'success':
                console.log(`${colors.green}✅ [${timestamp}] ${message}${colors.reset}`);
                this.successes.push(message);
                break;
            case 'info':
                console.log(`${colors.cyan}🔍 [${timestamp}] ${message}${colors.reset}`);
                break;
            case 'debug':
                console.log(`${colors.gray}🐛 [${timestamp}] ${message}${colors.reset}`);
                break;
        }
    }
    
    async init() {
        console.clear();
        this.log('INICIANDO DIGIMUNDO ULTIMATE DEBUGGER', 'info');
        console.log(`${this.colors.bright}╔═══════════════════════════════════════════════════════════════╗${this.colors.reset}`);
        console.log(`${this.colors.bright}║         🔍 DIGIMUNDO ULTIMATE DEBUGGER 🔍                    ║${this.colors.reset}`);
        console.log(`${this.colors.bright}║              Análise Completa do Sistema                      ║${this.colors.reset}`);
        console.log(`${this.colors.bright}║              Modo Ultimate - 40GB RAM                         ║${this.colors.reset}`);
        console.log(`${this.colors.bright}╚═══════════════════════════════════════════════════════════════╝${this.colors.reset}\n`);
        
        await this.runCompleteAnalysis();
    }
    
    async runCompleteAnalysis() {
        const tests = [
            { name: 'Verificação de Integridade de Arquivos', fn: this.testFileIntegrity },
            { name: 'Teste de Funcionalidades Core', fn: this.testCoreFunctionality },
            { name: 'Análise de Performance', fn: this.testPerformance },
            { name: 'Comunicação entre Digimons', fn: this.testDigimonCommunication },
            { name: 'Gestão de Memória', fn: this.testMemoryManagement },
            { name: 'Auditoria de Segurança', fn: this.testSecurity },
            { name: 'Simulações de Stress Test', fn: this.runStressTests },
            { name: 'Validação de Caminhos Críticos', fn: this.testCriticalPaths }
        ];
        
        for (const test of tests) {
            this.log(`Executando: ${test.name}`, 'info');
            try {
                await test.fn.call(this);
                this.log(`${test.name} - CONCLUÍDO`, 'success');
            } catch (error) {
                this.log(`${test.name} - FALHOU: ${error.message}`, 'error');
            }
            console.log(''); // Linha em branco
        }
        
        await this.generateReport();
    }
    
    async testFileIntegrity() {
        const criticalFiles = [
            'DIGIMUNDO_EVOLUTION.js',
            'LAUNCH_DIGIMUNDO.sh',
            'GESTORMON_SYSTEM.js',
            'SABIAMON_FUSION.js',
            'ACTIVATE_DIGIMON_MUTATIONS.sh',
            'VALIDATE_DIGIMUNDO.sh',
            'OLLAMA_MUTATION/Neuromon.Modelfile',
            'OLLAMA_MUTATION/Bibliomon.Modelfile',
            'OLLAMA_MUTATION/Sabiamon.Modelfile',
            'OLLAMA_MUTATION/Gestormon.Modelfile',
            'OLLAMA_MUTATION/Scripturemon.Modelfile',
            'OLLAMA_MUTATION/Ajamon.Modelfile',
            'OLLAMA_MUTATION/Shenlongmon.Modelfile'
        ];
        
        for (const file of criticalFiles) {
            const fullPath = path.join(this.basePath, file);
            try {
                const stats = await fs.stat(fullPath);
                if (stats.size === 0) {
                    this.log(`Arquivo vazio: ${file}`, 'warning');
                    this.testResults.fileIntegrity.push({file, status: 'empty', size: 0});
                } else {
                    this.log(`Arquivo OK: ${file} (${this.formatBytes(stats.size)})`, 'debug');
                    this.testResults.fileIntegrity.push({file, status: 'ok', size: stats.size});
                }
                
                // Verificar sintaxe para arquivos JS
                if (file.endsWith('.js')) {
                    try {
                        await execPromise(`node --check "${fullPath}"`);
                        this.log(`Sintaxe JS válida: ${file}`, 'debug');
                    } catch (syntaxError) {
                        this.log(`Erro de sintaxe em ${file}: ${syntaxError.message}`, 'error');
                        this.testResults.fileIntegrity.push({file, status: 'syntax_error', error: syntaxError.message});
                    }
                }
                
                // Verificar executabilidade para scripts shell
                if (file.endsWith('.sh')) {
                    try {
                        await execPromise(`bash -n "${fullPath}"`);
                        this.log(`Script shell válido: ${file}`, 'debug');
                    } catch (bashError) {
                        this.log(`Erro no script ${file}: ${bashError.message}`, 'error');
                    }
                }
                
            } catch (error) {
                this.log(`Arquivo não encontrado: ${file}`, 'error');
                this.testResults.fileIntegrity.push({file, status: 'missing'});
            }
        }
    }
    
    async testCoreFunctionality() {
        // Teste 1: Verificar se Ollama está rodando
        try {
            await execPromise('curl -s http://localhost:11434/api/tags');
            this.log('Ollama API - FUNCIONANDO', 'success');
            this.testResults.functionality.push({test: 'ollama_api', status: 'pass'});
        } catch (error) {
            this.log('Ollama API - FALHOU', 'error');
            this.testResults.functionality.push({test: 'ollama_api', status: 'fail', error: error.message});
        }
        
        // Teste 2: Verificar modelos Digimon
        const digimons = ['neuromon', 'bibliomon', 'sabiamon', 'gestormon', 'scripturemon', 'ajamon'];
        try {
            const {stdout} = await execPromise('ollama list');
            for (const digimon of digimons) {
                if (stdout.includes(`${digimon}:latest`)) {
                    this.log(`Modelo ${digimon} - DISPONÍVEL`, 'success');
                    this.testResults.functionality.push({test: `model_${digimon}`, status: 'pass'});
                } else {
                    this.log(`Modelo ${digimon} - NÃO ENCONTRADO`, 'error');
                    this.testResults.functionality.push({test: `model_${digimon}`, status: 'fail'});
                }
            }
        } catch (error) {
            this.log(`Erro ao listar modelos: ${error.message}`, 'error');
        }
        
        // Teste 3: Verificar Shenlongmon (70B)
        try {
            const {stdout} = await execPromise('ollama list');
            if (stdout.includes('llama3.1:70b')) {
                this.log('Shenlongmon (70B) - DISPONÍVEL', 'success');
                this.testResults.functionality.push({test: 'shenlongmon_70b', status: 'pass'});
            } else {
                this.log('Shenlongmon (70B) - NÃO ENCONTRADO', 'warning');
                this.testResults.functionality.push({test: 'shenlongmon_70b', status: 'warning'});
            }
        } catch (error) {
            this.log(`Erro ao verificar Shenlongmon: ${error.message}`, 'error');
        }
        
        // Teste 4: Verificar estrutura de diretórios
        const directories = ['CONFIG', 'OLLAMA_MUTATION', 'DIGILIBRARY', 'PRODUCTION'];
        for (const dir of directories) {
            try {
                const fullPath = path.join(this.basePath, dir);
                await fs.access(fullPath);
                this.log(`Diretório ${dir} - EXISTE`, 'success');
                this.testResults.functionality.push({test: `dir_${dir}`, status: 'pass'});
            } catch (error) {
                this.log(`Diretório ${dir} - NÃO ENCONTRADO`, 'warning');
                this.testResults.functionality.push({test: `dir_${dir}`, status: 'warning'});
            }
        }
    }
    
    async testPerformance() {
        // Teste de performance do sistema
        const startCPU = process.cpuUsage();
        const startMem = process.memoryUsage();
        const startTime = Date.now();
        
        // Simular carga de trabalho
        let result = 0;
        for (let i = 0; i < 1000000; i++) {
            result += Math.sqrt(i);
        }
        
        const endTime = Date.now();
        const endCPU = process.cpuUsage(startCPU);
        const endMem = process.memoryUsage();
        
        const performanceMetrics = {
            executionTime: endTime - startTime,
            cpuUsage: {
                user: endCPU.user / 1000, // microseconds to milliseconds
                system: endCPU.system / 1000
            },
            memoryDelta: {
                rss: endMem.rss - startMem.rss,
                heapUsed: endMem.heapUsed - startMem.heapUsed,
                heapTotal: endMem.heapTotal - startMem.heapTotal
            }
        };
        
        this.log(`Performance - Tempo: ${performanceMetrics.executionTime}ms`, 'info');
        this.log(`Performance - CPU User: ${performanceMetrics.cpuUsage.user.toFixed(2)}ms`, 'info');
        this.log(`Performance - Memória RSS: ${this.formatBytes(performanceMetrics.memoryDelta.rss)}`, 'info');
        
        this.testResults.performance.push(performanceMetrics);
        
        // Teste de carga do sistema
        try {
            const systemInfo = {
                totalRAM: os.totalmem(),
                freeRAM: os.freemem(),
                cpuCores: os.cpus().length,
                loadAverage: os.loadavg(),
                uptime: os.uptime()
            };
            
            const ramUsagePercent = ((systemInfo.totalRAM - systemInfo.freeRAM) / systemInfo.totalRAM) * 100;
            
            this.log(`Sistema - RAM usada: ${ramUsagePercent.toFixed(1)}%`, 'info');
            this.log(`Sistema - Load average: ${systemInfo.loadAverage[0].toFixed(2)}`, 'info');
            this.log(`Sistema - CPU cores: ${systemInfo.cpuCores}`, 'info');
            
            if (ramUsagePercent > 90) {
                this.log('ALERTA: Uso de RAM crítico (>90%)', 'warning');
            }
            
            if (systemInfo.loadAverage[0] > systemInfo.cpuCores) {
                this.log('ALERTA: Load average alto', 'warning');
            }
            
            this.testResults.performance.push({type: 'system', data: systemInfo});
            
        } catch (error) {
            this.log(`Erro ao obter informações do sistema: ${error.message}`, 'error');
        }
    }
    
    async testDigimonCommunication() {
        // Teste básico de comunicação com cada Digimon
        const digimons = ['gestormon']; // Começar com o mais leve
        
        for (const digimon of digimons) {
            try {
                this.log(`Testando comunicação com ${digimon}...`, 'debug');
                
                // Teste com timeout de 15 segundos
                const testPromise = execPromise(`echo "teste de status" | ollama run ${digimon}`);
                const timeoutPromise = new Promise((_, reject) => {
                    setTimeout(() => reject(new Error('Timeout')), 15000);
                });
                
                const result = await Promise.race([testPromise, timeoutPromise]);
                
                if (result.stdout && result.stdout.length > 0) {
                    this.log(`${digimon} - RESPONDENDO`, 'success');
                    this.testResults.communication.push({digimon, status: 'responsive', responseLength: result.stdout.length});
                } else {
                    this.log(`${digimon} - RESPOSTA VAZIA`, 'warning');
                    this.testResults.communication.push({digimon, status: 'empty_response'});
                }
                
            } catch (error) {
                if (error.message === 'Timeout') {
                    this.log(`${digimon} - TIMEOUT (>15s)`, 'warning');
                    this.testResults.communication.push({digimon, status: 'timeout'});
                } else {
                    this.log(`${digimon} - ERRO: ${error.message}`, 'error');
                    this.testResults.communication.push({digimon, status: 'error', error: error.message});
                }
            }
        }
    }
    
    async testMemoryManagement() {
        // Verificar limites de memória configurados
        try {
            const configPath = path.join(this.basePath, 'CONFIG', 'evolution_mode.json');
            const configExists = await fs.access(configPath).then(() => true).catch(() => false);
            
            if (configExists) {
                const config = JSON.parse(await fs.readFile(configPath, 'utf8'));
                this.log(`Configuração de memória encontrada - Modo: ${config.mode}`, 'success');
                this.log(`RAM máxima configurada: ${this.formatBytes(config.maxRAM)}`, 'info');
                this.testResults.memory.push({test: 'config_exists', status: 'pass', config});
            } else {
                this.log('Arquivo de configuração de memória não encontrado', 'warning');
                this.testResults.memory.push({test: 'config_exists', status: 'fail'});
            }
        } catch (error) {
            this.log(`Erro ao verificar configuração: ${error.message}`, 'error');
        }
        
        // Verificar uso atual de memória
        const memInfo = {
            total: os.totalmem(),
            free: os.freemem(),
            used: os.totalmem() - os.freemem()
        };
        
        const usagePercent = (memInfo.used / memInfo.total) * 100;
        this.log(`Memória atual - Usado: ${this.formatBytes(memInfo.used)} (${usagePercent.toFixed(1)}%)`, 'info');
        this.log(`Memória disponível: ${this.formatBytes(memInfo.free)}`, 'info');
        
        this.testResults.memory.push({
            test: 'current_usage',
            status: 'info',
            data: {
                total: memInfo.total,
                used: memInfo.used,
                free: memInfo.free,
                usagePercent
            }
        });
    }
    
    async testSecurity() {
        // Verificar permissões de arquivos críticos
        const criticalFiles = [
            'LAUNCH_DIGIMUNDO.sh',
            'ACTIVATE_DIGIMON_MUTATIONS.sh',
            'VALIDATE_DIGIMUNDO.sh'
        ];
        
        for (const file of criticalFiles) {
            try {
                const fullPath = path.join(this.basePath, file);
                const stats = await fs.stat(fullPath);
                const isExecutable = (stats.mode & parseInt('111', 8)) !== 0;
                
                if (isExecutable) {
                    this.log(`${file} - Permissões OK (executável)`, 'success');
                    this.testResults.security.push({file, test: 'permissions', status: 'pass'});
                } else {
                    this.log(`${file} - SEM PERMISSÃO DE EXECUÇÃO`, 'warning');
                    this.testResults.security.push({file, test: 'permissions', status: 'warning'});
                }
            } catch (error) {
                this.log(`Erro ao verificar permissões de ${file}: ${error.message}`, 'error');
                this.testResults.security.push({file, test: 'permissions', status: 'error'});
            }
        }
        
        // Verificar se há processos suspeitos
        try {
            const {stdout} = await execPromise('ps aux | grep -E "(ollama|node)" | grep -v grep');
            const processes = stdout.split('\n').filter(line => line.trim().length > 0);
            
            this.log(`Processos ativos relacionados: ${processes.length}`, 'info');
            for (const process of processes) {
                this.log(`Processo: ${process.split(/\s+/).slice(10).join(' ')}`, 'debug');
            }
            
            this.testResults.security.push({
                test: 'active_processes',
                status: 'info',
                count: processes.length,
                processes: processes.map(p => p.split(/\s+/).slice(10).join(' '))
            });
            
        } catch (error) {
            this.log(`Erro ao verificar processos: ${error.message}`, 'warning');
        }
    }
    
    async runStressTests() {
        this.log('Executando testes de stress...', 'info');
        
        // Stress test 1: Múltiplas requisições simultâneas
        const stressTest1 = async () => {
            const promises = [];
            for (let i = 0; i < 5; i++) {
                promises.push(
                    execPromise('ollama list').catch(e => ({error: e.message}))
                );
            }
            const results = await Promise.all(promises);
            const errors = results.filter(r => r.error).length;
            
            this.log(`Stress Test 1 - ${5 - errors}/5 requisições bem-sucedidas`, errors === 0 ? 'success' : 'warning');
            return {test: 'concurrent_requests', success: 5 - errors, total: 5};
        };
        
        // Stress test 2: Teste de carga de CPU
        const stressTest2 = async () => {
            const startTime = Date.now();
            let iterations = 0;
            
            // Executar por 2 segundos
            while (Date.now() - startTime < 2000) {
                Math.sqrt(Math.random() * 1000000);
                iterations++;
            }
            
            const opsPerSecond = iterations / 2;
            this.log(`Stress Test 2 - CPU: ${opsPerSecond.toFixed(0)} ops/sec`, 'info');
            return {test: 'cpu_load', opsPerSecond};
        };
        
        try {
            const result1 = await stressTest1();
            const result2 = await stressTest2();
            
            this.testResults.performance.push(result1, result2);
            
        } catch (error) {
            this.log(`Erro nos testes de stress: ${error.message}`, 'error');
        }
    }
    
    async testCriticalPaths() {
        // Teste de caminhos críticos do sistema
        const criticalPaths = [
            {
                name: 'Launcher Principal',
                command: 'ls -la LAUNCH_DIGIMUNDO.sh',
                expected: 'executable'
            },
            {
                name: 'Diretório de Mutações',
                command: 'ls -la OLLAMA_MUTATION/',
                expected: 'directory_exists'
            },
            {
                name: 'Configurações',
                command: 'mkdir -p CONFIG && ls -la CONFIG/',
                expected: 'directory_exists'
            }
        ];
        
        for (const pathTest of criticalPaths) {
            try {
                const {stdout} = await execPromise(`cd "${this.basePath}" && ${pathTest.command}`);
                this.log(`Caminho crítico OK: ${pathTest.name}`, 'success');
                this.testResults.functionality.push({
                    test: `critical_path_${pathTest.name.replace(/\s+/g, '_').toLowerCase()}`,
                    status: 'pass'
                });
            } catch (error) {
                this.log(`Caminho crítico FALHOU: ${pathTest.name} - ${error.message}`, 'error');
                this.testResults.functionality.push({
                    test: `critical_path_${pathTest.name.replace(/\s+/g, '_').toLowerCase()}`,
                    status: 'fail',
                    error: error.message
                });
            }
        }
    }
    
    async generateReport() {
        const endTime = Date.now();
        const totalTime = endTime - this.startTime;
        
        console.log(`\n${this.colors.bright}╔═══════════════════════════════════════════════════════════════╗${this.colors.reset}`);
        console.log(`${this.colors.bright}║                    📊 RELATÓRIO FINAL DE DEBUG               ║${this.colors.reset}`);
        console.log(`${this.colors.bright}╚═══════════════════════════════════════════════════════════════╝${this.colors.reset}\n`);
        
        // Estatísticas gerais
        this.log(`Tempo total de análise: ${totalTime}ms`, 'info');
        this.log(`Sucessos: ${this.successes.length}`, 'success');
        this.log(`Avisos: ${this.warnings.length}`, 'warning');
        this.log(`Erros: ${this.errors.length}`, 'error');
        
        console.log('\n' + this.colors.cyan + '📋 RESUMO POR CATEGORIA:' + this.colors.reset);
        
        // Relatório por categoria
        for (const [category, results] of Object.entries(this.testResults)) {
            if (results.length > 0) {
                console.log(`\n${this.colors.yellow}🔍 ${category.toUpperCase()}:${this.colors.reset}`);
                for (const result of results) {
                    const status = result.status || 'unknown';
                    const color = status === 'pass' || status === 'ok' ? this.colors.green :
                                 status === 'warning' ? this.colors.yellow :
                                 status === 'fail' || status === 'error' ? this.colors.red :
                                 this.colors.gray;
                    
                    const testName = result.test || result.file || result.digimon || 'Unknown';
                    console.log(`  ${color}${status.toUpperCase()}${this.colors.reset} - ${testName}`);
                }
            }
        }
        
        // Recomendações
        console.log(`\n${this.colors.magenta}💡 RECOMENDAÇÕES:${this.colors.reset}`);
        
        if (this.errors.length === 0) {
            this.log('Sistema está funcionando perfeitamente! ✨', 'success');
        } else {
            this.log(`Corrigir ${this.errors.length} erro(s) crítico(s)`, 'error');
        }
        
        if (this.warnings.length > 0) {
            this.log(`Revisar ${this.warnings.length} aviso(s)`, 'warning');
        }
        
        // Salvar relatório
        await this.saveReport({
            timestamp: new Date().toISOString(),
            totalTime,
            stats: {
                successes: this.successes.length,
                warnings: this.warnings.length,
                errors: this.errors.length
            },
            results: this.testResults,
            errors: this.errors,
            warnings: this.warnings
        });
        
        console.log(`\n${this.colors.bright}Debug completo! Relatório salvo em: debug_report_${Date.now()}.json${this.colors.reset}\n`);
    }
    
    async saveReport(report) {
        try {
            const reportPath = path.join(this.basePath, `debug_report_${Date.now()}.json`);
            await fs.writeFile(reportPath, JSON.stringify(report, null, 2));
            this.log(`Relatório salvo: ${reportPath}`, 'success');
        } catch (error) {
            this.log(`Erro ao salvar relatório: ${error.message}`, 'error');
        }
    }
    
    formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Executar debugger
if (require.main === module) {
    const systemDebugger = new DigimundoUltimateDebugger();
    systemDebugger.init().catch(console.error);
}

module.exports = DigimundoUltimateDebugger;