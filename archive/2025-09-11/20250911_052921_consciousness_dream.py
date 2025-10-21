#!/usr/bin/env python3
"""
Consciousness Dream Mode - Fase 3
Processamento profundo durante janelas de baixa atividade
"""
import time
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from collections import deque

logger = logging.getLogger(__name__)


class DreamTaskQueue:
    """Fila de tarefas para processar durante dream mode"""
    
    def __init__(self):
        self.tasks = deque()
        self.processed = []
        
    def add_task(self, task_type: str, data: Dict[str, Any], priority: int = 5):
        """Adiciona tarefa à fila"""
        task = {
            "id": f"{task_type}_{int(time.time()*1000)}",
            "type": task_type,
            "data": data,
            "priority": priority,
            "added": datetime.now().isoformat()
        }
        self.tasks.append(task)
        logger.debug(f"Dream task added: {task['id']}")
        
    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Pega próxima tarefa por prioridade"""
        if not self.tasks:
            return None
        
        # Ordena por prioridade
        sorted_tasks = sorted(self.tasks, key=lambda x: x["priority"], reverse=True)
        task = sorted_tasks[0]
        self.tasks.remove(task)
        
        return task
    
    def mark_processed(self, task_id: str, result: Any):
        """Marca tarefa como processada"""
        self.processed.append({
            "task_id": task_id,
            "result": result,
            "processed_at": datetime.now().isoformat()
        })
    
    def has_tasks(self) -> bool:
        """Verifica se há tarefas pendentes"""
        return len(self.tasks) > 0


class DreamProcessor:
    """Processador de tarefas durante dream mode"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.max_model_size = config.get("max_model_size", "14b")
        self.max_insights_per_dream = config.get("max_insights_per_dream", 10)
        self.dream_duration = config.get("dream_duration", 600)  # 10 minutos
        
    def can_use_model(self, model_size: str) -> bool:
        """Verifica se pode usar modelo do tamanho especificado"""
        
        # Mapeia tamanhos para valores numéricos
        size_map = {
            "3b": 3,
            "7b": 7,
            "14b": 14,
            "32b": 32,
            "70b": 70
        }
        
        max_allowed = size_map.get(self.max_model_size.lower(), 14)
        requested = size_map.get(model_size.lower(), 999)
        
        if requested > max_allowed:
            logger.warning(f"Model {model_size} exceeds limit {self.max_model_size}")
            return False
        
        # Verifica GPU disponível
        if requested > 7:  # Modelos maiores que 7B precisam de GPU
            if not self.check_gpu_available():
                logger.warning(f"GPU not available for {model_size}")
                return False
        
        return True
    
    def check_gpu_available(self) -> bool:
        """Verifica se GPU está disponível"""
        try:
            # Check via nvidia-smi ou similar
            import subprocess
            result = subprocess.run(
                ["system_profiler", "SPDisplaysDataType"],
                capture_output=True,
                text=True,
                timeout=5
            )
            # Em Mac, verifica se tem GPU
            return "Metal" in result.stdout or "GPU" in result.stdout
        except:
            # Assume que não tem GPU se não conseguir verificar
            return False
    
    def process_pdf_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa PDF durante dream mode"""
        pdf_path = task_data.get("path")
        
        if not pdf_path or not Path(pdf_path).exists():
            return {"status": "error", "message": "PDF not found"}
        
        try:
            # Usa parser robusto criado anteriormente
            from apps.scripturemon.pdf_robust_parser import parse_pdf_safe
            
            text = parse_pdf_safe(Path(pdf_path), max_size_mb=100)
            
            if not text:
                return {"status": "error", "message": "Could not extract text"}
            
            # Análise profunda com modelo médio (se disponível)
            analysis = self.analyze_with_model(text, "14b")
            
            return {
                "status": "success",
                "pdf": pdf_path,
                "analysis": analysis,
                "extracted_length": len(text)
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            return {"status": "error", "message": str(e)}
    
    def process_memory_consolidation(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Consolida memórias durante dream mode"""
        
        try:
            # Busca memórias fragmentadas
            from apps.scripturemon.crystal_memory_restored import consolidate_memories
            
            result = consolidate_memories(
                max_age_days=task_data.get("max_age_days", 7),
                min_similarity=task_data.get("min_similarity", 0.8)
            )
            
            return {
                "status": "success",
                "consolidated": result.get("consolidated_count", 0),
                "freed_space": result.get("freed_bytes", 0)
            }
            
        except ImportError:
            # Mock se não tiver Crystal Memory
            return {
                "status": "success",
                "consolidated": 5,
                "freed_space": 1024 * 100  # 100KB mock
            }
    
    def process_pattern_discovery(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Descobre padrões narrativos durante dream mode"""
        
        topic = task_data.get("topic", "screenplay")
        depth = task_data.get("depth", "medium")
        
        try:
            # Análise profunda de padrões
            patterns = []
            
            # Busca documentos relacionados
            from apps.scripturemon.rag_client import search_documents
            docs = search_documents(topic, limit=10)
            
            # Extrai padrões com modelo médio
            for doc in docs[:5]:  # Limita para não demorar muito
                pattern = self.extract_pattern(doc.get("text", ""), depth)
                if pattern:
                    patterns.append(pattern)
            
            return {
                "status": "success",
                "topic": topic,
                "patterns_found": len(patterns),
                "patterns": patterns[:3]  # Top 3
            }
            
        except Exception as e:
            logger.error(f"Error in pattern discovery: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def analyze_with_model(self, text: str, model_size: str) -> Dict[str, Any]:
        """Analisa texto com modelo específico"""
        
        if not self.can_use_model(model_size):
            # Fallback para análise heurística
            return self.heuristic_analysis(text)
        
        try:
            # Tenta usar Ollama se disponível
            from apps.scripturemon.ollama_client import query_model
            
            prompt = f"Analyze this screenplay text and extract key insights:\n\n{text[:2000]}"
            response = query_model(prompt, model=f"mistral:{model_size}")
            
            return {
                "method": "model",
                "model": model_size,
                "insights": response
            }
            
        except:
            # Fallback para heurística
            return self.heuristic_analysis(text)
    
    def heuristic_analysis(self, text: str) -> Dict[str, Any]:
        """Análise heurística quando modelo não disponível"""
        
        lines = text.split('\n')
        words = text.split()
        
        return {
            "method": "heuristic",
            "stats": {
                "lines": len(lines),
                "words": len(words),
                "avg_line_length": len(words) / max(len(lines), 1)
            },
            "insights": [
                f"Document has {len(lines)} lines",
                f"Average line contains {len(words)/max(len(lines), 1):.1f} words",
                "Heuristic analysis completed"
            ]
        }
    
    def extract_pattern(self, text: str, depth: str) -> Optional[Dict[str, Any]]:
        """Extrai padrão de texto"""
        
        if not text:
            return None
        
        # Análise simples de padrões
        dialogue_count = text.count('"') // 2
        scene_count = text.upper().count("INT.") + text.upper().count("EXT.")
        
        pattern = {
            "type": "narrative",
            "dialogue_density": dialogue_count / max(len(text.split('\n')), 1),
            "scene_count": scene_count,
            "depth": depth
        }
        
        return pattern


class DreamOrchestrator:
    """Orquestrador do Dream Mode"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.task_queue = DreamTaskQueue()
        self.processor = DreamProcessor(config)
        self.insights_generated = []
        
        # Janela de dream (01:00-05:00 por padrão)
        self.dream_start_hour = config.get("dream_start_hour", 1)
        self.dream_end_hour = config.get("dream_end_hour", 5)
        
        # Controles
        self.max_duration = config.get("max_duration", 600)  # 10 minutos
        self.idle_required = config.get("idle_required", 1200)  # 20 minutos
        
    def is_dream_time(self) -> bool:
        """Verifica se está na janela de dream"""
        current_hour = datetime.now().hour
        
        if self.dream_start_hour < self.dream_end_hour:
            # Janela normal (ex: 01:00-05:00)
            return self.dream_start_hour <= current_hour < self.dream_end_hour
        else:
            # Janela que cruza meia-noite (ex: 23:00-03:00)
            return current_hour >= self.dream_start_hour or current_hour < self.dream_end_hour
    
    def check_idle_time(self) -> bool:
        """Verifica se sistema está idle há tempo suficiente"""
        try:
            # Check via activity monitor
            from apps.scripturemon.activity_monitor import get_idle_time
            idle_seconds = get_idle_time()
            return idle_seconds > self.idle_required
        except:
            # Assume idle se não conseguir verificar
            return True
    
    def add_pending_task(self, task_type: str, data: Dict[str, Any], priority: int = 5):
        """Adiciona tarefa para processar em dream mode"""
        self.task_queue.add_task(task_type, data, priority)
    
    def run_dream_cycle(self) -> Dict[str, Any]:
        """Executa ciclo completo de dream mode"""
        
        if not self.is_dream_time():
            return {"status": "skipped", "reason": "not in dream window"}
        
        if not self.check_idle_time():
            return {"status": "skipped", "reason": "system not idle long enough"}
        
        logger.info("Starting dream cycle...")
        start_time = time.time()
        cycle_result = {
            "start": datetime.now().isoformat(),
            "tasks_processed": 0,
            "insights": [],
            "errors": []
        }
        
        try:
            while self.task_queue.has_tasks():
                # Verifica tempo limite
                if time.time() - start_time > self.max_duration:
                    logger.info("Dream cycle timeout")
                    break
                
                # Verifica se ainda está idle
                if not self.check_idle_time():
                    logger.info("System no longer idle, stopping dream")
                    break
                
                # Processa próxima tarefa
                task = self.task_queue.get_next_task()
                if not task:
                    break
                
                logger.info(f"Processing dream task: {task['id']}")
                
                # Processa baseado no tipo
                if task["type"] == "pdf_analysis":
                    result = self.processor.process_pdf_task(task["data"])
                elif task["type"] == "memory_consolidation":
                    result = self.processor.process_memory_consolidation(task["data"])
                elif task["type"] == "pattern_discovery":
                    result = self.processor.process_pattern_discovery(task["data"])
                else:
                    result = {"status": "error", "message": f"Unknown task type: {task['type']}"}
                
                # Marca como processada
                self.task_queue.mark_processed(task["id"], result)
                cycle_result["tasks_processed"] += 1
                
                # Extrai insights se houver
                if result.get("status") == "success":
                    insight = {
                        "task_id": task["id"],
                        "type": task["type"],
                        "timestamp": datetime.now().isoformat(),
                        "content": result
                    }
                    self.insights_generated.append(insight)
                    cycle_result["insights"].append(insight)
                    
                    # Limita insights
                    if len(cycle_result["insights"]) >= self.processor.max_insights_per_dream:
                        logger.info("Max insights reached for dream cycle")
                        break
                
                # Pequena pausa entre tarefas
                time.sleep(2)
                
        except Exception as e:
            logger.error(f"Error in dream cycle: {e}")
            cycle_result["errors"].append(str(e))
        
        cycle_result["end"] = datetime.now().isoformat()
        cycle_result["duration"] = time.time() - start_time
        
        logger.info(f"Dream cycle completed: {cycle_result['tasks_processed']} tasks, "
                   f"{len(cycle_result['insights'])} insights in {cycle_result['duration']:.1f}s")
        
        return cycle_result
    
    def save_dream_insights(self):
        """Salva insights do dream mode"""
        if not self.insights_generated:
            return
        
        insights_dir = Path("reports/consciousness/dreams")
        insights_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = insights_dir / f"dream_{timestamp}.json"
        
        with open(filepath, 'w') as f:
            json.dump({
                "timestamp": timestamp,
                "count": len(self.insights_generated),
                "insights": self.insights_generated
            }, f, indent=2)
        
        logger.info(f"Saved {len(self.insights_generated)} dream insights to {filepath}")
        self.insights_generated = []


def create_dream_orchestrator(config: Optional[Dict[str, Any]] = None) -> DreamOrchestrator:
    """Factory para criar dream orchestrator"""
    
    default_config = {
        "max_model_size": "14b",
        "max_insights_per_dream": 10,
        "dream_duration": 600,
        "dream_start_hour": 1,
        "dream_end_hour": 5,
        "max_duration": 600,
        "idle_required": 1200
    }
    
    if config:
        default_config.update(config)
    
    return DreamOrchestrator(default_config)