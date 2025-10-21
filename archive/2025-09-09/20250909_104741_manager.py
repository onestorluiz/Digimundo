"""
Personas Manager - Multiple Personality System
Phase 6 - Harmony vFinal

Manages different critic personas with controlled variation.
"""

import yaml
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Persona:
    """Represents a critic persona configuration"""
    name: str
    description: str
    display_name: str
    score_strategy: str  # fixed, variable_plus, calculated
    tone: str  # harsh, gentle, technical, inspiring
    emphasis: str  # failures, strengths, structure, originality
    base_score: Optional[int] = None
    score_offset: Optional[int] = None
    score_multiplier: Optional[float] = None
    min_score: Optional[int] = None
    max_score: Optional[int] = None
    signature_phrases: List[str] = None
    
    def __post_init__(self):
        if self.signature_phrases is None:
            self.signature_phrases = []
        
        # Set defaults based on strategy
        if self.score_strategy == "fixed" and self.base_score is None:
            self.base_score = 62
        if self.score_strategy == "variable_plus" and self.score_offset is None:
            self.score_offset = 10
        if self.score_strategy == "calculated" and self.score_multiplier is None:
            self.score_multiplier = 1.0
    
    def apply_score_strategy(self, base_score: float) -> float:
        """
        Apply persona's score strategy to modify the base score.
        
        Args:
            base_score: Original calculated score
            
        Returns:
            Modified score based on persona strategy
        """
        if self.score_strategy == "fixed":
            # Always return fixed score
            return float(self.base_score or 62)
        
        elif self.score_strategy == "variable_plus":
            # Add offset to base score
            offset = self.score_offset or 0
            new_score = base_score + offset
            
            # Apply min/max limits
            if self.min_score:
                new_score = max(new_score, self.min_score)
            if self.max_score:
                new_score = min(new_score, self.max_score)
            else:
                new_score = min(new_score, 100)  # Cap at 100
            
            return new_score
        
        elif self.score_strategy == "calculated":
            # Apply multiplier
            multiplier = self.score_multiplier or 1.0
            new_score = base_score * multiplier
            
            # Apply limits
            if self.min_score:
                new_score = max(new_score, self.min_score)
            if self.max_score:
                new_score = min(new_score, self.max_score)
            else:
                new_score = min(new_score, 100)
            
            return new_score
        
        else:
            # Unknown strategy, return original
            return base_score
    
    def format_feedback(self, feedback: str, score: float) -> str:
        """
        Adjust feedback tone based on persona.
        
        Args:
            feedback: Original feedback text
            score: Final score
            
        Returns:
            Adjusted feedback
        """
        # Add signature phrase if available
        if self.signature_phrases:
            import random
            signature = random.choice(self.signature_phrases)
            feedback = f"{signature}\n\n{feedback}"
        
        # Adjust tone
        if self.tone == "harsh":
            # Emphasize failures
            replacements = {
                "pode melhorar": "precisa melhorar urgentemente",
                "bom": "aceitável",
                "excelente": "adequado",
                "interessante": "básico",
                "criativo": "previsível com lampejos"
            }
        elif self.tone == "gentle":
            # Emphasize positives
            replacements = {
                "falhou": "tem oportunidade de melhorar",
                "ruim": "precisa de desenvolvimento",
                "fraco": "em desenvolvimento",
                "inadequado": "pode ser aprimorado",
                "péssimo": "tem potencial não explorado"
            }
        elif self.tone == "technical":
            # Focus on structure
            replacements = {
                "bom": "estruturalmente sólido",
                "ruim": "estruturalmente deficiente",
                "interessante": "tecnicamente notável",
                "criativo": "inovador na forma"
            }
        elif self.tone == "inspiring":
            # Encourage creativity
            replacements = {
                "comum": "com potencial único",
                "básico": "fundação para algo maior",
                "simples": "elegantemente minimalista",
                "complexo": "ricamente elaborado"
            }
        else:
            replacements = {}
        
        # Apply replacements
        for old, new in replacements.items():
            feedback = feedback.replace(old, new)
        
        # Add emphasis based on persona
        if self.emphasis == "failures" and score < 70:
            feedback += "\n\n⚠️ Atenção aos pontos fracos mencionados."
        elif self.emphasis == "strengths" and score > 40:
            feedback += "\n\n✨ Continue desenvolvendo seus pontos fortes!"
        elif self.emphasis == "structure":
            feedback += "\n\n📐 Foque na estrutura narrativa."
        elif self.emphasis == "originality":
            feedback += "\n\n🎨 Valorize sua voz única."
        
        return feedback


