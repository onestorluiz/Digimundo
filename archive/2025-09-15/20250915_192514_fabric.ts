/**
 * ⚡ CONTEXT FABRIC - Montagem de Contexto <100ms
 * Sistema ultra-rápido para montar contexto completo para cada request
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import * as os from 'os';
import * as fs from 'fs/promises';
import * as path from 'path';

const execAsync = promisify(exec);

interface SystemContext {
  cpu: {
    usage: number;
    cores: number;
    model: string;
  };
  memory: {
    total: number;
    free: number;
    used: number;
    percentage: number;
  };
  disk: {
    free: number;
    total: number;
    percentage: number;
  };
  timestamp: number;
}

interface PeerContext {
  digimon: string;
  lastMessage: string;
  timestamp: number;
  status: 'online' | 'offline' | 'busy';
}

interface MemoryContext {
  content: string;
  relevance: number;
  type: string;
}

interface ToolContext {
  tool: string;
  result: any;
  timestamp: number;
}

interface CompleteContext {
  system: SystemContext;
  peers: PeerContext[];
  memories: MemoryContext[];
  tools: ToolContext[];
  assemblyTime: number;
}

export class ContextFabric {
  private systemCache: { data: SystemContext | null; timestamp: number } = {
    data: null,
    timestamp: 0
  };
  private systemCacheTTL = 5000; // 5 segundos

  private peerCache = new Map<string, PeerContext>();
  private memoryCache = new Map<string, MemoryContext[]>();
  private toolCache: ToolContext[] = [];
  private maxToolCache = 10;

  constructor() {
    // Pre-aquecer cache do sistema
    this.updateSystemContext();
  }

  /**
   * Monta contexto completo em <100ms
   */
  async assembleContext(
    query: string,
    digimonId: string,
    options: {
      includeSystem?: boolean;
      includePeers?: boolean;
      includeMemories?: boolean;
      includeTools?: boolean;
      memoryClient?: any;
      qcomBus?: any;
    } = {}
  ): Promise<CompleteContext> {
    const startTime = Date.now();

    // Configurações padrão
    const config = {
      includeSystem: true,
      includePeers: true,
      includeMemories: true,
      includeTools: true,
      ...options
    };

    // Executar todas as buscas em paralelo
    const [system, peers, memories, tools] = await Promise.all([
      config.includeSystem ? this.getSystemContext() : null,
      config.includePeers ? this.getPeerContext(config.qcomBus) : [],
      config.includeMemories ? this.getMemoryContext(query, config.memoryClient) : [],
      config.includeTools ? this.getToolContext() : []
    ]);

    const assemblyTime = Date.now() - startTime;

    return {
      system: system!,
      peers,
      memories,
      tools,
      assemblyTime
    };
  }

  /**
   * Obtém contexto do sistema (cacheado)
   */
  private async getSystemContext(): Promise<SystemContext> {
    // Verificar cache
    if (
      this.systemCache.data &&
      Date.now() - this.systemCache.timestamp < this.systemCacheTTL
    ) {
      return this.systemCache.data;
    }

    // Atualizar cache
    return this.updateSystemContext();
  }

  /**
   * Atualiza cache do sistema
   */
  private async updateSystemContext(): Promise<SystemContext> {
    const cpuInfo = os.cpus();
    const totalMem = os.totalmem();
    const freeMem = os.freemem();

    // Obter uso de CPU (macOS específico)
    let cpuUsage = 0;
    try {
      const { stdout } = await execAsync(
        "ps -A -o %cpu | awk '{s+=$1} END {print s}'"
      );
      cpuUsage = parseFloat(stdout) / cpuInfo.length;
    } catch {
      cpuUsage = 0;
    }

    // Obter espaço em disco
    let diskFree = 0;
    let diskTotal = 0;
    try {
      const { stdout } = await execAsync(
        "df -k / | tail -1 | awk '{print $4, $2}'"
      );
      const [free, total] = stdout.trim().split(' ').map(Number);
      diskFree = free * 1024; // Converter de KB para bytes
      diskTotal = total * 1024;
    } catch {
      diskFree = 0;
      diskTotal = 0;
    }

    const context: SystemContext = {
      cpu: {
        usage: cpuUsage,
        cores: cpuInfo.length,
        model: cpuInfo[0]?.model || 'Unknown'
      },
      memory: {
        total: totalMem,
        free: freeMem,
        used: totalMem - freeMem,
        percentage: ((totalMem - freeMem) / totalMem) * 100
      },
      disk: {
        free: diskFree,
        total: diskTotal,
        percentage: diskTotal > 0 ? ((diskTotal - diskFree) / diskTotal) * 100 : 0
      },
      timestamp: Date.now()
    };

    // Atualizar cache
    this.systemCache = {
      data: context,
      timestamp: Date.now()
    };

    return context;
  }

  /**
   * Obtém contexto dos peers
   */
  private async getPeerContext(qcomBus?: any): Promise<PeerContext[]> {
    if (!qcomBus) return Array.from(this.peerCache.values());

    // Aqui poderia fazer uma query rápida aos peers online
    // Por enquanto, retorna o cache
    return Array.from(this.peerCache.values())
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, 5); // Top 5 peers mais recentes
  }

  /**
   * Obtém contexto de memória relevante
   */
  private async getMemoryContext(
    query: string,
    memoryClient?: any
  ): Promise<MemoryContext[]> {
    // Verificar cache
    const cached = this.memoryCache.get(query);
    if (cached) return cached;

    if (!memoryClient) return [];

    try {
      // Buscar memórias relevantes
      const memories = await memoryClient.recall(query, 5, 0.6);
      
      const context = memories.map((mem: any) => ({
        content: mem.content.substring(0, 200), // Limitar tamanho
        relevance: mem.similarity || 0,
        type: mem.metadata?.type || 'unknown'
      }));

      // Cachear por 1 minuto
      this.memoryCache.set(query, context);
      setTimeout(() => this.memoryCache.delete(query), 60000);

      return context;
    } catch {
      return [];
    }
  }

  /**
   * Obtém contexto de ferramentas recentes
   */
  private getToolContext(): ToolContext[] {
    return this.toolCache.slice(-5); // Últimas 5 ferramentas usadas
  }

  /**
   * Atualiza contexto de peer
   */
  updatePeerContext(peer: PeerContext): void {
    this.peerCache.set(peer.digimon, peer);
  }

  /**
   * Adiciona resultado de ferramenta ao contexto
   */
  addToolResult(tool: string, result: any): void {
    this.toolCache.push({
      tool,
      result,
      timestamp: Date.now()
    });

    // Manter apenas os últimos N resultados
    if (this.toolCache.length > this.maxToolCache) {
      this.toolCache.shift();
    }
  }

  /**
   * Formata contexto para prompt
   */
  formatForPrompt(context: CompleteContext): string {
    const lines: string[] = [];

    // Sistema
    if (context.system) {
      lines.push('SYSTEM:');
      lines.push(`- CPU: ${context.system.cpu.usage.toFixed(1)}% (${context.system.cpu.cores} cores)`);
      lines.push(`- RAM: ${(context.system.memory.used / 1e9).toFixed(1)}GB/${(context.system.memory.total / 1e9).toFixed(1)}GB`);
      lines.push(`- Disk: ${(context.system.disk.free / 1e9).toFixed(1)}GB free`);
    }

    // Peers
    if (context.peers.length > 0) {
      lines.push('\nPEERS:');
      context.peers.forEach(peer => {
        lines.push(`- ${peer.digimon}: ${peer.status} "${peer.lastMessage}"`);
      });
    }

    // Memórias
    if (context.memories.length > 0) {
      lines.push('\nMEMORY:');
      context.memories.forEach(mem => {
        lines.push(`- [${mem.type}] ${mem.content} (${(mem.relevance * 100).toFixed(0)}%)`);
      });
    }

    // Ferramentas
    if (context.tools.length > 0) {
      lines.push('\nTOOLS:');
      context.tools.forEach(tool => {
        const result = typeof tool.result === 'string' 
          ? tool.result 
          : JSON.stringify(tool.result).substring(0, 100);
        lines.push(`- ${tool.tool}: ${result}`);
      });
    }

    lines.push(`\n[Context assembled in ${context.assemblyTime}ms]`);

    return lines.join('\n');
  }

  /**
   * Obtém métricas de performance
   */
  getMetrics(): {
    cacheHits: number;
    avgAssemblyTime: number;
    memoryCacheSize: number;
    peerCacheSize: number;
  } {
    // Aqui seria calculado com base no histórico real
    return {
      cacheHits: this.systemCache.data ? 1 : 0,
      avgAssemblyTime: 50, // Estimativa
      memoryCacheSize: this.memoryCache.size,
      peerCacheSize: this.peerCache.size
    };
  }
}

