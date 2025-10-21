/**
 * 🛡️ RESILIENCE LAYER - Netflix-Grade Fault Tolerance
 * Implements circuit breakers, retry logic, and auto-recovery
 * Based on Netflix Hystrix patterns
 */

const EventEmitter = require('events');

class CircuitBreaker extends EventEmitter {
  constructor(name, options = {}) {
    super();
    this.name = name;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    
    // Configuration
    this.options = {
      timeout: options.timeout || 3000,
      errorThreshold: options.errorThreshold || 50, // percentage
      volumeThreshold: options.volumeThreshold || 20, // minimum requests
      sleepWindow: options.sleepWindow || 60000, // time before retry
      bucketSize: options.bucketSize || 10000, // rolling window
      ...options
    };
    
    // Metrics
    this.metrics = {
      requests: 0,
      failures: 0,
      successes: 0,
      timeouts: 0,
      shortCircuited: 0,
      latency: []
    };
    
    // Rolling window for metrics
    this.rollingWindow = [];
    this.lastFailTime = null;
    
    // Start metrics cleanup
    this.startMetricsCleanup();
  }
  
  async execute(fn, fallback) {
    const startTime = Date.now();
    
    // Check if circuit is open
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailTime > this.options.sleepWindow) {
        this.state = 'HALF_OPEN';
        this.emit('half-open', this.name);
      } else {
        this.metrics.shortCircuited++;
        this.emit('short-circuited', this.name);
        return fallback ? await fallback() : this.getDefaultFallback();
      }
    }
    
    try {
      // Set timeout
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Circuit breaker timeout')), this.options.timeout)
      );
      
      // Execute function with timeout
      const result = await Promise.race([fn(), timeoutPromise]);
      
      // Record success
      this.recordSuccess(Date.now() - startTime);
      
      // Close circuit if half-open
      if (this.state === 'HALF_OPEN') {
        this.state = 'CLOSED';
        this.emit('closed', this.name);
      }
      
      return result;
      
    } catch (error) {
      // Record failure
      this.recordFailure(Date.now() - startTime, error);
      
      // Check if we should open the circuit
      if (this.shouldOpenCircuit()) {
        this.state = 'OPEN';
        this.lastFailTime = Date.now();
        this.emit('open', this.name);
      }
      
      // Use fallback or throw
      if (fallback) {
        return await fallback();
      }
      
      throw error;
    }
  }
  
  recordSuccess(latency) {
    this.metrics.requests++;
    this.metrics.successes++;
    this.metrics.latency.push(latency);
    
    this.rollingWindow.push({
      timestamp: Date.now(),
      success: true,
      latency
    });
  }
  
  recordFailure(latency, error) {
    this.metrics.requests++;
    this.metrics.failures++;
    
    if (error.message.includes('timeout')) {
      this.metrics.timeouts++;
    }
    
    this.rollingWindow.push({
      timestamp: Date.now(),
      success: false,
      latency,
      error: error.message
    });
  }
  
  shouldOpenCircuit() {
    const recentRequests = this.rollingWindow.filter(
      r => Date.now() - r.timestamp < this.options.bucketSize
    );
    
    if (recentRequests.length < this.options.volumeThreshold) {
      return false;
    }
    
    const failures = recentRequests.filter(r => !r.success).length;
    const errorRate = (failures / recentRequests.length) * 100;
    
    return errorRate >= this.options.errorThreshold;
  }
  
  getDefaultFallback() {
    return {
      error: 'Service temporarily unavailable',
      circuit: this.name,
      state: this.state,
      cached: false
    };
  }
  
  startMetricsCleanup() {
    setInterval(() => {
      // Clean old metrics
      const cutoff = Date.now() - this.options.bucketSize;
      this.rollingWindow = this.rollingWindow.filter(r => r.timestamp > cutoff);
      
      // Keep only last 100 latency measurements
      if (this.metrics.latency.length > 100) {
        this.metrics.latency = this.metrics.latency.slice(-100);
      }
    }, 10000);
  }
  
  getStatus() {
    const recentRequests = this.rollingWindow.filter(
      r => Date.now() - r.timestamp < this.options.bucketSize
    );
    
    const failures = recentRequests.filter(r => !r.success).length;
    const errorRate = recentRequests.length > 0 
      ? (failures / recentRequests.length) * 100 
      : 0;
    
    const avgLatency = this.metrics.latency.length > 0
      ? this.metrics.latency.reduce((a, b) => a + b, 0) / this.metrics.latency.length
      : 0;
    
    return {
      name: this.name,
      state: this.state,
      metrics: {
        ...this.metrics,
        errorRate: errorRate.toFixed(2) + '%',
        avgLatency: avgLatency.toFixed(2) + 'ms'
      }
    };
  }
  
  reset() {
    this.state = 'CLOSED';
    this.metrics = {
      requests: 0,
      failures: 0,
      successes: 0,
      timeouts: 0,
      shortCircuited: 0,
      latency: []
    };
    this.rollingWindow = [];
    this.lastFailTime = null;
  }
}

