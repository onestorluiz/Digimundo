#!/usr/bin/env python3
"""
🎯 AUTO OPTIMIZER - Sistema de Auto-Otimização EXTREMAMENTE INTELIGENTE
Machine Learning para auto-tuning de parâmetros e performance
"""

import time
import json
import math
import threading
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional, Callable
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import statistics
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pickle

@dataclass
class PerformanceMetric:
    """Métrica de performance com contexto"""
    timestamp: float
    metric_name: str
    value: float
    context: Dict[str, Any]
    system_state: Dict[str, float]

@dataclass
class OptimizationTarget:
    """Alvo de otimização"""
    name: str
    current_value: float
    target_value: float
    weight: float  # Importância relativa
    direction: str  # 'maximize' ou 'minimize'

class AutoOptimizer:
    """Sistema de auto-otimização baseado em Machine Learning"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path("/Users/clubproducoes/Digimundo/scripturemon-validation")
        self.optimizer_path = self.base_path / "runtime" / "optimizer"
        self.optimizer_path.mkdir(parents=True, exist_ok=True)
        
        # Modelo de ML para predições
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.model_trained = False
        
        # Histórico de métricas
        self.metrics_history = deque(maxlen=10000)  # Últimas 10k métricas
        self.parameter_history = deque(maxlen=1000)  # Últimas 1k configurações
        
        # Parâmetros otimizáveis
        self.parameters = {
            # Cache
            'cache_l1_ttl': {'min': 60, 'max': 900, 'current': 300, 'type': 'int'},
            'cache_l2_ttl': {'min': 600, 'max': 7200, 'current': 3600, 'type': 'int'},
            'cache_l1_max_items': {'min': 100, 'max': 5000, 'current': 1000, 'type': 'int'},
            'cache_l2_max_items': {'min': 500, 'max': 20000, 'current': 5000, 'type': 'int'},
            
            # Pipeline
            'pipeline_workers': {'min': 1, 'max': 64, 'current': 8, 'type': 'int'},
            'pipeline_queue_size': {'min': 100, 'max': 5000, 'current': 1000, 'type': 'int'},
            'backpressure_threshold': {'min': 0.5, 'max': 0.95, 'current': 0.8, 'type': 'float'},
            
            # Modelos
            'model_timeout': {'min': 10, 'max': 300, 'current': 60, 'type': 'int'},
            'model_temperature': {'min': 0.1, 'max': 2.0, 'current': 0.7, 'type': 'float'},
            'model_top_p': {'min': 0.1, 'max': 1.0, 'current': 0.9, 'type': 'float'},
            
            # Memória
            'memory_batch_size': {'min': 1, 'max': 100, 'current': 10, 'type': 'int'},
            'memory_consolidation_interval': {'min': 300, 'max': 3600, 'current': 1800, 'type': 'int'}
        }
        
        # Objetivos de otimização
        self.targets = {
            'response_time_ms': OptimizationTarget(
                name='response_time_ms',
                current_value=1000,
                target_value=500,
                weight=0.3,
                direction='minimize'
            ),
            'cache_hit_rate': OptimizationTarget(
                name='cache_hit_rate',
                current_value=0.7,
                target_value=0.9,
                weight=0.25,
                direction='maximize'
            ),
            'memory_usage_mb': OptimizationTarget(
                name='memory_usage_mb',
                current_value=500,
                target_value=300,
                weight=0.2,
                direction='minimize'
            ),
            'throughput_qps': OptimizationTarget(
                name='throughput_qps',
                current_value=10,
                target_value=50,
                weight=0.25,
                direction='maximize'
            )
        }
        
        # Estratégias de otimização
        self.strategies = {
            'gradient_descent': self._gradient_descent_step,
            'random_search': self._random_search_step,
            'bayesian': self._bayesian_optimization_step,
            'genetic': self._genetic_algorithm_step
        }
        
        self.current_strategy = 'gradient_descent'
        
        # Estado interno
        self.optimization_running = False
        self.last_optimization = 0
        self.optimization_interval = 600  # 10 minutos
        
        # Thread de otimização
        self.optimizer_thread = threading.Thread(
            target=self._optimization_loop,
            daemon=True
        )
        
        # Caregar configurações salvas
        self._load_configuration()
        
        print("🎯 Sistema de Auto-Otimização inicializado")
        print(f"   Parâmetros: {len(self.parameters)}")
        print(f"   Objetivos: {len(self.targets)}")
        print(f"   Estratégia: {self.current_strategy}")
    
    def start_optimization(self):
        """Inicia otimização automática"""
        if not self.optimization_running:
            self.optimization_running = True
            self.optimizer_thread.start()
            print("🚀 Auto-otimização iniciada")
    
    def stop_optimization(self):
        """Para otimização automática"""
        self.optimization_running = False
        print("⛔ Auto-otimização parada")
    
    def record_metric(self, name: str, value: float, context: Dict = None):
        """
        Registra métrica para otimização
        
        Args:
            name: Nome da métrica
            value: Valor da métrica
            context: Contexto adicional
        """
        metric = PerformanceMetric(
            timestamp=time.time(),
            metric_name=name,
            value=value,
            context=context or {},
            system_state=self._get_current_system_state()
        )
        
        self.metrics_history.append(metric)
        
        # Atualizar alvo se existir
        if name in self.targets:
            self.targets[name].current_value = value
    
    def suggest_parameters(self, strategy: str = None) -> Dict[str, Any]:
        """
        Sugere novos parâmetros baseado em ML
        
        Args:
            strategy: Estratégia a usar (None = atual)
        
        Returns:
            Dicionário com parâmetros sugeridos
        """
        if len(self.metrics_history) < 50:
            # Poucos dados - usar valores padrão com pequenas variações
            return self._random_variations()
        
        strategy = strategy or self.current_strategy
        strategy_func = self.strategies.get(strategy, self._gradient_descent_step)
        
        return strategy_func()
    
    def apply_parameters(self, parameters: Dict[str, Any], test_duration: int = 300):
        """
        Aplica parâmetros e testa performance
        
        Args:
            parameters: Parâmetros a aplicar
            test_duration: Duração do teste em segundos
        """
        print(f"🧪 Testando nova configuração por {test_duration}s:")
        
        # Salvar configuração anterior
        previous_params = {k: v['current'] for k, v in self.parameters.items()}
        
        # Aplicar novos parâmetros
        for param, value in parameters.items():
            if param in self.parameters:
                self.parameters[param]['current'] = value
                print(f"   {param}: {previous_params[param]} -> {value}")
        
        # Registrar configuração
        self.parameter_history.append({
            'timestamp': time.time(),
            'parameters': parameters.copy(),
            'previous': previous_params.copy()
        })
        
        # TODO: Aplicar parâmetros nos sistemas (cache, pipeline, etc)
        # Isso seria feito através de callbacks ou integração direta
        
        return True
    
    def evaluate_performance(self) -> float:
        """
        Avalia performance atual baseada nos objetivos
        
        Returns:
            Score de performance (0-1, maior = melhor)
        """
        if len(self.metrics_history) < 10:
            return 0.5  # Score neutro
        
        total_score = 0
        total_weight = 0
        
        # Calcular score para cada objetivo
        for target in self.targets.values():
            # Pegar métricas recentes
            recent_metrics = [
                m for m in self.metrics_history
                if m.metric_name == target.name and 
                   time.time() - m.timestamp < 300  # Últimos 5 minutos
            ]
            
            if not recent_metrics:
                continue
            
            # Calcular média recente
            avg_value = statistics.mean(m.value for m in recent_metrics)
            
            # Calcular score normalizado
            if target.direction == 'minimize':
                # Quanto menor, melhor
                if target.target_value == 0:
                    score = max(0, 1 - (avg_value / max(1, target.current_value)))
                else:
                    # Score alto quando valor está próximo ou abaixo do target
                    score = max(0, min(1, target.target_value / max(avg_value, 1)))
            else:
                # Quanto maior, melhor
                if target.target_value == 0:
                    score = 0.5
                else:
                    score = min(1, avg_value / target.target_value)
            
            total_score += score * target.weight
            total_weight += target.weight
        
        return total_score / max(total_weight, 1)
    
    def get_recommendations(self) -> List[Dict]:
        """Retorna recomendações de otimização"""
        recommendations = []
        
        # Analisar tendências
        if len(self.metrics_history) >= 100:
            for target_name, target in self.targets.items():
                recent_metrics = [
                    m.value for m in self.metrics_history
                    if m.metric_name == target_name
                ][-50:]  # Últimas 50
                
                if len(recent_metrics) >= 10:
                    # Calcular tendência
                    x = list(range(len(recent_metrics)))
                    slope = np.polyfit(x, recent_metrics, 1)[0]
                    
                    recommendation = {
                        'metric': target_name,
                        'current': recent_metrics[-1],
                        'target': target.target_value,
                        'trend': 'improving' if (
                            (slope > 0 and target.direction == 'maximize') or
                            (slope < 0 and target.direction == 'minimize')
                        ) else 'degrading',
                        'slope': slope,
                        'priority': 'high' if abs(slope) > 0.1 else 'medium'
                    }
                    
                    recommendations.append(recommendation)
        
        return recommendations
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do otimizador"""
        performance_score = self.evaluate_performance()
        
        return {
            'optimization_running': self.optimization_running,
            'current_strategy': self.current_strategy,
            'performance_score': f"{performance_score:.3f}",
            'metrics_collected': len(self.metrics_history),
            'configurations_tested': len(self.parameter_history),
            'last_optimization': self.last_optimization,
            'model_trained': self.model_trained,
            'current_parameters': {
                k: v['current'] for k, v in self.parameters.items()
            },
            'targets_status': {
                name: {
                    'current': target.current_value,
                    'target': target.target_value,
                    'progress': min(1, target.current_value / max(1, target.target_value))
                    if target.direction == 'maximize'
                    else max(0, 1 - target.current_value / max(1, target.target_value))
                }
                for name, target in self.targets.items()
            }
        }
    
    # Métodos privados - Estratégias de otimização
    
    def _gradient_descent_step(self) -> Dict[str, Any]:
        """Passo de gradient descent baseado em métricas históricas"""
        if not self.model_trained:
            self._train_model()
        
        current_params = {k: v['current'] for k, v in self.parameters.items()}
        suggestions = {}
        
        # Calcular gradientes aproximados
        for param_name, param_config in self.parameters.items():
            current_val = param_config['current']
            param_range = param_config['max'] - param_config['min']
            step_size = param_range * 0.05  # 5% do range
            
            if param_config['type'] == 'int':
                step_size = max(1, int(step_size))
            
            # Direção baseada na performance recente
            performance_score = self.evaluate_performance()
            
            # Se performance está baixa, fazer mudanças maiores
            if performance_score < 0.6:
                step_size *= 2
            
            # Direção aleatória com viés para melhoria
            direction = 1 if np.random.random() > 0.5 else -1
            
            new_val = current_val + (step_size * direction)
            
            # Aplicar limites
            new_val = max(param_config['min'], 
                         min(param_config['max'], new_val))
            
            if param_config['type'] == 'int':
                new_val = int(new_val)
            
            suggestions[param_name] = new_val
        
        return suggestions
    
    def _random_search_step(self) -> Dict[str, Any]:
        """Busca aleatória nos parâmetros"""
        suggestions = {}
        
        for param_name, param_config in self.parameters.items():
            min_val = param_config['min']
            max_val = param_config['max']
            
            if param_config['type'] == 'int':
                new_val = np.random.randint(min_val, max_val + 1)
            else:
                new_val = np.random.uniform(min_val, max_val)
            
            suggestions[param_name] = new_val
        
        return suggestions
    
    def _bayesian_optimization_step(self) -> Dict[str, Any]:
        """Otimização Bayesiana (simplificada)"""
        # Por simplicidade, usar exploração vs exploração
        exploration_prob = 0.3
        
        if np.random.random() < exploration_prob:
            # Explorar: busca aleatória
            return self._random_search_step()
        else:
            # Explorar: gradient descent
            return self._gradient_descent_step()
    
    def _genetic_algorithm_step(self) -> Dict[str, Any]:
        """Passo de algoritmo genético (simplificado)"""
        if len(self.parameter_history) < 5:
            return self._random_search_step()
        
        # Pegar as 3 melhores configurações recentes
        recent_configs = list(self.parameter_history)[-10:]
        
        # Para simplicidade, fazer crossover simples entre duas configurações
        config1 = recent_configs[-1]['parameters']
        config2 = recent_configs[-2]['parameters']
        
        suggestions = {}
        for param_name in self.parameters:
            # Crossover: escolher aleatoriamente entre os pais
            if param_name in config1 and param_name in config2:
                parent_val = config1[param_name] if np.random.random() > 0.5 else config2[param_name]
                
                # Mutação: pequena variação
                param_config = self.parameters[param_name]
                mutation_rate = 0.1
                
                if np.random.random() < mutation_rate:
                    param_range = param_config['max'] - param_config['min']
                    mutation = (np.random.random() - 0.5) * param_range * 0.1
                    
                    new_val = parent_val + mutation
                    new_val = max(param_config['min'], 
                                 min(param_config['max'], new_val))
                    
                    if param_config['type'] == 'int':
                        new_val = int(new_val)
                    
                    suggestions[param_name] = new_val
                else:
                    suggestions[param_name] = parent_val
        
        return suggestions
    
    def _random_variations(self) -> Dict[str, Any]:
        """Pequenas variações aleatórias dos valores atuais"""
        suggestions = {}
        
        for param_name, param_config in self.parameters.items():
            current = param_config['current']
            param_range = param_config['max'] - param_config['min']
            
            # Variação de até 10%
            variation = (np.random.random() - 0.5) * param_range * 0.2
            new_val = current + variation
            
            # Aplicar limites
            new_val = max(param_config['min'], 
                         min(param_config['max'], new_val))
            
            if param_config['type'] == 'int':
                new_val = int(new_val)
            
            suggestions[param_name] = new_val
        
        return suggestions
    
    def _train_model(self):
        """Treina modelo ML com dados históricos"""
        if len(self.metrics_history) < 100:
            return
        
        # Preparar dados de treinamento
        X = []  # Features: parâmetros do sistema
        y = []  # Target: performance score
        
        for param_entry in self.parameter_history:
            timestamp = param_entry['timestamp']
            
            # Encontrar métricas próximas no tempo
            related_metrics = [
                m for m in self.metrics_history
                if abs(m.timestamp - timestamp) < 300  # 5 minutos
            ]
            
            if related_metrics:
                # Calcular performance score para esse período
                performance = self._calculate_performance_for_period(related_metrics)
                
                # Features: valores dos parâmetros
                features = [
                    param_entry['parameters'].get(param, 0)
                    for param in self.parameters.keys()
                ]
                
                X.append(features)
                y.append(performance)
        
        if len(X) >= 10:
            try:
                X_scaled = self.scaler.fit_transform(X)
                self.model.fit(X_scaled, y)
                self.model_trained = True
                print("🤖 Modelo ML treinado com sucesso")
            except Exception as e:
                print(f"❌ Erro ao treinar modelo: {e}")
    
    def _calculate_performance_for_period(self, metrics: List[PerformanceMetric]) -> float:
        """Calcula performance para um período específico"""
        if not metrics:
            return 0.5
        
        # Agrupar por tipo de métrica
        metric_groups = defaultdict(list)
        for m in metrics:
            metric_groups[m.metric_name].append(m.value)
        
        # Calcular score para cada métrica
        total_score = 0
        total_weight = 0
        
        for metric_name, values in metric_groups.items():
            if metric_name in self.targets:
                target = self.targets[metric_name]
                avg_value = statistics.mean(values)
                
                if target.direction == 'minimize':
                    score = max(0, 1 - (avg_value / max(1, target.target_value)))
                else:
                    score = min(1, avg_value / max(1, target.target_value))
                
                total_score += score * target.weight
                total_weight += target.weight
        
        return total_score / max(total_weight, 1)
    
    def _get_current_system_state(self) -> Dict[str, float]:
        """Coleta estado atual do sistema"""
        return {param: config['current'] for param, config in self.parameters.items()}
    
    def _optimization_loop(self):
        """Loop principal de otimização"""
        while self.optimization_running:
            try:
                current_time = time.time()
                
                if current_time - self.last_optimization >= self.optimization_interval:
                    print("🔧 Executando ciclo de otimização...")
                    
                    # Avaliar performance atual
                    current_performance = self.evaluate_performance()
                    print(f"   Performance atual: {current_performance:.3f}")
                    
                    # Se performance está baixa, otimizar
                    if current_performance < 0.8:
                        # Sugerir novos parâmetros
                        new_params = self.suggest_parameters()
                        
                        # Aplicar e testar
                        self.apply_parameters(new_params, test_duration=300)
                        
                        # Treinar modelo com novos dados
                        if len(self.metrics_history) >= 200:
                            self._train_model()
                    
                    self.last_optimization = current_time
                
                time.sleep(60)  # Verificar a cada minuto
                
            except Exception as e:
                print(f"❌ Erro na otimização: {e}")
                time.sleep(60)
    
    def _save_configuration(self):
        """Salva configuração atual"""
        config_file = self.optimizer_path / "optimizer_config.json"
        
        config = {
            'parameters': self.parameters,
            'targets': {name: asdict(target) for name, target in self.targets.items()},
            'current_strategy': self.current_strategy,
            'optimization_interval': self.optimization_interval
        }
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _load_configuration(self):
        """Carrega configuração salva"""
        config_file = self.optimizer_path / "optimizer_config.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                # Atualizar parâmetros salvos
                if 'parameters' in config:
                    for param_name, param_data in config['parameters'].items():
                        if param_name in self.parameters:
                            self.parameters[param_name].update(param_data)
                
                print("📁 Configuração carregada do arquivo")
            except Exception as e:
                print(f"⚠️ Erro ao carregar configuração: {e}")


# Singleton global
_optimizer = None

def get_optimizer() -> AutoOptimizer:
    """Retorna instância singleton do otimizador"""
    global _optimizer
    if _optimizer is None:
        _optimizer = AutoOptimizer()
    return _optimizer