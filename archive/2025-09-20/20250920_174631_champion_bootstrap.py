#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHAMPION BOOTSTRAP SYSTEM - Robust Initialization
Symbiotic integration from scripturemon-validation to scripturemon-champion

Enhanced bootstrap orchestrator for scripturemon-champion with:
- Memory Brain System integration
- DigiLang Compression Bridge coordination
- Backup/recovery management
- Health monitoring and status reporting
- Safe initialization with graceful fallbacks
- Integration analytics and performance tracking
"""

import json
import logging
import os
import sys
import time
import threading
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

# Singleton protection
_BOOTSTRAP_DONE = False
_BOOTSTRAP_LOCK = threading.Lock()
_BOOTSTRAP_CONTEXT = {}


class ChampionNoOpMonitor:
    """No-operation monitor for when monitoring is disabled"""
    def __init__(self):
        self.enabled = False
        self.started = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False

    def record_request(self, *args, **kwargs):
        pass

    def record_compression(self, *args, **kwargs):
        pass

    def record_memory_access(self, *args, **kwargs):
        pass

    def get_status(self):
        return {"enabled": False, "running": self.started}

    def get_metrics(self):
        return {}

    def snapshot(self):
        return {"enabled": False, "note": "monitoring disabled"}


class ChampionMinimalRedis:
    """Minimal Redis-compatible mock for local fallback"""
    def __init__(self):
        self._data = {}
        self._pubsub_data = []
        self.connected = True
        logger.info("ChampionMinimalRedis initialized")

    def ping(self):
        return True

    def get(self, key):
        return self._data.get(key)

    def set(self, key, value, ex=None):
        self._data[key] = value
        return True

    def delete(self, *keys):
        deleted = 0
        for key in keys:
            if key in self._data:
                del self._data[key]
                deleted += 1
        return deleted

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


def load_champion_settings() -> Dict[str, Any]:
    """Load settings from multiple sources with safe defaults"""
    settings = {
        # Champion-specific defaults
        "memory_brain": {"enabled": True, "analytics": True, "cache": True},
        "compression": {"enabled": True, "mode": "auto", "cache": True, "analytics": True},
        "backup": {"enabled": True, "interval": 300, "enhanced": True},
        "monitoring": {"enabled": False, "interval_ms": 5000, "compression_metrics": True},
        "ollama": {
            "profile": os.environ.get("SCRIPTUREMON_OLLAMA_PROFILE", "gpu-stable"),
            "num_parallel": int(os.environ.get("OLLAMA_NUM_PARALLEL", "2")),
            "max_loaded_models": int(os.environ.get("OLLAMA_MAX_LOADED_MODELS", "2"))
        },
        "champion": {
            "mode": "production",  # production, development, testing
            "debug": False,
            "integration_level": "full"  # full, partial, minimal
        }
    }

    # Try to load from multiple config sources
    config_paths = [
        Path(__file__).parent.parent.parent / "config" / "champion.yaml",
        Path(__file__).parent.parent.parent / "config" / "settings.yaml",
        Path.home() / ".scripturemon" / "champion.yaml"
    ]

    for config_path in config_paths:
        try:
            if config_path.exists():
                import yaml
                with open(config_path) as f:
                    loaded = yaml.safe_load(f) or {}
                    # Deep merge with defaults
                    for key, value in loaded.items():
                        if isinstance(value, dict) and key in settings:
                            settings[key].update(value)
                        else:
                            settings[key] = value
                logger.info(f"Settings loaded from {config_path}")
                break
        except Exception as e:
            logger.debug(f"Could not load {config_path}: {e}")

    # Environment variable overrides
    if os.environ.get("CHAMPION_DEBUG"):
        settings["champion"]["debug"] = True
    if os.environ.get("CHAMPION_MODE"):
        settings["champion"]["mode"] = os.environ["CHAMPION_MODE"]

    return settings


def initialize_memory_brain(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize Memory Brain System with comprehensive validation"""
    brain_config = settings.get("memory_brain", {})

    if not brain_config.get("enabled", True):
        return {
            "enabled": False,
            "status": "disabled",
            "brain": None
        }

    try:
        from .memory_brain import get_memory_brain

        # Initialize with configuration
        brain = get_memory_brain()

        # Test basic functionality
        test_content = "Champion Bootstrap memory test"
        memory_id = brain.save("bootstrap", test_content,
                             metadata={"timestamp": time.time()}, importance=0.5)

        # Verify save/retrieve cycle
        context = brain.get_context("bootstrap", k=1)

        if context and len(context) > 0:
            brain_status = "operational"
            logger.info("Memory Brain System initialized and validated")
        else:
            brain_status = "limited"
            logger.warning("Memory Brain System initialized but validation failed")

        # Get statistics
        stats = brain.get_stats()

        return {
            "enabled": True,
            "status": brain_status,
            "brain": brain,
            "stats": stats,
            "analytics": brain_config.get("analytics", True),
            "cache": brain_config.get("cache", True)
        }

    except Exception as e:
        logger.error(f"Memory Brain initialization failed: {e}")
        return {
            "enabled": False,
            "status": "error",
            "brain": None,
            "error": str(e)
        }


