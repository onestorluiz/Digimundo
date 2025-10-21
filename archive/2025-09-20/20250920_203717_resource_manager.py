#!/usr/bin/env python3
"""
🔧 RESOURCE MANAGER - Gerenciamento de Recursos do Sistema
Controla CPU, GPU, memória e presets do sistema
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional
import psutil
import platform

class SystemSector(Enum):
    """Setores do sistema para gerenciamento de recursos"""
    CPU = "cpu"
    GPU = "gpu"
    MEMORY = "memory"
    STORAGE = "storage"
    NETWORK = "network"

@dataclass
class ResourcePreset:
    """Preset de configuração de recursos"""
    name: str
    description: str
    cpu_threads: int
    memory_limit_gb: int
    gpu_usage: float  # 0.0 to 1.0
    ollama_config: Dict[str, Any]

class ResourceManager:
    """Gerenciador central de recursos do sistema"""

    def __init__(self):
        self.current_preset = "balanced"
        self.system_info = self._get_system_info()
        self.presets = self._create_presets()

    def _get_system_info(self) -> Dict[str, Any]:
        """Obtém informações do sistema"""
        try:
            return {
                "cpu_count": psutil.cpu_count(),
                "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "platform": platform.system(),
                "machine": platform.machine(),
                "python_version": platform.python_version()
            }
        except Exception:
            return {
                "cpu_count": 8,  # Default fallback
                "memory_total_gb": 16.0,
                "platform": "Unknown",
                "machine": "Unknown",
                "python_version": "3.11"
            }

    def _create_presets(self) -> Dict[str, ResourcePreset]:
        """Cria presets baseados no hardware disponível"""
        cpu_count = self.system_info.get("cpu_count", 8)
        memory_gb = self.system_info.get("memory_total_gb", 16.0)

        return {
            "eco": ResourcePreset(
                name="eco",
                description="Modo econômico - uso mínimo de recursos",
                cpu_threads=max(2, cpu_count // 4),
                memory_limit_gb=max(4, int(memory_gb * 0.25)),
                gpu_usage=0.3,
                ollama_config={
                    'num_ctx': 32768,
                    'num_thread': max(2, cpu_count // 4),
                    'num_gpu': 30,
                    'num_batch': 1024,
                    'temperature': 0.3
                }
            ),
            "balanced": ResourcePreset(
                name="balanced",
                description="Modo balanceado - uso moderado de recursos",
                cpu_threads=max(4, cpu_count // 2),
                memory_limit_gb=max(8, int(memory_gb * 0.5)),
                gpu_usage=0.6,
                ollama_config={
                    'num_ctx': 65536,
                    'num_thread': max(4, cpu_count // 2),
                    'num_gpu': 45,
                    'num_batch': 2048,
                    'temperature': 0.3
                }
            ),
            "performance": ResourcePreset(
                name="performance",
                description="Modo performance - uso intenso de recursos",
                cpu_threads=max(6, int(cpu_count * 0.75)),
                memory_limit_gb=max(12, int(memory_gb * 0.75)),
                gpu_usage=0.9,
                ollama_config={
                    'num_ctx': 131072,
                    'num_thread': max(6, int(cpu_count * 0.75)),
                    'num_gpu': 60,
                    'num_batch': 4096,
                    'temperature': 0.3
                }
            ),
            "maximum": ResourcePreset(
                name="maximum",
                description="Modo máximo - uso total de recursos",
                cpu_threads=cpu_count,
                memory_limit_gb=int(memory_gb * 0.9),
                gpu_usage=1.0,
                ollama_config={
                    'num_ctx': 200000,
                    'num_thread': cpu_count,
                    'num_gpu': 60,
                    'num_batch': 8192,
                    'temperature': 0.3
                }
            )
        }

    def apply_preset(self, preset_name: str) -> bool:
        """Aplica um preset de recursos"""
        if preset_name not in self.presets:
            return False

        self.current_preset = preset_name
        return True

    def get_current_preset(self) -> ResourcePreset:
        """Retorna o preset atual"""
        return self.presets[self.current_preset]

    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do gerenciador"""
        current = self.get_current_preset()

        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
        except:
            cpu_percent = 0
            memory = None

        return {
            "current_preset": self.current_preset,
            "preset_description": current.description,
            "system_info": self.system_info,
            "current_usage": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent if memory else 0,
                "memory_used_gb": round(memory.used / (1024**3), 2) if memory else 0
            },
            "preset_config": {
                "cpu_threads": current.cpu_threads,
                "memory_limit_gb": current.memory_limit_gb,
                "gpu_usage": current.gpu_usage
            }
        }

    def get_ollama_config(self, preset_name: Optional[str] = None) -> Dict[str, Any]:
        """Retorna configuração Ollama para o preset especificado"""
        preset = self.presets.get(preset_name or self.current_preset)
        if preset:
            return preset.ollama_config.copy()
        return self.presets["balanced"].ollama_config.copy()

    def is_resource_available(self, sector: SystemSector, threshold: float = 0.8) -> bool:
        """Verifica se um recurso está disponível (abaixo do threshold)"""
        try:
            if sector == SystemSector.CPU:
                return psutil.cpu_percent(interval=1) < (threshold * 100)
            elif sector == SystemSector.MEMORY:
                return psutil.virtual_memory().percent < (threshold * 100)
            elif sector == SystemSector.STORAGE:
                return psutil.disk_usage('/').percent < (threshold * 100)
        except:
            pass
        return True  # Default to available if can't check

    def get_recommended_preset(self) -> str:
        """Recomenda um preset baseado no uso atual do sistema"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent

            if cpu_percent > 80 or memory_percent > 80:
                return "eco"
            elif cpu_percent > 50 or memory_percent > 60:
                return "balanced"
            elif cpu_percent < 30 and memory_percent < 40:
                return "performance"
            else:
                return "balanced"
        except:
            return "balanced"

# Instância global para fácil acesso
_resource_manager = None

def get_resource_manager() -> ResourceManager:
    """Retorna instância singleton do ResourceManager"""
    global _resource_manager
    if _resource_manager is None:
        _resource_manager = ResourceManager()
    return _resource_manager