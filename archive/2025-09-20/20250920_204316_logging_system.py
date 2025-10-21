#!/usr/bin/env python3
"""
📊 LOGGING SYSTEM - Sistema de Logging Centralizado
Substitui 2,096+ prints por logging estruturado e observabilidade
"""

import logging
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from contextlib import contextmanager

class LogLevel(Enum):
    """Níveis de log customizados"""
    TRACE = 5      # Muito detalhado
    DEBUG = 10     # Debugging
    INFO = 20      # Informação geral
    SUCCESS = 25   # Operações bem-sucedidas
    WARNING = 30   # Avisos
    ERROR = 40     # Erros
    CRITICAL = 50  # Crítico

class LogCategory(Enum):
    """Categorias de log para filtragem"""
    SYSTEM = "system"
    MEMORY = "memory"
    OLLAMA = "ollama"
    ANALYSIS = "analysis"
    PERFORMANCE = "performance"
    ERROR = "error"
    USER = "user"
    SECURITY = "security"
    ML = "ml"
    CLI = "cli"

@dataclass
class LogEntry:
    """Entrada estruturada de log"""
    timestamp: datetime
    level: str
    category: str
    message: str
    component: str
    metadata: Dict[str, Any]
    session_id: str
    thread_id: str
    execution_time: Optional[float] = None

class ScriptureMonLogger:
    """
    Logger centralizado para ScriptureMon
    Substitui todos os prints por logging estruturado
    """

    def __init__(self, name: str = "scripturemon", base_path: Path = None):
        self.name = name
        self.base_path = base_path or Path("logs")
        self.base_path.mkdir(exist_ok=True)

        # Session tracking
        self.session_id = f"session_{int(time.time())}"
        self._metrics = {}
        self._lock = threading.Lock()

        # Configure logging
        self._setup_logging()

        # Performance tracking
        self._timers = {}

    def _setup_logging(self):
        """Configura sistema de logging multi-target"""

        # Criar custom levels
        logging.addLevelName(LogLevel.TRACE.value, "TRACE")
        logging.addLevelName(LogLevel.SUCCESS.value, "SUCCESS")

        # Logger principal
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(LogLevel.TRACE.value)

        # Remover handlers existentes
        self.logger.handlers.clear()

        # 1. Console Handler (colorido)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LogLevel.INFO.value)
        console_formatter = ColorFormatter(
            '%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # 2. File Handler (JSON estruturado)
        log_file = self.base_path / f"{self.name}_{datetime.now().strftime('%Y%m%d')}.jsonl"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(LogLevel.TRACE.value)
        file_formatter = JSONFormatter()
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # 3. Error Handler (apenas erros)
        error_file = self.base_path / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = logging.FileHandler(error_file)
        error_handler.setLevel(LogLevel.ERROR.value)
        error_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s'
        )
        error_handler.setFormatter(error_formatter)
        self.logger.addHandler(error_handler)

    def log(self, level: LogLevel, message: str, category: LogCategory = LogCategory.SYSTEM,
            component: str = "unknown", **metadata):
        """Log estruturado principal"""

        with self._lock:
            # Criar entrada estruturada
            entry = LogEntry(
                timestamp=datetime.now(),
                level=level.name,
                category=category.value,
                message=message,
                component=component,
                metadata=metadata,
                session_id=self.session_id,
                thread_id=threading.current_thread().name
            )

            # Log usando logger padrão
            extra = {
                'category': category.value,
                'component': component,
                'session_id': self.session_id,
                'metadata': metadata
            }

            self.logger.log(level.value, message, extra=extra)

            # Atualizar métricas
            self._update_metrics(level, category)

    def _update_metrics(self, level: LogLevel, category: LogCategory):
        """Atualiza métricas internas"""
        key = f"{level.name}_{category.value}"
        self._metrics[key] = self._metrics.get(key, 0) + 1

        # Métricas gerais
        self._metrics['total_logs'] = self._metrics.get('total_logs', 0) + 1

    # Métodos de conveniência (substituem prints)

    def trace(self, message: str, category: LogCategory = LogCategory.SYSTEM,
              component: str = "unknown", **metadata):
        """Log de trace (muito detalhado)"""
        self.log(LogLevel.TRACE, message, category, component, **metadata)

    def debug(self, message: str, category: LogCategory = LogCategory.SYSTEM,
              component: str = "unknown", **metadata):
        """Log de debug"""
        self.log(LogLevel.DEBUG, message, category, component, **metadata)

    def info(self, message: str, category: LogCategory = LogCategory.SYSTEM,
             component: str = "unknown", **metadata):
        """Log de informação (substitui print)"""
        self.log(LogLevel.INFO, message, category, component, **metadata)

    def success(self, message: str, category: LogCategory = LogCategory.SYSTEM,
                component: str = "unknown", **metadata):
        """Log de sucesso (operações bem-sucedidas)"""
        self.log(LogLevel.SUCCESS, message, category, component, **metadata)

    def warning(self, message: str, category: LogCategory = LogCategory.SYSTEM,
                component: str = "unknown", **metadata):
        """Log de warning"""
        self.log(LogLevel.WARNING, message, category, component, **metadata)

    def error(self, message: str, category: LogCategory = LogCategory.ERROR,
              component: str = "unknown", **metadata):
        """Log de erro"""
        self.log(LogLevel.ERROR, message, category, component, **metadata)

    def critical(self, message: str, category: LogCategory = LogCategory.ERROR,
                 component: str = "unknown", **metadata):
        """Log crítico"""
        self.log(LogLevel.CRITICAL, message, category, component, **metadata)

    @contextmanager
    def timer(self, operation: str, category: LogCategory = LogCategory.PERFORMANCE,
              component: str = "unknown", **metadata):
        """Context manager para medir tempo de operações"""
        start_time = time.perf_counter()
        timer_id = f"{component}_{operation}_{int(time.time())}"

        self.debug(f"⏱️ Iniciando: {operation}", category, component, **metadata)

        try:
            yield timer_id
        finally:
            execution_time = time.perf_counter() - start_time

            # Log do resultado
            self.info(
                f"⚡ Concluído: {operation} em {execution_time:.3f}s",
                category,
                component,
                execution_time=execution_time,
                **metadata
            )

            # Salvar métricas de performance
            perf_key = f"perf_{component}_{operation}"
            if perf_key not in self._metrics:
                self._metrics[perf_key] = []
            self._metrics[perf_key].append(execution_time)

    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas coletadas"""
        with self._lock:
            metrics = self._metrics.copy()

            # Calcular estatísticas de performance
            perf_stats = {}
            for key, values in metrics.items():
                if key.startswith('perf_') and isinstance(values, list):
                    if values:
                        perf_stats[key] = {
                            'count': len(values),
                            'avg': sum(values) / len(values),
                            'min': min(values),
                            'max': max(values),
                            'total': sum(values)
                        }

            return {
                'session_id': self.session_id,
                'log_counts': {k: v for k, v in metrics.items() if not k.startswith('perf_')},
                'performance': perf_stats,
                'total_logs': metrics.get('total_logs', 0)
            }

    def export_metrics(self, format: str = "json") -> str:
        """Exporta métricas em formato específico"""
        metrics = self.get_metrics()

        if format == "json":
            return json.dumps(metrics, indent=2, default=str)
        elif format == "summary":
            total = metrics['total_logs']
            return f"""
