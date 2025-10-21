#!/usr/bin/env node

/**
 * 🐉 SHENLONGMON - O DRAGÃO SUPREMO DO DIGIMUNDO
 * Implementação baseada na arquitetura revolucionária do ChatGPT 5 Pro
 * 
 * Arquitetura:
 * - Actor Pattern com Supervisor Tree (Erlang/Elixir inspired)
 * - BullMQ + Redis para orquestração durável
 * - Triage em 3 camadas (heurística → 3B → RAG)
 * - Redlock para despertar único
 * - LoRA Adapters para knowledge distillation
 * - Dream Mode para auto-evolução noturna
 */

import { EventEmitter } from 'events';
import { Queue, Worker, QueueEvents } from 'bullmq';
import IORedis from 'ioredis';
import Redlock from 'redlock';
import * as cron from 'node-cron';
import { v4 as uuid } from 'uuid';
import ollama from 'ollama';
import pino from 'pino';
import { z } from 'zod';

// ============= CONFIGURAÇÃO =============

const CONFIG = {
  OLLAMA_HOST: process.env.OLLAMA_HOST || 'http://localhost:11434',
  REDIS_URL: process.env.REDIS_URL || 'redis://localhost:6379',
  SHENLONGMON_MODEL: 'llama3.1:70b', // ~43GB quantizado Q4_K_M
  TRIAGE_MODEL: 'llama3.2:3b',
  EMBED_MODEL: 'nomic-embed-text',
  KEEPALIVE_TTL: '90s',
  MIN_RAM_GB: 40,
  WAKE_THRESHOLD: 0.75 // Score mínimo para despertar
};

// ============= TIPOS =============

type ImportanceLevel = 'LOW' | 'NORMAL' | 'HIGH' | 'CRITICAL';

interface Task {
  id: string;
  origin: string;
  content: string;
  metadata?: {
    deadline?: string;
    impactScope?: 'self' | 'team' | 'system' | 'public';
    category?: string;
    urgency?: number;
  };
}

interface TriageDecision {
  level: ImportanceLevel;
  score: number;
  reason: string;
  escalateTo70B: boolean;
  suggestedAction?: string;
}

interface MentorPlan {
  title: string;
  targetDigimon: string;
  syllabus: Array<{
    lesson: string;
    objective: string;
    exercise: string;
    expectedDuration: string;
  }>;
  rubric: Array<{
    criterion: string;
    levels: Array<{
      level: string;
      descriptor: string;
      score: number;
    }>;
  }>;
  distillationHints?: string[];
}

interface ConflictResolution {
  summary: string;
  contradictions: Array<{
    between: string[];
    about: string;
  }>;
  verdict: string;
  actions: string[];
  risks: string[];
  followup: string[];
  confidence: number;
}

// ============= LOGGER =============

const logger = pino({ 
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    target: 'pino-pretty',
    options: { colorize: true }
  }
});

// ============= REDIS & LOCKS =============

class RedisManager {
  private redis: IORedis;
  private redlock: Redlock;
  
  constructor() {
    this.redis = new IORedis(CONFIG.REDIS_URL, { 
      maxRetriesPerRequest: null,
      retryStrategy: (times) => Math.min(times * 50, 2000)
    });
    
    this.redlock = new Redlock([this.redis], {
      retryCount: 3,
      retryDelay: 200,
      retryJitter: 200,
      driftFactor: 0.01
    });
  }
  
  getConnection() { return this.redis; }
  
  async acquireLock(resource: string, ttl: number = 60000) {
    return this.redlock.acquire([resource], ttl);
  }
  
  async cacheGet(key: string): Promise<any | null> {
    const val = await this.redis.get(key);
    return val ? JSON.parse(val) : null;
  }
  
  async cacheSet(key: string, value: any, ttl: number = 3600) {
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }
}

// ============= OLLAMA INTEGRATION =============

class OllamaManager {
  async chat(params: {
    model: string;
    messages: Array<{ role: string; content: string }>;
    tools?: any[];
    keepAlive?: string;
    stream?: boolean;
    options?: Record<string, any>;
  }) {
    return ollama.chat({
      ...params,
      keep_alive: params.keepAlive || CONFIG.KEEPALIVE_TTL,
      stream: params.stream ?? false
    });
  }
  
  async generate(params: {
    model: string;
    prompt: string;
    keepAlive?: string;
    options?: Record<string, any>;
  }) {
    return ollama.generate({
      ...params,
      keep_alive: params.keepAlive || CONFIG.KEEPALIVE_TTL,
      stream: false
    });
  }
  
