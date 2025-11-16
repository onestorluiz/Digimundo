# 🚀 Guia de Upgrade & Migração - CineProd v2.3.1 → v3.0 (Fase 5)

**Implementação Prática da Intelligence Layer**

> "Um grande sistema não é construído, é evolved metodicamente"

**Data**: 2025-11-15
**Versão**: 1.0
**Target**: CineProd v3.0 com Intelligence Layer

---

## 📋 Índice

1. [Visão Geral do Upgrade](#visão-geral-do-upgrade)
2. [Pré-requisitos](#pré-requisitos)
3. [Fase 5.1: Foundation](#fase-51-foundation)
4. [Fase 5.2: Conflict Detection](#fase-52-conflict-detection)
5. [Fase 5.3: Schedule Optimizer](#fase-53-schedule-optimizer)
6. [Fase 5.4: Predictive Analytics](#fase-54-predictive-analytics)
7. [Testing & Validation](#testing--validation)
8. [Deployment Strategy](#deployment-strategy)
9. [Rollback Plan](#rollback-plan)
10. [Post-Upgrade Checklist](#post-upgrade-checklist)

---

## 🎯 VISÃO GERAL DO UPGRADE

### O Que Muda

```
v2.3.1 (Atual)                    v3.0 (Target)
===============                   ==============
- Sistema reativo                 - Sistema proativo
- Detecção manual de conflitos    - Detecção automática
- Scheduling manual               - Otimização automática
- Sem predições                   - Analytics preditivo
- Test coverage: 37.13%           - Test coverage: 80%+
- 570 failing/error tests         - 0 failing tests
```

### Timeline (ATUALIZADO 2025-11-16)

> **IMPORTANTE**: Timeline ajustada de 10→17 semanas após análise profunda do baseline real.
> Motivo: 570 testes com problemas (não 175), Event Sourcing movido para Fase 5.1, complexidade subestimada.

| Fase | Duração | Esforço (dev-weeks) | Mudança |
|------|---------|---------------------|---------|
| Fase 5.1: Foundation | **4 semanas** | 8 | +2 semanas (570 testes + Event Sourcing MVP) |
| Fase 5.2: Conflict Detection | **3 semanas** | 6 | +1 semana (depende de Event Sourcing) |
| Fase 5.3: Schedule Optimizer | **5 semanas** | 10 | +2 semanas (CP Solver complexo) |
| Fase 5.4: Predictive Analytics | **4 semanas** | 8 | +2 semanas (ML infra setup) |
| Testing & Validation | 1 semana | 2 | - |
| **Total** | **17 semanas** | **34** | +7 semanas (+70%) |

### Recursos Necessários

- 2 desenvolvedores Python fulltime
- 1 DevOps (part-time para infraestrutura)
- 1 QA/Tester (part-time)

---

## ✅ PRÉ-REQUISITOS

### Checklist Antes de Começar

- [ ] Backup completo do banco de dados
- [ ] Código atual em Git (tag v2.3.1)
- [ ] Ambiente de staging configurado
- [ ] Testes atuais documentados (quais estão failing)
- [ ] Aprovação stakeholders
- [ ] Janela de manutenção agendada (se necessário)

### Ambiente de Desenvolvimento

```bash
# 1. Clone do repositório
git clone https://github.com/onestorluiz/Digimundo.git
cd Digimundo/Projeto_Digimundo/cineprod-flask

# 2. Criar branch de desenvolvimento
git checkout -b feature/intelligence-layer-phase5

# 3. Verificar Python version
python --version  # Deve ser 3.11+

# 4. Criar virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 5. Instalar dependências atuais
pip install -r requirements.txt

# 6. Rodar testes atuais (baseline)
pytest tests/ --cov=app --cov-report=html
# Resultado (2025-11-16): 3,460 passing, 140 failing, 430 errors, 37.13% coverage
```

### Novas Dependências

Adicionar ao `requirements.txt`:

```txt
# Intelligence Layer dependencies
redis==5.0.1               # Cache
celery==5.3.4              # Async tasks
numpy==1.26.2              # Numeric computation
pandas==2.1.3              # Data analysis
scikit-learn==1.3.2        # Machine learning (predictive)

# Schedule Optimization
ortools==9.8.3296          # Google OR-Tools (CP solver)

# Testing
pytest-asyncio==0.21.1     # Async tests
faker==20.1.0              # Test data generation
factory-boy==3.3.0         # Model factories

# Monitoring
prometheus-client==0.19.0  # Metrics
```

Instalar:

```bash
pip install -r requirements.txt
```

---

## 🏗️ FASE 5.1: FOUNDATION (Semanas 1-4) - ATUALIZADO

> **IMPORTANTE**: Fase 5.1 expandida de 2→4 semanas para incluir Event Sourcing MVP.
> Event Sourcing é bloqueador crítico para Conflict Detection (Fase 5.2).

### Objetivos:

1. ✅ Corrigir **570 testes** com problemas (430 errors + 140 failures)
2. ✅ Aumentar test coverage para **70%+** (de 37.13%)
3. ✅ Adicionar Redis cache
4. ✅ Setup Celery para async tasks
5. ✅ **Implementar Event Sourcing MVP** (novo requisito)

### Task 1.1: Corrigir Testes Falhando (Semanas 1-2) - ATUALIZADO

> **ATUALIZAÇÃO**: 570 testes com problemas (não 175):
> - 430 import/collection errors
> - 140 test logic failures
>
> Plano detalhado em `TEST_CORRECTION_PLAN.md` (4 semanas).

**Análise**:

```bash
# Identificar testes falhando
pytest tests/ -v | grep FAILED > failing_tests.txt

# Analisar padrões
cat failing_tests.txt
```

**Categorias Comuns**:
- Imports quebrados
- Fixtures desatualizadas
- Mocks incorretos
- Assertions obsoletas

**Estratégia**:

```bash
# Dividir trabalho
# Dev 1: tests/unit/ (80 failing)
# Dev 2: tests/integration/ (95 failing)

# Corrigir por categoria:
# 1. Imports (fix all imports first)
# 2. Fixtures (update fixtures)
# 3. Assertions (fix assertion logic)
# 4. Removals (delete obsolete tests)
```

**Exemplo de Correção**:

```python
# ANTES (failing)
def test_scene_creation(client):
    response = client.post('/api/scenes', json={'name': 'Test'})
    assert response.status_code == 201

# PROBLEMA: Falta project_id (required field)

# DEPOIS (fixed)
def test_scene_creation(client, sample_project):
    response = client.post('/api/v1/scenes', json={
        'name': 'Test Scene',
        'project_id': sample_project.id,
        'scene_number': '01'
    })
    assert response.status_code == 201
    assert 'id' in response.json
```

**Verificação**:

```bash
# Rodar testes após correções
pytest tests/ -v

# Target: 0 failing
```

---

### Task 1.2: Aumentar Test Coverage (Semana 1-2)

**Gaps Atuais** (coverage por módulo):

```
app/routes/auth.py         18% ❌
app/routes/budget.py       35% ❌
app/routes/scripts.py      34% ❌
app/routes/scenes.py       47% ⚠️
app/routes/breakdown.py    41% ⚠️
app/routes/call_sheets.py  38% ❌
```

**Estratégia**:

Adicionar **200+ testes** focados em routes:

```bash
# Dividir por módulo
# Dev 1: auth (30 tests), budget (25 tests), scripts (20 tests)
# Dev 2: scenes (35 tests), breakdown (30 tests), call_sheets (25 tests)
```

**Template de Teste**:

```python
# tests/integration/test_auth_routes.py

class TestAuthRoutes:
    """Test suite for authentication routes"""

    def test_register_success(self, client):
        """
        GIVEN valid registration data
        WHEN POST /api/auth/register
        THEN user is created and returns 201
        """
        response = client.post('/api/auth/register', json={
            'email': 'newuser@example.com',
            'password': 'SecurePass123',
            'name': 'New User'
        })

        assert response.status_code == 201
        assert 'access_token' in response.json

    def test_register_duplicate_email(self, client, sample_user):
        """
        GIVEN email already exists
        WHEN POST /api/auth/register with same email
        THEN returns 409 Conflict
        """
        response = client.post('/api/auth/register', json={
            'email': sample_user.email,
            'password': 'SecurePass123',
            'name': 'Another User'
        })

        assert response.status_code == 409
        assert 'already exists' in response.json['error'].lower()

    def test_login_success(self, client, sample_user):
        """
        GIVEN valid credentials
        WHEN POST /api/auth/login
        THEN returns 200 with tokens
        """
        response = client.post('/api/auth/login', json={
            'email': sample_user.email,
            'password': 'password123'  # Sample user password
        })

        assert response.status_code == 200
        assert 'access_token' in response.json
        assert 'refresh_token' in response.json

    def test_login_wrong_password(self, client, sample_user):
        """
        GIVEN wrong password
        WHEN POST /api/auth/login
        THEN returns 401 Unauthorized
        """
        response = client.post('/api/auth/login', json={
            'email': sample_user.email,
            'password': 'wrongpassword'
        })

        assert response.status_code == 401

    def test_refresh_token(self, client, auth_tokens):
        """
        GIVEN valid refresh token
        WHEN POST /api/auth/refresh
        THEN returns new access token
        """
        response = client.post('/api/auth/refresh', headers={
            'Authorization': f'Bearer {auth_tokens["refresh_token"]}'
        })

        assert response.status_code == 200
        assert 'access_token' in response.json

    # ... adicionar 25+ testes similares
```

**Meta**: auth routes coverage 18% → 80%+

**Repetir** para todos os módulos.

---

### Task 1.3: Setup Redis Cache (Semana 2)

**Instalação**:

```bash
# macOS
brew install redis

# Ubuntu
sudo apt-get install redis-server

# Start Redis
redis-server
```

**Configuração**:

```python
# app/config.py

class Config:
    # ... existing config ...

    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
```

**Implementação**:

```python
# app/__init__.py

from flask_caching import Cache

cache = Cache()

def create_app(config_name='default'):
    app = Flask(__name__)
    # ... existing setup ...

    # Initialize cache
    cache.init_app(app, config={
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': app.config['REDIS_URL']
    })

    return app
```

**Uso**:

```python
# app/routes/scenes.py

from app import cache

@bp.route('/api/v1/scenes/<int:project_id>', methods=['GET'])
@cache.cached(timeout=300, key_prefix='scenes_project')  # Cache 5 min
def list_scenes(project_id):
    scenes = Scene.query.filter_by(project_id=project_id).all()
    return jsonify([s.to_dict() for s in scenes])

# Invalidar cache ao criar/editar scene
@bp.route('/api/v1/scenes', methods=['POST'])
def create_scene():
    # ... create scene ...

    # Invalidar cache
    cache.delete(f'scenes_project_{scene.project_id}')

    return jsonify(scene.to_dict()), 201
```

---

### Task 1.4: Setup Celery (Semana 2)

**Configuração**:

```python
# app/celery_app.py

from celery import Celery
from app import create_app

flask_app = create_app()

celery = Celery(
    flask_app.import_name,
    broker=flask_app.config['REDIS_URL'],
    backend=flask_app.config['REDIS_URL']
)

celery.conf.update(flask_app.config)

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask
```

**Task Example**:

```python
# app/tasks/conflict_detection.py

from app.celery_app import celery
from app.intelligence.conflict_detection.engine import ConflictDetectionEngine

@celery.task
def detect_conflicts_async(project_id):
    """
    Async task para detectar conflitos
    """
    engine = ConflictDetectionEngine()
    result = engine.detect(project_id)

    # Salvar resultado no cache
    from app import cache
    cache.set(f'conflicts_{project_id}', result, timeout=3600)

    return result
```

**Rodar Worker**:

```bash
# Terminal 1: Flask app
flask run

# Terminal 2: Celery worker
celery -A app.celery_app worker --loglevel=info
```

---

### Verificação Fase 5.1

**Checklist**:
- [ ] 0 failing tests
- [ ] Test coverage >= 70%
- [ ] Redis funcionando
- [ ] Celery worker rodando
- [ ] Cache invalidation testado
- [ ] Performance benchmark (queries 3x mais rápidas)

**Métricas**:

```bash
# Coverage
pytest --cov=app --cov-report=term

# Deve mostrar:
# TOTAL: 70%+

# Performance
# Antes (sem cache): GET /api/v1/scenes/1 → 450ms
# Depois (com cache): GET /api/v1/scenes/1 → 50ms  ✅
```

---

### Task 1.5: Event Sourcing MVP (Semanas 3-4) ⭐ NOVO

> **⚠️ BLOQUEADOR CRÍTICO**: Conflict Detection (Fase 5.2) precisa de Event Sourcing
> para rastrear histórico de mudanças em cenas, recursos e conflitos.

#### Por Que Event Sourcing Agora?

**Problema Identificado**:
```python
# Conflict Detection precisa responder:
# - Quando este conflito começou?
# - Quem mudou esta cena que causou conflito?
# - Qual era o estado da locação antes do conflito?

# Sem Event Sourcing → IMPOSSÍVEL responder estas perguntas
# Com Event Sourcing → Event Store tem TODA a história
```

**Decisão**: Implementar Event Sourcing MVP em Fase 5.1 (não esperar Phase 2).

---

#### Implementação MVP

**Escopo Reduzido** (apenas eventos críticos):

1. **SceneUpdated** - Mudanças em cenas
2. **ResourceBooked** - Reservas de recursos (atores, locações, equipamentos)
3. **ConflictDetected** - Detecção de conflitos
4. **ConflictResolved** - Resolução de conflitos

**Database Schema** (3 tabelas):

```sql
-- app/migrations/versions/xxx_add_event_store.py

def upgrade():
    # Tabela principal de eventos
    op.create_table('events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('aggregate_type', sa.String(50), nullable=False),  # 'Scene', 'Resource', etc
        sa.Column('aggregate_id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(100), nullable=False),  # 'SceneUpdated', 'ResourceBooked'
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('sequence_number', sa.Integer(), nullable=False),  # Para ordenação
        sa.Index('idx_aggregate', 'aggregate_type', 'aggregate_id'),
        sa.Index('idx_timestamp', 'timestamp'),
    )

    # Snapshots (otimização - opcional para MVP)
    op.create_table('event_snapshots',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('aggregate_type', sa.String(50), nullable=False),
        sa.Column('aggregate_id', sa.Integer(), nullable=False),
        sa.Column('snapshot_data', sa.JSON(), nullable=False),
        sa.Column('sequence_number', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint('aggregate_type', 'aggregate_id', name='uq_snapshot'),
    )

    # Subscriptions (quem quer ser notificado de eventos - opcional)
    op.create_table('event_subscriptions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('event_type', sa.String(100), nullable=False),
        sa.Column('handler', sa.String(200), nullable=False),  # 'conflict_detection_service.on_scene_updated'
        sa.Column('active', sa.Boolean(), default=True),
    )
```

**Event Store Service**:

```python
# app/services/event_store_service.py

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, List, Dict
from app.models import db

@dataclass
class Event:
    aggregate_type: str  # 'Scene'
    aggregate_id: int    # scene_id
    event_type: str      # 'SceneUpdated'
    payload: Dict[str, Any]
    user_id: int
    timestamp: datetime = None
    sequence_number: int = None

class EventStoreService:
    """
    MVP Event Store - armazena e consulta eventos
    """

    @staticmethod
    def append_event(event: Event):
        """
        Adiciona evento ao store
        """
        # Auto-gerar sequence number
        last_event = db.session.execute(
            sa.select(Event).filter_by(
                aggregate_type=event.aggregate_type,
                aggregate_id=event.aggregate_id
            ).order_by(Event.sequence_number.desc()).limit(1)
        ).scalar_one_or_none()

        sequence = (last_event.sequence_number + 1) if last_event else 1

        event_record = Event(
            aggregate_type=event.aggregate_type,
            aggregate_id=event.aggregate_id,
            event_type=event.event_type,
            payload=event.payload,
            user_id=event.user_id,
            timestamp=event.timestamp or datetime.utcnow(),
            sequence_number=sequence
        )

        db.session.add(event_record)
        db.session.commit()

        return event_record

    @staticmethod
    def get_events(aggregate_type: str, aggregate_id: int, from_sequence: int = 0) -> List[Event]:
        """
        Busca eventos de um agregado
        """
        events = db.session.execute(
            sa.select(Event).filter(
                Event.aggregate_type == aggregate_type,
                Event.aggregate_id == aggregate_id,
                Event.sequence_number >= from_sequence
            ).order_by(Event.sequence_number)
        ).scalars().all()

        return events

    @staticmethod
    def get_timeline(aggregate_type: str, aggregate_id: int) -> List[Dict]:
        """
        Retorna timeline de mudanças (para UI)
        """
        events = EventStoreService.get_events(aggregate_type, aggregate_id)

        return [{
            'timestamp': e.timestamp,
            'event_type': e.event_type,
            'user_id': e.user_id,
            'changes': e.payload
        } for e in events]

    @staticmethod
    def replay_events(aggregate_type: str, aggregate_id: int):
        """
        Replay de eventos (debugging / rebuild)
        """
        events = EventStoreService.get_events(aggregate_type, aggregate_id)

        # Reconstruir estado a partir de eventos
        state = {}
        for event in events:
            # Aplicar evento ao estado
            # (lógica depende do aggregate)
            pass

        return state
```

**Integração em SceneService** (exemplo):

```python
# app/services/scene_service.py

class SceneService:

    @staticmethod
    def update(scene_id, updates, user_id):
        scene = db.session.get(Scene, scene_id)

        # Capturar estado antigo
        old_values = {}
        for field, new_value in updates.items():
            old_values[field] = getattr(scene, field)

        # Aplicar mudanças
        for field, value in updates.items():
            setattr(scene, field, value)

        db.session.commit()

        # ✨ NOVO: Registrar evento
        event = Event(
            aggregate_type='Scene',
            aggregate_id=scene_id,
            event_type='SceneUpdated',
            payload={
                'changes': {
                    field: {'old': old_values[field], 'new': updates[field]}
                    for field in updates.keys()
                }
            },
            user_id=user_id
        )
        EventStoreService.append_event(event)

        return scene
```

**Teste do Event Store**:

```python
# tests/unit/test_event_store_service.py

def test_append_and_retrieve_events(db_session, sample_user):
    # Criar evento
    event = Event(
        aggregate_type='Scene',
        aggregate_id=123,
        event_type='SceneUpdated',
        payload={'changes': {'name': {'old': 'Scene 1', 'new': 'Scene 1A'}}},
        user_id=sample_user.id
    )

    # Salvar
    EventStoreService.append_event(event)

    # Recuperar
    events = EventStoreService.get_events('Scene', 123)

    assert len(events) == 1
    assert events[0].event_type == 'SceneUpdated'
    assert events[0].sequence_number == 1

def test_event_timeline(db_session, sample_user):
    # Criar 3 eventos
    for i in range(3):
        event = Event(
            aggregate_type='Scene',
            aggregate_id=456,
            event_type='SceneUpdated',
            payload={'change': i},
            user_id=sample_user.id
        )
        EventStoreService.append_event(event)

    # Recuperar timeline
    timeline = EventStoreService.get_timeline('Scene', 456)

    assert len(timeline) == 3
    assert timeline[0]['event_type'] == 'SceneUpdated'
```

**Migrations**:

```bash
# Criar migration
flask db migrate -m "Add Event Store tables"

# Aplicar
flask db upgrade

# Verificar
flask db current
```

**Checklist**:

- [ ] Criar migration `xxx_add_event_store.py` com 3 tabelas
- [ ] Aplicar migration (`flask db upgrade`)
- [ ] Criar `app/services/event_store_service.py`
- [ ] Criar `app/models/event.py` (Event, EventSnapshot, EventSubscription)
- [ ] Integrar em `scene_service.py` (método `update()`)
- [ ] Criar 10+ testes em `test_event_store_service.py`
- [ ] Testar event replay manualmente
- [ ] Documentar uso em `docs/EVENT_SOURCING_MVP.md`

**Validação**:

```bash
# Rodar testes
pytest tests/unit/test_event_store_service.py -v

# Criar cena, atualizar, e verificar eventos
curl -X POST /api/v1/scenes -d '{"name": "Test", "project_id": 1}'
# → scene_id = 123

curl -X PATCH /api/v1/scenes/123 -d '{"name": "Test Updated"}'

# Verificar eventos no DB
psql cineprod_dev
SELECT * FROM events WHERE aggregate_type='Scene' AND aggregate_id=123;

# Deve mostrar 1 evento SceneUpdated
```

**Critério de Conclusão**:

✅ Event Store funcionando (append + retrieve)
✅ SceneService registrando eventos em update
✅ 10+ testes passando
✅ Timeline de mudanças exibida na UI (bônus)

---

## 🔍 FASE 5.2: CONFLICT DETECTION (Semanas 5-7) - ATUALIZADO

> **AJUSTE**: Fase 5.2 agora começa na Semana 5 (após Fase 5.1 de 4 semanas).
> Duração: 3 semanas (expandida de 2 semanas devido à dependência de Event Sourcing).

### Objetivo: Implementar Conflict Detection MVP

**Pré-requisito**: Event Sourcing MVP completo (Fase 5.1 Task 1.5) ✅

### Task 2.1: Database Schema (Dia 1)

**Migration**:

```bash
# Criar migration
flask db revision -m "Add conflict detection tables"
```

```python
# migrations/versions/xxxx_add_conflict_detection_tables.py

def upgrade():
    # Conflicts table
    op.create_table('conflicts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conflict_id', sa.String(255), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('severity', sa.String(20), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('entities', sa.JSON(), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('resolution_suggestions', sa.JSON()),
        sa.Column('cost_impact', sa.Numeric(10, 2)),
        sa.Column('detected_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('resolved_at', sa.DateTime()),
        sa.Column('resolution_applied', sa.JSON()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('conflict_id'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE')
    )

    # Indexes
    op.create_index('idx_conflicts_project', 'conflicts', ['project_id'])
    op.create_index('idx_conflicts_type', 'conflicts', ['type'])
    op.create_index('idx_conflicts_severity', 'conflicts', ['severity'])

def downgrade():
    op.drop_table('conflicts')
```

**Aplicar**:

```bash
flask db upgrade
```

---

### Task 2.2: Implementar Engine (Dias 2-5)

**Estrutura**:

```bash
mkdir -p app/intelligence/conflict_detection/detectors
mkdir -p app/intelligence/conflict_detection/resolvers
mkdir -p app/intelligence/conflict_detection/models
```

**Implementação** (seguir arquitetura do `08_INTELLIGENCE_LAYER_ARCHITECTURE.md`):

1. `app/intelligence/conflict_detection/models/conflict.py`
2. `app/intelligence/conflict_detection/detectors/crew_detector.py`
3. `app/intelligence/conflict_detection/detectors/equipment_detector.py`
4. `app/intelligence/conflict_detection/detectors/location_detector.py`
5. `app/intelligence/conflict_detection/detectors/budget_detector.py`
6. `app/intelligence/conflict_detection/resolvers/suggestion_generator.py`
7. `app/intelligence/conflict_detection/engine.py`

**Verificação Incremental**:

```bash
# Após cada detector, rodar testes
pytest tests/unit/intelligence/test_crew_detector.py -v
```

---

### Task 2.3: API Endpoints (Dias 6-7)

**Routes**:

```python
# app/api/v5/conflicts.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.intelligence.conflict_detection.engine import ConflictDetectionEngine
from app.decorators import permission_required

bp = Blueprint('conflicts_v5', __name__, url_prefix='/api/v5/conflicts')

@bp.route('/detect/<int:project_id>', methods=['GET'])
@jwt_required()
@permission_required('view_project')
def detect_conflicts(project_id):
    """
    Detectar conflitos de um projeto

    Query params:
        - start_date (optional): YYYY-MM-DD
        - end_date (optional): YYYY-MM-DD

    Returns:
        {
            'conflicts': [...],
            'summary': {...},
            'recommendations': [...]
        }
    """
    try:
        engine = ConflictDetectionEngine()

        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        date_range = (start_date, end_date) if start_date and end_date else None

        result = engine.detect(project_id, date_range)

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/resolve/<conflict_id>', methods=['POST'])
@jwt_required()
@permission_required('edit_project')
def resolve_conflict(conflict_id):
    """
    Aplicar resolução para conflito

    Body:
        {
            'resolution_index': 0,
            'auto_apply': true
        }
    """
    # Implementar lógica de resolução
    pass

# Registrar blueprint
# app/api/v5/__init__.py
from app.api.v5.conflicts import bp as conflicts_bp

def register_blueprints(app):
    app.register_blueprint(conflicts_bp)
```

**Testes de API**:

```python
# tests/integration/test_conflicts_api.py

def test_detect_conflicts_success(client, auth_headers, sample_project):
    """
    GIVEN um projeto com conflitos
    WHEN GET /api/v5/conflicts/detect/:id
    THEN retorna conflitos detectados
    """
    # Criar scenes com conflito (mesmo crew, mesmo dia)
    # ...

    response = client.get(
        f'/api/v5/conflicts/detect/{sample_project.id}',
        headers=auth_headers
    )

    assert response.status_code == 200
    assert 'conflicts' in response.json
    assert 'summary' in response.json
    assert len(response.json['conflicts']) > 0
```

---

### Task 2.4: Frontend Dashboard (Dias 8-10)

**Template**:

```html
<!-- templates/conflicts_dashboard.html -->

{% extends "base.html" %}

{% block content %}
<div class="conflicts-container">
    <div class="conflicts-header">
        <h1>Conflict Detection Dashboard</h1>
        <button id="scan-conflicts" class="btn-primary">
            Scan for Conflicts
        </button>
    </div>

    <div id="conflicts-summary" class="summary-grid">
        <div class="summary-card critical">
            <div class="card-value" id="critical-count">0</div>
            <div class="card-label">Critical</div>
        </div>
        <div class="summary-card high">
            <div class="card-value" id="high-count">0</div>
            <div class="card-label">High</div>
        </div>
        <div class="summary-card medium">
            <div class="card-value" id="medium-count">0</div>
            <div class="card-label">Medium</div>
        </div>
        <div class="summary-card low">
            <div class="card-value" id="low-count">0</div>
            <div class="card-label">Low</div>
        </div>
    </div>

    <div id="conflicts-list" class="conflicts-list">
        <!-- Conflitos renderizados via JS -->
    </div>
</div>

<script src="{{ url_for('static', filename='js/conflicts.js') }}"></script>
{% endblock %}
```

**JavaScript**:

```javascript
// static/js/conflicts.js

const ConflictsManager = {
    projectId: null,

    init(projectId) {
        this.projectId = projectId;
        this.bindEvents();
        this.scanConflicts();  // Auto-scan on load
    },

    bindEvents() {
        document.getElementById('scan-conflicts').addEventListener('click', () => {
            this.scanConflicts();
        });
    },

    async scanConflicts() {
        try {
            const response = await fetch(`/api/v5/conflicts/detect/${this.projectId}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const data = await response.json();

            this.renderSummary(data.summary);
            this.renderConflicts(data.conflicts);
            this.renderRecommendations(data.recommendations);

        } catch (error) {
            console.error('Error scanning conflicts:', error);
            alert('Failed to scan conflicts');
        }
    },

    renderSummary(summary) {
        document.getElementById('critical-count').textContent = summary.by_severity.critical;
        document.getElementById('high-count').textContent = summary.by_severity.high;
        document.getElementById('medium-count').textContent = summary.by_severity.medium;
        document.getElementById('low-count').textContent = summary.by_severity.low;
    },

    renderConflicts(conflicts) {
        const list = document.getElementById('conflicts-list');
        list.innerHTML = '';

        conflicts.forEach(conflict => {
            const item = this.createConflictCard(conflict);
            list.appendChild(item);
        });
    },

    createConflictCard(conflict) {
        const card = document.createElement('div');
        card.className = `conflict-card severity-${conflict.severity}`;

        card.innerHTML = `
            <div class="conflict-header">
                <span class="conflict-id">${conflict.id}</span>
                <span class="conflict-type">${conflict.type}</span>
                <span class="conflict-severity badge-${conflict.severity}">${conflict.severity}</span>
            </div>
            <div class="conflict-body">
                <p class="conflict-description">${conflict.description}</p>
                <div class="conflict-entities">
                    ${this.renderEntities(conflict.entities)}
                </div>
            </div>
            <div class="conflict-footer">
                <div class="cost-impact">
                    Impact: R$ ${conflict.cost_impact.toLocaleString('pt-BR')}
                </div>
                <div class="suggestions">
                    <strong>Suggestions:</strong>
                    <ul>
                        ${conflict.resolution_suggestions.map(s => `
                            <li>
                                ${s.description}
                                ${s.auto_applicable ? '<button class="btn-sm apply-suggestion">Apply</button>' : ''}
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>
        `;

        return card;
    },

    renderEntities(entities) {
        // Renderizar entities dependendo do tipo
        // ...
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const projectId = window.location.pathname.split('/')[2];  // Extract from URL
    ConflictsManager.init(projectId);
});
```

**CSS**:

```css
/* static/css/conflicts.css */

.conflicts-container {
    padding: 2rem;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}

.summary-card {
    padding: 1.5rem;
    border-radius: 8px;
    text-align: center;
}

.summary-card.critical {
    background: #fee;
    border: 2px solid #f00;
}

.summary-card.high {
    background: #ffeaa7;
    border: 2px solid #fdcb6e;
}

.summary-card.medium {
    background: #dfe6e9;
    border: 2px solid #b2bec3;
}

.summary-card.low {
    background: #e8f8f5;
    border: 2px solid #00b894;
}

.card-value {
    font-size: 3rem;
    font-weight: bold;
}

.conflict-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 1rem;
    padding: 1rem;
}

.conflict-card.severity-critical {
    border-left: 4px solid #f00;
}

.conflict-card.severity-high {
    border-left: 4px solid #ff6b6b;
}

.conflict-card.severity-medium {
    border-left: 4px solid #fdcb6e;
}

.conflict-card.severity-low {
    border-left: 4px solid #00b894;
}
```

---

### Verificação Fase 5.2

**Checklist**:
- [ ] Database migration aplicada
- [ ] Todos os detectores implementados (5)
- [ ] API endpoints funcionando
- [ ] Frontend dashboard renderizando conflitos
- [ ] 40+ testes (unit + integration)
- [ ] Coverage >= 80% no módulo conflict_detection

**Teste End-to-End**:

```bash
# 1. Criar projeto de teste
# 2. Criar 2 scenes no mesmo dia com mesmo crew
# 3. Abrir dashboard de conflitos
# 4. Verificar: 1 conflict crítico aparece
# 5. Click em "Apply" suggestion
# 6. Verificar: conflict resolvido
```

---

## ⚙️ FASE 5.3: SCHEDULE OPTIMIZER (Semanas 5-7)

### Objetivo: Implementar Schedule Optimizer com algoritmo Greedy (MVP)

### Task 3.1: Database Schema (Dia 1)

**Migration**:

```python
# migrations/versions/xxxx_add_optimized_schedules.py

def upgrade():
    op.create_table('optimized_schedules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('algorithm', sa.String(50), nullable=False),
        sa.Column('constraints', sa.JSON()),
        sa.Column('schedule_data', sa.JSON(), nullable=False),
        sa.Column('metrics', sa.JSON()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('applied_at', sa.DateTime()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE')
    )
```

---

### Task 3.2: Implementar Greedy Optimizer (Dias 2-5)

(Implementação conforme `08_INTELLIGENCE_LAYER_ARCHITECTURE.md`)

---

### Task 3.3: API & Frontend (Dias 6-15)

(Similar à Fase 5.2)

---

## 📊 FASE 5.4: PREDICTIVE ANALYTICS (Semanas 8-9)

(Implementação conforme `08_INTELLIGENCE_LAYER_ARCHITECTURE.md`)

---

## ✅ TESTING & VALIDATION (Semana 10)

### Integration Tests

```bash
# Rodar TODOS os testes
pytest tests/ -v --cov=app --cov-report=html

# Target:
# - 0 failing
# - 80%+ coverage
# - <5 min execution time
```

### Load Testing

```bash
# Usar Locust
locust -f tests/performance/locustfile.py --users 100 --spawn-rate 10
```

---

## 🚀 DEPLOYMENT STRATEGY

### Blue-Green Deployment

1. Deploy v3.0 para "green" (offline)
2. Smoke tests em green
3. Rotear 10% tráfego para green
4. Monitorar 1h
5. Rotear 100% tráfego
6. Desligar "blue"

---

## ↩️ ROLLBACK PLAN

Se algo der errado:

```bash
# 1. Rotear tráfego de volta para blue
nginx -s reload

# 2. Database rollback
flask db downgrade

# 3. Git revert
git revert HEAD~10

# Downtime estimado: <2 minutos
```

---

## 📋 POST-UPGRADE CHECKLIST

- [ ] Testes passando (100%)
- [ ] Coverage >= 80%
- [ ] Conflict Detection funcionando
- [ ] Schedule Optimizer funcionando
- [ ] Predictive Analytics funcionando
- [ ] Performance OK (APIs <200ms)
- [ ] Sem erros em logs
- [ ] Usuários validaram (UAT)
- [ ] Documentação atualizada
- [ ] Changelog publicado

---

**DIGIMUNDO PRESENTE 🥷**
