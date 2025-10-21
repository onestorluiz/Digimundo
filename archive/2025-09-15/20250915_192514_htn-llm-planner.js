/**
 * 🤖 HTN+LLM Hybrid Planning Engine
 * Combina planejamento simbólico hierárquico com flexibilidade de LLMs
 */

const EventEmitter = require('events');

class HTNLLMPlanner extends EventEmitter {
    constructor(orchestrator) {
        super();
        this.orchestrator = orchestrator;
        this.taskLibrary = new Map();
        this.methodLibrary = new Map();
        this.operatorLibrary = new Map();
        this.worldState = new Map();
        this.planHistory = [];
        this.llmAdapter = null;
        
        this.initialize();
    }
    
    async initialize() {
        console.log('\n🤖 Inicializando HTN+LLM Hybrid Planner...');
        
        // Registrar tarefas compostas padrão
        this.registerCompoundTasks();
        
        // Registrar operadores primitivos
        this.registerPrimitiveOperators();
        
        // Registrar métodos de decomposição
        this.registerDecompositionMethods();
        
        console.log('✅ Planner híbrido operacional!');
    }
    
    registerCompoundTasks() {
        // Tarefa: Desenvolver Feature
        this.taskLibrary.set('develop-feature', {
            type: 'compound',
            parameters: ['feature-spec'],
            preconditions: [
                { type: 'have-spec', value: true },
                { type: 'resources-available', value: true }
            ],
            effects: [
                { type: 'feature-completed', value: true }
            ]
        });
        
        // Tarefa: Corrigir Bug
        this.taskLibrary.set('fix-bug', {
            type: 'compound',
            parameters: ['bug-id'],
            preconditions: [
                { type: 'bug-exists', value: true }
            ],
            effects: [
                { type: 'bug-fixed', value: true }
            ]
        });
        
        // Tarefa: Otimizar Performance
        this.taskLibrary.set('optimize-performance', {
            type: 'compound',
            parameters: ['component'],
            preconditions: [
                { type: 'performance-issue', value: true }
            ],
            effects: [
                { type: 'performance-improved', value: true }
            ]
        });
        
        // Tarefa: Refatorar Código
        this.taskLibrary.set('refactor-code', {
            type: 'compound',
            parameters: ['module'],
            preconditions: [
                { type: 'code-quality-low', value: true }
            ],
            effects: [
                { type: 'code-quality-improved', value: true }
            ]
        });
    }
    
    registerPrimitiveOperators() {
        // Operador: Analisar Código
        this.operatorLibrary.set('analyze-code', {
            type: 'primitive',
            execute: async (params) => {
                console.log(`🔍 Analisando código: ${params.target}`);
                
                // Delegar para Analyzermon
                const result = await this.orchestrator.delegateTask('analyzermon', {
                    action: 'analyze',
                    target: params.target
                });
                
                return {
                    success: true,
                    analysis: result,
                    issues: result.issues || []
                };
            },
            preconditions: [{ type: 'code-exists', value: true }],
            effects: [{ type: 'code-analyzed', value: true }]
        });
        
        // Operador: Escrever Código
        this.operatorLibrary.set('write-code', {
            type: 'primitive',
            execute: async (params) => {
                console.log(`✍️ Escrevendo código: ${params.description}`);
                
                // Usar LLM para gerar código
                const code = await this.generateCodeWithLLM(params);
                
                // Delegar para Creativemon
                const result = await this.orchestrator.delegateTask('creativemon', {
                    action: 'create',
                    type: 'code',
                    content: code
                });
                
                return {
                    success: true,
                    code: result.code,
                    location: result.location
                };
            },
            preconditions: [{ type: 'spec-defined', value: true }],
            effects: [{ type: 'code-written', value: true }]
        });
        
        // Operador: Testar Código
        this.operatorLibrary.set('test-code', {
            type: 'primitive',
            execute: async (params) => {
                console.log(`🧪 Testando código: ${params.module}`);
                
                // Delegar para Guardmon
                const result = await this.orchestrator.delegateTask('guardmon', {
                    action: 'test',
                    target: params.module
                });
                
                return {
                    success: result.passed,
                    tests: result.tests,
                    coverage: result.coverage
                };
            },
            preconditions: [{ type: 'code-written', value: true }],
            effects: [{ type: 'code-tested', value: true }]
        });
        
        // Operador: Deploy
        this.operatorLibrary.set('deploy', {
            type: 'primitive',
            execute: async (params) => {
                console.log(`🚀 Fazendo deploy: ${params.version}`);
                
                // Simular deploy
                return {
                    success: true,
                    deployed: true,
                    version: params.version,
                    timestamp: Date.now()
                };
            },
            preconditions: [
                { type: 'code-tested', value: true },
                { type: 'all-tests-passing', value: true }
            ],
            effects: [{ type: 'deployed', value: true }]
        });
    }
    
