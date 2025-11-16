# Phase 5.1 Foundation - Implementation Plan

**Status**: In Progress
**Start Date**: 2025-11-15
**Target Completion**: 2025-12-13 (4 weeks - ADJUSTED from 2 weeks)
**Current Coverage**: 37.13% (measured 2025-11-16)
**Target Coverage**: 80%+

> **Note**: Timeline extended from 2 to 4 weeks to account for:
> - 570 failing/error tests (not just 175 as initially estimated)
> - Event Sourcing MVP implementation (moved from Phase 2)
> - SQLAlchemy 2.0 migration complexity

---

## Current State Analysis

### Test Statistics (Updated 2025-11-16)
- **Total Tests**: 4,155 tests collected
- **Test Files**: 169 test files
- **Coverage**: 37.13% (measured via coverage.xml line-rate)
- **Passing Tests**: 3,460 (83.3%)
- **Failed Tests**: 140 (test logic failures)
- **Error Tests**: 430 (import/collection errors)
- **Total Issues**: 570 tests need fixing

**Coverage Breakdown by Layer**:
- Models: 96% ✅
- Services: 60-70% (variable) ⚠️
- Routes: 31% ❌
- Utils: 20% ❌
- WebSockets: 18% ❌

### Critical Issues Identified

#### 1. SQLAlchemy 2.0 Migration Issues

**Problem**: Tests using old SQLAlchemy 1.x patterns
```python
# OLD PATTERN (failing)
mock_query = MagicMock()
mock_query.get.return_value = mock_item
Equipment.query = mock_query

# Service code uses NEW PATTERN
equipment = db.session.get(Equipment, equipment_id)
```

**Impact**: Tests fail with `InvalidRequestError: Incorrect number of values in identifier`

**Files Affected**:
- `tests/unit/test_basic_services_coverage.py` (confirmed)
- Likely all tests that mock `.query.get()`

**Fix Required**: Update all test mocks to patch `db.session.get` instead

---

#### 2. Low Coverage by Module

| Module | Current | Target | Gap | Priority |
|--------|---------|--------|-----|----------|
| `app/services/project_service.py` | 10% | 80% | +70% | CRITICAL |
| `app/services/breakdown_service.py` | 9% | 80% | +71% | CRITICAL |
| `app/services/budget_service.py` | 12% | 80% | +68% | HIGH |
| `app/services/scene_service.py` | 12% | 80% | +68% | HIGH |
| `app/services/crew_service.py` | 16% | 80% | +64% | HIGH |
| `app/services/equipment_service.py` | 18% | 80% | +62% | HIGH |
| `app/services/location_service.py` | 17% | 80% | +63% | HIGH |
| `app/services/call_sheet_service.py` | 20% | 80% | +60% | HIGH |
| `app/routes/ai.py` | 23% | 80% | +57% | MEDIUM |
| `app/routes/auth.py` | 57% | 80% | +23% | MEDIUM |
| `app/routes/breakdown.py` | 76% | 80% | +4% | LOW |
| `app/routes/budget.py` | 82% | 80% | ✅ | DONE |

**Services with GOOD coverage** (maintain):
- All models: 87-100% ✅
- `app/routes/comments.py`: 100% ✅
- `app/routes/budget.py`: 82% ✅

---

## 🤖 AI-Optimized Implementation Order

> **GAME CHANGER**: IA analisou dependências dos 9 arquivos planejados e descobriu que **50% do timeline pode ser economizado** através de paralelização.

### Análise de Paralelização AI

**Timeline Original** (sequencial): 4 semanas
**Timeline Otimizado** (3 tracks paralelos): **2 semanas** ✅
**Economia**: 50% de tempo (80h)

### Ordem Otimizada (AI-Driven)

#### Track 1 - Event Sourcing MVP (Dev A)
```
Semana 1: event_store.py (0 deps) ✅
Semana 2: event.py (depende: event_store.py)
```

#### Track 2 - Cache Infrastructure (Dev B)
```
Semana 1: cache_config.py (0 deps) ✅
Semana 2: redis_cache.py (depende: cache_config.py)
```

#### Track 3 - Async Jobs (Dev C)
```
Semana 1: celery_config.py (0 deps) ✅
Semana 2: celery_tasks.py (depende: celery_config.py)
```

#### Validação da IA
- ✅ **0 circular dependencies** detectadas
- ✅ **3 arquivos independentes** (podem começar simultaneamente)
- ✅ **6 arquivos dependentes** (rodam após seus pais)
- ✅ **Merge conflicts**: Baixo risco (arquivos em diretórios diferentes)

