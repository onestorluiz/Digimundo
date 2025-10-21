from dataclasses import dataclass
from .paths import MEMORY_DB
@dataclass
class PathConfig: memory_db: str = str(MEMORY_DB)
@dataclass
class SystemConfig: log_level: str = 'INFO'
@dataclass
class OllamaConfig:
    default_model: str = 'mock-model'
    context_size: int = 8192
    fallback_models: list[str] = None
PATHS = PathConfig(); SYSTEM = SystemConfig(); OLLAMA = OllamaConfig(fallback_models=['mock-fallback'])
