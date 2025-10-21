"""
Bootstrap único do ecossistema Scripturemon
Singleton para inicialização e coordenação de todos os subsistemas
"""

import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional
import threading

logger = logging.getLogger(__name__)

# Singleton flag
_BOOTSTRAP_DONE = False
_BOOTSTRAP_LOCK = threading.Lock()
_BOOTSTRAP_CONTEXT = {}


class NoOpMonitor:
    """No-operation monitor for when monitoring is disabled"""
    def __init__(self):
        self.enabled = False
    
    def start(self):
        pass
    
    def stop(self):
        pass
    
    def record_request(self, *args, **kwargs):
        pass
    
    def record_memory_access(self, *args, **kwargs):
        pass
    
    def record_rag_access(self, *args, **kwargs):
        pass
    
    def update_telepathy_mode(self, *args, **kwargs):
        pass
    
    def get_status(self):
        return {"enabled": False, "running": False}
    
    def get_last_snapshot(self):
        return None
    
    def snapshot(self):
        return {"enabled": False, "note": "monitoring disabled"}


class MinimalRedisMock:
    """Minimal Redis mock for local fallback"""
    def __init__(self):
        self._data = {}
        self._pubsub_data = []
        self.connected = True
        logger.info("MinimalRedisMock initialized")
    
    def ping(self):
        return True
    
    def get(self, key):
        return self._data.get(key)
    
    def set(self, key, value, ex=None):
        self._data[key] = value
        return True
    
    def delete(self, *keys):
        for key in keys:
            self._data.pop(key, None)
        return len(keys)
    
    def exists(self, key):
        return key in self._data
    
    def publish(self, channel, message):
        self._pubsub_data.append({"channel": channel, "message": message})
        return 1
    
    def pubsub(self):
        return self
    
    def subscribe(self, *channels):
        pass
    
    def get_message(self, timeout=None):
        if self._pubsub_data:
            return self._pubsub_data.pop(0)
        return None


def load_settings() -> Dict[str, Any]:
    """Load settings from config files with safe defaults"""
    settings = {
        # Safe defaults
        "memory": {"enabled": True},
        "telepathy": {"enabled": True, "redis_url": "redis://localhost:6379", "timeout": 2.0},
        "monitoring": {"enabled": False, "interval_ms": 5000},
        "soulos": {"enabled": False, "auto_execute": False},
        "backup": {"enabled": True, "interval": 300},
        "personas": {"default": "brutal"},
        "mode": "normal"  # normal or deep
    }
    
    # Try to load from settings.yaml
    try:
        settings_path = Path(__file__).parent.parent.parent / "config" / "settings.yaml"
        if settings_path.exists():
            import yaml
            with open(settings_path) as f:
                loaded = yaml.safe_load(f) or {}
                # Merge with defaults (loaded overrides defaults)
                for key, value in loaded.items():
                    if isinstance(value, dict) and key in settings:
                        settings[key].update(value)
                    else:
                        settings[key] = value
            logger.info(f"Settings loaded from {settings_path}")
    except Exception as e:
        logger.warning(f"Could not load settings.yaml: {e}, using defaults")
    
    return settings


