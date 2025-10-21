#!/usr/bin/env python3
"""
BENCHMARK DE PERFORMANCE DO OLLAMA/MIXTRAL
Testa diferentes configurações e mede performance
"""

import subprocess
import time
import json
from typing import Dict, List

def run_ollama_test(model: str, num_ctx: int, prompt: str) -> Dict:
    """Executa teste com Ollama e mede performance"""

    print(f"\n🔍 Testando com {num_ctx//1024}K contexto...")

    start_time = time.time()

    # Comando Ollama
    cmd = [
        'ollama', 'run', model,
        '--verbose',
        '-o', f'num_ctx={num_ctx}',
        prompt
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        elapsed = time.time() - start_time

        # Extrair métricas do output (se disponível)
        output = result.stderr + result.stdout

        return {
            'context': num_ctx,
            'time': elapsed,
            'success': result.returncode == 0,
            'response_length': len(result.stdout)
        }

    except subprocess.TimeoutExpired:
        return {
            'context': num_ctx,
            'time': 30,
            'success': False,
            'error': 'timeout'
        }
    except Exception as e:
        return {
            'context': num_ctx,
            'time': 0,
            'success': False,
            'error': str(e)
        }

def main():
    print("📊 BENCHMARK OLLAMA/MIXTRAL PERFORMANCE")
    print("="*60)

    model = "mixtral:8x7b-instruct-v0.1-q5_K_M"

    # Prompt de teste
    test_prompt = """Analise rapidamente:
    FADE IN:
    INT. LAB - NIGHT
    Sarah trabalha. Aurora (V.O.) fala.
    FADE OUT.

    Identifique apenas: 1) Personagens 2) Local"""

    # Configurações para testar
    contexts = [8192, 16384, 32768, 65536, 131072]

    results = []

    for ctx in contexts:
        print(f"\n{'='*40}")
        print(f"Testando {ctx//1024}K tokens...")

        result = run_ollama_test(model, ctx, test_prompt)
        results.append(result)

        if result['success']:
            print(f"✅ Sucesso em {result['time']:.2f}s")
        else:
            print(f"❌ Falhou: {result.get('error', 'unknown')}")

    # Resumo
    print(f"\n{'='*60}")
    print("📈 RESUMO DOS TESTES:")
    print(f"{'Context':>10} | {'Tempo':>8} | {'Status':>10}")
    print("-"*35)

    for r in results:
        ctx_str = f"{r['context']//1024}K"
        time_str = f"{r['time']:.2f}s" if r['success'] else "N/A"
        status = "✅" if r['success'] else "❌"
        print(f"{ctx_str:>10} | {time_str:>8} | {status:>10}")

    # Salvar resultados
    with open('benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n💾 Resultados salvos em benchmark_results.json")

    # Recomendações
    print("\n💡 RECOMENDAÇÕES:")

    # Encontrar contexto ótimo
    successful = [r for r in results if r['success']]
    if successful:
        fastest = min(successful, key=lambda x: x['time'])
        print(f"   Contexto mais rápido: {fastest['context']//1024}K")

        largest = max(successful, key=lambda x: x['context'])
        print(f"   Maior contexto funcional: {largest['context']//1024}K")

    print("\n⚡ OTIMIZAÇÕES SUGERIDAS:")
    print("   1. Use num_ctx=32768 para velocidade")
    print("   2. Use num_ctx=131072 para análises completas")
    print("   3. Considere num_batch=512 para melhor throughput")
    print("   4. Mantenha num_thread=8 no Mac M3")

if __name__ == "__main__":
    main()