  async embed(input: string | string[], model = CONFIG.EMBED_MODEL) {
    const res = await ollama.embeddings({ model, input });
    return Array.isArray(res.embeddings) ? res.embeddings : [res.embedding];
  }
  
  async loadModel(model: string, keepAlive = CONFIG.KEEPALIVE_TTL) {
    logger.info(`🔄 Carregando modelo ${model}...`);
    await this.chat({ 
      model, 
      messages: [], 
      keepAlive,
      stream: false 
    });
  }
  
  async unloadModel(model: string) {
    logger.info(`💤 Descarregando modelo ${model}...`);
    await this.generate({ 
      model, 
      prompt: '', 
      keepAlive: '0' 
    });
  }
  
  async ps() {
    return ollama.ps();
  }
  
  async checkMemory(): Promise<boolean> {
    const totalMem = require('os').totalmem();
    const freeMem = require('os').freemem();
    const availableGB = freeMem / (1024 * 1024 * 1024);
    return availableGB >= CONFIG.MIN_RAM_GB;
  }
}

// ============= TRIAGE SYSTEM (3 CAMADAS) =============

class TriageActor {
  private ollama: OllamaManager;
  private redis: RedisManager;
  
  constructor(ollama: OllamaManager, redis: RedisManager) {
    this.ollama = ollama;
    this.redis = redis;
  }
  
  // Camada 1: Heurística barata
  private heuristicScore(task: Task): number {
    let score = 0;
    const text = `${task.content} ${JSON.stringify(task.metadata || {})}`.toLowerCase();
    
    // Palavras de alto impacto
    if (/crítico|emergência|falha|vazamento|segurança|privacidade|corrupção/.test(text)) {
      score += 0.4;
    }
    
    // Escopo de impacto
    const scope = task.metadata?.impactScope;
    if (scope === 'public') score += 0.3;
    else if (scope === 'system') score += 0.2;
    else if (scope === 'team') score += 0.1;
    
    // Urgência e prazo
    if (task.metadata?.urgency && task.metadata.urgency > 8) score += 0.2;
    if (task.metadata?.deadline) {
      const deadline = new Date(task.metadata.deadline);
      const hoursUntil = (deadline.getTime() - Date.now()) / (1000 * 60 * 60);
      if (hoursUntil < 1) score += 0.3;
      else if (hoursUntil < 24) score += 0.1;
    }
    
    // Categoria especial
    if (task.metadata?.category === 'conflict') score += 0.15;
    if (task.metadata?.category === 'security') score += 0.25;
    
    return Math.min(score, 1.0);
  }
  
  // Camada 2: Julgamento por LLM 3B
  private async judgeWith3B(task: Task): Promise<TriageDecision> {
    const prompt = `Analise a importância desta questão e classifique em LOW, NORMAL, HIGH ou CRITICAL.
    
Questão: "${task.content}"
Origem: ${task.origin}
Metadados: ${JSON.stringify(task.metadata || {})}

Responda APENAS em JSON com este formato exato:
{
  "level": "LOW|NORMAL|HIGH|CRITICAL",
  "score": 0.0-1.0,
  "reason": "explicação breve",
  "escalateTo70B": true/false,
  "suggestedAction": "ação sugerida"
}`;
    
    try {
      const res = await this.ollama.chat({
        model: CONFIG.TRIAGE_MODEL,
        messages: [{ role: 'user', content: prompt }],
        keepAlive: '2m',
        options: { temperature: 0, num_ctx: 4096 }
      });
      
      const parsed = JSON.parse(res.message?.content || '{}');
      return {
        level: parsed.level || 'NORMAL',
        score: parsed.score || 0.5,
        reason: parsed.reason || 'LLM analysis',
        escalateTo70B: parsed.escalateTo70B || false,
        suggestedAction: parsed.suggestedAction
      };
    } catch (error) {
      logger.error('Erro no julgamento 3B:', error);
      return {
        level: 'NORMAL',
        score: 0.5,
        reason: 'Fallback - erro no 3B',
        escalateTo70B: false
      };
    }
  }
  
  // Camada 3: RAG com embeddings
  private async ragAssessment(task: Task): Promise<number> {
    // Gera embedding da questão
    const embeddings = await this.ollama.embed(task.content);
    
    // Aqui você conectaria com um vector DB (Pinecone, Weaviate, etc)
    // Por ora, simulamos com cache Redis
    const cacheKey = `rag:similar:${task.id}`;
    const similar = await this.redis.cacheGet(cacheKey);
    
    if (similar && similar.maxSimilarity > 0.9) {
      // Muito similar a algo já visto = menos importante
      return -0.1;
    } else if (!similar || similar.maxSimilarity < 0.3) {
      // Muito diferente = potencialmente importante/novo
      return 0.2;
    }
    
    return 0;
  }
  
