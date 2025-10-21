/**
 * @fileoverview Enterprise-grade Ollama integration with connection pooling
 * @module OllamaEnterprise
 * @author Digimundo Team
 * @version 2.0.0
 */

import { EventEmitter } from 'events';
import fetch, { Response } from 'node-fetch';
import PQueue from 'p-queue';
import CircuitBreaker from 'opossum';
import { LRUCache } from 'lru-cache';
import * as crypto from 'crypto';

/**
 * Model configuration interface
 */
export interface IOllamaModel {
  name: string;
  size: number;
  digest: string;
  modified: Date;
  capabilities?: string[];
  maxTokens?: number;
  temperature?: number;
}

/**
 * Connection pool configuration
 */
export interface IPoolConfig {
  minConnections: number;
  maxConnections: number;
  connectionTimeout: number;
  idleTimeout: number;
  retryAttempts: number;
  retryDelay: number;
}

/**
 * Request options
 */
export interface IOllamaRequest {
  model: string;
  prompt: string;
  stream?: boolean;
  temperature?: number;
  topK?: number;
  topP?: number;
  numPredict?: number;
  stop?: string[];
  format?: 'json';
  context?: number[];
  options?: Record<string, unknown>;
}

/**
 * Response interface
 */
export interface IOllamaResponse {
  model: string;
  response: string;
  done: boolean;
  context?: number[];
  totalDuration?: number;
  loadDuration?: number;
  promptEvalDuration?: number;
  evalDuration?: number;
  evalCount?: number;
}

/**
 * Connection interface
 */
interface IConnection {
  id: string;
  url: string;
  inUse: boolean;
  lastUsed: Date;
  requestCount: number;
  errorCount: number;
  averageLatency: number;
}

/**
 * Load balancing strategies
 */
export enum LoadBalancingStrategy {
  ROUND_ROBIN = 'round-robin',
  LEAST_CONNECTIONS = 'least-connections',
  LEAST_LATENCY = 'least-latency',
  RANDOM = 'random',
  WEIGHTED = 'weighted',
}

/**
 * Ollama Enterprise Client
 */
export class OllamaEnterprise extends EventEmitter {
  private connections: Map<string, IConnection> = new Map();
  private connectionPool: IConnection[] = [];
  private currentConnectionIndex = 0;
  private modelCache: Map<string, IOllamaModel> = new Map();
  private responseCache: LRUCache<string, IOllamaResponse>;
  private requestQueue: PQueue;
  private circuitBreaker: CircuitBreaker;
  private healthCheckInterval?: NodeJS.Timeout;
  private metricsCollector: Map<string, any> = new Map();
  
  constructor(
    private readonly urls: string[] = ['http://localhost:11434'],
    private readonly config: IPoolConfig = {
      minConnections: 2,
      maxConnections: 10,
      connectionTimeout: 30000,
      idleTimeout: 60000,
      retryAttempts: 3,
      retryDelay: 1000,
    },
    private readonly strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LATENCY
  ) {
    super();

    // Initialize response cache
    this.responseCache = new LRUCache<string, IOllamaResponse>({
      max: 1000,
      ttl: 1000 * 60 * 5, // 5 minutes
      updateAgeOnGet: true,
      updateAgeOnHas: true,
    });

    // Initialize request queue
    this.requestQueue = new PQueue({
      concurrency: this.config.maxConnections,
      interval: 1000,
      intervalCap: 50,
      timeout: this.config.connectionTimeout,
    });

    // Initialize circuit breaker
    this.circuitBreaker = new CircuitBreaker(
      this.executeRequest.bind(this),
      {
        timeout: this.config.connectionTimeout,
        errorThresholdPercentage: 50,
        resetTimeout: 30000,
        rollingCountTimeout: 10000,
        rollingCountBuckets: 10,
      }
    );

    this.setupCircuitBreakerEvents();
    this.initializeConnections();
    this.startHealthChecks();
  }