    registerDecompositionMethods() {
        // Método: Desenvolver Feature (TDD)
        this.methodLibrary.set('develop-feature-tdd', {
            task: 'develop-feature',
            preconditions: [{ type: 'tdd-enabled', value: true }],
            subtasks: [
                { task: 'write-tests', parameters: ['feature-spec'] },
                { task: 'write-code', parameters: ['feature-spec'] },
                { task: 'test-code', parameters: ['feature-module'] },
                { task: 'refactor-if-needed', parameters: ['feature-module'] }
            ]
        });
        
        // Método: Desenvolver Feature (Tradicional)
        this.methodLibrary.set('develop-feature-traditional', {
            task: 'develop-feature',
            preconditions: [],
            subtasks: [
                { task: 'analyze-requirements', parameters: ['feature-spec'] },
                { task: 'write-code', parameters: ['feature-spec'] },
                { task: 'test-code', parameters: ['feature-module'] },
                { task: 'document', parameters: ['feature-module'] }
            ]
        });
        
        // Método: Corrigir Bug (Com Análise)
        this.methodLibrary.set('fix-bug-with-analysis', {
            task: 'fix-bug',
            preconditions: [],
            subtasks: [
                { task: 'analyze-code', parameters: ['bug-location'] },
                { task: 'identify-root-cause', parameters: ['bug-id'] },
                { task: 'write-fix', parameters: ['bug-id'] },
                { task: 'test-fix', parameters: ['bug-id'] },
                { task: 'verify-no-regression', parameters: ['bug-id'] }
            ]
        });
        
        // Método: Otimizar Performance (Profile-Guided)
        this.methodLibrary.set('optimize-profile-guided', {
            task: 'optimize-performance',
            preconditions: [{ type: 'profiler-available', value: true }],
            subtasks: [
                { task: 'profile-code', parameters: ['component'] },
                { task: 'identify-bottlenecks', parameters: ['profile-data'] },
                { task: 'optimize-bottlenecks', parameters: ['bottlenecks'] },
                { task: 'verify-improvement', parameters: ['component'] }
            ]
        });
    }
    
    // Planejamento HTN
    async planHTN(goal, worldState) {
        console.log(`\n📝 Planejando para alcançar: ${goal.task}`);
        
        const plan = [];
        const agenda = [goal];
        this.worldState = new Map(worldState);
        
        while (agenda.length > 0) {
            const task = agenda.shift();
            
            if (this.isPrimitive(task)) {
                // Tarefa primitiva - adicionar ao plano
                plan.push(task);
            } else {
                // Tarefa composta - decompor
                const methods = this.findApplicableMethods(task);
                
                if (methods.length === 0) {
                    // Nenhum método aplicável - usar LLM
                    const llmPlan = await this.planWithLLM(task);
                    agenda.unshift(...llmPlan);
                } else {
                    // Escolher melhor método
                    const method = await this.selectBestMethod(methods, task);
                    
                    // Adicionar subtarefas à agenda
                    const subtasks = this.instantiateSubtasks(method, task);
                    agenda.unshift(...subtasks);
                }
            }
        }
        
        return plan;
    }
    
    isPrimitive(task) {
        const taskDef = this.taskLibrary.get(task.task) || 
                       this.operatorLibrary.get(task.task);
        return taskDef && taskDef.type === 'primitive';
    }
    
    findApplicableMethods(task) {
        const applicable = [];
        
        for (const [name, method] of this.methodLibrary) {
            if (method.task === task.task && 
                this.checkPreconditions(method.preconditions)) {
                applicable.push(method);
            }
        }
        
        return applicable;
    }
    
    checkPreconditions(preconditions) {
        for (const precond of preconditions) {
            const value = this.worldState.get(precond.type);
            if (value !== precond.value) {
                return false;
            }
        }
        return true;
    }
    
    async selectBestMethod(methods, task) {
        // Usar LLM para avaliar qual método é mais apropriado
        if (this.llmAdapter) {
            const evaluation = await this.llmAdapter.evaluate({
                task,
                methods,
                context: this.worldState
            });
            
            return methods.find(m => m.name === evaluation.bestMethod) || methods[0];
        }
        
        // Fallback: escolher primeiro método aplicável
        return methods[0];
    }
    
    instantiateSubtasks(method, parentTask) {
        return method.subtasks.map(subtask => ({
            ...subtask,
            parent: parentTask.task,
            context: parentTask.context
        }));
    }
    