def ensure_bootstrap_once(settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Singleton bootstrap function - initializes all subsystems once
    
    Returns:
        Bootstrap context with subsystem states
    """
    global _BOOTSTRAP_DONE, _BOOTSTRAP_CONTEXT
    
    with _BOOTSTRAP_LOCK:
        if _BOOTSTRAP_DONE:
            logger.debug("Bootstrap already done, returning cached context")
            return _BOOTSTRAP_CONTEXT
        
        logger.info("Starting Scripturemon bootstrap...")
        
        # Load settings
        if settings is None:
            settings = load_settings()
        
        context = {
            "telepathy_mode": "offline",
            "monitor_enabled": False,
            "soulos": {"enabled": False, "auto_execute": False},
            "memory_ok": False,
            "backup_enabled": False,
            "settings": settings
        }
        
        # 1. Memory Manager - Use canonical import
        try:
            from apps.scripturemon.canonical.memory_manager import get_memory_manager
            memory_manager = get_memory_manager()
            
            # Check if it's functional (not NoOp)
            if hasattr(memory_manager, 'functional') and not memory_manager.functional:
                context["memory_ok"] = False
                context["memory_canonical"] = "NoOpMemoryManager"
                logger.warning("Memory manager is NoOp (no working implementation found)")
            else:
                context["memory_ok"] = True
                context["memory_canonical"] = memory_manager.__class__.__module__ + "." + memory_manager.__class__.__name__
                logger.info(f"✅ Memory manager initialized: {context['memory_canonical']}")
            
            context["memory_manager"] = memory_manager
            
        except Exception as e:
            logger.error(f"Memory initialization failed: {e}")
            context["memory_ok"] = False
            context["memory_canonical"] = "ERROR"
        
        # 2. Telepathy Adaptive
        try:
            telepathy_mode = "offline"
            telepathy_client = None
            
            if settings.get("telepathy", {}).get("enabled", True):
                redis_url = settings.get("telepathy", {}).get("redis_url", "redis://localhost:6379")
                timeout = settings.get("telepathy", {}).get("timeout", 2.0)
                
                # Try Redis
                try:
                    import redis
                    client = redis.from_url(redis_url, socket_connect_timeout=timeout)
                    client.ping()
                    telepathy_client = client
                    telepathy_mode = "redis"
                    logger.info(f"✅ Redis connected: {redis_url}")
                except Exception as e:
                    logger.debug(f"Redis failed: {e}, trying fakeredis")
                    
                    # Try FakeRedis
                    if telepathy_mode == "offline":
                        try:
                            import fakeredis
                            telepathy_client = fakeredis.FakeRedis()
                            telepathy_mode = "fakeredis"
                            logger.info("✅ FakeRedis initialized")
                        except ImportError:
                            logger.debug("FakeRedis not available, using mock")
                    
                    # Fallback to mock
                    if telepathy_mode == "offline":
                        telepathy_client = MinimalRedisMock()
                        telepathy_mode = "mock"
                        logger.info("✅ MinimalRedisMock initialized")
            
            context["telepathy_mode"] = telepathy_mode
            context["telepathy_client"] = telepathy_client
            
        except Exception as e:
            logger.error(f"Telepathy initialization failed: {e}")
            context["telepathy_mode"] = "error"
        
        # 3. Backup Immortal
        try:
            if settings.get("backup", {}).get("enabled", True):
                # Check if immortality module exists
                try:
                    from apps.scripturemon.immortality import start_background
                    start_background()
                    context["backup_enabled"] = True
                    logger.info("✅ Immortality backup started")
                except ImportError:
                    logger.debug("Immortality module not found, backup disabled")
                    context["backup_enabled"] = False
        except Exception as e:
            logger.error(f"Backup initialization failed: {e}")
            context["backup_enabled"] = False
        
        # 4. Monitor
        try:
            monitor = None
            if settings.get("monitoring", {}).get("enabled", False):
                from apps.scripturemon.monitoring_system import get_monitor
                monitor = get_monitor(settings.get("monitoring", {}))
                monitor.start()
                context["monitor_enabled"] = True
                logger.info("✅ Monitoring system started")
            else:
                monitor = NoOpMonitor()
                context["monitor_enabled"] = False
                logger.info("ℹ️ Monitoring disabled (opt-in)")
            
            context["monitor"] = monitor
            
        except Exception as e:
            logger.error(f"Monitor initialization failed: {e}")
            context["monitor"] = NoOpMonitor()
            context["monitor_enabled"] = False
        
        # 5. SoulOS - ALWAYS OFF by default
        try:
            soulos_config = settings.get("soulos", {})
            # Force OFF by default for safety
            soulos_config["enabled"] = soulos_config.get("enabled", False)
            soulos_config["auto_execute"] = soulos_config.get("auto_execute", False)
            
            context["soulos"] = soulos_config
            
            if soulos_config["enabled"]:
                logger.warning("⚠️ SoulOS is ENABLED - use with caution")
            else:
                logger.info("✅ SoulOS is safely DISABLED")
                
        except Exception as e:
            logger.error(f"SoulOS configuration failed: {e}")
            context["soulos"] = {"enabled": False, "auto_execute": False}
        
        # Mark as done and cache
        _BOOTSTRAP_DONE = True
        _BOOTSTRAP_CONTEXT = context
        
        logger.info("Bootstrap complete!")
        logger.info(f"Context: telepathy={context['telepathy_mode']}, monitor={context['monitor_enabled']}, "
                   f"memory={context['memory_ok']}, backup={context['backup_enabled']}, "
                   f"soulos={context['soulos']['enabled']}")
        
        return context


def status_report() -> Dict[str, Any]:
    """
    Generate standardized status report
    
    Returns:
        Status dictionary with all subsystem states
    """
    # Ensure bootstrap
    context = ensure_bootstrap_once()
    
    # Get current persona
    persona = "brutal"  # default
    try:
        from src.personas.manager import get_personas_manager
        manager = get_personas_manager()
        persona = manager.current_persona_name
    except:
        pass
    
    # Get mode (normal/deep)
    mode = context.get("settings", {}).get("mode", "normal")
    
    # Get telepathy details
    telepathy = {
        "mode": context.get("telepathy_mode", "offline"),
        "url": context.get("settings", {}).get("telepathy", {}).get("redis_url", "N/A")
    }
    
    # Get monitor snapshot
    monitor_data = {"enabled": False, "cpu": None, "mem_mb": None}
    if context.get("monitor_enabled") and context.get("monitor"):
        try:
            snapshot = context["monitor"].get_last_snapshot()
            if snapshot and "system" in snapshot:
                monitor_data["enabled"] = True
                monitor_data["cpu"] = snapshot["system"].get("cpu_percent")
                monitor_data["mem_mb"] = snapshot["system"].get("memory_mb")
        except:
            pass
    
    # Memory status
    memory = {
        "ok": context.get("memory_ok", False),
        "canonical": context.get("memory_canonical", "Unknown"),
        "probe": "pass" if context.get("memory_ok", False) else "fail"
    }
    
    status = {
        "persona": persona,
        "mode": mode,
        "telepathy": telepathy,
        "soulos": context.get("soulos", {"enabled": False, "auto_execute": False}),
        "monitor": monitor_data,
        "memory": memory,
        "backup": {"enabled": context.get("backup_enabled", False)}
    }
    
    return status


def format_status_text(status: Optional[Dict[str, Any]] = None) -> str:
    """
    Format status report as human-readable text
    
    Args:
        status: Status dict or None (will generate if None)
        
    Returns:
        Formatted status text
    """
    if status is None:
        status = status_report()
    
    lines = [
        "=" * 60,
        "📊 SCRIPTUREMON STATUS",
        "=" * 60,
        "",
        f"🎭 Persona: {status['persona']}",
        f"⚙️ Mode: {status['mode']}",
        "",
        f"📡 Telepathy: {status['telepathy']['mode'].upper()}",
        f"   URL: {status['telepathy']['url']}",
        "",
        f"🤖 SoulOS: {'ENABLED' if status['soulos']['enabled'] else 'DISABLED'}",
        f"   Auto-execute: {'YES' if status['soulos']['auto_execute'] else 'NO'}",
        "",
        f"📊 Monitor: {'ENABLED' if status['monitor']['enabled'] else 'DISABLED'}",
    ]
    
    if status['monitor']['enabled'] and status['monitor']['cpu'] is not None:
        lines.append(f"   CPU: {status['monitor']['cpu']}%")
        lines.append(f"   Memory: {status['monitor']['mem_mb']} MB")
    
    lines.extend([
        "",
        f"🧠 Memory Manager: {'OK' if status['memory']['ok'] else 'ERROR'}",
        f"💾 Backup: {'ENABLED' if status['backup']['enabled'] else 'DISABLED'}",
        "",
        "=" * 60
    ])
    
    return "\n".join(lines)


# Export key functions
__all__ = [
    'ensure_bootstrap_once',
    'status_report', 
    'format_status_text',
    'NoOpMonitor',
    'MinimalRedisMock'
]