#!/usr/bin/env python3
"""
Consciousness Bursts - Fase 2
Implementação de ciclos orçados de consciência
"""
import time
import json
import hashlib
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)


class InsightManager:
    """Gerenciador de insights com deduplicação e scoring"""
    
    def __init__(self, max_per_burst: int = 3):
        self.max_per_burst = max_per_burst
        self.seen_hashes = set()
        self.current_burst = []
        
    def add_candidate(self, content: str, metadata: Dict[str, Any]) -> bool:
        """Adiciona candidato a insight se passar nos filtros"""
        
        # Calcula hash para deduplicação
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        
        if content_hash in self.seen_hashes:
            logger.debug(f"Insight duplicado ignorado: {content_hash}")
            return False
        
        # Calcula score de utilidade
        score = self._calculate_score(content, metadata)
        
        if score < 0.3:  # Threshold mínimo
            logger.debug(f"Insight com score baixo ignorado: {score:.2f}")
            return False
        
        # Adiciona se houver espaço
        if len(self.current_burst) < self.max_per_burst:
            self.current_burst.append({
                "content": content,
                "metadata": metadata,
                "score": score,
                "hash": content_hash,
                "timestamp": datetime.now().isoformat()
            })
            self.seen_hashes.add(content_hash)
            return True
        
        return False
    
    def _calculate_score(self, content: str, metadata: Dict[str, Any]) -> float:
        """Calcula score de utilidade do insight"""
        score = 0.5  # Base
        
        # Densidade (palavras únicas / total)
        words = content.lower().split()
        if words:
            unique_ratio = len(set(words)) / len(words)
            score += unique_ratio * 0.3
        
        # Novidade temporal
        if "is_recent" in metadata and metadata["is_recent"]:
            score += 0.2
        
        # Relevância temática
        if "relevance" in metadata:
            score += metadata["relevance"] * 0.2
        
        return min(score, 1.0)
    
    def get_burst_insights(self) -> List[Dict[str, Any]]:
        """Retorna insights do burst atual e limpa"""
        insights = self.current_burst[:]
        self.current_burst = []
        return insights


class MemoryScanner:
    """Scanner leve de memória para detectar tópicos quentes"""
    
    def __init__(self):
        self.hot_topics = deque(maxlen=10)
        self.scan_count = 0
        
    def scan_light(self) -> List[Tuple[str, float]]:
        """Varredura leve de memória - retorna tópicos e scores"""
        self.scan_count += 1
        
        try:
            # Tenta usar Crystal Memory se disponível
            from apps.scripturemon.crystal_memory_restored import get_memory_patterns
            patterns = get_memory_patterns(limit=5)
            
            topics = []
            for pattern in patterns:
                topic = pattern.get("topic", "unknown")
                heat = pattern.get("access_count", 0) / 10.0  # Normaliza
                topics.append((topic, min(heat, 1.0)))
            
            return topics
            
        except ImportError:
            # Fallback para mock
            logger.debug("Crystal Memory não disponível, usando mock")
            return [
                ("screenplay_structure", 0.7),
                ("character_development", 0.5),
                ("dialogue_patterns", 0.6)
            ]
    
    def mark_hot(self, topic: str):
        """Marca tópico como quente"""
        self.hot_topics.append({
            "topic": topic,
            "timestamp": time.time()
        })


class LightweightRAG:
    """RAG leve para bursts - sem modelos pesados"""
    
    def __init__(self, top_k: int = 3):
        self.top_k = top_k
        
    def retrieve_context(self, query: str) -> List[Dict[str, Any]]:
        """Recupera contexto relevante com TF-IDF ou ChromaDB"""
        
        try:
            # Tenta ChromaDB primeiro
            from apps.scripturemon.rag_client import search_documents
            results = search_documents(query, limit=self.top_k)
            return results
            
        except ImportError:
            # Fallback para TF-IDF simples
            logger.debug("ChromaDB não disponível, usando TF-IDF mock")
            return [
                {"text": "Contexto mock 1", "score": 0.8},
                {"text": "Contexto mock 2", "score": 0.6},
                {"text": "Contexto mock 3", "score": 0.4}
            ]


