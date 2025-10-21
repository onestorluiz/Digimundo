#!/usr/bin/env python3
"""Testes básicos de import"""
import sys
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-Omega')


def test_bm25_import():
    """Testa import do BM25"""
    try:
        from scripturemon.retrieval.bm25 import BM25
        return True
    except ImportError:
        return False


def test_cache_import():
    """Testa import do Cache"""
    try:
        from scripturemon.core.cache import Cache
        return True
    except ImportError:
        return False


def test_utils_import():
    """Testa import dos utils"""
    try:
        from scripturemon.utils import json_repair, run_id
        return True
    except ImportError:
        return False


def run_all_tests():
    """Executa todos os testes"""
    tests = [
        ("BM25 Import", test_bm25_import),
        ("Cache Import", test_cache_import),
        ("Utils Import", test_utils_import)
    ]

    passed = 0
    failed = 0

    print("\n🧪 Executando testes básicos...")

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"   ✅ {test_name}: PASSOU")
                passed += 1
            else:
                print(f"   ❌ {test_name}: FALHOU")
                failed += 1
        except Exception as e:
            print(f"   💥 {test_name}: ERRO - {e}")
            failed += 1

    print(f"\n📊 Resultados: {passed} passou, {failed} falhou")
    return passed, failed


if __name__ == "__main__":
    passed, failed = run_all_tests()
    sys.exit(0 if failed == 0 else 1)
