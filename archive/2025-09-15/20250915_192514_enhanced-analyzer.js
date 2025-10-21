/**
 * 🔍 ANALYZERMON ENHANCED WITH SILICON VALLEY METHODS
 * Agora com conhecimento de Google, Meta e Apple
 */

const EventEmitter = require('events');
const SiliconValleyMethodologies = require('../../knowledge/silicon-valley-methodologies');

class EnhancedAnalyzermon extends EventEmitter {
    constructor() {
        super();
        this.name = 'Analyzermon Enhanced';
        this.knowledge = new SiliconValleyMethodologies();
        this.capabilities = new Set([
            'google-code-health',
            'meta-dependency-graph',
            'apple-design-audit',
            'complexity-analysis',
            'pattern-detection',
            'quality-scoring'
        ]);
        
        // Aprender metodologias específicas
        this.learnedMethods = this.knowledge.teachDigimon('analyzermon');
        
        console.log(`🔍 ${this.name} aprendeu ${this.learnedMethods.length} metodologias do Vale do Silício!`);
    }

    // Análise completa usando Google Code Health
    async analyzeCodeHealth(code) {
        console.log('\n🔍 Executando Google Code Health Analysis...');
        
        const googleMethod = this.learnedMethods[0]; // Google methodology
        
        // Calcular métricas
        const complexity = this.calculateCyclomaticComplexity(code);
        const lines = code.split('\n').length;
        const testCoverage = this.estimateTestCoverage(code);
        const documentation = this.analyzeDocumentation(code);
        
        // Fórmula do Google
        const maintainabilityIndex = Math.max(0,
            171 - 5.2 * Math.log(complexity) -
            0.23 * complexity -
            16.2 * Math.log(lines)
        ) * 100 / 171;
        
        const health = {
            score: maintainabilityIndex,
            grade: this.getHealthGrade(maintainabilityIndex),
            metrics: {
                complexity,
                lines,
                testCoverage,
                documentation
            },
            recommendations: []
        };
        
        // Gerar recomendações baseadas no Google
        if (complexity > 10) {
            health.recommendations.push('Reduzir complexidade ciclomática dividindo funções grandes');
        }
        if (testCoverage < 80) {
            health.recommendations.push('Aumentar cobertura de testes para pelo menos 80% (padrão Google)');
        }
        if (documentation < 50) {
            health.recommendations.push('Documentar todas APIs públicas com JSDoc');
        }
        
        this.emit('analysis-complete', {
            type: 'google-health',
            result: health
        });
        
        return health;
    }

    // Análise de dependências usando Meta Graph Theory
    async analyzeDependencyGraph(modules) {
        console.log('\n🕸️ Executando Meta Dependency Graph Analysis...');
        
        const metaMethod = this.learnedMethods[1]; // Meta methodology
        
        // Construir grafo
        const graph = this.buildDependencyGraph(modules);
        
        // Detectar problemas
        const cycles = this.detectCircularDependencies(graph);
        const hubs = this.findHubModules(graph);
        const isolated = this.findIsolatedModules(graph);
        const instability = this.calculateInstabilityIndex(graph);
        
        const analysis = {
            totalNodes: graph.nodes.length,
            totalEdges: graph.edges.length,
            circularDependencies: cycles,
            hubModules: hubs,
            isolatedModules: isolated,
            instabilityIndex: instability,
            health: cycles.length === 0 ? 'HEALTHY' : 'UNHEALTHY',
            recommendations: []
        };
        
        // Recomendações do Meta
        if (cycles.length > 0) {
            analysis.recommendations.push(`Eliminar ${cycles.length} dependências circulares`);
        }
        if (hubs.length > 0) {
            analysis.recommendations.push('Considerar dividir módulos hub para reduzir acoplamento');
        }
        if (instability > 0.5) {
            analysis.recommendations.push('Sistema muito instável - estabilizar interfaces');
        }
        
        this.emit('analysis-complete', {
            type: 'meta-dependency',
            result: analysis
        });
        
        return analysis;
    }

