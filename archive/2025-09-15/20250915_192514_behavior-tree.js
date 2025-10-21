/**
 * 🌳 BEHAVIOR TREE - Sistema de Árvore de Comportamento para Decisões
 * Implementa árvore de comportamento para tomada de decisão estratégica
 */

// Estados de execução
const SUCCESS = Symbol('SUCCESS');
const FAILURE = Symbol('FAILURE');
const RUNNING = Symbol('RUNNING');

/**
 * Nó base da árvore de comportamento
 */
class Node {
    constructor(name = 'Node') {
        this.name = name;
        this.status = null;
        this.parent = null;
        this.children = [];
    }
    
    tick() {
        throw new Error('tick() deve ser implementado pela subclasse');
    }
    
    reset() {
        this.status = null;
        for (const child of this.children) {
            child.reset();
        }
    }
    
    addChild(child) {
        child.parent = this;
        this.children.push(child);
        return this;
    }
}

/**
 * Nó Sequence - Executa filhos em sequência até um falhar
 */
class Sequence extends Node {
    constructor(name = 'Sequence', ...children) {
        super(name);
        this.children = children;
        children.forEach(child => child.parent = this);
        this.currentChild = 0;
    }
    
    tick() {
        // Se já processou todos os filhos com sucesso
        if (this.currentChild >= this.children.length) {
            this.status = SUCCESS;
            this.currentChild = 0;
            return this.status;
        }
        
        // Processar filho atual
        const child = this.children[this.currentChild];
        const status = child.tick();
        
        if (status === FAILURE) {
            this.status = FAILURE;
            this.currentChild = 0;
            return this.status;
        }
        
        if (status === SUCCESS) {
            this.currentChild++;
            
            // Se processou todos com sucesso
            if (this.currentChild >= this.children.length) {
                this.status = SUCCESS;
                this.currentChild = 0;
                return this.status;
            }
            
            // Continuar com próximo filho
            return RUNNING;
        }
        
        // Child ainda está rodando
        return RUNNING;
    }
    
    reset() {
        super.reset();
        this.currentChild = 0;
    }
}

/**
 * Nó Selector - Executa filhos até um ter sucesso
 */
class Selector extends Node {
    constructor(name = 'Selector', ...children) {
        super(name);
        this.children = children;
        children.forEach(child => child.parent = this);
        this.currentChild = 0;
    }
    
    tick() {
        // Se já processou todos os filhos sem sucesso
        if (this.currentChild >= this.children.length) {
            this.status = FAILURE;
            this.currentChild = 0;
            return this.status;
        }
        
        // Processar filho atual
        const child = this.children[this.currentChild];
        const status = child.tick();
        
        if (status === SUCCESS) {
            this.status = SUCCESS;
            this.currentChild = 0;
            return this.status;
        }
        
        if (status === FAILURE) {
            this.currentChild++;
            
            // Se todos falharam
            if (this.currentChild >= this.children.length) {
                this.status = FAILURE;
                this.currentChild = 0;
                return this.status;
            }
            
            // Tentar próximo filho
            return RUNNING;
        }
        
        // Child ainda está rodando
        return RUNNING;
    }
    
    reset() {
        super.reset();
        this.currentChild = 0;
    }
}

/**
 * Nó Parallel - Executa todos os filhos em paralelo
 */
class Parallel extends Node {
    constructor(name = 'Parallel', successThreshold = 1, ...children) {
        super(name);
        this.children = children;
        this.successThreshold = successThreshold;
        children.forEach(child => child.parent = this);
    }
    
    tick() {
        let successCount = 0;
        let failureCount = 0;
        let runningCount = 0;
        
        // Executar todos os filhos
        for (const child of this.children) {
            const status = child.tick();
            
            if (status === SUCCESS) {
                successCount++;
            } else if (status === FAILURE) {
                failureCount++;
            } else {
                runningCount++;
            }
        }
        
        // Verificar condições de término
        if (successCount >= this.successThreshold) {
            this.status = SUCCESS;
            return this.status;
        }
        
        if (failureCount > this.children.length - this.successThreshold) {
            this.status = FAILURE;
            return this.status;
        }
        
        // Ainda tem filhos rodando
        return RUNNING;
    }
}

/**
 * Nó Action - Executa uma ação específica
 */
class Action extends Node {
    constructor(fn, name = 'Action') {
        super(name);
        this.fn = fn;
    }
    
    tick() {
        try {
            this.status = this.fn();
            return this.status;
        } catch (error) {
            console.error(`Erro na ação ${this.name}:`, error);
            this.status = FAILURE;
            return this.status;
        }
    }
}

/**
 * Nó Condition - Verifica uma condição
 */
class Condition extends Node {
    constructor(fn, name = 'Condition') {
        super(name);
        this.fn = fn;
    }
    
