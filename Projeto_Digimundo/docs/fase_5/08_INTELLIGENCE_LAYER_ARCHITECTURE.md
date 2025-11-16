# 🧠 Intelligence Layer Architecture - CineProd

**Arquitetura Completa do Sistema de Inteligência**

> "A diferença entre um bom sistema e um sistema de classe mundial está na camada de inteligência"

**Data**: 2025-11-15
**Versão**: 1.0
**Status**: Proposta Arquitetural

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Componentes do Intelligence Layer](#componentes-do-intelligence-layer)
3. [Conflict Detection Engine](#conflict-detection-engine)
4. [Schedule Optimization Engine](#schedule-optimization-engine)
5. [Predictive Analytics Engine](#predictive-analytics-engine)
6. [Data Flow Architecture](#data-flow-architecture)
7. [Database Schema](#database-schema)
8. [API Specification](#api-specification)
9. [Integration Points](#integration-points)
10. [Performance & Scalability](#performance--scalability)

---

## 🎯 VISÃO GERAL

### O Que é Intelligence Layer?

**Intelligence Layer** é uma camada de software que adiciona capacidades cognitivas ao CineProd:

```
┌─────────────────────────────────────────────┐
│         PRESENTATION LAYER (UI/UX)          │
│     (Dashboard, Forms, Visualizations)      │
└─────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────┐
│        🧠 INTELLIGENCE LAYER (NEW!)         │
│  ┌─────────────────────────────────────┐   │
│  │  Conflict Detection Engine          │   │
│  ├─────────────────────────────────────┤   │
│  │  Schedule Optimization Engine       │   │
│  ├─────────────────────────────────────┤   │
│  │  Predictive Analytics Engine        │   │
│  ├─────────────────────────────────────┤   │
│  │  Recommendation Engine              │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────┐
│         BUSINESS LOGIC LAYER                │
│     (Services, Workflows, Validations)      │
└─────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────┐
│            DATA LAYER (Models)              │
│    (PostgreSQL, Redis, Event Store)         │
└─────────────────────────────────────────────┘
```

### Objetivos

1. **Detecção Proativa**: Identificar problemas ANTES de acontecerem
2. **Otimização Automática**: Sugerir melhorias no schedule
3. **Predição**: Antecipar delays, overruns, burnout
4. **Recomendação**: Guiar usuário para melhores decisões

### Inspirações Arquiteturais

| Sistema | Conceito Aplicado | Como usamos |
|---------|-------------------|-------------|
| **BIM/CAD** | Clash Detection | Conflict Detection multi-dimensional |
| **Hospital Scheduling** | Nash Equilibrium | Resource allocation optimization |
| **Google Maps** | Route Optimization | Schedule path optimization |
| **Netflix** | Recommendation Engine | Scene sequence suggestions |
| **Waze** | Predictive Traffic | Predictive delays & conflicts |

---

## 🔧 COMPONENTES DO INTELLIGENCE LAYER

### 1. Conflict Detection Engine

**Responsabilidade**: Detectar conflitos de recursos em tempo real

**Inputs**:
- Scene schedule (dates, times)
- Crew assignments
- Equipment allocations
- Location reservations
- Budget allocations

**Outputs**:
- Lista de conflitos (tipo, severidade, entidades)
- Sugestões de resolução
- Impacto financeiro estimado

**Algoritmos**:
- Graph-based conflict detection
- Temporal overlap analysis
- Resource availability checking

---

### 2. Schedule Optimization Engine

**Responsabilidade**: Otimizar sequência de scenes no stripboard

**Inputs**:
- All scenes com metadata
- Constraints (crew availability, location permits)
- Optimization goals (minimize cost, minimize days, balance workload)

**Outputs**:
- Sequência otimizada de scenes
- Comparação (manual vs otimizado)
- Métricas de melhoria

**Algoritmos**:
- Genetic Algorithm (GA)
- Constraint Programming (CP)
- Simulated Annealing
- Greedy heuristics (MVP)

---

### 3. Predictive Analytics Engine

**Responsabilidade**: Prever problemas futuros

**Inputs**:
- Historical data (projetos passados)
- Current project metrics
- Production velocity
- Spending rate

**Outputs**:
- Budget overrun probability
- Schedule delay probability
- Crew burnout risk score
- Quality risk score

**Algoritmos**:
- Time series forecasting (ARIMA)
- Regression models
- Anomaly detection
- Monte Carlo simulation

---

### 4. Recommendation Engine

**Responsabilidade**: Sugerir próximas ações

**Inputs**:
- Current project state
- User behavior patterns
- Industry best practices

**Outputs**:
- Next best action
- Alternative options
- Expected outcomes

**Algoritmos**:
- Collaborative filtering
- Content-based filtering
- Reinforcement learning (futuro)

---

## 🔍 CONFLICT DETECTION ENGINE (Detalhado)

### Arquitetura

```python
# app/intelligence/conflict_detection/

├── __init__.py
├── engine.py                    # Main engine
├── detectors/
│   ├── __init__.py
│   ├── crew_detector.py         # Crew conflicts
│   ├── equipment_detector.py    # Equipment conflicts
│   ├── location_detector.py     # Location conflicts
│   ├── budget_detector.py       # Budget conflicts
│   └── weather_detector.py      # Weather conflicts
├── resolvers/
│   ├── __init__.py
│   ├── auto_resolver.py         # Auto-resolution logic
│   └── suggestion_generator.py  # Generate suggestions
├── models/
│   ├── conflict.py              # Conflict model
│   └── resolution.py            # Resolution model
└── utils/
    ├── graph.py                 # Graph utilities
    └── temporal.py              # Temporal analysis
```

### Conflict Model

```python
# app/intelligence/conflict_detection/models/conflict.py

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class ConflictType(Enum):
    CREW_DOUBLE_BOOKING = 'crew_double_booking'
    EQUIPMENT_UNAVAILABLE = 'equipment_unavailable'
    LOCATION_CONFLICT = 'location_conflict'
    LOCATION_PERMIT_EXPIRED = 'location_permit_expired'
    BUDGET_OVERRUN = 'budget_overrun'
    WEATHER_RISK = 'weather_risk'
    SCHEDULE_OVERLAP = 'schedule_overlap'

class ConflictSeverity(Enum):
    CRITICAL = 'critical'  # Blocker - não pode filmar
    HIGH = 'high'          # Problema sério - $$$
    MEDIUM = 'medium'      # Inconveniência - $
    LOW = 'low'            # Warning apenas

@dataclass
class Conflict:
    """
    Representa um conflito detectado
    """
    id: str
    type: ConflictType
    severity: ConflictSeverity
    date: datetime
    entities: Dict
    description: str
    resolution_suggestions: List[Dict]
    cost_impact: float
    detected_at: datetime
    resolved_at: Optional[datetime] = None
    resolution_applied: Optional[Dict] = None

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'type': self.type.value,
            'severity': self.severity.value,
            'date': self.date.isoformat(),
            'entities': self.entities,
            'description': self.description,
            'resolution_suggestions': self.resolution_suggestions,
            'cost_impact': self.cost_impact,
            'detected_at': self.detected_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolution_applied': self.resolution_applied
        }

    @property
    def is_resolved(self) -> bool:
        return self.resolved_at is not None

    @property
    def age_hours(self) -> float:
        """Quantas horas desde detecção"""
        delta = datetime.now() - self.detected_at
        return delta.total_seconds() / 3600
```

### Main Engine

```python
# app/intelligence/conflict_detection/engine.py

from typing import List, Dict, Optional
from datetime import datetime, date
from app.intelligence.conflict_detection.detectors import (
    CrewDetector,
    EquipmentDetector,
    LocationDetector,
    BudgetDetector,
    WeatherDetector
)
from app.intelligence.conflict_detection.models.conflict import Conflict
from app.intelligence.conflict_detection.resolvers import SuggestionGenerator
from app.models.project import Project
import logging

logger = logging.getLogger(__name__)

class ConflictDetectionEngine:
    """
    Engine principal de detecção de conflitos

    Coordena múltiplos detectores especializados e gera relatório consolidado
    """

    def __init__(self):
        self.detectors = [
            CrewDetector(),
            EquipmentDetector(),
            LocationDetector(),
            BudgetDetector(),
            WeatherDetector()
        ]
        self.suggestion_generator = SuggestionGenerator()

    def detect(self, project_id: int, date_range: Optional[tuple] = None) -> Dict:
        """
        Detectar todos os conflitos de um projeto

        Args:
            project_id: ID do projeto
            date_range: (start_date, end_date) opcional para filtrar

        Returns:
            {
                'conflicts': [Conflict, ...],
                'summary': {...},
                'recommendations': [...]
            }
        """
        logger.info(f"Starting conflict detection for project {project_id}")

        project = Project.query.get(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        all_conflicts = []

        # Executar cada detector
        for detector in self.detectors:
            try:
                logger.debug(f"Running {detector.__class__.__name__}")
                conflicts = detector.detect(project, date_range)
                all_conflicts.extend(conflicts)
                logger.info(f"{detector.__class__.__name__}: {len(conflicts)} conflicts found")
            except Exception as e:
                logger.error(f"Error in {detector.__class__.__name__}: {e}")
                # Continuar com outros detectores

        # Gerar sugestões de resolução
        for conflict in all_conflicts:
            conflict.resolution_suggestions = self.suggestion_generator.generate(conflict)

        # Build report
        report = self._build_report(all_conflicts, project)

        logger.info(f"Detection complete: {len(all_conflicts)} total conflicts")

        return report

    def _build_report(self, conflicts: List[Conflict], project: Project) -> Dict:
        """
        Consolidar conflitos em relatório

        Inclui:
        - Summary statistics
        - Conflicts agrupados por tipo
        - Conflicts agrupados por severidade
        - Recommendations de alto nível
        """
        from collections import Counter

        # Estatísticas
        type_counts = Counter(c.type for c in conflicts)
        severity_counts = Counter(c.severity for c in conflicts)

        # Impacto financeiro total
        total_cost_impact = sum(c.cost_impact for c in conflicts)

        # Conflicts críticos não resolvidos
        critical_unresolved = [
            c for c in conflicts
            if c.severity == ConflictSeverity.CRITICAL and not c.is_resolved
        ]

        # Recommendations de alto nível
        recommendations = self._generate_high_level_recommendations(
            conflicts, project
        )

        return {
            'project_id': project.id,
            'project_name': project.name,
            'generated_at': datetime.now().isoformat(),
            'conflicts': [c.to_dict() for c in conflicts],
            'summary': {
                'total': len(conflicts),
                'by_severity': {
                    'critical': severity_counts[ConflictSeverity.CRITICAL],
                    'high': severity_counts[ConflictSeverity.HIGH],
                    'medium': severity_counts[ConflictSeverity.MEDIUM],
                    'low': severity_counts[ConflictSeverity.LOW]
                },
                'by_type': {
                    t.value: count for t, count in type_counts.items()
                },
                'unresolved_critical': len(critical_unresolved),
                'total_cost_impact': total_cost_impact
            },
            'recommendations': recommendations
        }

    def _generate_high_level_recommendations(
        self,
        conflicts: List[Conflict],
        project: Project
    ) -> List[Dict]:
        """
        Gerar recomendações de alto nível baseado no padrão de conflitos
        """
        recommendations = []

        # Muitos crew conflicts? Sugerir contratação
        crew_conflicts = [c for c in conflicts if c.type == ConflictType.CREW_DOUBLE_BOOKING]
        if len(crew_conflicts) > 5:
            recommendations.append({
                'priority': 'high',
                'category': 'crew',
                'title': 'Considerar contratar crew adicional',
                'description': f'{len(crew_conflicts)} conflitos de crew detectados. '
                               'Pode ser mais econômico contratar crew adicional.',
                'estimated_impact': sum(c.cost_impact for c in crew_conflicts)
            })

        # Muitos location conflicts? Sugerir revisão de schedule
        location_conflicts = [
            c for c in conflicts
            if c.type in [ConflictType.LOCATION_CONFLICT, ConflictType.LOCATION_PERMIT_EXPIRED]
        ]
        if len(location_conflicts) > 3:
            recommendations.append({
                'priority': 'critical',
                'category': 'location',
                'title': 'Revisar planejamento de locações',
                'description': f'{len(location_conflicts)} conflitos de locação. '
                               'Considerar usar Schedule Optimizer.',
                'action': 'optimize_schedule'
            })

        # Budget overrun? Alerta urgente
        budget_conflicts = [c for c in conflicts if c.type == ConflictType.BUDGET_OVERRUN]
        if budget_conflicts:
            total_overrun = sum(c.cost_impact for c in budget_conflicts)
            recommendations.append({
                'priority': 'critical',
                'category': 'budget',
                'title': 'Ação urgente: Budget overrun detectado',
                'description': f'R$ {total_overrun:,.2f} acima do orçado em {len(budget_conflicts)} categorias.',
                'action': 'review_budget'
            })

        return recommendations
```

### Detector Example: CrewDetector

```python
# app/intelligence/conflict_detection/detectors/crew_detector.py

from typing import List
from datetime import date
from collections import defaultdict
from app.intelligence.conflict_detection.models.conflict import (
    Conflict, ConflictType, ConflictSeverity
)
from app.models.project import Project
from app.models.scene import Scene
import logging

logger = logging.getLogger(__name__)

class CrewDetector:
    """
    Detecta conflitos de crew (double-booking)

    Algoritmo:
    1. Buscar todas as scenes com crew atribuído
    2. Agrupar por crew member + data
    3. Se crew em 2+ scenes no mesmo dia → CONFLICT
    """

    def detect(self, project: Project, date_range: tuple = None) -> List[Conflict]:
        """
        Detectar crew conflicts
        """
        conflicts = []

        # Buscar scenes do projeto
        scenes = Scene.query.filter_by(project_id=project.id).all()

        if date_range:
            start_date, end_date = date_range
            scenes = [s for s in scenes if s.shooting_date and start_date <= s.shooting_date <= end_date]

        # Agrupar por crew member + data
        crew_schedule = defaultdict(lambda: defaultdict(list))

        for scene in scenes:
            if not scene.shooting_date:
                continue

            for crew_member in scene.crew:
                day = scene.shooting_date.date()
                crew_schedule[crew_member.id][day].append(scene)

        # Detectar double-booking
        for crew_id, schedule in crew_schedule.items():
            for day, scenes_on_day in schedule.items():
                if len(scenes_on_day) > 1:
                    conflict = self._create_conflict(crew_id, day, scenes_on_day)
                    conflicts.append(conflict)

        logger.info(f"CrewDetector: {len(conflicts)} conflicts found")
        return conflicts

    def _create_conflict(self, crew_id: int, day: date, scenes: List[Scene]) -> Conflict:
        """
        Criar objeto Conflict para crew double-booking
        """
        from app.models.crew import Crew

        crew = Crew.query.get(crew_id)

        # Calcular impacto financeiro (overtime estimado)
        cost_impact = crew.daily_rate * 0.5  # 50% overtime

        return Conflict(
            id=f'CREW-{crew_id}-{day.isoformat()}',
            type=ConflictType.CREW_DOUBLE_BOOKING,
            severity=ConflictSeverity.HIGH,
            date=day,
            entities={
                'crew': {
                    'id': crew.id,
                    'name': crew.name,
                    'role': crew.role,
                    'daily_rate': crew.daily_rate
                },
                'scenes': [
                    {
                        'id': s.id,
                        'name': s.name,
                        'location': s.location.name if s.location else None
                    }
                    for s in scenes
                ]
            },
            description=f'{crew.name} está agendado para {len(scenes)} scenes no mesmo dia: '
                       f'{", ".join(s.name for s in scenes)}',
            resolution_suggestions=[],  # Será preenchido pelo SuggestionGenerator
            cost_impact=cost_impact,
            detected_at=datetime.now()
        )
```

### Suggestion Generator

```python
# app/intelligence/conflict_detection/resolvers/suggestion_generator.py

from typing import List, Dict
from app.intelligence.conflict_detection.models.conflict import Conflict, ConflictType
from app.models.scene import Scene
from datetime import timedelta

class SuggestionGenerator:
    """
    Gera sugestões de resolução para conflitos detectados
    """

    def generate(self, conflict: Conflict) -> List[Dict]:
        """
        Gerar sugestões baseado no tipo de conflito
        """
        if conflict.type == ConflictType.CREW_DOUBLE_BOOKING:
            return self._suggest_crew_conflict_resolution(conflict)
        elif conflict.type == ConflictType.EQUIPMENT_UNAVAILABLE:
            return self._suggest_equipment_conflict_resolution(conflict)
        elif conflict.type == ConflictType.LOCATION_PERMIT_EXPIRED:
            return self._suggest_location_permit_resolution(conflict)
        elif conflict.type == ConflictType.BUDGET_OVERRUN:
            return self._suggest_budget_resolution(conflict)
        else:
            return []

    def _suggest_crew_conflict_resolution(self, conflict: Conflict) -> List[Dict]:
        """
        Sugestões para crew double-booking
        """
        crew = conflict.entities['crew']
        scenes = conflict.entities['scenes']

        suggestions = []

        # Sugestão 1: Mover última scene para outro dia
        suggestions.append({
            'action': 'reschedule_scene',
            'description': f'Mover "{scenes[-1]["name"]}" para outro dia',
            'scene_id': scenes[-1]['id'],
            'estimated_cost': 0,  # Sem custo adicional
            'difficulty': 'easy',
            'auto_applicable': True
        })

        # Sugestão 2: Contratar crew adicional
        suggestions.append({
            'action': 'hire_additional_crew',
            'description': f'Contratar {crew["role"]} adicional',
            'estimated_cost': crew['daily_rate'],
            'difficulty': 'medium',
            'auto_applicable': False
        })

        # Sugestão 3: Combinar scenes se mesma locação
        same_location = len(set(s.get('location') for s in scenes)) == 1
        if same_location:
            suggestions.append({
                'action': 'combine_scenes',
                'description': 'Filmar ambas scenes de uma vez (mesma locação)',
                'estimated_cost': crew['daily_rate'] * 0.5,  # Overtime
                'difficulty': 'hard',
                'auto_applicable': False
            })

        return suggestions

    def _suggest_equipment_conflict_resolution(self, conflict: Conflict) -> List[Dict]:
        """
        Sugestões para equipment unavailable
        """
        equipment = conflict.entities['equipment']

        return [
            {
                'action': 'reschedule_scene',
                'description': 'Mover scene para quando equipamento estiver disponível',
                'auto_applicable': True
            },
            {
                'action': 'rent_additional_equipment',
                'description': f'Alugar {equipment["name"]} adicional',
                'estimated_cost': equipment.get('rental_cost', 0),
                'auto_applicable': False
            },
            {
                'action': 'use_alternative_equipment',
                'description': 'Usar equipamento alternativo',
                'auto_applicable': False
            }
        ]

    def _suggest_location_permit_resolution(self, conflict: Conflict) -> List[Dict]:
        """
        Sugestões para location permit expired
        """
        return [
            {
                'action': 'renew_permit',
                'description': 'Renovar permissão da locação',
                'priority': 'critical',
                'auto_applicable': False
            },
            {
                'action': 'reschedule_scene',
                'description': 'Mover scene para antes do vencimento',
                'auto_applicable': True
            },
            {
                'action': 'change_location',
                'description': 'Trocar para locação alternativa',
                'auto_applicable': False
            }
        ]

    def _suggest_budget_resolution(self, conflict: Conflict) -> List[Dict]:
        """
        Sugestões para budget overrun
        """
        item = conflict.entities['budget_item']
        overrun_amount = conflict.cost_impact

        return [
            {
                'action': 'review_expenses',
                'description': f'Revisar gastos de "{item["name"]}" e cortar despesas não-essenciais',
                'auto_applicable': False
            },
            {
                'action': 'transfer_budget',
                'description': 'Transferir budget de categoria com folga',
                'auto_applicable': False
            },
            {
                'action': 'request_budget_increase',
                'description': f'Solicitar aumento de R$ {overrun_amount:,.2f} ao produtor',
                'priority': 'high',
                'auto_applicable': False
            }
        ]
```

---

## ⚙️ SCHEDULE OPTIMIZATION ENGINE

### Arquitetura

```python
# app/intelligence/schedule_optimization/

├── __init__.py
├── engine.py                    # Main optimizer
├── algorithms/
│   ├── __init__.py
│   ├── genetic_algorithm.py     # GA optimizer
│   ├── greedy.py                # Greedy heuristic (MVP)
│   ├── constraint_programming.py # CP solver
│   └── simulated_annealing.py   # SA optimizer
├── models/
│   ├── schedule.py              # Schedule representation
│   └── constraint.py            # Constraint models
└── evaluators/
    ├── __init__.py
    ├── cost_evaluator.py        # Evaluate cost
    ├── time_evaluator.py        # Evaluate time
    └── quality_evaluator.py     # Evaluate quality
```

### Schedule Model

```python
# app/intelligence/schedule_optimization/models/schedule.py

from typing import List
from dataclasses import dataclass
from app.models.scene import Scene

@dataclass
class ScheduledScene:
    scene: Scene
    day: int  # Day index (0-based)
    order: int  # Order within day

@dataclass
class Schedule:
    """
    Representa uma sequência de scenes
    """
    scenes: List[ScheduledScene]
    total_days: int
    total_cost: float
    metrics: dict

    def to_dict(self):
        return {
            'scenes': [
                {
                    'scene_id': ss.scene.id,
                    'scene_name': ss.scene.name,
                    'day': ss.day,
                    'order': ss.order
                }
                for ss in self.scenes
            ],
            'total_days': self.total_days,
            'total_cost': self.total_cost,
            'metrics': self.metrics
        }
```

### Greedy Optimizer (MVP)

```python
# app/intelligence/schedule_optimization/algorithms/greedy.py

from typing import List
from collections import defaultdict
from app.models.scene import Scene
from app.intelligence.schedule_optimization.models.schedule import Schedule, ScheduledScene

class GreedyOptimizer:
    """
    Otimizador greedy (MVP)

    Estratégia:
    1. Agrupar scenes por locação
    2. Ordenar grupos por número de scenes (maior primeiro)
    3. Sequenciar scenes dentro do grupo por crew overlap (maximizar)
    """

    def optimize(self, scenes: List[Scene], constraints: dict) -> Schedule:
        """
        Otimizar schedule usando algoritmo greedy
        """
        # Agrupar por locação
        by_location = defaultdict(list)
        for scene in scenes:
            location_id = scene.location_id if scene.location_id else 'NO_LOCATION'
            by_location[location_id].append(scene)

        # Ordenar locações por número de scenes (maior primeiro)
        sorted_locations = sorted(
            by_location.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )

        scheduled_scenes = []
        current_day = 0

        for location_id, location_scenes in sorted_locations:
            # Ordenar scenes dentro da locação por crew overlap
            sorted_scenes = self._sort_by_crew_overlap(location_scenes)

            for i, scene in enumerate(sorted_scenes):
                scheduled_scenes.append(ScheduledScene(
                    scene=scene,
                    day=current_day,
                    order=i
                ))

            current_day += 1  # Próxima locação = próximo dia (simplificado)

        # Calcular métricas
        metrics = self._calculate_metrics(scheduled_scenes, constraints)

        return Schedule(
            scenes=scheduled_scenes,
            total_days=current_day,
            total_cost=metrics['total_cost'],
            metrics=metrics
        )

    def _sort_by_crew_overlap(self, scenes: List[Scene]) -> List[Scene]:
        """
        Ordenar scenes para maximizar crew overlap (reduzir custos)
        """
        # Implementação simplificada: ordenar por número de crew
        return sorted(scenes, key=lambda s: len(s.crew), reverse=True)

    def _calculate_metrics(self, scheduled_scenes: List[ScheduledScene], constraints: dict) -> dict:
        """
        Calcular métricas do schedule
        """
        # Custo total
        total_cost = sum(ss.scene.estimated_cost or 0 for ss in scheduled_scenes)

        # Company moves (mudanças de locação)
        company_moves = 0
        prev_location = None
        for ss in scheduled_scenes:
            if prev_location and ss.scene.location_id != prev_location:
                company_moves += 1
            prev_location = ss.scene.location_id

        return {
            'total_cost': total_cost,
            'total_days': len(set(ss.day for ss in scheduled_scenes)),
            'company_moves': company_moves,
            'avg_scenes_per_day': len(scheduled_scenes) / len(set(ss.day for ss in scheduled_scenes))
        }
```

---

## 📊 PREDICTIVE ANALYTICS ENGINE

### Arquitetura

```python
# app/intelligence/predictive_analytics/

├── __init__.py
├── engine.py                    # Main predictor
├── predictors/
│   ├── __init__.py
│   ├── budget_predictor.py      # Budget overrun prediction
│   ├── schedule_predictor.py    # Schedule delay prediction
│   └── quality_predictor.py     # Quality risk prediction
└── models/
    ├── prediction.py            # Prediction model
    └── alert.py                 # Alert model
```

### Budget Predictor

```python
# app/intelligence/predictive_analytics/predictors/budget_predictor.py

from datetime import datetime
from typing import Dict
from app.models.project import Project
from app.models.budget import Budget

class BudgetPredictor:
    """
    Prediz budget overrun baseado em burn rate
    """

    def predict(self, project: Project) -> Dict:
        """
        Prever se projeto vai estourar orçamento

        Algoritmo:
        1. Calcular burn rate (gasto/dia)
        2. Calcular dias restantes
        3. Projetar gasto total
        4. Comparar com budget estimado
        """
        budget = Budget.query.filter_by(project_id=project.id).first()

        if not budget:
            return {'error': 'No budget found'}

        # Dias decorridos
        if not project.start_date:
            return {'error': 'Project has no start date'}

        days_elapsed = (datetime.now().date() - project.start_date).days
        if days_elapsed <= 0:
            days_elapsed = 1

        # Burn rate
        burn_rate = budget.total_actual / days_elapsed

        # Dias restantes (estimado)
        total_estimated_days = 60  # Placeholder - calcular baseado em scenes
        days_remaining = total_estimated_days - days_elapsed

        # Projeção
        projected_total = budget.total_actual + (burn_rate * days_remaining)

        # Overrun?
        overrun = projected_total - budget.total_estimated
        overrun_pct = (overrun / budget.total_estimated) * 100 if budget.total_estimated > 0 else 0

        return {
            'current_actual': budget.total_actual,
            'current_estimated': budget.total_estimated,
            'projected_total': projected_total,
            'overrun_amount': overrun,
            'overrun_percentage': overrun_pct,
            'days_elapsed': days_elapsed,
            'days_remaining': days_remaining,
            'burn_rate_per_day': burn_rate,
            'probability': self._calculate_probability(overrun_pct),
            'severity': self._calculate_severity(overrun_pct)
        }

    def _calculate_probability(self, overrun_pct: float) -> float:
        """
        Calcular probabilidade de overrun acontecer

        Baseado em:
        - Magnitude do overrun projetado
        - Variabilidade histórica (placeholder - usar dados históricos)
        """
        if overrun_pct <= 0:
            return 0.1  # Sempre há alguma chance

        elif overrun_pct < 5:
            return 0.3

        elif overrun_pct < 10:
            return 0.5

        elif overrun_pct < 20:
            return 0.7

        else:
            return 0.9

    def _calculate_severity(self, overrun_pct: float) -> str:
        """
        Classificar severidade
        """
        if overrun_pct <= 5:
            return 'low'
        elif overrun_pct <= 10:
            return 'medium'
        elif overrun_pct <= 20:
            return 'high'
        else:
            return 'critical'
```

---

## 🗄️ DATABASE SCHEMA

### Novas Tabelas

```sql
-- Conflict Detection

CREATE TABLE conflicts (
    id SERIAL PRIMARY KEY,
    conflict_id VARCHAR(255) UNIQUE NOT NULL,
    project_id INTEGER REFERENCES projects(id),
    type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    entities JSONB NOT NULL,
    description TEXT,
    resolution_suggestions JSONB,
    cost_impact DECIMAL(10,2),
    detected_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP,
    resolution_applied JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conflicts_project ON conflicts(project_id);
CREATE INDEX idx_conflicts_type ON conflicts(type);
CREATE INDEX idx_conflicts_severity ON conflicts(severity);
CREATE INDEX idx_conflicts_resolved ON conflicts(resolved_at);

-- Schedule Optimization

CREATE TABLE optimized_schedules (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    algorithm VARCHAR(50) NOT NULL,
    constraints JSONB,
    schedule_data JSONB NOT NULL,
    metrics JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    applied_at TIMESTAMP
);

-- Predictive Analytics

CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    prediction_type VARCHAR(50) NOT NULL,  -- budget_overrun, schedule_delay, etc
    prediction_data JSONB NOT NULL,
    probability DECIMAL(3,2),
    severity VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_predictions_project ON predictions(project_id);
CREATE INDEX idx_predictions_type ON predictions(prediction_type);
```

---

## 🌐 API SPECIFICATION

### Conflict Detection API

```yaml
# OpenAPI 3.0 spec

/api/v5/intelligence/conflicts/detect/{project_id}:
  get:
    summary: Detectar todos os conflitos de um projeto
    parameters:
      - name: project_id
        in: path
        required: true
        schema:
          type: integer
      - name: start_date
        in: query
        schema:
          type: string
          format: date
      - name: end_date
        in: query
        schema:
          type: string
          format: date
    responses:
      200:
        description: Conflitos detectados
        content:
          application/json:
            schema:
              type: object
              properties:
                conflicts:
                  type: array
                summary:
                  type: object
                recommendations:
                  type: array

/api/v5/intelligence/conflicts/resolve/{conflict_id}:
  post:
    summary: Aplicar resolução para conflito
    parameters:
      - name: conflict_id
        in: path
        required: true
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              resolution_index:
                type: integer
              auto_apply:
                type: boolean
    responses:
      200:
        description: Resolução aplicada
```

### Schedule Optimization API

```yaml
/api/v5/intelligence/schedule/optimize/{project_id}:
  post:
    summary: Otimizar schedule do projeto
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              algorithm:
                type: string
                enum: [greedy, genetic, simulated_annealing]
              constraints:
                type: object
              optimization_goals:
                type: array
    responses:
      200:
        description: Schedule otimizado
        content:
          application/json:
            schema:
              type: object
              properties:
                optimized_schedule:
                  type: object
                comparison:
                  type: object
                metrics:
                  type: object
```

### Predictive Analytics API

```yaml
/api/v5/intelligence/predictions/budget/{project_id}:
  get:
    summary: Prever budget overrun
    responses:
      200:
        description: Predição de budget
        content:
          application/json:
            schema:
              type: object
              properties:
                projected_total:
                  type: number
                overrun_amount:
                  type: number
                probability:
                  type: number
                severity:
                  type: string

/api/v5/intelligence/predictions/schedule/{project_id}:
  get:
    summary: Prever schedule delay
    responses:
      200:
        description: Predição de delay
```

---

## 🔗 INTEGRATION POINTS

### Com Sistemas Existentes

1. **Scene Service**:
   - Trigger conflict detection ao agendar scene
   - Aplicar schedule otimizado ao stripboard

2. **Budget Service**:
   - Trigger budget prediction ao atualizar gastos
   - Alertar se overrun iminente

3. **Crew/Equipment Services**:
   - Validar availability antes de atribuir
   - Sugerir alternatives se conflict

4. **Notification Service**:
   - Enviar alertas de conflicts críticos
   - Notificar quando prediction muda severidade

---

## 📈 PERFORMANCE & SCALABILITY

### Otimizações

1. **Caching**:
   - Cache conflict detection results (TTL 5 min)
   - Cache optimization results (TTL 1h)
   - Invalidar cache ao modificar scenes

2. **Async Processing**:
   - Conflict detection em background (Celery)
   - Schedule optimization em queue (pode demorar)
   - Predictions calculadas overnight

3. **Indexing**:
   - Indexes em project_id, date, type, severity
   - Composite indexes para queries comuns

4. **Batching**:
   - Detectar conflitos em batch (não individual)
   - Otimizar schedule de todos os projetos juntos (overnight)

---

## 🏁 CONCLUSÃO

**Intelligence Layer** é a diferença entre um sistema MUITO BOM e um sistema CLASSE MUNDIAL.

Implementação phased:
- **Fase 5.1** (2 semanas): Conflict Detection MVP
- **Fase 5.2** (3 semanas): Schedule Optimizer Greedy
- **Fase 5.3** (2 semanas): Predictive Analytics básico
- **Fase 5.4** (3 semanas): Advanced algorithms (GA, CP)

**ROI**: 285% em 1 ano

---

**DIGIMUNDO PRESENTE 🥷**
