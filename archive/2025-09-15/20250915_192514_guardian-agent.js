/**
 * 🔐 GUARDIAN AGENT - Protetor de Agentes e Zero-Trust
 * Protege outros agentes, valida integridade e aplica políticas zero-trust
 * Implementa proteção em camadas e validação contínua
 */

const EventEmitter = require('events');
const crypto = require('crypto');

class GuardianAgent extends EventEmitter {
    constructor(id = crypto.randomUUID()) {
        super();
        this.id = id;
        this.name = `Guardian-${id.slice(0, 8)}`;
        this.type = 'guardian';
        this.purpose = 'Proteger agentes, validar integridade e aplicar zero-trust';
        
        // Estado do agente
        this.state = {
            active: true,
            mode: 'PROTECT', // PROTECT, VERIFY, ENFORCE, LOCKDOWN
            trustLevel: 'ZERO', // ZERO, LIMITED, VERIFIED, TRUSTED
            integrityStatus: 'INTACT'
        };
        
        // Sistema Zero-Trust
        this.zeroTrust = {
            principles: [
                'Never trust, always verify',
                'Assume breach',
                'Verify explicitly',
                'Least privilege access',
                'Continuous validation'
            ],
            policies: new Map(),
            verificationQueue: [],
            trustScores: new Map()
        };
        
        // Proteção de agentes
        this.agentProtection = {
            protectedAgents: new Map(),
            integrityHashes: new Map(),
            healthChecks: new Map(),
            isolatedAgents: new Set()
        };
        
        // Sistema de validação
        this.validationSystem = {
            validators: new Map(),
            validationRules: new Map(),
            validationHistory: [],
            anomalies: []
        };
        
        // Controle de acesso
        this.accessControl = {
            permissions: new Map(),
            activeTokens: new Map(),
            deniedRequests: [],
            accessLog: []
        };
        
        // Métricas
        this.metrics = {
            agentsProtected: 0,
            integrityChecks: 0,
            validationsPerformed: 0,
            threatsBlocked: 0,
            trustViolations: 0,
            falsePositives: 0
        };
        
        // Sistema de políticas
        this.policyEngine = {
            activePolicies: new Map(),
            policyViolations: [],
            enforcement: true
        };
        
        console.log(`🔐 ${this.name} ativado - Guardião zero-trust online`);
        console.log(`   Princípios: ${this.zeroTrust.principles[0]}`);
        
        this.initialize();
    }
    
    /**
     * Inicializa o agente guardião
     */
    initialize() {
        // Estabelecer políticas zero-trust
        this.establishZeroTrustPolicies();
        
        // Configurar validadores
        this.setupValidators();
        
        // Iniciar ciclos de proteção
        this.startProtectionCycles();
    }
    
    /**
     * Estabelece políticas zero-trust
     */
    establishZeroTrustPolicies() {
        console.log(`📜 ${this.name}: Estabelecendo políticas zero-trust...`);
        
        // Política de autenticação contínua
        this.zeroTrust.policies.set('CONTINUOUS_AUTH', {
            name: 'Autenticação Contínua',
            interval: 60000, // 1 minuto
            action: 'REVALIDATE',
            priority: 'HIGH'
        });
        
        // Política de privilégio mínimo
        this.zeroTrust.policies.set('LEAST_PRIVILEGE', {
            name: 'Privilégio Mínimo',
            maxPermissions: 3,
            defaultAccess: 'DENY',
            priority: 'CRITICAL'
        });
        
        // Política de verificação de integridade
        this.zeroTrust.policies.set('INTEGRITY_CHECK', {
            name: 'Verificação de Integridade',
            frequency: 30000, // 30 segundos
            hashAlgorithm: 'sha256',
            priority: 'HIGH'
        });
        
        // Política de isolamento automático
        this.zeroTrust.policies.set('AUTO_ISOLATION', {
            name: 'Isolamento Automático',
            trigger: 'ANOMALY_DETECTED',
            isolationTime: 300000, // 5 minutos
            priority: 'MEDIUM'
        });
        
        // Política de comunicação segura
        this.zeroTrust.policies.set('SECURE_COMM', {
            name: 'Comunicação Segura',
            encryption: 'REQUIRED',
            minKeyLength: 256,
            priority: 'CRITICAL'
        });
    }
    
