/**
 * 🔄 AUTO-RECOVERY SYSTEM
 * Netflix-grade self-healing mechanisms
 */

const { spawn } = require('child_process');
const EventEmitter = require('events');

class AutoRecoverySystem extends EventEmitter {
  constructor(options = {}) {
    super();
    
    this.options = {
      maxRestarts: options.maxRestarts || 3,
      restartDelay: options.restartDelay || 2000,
      healthCheckInterval: options.healthCheckInterval || 30000,
      memoryThreshold: options.memoryThreshold || 500 * 1024 * 1024, // 500MB
      cpuThreshold: options.cpuThreshold || 80, // 80% CPU
      ...options
    };
    
    this.components = new Map();
    this.restartCounts = new Map();
    this.healthChecks = new Map();
  }
  
  /**
   * Register a component for monitoring
   */
  registerComponent(name, config) {
    this.components.set(name, {
      name,
      process: config.process || null,
      command: config.command,
      args: config.args || [],
      critical: config.critical || false,
      autoRestart: config.autoRestart !== false,
      healthCheck: config.healthCheck || null,
      status: 'unknown',
      lastHealth: null
    });
    
    this.restartCounts.set(name, 0);
    
    // Start health monitoring
    if (config.healthCheck) {
      this.startHealthMonitoring(name);
    }
    
    console.log(`🔄 Registered component: ${name} for auto-recovery`);
  }
  
  /**
   * Start health monitoring for a component
   */
  startHealthMonitoring(name) {
    const component = this.components.get(name);
    if (!component || !component.healthCheck) return;
    
    const checkHealth = async () => {
      try {
        const healthy = await component.healthCheck();
        component.lastHealth = Date.now();
        
        if (!healthy && component.status === 'running') {
          console.log(`⚠️ Component ${name} health check failed`);
          this.handleComponentFailure(name, 'health_check_failed');
        } else if (healthy && component.status !== 'running') {
          component.status = 'running';
          this.emit('recovered', { component: name });
        }
      } catch (error) {
        console.error(`❌ Health check error for ${name}:`, error.message);
        this.handleComponentFailure(name, 'health_check_error');
      }
    };
    
    // Initial check
    checkHealth();
    
    // Schedule periodic checks
    const intervalId = setInterval(checkHealth, this.options.healthCheckInterval);
    this.healthChecks.set(name, intervalId);
  }
  
  /**
   * Handle component failure with auto-recovery
   */
  async handleComponentFailure(name, reason) {
    const component = this.components.get(name);
    if (!component) return;
    
    console.log(`🚨 Component failure detected: ${name} (${reason})`);
    component.status = 'failed';
    
    this.emit('component-failed', {
      component: name,
      reason,
      critical: component.critical
    });
    
    // Check if auto-restart is enabled
    if (!component.autoRestart) {
      console.log(`⚠️ Auto-restart disabled for ${name}`);
      return;
    }
    
    // Check restart limit
    const restartCount = this.restartCounts.get(name) || 0;
    if (restartCount >= this.options.maxRestarts) {
      console.log(`❌ Max restarts (${this.options.maxRestarts}) reached for ${name}`);
      component.status = 'permanently_failed';
      
      if (component.critical) {
        this.emit('critical-failure', {
          component: name,
          reason: 'max_restarts_exceeded'
        });
      }
      return;
    }
    
    // Attempt restart
    await this.restartComponent(name);
  }
  
