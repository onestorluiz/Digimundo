# 📁 CineProd - Estrutura Completa do Projeto

**Data**: 2025-11-15
**Versão**: 2.3.1
**Propósito**: Mapa completo para navegação e desenvolvimento

---

## 🗺️ Visão Geral da Estrutura

```
/Users/clubproducoes/Digimundo/
├── Projeto_Digimundo/
│   └── cineprod-flask/          ← 🎯 VOCÊ ESTÁ AQUI
│       ├── app/                  ← Aplicação principal
│       ├── config/               ← Configurações
│       ├── migrations/           ← Migrações de banco
│       ├── tests/                ← Testes
│       ├── docs/                 ← Documentação
│       ├── scripts/              ← Scripts utilitários
│       ├── logs/                 ← Arquivos de log
│       ├── instance/             ← Banco de dados SQLite
│       ├── venv/                 ← Ambiente virtual Python
│       └── wsgi.py               ← Entry point
│
├── claude_code/                  ← Memórias e análises Claude
│   └── MEMORY/
│       ├── erros_aprendidos/     ← 🔴 LEIA para evitar erros
│       ├── conhecimentos/        ← Templates e checklists
│       └── analises/             ← Análises de sistemas
│
└── scripturemon/                 ← Sistema de análise de roteiros
```

---

## 📂 Estrutura Detalhada: `/app/`

### 🎯 Diretório Raiz `app/`

```
app/
├── __init__.py              ← Inicialização da aplicação Flask (100 linhas)
├── logger.py                ← Sistema de logging (6.6 KB)
├── logging_config.py        ← Configuração de logs (6.4 KB)
├── middleware.py            ← Request logging middleware (7.6 KB)
├── email_service.py         ← Serviço de email (8.0 KB)
├── rate_limit.py            ← Rate limiting (6.3 KB)
├── sentry_config.py         ← Configuração Sentry (5.2 KB)
│
├── models/                  ← 📦 Modelos de dados (27 arquivos)
├── routes/                  ← 🛣️ Endpoints da API (45+ arquivos)
├── services/                ← ⚙️ Lógica de negócio (19 arquivos)
├── sockets/                 ← 🔌 WebSocket handlers (5 arquivos)
├── schemas/                 ← 📋 Validação Marshmallow (15 arquivos)
├── utils/                   ← 🔧 Utilitários (12 arquivos)
├── templates/               ← 🎨 Frontend HTML
├── static/                  ← 📦 Assets estáticos
└── uploads/                 ← 📁 Arquivos de upload
```

---

## 📦 `app/models/` - Modelos de Dados (27 arquivos)

### Estrutura de Models

```python
app/models/
├── __init__.py          ← Importa todos os models (2.2 KB)
│
├── user.py              ← Usuários e autenticação (7.0 KB)
├── project.py           ← Projetos audiovisuais (4.9 KB)
├── project_member.py    ← Membros de projetos (10.8 KB)
│
├── scene.py             ← Cenas de roteiro (7.4 KB)
├── shot.py              ← Shots/tomadas (5.8 KB)
├── script.py            ← Roteiros (3.6 KB)
├── element.py           ← Elementos de breakdown (5.7 KB)
├── scene_element.py     ← Relação scene-element (3.0 KB)
│
├── call_sheet.py        ← Mapas de filmagem (12.1 KB)
├── schedule.py          ← Programação de filmagem (2.4 KB)
├── storyboard.py        ← Storyboards (13.3 KB)
├── moodboard.py         ← Moodboards (4.5 KB)
│
├── crew.py              ← Equipe técnica (3.2 KB)
├── equipment.py         ← Equipamentos (2.9 KB)
├── location.py          ← Locações (2.8 KB)
│
├── budget.py            ← Orçamento (6.0 KB)
├── expense.py           ← Despesas (5.4 KB)
│
├── document.py          ← Documentos (3.6 KB)
├── comment.py           ← Comentários (5.8 KB)
├── activity.py          ← Atividades/logs (6.5 KB)
├── notification.py      ← Notificações (7.2 KB)
│
├── role.py              ← Roles (4.8 KB)
├── permission.py        ← Permissões (5.1 KB)
├── role_permission.py   ← Role-Permission (6.7 KB)
│
└── workspace_member.py  ← (Legacy - migrar para project_member)
```

### 🔍 Models por Categoria

#### 👤 Autenticação & Permissões