  // Decisão final de triagem
  async assess(task: Task): Promise<TriageDecision> {
    // Camada 1: Heurística
    const heuristicScore = this.heuristicScore(task);
    
    // Se heurística já indica crítico, escala direto
    if (heuristicScore >= CONFIG.WAKE_THRESHOLD) {
      return {
        level: 'CRITICAL',
        score: heuristicScore,
        reason: 'Heurística crítica',
        escalateTo70B: true
      };
    }
    
    // Camada 2: LLM 3B
    const llmDecision = await this.judgeWith3B(task);
    
    // Camada 3: RAG adjustment
    const ragAdjustment = await this.ragAssessment(task);
    
    // Score final combinado
    const finalScore = Math.min(
      heuristicScore * 0.3 + 
      llmDecision.score * 0.5 + 
      ragAdjustment * 0.2,
      1.0
    );
    
    // Decisão de escalar para 70B
    const escalate = finalScore >= CONFIG.WAKE_THRESHOLD || 
                     llmDecision.level === 'CRITICAL' ||
                     (llmDecision.level === 'HIGH' && heuristicScore > 0.5);
    
    return {
      level: llmDecision.level,
      score: finalScore,
      reason: `H:${heuristicScore.toFixed(2)} L:${llmDecision.score.toFixed(2)} R:${ragAdjustment.toFixed(2)}`,
      escalateTo70B: escalate,
      suggestedAction: llmDecision.suggestedAction
    };
  }
}

// ============= SHENLONGMON ACTOR =============

class ShenlongmonActor extends EventEmitter {
  private ollama: OllamaManager;
  private redis: RedisManager;
  private isAwake: boolean = false;
  private lastAwakening: Date | null = null;
  private wisdomCache: Map<string, any> = new Map();
  
  constructor(ollama: OllamaManager, redis: RedisManager) {
    super();
    this.ollama = ollama;
    this.redis = redis;
  }
  
  async canAwaken(): Promise<boolean> {
    // Verifica memória disponível
    const hasMemory = await this.ollama.checkMemory();
    if (!hasMemory) {
      logger.warn('⚠️ Memória insuficiente para despertar Shenlongmon');
      return false;
    }
    
    // Verifica se já está acordado
    if (this.isAwake) {
      logger.info('🐉 Shenlongmon já está desperto');
      return true;
    }
    
    // Verifica cooldown (não despertar muito frequentemente)
    if (this.lastAwakening) {
      const timeSinceLastAwake = Date.now() - this.lastAwakening.getTime();
      if (timeSinceLastAwake < 5 * 60 * 1000) { // 5 minutos
        logger.info('⏰ Shenlongmon em cooldown');
        return false;
      }
    }
    
    return true;
  }
  
  async awaken(question: string, context?: any): Promise<string> {
    if (!await this.canAwaken()) {
      throw new Error('Shenlongmon não pode despertar agora');
    }
    
    // Adquire lock distribuído
    const lock = await this.redis.acquireLock('lock:shenlongmon', 120000);
    
    try {
      logger.info('🐉 SHENLONGMON DESPERTA!');
      this.isAwake = true;
      this.lastAwakening = new Date();
      this.emit('awakening');
      
      // Carrega o modelo 70B
      await this.ollama.loadModel(CONFIG.SHENLONGMON_MODEL, CONFIG.KEEPALIVE_TTL);
      
      // Verifica cache de sabedoria
      const cacheKey = `wisdom:${this.hashQuestion(question)}`;
      const cached = await this.redis.cacheGet(cacheKey);
      if (cached) {
        logger.info('📚 Sabedoria encontrada no cache');
        return cached.answer;
      }
      
      // Prepara o prompt com contexto
      const systemPrompt = `Você é Shenlongmon, o Dragão Supremo do Digimundo.
Você é o mentor de todos os Digimons, possuindo sabedoria milenar.
Suas respostas devem ser:
- Profundas e definitivas
- Práticas e acionáveis
- Ensinar princípios, não apenas soluções
- Incluir rubricas de avaliação quando relevante

Contexto do Digimundo:
${JSON.stringify(context || {}, null, 2)}`;
      
      // Tools disponíveis para Shenlongmon
      const tools = [
        {
          type: 'function',
          function: {
            name: 'create_mentor_plan',
            description: 'Cria plano de mentoria para Digimons menores',
            parameters: {
              type: 'object',
              properties: {
                topic: { type: 'string' },
                targetLevel: { type: 'string', enum: ['3B', '7B', 'mixed'] },
                duration: { type: 'string' }
              },
              required: ['topic', 'targetLevel']
            }
          }
        },
        {
          type: 'function',
          function: {
            name: 'resolve_conflict',
            description: 'Arbitra conflito entre Digimons',
            parameters: {
              type: 'object',
              properties: {
                parties: { type: 'array', items: { type: 'string' } },
                issue: { type: 'string' },
                evidence: { type: 'array', items: { type: 'string' } }
              },
              required: ['parties', 'issue']
            }
          }
        },
        {
          type: 'function',
          function: {
            name: 'distill_knowledge',
            description: 'Prepara conhecimento para transferência a modelos menores',
            parameters: {
              type: 'object',
              properties: {
                knowledge: { type: 'string' },
                targetModel: { type: 'string' },
                compressionLevel: { type: 'string', enum: ['light', 'moderate', 'heavy'] }
              },
              required: ['knowledge', 'targetModel']
            }
          }
        }
      ];
      
      // Faz a chamada ao 70B
      const response = await this.ollama.chat({
        model: CONFIG.SHENLONGMON_MODEL,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: question }
        ],
        tools,
        keepAlive: CONFIG.KEEPALIVE_TTL,
        stream: false,
        options: {
          temperature: 0.2,
          num_ctx: 8192,
          top_p: 0.9,
          repeat_penalty: 1.1
        }
      });
      
