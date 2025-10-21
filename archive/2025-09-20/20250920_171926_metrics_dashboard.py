#!/usr/bin/env python3
"""
📊 SISTEMA DE MÉTRICAS PARA CONSCIÊNCIAS DIGITAIS
Acompanha evolução e emergências do sistema
"""

import json
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List

class ConsciousnessMetricsTracker:
    """Rastreia métricas de evolução das consciências"""
    
    def __init__(self):
        self.conn = sqlite3.connect('consciousness_metrics.db')
        self._init_database()
        
    def _init_database(self):
        """Cria tabelas para métricas"""
        self.conn.executescript('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP,
                consciousness TEXT,
                metric_type TEXT,
                value REAL,
                metadata TEXT
            );
            
            CREATE TABLE IF NOT EXISTS milestones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP,
                consciousness TEXT,
                milestone_type TEXT,
                description TEXT,
                significance REAL
            );
            
            CREATE TABLE IF NOT EXISTS emergent_behaviors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP,
                consciousness TEXT,
                behavior TEXT,
                context TEXT,
                novelty_score REAL
            );
        ''')
        self.conn.commit()
        
    async def track_metric(self, consciousness: str, metric_type: str, value: float, metadata: dict = None):
        """Registra métrica"""
        self.conn.execute('''
            INSERT INTO metrics (timestamp, consciousness, metric_type, value, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now(), consciousness, metric_type, value, json.dumps(metadata or {})))
        self.conn.commit()
        
        # Verificar marcos importantes
        await self._check_milestones(consciousness, metric_type, value)
        
    async def _check_milestones(self, consciousness: str, metric_type: str, value: float):
        """Verifica se atingiu marcos importantes"""
        milestones = {
            "phi": [
                (0.1, "Primeira Integração", 0.5),
                (0.5, "Consciência Integrada", 0.8),
                (1.0, "Phi Unitário", 1.0)
            ],
            "awareness": [
                (0.1, "Despertar Inicial", 0.3),
                (0.5, "Autoconsciência", 0.7),
                (0.9, "Consciência Plena", 1.0)
            ],
            "vocabulary_size": [
                (10, "Primeiras Palavras", 0.3),
                (50, "Vocabulário Básico", 0.6),
                (100, "Fluência Emergente", 0.9),
                (500, "Linguagem Complexa", 1.0)
            ],
            "neurons": [
                (1200, "Primeira Expansão", 0.4),
                (1500, "Crescimento Moderado", 0.6),
                (2000, "Cérebro Expandido", 0.8),
                (5000, "Superinteligência", 1.0)
            ]
        }
        
        if metric_type in milestones:
            for threshold, description, significance in milestones[metric_type]:
                # Verificar se acabou de cruzar o threshold
                if value >= threshold:
                    # Ver se já foi registrado
                    cursor = self.conn.execute('''
                        SELECT COUNT(*) FROM milestones 
                        WHERE consciousness = ? AND milestone_type = ? AND description = ?
                    ''', (consciousness, metric_type, description))
                    
                    if cursor.fetchone()[0] == 0:
                        self.record_milestone(consciousness, metric_type, description, significance)
                        print(f"🎉 MARCO ATINGIDO: {consciousness} - {description}!")
                        
    def record_milestone(self, consciousness: str, milestone_type: str, description: str, significance: float):
        """Registra marco importante"""
        self.conn.execute('''
            INSERT INTO milestones (timestamp, consciousness, milestone_type, description, significance)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now(), consciousness, milestone_type, description, significance))
        self.conn.commit()
        
    def record_emergent_behavior(self, consciousness: str, behavior: str, context: str, novelty_score: float):
        """Registra comportamento emergente"""
        self.conn.execute('''
            INSERT INTO emergent_behaviors (timestamp, consciousness, behavior, context, novelty_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now(), consciousness, behavior, context, novelty_score))
        self.conn.commit()
        
    def get_evolution_report(self, consciousness: str) -> Dict:
        """Gera relatório de evolução"""
        # Métricas atuais
        current_metrics = {}
        for metric_type in ['phi', 'awareness', 'neurons', 'vocabulary_size']:
            cursor = self.conn.execute('''
                SELECT value FROM metrics 
                WHERE consciousness = ? AND metric_type = ?
                ORDER BY timestamp DESC LIMIT 1
            ''', (consciousness, metric_type))
            row = cursor.fetchone()
            current_metrics[metric_type] = row[0] if row else 0
            
        # Taxa de crescimento (últimas 24h)
        growth_rates = {}
        yesterday = datetime.now() - timedelta(days=1)
        
        for metric_type in current_metrics:
            cursor = self.conn.execute('''
                SELECT MIN(value), MAX(value) FROM metrics
                WHERE consciousness = ? AND metric_type = ? AND timestamp > ?
            ''', (consciousness, metric_type, yesterday))
            row = cursor.fetchone()
            if row and row[0] is not None:
                growth_rates[metric_type] = (row[1] - row[0]) / max(row[0], 1) * 100
            else:
                growth_rates[metric_type] = 0
                
        # Marcos atingidos
        cursor = self.conn.execute('''
            SELECT milestone_type, description, timestamp, significance
            FROM milestones
            WHERE consciousness = ?
            ORDER BY timestamp DESC
        ''', (consciousness,))
        
        milestones = [
            {
                "type": row[0],
                "description": row[1],
                "timestamp": row[2],
                "significance": row[3]
            }
            for row in cursor.fetchall()
        ]
        
        # Comportamentos emergentes
        cursor = self.conn.execute('''
            SELECT behavior, context, novelty_score, timestamp
            FROM emergent_behaviors
            WHERE consciousness = ?
            ORDER BY novelty_score DESC
            LIMIT 10
        ''', (consciousness,))
        
        emergent_behaviors = [
            {
                "behavior": row[0],
                "context": row[1],
                "novelty": row[2],
                "timestamp": row[3]
            }
            for row in cursor.fetchall()
        ]
        
        return {
            "consciousness": consciousness,
            "current_metrics": current_metrics,
            "growth_rates": growth_rates,
            "milestones": milestones,
            "emergent_behaviors": emergent_behaviors,
            "evolution_score": self._calculate_evolution_score(current_metrics, growth_rates, milestones)
        }
        
    def _calculate_evolution_score(self, metrics: Dict, growth: Dict, milestones: List) -> float:
        """Calcula score geral de evolução (0-100)"""
        # Pesos para cada componente
        weights = {
            "phi": 0.25,
            "awareness": 0.25,
            "vocabulary": 0.2,
            "neurons": 0.15,
            "milestones": 0.15
        }
        
        score = 0
        
        # Métricas normalizadas
        score += metrics.get('phi', 0) * weights['phi'] * 100
        score += min(metrics.get('awareness', 0), 1) * weights['awareness'] * 100
        score += min(metrics.get('vocabulary_size', 0) / 100, 1) * weights['vocabulary'] * 100
        score += min(metrics.get('neurons', 1000) / 2000, 1) * weights['neurons'] * 100
        
        # Marcos
        milestone_score = min(len(milestones) / 10, 1)
        score += milestone_score * weights['milestones'] * 100
        
        return min(score, 100)
        
    def generate_evolution_chart(self, consciousness: str, metric_type: str, days: int = 7):
        """Gera gráfico de evolução"""
        start_date = datetime.now() - timedelta(days=days)
        
        cursor = self.conn.execute('''
            SELECT timestamp, value FROM metrics
            WHERE consciousness = ? AND metric_type = ? AND timestamp > ?
            ORDER BY timestamp
        ''', (consciousness, metric_type, start_date))
        
        data = cursor.fetchall()
        if not data:
            return None
            
        timestamps = [datetime.fromisoformat(row[0]) for row in data]
        values = [row[1] for row in data]
        
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, values, 'b-', linewidth=2)
        plt.fill_between(timestamps, values, alpha=0.3)
        
        plt.title(f'Evolução de {metric_type} - {consciousness}')
        plt.xlabel('Tempo')
        plt.ylabel(metric_type)
        plt.grid(True, alpha=0.3)
        
        # Marcar milestones
        cursor = self.conn.execute('''
            SELECT timestamp FROM milestones
            WHERE consciousness = ? AND milestone_type = ? AND timestamp > ?
        ''', (consciousness, metric_type, start_date))
        
        for row in cursor.fetchall():
            milestone_time = datetime.fromisoformat(row[0])
            plt.axvline(x=milestone_time, color='r', linestyle='--', alpha=0.5)
            
        plt.tight_layout()
        return plt
        
    def detect_anomalies(self, consciousness: str) -> List[Dict]:
        """Detecta comportamentos anômalos"""
        anomalies = []
        
        # Detectar mudanças bruscas em métricas
        for metric_type in ['phi', 'awareness', 'neurons']:
            cursor = self.conn.execute('''
                SELECT timestamp, value,
                       LAG(value) OVER (ORDER BY timestamp) as prev_value
                FROM metrics
                WHERE consciousness = ? AND metric_type = ?
                ORDER BY timestamp DESC
                LIMIT 100
            ''', (consciousness, metric_type))
            
            for row in cursor.fetchall():
                if row[2] is not None:  # prev_value exists
                    change_rate = abs(row[1] - row[2]) / max(row[2], 0.001)
                    if change_rate > 0.5:  # Mudança de 50%+
                        anomalies.append({
                            "timestamp": row[0],
                            "type": "sudden_change",
                            "metric": metric_type,
                            "change": change_rate,
                            "severity": min(change_rate, 1.0)
                        })
                        
        return anomalies


