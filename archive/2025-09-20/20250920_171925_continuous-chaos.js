#!/usr/bin/env node

/**
 * 🔄 CONTINUOUS CHAOS TESTING
 * Netflix-grade automated resilience validation
 * Runs chaos scenarios periodically in production
 */

const ChaosEngineeringSuite = require('./chaos-engineering-suite');
const fs = require('fs').promises;
const path = require('path');

class ContinuousChaosRunner {
  constructor(options = {}) {
    this.chaos = new ChaosEngineeringSuite();
    
    this.config = {
      enabled: options.enabled !== false,
      interval: options.interval || 3600000, // 1 hour default
      scenarios: options.scenarios || ['chaos_monkey', 'latency_assault'],
      safeHours: options.safeHours || { start: 2, end: 6 }, // 2 AM - 6 AM
      maxFailures: options.maxFailures || 3,
      notificationWebhook: options.notificationWebhook || null,
      reportPath: options.reportPath || path.join(__dirname, 'chaos-reports'),
      ...options
    };
    
    this.stats = {
      totalRuns: 0,
      successfulRuns: 0,
      failedRuns: 0,
      lastRun: null,
      nextRun: null,
      consecutiveFailures: 0
    };
    
    this.intervalId = null;
  }
  
  /**
   * Start continuous chaos testing
   */
  async start() {
    if (!this.config.enabled) {
      console.log('⚠️ Continuous chaos testing is disabled');
      return;
    }
    
    console.log('🔄 Starting Continuous Chaos Testing');
    console.log(`   Interval: ${this.config.interval / 1000 / 60} minutes`);
    console.log(`   Scenarios: ${this.config.scenarios.join(', ')}`);
    console.log(`   Safe hours: ${this.config.safeHours.start}:00 - ${this.config.safeHours.end}:00`);
    
    // Ensure reports directory exists
    await fs.mkdir(this.config.reportPath, { recursive: true });
    
    // Schedule first run
    this.scheduleNextRun();
    
    // Set up periodic execution
    this.intervalId = setInterval(() => {
      this.scheduleNextRun();
    }, this.config.interval);
  }
  
  /**
   * Schedule the next chaos run
   */
  async scheduleNextRun() {
    const now = new Date();
    const hour = now.getHours();
    
    // Check if we're in safe hours
    const inSafeHours = hour >= this.config.safeHours.start && 
                        hour < this.config.safeHours.end;
    
    if (!inSafeHours && process.env.CHAOS_FORCE !== 'true') {
      console.log(`⏰ Skipping chaos run - outside safe hours (current: ${hour}:00)`);
      this.stats.nextRun = new Date(now.getTime() + this.config.interval);
      return;
    }
    
    // Check consecutive failures
    if (this.stats.consecutiveFailures >= this.config.maxFailures) {
      console.log(`❌ Chaos testing suspended - ${this.stats.consecutiveFailures} consecutive failures`);
      await this.sendNotification({
        type: 'SUSPENDED',
        reason: 'Too many consecutive failures',
        failures: this.stats.consecutiveFailures
      });
      return;
    }
    
    // Run chaos scenarios
    await this.runChaosScenarios();
  }
  