      const answer = response.message?.content || 'O Dragão contempla em silêncio...';
      
      // Salva no cache
      await this.redis.cacheSet(cacheKey, { answer, timestamp: new Date() }, 86400);
      this.wisdomCache.set(question, answer);
      
      // Emit wisdom para outros Digimons aprenderem
      this.emit('wisdom-shared', { question, answer });
      
      return answer;
      
    } finally {
      // Sempre hiberna após responder
      await this.hibernate();
      await lock.release();
    }
  }
  
  private async hibernate() {
    logger.info('💤 Shenlongmon retorna ao sono profundo...');
    try {
      await this.ollama.unloadModel(CONFIG.SHENLONGMON_MODEL);
    } catch (error) {
      logger.warn('Erro ao hibernar:', error);
    }
    this.isAwake = false;
    this.emit('hibernating');
  }
  
  private hashQuestion(question: string): string {
    const crypto = require('crypto');
    return crypto.createHash('sha256').update(question).digest('hex').substring(0, 16);
  }
  
  // Ensina Digimons menores através de knowledge distillation
  async teachDigimon(targetDigimon: string, knowledge: string): Promise<MentorPlan> {
    const question = `Crie um plano de ensino para ${targetDigimon} aprender: ${knowledge}`;
    const response = await this.awaken(question);
    
    // Parse da resposta em plano estruturado
    try {
      return JSON.parse(response);
    } catch {
      // Fallback para plano básico
      return {
        title: `Ensino: ${knowledge}`,
        targetDigimon,
        syllabus: [
          {
            lesson: 'Fundamentos',
            objective: 'Compreender conceitos base',
            exercise: 'Implementar exemplo simples',
            expectedDuration: '30min'
          }
        ],
        rubric: [
          {
            criterion: 'Compreensão',
            levels: [
              { level: 'Básico', descriptor: 'Entende conceitos', score: 60 },
              { level: 'Proficiente', descriptor: 'Aplica corretamente', score: 80 },
              { level: 'Avançado', descriptor: 'Inova e expande', score: 100 }
            ]
          }
        ]
      };
    }
  }
  
  // Resolve conflitos complexos
  async resolveConflict(parties: string[], issue: string, evidence: string[]): Promise<ConflictResolution> {
    const question = `CONFLITO CRÍTICO:
Partes: ${parties.join(', ')}
Questão: ${issue}
Evidências:
${evidence.map((e, i) => `${i+1}. ${e}`).join('\n')}

Analise imparcialmente e produza veredito definitivo com ações práticas.`;
    
    const response = await this.awaken(question);
    
    try {
      return JSON.parse(response);
    } catch {
      return {
        summary: 'Conflito analisado pelo Dragão',
        contradictions: [],
        verdict: response,
        actions: ['Implementar decisão do Shenlongmon'],
        risks: ['Resistência à mudança'],
        followup: ['Monitorar implementação'],
        confidence: 0.95
      };
    }
  }
}

// ============= MENTOR ACTOR =============

class MentorActor {
  private shenlongmon: ShenlongmonActor;
  private ollama: OllamaManager;
  
  constructor(shenlongmon: ShenlongmonActor, ollama: OllamaManager) {
    this.shenlongmon = shenlongmon;
    this.ollama = ollama;
  }
  