    /**
     * Configura validadores
     */
    setupValidators() {
        console.log(`🔍 ${this.name}: Configurando validadores...`);
        
        // Validador de identidade
        this.validationSystem.validators.set('IDENTITY', {
            type: 'identity',
            validate: (agent) => this.validateIdentity(agent)
        });
        
        // Validador de comportamento
        this.validationSystem.validators.set('BEHAVIOR', {
            type: 'behavior',
            validate: (agent) => this.validateBehavior(agent)
        });
        
        // Validador de permissões
        this.validationSystem.validators.set('PERMISSIONS', {
            type: 'permissions',
            validate: (agent) => this.validatePermissions(agent)
        });
        
        // Validador de integridade
        this.validationSystem.validators.set('INTEGRITY', {
            type: 'integrity',
            validate: (agent) => this.validateIntegrity(agent)
        });
    }
    
    /**
     * Inicia ciclos de proteção
     */
    startProtectionCycles() {
        // Verificação de integridade (30s)
        setInterval(() => this.performIntegrityChecks(), 30000);
        
        // Validação zero-trust (1min)
        setInterval(() => this.performZeroTrustValidation(), 60000);
        
        // Monitoramento de saúde (10s)
        setInterval(() => this.monitorAgentHealth(), 10000);
        
        // Aplicação de políticas (5s)
        setInterval(() => this.enforcePolicies(), 5000);
    }
    
    /**
     * Protege um agente
     */
    async protectAgent(agent) {
        console.log(`\n🛡️ ${this.name}: Protegendo agente ${agent.name}`);
        
        // Calcular hash de integridade inicial
        const integrityHash = this.calculateIntegrityHash(agent);
        
        // Registrar agente protegido
        this.agentProtection.protectedAgents.set(agent.id, {
            agent,
            protectionStart: new Date(),
            integrityHash,
            trustScore: 0,
            status: 'PROTECTED'
        });
        
        // Salvar hash de integridade
        this.agentProtection.integrityHashes.set(agent.id, integrityHash);
        
        // Estabelecer monitoramento de saúde
        this.agentProtection.healthChecks.set(agent.id, {
            lastCheck: new Date(),
            status: 'HEALTHY',
            issues: []
        });
        
        // Aplicar políticas zero-trust
        await this.applyZeroTrustToAgent(agent);
        
        // Atualizar métricas
        this.metrics.agentsProtected++;
        
        console.log(`   ✅ Agente ${agent.name} sob proteção`);
        console.log(`   Hash de integridade: ${integrityHash.slice(0, 16)}...`);
        
        // Emitir evento
        this.emit('agent-protected', {
            agentId: agent.id,
            agentName: agent.name,
            integrityHash,
            timestamp: new Date()
        });
        
        return {
            success: true,
            integrityHash,
            protectionId: crypto.randomUUID()
        };
    }
    
    /**
     * Calcula hash de integridade
     */
    calculateIntegrityHash(agent) {
        const data = JSON.stringify({
            id: agent.id,
            type: agent.type,
            purpose: agent.purpose,
            capabilities: agent.capabilities || {},
            timestamp: Date.now()
        });
        
        return crypto.createHash('sha256').update(data).digest('hex');
    }
    
    /**
     * Aplica zero-trust ao agente
     */
    async applyZeroTrustToAgent(agent) {
        console.log(`🔒 Aplicando zero-trust ao agente ${agent.name}`);
        
        // Iniciar com score de confiança zero
        this.zeroTrust.trustScores.set(agent.id, 0);
        
        // Configurar permissões mínimas
        this.accessControl.permissions.set(agent.id, {
            read: false,
            write: false,
            execute: false,
            communicate: false
        });
        
        // Adicionar à fila de verificação
        this.zeroTrust.verificationQueue.push({
            agentId: agent.id,
            priority: 'HIGH',
            timestamp: new Date()
        });
        
        // Criar token de acesso temporário
        const token = this.createAccessToken(agent.id, 300000); // 5 minutos
        
        return token;
    }
    
    /**
     * Cria token de acesso
     */
    createAccessToken(agentId, duration) {
        const token = {
            id: crypto.randomUUID(),
            agentId,
            created: new Date(),
            expires: new Date(Date.now() + duration),
            permissions: ['READ'],
            used: 0
        };
        
        this.accessControl.activeTokens.set(token.id, token);
        
        // Auto-expirar token
        setTimeout(() => {
            this.revokeToken(token.id);
        }, duration);
        
        return token;
    }
    
