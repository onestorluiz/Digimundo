/**
 * @fileoverview Enterprise-grade Agent Orchestrator using Actor Model
 * @module AgentOrchestrator
 * @author Digimundo Team
 * @version 2.0.0
 */

import { EventEmitter } from 'events';
import { Worker } from 'worker_threads';
import * as crypto from 'crypto';
import { performance } from 'perf_hooks';
import PQueue from 'p-queue';
import CircuitBreaker from 'opossum';

/**
 * Agent state enumeration
 */
export enum AgentState {
  IDLE = 'idle',
  PROCESSING = 'processing',
  WAITING = 'waiting',
  ERROR = 'error',
  TERMINATED = 'terminated',
}

/**
 * Message priority levels
 */
export enum MessagePriority {
  CRITICAL = 0,
  HIGH = 1,
  NORMAL = 2,
  LOW = 3,
}

/**
 * Agent interface definition
 */
export interface IAgent {
  id: string;
  name: string;
  type: string;
  state: AgentState;
  capabilities: string[];
  metadata: Record<string, unknown>;
  metrics: IAgentMetrics;
}

/**
 * Agent metrics interface
 */
export interface IAgentMetrics {
  messagesProcessed: number;
  averageResponseTime: number;
  errorRate: number;
  lastActivity: Date;
  uptime: number;
  memoryUsage: number;
  cpuUsage: number;
}

/**
 * Message interface
 */
export interface IMessage<T = unknown> {
  id: string;
  from: string;
  to: string;
  type: string;
  payload: T;
  priority: MessagePriority;
  timestamp: Date;
  correlationId?: string;
  replyTo?: string;
  ttl?: number;
}

/**
 * Actor interface
 */
export interface IActor {
  id: string;
  receive(message: IMessage): Promise<void>;
  send(to: string, message: IMessage): Promise<void>;
  getState(): AgentState;
  getMetrics(): IAgentMetrics;
  start(): Promise<void>;
  stop(): Promise<void>;
}

/**
 * Circuit breaker options
 */
interface ICircuitBreakerOptions {
  timeout: number;
  errorThresholdPercentage: number;
  resetTimeout: number;
  rollingCountTimeout: number;
  rollingCountBuckets: number;
}

/**
 * Actor implementation
 */
class Actor extends EventEmitter implements IActor {
  public readonly id: string;
  private state: AgentState = AgentState.IDLE;
  private mailbox: PQueue;
  private metrics: IAgentMetrics;
  private worker?: Worker;
  private circuitBreaker: CircuitBreaker;

  constructor(
    public readonly agent: IAgent,
    private readonly orchestrator: AgentOrchestrator
  ) {
    super();
    this.id = agent.id;
    this.mailbox = new PQueue({ 
      concurrency: 1,
      interval: 100,
      intervalCap: 10,
      carryoverConcurrencyCount: true
    });
    
    this.metrics = {
      messagesProcessed: 0,
      averageResponseTime: 0,
      errorRate: 0,
      lastActivity: new Date(),
      uptime: 0,
      memoryUsage: 0,
      cpuUsage: 0,
    };

    // Setup circuit breaker
    const breakerOptions: ICircuitBreakerOptions = {
      timeout: 3000,
      errorThresholdPercentage: 50,
      resetTimeout: 30000,
      rollingCountTimeout: 10000,
      rollingCountBuckets: 10,
    };

    this.circuitBreaker = new CircuitBreaker(
      this.processMessage.bind(this),
      breakerOptions
    );

    this.setupCircuitBreakerEvents();
  }

  /**
   * Setup circuit breaker event handlers
   */
  private setupCircuitBreakerEvents(): void {
    this.circuitBreaker.on('open', () => {
      console.error(`Circuit breaker opened for agent ${this.id}`);
      this.state = AgentState.ERROR;
      this.emit('circuit-open', this.id);
    });

    this.circuitBreaker.on('halfOpen', () => {
      console.warn(`Circuit breaker half-open for agent ${this.id}`);
      this.emit('circuit-halfOpen', this.id);
    });

    this.circuitBreaker.on('close', () => {
      console.log(`Circuit breaker closed for agent ${this.id}`);
      this.state = AgentState.IDLE;
      this.emit('circuit-close', this.id);
    });
  }

  /**
   * Receive a message
   */
  public async receive(message: IMessage): Promise<void> {
    const startTime = performance.now();

    try {
      // Check TTL
      if (message.ttl && Date.now() - message.timestamp.getTime() > message.ttl) {
        throw new Error(`Message ${message.id} expired`);
      }

      // Add to mailbox with priority
      await this.mailbox.add(
        async () => await this.circuitBreaker.fire(message),
        { priority: message.priority }
      );

      // Update metrics
      const responseTime = performance.now() - startTime;
      this.updateMetrics(responseTime, false);
    } catch (error) {
      this.updateMetrics(performance.now() - startTime, true);
      throw error;
    }
  }