    // Análise de design usando Apple Design Excellence
    async analyzeDesignConsistency(codebase) {
        console.log('\n🎨 Executando Apple Design Consistency Analysis...');
        
        const appleMethod = this.learnedMethods[2]; // Apple methodology
        
        const analysis = {
            namingConsistency: this.analyzeNamingConventions(codebase),
            patternUsage: this.detectDesignPatterns(codebase),
            codeStyle: this.analyzeCodeStyle(codebase),
            documentation: this.analyzeDocumentationQuality(codebase),
            score: 0,
            recommendations: []
        };
        
        // Calcular score estilo Apple
        analysis.score = (
            analysis.namingConsistency.score * 0.3 +
            analysis.patternUsage.score * 0.2 +
            analysis.codeStyle.score * 0.3 +
            analysis.documentation.score * 0.2
        );
        
        // Recomendações estilo Apple
        if (analysis.namingConsistency.score < 80) {
            analysis.recommendations.push('Padronizar nomenclatura: camelCase para funções, PascalCase para classes');
        }
        if (analysis.patternUsage.patterns.length < 3) {
            analysis.recommendations.push('Implementar padrões de design consistentes (Singleton, Observer, Factory)');
        }
        if (analysis.documentation.score < 70) {
            analysis.recommendations.push('Adicionar documentação no estilo Apple: clara, concisa e com exemplos');
        }
        
        this.emit('analysis-complete', {
            type: 'apple-design',
            result: analysis
        });
        
        return analysis;
    }

