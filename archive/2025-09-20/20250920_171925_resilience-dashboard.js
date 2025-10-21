#!/usr/bin/env node

/**
 * 📊 RESILIENCE DASHBOARD
 * Real-time monitoring of system resilience metrics
 * Netflix-grade observability
 */

const http = require('http');
const path = require('path');
const { getResilienceOrchestrator } = require('./src/main/resilience-layer');
const { getAutoRecovery } = require('./src/main/auto-recovery');

class ResilienceDashboard {
  constructor(port = 8089) {
    this.port = port;
    this.resilience = getResilienceOrchestrator();
    this.recovery = getAutoRecovery();
    this.server = null;
    
    // Metrics history
    this.metricsHistory = {
      timestamps: [],
      circuitStates: [],
      errorRates: [],
      recoveryTimes: [],
      healthScores: []
    };
    
    // Start collecting metrics
    this.startMetricsCollection();
  }
  
  startMetricsCollection() {
    setInterval(() => {
      const health = this.resilience.getSystemHealth();
      const recovery = this.recovery.getStatus();
      const timestamp = new Date().toISOString();
      
      // Store metrics (keep last 100 points)
      this.metricsHistory.timestamps.push(timestamp);
      
      // Calculate error rate
      const totalRequests = health.metrics.totalRequests || 1;
      const errorRate = (health.metrics.totalFailures / totalRequests * 100).toFixed(2);
      this.metricsHistory.errorRates.push(parseFloat(errorRate));
      
      // Calculate health score
      let healthScore = 100;
      if (health.status === 'DEGRADED') healthScore = 70;
      if (health.status === 'UNHEALTHY') healthScore = 30;
      this.metricsHistory.healthScores.push(healthScore);
      
      // Track circuit states
      let openCircuits = 0;
      for (const breaker of Object.values(health.circuitBreakers)) {
        if (breaker.state === 'OPEN') openCircuits++;
      }
      this.metricsHistory.circuitStates.push(openCircuits);
      
      // Limit history size
      if (this.metricsHistory.timestamps.length > 100) {
        this.metricsHistory.timestamps.shift();
        this.metricsHistory.errorRates.shift();
        this.metricsHistory.healthScores.shift();
        this.metricsHistory.circuitStates.shift();
      }
    }, 5000);
  }
  
