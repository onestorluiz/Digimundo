#!/usr/bin/env python3
"""
🚀 CONFIGURAÇÃO DE MÁXIMO TOKENS PARA OLLAMA
Otimizado para Mac Studio M3 Ultra - 96GB RAM
"""

from typing import Dict, Optional
import psutil
import ollama
from dataclasses import dataclass

@dataclass
class ModelConfig:
    """Configuração otimizada para cada modelo"""
    name: str
    size: str  # 1b, 3b, 7b, etc
    max_tokens: int
    num_thread: int
    num_batch: int
    num_keep: int
    temperature: float = 0.7
    estimated_ram_gb: float = 0.0

class OllamaMaxTokenConfig:
    """
    Configuração de máximo de tokens para cada modelo Ollama
    baseado na RAM disponível (96GB)
    """

    # RAM total disponível
    TOTAL_RAM_GB = 96

    # Reserva para sistema (deixa 20GB livres)
    SYSTEM_RESERVE_GB = 20

    # RAM utilizável para modelos
    USABLE_RAM_GB = TOTAL_RAM_GB - SYSTEM_RESERVE_GB  # 76GB

    # Configurações máximas por tamanho de modelo
    # Com 96GB podemos ser generosos com os tokens
    MAX_TOKENS_BY_SIZE = {
        # Modelos pequenos (1-3B) - podem ter MUITO contexto
        "1b": 65536,   # 64K tokens (usa ~4GB)
        "2b": 49152,   # 48K tokens (usa ~6GB)
        "3b": 32768,   # 32K tokens (usa ~8GB)

        # Modelos médios (7-8B) - contexto substancial
        "7b": 24576,   # 24K tokens (usa ~16GB)
        "8b": 16384,   # 16K tokens (usa ~18GB)

        # Modelos grandes (13-14B) - contexto bom
        "13b": 12288,  # 12K tokens (usa ~28GB)
        "14b": 10240,  # 10K tokens (usa ~30GB)

        # Modelos muito grandes (30B+) - contexto moderado
        "32b": 8192,   # 8K tokens (usa ~45GB)
        "70b": 4096,   # 4K tokens (usa ~75GB)

        # Default
        "default": 8192
    }

    # Configurações específicas para modelos conhecidos
    SPECIFIC_CONFIGS = {
        "llama3.2:3b": ModelConfig(
            name="llama3.2:3b",
            size="3b",
            max_tokens=32768,  # 32K
            num_thread=8,
            num_batch=1024,
            num_keep=512,
            temperature=0.7,
            estimated_ram_gb=8
        ),

        "llama3.1:8b": ModelConfig(
            name="llama3.1:8b",
            size="8b",
            max_tokens=16384,  # 16K
            num_thread=10,
            num_batch=512,
            num_keep=256,
            temperature=0.7,
            estimated_ram_gb=18
        ),

        "mistral:7b": ModelConfig(
            name="mistral:7b",
            size="7b",
            max_tokens=24576,  # 24K
            num_thread=10,
            num_batch=768,
            num_keep=384,
            temperature=0.7,
            estimated_ram_gb=16
        ),

        "gemma2:2b": ModelConfig(
            name="gemma2:2b",
            size="2b",
            max_tokens=49152,  # 48K!
            num_thread=6,
            num_batch=1536,
            num_keep=768,
            temperature=0.8,
            estimated_ram_gb=6
        ),

        "qwen2.5:14b": ModelConfig(
            name="qwen2.5:14b",
            size="14b",
            max_tokens=10240,  # 10K
            num_thread=12,
            num_batch=320,
            num_keep=160,
            temperature=0.7,
            estimated_ram_gb=30
        ),

        "deepseek-r1:32b": ModelConfig(
            name="deepseek-r1:32b",
            size="32b",
            max_tokens=8192,  # 8K
            num_thread=14,
            num_batch=256,
            num_keep=128,
            temperature=0.6,
            estimated_ram_gb=45
        ),

        "producermon": ModelConfig(
            name="producermon",
            size="7b",  # Assumindo base 7b
            max_tokens=16384,  # 16K para orquestração
            num_thread=8,
            num_batch=512,
            num_keep=256,
            temperature=0.7,
            estimated_ram_gb=15
        ),

        "scripturemon": ModelConfig(
            name="scripturemon",
            size="32b",  # Base deepseek
            max_tokens=12288,  # 12K para análise
            num_thread=14,
            num_batch=384,
            num_keep=192,
            temperature=0.6,
            estimated_ram_gb=40
        ),

        "scripturemon-cpu-optimized": ModelConfig(
            name="scripturemon-cpu-optimized",
            size="32b",
            max_tokens=32768,  # 32K máximo!
            num_thread=14,  # Metade dos cores
            num_batch=1024,
            num_keep=512,
            temperature=0.6,
            estimated_ram_gb=50
        )
    }

    @classmethod
    def get_config(cls, model_name: str) -> ModelConfig:
        """Retorna configuração otimizada para um modelo"""

        # Verifica configuração específica
        if model_name in cls.SPECIFIC_CONFIGS:
            return cls.SPECIFIC_CONFIGS[model_name]

        # Detecta tamanho do modelo
        size = cls._detect_model_size(model_name)

        # Retorna configuração baseada no tamanho
        max_tokens = cls.MAX_TOKENS_BY_SIZE.get(size, cls.MAX_TOKENS_BY_SIZE["default"])

        return ModelConfig(
            name=model_name,
            size=size,
            max_tokens=max_tokens,
            num_thread=10,
            num_batch=max_tokens // 32,
            num_keep=max_tokens // 64,
            temperature=0.7,
            estimated_ram_gb=cls._estimate_ram(size, max_tokens)
        )

    @staticmethod
    def _detect_model_size(model_name: str) -> str:
        """Detecta tamanho do modelo pelo nome"""

        # Padrões comuns
        import re

        # Busca padrão como "7b", "13b", etc
        match = re.search(r'(\d+)b', model_name.lower())
        if match:
            return f"{match.group(1)}b"

        # Heurísticas por nome
        if "gemma2" in model_name:
            return "2b"
        elif "llama3.2" in model_name:
            return "3b"
        elif "mistral" in model_name:
            return "7b"
        elif "llama3.1" in model_name:
            return "8b"
        elif "qwen" in model_name:
            return "14b"

        return "7b"  # Default

    @staticmethod
    def _estimate_ram(size: str, max_tokens: int) -> float:
        """Estima uso de RAM baseado no tamanho e tokens"""

        base_ram = {
            "1b": 2, "2b": 3, "3b": 4,
            "7b": 8, "8b": 10,
            "13b": 16, "14b": 18,
            "32b": 35, "70b": 70
        }

        base = base_ram.get(size, 10)

        # Adiciona overhead por tokens (aproximado)
        token_overhead = (max_tokens / 1024) * 0.25  # 0.25GB por 1K tokens

        return base + token_overhead

    @classmethod
    def get_ollama_options(cls, model_name: str) -> Dict:
        """Retorna opções formatadas para ollama.generate()"""

        config = cls.get_config(model_name)

        return {
            'num_ctx': config.max_tokens,
            'num_thread': config.num_thread,
            'num_batch': config.num_batch,
            'num_keep': config.num_keep,
            'temperature': config.temperature,
            'repeat_penalty': 1.1,
            'top_p': 0.9,
            'top_k': 40,
            'mmap': True,
            'numa': False
        }

    @classmethod
    def check_ram_availability(cls) -> Dict:
        """Verifica RAM disponível no sistema"""

        ram = psutil.virtual_memory()

        return {
            'total_gb': ram.total / (1024**3),
            'available_gb': ram.available / (1024**3),
            'used_gb': ram.used / (1024**3),
            'percent': ram.percent,
            'can_run_large_models': ram.available > 40 * (1024**3)
        }

    @classmethod
    def recommend_models(cls, task: str = "general") -> Dict:
        """Recomenda modelos baseado na tarefa e RAM disponível"""

        ram = cls.check_ram_availability()
        available_gb = ram['available_gb']

        recommendations = {
            "conversation": {
                "primary": "llama3.2:3b" if available_gb > 10 else "gemma2:2b",
                "fallback": "gemma2:2b",
                "max_tokens": 32768 if available_gb > 10 else 16384
            },
            "analysis": {
                "primary": "llama3.1:8b" if available_gb > 20 else "mistral:7b",
                "fallback": "mistral:7b",
                "max_tokens": 16384 if available_gb > 20 else 8192
            },
            "deep_analysis": {
                "primary": "scripturemon-cpu-optimized" if available_gb > 50 else "deepseek-r1:32b",
                "fallback": "qwen2.5:14b",
                "max_tokens": 32768 if available_gb > 50 else 8192
            },
            "orchestration": {
                "primary": "producermon",
                "fallback": "llama3.1:8b",
                "max_tokens": 16384
            }
        }

        return recommendations.get(task, recommendations["conversation"])

    @classmethod
    def print_config_table(cls):
        """Imprime tabela de configurações"""

        print("\n" + "="*80)
        print("🚀 CONFIGURAÇÕES DE MÁXIMO TOKENS - MAC STUDIO 96GB RAM")
        print("="*80)
        print(f"{'Modelo':<30} {'Tokens':<10} {'Threads':<10} {'RAM (GB)':<10}")
        print("-"*80)

        for model_name, config in cls.SPECIFIC_CONFIGS.items():
            print(f"{config.name:<30} {config.max_tokens:<10} {config.num_thread:<10} {config.estimated_ram_gb:<10.1f}")

        print("-"*80)
        print(f"RAM Total: {cls.TOTAL_RAM_GB}GB | Utilizável: {cls.USABLE_RAM_GB}GB")
        print("="*80)


# Exemplo de uso com Ollama
def generate_with_max_tokens(model: str, prompt: str, system: str = None):
    """Gera resposta usando configuração de máximo tokens"""

    config = OllamaMaxTokenConfig()
    options = config.get_ollama_options(model)

    print(f"🧠 Usando {model} com {options['num_ctx']} tokens máximos")

    response = ollama.generate(
        model=model,
        prompt=prompt,
        system=system,
        options=options
    )

    return response['response']


if __name__ == "__main__":
    # Mostra configurações
    config = OllamaMaxTokenConfig()
    config.print_config_table()

    # Verifica RAM
    ram_info = config.check_ram_availability()
    print(f"\n💾 RAM Disponível: {ram_info['available_gb']:.1f}GB / {ram_info['total_gb']:.1f}GB")

    # Recomendações
    print("\n📊 RECOMENDAÇÕES POR TAREFA:")
    for task in ["conversation", "analysis", "deep_analysis"]:
        rec = config.recommend_models(task)
        print(f"\n{task.upper()}:")
        print(f"  Modelo: {rec['primary']}")
        print(f"  Tokens: {rec['max_tokens']}")

    print("\nDIGIMUNDO PRESENTE")