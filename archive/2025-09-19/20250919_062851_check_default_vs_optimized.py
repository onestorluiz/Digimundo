#!/usr/bin/env python3
"""
🔍 VERIFICA CONFIGURAÇÃO PADRÃO vs OTIMIZADA
Mostra o que vem por default e o que precisamos configurar
"""

import ollama
import json
import time
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado


def test_model_config(model_name: str, custom_options: dict = None):
    """Testa configuração de um modelo"""

    print(f"\n{'='*60}")
    print(f"📊 TESTANDO: {model_name}")
    print('='*60)

    # Prompt simples para teste
    test_prompt = "Respond with just 'OK' to confirm you're working"

    tests = [
        ("PADRÃO (sem configuração)", {}),
        ("OTIMIZADO (configurado)", custom_options or {})
    ]

    for test_name, options in tests:
        print(f"\n🧪 {test_name}:")
        print("-"*40)

        if options:
            print("Configurações aplicadas:")
            for k, v in options.items():
                print(f"  • {k}: {v}")
        else:
            print("  Usando defaults do Ollama")

        try:
            start = time.time()

            # Faz chamada
            response = ollama.generate(
                model=model_name,
                prompt=test_prompt,
                options=options if options else {},
                keep_alive="1m"  # Mantém na memória por 1 min
            )

            elapsed = time.time() - start

            # Analisa resposta
            if response:
                print(f"\n  ✅ Funcionou!")
                print(f"  ⏱️  Tempo: {elapsed:.2f}s")

                # Tenta pegar info de contexto se disponível
                if 'context' in response:
                    print(f"  📝 Contexto usado: {len(response.get('context', []))} tokens")

                if 'eval_count' in response:
                    print(f"  🔢 Tokens gerados: {response['eval_count']}")

                if 'eval_duration' in response:
                    eval_time = response['eval_duration'] / 1e9  # nano to seconds
                    if eval_time > 0:
                        tokens_per_sec = response.get('eval_count', 0) / eval_time
                        print(f"  ⚡ Velocidade: {tokens_per_sec:.1f} tokens/s")

        except Exception as e:
            print(f"  ❌ Erro: {str(e)[:100]}")

def main():
    print("🚀 ANÁLISE: CONFIGURAÇÃO PADRÃO vs OTIMIZADA")
    print("Mac Studio M3 Ultra - 96GB RAM - 28 cores")

    # Configurações otimizadas para diferentes modelos
    optimized_configs = {
        "deepseek-r1:70b": {
            'num_gpu': 999,      # Todas camadas na GPU
            'num_thread': 14,    # 14 cores CPU
            'num_ctx': 131072,   # 128K contexto
            'num_batch': 2048,   # Batch grande
            'num_keep': 2048,
            'mmap': True,
            'numa': False,
            'temperature': 0.7
        },

        "deepseek-r1:32b": {
            'num_gpu': 999,
            'num_thread': 12,
            'num_ctx': 65536,    # 64K contexto
            'num_batch': 1024,
            'num_keep': 1024,
            'mmap': True,
            'temperature': 0.7
        },

        "llama3.2:3b": {
            'num_gpu': 999,
            'num_thread': 8,
            'num_ctx': 65536,    # 64K mesmo sendo pequeno!
            'num_batch': 1024,
            'num_keep': 512,
            'temperature': 0.7
        }
    }

    # Lista modelos disponíveis
    try:
        models_response = ollama.list()
        available_models = [m['name'] for m in models_response['models']]
        print(f"\n📦 {len(available_models)} modelos encontrados")
    except:
        available_models = []
        print("\n⚠️  Não consegui listar modelos")

    # Testa modelos prioritários
    priority_models = ["deepseek-r1:70b", "deepseek-r1:32b", "llama3.2:3b"]

    for model in priority_models:
        if model in available_models:
            config = optimized_configs.get(model, {})
            test_model_config(model, config)
        else:
            print(f"\n⚠️  {model} não está instalado")

    # EXPLICAÇÃO IMPORTANTE
    print("\n" + "="*60)
    print("📚 EXPLICAÇÃO: PADRÃO vs CONFIGURADO")
    print("="*60)

    explanation = """
🔴 CONFIGURAÇÃO PADRÃO (Ollama defaults):
------------------------------------------
• num_ctx: 2048 tokens (muito pouco!)
• num_thread: 4-8 cores (subutiliza CPU)
• num_gpu: automático (geralmente OK)
• num_batch: 512 (poderia ser maior)
• mmap: false (menos eficiente)

🟢 CONFIGURAÇÃO OTIMIZADA (nossa):
-----------------------------------
• num_ctx: 131,072 tokens (64x mais!)
• num_thread: 14 cores (usa metade do CPU)
• num_gpu: 999 (força tudo na GPU)
• num_batch: 2048 (4x maior)
• mmap: true (memory mapping eficiente)

💡 RESUMO:
---------
SIM, precisamos configurar! O Ollama por padrão:
- Usa contexto MUITO pequeno (2K vs 128K possível)
- Subutiliza CPU (4 cores vs 14 possível)
- Não otimiza batch size
- Não usa memory mapping

Para usar TODO o potencial, SEMPRE passe options:
```python
ollama.generate(
    model="deepseek-r1:70b",
    prompt=prompt,
    options={
        'num_ctx': 131072,    # <-- ESSENCIAL!
        'num_thread': 14,      # <-- IMPORTANTE!
        'num_batch': 2048,     # <-- MELHORA VELOCIDADE!
        'mmap': True          # <-- EFICIÊNCIA!
    }
)
```
"""

    print(explanation)
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
