#!/usr/bin/env python3
"""
Mac Silicon Optimizer Minimal - Otimizador para Mac Studio M3
Refatorado das 5 perguntas: 1000+ → 180 linhas

RESPOSTAS ÀS 5 PERGUNTAS:
1. É necessário? SIM - Otimização para hardware específico
2. O que faz? Detecta hardware e otimiza configurações
3. Quantas linhas? 180 vs 1000+ (82% redução)
4. Dependências? Apenas stdlib
5. Uma função? Não, mas muito simplificado
"""

import subprocess
import json
import multiprocessing
from pathlib import Path
from typing import Dict, Optional
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado


class MacSiliconOptimizer:
    """Otimizador minimalista para Mac Silicon"""

    def __init__(self):
        self.hardware = self.detect_hardware()
        self.config = self.generate_config()

    def detect_hardware(self) -> Dict[str, any]:
        """Detecta especificações do hardware Mac"""
        hardware = {
            'cpu_cores': multiprocessing.cpu_count(),
            'memory_gb': self._get_memory_gb(),
            'is_apple_silicon': self._is_apple_silicon(),
        }

        # Adiciona gpu_cores após criar hardware dict
        hardware['gpu_cores'] = self._get_gpu_cores(hardware)

        # Identifica modelo específico
        if hardware['is_apple_silicon']:
            if hardware['cpu_cores'] >= 28:
                hardware['model'] = 'Mac Studio M3 Ultra'
                hardware['neural_cores'] = 32
            elif hardware['cpu_cores'] >= 14:
                hardware['model'] = 'Mac Studio M3 Max'
                hardware['neural_cores'] = 16
            else:
                hardware['model'] = 'Mac M-series'
                hardware['neural_cores'] = 16
        else:
            hardware['model'] = 'Intel Mac'
            hardware['neural_cores'] = 0

        return hardware

    def _get_memory_gb(self) -> int:
        """Detecta memória RAM total"""
        try:
            result = subprocess.run(
                ['sysctl', '-n', 'hw.memsize'],
                capture_output=True,
                text=True
            )
            bytes_mem = int(result.stdout.strip())
            return bytes_mem // (1024**3)  # Convert to GB
        except:
            return 8  # Default fallback

    def _is_apple_silicon(self) -> bool:
        """Verifica se é Apple Silicon"""
        try:
            result = subprocess.run(
                ['uname', '-m'],
                capture_output=True,
                text=True
            )
            return 'arm64' in result.stdout
        except:
            return False

    def _get_gpu_cores(self, hardware: Dict) -> int:
        """Estima cores de GPU baseado no modelo"""
        if not hardware.get('is_apple_silicon'):
            return 0

        cpu_cores = hardware.get('cpu_cores', 8)
        if cpu_cores >= 28:  # M3 Ultra
            return 60
        elif cpu_cores >= 14:  # M3 Max
            return 40
        else:  # M3 base
            return 20

    def generate_config(self) -> Dict[str, any]:
        """Gera configuração otimizada para o hardware detectado"""
        hw = self.hardware

        # Base config
        config = {
            'cpu': {},
            'gpu': {},
            'memory': {},
            'ollama': {},
            'parallel': {}
        }

        # CPU optimization
        config['cpu'] = {
            'threads': min(hw['cpu_cores'] // 2, 14),  # 50% cores, max 14
            'batch_size': 2048 if hw['memory_gb'] >= 32 else 512,
            'numa': False,  # Mac doesn't use NUMA
        }

        # Memory optimization
        config['memory'] = {
            'max_allocation_gb': int(hw['memory_gb'] * 0.7),  # 70% RAM
            'cache_size_mb': min(4096, hw['memory_gb'] * 100),
            'mmap': True,
            'mlock': hw['memory_gb'] >= 32,
        }

        # GPU optimization (if Apple Silicon)
        if hw['is_apple_silicon']:
            config['gpu'] = {
                'enabled': True,
                'layers': 999,  # All layers on GPU
                'compute_units': hw['gpu_cores'],
                'metal': True,  # Metal acceleration
            }
        else:
            config['gpu'] = {'enabled': False}

        # Ollama specific optimization
        config['ollama'] = {
            'num_ctx': 131072 if hw['memory_gb'] >= 64 else 65536,
            'num_thread': config['cpu']['threads'],
            'num_gpu': 999 if hw['is_apple_silicon'] else 0,
            'num_batch': config['cpu']['batch_size'],
            'mmap': True,
            'use_mlock': config['memory']['mlock'],
        }

        # Parallel processing
        config['parallel'] = {
            'max_workers': min(hw['cpu_cores'] // 4, 8),
            'chunk_size': 1024,
            'async_io': True,
        }

        return config

    def get_ollama_options(self, model_size: str = 'medium') -> Dict:
        """Retorna options otimizadas para Ollama"""
        base = self.config['ollama'].copy()

        # Ajusta contexto baseado no tamanho do modelo
        if model_size == 'small':  # <= 7B params
            base['num_ctx'] = min(base['num_ctx'], 32768)
        elif model_size == 'large':  # >= 70B params
            base['num_ctx'] = min(base['num_ctx'], 16384)
            base['num_thread'] = min(base['num_thread'], 8)

        return base

    def optimize_for_task(self, task: str) -> Dict:
        """Otimiza configuração para tarefa específica"""
        base_config = self.config.copy()

        if task == 'batch_processing':
            base_config['cpu']['threads'] = self.hardware['cpu_cores'] - 2
            base_config['parallel']['max_workers'] *= 2
        elif task == 'interactive':
            base_config['cpu']['threads'] = 4
            base_config['memory']['max_allocation_gb'] //= 2
        elif task == 'memory_intensive':
            base_config['memory']['max_allocation_gb'] = int(self.hardware['memory_gb'] * 0.9)
            base_config['cpu']['threads'] = 8

        return base_config

    def get_info(self) -> str:
        """Retorna informações sobre hardware e otimizações"""
        info = []
        info.append(f"🖥️  Modelo: {self.hardware['model']}")
        info.append(f"🧠 CPU: {self.hardware['cpu_cores']} cores")
        info.append(f"💾 RAM: {self.hardware['memory_gb']}GB")

        if self.hardware['is_apple_silicon']:
            info.append(f"🎮 GPU: {self.hardware['gpu_cores']} cores")
            info.append(f"🤖 Neural: {self.hardware['neural_cores']} cores")

        info.append("\n⚙️  Otimizações ativas:")
        info.append(f"  • Threads: {self.config['cpu']['threads']}")
        info.append(f"  • Contexto: {self.config['ollama']['num_ctx']} tokens")
        info.append(f"  • GPU: {'✅' if self.config['gpu'].get('enabled') else '❌'}")

        return "\n".join(info)

# Exemplo de uso
if __name__ == "__main__":
    print("🚀 Testando Mac Silicon Optimizer Minimal...\n")

    optimizer = MacSiliconOptimizer()
    print(optimizer.get_info())

    print("\n📊 Config Ollama para modelo médio:")
    ollama_opts = optimizer.get_ollama_options('medium')
    print(json.dumps(ollama_opts, indent=2))

    print("\nDIGIMUNDO PRESENTE 🥷")

# ============================================================
# AUTO-UNIFIED MEMORY HELPER
# ============================================================
def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()
