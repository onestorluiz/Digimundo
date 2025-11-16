# 🚀 Procedimentos de Deploy - CineProd

**Guia Completo para Deploy Seguro e Confiável**

> "Deploy não é o fim do desenvolvimento, é apenas o começo da operação"

**Data**: 2025-11-15
**Versão**: 1.0

---

## 📋 Índice

1. [Ambientes](#ambientes)
2. [Deploy para Staging](#deploy-para-staging)
3. [Deploy para Production](#deploy-para-production)
4. [Database Migrations](#database-migrations)
5. [Zero-Downtime Deployment](#zero-downtime-deployment)
6. [Rollback Procedures](#rollback-procedures)
7. [Health Checks](#health-checks)
8. [Monitoring & Alerts](#monitoring--alerts)
9. [Troubleshooting](#troubleshooting)
10. [Emergency Procedures](#emergency-procedures)

---

## 🌍 Ambientes

### Estrutura de Ambientes:

```
Development (local)
    ↓
Staging (VPS staging)
    ↓
Production (VPS 82.25.74.142)
```

### Configuração por Ambiente:

| Aspecto | Development | Staging | Production |
|---------|-------------|---------|------------|
| **Database** | SQLite | PostgreSQL | PostgreSQL |
| **Debug Mode** | True | False | False |
| **Log Level** | DEBUG | INFO | WARNING |
| **Cache** | Nenhum | Redis | Redis |
| **Email** | Console | Mailtrap | SendGrid |
| **Domain** | localhost:5000 | staging.cineprod.com | cineprod.com |
| **SSL** | Não | Sim (Let's Encrypt) | Sim (Let's Encrypt) |

---

## 🧪 Deploy para Staging

### Pré-requisitos:

✅ Todos os testes passando
✅ Coverage >= 80%
✅ Code review aprovado
✅ Branch atualizada com `github-main`

### Passo a Passo:

#### 1. Verificar Testes Localmente

```bash
# Rodar todos os testes
venv/bin/python3 -m pytest tests/ --cov=app --cov-fail-under=80

# Verificar linting
venv/bin/ruff check app/

# Verificar security
venv/bin/bandit -r app/
```

#### 2. Commit e Push

```bash
# Commit com mensagem descritiva
git add .
git commit -m "feat: Add conflict detection service

- Implements ConflictDetectionService with actor double-booking detection
- Adds API endpoint POST /api/v1/conflicts/detect
- Includes unit and integration tests (95% coverage)

Closes #42
"

# Push para GitHub
git push origin github-main
```

#### 3. SSH no Servidor Staging

```bash
ssh root@staging.cineprod.com
```

#### 4. Pull e Deploy

```bash
# Navegar para diretório
cd /opt/cineprod

# Backup antes de pull
./scripts/backup_before_deploy.sh

# Pull mudanças
git pull origin github-main

# Ativar virtual environment
source venv/bin/activate

# Instalar/atualizar dependências
pip install -r requirements.txt

# Rodar migrations
flask db upgrade

# Coletar static files (se houver)
flask collect-static

# Restart application
systemctl restart cineprod-staging

# Verificar logs
journalctl -u cineprod-staging -f --lines=50
```

#### 5. Smoke Tests

```bash
# Health check
curl https://staging.cineprod.com/health

# Test API
curl -X POST https://staging.cineprod.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'

# Testar nova feature
curl -X GET https://staging.cineprod.com/api/v1/conflicts/detect/1 \
  -H "Authorization: Bearer $TOKEN"
```

#### 6. Validação Manual

1. Abrir https://staging.cineprod.com no navegador
2. Login com usuário de teste
3. Testar fluxo crítico:
   - Criar projeto
   - Adicionar scenes
   - Gerar breakdown
   - Otimizar schedule
4. Verificar logs de erro (deve estar vazio)

### ✅ Checklist de Staging Deploy:

- [ ] Testes locais passando
- [ ] Code linted e formatado
- [ ] Commit no GitHub
- [ ] Pull no servidor
- [ ] Migrations executadas
- [ ] Service reiniciado
- [ ] Health check OK
- [ ] Smoke tests OK
- [ ] Validação manual OK
- [ ] Logs sem erros

---

## 🏭 Deploy para Production

### ⚠️ IMPORTANTE - Checklist Pré-Deploy:

- [ ] Feature testada em staging por pelo menos 24h
- [ ] Aprovação do Product Owner
- [ ] Backup do banco de dados
- [ ] Comunicação para equipe (Slack/Email)
- [ ] Janela de manutenção agendada (se necessário)
- [ ] Rollback plan definido

### Horário Recomendado:

🕐 **Melhor**: Terça ou Quarta, 22h-23h (baixo tráfego)
⚠️ **Evitar**: Sexta-feira, véspera de feriado, horário comercial

### Passo a Passo:

#### 1. Notificar Equipe

```bash
# Slack
/announce "🚀 Deploy para production agendado para hoje 22h. ETA: 30 min. Janela de manutenção: 22h-22h30."
```

#### 2. Backup Completo

```bash
# SSH no servidor production
ssh root@82.25.74.142

# Backup do banco
cd /opt/cineprod
./scripts/backup_database.sh

# Backup dos arquivos
tar -czf /backups/cineprod_$(date +%Y%m%d_%H%M%S).tar.gz \
  /opt/cineprod \
  --exclude=venv \
  --exclude=node_modules \
  --exclude=__pycache__
```

#### 3. Ativar Modo Manutenção (Opcional)

```bash
# Criar página de manutenção
touch /opt/cineprod/MAINTENANCE_MODE

# Nginx vai retornar 503 com página customizada
```

#### 4. Pull e Deploy

```bash
cd /opt/cineprod

# Pull mudanças
git fetch origin
git log HEAD..origin/github-main --oneline  # Ver commits que vão entrar
git pull origin github-main

# Ativar venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt --upgrade

# Rodar migrations
flask db upgrade

# Compilar assets (se houver)
npm run build  # Se houver frontend assets

# Coletar static
flask collect-static
```

#### 5. Restart com Zero Downtime

```bash
# Usar systemd reload (graceful restart)
systemctl reload cineprod

# OU restart completo (breve downtime ~2s)
systemctl restart cineprod

# Verificar status
systemctl status cineprod
```

#### 6. Desativar Modo Manutenção

```bash
# Remover flag
rm /opt/cineprod/MAINTENANCE_MODE

# Nginx volta a rotear para aplicação
```

#### 7. Verificação Pós-Deploy

```bash
# 1. Health check
curl http://82.25.74.142/health

# 2. Verificar versão deployed
curl http://82.25.74.142/api/version

# 3. Testar endpoints críticos
curl -X POST http://82.25.74.142/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "producer@example.com",
    "password": "RealPassword"
  }'

# 4. Verificar logs em tempo real
journalctl -u cineprod -f
```

#### 8. Smoke Tests Automatizados

```bash
# Rodar smoke tests do diretório tests/smoke/
venv/bin/python3 -m pytest tests/smoke/ --base-url=http://82.25.74.142

# Exemplo: tests/smoke/test_critical_paths.py
def test_login_works():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "test@example.com",
        "password": "TestPass123"
    })
    assert response.status_code == 200
    assert 'access_token' in response.json()
```

#### 9. Monitorar Métricas

```bash
# Prometheus metrics
curl http://82.25.74.142/metrics

# Verificar:
# - request_count
# - request_latency_seconds
# - error_rate
# - database_connections
```

#### 10. Notificar Sucesso

```bash
# Slack
/announce "✅ Deploy concluído com sucesso! Aplicação rodando normalmente. Todos os testes OK."

# OU se houver problema
/announce "⚠️ Deploy com problemas. Iniciando rollback."
```

### ✅ Checklist de Production Deploy:

- [ ] Backup realizado
- [ ] Equipe notificada
- [ ] Modo manutenção ativado (se necessário)
- [ ] Git pull executado
- [ ] Dependências atualizadas
- [ ] Migrations executadas
- [ ] Assets compilados
- [ ] Service reiniciado
- [ ] Modo manutenção desativado
- [ ] Health check OK
- [ ] Smoke tests OK
- [ ] Logs sem erros críticos
- [ ] Métricas normais
- [ ] Equipe notificada de sucesso

---

## 🗄️ Database Migrations

### Criar Nova Migration:

```bash
# Gerar migration automaticamente (baseada em mudanças nos models)
flask db revision --autogenerate -m "Add call_sheet table"

# OU criar migration vazia
flask db revision -m "Add custom index"

# Editar migration gerada
vim migrations/versions/abc123_add_call_sheet_table.py
```

### Exemplo de Migration:

```python
# migrations/versions/abc123_add_call_sheet_table.py

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Criar tabela
    op.create_table('call_sheets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('call_time', sa.Time(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar índice
    op.create_index('ix_call_sheets_project_date', 'call_sheets', ['project_id', 'date'])

    # Adicionar coluna em tabela existente
    op.add_column('scenes', sa.Column('weather_dependency_score', sa.Float(), nullable=True))

    # Atualizar dados existentes
    op.execute("""
        UPDATE scenes
        SET weather_dependency_score = 0.5
        WHERE interior_exterior = 'exterior'
    """)

def downgrade():
    # Reverter tudo (ordem inversa)
    op.drop_column('scenes', 'weather_dependency_score')
    op.drop_index('ix_call_sheets_project_date')
    op.drop_table('call_sheets')
```

### Aplicar Migrations:

```bash
# Ver status
flask db current
flask db history

# Aplicar todas as pending migrations
flask db upgrade

# Aplicar até migration específica
flask db upgrade abc123

# Reverter última migration
flask db downgrade

# Reverter até migration específica
flask db downgrade def456
```

### Migrations em Production:

```bash
# Sempre fazer backup antes!
./scripts/backup_database.sh

# Testar migration primeiro em staging
ssh root@staging.cineprod.com
cd /opt/cineprod
source venv/bin/activate
flask db upgrade

# Se OK, aplicar em production
ssh root@82.25.74.142
cd /opt/cineprod
source venv/bin/activate

# IMPORTANTE: Migrations podem causar downtime
# Para migrations longas, usar estratégia blue-green

flask db upgrade

# Verificar que migration aplicou
flask db current
```

### Migrations Complexas (Zero Downtime):

Para mudanças que causam downtime, usar estratégia multi-fase:

**Exemplo**: Renomear coluna `scene_duration` para `duration_minutes`

**Fase 1** (Deploy N):
```python
def upgrade():
    # Adicionar nova coluna
    op.add_column('scenes', sa.Column('duration_minutes', sa.Integer()))

    # Copiar dados
    op.execute("UPDATE scenes SET duration_minutes = scene_duration")
```

**Fase 2** (Deploy N+1 - após 1 semana):
```python
def upgrade():
    # Remover coluna antiga
    op.drop_column('scenes', 'scene_duration')
```

---

## ⚡ Zero-Downtime Deployment

### Estratégia: Blue-Green Deployment

```
[Nginx Load Balancer]
     ↓        ↓
  [Blue]   [Green]
(version N) (version N+1)
```

#### Setup:

1. **Configurar 2 instâncias da aplicação**:

```bash
# /etc/systemd/system/cineprod-blue.service
[Service]
ExecStart=/opt/cineprod/blue/venv/bin/gunicorn -w 4 -b 127.0.0.1:8001 app:app

# /etc/systemd/system/cineprod-green.service
[Service]
ExecStart=/opt/cineprod/green/venv/bin/gunicorn -w 4 -b 127.0.0.1:8002 app:app
```

2. **Nginx Load Balancer**:

```nginx
# /etc/nginx/sites-available/cineprod

upstream cineprod_backend {
    server 127.0.0.1:8001 weight=100;  # Blue (100% tráfego)
    server 127.0.0.1:8002 weight=0;    # Green (0% tráfego)
}

server {
    listen 80;
    server_name cineprod.com;

    location / {
        proxy_pass http://cineprod_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Processo de Deploy:

```bash
# 1. Deploy para Green (offline)
cd /opt/cineprod/green
git pull origin github-main
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade  # Migration aplicada offline
systemctl restart cineprod-green

# 2. Smoke test Green
curl http://127.0.0.1:8002/health

# 3. Gradualmente rotear tráfego de Blue → Green
# 3a. 10% do tráfego
nginx -s reload  # (após editar weight para 90/10)

# 3b. 50%
nginx -s reload  # (weight 50/50)

# 3c. 100%
nginx -s reload  # (weight 0/100)

# 4. Monitorar métricas
# Se tudo OK após 10min, considerar deploy bem-sucedido

# 5. Desligar Blue
systemctl stop cineprod-blue
```

---

## ↩️ Rollback Procedures

### Quando Fazer Rollback:

⚠️ **Critérios para rollback imediato**:
- Error rate > 5%
- Latency > 2x normal
- Critical bug afeta funcionalidade core
- Database corruption

### Rollback Rápido (Git):

```bash
# SSH no servidor
ssh root@82.25.74.142
cd /opt/cineprod

# Ver último commit
git log -1

# Rollback para commit anterior
git reset --hard HEAD~1

# OU para commit específico
git reset --hard abc123def

# Restart
systemctl restart cineprod

# Verificar
systemctl status cineprod
journalctl -u cineprod -f
```

### Rollback com Database Migration:

```bash
# Ver migrations aplicadas
flask db current
flask db history

# Reverter última migration
flask db downgrade

# Reverter para migration específica
flask db downgrade abc123

# Restart application
systemctl restart cineprod
```

### Rollback Blue-Green:

```bash
# Simplesmente rotear tráfego de volta para Blue

# Nginx config
upstream cineprod_backend {
    server 127.0.0.1:8001 weight=100;  # Blue (restaurar 100%)
    server 127.0.0.1:8002 weight=0;    # Green (remover)
}

# Reload
nginx -s reload

# Downtime: ~0 segundos
```

---

## 🏥 Health Checks

### Endpoint de Health Check:

```python
# app/routes/health.py

from flask import Blueprint, jsonify
from app import db
import redis

bp = Blueprint('health', __name__)

@bp.route('/health')
def health_check():
    """
    Health check endpoint

    Returns:
        200 OK se tudo funcionando
        503 Service Unavailable se houver problema
    """
    checks = {}

    # 1. Database check
    try:
        db.session.execute('SELECT 1')
        checks['database'] = 'ok'
    except Exception as e:
        checks['database'] = f'error: {str(e)}'

    # 2. Redis check
    try:
        r = redis.from_url(current_app.config['REDIS_URL'])
        r.ping()
        checks['redis'] = 'ok'
    except Exception as e:
        checks['redis'] = f'error: {str(e)}'

    # 3. Disk space check
    import shutil
    usage = shutil.disk_usage('/')
    checks['disk_usage'] = {
        'total_gb': usage.total / (1024**3),
        'used_gb': usage.used / (1024**3),
        'free_gb': usage.free / (1024**3),
        'percent': (usage.used / usage.total) * 100
    }

    # Determinar status geral
    if all(v == 'ok' for k, v in checks.items() if k != 'disk_usage'):
        status_code = 200
    else:
        status_code = 503

    return jsonify({
        'status': 'ok' if status_code == 200 else 'degraded',
        'checks': checks,
        'timestamp': datetime.utcnow().isoformat()
    }), status_code
```

### Monitoramento Externo:

#### UptimeRobot:

1. Criar monitor HTTP(S)
2. URL: `https://cineprod.com/health`
3. Intervalo: 5 minutos
4. Alertas: Email + Slack

#### Prometheus:

```yaml
# prometheus.yml

scrape_configs:
  - job_name: 'cineprod'
    scrape_interval: 30s
    static_configs:
      - targets: ['82.25.74.142:5000']
    metrics_path: '/metrics'
```

---

## 📊 Monitoring & Alerts

### Métricas Críticas:

| Métrica | Threshold | Ação |
|---------|-----------|------|
| **CPU Usage** | >80% por 5min | Investigar + Escalar |
| **Memory Usage** | >85% | Restart + Escalar |
| **Disk Usage** | >90% | Limpar logs + Escalar |
| **Request Latency** | p95 > 1s | Investigar queries lentas |
| **Error Rate** | >1% | Alertar equipe |
| **Database Connections** | >80% do pool | Investigar leaks |

### Alertas via Slack:

```python
# app/utils/alerts.py

import requests

def send_alert(message, severity='warning'):
    """
    Enviar alerta para Slack
    """
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')

    color = {
        'info': '#36a64f',
        'warning': '#ff9900',
        'critical': '#ff0000'
    }[severity]

    payload = {
        'attachments': [{
            'color': color,
            'title': f'🚨 CineProd Alert - {severity.upper()}',
            'text': message,
            'footer': 'CineProd Monitoring',
            'ts': int(datetime.utcnow().timestamp())
        }]
    }

    requests.post(webhook_url, json=payload)
```

---

## 🐛 Troubleshooting

### Application não inicia:

```bash
# Ver logs
journalctl -u cineprod -n 100

# Verificar permissões
ls -la /opt/cineprod

# Verificar venv
source venv/bin/activate
which python
python --version

# Testar import
python -c "from app import create_app; app = create_app()"
```

### Database connection error:

```bash
# Verificar PostgreSQL rodando
systemctl status postgresql

# Testar conexão
psql -h localhost -U cineprod -d cineprod_production

# Ver connections ativas
SELECT count(*) FROM pg_stat_activity WHERE datname = 'cineprod_production';
```

### High CPU/Memory:

```bash
# Ver processos
top
htop

# Ver workers Gunicorn
ps aux | grep gunicorn

# Reduzir workers temporariamente
systemctl edit cineprod

# Adicionar:
[Service]
ExecStart=
ExecStart=/opt/cineprod/venv/bin/gunicorn -w 2 -b 127.0.0.1:8000 app:app
```

---

## 🚨 Emergency Procedures

### Outage Total:

```bash
# 1. Verificar servidor está UP
ping 82.25.74.142

# 2. SSH (se responder)
ssh root@82.25.74.142

# 3. Verificar services
systemctl status nginx
systemctl status cineprod
systemctl status postgresql

# 4. Restart tudo
systemctl restart nginx
systemctl restart cineprod
systemctl restart postgresql

# 5. Notificar equipe
/announce "⚠️ OUTAGE TOTAL. Investigando..."
```

### Database Corrupted:

```bash
# 1. Parar application
systemctl stop cineprod

# 2. Restaurar backup mais recente
./scripts/restore_database.sh /backups/cineprod_20250115_220000.sql

# 3. Verificar integridade
psql -U cineprod -d cineprod_production -c "VACUUM ANALYZE;"

# 4. Restart application
systemctl start cineprod
```

---

## 📚 Leia Também

**Antes de fazer deploy**:
- `04_TESTING_STRATEGY.md` - Como testar antes de deploy
- `03_QUICK_START_GUIDES.md` - Como implementar features

**Para organização**:
- `06_ORGANIZATION_RULES.md` - Regras de organização de código

**Para entender estrutura**:
- `01_PROJECT_STRUCTURE.md` - Estrutura do projeto

---

**Criado**: 2025-11-15
**Mantido por**: Claude Code + Equipe Digimundo

---

**DIGIMUNDO PRESENTE 🥷**