  generateDashboardHTML() {
    const health = this.resilience.getSystemHealth();
    const recovery = this.recovery.getStatus();
    
    return `<!DOCTYPE html>
<html>
<head>
  <title>🛡️ Digimundo Resilience Dashboard</title>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="5">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 20px;
    }
    .container {
      max-width: 1400px;
      margin: 0 auto;
    }
    h1 {
      text-align: center;
      font-size: 2.5em;
      margin-bottom: 30px;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
    }
    .metric-card {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border-radius: 15px;
      padding: 20px;
      border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .metric-card h2 {
      font-size: 1.2em;
      margin-bottom: 15px;
      opacity: 0.9;
    }
    .metric-value {
      font-size: 2.5em;
      font-weight: bold;
      margin-bottom: 10px;
    }
    .metric-label {
      font-size: 0.9em;
      opacity: 0.8;
    }
    .status-healthy { color: #4ade80; }
    .status-degraded { color: #fbbf24; }
    .status-unhealthy { color: #f87171; }
    .status-unknown { color: #94a3b8; }
    
    .circuit-breakers {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border-radius: 15px;
      padding: 20px;
      margin-bottom: 20px;
    }
    .circuit-breaker {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px;
      margin: 10px 0;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 8px;
    }
    .circuit-state {
      padding: 5px 10px;
      border-radius: 5px;
      font-weight: bold;
    }
    .state-closed { background: #22c55e; }
    .state-open { background: #ef4444; }
    .state-half-open { background: #f59e0b; }
    
    .health-checks {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border-radius: 15px;
      padding: 20px;
    }
    .health-check {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px;
      margin: 10px 0;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 8px;
    }
    .health-status {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      display: inline-block;
      margin-right: 10px;
    }
    .health-healthy { background: #22c55e; }
    .health-unhealthy { background: #ef4444; }
    .health-unknown { background: #6b7280; }
    
    .recovery-status {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border-radius: 15px;
      padding: 20px;
      margin-top: 20px;
    }
    .component-status {
      display: flex;
      justify-content: space-between;
      padding: 10px;
      margin: 10px 0;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 8px;
    }
    
    .chart {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border-radius: 15px;
      padding: 20px;
      margin-top: 20px;
      height: 300px;
      position: relative;
    }
    
    .timestamp {
      text-align: center;
      opacity: 0.7;
      margin-top: 30px;
      font-size: 0.9em;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🛡️ Digimundo Resilience Dashboard</h1>
    
    <div class="metrics-grid">
      <div class="metric-card">
        <h2>System Health</h2>
        <div class="metric-value status-${health.status.toLowerCase()}">${health.status}</div>
        <div class="metric-label">Overall system status</div>
      </div>
      
      <div class="metric-card">
        <h2>Total Requests</h2>
        <div class="metric-value">${health.metrics.totalRequests || 0}</div>
        <div class="metric-label">Since startup</div>
      </div>
      
      <div class="metric-card">
        <h2>Error Rate</h2>
        <div class="metric-value">${health.metrics.totalRequests ? 
          ((health.metrics.totalFailures / health.metrics.totalRequests * 100).toFixed(2)) : 0}%</div>
        <div class="metric-label">Failed requests</div>
      </div>
      
      <div class="metric-card">
        <h2>Circuit Breakers Open</h2>
        <div class="metric-value">${Object.values(health.circuitBreakers).filter(cb => cb.state === 'OPEN').length}</div>
        <div class="metric-label">Out of ${Object.keys(health.circuitBreakers).length} total</div>
      </div>
      
      <div class="metric-card">
        <h2>Fallbacks Used</h2>
        <div class="metric-value">${health.metrics.fallbacksUsed || 0}</div>
        <div class="metric-label">Graceful degradations</div>
      </div>
      
      <div class="metric-card">
        <h2>Auto Restarts</h2>
        <div class="metric-value">${recovery.totalRestarts || 0}</div>
        <div class="metric-label">Component recoveries</div>
      </div>
    </div>
    
    <div class="circuit-breakers">
      <h2>Circuit Breakers</h2>
      ${Object.entries(health.circuitBreakers).map(([name, breaker]) => `
        <div class="circuit-breaker">
          <div>
            <strong>${name}</strong>
            <span style="margin-left: 20px; opacity: 0.8;">
              ${breaker.metrics.requests} requests | 
              ${breaker.metrics.errorRate} error rate | 
              ${breaker.metrics.avgLatency} avg latency
            </span>
          </div>
          <span class="circuit-state state-${breaker.state.toLowerCase()}">${breaker.state}</span>
        </div>
      `).join('')}
    </div>
    
    <div class="health-checks">
      <h2>Health Checks</h2>
      ${Object.entries(health.healthChecks).map(([name, check]) => `
        <div class="health-check">
          <div>
            <span class="health-status health-${check.status.toLowerCase()}"></span>
            <strong>${name}</strong>
          </div>
          <span>${check.status} ${check.lastCheck ? 
            `(${new Date(check.lastCheck).toLocaleTimeString()})` : ''}</span>
        </div>
      `).join('')}
    </div>
    
    <div class="recovery-status">
      <h2>Auto-Recovery Status</h2>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
        <div>
          <h3 style="margin-bottom: 10px; opacity: 0.9;">Healthy Components</h3>
          ${recovery.healthyComponents.map(comp => `
            <div class="component-status">
              <span>✅ ${comp}</span>
              <span>${recovery.components[comp]?.restarts || 0} restarts</span>
            </div>
          `).join('') || '<div style="opacity: 0.6;">No healthy components</div>'}
        </div>
        <div>
          <h3 style="margin-bottom: 10px; opacity: 0.9;">Failed Components</h3>
          ${recovery.failedComponents.map(comp => `
            <div class="component-status">
              <span>❌ ${comp}</span>
              <span>${recovery.components[comp]?.status || 'unknown'}</span>
            </div>
          `).join('') || '<div style="opacity: 0.6;">No failed components</div>'}
        </div>
      </div>
    </div>
    
    <div class="chart">
      <h2>Health Score Trend (Last 5 minutes)</h2>
      <canvas id="healthChart" style="width: 100%; height: 250px;"></canvas>
    </div>
    
    <div class="timestamp">
      Last updated: ${new Date().toLocaleString()} | Auto-refresh: 5 seconds
    </div>
  </div>
  
  <script>
    // Simple health score visualization
    const canvas = document.getElementById('healthChart');
    if (canvas && canvas.getContext) {
      const ctx = canvas.getContext('2d');
      const scores = ${JSON.stringify(this.metricsHistory.healthScores.slice(-20))};
      
      if (scores.length > 0) {
        const width = canvas.width = canvas.offsetWidth;
        const height = canvas.height = 250;
        const padding = 20;
        const graphWidth = width - padding * 2;
        const graphHeight = height - padding * 2;
        
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        scores.forEach((score, i) => {
          const x = padding + (i / (scores.length - 1)) * graphWidth;
          const y = padding + (1 - score / 100) * graphHeight;
          
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        });
        
        ctx.stroke();
        
        // Draw points
        scores.forEach((score, i) => {
          const x = padding + (i / (scores.length - 1)) * graphWidth;
          const y = padding + (1 - score / 100) * graphHeight;
          
          ctx.fillStyle = score >= 70 ? '#4ade80' : score >= 30 ? '#fbbf24' : '#f87171';
          ctx.beginPath();
          ctx.arc(x, y, 4, 0, Math.PI * 2);
          ctx.fill();
        });
      }
    }
  </script>
</body>
</html>`;
  }
  
  start() {
    this.server = http.createServer((req, res) => {
      if (req.url === '/health') {
        // JSON endpoint for monitoring tools
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          health: this.resilience.getSystemHealth(),
          recovery: this.recovery.getStatus(),
          metrics: this.metricsHistory
        }, null, 2));
      } else {
        // HTML dashboard
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(this.generateDashboardHTML());
      }
    });
    
    this.server.listen(this.port, () => {
      console.log(`📊 Resilience Dashboard running at http://localhost:${this.port}`);
      console.log(`📡 Health API available at http://localhost:${this.port}/health`);
    });
  }
  
  stop() {
    if (this.server) {
      this.server.close();
    }
  }
}

// Start dashboard if run directly
if (require.main === module) {
  const dashboard = new ResilienceDashboard();
  dashboard.start();
  
  console.log('\nPress Ctrl+C to stop the dashboard\n');
  
  process.on('SIGINT', () => {
    console.log('\nStopping dashboard...');
    dashboard.stop();
    process.exit(0);
  });
}

module.exports = ResilienceDashboard;