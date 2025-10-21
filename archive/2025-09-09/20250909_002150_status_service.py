"""
STATUS SERVICE - FASE 9
Unified status reporting for chat and CLI
"""

from datetime import datetime
from typing import Dict, Any, Optional, List


class StatusService:
    """Service for system status reporting"""
    
    def __init__(self, soul=None, processor=None, personality=None, 
                 telepathy=None, monitoring=None, settings=None):
        """Initialize status service
        
        Args:
            soul: Soul instance
            processor: OllamaProcessor instance
            personality: BrutalPersonality instance
            telepathy: TelepathyNetwork instance
            monitoring: MonitoringSystem instance
            settings: System settings dictionary
        """
        self.soul = soul
        self.processor = processor
        self.personality = personality
        self.telepathy = telepathy
        self.monitoring = monitoring
        self.settings = settings or {}
        
    def get_full_status(self, verbose: bool = False) -> Dict[str, Any]:
        """Get complete system status - FASE 9 unified
        
        Args:
            verbose: Include detailed information
            
        Returns:
            Status dictionary
        """
        status = {
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "metrics": {},
            "configuration": {},
            "health": "unknown"
        }
        
        # Soul status
        if self.soul:
            soul_status = self.soul.status()
            status["components"]["soul"] = {
                "signature": soul_status.get("signature"),
                "age_seconds": soul_status.get("age_seconds", 0),
                "interactions": soul_status.get("interactions", 0),
                "evolution_count": soul_status.get("evolution_count", 0),
                "dominant_state": soul_status.get("dominant_state"),
                "is_legacy": soul_status.get("is_legacy", False)
            }
        
        # Processor status
        if self.processor:
            status["components"]["processor"] = {
                "available": True,
                "models": getattr(self.processor, 'available_models', []),
                "default_model": getattr(self.processor, 'default_model', None)
            }
        
        # Personality status
        if self.personality:
            status["components"]["personality"] = {
                "base_score": self.personality.BASE_SCORE,
                "analyses_count": self.personality.analyses_count,
                "style": self.personality.style,
                "intensity": self.personality.intensity,
                "variance": getattr(self.personality, 'variance', 0.0)
            }
        
        # Telepathy status
        if self.telepathy:
            tele_status = self.telepathy.get_status() if hasattr(self.telepathy, 'get_status') else {}
            status["components"]["telepathy"] = {
                "mode": tele_status.get("mode", "unknown"),
                "connected": tele_status.get("connected", False),
                "peers": len(self.telepathy.get_active_peers()) if hasattr(self.telepathy, 'get_active_peers') else 0
            }
        
        # Monitoring status
        if self.monitoring:
            mon_status = self.monitoring.get_status() if hasattr(self.monitoring, 'get_status') else {}
            status["components"]["monitoring"] = {
                "enabled": mon_status.get("enabled", False),
                "running": mon_status.get("running", False),
                "snapshots": mon_status.get("snapshots_collected", 0)
            }
            
            # Add metrics if available
            if hasattr(self.monitoring, 'get_last_snapshot'):
                snapshot = self.monitoring.get_last_snapshot()
                if snapshot:
                    status["metrics"] = snapshot.get("metrics", {})
        
        # Configuration
        status["configuration"] = {
            "soulos_enabled": self.settings.get("soulos", {}).get("enabled", False),
            "monitoring_enabled": self.settings.get("monitoring", {}).get("enabled", False),
            "rag_enabled": self.settings.get("rag", {}).get("enabled", True),
            "redis_enabled": self.settings.get("redis", {}).get("enabled", True)
        }
        
        # Calculate overall health
        status["health"] = self._calculate_health(status["components"])
        
        # Add verbose details if requested
        if verbose:
            status["verbose"] = self._get_verbose_details()
        
        return status
    
    def get_component_status(self, component: str) -> Dict[str, Any]:
        """Get status for specific component
        
        Args:
            component: Component name (soul, processor, etc.)
            
        Returns:
            Component status
        """
        full_status = self.get_full_status()
        
        if component in full_status["components"]:
            return {
                "component": component,
                "status": full_status["components"][component],
                "health": self._component_health(component, full_status["components"][component])
            }
        
        return {
            "component": component,
            "status": None,
            "health": "not_found",
            "message": f"Component '{component}' not found"
        }
    
    def format_status(self, status: Dict[str, Any], format_type: str = "text") -> str:
        """Format status for display
        
        Args:
            status: Status dictionary
            format_type: Output format (text, markdown, json)
            
        Returns:
            Formatted status string
        """
        if format_type == "json":
            import json
            return json.dumps(status, indent=2, default=str)
        
        # Format as text/markdown
        lines = []
        lines.append("🧠 **SYSTEM STATUS - HARMONY V100**")
        lines.append("")
        
        # Components
        if "components" in status:
            for comp_name, comp_status in status["components"].items():
                if comp_status:
                    lines.append(f"**{comp_name.upper()}:**")
                    for key, value in comp_status.items():
                        lines.append(f"  • {key}: {value}")
                    lines.append("")
        
        # Metrics
        if "metrics" in status and status["metrics"]:
            lines.append("**METRICS:**")
            for key, value in status["metrics"].items():
                lines.append(f"  • {key}: {value}")
            lines.append("")
        
        # Configuration
        if "configuration" in status:
            lines.append("**CONFIGURATION:**")
            for key, value in status["configuration"].items():
                lines.append(f"  • {key}: {value}")
            lines.append("")
        
        # Health
        lines.append(f"**Overall Health:** {status.get('health', 'unknown')}")
        
        return "\n".join(lines)
    
    def _calculate_health(self, components: Dict[str, Any]) -> str:
        """Calculate overall system health
        
        Args:
            components: Component status dictionary
            
        Returns:
            Health status (healthy, degraded, unhealthy)
        """
        if not components:
            return "unknown"
        
        # Count healthy components
        healthy_count = 0
        total_count = 0
        
        for comp_status in components.values():
            if comp_status:
                total_count += 1
                # Simple heuristic: component is healthy if it has data
                if comp_status.get("available") or comp_status.get("signature") or comp_status.get("mode"):
                    healthy_count += 1
        
        if total_count == 0:
            return "unknown"
        
        health_ratio = healthy_count / total_count
        
        if health_ratio >= 0.8:
            return "healthy"
        elif health_ratio >= 0.5:
            return "degraded"
        else:
            return "unhealthy"
    
    def _component_health(self, name: str, status: Dict[str, Any]) -> str:
        """Calculate individual component health
        
        Args:
            name: Component name
            status: Component status
            
        Returns:
            Component health status
        """
        if not status:
            return "unavailable"
        
        # Component-specific health checks
        if name == "soul" and status.get("signature"):
            return "healthy"
        elif name == "processor" and status.get("available"):
            return "healthy"
        elif name == "telepathy" and status.get("mode"):
            return "healthy" if status.get("connected") else "degraded"
        elif name == "monitoring" and status.get("enabled"):
            return "healthy" if status.get("running") else "degraded"
        
        return "unknown"
    
    def _get_verbose_details(self) -> Dict[str, Any]:
        """Get verbose details for all components
        
        Returns:
            Verbose details dictionary
        """
        details = {}
        
        # Add any available verbose information
        if self.soul:
            details["soul_full"] = self.soul.status()
        
        if self.settings:
            details["settings_full"] = self.settings
        
        return details
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get status service's own status
        
        Returns:
            Service status
        """
        return {
            "service": "StatusService",
            "available": True,
            "components_monitored": [
                "soul", "processor", "personality", 
                "telepathy", "monitoring"
            ]
        }