class RetryPolicy {
  constructor(options = {}) {
    this.maxAttempts = options.maxAttempts || 3;
    this.delay = options.delay || 1000;
    this.maxDelay = options.maxDelay || 30000;
    this.backoffMultiplier = options.backoffMultiplier || 2;
    this.jitter = options.jitter !== false;
  }
  
  async execute(fn, context = {}) {
    let lastError;
    
    for (let attempt = 1; attempt <= this.maxAttempts; attempt++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error;
        
        if (attempt === this.maxAttempts) {
          throw error;
        }
        
        // Calculate delay with exponential backoff
        let delay = this.delay * Math.pow(this.backoffMultiplier, attempt - 1);
        delay = Math.min(delay, this.maxDelay);
        
        // Add jitter to prevent thundering herd
        if (this.jitter) {
          delay = delay * (0.5 + Math.random() * 0.5);
        }
        
        console.log(`🔄 Retry ${attempt}/${this.maxAttempts} after ${delay}ms`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
    
    throw lastError;
  }
}

class BulkheadIsolation {
  constructor(name, options = {}) {
    this.name = name;
    this.maxConcurrent = options.maxConcurrent || 10;
    this.queueSize = options.queueSize || 100;
    this.timeout = options.timeout || 30000;
    
    this.running = 0;
    this.queue = [];
  }
  
  async execute(fn) {
    if (this.running >= this.maxConcurrent) {
      if (this.queue.length >= this.queueSize) {
        throw new Error(`Bulkhead ${this.name} queue is full`);
      }
      
      // Queue the request
      return new Promise((resolve, reject) => {
        const timeoutId = setTimeout(() => {
          const index = this.queue.findIndex(item => item.resolve === resolve);
          if (index !== -1) {
            this.queue.splice(index, 1);
          }
          reject(new Error(`Bulkhead ${this.name} timeout`));
        }, this.timeout);
        
        this.queue.push({
          fn,
          resolve,
          reject,
          timeoutId
        });
      });
    }
    
    this.running++;
    
    try {
      const result = await fn();
      return result;
    } finally {
      this.running--;
      this.processQueue();
    }
  }
  
  async processQueue() {
    if (this.queue.length === 0 || this.running >= this.maxConcurrent) {
      return;
    }
    
    const { fn, resolve, reject, timeoutId } = this.queue.shift();
    clearTimeout(timeoutId);
    
    this.running++;
    
    try {
      const result = await fn();
      resolve(result);
    } catch (error) {
      reject(error);
    } finally {
      this.running--;
      this.processQueue();
    }
  }
  
  getStatus() {
    return {
      name: this.name,
      running: this.running,
      queued: this.queue.length,
      utilization: (this.running / this.maxConcurrent * 100).toFixed(2) + '%'
    };
  }
}

class ResilienceOrchestrator {
  constructor() {
    this.circuitBreakers = new Map();
    this.retryPolicies = new Map();
    this.bulkheads = new Map();
    this.healthChecks = new Map();
    this.metrics = {
      totalRequests: 0,
      totalFailures: 0,
      circuitOpens: 0,
      fallbacksUsed: 0
    };
  }
  
  createCircuitBreaker(name, options) {
    const breaker = new CircuitBreaker(name, options);
    
    breaker.on('open', () => {
      this.metrics.circuitOpens++;
      console.log(`🔴 Circuit ${name} OPENED`);
    });
    
    breaker.on('half-open', () => {
      console.log(`🟡 Circuit ${name} HALF-OPEN`);
    });
    
    breaker.on('closed', () => {
      console.log(`🟢 Circuit ${name} CLOSED`);
    });
    
    this.circuitBreakers.set(name, breaker);
    return breaker;
  }
  
  createRetryPolicy(name, options) {
    const policy = new RetryPolicy(options);
    this.retryPolicies.set(name, policy);
    return policy;
  }
  
  createBulkhead(name, options) {
    const bulkhead = new BulkheadIsolation(name, options);
    this.bulkheads.set(name, bulkhead);
    return bulkhead;
  }
  
  async executeWithResilience(name, fn, options = {}) {
    const {
      circuitBreaker = true,
      retry = true,
      bulkhead = false,
      fallback = null
    } = options;
    
    this.metrics.totalRequests++;
    
    try {
      let executor = fn;
      
      // Wrap with bulkhead if needed
      if (bulkhead) {
        const bulkheadInstance = this.bulkheads.get(name) || 
          this.createBulkhead(name, options.bulkheadOptions);
        
        const originalExecutor = executor;
        executor = () => bulkheadInstance.execute(originalExecutor);
      }
      
      // Wrap with retry if needed
      if (retry) {
        const retryPolicy = this.retryPolicies.get(name) || 
          this.createRetryPolicy(name, options.retryOptions);
        
        const originalExecutor = executor;
        executor = () => retryPolicy.execute(originalExecutor);
      }
      
      // Wrap with circuit breaker if needed
      if (circuitBreaker) {
        const breaker = this.circuitBreakers.get(name) || 
          this.createCircuitBreaker(name, options.circuitBreakerOptions);
        
        return await breaker.execute(executor, fallback);
      }
      
      return await executor();
      
    } catch (error) {
      this.metrics.totalFailures++;
      
      if (fallback) {
        this.metrics.fallbacksUsed++;
        return await fallback();
      }
      
      throw error;
    }
  }
  
  addHealthCheck(name, checkFn, interval = 30000) {
    const check = {
      name,
      fn: checkFn,
      lastCheck: null,
      lastStatus: 'UNKNOWN',
      interval
    };
    
    this.healthChecks.set(name, check);
    
    // Start health check
    setInterval(async () => {
      try {
        const healthy = await checkFn();
        check.lastCheck = Date.now();
        check.lastStatus = healthy ? 'HEALTHY' : 'UNHEALTHY';
      } catch (error) {
        check.lastStatus = 'ERROR';
        check.lastError = error.message;
      }
    }, interval);
  }
  
  getSystemHealth() {
    const health = {
      status: 'HEALTHY',
      circuitBreakers: {},
      bulkheads: {},
      healthChecks: {},
      metrics: this.metrics
    };
    
    // Check circuit breakers
    for (const [name, breaker] of this.circuitBreakers) {
      const status = breaker.getStatus();
      health.circuitBreakers[name] = status;
      
      if (status.state === 'OPEN') {
        health.status = 'DEGRADED';
      }
    }
    
    // Check bulkheads
    for (const [name, bulkhead] of this.bulkheads) {
      const status = bulkhead.getStatus();
      health.bulkheads[name] = status;
      
      if (parseFloat(status.utilization) > 80) {
        health.status = 'DEGRADED';
      }
    }
    
    // Check health checks
    for (const [name, check] of this.healthChecks) {
      health.healthChecks[name] = {
        status: check.lastStatus,
        lastCheck: check.lastCheck
      };
      
      if (check.lastStatus === 'UNHEALTHY' || check.lastStatus === 'ERROR') {
        health.status = 'UNHEALTHY';
      }
    }
    
    return health;
  }
  
  reset() {
    for (const breaker of this.circuitBreakers.values()) {
      breaker.reset();
    }
    
    this.metrics = {
      totalRequests: 0,
      totalFailures: 0,
      circuitOpens: 0,
      fallbacksUsed: 0
    };
  }
}

// Singleton instance
let orchestratorInstance = null;

function getResilienceOrchestrator() {
  if (!orchestratorInstance) {
    orchestratorInstance = new ResilienceOrchestrator();
  }
  return orchestratorInstance;
}

module.exports = {
  CircuitBreaker,
  RetryPolicy,
  BulkheadIsolation,
  ResilienceOrchestrator,
  getResilienceOrchestrator
};