| Model | Arquivo | Propósito | Linhas |
|-------|---------|-----------|--------|
| User | user.py | Usuários, auth, password | 170 |
| Role | role.py | Papéis (Director, Producer, etc) | 95 |
| Permission | permission.py | Permissões granulares | 110 |
| RolePermission | role_permission.py | Relação many-to-many | 135 |

#### 🎬 Produção

| Model | Arquivo | Propósito | Linhas |
|-------|---------|-----------|--------|
| Project | project.py | Projetos audiovisuais | 100 |
| ProjectMember | project_member.py | Membros + roles | 230 |
| Scene | scene.py | Cenas de roteiro | 155 |
| Shot | shot.py | Shots/tomadas | 125 |
| Script | script.py | Upload de roteiros | 80 |

#### 📋 Breakdown & Planejamento

| Model | Arquivo | Propósito | Linhas |
|-------|---------|-----------|--------|
| Element | element.py | Elementos (props, vestuário, etc) | 120 |
| SceneElement | scene_element.py | Relação scene-element | 65 |
| CallSheet | call_sheet.py | Mapas de filmagem | 260 |
| Schedule | schedule.py | Programação | 55 |
| Storyboard | storyboard.py | Storyboards visuais | 285 |
| Moodboard | moodboard.py | Moodboards | 95 |

#### 🔧 Recursos

| Model | Arquivo | Propósito | Linhas |
|-------|---------|-----------|--------|
| Crew | crew.py | Equipe técnica | 70 |
| Equipment | equipment.py | Equipamentos | 60 |
| Location | location.py | Locações | 58 |

#### 💰 Financeiro

| Model | Arquivo | Propósito | Linhas |
|-------|---------|-----------|--------|
| Budget | budget.py | Orçamento do projeto | 128 |
| Expense | expense.py | Despesas | 115 |

#### 🔔 Sistema

| Model | Arquivo | Propósito | Linhas |
|-------|---------|-----------|--------|
| Document | document.py | Upload de arquivos | 78 |
| Comment | comment.py | Comentários | 125 |
| Activity | activity.py | Activity feed/logs | 140 |
| Notification | notification.py | Notificações push | 155 |

---

## ⚙️ `app/services/` - Lógica de Negócio (19 arquivos)

```python
app/services/
├── base.py                          ← Exceções base (1.5 KB)
│
├── ai_service.py                    ← Integração com IA (13.4 KB)
├── breakdown_ai_service.py          ← Breakdown com IA (17.2 KB)
├── breakdown_advanced_ai_service.py ← Breakdown avançado (25.4 KB)
├── breakdown_collaboration_service.py ← Colaboração real-time (20.8 KB)
├── breakdown_integration_service.py  ← Integração breakdown (23.7 KB)
├── breakdown_service.py              ← Breakdown core (19.2 KB)
│
├── project_service.py               ← CRUD de projetos (19.5 KB)
├── scene_service.py                 ← CRUD de scenes (18.0 KB)
├── call_sheet_service.py            ← Call sheets (10.4 KB)
├── storyboard_service.py            ← Storyboards (19.1 KB)
├── moodboard_service.py             ← Moodboards (14.4 KB)
├── budget_service.py                ← Orçamento (11.8 KB)
│
├── crew_service.py                  ← Gestão de crew (7.1 KB)
├── equipment_service.py             ← Gestão de equipamentos (6.1 KB)
├── location_service.py              ← Gestão de locações (6.0 KB)
│
├── pdf_service.py                   ← Geração de PDFs (14.7 KB)
├── external_apis.py                 ← APIs externas (7.1 KB)
│
└── (10 services adicionais)
```

### 📊 Services por Categoria

#### 🤖 IA & Automação

- `ai_service.py` - Core IA (OpenAI/Anthropic)
- `breakdown_ai_service.py` - Auto-breakdown de roteiros
- `breakdown_advanced_ai_service.py` - Análise avançada
- `breakdown_collaboration_service.py` - Colaboração com IA

#### 🎬 Core de Produção

- `project_service.py` - Projetos (CRUD + lógica)
- `scene_service.py` - Scenes (CRUD + cálculos)
- `call_sheet_service.py` - Mapas de filmagem
- `storyboard_service.py` - Storyboards visuais
- `moodboard_service.py` - Moodboards

#### 💰 Financeiro

- `budget_service.py` - Orçamento e forecasting

#### 🔧 Recursos

- `crew_service.py` - Equipe
- `equipment_service.py` - Equipamentos
- `location_service.py` - Locações

#### 📄 Utilitários

