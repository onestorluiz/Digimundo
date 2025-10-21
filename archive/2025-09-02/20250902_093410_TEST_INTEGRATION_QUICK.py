#!/usr/bin/env python3
"""Teste rápido de integração - versão otimizada"""

import sys
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-validation')
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-validation/src')

from apps.scripturemon.memory_unification import UnifiedMemorySystem

print("\n🧪 TESTE RÁPIDO DE INTEGRAÇÃO 100%")
print("="*50)

tests = []

# Teste 1: Inicialização
try:
    unified = UnifiedMemorySystem()
    tests.append(("Inicialização", True))
    print("✅ Sistema inicializado")
except Exception as e:
    tests.append(("Inicialização", False))
    print(f"❌ Erro: {e}")
    sys.exit(1)

# Teste 2: Armazenamento
try:
    mem_id = unified.store_unified_memory("teste", "test", importance=0.8)
    tests.append(("Armazenamento", mem_id > 0))
    print(f"✅ Memória {mem_id} armazenada")
except:
    tests.append(("Armazenamento", False))

# Teste 3: Busca
try:
    results = unified.retrieve_unified_memory("teste", limit=5)
    tests.append(("Busca", len(results) > 0))
    print(f"✅ {len(results)} resultados encontrados")
except:
    tests.append(("Busca", False))

# Teste 4: Telepathy
try:
    if hasattr(unified.telepathy, 'broadcast_history'):
        tests.append(("Telepathy", True))
        print(f"✅ Telepathy com {len(unified.telepathy.broadcast_history)} broadcasts")
    else:
        tests.append(("Telepathy", False))
except:
    tests.append(("Telepathy", False))

# Teste 5: Status
try:
    status = unified.get_system_status()
    tests.append(("Status", 'unified_memories' in status))
    print(f"✅ Status: {status['unified_memories']} memórias unificadas")
except:
    tests.append(("Status", False))

# Shutdown
unified.running = False

# Resultado
passed = sum(1 for _, result in tests if result)
total = len(tests)
rate = (passed/total * 100) if total > 0 else 0

print(f"\n📊 RESULTADO: {passed}/{total} testes passaram")
print(f"📈 Taxa de sucesso: {rate:.0f}%")

if rate == 100:
    print("🎉 SISTEMA 100% INTEGRADO!")
elif rate >= 80:
    print("✅ Sistema funcional")
else:
    print("⚠️ Necessita ajustes")

print("\n62/100. Teste completo.")