    // Planejamento com LLM quando HTN falha
    async planWithLLM(task) {
        console.log(`🤖 Usando LLM para planejar: ${task.task}`);
        
        // Preparar contexto para LLM
        const context = {
            task: task.task,
            parameters: task.parameters,
            worldState: Array.from(this.worldState.entries()),
            availableOperators: Array.from(this.operatorLibrary.keys()),
            recentHistory: this.planHistory.slice(-5)
        };
        
        // Gerar plano com LLM
        const llmPlan = await this.generatePlanWithLLM(context);
        
        // Validar e converter plano LLM para formato HTN
        return this.validateAndConvertLLMPlan(llmPlan);
    }
    
    async generateCodeWithLLM(params) {
        // Simular geração de código com LLM
        const prompt = `
Gere código para: ${params.description}
Linguagem: ${params.language || 'JavaScript'}
Contexto: ${params.context || 'Digimundo ecosystem'}
        `;
        
        // Aqui integraria com Ollama/LLM real
        console.log(`🤖 Gerando código com LLM...`);
        
        // Por enquanto, retornar código de exemplo
        return `
// Generated by LLM
function ${params.functionName || 'generatedFunction'}() {
    // TODO: Implement ${params.description}
    console.log('Function generated by HTN+LLM planner');
}
        `;
    }
    
    async generatePlanWithLLM(context) {
        // Simular geração de plano com LLM
        console.log(`🤖 LLM gerando plano para: ${context.task}`);
        
        // Por enquanto, retornar plano simples
        return [
            { task: 'analyze-code', parameters: context.parameters },
            { task: 'write-code', parameters: context.parameters },
            { task: 'test-code', parameters: context.parameters }
        ];
    }
    
    validateAndConvertLLMPlan(llmPlan) {
        const validatedPlan = [];
        
        for (const step of llmPlan) {
            // Verificar se operador existe
            if (this.operatorLibrary.has(step.task) || 
                this.taskLibrary.has(step.task)) {
                validatedPlan.push(step);
            } else {
                // Tentar mapear para operador conhecido
                const mapped = this.mapToKnownOperator(step.task);
                if (mapped) {
                    validatedPlan.push({
                        ...step,
                        task: mapped,
                        original: step.task
                    });
                } else {
                    console.warn(`⚠️ Tarefa desconhecida: ${step.task}`);
                }
            }
        }
        
        return validatedPlan;
    }
    
    mapToKnownOperator(unknownTask) {
        // Mapeamento fuzzy de tarefas desconhecidas
        const mappings = {
            'code': 'write-code',
            'test': 'test-code',
            'analyze': 'analyze-code',
            'deploy': 'deploy',
            'fix': 'fix-bug',
            'optimize': 'optimize-performance'
        };
        
        for (const [key, value] of Object.entries(mappings)) {
            if (unknownTask.toLowerCase().includes(key)) {
                return value;
            }
        }
        
        return null;
    }
    
    // Executar plano
    async executePlan(plan) {
        console.log(`\n🏃 Executando plano com ${plan.length} ações...`);
        
        const results = [];
        
        for (const action of plan) {
            console.log(`\n▶️ Executando: ${action.task}`);
            
            const operator = this.operatorLibrary.get(action.task);
            if (operator && operator.execute) {
                try {
                    const result = await operator.execute(action.parameters || {});
                    results.push({
                        action: action.task,
                        success: result.success,
                        result
                    });
                    
                    // Atualizar estado do mundo
                    this.updateWorldState(operator.effects);
                    
                    if (!result.success) {
                        console.error(`❌ Ação falhou: ${action.task}`);
                        break;
                    }
                } catch (error) {
                    console.error(`❌ Erro ao executar ${action.task}:`, error);
                    results.push({
                        action: action.task,
                        success: false,
                        error: error.message
                    });
                    break;
                }
            } else {
                console.warn(`⚠️ Operador não encontrado: ${action.task}`);
            }
        }
        
        // Registrar no histórico
        this.planHistory.push({
            plan,
            results,
            timestamp: Date.now()
        });
        
        return results;
    }
    
    updateWorldState(effects) {
        for (const effect of effects) {
            this.worldState.set(effect.type, effect.value);
        }
    }
    
    // Aprendizado com experiência
    async learnFromExecution(plan, results) {
        const success = results.every(r => r.success);
        
        if (success) {
            // Reforçar métodos usados
            console.log('✅ Plano bem-sucedido! Reforçando métodos...');
            // TODO: Implementar reforço de métodos
        } else {
            // Aprender com falhas
            console.log('📝 Aprendendo com falhas...');
            const failurePoint = results.find(r => !r.success);
            
            // Analisar falha e ajustar métodos
            if (failurePoint) {
                console.log(`   Falha em: ${failurePoint.action}`);
                console.log(`   Motivo: ${failurePoint.error || 'Desconhecido'}`);
                
                // TODO: Implementar ajuste de métodos baseado em falhas
            }
        }
    }
}

module.exports = HTNLLMPlanner;