#!/usr/bin/env python3
"""
Teste do SoulOS Wrapper - Verifica que SoulOS está seguro e controlado.
"""

import sys
import time
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.soulos_wrapper import SoulOSWrapper, SAFE_SOULOS_CONFIG


def test_disabled_by_default():
    """Testa que SoulOS está desabilitado por padrão."""
    print("\n1. TESTANDO SOULOS DESABILITADO POR PADRÃO")
    print("-" * 40)
    
    # Usar config segura
    wrapper = SoulOSWrapper(SAFE_SOULOS_CONFIG)
    
    assert not wrapper.enabled, "SoulOS deve estar desabilitado por padrão"
    assert not wrapper.code_execution, "Code execution deve estar desabilitado"
    assert not wrapper.is_available(), "SoulOS não deve estar disponível"
    
    print("✅ SoulOS está desabilitado por padrão")
    print(f"  - enabled: {wrapper.enabled}")
    print(f"  - code_execution: {wrapper.code_execution}")
    print(f"  - available: {wrapper.is_available()}")
    
    return True


def test_safe_process_response():
    """Testa processamento seguro de resposta."""
    print("\n2. TESTANDO PROCESSAMENTO SEGURO")
    print("-" * 40)
    
    wrapper = SoulOSWrapper(SAFE_SOULOS_CONFIG)
    
    # Resposta com syscall potencial
    response = "Análise completa. [MEMO.SAVE] {content: 'teste'}"
    
    # Deve retornar resposta original (SoulOS desabilitado)
    processed = wrapper.process_response(response)
    
    assert processed == response, "Deve retornar resposta original quando desabilitado"
    
    print("✅ Resposta não processada (SoulOS desabilitado)")
    print(f"  - Original: {response[:50]}...")
    print(f"  - Processada: {processed[:50]}...")
    
    return True


def test_timeout_protection():
    """Testa proteção de timeout."""
    print("\n3. TESTANDO PROTEÇÃO DE TIMEOUT")
    print("-" * 40)
    
    wrapper = SoulOSWrapper(SAFE_SOULOS_CONFIG)
    
    # Função que demora muito
    def slow_function():
        time.sleep(10)
        return "não deve chegar aqui"
    
    # Executar com timeout de 1 segundo
    start = time.time()
    result = wrapper.execute_with_timeout(slow_function, timeout=1.0)
    elapsed = time.time() - start
    
    assert result is None, "Deve retornar None em timeout"
    assert elapsed < 2.0, "Deve respeitar timeout"
    
    print(f"✅ Timeout funcionando ({elapsed:.2f}s)")
    print(f"  - Resultado: {result}")
    print(f"  - Tempo limite: 1.0s")
    
    return True


def test_error_handling():
    """Testa tratamento de erros."""
    print("\n4. TESTANDO TRATAMENTO DE ERROS")
    print("-" * 40)
    
    wrapper = SoulOSWrapper(SAFE_SOULOS_CONFIG)
    
    # Função que gera erro
    def error_function():
        raise ValueError("Erro intencional")
    
    # Executar com proteção
    result = wrapper.execute_with_timeout(error_function)
    
    assert result is None, "Deve retornar None em erro"
    
    print("✅ Erros tratados corretamente")
    print(f"  - Resultado: {result}")
    
    return True


def test_stats():
    """Testa estatísticas do wrapper."""
    print("\n5. TESTANDO ESTATÍSTICAS")
    print("-" * 40)
    
    wrapper = SoulOSWrapper(SAFE_SOULOS_CONFIG)
    
    stats = wrapper.get_stats()
    
    assert 'enabled' in stats
    assert 'code_execution' in stats
    assert 'available' in stats
    assert 'timeout' in stats
    
    print("✅ Estatísticas disponíveis:")
    for key, value in stats.items():
        print(f"  - {key}: {value}")
    
    return True


def main():
    """Executa todos os testes."""
    print("=" * 60)
    print("TESTE DO SOULOS WRAPPER")
    print("=" * 60)
    
    tests = [
        test_disabled_by_default,
        test_safe_process_response,
        test_timeout_protection,
        test_error_handling,
        test_stats
    ]
    
    results = []
    for test in tests:
        try:
            passed = test()
            results.append((test.__name__, passed))
        except Exception as e:
            print(f"❌ Erro no teste {test.__name__}: {e}")
            results.append((test.__name__, False))
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    
    passed = sum(1 for _, p in results if p)
    total = len(results)
    
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"{status} {name}")
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 SOULOS ESTÁ SEGURO E CONTROLADO!")
    else:
        print("\n⚠️ Alguns testes falharam")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    exit(main())