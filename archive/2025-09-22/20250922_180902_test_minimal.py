#!/usr/bin/env python3
"""Teste mínimo do sistema Scripturemon-Ultimate"""

import requests
import sqlite3
from pathlib import Path
import sys

print("=== TESTE MÍNIMO DO SISTEMA ===\n")

# Teste 1: Ollama
print("1. Verificando Ollama...")
try:
    r = requests.get("http://127.0.0.1:11434/", timeout=5)
    if r.status_code == 200:
        print("✅ Ollama rodando")
    else:
        print(f"❌ Ollama retornou status {r.status_code}")
except Exception as e:
    print(f"❌ Ollama não acessível: {e}")

# Teste 2: Banco de dados
print("\n2. Verificando banco de dados...")
db_path = Path("data/learning/ollama_knowledge.db")
if db_path.exists():
    try:
        conn = sqlite3.connect(db_path)
        count = conn.execute("SELECT COUNT(*) FROM insights").fetchone()[0]
        avg_conf = conn.execute("SELECT AVG(confidence) FROM insights").fetchone()[0]
        print(f"✅ Banco OK: {count} insights (confidence média: {avg_conf:.2f})")
        conn.close()
    except Exception as e:
        print(f"❌ Erro ao acessar banco: {e}")
else:
    print("❌ Banco não existe")

# Teste 3: ProcessLock
print("\n3. Verificando ProcessLock...")
try:
    from process_lock import ProcessLock
    lock = ProcessLock("test")
    if lock.acquire(timeout=1):
        print("✅ ProcessLock funcionando")
        lock.release()
    else:
        print("❌ ProcessLock não conseguiu adquirir lock")
except ImportError:
    print("❌ ProcessLock não encontrado")
except Exception as e:
    print(f"❌ ProcessLock falhou: {e}")

# Teste 4: Verificar arquivos críticos
print("\n4. Verificando arquivos críticos...")
critical_files = [
    "ollama_continuous_learning.py",
    "process_lock.py",
    "data/learning/theory_of_mind.md"
]
for file in critical_files:
    if Path(file).exists():
        print(f"✅ {file} existe")
    else:
        print(f"❌ {file} não encontrado")

# Teste 5: Modelos Ollama disponíveis
print("\n5. Verificando modelos Ollama...")
try:
    import subprocess
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
        timeout=10
    )
    if "mixtral" in result.stdout:
        print("✅ Modelo Mixtral disponível")
        # Contar quantos modelos Mixtral temos
        mixtral_count = result.stdout.count("mixtral")
        print(f"   {mixtral_count} variantes de Mixtral encontradas")
    else:
        print("❌ Modelo Mixtral não encontrado")
except Exception as e:
    print(f"❌ Erro ao listar modelos: {e}")

print("\n=== RESUMO ===")
print("Sistema pronto para execução se todos os testes passaram.")
print("Execute: python3 ollama_continuous_learning.py --cycles 1")