- `pdf_service.py` - Geração de relatórios PDF
- `external_apis.py` - Integrações externas

---

## 🛣️ `app/routes/` - Endpoints da API (45+ arquivos)

```python
app/routes/
├── __init__.py              ← Registro de blueprints
│
├── auth.py                  ← Login, logout, JWT refresh
├── index.py                 ← Homepage, health checks
├── health.py                ← Health check endpoint
│
├── projects.py              ← /api/projects
├── scenes.py                ← /api/scenes
├── shots.py                 ← /api/shots
├── scripts.py               ← /api/scripts
│
├── breakdown.py             ← /api/breakdown
├── breakdown_integration.py ← /api/breakdown-integration
├── breakdown_collab.py      ← /api/breakdown-collab
│
├── call_sheets.py           ← /api/call-sheets
├── schedule.py              ← /api/schedule
├── storyboards.py           ← /api/storyboards
├── moodboards.py            ← /api/moodboards
│
├── crew.py                  ← /api/crew
├── equipment.py             ← /api/equipment
├── locations.py             ← /api/locations
│
├── budget.py                ← /api/budget
├── documents.py             ← /api/documents
├── comments.py              ← /api/comments
├── notifications.py         ← /api/notifications
│
├── roles.py                 ← /api/roles
├── permissions.py           ← /api/permissions
│
├── reports.py               ← /api/reports (PDF exports)
├── ai.py                    ← /api/ai (IA endpoints)
│
├── v2.py                    ← /v2/* (nova versão)
├── v4/                      ← /v4/* (versão 4)
│   ├── activities.py
│   ├── comments.py
│   ├── projects.py
│   └── scenes.py
│
└── debug.py                 ← Debug endpoints (só dev)
```

### 🎯 Routes por Versão

#### V1 (Legacy - Deprecated)
- Rotas diretas sem prefixo `/api`
- Mantidas por compatibilidade

#### V2 (Atual - Produção)
- Prefixo: `/api/*`
- RESTful design
- JWT authentication
- Rate limiting
- Usado em produção

#### V4 (Experimental)
- Prefixo: `/v4/*`
- Novas features
- Breaking changes vs V2

---

## 🔌 `app/sockets/` - WebSocket Handlers

```python
app/sockets/
├── __init__.py          ← Setup SocketIO
├── collaboration.py     ← Colaboração real-time (7.6 KB)
├── presence.py          ← User presence
├── comments.py          ← Comentários real-time
└── updates.py           ← Updates de projeto
```

### Eventos WebSocket

| Namespace | Evento | Handler | Propósito |
|-----------|--------|---------|-----------|
| `/collab` | `join_scene` | collaboration.py | Entrar em cena para edição |
| `/collab` | `scene_update` | collaboration.py | Atualização de cena |
| `/collab` | `cursor_move` | collaboration.py | Cursor de colaborador |
| `/presence` | `user_online` | presence.py | Usuário ficou online |
| `/comments` | `new_comment` | comments.py | Novo comentário |

---

## 🔧 `app/utils/` - Utilitários

```python
app/utils/
├── decorators.py        ← @requires_permission, @limiter, etc
├── permissions.py       ← Check de permissões
├── validation.py        ← Validações customizadas
├── pagination.py        ← Paginação de queries
├── error_interceptor.py ← Global error handler
├── file_upload.py       ← Upload de arquivos
├── script_parser.py     ← Parse de roteiros (FDX, PDF)
├── schema_analyzer.py   ← Análise de schemas
└── (4+ utils)
```

---

## 📋 `app/schemas/` - Validação Marshmallow

```python
app/schemas/
├── user_schema.py       ← Validação de User
├── project_schema.py    ← Validação de Project
├── scene_schema.py      ← Validação de Scene
├── (12+ schemas)
└── base_schema.py       ← Schema base
```

---

## 🎨 `app/templates/` - Frontend

```
app/templates/
├── v2/                  ← Frontend atual (produção)
│   ├── index.html       ← SPA principal
│   ├── login.html       ← Tela de login
│   ├── projects.html    ← Lista de projetos
│   └── (20+ páginas)
│
├── pdfs/                ← Templates para PDF
│   ├── call_sheet.html  ← Template de mapa
│   ├── budget.html      ← Template de orçamento
│   └── storyboard.html  ← Template de storyboard
│
└── emails/              ← Templates de email
    ├── forgot_password.html
    └── welcome.html
```

---

## 📦 `app/static/` - Assets Estáticos

