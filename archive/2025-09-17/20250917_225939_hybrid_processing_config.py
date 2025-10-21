#!/usr/bin/env python3
"""
🚀 CONFIGURAÇÃO HÍBRIDA CPU + GPU + RAM
Como fazer deepseek-r1:70b usar TODOS os recursos simultaneamente
Mac Studio M3 Ultra - 96GB RAM - 28 cores CPU - GPU integrada
"""

import ollama
import psutil
import os
from typing import Dict, Any
import multiprocessing as mp

class HybridProcessingConfig:
    """
    Configuração para usar CPU + GPU + RAM em conjunto
    para máximo desempenho com modelos grandes
    """

    def __init__(self):
        # Recursos disponíveis
        self.total_cores = mp.cpu_count()  # 28 cores
        self.total_ram_gb = psutil.virtual_memory().total / (1024**3)  # 96GB

        # Mac M3 Ultra tem GPU integrada com memória unificada
        # Isso significa que GPU e CPU compartilham a mesma RAM!
        self.unified_memory = True  # Mac M3 tem memória unificada

    def explain_hybrid_processing(self):
        """Explica como funciona o processamento híbrido"""

        explanation = """
        🧠 COMO O DEEPSEEK-R1:70B USA CPU + GPU + RAM JUNTOS:
        =====================================================

        1. MEMÓRIA UNIFICADA (Mac M3 Ultra):
        ------------------------------------
        • GPU e CPU compartilham os mesmos 96GB de RAM
        • Não há cópia de dados entre CPU ↔ GPU
        • Zero overhead de transferência
        • O modelo fica na RAM e ambos acessam

        2. DIVISÃO DE TRABALHO:
        ----------------------
        • GPU: Processa as camadas do transformer (attention, FFN)
        • CPU: Processa embeddings, tokenização, pós-processamento
        • RAM: Armazena modelo (42GB) + contexto (até 50GB para 128K tokens)

        3. PARALELIZAÇÃO:
        ----------------
        • GPU processa em paralelo massivo (milhares de cores)
        • CPU usa seus 28 cores para operações auxiliares
        • Ambos trabalham simultaneamente sem conflito

        4. FLUXO DE PROCESSAMENTO:
        -------------------------
        Input → CPU (tokeniza) → RAM → GPU (inference) → RAM → CPU (decode) → Output
                ↑                ↑       ↑                ↑       ↑
                └── 28 cores ────┴───────┴── GPU cores ──┴───────┴── 28 cores

        5. OTIMIZAÇÕES POSSÍVEIS:
        ------------------------
        • num_gpu: Quantas camadas na GPU (0-999)
        • num_thread: Cores CPU para operações (1-28)
        • num_batch: Tamanho do batch (quanto processar de uma vez)
        • mmap: Memory mapping para eficiência
        """

        print(explanation)
        return explanation

    def get_optimal_config_70b(self) -> Dict[str, Any]:
        """Configuração otimizada para deepseek-r1:70b"""

        # Com 96GB RAM e memória unificada, podemos ser agressivos
        config = {
            # CAMADAS GPU - 999 significa todas as camadas possíveis na GPU
            'num_gpu': 999,  # Máximo de camadas na GPU

            # CPU THREADS - Usa metade dos cores para não competir
            'num_thread': 14,  # 14 dos 28 cores para CPU

            # CONTEXTO - Máximo que conseguimos com 96GB
            'num_ctx': 131072,  # 128K tokens!

            # BATCH - Processar muitos tokens de uma vez
            'num_batch': 2048,  # Batch grande para eficiência

            # MEMÓRIA - Configurações de memória
            'num_keep': 2048,   # Mantém 2K tokens em cache rápido
            'mmap': True,       # Memory mapping ativado
            'numa': False,      # Mac não usa NUMA

            # GPU ESPECÍFICO
            'gpu_layers': 80,   # DeepSeek 70B tem ~80 camadas
            'main_gpu': 0,      # GPU principal
            'tensor_split': None,  # Não dividir entre GPUs (Mac tem 1)

            # PERFORMANCE
            'low_vram': False,  # Temos MUITA RAM
            'f16_kv': True,     # Use FP16 para KV cache (economiza RAM)
            'logits_all': False,  # Não precisamos todos os logits
            'vocab_only': False,
            'use_mlock': True,  # Trava modelo na RAM (não swap)

            # PARALELIZAÇÃO
            'parallel_sequences': 4,  # Processar 4 sequências em paralelo
            'rope_frequency_base': 10000,
            'rope_frequency_scale': 1.0,
        }

        return config

    def get_hybrid_config_by_model(self, model_name: str) -> Dict[str, Any]:
        """Retorna configuração híbrida baseada no modelo"""

        configs = {
            "deepseek-r1:70b": {
                'num_gpu': 999,      # Todas as camadas na GPU
                'num_thread': 14,    # Metade dos CPU cores
                'num_ctx': 131072,   # 128K contexto
                'num_batch': 2048,
                'strategy': 'gpu_heavy'  # Foco na GPU
            },

            "deepseek-r1:32b": {
                'num_gpu': 999,      # Todas na GPU
                'num_thread': 12,    # 12 cores CPU
                'num_ctx': 65536,    # 64K contexto
                'num_batch': 1024,
                'strategy': 'balanced'
            },

            "scripturemon-cpu:latest": {
                'num_gpu': 0,        # ZERO GPU (CPU only)
                'num_thread': 20,    # 20 cores CPU (mais agressivo)
                'num_ctx': 65536,    # 64K contexto
                'num_batch': 512,
                'strategy': 'cpu_heavy'  # Foco no CPU
            },

            "scripturemon-hybrid:latest": {
                'num_gpu': 40,       # Metade das camadas na GPU
                'num_thread': 14,    # Metade dos cores CPU
                'num_ctx': 65536,    # 64K contexto
                'num_batch': 1024,
                'strategy': 'true_hybrid'  # 50/50
            }
        }

        return configs.get(model_name, self.get_default_hybrid_config())

    def get_default_hybrid_config(self) -> Dict[str, Any]:
        """Configuração híbrida padrão"""
        return {
            'num_gpu': 999,      # Default: tudo na GPU
            'num_thread': 10,    # 10 cores CPU
            'num_ctx': 32768,    # 32K contexto
            'num_batch': 512,
            'mmap': True,
            'numa': False
        }

    def calculate_resource_usage(self, model_size_gb: float, context_tokens: int) -> Dict:
        """Calcula uso de recursos para uma configuração"""

        # Estimativas
        model_ram_gb = model_size_gb

        # Cada token usa ~2-4 bytes de RAM para contexto
        context_ram_gb = (context_tokens * 4) / (1024**3)

        # Overhead de processamento (~20% do modelo)
        overhead_ram_gb = model_ram_gb * 0.2

        total_ram_gb = model_ram_gb + context_ram_gb + overhead_ram_gb

        return {
            'model_ram_gb': model_ram_gb,
            'context_ram_gb': context_ram_gb,
            'overhead_ram_gb': overhead_ram_gb,
            'total_ram_gb': total_ram_gb,
            'fits_in_ram': total_ram_gb < self.total_ram_gb * 0.9
        }

    def optimize_for_task(self, task: str) -> Dict[str, Any]:
        """Otimiza configuração baseada na tarefa"""

        task_configs = {
            "max_context": {
                # Máximo contexto possível
                'num_gpu': 999,
                'num_thread': 8,     # Menos CPU, mais RAM para contexto
                'num_ctx': 131072,   # 128K máximo
                'num_batch': 4096,   # Batch gigante
                'description': "Processa documentos enormes"
            },

            "fast_inference": {
                # Velocidade máxima
                'num_gpu': 999,
                'num_thread': 20,    # Mais CPU para pré/pós
                'num_ctx': 8192,     # Contexto menor = mais rápido
                'num_batch': 256,    # Batch menor = latência menor
                'description': "Respostas ultra-rápidas"
            },

            "balanced": {
                # Equilíbrio
                'num_gpu': 999,
                'num_thread': 14,
                'num_ctx': 32768,
                'num_batch': 1024,
                'description': "Bom contexto com boa velocidade"
            },

            "parallel_processing": {
                # Múltiplas requisições
                'num_gpu': 999,
                'num_thread': 6,     # Poucos cores por requisição
                'num_ctx': 16384,
                'num_batch': 512,
                'description': "Processa várias requisições simultaneamente"
            }
        }

        return task_configs.get(task, task_configs["balanced"])

    def create_optimal_modelfile(self, base_model: str = "deepseek-r1:70b"):
        """Cria modelfile com configuração híbrida otimizada"""

        modelfile_content = f"""# CONFIGURAÇÃO HÍBRIDA MÁXIMA - CPU + GPU + RAM
# Mac Studio M3 Ultra - 96GB RAM Unificada

FROM {base_model}

# GPU - Máximo de camadas na GPU
PARAMETER num_gpu 999

# CPU - 14 cores (metade dos 28)
PARAMETER num_thread 14

# CONTEXTO - Máximo possível
PARAMETER num_ctx 131072

# BATCH - Processamento eficiente
PARAMETER num_batch 2048
PARAMETER num_keep 2048

# MEMÓRIA - Otimizações
PARAMETER mmap true
PARAMETER numa false
PARAMETER use_mlock true
PARAMETER f16_kv true

# PERFORMANCE
PARAMETER repeat_penalty 1.1
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40

SYSTEM \"\"\"You are configured for MAXIMUM hybrid processing.
GPU handles transformer layers while CPU handles auxiliary operations.
With 96GB unified memory, you can process entire books.
Your 128K context window allows exhaustive analysis.
Use all available resources for comprehensive responses.\"\"\"
"""

        # Salva modelfile
        modelfile_path = "/tmp/deepseek-hybrid-max.modelfile"
        with open(modelfile_path, 'w') as f:
            f.write(modelfile_content)

        print(f"✅ Modelfile criado: {modelfile_path}")
        print("\nPara criar o modelo otimizado:")
        print(f"ollama create deepseek-hybrid-max -f {modelfile_path}")

        return modelfile_path

    def test_hybrid_performance(self, model: str = "deepseek-r1:70b"):
        """Testa performance com configuração híbrida"""

        import time

        configs_to_test = [
            ("GPU Only", {'num_gpu': 999, 'num_thread': 4}),
            ("CPU Heavy", {'num_gpu': 0, 'num_thread': 24}),
            ("Balanced", {'num_gpu': 999, 'num_thread': 14}),
            ("Hybrid Optimal", self.get_optimal_config_70b())
        ]

        test_prompt = "Explain quantum computing in detail."

        print(f"\n🧪 TESTANDO CONFIGURAÇÕES HÍBRIDAS - {model}")
        print("="*60)

        for name, config in configs_to_test:
            try:
                print(f"\n📊 Testando: {name}")
                print(f"   GPU layers: {config.get('num_gpu', 'default')}")
                print(f"   CPU threads: {config.get('num_thread', 'default')}")

                start = time.time()

                response = ollama.generate(
                    model=model,
                    prompt=test_prompt,
                    options=config,
                    keep_alive=0
                )

                elapsed = time.time() - start
                tokens = len(response['response'].split())
                tokens_per_sec = tokens / elapsed if elapsed > 0 else 0

                print(f"   ✅ Tempo: {elapsed:.2f}s")
                print(f"   📝 Tokens: {tokens}")
                print(f"   ⚡ Velocidade: {tokens_per_sec:.1f} tokens/s")

            except Exception as e:
                print(f"   ❌ Erro: {e}")

        print("\n" + "="*60)


