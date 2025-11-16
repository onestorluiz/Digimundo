# ⚡ Quick Start Guides - CineProd

**Guias práticos para implementação rápida de features**

> "Do zero ao deploy em minutos, não horas"

**Data**: 2025-11-15
**Versão**: 1.0

---

## 📋 Índice

1. [Como Usar Este Guia](#como-usar-este-guia)
2. [🤖 Quick Start - AI Analysis Tools](#-quick-start---ai-analysis-tools) ⭐⭐ **NOVO**
3. [Guia 1: Adicionar Nova Scene](#guia-1-adicionar-nova-scene)
4. [Guia 2: Criar Breakdown Automático](#guia-2-criar-breakdown-automático)
5. [Guia 3: Otimizar Schedule](#guia-3-otimizar-schedule)
6. [Guia 4: Resolver Conflitos](#guia-4-resolver-conflitos)
7. [Guia 5: Deploy de Feature](#guia-5-deploy-de-feature)
8. [Guia 6: Rollback de Deploy](#guia-6-rollback-de-deploy)
9. [Guia 7: Adicionar Novo Model](#guia-7-adicionar-novo-model)
10. [Guia 8: Criar Nova Route/API](#guia-8-criar-nova-routeapi)
11. [Guia 9: Implementar WebSocket Handler](#guia-9-implementar-websocket-handler)
12. [Guia 10: Adicionar Permission RBAC](#guia-10-adicionar-permission-rbac)

---

## Como Usar Este Guia

### Estrutura de Cada Guia:

```
⏱️ Tempo estimado
📍 Arquivos afetados
🎯 Objetivo
📝 Passo a passo
✅ Como verificar se funcionou
⚠️ Armadilhas comuns
```

### Pré-requisitos:

1. ✅ Leu `00_START_HERE_CLAUDE_METHODOLOGY.md`
2. ✅ Executou checklist obrigatório (pwd, ls, cat)
3. ✅ Conhece `01_PROJECT_STRUCTURE.md`
4. ✅ Ambiente de dev configurado

---

## 🤖 Quick Start - AI Analysis Tools

⏱️ **Tempo estimado**: 5 minutos para setup, 2 minutos por análise

📍 **Scripts disponíveis**:
- `scripts/phase5/ai_semantic_analyzer.py` - Detecta duplicação semântica e dead code
- `scripts/phase5/ai_impact_analyzer.py` - Analisa impacto de mudanças

🎯 **Objetivo**: Usar IA para evitar duplicação, prever impacto, otimizar implementação

### 📝 Workflows Diários com IA

#### Workflow 1: "Antes de Criar Qualquer Código"

**Problema**: Você vai criar uma função `export_to_pdf()` em `app/services/report_service.py`

**Checklist AI-First**:

```bash
# 1. Verificar se já existe duplicação semântica no projeto
cd /Users/clubproducoes/Digimundo/Projeto_Digimundo
python3 scripts/phase5/ai_semantic_analyzer.py --duplicates --threshold 0.80

# Output esperado (filtrando por "export"):
# 🔍 GRUPOS DE DUPLICAÇÃO DETECTADOS: 1,847 grupos
#
# Grupo #7: export_to_excel (15 funções, similaridade: 100%)
# - app/services/budget_service.py:142 - export_to_excel()
# - app/services/scene_service.py:203 - export_to_excel()
# - app/services/schedule_service.py:88 - export_pdf()
# ... (mais 12 funções)
#
# 💡 RECOMENDAÇÃO: Refatorar para app/utils/excel_exporter.py
```

**Ação**: Se similaridade > 0.85, **NÃO CRIAR**. Refatorar código existente.

**ROI**: 2 minutos de análise economizam 40h de manutenção futura

---

#### Workflow 2: "Antes de Modificar Model Crítico"

**Problema**: Você vai adicionar campo `priority` no `Scene` model

**Checklist AI-First**:

```bash
# 1. Prever impacto da mudança
python3 scripts/phase5/ai_impact_analyzer.py --analyze app/models/scene.py

# Output esperado:
# 📊 ANÁLISE DE IMPACTO: app/models/scene.py
#
# Arquivos Diretamente Afetados (15):
# - app/services/scene_service.py
# - app/services/breakdown_service.py
# - app/routes/scenes.py
# - tests/unit/test_scene_service.py
# ... (mais 11 arquivos)
#
# Arquivos Indiretamente Afetados (32):
# - app/services/call_sheet_service.py (via scene_service)
# - app/services/schedule_optimizer_service.py (via scene_service)
# ... (mais 30 arquivos)
#
# ⏱️  ESTIMATIVA DE ESFORÇO:
# - Mudança no model: 0.5h
# - Atualização de services: 3.2h
# - Atualização de routes: 1.5h
# - Testes: 3.6h
# - TOTAL: 8.8h (não 2h como você pensou!)
```

**Ação**:
1. Revisar TODOS os arquivos listados
2. Ajustar estimativa de tempo (4.4x maior!)
3. Planejar mudanças em cascata

**ROI**: 2 minutos de análise evitam surpresas e retrabalho

---

#### Workflow 3: "Otimizar Ordem de Implementação"

**Problema**: Você tem 9 arquivos para criar na Fase 5.1

**Checklist AI-First**:

```bash
# 1. Descobrir ordem ótima (quais podem rodar em paralelo)
python3 scripts/phase5/ai_impact_analyzer.py --order fase_5_1

# Output esperado:
# 🎯 ORDEM OTIMIZADA - Fase 5.1
#
# Track 1 (paralelo):
# 1. event_store.py (0 deps) ✅
# 2. event.py (0 deps) ✅
# 3. event_snapshot.py (depende: event.py) ⏳
#
# Track 2 (paralelo):
# 1. cache_config.py (0 deps) ✅
# 2. redis_cache.py (depende: cache_config.py) ⏳
#
# Track 3 (paralelo):
# 1. celery_config.py (0 deps) ✅
# 2. celery_tasks.py (depende: celery_config.py) ⏳
#
# ⏱️  TIMELINE:
# - Sequencial: 9 semanas
# - Paralelizado (3 tracks): 4.5 semanas
# - ECONOMIA: 50% ⭐
```

**Ação**:
1. Dividir equipe em 3 tracks paralelos
2. Começar pelos arquivos com 0 dependências
3. Economizar 50% do tempo

**ROI**: 5 minutos de análise economizam 4.5 semanas de implementação

---

### 💡 Casos de Uso Detalhados

#### Caso 1: Evitar Duplicação de `export_to_excel()`

**Contexto**: A IA detectou 15 funções com 100% similaridade semântica

**Análise**:

```bash
python3 scripts/phase5/ai_semantic_analyzer.py --duplicates --threshold 0.95

# Output:
# 🔍 ANÁLISE DE DUPLICAÇÃO SEMÂNTICA
#
# Total de arquivos analisados: 280
# Funções analisadas: 2,347
# Grupos de duplicação encontrados: 1,847
#
# === TOP 10 GRUPOS POR IMPACTO ===
#
# Grupo #7: export_to_excel (15 funções, 100% similaridade)
# Arquivos:
# - app/services/budget_service.py:142 - export_to_excel()
# - app/services/scene_service.py:203 - export_to_excel()
# - app/services/call_sheet_service.py:95 - export_excel()
# ... (mais 12 funções)
#
# Padrão detectado:
# - Operações: criar workbook → adicionar sheet → formatar → salvar
# - Retorno: BytesIO
#
# 💡 RECOMENDAÇÃO:
# Criar app/utils/excel_exporter.py
# Economia: ~200 LOC + 40h manutenção/ano
```

**Implementação**:

```python
# app/utils/excel_exporter.py (novo arquivo, criado ANTES de duplicar)

from openpyxl import Workbook
from io import BytesIO

class ExcelExporter:
    """
    Classe centralizada para exportação Excel
    Substituiu 15 funções duplicadas (detectado por AI)
    """

    @staticmethod
    def export(data, columns, filename='export.xlsx'):
        """
        Exporta dados para Excel

        Args:
            data: List[Dict] - Dados a exportar
            columns: List[str] - Colunas desejadas
            filename: str - Nome do arquivo

        Returns:
            BytesIO - Arquivo Excel em memória
        """
        wb = Workbook()
        ws = wb.active
        ws.title = "Dados"

        # Header
        ws.append(columns)

        # Data
        for row in data:
            ws.append([row.get(col, '') for col in columns])

        # Save to BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        return output
```

**Uso nos services**:

```python
# app/services/budget_service.py (refatorado)

from app.utils.excel_exporter import ExcelExporter

class BudgetService:
    def export_to_excel(self, budget_id):
        budget = Budget.query.get(budget_id)

        data = [item.to_dict() for item in budget.items]
        columns = ['description', 'category', 'amount', 'status']

        # ANTES (duplicado): 15 linhas de código openpyxl
        # DEPOIS (refatorado): 1 linha
        return ExcelExporter.export(data, columns, f'budget_{budget_id}.xlsx')
```

**Resultado**:
- ✅ -200 linhas duplicadas
- ✅ -40h manutenção futura (8 files × 5h cada)
- ✅ +1 ponto de verdade
- ✅ ROI: 80x (40h economizadas / 0.5h refatoração)

---

#### Caso 2: Estimar Refatoração de `Scene` Model

**Contexto**: Você quer adicionar `priority` field no Scene

**Análise**:

```bash
python3 scripts/phase5/ai_impact_analyzer.py --analyze app/models/scene.py --verbose

# Output detalhado:
# 📊 ANÁLISE DE IMPACTO COMPLETO
#
# ┌─────────────────────────────────────────┐
# │ GRAFO DE DEPENDÊNCIAS (3 níveis)       │
# └─────────────────────────────────────────┘
#
# Nível 1 (Direto): 15 arquivos
# ├─ app/services/scene_service.py (38 referências)
# ├─ app/services/breakdown_service.py (22 refs)
# ├─ app/routes/scenes.py (18 refs)
# ├─ tests/unit/test_scene_service.py (45 refs)
# └─ ... (mais 11)
#
# Nível 2 (Indireto): 32 arquivos
# ├─ app/services/call_sheet_service.py
# │   └─ via scene_service.py
# ├─ app/services/schedule_optimizer_service.py
# │   └─ via scene_service.py
# └─ ... (mais 30)
#
# Nível 3 (Cascata): 8 arquivos
# └─ Frontend components usando API
#
# ⏱️  ESTIMATIVA DETALHADA:
# ┌──────────────────────────┬──────────┐
# │ Tarefa                   │ Tempo    │
# ├──────────────────────────┼──────────┤
# │ Adicionar field no model │ 0.5h     │
# │ Migration + rollback     │ 0.5h     │
# │ Atualizar services (15)  │ 3.2h     │
# │ Atualizar routes (5)     │ 1.5h     │
# │ Atualizar testes (8)     │ 3.6h     │
# │ Frontend (opcional)      │ 2.0h     │
# ├──────────────────────────┼──────────┤
# │ TOTAL                    │ 11.3h    │
# └──────────────────────────┴──────────┘
#
# 🎯 RECOMENDAÇÕES:
# 1. Testar migration em staging primeiro
# 2. Atualizar tests ANTES de services (TDD)
# 3. Deploy gradual (feature flag)
# 4. Monitorar performance (Scene é hot path)
```

**Ação**:
1. Ajustar estimativa: 2h → 11.3h (5.65x mais realista!)
2. Planejar cascata de mudanças
3. Testar em staging primeiro

**ROI**: 2 minutos de análise evitam surpresas de 9h extras

---

### ⚡ Comandos Quick Reference

```bash
# Detectar duplicação semântica
python3 scripts/phase5/ai_semantic_analyzer.py --duplicates --threshold 0.85

# Detectar código morto
python3 scripts/phase5/ai_semantic_analyzer.py --dead-code

# Analisar padrões arquiteturais
python3 scripts/phase5/ai_semantic_analyzer.py --patterns

# Analisar impacto de mudança em arquivo
python3 scripts/phase5/ai_impact_analyzer.py --analyze app/models/scene.py

# Detectar dependências circulares
python3 scripts/phase5/ai_impact_analyzer.py --circular

# Otimizar ordem de implementação de fase
python3 scripts/phase5/ai_impact_analyzer.py --order fase_5_1

# Análise completa (todos os modos)
python3 scripts/phase5/ai_semantic_analyzer.py --duplicates --dead-code --patterns
```

### 🔗 Integração com Ferramentas Existentes

**Usar ANTES de**:
- ✅ `scripts/phase5/check_file_exists.py` - Para evitar duplicatas
- ✅ Git commit - Para verificar impacto de mudanças
- ✅ Pull request - Para validar que não está introduzindo duplicação
- ✅ Estimativas de tempo - Para ser 4-5x mais preciso

**Usar DEPOIS de**:
- ❌ Criar código duplicado (tarde demais!)
- ❌ Quebrar 47 arquivos sem saber (surpresa!)

### 📚 Documentação Completa

- **Estratégia**: [`AI_STRATEGY_MASTER.md`](AI_STRATEGY_MASTER.md)
- **Descobertas**: [`AI_INSIGHTS_REPORT.md`](AI_INSIGHTS_REPORT.md)
- **Implementação**: [`AI_POWERED_ANALYSIS.md`](AI_POWERED_ANALYSIS.md)
- **Guia de uso**: [`QUICK_START_GUIDE.md`](QUICK_START_GUIDE.md) (scripts)

### ⚠️ Armadilhas Comuns com IA

1. **Ignorar threshold < 0.85**
   - ❌ "80% de similaridade não é duplicação"
   - ✅ 80% já indica padrão compartilhável

2. **Não rodar ANTES de criar código**
   - ❌ Criar primeiro, analisar depois
   - ✅ Analisar primeiro, criar se necessário

3. **Desconfiar das estimativas da IA**
   - ❌ "A IA está exagerando, 2h é suficiente"
   - ✅ A IA analisa 280 arquivos em 10s, você analisa 5 em 10min

4. **Não paralelizar quando possível**
   - ❌ Implementar sequencialmente por hábito
   - ✅ Seguir sugestão de tracks paralelos (50% economia)

**Resultado esperado**: -30% tempo de implementação, -90% duplicação introduzida, +400% precisão de estimativas

---

## Guia 1: Adicionar Nova Scene

⏱️ **Tempo estimado**: 10 minutos

📍 **Arquivos afetados**:
- `app/services/scene_service.py` (ler para entender padrão)
- Frontend: `templates/scenes/new.html` ou API client

🎯 **Objetivo**: Adicionar scene a um projeto existente

### 📝 Passo a Passo

#### 1. Via API (Recomendado)

```bash
# 1. Obter token JWT
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password"
  }' | jq -r '.access_token')

# 2. Criar scene
curl -X POST http://localhost:5000/api/v1/scenes \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "name": "CENA 01 - ESCRITÓRIO - DIA",
    "scene_number": "01",
    "location_id": 5,
    "time_of_day": "day",
    "interior_exterior": "interior",
    "description": "João entra no escritório e encontra o envelope misterioso.",
    "duration_minutes": 120,
    "cast_ids": [1, 3, 5],
    "equipment_ids": [10, 11]
  }'
```

#### 2. Via Service (Programático)

```python
# app/scripts/add_scene_example.py

from app import create_app, db
from app.services.scene_service import SceneService

app = create_app()

with app.app_context():
    scene = SceneService().create(
        project_id=1,
        data={
            'name': 'CENA 01 - ESCRITÓRIO - DIA',
            'scene_number': '01',
            'location_id': 5,
            'time_of_day': 'day',
            'interior_exterior': 'interior',
            'description': 'João entra no escritório...',
            'duration_minutes': 120
        },
        user_id=1
    )

    print(f"Scene criada: {scene.id} - {scene.name}")
```

#### 3. Via Frontend (Interface)

```html
<!-- templates/scenes/new.html -->

<form action="/scenes/create" method="POST">
    <input type="hidden" name="project_id" value="{{ project.id }}">

    <label>Número da Cena:</label>
    <input type="text" name="scene_number" required>

    <label>Nome:</label>
    <input type="text" name="name" placeholder="EX: CENA 01 - ESCRITÓRIO - DIA" required>

    <label>Locação:</label>
    <select name="location_id">
        {% for location in locations %}
        <option value="{{ location.id }}">{{ location.name }}</option>
        {% endfor %}
    </select>

    <label>Int/Ext:</label>
    <select name="interior_exterior">
        <option value="interior">Interior</option>
        <option value="exterior">Exterior</option>
    </select>

    <label>Dia/Noite:</label>
    <select name="time_of_day">
        <option value="day">Dia</option>
        <option value="night">Noite</option>
        <option value="sunset">Pôr do Sol</option>
        <option value="dawn">Amanhecer</option>
    </select>

    <button type="submit">Criar Scene</button>
</form>
```

### ✅ Como Verificar

```bash
# 1. Verificar no banco
venv/bin/python3 << EOF
from app import create_app, db
from app.models.scene import Scene

app = create_app()
with app.app_context():
    scene = Scene.query.filter_by(name='CENA 01 - ESCRITÓRIO - DIA').first()
    print(f"Scene encontrada: {scene.id} - {scene.name}")
    print(f"Locação: {scene.location.name}")
    print(f"Cast: {[actor.name for actor in scene.cast]}")
EOF

# 2. Verificar via API
curl -X GET http://localhost:5000/api/v1/scenes/1 \
  -H "Authorization: Bearer $TOKEN"
```

### ⚠️ Armadilhas Comuns

1. **Esquecer de associar cast/equipment**
   - Solução: Sempre passar `cast_ids` e `equipment_ids`

2. **project_id inválido**
   - Solução: Verificar que projeto existe antes

3. **Duplicar scene_number**
   - Solução: Implementar validação única por projeto

---

## Guia 2: Criar Breakdown Automático

⏱️ **Tempo estimado**: 15 minutos

📍 **Arquivos afetados**:
- `app/services/breakdown_service.py`
- `app/ai/script_analyzer.py`

🎯 **Objetivo**: Gerar breakdown automático de um roteiro

### 📝 Passo a Passo

#### 1. Upload de Roteiro

```python
# app/services/breakdown_service.py

class BreakdownService:
    def auto_breakdown_from_script(self, script_id, project_id, user_id):
        """
        Gerar breakdown automático usando AI
        """
        from app.ai.script_analyzer import ScriptAnalyzer

        script = Script.query.get(script_id)

        # 1. Analisar roteiro com AI
        analyzer = ScriptAnalyzer()
        analysis = analyzer.analyze(script.content)

        # 2. Criar scenes detectadas
        scenes_created = []

        for scene_data in analysis['scenes']:
            scene = self.create_scene(
                project_id=project_id,
                name=scene_data['heading'],
                description=scene_data['description'],
                scene_number=scene_data['number'],
                location=scene_data['location'],
                time_of_day=scene_data['time_of_day'],
                user_id=user_id
            )
            scenes_created.append(scene)

        # 3. Detectar personagens
        for character_data in analysis['characters']:
            character = self.create_character(
                project_id=project_id,
                name=character_data['name'],
                description=character_data['description']
            )

        # 4. Associar personagens a scenes
        for scene, scene_data in zip(scenes_created, analysis['scenes']):
            for char_name in scene_data['characters']:
                character = Character.query.filter_by(
                    project_id=project_id,
                    name=char_name
                ).first()

                if character:
                    scene.cast.append(character)

        db.session.commit()

        return {
            'scenes_created': len(scenes_created),
            'characters_detected': len(analysis['characters']),
            'locations_detected': len(set(s['location'] for s in analysis['scenes']))
        }
```

#### 2. Usar via API

```bash
# 1. Upload script
curl -X POST http://localhost:5000/api/v1/scripts \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@roteiro.pdf" \
  -F "project_id=1"

# 2. Gerar breakdown automático
curl -X POST http://localhost:5000/api/v1/breakdown/auto \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "script_id": 1,
    "project_id": 1
  }'
```

### ✅ Como Verificar

```bash
# Verificar scenes criadas
curl -X GET http://localhost:5000/api/v1/projects/1/scenes \
  -H "Authorization: Bearer $TOKEN" | jq '.scenes | length'

# Verificar personagens detectados
curl -X GET http://localhost:5000/api/v1/projects/1/characters \
  -H "Authorization: Bearer $TOKEN" | jq
```

### ⚠️ Armadilhas Comuns

1. **Roteiro mal formatado**
   - Solução: Validar formato (Fountain, Final Draft)

2. **AI não detecta todas as scenes**
   - Solução: Permitir edição manual após breakdown

3. **Personagens duplicados**
   - Solução: Normalizar nomes (JOÃO vs João vs joão)

---

## Guia 3: Otimizar Schedule

⏱️ **Tempo estimado**: 20 minutos

📍 **Arquivos afetados**:
- `app/services/scheduling_service.py` (futuro: `cp_scheduler_service.py`)

🎯 **Objetivo**: Otimizar schedule usando Constraint Programming

### 📝 Passo a Passo

#### 1. Implementar CP Scheduler (Fase 2 do Master Plan)

```python
# app/services/cp_scheduler_service.py

from ortools.sat.python import cp_model

class CPSchedulerService:
    def optimize_schedule(self, project_id):
        """
        Usar Google OR-Tools para otimizar schedule
        """
        model = cp_model.CpModel()

        scenes = Scene.query.filter_by(project_id=project_id).all()
        max_days = 60

        # Variáveis: day[scene_id] = dia escolhido (0-59)
        scene_days = {}
        for scene in scenes:
            scene_days[scene.id] = model.NewIntVar(0, max_days - 1, f'day_{scene.id}')

        # CONSTRAINT 1: Ator não pode estar em 2 places no mesmo dia
        for actor in Actor.query.join(Scene.cast).filter(Scene.project_id == project_id).distinct().all():
            scenes_with_actor = [s for s in scenes if actor in s.cast]

            for i, scene1 in enumerate(scenes_with_actor):
                for scene2 in scenes_with_actor[i+1:]:
                    # Se ambas no mesmo dia, forçar locações próximas OU bloquear
                    model.Add(scene_days[scene1.id] != scene_days[scene2.id])

        # CONSTRAINT 2: Locação: Agrupar scenes da mesma locação em dias consecutivos
        for location in Location.query.join(Scene).filter(Scene.project_id == project_id).distinct().all():
            scenes_at_location = [s for s in scenes if s.location_id == location.id]

            if len(scenes_at_location) > 1:
                # Minimizar span de dias
                min_day = model.NewIntVar(0, max_days, f'loc_{location.id}_min')
                max_day = model.NewIntVar(0, max_days, f'loc_{location.id}_max')

                for scene in scenes_at_location:
                    model.AddMinEquality(min_day, [scene_days[s.id] for s in scenes_at_location])
                    model.AddMaxEquality(max_day, [scene_days[s.id] for s in scenes_at_location])

                # Penalizar span grande
                span = model.NewIntVar(0, max_days, f'loc_{location.id}_span')
                model.Add(span == max_day - min_day)
                model.Minimize(span * 10)  # Custo de logística

        # CONSTRAINT 3: Ordem de roteiro (opcional)
        # Se diretor quer filmar em ordem
        if project.shoot_in_script_order:
            for i in range(len(scenes) - 1):
                model.Add(scene_days[scenes[i].id] <= scene_days[scenes[i+1].id])

        # Resolver
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            # Aplicar solução
            for scene in scenes:
                day = solver.Value(scene_days[scene.id])
                scene.shooting_date = project.start_date + timedelta(days=day)

            db.session.commit()

            return {
                'status': 'optimized',
                'scenes_scheduled': len(scenes),
                'total_days': max(solver.Value(d) for d in scene_days.values()) + 1
            }
        else:
            return {'status': 'infeasible', 'reason': 'Constraints cannot be satisfied'}
```

#### 2. Usar via API

```bash
curl -X POST http://localhost:5000/api/v1/schedule/optimize \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "constraints": {
      "shoot_in_order": false,
      "group_by_location": true,
      "avoid_actor_conflicts": true
    }
  }'
```

### ✅ Como Verificar

```bash
# Ver schedule otimizado
curl -X GET http://localhost:5000/api/v1/schedule/calendar/1 \
  -H "Authorization: Bearer $TOKEN" | jq

# Verificar conflitos
curl -X GET http://localhost:5000/api/v1/schedule/conflicts/1 \
  -H "Authorization: Bearer $TOKEN"
```

### ⚠️ Armadilhas Comuns

1. **Solver não acha solução**
   - Solução: Relaxar constraints (permitir alguns conflitos com penalidade)

2. **Otimização lenta (>10s)**
   - Solução: Limitar número de scenes (processar em batches)

---

## Guia 4: Resolver Conflitos

⏱️ **Tempo estimado**: 10 minutos

📍 **Arquivos afetados**:
- `app/services/conflict_detection_service.py`

🎯 **Objetivo**: Detectar e resolver conflitos de schedule

### 📝 Passo a Passo

#### 1. Detectar Conflitos

```python
# app/services/conflict_detection_service.py

class ConflictDetectionService:
    def detect_all_conflicts(self, project_id):
        """
        Detectar todos os tipos de conflitos
        """
        conflicts = []

        scenes = Scene.query.filter_by(project_id=project_id).all()

        # CONFLITO 1: Ator em 2 lugares no mesmo dia
        for scene in scenes:
            if not scene.shooting_date:
                continue

            for actor in scene.cast:
                other_scenes = Scene.query.filter(
                    Scene.shooting_date == scene.shooting_date,
                    Scene.id != scene.id,
                    Scene.cast.contains(actor)
                ).all()

                if other_scenes:
                    conflicts.append({
                        'type': 'actor_double_booking',
                        'severity': 'high',
                        'scene_id': scene.id,
                        'actor': actor.name,
                        'conflicting_scenes': [s.id for s in other_scenes]
                    })

        # CONFLITO 2: Equipamento em 2 lugares
        # Similar ao actor

        # CONFLITO 3: Locação com permissão vencida
        for scene in scenes:
            if scene.location and scene.location.permit_expiry_date:
                if scene.shooting_date > scene.location.permit_expiry_date:
                    conflicts.append({
                        'type': 'location_permit_expired',
                        'severity': 'critical',
                        'scene_id': scene.id,
                        'location': scene.location.name
                    })

        return conflicts
```

#### 2. Resolver Automaticamente

```python
def auto_resolve_conflict(self, conflict):
    """
    Resolver conflito automaticamente
    """
    if conflict['type'] == 'actor_double_booking':
        # Estratégia: Mover scene para próximo dia disponível
        scene = Scene.query.get(conflict['scene_id'])

        # Achar próximo dia sem conflito
        next_available_day = self._find_next_available_day(
            scene=scene,
            actor_id=conflict['actor_id'],
            start_from=scene.shooting_date
        )

        # Mover scene
        scene.shooting_date = next_available_day
        db.session.commit()

        return {'status': 'resolved', 'new_date': next_available_day}

    elif conflict['type'] == 'location_permit_expired':
        # Estratégia: Notificar produtor
        NotificationService().send_to_producer(
            project_id=scene.project_id,
            message=f"⚠️ Permissão da locação '{scene.location.name}' vencida!"
        )

        return {'status': 'notification_sent'}
```

### ✅ Como Verificar

```bash
# Detectar conflitos
curl -X GET http://localhost:5000/api/v1/conflicts/detect/1 \
  -H "Authorization: Bearer $TOKEN" | jq

# Resolver conflitos
curl -X POST http://localhost:5000/api/v1/conflicts/resolve \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "auto_resolve": true
  }'
```

---

## Guia 5: Deploy de Feature

⏱️ **Tempo estimado**: 15 minutos

📍 **Arquivos afetados**:
- `.git/`
- VPS: `/opt/cineprod/`

🎯 **Objetivo**: Deploy seguro para production

### 📝 Passo a Passo

```bash
# 1. Commit changes
git add .
git commit -m "feat: Adicionar conflict detection service

- Implementa ConflictDetectionService
- Detecta actor double booking
- Detecta location permit expiry
- Auto-resolve de conflitos simples

Closes #42"

# 2. Push para GitHub
git push origin github-main

# 3. SSH no VPS
ssh root@82.25.74.142

# 4. Pull no servidor
cd /opt/cineprod
git pull origin github-main

# 5. Ativar venv e instalar deps
source venv/bin/activate
pip install -r requirements.txt

# 6. Rodar migrations
flask db upgrade

# 7. Restart service
systemctl restart cineprod

# 8. Verificar health
curl http://localhost:5000/health

# 9. Ver logs
journalctl -u cineprod -f
```

### ✅ Como Verificar

```bash
# Health check
curl http://82.25.74.142/health

# Test endpoint
curl http://82.25.74.142/api/v1/conflicts/detect/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## Guia 6: Rollback de Deploy

⏱️ **Tempo estimado**: 5 minutos

📍 **Arquivos afetados**:
- `.git/`
- VPS

🎯 **Objetivo**: Reverter deploy com problema

### 📝 Passo a Passo

```bash
# 1. SSH no VPS
ssh root@82.25.74.142

# 2. Ver commits recentes
cd /opt/cineprod
git log --oneline -10

# 3. Rollback para commit anterior
git revert HEAD  # Cria commit reverso

# OU reset hard (CUIDADO!)
git reset --hard <commit-hash-anterior>

# 4. Rollback de migration (se necessário)
flask db downgrade

# 5. Restart
systemctl restart cineprod

# 6. Verificar
journalctl -u cineprod -f
```

---

## Guia 7: Adicionar Novo Model

⏱️ **Tempo estimado**: 20 minutos

📍 **Arquivos afetados**:
- `app/models/new_model.py` (criar)
- `app/models/__init__.py` (import)

🎯 **Objetivo**: Criar novo modelo no banco

### 📝 Passo a Passo

#### 1. Criar Model

```python
# app/models/call_sheet.py

from app import db
from datetime import datetime

class CallSheet(db.Model):
    __tablename__ = 'call_sheets'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    call_time = db.Column(db.Time, nullable=False)
    wrap_time = db.Column(db.Time)

    # Relationships
    project = db.relationship('Project', backref='call_sheets')
    scenes = db.relationship('Scene', secondary='call_sheet_scenes')

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'date': self.date.isoformat(),
            'call_time': self.call_time.isoformat(),
            'scenes': [s.to_dict() for s in self.scenes]
        }

# Tabela associativa
call_sheet_scenes = db.Table('call_sheet_scenes',
    db.Column('call_sheet_id', db.Integer, db.ForeignKey('call_sheets.id')),
    db.Column('scene_id', db.Integer, db.ForeignKey('scenes.id'))
)
```

#### 2. Registrar Model

```python
# app/models/__init__.py

from app.models.call_sheet import CallSheet

__all__ = ['CallSheet', 'Scene', 'Project', ...]
```

#### 3. Criar Migration

```bash
# Gerar migration
flask db revision -m "Add CallSheet model"

# Editar migration gerada (migrations/versions/xxxx_add_call_sheet_model.py)
def upgrade():
    op.create_table('call_sheets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('call_time', sa.Time(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('call_sheets')

# Aplicar migration
flask db upgrade
```

### ✅ Como Verificar

```bash
# Verificar no banco
venv/bin/python3 << EOF
from app import create_app, db
from app.models.call_sheet import CallSheet

app = create_app()
with app.app_context():
    # Criar call sheet de teste
    cs = CallSheet(
        project_id=1,
        date='2025-01-15',
        call_time='08:00'
    )
    db.session.add(cs)
    db.session.commit()

    print(f"Call sheet criado: {cs.id}")
EOF
```

---

## Guia 8: Criar Nova Route/API

⏱️ **Tempo estimado**: 15 minutos

📍 **Arquivos afetados**:
- `app/api/v4/new_route.py` (criar)
- `app/api/v4/__init__.py`

🎯 **Objetivo**: Expor nova funcionalidade via API

### 📝 Passo a Passo

```python
# app/api/v4/call_sheets.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.call_sheet_service import CallSheetService
from app.decorators import permission_required

bp = Blueprint('call_sheets', __name__, url_prefix='/api/v4/call-sheets')

@bp.route('/', methods=['POST'])
@jwt_required()
@permission_required('create_call_sheet')
def create_call_sheet():
    """
    Criar novo call sheet

    POST /api/v4/call-sheets
    {
        "project_id": 1,
        "date": "2025-01-15",
        "call_time": "08:00",
        "scene_ids": [1, 2, 3]
    }
    """
    data = request.json
    user_id = get_jwt_identity()

    try:
        call_sheet = CallSheetService().create(
            project_id=data['project_id'],
            date=data['date'],
            call_time=data['call_time'],
            scene_ids=data.get('scene_ids', []),
            user_id=user_id
        )

        return jsonify(call_sheet.to_dict()), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_call_sheet(id):
    """
    Buscar call sheet por ID
    """
    call_sheet = CallSheet.query.get_or_404(id)

    # Verificar permissão de acesso
    if not can_access_project(get_jwt_identity(), call_sheet.project_id):
        return jsonify({'error': 'Forbidden'}), 403

    return jsonify(call_sheet.to_dict())
```

Registrar blueprint:

```python
# app/api/v4/__init__.py

from app.api.v4.call_sheets import bp as call_sheets_bp

def register_blueprints(app):
    app.register_blueprint(call_sheets_bp)
```

### ✅ Como Verificar

```bash
# Test endpoint
curl -X POST http://localhost:5000/api/v4/call-sheets \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "date": "2025-01-15",
    "call_time": "08:00",
    "scene_ids": [1, 2]
  }'
```

---

## Guia 9: Implementar WebSocket Handler

⏱️ **Tempo estimado**: 20 minutos

📍 **Arquivos afetados**:
- `app/sockets/new_handler.py`

🎯 **Objetivo**: Adicionar handler WebSocket para real-time

### 📝 Passo a Passo

```python
# app/sockets/scene_collaboration.py

from flask_socketio import emit, join_room, leave_room
from app import socketio
from flask_jwt_extended import decode_token

@socketio.on('join_scene')
def handle_join_scene(data):
    """
    Cliente entra em room de colaboração de scene

    Evento: join_scene
    Data: { scene_id: 1, token: "JWT_TOKEN" }
    """
    try:
        # Validar token
        token_data = decode_token(data['token'])
        user_id = token_data['sub']

        scene_id = data['scene_id']
        room = f'scene_{scene_id}'

        # Entrar na room
        join_room(room)

        # Notificar outros usuários
        emit('user_joined', {
            'user_id': user_id,
            'scene_id': scene_id,
            'timestamp': datetime.utcnow().isoformat()
        }, room=room, skip_sid=request.sid)

        # Confirmar para cliente
        emit('joined_scene', {
            'scene_id': scene_id,
            'active_users': get_active_users_in_room(room)
        })

    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('scene_edit')
def handle_scene_edit(data):
    """
    Cliente editou campo da scene

    Evento: scene_edit
    Data: {
        scene_id: 1,
        field: "description",
        value: "Novo texto",
        cursor_position: 42
    }
    """
    scene_id = data['scene_id']
    room = f'scene_{scene_id}'

    # Broadcast para outros usuários na mesma room
    emit('scene_updated', {
        'scene_id': scene_id,
        'field': data['field'],
        'value': data['value'],
        'user_id': get_current_user_id(),
        'timestamp': datetime.utcnow().isoformat()
    }, room=room, skip_sid=request.sid)

    # Persistir no banco (opcional - depende de estratégia CRDT)
    from app.services.scene_service import SceneService
    SceneService().update(scene_id, {data['field']: data['value']})
```

Frontend:

```javascript
// static/js/scene_collaboration.js

const socket = io();

// Entrar em room
socket.emit('join_scene', {
    scene_id: currentSceneId,
    token: localStorage.getItem('access_token')
});

// Escutar updates de outros usuários
socket.on('scene_updated', (data) => {
    if (data.field === 'description') {
        document.getElementById('scene-description').value = data.value;
    }

    showNotification(`${data.user_id} editou ${data.field}`);
});

// Enviar edit
document.getElementById('scene-description').addEventListener('input', (e) => {
    socket.emit('scene_edit', {
        scene_id: currentSceneId,
        field: 'description',
        value: e.target.value
    });
});
```

---

## Guia 10: Adicionar Permission RBAC

⏱️ **Tempo estimado**: 10 minutos

📍 **Arquivos afetados**:
- `app/models/permission.py`
- `app/decorators/permission_required.py`

🎯 **Objetivo**: Adicionar nova permissão ao sistema

### 📝 Passo a Passo

#### 1. Definir Permission

```python
# app/config/permissions.py

PERMISSIONS = {
    # ... existing permissions ...

    'create_call_sheet': {
        'name': 'Criar Call Sheet',
        'description': 'Permissão para criar call sheets',
        'category': 'call_sheets'
    },

    'edit_call_sheet': {
        'name': 'Editar Call Sheet',
        'description': 'Permissão para editar call sheets',
        'category': 'call_sheets'
    },
}
```

#### 2. Seed Permissions no Banco

```python
# app/scripts/seed_permissions.py

from app import create_app, db
from app.models.permission import Permission
from app.config.permissions import PERMISSIONS

app = create_app()

with app.app_context():
    for key, data in PERMISSIONS.items():
        perm = Permission.query.filter_by(key=key).first()

        if not perm:
            perm = Permission(
                key=key,
                name=data['name'],
                description=data['description'],
                category=data['category']
            )
            db.session.add(perm)

    db.session.commit()
    print("Permissions seeded!")
```

#### 3. Atribuir a Roles

```python
# Atribuir permissão ao role "Producer"
from app.models.role import Role

producer_role = Role.query.filter_by(name='Producer').first()
call_sheet_perm = Permission.query.filter_by(key='create_call_sheet').first()

producer_role.permissions.append(call_sheet_perm)
db.session.commit()
```

#### 4. Usar em Routes

```python
from app.decorators import permission_required

@bp.route('/call-sheets', methods=['POST'])
@jwt_required()
@permission_required('create_call_sheet')
def create_call_sheet():
    # Apenas usuários com permission podem acessar
    pass
```

---

## 📚 Leia Também

**Antes de implementar**:
- `00_START_HERE_CLAUDE_METHODOLOGY.md` - Evite erros
- `01_PROJECT_STRUCTURE.md` - Onde criar arquivos

**Para entender contexto**:
- `02_IMPLEMENTATION_MASTER_PLAN.md` - Roadmap completo
- `CINEPROD_ARCHITECTURE_CORRELATIONS_DEEP_ANALYSIS.md` - Por quês

**Para deploy**:
- `04_TESTING_STRATEGY.md` - Como testar
- `05_DEPLOYMENT_PROCEDURES.md` - Como fazer deploy

---

**Criado**: 2025-11-15
**Mantido por**: Claude Code + Equipe Digimundo

---

**DIGIMUNDO PRESENTE 🥷**
