#!/usr/bin/env python3
"""
ConsciousnessStream - Implementação canônica com orçamento estrito
Fase 1: Stub + Compatibilidade (OFF por padrão)
"""
import time
import json
import logging
import threading
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from collections import deque

logger = logging.getLogger(__name__)

class CircuitBreaker:
    """Circuit breaker para prevenir loops infinitos"""
    
    def __init__(self, threshold: int = 5, timeout: float = 60.0):
        self.threshold = threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = 0
        self.state = "closed"  # closed, open, half-open
        self._lock = threading.Lock()
    
    def is_open(self) -> bool:
        """Check if circuit breaker is open"""
        return self.state == "open"
    
    def call(self, func, *args, **kwargs):
        """Executa função com proteção de circuit breaker"""
        with self._lock:
            current_time = time.time()
            
            # Se está aberto, verifica timeout
            if self.state == "open":
                if current_time - self.last_failure_time > self.timeout:
                    self.state = "half-open"
                    logger.info("Circuit breaker: half-open (testing)")
                else:
                    logger.warning("Circuit breaker: open (blocked)")
                    return None
            
            try:
                result = func(*args, **kwargs)
                
                # Reset em caso de sucesso
                if self.state == "half-open":
                    self.state = "closed"
                    self.failures = 0
                    logger.info("Circuit breaker: closed (recovered)")
                
                return result
                
            except Exception as e:
                self.failures += 1
                self.last_failure_time = current_time
                
                if self.failures >= self.threshold:
                    self.state = "open"
                    logger.error(f"Circuit breaker: open after {self.failures} failures")
                
                raise e
    
    def reset(self):
        """Reseta o circuit breaker"""
        with self._lock:
            self.failures = 0
            self.state = "closed"
            logger.info("Circuit breaker: reset")


class BudgetManager:
    """Gerenciador de orçamento para CPU/memória/tempo"""
    
    def __init__(self):
        self.cpu_limit = 40.0  # % máximo de CPU
        self.memory_limit = 100  # MB máximo de memória adicional
        self.time_limit = 30  # segundos por burst
        self.start_time = None
        self.start_memory = None
        
    def start_tracking(self):
        """Inicia rastreamento de recursos"""
        self.start_time = time.time()
        try:
            import psutil
            process = psutil.Process()
            self.start_memory = process.memory_info().rss / 1024 / 1024  # MB
        except:
            self.start_memory = 0
    
    def check_budget(self) -> bool:
        """Verifica se ainda está dentro do orçamento"""
        if not self.start_time:
            return True
            
        # Verifica tempo
        elapsed = time.time() - self.start_time
        if elapsed > self.time_limit:
            logger.warning(f"Budget exceeded: time {elapsed:.1f}s > {self.time_limit}s")
            return False
        
        # Verifica CPU (simplificado)
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.1)
            if cpu_percent > self.cpu_limit:
                logger.warning(f"Budget exceeded: CPU {cpu_percent:.1f}% > {self.cpu_limit}%")
                return False
        except:
            pass
        
        return True