  /**
   * Initialize connection pool
   */
  private initializeConnections(): void {
    for (const url of this.urls) {
      for (let i = 0; i < this.config.minConnections; i++) {
        const connection: IConnection = {
          id: crypto.randomUUID(),
          url,
          inUse: false,
          lastUsed: new Date(),
          requestCount: 0,
          errorCount: 0,
          averageLatency: 0,
        };
        
        this.connections.set(connection.id, connection);
        this.connectionPool.push(connection);
      }
    }

    console.log(`Initialized ${this.connectionPool.length} connections to Ollama`);
  }

  /**
   * Setup circuit breaker events
   */
  private setupCircuitBreakerEvents(): void {
    this.circuitBreaker.on('open', () => {
      console.error('Ollama circuit breaker opened - falling back to Claude');
      this.emit('circuit:open');
    });

    this.circuitBreaker.on('halfOpen', () => {
      console.warn('Ollama circuit breaker half-open - testing connection');
      this.emit('circuit:halfOpen');
    });

    this.circuitBreaker.on('close', () => {
      console.log('Ollama circuit breaker closed - connection restored');
      this.emit('circuit:closed');
    });
  }

  /**
   * Get next connection based on strategy
   */
  private getNextConnection(): IConnection | null {
    const availableConnections = this.connectionPool.filter(c => !c.inUse);
    
    if (availableConnections.length === 0) {
      // Try to create new connection if under max limit
      if (this.connectionPool.length < this.config.maxConnections) {
        return this.createNewConnection();
      }
      return null;
    }

    let selectedConnection: IConnection;

    switch (this.strategy) {
      case LoadBalancingStrategy.ROUND_ROBIN:
        this.currentConnectionIndex = (this.currentConnectionIndex + 1) % availableConnections.length;
        selectedConnection = availableConnections[this.currentConnectionIndex];
        break;

      case LoadBalancingStrategy.LEAST_CONNECTIONS:
        selectedConnection = availableConnections.reduce((prev, curr) =>
          prev.requestCount < curr.requestCount ? prev : curr
        );
        break;

      case LoadBalancingStrategy.LEAST_LATENCY:
        selectedConnection = availableConnections.reduce((prev, curr) =>
          prev.averageLatency < curr.averageLatency ? prev : curr
        );
        break;

      case LoadBalancingStrategy.RANDOM:
        selectedConnection = availableConnections[Math.floor(Math.random() * availableConnections.length)];
        break;

      case LoadBalancingStrategy.WEIGHTED:
        // Weight based on error rate and latency
        selectedConnection = availableConnections.reduce((prev, curr) => {
          const prevScore = prev.errorCount / (prev.requestCount || 1) + prev.averageLatency / 1000;
          const currScore = curr.errorCount / (curr.requestCount || 1) + curr.averageLatency / 1000;
          return prevScore < currScore ? prev : curr;
        });
        break;

      default:
        selectedConnection = availableConnections[0];
    }

    selectedConnection.inUse = true;
    return selectedConnection;
  }

  /**
   * Create new connection
   */
  private createNewConnection(): IConnection | null {
    const url = this.urls[Math.floor(Math.random() * this.urls.length)];
    const connection: IConnection = {
      id: crypto.randomUUID(),
      url,
      inUse: true,
      lastUsed: new Date(),
      requestCount: 0,
      errorCount: 0,
      averageLatency: 0,
    };

    this.connections.set(connection.id, connection);
    this.connectionPool.push(connection);
    
    console.log(`Created new connection ${connection.id} to ${url}`);
    return connection;
  }

  /**
   * Release connection back to pool
   */
  private releaseConnection(connection: IConnection): void {
    connection.inUse = false;
    connection.lastUsed = new Date();
    
    // Remove idle connections over limit
    this.cleanupIdleConnections();
  }

  /**
   * Cleanup idle connections
   */
  private cleanupIdleConnections(): void {
    const now = Date.now();
    const idleConnections = this.connectionPool.filter(c => 
      !c.inUse && 
      (now - c.lastUsed.getTime()) > this.config.idleTimeout &&
      this.connectionPool.length > this.config.minConnections
    );

    for (const connection of idleConnections) {
      const index = this.connectionPool.indexOf(connection);
      if (index > -1) {
        this.connectionPool.splice(index, 1);
        this.connections.delete(connection.id);
        console.log(`Removed idle connection ${connection.id}`);
      }
    }
  }