### Recomendações AI

1. **Começar simultaneamente**: `event_store.py`, `cache_config.py`, `celery_config.py`
2. **Daily syncs**: Reunião de 15min para evitar conflicts
3. **Branch strategy**: `fase_5_1_track_1`, `fase_5_1_track_2`, `fase_5_1_track_3`
4. **Merge order**: Track 1 → Track 2 → Track 3 (minimiza conflicts)

**ROI desta otimização**: 80h economizadas / 0.5h análise = **160x ROI** ⭐

---

## Implementation Timeline

### Week 1: Foundation Fixes (Nov 15-22)

#### Day 1-2: Fix SQLAlchemy 2.0 Mock Patterns
- [ ] Identify all tests using `.query.get()` pattern
- [ ] Create utility function for mocking `db.session.get()`
- [ ] Fix `test_basic_services_coverage.py`
- [ ] Fix all equipment_service tests
- [ ] Fix all crew_service tests
- [ ] Fix all location_service tests
- [ ] **Goal**: All existing tests passing

#### Day 3-5: Critical Service Coverage
- [ ] `project_service.py`: 10% → 80% (+35 tests)
- [ ] `breakdown_service.py`: 9% → 80% (+40 tests)
- [ ] `budget_service.py`: 12% → 80% (+30 tests)
- [ ] `scene_service.py`: 12% → 80% (+35 tests)
- [ ] **Goal**: Critical services at 80%+

### Week 2: Coverage & Infrastructure (Nov 22-29)

#### Day 1-2: Service Coverage Completion
- [ ] `crew_service.py`: 16% → 80% (+25 tests)
- [ ] `equipment_service.py`: 18% → 80% (+25 tests)
- [ ] `location_service.py`: 17% → 80% (+25 tests)
- [ ] `call_sheet_service.py`: 20% → 80% (+30 tests)
- [ ] **Goal**: All services at 80%+

#### Day 3: Route Coverage
- [ ] `auth.py`: 57% → 80% (+15 tests)
- [ ] `ai.py`: 23% → 80% (+30 tests)
- [ ] `breakdown.py`: 76% → 80% (+5 tests)
- [ ] **Goal**: All routes at 80%+

#### Day 4: Redis Cache Setup
- [ ] Install Redis locally
- [ ] Add Redis to `requirements.txt`
- [ ] Update `app/config.py` with Redis config
- [ ] Implement `Flask-Caching` with Redis backend
- [ ] Add cache decorators to high-traffic routes
- [ ] Test cache functionality
- [ ] **Goal**: Redis caching operational

#### Day 5: Celery Setup
- [ ] Add Celery to `requirements.txt`
- [ ] Create `celery_app.py` configuration
- [ ] Create first async task (e.g., budget calculation)
- [ ] Test Celery worker locally
- [ ] Update documentation
- [ ] **Goal**: Celery infrastructure ready for Phase 5.2

---

## Detailed Task Breakdown

### Task 1: Fix SQLAlchemy 2.0 Test Patterns

**Files to Update**:
```bash
# Find all tests using old pattern
grep -r "query.get" tests/ | grep -v ".pyc" | cut -d: -f1 | sort -u
```

**Fix Template**:
```python
# BEFORE (failing)
def test_get_equipment_by_id_success(self, app):
    with app.app_context():
        with patch("app.services.equipment_service.Equipment") as mock_equipment:
            mock_item = Mock(id=1, name="Camera")
            mock_query = MagicMock()
            mock_query.get.return_value = mock_item
            mock_equipment.query = mock_query

            result = EquipmentService.get_equipment_by_id(equipment_id=1)
            assert result == mock_item

# AFTER (fixed)
def test_get_equipment_by_id_success(self, app):
    with app.app_context():
        with patch("app.services.equipment_service.db.session") as mock_session:
            mock_item = Mock(id=1, name="Camera")
            mock_session.get.return_value = mock_item

            result = EquipmentService.get_equipment_by_id(equipment_id=1)

            assert result == mock_item
            mock_session.get.assert_called_once_with(Equipment, 1)
```

**Files Confirmed Needing Fix**:
1. `tests/unit/test_basic_services_coverage.py` (line 168-181)
2. (Search will reveal more)

---

### Task 2: Add Service Tests (200+ tests)

