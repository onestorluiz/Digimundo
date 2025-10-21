#!/usr/bin/env python3
"""
⚡ TEST PERFORMANCE IMPROVEMENTS
Testa melhorias de performance da FASE C2
"""

import subprocess
import time
from pathlib import Path

def measure_startup_time():
    """Mede tempo de startup do sistema"""
    
    print("⚡ TESTANDO PERFORMANCE DE STARTUP")
    print("="*60)
    
    # Teste 1: Tempo de inicialização
    print("\n📊 Teste 1: Tempo de inicialização")
    print("-"*40)
    
    start = time.time()
    
    try:
        result = subprocess.run(
            ['echo', 'status', '|', './bin/scripturemon', '--timeout', '5'],
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            cwd='/Users/clubproducoes/Digimundo/scripturemon-validation'
        )
        
        init_time = time.time() - start
        
        print(f"  ⏱️ Tempo de inicialização: {init_time:.2f}s")
        
        if init_time < 3:
            print("  ✅ Inicialização RÁPIDA (< 3s)")
        elif init_time < 5:
            print("  ⚠️ Inicialização aceitável (3-5s)")
        else:
            print("  ❌ Inicialização lenta (> 5s)")
        
        # Contar sistemas carregados
        lazy_loaded = result.stdout.count("carregado sob demanda")
        parallel_loaded = result.stdout.count("inicializado em paralelo")
        
        print(f"  📦 Sistemas lazy loaded: {lazy_loaded}")
        print(f"  ⚡ Sistemas em paralelo: {parallel_loaded}")
        
    except subprocess.TimeoutExpired:
        print("  ❌ Timeout na inicialização")
    except Exception as e:
        print(f"  ❌ Erro: {e}")
    
    # Teste 2: Uso de memória
    print("\n📊 Teste 2: Uso de memória")
    print("-"*40)
    
    try:
        # Verificar memória antes
        result_before = subprocess.run(
            ['ps', '-o', 'rss=', '-p', str(subprocess.run(['pgrep', '-f', 'scripturemon'], 
            capture_output=True, text=True).stdout.strip())],
            capture_output=True,
            text=True
        )
        
        if result_before.stdout:
            mem_kb = int(result_before.stdout.strip())
            mem_mb = mem_kb / 1024
            print(f"  💾 Memória em uso: {mem_mb:.1f} MB")
            
            if mem_mb < 100:
                print("  ✅ Uso de memória BAIXO (< 100 MB)")
            elif mem_mb < 200:
                print("  ⚠️ Uso de memória moderado (100-200 MB)")
            else:
                print("  ❌ Uso de memória alto (> 200 MB)")
    except:
        print("  ⚠️ Não foi possível medir memória")
    
    # Teste 3: Resposta a comandos
    print("\n📊 Teste 3: Tempo de resposta")
    print("-"*40)
    
    commands = ['help', 'status', 'memory']
    
    for cmd in commands:
        start = time.time()
        try:
            result = subprocess.run(
                f'echo "{cmd}" | ./bin/scripturemon --timeout 3',
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
                cwd='/Users/clubproducoes/Digimundo/scripturemon-validation'
            )
            
            response_time = time.time() - start
            print(f"  {cmd}: {response_time:.2f}s")
            
        except:
            print(f"  {cmd}: ❌ Timeout")
    
    print("\n✅ Teste de performance completo!")

def test_lazy_loading():
    """Testa se lazy loading está funcionando"""
    
    print("\n🔄 TESTANDO LAZY LOADING")
    print("="*60)
    
    # Executar comando que não precisa de todos os sistemas
    print("\nExecutando comando simples (não deve carregar tudo)...")
    
    result = subprocess.run(
        'echo "help" | ./bin/scripturemon --timeout 3 -v',
        shell=True,
        capture_output=True,
        text=True,
        timeout=5,
        cwd='/Users/clubproducoes/Digimundo/scripturemon-validation'
    )
    
    # Verificar o que foi carregado
    lazy_systems = [
        'TELEPATHY',
        'MEMORY_COORDINATOR',
        'CINEMA_KNOWLEDGE',
        'QUANTUM_ENTANGLEMENT',
        'PARALLEL_PROCESSOR'
    ]
    
    for system in lazy_systems:
        if f"{system} carregado sob demanda" in result.stdout:
            print(f"  ⚠️ {system} foi carregado (não deveria)")
        else:
            print(f"  ✅ {system} não foi carregado (lazy)")
    
    print("\nExecutando comando complexo (deve carregar sistemas)...")
    
    result = subprocess.run(
        'echo "analisar roteiro complexo" | ./bin/scripturemon --timeout 5 -v',
        shell=True,
        capture_output=True,
        text=True,
        timeout=10,
        cwd='/Users/clubproducoes/Digimundo/scripturemon-validation'
    )
    
    loaded = 0
    for system in lazy_systems:
        if f"{system} carregado sob demanda" in result.stdout:
            print(f"  ✅ {system} carregado sob demanda")
            loaded += 1
    
    if loaded > 0:
        print(f"\n✅ Lazy loading funcionando! {loaded} sistemas carregados sob demanda")
    else:
        print("\n⚠️ Lazy loading pode não estar ativo")

if __name__ == "__main__":
    measure_startup_time()
    test_lazy_loading()
