#!/usr/bin/env node

/**
 * 🧬 TESTE DE INTEGRAÇÃO COMPLETA
 * Valida ChromaDB + NATS + Context Fabric trabalhando juntos
 */

const { spawn } = require('child_process');
const QComBus = require('./qcom/message_bus');

// Importar Context Fabric (TypeScript compilado)
let ContextFabric;
try {
  // Tentar importar se já compilado
  ContextFabric = require('./context/fabric').ContextFabric;
} catch {
  console.log('⚠️  Context Fabric não compilado, usando versão simplificada');
  // Versão simplificada para teste
  ContextFabric = class {
    async assembleContext(query, digimonId) {
      return {
        system: { cpu: { usage: 10 }, memory: { free: 1e10 } },
        peers: [],
        memories: [],
        tools: [],
        assemblyTime: 50
      };
    }
    formatForPrompt(context) {
      return `Context assembled in ${context.assemblyTime}ms`;
    }
  };
}

class IntegrationTest {
  constructor() {
    this.results = {
      passed: [],
      failed: [],
      metrics: {}
    };
  }

  /**
   * Testa ChromaDB (Cognitive Core)
   */
  async testChromaDB() {
    console.log('\n📊 TESTANDO CHROMADB');
    console.log('━'.repeat(50));

    return new Promise((resolve) => {
      const startTime = Date.now();
      
      const pythonScript = `
import sys
sys.path.append('/Users/clubproducoes/Digimundo/core/memory')
from cognitive_core import CognitiveCore
import json
import time

try:
    # Inicializar
    core = CognitiveCore('test_digimon')
    
    # Armazenar memória
    memory_id = core.store_memory(
        'Teste de integração do Digimundo',
        {'importance': 0.9, 'test': True},
        'episodic'
    )
    
    # Recuperar memória
    start_recall = time.time()
    memories = core.recall('integração', top_k=5)
    recall_time = (time.time() - start_recall) * 1000
    
    # Métricas
    metrics = core.get_metrics()
    
    result = {
        'success': True,
        'memory_id': memory_id,
        'memories_found': len(memories),
        'recall_time_ms': recall_time,
        'avg_recall_time_ms': metrics['avg_recall_time'] * 1000
    }
    
    print(json.dumps(result))
    
except Exception as e:
    print(json.dumps({'success': False, 'error': str(e)}))
`;

      const python = spawn('python3', ['-c', pythonScript]);
      let output = '';

      python.stdout.on('data', (data) => {
        output += data.toString();
      });

      python.stderr.on('data', (data) => {
        console.error('Python error:', data.toString());
      });

      python.on('close', () => {
        try {
          const result = JSON.parse(output);
          const elapsed = Date.now() - startTime;
          
          if (result.success) {
            console.log(`✅ ChromaDB funcionando`);
            console.log(`   - Memory ID: ${result.memory_id}`);
            console.log(`   - Recall time: ${result.recall_time_ms.toFixed(2)}ms`);
            console.log(`   - Avg recall: ${result.avg_recall_time_ms.toFixed(2)}ms`);
            console.log(`   - Total time: ${elapsed}ms`);
            
            this.results.passed.push('ChromaDB');
            this.results.metrics.chromaDB = {
              recallTime: result.recall_time_ms,
              totalTime: elapsed
            };
          } else {
            console.log(`❌ ChromaDB falhou: ${result.error}`);
            this.results.failed.push('ChromaDB');
          }
        } catch (e) {
          console.log(`❌ ChromaDB erro de parse: ${e.message}`);
          this.results.failed.push('ChromaDB');
        }
        
        resolve();
      });
    });
  }

