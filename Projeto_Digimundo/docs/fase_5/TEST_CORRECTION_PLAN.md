# 🔧 Plano de Correção dos 175 Testes Falhando

**Data**: 2025-11-16
**Duração Estimada**: 4 semanas (80-100 horas)
**Prioridade**: CRÍTICA - Bloqueia início da Fase 5.2

---

## 📊 Situação Atual

### Estatísticas dos Testes

```
RESULTADO DO pytest (2025-11-16):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Passing:  3,460 testes
❌ Failed:   140 testes
⚠️ Errors:   430 testes (collection/import errors)
⏭️ Skipped:  117 testes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:      4,155 testes

Taxa de Sucesso: 83.3% (3,460/4,155)
Taxa de Falha:   16.7% (570/4,155)
```

### Breakdown por Tipo de Problema

| Categoria | Quantidade | % do Total | Tempo Est. |
|-----------|-----------|-----------|------------|
| **Import Errors** | 430 | 75% | 30-40h |
| **Test Logic Failures** | 140 | 25% | 50-60h |
| **Total** | 570 | 100% | **80-100h** |

---

## 🔍 Análise de Categorias de Erros

### Categoria 1: Import/Collection Errors (430 erros)

**Sintomas:**
```python
ERROR tests/unit/test_storyboard_system_complete.py::TestStoryboardService::test_delete_frame
ERROR tests/unit/test_storyboard_system_complete.py::TestStoryboardModels::test_storyboard_to_dict
```

**Causas Prováveis:**
1. Módulos com dependências circulares
2. Imports faltando ou incorretos
3. Fixtures mal configuradas
4. pytest plugins não instalados

**Solução:**
```bash
# Identificar erros específicos
pytest tests/unit/test_storyboard_system_complete.py -v --tb=short

# Padrões comuns:
# - ImportError: cannot import name 'X' from 'Y'
#   → Verificar imports circulares, renomear módulos
#
# - AttributeError: module 'X' has no attribute 'Y'
#   → Verificar se módulo foi refatorado, atualizar imports
#
# - FixtureNotFoundError: fixture 'X' not found
#   → Adicionar fixture em conftest.py ou decorator
```

**Tempo Estimado**: 30-40 horas (1.5-2 semanas)

---

### Categoria 2: Test Logic Failures (140 falhas)

**Sintomas:**
```python
FAILED tests/unit/test_project_service_comprehensive.py::TestProjectServiceGetUserProjects::test_get_user_projects_with_memberships
AssertionError: assert <Mock name='OWNER.name' id='4500217136'> == 'OWNER'
```

**Causas Prováveis:**
1. Mocks incorretos (SQLAlchemy 1.x vs 2.0)
2. Assertions desatualizadas
3. Lógica de negócio mudou mas teste não
4. Fixtures retornando dados errados

**Solução:**
```python
# ANTES (failing)
mock_role.name = Mock()  # ❌ name vira Mock object

# DEPOIS (fixed)
mock_role.name = "OWNER"  # ✅ name é string
```

**Tempo Estimado**: 50-60 horas (2.5-3 semanas)

---

## 📅 Cronograma de 4 Semanas

### Semana 1: Import Errors Críticos (40h)

**Objetivo**: Resolver 50% dos import errors (215 de 430)

**Dia 1-2: Storyboard System (100+ erros)**
```bash
# Investigar
pytest tests/unit/test_storyboard_system_complete.py -v --tb=short > storyboard_errors.txt

# Causas possíveis:
# - app/models/storyboard.py tem imports circulares?
# - Fixtures de storyboard mal configuradas?
# - Schema validation quebrando imports?

# Ações:
# 1. Verificar imports em storyboard.py
# 2. Revisar fixtures em conftest.py
# 3. Testar imports manualmente: python -c "from app.models import Storyboard"
```

**Dia 3-4: User Permissions (50+ erros)**
```bash
pytest tests/unit/test_user_permissions.py -v --tb=short

# Ações:
# 1. Verificar app/utils/permissions.py imports
# 2. Atualizar fixtures de User + ProjectMember
# 3. Garantir Role + Permission seeders funcionam
```

**Dia 5: Utils & Validation (50+ erros)**
```bash
pytest tests/unit/test_utils.py -v --tb=short

# Ações:
# 1. Verificar decorators.py imports
# 2. Atualizar permission fixtures
# 3. Garantir schema_analyzer funciona
```

**Checkpoint Semana 1:**
- [ ] 215 import errors resolvidos (50%)
- [ ] 215 import errors restantes
- [ ] Documentar padrões encontrados

---