📊 MÉTRICAS DE LOGGING - Sessão {self.session_id}
{'='*50}
Total de logs: {total:,}
Categorias mais ativas:
{chr(10).join([f'  {k}: {v}' for k, v in sorted(metrics['log_counts'].items(), key=lambda x: x[1], reverse=True)[:5]])}

Performance (operações mais lentas):
{chr(10).join([f'  {k.replace("perf_", "")}: {v["avg"]:.3f}s avg' for k, v in sorted(metrics['performance'].items(), key=lambda x: x[1]['avg'], reverse=True)[:3]])}
            """.strip()

        return str(metrics)

class ColorFormatter(logging.Formatter):
    """Formatter colorido para console"""

    COLORS = {
        'TRACE': '\033[90m',     # Cinza
        'DEBUG': '\033[94m',     # Azul
        'INFO': '\033[92m',      # Verde
        'SUCCESS': '\033[96m',   # Ciano
        'WARNING': '\033[93m',   # Amarelo
        'ERROR': '\033[91m',     # Vermelho
        'CRITICAL': '\033[95m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }

    def format(self, record):
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

class JSONFormatter(logging.Formatter):
    """Formatter JSON estruturado para arquivos"""

    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'thread': record.threadName
        }

        # Adicionar campos extras se existirem
        if hasattr(record, 'category'):
            log_entry['category'] = record.category
        if hasattr(record, 'component'):
            log_entry['component'] = record.component
        if hasattr(record, 'session_id'):
            log_entry['session_id'] = record.session_id
        if hasattr(record, 'metadata'):
            log_entry['metadata'] = record.metadata

        return json.dumps(log_entry)

# Singleton global
_global_logger = None

def get_logger(name: str = "scripturemon") -> ScriptureMonLogger:
    """Retorna logger singleton"""
    global _global_logger
    if _global_logger is None:
        _global_logger = ScriptureMonLogger(name)
    return _global_logger

# Funções de conveniência para substituir prints
def log_info(message: str, category: LogCategory = LogCategory.SYSTEM, component: str = "unknown", **metadata):
    """Substituto direto para print()"""
    get_logger().info(message, category, component, **metadata)

def log_success(message: str, category: LogCategory = LogCategory.SYSTEM, component: str = "unknown", **metadata):
    """Log de sucesso"""
    get_logger().success(message, category, component, **metadata)

def log_warning(message: str, category: LogCategory = LogCategory.SYSTEM, component: str = "unknown", **metadata):
    """Log de warning"""
    get_logger().warning(message, category, component, **metadata)

def log_error(message: str, category: LogCategory = LogCategory.ERROR, component: str = "unknown", **metadata):
    """Log de erro"""
    get_logger().error(message, category, component, **metadata)

def log_debug(message: str, category: LogCategory = LogCategory.SYSTEM, component: str = "unknown", **metadata):
    """Log de debug"""
    get_logger().debug(message, category, component, **metadata)

# Context manager para timing
def timed_operation(operation: str, category: LogCategory = LogCategory.PERFORMANCE,
                   component: str = "unknown", **metadata):
    """Context manager para operações cronometradas"""
    return get_logger().timer(operation, category, component, **metadata)

# Exports
__all__ = [
    'ScriptureMonLogger',
    'LogLevel',
    'LogCategory',
    'get_logger',
    'log_info',
    'log_success',
    'log_warning',
    'log_error',
    'log_debug',
    'timed_operation'
]

# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado
from src.core.unified_memory_system import get_unified_memory, MemoryType

def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()