class ConsciousnessStream:
    """
    Stream de consciência com orçamento estrito e proteções
    OFF por padrão - opt-in via configuração
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Feature flags - OFF por padrão
        self.enabled = self.config.get("enabled", False)
        self.mode = self.config.get("mode", "off")  # off, bursts, dream
        self.bursts_enabled = self.config.get("bursts", False)
        self.dream_enabled = self.config.get("dream", False)
        
        # Proteções
        self.circuit_breaker = CircuitBreaker(threshold=3, timeout=60)
        self.budget_manager = BudgetManager()
        
        # Estado
        self.thread = None
        self.stop_event = threading.Event()
        self.is_running = False
        self.iteration_count = 0
        self.max_iterations = 1000
        
        # Insights buffer
        self.insights_buffer = deque(maxlen=100)
        self.insights_dir = Path("reports/consciousness")
        
        # Idle detection
        self.last_activity_time = time.time()
        self.idle_threshold = 120  # 2 minutos
        
        # Semáforo para modelos
        self.model_semaphore = threading.Semaphore(1)
        
        logger.info(f"ConsciousnessStream initialized: enabled={self.enabled}, mode={self.mode}")
    
    def start(self):
        """Inicia o stream (apenas se habilitado)"""
        if not self.enabled:
            logger.debug("ConsciousnessStream.start() called but disabled")
            return
        
        if self.is_running:
            logger.warning("ConsciousnessStream already running")
            return
        
        self.stop_event.clear()
        self.is_running = True
        
        # Cria thread daemon (não bloqueia shutdown)
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
        logger.info(f"ConsciousnessStream started in mode: {self.mode}")
    
    def stop(self):
        """Para o stream gracefully"""
        if not self.is_running:
            return
        
        logger.info("Stopping ConsciousnessStream...")
        self.stop_event.set()
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        
        self.is_running = False
        logger.info("ConsciousnessStream stopped")
    
    def tick(self) -> Optional[Dict[str, Any]]:
        """
        Executa um tick de processamento (no-op se desabilitado)
        Retorna insight gerado ou None
        """
        if not self.enabled:
            return None
        
        # Proteção contra loops
        self.iteration_count += 1
        if self.iteration_count > self.max_iterations:
            logger.warning(f"Max iterations reached: {self.max_iterations}")
            self.stop()
            return None
        
        # Verifica orçamento
        if not self.budget_manager.check_budget():
            return None
        
        # Placeholder para lógica real (será implementado na Fase 2)
        insight = {
            "timestamp": datetime.now().isoformat(),
            "iteration": self.iteration_count,
            "type": "stub",
            "content": "Consciousness tick (stub implementation)"
        }
        
        return insight
    
    # ============ PHASE 1 COMPATIBILITY SHIM ============
    def process(self, input_data: str, budget_ms: int = 200) -> dict:
        """
        Non-blocking process method with circuit breaker and budget.
        Compatibility shim for missing process() method.
        
        Args:
            input_data: Input string to process
            budget_ms: Maximum milliseconds allowed (default 200ms)
            
        Returns:
            dict with processing result or circuit breaker status
        """
        import time
        start_time = time.time()
        
        # Check circuit breaker first
        if hasattr(self, 'circuit_breaker') and self.circuit_breaker.is_open():
            return {
                'status': 'circuit_open',
                'message': 'Circuit breaker is open',
                'processed': False
            }
        
        try:
            # Non-blocking processing with budget
            result = None
            
            # Try stream method if available
            if hasattr(self, 'stream'):
                # Start streaming if not running
                if not self.is_running:
                    self.stream()
                
                # Get current insight within budget
                deadline = start_time + (budget_ms / 1000.0)
                while time.time() < deadline:
                    insight = self.tick()
                    if insight:
                        result = {
                            'status': 'success',
                            'data': insight,
                            'input': input_data,
                            'processed': True
                        }
                        break
                    time.sleep(0.01)  # Small sleep to prevent CPU spinning
            
            # Fallback if no result within budget
            if not result:
                result = {
                    'status': 'timeout',
                    'message': f'Processing exceeded {budget_ms}ms budget',
                    'input': input_data,
                    'processed': False
                }
            
            # Update circuit breaker on success
            if hasattr(self, 'circuit_breaker') and result['processed']:
                self.circuit_breaker.call_succeeded()
                
            return result
            
        except Exception as e:
            # Update circuit breaker on failure
            if hasattr(self, 'circuit_breaker'):
                self.circuit_breaker.call_failed()
            
            # Fail loud as requested
            raise RuntimeError(f"consciousness.process() failed: {e}")
    # ============ END PHASE 1 SHIM ============
    
    def _run_loop(self):
        """Loop principal do stream (roda em thread separada)"""
        logger.info(f"ConsciousnessStream loop started: mode={self.mode}")
        
        while not self.stop_event.is_set():
            try:
                if self.mode == "off":
                    # Modo OFF - apenas dorme
                    time.sleep(1)
                    
                elif self.mode == "bursts":
                    # Modo bursts - ciclos curtos
                    self._run_burst()
                    # Espera próximo burst (45 min default)
                    self.stop_event.wait(timeout=2700)
                    
                elif self.mode == "dream":
                    # Modo dream - apenas durante janela
                    if self._in_dream_window():
                        self._run_dream_cycle()
                    time.sleep(300)  # Check a cada 5 min
                    
                else:
                    # Modo desconhecido - dorme
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error in consciousness loop: {e}")
                time.sleep(5)  # Backoff on error
        
        logger.info("ConsciousnessStream loop ended")
    
    def _run_burst(self):
        """Executa um burst de consciência (Fase 2)"""
        if not self.bursts_enabled:
            return
        
        try:
            # Importa e usa o orchestrator real
            from apps.scripturemon.canonical.consciousness_bursts import create_burst_orchestrator
            
            # Cria orchestrator com config
            orchestrator = create_burst_orchestrator({
                "max_insights_per_burst": 3,
                "burst_duration": 30,
                "ticks_per_burst": 20,
                "tick_interval": 0.5,
                "idle_threshold": self.idle_threshold,
                "cpu_limit": self.budget_manager.cpu_limit
            })
            
            # Sincroniza estado de idle
            orchestrator.last_user_activity = self.last_activity_time
            
            # Executa burst
            burst_result = orchestrator.run_burst()
            
            # Processa insights
            if burst_result.get("insights"):
                for insight in burst_result["insights"]:
                    self.insights_buffer.append(insight)
                
                # Salva insights se houver muitos
                if len(self.insights_buffer) > 50:
                    self.save_insights()
            
            logger.info(f"Burst completed: {burst_result.get('ticks', 0)} ticks, "
                       f"{len(burst_result.get('insights', []))} insights")
            
        except ImportError:
            # Fallback para implementação simples
            logger.debug("Burst orchestrator not available, using simple implementation")
            self.budget_manager.start_tracking()
            
            for _ in range(20):  # 20 ticks por burst
                if not self.budget_manager.check_budget():
                    break
                
                insight = self.tick()
                if insight:
                    self.insights_buffer.append(insight)
                
                time.sleep(0.5)  # 500ms entre ticks
            
            logger.debug(f"Simple burst completed: {len(self.insights_buffer)} insights")
    
    def _run_dream_cycle(self):
        """Executa ciclo dream (Fase 3)"""
        if not self.dream_enabled:
            return
        
        try:
            # Importa e usa o dream orchestrator
            from apps.scripturemon.canonical.consciousness_dream import create_dream_orchestrator
            
            # Cria orchestrator com config
            dream_config = {
                "max_model_size": self.config.get("dream_max_model", "14b"),
                "max_insights_per_dream": 10,
                "dream_duration": 600,
                "dream_start_hour": self.config.get("dream_start_hour", 1),
                "dream_end_hour": self.config.get("dream_end_hour", 5)
            }
            
            orchestrator = create_dream_orchestrator(dream_config)
            
            # Adiciona tarefas pendentes (exemplo)
            # Em produção, isso viria de uma fila persistente
            orchestrator.add_pending_task(
                "memory_consolidation",
                {"max_age_days": 7, "min_similarity": 0.8},
                priority=8
            )
            
            # Executa ciclo dream
            dream_result = orchestrator.run_dream_cycle()
            
            # Processa insights
            if dream_result.get("insights"):
                for insight in dream_result["insights"]:
                    self.insights_buffer.append({
                        "type": "dream",
                        "content": insight,
                        "timestamp": datetime.now().isoformat()
                    })
                
                # Salva insights
                orchestrator.save_dream_insights()
            
            logger.info(f"Dream cycle completed: {dream_result.get('tasks_processed', 0)} tasks, "
                       f"{len(dream_result.get('insights', []))} insights")
            
        except ImportError:
            logger.debug("Dream orchestrator not available")
            pass
    
    def _in_dream_window(self) -> bool:
        """Verifica se está na janela de dream (01:00-05:00)"""
        current_hour = datetime.now().hour
        return 1 <= current_hour <= 5
    
    def is_idle(self) -> bool:
        """Verifica se o sistema está idle"""
        return (time.time() - self.last_activity_time) > self.idle_threshold
    
    def mark_activity(self):
        """Marca atividade do usuário"""
        self.last_activity_time = time.time()
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual para relatórios"""
        return {
            "enabled": self.enabled,
            "mode": self.mode,
            "bursts": self.bursts_enabled,
            "dream": self.dream_enabled,
            "running": self.is_running,
            "iterations": self.iteration_count,
            "insights_count": len(self.insights_buffer),
            "circuit_breaker": self.circuit_breaker.state,
            "idle": self.is_idle()
        }
    
    def save_insights(self):
        """Salva insights em disco (com throttle)"""
        if not self.insights_buffer:
            return
        
        # Cria diretório se necessário
        self.insights_dir.mkdir(parents=True, exist_ok=True)
        
        # Salva com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = self.insights_dir / f"insights_{timestamp}.json"
        
        insights = list(self.insights_buffer)
        self.insights_buffer.clear()
        
        with open(filepath, 'w') as f:
            json.dump({
                "timestamp": timestamp,
                "mode": self.mode,
                "count": len(insights),
                "insights": insights
            }, f, indent=2)
        
        logger.info(f"Saved {len(insights)} insights to {filepath}")


# Singleton global (OFF por padrão)
_consciousness_instance: Optional[ConsciousnessStream] = None


def get_consciousness(config: Optional[Dict[str, Any]] = None) -> ConsciousnessStream:
    """Retorna instância singleton do ConsciousnessStream"""
    global _consciousness_instance
    
    if _consciousness_instance is None:
        _consciousness_instance = ConsciousnessStream(config)
    
    return _consciousness_instance


def initialize(config: Optional[Dict[str, Any]] = None):
    """Inicializa ConsciousnessStream com configuração"""
    consciousness = get_consciousness(config)
    
    if consciousness.enabled:
        logger.info(f"Initializing ConsciousnessStream: {config}")
        consciousness.start()
    else:
        logger.debug("ConsciousnessStream disabled by config")
    
    return consciousness


def shutdown():
    """Desliga ConsciousnessStream gracefully"""
    global _consciousness_instance
    
    if _consciousness_instance and _consciousness_instance.is_running:
        _consciousness_instance.stop()
        _consciousness_instance.save_insights()
        logger.info("ConsciousnessStream shutdown complete")