```
app/static/
├── css/
│   └── tailwind.css     ← Tailwind CSS
├── js/
│   ├── app.js           ← JavaScript principal
│   └── (modules)
└── images/
    └── logo.png
```

---

## 📁 `app/uploads/` - Arquivos de Upload

```
app/uploads/
├── scripts/             ← Roteiros (.fdx, .pdf, .txt)
├── storyboards/         ← Imagens de storyboard
├── call_sheets/         ← PDFs de mapas
├── documents/           ← Documentos diversos
└── avatars/             ← Avatars de usuários
```

---

## ⚙️ `/config/` - Configurações

```
config/
├── __init__.py          ← Config base
├── development.py       ← Config dev
├── production.py        ← Config prod
├── testing.py           ← Config testes
└── docker.py            ← Config Docker
```

### Variáveis de Ambiente (.env)

```bash
# Flask
FLASK_ENV=development
SECRET_KEY=<secret>
JWT_SECRET_KEY=<secret>

# Database
SQLALCHEMY_DATABASE_URI=postgresql://user:pass@localhost/cineprod

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=email@gmail.com
MAIL_PASSWORD=<app-password>

# Redis
REDIS_URL=redis://localhost:6379

# Sentry
SENTRY_DSN=<dsn>

# AI
OPENAI_API_KEY=<key>
ANTHROPIC_API_KEY=<key>
```

---

## 🗄️ `/migrations/` - Migrações de Banco

```
migrations/
├── env.py               ← Config Alembic
├── script.py.mako       ← Template de migration
└── versions/            ← Migrações versionadas
    ├── 1fe3fdf07087_initial_migration.py
    ├── add_storyboard_system.py
    ├── add_moodboard_system.py
    └── (20+ migrations)
```

### Como criar migration:

```bash
# Auto-gerar a partir de models:
flask db migrate -m "Descrição da mudança"

# Aplicar:
flask db upgrade

# Reverter:
flask db downgrade
```

---

## 🧪 `/tests/` - Testes Automatizados

```
tests/
├── unit/                ← Testes unitários
│   ├── test_models/
│   ├── test_services/
│   └── test_routes/
│
├── integration/         ← Testes de integração
│   ├── test_api_workflow.py
│   └── test_database.py
│
├── conftest.py          ← Fixtures pytest
└── (169 arquivos de teste)
```

### Rodar testes:

```bash
# Todos os testes:
pytest

# Com coverage:
pytest --cov=app --cov-report=html

# Apenas unit:
pytest tests/unit

# Apenas integration:
pytest tests/integration
```

---

## 📚 `/docs/` - Documentação

```
docs/
├── 00_START_HERE_CLAUDE_METHODOLOGY.md  ← 🔥 LER PRIMEIRO
├── 01_PROJECT_STRUCTURE.md              ← Este arquivo
├── 02_IMPLEMENTATION_MASTER_PLAN.md     ← Roadmap completo
├── CINEPROD_ARCHITECTURE_CORRELATIONS_DEEP_ANALYSIS.md  ← Análise profunda
│
├── architecture/        ← Arquitetura do sistema
│   ├── MAPA_SISTEMA_COMPLETO.md
│   └── CINEPROD_SYSTEM_ANALYSIS_COMPLETE.md
│
├── development/         ← Guias de desenvolvimento
│   ├── CINEPROD_UPGRADE_MASTER_PLAN.md
│   └── PLANO_DESENVOLVIMENTO_ATUALIZADO.md
│
├── deployment/          ← Deploy e produção
│   ├── DEPLOYMENT_FINAL_GUIDE.md
│   ├── DOCKER_GUIDE.md
│   └── MAINTENANCE_GUIDE.md
│
└── reports/             ← Relatórios e análises
    ├── VPS_STATUS_REPORT_2025-10-28.md
    └── COMPLETE_SYSTEM_AUDIT_2025-10-31.md
```

---

## 🔧 `/scripts/` - Scripts Utilitários

```
scripts/
├── seed_permissions.py  ← Popular permissões iniciais
├── test_complete_workflow.sh ← Teste end-to-end
├── backup_database.sh   ← Backup do banco
└── deploy/              ← Scripts de deploy
    └── production/
        ├── deploy.sh
        └── sync_to_vps.sh
```

---

## 📊 Estatísticas do Projeto

