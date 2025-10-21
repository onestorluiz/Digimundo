#!/usr/bin/env python3
"""Debug da inicialização linha por linha"""

import sys
sys.path.insert(0, 'src')

print("1. Imports básicos...", flush=True)
import json
import time
from datetime import datetime
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
import requests
import hashlib
import subprocess
import os
import re

print("2. Import ProcessLock...", flush=True)
from process_lock import ProcessLock

print("3. Import ScriptDoctor...", flush=True)
from scripturemon_champion.analysis.script_doctor import ScriptDoctor

print("4. Criando ScriptDoctor...", flush=True)
doctor = ScriptDoctor()
print("   ScriptDoctor criado!", flush=True)

print("\n5. Simulando __init__ do OllamaContinuousLearning...", flush=True)

model = "mixtral-cpu-force:latest"
timeout = 300

print(f"   5.1 Model: {model}", flush=True)
print(f"   5.2 Timeout: {timeout}", flush=True)

print("   5.3 Definindo endpoint...", flush=True)
ollama_endpoint = "http://127.0.0.1:11434/api/generate"

print("   5.4 Chamando cleanup_orphan_processes (simulado)...", flush=True)
# Simular cleanup
result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
ollama_processes = []
for line in result.stdout.split('\n'):
    if 'ollama' in line.lower() and 'grep' not in line:
        parts = line.split()
        if len(parts) > 1:
            ollama_processes.append(parts[1])
print(f"      Encontrados {len(ollama_processes)} processos Ollama", flush=True)

print("   5.5 Verificando Ollama com retry...", flush=True)
try:
    response = requests.get("http://127.0.0.1:11434/api/tags", timeout=10)
    print(f"      Status: {response.status_code}", flush=True)
except Exception as e:
    print(f"      Erro: {e}", flush=True)

print("   5.6 Verificando diretórios...", flush=True)
theory_dir = Path("theory")
masters_dir = Path("screenplays/masters")
print(f"      theory exists: {theory_dir.exists()}", flush=True)
print(f"      masters exists: {masters_dir.exists()}", flush=True)

print("\n=== DEBUG COMPLETO ===", flush=True)
print("Todos os passos executados sem travamento!", flush=True)
print("DIGIMUNDO PRESENTE!", flush=True)