    /**
     * Verifica integridade dos agentes
     */
    performIntegrityChecks() {
        if (!this.state.active) return;
        
        console.log(`\n🔍 ${this.name}: Verificando integridade dos agentes...`);
        
        for (const [agentId, protection] of this.agentProtection.protectedAgents) {
            const currentHash = this.calculateIntegrityHash(protection.agent);
            const originalHash = this.agentProtection.integrityHashes.get(agentId);
            
            if (currentHash !== originalHash) {
                console.log(`⚠️ VIOLAÇÃO DE INTEGRIDADE: ${protection.agent.name}`);
                
                // Isolar agente comprometido
                this.isolateAgent(agentId, 'INTEGRITY_VIOLATION');
                
                // Emitir alerta
                this.emit('integrity-violation', {
                    agentId,
                    agentName: protection.agent.name,
                    originalHash,
                    currentHash,
                    timestamp: new Date()
                });
                
                this.metrics.trustViolations++;
            }
            
            this.metrics.integrityChecks++;
        }
    }
    
    /**
     * Validação zero-trust
     */
    performZeroTrustValidation() {
        console.log(`\n🔐 ${this.name}: Executando validação zero-trust...`);
        
        // Processar fila de verificação
        while (this.zeroTrust.verificationQueue.length > 0) {
            const verification = this.zeroTrust.verificationQueue.shift();
            this.verifyAgent(verification.agentId);
        }
        
        // Revalidar todos os agentes
        for (const [agentId, protection] of this.agentProtection.protectedAgents) {
            const trustScore = this.calculateTrustScore(protection.agent);
            this.zeroTrust.trustScores.set(agentId, trustScore);
            
            console.log(`   Agente ${protection.agent.name}: Trust ${(trustScore * 100).toFixed(1)}%`);
            
            // Ajustar permissões baseado no trust score
            this.adjustPermissions(agentId, trustScore);
        }
        
        this.metrics.validationsPerformed++;
    }
    
    /**
     * Verifica agente específico
     */
    async verifyAgent(agentId) {
        const protection = this.agentProtection.protectedAgents.get(agentId);
        if (!protection) return;
        
        const agent = protection.agent;
        const validations = [];
        
        // Executar todas as validações
        for (const [name, validator] of this.validationSystem.validators) {
            const result = await validator.validate(agent);
            validations.push({
                type: name,
                passed: result.passed,
                score: result.score,
                details: result.details
            });
        }
        
        // Calcular score geral
        const overallScore = validations.reduce((sum, v) => sum + v.score, 0) / validations.length;
        
        // Atualizar trust score
        this.zeroTrust.trustScores.set(agentId, overallScore);
        
        // Registrar na história
        this.validationSystem.validationHistory.push({
            agentId,
            validations,
            overallScore,
            timestamp: new Date()
        });
        
        return {
            agentId,
            trustScore: overallScore,
            validations
        };
    }
    
    /**
     * Valida identidade
     */
    validateIdentity(agent) {
        // Verificar se o agente é quem diz ser
        const isValid = agent.id && agent.name && agent.type;
        
        return {
            passed: isValid,
            score: isValid ? 1.0 : 0,
            details: 'Identity validation'
        };
    }
    
    /**
     * Valida comportamento
     */
    validateBehavior(agent) {
        // Analisar comportamento do agente
        const protection = this.agentProtection.protectedAgents.get(agent.id);
        
        if (!protection) {
            return { passed: false, score: 0, details: 'No protection record' };
        }
        
        // Verificar anomalias comportamentais
        const hasAnomalies = this.validationSystem.anomalies.some(
            a => a.agentId === agent.id
        );
        
        return {
            passed: !hasAnomalies,
            score: hasAnomalies ? 0.3 : 0.9,
            details: hasAnomalies ? 'Behavioral anomalies detected' : 'Normal behavior'
        };
    }
    
    /**
     * Valida permissões
     */
    validatePermissions(agent) {
        const permissions = this.accessControl.permissions.get(agent.id);
        
        if (!permissions) {
            return { passed: false, score: 0, details: 'No permissions set' };
        }
        
        // Verificar se está seguindo princípio de privilégio mínimo
        const permissionCount = Object.values(permissions).filter(p => p).length;
        const isMinimal = permissionCount <= 2;
        
        return {
            passed: isMinimal,
            score: isMinimal ? 1.0 : 0.5,
            details: `${permissionCount} permissions active`
        };
    }
    
