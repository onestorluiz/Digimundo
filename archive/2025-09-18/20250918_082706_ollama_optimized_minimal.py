#!/usr/bin/env python3
"""
ollama_optimized - Versão Minimalista
Configuração essencial apenas
"""

CONFIG = {
    'num_ctx': 16384,
    'num_thread': 8,
    'num_gpu': 999,
    'temperature': 0.7
}

def get_config():
    return CONFIG

if __name__ == "__main__":
    print("✅ Config:", get_config())
