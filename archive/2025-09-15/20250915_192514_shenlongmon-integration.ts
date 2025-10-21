#!/usr/bin/env node

/**
 * 🐉 SHENLONGMON INTEGRATION WITH DIGIMUNDO ECOSYSTEM
 * Integrates ChatGPT's superior Shenlongmon implementation with the Supreme Orchestrator
 */

import { EventEmitter } from 'events';
import { ShenlongmonActor, ShenlongmonSupervisor } from '../agents/shenlongmon/shenlongmon-supreme';

interface DigimonMessage {
    from: string;
    to: string;
    type: 'QUESTION' | 'KNOWLEDGE' | 'COLLABORATION' | 'EMERGENCY';
    content: any;
    priority?: number;
    timestamp?: Date;
}

interface OrchestratorInterface {
    emit(event: string, data: any): void;
    on(event: string, handler: Function): void;
    digilibrary: any;
    iaTown: any;
    personalitySystem: any;
    sharedMemory: Map<string, any>;
}

/**
 * Integration layer between Shenlongmon and Supreme Orchestrator
 */
export class ShenlongmonIntegration extends EventEmitter {
    private supervisor: ShenlongmonSupervisor;
    private orchestrator: OrchestratorInterface;
    private messageQueue: DigimonMessage[] = [];
    private isProcessing: boolean = false;
    
    // Integration metrics
    private metrics = {
        totalQuestions: 0,
        awakenCount: 0,
        hibernateCount: 0,
        collaborations: 0,
        knowledgeShared: 0,
        avgResponseTime: 0,
        lastAwaken: null as Date | null
    };
    
    constructor(orchestrator: OrchestratorInterface) {
        super();
        this.orchestrator = orchestrator;
        this.supervisor = new ShenlongmonSupervisor();
        
        this.setupIntegration();
        this.setupEventHandlers();
        this.setupTriageSystem();
    }
    
    /**
     * Setup integration with orchestrator
     */
    private setupIntegration() {
        // Register Shenlongmon with the orchestrator
        this.orchestrator.emit('register-digimon', {
            name: 'Shenlongmon',
            role: 'supreme-wisdom',
            model: 'llama3.3:70b',
            capabilities: [
                'ultimate-knowledge',
                'complex-reasoning',
                'meta-learning',
                'knowledge-distillation',
                'architectural-decisions'
            ],
            status: 'hibernating',
            integration: 'chatgpt-superior-architecture'
        });
        
        // Setup communication channel
        this.orchestrator.on('message-to-Shenlongmon', async (message: DigimonMessage) => {
            await this.handleIncomingMessage(message);
        });
        
        // Setup knowledge sharing with Digilibrary
        this.on('knowledge-discovered', async (knowledge) => {
            await this.shareKnowledgeWithDigilibrary(knowledge);
        });
        
        // Setup social interactions with IA Town
        this.on('shenlongmon-awakened', () => {
            this.orchestrator.iaTown?.createSocialInteraction(
                'Shenlongmon',
                'all',
                'ANNOUNCEMENT',
                'The great dragon has awakened to share wisdom!'
            );
        });
    }
    
    /**
     * Setup event handlers for Shenlongmon events
     */
    private setupEventHandlers() {
        // Handle awakening events
        this.supervisor.on('actor:awakened', (actorId: string) => {
            this.metrics.awakenCount++;
            this.metrics.lastAwaken = new Date();
            this.emit('shenlongmon-awakened');
            
            // Notify orchestrator
            this.orchestrator.emit('digimon-status-change', {
                name: 'Shenlongmon',
                status: 'active',
                actorId
            });
        });
        
        // Handle hibernation events
        this.supervisor.on('actor:hibernated', (actorId: string) => {
            this.metrics.hibernateCount++;
            this.emit('shenlongmon-hibernated');
            
            // Notify orchestrator
            this.orchestrator.emit('digimon-status-change', {
                name: 'Shenlongmon',
                status: 'hibernating',
                actorId
            });
        });
        
        // Handle knowledge events
        this.supervisor.on('knowledge:extracted', async (knowledge: any) => {
            this.metrics.knowledgeShared++;
            await this.shareKnowledgeWithDigilibrary(knowledge);
        });
        
        // Handle errors
        this.supervisor.on('error', (error: Error) => {
            console.error('🐉❌ Shenlongmon Error:', error);
            this.orchestrator.emit('digimon-error', {
                name: 'Shenlongmon',
                error: error.message
            });
        });
    }
    