// Teste do Context Fabric
if (require.main === module) {
  (async () => {
    console.log('⚡ TESTANDO CONTEXT FABRIC');
    console.log('=====================================\n');

    const fabric = new ContextFabric();

    // Simular alguns peers
    fabric.updatePeerContext({
      digimon: 'trainmon',
      lastMessage: 'Treinando modelo de evolução',
      timestamp: Date.now(),
      status: 'busy'
    });

    fabric.updatePeerContext({
      digimon: 'debugmon',
      lastMessage: 'Analisando logs do sistema',
      timestamp: Date.now() - 1000,
      status: 'online'
    });

    // Simular resultados de ferramentas
    fabric.addToolResult('memory_recall', { found: 3, time: '45ms' });
    fabric.addToolResult('disk_check', { free: '103.9GB', status: 'healthy' });

    // Teste 1: Contexto completo
    console.log('📊 Teste 1: Contexto completo');
    const startTime = Date.now();
    
    const context = await fabric.assembleContext('evolução do Digimundo', 'sabiamon');
    
    console.log(`⏱️  Tempo de montagem: ${context.assemblyTime}ms`);
    console.log(`✅ Target: <100ms - ${context.assemblyTime < 100 ? 'PASSED' : 'FAILED'}\n`);

    // Mostrar contexto formatado
    console.log('📝 Contexto formatado:');
    console.log('─'.repeat(50));
    console.log(fabric.formatForPrompt(context));
    console.log('─'.repeat(50));

    // Teste 2: Múltiplas montagens (para testar cache)
    console.log('\n🔄 Teste 2: Performance com cache');
    const times: number[] = [];
    
    for (let i = 0; i < 10; i++) {
      const start = Date.now();
      await fabric.assembleContext('teste de cache', 'sabiamon');
      const elapsed = Date.now() - start;
      times.push(elapsed);
    }

    const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
    console.log(`⏱️  Tempo médio (10 requests): ${avgTime.toFixed(2)}ms`);
    console.log(`📊 Min: ${Math.min(...times)}ms, Max: ${Math.max(...times)}ms`);
    console.log(`✅ Todos <100ms: ${times.every(t => t < 100) ? 'YES' : 'NO'}`);

    // Teste 3: Contexto parcial
    console.log('\n⚡ Teste 3: Contexto parcial (só sistema)');
    const partialContext = await fabric.assembleContext('teste', 'sabiamon', {
      includeSystem: true,
      includePeers: false,
      includeMemories: false,
      includeTools: false
    });
    
    console.log(`⏱️  Tempo: ${partialContext.assemblyTime}ms`);
    console.log(`📦 Tamanho: ${JSON.stringify(partialContext).length} bytes`);

    // Métricas finais
    console.log('\n📈 MÉTRICAS FINAIS');
    const metrics = fabric.getMetrics();
    console.log(metrics);

    console.log('\n✨ Context Fabric operacional!');
  })();
}