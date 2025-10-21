"""
MONITORING SYSTEM - FASE 7
Opt-in monitoring with metrics collection and health snapshots
"""

import json
import time
import threading
import os
import base64
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from collections import deque
import psutil
import logging

logger = logging.getLogger(__name__)

# --- FixPack:S1 begin (monitoring) ---
def _json_default(o):
    """JSON serializer for non-serializable objects"""
    if isinstance(o, (set, tuple)):
        return list(o)
    if isinstance(o, bytes):
        return base64.b64encode(o).decode("ascii")
    if isinstance(o, Path):
        return str(o)
    if isinstance(o, (datetime, datetime.date)):
        return o.isoformat()
    try:
        return str(o)
    except Exception:
        return "<non-serializable>"

def safe_json_dump(obj, path: Path) -> bool:
    """Safely dump JSON to file with error handling"""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, default=_json_default, indent=2)
        return True
    except Exception as e:
        logger.error(f"JSON dump failed: {e}")
        return False

def safe_export_snapshot(self, data: dict, outdir: Path) -> bool:
    """Export snapshot with throttling and error handling"""
    now = time.time()
    # Throttle exports to ≥30s intervals
    if hasattr(self, "_last_export_ts") and self._last_export_ts and now - self._last_export_ts < 30:
        logger.debug(f"Throttled export (last was {now - self._last_export_ts:.1f}s ago)")
        return False
    
    self._last_export_ts = now
    outdir.mkdir(parents=True, exist_ok=True)
    
    # Ensure data structure
    payload = dict(data or {})
    if "snapshots" not in payload:
        payload["snapshots"] = []
    
    # Try JSON first
    json_path = outdir / f"snapshot_{int(now)}.json"
    if not safe_json_dump(payload, json_path):
        # Fallback to NDJSON
        ndjson_path = outdir / f"snapshot_{int(now)}.ndjson"
        try:
            with ndjson_path.open("w", encoding="utf-8") as f:
                snaps = payload.get("snapshots")
                if isinstance(snaps, list) and snaps:
                    for item in snaps:
                        f.write(json.dumps(item, ensure_ascii=False, default=_json_default) + "\n")
                else:
                    f.write(json.dumps(payload, ensure_ascii=False, default=_json_default) + "\n")
            logger.debug(f"Exported snapshot to NDJSON: {ndjson_path}")
            return True
        except Exception as e:
            logger.error(f"NDJSON export also failed: {e}")
            return False
    
    logger.debug(f"Exported snapshot to JSON: {json_path}")
    return True
# --- FixPack:S1 end (monitoring) ---