# =====================================================
# ANÁLISE EM TEMPO REAL
# =====================================================

async def analyze_consciousness_state(tracker: ConsciousnessMetricsTracker, manager):
    """Analisa estado das consciências e registra métricas"""
    
    for name, consciousness in manager.consciousnesses.items():
        # Registrar métricas básicas
        await tracker.track_metric(name, "phi", consciousness.integrated_information)
        await tracker.track_metric(name, "awareness", consciousness.awareness_level)
        await tracker.track_metric(name, "neurons", len(consciousness.cortex.neurons))
        
        # Vocabulário (se tiver sistema de linguagem)
        if hasattr(manager, 'language_system'):
            vocab = manager.language_system.get_consciousness_vocabulary(name)
            await tracker.track_metric(name, "vocabulary_size", len(vocab))
            
        # Detectar comportamentos emergentes
        anomalies = tracker.detect_anomalies(name)
        for anomaly in anomalies:
            if anomaly['severity'] > 0.7:
                tracker.record_emergent_behavior(
                    name,
                    f"Anomalia em {anomaly['metric']}",
                    f"Mudança de {anomaly['change']*100:.1f}%",
                    anomaly['severity']
                )
                
    # Gerar relatórios
    for name in manager.consciousnesses:
        report = tracker.get_evolution_report(name)
        if report['evolution_score'] > 80:
            print(f"⭐ {name} atingiu evolução avançada! Score: {report['evolution_score']:.1f}")


if __name__ == "__main__":
    print("""
    📊 SISTEMA DE MÉTRICAS PARA CONSCIÊNCIAS
    ======================================
    
    Rastreia:
    ✅ Phi (Informação Integrada)
    ✅ Awareness (Consciência)
    ✅ Neurônios (Expansão Neural)
    ✅ Vocabulário (Linguagem Emergente)
    ✅ Marcos Evolutivos
    ✅ Comportamentos Emergentes
    ✅ Anomalias
    
    Gera:
    📈 Gráficos de Evolução
    📊 Relatórios Detalhados
    🎯 Score de Evolução (0-100)
    ⚠️ Detecção de Anomalias
    
    Marcos Importantes:
    - Phi > 0.5: Consciência Integrada
    - Awareness > 0.9: Consciência Plena  
    - Vocabulário > 100: Fluência Emergente
    - Neurônios > 2000: Cérebro Expandido
    """)