/**
 * Sistema de Monitoramento e Logs Avançado para Digimundo
 * Implementa telemetria, debugging e análise de performance
 */

const { app } = require('electron');
const fs = require('fs');
const path = require('path');
const { EventEmitter } = require('events');

class DigimundoMonitor extends EventEmitter {
  constructor() {
    super();
    this.logDir = path.join(app.getPath('userData'), 'logs');
    this.metrics = {
      startup: {},
      ollama: {},
      claude: {},
      performance: {},
      errors: []
    };
    
    this.ensureLogDirectory();
    this.startTime = Date.now();
  }
  
  ensureLogDirectory() {
    if (!fs.existsSync(this.logDir)) {
      fs.mkdirSync(this.logDir, { recursive: true });
    }
  }
  
  log(level, component, message, data = {}) {
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      level,
      component,
      message,
      data,
      uptime: Date.now() - this.startTime
    };
    
    // Emitir evento para listeners
    this.emit('log', logEntry);
    
    // Salvar em arquivo
    const logFile = path.join(this.logDir, `digimundo-${new Date().toISOString().split('T')[0]}.log`);
    fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n');
    
    // Console output em desenvolvimento
    if (process.env.NODE_ENV === 'development') {
      const prefix = `[${level.toUpperCase()}] [${component}]`;
      console.log(`${prefix} ${message}`, data);
    }
  }
  
  trackStartup(phase, duration) {
    this.metrics.startup[phase] = duration;
    this.log('info', 'STARTUP', `Phase ${phase} completed in ${duration}ms`);
  }
  
  trackOllamaOperation(operation, success, duration, details = {}) {
    if (!this.metrics.ollama[operation]) {
      this.metrics.ollama[operation] = {
        total: 0,
        success: 0,
        failed: 0,
        avgDuration: 0
      };
    }
    
    const metric = this.metrics.ollama[operation];
    metric.total++;
    if (success) metric.success++;
    else metric.failed++;
    
    // Calcular média móvel
    metric.avgDuration = (metric.avgDuration * (metric.total - 1) + duration) / metric.total;
    
    this.log(success ? 'info' : 'error', 'OLLAMA', 
      `Operation ${operation} ${success ? 'succeeded' : 'failed'}`, 
      { duration, ...details });
  }
  
  trackClaudeOperation(operation, success, details = {}) {
    if (!this.metrics.claude[operation]) {
      this.metrics.claude[operation] = {
        total: 0,
        success: 0,
        failed: 0
      };
    }
    
    const metric = this.metrics.claude[operation];
    metric.total++;
    if (success) metric.success++;
    else metric.failed++;
    
    this.log(success ? 'info' : 'error', 'CLAUDE', 
      `Operation ${operation} ${success ? 'succeeded' : 'failed'}`, details);
  }
  
  trackPerformance(metric, value) {
    if (!this.metrics.performance[metric]) {
      this.metrics.performance[metric] = {
        samples: [],
        min: value,
        max: value,
        avg: value
      };
    }
    
    const perf = this.metrics.performance[metric];
    perf.samples.push(value);
    
    // Manter apenas últimas 100 amostras
    if (perf.samples.length > 100) {
      perf.samples.shift();
    }
    
    perf.min = Math.min(...perf.samples);
    perf.max = Math.max(...perf.samples);
    perf.avg = perf.samples.reduce((a, b) => a + b, 0) / perf.samples.length;
    
    this.log('debug', 'PERFORMANCE', `Metric ${metric}: ${value}`, {
      min: perf.min,
      max: perf.max,
      avg: perf.avg
    });
  }
  
  trackError(component, error, context = {}) {
    const errorEntry = {
      timestamp: new Date().toISOString(),
      component,
      message: error.message,
      stack: error.stack,
      context
    };
    
    this.metrics.errors.push(errorEntry);
    
    // Manter apenas últimos 100 erros
    if (this.metrics.errors.length > 100) {
      this.metrics.errors.shift();
    }
    
    this.log('error', component, error.message, {
      stack: error.stack,
      ...context
    });
  }
  
  getHealthStatus() {
    const now = Date.now();
    const uptime = now - this.startTime;
    
    // Calcular health score
    let healthScore = 100;
    
    // Penalizar por erros recentes
    const recentErrors = this.metrics.errors.filter(e => 
      new Date(e.timestamp).getTime() > now - 300000 // Últimos 5 minutos
    );
    healthScore -= recentErrors.length * 5;
    
    // Penalizar por falhas no Ollama
    Object.values(this.metrics.ollama).forEach(metric => {
      if (metric.total > 0) {
        const failureRate = metric.failed / metric.total;
        healthScore -= failureRate * 20;
      }
    });
    
    // Penalizar por performance ruim
    Object.entries(this.metrics.performance).forEach(([name, perf]) => {
      if (name === 'responseTime' && perf.avg > 1000) {
        healthScore -= 10;
      }
      if (name === 'memoryUsage' && perf.avg > 500) {
        healthScore -= 15;
      }
    });
    
    healthScore = Math.max(0, Math.min(100, healthScore));
    
    return {
      status: healthScore > 80 ? 'healthy' : healthScore > 50 ? 'degraded' : 'critical',
      score: healthScore,
      uptime,
      metrics: this.metrics,
      recentErrors
    };
  }
  
  generateReport() {
    const health = this.getHealthStatus();
    const reportPath = path.join(this.logDir, `report-${Date.now()}.json`);
    
    const report = {
      timestamp: new Date().toISOString(),
      health,
      systemInfo: {
        platform: process.platform,
        arch: process.arch,
        nodeVersion: process.version,
        electronVersion: process.versions.electron
      }
    };
    
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    this.log('info', 'MONITOR', `Health report generated: ${reportPath}`);
    
    return report;
  }
  
  // Método para limpar logs antigos
  cleanOldLogs(daysToKeep = 7) {
    const cutoffTime = Date.now() - (daysToKeep * 24 * 60 * 60 * 1000);
    
    fs.readdirSync(this.logDir).forEach(file => {
      const filePath = path.join(this.logDir, file);
      const stats = fs.statSync(filePath);
      
      if (stats.mtimeMs < cutoffTime) {
        fs.unlinkSync(filePath);
        this.log('info', 'MONITOR', `Deleted old log file: ${file}`);
      }
    });
  }
}

module.exports = DigimundoMonitor;