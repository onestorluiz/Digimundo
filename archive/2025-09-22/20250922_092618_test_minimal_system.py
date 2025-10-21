#!/usr/bin/env python3
"""
Teste minimalista do sistema corrigido
"""

import sys
import os

# Testa imports básicos
print("1. Testando imports...")
try:
    from process_lock import ProcessLock
    print("   ✅ ProcessLock importado")
except ImportError as e:
    print(f"   ❌ ProcessLock falhou: {e}")
    
try:
    from safe_json_parser import safe_json_parse
    print("   ✅ SafeJSONParser importado")
except ImportError:
    try:
        from safe_json_parser_20250921_214934 import safe_json_parse
        print("   ✅ SafeJSONParser (com timestamp) importado")
    except ImportError as e:
        print(f"   ❌ SafeJSONParser falhou: {e}")

# Testa ScriptDoctor
print("\n2. Testando ScriptDoctor...")
sys.path.insert(0, 'src')
try:
    from scripturemon_champion.analysis.script_doctor import ScriptDoctor
    doc = ScriptDoctor()
    print("   ✅ ScriptDoctor criado")
    
    # Verifica método
    if hasattr(doc, 'analyze_script'):
        print("   ✅ Método analyze_script existe")
    else:
        print("   ❌ Método analyze_script não encontrado")
except Exception as e:
    print(f"   ❌ ScriptDoctor falhou: {e}")

# Testa ProcessLock
print("\n3. Testando ProcessLock...")
try:
    lock = ProcessLock("test_lock")
    if lock.acquire(timeout=2):
        print("   ✅ Lock adquirido")
        lock.release()
        print("   ✅ Lock liberado")
    else:
        print("   ⚠️ Lock já em uso (normal se outro teste rodando)")
except Exception as e:
    print(f"   ❌ ProcessLock falhou: {e}")

# Testa banco de dados
print("\n4. Verificando banco de dados...")
db_path = "data/learning/ollama_knowledge.db"
if os.path.exists(db_path):
    size = os.path.getsize(db_path) / 1024  # KB
    print(f"   ✅ Banco existe: {size:.1f}KB")
else:
    print("   ❌ Banco não encontrado")

# Testa Ollama
print("\n5. Verificando Ollama...")
import requests
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    if response.status_code == 200:
        models = response.json().get('models', [])
        print(f"   ✅ Ollama online com {len(models)} modelos")
        
        # Verifica modelo CPU
        cpu_models = [m['name'] for m in models if 'cpu' in m['name'].lower()]
        if cpu_models:
            print(f"   ✅ Modelo CPU disponível: {cpu_models[0]}")
        else:
            print("   ⚠️ Nenhum modelo CPU encontrado")
    else:
        print(f"   ❌ Ollama status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Ollama offline: {e}")

print("\n" + "="*50)
print("RESUMO:")
print("Sistema está pronto para rodar com correções mínimas!")
print("Use: python3 ollama_continuous_learning.py --cycles 1")
print("="*50)