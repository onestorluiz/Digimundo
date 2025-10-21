"""
Production Monitoring System.
Tracks performance, errors, and system health.
"""

import time
import psutil
import logging
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from threading import Thread, Lock
from collections import deque
import traceback

logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Coleta métricas de sistema e aplicação.
    Otimizado para Mac Studio M3 Ultra.
    """

    def __init__(self, metrics_dir: Optional[Path] = None):
        """
        Inicializa o coletor de métricas.

        Args:
            metrics_dir: Diretório para salvar métricas
        """
        self.metrics_dir = metrics_dir or Path.home() / '.scripturemon_metrics'
        self.metrics_dir.mkdir(parents=True, exist_ok=True)

        # Buffers circulares para métricas recentes
        self.cpu_history = deque(maxlen=100)
        self.memory_history = deque(maxlen=100)
        self.gpu_history = deque(maxlen=100)  # GPU metrics
        self.request_times = deque(maxlen=1000)
        self.error_log = deque(maxlen=100)

        # Contadores
        self.counters = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'ollama_calls': 0,
            'pipeline_runs': 0
        }

        # Lock para thread safety
        self.lock = Lock()

        # Thread de coleta contínua
        self.collecting = True
        self.collector_thread = Thread(target=self._collect_system_metrics, daemon=True)
        self.collector_thread.start()

        logger.info("MetricsCollector initialized")

    def _collect_system_metrics(self):
        """Thread que coleta métricas do sistema continuamente."""
        while self.collecting:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self.cpu_history.append({
                    'timestamp': time.time(),
                    'value': cpu_percent
                })

                # Memory usage
                memory = psutil.virtual_memory()
                self.memory_history.append({
                    'timestamp': time.time(),
                    'percent': memory.percent,
                    'used_gb': memory.used / (1024**3),
                    'available_gb': memory.available / (1024**3)
                })

                # GPU metrics (M3 specific - via Metal Performance Shaders)
                # Note: Real GPU metrics would require pyobjc-framework-Metal
                # This is a placeholder
                gpu_metrics = self._get_gpu_metrics()
                if gpu_metrics:
                    self.gpu_history.append({
                        'timestamp': time.time(),
                        **gpu_metrics
                    })

            except Exception as e:
                logger.error(f"Error collecting system metrics: {e}")

            time.sleep(5)  # Coleta a cada 5 segundos

    def _get_gpu_metrics(self) -> Optional[Dict[str, Any]]:
        """
        Obtém métricas da GPU M3 Ultra.
        Placeholder - implementação real requereria Metal framework.
        """
        # TODO: Implementar com pyobjc-framework-Metal
        return None

    def record_request(self, endpoint: str, duration: float, success: bool = True):
        """
        Registra uma requisição.

        Args:
            endpoint: Endpoint chamado
            duration: Duração em segundos
            success: Se foi bem-sucedida
        """
        with self.lock:
            self.counters['total_requests'] += 1

            if success:
                self.counters['successful_requests'] += 1
            else:
                self.counters['failed_requests'] += 1

            self.request_times.append({
                'timestamp': time.time(),
                'endpoint': endpoint,
                'duration': duration,
                'success': success
            })

    def record_error(self, error: Exception, context: str = ""):
        """
        Registra um erro.

        Args:
            error: Exceção ocorrida
            context: Contexto do erro
        """
        with self.lock:
            self.error_log.append({
                'timestamp': time.time(),
                'type': type(error).__name__,
                'message': str(error),
                'context': context,
                'traceback': traceback.format_exc()
            })

    def increment_counter(self, counter_name: str, value: int = 1):
        """Incrementa um contador."""
        with self.lock:
            if counter_name in self.counters:
                self.counters[counter_name] += value

    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Retorna resumo das métricas.

        Returns:
            Dicionário com métricas resumidas
        """
        with self.lock:
            # Calcula estatísticas de requisições
            if self.request_times:
                recent_requests = list(self.request_times)
                avg_duration = sum(r['duration'] for r in recent_requests) / len(recent_requests)
                success_rate = sum(1 for r in recent_requests if r['success']) / len(recent_requests)
            else:
                avg_duration = 0
                success_rate = 1.0

            # CPU e memória atuais
            current_cpu = self.cpu_history[-1]['value'] if self.cpu_history else 0
            current_memory = self.memory_history[-1] if self.memory_history else {
                'percent': 0,
                'used_gb': 0,
                'available_gb': 96
            }

            return {
                'timestamp': datetime.now().isoformat(),
                'system': {
                    'cpu_percent': current_cpu,
                    'memory_percent': current_memory['percent'],
                    'memory_used_gb': current_memory['used_gb'],
                    'memory_available_gb': current_memory['available_gb']
                },
                'application': {
                    'total_requests': self.counters['total_requests'],
                    'success_rate': f"{success_rate * 100:.2f}%",
                    'avg_request_time': f"{avg_duration:.3f}s",
                    'recent_errors': len(self.error_log),
                    'cache_hit_rate': self._calculate_cache_hit_rate()
                },
                'counters': dict(self.counters)
            }

    def _calculate_cache_hit_rate(self) -> str:
        """Calcula taxa de cache hit."""
        total_cache = self.counters['cache_hits'] + self.counters['cache_misses']
        if total_cache > 0:
            rate = self.counters['cache_hits'] / total_cache
            return f"{rate * 100:.2f}%"
        return "N/A"

    def save_metrics(self):
        """Salva métricas em arquivo."""
        try:
            metrics = self.get_metrics_summary()
            filename = f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = self.metrics_dir / filename

            with open(filepath, 'w') as f:
                json.dump(metrics, f, indent=2)

            # Limpa arquivos antigos (mantém últimos 7 dias)
            self._cleanup_old_metrics()

        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")

    def _cleanup_old_metrics(self):
        """Remove arquivos de métricas com mais de 7 dias."""
        cutoff = datetime.now() - timedelta(days=7)

        for filepath in self.metrics_dir.glob("metrics_*.json"):
            try:
                # Parse timestamp from filename
                timestamp_str = filepath.stem.replace("metrics_", "")
                file_date = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")

                if file_date < cutoff:
                    filepath.unlink()
                    logger.debug(f"Removed old metrics file: {filepath.name}")

            except Exception as e:
                logger.warning(f"Failed to cleanup metrics file {filepath}: {e}")

    def stop(self):
        """Para a coleta de métricas."""
        self.collecting = False
        self.save_metrics()
        logger.info("MetricsCollector stopped")