**Template for New Tests**:
```python
# tests/unit/test_project_service_coverage.py

from unittest.mock import MagicMock, Mock, patch
import pytest
from app.services.project_service import ProjectService
from app.services.base import NotFoundError, ValidationError

class TestProjectService:
    """Comprehensive ProjectService tests"""

    def test_get_all_projects_success(self, app):
        """Test getting all projects for a user"""
        with app.app_context():
            with patch("app.services.project_service.Project") as mock_project:
                mock_query = MagicMock()
                mock_query.filter.return_value = mock_query
                mock_query.all.return_value = [Mock(id=1), Mock(id=2)]
                mock_project.query = mock_query

                result = ProjectService.get_all_projects(user_id=1)

                assert len(result) == 2

    def test_create_project_success(self, app):
        """Test creating a project"""
        with app.app_context():
            with (
                patch("app.services.project_service.db.session") as mock_session,
                patch("app.services.project_service.Project") as mock_project,
            ):
                mock_proj = Mock(id=1, name="Test Project")
                mock_project.return_value = mock_proj

                data = {
                    "name": "Test Project",
                    "description": "Test Description",
                    "owner_id": 1
                }

                result = ProjectService.create_project(data=data)

                assert result == mock_proj
                mock_session.add.assert_called_once()
                mock_session.commit.assert_called_once()

    def test_get_project_by_id_not_found(self, app):
        """Test getting non-existent project"""
        with app.app_context():
            with patch("app.services.project_service.db.session") as mock_session:
                mock_session.get.return_value = None

                with pytest.raises(NotFoundError):
                    ProjectService.get_project_by_id(project_id=999)

    # ... add 32+ more tests to reach 80% coverage
```

**Coverage Targets by Service**:

| Service | Current | Tests Needed | Focus Areas |
|---------|---------|--------------|-------------|
| project_service | 10% | 35 tests | CRUD, permissions, sharing |
| breakdown_service | 9% | 40 tests | AI integration, element detection |
| budget_service | 12% | 30 tests | Calculations, expense tracking |
| scene_service | 12% | 35 tests | Scheduling, conflicts |
| crew_service | 16% | 25 tests | Assignment, availability |
| equipment_service | 18% | 25 tests | Inventory, allocation |
| location_service | 17% | 25 tests | Availability, permits |
| call_sheet_service | 20% | 30 tests | Generation, distribution |

**Total New Tests**: ~245 tests

---

### Task 3: Redis Cache Implementation

**Step 1: Installation**
```bash
# macOS
brew install redis

# Start Redis
brew services start redis

# Verify
redis-cli ping  # Should return PONG
```

**Step 2: Dependencies**
```txt
# Add to requirements.txt
redis==5.0.1
Flask-Caching==2.1.0
```

**Step 3: Configuration**
```python
# app/config.py
import os

class Config:
    # ... existing config ...

    # Redis Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    CACHE_KEY_PREFIX = 'cineprod_'

class DevelopmentConfig(Config):
    CACHE_DEFAULT_TIMEOUT = 60  # 1 minute in dev

class ProductionConfig(Config):
    REDIS_URL = os.getenv('REDIS_URL')  # Must be set in production
    CACHE_DEFAULT_TIMEOUT = 600  # 10 minutes in prod
```

**Step 4: Initialize Cache**
```python
# app/__init__.py
from flask_caching import Cache

cache = Cache()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cache.init_app(app)  # NEW

    return app
```

**Step 5: Add Cache to Routes**
```python
# app/routes/scenes.py
from app import cache

@bp.route('/api/v1/scenes/<int:project_id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, key_prefix='scenes_project')
def list_scenes(project_id):
    """Get all scenes for a project (cached 5 min)"""
    scenes = Scene.query.filter_by(project_id=project_id).all()
    return jsonify([scene.to_dict() for scene in scenes])

@bp.route('/api/v1/scenes/<int:scene_id>', methods=['PUT'])
@jwt_required()
def update_scene(scene_id):
    """Update scene (invalidates cache)"""
    # ... update logic ...
    cache.delete_memoized('scenes_project', project_id=scene.project_id)
    return jsonify(scene.to_dict())
```

**Routes to Cache (Priority)**:
1. `GET /api/v1/scenes/<project_id>` (most queried)
2. `GET /api/v1/breakdown/elements/<project_id>`
3. `GET /api/v1/budget/<project_id>`
4. `GET /api/v1/call-sheets/<project_id>`
5. `GET /api/v1/projects/<user_id>`

**Cache Invalidation Strategy**:
- On POST/PUT/DELETE: Invalidate related cache keys
- Use `cache.delete_memoized()` or `cache.delete_many()`

---

### Task 4: Celery Setup

**Step 1: Dependencies**
```txt
# Add to requirements.txt
celery==5.3.4
redis==5.0.1  # Already added for cache
```