    tick() {
        try {
            const result = this.fn();
            this.status = result ? SUCCESS : FAILURE;
            return this.status;
        } catch (error) {
            console.error(`Erro na condição ${this.name}:`, error);
            this.status = FAILURE;
            return this.status;
        }
    }
}

/**
 * Nó Decorator - Modifica comportamento de um filho
 */
class Decorator extends Node {
    constructor(name = 'Decorator', child = null) {
        super(name);
        if (child) {
            this.addChild(child);
        }
    }
}

/**
 * Decorator Inverter - Inverte resultado do filho
 */
class Inverter extends Decorator {
    constructor(child) {
        super('Inverter', child);
    }
    
    tick() {
        if (this.children.length === 0) {
            return FAILURE;
        }
        
        const status = this.children[0].tick();
        
        if (status === SUCCESS) {
            this.status = FAILURE;
        } else if (status === FAILURE) {
            this.status = SUCCESS;
        } else {
            this.status = status;
        }
        
        return this.status;
    }
}

/**
 * Decorator Repeater - Repete filho N vezes
 */
class Repeater extends Decorator {
    constructor(times, child) {
        super('Repeater', child);
        this.times = times;
        this.count = 0;
    }
    
    tick() {
        if (this.children.length === 0) {
            return FAILURE;
        }
        
        while (this.count < this.times) {
            const status = this.children[0].tick();
            
            if (status === RUNNING) {
                return RUNNING;
            }
            
            if (status === FAILURE) {
                this.count = 0;
                this.status = FAILURE;
                return this.status;
            }
            
            this.count++;
        }
        
        this.count = 0;
        this.status = SUCCESS;
        return this.status;
    }
    
    reset() {
        super.reset();
        this.count = 0;
    }
}

/**
 * Decorator RetryUntilSuccess - Repete até ter sucesso
 */
class RetryUntilSuccess extends Decorator {
    constructor(maxTries, child) {
        super('RetryUntilSuccess', child);
        this.maxTries = maxTries;
        this.tries = 0;
    }
    
    tick() {
        if (this.children.length === 0) {
            return FAILURE;
        }
        
        while (this.tries < this.maxTries) {
            const status = this.children[0].tick();
            
            if (status === SUCCESS) {
                this.tries = 0;
                this.status = SUCCESS;
                return this.status;
            }
            
            if (status === RUNNING) {
                return RUNNING;
            }
            
            this.tries++;
        }
        
        this.tries = 0;
        this.status = FAILURE;
        return this.status;
    }
    
    reset() {
        super.reset();
        this.tries = 0;
    }
}

/**
 * Nó Wait - Espera por um tempo determinado
 */
class Wait extends Node {
    constructor(milliseconds, name = 'Wait') {
        super(name);
        this.milliseconds = milliseconds;
        this.startTime = null;
    }
    
    tick() {
        if (!this.startTime) {
            this.startTime = Date.now();
            return RUNNING;
        }
        
        const elapsed = Date.now() - this.startTime;
        
        if (elapsed >= this.milliseconds) {
            this.startTime = null;
            this.status = SUCCESS;
            return this.status;
        }
        
        return RUNNING;
    }
    
    reset() {
        super.reset();
        this.startTime = null;
    }
}

/**
 * Árvore de Comportamento principal
 */
class BehaviorTree {
    constructor(root) {
        this.root = root;
        this.blackboard = new Map(); // Memória compartilhada
    }
    
    tick() {
        return this.root.tick();
    }
    
    reset() {
        this.root.reset();
    }
    
    // Métodos do blackboard
    set(key, value) {
        this.blackboard.set(key, value);
    }
    
    get(key) {
        return this.blackboard.get(key);
    }
    
    has(key) {
        return this.blackboard.has(key);
    }
    
    delete(key) {
        return this.blackboard.delete(key);
    }
    
    clear() {
        this.blackboard.clear();
    }
}

// Funções utilitárias
function createSequence(name, ...children) {
    return new Sequence(name, ...children);
}

function createSelector(name, ...children) {
    return new Selector(name, ...children);
}

function createParallel(name, threshold, ...children) {
    return new Parallel(name, threshold, ...children);
}

function createAction(fn, name) {
    return new Action(fn, name);
}

function createCondition(fn, name) {
    return new Condition(fn, name);
}

module.exports = {
    // Classes
    BehaviorTree,
    Node,
    Sequence,
    Selector,
    Parallel,
    Action,
    Condition,
    Decorator,
    Inverter,
    Repeater,
    RetryUntilSuccess,
    Wait,
    
    // Estados
    SUCCESS,
    FAILURE,
    RUNNING,
    
    // Funções utilitárias
    createSequence,
    createSelector,
    createParallel,
    createAction,
    createCondition
};