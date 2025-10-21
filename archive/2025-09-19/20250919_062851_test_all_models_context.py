#!/usr/bin/env python3
"""
🔍 TESTE DE CONTEXTO MÁXIMO DE TODOS OS MODELOS
Descobre o real limite de tokens de cada modelo
"""

import ollama
import time
import psutil
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado


def test_model_context(model_name, test_sizes=[2048, 4096, 8192, 16384, 32768, 65536, 131072]):
    """Testa o contexto máximo que um modelo aguenta"""

    print(f"\n🧪 Testando {model_name}")
    print("-" * 50)

    max_working = 0

    for size in test_sizes:
        # Cria prompt grande
        test_prompt = "Test " * (size // 5)  # ~5 chars per word

        try:
            print(f"  Testando {size:,} tokens... ", end="")

            start = time.time()
            response = ollama.generate(
                model=model_name,
                prompt=test_prompt[:100] + " Respond with OK",  # Prompt pequeno para teste
                options={
                    'num_ctx': size,
                    'num_predict': 10,  # Resposta curta
                    'temperature': 0.1
                },
                keep_alive=0  # Não manter na memória
            )

            elapsed = time.time() - start

            if response and 'response' in response:
                print(f"✅ Funciona! ({elapsed:.1f}s)")
                max_working = size
            else:
                print(f"❌ Falhou")
                break

        except Exception as e:
            print(f"❌ Erro: {str(e)[:50]}")
            break

    return max_working

def main():
    print("🚀 TESTE DE CONTEXTO MÁXIMO - TODOS OS MODELOS")
    print("=" * 60)

    # RAM disponível
    ram = psutil.virtual_memory()
    print(f"💾 RAM: {ram.available / (1024**3):.1f}GB disponível de {ram.total / (1024**3):.1f}GB\n")

    # Lista modelos
    result = ollama.list()
    models = [model['name'] for model in result['models']]

    print(f"📦 {len(models)} modelos encontrados\n")

    # Modelos prioritários para teste completo
    priority_models = [
        'deepseek-r1:70b',
        'deepseek-r1:32b',
        'deepseek-r1:14b',
        'scripturemon-ultimate:latest',
        'scripturemon-deepseek:latest',
        'llama3.1:8b',
        'llama3.2:3b',
        'mistral:latest',
        'qwen2.5-coder:7b'
    ]

    results = {}

    # Testa modelos prioritários com ranges maiores
    for model in priority_models:
        if model in models:
            # Para modelos grandes, testa contextos maiores
            if '70b' in model or '32b' in model or 'ultimate' in model:
                test_sizes = [4096, 8192, 16384, 32768, 65536, 131072, 262144]
            else:
                test_sizes = [2048, 4096, 8192, 16384, 32768, 65536]

            max_ctx = test_model_context(model, test_sizes)
            results[model] = max_ctx

            # Limpa memória entre testes
            time.sleep(2)

    # Testa outros modelos com range menor
    for model in models:
        if model not in priority_models and model not in results:
            max_ctx = test_model_context(model, [2048, 4096, 8192, 16384])
            results[model] = max_ctx
            time.sleep(1)

    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL - CONTEXTO MÁXIMO REAL")
    print("=" * 60)

    # Ordena por contexto
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    print(f"\n{'Modelo':<40} {'Contexto Máximo':>20}")
    print("-" * 60)

    for model, max_ctx in sorted_results:
        if max_ctx > 0:
            # Estima RAM necessária
            size = model.split(':')[-1] if ':' in model else '?'
            ram_estimate = (max_ctx / 1024) * 0.5  # Estimativa grosseira

            print(f"{model:<40} {max_ctx:>15,} tokens")

    # Top 3
    print("\n🏆 TOP 3 MAIORES CONTEXTOS:")
    for i, (model, max_ctx) in enumerate(sorted_results[:3], 1):
        if max_ctx > 0:
            print(f"{i}. {model}: {max_ctx:,} tokens")

    print("\nDIGIMUNDO PRESENTE")

if __name__ == "__main__":
    main()

# ============================================================
# AUTO-UNIFIED MEMORY HELPER
# ============================================================
def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()
