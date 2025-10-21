#!/usr/bin/env python3
"""Teste absolutamente mínimo do Ollama"""

import subprocess
import sys

print("=== TESTE MÍNIMO ABSOLUTO ===", flush=True)

# Teste 1: Ollama está instalado?
print("\n1. Verificando ollama instalado...", flush=True)
try:
    result = subprocess.run(["which", "ollama"], capture_output=True, text=True, timeout=5)
    print(f"   Ollama em: {result.stdout.strip()}", flush=True)
except Exception as e:
    print(f"   ERRO: {e}", flush=True)
    sys.exit(1)

# Teste 2: Ollama responde?
print("\n2. Testando ollama list...", flush=True)
try:
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
    lines = result.stdout.strip().split('\n')
    print(f"   {len(lines)-1} modelos encontrados", flush=True)
except Exception as e:
    print(f"   ERRO: {e}", flush=True)

# Teste 3: Modelo simples funciona?
print("\n3. Testando geração simples...", flush=True)
print("   Executando: ollama run llama2 'Say OK'", flush=True)
try:
    result = subprocess.run(
        ["ollama", "run", "llama2", "Say just OK"],
        capture_output=True,
        text=True,
        timeout=30
    )
    print(f"   Resposta: {result.stdout[:100]}", flush=True)
    if result.stderr:
        print(f"   Stderr: {result.stderr[:100]}", flush=True)
except subprocess.TimeoutExpired:
    print("   TIMEOUT após 30 segundos!", flush=True)
except Exception as e:
    print(f"   ERRO: {e}", flush=True)

print("\n=== FIM DO TESTE ===", flush=True)
print("DIGIMUNDO PRESENTE!", flush=True)