  /**
   * Process a message
   */
  private async processMessage(message: IMessage): Promise<void> {
    this.state = AgentState.PROCESSING;
    this.metrics.lastActivity = new Date();

    try {
      // Process based on message type
      switch (message.type) {
        case 'compute':
          await this.handleCompute(message);
          break;
        case 'query':
          await this.handleQuery(message);
          break;
        case 'command':
          await this.handleCommand(message);
          break;
        default:
          await this.handleDefault(message);
      }

      this.metrics.messagesProcessed++;
    } finally {
      this.state = AgentState.IDLE;
    }
  }

  /**
   * Send a message to another actor
   */
  public async send(to: string, message: IMessage): Promise<void> {
    await this.orchestrator.routeMessage(to, message);
  }

  /**
   * Handle compute messages
   */
  private async handleCompute(message: IMessage): Promise<void> {
    // Implement compute logic
    this.emit('compute', message);
  }

  /**
   * Handle query messages
   */
  private async handleQuery(message: IMessage): Promise<void> {
    // Implement query logic
    this.emit('query', message);
  }

  /**
   * Handle command messages
   */
  private async handleCommand(message: IMessage): Promise<void> {
    // Implement command logic
    this.emit('command', message);
  }

  /**
   * Handle default messages
   */
  private async handleDefault(message: IMessage): Promise<void> {
    // Implement default logic
    this.emit('message', message);
  }

  /**
   * Update actor metrics
   */
  private updateMetrics(responseTime: number, isError: boolean): void {
    const alpha = 0.2; // Exponential moving average factor
    
    this.metrics.averageResponseTime = 
      alpha * responseTime + (1 - alpha) * this.metrics.averageResponseTime;
    
    if (isError) {
      this.metrics.errorRate = 
        alpha * 1 + (1 - alpha) * this.metrics.errorRate;
    } else {
      this.metrics.errorRate = 
        alpha * 0 + (1 - alpha) * this.metrics.errorRate;
    }

    // Update memory usage
    if (process.memoryUsage) {
      this.metrics.memoryUsage = process.memoryUsage().heapUsed;
    }
  }

  /**
   * Get current state
   */
  public getState(): AgentState {
    return this.state;
  }

  /**
   * Get metrics
   */
  public getMetrics(): IAgentMetrics {
    return { ...this.metrics };
  }

  /**
   * Start the actor
   */
  public async start(): Promise<void> {
    this.state = AgentState.IDLE;
    this.mailbox.start();
    this.emit('started', this.id);
  }

  /**
   * Stop the actor
   */
  public async stop(): Promise<void> {
    this.state = AgentState.TERMINATED;
    this.mailbox.pause();
    this.mailbox.clear();
    
    if (this.worker) {
      await this.worker.terminate();
    }
    
    this.emit('stopped', this.id);
  }
}

/**
 * Agent Orchestrator - Main controller
 */
export class AgentOrchestrator extends EventEmitter {
  private actors: Map<string, Actor> = new Map();
  private supervisors: Map<string, string> = new Map();
  private messageRouter: Map<string, string[]> = new Map();
  private globalQueue: PQueue;
  private metrics: Map<string, IAgentMetrics> = new Map();
  private healthCheckInterval?: NodeJS.Timeout;

  constructor(private readonly config: IOrchestatorConfig = {}) {
    super();
    
    this.globalQueue = new PQueue({
      concurrency: config.maxConcurrency || 100,
      interval: config.interval || 1000,
      intervalCap: config.intervalCap || 50,
    });

    this.setupHealthChecks();
  }

  /**
   * Register a new agent
   */
  public async registerAgent(agent: IAgent): Promise<void> {
    if (this.actors.has(agent.id)) {
      throw new Error(`Agent ${agent.id} already registered`);
    }

    const actor = new Actor(agent, this);
    
    // Setup actor event handlers
    actor.on('circuit-open', (agentId) => this.handleCircuitOpen(agentId));
    actor.on('started', (agentId) => this.emit('agent:started', agentId));
    actor.on('stopped', (agentId) => this.emit('agent:stopped', agentId));

    this.actors.set(agent.id, actor);
    await actor.start();
    
    console.log(`Agent ${agent.name} (${agent.id}) registered`);
    this.emit('agent:registered', agent);
  }

  /**
   * Unregister an agent
   */
  public async unregisterAgent(agentId: string): Promise<void> {
    const actor = this.actors.get(agentId);
    
    if (!actor) {
      throw new Error(`Agent ${agentId} not found`);
    }

    await actor.stop();
    this.actors.delete(agentId);
    this.metrics.delete(agentId);
    
    console.log(`Agent ${agentId} unregistered`);
    this.emit('agent:unregistered', agentId);
  }

  /**
   * Send a message to an agent
   */
  public async sendMessage<T = unknown>(
    to: string,
    message: Partial<IMessage<T>>
  ): Promise<void> {
    const actor = this.actors.get(to);
    
    if (!actor) {
      throw new Error(`Agent ${to} not found`);
    }

    const fullMessage: IMessage<T> = {
      id: message.id || crypto.randomUUID(),
      from: message.from || 'orchestrator',
      to,
      type: message.type || 'default',
      payload: message.payload as T,
      priority: message.priority || MessagePriority.NORMAL,
      timestamp: message.timestamp || new Date(),
      correlationId: message.correlationId,
      replyTo: message.replyTo,
      ttl: message.ttl,
    };

    await actor.receive(fullMessage);
  }