| Métrica | Valor |
|---------|-------|
| **Linhas de código Python** | 31.561 |
| **Modelos (models)** | 27 arquivos |
| **Serviços (services)** | 19 arquivos |
| **Rotas (routes)** | 45+ arquivos |
| **Testes** | 169 arquivos |
| **Migrações** | 20+ arquivos |
| **Documentação** | 30+ arquivos |
| **Cobertura de testes** | ~80% |

---

## 🎯 Onde Criar Cada Tipo de Arquivo

### Novos Models

```bash
# Local:
app/models/novo_model.py

# Template:
cat app/models/scene.py  # Como referência

# Adicionar em:
app/models/__init__.py  # Importar o model
```

### Novos Services

```bash
# Local:
app/services/novo_service.py

# Template:
cat app/services/scene_service.py  # Como referência

# Herdar de:
from app.services.base import ServiceError, NotFoundError
```

### Novas Routes

```bash
# Local:
app/routes/novo_route.py

# Template:
cat app/routes/scenes.py  # Como referência

# Registrar em:
app/routes/__init__.py  # Adicionar blueprint
app/__init__.py         # Registrar blueprint
```

### Novos WebSocket Handlers

```bash
# Local:
app/sockets/novo_handler.py

# Template:
cat app/sockets/collaboration.py

# Registrar em:
app/sockets/__init__.py
```

### Novos Utilitários

```bash
# Local:
app/utils/novo_util.py

# Template:
cat app/utils/decorators.py
```

### Novos Testes

```bash
# Local:
tests/unit/test_novo.py          # Teste unitário
tests/integration/test_novo.py   # Teste de integração

# Template:
cat tests/unit/test_scene_service.py
```

---

## 🔍 Como Encontrar Algo no Projeto

### Procurar por funcionalidade:

```bash
# Buscar classe/função:
grep -r "class SceneService" app/

# Buscar uso de algo:
grep -r "SceneService" app/ --include="*.py"

# Buscar em models:
grep -r "class.*Model" app/models/

# Buscar routes:
grep -r "@bp.route" app/routes/
```

### Procurar por arquivo:

```bash
# Por nome:
find app -name "*scene*"

# Por tipo:
find app -name "*.py" -type f

# Por tamanho:
find app -size +10k -name "*.py"
```

---

## 📖 Convenções de Nomenclatura

### Arquivos Python:

- **Models**: `snake_case.py` (ex: `project_member.py`)
- **Services**: `snake_case_service.py` (ex: `scene_service.py`)
- **Routes**: `snake_case.py` (ex: `storyboards.py`)
- **Utils**: `snake_case.py` (ex: `file_upload.py`)

### Classes:

- **Models**: `PascalCase` (ex: `ProjectMember`)
- **Services**: `PascalCase` (ex: `SceneService`)
- **Schemas**: `PascalCase` + `Schema` (ex: `SceneSchema`)
- **Exceptions**: `PascalCase` + `Error` (ex: `NotFoundError`)

### Funções/Métodos:

- **Tudo**: `snake_case` (ex: `calculate_budget()`)

### Variáveis:

- **Tudo**: `snake_case` (ex: `total_cost`)
- **Constantes**: `UPPER_CASE` (ex: `MAX_FILE_SIZE`)

---

## 🚀 Fluxo de Desenvolvimento Típico

### 1. Nova Feature: "Sistema de Equipamentos"

```bash
# 1. Contexto
cd /Users/clubproducoes/Digimundo/Projeto_Digimundo/cineprod-flask

# 2. Verificar se já existe
grep -r "equipment" app/ --ignore-case
ls app/models/ | grep equipment
ls app/services/ | grep equipment

# 3. Criar model (se não existe)
# app/models/equipment.py

# 4. Criar service
# app/services/equipment_service.py

# 5. Criar routes
# app/routes/equipment.py

# 6. Criar migration
flask db migrate -m "Add equipment system"
flask db upgrade

# 7. Criar testes
# tests/unit/test_equipment_service.py
# tests/integration/test_equipment_api.py

# 8. Rodar testes
pytest tests/unit/test_equipment_service.py

# 9. Commit
git add .
git commit -m "feat: Add equipment management system"
```

---

## 📞 Contato & Suporte

**Documentação Técnica**: `/docs/`
**Erros Conhecidos**: `/claude_code/MEMORY/erros_aprendidos/`
**Templates**: `/claude_code/MEMORY/conhecimentos/`

---

**Atualizado**: 2025-11-15
**Mantido por**: Claude AI + Human Developer
**Versão do Projeto**: 2.3.1

---

**DIGIMUNDO PRESENTE 🥷**