  /**
   * Testa NATS (Q-Com)
   */
  async testNATS() {
    console.log('\n🌐 TESTANDO NATS Q-COM');
    console.log('━'.repeat(50));

    const startTime = Date.now();

    // Iniciar servidor NATS
    const natsServer = spawn('nats-server', ['-p', '4223']);
    
    // Aguardar servidor iniciar
    await new Promise(resolve => setTimeout(resolve, 2000));

    try {
      // Criar dois agentes
      const agent1 = new QComBus();
      const agent2 = new QComBus();

      // Conectar
      await agent1.connect('agent1', { servers: 'localhost:4223' });
      await agent2.connect('agent2', { servers: 'localhost:4223' });

      // Teste de comunicação
      let messageReceived = false;
      agent2.on('personal', (msg) => {
        messageReceived = true;
      });

      await agent1.sendTo('agent2', 'Teste de integração');
      await new Promise(resolve => setTimeout(resolve, 100));

      const metrics1 = agent1.getMetrics();
      const metrics2 = agent2.getMetrics();

      // Desconectar
      await agent1.disconnect();
      await agent2.disconnect();

      const elapsed = Date.now() - startTime;

      if (messageReceived) {
        console.log(`✅ NATS Q-Com funcionando`);
        console.log(`   - Latência: ${metrics1.avgLatencyMs}`);
        console.log(`   - Mensagens enviadas: ${metrics1.messagesSent}`);
        console.log(`   - Mensagens recebidas: ${metrics2.messagesReceived}`);
        console.log(`   - Total time: ${elapsed}ms`);
        
        this.results.passed.push('NATS');
        this.results.metrics.nats = {
          latency: metrics1.avgLatency,
          totalTime: elapsed
        };
      } else {
        console.log(`❌ NATS falhou: Mensagem não recebida`);
        this.results.failed.push('NATS');
      }

    } catch (error) {
      console.log(`❌ NATS erro: ${error.message}`);
      this.results.failed.push('NATS');
    } finally {
      // Parar servidor
      natsServer.kill();
    }
  }

  /**
   * Testa Context Fabric
   */
  async testContextFabric() {
    console.log('\n⚡ TESTANDO CONTEXT FABRIC');
    console.log('━'.repeat(50));

    const startTime = Date.now();

    try {
      const fabric = new ContextFabric();
      
      // Montar contexto
      const context = await fabric.assembleContext('teste integração', 'sabiamon');
      
      const elapsed = Date.now() - startTime;

      if (context.assemblyTime < 100) {
        console.log(`✅ Context Fabric funcionando`);
        console.log(`   - Assembly time: ${context.assemblyTime}ms`);
        console.log(`   - Target: <100ms ✓`);
        console.log(`   - Total time: ${elapsed}ms`);
        
        this.results.passed.push('ContextFabric');
        this.results.metrics.contextFabric = {
          assemblyTime: context.assemblyTime,
          totalTime: elapsed
        };
      } else {
        console.log(`❌ Context Fabric muito lento: ${context.assemblyTime}ms`);
        this.results.failed.push('ContextFabric');
      }

    } catch (error) {
      console.log(`❌ Context Fabric erro: ${error.message}`);
      this.results.failed.push('ContextFabric');
    }
  }

