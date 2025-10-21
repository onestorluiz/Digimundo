#!/usr/bin/env python3
"""
SDL Auto-Consolidation System - Sistema de Aprendizado Contínuo
Self-Directed Learning com consolidação automática de conhecimento
Integrado com Crystal Memory e administrado pelo Digimon Producer

DIGIMUNDO PRESENTE - APRENDIZADO REVOLUCIONÁRIO!
"""

import json
import time
import asyncio
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import hashlib
import sqlite3
from collections import defaultdict

logger = logging.getLogger(__name__)


class LearningMode(Enum):
    """Modos de aprendizado do sistema"""
    PASSIVE = "passive"          # Aprendizado passivo baseado em observações
    ACTIVE = "active"            # Aprendizado ativo com busca de conhecimento
    REINFORCEMENT = "reinforcement"  # Aprendizado por reforço baseado em feedback
    ADAPTIVE = "adaptive"        # Aprendizado adaptativo que muda de acordo com o contexto


class ConsolidationStrategy(Enum):
    """Estratégias de consolidação de conhecimento"""
    FREQUENCY_BASED = "frequency"    # Baseado na frequência de uso
    IMPORTANCE_BASED = "importance"  # Baseado na importância do conhecimento
    RECENCY_BASED = "recency"       # Baseado na recência das informações
    HYBRID = "hybrid"               # Combinação de múltiplas estratégias


@dataclass
class LearningPattern:
    """Padrão de aprendizado identificado"""
    pattern_id: str
    pattern_type: str
    frequency: int
    confidence: float
    last_seen: float
    contexts: List[str]
    reinforcement_score: float
    consolidation_priority: float


@dataclass
class KnowledgeNode:
    """Nó de conhecimento no grafo de aprendizado"""
    node_id: str
    content: str
    category: str
    connections: List[str]
    usage_count: int
    last_accessed: float
    importance_score: float
    consolidation_level: int  # 0=raw, 1=processed, 2=consolidated, 3=crystallized