  /**
   * Broadcast a message to multiple agents
   */
  public async broadcast<T = unknown>(
    message: Partial<IMessage<T>>,
    filter?: (agent: IAgent) => boolean
  ): Promise<void> {
    const tasks: Promise<void>[] = [];

    for (const actor of this.actors.values()) {
      if (!filter || filter(actor.agent)) {
        tasks.push(this.sendMessage(actor.id, message));
      }
    }

    await Promise.allSettled(tasks);
  }

  /**
   * Route a message between actors
   */
  public async routeMessage(to: string, message: IMessage): Promise<void> {
    await this.sendMessage(to, message);
  }

  /**
   * Get agent by ID
   */
  public getAgent(agentId: string): IAgent | undefined {
    return this.actors.get(agentId)?.agent;
  }

  /**
   * Get all agents
   */
  public getAgents(): IAgent[] {
    return Array.from(this.actors.values()).map(actor => actor.agent);
  }

  /**
   * Get agent metrics
   */
  public getAgentMetrics(agentId: string): IAgentMetrics | undefined {
    return this.actors.get(agentId)?.getMetrics();
  }

  /**
   * Get all metrics
   */
  public getAllMetrics(): Map<string, IAgentMetrics> {
    const metrics = new Map<string, IAgentMetrics>();
    
    for (const [id, actor] of this.actors) {
      metrics.set(id, actor.getMetrics());
    }
    
    return metrics;
  }

  /**
   * Setup health checks
   */
  private setupHealthChecks(): void {
    this.healthCheckInterval = setInterval(() => {
      this.performHealthCheck();
    }, this.config.healthCheckInterval || 30000);
  }

  /**
   * Perform health check on all agents
   */
  private async performHealthCheck(): Promise<void> {
    const healthChecks: Promise<void>[] = [];

    for (const [id, actor] of this.actors) {
      healthChecks.push(this.checkAgentHealth(id, actor));
    }

    await Promise.allSettled(healthChecks);
    this.emit('health:checked', this.getAllMetrics());
  }

  /**
   * Check individual agent health
   */
  private async checkAgentHealth(id: string, actor: Actor): Promise<void> {
    const metrics = actor.getMetrics();
    const state = actor.getState();

    // Check for unhealthy conditions
    if (metrics.errorRate > 0.5) {
      console.warn(`Agent ${id} has high error rate: ${metrics.errorRate}`);
      this.emit('agent:unhealthy', { id, reason: 'high-error-rate', metrics });
    }

    if (metrics.averageResponseTime > 5000) {
      console.warn(`Agent ${id} has slow response time: ${metrics.averageResponseTime}ms`);
      this.emit('agent:unhealthy', { id, reason: 'slow-response', metrics });
    }

    if (state === AgentState.ERROR) {
      console.error(`Agent ${id} is in error state`);
      this.emit('agent:error', { id, state, metrics });
      
      // Attempt recovery
      await this.recoverAgent(id);
    }
  }

  /**
   * Handle circuit breaker open event
   */
  private async handleCircuitOpen(agentId: string): Promise<void> {
    console.error(`Circuit opened for agent ${agentId}, attempting recovery...`);
    await this.recoverAgent(agentId);
  }

  /**
   * Recover an agent
   */
  private async recoverAgent(agentId: string): Promise<void> {
    const actor = this.actors.get(agentId);
    
    if (!actor) return;

    try {
      // Stop and restart the agent
      await actor.stop();
      await new Promise(resolve => setTimeout(resolve, 1000));
      await actor.start();
      
      console.log(`Agent ${agentId} recovered successfully`);
      this.emit('agent:recovered', agentId);
    } catch (error) {
      console.error(`Failed to recover agent ${agentId}:`, error);
      this.emit('agent:recovery-failed', { agentId, error });
    }
  }

  /**
   * Shutdown the orchestrator
   */
  public async shutdown(): Promise<void> {
    console.log('Shutting down Agent Orchestrator...');
    
    // Clear health check interval
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
    }

    // Stop all actors
    const stopTasks: Promise<void>[] = [];
    
    for (const actor of this.actors.values()) {
      stopTasks.push(actor.stop());
    }

    await Promise.allSettled(stopTasks);
    
    // Clear collections
    this.actors.clear();
    this.metrics.clear();
    this.supervisors.clear();
    this.messageRouter.clear();
    
    console.log('Agent Orchestrator shutdown complete');
    this.emit('shutdown');
  }
}

/**
 * Orchestrator configuration interface
 */
interface IOrchestatorConfig {
  maxConcurrency?: number;
  interval?: number;
  intervalCap?: number;
  healthCheckInterval?: number;
}

/**
 * Factory function to create orchestrator
 */
export function createOrchestrator(config?: IOrchestatorConfig): AgentOrchestrator {
  return new AgentOrchestrator(config);
}

// Export types
export type { IOrchestatorConfig, ICircuitBreakerOptions };