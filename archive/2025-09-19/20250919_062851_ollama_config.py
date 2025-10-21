#!/usr/bin/env python3
"""
Ollama Configuration - Configuração inteligente baseada em hardware real
Substitui ollama_config_maximum.py com configuração sensata
"""

import subprocess
import psutil
from pathlib import Path
from typing import Dict, Optional
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado


class OllamaConfig:
    """Configuração inteligente do Ollama baseada em recursos disponíveis"""

    def __init__(self):
        self.cpu_cores = psutil.cpu_count(logical=False)
        self.memory_gb = psutil.virtual_memory().total / (1024**3)
        self.gpu_available = self._check_gpu()

    def _check_gpu(self) -> bool:
        """Verifica se GPU está disponível"""
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True)
            return result.returncode == 0
        except:
            # Mac com Apple Silicon
            return subprocess.run(['sysctl', 'hw.optional.arm64'], capture_output=True).returncode == 0

    def get_optimal_config(self, model_size: str = "7b") -> Dict:
        """Retorna configuração otimizada baseada no hardware"""

        # Parse do tamanho do modelo
        size_gb = self._parse_model_size(model_size)

        # Configuração baseada em recursos reais
        config = {
            'num_thread': min(self.cpu_cores - 1, 8),  # Deixa 1 core pro sistema
            'num_ctx': self._calculate_context_size(size_gb),
            'num_batch': 512,  # Padrão sensato
            'temperature': 0.7,  # Balanceado
            'top_k': 40,  # Padrão
            'top_p': 0.9,  # Padrão
        }

        # GPU config se disponível
        if self.gpu_available:
            # Usa GPU mas não "999 layers"
            config['num_gpu'] = -1  # Auto-detect layers
        else:
            config['num_gpu'] = 0

        return config

    def _parse_model_size(self, model_size: str) -> float:
        """Extrai tamanho do modelo em GB"""
        size = model_size.lower().replace('b', '')
        try:
            return float(size)
        except:
            return 7.0  # Default para 7B

    def _calculate_context_size(self, model_gb: float) -> int:
        """Calcula contexto baseado na RAM disponível"""
        # Regra: ~2GB RAM por 1k tokens de contexto
        available_ram = self.memory_gb * 0.6  # Usa 60% da RAM
        max_context = int((available_ram / model_gb) * 4096)

        # Limites sensatos
        return min(max(max_context, 2048), 32768)

    def test_model(self, model: str) -> bool:
        """Testa modelo com configuração otimizada"""
        config = self.get_optimal_config(model)

        try:
            cmd = ['ollama', 'run', model, '--verbose']
            for key, value in config.items():
                cmd.extend(['--' + key.replace('_', '-'), str(value)])

            # Teste simples
            test = subprocess.run(
                cmd + ['echo "test"'],
                capture_output=True,
                timeout=30  # Timeout sensato
            )
            return test.returncode == 0
        except:
            return False

    def save_config(self, model: str, output_dir: Path = Path.home() / '.ollama'):
        """Salva configuração otimizada"""
        config = self.get_optimal_config(model)
        output_dir.mkdir(exist_ok=True)

        config_file = output_dir / f"{model}_config.json"

        import json
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

        return config_file


# Uso simples
if __name__ == "__main__":
    config = OllamaConfig()

    print("🔧 OLLAMA INTELLIGENT CONFIGURATION")
    print("="*50)
    print(f"CPU Cores: {config.cpu_cores}")
    print(f"Memory: {config.memory_gb:.1f}GB")
    print(f"GPU: {'Available' if config.gpu_available else 'Not available'}")

    # Configuração otimizada
    optimal = config.get_optimal_config("7b")
    print(f"\n📊 Optimal Config for 7B model:")
    for key, value in optimal.items():
        print(f"  {key}: {value}")

    print("\n✅ Configuration based on REAL hardware, not fantasy!")

# ============================================================
# AUTO-UNIFIED MEMORY HELPER
# ============================================================
def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()
