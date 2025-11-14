# 🗺️ CineProd - Mapa de Debugging Completo

**Data:** 27 de Outubro de 2025
**Versão:** v2.1.0-consolidated
**Gestor:** Claude Code (Prompt 00)

---

## 📋 ÍNDICE RÁPIDO

1. [Issues Críticas Identificadas](#issues-críticas)
2. [Debugging por Sintoma](#debugging-por-sintoma)
3. [Debugging por Componente](#debugging-por-componente)
4. [Comandos de Emergência](#comandos-de-emergência)
5. [Logs e Monitoramento](#logs-e-monitoramento)
6. [Rollback Procedures](#rollback-procedures)

---

## 🚨 ISSUES CRÍTICAS

### ISSUE #1: Import Mismatch v2 vs v4
**Status:** 🔴 BLOQUEADOR
**Descoberto:** 27/10/2025 11:30 UTC

**Problema:**
```python
# app/__init__.py está importando:
from app.routes import workspaces_v2_bp  # ❌ ERRADO

# Mas app/routes/__init__.py exporta:
from .v4.workspaces import bp as workspaces_v4_bp  # ✅ CORRETO
```

**Impacto:**
- App não inicia
- Testes falham (148 errors)
- ModuleNotFoundError

**Correção:**
```python
# Opção A: Renomear em app/__init__.py (linhas 122-125)
from app.routes import (
    workspaces_v4_bp,  # ✅ Corrigido
    elements_v4_bp,
    comments_v4_bp,
    activities_v4_bp
)

# E registrar (linhas 157-160)
app.register_blueprint(workspaces_v4_bp)
app.register_blueprint(elements_v4_bp)
app.register_blueprint(comments_v4_bp)
app.register_blueprint(activities_v4_bp)
```

**Teste:**
```bash
python3 -c "from app import create_app; app = create_app(); print('✅ Success')"
```

---

### ISSUE #2: Venv Sem Dependências
**Status:** 🟡 IMPORTANTE
**Descoberto:** 27/10/2025 11:30 UTC

**Problema:**
```
ModuleNotFoundError: No module named 'flask_login'
```

**Correção:**
```bash
cd /Users/clubproducoes/Digimundo/Projeto_Digimundo/cineprod-flask
./venv/bin/pip install -r requirements.txt
./venv/bin/pip install -r requirements-dev.txt
```

**Validação:**
```bash
./venv/bin/python -c "import flask_login; print('✅ OK')"
./venv/bin/python -c "import mypy; print('✅ OK')"
./venv/bin/python -c "import pytest; print('✅ OK')"
```

---

### ISSUE #3: Phase 2 Branch Não Merged
**Status:** 🟡 IMPORTANTE
**Descoberto:** 27/10/2025 11:00 UTC

**Problema:**
Branch `feature/code-audit-phase2-typing` com 15 commits (8 horas de trabalho) não está merged.

**Type hints completados mas não em develop:**
- 16/16 models
- 6/6 utils
- 2/2 scripts

**Correção:**
```bash
git checkout develop
git pull origin develop
git merge feature/code-audit-phase2-typing --no-ff -m "merge: Phase 2 code audit - type hints complete"
git push origin develop
git tag v2.1.1-type-hints -m "Phase 2 complete: models + utils type hints"
git push origin v2.1.1-type-hints
```

---

## 🔍 DEBUGGING POR SINTOMA

### Sintoma: "App Não Inicia"

#### Check 1: Import Errors
```bash
python3 -c "from app import create_app"
```

**Se falhar com ModuleNotFoundError:**
→ Ver [ISSUE #1](#issue-1-import-mismatch-v2-vs-v4) ou [ISSUE #2](#issue-2-venv-sem-dependências)

---

#### Check 2: Database Connection
```bash
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.session.execute(db.text('SELECT 1'))"
```

**Se falhar:**
```bash
# Verificar DATABASE_URL em .env
cat .env | grep DATABASE_URL

# Verificar PostgreSQL rodando (produção)
ssh root@82.25.74.142 "systemctl status postgresql"

# Verificar SQLite existe (dev)
ls -la instance/cineprod_dev.db
```

---

#### Check 3: Configuration
```bash
python3 -c "from config.config import config; print(config['development'])"
```

**Se falhar:**
```bash
# Verificar .env existe
ls -la .env

# Verificar SECRET_KEY definido
cat .env | grep SECRET_KEY
```

---

### Sintoma: "Testes Falhando"

#### Check 1: Import Errors nos Testes
```bash
./venv/bin/pytest tests/ --collect-only
```

**Se coletar 0 tests:**
→ Problema de imports nos test files

**Se coletar mas falhar:**
→ Ver imports em conftest.py

---

#### Check 2: Database Test
```bash
./venv/bin/pytest tests/test_auth.py -v
```

**Se falhar com database error:**
```bash
# Criar database test
FLASK_ENV=testing flask db upgrade
```

---

#### Check 3: Fixtures
```bash
./venv/bin/pytest tests/ -v --setup-show
```

**Mostra setup de fixtures:**
- Se fixture falhar → problema em conftest.py
- Se test falhar → problema no test específico

---

### Sintoma: "Type Checking Falhando"

#### Check 1: mypy Instalado
```bash
./venv/bin/mypy --version
```

**Se não instalado:**
```bash
./venv/bin/pip install mypy
```

---

#### Check 2: Configuração mypy
```bash
cat mypy.ini
```

**Deve ter:**
```ini
[mypy]
python_version = 3.9
files = app/models, app/utils
```

---

#### Check 3: Rodar mypy
```bash
./venv/bin/mypy app/models app/utils --config-file mypy.ini
```

**Erros comuns:**
- `error: Cannot find implementation` → Install type stubs
- `error: Module X has no attribute Y` → Missing type hint
- `error: Incompatible types` → Type mismatch

---

### Sintoma: "CI/CD Falhando"

#### Check 1: GitHub Actions
```bash
# Ver último workflow
gh run list --limit 1

# Ver logs
gh run view --log
```

---

#### Check 2: Simular CI Localmente
```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run linting
black --check app/
flake8 app/ --count --exit-zero

# Run security scan
safety check
bandit -r app/
```

---

### Sintoma: "502 Bad Gateway (Produção)"

#### Check 1: Serviço CineProd
```bash
ssh root@82.25.74.142 "systemctl status cineprod"
```

**Se inactive/failed:**
```bash
# Ver logs
ssh root@82.25.74.142 "journalctl -u cineprod -n 50"

# Restart
ssh root@82.25.74.142 "systemctl restart cineprod"
```

---

#### Check 2: nginx
```bash
ssh root@82.25.74.142 "nginx -t"
```

**Se erro de config:**
```bash
# Ver config
ssh root@82.25.74.142 "cat /etc/nginx/sites-available/cineprod"

# Reload
ssh root@82.25.74.142 "systemctl reload nginx"
```

---

#### Check 3: Gunicorn
```bash
ssh root@82.25.74.142 "tail -100 /opt/cineprod/logs/gunicorn_error.log"
```

**Erros comuns:**
- Import errors → Corrigir código
- Permission denied → `chown cineprod:cineprod`
- Port already in use → `lsof -i :8000`

---

### Sintoma: "Database Migration Error"

#### Check 1: Migration Status
```bash
flask db current
flask db history
```

---

#### Check 2: Tentar Upgrade
```bash
flask db upgrade
```

**Se falhar:**
```bash
# Ver migrations pendentes
flask db show

# Downgrade e retry
flask db downgrade -1
flask db upgrade
```

---

#### Check 3: Criar Nova Migration
```bash
flask db migrate -m "description"
flask db upgrade
```

---

## 🧩 DEBUGGING POR COMPONENTE

### Backend (Flask App)

#### Verificar Estrutura
```bash
python3 -c "from app import create_app; app = create_app(); print(app.url_map)"
```

**Mostra todas as rotas registradas**

---

#### Verificar Blueprints
```bash
python3 -c "from app import create_app; app = create_app(); print(list(app.blueprints.keys()))"
```

**Deve mostrar:**
```
['auth', 'projects', 'scenes', 'shots', 'v2', ...]
```

---

#### Verificar Models
```bash
python3 -c "from app.models import User, Project, Scene; print('✅ Models OK')"
```

---

### Database

#### Verificar Conexão
```bash
# Development (SQLite)
sqlite3 instance/cineprod_dev.db "SELECT COUNT(*) FROM users;"

# Production (PostgreSQL)
ssh root@82.25.74.142 "sudo -u postgres psql -d cineprod_db -c 'SELECT COUNT(*) FROM users;'"
```

---

#### Verificar Schema
```bash
# Development
sqlite3 instance/cineprod_dev.db ".schema users"

# Production
ssh root@82.25.74.142 "sudo -u postgres psql -d cineprod_db -c '\d users'"
```

---

#### Backup Database
```bash
# Development
cp instance/cineprod_dev.db instance/cineprod_dev.db.backup_$(date +%Y%m%d_%H%M%S)

# Production
ssh root@82.25.74.142 "sudo -u postgres pg_dump cineprod_db > /tmp/cineprod_backup_$(date +%Y%m%d).sql"
```

---

### Frontend (Templates + JS)

#### Verificar Templates
```bash
find app/templates -name "*.html" | wc -l
```

**Deve ter ~50+ templates**

---

#### Verificar Static Files
```bash
find app/static -type f | wc -l
```

---

#### Test Frontend Locally
```bash
# Start dev server
FLASK_ENV=development python wsgi.py

# Visit in browser
open http://localhost:5001/v2/login
```

---

### API Endpoints

#### Health Check
```bash
curl http://localhost:5001/health
```

**Deve retornar:**
```json
{"app":"CineProd","status":"healthy"}
```

---

#### Test Auth
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

---

#### Test Protected Endpoint
```bash
TOKEN="your_jwt_token"
curl -X GET http://localhost:5001/api/v2/projects \
  -H "Authorization: Bearer $TOKEN"
```

---

## ⚡ COMANDOS DE EMERGÊNCIA

### Parar Tudo
```bash
# Local
pkill -f "python.*wsgi"

# Produção
ssh root@82.25.74.142 "systemctl stop cineprod"
ssh root@82.25.74.142 "systemctl stop nginx"
```

---

### Restart Tudo
```bash
# Produção
ssh root@82.25.74.142 "systemctl restart cineprod"
ssh root@82.25.74.142 "systemctl reload nginx"
ssh root@82.25.74.142 "systemctl status cineprod"
```

---

### Rollback Git
```bash
# Ver último commit
git log --oneline -1

# Desfazer último commit (CUIDADO!)
git reset --hard HEAD~1

# Rollback para commit específico
git reset --hard <commit-hash>

# Restaurar arquivo específico
git checkout <commit-hash> -- path/to/file
```

---

### Restore Database
```bash
# Development
cp instance/cineprod_dev.db.backup_YYYYMMDD_HHMMSS instance/cineprod_dev.db

# Production
ssh root@82.25.74.142 "sudo -u postgres psql -d cineprod_db < /tmp/cineprod_backup_YYYYMMDD.sql"
```

---

### Clear Cache
```bash
# Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# Pip cache
./venv/bin/pip cache purge

# Browser cache
# F12 → Network → Disable cache (checkbox)
```

---

## 📊 LOGS E MONITORAMENTO

### Logs Disponíveis

#### Development
```bash
# App log
tail -f logs/app.log

# Error log
tail -f logs/error.log

# Access log
tail -f logs/access.log

# Security log
tail -f logs/security.log
```

---

#### Production
```bash
# Gunicorn error
ssh root@82.25.74.142 "tail -f /opt/cineprod/logs/gunicorn_error.log"

# Gunicorn access
ssh root@82.25.74.142 "tail -f /opt/cineprod/logs/gunicorn_access.log"

# nginx error
ssh root@82.25.74.142 "tail -f /var/log/nginx/error.log"

# nginx access
ssh root@82.25.74.142 "tail -f /var/log/nginx/access.log"

# systemd journal
ssh root@82.25.74.142 "journalctl -u cineprod -f"
```

---

### Monitoramento Real-Time

#### App Status
```bash
# Production health
curl https://templooculto.cloud/health

# Detailed health
curl https://templooculto.cloud/health/detailed
```

---

#### System Metrics
```bash
ssh root@82.25.74.142 "htop"
ssh root@82.25.74.142 "free -h"
ssh root@82.25.74.142 "df -h"
```

---

#### Process Monitoring
```bash
# CineProd processes
ssh root@82.25.74.142 "ps aux | grep gunicorn"

# nginx processes
ssh root@82.25.74.142 "ps aux | grep nginx"

# PostgreSQL
ssh root@82.25.74.142 "ps aux | grep postgres"
```

---

## 🔄 ROLLBACK PROCEDURES

### Rollback Code

#### Option A: Git Reset
```bash
# Ver histórico
git log --oneline -10

# Reset HARD (perde mudanças)
git reset --hard <commit-hash>

# Reset SOFT (mantém mudanças)
git reset --soft <commit-hash>

# Push force (CUIDADO!)
git push origin develop --force
```

---

#### Option B: Git Revert
```bash
# Reverter commit específico (cria novo commit)
git revert <commit-hash>

# Reverter merge
git revert -m 1 <merge-commit-hash>

# Push normal
git push origin develop
```

---

### Rollback Database

#### Development
```bash
# Downgrade 1 migration
flask db downgrade -1

# Downgrade to specific
flask db downgrade <revision>

# Restore from backup
cp instance/cineprod_dev.db.backup instance/cineprod_dev.db
```

---

#### Production
```bash
# Downgrade (CUIDADO!)
ssh root@82.25.74.142 "cd /opt/cineprod && source venv/bin/activate && flask db downgrade -1"

# Restore from backup
ssh root@82.25.74.142 "sudo -u postgres psql -d cineprod_db < /backups/cineprod_YYYYMMDD.sql"
```

---

### Rollback Deploy

```bash
# Via git
ssh root@82.25.74.142 "cd /opt/cineprod && git checkout <previous-commit>"
ssh root@82.25.74.142 "systemctl restart cineprod"

# Via backup
ssh root@82.25.74.142 "cd /opt/cineprod && tar xzf /backups/cineprod_backup_YYYYMMDD.tar.gz"
ssh root@82.25.74.142 "systemctl restart cineprod"
```

---

## 📞 QUICK REFERENCE

### Ports
- Development: 5001
- Production: 8000 (gunicorn) → 443 (nginx)
- PostgreSQL: 5432

### Paths
- Local: `/Users/clubproducoes/Digimundo/Projeto_Digimundo/cineprod-flask`
- Production: `/opt/cineprod`
- Logs: `logs/` (dev), `/opt/cineprod/logs/` (prod)
- Database: `instance/cineprod_dev.db` (dev), PostgreSQL (prod)

### URLs
- Production: https://templooculto.cloud
- Health: https://templooculto.cloud/health
- API: https://templooculto.cloud/api/
- VPS: 82.25.74.142

### Credentials
- Admin: admin / admin123 (local)
- VPS: root@82.25.74.142
- DB: Ver .env

---

## 🎯 DEBUGGING DECISION TREE

```
┌─ App não inicia?
│  ├─ Import error?
│  │  ├─ workspaces_v2_bp? → FIX: Renomear para v4
│  │  └─ flask_login? → FIX: pip install -r requirements.txt
│  │
│  ├─ Database error?
│  │  ├─ Connection refused? → Check PostgreSQL running
│  │  └─ No such table? → flask db upgrade
│  │
│  └─ Config error?
│     └─ Missing .env? → cp .env.example .env
│
├─ Testes falhando?
│  ├─ 148 errors import? → FIX: workspaces_v2_bp → v4
│  ├─ Database? → FLASK_ENV=testing flask db upgrade
│  └─ Fixtures? → Check conftest.py
│
├─ Type checking failing?
│  ├─ mypy not found? → pip install mypy
│  └─ Type errors? → Check type hints
│
├─ CI/CD failing?
│  ├─ Simular local → pytest, black, flake8
│  └─ Check GitHub Actions logs
│
└─ Production 502?
   ├─ Check cineprod service → systemctl status
   ├─ Check nginx → nginx -t
   └─ Check logs → tail gunicorn_error.log
```

---

**Criado:** 27 de Outubro de 2025, 11:45 UTC
**Última Atualização:** 27 de Outubro de 2025, 11:45 UTC
**Versão:** 1.0
**Por:** Claude Code (Gestor - Prompt 00)