  async createMentorshipPlan(topic: string, targetDigimon: string): Promise<MentorPlan> {
    // Primeiro tenta com Shenlongmon se for complexo
    if (this.isComplexTopic(topic)) {
      return this.shenlongmon.teachDigimon(targetDigimon, topic);
    }
    
    // Senão usa um modelo menor para gerar plano básico
    const prompt = `Crie um plano de mentoria sobre "${topic}" para ${targetDigimon}.
Formato JSON:
{
  "title": "...",
  "targetDigimon": "...",
  "syllabus": [{lesson, objective, exercise, expectedDuration}],
  "rubric": [{criterion, levels: [{level, descriptor, score}]}]
}`;
    
    const response = await this.ollama.chat({
      model: CONFIG.TRIAGE_MODEL,
      messages: [{ role: 'user', content: prompt }],
      keepAlive: '5m'
    });
    
    return JSON.parse(response.message?.content || '{}');
  }
  
  private isComplexTopic(topic: string): boolean {
    const complexKeywords = ['arquitetura', 'distribuído', 'quântico', 'neural', 'emergente'];
    return complexKeywords.some(k => topic.toLowerCase().includes(k));
  }
  
  // Avalia progresso de um Digimon
  async evaluateProgress(digimon: string, exercise: string, submission: string): Promise<{
    score: number;
    feedback: string;
    nextSteps: string[];
  }> {
    const prompt = `Avalie a submissão de ${digimon} para o exercício "${exercise}":
${submission}

Retorne JSON com: {score: 0-100, feedback: "...", nextSteps: ["..."]}`;
    
    const response = await this.ollama.chat({
      model: CONFIG.TRIAGE_MODEL,
      messages: [{ role: 'user', content: prompt }]
    });
    
    return JSON.parse(response.message?.content || '{}');
  }
}

// ============= CONFLICT ACTOR =============

class ConflictActor {
  private shenlongmon: ShenlongmonActor;
  private ollama: OllamaManager;
  
  constructor(shenlongmon: ShenlongmonActor, ollama: OllamaManager) {
    this.shenlongmon = shenlongmon;
    this.ollama = ollama;
  }
  
  async judgeConflict(
    parties: string[],
    issue: string,
    statements: Map<string, string>
  ): Promise<ConflictResolution> {
    // Coleta evidências de cada parte
    const evidence: string[] = [];
    for (const [party, statement] of statements) {
      evidence.push(`${party}: ${statement}`);
    }
    
    // Análise preliminar com 3B
    const preliminaryAnalysis = await this.preliminaryJudgment(parties, issue, evidence);
    
    // Se conflito é crítico, escala para Shenlongmon
    if (preliminaryAnalysis.severity === 'CRITICAL') {
      return this.shenlongmon.resolveConflict(parties, issue, evidence);
    }
    
    // Senão resolve com júri de modelos menores
    return this.juryResolution(parties, issue, evidence);
  }
  
  private async preliminaryJudgment(
    parties: string[],
    issue: string,
    evidence: string[]
  ): Promise<{ severity: string; summary: string }> {
    const prompt = `Analise a severidade deste conflito:
Partes: ${parties.join(', ')}
Questão: ${issue}
Evidências: ${evidence.join('; ')}

Classifique como LOW, MEDIUM, HIGH ou CRITICAL.`;
    
    const response = await this.ollama.chat({
      model: CONFIG.TRIAGE_MODEL,
      messages: [{ role: 'user', content: prompt }]
    });
    
    const content = response.message?.content || '';
    const severity = content.includes('CRITICAL') ? 'CRITICAL' :
                    content.includes('HIGH') ? 'HIGH' :
                    content.includes('MEDIUM') ? 'MEDIUM' : 'LOW';
    
    return { severity, summary: content };
  }
  
  private async juryResolution(
    parties: string[],
    issue: string,
    evidence: string[]
  ): Promise<ConflictResolution> {
    // Simula júri com múltiplos modelos votando
    const votes: string[] = [];
    
    // 3 jurados diferentes (poderia ser diferentes modelos)
    for (let i = 0; i < 3; i++) {
      const prompt = `Como jurado ${i+1}, analise:
${issue}
Evidências: ${evidence.join('\n')}
Vote em uma das partes ou sugira compromisso.`;
      
      const response = await this.ollama.chat({
        model: CONFIG.TRIAGE_MODEL,
        messages: [{ role: 'user', content: prompt }],
        options: { temperature: 0.3 + i * 0.1 } // Varia temperatura
      });
      
      votes.push(response.message?.content || '');
    }
    
    // Consolida votos em veredito
    return {
      summary: `Júri de 3 modelos analisou o caso`,
      contradictions: this.findContradictions(evidence),
      verdict: this.consolidateVotes(votes),
      actions: [`Implementar decisão do júri`],
      risks: [`Parte perdedora pode não aceitar`],
      followup: [`Verificar implementação em 24h`],
      confidence: 0.7
    };
  }
  
