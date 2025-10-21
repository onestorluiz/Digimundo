#!/usr/bin/env python3
"""Rastreamento detalhado do travamento"""

import sys
import time
import requests

print("=== RASTREAMENTO DETALHADO ===\n", flush=True)

# 1. Teste de imports
print("1. Importando sys.path...", flush=True)
sys.path.insert(0, 'src')

print("2. Importando ProcessLock...", flush=True)
from process_lock import ProcessLock

print("3. Testando ProcessLock isolado...", flush=True)
lock = ProcessLock("test_trace")
print("   3.1 Tentando adquirir lock...", flush=True)
if lock.acquire(timeout=2):
    print("   3.2 Lock adquirido!", flush=True)
    lock.release()
    print("   3.3 Lock liberado!", flush=True)
else:
    print("   3.2 FALHOU ao adquirir lock!", flush=True)

print("\n4. Testando Ollama API...", flush=True)
try:
    print("   4.1 Fazendo request para http://127.0.0.1:11434/api/tags...", flush=True)
    response = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
    print(f"   4.2 Status: {response.status_code}", flush=True)
    if response.status_code == 200:
        models = response.json().get("models", [])
        print(f"   4.3 Modelos encontrados: {len(models)}", flush=True)
        for m in models[:3]:
            print(f"      - {m.get('name')}", flush=True)
except Exception as e:
    print(f"   4.2 ERRO: {e}", flush=True)

print("\n5. Importando ScriptDoctor...", flush=True)
from scripturemon_champion.analysis.script_doctor import ScriptDoctor
print("   5.1 ScriptDoctor importado!", flush=True)

print("\n6. Criando instância ScriptDoctor...", flush=True)
doctor = ScriptDoctor()
print("   6.1 ScriptDoctor criado!", flush=True)

print("\n7. Simulando inicialização OllamaContinuousLearning...", flush=True)

print("   7.1 Criando lock 'ollama_learning'...", flush=True)
main_lock = ProcessLock("ollama_learning")

print("   7.2 Tentando adquirir lock (timeout=5)...", flush=True)
if not main_lock.acquire(timeout=5):
    print("   7.3 ⚠️ Lock não adquirido - outra instância rodando?", flush=True)
    # Verificar se há processo travado
    import subprocess
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'ollama_continuous' in line and 'grep' not in line:
            print(f"   7.4 Processo encontrado: {line[:100]}", flush=True)
else:
    print("   7.3 ✅ Lock adquirido com sucesso!", flush=True)
    main_lock.release()
    print("   7.4 Lock liberado!", flush=True)

print("\n=== RASTREAMENTO COMPLETO ===", flush=True)
print("DIGIMUNDO PRESENTE!", flush=True)