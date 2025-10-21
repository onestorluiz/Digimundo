#!/usr/bin/env python3
"""
📡 ADVANCED TELEMETRY & MONITORING SYSTEM
=========================================
Sistema de Telemetria com Análise em Tempo Real
Silicon Valley Grade™ - Observability at Scale

Think Different. Stay Hungry. Stay Foolish.
"""

import os
import sys
import json
import time
import psutil
import socket
import threading
import asyncio
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict, deque
import hashlib
import subprocess
import platform
import traceback
import warnings


class MetricType(Enum):
    """Tipos de métricas"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"
    TRACE = "trace"
    LOG = "log"
    EVENT = "event"
    SPAN = "span"


class AlertSeverity(Enum):
    """Severidade dos alertas"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class Metric:
    """Estrutura de métrica"""
    name: str
    type: MetricType
    value: Any
    timestamp: float
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Alert:
    """Estrutura de alerta"""
    id: str
    severity: AlertSeverity
    title: str
    description: str
    metric_name: str
    threshold: float
    current_value: float
    timestamp: float
    resolved: bool = False
    resolution_time: Optional[float] = None


@dataclass
class Trace:
    """Estrutura de trace distribuído"""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    operation: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    tags: Dict[str, Any] = field(default_factory=dict)
    logs: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "in_progress"