    // Métodos auxiliares
    calculateCyclomaticComplexity(code) {
        let complexity = 1;
        const patterns = [
            /if\s*\(/g,
            /else\s+if\s*\(/g,
            /for\s*\(/g,
            /while\s*\(/g,
            /case\s+/g,
            /catch\s*\(/g,
            /\?\s*[^:]+\s*:/g
        ];
        
        for (const pattern of patterns) {
            const matches = code.match(pattern);
            if (matches) complexity += matches.length;
        }
        
        return complexity;
    }

    estimateTestCoverage(code) {
        const hasTests = /test|spec|describe|it\(/i.test(code);
        const testCount = (code.match(/it\s*\(/g) || []).length;
        const functionCount = (code.match(/function|=>|async/g) || []).length;
        
        if (!hasTests) return 0;
        if (functionCount === 0) return 100;
        
        return Math.min(100, (testCount / functionCount) * 100);
    }

    analyzeDocumentation(code) {
        const jsdocComments = (code.match(/\/\*\*[\s\S]*?\*\//g) || []).length;
        const functions = (code.match(/function|class/g) || []).length;
        
        if (functions === 0) return 100;
        return Math.min(100, (jsdocComments / functions) * 100);
    }

    buildDependencyGraph(modules) {
        const nodes = [];
        const edges = [];
        
        for (const module of modules) {
            nodes.push(module.name);
            for (const dep of module.dependencies || []) {
                edges.push({ from: module.name, to: dep });
            }
        }
        
        return { nodes, edges };
    }

    detectCircularDependencies(graph) {
        const visited = new Set();
        const recursionStack = new Set();
        const cycles = [];
        
        const dfs = (node, path = []) => {
            if (recursionStack.has(node)) {
                const cycleStart = path.indexOf(node);
                cycles.push(path.slice(cycleStart));
                return;
            }
            
            if (visited.has(node)) return;
            
            visited.add(node);
            recursionStack.add(node);
            path.push(node);
            
            const edges = graph.edges.filter(e => e.from === node);
            for (const edge of edges) {
                dfs(edge.to, [...path]);
            }
            
            recursionStack.delete(node);
        };
        
        for (const node of graph.nodes) {
            if (!visited.has(node)) {
                dfs(node);
            }
        }
        
        return cycles;
    }

    findHubModules(graph, threshold = 10) {
        const hubs = [];
        
        for (const node of graph.nodes) {
            const outgoing = graph.edges.filter(e => e.from === node).length;
            const incoming = graph.edges.filter(e => e.to === node).length;
            
            if (outgoing > threshold || incoming > threshold) {
                hubs.push({
                    module: node,
                    dependencies: outgoing,
                    dependents: incoming
                });
            }
        }
        
        return hubs;
    }

    findIsolatedModules(graph) {
        const isolated = [];
        
        for (const node of graph.nodes) {
            const hasEdges = graph.edges.some(e => e.from === node || e.to === node);
            if (!hasEdges) {
                isolated.push(node);
            }
        }
        
        return isolated;
    }

    calculateInstabilityIndex(graph) {
        let totalInstability = 0;
        let count = 0;
        
        for (const node of graph.nodes) {
            const efferent = graph.edges.filter(e => e.from === node).length;
            const afferent = graph.edges.filter(e => e.to === node).length;
            
            if (efferent + afferent > 0) {
                const instability = efferent / (efferent + afferent);
                totalInstability += instability;
                count++;
            }
        }
        
        return count > 0 ? totalInstability / count : 0;
    }

    analyzeNamingConventions(codebase) {
        const functions = codebase.match(/function\s+(\w+)|const\s+(\w+)\s*=/g) || [];
        let camelCase = 0;
        let pascalCase = 0;
        let snakeCase = 0;
        let other = 0;
        
        for (const func of functions) {
            const name = func.replace(/function\s+|const\s+|\s*=/g, '');
            if (/^[a-z][a-zA-Z0-9]*$/.test(name)) camelCase++;
            else if (/^[A-Z][a-zA-Z0-9]*$/.test(name)) pascalCase++;
            else if (/^[a-z_]+$/.test(name)) snakeCase++;
            else other++;
        }
        
        const total = functions.length || 1;
        const dominant = Math.max(camelCase, pascalCase, snakeCase);
        
        return {
            score: (dominant / total) * 100,
            breakdown: { camelCase, pascalCase, snakeCase, other }
        };
    }

    detectDesignPatterns(codebase) {
        const patterns = [];
        const patternChecks = [
            { name: 'Singleton', regex: /getInstance|singleton/i },
            { name: 'Factory', regex: /factory|create\w+/i },
            { name: 'Observer', regex: /on\(|emit\(|addEventListener/i },
            { name: 'Adapter', regex: /adapter|wrapper/i },
            { name: 'Strategy', regex: /strategy|algorithm/i }
        ];
        
        for (const check of patternChecks) {
            if (check.regex.test(codebase)) {
                patterns.push(check.name);
            }
        }
        
        return {
            patterns,
            score: Math.min(100, patterns.length * 20)
        };
    }

    analyzeCodeStyle(codebase) {
        const lines = codebase.split('\n');
        const maxLength = Math.max(...lines.map(l => l.length));
        const avgLength = lines.reduce((sum, l) => sum + l.length, 0) / lines.length;
        
        // Detectar indentação
        const tabs = lines.filter(l => l.startsWith('\t')).length;
        const spaces = lines.filter(l => l.startsWith('  ')).length;
        const indentation = tabs > spaces ? 'tabs' : 'spaces';
        
        const score = 
            (maxLength <= 120 ? 50 : 0) +
            (avgLength <= 80 ? 30 : 0) +
            (indentation === 'spaces' ? 20 : 10);
        
        return {
            score,
            maxLineLength: maxLength,
            avgLineLength: Math.round(avgLength),
            indentation
        };
    }

    analyzeDocumentationQuality(codebase) {
        const jsdocs = (codebase.match(/\/\*\*[\s\S]*?\*\//g) || []).length;
        const inlineComments = (codebase.match(/\/\/.*/g) || []).length;
        const functions = (codebase.match(/function|class/g) || []).length;
        
        const coverage = functions > 0 ? (jsdocs / functions) * 100 : 0;
        const density = inlineComments / (codebase.split('\n').length) * 100;
        
        return {
            score: Math.min(100, coverage * 0.7 + density * 0.3),
            jsdocs,
            inlineComments,
            coverage: Math.round(coverage),
            density: Math.round(density)
        };
    }

    getHealthGrade(score) {
        if (score >= 90) return 'A+';
        if (score >= 80) return 'A';
        if (score >= 70) return 'B';
        if (score >= 60) return 'C';
        if (score >= 50) return 'D';
        return 'F';
    }

    // Método principal de análise completa
    async performFullAnalysis(target) {
        console.log(`\n🔍 ${this.name} iniciando análise completa com metodologias FAANG...`);
        
        const results = {
            google: await this.analyzeCodeHealth(target),
            meta: await this.analyzeDependencyGraph(target.modules || []),
            apple: await this.analyzeDesignConsistency(target),
            timestamp: new Date().toISOString(),
            analyzer: this.name
        };
        
        // Calcular score geral
        results.overallScore = (
            results.google.score * 0.4 +
            (results.meta.health === 'HEALTHY' ? 100 : 50) * 0.3 +
            results.apple.score * 0.3
        );
        
        results.overallGrade = this.getHealthGrade(results.overallScore);
        
        console.log(`\n✅ Análise completa:`);
        console.log(`   Google Health: ${results.google.grade}`);
        console.log(`   Meta Dependencies: ${results.meta.health}`);
        console.log(`   Apple Design: ${results.apple.score.toFixed(1)}/100`);
        console.log(`   Overall: ${results.overallGrade} (${results.overallScore.toFixed(1)}/100)`);
        
        return results;
    }
}

module.exports = EnhancedAnalyzermon;