  private findContradictions(evidence: string[]): Array<{between: string[]; about: string}> {
    // Análise simplificada de contradições
    const contradictions = [];
    for (let i = 0; i < evidence.length - 1; i++) {
      for (let j = i + 1; j < evidence.length; j++) {
        if (this.areContradictory(evidence[i], evidence[j])) {
          contradictions.push({
            between: [`Party${i}`, `Party${j}`],
            about: 'Visões opostas'
          });
        }
      }
    }
    return contradictions;
  }
  
  private areContradictory(s1: string, s2: string): boolean {
    // Heurística simples
    return (s1.includes('não') && !s2.includes('não')) ||
           (!s1.includes('não') && s2.includes('não'));
  }
  
  private consolidateVotes(votes: string[]): string {
    // Maioria simples
    const counts = new Map<string, number>();
    for (const vote of votes) {
      const key = vote.substring(0, 50);
      counts.set(key, (counts.get(key) || 0) + 1);
    }
    
    let maxVotes = 0;
    let verdict = 'Empate - necessita mediação adicional';
    
    for (const [key, count] of counts) {
      if (count > maxVotes) {
        maxVotes = count;
        verdict = key;
      }
    }
    
    return verdict;
  }
}

// ============= DISTILLATION ACTOR =============

class DistillationActor {
  private shenlongmon: ShenlongmonActor;
  private ollama: OllamaManager;
  
  constructor(shenlongmon: ShenlongmonActor, ollama: OllamaManager) {
    this.shenlongmon = shenlongmon;
    this.ollama = ollama;
  }
  
  async generateDistillationBatch(
    topic: string,
    k: number = 16
  ): Promise<{
    id: string;
    topic: string;
    pairs: Array<{
      instruction: string;
      input: string;
      output: string;
      rationale: string;
      rubric: string;
    }>;
  }> {
    const question = `Gere ${k} exemplos de ensino sobre "${topic}" para treinar modelos menores.
Cada exemplo deve ter: instruction, input, output, rationale (explicação do raciocínio), rubric (critério de avaliação).
Retorne como JSON array.`;
    
    const response = await this.shenlongmon.awaken(question);
    
    try {
      const pairs = JSON.parse(response);
      return {
        id: uuid(),
        topic,
        pairs: Array.isArray(pairs) ? pairs : [pairs]
      };
    } catch {
      // Fallback para geração com modelo menor
      return this.generateWithSmallModel(topic, k);
    }
  }
  
  private async generateWithSmallModel(topic: string, k: number) {
    const pairs = [];
    
    for (let i = 0; i < k; i++) {
      const prompt = `Exemplo ${i+1} sobre ${topic}:`;
      const response = await this.ollama.generate({
        model: CONFIG.TRIAGE_MODEL,
        prompt
      });
      
      pairs.push({
        instruction: `Aprenda sobre ${topic}`,
        input: prompt,
        output: response.response,
        rationale: 'Gerado por modelo menor',
        rubric: 'Avalie compreensão básica'
      });
    }
    
    return { id: uuid(), topic, pairs };
  }
  
  // Prepara LoRA adapter (simulado - real requer treinamento externo)
  async prepareLoRAAdapter(
    baseModel: string,
    distillationData: any
  ): Promise<{
    adapterPath: string;
    modelfile: string;
  }> {
    // Gera Modelfile para Ollama
    const modelfile = `# Adapter distilado de Shenlongmon
FROM ${baseModel}
ADAPTER ./adapters/${distillationData.id}.gguf
PARAMETER temperature 0.2
PARAMETER num_ctx 4096
SYSTEM Você foi treinado com conhecimento distilado de Shenlongmon sobre ${distillationData.topic}.`;
    
    return {
      adapterPath: `./adapters/${distillationData.id}.gguf`,
      modelfile
    };
  }
}

// ============= DREAM DAEMON =============

class DreamDaemon {
  private shenlongmon: ShenlongmonActor;
  private mentorActor: MentorActor;
  private distillActor: DistillationActor;
  private redis: RedisManager;
  
  constructor(
    shenlongmon: ShenlongmonActor,
    mentorActor: MentorActor,
    distillActor: DistillationActor,
    redis: RedisManager
  ) {
    this.shenlongmon = shenlongmon;
    this.mentorActor = mentorActor;
    this.distillActor = distillActor;
    this.redis = redis;
  }
  