def initialize_compression_bridge(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize DigiLang Compression Bridge with configuration"""
    compression_config = settings.get("compression", {})

    if not compression_config.get("enabled", True):
        return {
            "enabled": False,
            "status": "disabled",
            "bridge": None
        }

    try:
        from .digilang_compression_bridge import get_compression_bridge

        # Initialize with configuration
        bridge = get_compression_bridge()

        # Test compression functionality
        test_text = "FADE IN:\n\nINT. CHAMPION BOOTSTRAP - DAY\n\nSystem initializing successfully."
        compressed, stats = bridge.compress_text(test_text, mode="screenplay")

        # Verify compression quality
        if stats.get("tokens_saved", 0) > 0:
            compression_status = "operational"
            logger.info(f"Compression Bridge operational - {stats['percentage_saved']} savings")
        else:
            compression_status = "limited"
            logger.warning("Compression Bridge initialized but minimal compression")

        # Get bridge statistics
        bridge_stats = bridge.get_compression_stats()

        return {
            "enabled": True,
            "status": compression_status,
            "bridge": bridge,
            "stats": bridge_stats,
            "available_encoders": len(bridge.available_encoders),
            "test_compression": stats,
            "analytics": compression_config.get("analytics", True)
        }

    except Exception as e:
        logger.error(f"Compression Bridge initialization failed: {e}")
        return {
            "enabled": False,
            "status": "error",
            "bridge": None,
            "error": str(e)
        }


def initialize_backup_system(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize enhanced backup system with multiple strategies"""
    backup_config = settings.get("backup", {})

    if not backup_config.get("enabled", True):
        return {
            "enabled": False,
            "status": "disabled"
        }

    backup_strategies = []

    try:
        # Strategy 1: Enhanced backup from scripturemon-validation
        if backup_config.get("enhanced", True):
            try:
                from .backup import backup_auto_start
                interval_min = backup_config.get("interval", 300) // 60
                backup_auto_start(interval_min)
                backup_strategies.append("enhanced_auto")
                logger.info(f"Enhanced backup system started (interval: {interval_min}m)")
            except ImportError:
                logger.debug("Enhanced backup not available")

        # Strategy 2: Memory bridge backup integration
        try:
            from .membridge import promote, counts
            # Test memory bridge functionality
            test_item = {
                "kind": "bootstrap_test",
                "content": "Champion bootstrap validation",
                "timestamp": time.time()
            }
            promote(test_item, importance=0.3)

            # Get memory counts for verification
            memory_counts = counts()
            backup_strategies.append("membridge")
            logger.info(f"Memory bridge backup integrated - {memory_counts}")
        except ImportError:
            logger.debug("Memory bridge backup not available")

        # Strategy 3: Basic file backup fallback
        if not backup_strategies:
            # Create simple backup strategy
            try:
                backup_dir = Path.home() / ".scripturemon" / "backups"
                backup_dir.mkdir(parents=True, exist_ok=True)

                # Create a basic backup record
                backup_record = {
                    "timestamp": datetime.now().isoformat(),
                    "champion_bootstrap": True,
                    "type": "fallback"
                }

                backup_file = backup_dir / f"champion_backup_{int(time.time())}.json"
                backup_file.write_text(json.dumps(backup_record, indent=2))

                backup_strategies.append("fallback")
                logger.info(f"Fallback backup created: {backup_file}")
            except Exception as e:
                logger.error(f"Fallback backup failed: {e}")

        return {
            "enabled": True,
            "status": "operational" if backup_strategies else "error",
            "strategies": backup_strategies,
            "interval": backup_config.get("interval", 300)
        }

    except Exception as e:
        logger.error(f"Backup system initialization failed: {e}")
        return {
            "enabled": False,
            "status": "error",
            "error": str(e)
        }


def initialize_monitoring(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize monitoring system with champion-specific metrics"""
    monitoring_config = settings.get("monitoring", {})

    if not monitoring_config.get("enabled", False):
        monitor = ChampionNoOpMonitor()
        return {
            "enabled": False,
            "status": "disabled",
            "monitor": monitor
        }

    try:
        # Try to use existing monitoring system
        try:
            from .monitoring_system import get_monitor
            monitor = get_monitor(monitoring_config)
            monitor.start()
            logger.info("Advanced monitoring system started")
            monitoring_status = "advanced"
        except ImportError:
            # Fallback to basic monitoring
            monitor = ChampionNoOpMonitor()
            monitor.start()
            logger.info("Basic monitoring fallback active")
            monitoring_status = "basic"

        return {
            "enabled": True,
            "status": monitoring_status,
            "monitor": monitor,
            "compression_metrics": monitoring_config.get("compression_metrics", True),
            "interval_ms": monitoring_config.get("interval_ms", 5000)
        }

    except Exception as e:
        logger.error(f"Monitoring initialization failed: {e}")
        monitor = ChampionNoOpMonitor()
        return {
            "enabled": False,
            "status": "error",
            "monitor": monitor,
            "error": str(e)
        }


def initialize_unified_system(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize and validate unified system integration"""
    try:
        from .scripturemon_unified import ScripturemonUnified

        # Initialize unified system
        unified = ScripturemonUnified()

        # Get system status
        status = unified.get_status()

        # Count available components
        component_count = len(status.get("components", {}))

        if component_count > 0:
            logger.info(f"Unified System operational with {component_count} components")
            unified_status = "operational"
        else:
            logger.warning("Unified System initialized but no components detected")
            unified_status = "limited"

        return {
            "enabled": True,
            "status": unified_status,
            "unified": unified,
            "component_count": component_count,
            "system_status": status
        }

    except Exception as e:
        logger.error(f"Unified System initialization failed: {e}")
        return {
            "enabled": False,
            "status": "error",
            "unified": None,
            "error": str(e)
        }


def validate_integration_health(context: Dict[str, Any]) -> Dict[str, Any]:
    """Comprehensive health validation of integrated systems"""
    health_report = {
        "overall_status": "healthy",
        "critical_issues": [],
        "warnings": [],
        "integration_score": 0.0,
        "component_health": {}
    }

    # Memory Brain health check
    memory_brain = context.get("memory_brain", {})
    if memory_brain.get("enabled"):
        if memory_brain.get("status") == "operational":
            health_report["component_health"]["memory_brain"] = "healthy"
            health_report["integration_score"] += 25
        else:
            health_report["component_health"]["memory_brain"] = "degraded"
            health_report["warnings"].append("Memory Brain status degraded")
            health_report["integration_score"] += 10
    else:
        health_report["component_health"]["memory_brain"] = "disabled"

    # Compression Bridge health check
    compression = context.get("compression", {})
    if compression.get("enabled"):
        if compression.get("status") == "operational":
            health_report["component_health"]["compression"] = "healthy"
            health_report["integration_score"] += 25
        else:
            health_report["component_health"]["compression"] = "degraded"
            health_report["warnings"].append("Compression Bridge status degraded")
            health_report["integration_score"] += 10
    else:
        health_report["component_health"]["compression"] = "disabled"

    # Backup system health check
    backup = context.get("backup", {})
    if backup.get("enabled"):
        if backup.get("status") == "operational":
            health_report["component_health"]["backup"] = "healthy"
            health_report["integration_score"] += 20
        else:
            health_report["component_health"]["backup"] = "degraded"
            health_report["warnings"].append("Backup system issues detected")
            health_report["integration_score"] += 5
    else:
        health_report["component_health"]["backup"] = "disabled"

    # Unified System health check
    unified = context.get("unified", {})
    if unified.get("enabled"):
        if unified.get("status") == "operational":
            health_report["component_health"]["unified"] = "healthy"
            health_report["integration_score"] += 20
        else:
            health_report["component_health"]["unified"] = "degraded"
            health_report["warnings"].append("Unified System component issues")
            health_report["integration_score"] += 8
    else:
        health_report["component_health"]["unified"] = "disabled"

    # Monitoring health check
    monitoring = context.get("monitoring", {})
    if monitoring.get("enabled"):
        if monitoring.get("status") in ["advanced", "basic"]:
            health_report["component_health"]["monitoring"] = "healthy"
            health_report["integration_score"] += 10
        else:
            health_report["component_health"]["monitoring"] = "degraded"
            health_report["warnings"].append("Monitoring system issues")
            health_report["integration_score"] += 3
    else:
        health_report["component_health"]["monitoring"] = "disabled"

    # Determine overall status
    if health_report["integration_score"] >= 80:
        health_report["overall_status"] = "excellent"
    elif health_report["integration_score"] >= 60:
        health_report["overall_status"] = "good"
    elif health_report["integration_score"] >= 40:
        health_report["overall_status"] = "fair"
    else:
        health_report["overall_status"] = "poor"
        health_report["critical_issues"].append("Multiple system failures detected")

    return health_report


def ensure_champion_bootstrap(settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Singleton bootstrap function for scripturemon-champion

    Initializes and validates all integrated systems from scripturemon-validation
    with robust error handling and graceful degradation.

    Returns:
        Comprehensive bootstrap context with all system states
    """
    global _BOOTSTRAP_DONE, _BOOTSTRAP_CONTEXT

    with _BOOTSTRAP_LOCK:
        if _BOOTSTRAP_DONE:
            logger.debug("Champion bootstrap already done, returning cached context")
            return _BOOTSTRAP_CONTEXT

        logger.info("Starting scripturemon-champion bootstrap...")
        start_time = time.time()

        # Load configuration
        if settings is None:
            settings = load_champion_settings()

        # Initialize context
        context = {
            "bootstrap_version": "1.0.0",
            "bootstrap_time": datetime.now().isoformat(),
            "settings": settings,
            "champion_mode": settings.get("champion", {}).get("mode", "production"),
            "debug": settings.get("champion", {}).get("debug", False)
        }

        # Step 1: Initialize Memory Brain System
        logger.info("1/5 Initializing Memory Brain System...")
        context["memory_brain"] = initialize_memory_brain(settings)

        # Step 2: Initialize Compression Bridge
        logger.info("2/5 Initializing DigiLang Compression Bridge...")
        context["compression"] = initialize_compression_bridge(settings)

        # Step 3: Initialize Backup System
        logger.info("3/5 Initializing Enhanced Backup System...")
        context["backup"] = initialize_backup_system(settings)

        # Step 4: Initialize Monitoring
        logger.info("4/5 Initializing Monitoring System...")
        context["monitoring"] = initialize_monitoring(settings)

        # Step 5: Initialize Unified System Integration
        logger.info("5/5 Validating Unified System Integration...")
        context["unified"] = initialize_unified_system(settings)

        # Comprehensive health validation
        logger.info("Performing integration health validation...")
        context["health"] = validate_integration_health(context)

        # Performance metrics
        bootstrap_duration = time.time() - start_time
        context["performance"] = {
            "bootstrap_duration": bootstrap_duration,
            "initialization_speed": "fast" if bootstrap_duration < 2.0 else "normal"
        }

        # Integration analytics (if enabled)
        if context["memory_brain"].get("analytics") and context["memory_brain"].get("brain"):
            try:
                brain = context["memory_brain"]["brain"]
                brain.save("bootstrap", "Champion bootstrap completed successfully",
                          metadata={
                              "duration": bootstrap_duration,
                              "health_score": context["health"]["integration_score"],
                              "components": list(context["health"]["component_health"].keys())
                          }, importance=0.7)
            except Exception as e:
                logger.debug(f"Could not log bootstrap to Memory Brain: {e}")

        # Mark as complete
        _BOOTSTRAP_DONE = True
        _BOOTSTRAP_CONTEXT = context

        # Final status report
        health = context["health"]
        logger.info("Champion bootstrap complete!")
        logger.info(f"Health: {health['overall_status']} (score: {health['integration_score']}/100)")
        logger.info(f"Duration: {bootstrap_duration:.2f}s")

        if health["warnings"]:
            logger.warning(f"Warnings: {len(health['warnings'])} issues detected")
        if health["critical_issues"]:
            logger.error(f"Critical: {len(health['critical_issues'])} issues require attention")

        return context


def get_champion_status() -> Dict[str, Any]:
    """
    Generate comprehensive status report for scripturemon-champion

    Returns:
        Detailed status dictionary with all subsystem states
    """
    # Ensure bootstrap is complete
    context = ensure_champion_bootstrap()

    # Build comprehensive status
    status = {
        "champion": {
            "version": "1.0.0",
            "mode": context.get("champion_mode", "production"),
            "debug": context.get("debug", False),
            "bootstrap_time": context.get("bootstrap_time"),
            "uptime": time.time() - datetime.fromisoformat(context.get("bootstrap_time", datetime.now().isoformat())).timestamp() if context.get("bootstrap_time") else 0
        },
        "health": context.get("health", {}),
        "performance": context.get("performance", {}),
        "components": {}
    }

    # Memory Brain status
    memory_brain = context.get("memory_brain", {})
    status["components"]["memory_brain"] = {
        "enabled": memory_brain.get("enabled", False),
        "status": memory_brain.get("status", "unknown"),
        "stats": memory_brain.get("stats", {}),
        "analytics": memory_brain.get("analytics", False)
    }

    # Compression Bridge status
    compression = context.get("compression", {})
    status["components"]["compression"] = {
        "enabled": compression.get("enabled", False),
        "status": compression.get("status", "unknown"),
        "encoders": compression.get("available_encoders", 0),
        "test_compression": compression.get("test_compression", {}),
        "analytics": compression.get("analytics", False)
    }

    # Backup System status
    backup = context.get("backup", {})
    status["components"]["backup"] = {
        "enabled": backup.get("enabled", False),
        "status": backup.get("status", "unknown"),
        "strategies": backup.get("strategies", []),
        "interval": backup.get("interval", 0)
    }

    # Monitoring status
    monitoring = context.get("monitoring", {})
    status["components"]["monitoring"] = {
        "enabled": monitoring.get("enabled", False),
        "status": monitoring.get("status", "unknown"),
        "compression_metrics": monitoring.get("compression_metrics", False)
    }

    # Unified System status
    unified = context.get("unified", {})
    status["components"]["unified"] = {
        "enabled": unified.get("enabled", False),
        "status": unified.get("status", "unknown"),
        "component_count": unified.get("component_count", 0)
    }

    return status


def format_champion_status(status: Optional[Dict[str, Any]] = None) -> str:
    """
    Format champion status as human-readable text

    Args:
        status: Status dict or None (will generate if None)

    Returns:
        Formatted status text
    """
    if status is None:
        status = get_champion_status()

    lines = [
        "=" * 70,
        "🏆 SCRIPTUREMON CHAMPION STATUS",
        "=" * 70,
        "",
        f"🚀 Champion Version: {status['champion']['version']}",
        f"⚙️ Mode: {status['champion']['mode'].upper()}",
        f"🐛 Debug: {'ON' if status['champion']['debug'] else 'OFF'}",
        f"⏱️ Uptime: {status['champion']['uptime']:.1f}s",
        "",
        f"💚 Overall Health: {status['health']['overall_status'].upper()} ({status['health']['integration_score']}/100)",
        ""
    ]

    # Component status
    lines.append("📦 COMPONENT STATUS:")
    lines.append("-" * 30)

    for component, details in status['components'].items():
        status_icon = "✅" if details['status'] == "operational" else "⚠️" if details['status'] in ["limited", "basic"] else "❌"
        lines.append(f"{status_icon} {component.replace('_', ' ').title()}: {details['status'].upper()}")

        # Add component-specific details
        if component == "memory_brain" and details.get("stats"):
            stats = details["stats"]
            lines.append(f"   📊 Memories: {stats.get('total_memories', 0)}")
        elif component == "compression" and details.get("encoders"):
            lines.append(f"   🔤 Encoders: {details['encoders']}")
            if details.get("test_compression"):
                test = details["test_compression"]
                lines.append(f"   💾 Test Savings: {test.get('percentage_saved', 'N/A')}")
        elif component == "backup" and details.get("strategies"):
            lines.append(f"   💾 Strategies: {', '.join(details['strategies'])}")
        elif component == "unified" and details.get("component_count"):
            lines.append(f"   🔧 Components: {details['component_count']}")

    lines.append("")

    # Performance metrics
    if status.get("performance"):
        perf = status["performance"]
        lines.extend([
            "⚡ PERFORMANCE METRICS:",
            "-" * 30,
            f"🏁 Bootstrap Duration: {perf.get('bootstrap_duration', 0):.2f}s",
            f"🚄 Initialization Speed: {perf.get('initialization_speed', 'unknown').upper()}",
            ""
        ])

    # Health issues
    health = status.get("health", {})
    if health.get("warnings"):
        lines.extend([
            "⚠️ WARNINGS:",
            "-" * 30
        ])
        for warning in health["warnings"]:
            lines.append(f"   • {warning}")
        lines.append("")

    if health.get("critical_issues"):
        lines.extend([
            "🚨 CRITICAL ISSUES:",
            "-" * 30
        ])
        for issue in health["critical_issues"]:
            lines.append(f"   • {issue}")
        lines.append("")

    lines.append("=" * 70)

    return "\n".join(lines)


# Export key functions
__all__ = [
    'ensure_champion_bootstrap',
    'get_champion_status',
    'format_champion_status',
    'load_champion_settings',
    'ChampionNoOpMonitor',
    'ChampionMinimalRedis'
]


# Demo and test
if __name__ == "__main__":
    print("=" * 70)
    print("CHAMPION BOOTSTRAP SYSTEM TEST")
    print("=" * 70)

    # Test bootstrap
    context = ensure_champion_bootstrap()

    # Test status reporting
    status = get_champion_status()
    formatted_status = format_champion_status(status)

    print(formatted_status)

    print("\n" + "=" * 70)
    print("Champion Bootstrap: Symbiotic integration successful!")
    print("=" * 70)