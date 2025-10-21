#!/usr/bin/env node

/**
 * 🧪 NEUROMON TEST SUITE
 * Demonstrates the symbiotic AI system in action
 */

import { NeuromonSymbioticEngine } from './neuromon_symbiotic_engine.js'

async function runTests() {
  console.log(`
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                  🧪 NEUROMON TEST SUITE 🧪                       ║
║                                                                  ║
║         Testing Symbiotic AI Processing Capabilities            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
  `)
  
  // Initialize Neuromon
  const neuromon = new NeuromonSymbioticEngine()
  await neuromon.initialize()
  
  // Test Cases
  const testCases = [
    {
      name: 'Simple Code Analysis',
      task: {
        type: 'code_analysis',
        description: 'Analyze this function for issues',
        prompt: `
        function getData() {
          let data = [];
          for (let i = 0; i < 1000000; i++) {
            data.push({ id: i, value: Math.random() });
          }
          return data;
        }
        `,
        priority: 'LOW'
      }
    },
    {
      name: 'Memory Leak Detection',
      task: {
        type: 'debug_analysis',
        description: 'Find potential memory leaks',
        context: 'Server shows increasing memory usage over time',
        keywords: ['memory', 'leak', 'gc'],
        priority: 'HIGH'
      }
    },
    {
      name: 'Architecture Design',
      task: {
        type: 'system_design',
        description: 'Design a scalable microservices architecture',
        context: 'Need to handle 1M requests per second',
        priority: 'CRITICAL'
      }
    },
    {
      name: 'Performance Optimization',
      task: {
        type: 'optimization',
        description: 'Optimize database queries for better performance',
        context: 'Current queries take 5+ seconds',
        keywords: ['database', 'query', 'optimization'],
        priority: 'MEDIUM'
      }
    }
  ]
  
  // Run tests
  console.log('\n📋 Running Test Cases:\n')
  
  for (const testCase of testCases) {
    console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
    console.log(`📝 Test: ${testCase.name}`)
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)
    
    const startTime = Date.now()
    const result = await neuromon.processTask(testCase.task)
    const duration = Date.now() - startTime
    
    console.log(`\n📊 Results:`)
    console.log(`   Success: ${result.success ? '✅' : '❌'}`)
    console.log(`   Confidence: ${((result.confidence || 0) * 100).toFixed(1)}%`)
    console.log(`   Method: ${result.method || result.processingPath || 'unknown'}`)
    console.log(`   Duration: ${duration}ms`)
    
    if (result.response) {
      console.log(`   Response Preview: ${result.response.substring(0, 100)}...`)
    }
  }
  
  // Show final metrics
  console.log(`\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
  console.log(`📊 FINAL METRICS`)
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)
  
  const metrics = neuromon.metrics
  console.log(`   Tasks Processed: ${metrics.tasksProcessed}`)
  console.log(`   Ollama Computations: ${metrics.ollamaComputations}`)
  console.log(`   Claude Consultations: ${metrics.claudeConsultations}`)
  console.log(`   Challenges Logged: ${metrics.challengesLogged}`)
  console.log(`   Efficiency Score: ${metrics.efficiencyScore.toFixed(2)}`)
  console.log(`   Symbiotic Sync Rate: ${metrics.symbioticSyncRate}`)
  
  // Calculate token savings
  const tokensSaved = metrics.ollamaComputations * 1000 // Estimate 1000 tokens per Ollama call
  const costSaved = (tokensSaved / 1000000) * 15 // $15 per million tokens (Claude pricing)
  
  console.log(`\n💰 COST ANALYSIS:`)
  console.log(`   Tokens Saved: ${tokensSaved.toLocaleString()}`)
  console.log(`   Estimated Savings: $${costSaved.toFixed(2)}`)
  console.log(`   Efficiency vs Pure Claude: ${((metrics.ollamaComputations / metrics.tasksProcessed) * 100).toFixed(1)}% local processing`)
  
  // Show challenges if any
  if (neuromon.challengeLog.length > 0) {
    console.log(`\n📝 CHALLENGES LOGGED FOR CLAUDE:`)
    neuromon.challengeLog.forEach(challenge => {
      console.log(`   - ${challenge.reason} (Task: ${challenge.task.type})`)
    })
    console.log(`\n   Check ./challenge_logs/ for detailed challenge information`)
  }
  
  // Evolution status
  const evolutionStatus = {
    patterns: neuromon.evolutionaryMemory.patterns.size,
    solutions: neuromon.evolutionaryMemory.solutions.size,
    failures: neuromon.evolutionaryMemory.failures.size
  }
  
  console.log(`\n🧬 EVOLUTION STATUS:`)
  console.log(`   Patterns Learned: ${evolutionStatus.patterns}`)
  console.log(`   Solutions Stored: ${evolutionStatus.solutions}`)
  console.log(`   Failures Analyzed: ${evolutionStatus.failures}`)
  
  console.log(`\n✨ Test suite complete! Neuromon is learning and evolving.`)
  
  // Graceful shutdown
  process.exit(0)
}

// Run tests
runTests().catch(error => {
  console.error('❌ Test suite failed:', error)
  process.exit(1)
})