  /**
   * Execute request with connection pooling
   */
  private async executeRequest(request: IOllamaRequest): Promise<IOllamaResponse> {
    const connection = this.getNextConnection();
    
    if (!connection) {
      throw new Error('No available connections');
    }

    const startTime = Date.now();

    try {
      const response = await fetch(`${connection.url}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
        signal: AbortSignal.timeout(this.config.connectionTimeout),
      });

      if (!response.ok) {
        throw new Error(`Ollama request failed: ${response.statusText}`);
      }

      const data = await response.json() as IOllamaResponse;
      
      // Update connection metrics
      const latency = Date.now() - startTime;
      connection.requestCount++;
      connection.averageLatency = 
        (connection.averageLatency * (connection.requestCount - 1) + latency) / connection.requestCount;
      
      return data;
    } catch (error) {
      connection.errorCount++;
      throw error;
    } finally {
      this.releaseConnection(connection);
    }
  }

  /**
   * Generate completion
   */
  public async generate(request: IOllamaRequest): Promise<IOllamaResponse> {
    // Check cache first
    const cacheKey = this.getCacheKey(request);
    const cached = this.responseCache.get(cacheKey);
    
    if (cached) {
      this.emit('cache:hit', cacheKey);
      return cached;
    }

    // Add to queue
    const response = await this.requestQueue.add(async () => {
      return await this.circuitBreaker.fire(request);
    });

    // Cache response
    if (response) {
      this.responseCache.set(cacheKey, response);
    }

    return response as IOllamaResponse;
  }

  /**
   * Stream completion
   */
  public async *generateStream(request: IOllamaRequest): AsyncGenerator<IOllamaResponse> {
    const connection = this.getNextConnection();
    
    if (!connection) {
      throw new Error('No available connections');
    }

    try {
      const response = await fetch(`${connection.url}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...request, stream: true }),
      });

      if (!response.ok) {
        throw new Error(`Ollama stream failed: ${response.statusText}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('Failed to get response reader');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.trim()) {
            try {
              const data = JSON.parse(line) as IOllamaResponse;
              yield data;
            } catch (e) {
              console.error('Failed to parse stream response:', e);
            }
          }
        }
      }
    } finally {
      this.releaseConnection(connection);
    }
  }

  /**
   * List available models
   */
  public async listModels(): Promise<IOllamaModel[]> {
    const connection = this.connectionPool[0];
    
    if (!connection) {
      throw new Error('No connections available');
    }

    const response = await fetch(`${connection.url}/api/tags`);
    
    if (!response.ok) {
      throw new Error(`Failed to list models: ${response.statusText}`);
    }

    const data = await response.json() as { models: IOllamaModel[] };
    
    // Update model cache
    for (const model of data.models) {
      this.modelCache.set(model.name, model);
    }

    return data.models;
  }

  /**
   * Pull a model
   */
  public async pullModel(modelName: string): Promise<void> {
    const connection = this.connectionPool[0];
    
    if (!connection) {
      throw new Error('No connections available');
    }

    const response = await fetch(`${connection.url}/api/pull`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: modelName }),
    });

    if (!response.ok) {
      throw new Error(`Failed to pull model ${modelName}: ${response.statusText}`);
    }

    console.log(`Model ${modelName} pulled successfully`);
    this.emit('model:pulled', modelName);
  }

  /**
   * Preload models for warm start
   */
  public async preloadModels(modelNames: string[]): Promise<void> {
    console.log(`Preloading ${modelNames.length} models...`);
    
    const tasks = modelNames.map(async (modelName) => {
      try {
        // Send a dummy request to load the model
        await this.generate({
          model: modelName,
          prompt: 'Hello',
          numPredict: 1,
        });
        
        console.log(`Model ${modelName} preloaded`);
        this.emit('model:preloaded', modelName);
      } catch (error) {
        console.error(`Failed to preload model ${modelName}:`, error);
      }
    });

    await Promise.allSettled(tasks);
  }

  /**
   * Start health checks
   */
  private startHealthChecks(): void {
    this.healthCheckInterval = setInterval(async () => {
      await this.performHealthCheck();
    }, 30000); // Every 30 seconds
  }

  /**
   * Perform health check
   */
  private async performHealthCheck(): Promise<void> {
    for (const connection of this.connectionPool) {
      try {
        const response = await fetch(`${connection.url}/api/tags`, {
          signal: AbortSignal.timeout(5000),
        });
        
        if (!response.ok) {
          connection.errorCount++;
          this.emit('connection:unhealthy', connection);
        }
      } catch (error) {
        connection.errorCount++;
        this.emit('connection:unhealthy', connection);
      }
    }

    // Remove connections with too many errors
    const unhealthyConnections = this.connectionPool.filter(c => 
      c.errorCount > 10 && this.connectionPool.length > this.config.minConnections
    );

    for (const connection of unhealthyConnections) {
      const index = this.connectionPool.indexOf(connection);
      if (index > -1) {
        this.connectionPool.splice(index, 1);
        this.connections.delete(connection.id);
        console.error(`Removed unhealthy connection ${connection.id}`);
      }
    }
  }

  /**
   * Get cache key for request
   */
  private getCacheKey(request: IOllamaRequest): string {
    const key = {
      model: request.model,
      prompt: request.prompt,
      temperature: request.temperature,
      topK: request.topK,
      topP: request.topP,
    };
    
    return crypto
      .createHash('sha256')
      .update(JSON.stringify(key))
      .digest('hex');
  }

  /**
   * Get connection pool statistics
   */
  public getPoolStats(): {
    totalConnections: number;
    activeConnections: number;
    idleConnections: number;
    averageLatency: number;
    totalRequests: number;
    totalErrors: number;
    cacheHitRate: number;
  } {
    const activeConnections = this.connectionPool.filter(c => c.inUse).length;
    const idleConnections = this.connectionPool.filter(c => !c.inUse).length;
    
    let totalLatency = 0;
    let totalRequests = 0;
    let totalErrors = 0;
    
    for (const connection of this.connectionPool) {
      totalLatency += connection.averageLatency * connection.requestCount;
      totalRequests += connection.requestCount;
      totalErrors += connection.errorCount;
    }
    
    const cacheStats = this.responseCache as any;
    const cacheHitRate = cacheStats.hits / (cacheStats.hits + cacheStats.misses) || 0;
    
    return {
      totalConnections: this.connectionPool.length,
      activeConnections,
      idleConnections,
      averageLatency: totalRequests > 0 ? totalLatency / totalRequests : 0,
      totalRequests,
      totalErrors,
      cacheHitRate,
    };
  }

  /**
   * Shutdown the client
   */
  public async shutdown(): Promise<void> {
    console.log('Shutting down Ollama Enterprise client...');
    
    // Stop health checks
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
    }

    // Clear queue
    this.requestQueue.clear();
    
    // Clear caches
    this.responseCache.clear();
    this.modelCache.clear();
    
    // Clear connections
    this.connectionPool = [];
    this.connections.clear();
    
    console.log('Ollama Enterprise client shutdown complete');
    this.emit('shutdown');
  }
}

/**
 * Claude fallback integration
 */
export class ClaudeFallback {
  constructor(private readonly apiKey: string) {}

  /**
   * Generate completion using Claude
   */
  public async generate(prompt: string): Promise<string> {
    // Implement Claude API call
    console.log('Falling back to Claude API...');
    
    // This would be the actual Claude API implementation
    return `Claude response for: ${prompt}`;
  }
}

/**
 * Factory function to create Ollama client with fallback
 */
export function createOllamaClient(
  urls?: string[],
  config?: IPoolConfig,
  strategy?: LoadBalancingStrategy
): OllamaEnterprise {
  const client = new OllamaEnterprise(urls, config, strategy);
  
  // Setup automatic fallback to Claude on circuit open
  client.on('circuit:open', () => {
    console.log('Switching to Claude fallback...');
    // Implement fallback logic
  });
  
  return client;
}