### Semana 2: Import Errors Restantes + Test Failures Críticos (40h)

**Objetivo**: Resolver 100% import errors + 30% test failures

**Dia 1-2: Import Errors Restantes (215 erros)**
```bash
# Testar todos arquivos com erros
pytest tests/ --collect-only 2>&1 | grep ERROR > remaining_errors.txt

# Resolver em ordem de impacto:
# 1. test_*.py com mais de 20 erros
# 2. test_*.py com 10-20 erros
# 3. test_*.py com <10 erros
```

**Dia 3-5: Test Failures Críticos (42 de 140)**
```bash
# Priorizar testes de services críticos:
pytest tests/unit/test_breakdown_service.py -v --tb=short
pytest tests/unit/test_budget_service.py -v --tb=short
pytest tests/unit/test_scene_service.py -v --tb=short

# Padrões comuns:
# 1. SQLAlchemy 2.0 mock patterns (query.get → db.session.get)
# 2. Mock objects retornando Mock ao invés de valores
# 3. Assertions esperando estrutura antiga de dados
```

**Checkpoint Semana 2:**
- [ ] 430 import errors resolvidos (100%)
- [ ] 42 test failures resolvidos (30%)
- [ ] 98 test failures restantes

---

### Semana 3: Test Failures Routes + Integration (40h)

**Objetivo**: Resolver 50% dos test failures restantes

**Dia 1-2: Route Tests (30 falhas)**
```bash
# Routes com mais falhas:
pytest tests/integration/test_breakdown_routes.py -v --tb=short
pytest tests/integration/test_budget_routes.py -v --tb=short
pytest tests/integration/test_scene_routes.py -v --tb=short

# Problemas comuns:
# 1. JWT auth não configurado em fixtures
# 2. Permissions não mockadas corretamente
# 3. Request body validation mudou
```

**Dia 3-4: Service Integration Tests (20 falhas)**
```bash
pytest tests/integration/ -k "service" -v --tb=short

# Problemas comuns:
# 1. Database não populada com seed data
# 2. Relacionamentos ORM quebrados
# 3. Transações não commitadas em fixtures
```

**Dia 5: WebSocket & Collaboration (10 falhas)**
```bash
pytest tests/unit/test_collaboration.py -v --tb=short

# Problemas comuns:
# 1. SocketIO mock não configurado
# 2. Eventos assíncronos não esperados
# 3. Room management quebrado
```

**Checkpoint Semana 3:**
- [ ] 98 test failures resolvidos (70% do total)
- [ ] 42 test failures restantes

---

### Semana 4: Test Failures Finais + Validação (20h)

**Objetivo**: Resolver 100% dos test failures + validação completa

**Dia 1-2: Últimos 42 Test Failures**
```bash
# Resolver casos edge:
pytest tests/ -v --tb=short | grep FAILED > final_failures.txt

# Abordar um por um:
for test in $(cat final_failures.txt); do
    pytest "$test" -vv --tb=long
    # Analisar, corrigir, validar
done
```

**Dia 3: Validação Completa**
```bash
# Rodar suite completa
pytest tests/ --cov=app --cov-report=html --cov-report=term -v

# Verificar:
# ✅ 0 import errors
# ✅ 0 test failures
# ✅ Taxa de sucesso: 100% (4,155/4,155)
# ✅ Coverage: 70%+ (target para Fase 5.1)
```

**Dia 4: Documentação & Refactoring**
```bash
# Documentar padrões encontrados:
# 1. SQLAlchemy 2.0 migration guide
# 2. Mock patterns guide
# 3. Fixture best practices

# Refactoring (se tempo permitir):
# 1. Consolidar fixtures duplicadas
# 2. Criar helper functions para mocks comuns
# 3. Atualizar conftest.py com novos patterns
```

**Dia 5: Buffer & Contingência**
- Resolver problemas inesperados
- Re-testar casos edge
- Preparar handoff para Semana 5 (Fase 5.1 continua)

**Checkpoint Final:**
- [ ] ✅ 4,155 testes passando (100%)
- [ ] ✅ 0 import errors
- [ ] ✅ 0 test failures
- [ ] ✅ Coverage 70%+
- [ ] ✅ Documentação de padrões completa

---

## 🔧 Ferramentas & Scripts

### Script 1: Identificar Todos os Erros