class TelemetryCollector:
    """
    📡 Coletor de Telemetria Avançado

    Features:
    - Real-time metrics collection
    - Distributed tracing
    - Anomaly detection
    - Auto-scaling triggers
    - Performance profiling
    - Resource monitoring
    - Custom dashboards
    - Alert management
    - Log aggregation
    - Predictive analytics
    """

    def __init__(self, name: str = "claude_telemetry"):
        """Inicializa o sistema de telemetria"""
        self.name = name
        self.enabled = True
        self.debug = True

        # Storage
        self.db_path = Path("/Users/clubproducoes/Digimundo/claude_code/telemetry/metrics.db")
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_database()

        # Metrics storage
        self.metrics = defaultdict(deque)
        self.max_metrics_per_type = 10000

        # Alerts
        self.alerts = {}
        self.alert_thresholds = {}
        self.alert_callbacks = []

        # Traces
        self.active_traces = {}
        self.completed_traces = deque(maxlen=1000)

        # System monitoring
        self.system_metrics = {
            'cpu': deque(maxlen=100),
            'memory': deque(maxlen=100),
            'disk': deque(maxlen=100),
            'network': deque(maxlen=100),
            'processes': deque(maxlen=100)
        }

        # Performance profiling
        self.performance_profiles = {}
        self.slow_operations = deque(maxlen=100)

        # Anomaly detection
        self.baselines = {}
        self.anomalies = deque(maxlen=500)

        # Background threads
        self.monitoring_thread = None
        self.aggregation_thread = None
        self.stop_event = threading.Event()

        # Configuration
        self.sampling_rate = 1.0  # 100% sampling
        self.flush_interval = 60  # Flush to disk every 60 seconds
        self.retention_days = 30

        # Start monitoring
        self.start()

        print(f"📡 Telemetry Collector '{name}' initialized")
        print(f"   • Sampling rate: {self.sampling_rate * 100}%")
        print(f"   • Retention: {self.retention_days} days")

    def _init_database(self):
        """Inicializa banco de dados de métricas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                value REAL,
                timestamp REAL NOT NULL,
                tags TEXT,
                metadata TEXT
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_name_timestamp ON metrics (name, timestamp)
        """)

        # Alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id TEXT PRIMARY KEY,
                severity TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                metric_name TEXT,
                threshold REAL,
                current_value REAL,
                timestamp REAL NOT NULL,
                resolved BOOLEAN DEFAULT 0,
                resolution_time REAL
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON alerts (timestamp)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_severity ON alerts (severity)
        """)

        # Traces table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS traces (
                trace_id TEXT NOT NULL,
                span_id TEXT NOT NULL,
                parent_span_id TEXT,
                operation TEXT NOT NULL,
                start_time REAL NOT NULL,
                end_time REAL,
                duration REAL,
                tags TEXT,
                logs TEXT,
                status TEXT,
                PRIMARY KEY (trace_id, span_id)
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_trace_id ON traces (trace_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_operation ON traces (operation)
        """)

        # Performance profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                samples INTEGER,
                avg_duration REAL,
                min_duration REAL,
                max_duration REAL,
                p50 REAL,
                p95 REAL,
                p99 REAL,
                timestamp REAL NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def start(self):
        """Inicia coletores em background"""
        if not self.monitoring_thread:
            self.monitoring_thread = threading.Thread(target=self._monitor_system, daemon=True)
            self.monitoring_thread.start()

        if not self.aggregation_thread:
            self.aggregation_thread = threading.Thread(target=self._aggregate_metrics, daemon=True)
            self.aggregation_thread.start()

    def stop(self):
        """Para os coletores"""
        self.stop_event.set()
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        if self.aggregation_thread:
            self.aggregation_thread.join(timeout=5)

    def _monitor_system(self):
        """Monitor de sistema em background"""
        while not self.stop_event.is_set():
            try:
                # CPU metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                self.record_metric("system.cpu.usage", cpu_percent, MetricType.GAUGE)

                # Memory metrics
                mem = psutil.virtual_memory()
                self.record_metric("system.memory.usage", mem.percent, MetricType.GAUGE)
                self.record_metric("system.memory.available", mem.available, MetricType.GAUGE)

                # Disk metrics
                disk = psutil.disk_usage('/')
                self.record_metric("system.disk.usage", disk.percent, MetricType.GAUGE)
                self.record_metric("system.disk.free", disk.free, MetricType.GAUGE)

                # Network metrics
                net = psutil.net_io_counters()
                self.record_metric("system.network.bytes_sent", net.bytes_sent, MetricType.COUNTER)
                self.record_metric("system.network.bytes_recv", net.bytes_recv, MetricType.COUNTER)

                # Process count
                process_count = len(psutil.pids())
                self.record_metric("system.processes.count", process_count, MetricType.GAUGE)

                # Check for anomalies
                self._detect_anomalies()

                # Check alerts
                self._check_alerts()

            except Exception as e:
                if self.debug:
                    print(f"⚠️ Monitoring error: {e}")

            time.sleep(5)  # Collect every 5 seconds

    def _aggregate_metrics(self):
        """Agrega métricas periodicamente"""
        while not self.stop_event.is_set():
            try:
                time.sleep(self.flush_interval)
                self._flush_to_database()
                self._cleanup_old_data()
                self._calculate_baselines()
            except Exception as e:
                if self.debug:
                    print(f"⚠️ Aggregation error: {e}")

    def record_metric(self, name: str, value: Any, metric_type: MetricType = MetricType.GAUGE,
                      tags: Dict[str, str] = None, metadata: Dict[str, Any] = None):
        """Registra uma métrica"""
        if not self.enabled:
            return

        # Sampling
        if self.sampling_rate < 1.0:
            import random
            if random.random() > self.sampling_rate:
                return

        metric = Metric(
            name=name,
            type=metric_type,
            value=value,
            timestamp=time.time(),
            tags=tags or {},
            metadata=metadata or {}
        )

        # Store in memory
        self.metrics[name].append(metric)

        # Limit memory usage
        if len(self.metrics[name]) > self.max_metrics_per_type:
            self.metrics[name].popleft()

        # Check for slow operations
        if metric_type == MetricType.HISTOGRAM and "duration" in name:
            if value > 1.0:  # Operations slower than 1 second
                self.slow_operations.append({
                    'operation': name,
                    'duration': value,
                    'timestamp': metric.timestamp,
                    'tags': tags
                })

    def increment_counter(self, name: str, value: int = 1, tags: Dict[str, str] = None):
        """Incrementa um contador"""
        self.record_metric(name, value, MetricType.COUNTER, tags)

    def set_gauge(self, name: str, value: float, tags: Dict[str, str] = None):
        """Define um gauge"""
        self.record_metric(name, value, MetricType.GAUGE, tags)

    def record_histogram(self, name: str, value: float, tags: Dict[str, str] = None):
        """Registra valor em histograma"""
        self.record_metric(name, value, MetricType.HISTOGRAM, tags)

    def start_trace(self, operation: str, trace_id: Optional[str] = None,
                    parent_span_id: Optional[str] = None) -> Trace:
        """Inicia um trace distribuído"""
        if trace_id is None:
            trace_id = hashlib.md5(f"{operation}{time.time()}".encode()).hexdigest()

        span_id = hashlib.md5(f"{trace_id}{time.time()}".encode()).hexdigest()[:16]

        trace = Trace(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            operation=operation,
            start_time=time.time()
        )

        self.active_traces[span_id] = trace
        return trace

    def end_trace(self, span_id: str, status: str = "success", tags: Dict[str, Any] = None):
        """Finaliza um trace"""
        if span_id not in self.active_traces:
            return

        trace = self.active_traces[span_id]
        trace.end_time = time.time()
        trace.duration = trace.end_time - trace.start_time
        trace.status = status

        if tags:
            trace.tags.update(tags)

        # Move to completed
        del self.active_traces[span_id]
        self.completed_traces.append(trace)

        # Record duration as metric
        self.record_histogram(
            f"trace.duration.{trace.operation}",
            trace.duration,
            tags={'status': status}
        )

    def log_event(self, level: str, message: str, context: Dict[str, Any] = None):
        """Registra um evento/log"""
        self.record_metric(
            "logs",
            1,
            MetricType.LOG,
            tags={'level': level},
            metadata={'message': message, 'context': context or {}}
        )

    def set_alert_threshold(self, metric_name: str, threshold: float,
                           condition: str = "greater", severity: AlertSeverity = AlertSeverity.WARNING):
        """Define threshold para alerta"""
        self.alert_thresholds[metric_name] = {
            'threshold': threshold,
            'condition': condition,
            'severity': severity
        }

    def add_alert_callback(self, callback: Callable):
        """Adiciona callback para alertas"""
        self.alert_callbacks.append(callback)

    def _check_alerts(self):
        """Verifica condições de alerta"""
        for metric_name, threshold_config in self.alert_thresholds.items():
            if metric_name not in self.metrics:
                continue

            recent_metrics = list(self.metrics[metric_name])[-10:]
            if not recent_metrics:
                continue

            avg_value = sum(m.value for m in recent_metrics) / len(recent_metrics)

            threshold = threshold_config['threshold']
            condition = threshold_config['condition']
            severity = threshold_config['severity']

            triggered = False
            if condition == "greater" and avg_value > threshold:
                triggered = True
            elif condition == "less" and avg_value < threshold:
                triggered = True
            elif condition == "equal" and avg_value == threshold:
                triggered = True

            if triggered:
                alert_id = f"{metric_name}_{int(time.time())}"

                # Check if already alerted recently
                recent_alert = any(
                    a.metric_name == metric_name and not a.resolved
                    for a in self.alerts.values()
                )

                if not recent_alert:
                    alert = Alert(
                        id=alert_id,
                        severity=severity,
                        title=f"Alert: {metric_name}",
                        description=f"{metric_name} {condition} threshold ({avg_value:.2f} vs {threshold})",
                        metric_name=metric_name,
                        threshold=threshold,
                        current_value=avg_value,
                        timestamp=time.time()
                    )

                    self.alerts[alert_id] = alert

                    # Trigger callbacks
                    for callback in self.alert_callbacks:
                        try:
                            callback(alert)
                        except:
                            pass

                    if self.debug:
                        print(f"🚨 ALERT [{severity.value.upper()}]: {alert.description}")

    def _detect_anomalies(self):
        """Detecta anomalias usando estatísticas"""
        for metric_name, metrics_deque in self.metrics.items():
            if len(metrics_deque) < 50:
                continue

            metrics_list = list(metrics_deque)
            values = [m.value for m in metrics_list]

            # Calculate statistics
            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            std_dev = variance ** 0.5

            # Z-score anomaly detection
            recent_value = values[-1]
            if std_dev > 0:
                z_score = (recent_value - mean) / std_dev

                if abs(z_score) > 3:  # 3 standard deviations
                    anomaly = {
                        'metric': metric_name,
                        'value': recent_value,
                        'mean': mean,
                        'std_dev': std_dev,
                        'z_score': z_score,
                        'timestamp': time.time()
                    }
                    self.anomalies.append(anomaly)

                    if self.debug:
                        print(f"🔍 Anomaly detected in {metric_name}: z-score={z_score:.2f}")

    def _calculate_baselines(self):
        """Calcula baselines para métricas"""
        for metric_name, metrics_deque in self.metrics.items():
            if len(metrics_deque) < 100:
                continue

            metrics_list = list(metrics_deque)
            values = [m.value for m in metrics_list]

            # Calculate percentiles
            values_sorted = sorted(values)
            n = len(values_sorted)

            self.baselines[metric_name] = {
                'mean': sum(values) / n,
                'min': values_sorted[0],
                'max': values_sorted[-1],
                'p50': values_sorted[n // 2],
                'p95': values_sorted[int(n * 0.95)],
                'p99': values_sorted[int(n * 0.99)],
                'samples': n
            }

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Retorna sumário das métricas"""
        summary = {
            'total_metrics': sum(len(v) for v in self.metrics.values()),
            'metric_types': list(self.metrics.keys()),
            'active_alerts': len([a for a in self.alerts.values() if not a.resolved]),
            'active_traces': len(self.active_traces),
            'anomalies_detected': len(self.anomalies),
            'slow_operations': len(self.slow_operations)
        }

        # Add system metrics
        if self.system_metrics['cpu']:
            cpu_values = [m.value for m in list(self.system_metrics['cpu'])[-10:]]
            summary['system'] = {
                'cpu_avg': sum(cpu_values) / len(cpu_values) if cpu_values else 0,
                'memory_usage': self.metrics.get('system.memory.usage', [{}])[-1].value if self.metrics.get('system.memory.usage') else 0
            }

        # Add baselines
        summary['baselines'] = self.baselines

        return summary

    def _flush_to_database(self):
        """Salva métricas no banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Flush metrics
            for metric_name, metrics_deque in self.metrics.items():
                for metric in list(metrics_deque):
                    cursor.execute("""
                        INSERT INTO metrics (name, type, value, timestamp, tags, metadata)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        metric.name,
                        metric.type.value,
                        metric.value,
                        metric.timestamp,
                        json.dumps(metric.tags),
                        json.dumps(metric.metadata)
                    ))

            # Flush alerts
            for alert in self.alerts.values():
                cursor.execute("""
                    INSERT OR REPLACE INTO alerts
                    (id, severity, title, description, metric_name, threshold,
                     current_value, timestamp, resolved, resolution_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    alert.id,
                    alert.severity.value,
                    alert.title,
                    alert.description,
                    alert.metric_name,
                    alert.threshold,
                    alert.current_value,
                    alert.timestamp,
                    alert.resolved,
                    alert.resolution_time
                ))

            # Flush traces
            for trace in list(self.completed_traces):
                cursor.execute("""
                    INSERT OR REPLACE INTO traces
                    (trace_id, span_id, parent_span_id, operation, start_time,
                     end_time, duration, tags, logs, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    trace.trace_id,
                    trace.span_id,
                    trace.parent_span_id,
                    trace.operation,
                    trace.start_time,
                    trace.end_time,
                    trace.duration,
                    json.dumps(trace.tags),
                    json.dumps(trace.logs),
                    trace.status
                ))

            conn.commit()

            if self.debug:
                print(f"💾 Flushed {sum(len(v) for v in self.metrics.values())} metrics to database")

        except Exception as e:
            if self.debug:
                print(f"⚠️ Database flush error: {e}")
        finally:
            conn.close()

    def _cleanup_old_data(self):
        """Remove dados antigos"""
        cutoff_time = time.time() - (self.retention_days * 86400)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM metrics WHERE timestamp < ?", (cutoff_time,))
            cursor.execute("DELETE FROM alerts WHERE timestamp < ?", (cutoff_time,))
            cursor.execute("DELETE FROM traces WHERE start_time < ?", (cutoff_time,))

            deleted = cursor.rowcount
            conn.commit()

            if deleted > 0 and self.debug:
                print(f"🗑️ Cleaned up {deleted} old records")

        except Exception as e:
            if self.debug:
                print(f"⚠️ Cleanup error: {e}")
        finally:
            conn.close()

    def export_metrics(self, format: str = "json", filepath: Optional[Path] = None) -> str:
        """Exporta métricas"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'collector': self.name,
            'summary': self.get_metrics_summary(),
            'metrics': {
                name: [asdict(m) for m in list(metrics_deque)[-100:]]
                for name, metrics_deque in self.metrics.items()
            },
            'alerts': [asdict(a) for a in self.alerts.values()],
            'traces': [asdict(t) for t in self.completed_traces]
        }

        if format == "json":
            output = json.dumps(data, indent=2, default=str)
        else:
            output = str(data)

        if filepath:
            with open(filepath, 'w') as f:
                f.write(output)

        return output

    def create_dashboard_data(self) -> Dict[str, Any]:
        """Cria dados para dashboard"""
        return {
            'charts': {
                'cpu_usage': self._prepare_time_series('system.cpu.usage'),
                'memory_usage': self._prepare_time_series('system.memory.usage'),
                'disk_usage': self._prepare_time_series('system.disk.usage'),
                'network_bytes': self._prepare_time_series('system.network.bytes_sent')
            },
            'stats': self.get_metrics_summary(),
            'alerts': [
                {
                    'id': a.id,
                    'severity': a.severity.value,
                    'title': a.title,
                    'timestamp': a.timestamp,
                    'resolved': a.resolved
                }
                for a in sorted(self.alerts.values(), key=lambda x: x.timestamp, reverse=True)[:10]
            ],
            'slow_operations': list(self.slow_operations)[-10:],
            'anomalies': list(self.anomalies)[-10:]
        }

    def _prepare_time_series(self, metric_name: str) -> List[Dict[str, float]]:
        """Prepara dados para gráfico de série temporal"""
        if metric_name not in self.metrics:
            return []

        metrics = list(self.metrics[metric_name])[-100:]
        return [
            {'timestamp': m.timestamp, 'value': m.value}
            for m in metrics
        ]

    def __del__(self):
        """Cleanup ao destruir objeto"""
        self.stop()
        self._flush_to_database()


# Example usage
if __name__ == "__main__":
    print("📡 ADVANCED TELEMETRY SYSTEM")
    print("=" * 60)

    # Initialize telemetry
    telemetry = TelemetryCollector("test_telemetry")

    # Set alert thresholds
    telemetry.set_alert_threshold("system.cpu.usage", 80, "greater", AlertSeverity.WARNING)
    telemetry.set_alert_threshold("system.memory.usage", 90, "greater", AlertSeverity.CRITICAL)

    # Record custom metrics
    telemetry.increment_counter("app.requests", tags={'endpoint': '/api/v1'})
    telemetry.set_gauge("app.active_users", 42)
    telemetry.record_histogram("app.response_time", 0.125, tags={'endpoint': '/api/v1'})

    # Start a trace
    trace = telemetry.start_trace("process_request")
    time.sleep(0.1)
    telemetry.end_trace(trace.span_id, status="success")

    # Log events
    telemetry.log_event("info", "Application started", {'version': '1.0.0'})

    # Get summary
    print("\n📊 Metrics Summary:")
    summary = telemetry.get_metrics_summary()
    for key, value in summary.items():
        if not isinstance(value, dict):
            print(f"   • {key}: {value}")

    # Export metrics
    print("\n💾 Exporting metrics...")
    export_path = Path("/Users/clubproducoes/Digimundo/claude_code/telemetry_export.json")
    telemetry.export_metrics(filepath=export_path)
    print(f"   ✅ Exported to {export_path}")

    # Let it collect for a bit
    print("\n⏳ Collecting metrics for 10 seconds...")
    time.sleep(10)

    # Final summary
    print("\n📊 Final Summary:")
    final_summary = telemetry.get_metrics_summary()
    print(f"   • Total metrics: {final_summary['total_metrics']}")
    print(f"   • Active alerts: {final_summary['active_alerts']}")
    print(f"   • Anomalies detected: {final_summary['anomalies_detected']}")

    print("\n✅ TELEMETRY SYSTEM OPERATIONAL!")
    print("🚀 Think Different. Stay Hungry. Stay Foolish.")