class HealthChecker:
    """
    Verifica saúde do sistema.
    """

    def __init__(self, metrics_collector: MetricsCollector):
        """
        Inicializa health checker.

        Args:
            metrics_collector: Coletor de métricas
        """
        self.metrics = metrics_collector
        self.checks = []

    def check_cpu(self) -> Dict[str, Any]:
        """Verifica uso de CPU."""
        if self.metrics.cpu_history:
            current_cpu = self.metrics.cpu_history[-1]['value']
            status = 'healthy' if current_cpu < 80 else 'warning' if current_cpu < 95 else 'critical'
            return {
                'name': 'CPU Usage',
                'status': status,
                'value': f"{current_cpu:.1f}%",
                'threshold': '80% warning, 95% critical'
            }
        return {'name': 'CPU Usage', 'status': 'unknown', 'value': 'N/A'}

    def check_memory(self) -> Dict[str, Any]:
        """Verifica uso de memória."""
        if self.metrics.memory_history:
            current = self.metrics.memory_history[-1]
            percent = current['percent']
            status = 'healthy' if percent < 80 else 'warning' if percent < 90 else 'critical'
            return {
                'name': 'Memory Usage',
                'status': status,
                'value': f"{percent:.1f}% ({current['used_gb']:.1f}GB / 96GB)",
                'threshold': '80% warning, 90% critical'
            }
        return {'name': 'Memory Usage', 'status': 'unknown', 'value': 'N/A'}

    def check_disk_space(self) -> Dict[str, Any]:
        """Verifica espaço em disco."""
        try:
            disk = psutil.disk_usage('/')
            percent = disk.percent
            status = 'healthy' if percent < 80 else 'warning' if percent < 90 else 'critical'
            return {
                'name': 'Disk Space',
                'status': status,
                'value': f"{percent:.1f}% used",
                'free_gb': f"{disk.free / (1024**3):.1f}GB free"
            }
        except Exception as e:
            return {'name': 'Disk Space', 'status': 'error', 'value': str(e)}

    def check_ollama(self) -> Dict[str, Any]:
        """Verifica status do Ollama."""
        try:
            # Check if ollama is running
            ollama_running = any('ollama' in p.name().lower()
                                for p in psutil.process_iter(['name']))

            if ollama_running:
                return {
                    'name': 'Ollama Service',
                    'status': 'healthy',
                    'value': 'Running'
                }
            else:
                return {
                    'name': 'Ollama Service',
                    'status': 'critical',
                    'value': 'Not running'
                }
        except Exception as e:
            return {'name': 'Ollama Service', 'status': 'error', 'value': str(e)}

    def get_health_status(self) -> Dict[str, Any]:
        """
        Retorna status completo de saúde.

        Returns:
            Dicionário com status de todos os checks
        """
        checks = [
            self.check_cpu(),
            self.check_memory(),
            self.check_disk_space(),
            self.check_ollama()
        ]

        # Overall status
        statuses = [c['status'] for c in checks]
        if 'critical' in statuses:
            overall = 'critical'
        elif 'warning' in statuses:
            overall = 'warning'
        elif 'error' in statuses:
            overall = 'degraded'
        else:
            overall = 'healthy'

        return {
            'timestamp': datetime.now().isoformat(),
            'overall_status': overall,
            'checks': checks,
            'metrics_summary': self.metrics.get_metrics_summary()
        }


# Singleton global
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """Retorna instância singleton do metrics collector."""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector


def get_health_checker() -> HealthChecker:
    """Retorna health checker usando metrics collector global."""
    return HealthChecker(get_metrics_collector())