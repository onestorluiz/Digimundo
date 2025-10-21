#!/usr/bin/env python3
"""
🚀 CONFIGURAÇÃO COMPLETA DE TODOS OS MODELOS OLLAMA
Inclui deepseek-r1:70b e todos os modelos de 42GB
Mac Studio M3 Ultra - 96GB RAM
"""

from typing import Dict, Optional, List
import psutil
import ollama
from dataclasses import dataclass

@dataclass
class ModelConfig:
    """Configuração completa para cada modelo"""
    name: str
    size_gb: float
    max_tokens: int
    num_thread: int
    num_batch: int
    num_keep: int
    num_gpu: int  # Camadas GPU
    temperature: float = 0.7
    description: str = ""

class OllamaCompleteConfig:
    """
    Configuração COMPLETA de TODOS os modelos Ollama
    SEM LIMITAR - usando TODO o potencial de 96GB
    """

    # Configurações REAIS baseadas nos modelos instalados
    COMPLETE_MODEL_CONFIGS = {
        # ========== MODELOS GIGANTES (42GB) ==========
        "deepseek-r1:70b": ModelConfig(
            name="deepseek-r1:70b",
            size_gb=42,
            max_tokens=131072,  # 128K tokens!!!
            num_thread=20,      # Usa 20 dos 28 cores
            num_batch=2048,
            num_keep=1024,
            num_gpu=99,         # Todas as camadas na GPU
            temperature=0.6,
            description="O GIGANTE - 128K contexto, análise suprema"
        ),

        "scripturemon-ultimate:latest": ModelConfig(
            name="scripturemon-ultimate:latest",
            size_gb=42,
            max_tokens=131072,  # 128K tokens!!!
            num_thread=20,
            num_batch=2048,
            num_keep=1024,
            num_gpu=99,
            temperature=0.6,
            description="ScriptureMon Ultimate - Análise cinematográfica máxima"
        ),

        "scripturemon-deepseek:latest": ModelConfig(
            name="scripturemon-deepseek:latest",
            size_gb=42,
            max_tokens=131072,  # 128K tokens!!!
            num_thread=20,
            num_batch=2048,
            num_keep=1024,
            num_gpu=99,
            temperature=0.6,
            description="ScriptureMon com DeepSeek - Profundidade total"
        ),

        # ========== MODELOS GRANDES (19GB) ==========
        "deepseek-r1:32b": ModelConfig(
            name="deepseek-r1:32b",
            size_gb=19,
            max_tokens=65536,   # 64K tokens!
            num_thread=14,
            num_batch=1024,
            num_keep=512,
            num_gpu=99,
            temperature=0.6,
            description="DeepSeek 32B - Raciocínio profundo"
        ),

        "scripturemon-cpu:latest": ModelConfig(
            name="scripturemon-cpu:latest",
            size_gb=19,
            max_tokens=65536,   # 64K tokens!
            num_thread=14,
            num_batch=1024,
            num_keep=512,
            num_gpu=0,          # CPU only
            temperature=0.6,
            description="ScriptureMon CPU - Processamento paralelo"
        ),

        "scripturemon-hybrid:latest": ModelConfig(
            name="scripturemon-hybrid:latest",
            size_gb=19,
            max_tokens=65536,   # 64K tokens!
            num_thread=14,
            num_batch=1024,
            num_keep=512,
            num_gpu=50,         # Híbrido GPU/CPU
            temperature=0.6,
            description="ScriptureMon Híbrido - Melhor dos dois mundos"
        ),

        "scripturemon-gpu-stable:latest": ModelConfig(
            name="scripturemon-gpu-stable:latest",
            size_gb=19,
            max_tokens=65536,   # 64K tokens!
            num_thread=10,
            num_batch=1024,
            num_keep=512,
            num_gpu=99,         # Full GPU
            temperature=0.6,
            description="ScriptureMon GPU - Velocidade máxima"
        ),

        # ========== MODELOS MÉDIOS (9-14GB) ==========
        "deepseek-r1:14b": ModelConfig(
            name="deepseek-r1:14b",
            size_gb=9,
            max_tokens=32768,   # 32K tokens
            num_thread=10,
            num_batch=512,
            num_keep=256,
            num_gpu=99,
            temperature=0.6,
            description="DeepSeek 14B - Equilíbrio perfeito"
        ),

        # ========== MODELOS MÉDIOS (4-8GB) ==========
        "llama3.1:8b": ModelConfig(
            name="llama3.1:8b",
            size_gb=4.9,
            max_tokens=32768,   # 32K tokens
            num_thread=8,
            num_batch=512,
            num_keep=256,
            num_gpu=99,
            temperature=0.7,
            description="Llama 3.1 - Análise versátil"
        ),

        "deepseek-r1:7b": ModelConfig(
            name="deepseek-r1:7b",
            size_gb=4.7,
            max_tokens=32768,   # 32K tokens
            num_thread=8,
            num_batch=512,
            num_keep=256,
            num_gpu=99,
            temperature=0.6,
            description="DeepSeek 7B - Raciocínio eficiente"
        ),

        "qwen2.5-coder:7b": ModelConfig(
            name="qwen2.5-coder:7b",
            size_gb=4.7,
            max_tokens=32768,   # 32K tokens
            num_thread=8,
            num_batch=512,
            num_keep=256,
            num_gpu=99,
            temperature=0.7,
            description="Qwen 2.5 - Análise de código e estrutura"
        ),

        "mistral:latest": ModelConfig(
            name="mistral:latest",
            size_gb=4.4,
            max_tokens=32768,   # 32K tokens
            num_thread=8,
            num_batch=512,
            num_keep=256,
            num_gpu=99,
            temperature=0.7,
            description="Mistral - Respostas criativas"
        ),

        "mistral:instruct": ModelConfig(
            name="mistral:instruct",
            size_gb=4.1,
            max_tokens=32768,   # 32K tokens
            num_thread=8,
            num_batch=512,
            num_keep=256,
            num_gpu=99,
            temperature=0.7,
            description="Mistral Instruct - Seguir instruções"
        ),

        "producermon:latest": ModelConfig(
            name="producermon:latest",
            size_gb=4.1,
            max_tokens=32768,   # 32K tokens
            num_thread=8,
            num_batch=512,
            num_keep=256,
            num_gpu=99,
            temperature=0.7,
            description="ProducerMon - Orquestrador inteligente"
        ),

        # ========== MODELOS PEQUENOS (2-4GB) ==========
        "llama2:latest": ModelConfig(
            name="llama2:latest",
            size_gb=3.8,
            max_tokens=16384,   # 16K tokens
            num_thread=6,
            num_batch=256,
            num_keep=128,
            num_gpu=99,
            temperature=0.7,
            description="Llama 2 - Clássico confiável"
        ),

        "llama3.2:3b": ModelConfig(
            name="llama3.2:3b",
            size_gb=2.0,
            max_tokens=65536,   # 64K tokens para modelo pequeno!
            num_thread=6,
            num_batch=1024,
            num_keep=512,
            num_gpu=99,
            temperature=0.7,
            description="Llama 3.2 - Pequeno mas poderoso"
        ),

        "llama3.2:latest": ModelConfig(
            name="llama3.2:latest",
            size_gb=2.0,
            max_tokens=65536,   # 64K tokens!
            num_thread=6,
            num_batch=1024,
            num_keep=512,
            num_gpu=99,
            temperature=0.7,
            description="Llama 3.2 Latest - Contexto massivo"
        ),

        "scripturemon-ptbr:latest": ModelConfig(
            name="scripturemon-ptbr:latest",
            size_gb=2.0,
            max_tokens=32768,   # 32K tokens
            num_thread=6,
            num_batch=512,
            num_keep=256,
            num_gpu=99,
            temperature=0.7,
            description="ScriptureMon PT-BR - Português brasileiro"
        ),
    }

    @classmethod
    def get_best_model_for_task(cls, task: str, prefer_large: bool = True) -> ModelConfig:
        """Retorna o melhor modelo para uma tarefa específica"""

        task_recommendations = {
            "deep_analysis": [
                "deepseek-r1:70b",          # MELHOR: 128K tokens!
                "scripturemon-ultimate:latest",
                "scripturemon-deepseek:latest",
                "deepseek-r1:32b"
            ],
            "screenplay_analysis": [
                "scripturemon-ultimate:latest",  # Especializado
                "scripturemon-deepseek:latest",
                "scripturemon-gpu-stable:latest",
                "deepseek-r1:32b"
            ],
            "quick_chat": [
                "llama3.2:3b",               # Rápido com 64K contexto!
                "llama3.2:latest",
                "mistral:latest",
                "producermon:latest"
            ],
            "reasoning": [
                "deepseek-r1:70b",           # Melhor raciocínio
                "deepseek-r1:32b",
                "deepseek-r1:14b",
                "deepseek-r1:7b"
            ],
            "code_analysis": [
                "qwen2.5-coder:7b",          # Especializado em código
                "deepseek-r1:14b",
                "mistral:instruct"
            ],
            "portuguese": [
                "scripturemon-ptbr:latest",   # PT-BR nativo
                "llama3.1:8b",
                "mistral:latest"
            ],
            "orchestration": [
                "producermon:latest",         # Orquestrador
                "scripturemon-hybrid:latest",
                "llama3.1:8b"
            ],
            "cpu_only": [
                "scripturemon-cpu:latest",    # CPU dedicado
                "scripturemon-hybrid:latest"
            ]
        }

        recommendations = task_recommendations.get(task, task_recommendations["quick_chat"])

        # Verifica RAM disponível
        ram = psutil.virtual_memory()
        available_gb = ram.available / (1024**3)

        for model_name in recommendations:
            if model_name in cls.COMPLETE_MODEL_CONFIGS:
                config = cls.COMPLETE_MODEL_CONFIGS[model_name]

                # Se preferir modelos grandes e tem RAM suficiente
                if prefer_large:
                    if config.size_gb < available_gb * 0.6:  # Usa até 60% da RAM disponível
                        return config
                else:
                    # Prefere modelos menores para velocidade
                    if config.size_gb < 10:
                        return config

        # Fallback
        return cls.COMPLETE_MODEL_CONFIGS["llama3.2:3b"]

    @classmethod
    def get_ollama_options(cls, model_name: str) -> Dict:
        """Retorna opções otimizadas para ollama.generate()"""

        if model_name in cls.COMPLETE_MODEL_CONFIGS:
            config = cls.COMPLETE_MODEL_CONFIGS[model_name]
        else:
            # Default para modelos não listados
            config = ModelConfig(
                name=model_name,
                size_gb=5,
                max_tokens=16384,
                num_thread=8,
                num_batch=512,
                num_keep=256,
                num_gpu=99,
                temperature=0.7
            )

        return {
            'num_ctx': config.max_tokens,
            'num_thread': config.num_thread,
            'num_batch': config.num_batch,
            'num_keep': config.num_keep,
            'num_gpu': config.num_gpu,
            'temperature': config.temperature,
            'repeat_penalty': 1.1,
            'top_p': 0.9,
            'top_k': 40,
            'mmap': True,
            'numa': False
        }

    @classmethod
    def print_complete_table(cls):
        """Imprime tabela completa de todos os modelos"""

        print("\n" + "="*100)
        print("🚀 CONFIGURAÇÃO COMPLETA - TODOS OS MODELOS OLLAMA")
        print("Mac Studio M3 Ultra - 96GB RAM - 28 cores")
        print("="*100)

        # Agrupa por tamanho
        gigantes = []
        grandes = []
        medios = []
        pequenos = []

        for name, config in cls.COMPLETE_MODEL_CONFIGS.items():
            if config.size_gb >= 40:
                gigantes.append(config)
            elif config.size_gb >= 15:
                grandes.append(config)
            elif config.size_gb >= 4:
                medios.append(config)
            else:
                pequenos.append(config)

        # Imprime cada grupo
        groups = [
            ("🔥 MODELOS GIGANTES (40GB+) - CONTEXTO MÁXIMO 128K", gigantes),
            ("💪 MODELOS GRANDES (15-40GB) - CONTEXTO 64K", grandes),
            ("⚡ MODELOS MÉDIOS (4-15GB) - CONTEXTO 32K", medios),
            ("🚀 MODELOS PEQUENOS (<4GB) - CONTEXTO 16-64K", pequenos)
        ]

        for title, models in groups:
            if models:
                print(f"\n{title}")
                print("-"*100)
                print(f"{'Modelo':<35} {'Size':<8} {'Tokens':<12} {'GPU':<6} {'Descrição':<40}")
                print("-"*100)

                for config in sorted(models, key=lambda x: x.max_tokens, reverse=True):
                    gpu_str = "Full" if config.num_gpu == 99 else ("CPU" if config.num_gpu == 0 else f"{config.num_gpu}L")
                    print(f"{config.name:<35} {config.size_gb:<6.1f}GB {config.max_tokens:<10,}  {gpu_str:<6} {config.description[:40]}")

        # RAM Summary
        ram = psutil.virtual_memory()
        print("\n" + "="*100)
        print(f"💾 RAM Status: {ram.available/(1024**3):.1f}GB disponível de {ram.total/(1024**3):.1f}GB")
        print("="*100)

    @classmethod
    def can_run_model(cls, model_name: str) -> tuple[bool, str]:
        """Verifica se pode rodar um modelo específico"""

        ram = psutil.virtual_memory()
        available_gb = ram.available / (1024**3)

        if model_name in cls.COMPLETE_MODEL_CONFIGS:
            config = cls.COMPLETE_MODEL_CONFIGS[model_name]
            required_gb = config.size_gb * 1.5  # Margem de segurança

            if available_gb >= required_gb:
                return True, f"✅ Pode rodar (precisa {config.size_gb}GB, tem {available_gb:.1f}GB)"
            else:
                return False, f"❌ RAM insuficiente (precisa {required_gb:.1f}GB, tem {available_gb:.1f}GB)"

        return False, "❓ Modelo não encontrado na configuração"

if __name__ == "__main__":
    config = OllamaCompleteConfig()

    # Mostra tabela completa
    config.print_complete_table()

    # Recomendações
    print("\n📊 MELHORES MODELOS POR TAREFA:")
    print("-"*50)

    tasks = [
        "deep_analysis",
        "screenplay_analysis",
        "quick_chat",
        "reasoning",
        "code_analysis",
        "portuguese",
        "cpu_only"
    ]

    for task in tasks:
        best = config.get_best_model_for_task(task, prefer_large=True)
        can_run, msg = config.can_run_model(best.name)
        status = "✅" if can_run else "⚠️"
        print(f"{status} {task:20} → {best.name:30} ({best.max_tokens:,} tokens)")

    print("\nDIGIMUNDO PRESENTE")