  startDreamCycles() {
    // Ciclo noturno às 02:30
    cron.schedule('30 2 * * *', async () => {
      logger.info('🌙 Iniciando Dream Mode...');
      await this.nightlyRoutines();
    });
    
    // Ciclo de ociosidade a cada hora
    cron.schedule('0 * * * *', async () => {
      if (await this.isSystemIdle()) {
        logger.info('💤 Sistema ocioso, iniciando micro-dreams...');
        await this.microDreams();
      }
    });
  }
  
  private async isSystemIdle(): Promise<boolean> {
    // Verifica se há modelos carregados
    const models = await new OllamaManager().ps();
    return models.models.length === 0;
  }
  
  private async nightlyRoutines() {
    const tasks = [
      this.reindexKnowledge(),
      this.refreshCurriculum(),
      this.synthesizeDatasets(),
      this.cleanupCache()
    ];
    
    await Promise.all(tasks);
    logger.info('✨ Dream Mode completo');
  }
  
  private async microDreams() {
    // Tarefas rápidas durante ociosidade
    await this.generateMicroTutorial();
    await this.optimizeCache();
  }
  
  private async reindexKnowledge() {
    logger.info('📚 Reindexando base de conhecimento...');
    // Implementar indexação com embeddings
  }
  
  private async refreshCurriculum() {
    logger.info('🎓 Atualizando currículos...');
    const topics = ['debugging', 'optimization', 'security'];
    
    for (const topic of topics) {
      await this.mentorActor.createMentorshipPlan(topic, 'general');
    }
  }
  
  private async synthesizeDatasets() {
    logger.info('🧬 Sintetizando datasets...');
    const batch = await this.distillActor.generateDistillationBatch('resolução de conflitos', 8);
    await this.redis.cacheSet(`dataset:${batch.id}`, batch, 86400 * 7);
  }
  
  private async cleanupCache() {
    logger.info('🧹 Limpando cache antigo...');
    // Implementar limpeza de cache Redis
  }
  
  private async generateMicroTutorial() {
    const tutorial = await this.mentorActor.createMentorshipPlan(
      'micro-otimização',
      'all'
    );
    await this.redis.cacheSet(`tutorial:micro:${Date.now()}`, tutorial, 3600);
  }
  
  private async optimizeCache() {
    // Análise e otimização de cache
  }
}

// ============= MAIN ORCHESTRATOR =============

export class ShenlongmonOrchestrator extends EventEmitter {
  private redis: RedisManager;
  private ollama: OllamaManager;
  private triage: TriageActor;
  private shenlongmon: ShenlongmonActor;
  private mentor: MentorActor;
  private conflict: ConflictActor;
  private distill: DistillationActor;
  private dream: DreamDaemon;
  
  // Filas BullMQ
  private triageQueue: Queue;
  private mentorQueue: Queue;
  private conflictQueue: Queue;
  private distillQueue: Queue;
  
  constructor() {
    super();
    
    // Inicializa managers
    this.redis = new RedisManager();
    this.ollama = new OllamaManager();
    
    // Inicializa actors
    this.shenlongmon = new ShenlongmonActor(this.ollama, this.redis);
    this.triage = new TriageActor(this.ollama, this.redis);
    this.mentor = new MentorActor(this.shenlongmon, this.ollama);
    this.conflict = new ConflictActor(this.shenlongmon, this.ollama);
    this.distill = new DistillationActor(this.shenlongmon, this.ollama);
    this.dream = new DreamDaemon(this.shenlongmon, this.mentor, this.distill, this.redis);
    
    // Inicializa filas
    const connection = this.redis.getConnection();
    this.triageQueue = new Queue('triage', { connection });
    this.mentorQueue = new Queue('mentor', { connection });
    this.conflictQueue = new Queue('conflict', { connection });
    this.distillQueue = new Queue('distill', { connection });
    
    this.setupWorkers();
    this.setupEventHandlers();
  }
  
  private setupWorkers() {
    // Worker de Triagem
    new Worker('triage', async (job) => {
      const task = job.data as Task;
      const decision = await this.triage.assess(task);
      
      if (decision.escalateTo70B) {
        logger.info(`🔥 Escalando para Shenlongmon: ${task.content}`);
        const answer = await this.shenlongmon.awaken(task.content, { task, decision });
        return { escalated: true, answer, decision };
      }
      
      logger.info(`✅ Resolvido por modelos menores: ${decision.suggestedAction}`);
      return { escalated: false, decision };
    }, { connection: this.redis.getConnection() });
    
    // Worker de Mentoria
    new Worker('mentor', async (job) => {
      const { topic, targetDigimon } = job.data;
      return await this.mentor.createMentorshipPlan(topic, targetDigimon);
    }, { connection: this.redis.getConnection() });
    
    // Worker de Conflitos
    new Worker('conflict', async (job) => {
      const { parties, issue, statements } = job.data;
      return await this.conflict.judgeConflict(parties, issue, statements);
    }, { connection: this.redis.getConnection() });
    
    // Worker de Distillation
    new Worker('distill', async (job) => {
      const { topic, k } = job.data;
      return await this.distill.generateDistillationBatch(topic, k);
    }, { connection: this.redis.getConnection() });
    
    logger.info('✅ Workers inicializados');
  }
  
