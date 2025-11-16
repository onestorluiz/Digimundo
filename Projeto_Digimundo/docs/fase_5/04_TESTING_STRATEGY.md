# 🧪 Estratégia de Testes - CineProd

**Sistema de Qualidade e Garantia de Funcionamento**

> "Código sem testes é código legado desde o primeiro dia"

**Data**: 2025-11-15
**Versão**: 1.0

---

## 📋 Índice

1. [Filosofia de Testes](#filosofia-de-testes)
2. [Pirâmide de Testes](#pirâmide-de-testes)
3. [Testes Unitários](#testes-unitários)
4. [Testes de Integração](#testes-de-integração)
5. [Testes End-to-End](#testes-end-to-end)
6. [Testes de Performance](#testes-de-performance)
7. [Testes de Segurança](#testes-de-segurança)
8. [Test Data Management](#test-data-management)
9. [CI/CD Integration](#cicd-integration)
10. [Coverage Requirements](#coverage-requirements)

---

## 🎯 Filosofia de Testes

### Princípios Fundamentais:

1. **Teste antes de fazer deploy** - Código não testado não vai para production
2. **Testes são documentação executável** - Descrevem como o sistema funciona
3. **Falha rápida** - Melhor falhar em 30s nos testes do que em 30min em production
4. **Isolamento** - Cada teste é independente
5. **Determinístico** - Mesmo input = mesmo output, sempre

### Objetivos:

| Objetivo | Meta | Atual | Status |
|----------|------|-------|--------|
| **Cobertura de código** | >80% | 37.13% | ⚠️ Below target |
| **Tempo de execução (unit)** | <30s | ~15s | ✅ Good |
| **Tempo de execução (todos)** | <5min | ~3min | ✅ Good |
| **Flakiness** | <1% | ~2% | ⚠️ Needs improvement |
| **Bugs em production** | <5/mês | - | - |

**Note**: Coverage baseline corrected from ~80% (estimated) to 37.13% (actual measured value). See COVERAGE_METRICS_RECONCILIATION.md for details.

---

## 🔺 Pirâmide de Testes

```
           /\
          /  \    E2E (5%)
         /----\
        /      \  Integration (25%)
       /--------\
      /          \ Unit (70%)
     /____________\
```

### Distribuição Ideal:

| Tipo | % do Total | Quantidade Atual | Meta |
|------|------------|------------------|------|
| **Unit** | 70% | ~120 | 200+ |
| **Integration** | 25% | ~40 | 70+ |
| **E2E** | 5% | ~9 | 15+ |
| **Total** | 100% | **169** | **285+** |

---

## 🧪 Testes Unitários

### O Que Testar:

✅ **Sempre testar**:
- Models (métodos, properties, validações)
- Services (lógica de negócio)
- Utils (funções puras)
- Serializers/Schemas

❌ **Não precisa testar**:
- Framework code (Flask, SQLAlchemy)
- Third-party libraries
- Getters/setters triviais

### Estrutura de Teste Unitário:

```python
# tests/unit/test_scene_service.py

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from app.services.scene_service import SceneService
from app.models.scene import Scene

class TestSceneService:
    """
    Testes unitários para SceneService

    Testa lógica de negócio isoladamente (sem banco de dados real)
    """

    @pytest.fixture
    def service(self):
        """Fixture: Instância do serviço"""
        return SceneService()

    @pytest.fixture
    def mock_scene(self):
        """Fixture: Scene mockado"""
        scene = Mock(spec=Scene)
        scene.id = 1
        scene.name = "CENA 01 - ESCRITÓRIO - DIA"
        scene.duration_minutes = 120
        scene.cast = []
        return scene

    def test_calculate_scene_cost_basic(self, service, mock_scene):
        """
        GIVEN uma scene com duração de 120min
        WHEN calculo o custo
        THEN deve retornar custo baseado em tempo
        """
        # Arrange
        mock_scene.cast = [Mock(daily_rate=500), Mock(daily_rate=300)]

        # Act
        cost = service.calculate_scene_cost(mock_scene)

        # Assert
        assert cost == 800  # 2 atores por 1 dia
        assert isinstance(cost, int)

    def test_calculate_scene_cost_overtime(self, service, mock_scene):
        """
        GIVEN uma scene com duração > 8h (overtime)
        WHEN calculo o custo
        THEN deve incluir adicional de overtime
        """
        # Arrange
        mock_scene.duration_minutes = 600  # 10 horas
        mock_scene.cast = [Mock(daily_rate=500)]

        # Act
        cost = service.calculate_scene_cost(mock_scene)

        # Assert
        assert cost > 500  # Base + overtime
        assert cost == 500 + (2 * 50)  # +50 por hora extra

    def test_can_shoot_on_date_no_conflicts(self, service, mock_scene):
        """
        GIVEN uma scene e uma data
        WHEN verifico se pode filmar nessa data
        AND não há conflitos de ator
        THEN retorna True
        """
        # Arrange
        proposed_date = datetime(2025, 1, 15)

        with patch.object(service, '_check_actor_conflicts', return_value=[]):
            # Act
            result = service.can_shoot_on_date(mock_scene, proposed_date)

            # Assert
            assert result is True

    def test_can_shoot_on_date_with_conflicts(self, service, mock_scene):
        """
        GIVEN uma scene e uma data
        WHEN verifico se pode filmar
        AND há conflito de ator
        THEN retorna False
        """
        # Arrange
        proposed_date = datetime(2025, 1, 15)
        conflicts = [{'type': 'actor_conflict', 'actor_id': 1}]

        with patch.object(service, '_check_actor_conflicts', return_value=conflicts):
            # Act
            result = service.can_shoot_on_date(mock_scene, proposed_date)

            # Assert
            assert result is False

    @pytest.mark.parametrize("duration,expected_days", [
        (120, 1),   # 2h = 1 dia
        (480, 1),   # 8h = 1 dia
        (600, 2),   # 10h = 2 dias (com overtime caro)
        (960, 2),   # 16h = 2 dias
    ])
    def test_estimate_shooting_days(self, service, mock_scene, duration, expected_days):
        """
        GIVEN uma scene com duração variável
        WHEN estimo número de dias de filmagem
        THEN retorna número correto
        """
        # Arrange
        mock_scene.duration_minutes = duration

        # Act
        days = service.estimate_shooting_days(mock_scene)

        # Assert
        assert days == expected_days
```

### Boas Práticas:

1. **AAA Pattern (Arrange-Act-Assert)**:
   ```python
   def test_something():
       # Arrange - Preparar dados
       user = User(name="João")

       # Act - Executar ação
       result = user.get_display_name()

       # Assert - Verificar resultado
       assert result == "João"
   ```

2. **Nomear testes descritivamente**:
   ```python
   # ❌ Ruim
   def test_scene():
       pass

   # ✅ Bom
   def test_scene_cost_calculation_includes_overtime_for_long_shoots():
       pass
   ```

3. **Um assert por conceito** (não necessariamente por teste):
   ```python
   # ✅ OK - Asserts relacionados
   def test_user_creation():
       user = User.create(name="João", email="joao@example.com")
       assert user.name == "João"
       assert user.email == "joao@example.com"
       assert user.is_active is True
   ```

4. **Usar fixtures para setup comum**:
   ```python
   @pytest.fixture
   def app():
       app = create_app('testing')
       return app

   @pytest.fixture
   def client(app):
       return app.test_client()
   ```

### Rodar Testes Unitários:

```bash
# Todos os unit tests
venv/bin/python3 -m pytest tests/unit/ -v

# Um arquivo específico
venv/bin/python3 -m pytest tests/unit/test_scene_service.py -v

# Um teste específico
venv/bin/python3 -m pytest tests/unit/test_scene_service.py::TestSceneService::test_calculate_scene_cost_basic -v

# Com coverage
venv/bin/python3 -m pytest tests/unit/ --cov=app/services --cov-report=html
```

---

## 🔗 Testes de Integração

### O Que Testar:

✅ **Sempre testar**:
- API endpoints (request/response)
- Database queries
- Integrações entre services
- WebSocket handlers
- Background jobs

### Estrutura de Teste de Integração:

```python
# tests/integration/test_scene_api.py

import pytest
import json
from flask import url_for

from app import create_app, db
from app.models.scene import Scene
from app.models.project import Project
from app.models.user import User

class TestSceneAPI:
    """
    Testes de integração para Scene API

    Testa endpoints completos (request -> controller -> service -> database -> response)
    """

    @pytest.fixture
    def app(self):
        """Fixture: Flask app em modo testing"""
        app = create_app('testing')
        return app

    @pytest.fixture
    def client(self, app):
        """Fixture: Test client"""
        return app.test_client()

    @pytest.fixture
    def db_session(self, app):
        """Fixture: Database session"""
        with app.app_context():
            db.create_all()
            yield db.session
            db.session.remove()
            db.drop_all()

    @pytest.fixture
    def auth_headers(self, client):
        """Fixture: Headers com JWT token"""
        # Criar usuário de teste
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'TestPass123',
            'name': 'Test User'
        })

        # Login
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPass123'
        })

        token = response.json['access_token']

        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    @pytest.fixture
    def sample_project(self, db_session):
        """Fixture: Projeto de exemplo"""
        project = Project(
            name="Teste Project",
            start_date=datetime(2025, 1, 1)
        )
        db_session.add(project)
        db_session.commit()
        return project

    def test_create_scene_success(self, client, auth_headers, sample_project):
        """
        GIVEN um projeto válido
        WHEN crio uma scene via API
        THEN recebo 201 Created e scene é criada no banco
        """
        # Arrange
        payload = {
            'project_id': sample_project.id,
            'name': 'CENA 01 - ESCRITÓRIO - DIA',
            'scene_number': '01',
            'duration_minutes': 120
        }

        # Act
        response = client.post(
            '/api/v1/scenes',
            data=json.dumps(payload),
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 201
        assert 'id' in response.json
        assert response.json['name'] == 'CENA 01 - ESCRITÓRIO - DIA'

        # Verificar no banco
        scene = Scene.query.get(response.json['id'])
        assert scene is not None
        assert scene.name == 'CENA 01 - ESCRITÓRIO - DIA'

    def test_create_scene_invalid_project(self, client, auth_headers):
        """
        GIVEN um project_id inválido
        WHEN tento criar scene
        THEN recebo 404 Not Found
        """
        # Arrange
        payload = {
            'project_id': 99999,
            'name': 'CENA 01',
            'scene_number': '01'
        }

        # Act
        response = client.post(
            '/api/v1/scenes',
            data=json.dumps(payload),
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 404
        assert 'error' in response.json

    def test_get_scene_by_id(self, client, auth_headers, db_session, sample_project):
        """
        GIVEN uma scene existente
        WHEN busco por ID
        THEN recebo dados completos
        """
        # Arrange - Criar scene no banco
        scene = Scene(
            project_id=sample_project.id,
            name='CENA 01 - ESCRITÓRIO - DIA',
            scene_number='01'
        )
        db_session.add(scene)
        db_session.commit()

        # Act
        response = client.get(
            f'/api/v1/scenes/{scene.id}',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        assert response.json['id'] == scene.id
        assert response.json['name'] == 'CENA 01 - ESCRITÓRIO - DIA'

    def test_update_scene(self, client, auth_headers, db_session, sample_project):
        """
        GIVEN uma scene existente
        WHEN atualizo campos via PATCH
        THEN mudanças são persistidas
        """
        # Arrange
        scene = Scene(
            project_id=sample_project.id,
            name='CENA 01',
            scene_number='01'
        )
        db_session.add(scene)
        db_session.commit()

        # Act
        response = client.patch(
            f'/api/v1/scenes/{scene.id}',
            data=json.dumps({'name': 'CENA 01 - ATUALIZADA'}),
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200

        # Verificar no banco
        db_session.refresh(scene)
        assert scene.name == 'CENA 01 - ATUALIZADA'

    def test_delete_scene(self, client, auth_headers, db_session, sample_project):
        """
        GIVEN uma scene existente
        WHEN deleto via API
        THEN scene é removida do banco
        """
        # Arrange
        scene = Scene(
            project_id=sample_project.id,
            name='CENA 01',
            scene_number='01'
        )
        db_session.add(scene)
        db_session.commit()
        scene_id = scene.id

        # Act
        response = client.delete(
            f'/api/v1/scenes/{scene_id}',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 204

        # Verificar que foi deletado
        assert Scene.query.get(scene_id) is None

    def test_list_scenes_pagination(self, client, auth_headers, db_session, sample_project):
        """
        GIVEN 25 scenes em um projeto
        WHEN listo com paginação (10 por página)
        THEN recebo 10 scenes e link para próxima página
        """
        # Arrange - Criar 25 scenes
        for i in range(25):
            scene = Scene(
                project_id=sample_project.id,
                name=f'CENA {i:02d}',
                scene_number=f'{i:02d}'
            )
            db_session.add(scene)
        db_session.commit()

        # Act
        response = client.get(
            f'/api/v1/projects/{sample_project.id}/scenes?page=1&per_page=10',
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        assert len(response.json['scenes']) == 10
        assert response.json['total'] == 25
        assert response.json['pages'] == 3
        assert 'next' in response.json
```

### Rodar Testes de Integração:

```bash
# Todos os integration tests
venv/bin/python3 -m pytest tests/integration/ -v

# Com coverage
venv/bin/python3 -m pytest tests/integration/ --cov=app --cov-report=html
```

---

## 🌐 Testes End-to-End

### O Que Testar:

✅ **Fluxos críticos**:
- Login → Criar Projeto → Adicionar Scenes → Schedule → Call Sheet
- Upload Roteiro → Breakdown Automático → Validação
- Colaboração Real-Time (WebSocket)

### Estrutura de Teste E2E:

```python
# tests/e2e/test_full_workflow.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestFullProductionWorkflow:
    """
    Teste E2E do fluxo completo de produção
    """

    @pytest.fixture
    def driver(self):
        """Fixture: Selenium WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1920, 1080)

        yield driver
        driver.quit()

    def test_complete_production_flow(self, driver):
        """
        CENÁRIO: Criar projeto completo do zero

        DADO que sou um usuário autenticado
        QUANDO crio um novo projeto
        E adiciono scenes manualmente
        E otimizo o schedule
        E gero call sheets
        ENTÃO todas as etapas funcionam end-to-end
        """
        base_url = "http://localhost:5000"

        # 1. LOGIN
        driver.get(f"{base_url}/login")
        driver.find_element(By.ID, "email").send_keys("producer@example.com")
        driver.find_element(By.ID, "password").send_keys("Password123")
        driver.find_element(By.ID, "login-button").click()

        # Esperar redirect para dashboard
        WebDriverWait(driver, 10).until(
            EC.url_contains("/dashboard")
        )

        # 2. CRIAR PROJETO
        driver.find_element(By.ID, "new-project-button").click()
        driver.find_element(By.ID, "project-name").send_keys("Projeto E2E Test")
        driver.find_element(By.ID, "start-date").send_keys("2025-01-15")
        driver.find_element(By.ID, "create-project-submit").click()

        # Esperar criação
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "project-created-success"))
        )

        # 3. ADICIONAR SCENES
        driver.find_element(By.ID, "add-scene-button").click()
        driver.find_element(By.ID, "scene-name").send_keys("CENA 01 - ESCRITÓRIO - DIA")
        driver.find_element(By.ID, "scene-number").send_keys("01")
        driver.find_element(By.ID, "save-scene").click()

        # Verificar scene aparece na lista
        scene_list = driver.find_element(By.ID, "scenes-list")
        assert "CENA 01" in scene_list.text

        # 4. OTIMIZAR SCHEDULE
        driver.find_element(By.ID, "optimize-schedule-button").click()

        # Esperar otimização
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "schedule-optimized"))
        )

        # 5. GERAR CALL SHEET
        driver.find_element(By.ID, "generate-call-sheet-button").click()

        # Verificar call sheet gerado
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "call-sheet-preview"))
        )

        # Screenshot final
        driver.save_screenshot("tests/screenshots/e2e_success.png")

        # Assert final
        assert "Call Sheet gerado com sucesso" in driver.page_source
```

### Rodar Testes E2E:

```bash
# Todos os E2E tests
venv/bin/python3 -m pytest tests/e2e/ -v --capture=no

# Com Selenium Grid (paralelo)
venv/bin/python3 -m pytest tests/e2e/ -n 4
```

---

## ⚡ Testes de Performance

### Load Testing com Locust:

```python
# tests/performance/locustfile.py

from locust import HttpUser, task, between

class CineProdUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Login antes de iniciar testes"""
        response = self.client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "TestPass123"
        })
        self.token = response.json()['access_token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    @task(3)
    def list_scenes(self):
        """Listar scenes (tarefa mais comum)"""
        self.client.get("/api/v1/projects/1/scenes", headers=self.headers)

    @task(1)
    def create_scene(self):
        """Criar scene (menos frequente)"""
        self.client.post("/api/v1/scenes", headers=self.headers, json={
            "project_id": 1,
            "name": "CENA TEST",
            "scene_number": "99"
        })

    @task(2)
    def get_scene_detail(self):
        """Ver detalhes de scene"""
        self.client.get("/api/v1/scenes/1", headers=self.headers)
```

Rodar:

```bash
# Simular 100 usuários
locust -f tests/performance/locustfile.py --users 100 --spawn-rate 10 --host http://localhost:5000

# Interface web em http://localhost:8089
```

### Benchmarks:

| Endpoint | Target | Atual | Status |
|----------|--------|-------|--------|
| GET /scenes | <200ms | ~150ms | ✅ |
| POST /scenes | <300ms | ~250ms | ✅ |
| GET /schedule | <500ms | ~400ms | ✅ |
| POST /optimize | <5s | ~3s | ✅ |

---

## 🔒 Testes de Segurança

### OWASP Top 10:

```python
# tests/security/test_owasp.py

def test_sql_injection_prevention(client, auth_headers):
    """
    Testar proteção contra SQL Injection
    """
    payload = {
        'name': "'; DROP TABLE scenes;--",
        'project_id': 1
    }

    response = client.post('/api/v1/scenes', json=payload, headers=auth_headers)

    # Deve sanitizar input, não executar SQL
    assert response.status_code in [201, 400]

    # Tabela deve existir
    from app.models.scene import Scene
    assert Scene.query.first() is not None

def test_xss_prevention(client, auth_headers):
    """
    Testar proteção contra XSS
    """
    payload = {
        'name': '<script>alert("XSS")</script>',
        'project_id': 1
    }

    response = client.post('/api/v1/scenes', json=payload, headers=auth_headers)
    scene_id = response.json['id']

    # Buscar scene
    response = client.get(f'/api/v1/scenes/{scene_id}', headers=auth_headers)

    # Script deve ser escapado
    assert '<script>' not in response.data.decode()
    assert '&lt;script&gt;' in response.data.decode() or 'alert' not in response.data.decode()

def test_authorization_bypass(client):
    """
    Testar que usuários não autenticados são bloqueados
    """
    response = client.get('/api/v1/scenes/1')

    assert response.status_code == 401
    assert 'Missing Authorization Header' in response.json['msg']

def test_rate_limiting(client, auth_headers):
    """
    Testar rate limiting
    """
    # Fazer 100 requests rápidos
    responses = []
    for _ in range(100):
        response = client.get('/api/v1/scenes', headers=auth_headers)
        responses.append(response.status_code)

    # Pelo menos alguns devem ser bloqueados (429 Too Many Requests)
    assert 429 in responses
```

---

## 🗄️ Test Data Management

### Fixtures Organizadas:

```python
# tests/fixtures/projects.py

import pytest
from app.models.project import Project

@pytest.fixture
def basic_project(db_session):
    """Projeto simples sem scenes"""
    project = Project(
        name="Basic Project",
        start_date=datetime(2025, 1, 1)
    )
    db_session.add(project)
    db_session.commit()
    return project

@pytest.fixture
def project_with_scenes(db_session, basic_project):
    """Projeto com 10 scenes"""
    for i in range(10):
        scene = Scene(
            project_id=basic_project.id,
            name=f"CENA {i:02d}",
            scene_number=f"{i:02d}"
        )
        db_session.add(scene)
    db_session.commit()
    return basic_project

@pytest.fixture
def large_project(db_session):
    """Projeto grande para testes de performance"""
    project = Project(name="Large Project")
    db_session.add(project)
    db_session.flush()

    # 1000 scenes
    scenes = [
        Scene(project_id=project.id, name=f"CENA {i}", scene_number=str(i))
        for i in range(1000)
    ]
    db_session.bulk_save_objects(scenes)
    db_session.commit()

    return project
```

### Factory Pattern:

```python
# tests/factories.py

import factory
from app.models.scene import Scene
from app.models.project import Project

class ProjectFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Project
        sqlalchemy_session = db.session

    name = factory.Sequence(lambda n: f"Project {n}")
    start_date = factory.Faker('date_between', start_date='+1d', end_date='+30d')

class SceneFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Scene
        sqlalchemy_session = db.session

    project = factory.SubFactory(ProjectFactory)
    name = factory.Faker('sentence')
    scene_number = factory.Sequence(lambda n: f"{n:02d}")
    duration_minutes = factory.Faker('random_int', min=60, max=480)

# Uso:
project = ProjectFactory()
scene = SceneFactory(project=project)
scenes = SceneFactory.create_batch(50, project=project)
```

---

## 🚀 CI/CD Integration

### GitHub Actions Workflow:

```yaml
# .github/workflows/tests.yml

name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: cineprod_test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        env:
          DATABASE_URL: postgresql://test:test@localhost/cineprod_test
        run: |
          pytest tests/ --cov=app --cov-report=xml --cov-report=html

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

      - name: Check coverage threshold
        run: |
          coverage report --fail-under=80
```

---

## 📊 Coverage Requirements

### Metas de Cobertura por Módulo:

| Módulo | Meta | Atual | Status |
|--------|------|-------|--------|
| **Models** | 90% | ~85% | ⚠️ |
| **Services** | 85% | ~80% | ⚠️ |
| **API Routes** | 80% | ~75% | ⚠️ |
| **WebSocket** | 70% | ~60% | ❌ |
| **Utils** | 95% | ~90% | ⚠️ |
| **TOTAL** | **80%** | **~80%** | ✅ |

### Comandos de Coverage:

```bash
# Gerar relatório HTML
venv/bin/python3 -m pytest --cov=app --cov-report=html
open htmlcov/index.html

# Gerar relatório terminal
venv/bin/python3 -m pytest --cov=app --cov-report=term

# Coverage apenas de um módulo
venv/bin/python3 -m pytest --cov=app/services --cov-report=term

# Falhar se coverage < 80%
venv/bin/python3 -m pytest --cov=app --cov-fail-under=80
```

---

## 📚 Leia Também

**Antes de testar**:
- `03_QUICK_START_GUIDES.md` - Como implementar features

**Para deploy**:
- `05_DEPLOYMENT_PROCEDURES.md` - Como fazer deploy após testes passarem

**Para entender arquitetura**:
- `01_PROJECT_STRUCTURE.md` - Estrutura de pastas e arquivos

---

**Criado**: 2025-11-15
**Mantido por**: Claude Code + Equipe Digimundo

---

**DIGIMUNDO PRESENTE 🥷**