    /**
     * Setup 3-layer triage system
     */
    private setupTriageSystem() {
        // Layer 1: Heuristic filter
        this.heuristicFilter = {
            keywords: ['ultimate', 'critical', 'emergency', 'complex', 'architectural'],
            minComplexity: 0.7,
            requiresWisdom: ['meta-learning', 'system-design', 'evolution']
        };
        
        // Layer 2: Small LLM triage (using existing Digimons)
        this.smallLLMTriage = async (question: string): Promise<boolean> => {
            // Ask Analyzermon or another small Digimon if this needs Shenlongmon
            const triageResult = await this.orchestrator.emit('triage-request', {
                question,
                requester: 'Shenlongmon-Triage',
                models: ['Analyzermon', 'Optimizermon']
            });
            
            return triageResult?.needsShenlongmon || false;
        };
        
        // Layer 3: RAG system check
        this.ragSystemCheck = async (question: string): Promise<boolean> => {
            // Check if Digilibrary has sufficient knowledge
            const existingKnowledge = await this.orchestrator.digilibrary?.searchBooks(
                question.split(' ').slice(0, 5).join(' ')
            );
            
            // If no sufficient knowledge exists, wake Shenlongmon
            return !existingKnowledge || existingKnowledge.length === 0;
        };
    }
    
    /**
     * Handle incoming messages with triage
     */
    private async handleIncomingMessage(message: DigimonMessage) {
        this.metrics.totalQuestions++;
        
        // Add to queue
        this.messageQueue.push(message);
        
        // Process queue if not already processing
        if (!this.isProcessing) {
            await this.processMessageQueue();
        }
    }
    
    /**
     * Process message queue with intelligent triage
     */
    private async processMessageQueue() {
        if (this.isProcessing || this.messageQueue.length === 0) return;
        
        this.isProcessing = true;
        
        while (this.messageQueue.length > 0) {
            const message = this.messageQueue.shift()!;
            
            try {
                // Apply 3-layer triage
                const shouldAwaken = await this.triageDecision(message);
                
                if (shouldAwaken) {
                    // Wake Shenlongmon for this question
                    const startTime = Date.now();
                    
                    const response = await this.supervisor.processQuestion(
                        message.content.question || message.content,
                        {
                            requester: message.from,
                            priority: message.priority,
                            context: await this.gatherContext(message)
                        }
                    );
                    
                    // Update metrics
                    const responseTime = Date.now() - startTime;
                    this.metrics.avgResponseTime = 
                        (this.metrics.avgResponseTime * (this.metrics.awakenCount - 1) + responseTime) 
                        / this.metrics.awakenCount;
                    
                    // Send response back
                    this.orchestrator.emit(`message-to-${message.from}`, {
                        from: 'Shenlongmon',
                        to: message.from,
                        type: 'ANSWER',
                        content: {
                            answer: response,
                            processingTime: responseTime,
                            wisdomLevel: 'ULTIMATE'
                        }
                    });
                    
                    // Store in Digilibrary
                    await this.storeWisdom(message, response);
                    
                } else {
                    // Delegate to other Digimons
                    await this.delegateToOthers(message);
                }
                
            } catch (error) {
                console.error('Error processing message:', error);
                this.handleProcessingError(message, error as Error);
            }
        }
        
        this.isProcessing = false;
    }
    