```bash
#!/bin/bash
# scripts/analyze_test_failures.sh

echo "Coletando erros de testes..."
pytest tests/ -v --tb=no 2>&1 | tee test_output.txt

echo -e "\n=== IMPORT ERRORS ===" > test_analysis.txt
grep "ERROR" test_output.txt | wc -l >> test_analysis.txt
grep "ERROR" test_output.txt >> test_analysis.txt

echo -e "\n=== TEST FAILURES ===" >> test_analysis.txt
grep "FAILED" test_output.txt | wc -l >> test_analysis.txt
grep "FAILED" test_output.txt >> test_analysis.txt

echo -e "\n=== SUMMARY ===" >> test_analysis.txt
tail -5 test_output.txt >> test_analysis.txt

cat test_analysis.txt
```

### Script 2: Corrigir Padrão SQLAlchemy 2.0

```bash
#!/bin/bash
# scripts/fix_sqlalchemy_mocks.sh

# Encontrar todos os testes com pattern antigo
find tests/ -name "*.py" -exec grep -l "mock_query.get" {} \;

# Para cada arquivo, sugerir correção
# (manual review required)
```

### Script 3: Validar Fixtures

```python
# scripts/validate_fixtures.py
"""Valida que todas as fixtures necessárias existem"""

import pytest
import sys
from pathlib import Path

# Scan all test files for @pytest.fixture usage
test_files = Path("tests").rglob("test_*.py")

required_fixtures = set()
for test_file in test_files:
    with open(test_file) as f:
        for line in f:
            if "@pytest.fixture" in line or "def test_" in line:
                # Extract fixture name from signature
                pass  # TODO: implement

# Check if fixtures exist in conftest.py
# Report missing fixtures
```

---

## 📊 Métricas de Progresso

### Dashboard Semanal

| Semana | Import Errors | Test Failures | Total Resolvido | % Completo |
|--------|---------------|---------------|-----------------|-----------|
| 0 (Baseline) | 430 | 140 | 0 | 0% |
| 1 | 215 | 140 | 215 | 38% |
| 2 | 0 | 98 | 472 | 83% |
| 3 | 0 | 42 | 528 | 93% |
| 4 | 0 | 0 | **570** | **100%** ✅ |

### Comando de Monitoramento

```bash
# Rodar diariamente para trackear progresso
pytest tests/ -q --tb=no 2>&1 | tee -a progress_log.txt

# Extrair métricas
tail -1 progress_log.txt | grep -oP '\d+ failed|\d+ error|\d+ passed'
```

---

## 🚨 Riscos & Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| **Testes com dependências externas quebram** | Alta | Alto | Mockar todas APIs externas (Claude, OpenAI, SendGrid) |
| **Database migrations quebram fixtures** | Média | Alto | Criar seed_test_db.py com dados consistentes |
| **Refatoração quebra mais testes** | Média | Médio | Fix & test incrementalmente, não big bang |
| **Fixtures compartilhadas causam race conditions** | Baixa | Alto | Usar fixtures com scope="function" |
| **4 semanas não suficientes** | Média | Crítico | Adicionar Semana 5 buffer (20h contingência) |

---

## ✅ Critérios de Conclusão

### Must-Have (Obrigatório)

- [ ] ✅ 0 import/collection errors
- [ ] ✅ 0 test failures
- [ ] ✅ 4,155 testes passando (100%)
- [ ] ✅ Nenhum teste skipped por erro (apenas por @pytest.mark.skip válido)

### Should-Have (Desejável)

- [ ] ✅ Coverage total ≥ 70%
- [ ] ✅ Todos os services críticos ≥ 80% coverage
- [ ] ✅ Documentação de padrões de teste atualizada
- [ ] ✅ conftest.py refatorado e organizado

### Nice-to-Have (Bônus)

- [ ] 📚 Guia de migration SQLAlchemy 1.x → 2.0 para testes
- [ ] 🧹 Consolidação de fixtures duplicadas
- [ ] 📊 CI/CD configurado para rodar testes automaticamente
- [ ] 🎨 Pre-commit hook para validar testes antes de commit

---

## 📞 Próximos Passos Imediatos

### Hoje (Day 1)

```bash
# 1. Executar análise completa
cd /Users/clubproducoes/Digimundo/Projeto_Digimundo/cineprod-flask
bash scripts/analyze_test_failures.sh

# 2. Começar Semana 1, Dia 1: Storyboard errors
pytest tests/unit/test_storyboard_system_complete.py -v --tb=short > storyboard_debug.txt
cat storyboard_debug.txt | grep -A 5 "ERROR"

# 3. Documentar primeiros achados
# 4. Atualizar PHASE_5.1_PROGRESS_REPORT.md
```

---

**Mantido por**: Claude Code + Equipe Digimundo
**Última Atualização**: 2025-11-16
**Versão**: 1.0
