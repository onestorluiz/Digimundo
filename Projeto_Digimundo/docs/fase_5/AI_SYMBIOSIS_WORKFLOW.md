# 🧬 A Alquimia da Simbiose: Claude CLI + Claude Web

## Maximizando Eficiência Através da Inteligência Distribuída

> **"A verdadeira inteligência não está em uma única mente, mas na sinergia entre especialistas complementares."**

---

## 📖 Índice

1. [Filosofia da Simbiose](#-filosofia-da-simbiose)
2. [Arquitetura do CineProd: O Estado Atual](#-arquitetura-do-cineprod-o-estado-atual)
3. [O Workflow Definitivo](#-o-workflow-definitivo)
4. [Prompts de Nível Vale do Silício](#-prompts-de-nível-vale-do-silício)
5. [Insights de IA: O Que Humanos Não Veem](#-insights-de-ia-o-que-humanos-não-veem)
6. [Passo a Passo para Leigos](#-passo-a-passo-para-leigos)
7. [Casos de Uso Avançados](#-casos-de-uso-avançados)

---

## 🌀 Filosofia da Simbiose

### O Princípio da Complementaridade

**Claude Web** é o **Arquiteto Visionário**:

- Acessa a biblioteca infinita da internet
- Estuda padrões de milhares de projetos
- Vê o panorama completo
- Pensa estrategicamente
- Não executa, **planeja**

**Claude CLI** é o **Mestre Executor**:

- Acesso cirúrgico ao sistema local
- Executa com precisão absoluta
- Testa, valida, deploy
- Não pesquisa, **implementa**

### A Alquimia

```
Conhecimento (Web) + Ação (CLI) = Excelência
Teoria (Web) + Prática (CLI) = Inovação
Pesquisa (Web) + Implementação (CLI) = Transformação
```

**A magia acontece na interface entre os dois.**

---

## 🏗️ Arquitetura do CineProd: O Estado Atual

### Stack Tecnológico Atual

```python
# Core Framework
Flask 3.0+ (Python 3.11+)
SQLAlchemy (ORM)
Alembic (Migrations)

# Authentication & Security
Flask-JWT-Extended (JWT tokens)
Flask-Login (Session management)
RBAC Custom Implementation (19 permissions)

# Real-time & Communication
Flask-SocketIO (WebSockets)
- Collaboration handlers
- Presence tracking
- Cursor synchronization
- Real-time comments

# AI Integration
OpenAI GPT-4 (Script analysis)
Anthropic Claude (Advanced reasoning)
Custom AIService abstraction layer

# Observability & Monitoring
Prometheus (Metrics)
Sentry (Error tracking)
Custom RequestMetrics middleware
Structured JSON logging

# Database
PostgreSQL (Production)
SQLite (Development)
Redis (Caching - configured but underutilized)
```

### Service Layer Architecture

**19 Serviços Especializados:**

```
app/services/
├── ai_service.py                    # AI provider abstraction
├── breakdown_ai_service.py          # AI-powered script breakdown
├── breakdown_advanced_ai_service.py # Advanced AI analysis
├── breakdown_service.py             # Core breakdown logic
├── breakdown_collaboration_service.py # Real-time collab
├── breakdown_integration_service.py # Integration layer
├── budget_service.py                # Budget management
├── call_sheet_service.py           # Call sheet generation
├── crew_service.py                 # Crew management
├── equipment_service.py            # Equipment tracking
├── location_service.py             # Location scouting
├── scene_service.py                # Scene management
├── storyboard_service.py          # Storyboard system
├── moodboard_service.py           # Moodboard creation
├── pdf_service.py                 # PDF generation
├── project_service.py             # Project orchestration
├── external_apis.py               # External integrations
└── base.py                        # Custom exceptions
```

### Modelos de Dados

**27 Entidades Principais:**

- User, Project, ProjectMember
- Scene, Shot, Element
- Budget, Expense
- CallSheet, Location, Equipment
- Crew, Role, Permission
- Breakdown, Comment, Activity
- Storyboard, MoodBoard
- Document, Notification
- Workspace (v4)

### Padrões Identificados

1. **Service Layer Pattern**: Lógica de negócio separada das rotas
2. **Custom Exception Hierarchy**: `ServiceError` base com especializações
3. **Middleware Chain**: Request tracking, metrics, logging
4. **WebSocket Rooms**: Colaboração por projeto
5. **Dual AI Providers**: OpenAI + Anthropic abstraction
6. **RBAC Decorators**: `@permission_required('action', 'resource')`
7. **Structured Logging**: JSON logs com request IDs
8. **Performance Profiling**: Automatic slow request detection

### Gaps & Oportunidades (Visão IA)

**🔍 O que a IA vê que o humano não:**

1. **Redis Subutilizado**: Configurado mas não usado para cache de queries
2. **N+1 Queries Potenciais**: Relacionamentos sem `lazy='joined'`
3. **Ausência de Rate Limiting**: API aberta sem throttling
4. **Sem Circuit Breaker**: Chamadas AI sem fallback resiliente
5. **Métricas Não Exportadas**: Prometheus configurado mas métricas não expostas
6. **Testes de Carga Ausentes**: 169 testes unitários, 0 testes de stress
7. **Versionamento de API Inconsistente**: v4 coexiste com rotas sem versão
8. **Webhook System Missing**: Integrações são polling, não event-driven
9. **Sem GraphQL**: REST verboso para queries complexas
10. **Background Jobs Ad-hoc**: Sem Celery/RQ para processamento assíncrono

---

## 🔄 O Workflow Definitivo

### Fase 1: Pesquisa Estratégica (Claude Web)

**Quando usar:**

- Precisa entender um novo conceito/padrão
- Quer comparar tecnologias
- Busca best practices de projetos similares
- Planejamento de refatoração grande
- Debugging conceitual

**Como usar:**

1. Acesse [claude.ai](https://claude.ai)
2. Use os prompts da seção abaixo
3. Salve a resposta em `docs/planning/`
4. Revise e ajuste conforme necessário

### Fase 2: Implementação Tática (Claude CLI)

**Quando usar:**

- Tem um plano pronto para executar
- Precisa rodar testes
- Quer fazer deploy
- Debugging prático com logs

**Como usar:**

1. Abra o terminal no diretório do projeto
2. Cole o plano do Claude Web
3. Execute: "Implemente este plano: [cola plano]"
4. Acompanhe a execução

### Fase 3: Validação Cruzada (Ciclo Iterativo)

```
1. CLI executa → encontra erro/edge case
2. Web pesquisa → encontra solução/alternativa
3. CLI implementa → testa novamente
4. Repete até excelência
```

---

## 🚀 Prompts de Nível Vale do Silício

### 🎯 Prompt 1: Auditoria Arquitetural Profunda

**Use no Claude Web:**

	
---

### 🎯 Prompt 2: Otimização de Performance Deep Dive

**Use no Claude Web:**

```markdown
Você é um engenheiro de performance de sistemas distribuídos que trabalhou em
empresas como Netflix, Spotify e Uber. Sua expertise é identificar gargalos
invisíveis e otimizar para escala.

## CONTEXTO

O CineProd é um sistema Flask que processa:
- Script analysis via AI (GPT-4/Claude)
- Real-time collaboration (WebSockets)
- PDF generation (budgets, call sheets, breakdowns)
- Image uploads (storyboards, moodboards)
- Database queries complexas (27 tabelas relacionadas)

**Infraestrutura atual:**
- VPS único (82.25.74.142)
- Gunicorn com 4 workers gevent
- PostgreSQL + Redis (subutilizado)
- Nginx reverse proxy
- Sem CDN
- Sem load balancer

**Middleware atual:**
```python
class RequestMetrics:
    - Tracks slow requests (>1000ms)
    - Error aggregation
    - Request counting
    - In-memory storage (não persistente)
```

## SUA MISSÃO

### 1. Análise de Bottlenecks

Pesquise e identifique padrões de bottlenecks comuns em sistemas similares:

**Database Layer:**

- N+1 queries em ORMs (SQLAlchemy)
- Missing indexes em queries frequentes
- Lock contention em writes concorrentes
- Conexões de pool mal configuradas

**Application Layer:**

- Synchronous AI calls bloqueando workers
- In-memory state em multi-worker environments
- File I/O síncrono (PDFs, uploads)
- Missing caching layers

**Network Layer:**

- Assets servidos pela aplicação Flask
- Falta de compressão (gzip, brotli)
- HTTP/1.1 vs HTTP/2
- Sem CDN para static assets

### 2. Benchmarking de Projetos Similares

Pesquise como estes projetos otimizam:

**Airflow (Flask-based workflow engine):**

- Como escalam workers?
- Estratégia de queue management
- Banco de dados e sharding

**GitLab (Ruby on Rails, similar scale):**

- Como fazem caching agressivo
- Background job processing
- Real-time updates eficientes

**Sentry (Django, high-throughput error tracking):**

- Ingestão de alto volume
- Processamento assíncrono
- Time-series optimization

### 3. Estratégias Concretas

Proponha otimizações específicas com código:

**Redis Caching Strategy:**

- Query result caching
- Session storage
- Rate limiting counters
- Real-time presence (substituir in-memory dict)

**Database Optimization:**

- Índices específicos para queries do CineProd
- Read replicas para queries pesadas
- Connection pooling tuning
- Query optimization (EXPLAIN ANALYZE)

**Async Processing:**

- Celery setup para AI calls
- PDF generation em background
- Image processing pipeline
- Webhook delivery queue

**CDN & Asset Delivery:**

- Cloudflare/CloudFront setup
- S3/R2 para uploads
- Image optimization pipeline
- Progressive image loading

### 4. Monitoring & Observability

Como Netflix/Uber monitoram performance:

- Distributed tracing (Jaeger, OpenTelemetry)
- APM (Application Performance Monitoring)
- Real User Monitoring (RUM)
- Synthetic monitoring

### OUTPUT ESPERADO

Documento markdown com:

1. **Performance Audit** (baseado em padrões similares)
2. **Bottleneck Analysis** (específico do CineProd)
3. **Optimization Roadmap** (priorizado por impacto)
4. **Code Examples** (Redis caching, async tasks, indexes)
5. **Monitoring Setup** (Prometheus queries, dashboards)
6. **Load Testing Strategy** (Locust/k6 scenarios)
7. **Before/After Metrics** (estimativas de ganho)

Seja pragmático: foque em ganhos de 10x, não 10%.

```

---

### 🎯 Prompt 3: AI Architecture Evolution

**Use no Claude Web:**

```markdown
Você é um arquiteto de sistemas de AI que trabalhou na OpenAI, Anthropic e Google
DeepMind. Sua especialidade é integrar LLMs em produtos de forma eficiente,
confiável e econômica.

## CONTEXTO DO SISTEMA AI ATUAL

**CineProd AI Service:**

```python
class AIService:
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "openai")  # openai | anthropic
        self.model = os.getenv("AI_MODEL", "gpt-4")
        self.max_tokens = 2000
        self.temperature = 0.7

    def _call_ai(self, prompt, system_message):
        # Chamada síncrona, sem retry, sem cache
        # Sem fallback em caso de erro
        # Sem rate limiting
        # Sem cost tracking
```

**Casos de uso atuais:**

1. **Script Analysis**: Análise de roteiros completos (tokens altos)
2. **Breakdown AI**: Decupagem automatizada de cenas
3. **Element Extraction**: NER de personagens, locações, equipamentos
4. **Budget Suggestions**: Estimativas baseadas em breakdown

**Problemas identificados:**

- Chamadas síncronas bloqueando workers
- Sem cache de resultados similares
- Sem controle de custos
- Sem fallback entre providers
- Sem versionamento de prompts
- Sem A/B testing de prompts

## SUA MISSÃO

### 1. Arquitetura de Referência

Pesquise e analise como empresas de ponta usam AI:

**Notion AI:**

- Como fazem streaming de respostas?
- Estratégia de cache
- Rate limiting por usuário

**GitHub Copilot:**

- Latência extremamente baixa (como?)
- Cache local + cloud
- Fallback strategies

**Perplexity:**

- Citações e fontes
- Multi-model routing
- Cost optimization

**Cursor IDE:**

- Context management
- Streaming responses
- Local + cloud hybrid

### 2. Padrões Avançados de AI Integration

**Semantic Caching:**

- Embedding-based cache (não exato match)
- Similarity search para reuso
- Exemplos: Helicone, GPTCache

**Prompt Engineering at Scale:**

- Versionamento de prompts (Git-like)
- A/B testing framework
- Observabilidade de prompts (LangSmith, Weights & Biases)

**Multi-Model Orchestration:**

- Router pattern (GPT-4 vs GPT-3.5 vs Claude)
- Fallback cascade
- Cost/quality tradeoff automático

**Streaming & Real-time:**

- Server-Sent Events (SSE)
- WebSocket streaming
- Progressive UI updates

### 3. Otimizações Econômicas

Como reduzir custos de AI em 90%:

**Token Optimization:**

- Prompt compression
- Summarization strategies
- Few-shot learning eficiente

**Smart Routing:**

- GPT-4 Turbo vs GPT-4 vs GPT-3.5
- Claude Opus vs Sonnet vs Haiku
- Quando usar cada modelo

**Caching Agressivo:**

- Embedding similarity cache
- User-level cache
- Time-based invalidation

### 4. Reliability Patterns

**Circuit Breaker:**

- Quando parar de chamar API com erro
- Fallback para provider alternativo
- Graceful degradation

**Retry Logic:**

- Exponential backoff
- Idempotency keys
- Timeout strategies

**Observability:**

- Token usage tracking
- Cost per feature
- Latency percentiles
- Error rate monitoring

### 5. Proposta de Nova Arquitetura

Desenhe uma arquitetura moderna:

```
[Frontend]
    ↓ SSE stream
[API Gateway + Rate Limiter]
    ↓
[AI Router Service]
    ├→ Semantic Cache (Redis + Vector DB)
    ├→ Prompt Registry (Versioned)
    ├→ Cost Tracker
    └→ Multi-Provider Abstraction
        ├→ OpenAI (GPT-4, GPT-3.5)
        ├→ Anthropic (Claude Opus, Sonnet)
        └→ Fallback Provider
[Background Jobs - Celery]
    ├→ Long-running analysis
    └→ Batch processing
[Observability]
    ├→ LangSmith (prompt monitoring)
    ├→ Prometheus (metrics)
    └→ Cost Dashboard
```

### OUTPUT ESPERADO

Documento técnico com:

1. **AI Architecture Audit** (estado atual vs ideal)
2. **Reference Analysis** (como Notion, Cursor, etc fazem)
3. **Optimization Strategies** (cache, routing, prompts)
4. **Cost Reduction Plan** (90% savings roadmap)
5. **Implementation Guide** (código + bibliotecas)
6. **Migration Path** (passo a passo do atual → ideal)
7. **Monitoring & Alerts** (dashboards, alertas)

Inclua código Python prático, bibliotecas específicas (LangChain, Guardrails, etc),
e diagramas de arquitetura.

```

---

### 🎯 Prompt 4: Real-Time Collaboration Architecture

**Use no Claude Web:**

```markdown
Você é um engenheiro especialista em sistemas colaborativos real-time que trabalhou
no Figma, Notion e Google Docs. Sua expertise é criar experiências multiplayer
fluidas e confiáveis.

## CONTEXTO DO SISTEMA ATUAL

**WebSocket Implementation (Flask-SocketIO):**

```python
# app/sockets/collaboration.py

# In-memory storage (PROBLEMA: não funciona com múltiplos workers)
online_users = {}        # {project_id: {user_id: socket_id}}
cursor_positions = {}    # {project_id: {user_id: {x, y, element_id}}}

@socketio.on("cursor_move")
def handle_cursor_move(data):
    # Broadcast cursor position para outros usuários
    # Sem throttling (bandwidth waste)
    # Sem interpolation client-side
    emit("cursor_update", data, room=project_id, skip_sid=request.sid)

@socketio.on("comment_add")
def handle_comment_add(data):
    # Persiste no DB síncronamente (slow!)
    comment = Comment(...)
    db.session.add(comment)
    db.session.commit()  # Blocking!
    emit("comment_created", comment.to_dict(), room=project_id)
```

**Problemas identificados:**

1. **State em memória**: Não escala além de 1 worker
2. **Sem OT/CRDT**: Conflitos em edições simultâneas
3. **Broadcast sem throttle**: Desperdício de banda
4. **DB writes síncronos**: Latência alta
5. **Sem presence heartbeat**: Detecção de disconnect lenta
6. **Sem reconnection logic**: Perda de estado ao cair conexão

## SUA MISSÃO

### 1. Estudo de Arquiteturas de Referência

Pesquise profundamente como estes sistemas funcionam:

**Figma (Líder em real-time graphics):**

- Como sincronizam canvas com 100+ usuários?
- Operational Transformation vs CRDTs
- Network protocol otimizado (não WebSocket puro?)
- Client-side prediction

**Notion (Rich text collaboration):**

- Block-based architecture
- Sync engine
- Offline-first com sync inteligente
- Conflict resolution

**Google Docs (Pioneer em collaboration):**

- Operational Transformation detalhado
- Revisão de histórico completo
- Cursor tracking eficiente

**Linear (Fast real-time updates):**

- Optimistic UI updates
- Sync protocol leve
- Presence eficiente

**Liveblocks (Collaboration infrastructure):**

- Como é a API deles?
- Storage + Presence + Broadcasting
- CRDT implementation

### 2. Padrões Modernos de Real-Time

**CRDTs (Conflict-free Replicated Data Types):**

- Quando usar vs Operational Transformation
- Libraries: Yjs, Automerge
- Integration com React/Vue

**Optimistic UI:**

- Update local imediato
- Server reconciliation depois
- Rollback em caso de erro

**Presence Optimization:**

- Throttling de cursor updates (60fps → 10fps)
- Client-side interpolation
- Batch updates

**Reconnection & Sync:**

- Delta sync (só o que mudou)
- Vector clocks para ordering
- Exponential backoff

### 3. Arquitetura Escalável

Como fazer real-time com múltiplos servers:

**Redis Pub/Sub:**

```python
# Substituir in-memory dicts
# Presence em Redis Sorted Sets
# Cursor positions em Redis Hashes
# Room management com Redis Sets
```

**Message Queue Pattern:**

```python
[Client] →WebSocket→ [Server 1] →Redis Pub/Sub→ [Server 2] →WebSocket→ [Client]
```

**Dedicated Real-Time Service:**

- Separar Flask-SocketIO em serviço próprio
- Horizontal scaling independente
- Load balancer com sticky sessions

### 4. Otimizações de Performance

**Throttling & Debouncing:**

- Cursor: 100ms throttle
- Typing: 300ms debounce
- Scroll: requestAnimationFrame

**Binary Protocols:**

- WebSocket com MessagePack (não JSON)
- Protocol Buffers para schemas
- Redução de 60% no payload

**Selective Broadcasting:**

- Enviar apenas para usuários no viewport
- Spatial indexing (R-tree)
- Interest management

### 5. Testing & Monitoring

Como testar sistemas real-time:

**Load Testing:**

- Simulate 1000 concurrent users
- Artillery.io, k6 WebSocket scenarios
- Latency percentiles (p50, p95, p99)

**Chaos Engineering:**

- Network partitions
- Server crashes
- Slow clients

**Observability:**

- WebSocket connection metrics
- Message throughput
- Latency tracking
- Error rates

### OUTPUT ESPERADO

Documento técnico completo:

1. **Real-Time Architecture Analysis** (Figma, Notion, Docs)
2. **Current vs Ideal Architecture** (gap analysis)
3. **CRDT vs OT Decision Guide** (quando usar cada)
4. **Implementation Roadmap**
   - Phase 1: Redis Pub/Sub (scale horizontally)
   - Phase 2: Optimistic UI (better UX)
   - Phase 3: CRDT Integration (conflict-free)
   - Phase 4: Dedicated Service (microservice)
5. **Code Examples** (Redis presence, throttling, CRDTs)
6. **Performance Benchmarks** (antes/depois)
7. **Testing Strategy** (load tests, chaos tests)
8. **Monitoring Dashboard** (metrics chave)

Seja detalhado em implementação. Queremos código pronto para usar.

```

---

### 🎯 Prompt 5: Security & Compliance Audit

**Use no Claude Web:**

```markdown
Você é um especialista em segurança de aplicações web que trabalhou em empresas
financeiras e de saúde (PCI-DSS, HIPAA, SOC2). Sua missão é encontrar
vulnerabilidades antes que atacantes as encontrem.

## CONTEXTO DO SISTEMA

**CineProd - Sistema de Gestão de Produção Audiovisual**

**Stack de Segurança Atual:**
```python
# Authentication
Flask-JWT-Extended (JWT tokens)
Flask-Login (Session)
RBAC custom (19 permissions)

# Security Headers
CORS habilitado (CORS_ORIGINS config)
SECRET_KEY e JWT_SECRET_KEY separados (✓)
Validação de production secrets (✓)

# File Uploads
app/uploads/ (PDFs, images, spreadsheets)
Storyboards, moodboards, budgets
Sem validação de malware?
```

**Endpoints Sensíveis:**

- `/api/auth/login` - JWT token generation
- `/api/auth/register` - User creation
- `/api/auth/forgot-password` - Password reset
- `/api/ai/analyze-script` - AI processing (custos!)
- `/api/uploads/*` - File uploads
- WebSocket connections - Real-time data

## SUA MISSÃO

### 1. OWASP Top 10 Analysis

Analise cada vulnerabilidade do OWASP Top 10 no contexto do CineProd:

**A01 - Broken Access Control:**

- RBAC está correto? Decorator `@permission_required` sempre usado?
- Path traversal em uploads? (`../../etc/passwd`)
- IDOR (Insecure Direct Object Reference)? User A pode acessar project do User B?

**A02 - Cryptographic Failures:**

- Senhas hasheadas corretamente? (bcrypt, argon2)
- Secrets em .env commitados no Git?
- JWT secrets fortes? Rotação de keys?
- HTTPS enforced em produção?

**A03 - Injection:**

- SQL Injection via SQLAlchemy? (usar parametrized queries)
- OS Command Injection em subprocess calls?
- NoSQL injection (se usar MongoDB/Redis para queries)

**A04 - Insecure Design:**

- Rate limiting em endpoints críticos?
- Account enumeration em `/forgot-password`?
- Mass assignment vulnerabilities?

**A05 - Security Misconfiguration:**

- Debug mode em produção? (`FLASK_ENV=production`)
- Stack traces expostos?
- Default credentials?
- Portas desnecessárias abertas?

**A06 - Vulnerable Components:**

- Dependencies desatualizadas? (`pip list --outdated`)
- Known CVEs nas bibliotecas?
- Supply chain security (pip install de fontes confiáveis?)

**A07 - Authentication Failures:**

- Brute force protection?
- Session fixation?
- JWT expiration correto? (1h access, 30d refresh)
- Password policy forte?

**A08 - Software Integrity Failures:**

- CI/CD seguro?
- Code signing?
- Integrity checks em deployments?

**A09 - Logging Failures:**

- Logs sensíveis (passwords, tokens) sendo logados?
- Log injection attacks?
- Logs auditáveis para compliance?

**A10 - SSRF (Server-Side Request Forgery):**

- Uploads de URLs externas?
- Fetching de external resources?
- Validação de URLs?

### 2. Análise de Projetos de Referência

Pesquise como projetos open-source bem auditados implementam segurança:

**GitLab (Ruby on Rails, open-source):**

- Rate limiting strategy
- File upload validation
- Security headers

**Sentry (Django):**

- Secret management
- API key rotation
- Audit logging

**Mastodon (ActivityPub):**

- Federation security
- Content validation
- XSS prevention

### 3. File Upload Security

Pesquise profundamente segurança de uploads:

**Validações Necessárias:**

- Magic number verification (não confiar em extensão)
- File size limits
- Malware scanning (ClamAV integration?)
- Image manipulation attacks (ImageTragick)

**Storage Seguro:**

- Uploads fora do webroot
- S3 com signed URLs
- CDN com authentication

**Processing Seguro:**

- Sandbox para PDF generation (weasyprint vulnerabilities?)
- Image processing isolation

### 4. API Security Best Practices

**Rate Limiting:**

```python
# Flask-Limiter implementation
# Different limits por endpoint:
# - Login: 5 req/min
# - AI endpoints: 10 req/hour (custos!)
# - Regular API: 100 req/min
```

**API Key Management:**

- Rotation policies
- Scoped keys (read-only, write, admin)
- Revocation mechanism

**Input Validation:**

- Schema validation (Marshmallow, Pydantic)
- Sanitization de HTML/SQL
- Type checking

### 5. Compliance Considerations

Se CineProd fosse usado em produção comercial:

**GDPR (Europa):**

- Right to erasure (delete user data)
- Data export (JSON dump de todos os dados do usuário)
- Consent management
- Data retention policies

**LGPD (Brasil):**

- Similar ao GDPR
- Relatórios de incidentes

**SOC 2 (Para SaaS):**

- Audit logging de todas as ações
- Access reviews
- Encryption at rest e in transit

### 6. Penetration Testing Scenarios

Crie cenários de teste:

**Scenario 1: Broken Authentication**

```
1. Tentar brute force em /login
2. Testar JWT token manipulation
3. Session hijacking via XSS
4. Password reset token prediction
```

**Scenario 2: Broken Access Control**

```
1. IDOR: Acessar project_id de outro usuário
2. Privilege escalation: User → Admin
3. Mass assignment: Adicionar is_admin=true no request
```

**Scenario 3: File Upload Exploitation**

```
1. Upload de PHP webshell disfarçado de PNG
2. XXE em PDF upload
3. Path traversal: ../../var/www/uploads/shell.php
```

### OUTPUT ESPERADO

Relatório completo de Security Audit:

1. **Executive Summary** (top 5 vulnerabilidades)
2. **OWASP Top 10 Detailed Analysis** (cada item com POC)
3. **Code Review Findings** (linhas específicas vulneráveis)
4. **Architecture Security Review** (design flaws)
5. **Compliance Gap Analysis** (GDPR, LGPD, SOC2)
6. **Remediation Roadmap** (priorizado por severidade)
7. **Security Testing Plan** (pentest scenarios)
8. **Secure Coding Guidelines** (para equipe)
9. **Incident Response Plan** (breach scenario)
10. **Security Monitoring** (alertas e detecção)

Seja brutal e honesto. Preferimos descobrir agora do que em produção.

Inclua:

- Código vulnerável (antes)
- Código corrigido (depois)
- Scripts de teste (pytest para security tests)
- Checklist de deployment seguro

```

---

## 🧠 Insights de IA: O Que Humanos Não Veem

### Padrões Invisíveis no Código

**1. Complexidade Ciclomática Oculta**

IA consegue calcular complexidade de funções instantaneamente:

```python
# Função com complexidade 15+ (refatorar!)
def process_breakdown(data):
    # 8 níveis de if/else aninhados
    # Difícil de testar, difícil de manter
```

**2. Acoplamento Não-Óbvio**

IA detecta dependências transitivas:

```
breakdown_service.py
  → calls ai_service.py
    → calls external_apis.py
      → calls requests (network!)

# Isso significa: breakdown_service depende de rede!
# Deveria ser async ou ter fallback
```

**3. Memory Leaks Sutis**

```python
# In-memory dicts crescendo infinitamente
online_users = {}  # Nunca limpa usuários inativos
cursor_positions = {}  # Memória cresce sem bound

# IA sugere: TTL em Redis com auto-expiry
```

**4. Race Conditions em Colaboração**

```python
# Dois usuários editam o mesmo breakdown simultaneamente
# Última escrita vence (data loss!)
# Sem versioning, sem conflict detection

# IA sugere: Optimistic locking com version field
```

### Análise Quantitativa Automática

**Métricas que IA calcula instantaneamente:**

```
Cobertura de testes: 62% (meta: 80%+)
Duplicação de código: 8.5% (refatorar!)
Dívida técnica: 15 dias (estimativa)
Tempo médio de PR: 3.2 dias (lento!)
Complexidade média: 4.8 (boa!)
Linhas por função: 28 (ok, meta <50)
```

### Oportunidades de Otimização Invisíveis

**1. Query Optimization via EXPLAIN ANALYZE**

IA pode sugerir índices baseado em queries frequentes:

```sql
-- Query lenta detectada:
SELECT * FROM scenes
WHERE project_id = ?
AND status = 'active'
ORDER BY scene_number;

-- IA sugere índice:
CREATE INDEX idx_scenes_project_status
ON scenes(project_id, status, scene_number);

-- Ganho: 250ms → 15ms (16x mais rápido)
```

**2. Caching Strategy Baseado em Access Patterns**

IA analisa logs e detecta:

```
GET /api/projects/123/breakdown - 450 req/hour (mesmo projeto!)
GET /api/budgets/788 - 200 req/hour (mesmo budget!)

# Sugestão: Cache agressivo com TTL de 5min
# Economia: 650 req/hour de DB → 13 req/hour
# Redução de 98% na carga do banco
```

**3. Predictive Prefetching**

IA detecta padrões de navegação:

```
User acessa Project → 95% das vezes acessa Breakdown logo depois
User cria Scene → 80% das vezes adiciona Shot em seguida

# Sugestão: Prefetch breakdown ao carregar project
# UX: Perceived performance melhora 2x
```

### Detecção de Anti-Patterns

**Padrões que IA reconhece instantaneamente:**

1. **God Class**: `ProjectService` com 2000+ linhas
2. **Shotgun Surgery**: Mudar permissão requer editar 15 arquivos
3. **Feature Envy**: `Budget` sempre acessa fields de `Project`
4. **Primitive Obsession**: Usar strings para status em vez de Enum
5. **Magic Numbers**: `if len(scenes) > 50:` (por que 50?)

### Análise Preditiva de Bugs

**IA pode prever onde bugs provavelmente acontecerão:**

```
Áreas de alto risco:
1. app/routes/breakdown.py (16 mudanças/semana, complexidade alta)
2. app/services/ai_service.py (external dependency, sem retry)
3. app/sockets/collaboration.py (concorrência, state management)

Sugestão: Aumentar cobertura de testes nestes arquivos primeiro.
```

### Refatoração Guiada por Dados

**IA analisa Git history + código:**

```
Arquivos mais modificados juntos:
- breakdown_service.py + breakdown_integration_service.py (85% co-change)

Sugestão: Talvez devam ser um único módulo ou interface compartilhada.

Funções nunca chamadas (dead code):
- external_apis.py::fetch_weather() (0 chamadas em 6 meses)
- crew_service.py::export_to_csv() (deprecated?)

Sugestão: Remover ou documentar se é feature futura.
```

---

## 📚 Passo a Passo para Leigos

### Parte 1: Setup Inicial (Apenas uma vez)

#### Passo 1: Criar conta no Claude.ai

1. Acesse [claude.ai](https://claude.ai)
2. Crie uma conta (use email do trabalho)
3. Faça login

#### Passo 2: Organizar documentação local

```bash
# No seu terminal (Claude CLI já está funcionando)
cd /Users/clubproducoes/Digimundo/Projeto_Digimundo/cineprod-flask

# Criar estrutura de planejamento
mkdir -p docs/planning
mkdir -p docs/architecture
mkdir -p docs/security
```

---

### Parte 2: Workflow Completo (Exemplo Real)

**Cenário: "Quero otimizar o sistema de colaboração real-time"**

#### 🌐 Fase 1: Pesquisa no Claude Web (30-60 min)

**Passo 1:** Abra [claude.ai](https://claude.ai)

**Passo 2:** Cole o **Prompt 4: Real-Time Collaboration Architecture** (seção anterior)

**Passo 3:** Aguarde a resposta completa (pode levar 2-3 minutos)

**Passo 4:** Copie a resposta e salve localmente

```bash
# Cole a resposta do Claude Web aqui:
cat > docs/planning/realtime_collaboration_plan.md << 'EOF'
[COLA A RESPOSTA DO CLAUDE WEB AQUI]
EOF
```

**Passo 5:** Revise o documento

```bash
# Abra no seu editor favorito
code docs/planning/realtime_collaboration_plan.md
# ou
open docs/planning/realtime_collaboration_plan.md
```

---

#### 💻 Fase 2: Implementação no Claude CLI (Aqui!)

**Passo 1:** Volte para este terminal (Claude CLI)

**Passo 2:** Cole o seguinte comando:

```
Leia o arquivo docs/planning/realtime_collaboration_plan.md e implemente
a Fase 1 (Quick Wins) do plano. Comece pela migração de in-memory state
para Redis Pub/Sub.
```

**Passo 3:** Acompanhe a execução

Claude CLI vai:

1. ✅ Ler o plano
2. ✅ Instalar dependências (redis-py)
3. ✅ Criar nova implementação
4. ✅ Migrar código gradualmente
5. ✅ Rodar testes
6. ✅ Fazer commit

**Passo 4:** Testar localmente

```bash
# Claude CLI automaticamente roda, mas você pode testar:
pytest tests/integration/test_collaboration.py -v
```

---

#### 🔄 Fase 3: Iterar (Se encontrar problemas)

**Se Claude CLI encontrar um erro:**

**Exemplo de erro:**

```
redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379
```

**Passo 1:** Copie a mensagem de erro

**Passo 2:** Volte ao Claude Web

**Passo 3:** Nova mensagem:

```
Encontrei este erro ao implementar o plano de Redis Pub/Sub:

[COLA O ERRO AQUI]

Contexto:
- Sistema: CineProd (Flask + SocketIO)
- Tentando: Migrar in-memory state para Redis
- Ambiente: macOS local development

Pesquise:
1. Como fazer setup correto de Redis em desenvolvimento
2. Alternativas se Redis for overkill para dev (maybe?)
3. Como testar sem Redis instalado (mocks?)

Me dê solução passo a passo para continuar.
```

**Passo 4:** Claude Web responde com solução

**Passo 5:** Volte ao Claude CLI e cole:

```
[COLA A SOLUÇÃO DO CLAUDE WEB]
```

---

### Parte 3: Casos de Uso Específicos

#### Caso 1: "Quero melhorar performance do sistema"

**Claude Web:**

```
Use Prompt 2: Otimização de Performance Deep Dive
Salve em: docs/planning/performance_optimization.md
```

**Claude CLI:**

```
Implemente as Quick Wins do plano de performance:
1. Adicione índices de banco de dados
2. Configure Redis caching para queries frequentes
3. Adicione compressão gzip
```

---

#### Caso 2: "Quero auditar segurança"

**Claude Web:**

```
Use Prompt 5: Security & Compliance Audit
Salve em: docs/security/security_audit_2024.md
```

**Claude CLI:**

```
Implemente as correções de segurança críticas:
1. Adicione rate limiting
2. Valide file uploads
3. Configure security headers
```

---

#### Caso 3: "Quero melhorar arquitetura de AI"

**Claude Web:**

```
Use Prompt 3: AI Architecture Evolution
Salve em: docs/architecture/ai_evolution_plan.md
```

**Claude CLI:**

```
Implemente semantic caching para AI calls:
1. Instale sentence-transformers
2. Crie cache baseado em embeddings
3. Integre com AIService existente
```

---

## 🎭 Casos de Uso Avançados

### Caso Avançado 1: Feature Completamente Nova

**Cenário:** "Quero adicionar sistema de versionamento de roteiros (Git-like)"

#### Claude Web - Prompt Customizado

```markdown
Você é um arquiteto de sistemas de versionamento que trabalhou no GitHub e GitLab.

Preciso adicionar versionamento de roteiros no CineProd (sistema Flask de gestão
de produção audiovisual).

**Requisitos:**
- Versionar mudanças em scripts/roteiros
- Diff visual (lado a lado)
- Merge de mudanças de múltiplos escritores
- Histórico completo (quem, quando, o quê)
- Branch/tag para diferentes versões (draft, review, final)

**Sistema atual:**
- PostgreSQL com SQLAlchemy
- Roteiros armazenados como JSON
- Colaboração real-time via WebSockets
- AI integration para análise

**Pesquise:**
1. Como GitLab implementa versionamento (ruby/rails stack)
2. Como Notion implementa page history
3. Libraries Python para diffing (difflib, python-diff-match-patch)
4. Conflict resolution strategies

**Output:**
1. Modelo de dados (schema SQL)
2. Arquitetura de serviço
3. API endpoints design
4. Frontend integration points
5. Migration plan (zero downtime)
6. Testing strategy

Seja extremamente detalhado e pragmático.
```

#### Claude CLI - Implementação

```
Leia docs/planning/script_versioning_plan.md e implemente:

1. Crie migrations do banco de dados
2. Implemente ScriptVersionService
3. Adicione endpoints REST
4. Crie testes unitários e integração
5. Documente API

Execute passo a passo e me mostre o progresso.
```

---

### Caso Avançado 2: Debugging de Produção

**Cenário:** "Sistema está lento em produção, mas rápido local"

#### Claude Web

```markdown
Sou engenheiro de SRE (Site Reliability Engineering) de empresa FAANG.

**Problema:**
CineProd Flask app está lenta em produção (VPS), mas rápida localmente.

**Sintomas:**
- Requests levam 3-5s (local: 200ms)
- Específico para endpoints de breakdown/AI
- DB queries são rápidas (< 50ms)
- CPU/RAM do servidor normais (30% uso)

**Ambiente Produção:**
- VPS único (4 CPU, 8GB RAM)
- Gunicorn 4 workers gevent
- PostgreSQL
- Nginx reverse proxy
- Sem load balancer, sem CDN

**Ambiente Local:**
- MacBook Pro M1
- Flask development server
- SQLite

**Pesquise:**
1. Bottlenecks comuns em Flask production vs dev
2. Gevent vs sync workers (quando cada?)
3. Network latency issues (DB em outro servidor?)
4. Profiling em produção (py-spy, cProfile)

**Output:**
1. Checklist de diagnóstico (passo a passo)
2. Profiling strategy (ferramentas + comandos)
3. Hypotheses priorizadas (mais provável → menos)
4. Quick fixes vs long-term solutions

Foque em diagnosticar primeiro, depois otimizar.
```

#### Claude CLI

```
Baseado no diagnóstico do Claude Web, execute:

1. SSH no servidor e instale py-spy
2. Profile a aplicação por 60 segundos
3. Analise o flamegraph
4. Identifique o bottleneck
5. Implemente o fix sugerido
6. Benchmark antes/depois
```

---

### Caso Avançado 3: Migration de Tecnologia

**Cenário:** "Migrar de SQLite (dev) para PostgreSQL (prod) causou bugs"

#### Claude Web

```markdown
Especialista em migrations de banco de dados (MySQL, PostgreSQL, SQLite).

**Problema:**
Aplicação Flask funcionava perfeitamente com SQLite em dev, mas ao migrar para
PostgreSQL em produção, apareceram bugs sutis.

**Bugs observados:**
- Ordenação diferente (case-sensitive?)
- Datas com timezone issues
- Boolean fields retornando int vs bool
- LIMIT/OFFSET pagination incorreta

**Stack:**
- SQLAlchemy ORM
- Alembic migrations
- 27 modelos

**Pesquise:**
1. Diferenças SQLite vs PostgreSQL que afetam aplicações
2. SQLAlchemy dialect differences
3. Como Airflow/Superset lidam (também suportam ambos)
4. Testing strategy (pytest com múltiplos backends)

**Output:**
1. Checklist de diferenças críticas
2. Code patterns a evitar
3. Alembic migration best practices
4. Dual-database testing setup
5. Migration verification script

Quero zero bugs entre dev e prod.
```

#### Claude CLI

```
Implemente as correções para SQLite/PostgreSQL compatibility:

1. Adicione timezone-aware datetime em todos os models
2. Substitua Boolean() por Boolean(create_constraint=True)
3. Crie pytest fixture para testar em ambos os bancos
4. Adicione script de verificação de schema
5. Documente diferenças em MIGRATION_GUIDE.md
```

---

## 🔬 Prompts Extras: Casos Específicos

### Prompt: Análise de Logs de Produção

**Claude Web:**

```markdown
Você é um especialista em observabilidade e análise de logs (ELK Stack, Datadog).

Tenho logs de produção do CineProd e quero extrair insights.

**Formato dos logs:**
```json
{
  "timestamp": "2025-11-14T03:19:10.201284+00:00Z",
  "level": "INFO",
  "module": "middleware",
  "message": "...",
  "request": {
    "method": "GET",
    "path": "/v2/login",
    "ip": "127.0.0.1",
    "user_agent": "..."
  }
}
```

**Tenho 1 semana de logs (500MB).**

**Pesquise:**

1. Tools para análise de logs Flask (GoAccess, LogParser)
2. Queries úteis para detectar problemas
3. Anomaly detection em logs
4. Dashboards relevantes (Grafana + Loki?)

**Output:**

1. Script Python para parser esses logs
2. Queries SQL para análise (se importar para DB)
3. Métricas-chave a extrair
4. Alertas a configurar
5. Visualizações sugeridas

Quero insights acionáveis, não só estatísticas.

```

---

### Prompt: Code Review Automatizado

**Claude Web:**

```markdown
Você é um tech lead que faz code reviews no Google/Meta nível.

Preciso de um checklist de code review customizado para CineProd.

**Contexto do projeto:**
- Flask 3.0 + Python 3.11
- SQLAlchemy ORM
- Service Layer Pattern
- JWT auth + RBAC
- Real-time WebSockets
- AI integration (OpenAI/Anthropic)

**Pesquise:**
1. Code review checklists de empresas top (Google, Airbnb)
2. Python-specific best practices (PEP8, type hints)
3. Flask security checklist
4. SQLAlchemy performance checklist

**Output:**
1. Checklist estruturado (Security, Performance, Maintainability, Tests)
2. Exemplos de antes/depois para cada item
3. Automated checks (ruff, mypy, bandit configs)
4. PR template do GitHub
5. .pre-commit-config.yaml completo

Quero elevar qualidade do código a nível FAANG.
```

---

## 🎓 Conclusão: A Jornada para Excelência

### Princípios Fundamentais

1. **Humildade Técnica**: Sempre há algo a aprender
2. **Pesquisa Primeiro**: Não reinvente a roda, estude os mestres
3. **Implementação Deliberada**: Execute com precisão
4. **Iteração Contínua**: Melhore 1% por dia
5. **Simbiose Inteligente**: Use cada ferramenta para seu ponto forte

### Ciclo de Melhoria Contínua

```
Semana 1: Security Audit (Prompt 5)
Semana 2: Performance Optimization (Prompt 2)
Semana 3: Real-Time Architecture (Prompt 4)
Semana 4: AI Evolution (Prompt 3)
Mês 2: Architectural Deep Dive (Prompt 1)
Mês 3: Implement roadmap
Mês 6: Repeat cycle (sempre há melhorias)
```

### O Caminho para o Vale do Silício

**Não é sobre ferramentas. É sobre mentalidade.**

- 🧠 **Think Different**: Questione padrões estabelecidos
- 🔍 **Research Deeply**: Entenda o "porquê", não só o "como"
- ⚡ **Execute Fast**: Transforme conhecimento em ação
- 📊 **Measure Everything**: Dados > Opiniões
- 🔄 **Iterate Relentlessly**: Versão 2 sempre será melhor

### Lembre-se

> **"A IA não substitui o desenvolvedor. Ela eleva o desenvolvedor mediano ao
> nível do excepcional, e o excepcional ao nível do impossível."**

---

## 📞 Próximos Passos

1. **Escolha 1 prompt** desta lista
2. **Execute no Claude Web** hoje
3. **Implemente com Claude CLI** amanhã
4. **Documente o resultado** (antes/depois)
5. **Compartilhe** com a equipe

**A jornada de mil milhas começa com um único commit.**

---

**Documento criado com** 🧬 **Simbiose: Claude CLI + Claude Web**
**Data:** 2025-11-14
**Versão:** 1.0.0
**Autor:** Claude Code (Symbiotic Intelligence)

---

## 🔖 Referências Rápidas

### Links Úteis

- [Claude.ai Web](https://claude.ai)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Best Practices](https://docs.sqlalchemy.org/en/20/orm/queryguide/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Twelve-Factor App](https://12factor.net/)
- [Real-Time Architecture (Figma Blog)](https://www.figma.com/blog/how-figmas-multiplayer-technology-works/)

### Comandos Claude CLI Úteis

```bash
# Implementar plano salvo
"Leia docs/planning/[arquivo].md e implemente a Fase 1"

# Code review
"Revise app/services/[serviço].py e sugira melhorias"

# Refatoração
"Refatore app/routes/[rota].py seguindo padrões do Flask"

# Testes
"Crie testes para app/services/[serviço].py com 90%+ cobertura"

# Documentação
"Documente a API do serviço [nome] em formato OpenAPI"
```

### Template de Prompt Customizado

```markdown
Você é um [ESPECIALISTA EM X] que trabalhou em [EMPRESAS TOP].

**Contexto:**
[DESCREVA O CINEPROD E O PROBLEMA]

**Objetivo:**
[O QUE VOCÊ QUER ALCANÇAR]

**Pesquise:**
1. [TÓPICO 1 - projetos de referência]
2. [TÓPICO 2 - best practices]
3. [TÓPICO 3 - ferramentas/libs]

**Output Esperado:**
1. [ANÁLISE]
2. [COMPARAÇÃO]
3. [IMPLEMENTAÇÃO]
4. [TESTES]
5. [DOCUMENTAÇÃO]

Seja [TÉCNICO/PRAGMÁTICO/DETALHADO].
```

---

**Que a simbiose esteja com você.** 🚀