class PersonasManager:
    """Manages multiple personas and their configurations"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize personas manager.
        
        Args:
            config_path: Path to personas configuration file
        """
        self.config_path = config_path or Path("config/personas.yaml")
        self.personas: Dict[str, Persona] = {}
        self.current_persona_name: str = "brutal"
        self.current_persona: Optional[Persona] = None
        
        # Load personas
        self._load_personas()
    
    def _load_personas(self):
        """Load personas from configuration file or use defaults"""
        try:
            if self.config_path.exists():
                with open(self.config_path) as f:
                    config = yaml.safe_load(f)
                    
                for name, data in config.get("personas", {}).items():
                    persona = Persona(
                        name=name,
                        description=data.get("description", ""),
                        display_name=data.get("display_name", name.title()),
                        score_strategy=data.get("score_strategy", "calculated"),
                        tone=data.get("tone", "neutral"),
                        emphasis=data.get("emphasis", "balanced"),
                        base_score=data.get("base_score"),
                        score_offset=data.get("score_offset"),
                        score_multiplier=data.get("score_multiplier"),
                        min_score=data.get("min_score"),
                        max_score=data.get("max_score"),
                        signature_phrases=data.get("signature_phrases", [])
                    )
                    self.personas[name] = persona
                
                # Set default
                self.current_persona_name = config.get("default_persona", "brutal")
                
                logger.info(f"✅ Loaded {len(self.personas)} personas from {self.config_path}")
            else:
                # Use built-in defaults
                self._load_default_personas()
                
        except Exception as e:
            logger.error(f"Error loading personas: {e}")
            self._load_default_personas()
        
        # Set current persona
        self.current_persona = self.personas.get(self.current_persona_name)
    
    def _load_default_personas(self):
        """Load default built-in personas"""
        self.personas = {
            "brutal": Persona(
                name="brutal",
                description="Crítico severo e implacável. Nunca dá mais que 62/100.",
                display_name="Brutal (Clássico)",
                score_strategy="fixed",
                base_score=62,
                tone="harsh",
                emphasis="failures",
                signature_phrases=[
                    "62/100. Como sempre.",
                    "Reescreva. Do zero. Agora.",
                    "Até comercial de TV tem mais conteúdo."
                ]
            ),
            "merciful": Persona(
                name="merciful",
                description="Crítico construtivo e encorajador.",
                display_name="Misericordioso",
                score_strategy="variable_plus",
                score_offset=15,
                tone="gentle",
                emphasis="strengths",
                signature_phrases=[
                    "Há potencial aqui...",
                    "Com alguns ajustes, pode brilhar.",
                    "Continue desenvolvendo esta ideia."
                ]
            )
        }
        logger.info("📚 Using default personas (brutal, merciful)")
    
    def list_personas(self) -> List[Dict[str, Any]]:
        """
        List all available personas.
        
        Returns:
            List of persona information
        """
        result = []
        for name, persona in self.personas.items():
            result.append({
                "name": name,
                "display_name": persona.display_name,
                "description": persona.description,
                "active": name == self.current_persona_name
            })
        return result
    
    def set_persona(self, name: str) -> bool:
        """
        Set the active persona.
        
        Args:
            name: Persona name
            
        Returns:
            True if successful
        """
        if name in self.personas:
            self.current_persona_name = name
            self.current_persona = self.personas[name]
            logger.info(f"🎭 Persona changed to: {name}")
            return True
        else:
            logger.warning(f"Persona not found: {name}")
            return False
    
    def get_current_persona(self) -> Optional[Persona]:
        """Get the current active persona"""
        return self.current_persona
    
    def apply_persona(self, base_score: float, feedback: str) -> tuple[float, str]:
        """
        Apply current persona to score and feedback.
        
        Args:
            base_score: Original calculated score
            feedback: Original feedback text
            
        Returns:
            Tuple of (modified_score, modified_feedback)
        """
        if not self.current_persona:
            return base_score, feedback
        
        # Apply score strategy
        modified_score = self.current_persona.apply_score_strategy(base_score)
        
        # Format feedback
        modified_feedback = self.current_persona.format_feedback(feedback, modified_score)
        
        return modified_score, modified_feedback
    
    def format_status(self) -> str:
        """Format current persona status"""
        if not self.current_persona:
            return "Persona: Nenhuma"
        
        return f"Persona: {self.current_persona.display_name}"


# Global instance
_personas_manager: Optional[PersonasManager] = None


def get_personas_manager() -> PersonasManager:
    """Get or create global personas manager"""
    global _personas_manager
    if _personas_manager is None:
        _personas_manager = PersonasManager()
    return _personas_manager


if __name__ == "__main__":
    # Test personas
    print("🧪 Testing Personas Manager...")
    
    manager = PersonasManager()
    
    # List personas
    print("\n📚 Available Personas:")
    for p in manager.list_personas():
        active = " (active)" if p["active"] else ""
        print(f"  • {p['display_name']}{active}: {p['description']}")
    
    # Test score modification
    base_score = 75
    feedback = "O roteiro tem problemas estruturais mas mostra criatividade."
    
    print(f"\n🎯 Base Score: {base_score}")
    print(f"📝 Base Feedback: {feedback}")
    
    # Test each persona
    for name in ["brutal", "merciful"]:
        manager.set_persona(name)
        mod_score, mod_feedback = manager.apply_persona(base_score, feedback)
        print(f"\n🎭 Persona: {name}")
        print(f"  Score: {base_score} → {mod_score}")
        print(f"  Feedback preview: {mod_feedback[:100]}...")
    
    print("\n✅ Personas tests complete!")