class BurstOrchestrator:
    """Orquestrador de bursts com todas as proteções"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.insight_manager = InsightManager(max_per_burst=config.get("max_insights_per_burst", 3))
        self.memory_scanner = MemoryScanner()
        self.rag = LightweightRAG(top_k=3)
        
        # Controles de burst
        self.burst_duration = config.get("burst_duration", 30)  # segundos
        self.ticks_per_burst = config.get("ticks_per_burst", 20)
        self.tick_interval = config.get("tick_interval", 0.5)  # segundos
        
        # Idle detection
        self.last_user_activity = time.time()
        self.idle_threshold = config.get("idle_threshold", 120)  # 2 minutos
        
        # CPU guard
        self.cpu_limit = config.get("cpu_limit", 40.0)
        
    def should_run_burst(self) -> bool:
        """Verifica se deve rodar burst agora"""
        
        # Verifica idle
        if not self.is_idle():
            logger.debug("Sistema não está idle, pulando burst")
            return False
        
        # Verifica CPU
        if not self.check_cpu():
            logger.debug("CPU muito alta, pulando burst")
            return False
        
        # Verifica se há pipeline pesado rodando
        if self.heavy_pipeline_running():
            logger.debug("Pipeline pesado rodando, pulando burst")
            return False
        
        return True
    
    def is_idle(self) -> bool:
        """Verifica se sistema está idle"""
        idle_time = time.time() - self.last_user_activity
        return idle_time > self.idle_threshold
    
    def check_cpu(self) -> bool:
        """Verifica se CPU está abaixo do limite"""
        try:
            import psutil
            cpu_avg = psutil.cpu_percent(interval=1)
            return cpu_avg < self.cpu_limit
        except ImportError:
            # Sem psutil, assume OK
            return True
    
    def heavy_pipeline_running(self) -> bool:
        """Verifica se há pipeline pesado rodando"""
        # Check via semáforo ou flag global
        try:
            from apps.scripturemon.pipeline_monitor import is_heavy_running
            return is_heavy_running()
        except:
            return False
    
    def mark_user_activity(self):
        """Marca atividade do usuário"""
        self.last_user_activity = time.time()
    
    def run_burst(self) -> Dict[str, Any]:
        """Executa um burst completo"""
        
        if not self.should_run_burst():
            return {"status": "skipped", "reason": "conditions not met"}
        
        logger.info("Starting consciousness burst...")
        start_time = time.time()
        burst_results = {
            "start": datetime.now().isoformat(),
            "ticks": 0,
            "insights": [],
            "errors": []
        }
        
        try:
            for tick_num in range(self.ticks_per_burst):
                # Verifica tempo
                if time.time() - start_time > self.burst_duration:
                    logger.info(f"Burst timeout after {tick_num} ticks")
                    break
                
                # Executa tick
                tick_result = self.execute_tick(tick_num)
                burst_results["ticks"] += 1
                
                # Processa resultado
                if tick_result and "insight" in tick_result:
                    self.insight_manager.add_candidate(
                        tick_result["insight"],
                        tick_result.get("metadata", {})
                    )
                
                # Pausa entre ticks
                time.sleep(self.tick_interval)
                
                # Verifica interrupção
                if not self.is_idle():
                    logger.info("User activity detected, stopping burst")
                    break
        
        except Exception as e:
            logger.error(f"Error during burst: {e}")
            burst_results["errors"].append(str(e))
        
        # Coleta insights finais
        burst_results["insights"] = self.insight_manager.get_burst_insights()
        burst_results["end"] = datetime.now().isoformat()
        burst_results["duration"] = time.time() - start_time
        
        logger.info(f"Burst completed: {burst_results['ticks']} ticks, {len(burst_results['insights'])} insights")
        
        return burst_results
    
    def execute_tick(self, tick_num: int) -> Optional[Dict[str, Any]]:
        """Executa um tick do burst"""
        
        try:
            # 1. Scan de memória
            hot_topics = self.memory_scanner.scan_light()
            
            if not hot_topics:
                return None
            
            # 2. Pega tópico mais quente
            topic, heat = max(hot_topics, key=lambda x: x[1])
            
            # 3. Recupera contexto via RAG leve
            contexts = self.rag.retrieve_context(topic)
            
            # 4. Sintetiza insight (sem modelo, heurística)
            insight = self.synthesize_insight(topic, contexts, heat)
            
            return {
                "tick": tick_num,
                "insight": insight,
                "metadata": {
                    "topic": topic,
                    "heat": heat,
                    "context_count": len(contexts),
                    "is_recent": heat > 0.7,
                    "relevance": heat
                }
            }
            
        except Exception as e:
            logger.debug(f"Tick {tick_num} failed: {e}")
            return None
    
    def synthesize_insight(self, topic: str, contexts: List[Dict], heat: float) -> str:
        """Sintetiza insight sem usar modelo (heurística)"""
        
        # Heurística simples baseada em padrões
        if heat > 0.8:
            prefix = "Critical pattern detected"
        elif heat > 0.5:
            prefix = "Notable pattern emerging"
        else:
            prefix = "Background pattern observed"
        
        # Combina contextos
        context_summary = ""
        if contexts:
            top_context = contexts[0].get("text", "")[:100]
            context_summary = f" related to: {top_context}"
        
        insight = f"{prefix} in {topic}{context_summary}"
        
        return insight


def create_burst_orchestrator(config: Optional[Dict[str, Any]] = None) -> BurstOrchestrator:
    """Factory para criar orchestrator configurado"""
    
    default_config = {
        "max_insights_per_burst": 3,
        "burst_duration": 30,
        "ticks_per_burst": 20,
        "tick_interval": 0.5,
        "idle_threshold": 120,
        "cpu_limit": 40.0
    }
    
    if config:
        default_config.update(config)
    
    return BurstOrchestrator(default_config)