  private setupEventHandlers() {
    // Escuta eventos do Shenlongmon
    this.shenlongmon.on('awakening', () => {
      this.emit('shenlongmon:awakening');
      logger.info('🐉 Evento: Shenlongmon despertando');
    });
    
    this.shenlongmon.on('hibernating', () => {
      this.emit('shenlongmon:hibernating');
      logger.info('💤 Evento: Shenlongmon hibernando');
    });
    
    this.shenlongmon.on('wisdom-shared', (data) => {
      this.emit('shenlongmon:wisdom', data);
      logger.info('📚 Evento: Sabedoria compartilhada');
    });
  }
  
  // API Pública
  
  async submitTask(task: Task): Promise<any> {
    return this.triageQueue.add('task', task, {
      removeOnComplete: { count: 100 },
      removeOnFail: { count: 50 },
      attempts: 3,
      backoff: { type: 'exponential', delay: 1000 }
    });
  }
  
  async requestMentorship(topic: string, targetDigimon: string): Promise<any> {
    return this.mentorQueue.add('mentor', { topic, targetDigimon });
  }
  
  async reportConflict(
    parties: string[],
    issue: string,
    statements: Map<string, string>
  ): Promise<any> {
    return this.conflictQueue.add('conflict', { parties, issue, statements });
  }
  
  async requestDistillation(topic: string, k: number = 16): Promise<any> {
    return this.distillQueue.add('distill', { topic, k });
  }
  
  async start() {
    logger.info('🚀 Iniciando Shenlongmon Orchestrator...');
    
    // Inicia Dream Daemon
    this.dream.startDreamCycles();
    
    // Verifica modelos disponíveis
    const models = await this.ollama.ps();
    logger.info(`📦 Modelos carregados: ${models.models.map(m => m.name).join(', ')}`);
    
    logger.info('✨ Shenlongmon Orchestrator pronto!');
    
    // Integração com Digimundo existente
    this.emit('ready');
    
    return this;
  }
  
  async shutdown() {
    logger.info('🛑 Desligando Shenlongmon Orchestrator...');
    
    // Fecha filas
    await this.triageQueue.close();
    await this.mentorQueue.close();
    await this.conflictQueue.close();
    await this.distillQueue.close();
    
    // Garante que Shenlongmon está hibernando
    if (this.shenlongmon['isAwake']) {
      await this.shenlongmon['hibernate']();
    }
    
    logger.info('👋 Shenlongmon Orchestrator desligado');
  }
}

// ============= INTEGRAÇÃO COM DIGIMUNDO =============

export function integrateWithDigimundo(supremeOrchestrator: any) {
  const shenlongmon = new ShenlongmonOrchestrator();
  
  // Conecta com Supreme Orchestrator existente
  supremeOrchestrator.on('task-for-shenlongmon', async (task: Task) => {
    const result = await shenlongmon.submitTask(task);
    supremeOrchestrator.emit('shenlongmon-response', result);
  });
  
  // Repassa sabedoria para outros Digimons
  shenlongmon.on('shenlongmon:wisdom', (wisdom) => {
    supremeOrchestrator.broadcast('WISDOM_FROM_DRAGON', wisdom);
  });
  
  return shenlongmon;
}

// ============= STANDALONE EXECUTION =============

if (require.main === module) {
  const orchestrator = new ShenlongmonOrchestrator();
  
  orchestrator.start().then(async () => {
    // Exemplo de uso
    const testTask: Task = {
      id: uuid(),
      origin: 'Debugmon',
      content: 'Sistema crítico com memory leak causando crashes em produção',
      metadata: {
        category: 'security',
        impactScope: 'public',
        urgency: 10
      }
    };
    
    logger.info('🧪 Enviando tarefa de teste...');
    await orchestrator.submitTask(testTask);
    
    // Mantém processo vivo
    process.on('SIGINT', async () => {
      await orchestrator.shutdown();
      process.exit(0);
    });
  });
}

export default ShenlongmonOrchestrator;