class SDLAutoConsolidation:
    """Sistema de Aprendizado Contínuo com Auto-Consolidação"""

    def __init__(self, soul_id: str, data_dir: str = "data/sdl_auto"):
        self.soul_id = soul_id
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Configuração do banco de dados
        self.db_path = self.data_dir / f"sdl_{soul_id}.db"
        self._init_database()

        # Estado do sistema
        self.learning_mode = LearningMode.ADAPTIVE
        self.consolidation_strategy = ConsolidationStrategy.HYBRID
        self.running = False
        self.consolidation_thread = None

        # Métricas de aprendizado
        self.learning_stats = {
            'patterns_discovered': 0,
            'knowledge_nodes': 0,
            'consolidations_performed': 0,
            'learning_sessions': 0
        }

        # Callbacks para integração
        self.memory_callback: Optional[Callable] = None
        self.consciousness_callback: Optional[Callable] = None
        self.rag_callback: Optional[Callable] = None

        logger.info(f"SDL Auto-Consolidation inicializado - Soul: {soul_id}")

    def _init_database(self):
        """Inicializa banco de dados para aprendizado"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS learning_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    pattern_type TEXT,
                    frequency INTEGER DEFAULT 1,
                    confidence REAL DEFAULT 0.5,
                    last_seen REAL,
                    contexts TEXT,
                    reinforcement_score REAL DEFAULT 0.0,
                    consolidation_priority REAL DEFAULT 0.0
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_nodes (
                    node_id TEXT PRIMARY KEY,
                    content TEXT,
                    category TEXT,
                    connections TEXT,
                    usage_count INTEGER DEFAULT 0,
                    last_accessed REAL,
                    importance_score REAL DEFAULT 0.5,
                    consolidation_level INTEGER DEFAULT 0
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS learning_sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time REAL,
                    end_time REAL,
                    mode TEXT,
                    patterns_found INTEGER DEFAULT 0,
                    knowledge_gained INTEGER DEFAULT 0,
                    consolidations INTEGER DEFAULT 0
                )
            """)

            conn.commit()

    def set_callbacks(self, memory_callback: Callable = None,
                     consciousness_callback: Callable = None,
                     rag_callback: Callable = None):
        """Configura callbacks para integração com outros sistemas"""
        self.memory_callback = memory_callback
        self.consciousness_callback = consciousness_callback
        self.rag_callback = rag_callback

        logger.info("SDL callbacks configurados para integração")

    def start_learning(self, mode: LearningMode = LearningMode.ADAPTIVE):
        """Inicia sistema de aprendizado contínuo"""
        if self.running:
            logger.warning("SDL já está em execução")
            return

        self.running = True
        self.learning_mode = mode

        # Iniciar thread de consolidação
        self.consolidation_thread = threading.Thread(
            target=self._consolidation_loop,
            daemon=True
        )
        self.consolidation_thread.start()

        # Registrar sessão de aprendizado
        session_id = f"session_{int(time.time())}"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO learning_sessions (session_id, start_time, mode)
                VALUES (?, ?, ?)
            """, (session_id, time.time(), mode.value))
            conn.commit()

        self.learning_stats['learning_sessions'] += 1
        logger.info(f"SDL Auto-Consolidation iniciado - Modo: {mode.value}")

    def stop_learning(self):
        """Para sistema de aprendizado"""
        if not self.running:
            return

        self.running = False

        if self.consolidation_thread:
            self.consolidation_thread.join(timeout=5)

        logger.info("SDL Auto-Consolidation parado")

    def observe_pattern(self, content: str, context: str,
                       pattern_type: str = "behavioral") -> str:
        """Observa e registra padrão de comportamento/uso"""

        # Gerar ID único para o padrão
        pattern_data = f"{content}:{context}:{pattern_type}"
        pattern_id = hashlib.sha256(pattern_data.encode()).hexdigest()[:16]

        current_time = time.time()

        with sqlite3.connect(self.db_path) as conn:
            # Verificar se padrão já existe
            cursor = conn.execute(
                "SELECT frequency, contexts FROM learning_patterns WHERE pattern_id = ?",
                (pattern_id,)
            )
            existing = cursor.fetchone()

            if existing:
                # Atualizar padrão existente
                frequency = existing[0] + 1
                contexts = json.loads(existing[1])
                if context not in contexts:
                    contexts.append(context)

                # Calcular nova confiança baseada na frequência
                confidence = min(1.0, frequency / 10.0)

                conn.execute("""
                    UPDATE learning_patterns
                    SET frequency = ?, confidence = ?, last_seen = ?, contexts = ?
                    WHERE pattern_id = ?
                """, (frequency, confidence, current_time,
                     json.dumps(contexts), pattern_id))
            else:
                # Criar novo padrão
                conn.execute("""
                    INSERT INTO learning_patterns
                    (pattern_id, pattern_type, frequency, confidence, last_seen, contexts)
                    VALUES (?, ?, 1, 0.1, ?, ?)
                """, (pattern_id, pattern_type, current_time,
                     json.dumps([context])))

                self.learning_stats['patterns_discovered'] += 1

            conn.commit()

        # Callback para consciousness se disponível
        if self.consciousness_callback:
            self.consciousness_callback(f"pattern_observed:{pattern_type}")

        return pattern_id

    def add_knowledge_node(self, content: str, category: str = "general",
                          importance: float = 0.5) -> str:
        """Adiciona novo nó de conhecimento"""

        # Gerar ID único
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        node_id = f"node_{content_hash}"

        current_time = time.time()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO knowledge_nodes
                (node_id, content, category, connections, last_accessed, importance_score)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (node_id, content, category, json.dumps([]),
                 current_time, importance))
            conn.commit()

        self.learning_stats['knowledge_nodes'] += 1

        # Callback para memory se disponível
        if self.memory_callback:
            self.memory_callback(f"knowledge_added:{category}")

        return node_id

    def connect_knowledge_nodes(self, node1_id: str, node2_id: str,
                               strength: float = 1.0):
        """Conecta dois nós de conhecimento"""

        with sqlite3.connect(self.db_path) as conn:
            # Atualizar conexões do node1
            cursor = conn.execute(
                "SELECT connections FROM knowledge_nodes WHERE node_id = ?",
                (node1_id,)
            )
            result = cursor.fetchone()
            if result:
                connections = json.loads(result[0])
                connection_data = {"node": node2_id, "strength": strength}

                # Evitar duplicatas
                existing = next((c for c in connections if c.get("node") == node2_id), None)
                if existing:
                    existing["strength"] = max(existing["strength"], strength)
                else:
                    connections.append(connection_data)

                conn.execute(
                    "UPDATE knowledge_nodes SET connections = ? WHERE node_id = ?",
                    (json.dumps(connections), node1_id)
                )

            # Fazer o mesmo para node2 (conexão bidirecional)
            cursor = conn.execute(
                "SELECT connections FROM knowledge_nodes WHERE node_id = ?",
                (node2_id,)
            )
            result = cursor.fetchone()
            if result:
                connections = json.loads(result[0])
                connection_data = {"node": node1_id, "strength": strength}

                existing = next((c for c in connections if c.get("node") == node1_id), None)
                if existing:
                    existing["strength"] = max(existing["strength"], strength)
                else:
                    connections.append(connection_data)

                conn.execute(
                    "UPDATE knowledge_nodes SET connections = ? WHERE node_id = ?",
                    (json.dumps(connections), node2_id)
                )

            conn.commit()

    def _consolidation_loop(self):
        """Loop principal de consolidação automática"""

        while self.running:
            try:
                self._perform_consolidation()
                time.sleep(30)  # Consolidação a cada 30 segundos
            except Exception as e:
                logger.error(f"Erro na consolidação SDL: {e}")
                time.sleep(10)

    def _perform_consolidation(self):
        """Executa processo de consolidação de conhecimento"""

        consolidation_start = time.time()
        consolidations_made = 0

        with sqlite3.connect(self.db_path) as conn:

            # 1. Consolidar padrões frequentes
            cursor = conn.execute("""
                SELECT pattern_id, frequency, confidence, pattern_type
                FROM learning_patterns
                WHERE frequency >= 3 AND consolidation_priority < 0.8
                ORDER BY frequency DESC, confidence DESC
                LIMIT 10
            """)

            patterns_to_consolidate = cursor.fetchall()

            for pattern_id, frequency, confidence, pattern_type in patterns_to_consolidate:
                # Calcular prioridade de consolidação
                priority = min(1.0, (frequency * confidence) / 5.0)

                conn.execute("""
                    UPDATE learning_patterns
                    SET consolidation_priority = ?
                    WHERE pattern_id = ?
                """, (priority, pattern_id))

                consolidations_made += 1

                # Callback para memory
                if self.memory_callback and priority > 0.7:
                    self.memory_callback(f"consolidate_pattern:{pattern_type}")

            # 2. Promover nós de conhecimento importantes
            cursor = conn.execute("""
                SELECT node_id, importance_score, usage_count, consolidation_level
                FROM knowledge_nodes
                WHERE consolidation_level < 3 AND importance_score > 0.6
                ORDER BY importance_score DESC, usage_count DESC
                LIMIT 5
            """)

            nodes_to_promote = cursor.fetchall()

            for node_id, importance, usage, level in nodes_to_promote:
                new_level = min(3, level + 1)

                conn.execute("""
                    UPDATE knowledge_nodes
                    SET consolidation_level = ?
                    WHERE node_id = ?
                """, (new_level, node_id))

                consolidations_made += 1

                # Callback para memory se nível alto
                if self.memory_callback and new_level >= 2:
                    self.memory_callback(f"crystallize_knowledge:{node_id}")

            conn.commit()

        self.learning_stats['consolidations_performed'] += consolidations_made

        # Callback para consciousness sobre consolidação
        if self.consciousness_callback and consolidations_made > 0:
            self.consciousness_callback(f"knowledge_consolidated:{consolidations_made}")

        logger.debug(f"Consolidação SDL: {consolidations_made} items em {time.time() - consolidation_start:.2f}s")

    def get_learning_insights(self) -> Dict[str, Any]:
        """Retorna insights sobre o aprendizado atual"""

        insights = {
            'top_patterns': [],
            'knowledge_categories': defaultdict(int),
            'consolidation_progress': 0.0,
            'learning_efficiency': 0.0
        }

        with sqlite3.connect(self.db_path) as conn:
            # Top padrões por frequência
            cursor = conn.execute("""
                SELECT pattern_type, AVG(frequency), AVG(confidence), COUNT(*)
                FROM learning_patterns
                GROUP BY pattern_type
                ORDER BY AVG(frequency) DESC
                LIMIT 5
            """)

            for pattern_type, avg_freq, avg_conf, count in cursor.fetchall():
                insights['top_patterns'].append({
                    'type': pattern_type,
                    'average_frequency': avg_freq,
                    'average_confidence': avg_conf,
                    'pattern_count': count
                })

            # Categorias de conhecimento
            cursor = conn.execute("""
                SELECT category, COUNT(*), AVG(importance_score)
                FROM knowledge_nodes
                GROUP BY category
            """)

            for category, count, avg_importance in cursor.fetchall():
                insights['knowledge_categories'][category] = {
                    'node_count': count,
                    'average_importance': avg_importance
                }

            # Progresso de consolidação
            cursor = conn.execute("""
                SELECT consolidation_level, COUNT(*)
                FROM knowledge_nodes
                GROUP BY consolidation_level
            """)

            total_nodes = 0
            consolidated_nodes = 0

            for level, count in cursor.fetchall():
                total_nodes += count
                if level >= 2:  # Considerando nível 2+ como consolidado
                    consolidated_nodes += count

            if total_nodes > 0:
                insights['consolidation_progress'] = consolidated_nodes / total_nodes

        # Eficiência de aprendizado
        if self.learning_stats['learning_sessions'] > 0:
            insights['learning_efficiency'] = (
                self.learning_stats['patterns_discovered'] /
                self.learning_stats['learning_sessions']
            )

        return insights

    def get_sdl_status(self) -> Dict[str, Any]:
        """Status completo do sistema SDL"""
        return {
            'soul_id': self.soul_id,
            'running': self.running,
            'learning_mode': self.learning_mode.value,
            'consolidation_strategy': self.consolidation_strategy.value,
            'learning_stats': self.learning_stats.copy(),
            'learning_insights': self.get_learning_insights()
        }


def test_sdl_auto_consolidation():
    """Teste do sistema SDL Auto-Consolidation"""
    print("="*70)
    print("🧠 TESTE DO SDL AUTO-CONSOLIDATION SYSTEM 🧠")
    print("="*70)

    # Criar sistema SDL
    sdl = SDLAutoConsolidation("TestSDLSoul")

    # Iniciar aprendizado
    print("🚀 Iniciando aprendizado adaptativo...")
    sdl.start_learning(LearningMode.ADAPTIVE)

    # Simular observações de padrões
    print("\n📊 Simulando observações de padrões...")
    patterns = [
        ("User analyzes screenplay structure", "screenplay_analysis", "behavioral"),
        ("DigiLang compression applied", "compression", "technical"),
        ("Memory consolidation triggered", "memory", "system"),
        ("User analyzes screenplay structure", "screenplay_analysis", "behavioral"),  # Repetir para frequência
        ("RAG query for screenplay tips", "rag_query", "informational"),
        ("User analyzes screenplay structure", "screenplay_analysis", "behavioral"),  # Repetir novamente
    ]

    for content, context, ptype in patterns:
        pattern_id = sdl.observe_pattern(content, context, ptype)
        print(f"   📈 Padrão observado: {ptype} ({pattern_id[:8]}...)")

    # Adicionar nós de conhecimento
    print("\n🔗 Adicionando nós de conhecimento...")
    knowledge_items = [
        ("Screenplay structure follows three-act format", "screenplay", 0.8),
        ("Character development requires consistent voice", "character", 0.7),
        ("Dialogue should sound natural when read aloud", "dialogue", 0.9),
        ("Scene transitions need smooth flow", "structure", 0.6),
    ]

    node_ids = []
    for content, category, importance in knowledge_items:
        node_id = sdl.add_knowledge_node(content, category, importance)
        node_ids.append(node_id)
        print(f"   🧠 Conhecimento adicionado: {category} ({node_id[:8]}...)")

    # Conectar nós relacionados
    print("\n🔗 Conectando conhecimentos relacionados...")
    sdl.connect_knowledge_nodes(node_ids[0], node_ids[3], 0.8)  # Structure related
    sdl.connect_knowledge_nodes(node_ids[1], node_ids[2], 0.7)  # Character-dialogue

    # Aguardar consolidação
    print("\n⏳ Aguardando consolidação automática...")
    time.sleep(35)  # Aguardar mais que o ciclo de consolidação

    # Obter insights
    print("\n📊 INSIGHTS DE APRENDIZADO:")
    insights = sdl.get_learning_insights()

    print(f"   📈 Top Padrões:")
    for pattern in insights['top_patterns']:
        print(f"     • {pattern['type']}: {pattern['pattern_count']} padrões, "
              f"freq média {pattern['average_frequency']:.1f}")

    print(f"   🧠 Categorias de Conhecimento:")
    for category, stats in insights['knowledge_categories'].items():
        print(f"     • {category}: {stats['node_count']} nós, "
              f"importância {stats['average_importance']:.2f}")

    print(f"   🎯 Progresso Consolidação: {insights['consolidation_progress']:.1%}")
    print(f"   ⚡ Eficiência Aprendizado: {insights['learning_efficiency']:.2f}")

    # Status final
    print("\n📊 STATUS FINAL SDL:")
    status = sdl.get_sdl_status()
    stats = status['learning_stats']

    print(f"   🎯 Modo: {status['learning_mode']}")
    print(f"   📈 Padrões descobertos: {stats['patterns_discovered']}")
    print(f"   🧠 Nós de conhecimento: {stats['knowledge_nodes']}")
    print(f"   🔄 Consolidações realizadas: {stats['consolidations_performed']}")
    print(f"   📚 Sessões de aprendizado: {stats['learning_sessions']}")

    # Parar sistema
    print("\n⏹️ Parando sistema SDL...")
    sdl.stop_learning()

    print("="*70)
    print("🎯 TESTE SDL AUTO-CONSOLIDATION CONCLUÍDO!")
    print("="*70)


if __name__ == "__main__":
    test_sdl_auto_consolidation()