#!/usr/bin/env python3
"""
Análise de uso de tokens nos especialistas Scripturemon
"""

import json
import subprocess
import re
from pathlib import Path


def estimate_tokens_tiktoken_style(text):
    """
    Estimativa mais precisa de tokens baseada em padrões de tokenização.
    Para português: ~1.3-1.5 tokens por palavra
    """
    words = len(text.split())
    chars = len(text)

    # Estimativas baseadas em diferentes métodos
    by_words = int(words * 1.35)  # Método conservador
    by_chars = int(chars / 3.5)   # ~3.5 chars por token em português

    # Usar média dos dois métodos
    estimated = (by_words + by_chars) // 2

    return {
        'words': words,
        'chars': chars,
        'tokens_by_words': by_words,
        'tokens_by_chars': by_chars,
        'tokens_estimated': estimated
    }


def analyze_specialist_results():
    """Analisa resultados de todos especialistas graduados"""

    specialists = [
        {
            'file': 'test_all_specialists_v4_results.json',
            'names': ['DrDialogue', 'DrPsychemon', 'DrSubmon']
        },
        {
            'file': 'test_theme_specialist_v4_results.json',
            'name': 'DrThememon'
        }
    ]

    print('='*80)
    print('📊 ANÁLISE DETALHADA DE TOKENS - ESPECIALISTAS SCRIPTUREMON')
    print('='*80)
    print()

    all_results = []

    # Processar primeiro arquivo (3 especialistas)
    try:
        with open('test_all_specialists_v4_results.json', 'r') as f:
            data = json.load(f)

        for specialist_data in data['specialists_tested']:
            name = specialist_data['specialist'].split('(')[0].strip()
            insights = specialist_data['insights']
            elapsed = specialist_data['elapsed']

            tokens = estimate_tokens_tiktoken_style(insights)

            all_results.append({
                'name': name,
                'elapsed': elapsed,
                **tokens
            })

    except Exception as e:
        print(f'Erro ao processar v4_results: {e}')

    # Processar DrThememon
    try:
        with open('test_theme_specialist_v4_results.json', 'r') as f:
            data = json.load(f)

        insights = data['insights']
        elapsed = data['elapsed']
        tokens = estimate_tokens_tiktoken_style(insights)

        all_results.append({
            'name': 'DrThememon',
            'elapsed': elapsed,
            **tokens
        })

    except Exception as e:
        print(f'Erro ao processar theme: {e}')

    # Exibir resultados
    print(f"{'ESPECIALISTA':<20} {'TEMPO':>10} {'PALAVRAS':>10} {'CHARS':>10} {'TOKENS':>10}")
    print('-'*80)

    total_tokens = 0
    total_time = 0

    for r in all_results:
        print(f"{r['name']:<20} {r['elapsed']:>9.1f}s {r['words']:>10,} {r['chars']:>10,} {r['tokens_estimated']:>10,}")
        total_tokens += r['tokens_estimated']
        total_time += r['elapsed']

    print('-'*80)
    avg_tokens = total_tokens // len(all_results)
    avg_time = total_time / len(all_results)

    print(f"{'MÉDIA':<20} {avg_time:>9.1f}s {'-':>10} {'-':>10} {avg_tokens:>10,}")
    print(f"{'TOTAL (4 specs)':<20} {total_time:>9.1f}s {'-':>10} {'-':>10} {total_tokens:>10,}")

    print()
    print('='*80)
    print('📈 ANÁLISE DE EFICIÊNCIA')
    print('='*80)
    print()

    # Calcular tokens por segundo
    for r in all_results:
        tokens_per_sec = r['tokens_estimated'] / r['elapsed']
        print(f"{r['name']:<20} {tokens_per_sec:>6.1f} tokens/segundo")

    avg_tokens_per_sec = total_tokens / total_time
    print('-'*80)
    print(f"{'MÉDIA':<20} {avg_tokens_per_sec:>6.1f} tokens/segundo")

    print()
    print('='*80)
    print('🎯 COMPARAÇÃO COM LIMITES DO MODELO')
    print('='*80)
    print()

    # Configuração do modelo
    max_context = 131072  # num_ctx
    max_predict = 3000    # num_predict

    print(f"Modelo: scripturemon-ultimate:latest (Mistral 8x7b)")
    print(f"  Contexto máximo (num_ctx):    {max_context:,} tokens")
    print(f"  Predição máxima (num_predict): {max_predict:,} tokens")
    print()

    print(f"Uso atual:")
    print(f"  Média de output: {avg_tokens:,} tokens")
    print(f"  Uso do limite:   {(avg_tokens/max_predict)*100:.1f}% de num_predict")
    print()

    # Calcular input estimado (livro + roteiro + prompt)
    book_words = 77627
    screenplay_words = 5000
    prompt_words = 500  # estimativa

    total_input_words = book_words + screenplay_words + prompt_words
    estimated_input_tokens = int(total_input_words * 1.35)

    print(f"Estimativa de tokens de INPUT:")
    print(f"  Livro completo:   ~{int(book_words * 1.35):,} tokens")
    print(f"  Roteiro (5k pal): ~{int(screenplay_words * 1.35):,} tokens")
    print(f"  Prompt:           ~{int(prompt_words * 1.35):,} tokens")
    print(f"  TOTAL INPUT:      ~{estimated_input_tokens:,} tokens")
    print(f"  Uso do contexto:  {(estimated_input_tokens/max_context)*100:.1f}% de num_ctx")
    print()

    print(f"Total de tokens por análise completa:")
    print(f"  Input:  ~{estimated_input_tokens:,} tokens")
    print(f"  Output: ~{avg_tokens:,} tokens")
    print(f"  TOTAL:  ~{estimated_input_tokens + avg_tokens:,} tokens por especialista")
    print()

    print('='*80)
    print('💰 CUSTO ESTIMADO (se fosse API paga)')
    print('='*80)
    print()

    # Preços fictícios para comparação (baseados em APIs típicas)
    # GPT-4 Turbo 128k: $0.01/1k input, $0.03/1k output
    # Claude 3 Opus: $0.015/1k input, $0.075/1k output

    input_k = estimated_input_tokens / 1000
    output_k = avg_tokens / 1000

    print("Se usássemos APIs pagas (exemplo GPT-4 Turbo 128k):")
    print(f"  Input:  {input_k:.1f}k tokens × $0.01 = ${input_k * 0.01:.3f}")
    print(f"  Output: {output_k:.1f}k tokens × $0.03 = ${output_k * 0.03:.3f}")
    print(f"  TOTAL por análise: ${(input_k * 0.01) + (output_k * 0.03):.3f}")
    print()
    print(f"  Para 24 especialistas: ${24 * ((input_k * 0.01) + (output_k * 0.03)):.2f}")
    print()
    print("💚 Com Ollama (local): $0.00 (GRATUITO!)")
    print()

    print('='*80)
    print('🚀 PROJEÇÃO PARA 24 ESPECIALISTAS')
    print('='*80)
    print()

    print(f"Com base nos 4 especialistas graduados:")
    print(f"  Tokens médios por especialista: ~{avg_tokens:,}")
    print(f"  Tempo médio por especialista: {avg_time:.1f}s")
    print()
    print(f"Para completar os 24 especialistas:")
    print(f"  Tokens totais (output): ~{avg_tokens * 24:,} tokens")
    print(f"  Tempo total estimado: {(avg_time * 24)/60:.1f} minutos")
    print(f"  Tempo por roteiro completo: ~{(avg_time * 24)/60:.1f}min")
    print()

    return all_results


if __name__ == "__main__":
    analyze_specialist_results()
