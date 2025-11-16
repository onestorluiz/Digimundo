# 🤖 ML Infrastructure Guide - CineProd Fase 5.4

**Data**: 2025-11-16
**Propósito**: Guia completo para infraestrutura de Machine Learning em Predictive Analytics
**Aplicável a**: Fase 5.4 (Semanas 13-16)

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Stack Tecnológica](#stack-tecnológica)
3. [Arquitetura de ML](#arquitetura-de-ml)
4. [Training Pipeline](#training-pipeline)
5. [Model Deployment](#model-deployment)
6. [Model Versioning](#model-versioning)
7. [Monitoring & Retraining](#monitoring--retraining)
8. [Casos de Uso CineProd](#casos-de-uso-cineprod)

---

## 🎯 Visão Geral

### Objetivo

Implementar infraestrutura de ML para suportar:

1. **Budget Prediction** (ARIMA time-series)
2. **Schedule Delay Prediction** (Random Forest)
3. **Quality Score Prediction** (Linear Regression)
4. **Resource Demand Forecasting** (Prophet / ARIMA)

### Princípios

- **Simplicidade**: Começar com sklearn, evitar TensorFlow/PyTorch para MVP
- **Reproducibilidade**: Versionar modelos + dados de treino
- **Monitoramento**: Track model performance em produção
- **Incrementalidade**: Retreinar modelos com novos dados mensalmente

---

## 🛠️ Stack Tecnológica

### Bibliotecas Python

| Biblioteca | Versão | Uso |
|------------|--------|-----|
| `scikit-learn` | 1.3.2 | Modelos ML (Random Forest, Linear Regression) |
| `pandas` | 2.1.3 | Data manipulation |
| `numpy` | 1.26.2 | Numerical operations |
| `statsmodels` | 0.14.0 | ARIMA time-series |
| `prophet` | 1.1.5 | Time-series forecasting (Meta) |
| `joblib` | 1.3.2 | Model serialization |
| `mlflow` | 2.9.2 | Model tracking & versioning (opcional) |

### Infraestrutura

| Componente | Tecnologia | Uso |
|------------|-----------|-----|
| **Training** | Celery tasks | Treinar modelos assincronamente |
| **Storage** | S3 / FileSystem | Armazenar modelos (.pkl files) |
| **Versioning** | Git LFS / MLflow | Versionar modelos treinados |
| **Monitoring** | Prometheus | Métricas de predição (MAPE, RMSE) |
| **Scheduling** | Celery Beat | Retreinar modelos mensalmente |

---

## 🏗️ Arquitetura de ML

### Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────┐
│ 1. DATA COLLECTION                                          │
│                                                             │
│ PostgreSQL → Celery Task → Extract features → pandas DF    │
│   (scenes,                                                  │
│    budgets,                                                 │
│    delays)                                                  │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. TRAINING PIPELINE                                        │
│                                                             │
│ Feature Engineering → Train Model → Validate → Serialize   │
│   (preprocessing)      (sklearn)     (CV)      (.pkl)       │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. MODEL STORAGE                                            │
│                                                             │
│ models/budget_predictor_v1.2.pkl                            │
│ models/schedule_predictor_v0.9.pkl                          │
│ models/quality_predictor_v1.0.pkl                           │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. PREDICTION SERVICE                                       │
│                                                             │
│ Load Model (.pkl) → Predict (input features) → JSON        │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. MONITORING                                               │
│                                                             │
│ Prometheus: prediction_latency, mape_score, model_version  │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
cineprod-flask/
├── app/
│   ├── ml/                          # ← NOVO: ML module
│   │   ├── __init__.py
│   │   ├── models/                  # Model definitions
│   │   │   ├── budget_predictor.py
│   │   │   ├── schedule_predictor.py
│   │   │   └── base.py              # Base ML model class
│   │   ├── features/                # Feature engineering
│   │   │   ├── budget_features.py
│   │   │   └── schedule_features.py
│   │   ├── training/                # Training pipelines
│   │   │   ├── budget_trainer.py
│   │   │   └── scheduler_trainer.py
│   │   └── serving/                 # Prediction service
│   │       ├── predictor.py
│   │       └── cache.py
│   ├── services/
│   │   └── ml_service.py            # ML prediction API
│   └── routes/
│       └── ml_predictions.py        # /api/v1/predictions
├── ml_models/                       # Trained models storage
│   ├── budget_predictor_v1.0.pkl
│   ├── schedule_predictor_v1.0.pkl
│   └── metadata.json                # Model versions + metrics
├── ml_data/                         # Training data snapshots
│   ├── training_data_2025_11.csv
│   └── validation_data_2025_11.csv
└── celery_tasks/
    └── ml_tasks.py                  # Async training tasks
```

---

## 🔧 Training Pipeline

### 1. Data Extraction

**Task**: Extrair dados históricos de produção

```python
# app/ml/features/budget_features.py

import pandas as pd
from app.models import Project, Budget, Scene
from datetime import datetime, timedelta

class BudgetFeatureExtractor:
    """
    Extrai features para predição de budget
    """

    @staticmethod
    def extract_training_data(months=12):
        """
        Extrai dados de projetos dos últimos N meses
        """
        cutoff_date = datetime.utcnow() - timedelta(days=30 * months)

        projects = Project.query.filter(
            Project.created_at >= cutoff_date,
            Project.status == 'completed'  # Apenas projetos finalizados
        ).all()

        data = []
        for project in projects:
            budget = Budget.query.filter_by(project_id=project.id).first()
            scenes = Scene.query.filter_by(project_id=project.id).all()

            if not budget:
                continue

            features = {
                # Target variable
                'final_budget': budget.total_cost,

                # Input features
                'num_scenes': len(scenes),
                'num_locations': len(set(s.location_id for s in scenes if s.location_id)),
                'num_actors': len(project.cast),
                'shooting_days': project.shooting_days,
                'crew_size': len(project.crew),
                'genre': project.genre,  # Categorical
                'has_stunts': any(s.has_stunts for s in scenes),
                'has_vfx': any(s.has_vfx for s in scenes),
            }

            data.append(features)

        df = pd.DataFrame(data)
        return df
```

### 2. Feature Engineering

```python
# app/ml/features/budget_features.py (continuação)

class BudgetFeaturePreprocessor:
    """
    Preprocessa features para treino
    """

    @staticmethod
    def preprocess(df):
        """
        One-hot encoding, scaling, etc.
        """
        from sklearn.preprocessing import StandardScaler, OneHotEncoder
        from sklearn.compose import ColumnTransformer

        # Separar features numéricas e categóricas
        numeric_features = ['num_scenes', 'num_locations', 'num_actors',
                           'shooting_days', 'crew_size']
        categorical_features = ['genre']
        boolean_features = ['has_stunts', 'has_vfx']

        # Preprocessor pipeline
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
                ('bool', 'passthrough', boolean_features)
            ]
        )

        X = df.drop('final_budget', axis=1)
        y = df['final_budget']

        X_transformed = preprocessor.fit_transform(X)

        return X_transformed, y, preprocessor
```

### 3. Model Training

```python
# app/ml/training/budget_trainer.py

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_percentage_error
import joblib
import json
from datetime import datetime

class BudgetModelTrainer:
    """
    Treina modelo de predição de budget
    """

    def train(self, df, save_path='ml_models/budget_predictor.pkl'):
        """
        Treina e salva modelo
        """
        # Feature engineering
        from app.ml.features.budget_features import BudgetFeaturePreprocessor

        X, y, preprocessor = BudgetFeaturePreprocessor.preprocess(df)

        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        mape = mean_absolute_percentage_error(y_test, y_pred)

        # Cross-validation
        cv_scores = cross_val_score(
            model, X, y, cv=5,
            scoring='neg_mean_absolute_percentage_error'
        )

        # Serialize model + preprocessor
        model_artifact = {
            'model': model,
            'preprocessor': preprocessor,
            'metadata': {
                'trained_at': datetime.utcnow().isoformat(),
                'version': '1.0',
                'mape': float(mape),
                'cv_mape_mean': float(-cv_scores.mean()),
                'cv_mape_std': float(cv_scores.std()),
                'n_samples': len(df)
            }
        }

        joblib.dump(model_artifact, save_path)

        print(f"Model trained: MAPE = {mape:.2%}")
        print(f"CV MAPE: {-cv_scores.mean():.2%} ± {cv_scores.std():.2%}")

        return model_artifact
```

### 4. Training Task (Celery)

```python
# celery_tasks/ml_tasks.py

from celery import Celery
from app.ml.features.budget_features import BudgetFeatureExtractor
from app.ml.training.budget_trainer import BudgetModelTrainer

@celery.task(name='train_budget_predictor')
def train_budget_predictor_task():
    """
    Task assíncrona para treinar modelo de budget
    """
    # Extract data
    df = BudgetFeatureExtractor.extract_training_data(months=12)

    # Train model
    trainer = BudgetModelTrainer()
    model_artifact = trainer.train(df)

    # Log
    print(f"Budget predictor trained: v{model_artifact['metadata']['version']}")

    return model_artifact['metadata']

# Agendar retreino mensal
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'retrain-budget-predictor': {
        'task': 'train_budget_predictor',
        'schedule': crontab(day_of_month=1, hour=2, minute=0),  # Todo dia 1 às 2am
    }
}
```

---

## 🚀 Model Deployment

### Prediction Service

```python
# app/ml/serving/predictor.py

import joblib
import pandas as pd
from functools import lru_cache

class BudgetPredictor:
    """
    Carrega modelo e faz predições
    """

    def __init__(self, model_path='ml_models/budget_predictor.pkl'):
        self.model_artifact = self._load_model(model_path)
        self.model = self.model_artifact['model']
        self.preprocessor = self.model_artifact['preprocessor']
        self.metadata = self.model_artifact['metadata']

    @staticmethod
    @lru_cache(maxsize=1)
    def _load_model(model_path):
        """
        Carrega modelo (cached)
        """
        return joblib.load(model_path)

    def predict(self, features: dict) -> dict:
        """
        Prediz budget para projeto

        Args:
            features: {
                'num_scenes': 50,
                'num_locations': 10,
                'num_actors': 8,
                'shooting_days': 20,
                'crew_size': 15,
                'genre': 'Action',
                'has_stunts': True,
                'has_vfx': False
            }

        Returns:
            {
                'predicted_budget': 150000.0,
                'confidence_interval': [140000, 160000],
                'model_version': '1.0'
            }
        """
        # Convert to DataFrame
        df = pd.DataFrame([features])

        # Preprocess
        X = self.preprocessor.transform(df)

        # Predict
        prediction = self.model.predict(X)[0]

        # Confidence interval (±10%)
        ci_lower = prediction * 0.9
        ci_upper = prediction * 1.1

        return {
            'predicted_budget': float(prediction),
            'confidence_interval': [float(ci_lower), float(ci_upper)],
            'model_version': self.metadata['version'],
            'model_mape': self.metadata['mape']
        }
```

### ML Service (API Layer)

```python
# app/services/ml_service.py

from app.ml.serving.predictor import BudgetPredictor

class MLService:
    """
    Service layer para ML predictions
    """

    def __init__(self):
        self.budget_predictor = BudgetPredictor()

    def predict_budget(self, project_data: dict) -> dict:
        """
        Prediz budget para projeto

        Args:
            project_data: {
                'num_scenes': 50,
                'num_locations': 10,
                ...
            }

        Returns:
            {
                'predicted_budget': 150000.0,
                'confidence_interval': [140000, 160000],
                'model_version': '1.0'
            }
        """
        return self.budget_predictor.predict(project_data)
```

### API Route

```python
# app/routes/ml_predictions.py

from flask import Blueprint, request, jsonify
from app.services.ml_service import MLService

bp = Blueprint('ml_predictions', __name__, url_prefix='/api/v1/predictions')

ml_service = MLService()

@bp.route('/budget', methods=['POST'])
def predict_budget():
    """
    POST /api/v1/predictions/budget
    {
        "num_scenes": 50,
        "num_locations": 10,
        "num_actors": 8,
        "shooting_days": 20,
        "crew_size": 15,
        "genre": "Action",
        "has_stunts": true,
        "has_vfx": false
    }

    Response:
    {
        "predicted_budget": 150000.0,
        "confidence_interval": [140000, 160000],
        "model_version": "1.0",
        "model_mape": 0.08
    }
    """
    data = request.json

    prediction = ml_service.predict_budget(data)

    return jsonify(prediction)
```

---

## 📦 Model Versioning

### Strategy

**Opção 1: Git LFS** (simples, recomendado para MVP)

```bash
# Instalar Git LFS
brew install git-lfs
git lfs install

# Track .pkl files
git lfs track "ml_models/*.pkl"
git add .gitattributes
git commit -m "Track ML models with Git LFS"

# Commit modelo
git add ml_models/budget_predictor_v1.0.pkl
git commit -m "Add budget predictor v1.0 (MAPE: 8.2%)"
git push
```

**Opção 2: MLflow** (avançado, recomendado para produção)

```python
# app/ml/training/budget_trainer.py (com MLflow)

import mlflow
import mlflow.sklearn

class BudgetModelTrainer:

    def train(self, df):
        with mlflow.start_run():
            # Train model
            model.fit(X_train, y_train)

            # Log metrics
            mlflow.log_metric("mape", mape)
            mlflow.log_metric("cv_mape_mean", -cv_scores.mean())

            # Log params
            mlflow.log_param("n_estimators", 100)
            mlflow.log_param("max_depth", 10)

            # Log model
            mlflow.sklearn.log_model(model, "budget_predictor")

            print(f"Model logged to MLflow: run_id={mlflow.active_run().info.run_id}")
```

### Metadata Tracking

```json
// ml_models/metadata.json

{
  "budget_predictor": {
    "current_version": "1.2",
    "versions": [
      {
        "version": "1.0",
        "trained_at": "2025-11-15T10:30:00Z",
        "mape": 0.095,
        "n_samples": 150,
        "file": "budget_predictor_v1.0.pkl"
      },
      {
        "version": "1.1",
        "trained_at": "2025-12-01T02:00:00Z",
        "mape": 0.087,
        "n_samples": 180,
        "file": "budget_predictor_v1.1.pkl"
      },
      {
        "version": "1.2",
        "trained_at": "2026-01-01T02:00:00Z",
        "mape": 0.082,
        "n_samples": 220,
        "file": "budget_predictor_v1.2.pkl"
      }
    ]
  },
  "schedule_predictor": {
    "current_version": "0.9",
    "versions": [...]
  }
}
```

---

## 📊 Monitoring & Retraining

### Prometheus Metrics

```python
# app/ml/serving/predictor.py (com monitoring)

from prometheus_client import Counter, Histogram

# Metrics
prediction_counter = Counter('ml_predictions_total', 'Total ML predictions', ['model'])
prediction_latency = Histogram('ml_prediction_latency_seconds', 'Prediction latency', ['model'])
prediction_error = Counter('ml_prediction_errors_total', 'Prediction errors', ['model'])

class BudgetPredictor:

    def predict(self, features: dict) -> dict:
        import time
        start_time = time.time()

        try:
            # Predict
            prediction = self.model.predict(X)[0]

            # Metrics
            prediction_counter.labels(model='budget_predictor').inc()
            prediction_latency.labels(model='budget_predictor').observe(time.time() - start_time)

            return {...}

        except Exception as e:
            prediction_error.labels(model='budget_predictor').inc()
            raise
```

### Model Drift Detection

```python
# celery_tasks/ml_monitoring.py

@celery.task(name='check_model_drift')
def check_model_drift():
    """
    Verifica se modelo precisa ser retreinado
    """
    # Calcular MAPE em produção vs MAPE de treino
    recent_predictions = get_recent_predictions(days=30)

    actual_budgets = [p['actual_budget'] for p in recent_predictions]
    predicted_budgets = [p['predicted_budget'] for p in recent_predictions]

    mape_production = mean_absolute_percentage_error(actual_budgets, predicted_budgets)

    # Comparar com MAPE de treino
    model_artifact = joblib.load('ml_models/budget_predictor.pkl')
    mape_training = model_artifact['metadata']['mape']

    # Se degradou mais de 20%, retreinar
    if mape_production > mape_training * 1.2:
        print(f"Model drift detected: {mape_production:.2%} vs {mape_training:.2%}")
        train_budget_predictor_task.delay()

# Agendar verificação semanal
celery.conf.beat_schedule['check-model-drift'] = {
    'task': 'check_model_drift',
    'schedule': crontab(day_of_week=1, hour=3, minute=0),  # Segundas às 3am
}
```

---

## 🎬 Casos de Uso CineProd

### 1. Budget Prediction

**Modelo**: Random Forest Regressor
**Features**: num_scenes, num_locations, shooting_days, genre, has_stunts
**Target**: final_budget
**Métrica**: MAPE < 10%

**Uso**: Ao criar novo projeto, sugerir budget estimado.

---

### 2. Schedule Delay Prediction

**Modelo**: Random Forest Classifier
**Features**: num_scenes, weather_forecast, crew_experience, location_complexity
**Target**: will_delay (boolean)
**Métrica**: F1-score > 0.8

**Uso**: Alertar produtor se projeto tem risco de atraso.

---

### 3. Resource Demand Forecasting

**Modelo**: ARIMA
**Features**: historical_actor_bookings (time-series)
**Target**: actor_bookings_next_month
**Métrica**: MAPE < 15%

**Uso**: Prever demanda de atores para próximo mês.

---

## ✅ Checklist de Implementação

### Fase 5.4 Week 1: ML Infrastructure Setup

- [ ] Criar estrutura `app/ml/` (models, features, training, serving)
- [ ] Adicionar dependencies (scikit-learn, statsmodels, prophet, joblib)
- [ ] Criar `BudgetFeatureExtractor` e `BudgetFeaturePreprocessor`
- [ ] Implementar `BudgetModelTrainer`
- [ ] Criar Celery task `train_budget_predictor_task`
- [ ] Treinar modelo inicial (v1.0)
- [ ] Salvar em `ml_models/budget_predictor_v1.0.pkl`

### Fase 5.4 Week 2: Prediction Service

- [ ] Criar `BudgetPredictor` (serving)
- [ ] Implementar `MLService` (API layer)
- [ ] Criar route `/api/v1/predictions/budget`
- [ ] Adicionar testes de predição
- [ ] Validar MAPE < 10%

### Fase 5.4 Week 3: Monitoring & Versioning

- [ ] Adicionar Prometheus metrics (prediction_latency, mape)
- [ ] Criar `metadata.json` para versionamento
- [ ] Implementar `check_model_drift` task
- [ ] Setup Git LFS para .pkl files
- [ ] Documentar uso em `ML_INFRASTRUCTURE_GUIDE.md`

### Fase 5.4 Week 4: Advanced Models

- [ ] Implementar Schedule Delay Predictor (Random Forest Classifier)
- [ ] Implementar Resource Demand Forecaster (ARIMA)
- [ ] Criar dashboard de métricas ML (Grafana)
- [ ] Adicionar A/B testing entre versões de modelo

---

## 📚 Referências

- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [ARIMA for Time Series](https://www.statsmodels.org/stable/examples/notebooks/generated/tsa_arma_0.html)
- [Production ML Best Practices](https://ml-ops.org/)

---

**Mantido por**: Claude Code + Equipe Digimundo
**Última Atualização**: 2025-11-16
**Versão**: 1.0