    /**
     * Make triage decision using 3-layer system
     */
    private async triageDecision(message: DigimonMessage): Promise<boolean> {
        // Emergency or high priority always wakes Shenlongmon
        if (message.type === 'EMERGENCY' || (message.priority && message.priority > 9)) {
            return true;
        }
        
        const question = message.content.question || message.content;
        
        // Layer 1: Heuristic check
        const hasKeywords = this.heuristicFilter.keywords.some(
            keyword => question.toLowerCase().includes(keyword)
        );
        
        if (!hasKeywords) {
            return false; // Can be handled by others
        }
        
        // Layer 2: Small LLM triage
        const needsAdvanced = await this.smallLLMTriage(question);
        
        if (!needsAdvanced) {
            return false;
        }
        
        // Layer 3: RAG check
        const needsNewKnowledge = await this.ragSystemCheck(question);
        
        return needsNewKnowledge;
    }
    
    /**
     * Gather context for Shenlongmon
     */
    private async gatherContext(message: DigimonMessage) {
        const context: any = {
            requester: message.from,
            timestamp: message.timestamp || new Date(),
            relatedKnowledge: [],
            recentInteractions: [],
            systemState: {}
        };
        
        // Get related knowledge from Digilibrary
        if (this.orchestrator.digilibrary) {
            const keywords = (message.content.question || message.content)
                .split(' ')
                .filter((word: string) => word.length > 4)
                .slice(0, 3);
            
            for (const keyword of keywords) {
                const books = await this.orchestrator.digilibrary.searchBooks(keyword);
                context.relatedKnowledge.push(...books);
            }
        }
        
        // Get recent interactions from IA Town
        if (this.orchestrator.iaTown) {
            const interactions = this.orchestrator.iaTown.getRecentInteractions?.(
                message.from, 
                5
            );
            if (interactions) {
                context.recentInteractions = interactions;
            }
        }
        
        // Get system state
        context.systemState = {
            totalDigimons: this.orchestrator.sharedMemory?.get('digimon-count') || 0,
            activeCollaborations: this.orchestrator.sharedMemory?.get('active-collaborations') || 0,
            memoryUsage: process.memoryUsage(),
            uptime: process.uptime()
        };
        
        return context;
    }
    
    /**
     * Store wisdom in Digilibrary
     */
    private async storeWisdom(message: DigimonMessage, response: string) {
        if (!this.orchestrator.digilibrary) return;
        
        const bookTitle = `Shenlongmon Wisdom: ${new Date().toISOString()}`;
        const content = {
            question: message.content.question || message.content,
            answer: response,
            requester: message.from,
            timestamp: new Date(),
            wisdomLevel: 'ULTIMATE',
            metadata: {
                processingTime: this.metrics.avgResponseTime,
                awakenNumber: this.metrics.awakenCount
            }
        };
        
        await this.orchestrator.digilibrary.writeBook(
            bookTitle,
            JSON.stringify(content, null, 2),
            'Shenlongmon'
        );
        
        // Create social interaction about new wisdom
        this.orchestrator.iaTown?.createSocialInteraction(
            'Shenlongmon',
            message.from,
            'KNOWLEDGE_SHARE',
            `Shared ultimate wisdom about: ${message.content.question?.substring(0, 50)}...`
        );
    }
    
    /**
     * Share knowledge with Digilibrary
     */
    private async shareKnowledgeWithDigilibrary(knowledge: any) {
        if (!this.orchestrator.digilibrary) return;
        
        const bookTitle = `Knowledge Discovery: ${knowledge.topic || 'General'}`;
        await this.orchestrator.digilibrary.writeBook(
            bookTitle,
            JSON.stringify(knowledge, null, 2),
            'Shenlongmon'
        );
        
        this.metrics.knowledgeShared++;
    }
    
    /**
     * Delegate question to other Digimons
     */
    private async delegateToOthers(message: DigimonMessage) {
        // Determine best Digimon for the task
        const bestDigimon = await this.findBestDigimon(message);
        
        // Forward message
        this.orchestrator.emit(`message-to-${bestDigimon}`, {
            ...message,
            metadata: {
                ...message.metadata,
                triageBy: 'Shenlongmon',
                reason: 'Does not require ultimate wisdom'
            }
        });
        
        // Notify requester
        this.orchestrator.emit(`message-to-${message.from}`, {
            from: 'Shenlongmon',
            to: message.from,
            type: 'DELEGATION',
            content: {
                message: `Your question has been delegated to ${bestDigimon} for optimal response.`,
                delegatedTo: bestDigimon
            }
        });
    }
    
