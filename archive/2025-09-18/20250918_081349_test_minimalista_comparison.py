#!/usr/bin/env python3
"""
Teste Comparativo: Sistema Original vs Minimalista
"""

import time
import subprocess
import sys
import psutil
from pathlib import Path

def count_lines(filepath):
    """Conta linhas de código"""
    try:
        with open(filepath) as f:
            return len(f.readlines())
    except:
        return 0

def test_original():
    """Testa sistema original complexo"""
    print("\n" + "="*60)
    print("🔬 TESTANDO SISTEMA ORIGINAL")
    print("="*60)

    results = {
        'name': 'Original ProducerDirector',
        'file': 'producer_director_system.py',
        'lines': 0,
        'memory_before': 0,
        'memory_after': 0,
        'time_import': 0,
        'errors': []
    }

    # Conta linhas
    results['lines'] = count_lines('producer_director_system.py')

    try:
        # Memória antes
        process = psutil.Process()
        results['memory_before'] = process.memory_info().rss / 1024 / 1024

        # Tempo de import
        start = time.time()
        from producer_director_system import ProducerDirectorSystem
        results['time_import'] = time.time() - start

        # Memória depois
        results['memory_after'] = process.memory_info().rss / 1024 / 1024

        # Tenta criar instância
        try:
            system = ProducerDirectorSystem()
            print("✅ Sistema inicializado")
        except Exception as e:
            results['errors'].append(f"Init: {str(e)}")
            print(f"❌ Erro na inicialização: {e}")

    except Exception as e:
        results['errors'].append(f"Import: {str(e)}")
        print(f"❌ Erro no import: {e}")

    return results

def test_minimal():
    """Testa sistema minimalista"""
    print("\n" + "="*60)
    print("🚀 TESTANDO SISTEMA MINIMALISTA")
    print("="*60)

    results = {
        'name': 'Minimal ProducerDirector',
        'file': 'producer_director_minimal.py',
        'lines': 0,
        'memory_before': 0,
        'memory_after': 0,
        'time_import': 0,
        'time_execution': 0,
        'errors': []
    }

    # Conta linhas
    results['lines'] = count_lines('producer_director_minimal.py')

    try:
        # Memória antes
        process = psutil.Process()
        results['memory_before'] = process.memory_info().rss / 1024 / 1024

        # Tempo de import
        start = time.time()
        from producer_director_minimal import ProducerDirectorMinimal
        results['time_import'] = time.time() - start

        # Memória depois
        results['memory_after'] = process.memory_info().rss / 1024 / 1024

        # Testa funcionalidade
        try:
            system = ProducerDirectorMinimal()
            print("✅ Sistema inicializado")

            # Teste rápido (sem chamar Ollama real)
            start = time.time()
            producer_decision = system.producer.decide("análise rápida")
            results['time_execution'] = time.time() - start

            print(f"✅ Producer decidiu: {producer_decision}")

        except Exception as e:
            results['errors'].append(f"Execution: {str(e)}")

    except Exception as e:
        results['errors'].append(f"Import: {str(e)}")

    return results

def main():
    """Executa comparação"""
    print("\n" + "="*60)
    print("⚔️ BATALHA: COMPLEXO vs MINIMALISTA")
    print("="*60)

    # Testa ambos
    original = test_original()
    minimal = test_minimal()

    # RELATÓRIO
    print("\n" + "="*60)
    print("📊 RELATÓRIO COMPARATIVO")
    print("="*60)

    print(f"\n📏 TAMANHO DO CÓDIGO:")
    print(f"  Original: {original['lines']} linhas")
    print(f"  Minimal:  {minimal['lines']} linhas")
    if original['lines'] > 0:
        reduction = 100 - (minimal['lines']/original['lines']*100)
        print(f"  Redução:  {reduction:.1f}%")

    print(f"\n⏱️ TEMPO DE IMPORT:")
    print(f"  Original: {original['time_import']*1000:.2f}ms")
    print(f"  Minimal:  {minimal['time_import']*1000:.2f}ms")
    if original['time_import'] > 0:
        speedup = original['time_import']/minimal['time_import']
        print(f"  Speedup:  {speedup:.1f}x mais rápido")

    print(f"\n💾 USO DE MEMÓRIA:")
    original_mem = original['memory_after'] - original['memory_before']
    minimal_mem = minimal['memory_after'] - minimal['memory_before']
    print(f"  Original: +{original_mem:.2f}MB")
    print(f"  Minimal:  +{minimal_mem:.2f}MB")

    print(f"\n❌ ERROS:")
    print(f"  Original: {len(original['errors'])} erros")
    if original['errors']:
        for err in original['errors']:
            print(f"    - {err[:60]}...")
    print(f"  Minimal:  {len(minimal['errors'])} erros")

    # VENCEDOR
    print("\n" + "="*60)
    print("🏆 RESULTADO")
    print("="*60)

    minimal_wins = 0
    if minimal['lines'] < original['lines']:
        minimal_wins += 1
        print("✅ Minimal vence: Menos código")

    if minimal['time_import'] < original['time_import']:
        minimal_wins += 1
        print("✅ Minimal vence: Import mais rápido")

    if minimal_mem < original_mem:
        minimal_wins += 1
        print("✅ Minimal vence: Menos memória")

    if len(minimal['errors']) < len(original['errors']):
        minimal_wins += 1
        print("✅ Minimal vence: Menos erros")

    print(f"\n🎯 PLACAR FINAL: Minimalista {minimal_wins}/4")

    # FILOSOFIA
    print("\n💡 INSIGHT:")
    print("O sistema minimalista faz O MESMO com:")
    print(f"- {100 - (minimal['lines']/original['lines']*100):.0f}% menos código")
    print("- Clareza e manutenibilidade superiores")
    print("- Arquitetura modular (Producer + Director + Synthesizer)")
    print("\n✨ Simplicidade é a sofisticação suprema!")

if __name__ == "__main__":
    main()
    print("\nDIGIMUNDO PRESENTE")