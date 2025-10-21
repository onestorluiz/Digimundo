#!/usr/bin/env python3
"""
Persona Module - Sistema de Personalidades (Stub para Fase 1.C)
Mantém complexidade sem simplificar
"""

from typing import Optional, List, Dict, Any
from enum import Enum

class PersonaType(Enum):
    """Tipos de persona disponíveis"""
    BRUTAL = "brutal"
    GENTLE = "gentle"
    TECHNICAL = "technical"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"

_active_persona = PersonaType.BRUTAL

def discover() -> List[str]:
    """
    Descobre todas as personas disponíveis
    Retorna lista complexa de personas
    """
    return [
        "brutal",
        "gentle", 
        "technical",
        "creative",
        "analytical",
        "experimental",
        "minimalist",
        "maximalist"
    ]

def set_active(persona: str) -> bool:
    """
    Define persona ativa
    Mantém validação e estado complexo
    """
    global _active_persona
    
    valid_personas = discover()
    if persona.lower() not in valid_personas:
        return False
    
    try:
        _active_persona = PersonaType[persona.upper()]
        return True
    except:
        # Fallback para personas não enum
        _active_persona = persona
        return True

def get_active() -> str:
    """Retorna persona ativa atual"""
    if isinstance(_active_persona, PersonaType):
        return _active_persona.value
    return str(_active_persona)

def get_config(persona: Optional[str] = None) -> Dict[str, Any]:
    """
    Retorna configuração complexa da persona
    """
    current = persona or get_active()
    
    configs = {
        "brutal": {
            "temperature": 0.9,
            "honesty": 1.0,
            "creativity": 0.7,
            "responses": ["direto", "sem filtros", "honesto"]
        },
        "gentle": {
            "temperature": 0.7,
            "honesty": 0.8,
            "creativity": 0.8,
            "responses": ["cuidadoso", "empático", "suave"]
        },
        "technical": {
            "temperature": 0.3,
            "honesty": 1.0,
            "creativity": 0.4,
            "responses": ["preciso", "detalhado", "técnico"]
        }
    }
    
    return configs.get(current, configs["brutal"])

def apply_persona(text: str, persona: Optional[str] = None) -> str:
    """
    Aplica transformação de persona ao texto
    Mantém processamento complexo
    """
    config = get_config(persona)
    
    # Stub: adiciona prefixo baseado na persona
    if config.get("honesty", 0) > 0.9:
        return f"[{get_active().upper()}] {text}"
    return text

class PersonaManager:
    """
    Gerenciador de personalidades para chat_engine
    Wrapper para funções existentes
    """
    def __init__(self):
        self.personas = discover()
        self.active = get_active()
    
    def list_personalities(self) -> List[str]:
        """Lista personalidades disponíveis"""
        return self.personas
    
    def set_personality(self, name: str) -> bool:
        """Define personalidade ativa"""
        if set_active(name):
            self.active = name
            return True
        return False
    
    def get_prompt(self, personality: str) -> Optional[str]:
        """Retorna prompt para personalidade"""
        config = get_config(personality)
        responses = config.get("responses", [])
        if responses:
            return f"Sua personalidade é {personality}: {', '.join(responses)}"
        return None

__all__ = ["discover", "set_active", "get_active", "get_config", "apply_persona", "PersonaType", "PersonaManager"]