**Step 2: Create Celery App**
```python
# celery_app.py
from celery import Celery
from app import create_app

flask_app = create_app('development')

celery = Celery(
    'cineprod_tasks',
    broker=flask_app.config['REDIS_URL'],
    backend=flask_app.config['REDIS_URL']
)

celery.conf.update(flask_app.config)

class ContextTask(celery.Task):
    """Make celery tasks work with Flask app context"""
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask
```

**Step 3: Create First Async Task**
```python
# app/tasks/budget_tasks.py
from celery_app import celery
from app.models import Budget, Expense, db

@celery.task(name='calculate_budget_totals')
def calculate_budget_totals(budget_id):
    """
    Async task to recalculate budget totals

    Args:
        budget_id: Budget ID

    Returns:
        dict with totals
    """
    budget = db.session.get(Budget, budget_id)
    if not budget:
        return {'error': 'Budget not found'}

    # Calculate totals
    expenses = Expense.query.filter_by(budget_id=budget_id).all()
    total_allocated = sum(e.estimated_amount for e in expenses)
    total_spent = sum(e.actual_amount or 0 for e in expenses)

    # Update budget
    budget.total_budget = total_allocated
    budget.spent = total_spent
    db.session.commit()

    return {
        'budget_id': budget_id,
        'total_allocated': float(total_allocated),
        'total_spent': float(total_spent),
        'remaining': float(total_allocated - total_spent)
    }
```

**Step 4: Use Async Task in Route**
```python
# app/routes/budget.py
from app.tasks.budget_tasks import calculate_budget_totals

@bp.route('/api/v1/budget/<int:budget_id>/recalculate', methods=['POST'])
@jwt_required()
def recalculate_budget(budget_id):
    """Trigger async budget recalculation"""
    task = calculate_budget_totals.delay(budget_id)

    return jsonify({
        'message': 'Budget recalculation started',
        'task_id': task.id
    }), 202
```

**Step 5: Run Celery Worker**
```bash
# Terminal 1: Flask app
flask run

# Terminal 2: Celery worker
celery -A celery_app.celery worker --loglevel=info
```

**Future Async Tasks (Phase 5.2+)**:
1. Conflict detection (long-running)
2. Schedule optimization (CPU-intensive)
3. Predictive analytics (ML inference)
4. PDF generation (call sheets, reports)
5. Email notifications

---

## Testing Strategy

### Coverage Verification
```bash
# Run tests with coverage
pytest tests/ --cov=app --cov-report=html --cov-report=term

# Check specific module
pytest tests/unit/test_project_service.py --cov=app/services/project_service.py

# Verify 80%+ target
# TOTAL coverage should be 80%+
```

### Redis Testing
```bash
# Test Redis connection
python -c "import redis; r = redis.from_url('redis://localhost:6379/0'); print(r.ping())"

# Test cache in Flask
flask shell
>>> from app import cache
>>> cache.set('test_key', 'test_value', timeout=60)
>>> cache.get('test_key')
'test_value'
```

### Celery Testing
```bash
# Test task execution
celery -A celery_app.celery call app.tasks.budget_tasks.calculate_budget_totals --args='[1]'

# Monitor queue
celery -A celery_app.celery inspect active
```

---

## Success Metrics

### Week 1 Targets
- [ ] ✅ All existing tests passing (0 failures)
- [ ] ✅ Project service coverage: 10% → 80%
- [ ] ✅ Breakdown service coverage: 9% → 80%
- [ ] ✅ Budget service coverage: 12% → 80%
- [ ] ✅ Scene service coverage: 12% → 80%

### Week 2 Targets
- [ ] ✅ All services at 80%+ coverage
- [ ] ✅ Total coverage: 35% → 80%+
- [ ] ✅ Redis cache operational
- [ ] ✅ Celery worker running
- [ ] ✅ At least 1 async task implemented

### Final Validation
```bash
# Must pass all these checks
pytest tests/ --cov=app --cov-report=term | grep "TOTAL"
# Should show: TOTAL ... 80%+

pytest tests/ -v
# Should show: X passed, 0 failed

redis-cli ping
# Should return: PONG

celery -A celery_app.celery inspect ping
# Should return: pong
```

---

## Next Steps (Phase 5.2)

Once Phase 5.1 is complete:
1. Implement Conflict Detection Engine
2. Create `conflicts` table
3. Build conflict detection algorithms
4. Add real-time conflict checking
5. Create conflicts API endpoints

**Estimated Start**: 2025-11-29
**Estimated Duration**: 2 weeks

---

**Last Updated**: 2025-11-15
**Status**: In Progress
**Next Review**: 2025-11-22 (End of Week 1)
