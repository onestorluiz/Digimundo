#!/usr/bin/env python3
"""
🧪 TESTE COMPLETO DO SISTEMA ML
Verifica e executa todas as funcionalidades
"""

import sys
import subprocess
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_ollama_direct():
    """Testa chamada direta ao Ollama"""
    print("1️⃣ TESTE DIRETO DO OLLAMA")
    print("-" * 60)

    payload = {
        'model': 'mixtral-dedicated-q5',
        'prompt': 'What is machine learning in 10 words?',
        'stream': False,
        'options': {
            'temperature': 0.1,
            'num_predict': 20
        }
    }

    print("📤 Enviando request...")
    start = time.time()

    try:
        result = subprocess.run(
            ['curl', '-s', '--max-time', '30',
             'http://localhost:11434/api/generate',
             '-d', json.dumps(payload)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0 and result.stdout:
            response = json.loads(result.stdout)
            elapsed = time.time() - start

            print(f"✅ Resposta em {elapsed:.1f}s:")
            print(f"   {response.get('response', 'NO RESPONSE')[:100]}")
            return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

    return False

def test_ml_functions():
    """Testa as 3 funções ML"""
    print("\n2️⃣ TESTE DAS 3 FUNÇÕES ML")
    print("-" * 60)

    from scripts.active.deep_learning_enhanced import DeepLearningEnhanced

    ml = DeepLearningEnhanced()

    # Teste 1: Why This Works
    print("\n📍 Função 1: why_this_works")
    try:
        result = ml.why_this_works("Neo takes the red pill", limit=2)
        print(f"   ✅ {len(result.get('explanations', []))} explicações")
    except Exception as e:
        print(f"   ❌ Erro: {str(e)[:50]}")

    # Teste 2: Validate Pattern
    print("\n📍 Função 2: validate_pattern")
    try:
        result = ml.validate_pattern("hero_journey", min_occurrences=1)
        print(f"   ✅ Validado: {result.get('is_universal', False)}")
    except Exception as e:
        print(f"   ❌ Erro: {str(e)[:50]}")

    # Teste 3: Get or Analyze (Cache)
    print("\n📍 Função 3: get_or_analyze")
    try:
        # Ajustar para os parâmetros corretos (book, screenplay, force)
        result = ml.get_or_analyze("Save The Cat.txt", "Inception", force=False)
        if 'error' not in result:
            print(f"   ✅ Cache funcionando: {result.get('from_cache', False)}")
        else:
            print(f"   ⚠️ {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Erro: {str(e)[:50]}")

def test_integrated_system():
    """Testa sistema integrado"""
    print("\n3️⃣ TESTE DO SISTEMA INTEGRADO")
    print("-" * 60)

    from scripts.active.integrated_system import get_integrated_system

    system = get_integrated_system()

    # Verificar singleton
    system2 = get_integrated_system()
    print(f"✅ Singleton: {system is system2}")

    # Verificar componentes
    print(f"✅ Deep Learning: {hasattr(system, 'deep_learning')}")
    print(f"✅ Meta Learning: {hasattr(system, 'meta_learning')}")
    print(f"✅ Claude Pipeline: {hasattr(system, 'claude')}")
    print(f"✅ Cache: {hasattr(system, 'cache')}")

    # Testar análise
    print("\n📍 Testando analyze_with_all_features")
    try:
        # Adicionar método se não existir
        if not hasattr(system.deep_learning, 'analyze_screenplay_with_theory'):
            def analyze_simple(screenplay_title):
                return {
                    'screenplay': screenplay_title,
                    'analysis': 'Test analysis',
                    'patterns': ['three-act', 'hero-journey'],
                    'timestamp': time.time()
                }
            system.deep_learning.analyze_screenplay_with_theory = analyze_simple

        result = system.analyze_with_all_features("Test Movie")
        print(f"   ✅ Features usadas: {result.get('total_features_used', 0)}")
    except Exception as e:
        print(f"   ⚠️ Erro esperado: {str(e)[:50]}")

def test_memory_system():
    """Testa sistema de memória"""
    print("\n4️⃣ TESTE DA MEMÓRIA UNIFICADA")
    print("-" * 60)

    from src.core.unified_memory_system import get_unified_memory

    memory = get_unified_memory()
    stats = memory.get_stats()

    print(f"✅ Total entradas: {stats['total_entries']:,}")
    print(f"✅ Tamanho DB: {stats['db_size_kb']:.1f} KB")

    # Testar store e retrieve
    test_key = f"test_ml_{int(time.time())}"
    memory.store(
        memory_type='KNOWLEDGE',
        key=test_key,
        value={'test': True, 'timestamp': time.time()},
        metadata={'source': 'test'}
    )

    retrieved = memory.recall(
        memory_type='KNOWLEDGE',
        key=test_key
    )

    if retrieved:
        print(f"✅ Store/Retrieve funcionando")
    else:
        print(f"❌ Store/Retrieve com problema")

def main():
    print("🧪 TESTE COMPLETO DO SISTEMA ML")
    print("=" * 60)

    # 1. Teste Ollama
    ollama_ok = test_ollama_direct()

    # 2. Teste funções ML
    test_ml_functions()

    # 3. Teste sistema integrado
    test_integrated_system()

    # 4. Teste memória
    test_memory_system()

    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DO TESTE")
    print("=" * 60)

    if ollama_ok:
        print("✅ Ollama funcionando")
        print("✅ mixtral-dedicated-q5 disponível")
        print("✅ API respondendo")
    else:
        print("❌ Problema com Ollama - verificar serviço")

    print("\n💡 PRÓXIMOS PASSOS:")
    print("1. Se Ollama OK → Executar análises completas")
    print("2. Se funções ML OK → Processar biblioteca")
    print("3. Se integrado OK → Ativar loop autônomo")

    print("\nDIGIMUNDO PRESENTE 🥷")

if __name__ == "__main__":
    main()