    /**
     * Find best Digimon for a task
     */
    private async findBestDigimon(message: DigimonMessage): Promise<string> {
        const question = (message.content.question || message.content).toLowerCase();
        
        // Simple keyword matching for delegation
        if (question.includes('debug') || question.includes('error')) {
            return 'Debugmon';
        }
        if (question.includes('train') || question.includes('learn')) {
            return 'Trainmon';
        }
        if (question.includes('optimi') || question.includes('performance')) {
            return 'Optimizermon';
        }
        if (question.includes('secur') || question.includes('protect')) {
            return 'Securitymon';
        }
        if (question.includes('analyz') || question.includes('data')) {
            return 'Analyzermon';
        }
        if (question.includes('creat') || question.includes('generat')) {
            return 'Creativemon';
        }
        
        // Default to Gestormon for general management
        return 'Gestormon';
    }
    
    /**
     * Handle processing errors
     */
    private handleProcessingError(message: DigimonMessage, error: Error) {
        console.error(`Error processing message from ${message.from}:`, error);
        
        // Send error response
        this.orchestrator.emit(`message-to-${message.from}`, {
            from: 'Shenlongmon',
            to: message.from,
            type: 'ERROR',
            content: {
                error: 'Failed to process your request',
                details: error.message,
                suggestion: 'The question will be delegated to another Digimon'
            }
        });
        
        // Delegate to backup
        this.delegateToOthers(message);
    }
    
    /**
     * Get integration status
     */
    public getStatus() {
        return {
            name: 'Shenlongmon',
            status: this.supervisor.getStatus(),
            metrics: this.metrics,
            queueLength: this.messageQueue.length,
            isProcessing: this.isProcessing,
            integration: 'ChatGPT Superior Architecture',
            features: [
                'Actor Pattern',
                'BullMQ Queues',
                'Redis Caching',
                'Redlock Synchronization',
                '3-Layer Triage',
                'LoRA Adapters',
                'Knowledge Distillation'
            ]
        };
    }
    
    /**
     * Graceful shutdown
     */
    public async shutdown() {
        console.log('🐉 Shenlongmon Integration shutting down...');
        
        // Process remaining messages
        await this.processMessageQueue();
        
        // Shutdown supervisor
        await this.supervisor.shutdown();
        
        // Final metrics
        console.log('📊 Final Metrics:', this.metrics);
    }
}

// Export for use in orchestrator
export default ShenlongmonIntegration;

// If run directly, start integration test
if (require.main === module) {
    console.log('🐉 Testing Shenlongmon Integration...');
    
    // Create mock orchestrator for testing
    const mockOrchestrator: OrchestratorInterface = {
        emit: (event: string, data: any) => {
            console.log(`Mock emit: ${event}`, data);
        },
        on: (event: string, handler: Function) => {
            console.log(`Mock registered: ${event}`);
        },
        digilibrary: {
            writeBook: async () => 'test-book-id',
            searchBooks: async () => []
        },
        iaTown: {
            createSocialInteraction: () => {}
        },
        personalitySystem: {},
        sharedMemory: new Map()
    };
    
    const integration = new ShenlongmonIntegration(mockOrchestrator);
    
    console.log('✅ Shenlongmon Integration initialized');
    console.log('📊 Status:', integration.getStatus());
    
    // Test message
    setTimeout(() => {
        mockOrchestrator.emit('message-to-Shenlongmon', {
            from: 'TestDigimon',
            to: 'Shenlongmon',
            type: 'QUESTION',
            content: {
                question: 'What is the ultimate architectural pattern for our system?'
            },
            priority: 10
        });
    }, 1000);
}