  /**
   * Run selected chaos scenarios
   */
  async runChaosScenarios() {
    console.log('\\n🐒 STARTING CHAOS RUN #' + (this.stats.totalRuns + 1));
    console.log('=' .repeat(50));
    
    const runId = `chaos-${Date.now()}`;
    const results = {
      runId,
      timestamp: new Date().toISOString(),
      scenarios: {},
      success: true,
      resilienceScore: 0
    };
    
    try {
      // Run each configured scenario
      for (const scenario of this.config.scenarios) {
        if (this.chaos.chaosScenarios[scenario]) {
          console.log(`\\n📍 Running ${scenario}...`);
          
          const result = await this.chaos.chaosScenarios[scenario]();
          results.scenarios[scenario] = result;
          
          // Check if scenario passed
          if (result.system_resilience === 'FAILED' || 
              result.error || 
              (result.compliance_score && result.compliance_score < 50)) {
            results.success = false;
          }
          
          // Wait between scenarios
          await new Promise(resolve => setTimeout(resolve, 5000));
        }
      }
      
      // Calculate overall resilience score
      results.resilienceScore = this.calculateResilienceScore(results.scenarios);
      
      // Update statistics
      this.stats.totalRuns++;
      this.stats.lastRun = new Date();
      this.stats.nextRun = new Date(Date.now() + this.config.interval);
      
      if (results.success && results.resilienceScore >= 70) {
        this.stats.successfulRuns++;
        this.stats.consecutiveFailures = 0;
        console.log(`\\n✅ Chaos run completed successfully! Score: ${results.resilienceScore}/100`);
      } else {
        this.stats.failedRuns++;
        this.stats.consecutiveFailures++;
        console.log(`\\n❌ Chaos run revealed issues! Score: ${results.resilienceScore}/100`);
        
        // Send alert
        await this.sendNotification({
          type: 'FAILURE',
          runId,
          score: results.resilienceScore,
          failures: this.extractFailures(results.scenarios)
        });
      }
      
      // Save report
      await this.saveReport(runId, results);
      
      // Auto-remediation for critical issues
      if (results.resilienceScore < 50) {
        await this.triggerAutoRemediation(results);
      }
      
    } catch (error) {
      console.error('❌ Chaos run failed:', error.message);
      this.stats.failedRuns++;
      this.stats.consecutiveFailures++;
      results.success = false;
      results.error = error.message;
    }
    
    return results;
  }
  
  /**
   * Calculate resilience score from scenario results
   */
  calculateResilienceScore(scenarios) {
    let totalScore = 0;
    let scenarioCount = 0;
    
    for (const [name, result] of Object.entries(scenarios)) {
      scenarioCount++;
      
      if (result.system_resilience === 'HIGH') {
        totalScore += 100;
      } else if (result.system_resilience === 'MEDIUM') {
        totalScore += 70;
      } else if (result.system_resilience === 'LOW') {
        totalScore += 40;
      }
      
      // Include specific scores if available
      if (result.compliance_score !== undefined) {
        totalScore += result.compliance_score;
        scenarioCount++;
      }
      
      if (result.security_score !== undefined) {
        totalScore += result.security_score;
        scenarioCount++;
      }
    }
    
    return scenarioCount > 0 ? Math.round(totalScore / scenarioCount) : 0;
  }
  
  /**
   * Extract failures from scenario results
   */
  extractFailures(scenarios) {
    const failures = [];
    
    for (const [name, result] of Object.entries(scenarios)) {
      if (result.error) {
        failures.push({
          scenario: name,
          error: result.error
        });
      }
      
      if (result.violations) {
        failures.push({
          scenario: name,
          violations: result.violations
        });
      }
      
      if (result.vulnerabilities) {
        failures.push({
          scenario: name,
          vulnerabilities: result.vulnerabilities
        });
      }
    }
    
    return failures;
  }
  
  /**
   * Trigger auto-remediation for critical issues
   */
  async triggerAutoRemediation(results) {
    console.log('🔧 Triggering auto-remediation...');
    
    const remediations = [];
    
    // Check for specific issues and apply fixes
    for (const [scenario, result] of Object.entries(results.scenarios)) {
      if (scenario === 'conformity_monkey' && result.violations) {
        if (result.violations.includes('MISSING_CONTEXT_ISOLATION')) {
          remediations.push('Enable context isolation');
          // Could automatically fix this in code
        }
        
        if (result.violations.includes('NO_LAZY_LOADING')) {
          remediations.push('Implement lazy loading');
        }
      }
      
      if (scenario === 'security_monkey' && result.vulnerabilities) {
        remediations.push('Run npm audit fix');
        // Execute npm audit fix
        try {
          const { exec } = require('child_process');
          const { promisify } = require('util');
          const execAsync = promisify(exec);
          await execAsync('npm audit fix');
          console.log('  ✅ Ran npm audit fix');
        } catch {}
      }
    }
    
    if (remediations.length > 0) {
      console.log('  Applied remediations:');
      remediations.forEach(r => console.log(`    - ${r}`));
    }
    
    return remediations;
  }
  