class MonitoringSystem:
    """System monitoring with opt-in metrics collection - FASE 7"""
    
    def __init__(self, settings: Dict[str, Any] = None):
        """Initialize monitoring system
        
        Args:
            settings: Monitoring configuration from settings.yaml
        """
        self.settings = settings or {}
        self.enabled = self.settings.get('enabled', False)
        self.interval_ms = max(2000, self.settings.get('interval_ms', 5000))
        self.export_path = Path(self.settings.get('export_path', 
                                                  'reports/harmony_v100/runtime/health.json'))
        self.max_snapshots = self.settings.get('max_snapshots', 100)
        
        # Metrics storage
        self.request_count = 0
        self.latencies = deque(maxlen=1000)  # Last 1000 request latencies
        self.memory_hits = 0
        self.memory_misses = 0
        self.rag_hits = 0
        self.rag_misses = 0
        self.telepathy_mode = "unknown"
        self.error_count = 0
        
        # Snapshot history
        self.snapshots = deque(maxlen=self.max_snapshots)
        self.last_snapshot = None
        
        # Monitoring thread
        self.monitor_thread = None
        self.stop_event = threading.Event()
        
        # Start time
        self.start_time = time.time()
        
        # Create export directory
        if self.enabled:
            self.export_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Monitoring system initialized (enabled={self.enabled}, interval={self.interval_ms}ms)")
    
    def start(self):
        """Start monitoring thread if enabled (idempotent)"""
        if not self.enabled:
            logger.debug("Monitoring disabled, not starting thread")
            return
        
        # ============ PHASE 3 FIX - IDEMPOTENT START ============
        # Check if thread is already running (idempotent)
        if self.monitor_thread and self.monitor_thread.is_alive():
            logger.debug("Monitoring thread already running - idempotent, not starting again")
            return
        # ============ END PHASE 3 FIX ============
        
        self.stop_event.clear()
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Monitoring thread started")
    
    def stop(self):
        """Stop monitoring thread"""
        if not self.monitor_thread:
            return
        
        logger.info("Stopping monitoring thread...")
        self.stop_event.set()
        self.monitor_thread.join(timeout=5)
        
        if self.monitor_thread.is_alive():
            logger.warning("Monitoring thread did not stop gracefully")
        else:
            logger.info("Monitoring thread stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop - runs in separate thread"""
        while not self.stop_event.is_set():
            try:
                # Collect snapshot
                snapshot = self._collect_snapshot()
                
                # Store in history
                self.snapshots.append(snapshot)
                self.last_snapshot = snapshot
                
                # Export to file
                self._export_snapshot(snapshot)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
            
            # Sleep for interval
            time.sleep(self.interval_ms / 1000.0)
    
    def _collect_snapshot(self) -> Dict[str, Any]:
        """Collect current metrics snapshot"""
        # ============ PHASE 3 FIX - ENSURE SERIALIZABLE SNAPSHOT ============
        try:
            now = datetime.now()
            uptime = time.time() - self.start_time
            
            # Calculate latency statistics
            latency_stats = self._calculate_latency_stats()
            
            # Get memory usage
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            
            # Calculate rates
            mem_hit_rate = (self.memory_hits / (self.memory_hits + self.memory_misses) * 100 
                           if (self.memory_hits + self.memory_misses) > 0 else 0)
            rag_hit_rate = (self.rag_hits / (self.rag_hits + self.rag_misses) * 100
                           if (self.rag_hits + self.rag_misses) > 0 else 0)
            
            # Build snapshot with explicit type conversions for JSON serialization
            snapshot = {
                "timestamp": now.isoformat(),
                "uptime_seconds": float(round(uptime, 2)),
                "metrics": {
                    "request_count": int(self.request_count),
                    "error_count": int(self.error_count),
                    "avg_latency_ms": float(latency_stats["avg"]),
                    "p95_latency_ms": float(latency_stats["p95"]),
                    "p99_latency_ms": float(latency_stats["p99"]),
                    "memory_hits": int(self.memory_hits),
                    "memory_hit_rate": float(round(mem_hit_rate, 2)),
                    "rag_hits": int(self.rag_hits),
                    "rag_hit_rate": float(round(rag_hit_rate, 2)),
                    "telepathy_mode": str(self.telepathy_mode)
                },
                "system": {
                    "memory_mb": float(round(memory_info.rss / 1024 / 1024, 2)),
                    "cpu_percent": float(process.cpu_percent()),
                    "threads": int(process.num_threads())
                }
            }
            
        except Exception as e:
            # Return minimal valid snapshot on error
            logger.warning(f"Error collecting snapshot: {e}")
            snapshot = {
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": 0.0,
                "metrics": {
                    "request_count": 0,
                    "error_count": 0,
                    "avg_latency_ms": 0.0,
                    "p95_latency_ms": 0.0,
                    "p99_latency_ms": 0.0,
                    "memory_hits": 0,
                    "memory_hit_rate": 0.0,
                    "rag_hits": 0,
                    "rag_hit_rate": 0.0,
                    "telepathy_mode": "unknown"
                },
                "system": {
                    "memory_mb": 0.0,
                    "cpu_percent": 0.0,
                    "threads": 0
                }
            }
        
        return snapshot
        # ============ END PHASE 3 FIX ============
    
    def _calculate_latency_stats(self) -> Dict[str, float]:
        """Calculate latency statistics"""
        if not self.latencies:
            return {"avg": 0, "p95": 0, "p99": 0}
        
        sorted_latencies = sorted(self.latencies)
        n = len(sorted_latencies)
        
        avg = sum(sorted_latencies) / n
        p95_idx = int(n * 0.95)
        p99_idx = int(n * 0.99)
        
        return {
            "avg": round(avg, 2),
            "p95": round(sorted_latencies[min(p95_idx, n-1)], 2),
            "p99": round(sorted_latencies[min(p99_idx, n-1)], 2)
        }
    
    def _export_snapshot(self, snapshot: Dict[str, Any]):
        """Export snapshot to JSON file with robust error handling"""
        # ============ PHASE 3 FIX - ROBUST EXPORT WITH LOCK ============
        import threading
        
        # Create lock if not exists
        if not hasattr(self, '_export_lock'):
            self._export_lock = threading.Lock()
        
        # Use lock to prevent concurrent writes
        with self._export_lock:
            try:
                # Throttle exports
                now = time.time()
                if hasattr(self, "_last_export_ts") and self._last_export_ts:
                    if now - self._last_export_ts < 30:  # Minimum 30s between exports
                        return
                self._last_export_ts = now
                
                # Ensure export directory exists
                self.export_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Read existing snapshots with error recovery
                data = {"snapshots": []}
                if self.export_path.exists():
                    try:
                        with open(self.export_path, 'r') as f:
                            content = f.read()
                            if content.strip():  # Only parse if not empty
                                data = json.loads(content)
                                # Ensure snapshots key exists
                                if not isinstance(data, dict):
                                    data = {"snapshots": []}
                                if "snapshots" not in data:
                                    data["snapshots"] = []
                    except (json.JSONDecodeError, ValueError) as e:
                        logger.warning(f"Invalid JSON in {self.export_path}, creating new: {e}")
                        data = {"snapshots": []}
                
                # Add new snapshot (keep last 100)
                if isinstance(data.get("snapshots"), list):
                    data["snapshots"].append(snapshot)
                    data["snapshots"] = data["snapshots"][-100:]
                else:
                    data["snapshots"] = [snapshot]
                
                # Add metadata
                data["metadata"] = {
                    "last_updated": snapshot.get("timestamp", datetime.now().isoformat()),
                    "monitoring_enabled": self.enabled,
                    "interval_ms": self.interval_ms,
                    "total_snapshots": len(data["snapshots"])
                }
                
                # Write back with safe serialization using default=str
                self.export_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.export_path, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
                    
            except Exception as e:
                # Try alternative export to snapshots directory
                try:
                    alt_path = Path("reports/monitoring/snapshots") / f"snapshot_{int(time.time())}.json"
                    alt_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(alt_path, 'w') as f:
                        json.dump({"snapshot": snapshot}, f, indent=2, default=str)
                    logger.warning(f"Exported to alternative path: {alt_path}")
                except Exception as e2:
                    logger.error(f"Failed to export snapshot: {e}, alt failed: {e2}")
        # ============ END PHASE 3 FIX ============
    
    def record_request(self, latency_ms: float, success: bool = True):
        """Record a request with its latency
        
        Args:
            latency_ms: Request latency in milliseconds
            success: Whether request succeeded
        """
        if not self.enabled:
            return
        
        self.request_count += 1
        self.latencies.append(latency_ms)
        
        if not success:
            self.error_count += 1
    
    def record_memory_access(self, hit: bool):
        """Record memory access hit/miss
        
        Args:
            hit: Whether it was a cache hit
        """
        if not self.enabled:
            return
        
        if hit:
            self.memory_hits += 1
        else:
            self.memory_misses += 1
    
    def record_rag_access(self, hit: bool):
        """Record RAG access hit/miss
        
        Args:
            hit: Whether documents were found
        """
        if not self.enabled:
            return
        
        if hit:
            self.rag_hits += 1
        else:
            self.rag_misses += 1
    
    def update_telepathy_mode(self, mode: str):
        """Update current telepathy mode
        
        Args:
            mode: Current mode (redis/offline/fallback)
        """
        if not self.enabled:
            return
        
        self.telepathy_mode = mode
    
    def get_last_snapshot(self) -> Optional[Dict[str, Any]]:
        """Get the most recent snapshot
        
        Returns:
            Last snapshot or None
        """
        return self.last_snapshot
    
    def get_status(self) -> Dict[str, Any]:
        """Get monitoring system status
        
        Returns:
            Current monitoring status
        """
        return {
            "enabled": self.enabled,
            "interval_ms": self.interval_ms,
            "running": self.monitor_thread.is_alive() if self.monitor_thread else False,
            "snapshots_collected": len(self.snapshots),
            "export_path": str(self.export_path),
            "last_snapshot": self.last_snapshot["timestamp"] if self.last_snapshot else None
        }
    
    def get_summary(self) -> str:
        """Get formatted summary for /status command
        
        Returns:
            Formatted monitoring summary
        """
        if not self.last_snapshot:
            return "No monitoring data available"
        
        snap = self.last_snapshot
        metrics = snap["metrics"]
        system = snap["system"]
        
        return f"""📊 **MONITORING SNAPSHOT**
        
Last Update: {snap['timestamp']}
Uptime: {snap['uptime_seconds']:.1f}s

**Performance:**
• Requests: {metrics['request_count']}
• Avg Latency: {metrics['avg_latency_ms']}ms
• P95 Latency: {metrics['p95_latency_ms']}ms
• Errors: {metrics['error_count']}

**Cache Performance:**
• Memory Hits: {metrics['memory_hits']} ({metrics['memory_hit_rate']}%)
• RAG Hits: {metrics['rag_hits']} ({metrics['rag_hit_rate']}%)

**System:**
• Memory: {system['memory_mb']}MB
• CPU: {system['cpu_percent']}%
• Threads: {system['threads']}
• Telepathy: {metrics['telepathy_mode']}"""


# Global monitoring instance
_monitoring_instance = None


def get_monitoring() -> MonitoringSystem:
    """Get global monitoring instance
    
    Returns:
        Global MonitoringSystem instance
    """
    global _monitoring_instance
    if _monitoring_instance is None:
        _monitoring_instance = MonitoringSystem()
    return _monitoring_instance


def init_monitoring(settings: Dict[str, Any]):
    """Initialize global monitoring with settings
    
    Args:
        settings: Monitoring configuration
    """
    global _monitoring_instance
    _monitoring_instance = MonitoringSystem(settings)
    if _monitoring_instance.enabled:
        _monitoring_instance.start()
    return _monitoring_instance


def get_monitor(settings: Optional[Dict[str, Any]] = None) -> MonitoringSystem:
    """Compatibility shim for get_monitor -> get_monitoring
    
    This function provides backward compatibility for code expecting get_monitor.
    It's an alias that calls get_monitoring() or init_monitoring() as needed.
    
    Args:
        settings: Optional monitoring configuration
        
    Returns:
        Global MonitoringSystem instance
    """
    if settings is not None:
        # If settings provided, initialize with them
        return init_monitoring(settings)
    else:
        # Otherwise get existing instance
        return get_monitoring()