    /**
     * Valida integridade
     */
    validateIntegrity(agent) {
        const currentHash = this.calculateIntegrityHash(agent);
        const originalHash = this.agentProtection.integrityHashes.get(agent.id);
        
        const isIntact = currentHash === originalHash;
        
        return {
            passed: isIntact,
            score: isIntact ? 1.0 : 0,
            details: isIntact ? 'Integrity intact' : 'Integrity compromised'
        };
    }
    
    /**
     * Calcula score de confiança
     */
    calculateTrustScore(agent) {
        let score = 0;
        let factors = 0;
        
        // Fator: Tempo de proteção
        const protection = this.agentProtection.protectedAgents.get(agent.id);
        if (protection) {
            const uptime = Date.now() - protection.protectionStart;
            score += Math.min(1, uptime / 3600000); // Max 1 após 1 hora
            factors++;
        }
        
        // Fator: Validações passadas
        const history = this.validationSystem.validationHistory.filter(
            v => v.agentId === agent.id
        );
        if (history.length > 0) {
            const avgScore = history.reduce((sum, v) => sum + v.overallScore, 0) / history.length;
            score += avgScore;
            factors++;
        }
        
        // Fator: Ausência de violações
        const violations = this.policyEngine.policyViolations.filter(
            v => v.agentId === agent.id
        );
        score += violations.length === 0 ? 1 : 0;
        factors++;
        
        return factors > 0 ? score / factors : 0;
    }
    
    /**
     * Ajusta permissões baseado em trust score
     */
    adjustPermissions(agentId, trustScore) {
        const permissions = this.accessControl.permissions.get(agentId);
        if (!permissions) return;
        
        // Permissões baseadas em trust score
        if (trustScore >= 0.9) {
            permissions.read = true;
            permissions.write = true;
            permissions.execute = true;
            permissions.communicate = true;
        } else if (trustScore >= 0.7) {
            permissions.read = true;
            permissions.write = false;
            permissions.execute = true;
            permissions.communicate = true;
        } else if (trustScore >= 0.5) {
            permissions.read = true;
            permissions.write = false;
            permissions.execute = false;
            permissions.communicate = true;
        } else {
            // Trust baixo - permissões mínimas
            permissions.read = true;
            permissions.write = false;
            permissions.execute = false;
            permissions.communicate = false;
        }
        
        this.accessControl.permissions.set(agentId, permissions);
    }
    
    /**
     * Monitora saúde dos agentes
     */
    monitorAgentHealth() {
        for (const [agentId, protection] of this.agentProtection.protectedAgents) {
            const health = this.checkAgentHealth(protection.agent);
            
            this.agentProtection.healthChecks.set(agentId, {
                lastCheck: new Date(),
                status: health.status,
                issues: health.issues
            });
            
            if (health.status === 'UNHEALTHY') {
                console.log(`⚠️ ${this.name}: Agente ${protection.agent.name} não saudável`);
                
                // Aplicar remediação
                this.remediateAgent(agentId, health.issues);
            }
        }
    }
    
    /**
     * Verifica saúde do agente
     */
    checkAgentHealth(agent) {
        const issues = [];
        let status = 'HEALTHY';
        
        // Verificar estado
        if (!agent.state || !agent.state.active) {
            issues.push('Agent inactive');
            status = 'UNHEALTHY';
        }
        
        // Verificar métricas (se disponíveis)
        if (agent.metrics) {
            if (agent.metrics.errors > 100) {
                issues.push('High error rate');
                status = 'DEGRADED';
            }
        }
        
        return { status, issues };
    }
    
    /**
     * Remedia agente com problemas
     */
    remediateAgent(agentId, issues) {
        console.log(`🔧 ${this.name}: Remediando agente...`);
        
        for (const issue of issues) {
            switch (issue) {
                case 'Agent inactive':
                    // Tentar reativar
                    this.reactivateAgent(agentId);
                    break;
                    
                case 'High error rate':
                    // Resetar ou reiniciar
                    this.resetAgent(agentId);
                    break;
                    
                default:
                    // Isolar para investigação
                    this.isolateAgent(agentId, 'HEALTH_ISSUES');
            }
        }
    }
    