  /**
   * Restart a failed component
   */
  async restartComponent(name) {
    const component = this.components.get(name);
    if (!component) return false;
    
    const restartCount = this.restartCounts.get(name) || 0;
    console.log(`🔄 Attempting restart ${restartCount + 1}/${this.options.maxRestarts} for ${name}...`);
    
    // Kill existing process if any
    if (component.process && !component.process.killed) {
      component.process.kill('SIGTERM');
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    // Wait before restart (exponential backoff)
    const delay = this.options.restartDelay * Math.pow(2, restartCount);
    console.log(`⏳ Waiting ${delay}ms before restart...`);
    await new Promise(resolve => setTimeout(resolve, delay));
    
    try {
      // Start new process
      const newProcess = spawn(component.command, component.args, {
        env: { ...process.env, AUTO_RECOVERY: 'true' }
      });
      
      component.process = newProcess;
      component.status = 'restarting';
      
      // Handle process events
      newProcess.on('error', (error) => {
        console.error(`❌ Failed to restart ${name}:`, error.message);
        this.handleComponentFailure(name, 'restart_failed');
      });
      
      newProcess.on('exit', (code, signal) => {
        if (code !== 0 && component.status === 'running') {
          console.log(`⚠️ ${name} exited with code ${code}`);
          this.handleComponentFailure(name, `exit_code_${code}`);
        }
      });
      
      // Wait for process to stabilize
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // Verify recovery
      if (component.healthCheck) {
        const healthy = await component.healthCheck();
        if (healthy) {
          component.status = 'running';
          this.restartCounts.set(name, 0); // Reset counter on success
          console.log(`✅ ${name} successfully recovered!`);
          
          this.emit('component-recovered', {
            component: name,
            restartCount: restartCount + 1
          });
          
          return true;
        }
      } else {
        // Assume success if no health check
        component.status = 'running';
        this.restartCounts.set(name, 0);
        console.log(`✅ ${name} restarted (no health check)`);
        return true;
      }
    } catch (error) {
      console.error(`❌ Restart failed for ${name}:`, error.message);
      this.restartCounts.set(name, restartCount + 1);
      this.handleComponentFailure(name, 'restart_exception');
    }
    
    return false;
  }
  
  /**
   * Monitor system resources
   */
  startResourceMonitoring() {
    setInterval(() => {
      const usage = process.memoryUsage();
      const cpuUsage = process.cpuUsage();
      
      // Check memory threshold
      if (usage.heapUsed > this.options.memoryThreshold) {
        console.log(`⚠️ Memory threshold exceeded: ${(usage.heapUsed / 1024 / 1024).toFixed(2)}MB`);
        
        this.emit('resource-warning', {
          type: 'memory',
          usage: usage.heapUsed,
          threshold: this.options.memoryThreshold
        });
        
        // Trigger garbage collection if available
        if (global.gc) {
          console.log('🗑️ Triggering garbage collection...');
          global.gc();
        }
      }
      
      // Calculate CPU percentage (simplified)
      const cpuPercent = (cpuUsage.user + cpuUsage.system) / 1000000;
      if (cpuPercent > this.options.cpuThreshold) {
        console.log(`⚠️ CPU threshold exceeded: ${cpuPercent.toFixed(2)}%`);
        
        this.emit('resource-warning', {
          type: 'cpu',
          usage: cpuPercent,
          threshold: this.options.cpuThreshold
        });
      }
    }, 10000);
  }
  
  /**
   * Graceful degradation when resources are constrained
   */
  enableGracefulDegradation() {
    this.on('resource-warning', (warning) => {
      console.log(`📉 Enabling graceful degradation due to ${warning.type} pressure`);
      
      if (warning.type === 'memory') {
        // Reduce cache sizes
        this.emit('reduce-cache');
        
        // Disable non-critical features
        this.emit('disable-features', ['animations', 'previews']);
      } else if (warning.type === 'cpu') {
        // Reduce processing frequency
        this.emit('throttle-processing');
        
        // Queue non-critical tasks
        this.emit('queue-tasks');
      }
    });
  }
  
  /**
   * Get recovery status
   */
  getStatus() {
    const status = {
      components: {},
      totalRestarts: 0,
      failedComponents: [],
      healthyComponents: []
    };
    
    for (const [name, component] of this.components) {
      status.components[name] = {
        status: component.status,
        restarts: this.restartCounts.get(name) || 0,
        lastHealth: component.lastHealth,
        critical: component.critical
      };
      
      status.totalRestarts += this.restartCounts.get(name) || 0;
      
      if (component.status === 'failed' || component.status === 'permanently_failed') {
        status.failedComponents.push(name);
      } else if (component.status === 'running') {
        status.healthyComponents.push(name);
      }
    }
    
    return status;
  }
  
  /**
   * Clean up resources
   */
  shutdown() {
    // Clear health check intervals
    for (const intervalId of this.healthChecks.values()) {
      clearInterval(intervalId);
    }
    
    // Kill all managed processes
    for (const component of this.components.values()) {
      if (component.process && !component.process.killed) {
        component.process.kill('SIGTERM');
      }
    }
    
    this.components.clear();
    this.restartCounts.clear();
    this.healthChecks.clear();
  }
}

// Singleton instance
let recoveryInstance = null;

function getAutoRecovery() {
  if (!recoveryInstance) {
    recoveryInstance = new AutoRecoverySystem();
    recoveryInstance.startResourceMonitoring();
    recoveryInstance.enableGracefulDegradation();
  }
  return recoveryInstance;
}

module.exports = {
  AutoRecoverySystem,
  getAutoRecovery
};