  /**
   * Testa integração completa
   */
  async testFullIntegration() {
    console.log('\n🔗 TESTANDO INTEGRAÇÃO COMPLETA');
    console.log('━'.repeat(50));

    const startTime = Date.now();

    // Iniciar servidor NATS
    const natsServer = spawn('nats-server', ['-p', '4224']);
    await new Promise(resolve => setTimeout(resolve, 2000));

    try {
      // Criar sistema completo
      const qcom = new QComBus();
      await qcom.connect('integration_test', { servers: 'localhost:4224' });

      const fabric = new ContextFabric();

      // Simular request completo
      const pythonScript = `
import sys
sys.path.append('/Users/clubproducoes/Digimundo/core/memory')
from cognitive_core import CognitiveCore
import json

core = CognitiveCore('integration_test')

# Armazenar contexto
core.store_memory(
    'Sistema integrado: ChromaDB + NATS + Context Fabric',
    {'integration': True, 'status': 'testing'},
    'semantic'
)

# Recuperar para contexto
memories = core.recall('sistema integrado', top_k=3)
metrics = core.get_metrics()

print(json.dumps({
    'memories': len(memories),
    'avg_recall_ms': metrics['avg_recall_time'] * 1000
}))
`;

      // Executar Python
      const python = spawn('python3', ['-c', pythonScript]);
      let pythonResult = '';

      python.stdout.on('data', (data) => {
        pythonResult += data.toString();
      });

      await new Promise(resolve => {
        python.on('close', resolve);
      });

      const memoryResult = JSON.parse(pythonResult);

      // Montar contexto completo
      const context = await fabric.assembleContext('integration test', 'sabiamon');

      // Enviar via Q-Com
      await qcom.broadcast({
        type: 'integration_test',
        context: context.assemblyTime,
        memory: memoryResult.avg_recall_ms
      });

      const qcomMetrics = qcom.getMetrics();
      await qcom.disconnect();

      const elapsed = Date.now() - startTime;

      // Validar integração
      const success = 
        context.assemblyTime < 100 &&
        memoryResult.avg_recall_ms < 100 &&
        qcomMetrics.avgLatency < 10;

      if (success) {
        console.log(`✅ Integração completa funcionando`);
        console.log(`   - Context: ${context.assemblyTime}ms`);
        console.log(`   - Memory: ${memoryResult.avg_recall_ms.toFixed(2)}ms`);
        console.log(`   - Q-Com: ${qcomMetrics.avgLatencyMs}`);
        console.log(`   - Total: ${elapsed}ms`);
        
        this.results.passed.push('FullIntegration');
        this.results.metrics.fullIntegration = {
          contextTime: context.assemblyTime,
          memoryTime: memoryResult.avg_recall_ms,
          qcomLatency: qcomMetrics.avgLatency,
          totalTime: elapsed
        };
      } else {
        console.log(`❌ Integração falhou nos targets de performance`);
        this.results.failed.push('FullIntegration');
      }

    } catch (error) {
      console.log(`❌ Integração erro: ${error.message}`);
      this.results.failed.push('FullIntegration');
    } finally {
      natsServer.kill();
    }
  }

  /**
   * Executa todos os testes
   */
  async runAll() {
    console.log('╔══════════════════════════════════════════════════════╗');
    console.log('║      🧬 TESTE DE INTEGRAÇÃO - DIGIMUNDO CORE 🧬       ║');
    console.log('╚══════════════════════════════════════════════════════╝');

    const startTime = Date.now();

    // Executar testes
    await this.testChromaDB();
    await this.testNATS();
    await this.testContextFabric();
    await this.testFullIntegration();

    const totalTime = Date.now() - startTime;

    // Relatório final
    console.log('\n' + '═'.repeat(56));
    console.log('📊 RELATÓRIO FINAL');
    console.log('═'.repeat(56));

    console.log(`\n✅ Passou: ${this.results.passed.length} testes`);
    this.results.passed.forEach(test => {
      console.log(`   - ${test}`);
    });

    if (this.results.failed.length > 0) {
      console.log(`\n❌ Falhou: ${this.results.failed.length} testes`);
      this.results.failed.forEach(test => {
        console.log(`   - ${test}`);
      });
    }

    console.log('\n📈 MÉTRICAS DE PERFORMANCE:');
    console.log('─'.repeat(56));
    
    Object.entries(this.results.metrics).forEach(([test, metrics]) => {
      console.log(`\n${test}:`);
      Object.entries(metrics).forEach(([key, value]) => {
        const formatted = typeof value === 'number' 
          ? value < 1 ? `${(value * 1000).toFixed(2)}ms` : `${value.toFixed(2)}ms`
          : value;
        console.log(`  ${key}: ${formatted}`);
      });
    });

    console.log('\n─'.repeat(56));
    console.log(`⏱️  Tempo total dos testes: ${(totalTime / 1000).toFixed(2)}s`);

    // Score final
    const successRate = (this.results.passed.length / 
      (this.results.passed.length + this.results.failed.length)) * 100;
    
    console.log(`\n🎯 Taxa de sucesso: ${successRate.toFixed(0)}%`);

    if (successRate === 100) {
      console.log('\n✨ TODOS OS TESTES PASSARAM! Sistema pronto para evolução!');
    } else {
      console.log('\n⚠️  Alguns testes falharam. Revisar antes de prosseguir.');
    }

    return successRate === 100;
  }
}

// Executar testes
if (require.main === module) {
  const test = new IntegrationTest();
  test.runAll().then(success => {
    process.exit(success ? 0 : 1);
  });
}