    /**
     * Isola agente
     */
    isolateAgent(agentId, reason) {
        console.log(`🔒 ${this.name}: Isolando agente ${agentId} - Razão: ${reason}`);
        
        // Adicionar ao conjunto de isolados
        this.agentProtection.isolatedAgents.add(agentId);
        
        // Revogar todas as permissões
        this.accessControl.permissions.set(agentId, {
            read: false,
            write: false,
            execute: false,
            communicate: false
        });
        
        // Atualizar status
        const protection = this.agentProtection.protectedAgents.get(agentId);
        if (protection) {
            protection.status = 'ISOLATED';
        }
        
        // Emitir evento
        this.emit('agent-isolated', {
            agentId,
            reason,
            timestamp: new Date()
        });
    }
    
    /**
     * Aplica políticas
     */
    enforcePolicies() {
        for (const [name, policy] of this.zeroTrust.policies) {
            this.enforcePolicy(name, policy);
        }
    }
    
    /**
     * Aplica política específica
     */
    enforcePolicy(name, policy) {
        switch (name) {
            case 'CONTINUOUS_AUTH':
                // Revalidar agentes periodicamente
                for (const [agentId] of this.agentProtection.protectedAgents) {
                    this.zeroTrust.verificationQueue.push({
                        agentId,
                        priority: policy.priority,
                        timestamp: new Date()
                    });
                }
                break;
                
            case 'LEAST_PRIVILEGE':
                // Verificar e ajustar permissões
                for (const [agentId, permissions] of this.accessControl.permissions) {
                    const count = Object.values(permissions).filter(p => p).length;
                    if (count > policy.maxPermissions) {
                        this.reportPolicyViolation(agentId, name, 'Too many permissions');
                    }
                }
                break;
        }
    }
    
    /**
     * Reporta violação de política
     */
    reportPolicyViolation(agentId, policyName, details) {
        const violation = {
            agentId,
            policyName,
            details,
            timestamp: new Date()
        };
        
        this.policyEngine.policyViolations.push(violation);
        
        console.log(`⚠️ Violação de política: ${policyName} por agente ${agentId}`);
        
        this.emit('policy-violation', violation);
    }
    
    /**
     * Reativa agente
     */
    reactivateAgent(agentId) {
        const protection = this.agentProtection.protectedAgents.get(agentId);
        if (protection && protection.agent.state) {
            protection.agent.state.active = true;
            console.log(`✅ Agente ${agentId} reativado`);
        }
    }
    
    /**
     * Reseta agente
     */
    resetAgent(agentId) {
        const protection = this.agentProtection.protectedAgents.get(agentId);
        if (protection && protection.agent.metrics) {
            protection.agent.metrics.errors = 0;
            console.log(`♻️ Agente ${agentId} resetado`);
        }
    }
    
    /**
     * Revoga token
     */
    revokeToken(tokenId) {
        this.accessControl.activeTokens.delete(tokenId);
    }
    
    /**
     * Recebe comando seguro do orquestrador
     */
    receiveSecureCommand(message) {
        console.log(`📨 ${this.name}: Comando recebido do orquestrador`);
        
        // Em produção, descriptografaria e validaria
        // Processar comando...
    }
    
    /**
     * Status do agente
     */
    getStatus() {
        return {
            id: this.id,
            name: this.name,
            type: this.type,
            purpose: this.purpose,
            state: this.state,
            metrics: this.metrics,
            protection: {
                agentsProtected: this.agentProtection.protectedAgents.size,
                agentsIsolated: this.agentProtection.isolatedAgents.size,
                integrityHashes: this.agentProtection.integrityHashes.size
            },
            zeroTrust: {
                policies: this.zeroTrust.policies.size,
                verificationQueue: this.zeroTrust.verificationQueue.length,
                avgTrustScore: this.calculateAvgTrustScore()
            },
            validation: {
                validators: this.validationSystem.validators.size,
                historySize: this.validationSystem.validationHistory.length,
                anomalies: this.validationSystem.anomalies.length
            },
            access: {
                activeTokens: this.accessControl.activeTokens.size,
                deniedRequests: this.accessControl.deniedRequests.length
            }
        };
    }
    
    /**
     * Calcula trust score médio
     */
    calculateAvgTrustScore() {
        if (this.zeroTrust.trustScores.size === 0) return 0;
        
        let sum = 0;
        for (const score of this.zeroTrust.trustScores.values()) {
            sum += score;
        }
        
        return sum / this.zeroTrust.trustScores.size;
    }
}

module.exports = GuardianAgent;