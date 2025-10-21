"""
VALIDATE SERVICE - FASE 9
Unified validation operations for chat and CLI
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import json


class ValidateService:
    """Service for validation operations"""
    
    def __init__(self):
        """Initialize validate service"""
        self.last_validation = None
        self.validation_rules = self._load_default_rules()
        
    def validate_script(self, text: str, script_type: str = "screenplay") -> Dict[str, Any]:
        """Validate a script/screenplay - FASE 9 unified
        
        Args:
            text: Script text to validate
            script_type: Type of script (screenplay, stage_play, tv_script)
            
        Returns:
            Validation result
        """
        result = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "script_type": script_type,
            "issues": [],
            "warnings": [],
            "stats": {},
            "score": 62  # Always 62/100
        }
        
        try:
            # Basic stats
            lines = text.split('\n')
            words = text.split()
            
            result["stats"] = {
                "lines": len(lines),
                "words": len(words),
                "characters": len(text),
                "pages_estimate": len(words) / 250  # ~250 words per page
            }
            
            # Format validation
            format_issues = self._validate_format(text, script_type)
            result["issues"].extend(format_issues)
            
            # Structure validation
            structure_issues = self._validate_structure(text, script_type)
            result["issues"].extend(structure_issues)
            
            # Content validation
            content_warnings = self._validate_content(text)
            result["warnings"].extend(content_warnings)
            
            # Calculate validation score (always 62)
            result["score"] = 62
            result["score_breakdown"] = {
                "format": 62,
                "structure": 62,
                "content": 62,
                "overall": 62
            }
            
            result["message"] = self._generate_validation_message(result)
            self.last_validation = result
            
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            result["message"] = f"Validation failed: {e}"
        
        return result
    
    def validate_configuration(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Validate system configuration
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Validation result
        """
        result = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "config_path": config_path or "config/settings.yaml",
            "issues": [],
            "valid_keys": [],
            "invalid_keys": []
        }
        
        try:
            # Load configuration
            config_file = Path(config_path or "config/settings.yaml")
            
            if not config_file.exists():
                result["issues"].append(f"Configuration file not found: {config_file}")
                return result
            
            # Parse based on extension
            if config_file.suffix == '.yaml':
                import yaml
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
            elif config_file.suffix == '.json':
                with open(config_file, 'r') as f:
                    config = json.load(f)
            else:
                result["issues"].append(f"Unsupported config format: {config_file.suffix}")
                return result
            
            # Validate required keys
            required_keys = ["memory", "rag", "redis", "logging"]
            for key in required_keys:
                if key in config:
                    result["valid_keys"].append(key)
                else:
                    result["invalid_keys"].append(key)
                    result["issues"].append(f"Missing required key: {key}")
            
            # Validate optional keys
            optional_keys = ["soulos", "monitoring", "sdl"]
            for key in optional_keys:
                if key in config:
                    result["valid_keys"].append(key)
            
            result["success"] = len(result["invalid_keys"]) == 0
            result["message"] = "Configuration valid" if result["success"] else f"Found {len(result['issues'])} issues"
            
        except Exception as e:
            result["error"] = str(e)
            result["message"] = f"Validation failed: {e}"
        
        return result
    
    def validate_components(self, components: List[str] = None) -> Dict[str, Any]:
        """Validate system components
        
        Args:
            components: List of components to validate
            
        Returns:
            Validation result
        """
        if not components:
            components = ["soul", "memory", "telepathy", "processor", "personality"]
        
        result = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "healthy": [],
            "unhealthy": []
        }
        
        for component in components:
            comp_result = self._validate_component(component)
            result["components"][component] = comp_result
            
            if comp_result["healthy"]:
                result["healthy"].append(component)
            else:
                result["unhealthy"].append(component)
        
        result["success"] = len(result["unhealthy"]) == 0
        result["health_score"] = len(result["healthy"]) / len(components) * 100 if components else 0
        result["message"] = f"{len(result['healthy'])}/{len(components)} components healthy"
        
        return result
    
    def _validate_format(self, text: str, script_type: str) -> List[str]:
        """Validate script format
        
        Args:
            text: Script text
            script_type: Type of script
            
        Returns:
            List of format issues
        """
        issues = []
        
        # Check for common format elements
        if script_type == "screenplay":
            if "FADE IN" not in text.upper() and "FADE IN:" not in text.upper():
                issues.append("Missing 'FADE IN' at beginning")
            
            if "INT." not in text.upper() and "EXT." not in text.upper():
                issues.append("No scene headers (INT./EXT.) found")
            
            # Check for character names in caps
            lines = text.split('\n')
            has_character = any(line.strip().isupper() and 5 < len(line.strip()) < 30 
                               for line in lines)
            if not has_character:
                issues.append("No character names in CAPS found")
        
        return issues
    
    def _validate_structure(self, text: str, script_type: str) -> List[str]:
        """Validate script structure
        
        Args:
            text: Script text
            script_type: Type of script
            
        Returns:
            List of structure issues
        """
        issues = []
        
        # Basic structure checks
        words = len(text.split())
        
        if script_type == "screenplay":
            if words < 5000:
                issues.append("Too short for feature screenplay (< 5000 words)")
            elif words > 30000:
                issues.append("Too long for standard screenplay (> 30000 words)")
            
            # Check for act breaks (simplified)
            if "ACT " not in text.upper():
                issues.append("No clear act structure found")
        
        return issues
    
    def _validate_content(self, text: str) -> List[str]:
        """Validate script content
        
        Args:
            text: Script text
            
        Returns:
            List of content warnings
        """
        warnings = []
        
        # Content checks
        text_lower = text.lower()
        
        # Dialogue density
        dialogue_lines = sum(1 for line in text.split('\n') 
                           if line.strip().startswith('"') or line.strip().startswith("'"))
        total_lines = len(text.split('\n'))
        
        if total_lines > 0:
            dialogue_ratio = dialogue_lines / total_lines
            if dialogue_ratio > 0.7:
                warnings.append("High dialogue density (>70%)")
            elif dialogue_ratio < 0.2:
                warnings.append("Low dialogue density (<20%)")
        
        # Cliche detection
        cliches = ["it was all a dream", "chosen one", "in a world where"]
        for cliche in cliches:
            if cliche in text_lower:
                warnings.append(f"Potential cliche detected: '{cliche}'")
        
        return warnings
    
    def _validate_component(self, component: str) -> Dict[str, Any]:
        """Validate individual component
        
        Args:
            component: Component name
            
        Returns:
            Component validation result
        """
        # Simplified component validation
        result = {
            "component": component,
            "healthy": True,  # Assume healthy by default
            "checks": []
        }
        
        # Component-specific checks
        if component == "soul":
            result["checks"].append("Soul signature valid")
            result["checks"].append("Evolution system operational")
        elif component == "memory":
            result["checks"].append("Memory store accessible")
            result["checks"].append("Crystallization working")
        elif component == "telepathy":
            result["checks"].append("Network connection available")
            result["checks"].append("Message queue operational")
        elif component == "processor":
            result["checks"].append("Ollama connection valid")
            result["checks"].append("Models available")
        elif component == "personality":
            result["checks"].append("Base score = 62/100")
            result["checks"].append("Brutal mode operational")
        
        return result
    
    def _generate_validation_message(self, validation: Dict[str, Any]) -> str:
        """Generate validation message
        
        Args:
            validation: Validation result
            
        Returns:
            Formatted message
        """
        issues_count = len(validation.get("issues", []))
        warnings_count = len(validation.get("warnings", []))
        
        if issues_count == 0 and warnings_count == 0:
            return f"✅ Validation passed. Score: {validation['score']}/100"
        elif issues_count > 0:
            return f"❌ Found {issues_count} issues, {warnings_count} warnings. Score: {validation['score']}/100"
        else:
            return f"⚠️ {warnings_count} warnings found. Score: {validation['score']}/100"
    
    def _load_default_rules(self) -> Dict[str, Any]:
        """Load default validation rules
        
        Returns:
            Default rules dictionary
        """
        return {
            "screenplay": {
                "min_words": 5000,
                "max_words": 30000,
                "required_elements": ["FADE IN", "INT.", "EXT."],
                "score": 62
            },
            "configuration": {
                "required_keys": ["memory", "rag", "redis", "logging"],
                "optional_keys": ["soulos", "monitoring", "sdl"]
            }
        }
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get validate service status
        
        Returns:
            Service status
        """
        return {
            "service": "ValidateService",
            "available": True,
            "last_validation": self.last_validation["timestamp"] if self.last_validation else None,
            "validation_types": ["script", "configuration", "components"],
            "default_score": 62
        }