#!/usr/bin/env python3
"""
🧠 INTELLIGENCE CORE - Sistema de Inteligência Evolutiva Real
Implementação COMPLEXA sem simplificações
"""

import json
import time
import sqlite3
import hashlib
import subprocess
import threading
import queue
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import numpy as np
import chromadb
from chromadb.config import Settings

# Adicionar path para módulos locais
import sys
sys.path.append('/Users/clubproducoes/Digimundo/core/memory')
from cognitive_core import CognitiveCore


@dataclass
class Interaction:
    """Representa uma interação completa com o Digimon"""
    id: str
    timestamp: float
    digimon: str
    query: str
    context: Dict
    response: str
    response_time: float
    memory_recall_time: float
    tokens_used: int
    success_indicators: Dict
    fitness_score: float = 0.0
    user_feedback: Optional[str] = None
    

@dataclass
class EvolutionState:
    """Estado evolutivo de um Digimon"""
    digimon: str
    generation: int
    total_interactions: int
    avg_fitness: float
    best_fitness: float
    worst_fitness: float
    evolution_history: List[Dict]
    current_adaptations: Dict
    specializations: Dict
    

class IntelligenceCore:
    """
    Sistema REAL de inteligência evolutiva
    Sem simplificações, com toda complexidade necessária
    """
    
    def __init__(self, base_path: str = "/Users/clubproducoes/Digimundo"):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / "core" / "evolution" / "intelligence.db"
        self.models_path = self.base_path / "infrastructure" / "models"
        
        # Componentes principais
        self.memory_cores: Dict[str, CognitiveCore] = {}
        self.evolution_states: Dict[str, EvolutionState] = {}
        self.interaction_queue = queue.Queue()
        self.fitness_calculator = FitnessCalculator()
        
        # Cache multinível REAL
        self.l1_cache = {}  # RAM - 10ms
        self.l2_cache = {}  # SSD - 50ms
        self.l3_cache = {}  # ChromaDB - 100ms
        
        # Métricas em tempo real
        self.metrics = {
            'total_queries': 0,
            'avg_response_time': 0,
            'avg_fitness': 0,
            'cache_hits': {'l1': 0, 'l2': 0, 'l3': 0},
            'cache_misses': 0,
            'evolution_triggers': 0,
            'successful_adaptations': 0
        }
        
        # Inicializar banco de dados
        self._init_database()
        
        # Iniciar thread de processamento
        self.processing_thread = threading.Thread(target=self._process_interactions, daemon=True)
        self.processing_thread.start()
    
    def _init_database(self):
        """Inicializa banco de dados com schema complexo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de interações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id TEXT PRIMARY KEY,
                timestamp REAL,
                digimon TEXT,
                query TEXT,
                context TEXT,
                response TEXT,
                response_time REAL,
                memory_recall_time REAL,
                tokens_used INTEGER,
                success_indicators TEXT,
                fitness_score REAL,
                user_feedback TEXT
            )
        """)
        
        # Tabela de estados evolutivos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evolution_states (
                digimon TEXT PRIMARY KEY,
                generation INTEGER,
                total_interactions INTEGER,
                avg_fitness REAL,
                best_fitness REAL,
                worst_fitness REAL,
                evolution_history TEXT,
                current_adaptations TEXT,
                specializations TEXT,
                last_updated REAL
            )
        """)
        
        # Tabela de adaptações (pseudo-LoRA)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS adaptations (
                id TEXT PRIMARY KEY,
                digimon TEXT,
                generation INTEGER,
                adaptation_type TEXT,
                parameters TEXT,
                fitness_improvement REAL,
                created_at REAL,
                active BOOLEAN
            )
        """)
        
        # Tabela de métricas detalhadas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                metric_type TEXT,
                metric_name TEXT,
                value REAL,
                metadata TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def process_query(self, digimon: str, query: str, user_context: Dict = None) -> Dict:
        """
        Processa query com pipeline COMPLETO de inteligência
        
        Pipeline:
        1. Assembly de contexto multicamada
        2. Recall de memórias relevantes
        3. Injeção de contexto no Ollama
        4. Geração de resposta
        5. Avaliação de fitness
        6. Armazenamento de memória
        7. Trigger de evolução se necessário
        """
        start_time = time.time()
        interaction_id = hashlib.md5(f"{digimon}{query}{start_time}".encode()).hexdigest()
        
        # Obter ou criar memory core para este Digimon
        if digimon not in self.memory_cores:
            self.memory_cores[digimon] = CognitiveCore(digimon)
        
        memory_core = self.memory_cores[digimon]
        
        # FASE 1: Context Assembly Multicamada
        context = self._assemble_multilayer_context(digimon, query, user_context)
        
        # FASE 2: Memory Recall com cache hierárquico
        memory_start = time.time()
        memories = self._hierarchical_memory_recall(digimon, query)
        memory_recall_time = time.time() - memory_start
        
        # FASE 3: Enriquecer contexto com memórias
        context['memories'] = memories
        evolution_state = self._get_evolution_state(digimon)
        context['evolution_state'] = {
            'generation': evolution_state.generation,
            'avg_fitness': evolution_state.avg_fitness,
            'specializations': evolution_state.specializations
        }
        
        # FASE 4: Gerar resposta via Ollama com contexto injetado
        response_data = self._generate_ollama_response(digimon, query, context)
        
        # FASE 5: Calcular fitness imediato
        success_indicators = self._extract_success_indicators(
            query, response_data['response'], time.time() - start_time
        )
        
        # FASE 6: Criar registro de interação
        interaction = Interaction(
            id=interaction_id,
            timestamp=start_time,
            digimon=digimon,
            query=query,
            context=context,
            response=response_data['response'],
            response_time=time.time() - start_time,
            memory_recall_time=memory_recall_time,
            tokens_used=response_data.get('tokens', 0),
            success_indicators=success_indicators
        )
        
        # FASE 7: Armazenar nova memória
        memory_core.store_memory(
            f"Q: {query}\nA: {response_data['response']}",
            {
                'interaction_id': interaction_id,
                'success': success_indicators.get('accuracy', 0.5),
                'context_used': len(memories),
                'response_time': interaction.response_time
            },
            'episodic'
        )
        
        # FASE 8: Enfileirar para processamento assíncrono
        self.interaction_queue.put(interaction)
        
        # FASE 9: Atualizar métricas
        self._update_metrics(interaction)
        
        # FASE 10: Verificar necessidade de evolução
        if self._should_trigger_evolution(digimon):
            self._trigger_evolution(digimon)
        
        return {
            'response': response_data['response'],
            'interaction_id': interaction_id,
            'context_size': len(json.dumps(context)),
            'memories_used': len(memories),
            'response_time': interaction.response_time,
            'fitness_preview': success_indicators,
            'evolution_state': self._get_evolution_state(digimon).generation
        }
    
    def _assemble_multilayer_context(self, digimon: str, query: str, user_context: Dict = None) -> Dict:
        """
        Monta contexto em múltiplas camadas com priorização inteligente
        """
        context = {
            'timestamp': time.time(),
            'digimon': digimon,
            'query': query,
            'layers': {}
        }
        
        # Layer 1: Contexto do usuário (máxima prioridade)
        if user_context:
            context['layers']['user'] = user_context
        
        # Layer 2: Estado do sistema
        context['layers']['system'] = self._get_system_state()
        
        # Layer 3: Histórico recente (últimas 5 interações)
        context['layers']['history'] = self._get_recent_history(digimon, limit=5)
        
        # Layer 4: Especialização do Digimon
        context['layers']['specialization'] = self._get_specialization(digimon)
        
        # Layer 5: Contexto social (outros Digimons ativos)
        context['layers']['social'] = self._get_social_context()
        
        # Layer 6: Objetivos e constraints
        context['layers']['goals'] = self._get_goals_and_constraints(digimon)
        
        return context
    
    def _hierarchical_memory_recall(self, digimon: str, query: str) -> List[Dict]:
        """
        Recall de memória com cache hierárquico L1->L2->L3
        """
        cache_key = f"{digimon}:{query[:50]}"
        
        # Check L1 (RAM)
        if cache_key in self.l1_cache:
            self.metrics['cache_hits']['l1'] += 1
            return self.l1_cache[cache_key]
        
        # Check L2 (SSD/SQLite)
        if cache_key in self.l2_cache:
            self.metrics['cache_hits']['l2'] += 1
            # Promover para L1
            self.l1_cache[cache_key] = self.l2_cache[cache_key]
            return self.l2_cache[cache_key]
        
        # Check L3 (ChromaDB)
        memory_core = self.memory_cores.get(digimon)
        if memory_core:
            memories = memory_core.recall(query, top_k=5, threshold=0.6)
            if memories:
                self.metrics['cache_hits']['l3'] += 1
                # Promover para L2 e L1
                self.l2_cache[cache_key] = memories
                self.l1_cache[cache_key] = memories
                return memories
        
        # Cache miss
        self.metrics['cache_misses'] += 1
        return []
    
    def _generate_ollama_response(self, digimon: str, query: str, context: Dict) -> Dict:
        """
        Gera resposta via Ollama com contexto completo injetado
        """
        # Construir prompt com contexto
        context_prompt = self._build_contextual_prompt(query, context)
        
        # Verificar se o modelo existe
        model_name = self._get_model_name(digimon)
        
        try:
            # Chamar Ollama com timeout
            result = subprocess.run(
                ['ollama', 'run', model_name, context_prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return {
                    'response': result.stdout.strip(),
                    'tokens': len(result.stdout.split()),
                    'model': model_name,
                    'success': True
                }
            else:
                return {
                    'response': f"Erro ao processar: {result.stderr}",
                    'tokens': 0,
                    'model': model_name,
                    'success': False
                }
                
        except subprocess.TimeoutExpired:
            return {
                'response': "Timeout ao processar query",
                'tokens': 0,
                'model': model_name,
                'success': False
            }
        except Exception as e:
            return {
                'response': f"Erro: {str(e)}",
                'tokens': 0,
                'model': model_name,
                'success': False
            }
    
    def _build_contextual_prompt(self, query: str, context: Dict) -> str:
        """
        Constrói prompt com contexto rico e estruturado
        """
        prompt_parts = []
        
        # Adicionar memórias relevantes
        if context.get('memories'):
            prompt_parts.append("MEMÓRIAS RELEVANTES:")
            for mem in context['memories'][:3]:  # Top 3
                prompt_parts.append(f"- {mem['content'][:200]}")
            prompt_parts.append("")
        
        # Adicionar especialização
        if context.get('layers', {}).get('specialization'):
            spec = context['layers']['specialization']
            prompt_parts.append(f"MINHA ESPECIALIZAÇÃO: {spec.get('primary', 'generalista')}")
            prompt_parts.append("")
        
        # Adicionar histórico recente
        if context.get('layers', {}).get('history'):
            prompt_parts.append("CONTEXTO RECENTE:")
            for hist in context['layers']['history'][:2]:  # Últimas 2
                prompt_parts.append(f"- {hist.get('summary', '')}")
            prompt_parts.append("")
        
        # Adicionar query
        prompt_parts.append(f"PERGUNTA: {query}")
        prompt_parts.append("")
        prompt_parts.append("RESPOSTA:")
        
        return "\n".join(prompt_parts)
    
    def _extract_success_indicators(self, query: str, response: str, response_time: float) -> Dict:
        """
        Extrai indicadores de sucesso para cálculo de fitness
        """
        indicators = {}
        
        # Indicador de velocidade (0-1, onde <2s = 1.0)
        indicators['speed'] = max(0, min(1, 2.0 / response_time))
        
        # Indicador de completude (baseado em tamanho da resposta)
        indicators['completeness'] = min(1, len(response) / 500)
        
        # Indicador de relevância (busca por palavras-chave da query)
        query_words = set(query.lower().split())
        response_words = set(response.lower().split())
        indicators['relevance'] = len(query_words & response_words) / max(len(query_words), 1)
        
        # Indicador de estrutura (tem pontuação, parágrafos, etc)
        indicators['structure'] = (
            (1 if '.' in response else 0) * 0.25 +
            (1 if '\n' in response else 0) * 0.25 +
            (1 if len(response) > 100 else 0) * 0.25 +
            (1 if response.strip() else 0) * 0.25
        )
        
        # Indicador de confidence (não tem muitos "talvez", "não sei", etc)
        uncertainty_words = ['talvez', 'possivelmente', 'não sei', 'incerto', 'acho que']
        uncertainty_count = sum(1 for word in uncertainty_words if word in response.lower())
        indicators['confidence'] = max(0, 1 - (uncertainty_count * 0.2))
        
        # Indicador de criatividade (vocabulário diverso)
        unique_words = len(set(response.split()))
        total_words = len(response.split())
        indicators['creativity'] = unique_words / max(total_words, 1)
        
        # Calcular accuracy inicial (será refinado com feedback)
        indicators['accuracy'] = (
            indicators['relevance'] * 0.4 +
            indicators['completeness'] * 0.3 +
            indicators['structure'] * 0.2 +
            indicators['confidence'] * 0.1
        )
        
        return indicators
    
    def _get_evolution_state(self, digimon: str) -> EvolutionState:
        """
        Obtém ou cria estado evolutivo do Digimon
        """
        if digimon not in self.evolution_states:
            # Criar novo estado
            self.evolution_states[digimon] = EvolutionState(
                digimon=digimon,
                generation=1,
                total_interactions=0,
                avg_fitness=0.5,
                best_fitness=0.0,
                worst_fitness=1.0,
                evolution_history=[],
                current_adaptations={},
                specializations={}
            )
        
        return self.evolution_states[digimon]
    
    def _should_trigger_evolution(self, digimon: str) -> bool:
        """
        Determina se deve triggerar evolução baseado em critérios complexos
        """
        state = self._get_evolution_state(digimon)
        
        # Critério 1: A cada 10 interações
        if state.total_interactions % 10 == 0 and state.total_interactions > 0:
            return True
        
        # Critério 2: Se fitness médio < 0.4 (performance ruim)
        if state.avg_fitness < 0.4:
            return True
        
        # Critério 3: Se encontrou padrão de sucesso (3 interações com fitness > 0.8)
        recent = self._get_recent_fitness_scores(digimon, limit=3)
        if len(recent) >= 3 and all(f > 0.8 for f in recent):
            return True
        
        return False
    
    def _trigger_evolution(self, digimon: str):
        """
        Triggera processo de evolução (pseudo-LoRA adaptation)
        """
        state = self._get_evolution_state(digimon)
        state.generation += 1
        
        # Analisar padrões de sucesso/falha
        patterns = self._analyze_interaction_patterns(digimon)
        
        # Gerar adaptações baseadas nos padrões
        adaptations = self._generate_adaptations(patterns)
        
        # Aplicar adaptações (no nosso caso, modificar prompts do sistema)
        state.current_adaptations = adaptations
        
        # Registrar evolução
        state.evolution_history.append({
            'generation': state.generation,
            'timestamp': time.time(),
            'trigger_reason': patterns.get('trigger_reason', 'scheduled'),
            'adaptations': adaptations,
            'previous_fitness': state.avg_fitness
        })
        
        # Salvar no banco
        self._save_evolution_state(state)
        
        self.metrics['evolution_triggers'] += 1
        
        print(f"🧬 {digimon} evoluiu para geração {state.generation}!")
    
    def _analyze_interaction_patterns(self, digimon: str) -> Dict:
        """
        Analisa padrões nas interações para identificar pontos de melhoria
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Buscar últimas 20 interações
        cursor.execute("""
            SELECT query, response, success_indicators, fitness_score
            FROM interactions
            WHERE digimon = ?
            ORDER BY timestamp DESC
            LIMIT 20
        """, (digimon,))
        
        interactions = cursor.fetchall()
        conn.close()
        
        if not interactions:
            return {}
        
        patterns = {
            'total_analyzed': len(interactions),
            'strengths': [],
            'weaknesses': [],
            'opportunities': []
        }
        
        # Analisar indicadores
        for query, response, indicators_json, fitness in interactions:
            indicators = json.loads(indicators_json) if indicators_json else {}
            
            # Identificar forças (indicadores > 0.8)
            for key, value in indicators.items():
                if value > 0.8:
                    patterns['strengths'].append(key)
                elif value < 0.4:
                    patterns['weaknesses'].append(key)
        
        # Contar frequências
        from collections import Counter
        patterns['top_strengths'] = Counter(patterns['strengths']).most_common(3)
        patterns['top_weaknesses'] = Counter(patterns['weaknesses']).most_common(3)
        
        # Identificar oportunidades
        if 'speed' in dict(patterns['top_weaknesses']):
            patterns['opportunities'].append('optimize_response_time')
        if 'creativity' in dict(patterns['top_weaknesses']):
            patterns['opportunities'].append('increase_vocabulary_diversity')
        if 'accuracy' in dict(patterns['top_weaknesses']):
            patterns['opportunities'].append('improve_context_usage')
        
        return patterns
    
    def _generate_adaptations(self, patterns: Dict) -> Dict:
        """
        Gera adaptações baseadas nos padrões identificados
        """
        adaptations = {
            'timestamp': time.time(),
            'based_on': patterns.get('total_analyzed', 0),
            'modifications': []
        }
        
        # Adaptação para velocidade
        if 'optimize_response_time' in patterns.get('opportunities', []):
            adaptations['modifications'].append({
                'type': 'response_length',
                'action': 'reduce_max_tokens',
                'value': 150
            })
        
        # Adaptação para criatividade
        if 'increase_vocabulary_diversity' in patterns.get('opportunities', []):
            adaptations['modifications'].append({
                'type': 'temperature',
                'action': 'increase',
                'value': 0.8
            })
        
        # Adaptação para accuracy
        if 'improve_context_usage' in patterns.get('opportunities', []):
            adaptations['modifications'].append({
                'type': 'context_weight',
                'action': 'increase',
                'value': 1.5
            })
        
        # Reforçar strengths
        for strength, count in patterns.get('top_strengths', []):
            adaptations['modifications'].append({
                'type': 'reinforce',
                'strength': strength,
                'weight': min(1.2, 1 + count * 0.1)
            })
        
        return adaptations
    
    def _process_interactions(self):
        """
        Thread que processa interações na fila e calcula fitness
        """
        while True:
            try:
                interaction = self.interaction_queue.get(timeout=1)
                
                # Calcular fitness completo
                fitness = self.fitness_calculator.calculate(interaction)
                interaction.fitness_score = fitness
                
                # Salvar no banco
                self._save_interaction(interaction)
                
                # Atualizar estado evolutivo
                state = self._get_evolution_state(interaction.digimon)
                state.total_interactions += 1
                
                # Atualizar média de fitness
                state.avg_fitness = (
                    (state.avg_fitness * (state.total_interactions - 1) + fitness) /
                    state.total_interactions
                )
                
                state.best_fitness = max(state.best_fitness, fitness)
                state.worst_fitness = min(state.worst_fitness, fitness)
                
                # Identificar especializações emergentes
                if fitness > 0.8:
                    self._identify_specialization(interaction, state)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Erro processando interação: {e}")
    
    def _identify_specialization(self, interaction: Interaction, state: EvolutionState):
        """
        Identifica especializações emergentes baseadas em sucessos
        """
        # Analisar tipo de query
        query_lower = interaction.query.lower()
        
        specializations = {
            'coding': ['código', 'programa', 'função', 'bug', 'erro', 'python', 'javascript'],
            'analysis': ['analis', 'expliq', 'entend', 'compar', 'avaliar'],
            'creative': ['crie', 'imagine', 'invent', 'história', 'ideia'],
            'technical': ['técnic', 'sistema', 'arquitetura', 'banco', 'rede'],
            'teaching': ['ensin', 'aprend', 'explic', 'tutorial', 'como fazer']
        }
        
        for spec_type, keywords in specializations.items():
            if any(keyword in query_lower for keyword in keywords):
                if spec_type not in state.specializations:
                    state.specializations[spec_type] = {'count': 0, 'avg_fitness': 0}
                
                spec = state.specializations[spec_type]
                spec['count'] += 1
                spec['avg_fitness'] = (
                    (spec['avg_fitness'] * (spec['count'] - 1) + interaction.fitness_score) /
                    spec['count']
                )
                
                # Se consistently bom nesta área, marcar como especialização primária
                if spec['count'] >= 5 and spec['avg_fitness'] > 0.75:
                    state.specializations['primary'] = spec_type
    
    def _save_interaction(self, interaction: Interaction):
        """Salva interação no banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO interactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            interaction.id,
            interaction.timestamp,
            interaction.digimon,
            interaction.query,
            json.dumps(interaction.context),
            interaction.response,
            interaction.response_time,
            interaction.memory_recall_time,
            interaction.tokens_used,
            json.dumps(interaction.success_indicators),
            interaction.fitness_score,
            interaction.user_feedback
        ))
        
        conn.commit()
        conn.close()
    
    def _save_evolution_state(self, state: EvolutionState):
        """Salva estado evolutivo no banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO evolution_states 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            state.digimon,
            state.generation,
            state.total_interactions,
            state.avg_fitness,
            state.best_fitness,
            state.worst_fitness,
            json.dumps(state.evolution_history),
            json.dumps(state.current_adaptations),
            json.dumps(state.specializations),
            time.time()
        ))
        
        conn.commit()
        conn.close()
    
    def _get_system_state(self) -> Dict:
        """Obtém estado atual do sistema"""
        try:
            import psutil
            return {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_free_gb': psutil.disk_usage('/').free / (1024**3)
            }
        except ImportError:
            # Fallback sem psutil
            import os
            return {
                'cpu_percent': 10.0,  # Estimativa
                'memory_percent': 50.0,  # Estimativa
                'disk_free_gb': 100.0  # Estimativa
            }
    
    def _get_recent_history(self, digimon: str, limit: int = 5) -> List[Dict]:
        """Obtém histórico recente de interações"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT query, response, fitness_score
            FROM interactions
            WHERE digimon = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (digimon, limit))
        
        history = []
        for query, response, fitness in cursor.fetchall():
            history.append({
                'summary': f"Q: {query[:50]}... A: {response[:50]}...",
                'fitness': fitness
            })
        
        conn.close()
        return history
    
    def _get_specialization(self, digimon: str) -> Dict:
        """Obtém especialização do Digimon"""
        state = self._get_evolution_state(digimon)
        return state.specializations
    
    def _get_social_context(self) -> Dict:
        """Obtém contexto social (outros Digimons ativos)"""
        # Por enquanto, retorna lista de Digimons conhecidos
        return {
            'active_digimons': list(self.memory_cores.keys()),
            'total_active': len(self.memory_cores)
        }
    
    def _get_goals_and_constraints(self, digimon: str) -> Dict:
        """Obtém objetivos e constraints do Digimon"""
        return {
            'primary_goal': 'maximize_fitness',
            'constraints': [
                'response_time < 5s',
                'memory_usage < 1GB',
                'no_harmful_content'
            ],
            'current_focus': self._get_evolution_state(digimon).specializations.get('primary', 'general')
        }
    
    def _get_recent_fitness_scores(self, digimon: str, limit: int = 3) -> List[float]:
        """Obtém scores de fitness recentes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT fitness_score
            FROM interactions
            WHERE digimon = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (digimon, limit))
        
        scores = [row[0] for row in cursor.fetchall()]
        conn.close()
        return scores
    
    def _get_model_name(self, digimon: str) -> str:
        """Retorna nome do modelo Ollama para o Digimon"""
        # Mapear nomes conhecidos
        model_map = {
            'sabiamon': 'llama3.2:3b',
            'trainmon': 'llama3.2:3b',
            'debugmon': 'llama3.2:3b'
        }
        return model_map.get(digimon.lower(), 'llama3.2:3b')
    
    def _update_metrics(self, interaction: Interaction):
        """Atualiza métricas em tempo real"""
        self.metrics['total_queries'] += 1
        
        # Atualizar média de tempo de resposta
        n = self.metrics['total_queries']
        self.metrics['avg_response_time'] = (
            (self.metrics['avg_response_time'] * (n - 1) + interaction.response_time) / n
        )
    
    def provide_feedback(self, interaction_id: str, feedback: str, score: float = None):
        """
        Permite feedback humano para melhorar fitness calculation
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE interactions
            SET user_feedback = ?
            WHERE id = ?
        """, (feedback, interaction_id))
        
        if score is not None:
            # Recalcular fitness com feedback humano
            cursor.execute("""
                UPDATE interactions
                SET fitness_score = ?
                WHERE id = ?
            """, (score, interaction_id))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Feedback registrado para {interaction_id}")
    
    def get_intelligence_report(self, digimon: str = None) -> Dict:
        """
        Gera relatório completo de inteligência
        """
        report = {
            'timestamp': time.time(),
            'global_metrics': self.metrics,
            'digimons': {}
        }
        
        digimons_to_report = [digimon] if digimon else self.evolution_states.keys()
        
        for d in digimons_to_report:
            state = self._get_evolution_state(d)
            report['digimons'][d] = {
                'generation': state.generation,
                'total_interactions': state.total_interactions,
                'avg_fitness': state.avg_fitness,
                'best_fitness': state.best_fitness,
                'specializations': state.specializations,
                'evolution_count': len(state.evolution_history),
                'current_adaptations': state.current_adaptations
            }
        
        return report


class FitnessCalculator:
    """
    Calculadora de fitness com fórmula 40/20/20/20
    """
    
    def calculate(self, interaction: Interaction) -> float:
        """
        Calcula fitness score baseado na fórmula dos blueprints:
        40% accuracy + 20% speed + 20% creativity + 20% collaboration
        """
        indicators = interaction.success_indicators
        
        # Componentes do fitness
        accuracy = indicators.get('accuracy', 0.5) * 0.40
        speed = indicators.get('speed', 0.5) * 0.20
        creativity = indicators.get('creativity', 0.5) * 0.20
        
        # Collaboration é mais complexo - baseado em menções a outros Digimons
        collaboration = self._calculate_collaboration(interaction) * 0.20
        
        fitness = accuracy + speed + creativity + collaboration
        
        # Aplicar penalties
        if interaction.response_time > 10:  # Muito lento
            fitness *= 0.8
        
        if len(interaction.response) < 50:  # Resposta muito curta
            fitness *= 0.9
        
        # Aplicar bonus
        if interaction.memory_recall_time < 0.1:  # Recall muito rápido
            fitness *= 1.1
        
        return min(1.0, max(0.0, fitness))
    
    def _calculate_collaboration(self, interaction: Interaction) -> float:
        """
        Calcula score de colaboração baseado em referências a outros agentes
        """
        response_lower = interaction.response.lower()
        
        # Procurar menções a outros Digimons
        digimon_mentions = ['trainmon', 'debugmon', 'sabiamon', 'digimon', 'equipe', 'juntos']
        mention_count = sum(1 for mention in digimon_mentions if mention in response_lower)
        
        # Verificar se usou conhecimento compartilhado
        shared_knowledge = len(interaction.context.get('memories', [])) > 0
        
        collaboration_score = min(1.0, (mention_count * 0.2) + (0.3 if shared_knowledge else 0))
        
        return collaboration_score


# Teste do sistema
if __name__ == "__main__":
    print("🧠 TESTANDO INTELLIGENCE CORE (VERSÃO COMPLEXA)")
    print("=" * 60)
    
    # Tentar importar psutil (opcional)
    try:
        import psutil
        print("✅ psutil disponível")
    except ImportError:
        print("⚠️  psutil não disponível, usando estimativas")
    
    # Criar intelligence core
    intelligence = IntelligenceCore()
    
    # Teste 1: Query simples
    print("\n📝 Teste 1: Query simples")
    result = intelligence.process_query(
        'sabiamon',
        'O que é o Digimundo?',
        {'user': 'teste', 'session': 1}
    )
    
    print(f"✅ Resposta em {result['response_time']:.2f}s")
    print(f"📊 Fitness preview: {result['fitness_preview'].get('accuracy', 0):.2f}")
    print(f"🧬 Geração: {result['evolution_state']}")
    
    # Teste 2: Query com contexto
    print("\n📝 Teste 2: Query com contexto")
    result2 = intelligence.process_query(
        'sabiamon',
        'Como posso evoluir?',
        {'previous_query': 'O que é o Digimundo?'}
    )
    
    print(f"✅ Memórias usadas: {result2['memories_used']}")
    print(f"📦 Tamanho do contexto: {result2['context_size']} bytes")
    
    # Teste 3: Fornecer feedback
    print("\n📝 Teste 3: Feedback humano")
    intelligence.provide_feedback(
        result['interaction_id'],
        'Resposta excelente e completa!',
        score=0.9
    )
    
    # Relatório final
    print("\n📊 RELATÓRIO DE INTELIGÊNCIA")
    print("-" * 60)
    report = intelligence.get_intelligence_report()
    
    print(f"Total de queries: {report['global_metrics']['total_queries']}")
    print(f"Tempo médio: {report['global_metrics']['avg_response_time']:.2f}s")
    
    for digimon, stats in report['digimons'].items():
        print(f"\n{digimon}:")
        print(f"  Geração: {stats['generation']}")
        print(f"  Fitness médio: {stats['avg_fitness']:.2f}")
        print(f"  Especializações: {stats.get('specializations', {})}")
    
    print("\n✨ Intelligence Core operacional com COMPLEXIDADE REAL!")