# 📐 Regras de Organização - CineProd

**Padrões, Convenções e Boas Práticas**

> "Código é lido 10x mais vezes do que é escrito. Organize para o leitor, não para o escritor."

**Data**: 2025-11-15
**Versão**: 1.0

---

## 📋 Índice

1. [Filosofia de Organização](#filosofia-de-organização)
2. [Estrutura de Pastas](#estrutura-de-pastas)
3. [Naming Conventions](#naming-conventions)
4. [Imports Organization](#imports-organization)
5. [Code Style Guide](#code-style-guide)
6. [Git Workflow](#git-workflow)
7. [Documentation Standards](#documentation-standards)
8. [Database Conventions](#database-conventions)
9. [API Design Principles](#api-design-principles)
10. [Frontend Organization](#frontend-organization)

---

## 🎯 Filosofia de Organização

### Princípios Fundamentais:

1. **Consistência > Perfeição**
   - Melhor código consistente "OK" do que código inconsistente "perfeito"

2. **Convenção sobre Configuração**
   - Seguir padrões estabelecidos reduz decisões e overhead mental

3. **Separação de Responsabilidades**
   - Models: Estado
   - Services: Lógica de negócio
   - Routes: HTTP/API
   - Utils: Funções auxiliares

4. **DRY (Don't Repeat Yourself)**
   - Se copiar código 3x, extrair para função/classe

5. **YAGNI (You Aren't Gonna Need It)**
   - Não criar abstrações "para o futuro"
   - Criar apenas o que é necessário agora

---

## 📁 Estrutura de Pastas

### Layout Padrão:

```
cineprod-flask/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config.py             # Configurações
│   ├── models/               # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── scene.py
│   │   ├── project.py
│   │   └── user.py
│   ├── services/             # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── scene_service.py
│   │   └── project_service.py
│   ├── routes/               # Flask routes (monolítico)
│   │   ├── __init__.py
│   │   ├── scenes.py
│   │   └── projects.py
│   ├── api/                  # REST API (versionado)
│   │   ├── v1/
│   │   ├── v2/
│   │   └── v4/
│   ├── sockets/              # WebSocket handlers
│   ├── utils/                # Funções auxiliares
│   ├── schemas/              # Marshmallow/Pydantic schemas
│   ├── decorators/           # Custom decorators
│   ├── middleware/           # Middlewares
│   └── templates/            # Jinja2 templates
├── migrations/               # Alembic migrations
├── tests/                    # Testes
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/                     # Documentação
├── scripts/                  # Scripts utilitários
├── static/                   # Assets estáticos
├── requirements.txt          # Dependências
└── .env                      # Variáveis de ambiente
```

### Regras de Diretório:

1. **Cada diretório tem `__init__.py`**
   - Facilita imports
   - Pode conter exports públicos

2. **Módulos < 500 linhas**
   - Se arquivo > 500 linhas, dividir em submodules

3. **Agrupamento por Feature (opcional)**
   ```
   app/
   ├── features/
   │   ├── scenes/
   │   │   ├── models.py
   │   │   ├── services.py
   │   │   ├── routes.py
   │   │   └── schemas.py
   │   └── projects/
   │       ├── models.py
   │       ├── services.py
   │       └── routes.py
   ```

---

## 🏷️ Naming Conventions

### Geral:

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| **Variáveis** | snake_case | `user_id`, `scene_name` |
| **Constantes** | UPPER_SNAKE_CASE | `MAX_SCENES`, `DEFAULT_TIMEOUT` |
| **Funções** | snake_case (verbo) | `get_scene()`, `calculate_cost()` |
| **Classes** | PascalCase (substantivo) | `Scene`, `ProjectService` |
| **Private** | _prefix | `_internal_method()` |
| **Arquivos** | snake_case | `scene_service.py` |

### Models:

```python
# ✅ BOM
class Scene(db.Model):
    __tablename__ = 'scenes'  # plural, snake_case

    id = db.Column(db.Integer, primary_key=True)
    scene_number = db.Column(db.String(10))  # snake_case
    created_at = db.Column(db.DateTime)

# ❌ RUIM
class scene(db.Model):  # Classe deve ser PascalCase
    __tablename__ = 'Scene'  # Tabela deve ser plural e snake_case

    ID = db.Column(db.Integer)  # Coluna não deve ser UPPER
    sceneNumber = db.Column(db.String(10))  # Deve ser snake_case
```

### Services:

```python
# ✅ BOM
class SceneService:
    """
    Serviço para manipular scenes

    Naming: <Model>Service
    """

    def get_scene(self, scene_id):  # Verbo + substantivo
        """Buscar scene por ID"""
        pass

    def create_scene(self, data):
        """Criar nova scene"""
        pass

# ❌ RUIM
class SceneManager:  # Usar "Service", não "Manager"
    def scene(self, id):  # Falta verbo
        pass
```

### Routes/Endpoints:

```python
# ✅ BOM
@bp.route('/scenes', methods=['GET'])  # plural, kebab-case
def list_scenes():
    """Listar scenes"""
    pass

@bp.route('/scenes/<int:id>', methods=['GET'])
def get_scene(id):
    """Buscar scene por ID"""
    pass

# ❌ RUIM
@bp.route('/Scene', methods=['GET'])  # Deve ser lowercase
def getScenes():  # Deve ser snake_case
    pass
```

### Variáveis:

```python
# ✅ BOM
scene_id = 1
user_name = "João"
is_active = True
has_permission = False

# ❌ RUIM
sceneId = 1  # camelCase é JavaScript
UserName = "João"  # PascalCase é para classes
active = True  # Falta prefixo is_/has_
```

---

## 📦 Imports Organization

### Ordem Padrão:

```python
# 1. Standard library
import os
import sys
from datetime import datetime, timedelta

# 2. Third-party
from flask import Blueprint, request, jsonify
from sqlalchemy import and_, or_
import numpy as np

# 3. Local application
from app import db
from app.models.scene import Scene
from app.services.scene_service import SceneService
from app.utils.validators import validate_email

# 4. Relative imports (evitar)
# from .models import Scene  # Preferir absolute imports
```

### Regras:

1. **Alfabético dentro de cada grupo**
2. **Uma linha por import** (exceto múltiplos itens do mesmo module)
3. **Evitar wildcard imports** (`from module import *`)
4. **Agrupar com linha em branco** entre grupos

```python
# ✅ BOM
from flask import Blueprint, jsonify, request
from app.models.scene import Scene
from app.services.scene_service import SceneService

# ❌ RUIM
from flask import *  # Wildcard
from app.models.scene import Scene
import os  # Fora de ordem
from app.services.scene_service import SceneService
```

### isort Configuration:

```ini
# setup.cfg ou .isort.cfg

[isort]
profile = black
multi_line_output = 3
include_trailing_comma = True
force_grid_wrap = 0
use_parentheses = True
ensure_newline_before_comments = True
line_length = 100
skip_gitignore = True

known_first_party = app
known_third_party = flask,sqlalchemy,marshmallow

sections = FUTURE,STDLIB,THIRDPARTY,FIRSTPARTY,LOCALFOLDER
```

Rodar:

```bash
# Ordenar imports automaticamente
isort app/ tests/

# Verificar sem modificar
isort --check-only app/
```

---

## 🎨 Code Style Guide

### Black Formatter:

```ini
# pyproject.toml

[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.venv
  | build
  | dist
)/
'''
```

Rodar:

```bash
# Formatar código
black app/ tests/

# Verificar sem modificar
black --check app/
```

### Ruff Linter:

```toml
# pyproject.toml

[tool.ruff]
line-length = 100
target-version = "py311"

select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]

ignore = [
    "E501",  # line too long (handled by black)
    "B008",  # do not perform function calls in argument defaults
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # Unused imports OK em __init__.py
```

Rodar:

```bash
# Verificar linting
ruff check app/

# Auto-fix
ruff check app/ --fix
```

### Type Hints:

```python
# ✅ BOM
from typing import List, Optional, Dict, Any

def get_scenes(project_id: int, limit: int = 10) -> List[Scene]:
    """
    Buscar scenes de um projeto

    Args:
        project_id: ID do projeto
        limit: Número máximo de scenes

    Returns:
        Lista de scenes
    """
    return Scene.query.filter_by(project_id=project_id).limit(limit).all()

def calculate_cost(scene: Scene) -> Optional[float]:
    """
    Calcular custo de uma scene

    Returns:
        Custo em reais, ou None se não puder calcular
    """
    if not scene.cast:
        return None

    return sum(actor.daily_rate for actor in scene.cast)

# ❌ RUIM
def get_scenes(project_id, limit=10):  # Sem type hints
    return Scene.query.filter_by(project_id=project_id).limit(limit).all()
```

### Docstrings:

```python
# ✅ BOM - Google Style
def create_scene(project_id: int, data: Dict[str, Any]) -> Scene:
    """
    Criar nova scene em um projeto.

    Args:
        project_id: ID do projeto
        data: Dados da scene (name, scene_number, etc)

    Returns:
        Scene criada

    Raises:
        ValueError: Se project_id inválido
        ValidationError: Se data inválido

    Example:
        >>> scene = create_scene(1, {'name': 'CENA 01', 'scene_number': '01'})
        >>> scene.id
        1
    """
    pass

# ❌ RUIM - Sem docstring ou docstring vaga
def create_scene(project_id, data):
    """Creates a scene."""
    pass
```

---

## 🔀 Git Workflow

### Branch Strategy:

```
main (production)
  ↑
github-main (develop)
  ↑
feature/add-conflict-detection
feature/update-scheduling
hotfix/fix-critical-bug
```

### Branch Naming:

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| **Feature** | `feature/<descrição>` | `feature/add-conflict-detection` |
| **Bugfix** | `bugfix/<descrição>` | `bugfix/fix-scene-duplication` |
| **Hotfix** | `hotfix/<descrição>` | `hotfix/fix-critical-login-bug` |
| **Refactor** | `refactor/<descrição>` | `refactor/extract-scene-service` |

### Commit Messages (Conventional Commits):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: Nova feature
- `fix`: Bug fix
- `refactor`: Refatoração (sem mudança de comportamento)
- `test`: Adicionar/modificar testes
- `docs`: Documentação
- `style`: Formatação (sem mudança de código)
- `perf`: Performance
- `chore`: Manutenção (deps, build, etc)

**Exemplos**:

```bash
# ✅ BOM
git commit -m "feat(scenes): Add conflict detection service

- Implements ConflictDetectionService with actor double-booking detection
- Adds API endpoint POST /api/v1/conflicts/detect
- Includes unit and integration tests (95% coverage)

Closes #42
"

git commit -m "fix(auth): Fix JWT token expiration bug

Token was expiring after 1h instead of 24h due to incorrect
timedelta calculation.

Fixes #67
"

git commit -m "refactor(services): Extract common validation logic

- Creates BaseService with shared validation methods
- Reduces duplication across scene_service and project_service
- No behavior changes

"

# ❌ RUIM
git commit -m "fix bug"  # Vago
git commit -m "updates"  # Sem tipo
git commit -m "WIP"  # Work in progress - não commitar
```

### Pull Request Template:

```markdown
## 📝 Descrição

Adiciona serviço de detecção de conflitos de scheduling.

## 🎯 Motivação

Closes #42

Atualmente, conflitos de scheduling (ator em 2 lugares ao mesmo tempo) só são detectados manualmente. Isso causa erros frequentes.

## 🛠️ Mudanças

- [ ] Adiciona `ConflictDetectionService`
- [ ] Adiciona endpoint `POST /api/v1/conflicts/detect`
- [ ] Adiciona testes (unit + integration)
- [ ] Atualiza documentação

## ✅ Checklist

- [x] Testes passando
- [x] Coverage >= 80%
- [x] Linted (ruff)
- [x] Formatted (black)
- [x] Type hints adicionados
- [x] Docstrings atualizadas
- [ ] Testado em staging
- [ ] Aprovado por code review

## 📸 Screenshots (se aplicável)

[screenshot]

## 🧪 Como Testar

1. Criar 2 scenes no mesmo dia
2. Associar mesmo ator a ambas
3. Chamar `POST /api/v1/conflicts/detect/1`
4. Deve retornar conflito
```

---

## 📚 Documentation Standards

### Code Comments:

```python
# ✅ BOM - Comentar "por quê", não "o quê"

def calculate_overtime_cost(scene: Scene) -> float:
    """Calcular custo de overtime"""

    # Usar 1.5x porque sindicato exige 50% adicional após 8h
    overtime_multiplier = 1.5

    base_hours = 8
    overtime_hours = max(0, (scene.duration_minutes / 60) - base_hours)

    return scene.base_cost + (overtime_hours * hourly_rate * overtime_multiplier)

# ❌ RUIM - Comentar o óbvio

def calculate_overtime_cost(scene):
    # Define overtime multiplier
    overtime_multiplier = 1.5  # Óbvio!

    # Calculate overtime hours
    overtime_hours = ...  # Óbvio!

    # Return cost
    return ...  # Óbvio!
```

### Module Docstrings:

```python
# app/services/conflict_detection_service.py

"""
Conflict Detection Service

Detecta conflitos de scheduling como:
- Atores em múltiplos lugares no mesmo dia
- Equipamentos double-booked
- Locações com permissão vencida

Usado por:
- SchedulingService para validar schedule
- API endpoint /conflicts/detect

Example:
    >>> service = ConflictDetectionService()
    >>> conflicts = service.detect_all_conflicts(project_id=1)
    >>> if conflicts:
    ...     print(f"Found {len(conflicts)} conflicts")
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class ConflictDetectionService:
    ...
```

### README por Feature:

```markdown
# app/services/README.md

# Services Layer

Contém lógica de negócio do CineProd.

## Estrutura

- `scene_service.py` - Operações com scenes
- `project_service.py` - Operações com projetos
- `conflict_detection_service.py` - Detecção de conflitos
- `scheduling_service.py` - Scheduling e otimização

## Convenções

1. Cada service é uma classe `<Model>Service`
2. Métodos são verbos: `get_`, `create_`, `update_`, `delete_`
3. Services não acessam request/response diretamente
4. Services podem chamar outros services

## Exemplo

```python
from app.services.scene_service import SceneService

service = SceneService()
scene = service.create(project_id=1, data={'name': 'CENA 01'})
```
```

---

## 🗄️ Database Conventions

### Table Names:

```python
# ✅ BOM
class Scene(db.Model):
    __tablename__ = 'scenes'  # Plural, snake_case

class CallSheet(db.Model):
    __tablename__ = 'call_sheets'

# ❌ RUIM
class Scene(db.Model):
    __tablename__ = 'Scene'  # Singular, PascalCase

class CallSheet(db.Model):
    __tablename__ = 'callsheets'  # Sem underscore
```

### Column Names:

```python
# ✅ BOM
id = db.Column(db.Integer, primary_key=True)
scene_number = db.Column(db.String(10))
created_at = db.Column(db.DateTime)
project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

# ❌ RUIM
ID = db.Column(db.Integer, primary_key=True)
sceneNumber = db.Column(db.String(10))
creation_date = db.Column(db.DateTime)  # Inconsistente com created_at
projectId = db.Column(db.Integer)
```

### Foreign Keys:

```
Padrão: <table_singular>_id

scene_id → scenes.id
project_id → projects.id
user_id → users.id
```

### Indexes:

```python
# ✅ BOM - Nomear índices explicitamente
__table_args__ = (
    db.Index('ix_scenes_project_id', 'project_id'),
    db.Index('ix_scenes_shooting_date', 'shooting_date'),
    db.Index('ix_scenes_project_date', 'project_id', 'shooting_date'),  # Composite
)

# ❌ RUIM - Deixar SQLAlchemy gerar nomes
```

---

## 🌐 API Design Principles

### RESTful URLs:

```
GET    /api/v1/scenes           # Listar scenes
POST   /api/v1/scenes           # Criar scene
GET    /api/v1/scenes/:id       # Buscar scene
PUT    /api/v1/scenes/:id       # Substituir scene (completo)
PATCH  /api/v1/scenes/:id       # Atualizar scene (parcial)
DELETE /api/v1/scenes/:id       # Deletar scene

# Nested resources
GET    /api/v1/projects/:id/scenes  # Scenes de um projeto
```

### HTTP Status Codes:

| Code | Significado | Uso |
|------|-------------|-----|
| **200 OK** | Sucesso | GET, PATCH, PUT |
| **201 Created** | Criado | POST |
| **204 No Content** | Sucesso sem body | DELETE |
| **400 Bad Request** | Validação falhou | Dados inválidos |
| **401 Unauthorized** | Não autenticado | JWT faltando |
| **403 Forbidden** | Sem permissão | RBAC bloqueou |
| **404 Not Found** | Recurso não existe | ID inválido |
| **409 Conflict** | Conflito (duplicate) | Email já existe |
| **422 Unprocessable Entity** | Validação semântica | Business rule violation |
| **500 Internal Server Error** | Erro do servidor | Exception não tratada |

### Response Format:

```json
// ✅ BOM - Consistente

// Sucesso (single resource)
{
  "id": 1,
  "name": "CENA 01",
  "scene_number": "01"
}

// Sucesso (collection)
{
  "scenes": [...],
  "total": 100,
  "page": 1,
  "per_page": 10,
  "pages": 10
}

// Erro
{
  "error": "Scene não encontrada",
  "code": "SCENE_NOT_FOUND",
  "details": {
    "scene_id": 999
  }
}

// ❌ RUIM - Inconsistente
{
  "data": {"id": 1},  // Às vezes "data", às vezes não
  "message": "OK"     // Campo desnecessário
}
```

---

## 🎨 Frontend Organization

### Templates Structure:

```
templates/
├── base.html              # Layout base
├── components/            # Componentes reutilizáveis
│   ├── navbar.html
│   ├── sidebar.html
│   └── modal.html
├── scenes/                # Por feature
│   ├── list.html
│   ├── detail.html
│   └── edit.html
└── projects/
    ├── list.html
    └── detail.html
```

### JavaScript:

```javascript
// static/js/scenes.js

// ✅ BOM - Modular
const SceneManager = {
  init() {
    this.bindEvents();
  },

  bindEvents() {
    document.getElementById('create-scene-btn').addEventListener('click', this.handleCreate);
  },

  async handleCreate(e) {
    e.preventDefault();
    const data = this.getFormData();
    await this.createScene(data);
  },

  async createScene(data) {
    const response = await fetch('/api/v1/scenes', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });

    return response.json();
  }
};

document.addEventListener('DOMContentLoaded', () => SceneManager.init());

// ❌ RUIM - Código solto, global
var sceneBtn = document.getElementById('btn');
sceneBtn.onclick = function() {
  // Inline handler
};
```

---

## 📚 Leia Também

**Para implementação**:
- `03_QUICK_START_GUIDES.md` - Como implementar features seguindo esses padrões
- `01_PROJECT_STRUCTURE.md` - Estrutura detalhada do projeto

**Para qualidade**:
- `04_TESTING_STRATEGY.md` - Como testar código organizado
- `05_DEPLOYMENT_PROCEDURES.md` - Deploy de código organizado

**Para metodologia**:
- `00_START_HERE_CLAUDE_METHODOLOGY.md` - Evitar erros de organização

---

**Criado**: 2025-11-15
**Mantido por**: Claude Code + Equipe Digimundo

---

**DIGIMUNDO PRESENTE 🥷**