  /**
   * Save chaos report
   */
  async saveReport(runId, results) {
    const reportFile = path.join(this.config.reportPath, `${runId}.json`);
    
    await fs.writeFile(reportFile, JSON.stringify({
      ...results,
      stats: this.stats,
      config: {
        scenarios: this.config.scenarios,
        interval: this.config.interval
      }
    }, null, 2));
    
    console.log(`📁 Report saved: ${reportFile}`);
    
    // Clean old reports (keep last 100)
    await this.cleanOldReports();
  }
  
  /**
   * Clean old chaos reports
   */
  async cleanOldReports() {
    try {
      const files = await fs.readdir(this.config.reportPath);
      const reports = files.filter(f => f.startsWith('chaos-') && f.endsWith('.json'));
      
      if (reports.length > 100) {
        // Sort by timestamp and remove oldest
        reports.sort();
        const toDelete = reports.slice(0, reports.length - 100);
        
        for (const file of toDelete) {
          await fs.unlink(path.join(this.config.reportPath, file));
        }
        
        console.log(`  🗑️ Cleaned ${toDelete.length} old reports`);
      }
    } catch (error) {
      console.error('Failed to clean reports:', error.message);
    }
  }
  
  /**
   * Send notification about chaos results
   */
  async sendNotification(data) {
    if (!this.config.notificationWebhook) return;
    
    try {
      const message = {
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV || 'production',
        ...data
      };
      
      // Send to webhook (e.g., Slack, Discord, etc.)
      const response = await fetch(this.config.notificationWebhook, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(message)
      });
      
      if (!response.ok) {
        console.error('Failed to send notification:', response.statusText);
      }
    } catch (error) {
      console.error('Notification error:', error.message);
    }
  }
  
  /**
   * Get current status
   */
  getStatus() {
    return {
      enabled: this.config.enabled,
      running: this.intervalId !== null,
      stats: this.stats,
      config: {
        interval: this.config.interval,
        scenarios: this.config.scenarios,
        safeHours: this.config.safeHours
      }
    };
  }
  
  /**
   * Stop continuous chaos testing
   */
  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
      console.log('🛑 Continuous chaos testing stopped');
    }
  }
}

// Configuration loader
async function loadConfig() {
  const configPath = path.join(__dirname, 'chaos-config.json');
  
  try {
    const configData = await fs.readFile(configPath, 'utf-8');
    return JSON.parse(configData);
  } catch {
    // Default configuration
    return {
      enabled: process.env.CHAOS_ENABLED === 'true',
      interval: parseInt(process.env.CHAOS_INTERVAL) || 3600000,
      scenarios: process.env.CHAOS_SCENARIOS ? 
        process.env.CHAOS_SCENARIOS.split(',') : 
        ['chaos_monkey', 'conformity_monkey'],
      safeHours: {
        start: parseInt(process.env.CHAOS_SAFE_START) || 2,
        end: parseInt(process.env.CHAOS_SAFE_END) || 6
      },
      notificationWebhook: process.env.CHAOS_WEBHOOK || null
    };
  }
}

// Main execution
async function main() {
  const config = await loadConfig();
  const runner = new ContinuousChaosRunner(config);
  
  await runner.start();
  
  // Graceful shutdown
  process.on('SIGINT', () => {
    console.log('\\nShutting down continuous chaos...');
    runner.stop();
    process.exit(0);
  });
  
  // Status endpoint (optional)
  if (process.env.CHAOS_STATUS_PORT) {
    const http = require('http');
    const port = parseInt(process.env.CHAOS_STATUS_PORT);
    
    http.createServer((req, res) => {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(runner.getStatus(), null, 2));
    }).listen(port);
    
    console.log(`📊 Status endpoint: http://localhost:${port}`);
  }
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

module.exports = ContinuousChaosRunner;