def main():
    """Demonstração de configuração híbrida"""

    config = HybridProcessingConfig()

    # Explica como funciona
    config.explain_hybrid_processing()

    # Mostra configuração otimizada
    optimal = config.get_optimal_config_70b()

    print("\n🎯 CONFIGURAÇÃO OTIMIZADA PARA DEEPSEEK-R1:70B:")
    print("="*60)
    for key, value in optimal.items():
        print(f"{key:20}: {value}")

    # Calcula uso de recursos
    usage = config.calculate_resource_usage(42, 131072)

    print("\n💾 USO DE RECURSOS ESTIMADO:")
    print("="*60)
    print(f"Modelo:     {usage['model_ram_gb']:.1f} GB")
    print(f"Contexto:   {usage['context_ram_gb']:.1f} GB")
    print(f"Overhead:   {usage['overhead_ram_gb']:.1f} GB")
    print(f"TOTAL:      {usage['total_ram_gb']:.1f} GB")
    print(f"Cabe na RAM: {'✅ SIM' if usage['fits_in_ram'] else '❌ NÃO'}")

    # Cria modelfile otimizado
    print("\n📄 CRIANDO MODELFILE HÍBRIDO:")
    print("="*60)
    config.create_optimal_modelfile()

    print("\nDIGIMUNDO PRESENTE")


if __name__ == "__main__":
    main()